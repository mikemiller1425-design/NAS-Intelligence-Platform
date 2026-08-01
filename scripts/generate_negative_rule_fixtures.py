#!/usr/bin/env python3
"""Generate the negative classification-rule fixtures.

Each negative fixture is the canonical positive example with exactly one
mutation applied, so the difference between "valid" and "rejected" is always a
single, reviewable change. Regenerate with:

    python3 scripts/generate_negative_rule_fixtures.py

This script writes files only under tests/fixtures/rules/negative/. It performs
no NAS access and no other filesystem mutation.
"""

from __future__ import annotations

import copy
import pathlib
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

REPO = pathlib.Path(__file__).resolve().parent.parent
POSITIVE = REPO / "config" / "rules" / "classification-rules.example.yaml"
OUT_DIR = REPO / "tests" / "fixtures" / "rules" / "negative"


def _live_root() -> str:
    """The sample forbidden live root, read from the governance policy.

    Read rather than embedded so this generator contains no literal live path
    and therefore needs no Class B exemption, while the fixtures it emits still
    carry the literal that proves the schema rejects it.
    """
    policy = REPO / "docs" / "05-governance" / "path-policy.md"
    text = policy.read_text()
    start = text.index("### Live path patterns")
    body = text[start:]
    end = body.find("\n### ")
    pats = re.findall(r"^\| `(.+?)` \|", body if end == -1 else body[:end], re.M)
    return pats[0]




def rule(doc, rid):
    for r in doc["rule_set"]["rules"]:
        if r["id"] == rid:
            return r
    raise KeyError(rid)


# (fixture-id, expected-failure-reason, mutation)
CASES = [
    ("provisional-auto-approve",
     "A provisional rule must not express an automatically approved or executable outcome.",
     lambda d: rule(d, "MEDIA-100-dogs")["then"].update(
         {"review_state": "approved", "outcome": "propose_destination",
          "destination_authority": "executable_candidate"})),
    ("provisional-confirmation-false",
     "A provisional rule must require operator confirmation.",
     lambda d: rule(d, "DATA-080-csv")["confirmation"].update({"required": False})),
    ("provisional-missing-policy-ref",
     "A provisional rule must name the open decision that blocks its promotion.",
     lambda d: rule(d, "MEDIA-100-dogs").pop("policy_ref")),
    ("unknown-field-rule",
     "Unknown field at rule level must be rejected (retired 'enabled' switch).",
     lambda d: rule(d, "SAFE-001-unreadable").update({"enabled": True})),
    ("unknown-field-ruleset",
     "Unknown field at rule-set level must be rejected (retired 'effective_date').",
     lambda d: d["rule_set"].update({"effective_date": "2026-07-31"})),
    ("unknown-field-then",
     "Unknown field inside 'then' must be rejected (retired 'review_required').",
     lambda d: rule(d, "SAFE-001-unreadable")["then"].update({"review_required": True})),
    ("unknown-field-confidence",
     "Unknown field inside 'confidence' must be rejected (retired 'confidence_threshold').",
     lambda d: rule(d, "SAFE-001-unreadable")["confidence"].update({"confidence_threshold": 0.9})),
    ("conflict-mode-merge",
     "Conflict mode 'merge' is prohibited: it fabricates a destination no rule authored.",
     lambda d: rule(d, "SAFE-001-unreadable")["conflict"].update({"mode": "merge"})),
    ("conflict-mode-keep-first",
     "Conflict mode 'keep_first' is prohibited: it makes configuration load order authoritative.",
     lambda d: rule(d, "SAFE-001-unreadable")["conflict"].update({"mode": "keep_first"})),
    ("conflict-mode-version",
     "Bare conflict mode 'version' is prohibited: destination versioning is a collision policy, not a rule-conflict mode.",
     lambda d: rule(d, "DATA-080-csv")["conflict"].update({"mode": "version"})),
    ("merge-content-true",
     "Content merging is never permitted; merge_content is pinned false.",
     lambda d: rule(d, "SAFE-001-unreadable")["conflict"].update({"merge_content": True})),
    ("load-order-significant",
     "Configuration load order must never influence which rule wins.",
     lambda d: d["rule_set"]["defaults"].update({"load_order_significance": "first_wins"})),
    ("reordered-conflict-resolution",
     "Conflict-resolution order is pinned and may not be redefined by configuration.",
     lambda d: d["rule_set"].update(
         {"conflict_resolution_order": ["manual_review", "higher_priority_deterministic"]})),
    ("reordered-evaluation-order",
     "Evaluation order is pinned and may not be reordered by configuration.",
     lambda d: d["rule_set"].update({"evaluation_order": ["unresolved_fallback", "safety_exclusions"]})),
    ("dry-run-disabled",
     "dry_run_only is pinned true for schema_version 1.",
     lambda d: d["rule_set"]["defaults"].update({"dry_run_only": False})),
    ("environment-live",
     "A live rule set is not expressible in schema_version 1.",
     lambda d: d["rule_set"].update({"environment": "live"})),
    ("missing-evidence",
     "Every rule must declare its required evidence.",
     lambda d: rule(d, "MEDIA-100-dogs").pop("evidence")),
    ("empty-evidence-list",
     "Required-evidence list must be non-empty.",
     lambda d: rule(d, "MEDIA-100-dogs")["evidence"].update({"required": []})),
    ("confidence-above-one",
     "Confidence must lie within [0.0, 1.0].",
     lambda d: rule(d, "MEDIA-100-dogs")["confidence"].update({"minimum": 1.5})),
    ("confidence-negative",
     "Confidence must lie within [0.0, 1.0].",
     lambda d: rule(d, "MEDIA-100-dogs")["confidence"].update({"minimum": -0.1})),
    ("absolute-live-destination",
     "Destination templates are relative; absolute live share paths are structurally rejected.",
     lambda d: rule(d, "MEDIA-095-drone")["then"].update(
         {"destination": _live_root() + "/30_DRONE/{capture_year}"})),
    ("parent-traversal-destination",
     "Parent traversal in a destination template is rejected.",
     lambda d: rule(d, "MEDIA-095-drone")["then"].update({"destination": "30_DRONE/../../etc"})),
    ("unapproved-placeholder",
     "Only approved destination placeholders may be used.",
     lambda d: rule(d, "MEDIA-095-drone")["then"].update({"destination": "30_DRONE/{operator_home}"})),
    ("literal-destination-root",
     "destination_root_ref must be a symbolic name, never a literal path.",
     lambda d: d["rule_set"].update({"destination_root_ref": _live_root() + "/destination"})),
    ("bad-schema-version",
     "Only schema_version 1 is defined; other versions must be rejected, not coerced.",
     lambda d: d.update({"schema_version": 2})),
    ("retired-flat-schema",
     "The retired flat rule schema must be rejected wholesale.",
     lambda d: (d.clear(), d.update(
         {"version": "1.0.0-example", "status": "non_production_example",
          "evaluation_order": ["safety_exclusions"],
          "rules": [{"id": "MEDIA-100-dogs", "enabled": True, "confidence_threshold": 0.9,
                     "review_required": False, "destination": "/fixtures/destination/x",
                     "applicable_file_types": ["image"], "metadata_conditions": {},
                     "visual_content_conditions": {}, "fallback": "manual_review"}]}))),
    ("ai-evidence-executable",
     "A rule relying on AI-suggested evidence can never yield an executable destination.",
     lambda d: rule(d, "MEDIA-050-known-person-candidate").update(
         {"status": "active", "privacy_classification": "none",
          "then": dict(rule(d, "MEDIA-050-known-person-candidate")["then"],
                       outcome="propose_destination",
                       destination_authority="executable_candidate",
                       review_state="approved")})),
    ("sensitive-identity-active",
     "A sensitive-identity rule may never carry status 'active'.",
     lambda d: rule(d, "MEDIA-050-known-person-candidate").update({"status": "active"})),
    ("priority-outside-band",
     "Priority must fall inside its declared band's range.",
     lambda d: rule(d, "MEDIA-100-dogs").update({"priority": 950})),
    ("band-kind-mismatch",
     "Rule kind must match its declared band.",
     lambda d: rule(d, "MEDIA-095-drone").update({"kind": "ai_assisted"})),
    ("always-outside-fallback",
     "An unconditional match is legal only in the fallback band.",
     lambda d: rule(d, "MEDIA-100-dogs").update({"when": {"always": True}})),
    ("active-rule-missing-tests",
     "An active rule requires positive, negative, boundary, conflict, and idempotency fixtures.",
     lambda d: rule(d, "SAFE-001-unreadable")["tests"].update({"conflict": []})),
    ("two-combinators-one-node",
     "A condition node carries exactly one combinator or leaf.",
     lambda d: rule(d, "MEDIA-100-dogs").update(
         {"when": {"all": [{"predicate": {"field": "extension", "op": "present",
                                          "evidence_source": "filesystem"}}],
                   "any": [{"predicate": {"field": "extension", "op": "present",
                                          "evidence_source": "filesystem"}}]}})),
    ("predicate-missing-evidence-source",
     "Every predicate must declare the provenance of the fact it tests.",
     lambda d: rule(d, "MEDIA-100-dogs").update(
         {"when": {"predicate": {"field": "extension", "op": "equals", "value": ".jpg"}}})),
    ("predicate-unknown-field",
     "Predicate fields are drawn from a closed vocabulary.",
     lambda d: rule(d, "MEDIA-100-dogs").update(
         {"when": {"predicate": {"field": "vibes", "op": "equals", "value": "good",
                                 "evidence_source": "ai_suggestion"}}})),
    ("regex-without-flavor",
     "A regex predicate must pin its regex flavor.",
     lambda d: rule(d, "MEDIA-100-dogs").update(
         {"when": {"predicate": {"field": "filename", "op": "regex", "value": "^x",
                                 "evidence_source": "path"}}})),
    ("active-ruleset-without-approval",
     "An active rule set must carry a granted approval.",
     lambda d: d["rule_set"].update({"status": "active"})),
    ("executable-in-unapproved-set",
     "An unapproved rule set may not contain an executable rule.",
     lambda d: rule(d, "SAFE-001-unreadable")["then"].update(
         {"outcome": "propose_destination", "destination_authority": "executable_candidate",
          "review_state": "approved"})),
    ("collision-versioned-missing-template",
     "Destination versioning requires an exact version template and a maximum.",
     lambda d: rule(d, "SAFE-001-unreadable").update(
         {"collision": {"policy": "versioned_suffix", "never_overwrite": True}})),
    ("collision-overwrite-allowed",
     "never_overwrite is pinned true under every collision policy.",
     lambda d: rule(d, "SAFE-001-unreadable").update(
         {"collision": {"policy": "skip", "never_overwrite": False}})),
    ("live-fixture-path",
     "Test fixtures must be repository-relative synthetic paths, never live share paths.",
     lambda d: rule(d, "SAFE-001-unreadable")["tests"].update(
         {"positive": ["/Volumes/NAS/real/photo.jpg"]})),
    ("manual-override-auto-approve",
     "A manual-override rule must not inherit automatic authority.",
     lambda d: rule(d, "FALLBACK-000-unresolved")["then"].update(
         {"outcome": "propose_destination", "destination_authority": "executable_candidate",
          "review_state": "approved"})),
    ("bad-rule-id-format",
     "Rule identifiers must match the stable identifier pattern.",
     lambda d: rule(d, "MEDIA-100-dogs").update({"id": "dogs rule #1"})),
    ("empty-rule-set",
     "A rule set must contain at least one rule.",
     lambda d: d["rule_set"].update({"rules": []})),
    # Loader-enforced cases (JSON Schema alone cannot express these).
    ("duplicate-rule-id",
     "LOADER: rule identifiers must be unique within a rule set.",
     lambda d: d["rule_set"]["rules"].append(
         dict(copy.deepcopy(rule(d, "DATA-080-csv")), priority=649))),
    ("duplicate-band-priority",
     "LOADER: no two rules may share the same band and priority.",
     lambda d: d["rule_set"]["rules"].append(
         dict(copy.deepcopy(rule(d, "DATA-080-csv")), id="DATA-081-csv-alt"))),
    ("two-fallback-rules",
     "LOADER: exactly one rule may match unconditionally.",
     lambda d: d["rule_set"]["rules"].append(
         dict(copy.deepcopy(rule(d, "FALLBACK-000-unresolved")),
              id="FALLBACK-001-second", priority=1))),
]


def main() -> int:
    doc = yaml.safe_load(POSITIVE.read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    expectations = {}
    for name, reason, mutate in CASES:
        d = copy.deepcopy(doc)
        mutate(d)
        header = (
            "# NEGATIVE EXAMPLE — MUST FAIL VALIDATION\n"
            f"# Case: {name}\n"
            f"# Expected failure: {reason}\n"
            "# Generated by scripts/generate_negative_rule_fixtures.py — do not hand-edit.\n"
        )
        (OUT_DIR / f"{name}.yaml").write_text(header + yaml.safe_dump(d, sort_keys=False))
        expectations[name] = reason

    (OUT_DIR / "expectations.yaml").write_text(
        "# Maps each negative fixture to the reason it must be rejected.\n"
        "# Verified by scripts/validate_rule_config.py.\n"
        + yaml.safe_dump(expectations, sort_keys=True)
    )
    print(f"wrote {len(CASES)} negative fixtures + expectations.yaml to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
