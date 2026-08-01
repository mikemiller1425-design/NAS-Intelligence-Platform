#!/usr/bin/env python3
"""Validate classification rule sets against the canonical contract.

Canonical schema: config/schemas/classification-rule-set.schema.json

Two layers of checking run here:

  1. JSON Schema (draft 2020-12) — structure, vocabularies, unknown-field
     rejection, and the conditional safety rules (notably: a provisional rule is
     structurally incapable of an automatically approved or executable outcome).

  2. Loader checks — constraints JSON Schema cannot express, such as uniqueness
     of rule identifiers across an array and cross-file reference resolution.
     Each has a stable VAL-* identifier so failures are citable.

Usage:
    python3 scripts/validate_rule_config.py              # validate everything
    python3 scripts/validate_rule_config.py FILE...      # validate specific files

Exit code 0 means every positive example validated and every negative example
was rejected. This script reads files only; it performs no NAS access and
mutates nothing.
"""

from __future__ import annotations

import json
import pathlib
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("Requires PyYAML and jsonschema: pip install pyyaml jsonschema")

REPO = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "config" / "schemas" / "classification-rule-set.schema.json"
POSITIVE_GLOBS = ["config/rules/*.yaml"]
NEGATIVE_DIR = REPO / "tests" / "fixtures" / "rules" / "negative"

BAND_RANGES = {
    "safety": (900, 1000),
    "deterministic": (600, 899),
    "content_inference": (300, 599),
    "ai_assisted": (100, 299),
    "fallback": (0, 99),
}


def loader_checks(doc) -> list[str]:
    """Constraints that JSON Schema cannot express. Returns a list of failures."""
    failures: list[str] = []
    rs = (doc or {}).get("rule_set")
    if not isinstance(rs, dict):
        return failures
    rules = rs.get("rules")
    if not isinstance(rules, list):
        return failures

    # VAL-RULE-DUPID — rule ids unique within a set.
    seen_ids: set[str] = set()
    for r in rules:
        if not isinstance(r, dict):
            continue
        rid = r.get("id")
        if rid in seen_ids:
            failures.append(f"VAL-RULE-DUPID: duplicate rule id {rid!r}")
        seen_ids.add(rid)

    # VAL-RULE-DUPPRI — no two rules share a (band, priority) slot.
    seen_slots: set[tuple] = set()
    for r in rules:
        if not isinstance(r, dict):
            continue
        slot = (r.get("band"), r.get("priority"))
        if slot in seen_slots:
            failures.append(
                f"VAL-RULE-DUPPRI: duplicate band/priority slot {slot} (rule {r.get('id')!r})")
        seen_slots.add(slot)

    # VAL-BAND-RANGE — priority inside its band (belt-and-braces vs the schema).
    for r in rules:
        if not isinstance(r, dict):
            continue
        band, pri = r.get("band"), r.get("priority")
        if band in BAND_RANGES and isinstance(pri, int):
            lo, hi = BAND_RANGES[band]
            if not lo <= pri <= hi:
                failures.append(
                    f"VAL-BAND-RANGE: rule {r.get('id')!r} priority {pri} outside band {band} [{lo},{hi}]")

    # VAL-FALLBACK-ONE — exactly one unconditional rule.
    unconditional = [r.get("id") for r in rules
                     if isinstance(r, dict) and isinstance(r.get("when"), dict)
                     and "always" in r["when"]]
    if len(unconditional) > 1:
        failures.append(
            f"VAL-FALLBACK-ONE: {len(unconditional)} unconditional rules {unconditional}; exactly one permitted")

    return failures


def missing_fixture_paths(doc) -> list[str]:
    """Referenced fixture paths that do not exist yet.

    Advisory only: the fixture corpus is built at gate G3, so absence is
    expected at Foundation stage and is not a validation failure.
    """
    missing: list[str] = []
    for r in ((doc or {}).get("rule_set") or {}).get("rules") or []:
        if not isinstance(r, dict):
            continue
        for paths in (r.get("tests") or {}).values():
            for p in paths or []:
                if not (REPO / p).exists():
                    missing.append(p)
    return missing


def validate(doc, validator) -> tuple[list[str], list[str]]:
    """Return (schema_errors, loader_errors)."""
    schema_errors = [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
                     for e in sorted(validator.iter_errors(doc), key=lambda e: list(e.path))]
    return schema_errors, loader_checks(doc)


def main(argv: list[str]) -> int:
    if not SCHEMA_PATH.exists():
        print(f"FAIL: canonical schema missing at {SCHEMA_PATH}")
        return 1

    schema = json.loads(SCHEMA_PATH.read_text())
    Draft202012Validator.check_schema(schema)
    print(f"PASS  schema is valid JSON Schema draft 2020-12: {SCHEMA_PATH.relative_to(REPO)}")
    validator = Draft202012Validator(schema)

    failed = 0

    if argv:
        targets = [pathlib.Path(a) for a in argv]
    else:
        targets = sorted(p for g in POSITIVE_GLOBS for p in REPO.glob(g))

    print(f"\nPositive examples ({len(targets)}) — must validate:")
    for path in targets:
        doc = yaml.safe_load(path.read_text())
        schema_errors, loader_errors = validate(doc, validator)
        errors = schema_errors + loader_errors
        rel = path.relative_to(REPO) if path.is_absolute() else path
        if errors:
            failed += 1
            print(f"  FAIL  {rel}")
            for e in errors[:8]:
                print(f"          {e[:160]}")
        else:
            print(f"  PASS  {rel}")
        pending = missing_fixture_paths(doc)
        if pending:
            print(f"        note VAL-FIXTURE-EXISTS: {len(pending)} fixture path(s) not yet created; "
                  f"the fixture corpus is built at gate G3, so this is not a Foundation-stage failure")

    if argv:
        return 1 if failed else 0

    exp_path = NEGATIVE_DIR / "expectations.yaml"
    if not exp_path.exists():
        print(f"\nFAIL: negative expectations missing at {exp_path.relative_to(REPO)}")
        return 1
    expectations = yaml.safe_load(exp_path.read_text())

    negatives = sorted(p for p in NEGATIVE_DIR.glob("*.yaml") if p.name != "expectations.yaml")
    print(f"\nNegative examples ({len(negatives)}) — must be rejected:")

    unlisted = {p.stem for p in negatives} ^ set(expectations)
    if unlisted:
        failed += 1
        print(f"  FAIL  fixture/expectation mismatch: {sorted(unlisted)}")

    for path in negatives:
        schema_errors, loader_errors = validate(yaml.safe_load(path.read_text()), validator)
        reason = expectations.get(path.stem, "<unlisted>")
        loader_expected = reason.startswith("LOADER:")
        if not schema_errors and not loader_errors:
            failed += 1
            print(f"  FAIL  {path.stem}: ACCEPTED — expected rejection: {reason}")
        elif loader_expected and not loader_errors:
            failed += 1
            print(f"  FAIL  {path.stem}: rejected, but not by the intended loader check — expected: {reason}")
        else:
            layers = "+".join(
                ([f"schema({len(schema_errors)})"] if schema_errors else [])
                + ([f"loader({len(loader_errors)})"] if loader_errors else []))
            print(f"  PASS  {path.stem}: rejected by {layers} — {reason[:70]}")

    print("\n" + ("ALL RULE-CONTRACT CHECKS PASSED" if not failed
                  else f"{failed} RULE-CONTRACT CHECK(S) FAILED"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
