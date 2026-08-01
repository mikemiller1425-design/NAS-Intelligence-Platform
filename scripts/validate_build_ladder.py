#!/usr/bin/env python3
"""Validate the Build Ladder as a planning artifact.

Checks structural integrity that a human reviewer cannot reliably hold in mind:
unique rung IDs, dependency resolution, absence of cycles, required-field
completeness, acceptance and open-decision coverage, canonical gate numbering,
and the safety invariant that no G3 rung declares NAS access.

    python3 scripts/validate_build_ladder.py

Reads files only. Performs no NAS access and mutates nothing.
Exit code 0 means every check passed.
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
LADDER = REPO / "docs" / "handoffs" / "build-ladder.md"

REQUIRED_FIELDS = [
    "Gate", "NAS access", "Objective", "Why here", "Prerequisites", "Blocked by",
    "Allowed work", "Prohibited work", "Specifications", "ADRs", "Acceptance",
    "Files affected", "Deliverables", "Positive tests", "Negative tests",
    "Failure-injection tests", "Operator validation", "Evidence package",
    "Rollback / recovery", "Stop conditions", "Definition of Ready",
    "Definition of Done", "Git boundary",
]

CANON_GATES = {
    "G1": "foundation", "G2": "build_ladder", "G3": "implementation",
    "G4": "dry_run", "G5": "pilot", "G6": "live", "G7": "retirement",
    "G8": "migration_completion",
}
GATE_NAS = {
    "G3": {"none"},
    "G4": {"none", "read-only"},
    "G5": {"none", "read-only", "bounded-write"},
    "G6": {"none", "read-only", "bounded-write"},
    "G7": {"none", "read-only", "bounded-write"},
    "G8": {"none", "read-only"},
}

fails: list[str] = []

def _live_patterns() -> list[str]:
    """Read forbidden live-path patterns from the governance policy.

    Read rather than embedded so this file contains no literal live path and
    therefore needs no Class B exemption. See docs/05-governance/path-policy.md.
    """
    policy = REPO / "docs" / "05-governance" / "path-policy.md"
    if not policy.exists():
        return []
    text = policy.read_text()
    start = text.find("### Live path patterns")
    if start == -1:
        return []
    body = text[start:]
    end = body.find("\n### ")
    return re.findall(r"^\| `(.+?)` \|", body if end == -1 else body[:end], re.M)





def check(num: int, name: str, ok: bool, detail: str = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {num:2}. {name}")
    if not ok:
        fails.append(name)
    if detail:
        for line in detail.split("\n")[:10]:
            print(f"          {line}")


def parse() -> dict:
    text = LADDER.read_text()
    parts = re.split(r"^### (FBL-\d{3}) — (.+)$", text, flags=re.M)
    rungs = {}
    order = []
    for i in range(1, len(parts), 3):
        rid, title, body = parts[i], parts[i + 1], parts[i + 2]
        fields = {}
        for m in re.finditer(r"^\| ([^|]+?) \| (.*?) \|\s*$", body, flags=re.M):
            key = m.group(1).strip().strip("*")
            if key in ("Field", "---"):
                continue
            fields[key] = m.group(2).strip()
        rungs[rid] = {"title": title.strip(), "fields": fields, "body": body}
        order.append(rid)
    return {"text": text, "rungs": rungs, "order": order}


def ids_in(value: str) -> set[str]:
    return set(re.findall(r"FBL-\d{3}", value or ""))


def main() -> int:
    if not LADDER.exists():
        print(f"FAIL: ladder missing at {LADDER}")
        return 1

    doc = parse()
    rungs, order = doc["rungs"], doc["order"]
    text = doc["text"]
    print("=" * 78)
    print(f"BUILD LADDER VALIDATION — {len(rungs)} rungs")
    print("=" * 78)

    # 1 — unique, well-formed, contiguous rung IDs
    dupes = [r for r in order if order.count(r) > 1]
    expected = [f"FBL-{i:03d}" for i in range(1, len(order) + 1)]
    check(1, "Rung IDs unique, well-formed, and contiguous",
          not dupes and order == expected,
          f"duplicates={sorted(set(dupes))}" if dupes else
          (f"first divergence: {[(a, b) for a, b in zip(order, expected) if a != b][:3]}"
           if order != expected else ""))

    # 2 — every rung carries every required field
    missing = []
    for rid, r in rungs.items():
        absent = [f for f in REQUIRED_FIELDS if f not in r["fields"]]
        if absent:
            missing.append(f"{rid}: missing {absent}")
    check(2, "Every rung carries all required fields", not missing, "\n".join(missing))

    # 3 — no empty required field
    empty = []
    for rid, r in rungs.items():
        for f in REQUIRED_FIELDS:
            v = r["fields"].get(f, "")
            if f in r["fields"] and (not v or v in ("—", "-", "TBD", "TODO")):
                if not (f in ("Blocked by",) and v == "none"):
                    empty.append(f"{rid}.{f} is empty or a placeholder")
    check(3, "No required field is empty or a placeholder", not empty, "\n".join(empty))

    # 4 — prerequisites resolve to real rungs
    unresolved = []
    for rid, r in rungs.items():
        for dep in ids_in(r["fields"].get("Prerequisites", "")):
            if dep not in rungs:
                unresolved.append(f"{rid} requires unknown {dep}")
    check(4, "Every prerequisite resolves to a defined rung", not unresolved,
          "\n".join(unresolved))

    # 5 — prerequisites precede their dependants (implies acyclicity)
    backward = []
    pos = {rid: i for i, rid in enumerate(order)}
    for rid, r in rungs.items():
        for dep in ids_in(r["fields"].get("Prerequisites", "")):
            if dep in pos and pos[dep] >= pos[rid]:
                backward.append(f"{rid} depends on {dep}, which is not earlier")
    check(5, "Dependencies point strictly backward (no cycles possible)",
          not backward, "\n".join(backward))

    # 6 — 'Enables' is consistent with the reverse prerequisite edges
    enables_issues = []
    for rid, r in rungs.items():
        for nxt in ids_in(r["fields"].get("Git boundary", "")) | ids_in(r["fields"].get("Enables", "")):
            if nxt not in rungs:
                enables_issues.append(f"{rid} enables unknown {nxt}")
            elif rid not in ids_in(rungs[nxt]["fields"].get("Prerequisites", "")):
                enables_issues.append(f"{rid} claims to enable {nxt}, but {nxt} does not list it")
    check(6, "'Enables' edges match the reverse prerequisite edges",
          not enables_issues, "\n".join(enables_issues))

    # 7 — canonical gate values only
    bad_gate = []
    for rid, r in rungs.items():
        g = r["fields"].get("Gate", "")
        toks = re.findall(r"\bG[0-9]\b", g)
        if len(toks) != 1 or toks[0] not in CANON_GATES:
            bad_gate.append(f"{rid}: gate field {g!r}")
    check(7, "Every rung declares exactly one canonical gate (G1-G8)",
          not bad_gate, "\n".join(bad_gate))

    # 8 — SAFETY: no G3 rung declares NAS access
    nas_violations = []
    for rid, r in rungs.items():
        gate = (re.findall(r"\bG[0-9]\b", r["fields"].get("Gate", "")) or [None])[0]
        nas = r["fields"].get("NAS access", "").strip().strip("*").lower()
        allowed = GATE_NAS.get(gate, {"none"})
        if nas not in allowed:
            nas_violations.append(f"{rid} ({gate}): NAS access {nas!r} not in {sorted(allowed)}")
    check(8, "SAFETY — no rung declares NAS access beyond its gate", not nas_violations,
          "\n".join(nas_violations))

    g3_nonnone = [rid for rid, r in rungs.items()
                  if "G3" in r["fields"].get("Gate", "")
                  and r["fields"].get("NAS access", "").strip().lower() != "none"]
    check(9, "SAFETY — every G3 rung is NAS access: none", not g3_nonnone,
          f"violations: {g3_nonnone}")

    # 10 — gates appear in non-decreasing order
    seq = []
    for rid in order:
        g = (re.findall(r"\bG([0-9])\b", rungs[rid]["fields"].get("Gate", "")) or ["0"])[0]
        seq.append((rid, int(g)))
    regress = [f"{seq[i][0]} (G{seq[i][1]}) follows {seq[i-1][0]} (G{seq[i-1][1]})"
               for i in range(1, len(seq)) if seq[i][1] < seq[i - 1][1]]
    check(10, "Gates never regress along the ladder", not regress, "\n".join(regress))

    # 11 — acceptance coverage
    acc_defined = set()
    for f in (REPO / "docs" / "04-acceptance").glob("*.md"):
        acc_defined |= set(re.findall(r"\b(?:V1-ACC|PILOT|LIVE|SAF)-\d{3}\b", f.read_text()))
    acc_mapped = set(re.findall(r"\b(?:V1-ACC|PILOT|LIVE|SAF)-\d{3}\b", text))
    unmapped = sorted(acc_defined - acc_mapped)
    check(11, "Every acceptance ID appears in the ladder",
          not unmapped, f"unmapped: {unmapped}")

    # 12 — open-decision coverage
    od_defined = set(re.findall(r"^\| (OD-\d{3})", (REPO / "docs" / "05-governance" /
                                                   "open-decisions.md").read_text(), flags=re.M))
    od_mapped = set(re.findall(r"\bOD-\d{3}\b", text))
    od_unmapped = sorted(od_defined - od_mapped)
    check(12, "Every open decision appears in the ladder",
          not od_unmapped, f"unmapped: {od_unmapped}")

    # 13 — every referenced planning finding is defined
    pf_ref = set(re.findall(r"\bPF-\d{2}\b", text))
    pf_def = set(re.findall(r"^\| (PF-\d{2}) \|", text, flags=re.M))
    pf_missing = sorted(pf_ref - pf_def)
    check(13, "Every referenced planning finding is defined",
          not pf_missing, f"undefined: {pf_missing}")

    # 14 — no implementation files were created
    impl = []
    for pkg in ["packages", "apps"]:
        for p in (REPO / pkg).rglob("*"):
            if p.is_file() and p.suffix in (".py", ".ts", ".tsx", ".js", ".go", ".rs"):
                impl.append(str(p.relative_to(REPO)))
    check(14, "No application implementation exists", not impl, "\n".join(impl))

    # 15 — no live NAS path anywhere in the ladder
    live = []
    for pat in _live_patterns():
        for m in re.finditer(re.escape(pat), text):
            line = text[:m.start()].count("\n") + 1
            live.append(f"build-ladder.md:{line}: {pat}")
    check(15, "SAFETY — no live NAS path in the ladder", not live, "\n".join(live))

    # 16 — no unresolved placeholders
    ph = []
    for m in re.finditer(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b", text, re.I):
        line = text[:m.start()].count("\n") + 1
        ph.append(f"build-ladder.md:{line}: {m.group(1)}")
    check(16, "No unresolved placeholders", not ph, "\n".join(ph))

    # 17 — the ladder authorizes nothing
    need = ["it authorizes nothing", "never authorizes rung"]
    absent = [n for n in need if n.lower() not in text.lower()]
    check(17, "The ladder states explicitly that it authorizes nothing",
          not absent, f"missing statements: {absent}")

    # 18 — no surviving "no write anywhere" wording (BLOCKER-02)
    #
    # G4 must write local control-plane evidence. Absolute no-write wording
    # contradicted this gate's own entry criteria and the Definition of Done,
    # and made the required evidence impossible to produce.
    bad18 = []
    for doc in [LADDER,
                REPO / "docs/05-governance/gate-model.md",
                REPO / "docs/05-governance/definition-of-done.md",
                REPO / "docs/06-operations/dry-run-playbook.md"]:
        if not doc.exists():
            continue
        dt = doc.read_text()
        for m in re.finditer(r"[Nn]o write(?:s)?(?: of any kind)? anywhere", dt):
            line = dt[:m.start()].count("\n") + 1
            ctx = dt[max(0, m.start() - 120):m.start() + 120]
            if "NAS path" in ctx or "control-data root" in ctx:
                continue  # correctly qualified
            if any(w in ctx for w in ("Earlier wording", "previously", "superseded",
                                      "replaced", "contradicted")):
                continue  # a quotation of the wording that was corrected, not a survival
            bad18.append(f"{doc.relative_to(REPO)}:{line}: unqualified no-write-anywhere wording")
    check(18, "BLOCKER-02 — no unqualified 'no write anywhere' wording survives",
          not bad18, "\n".join(bad18))

    # 19 — G4 states the control-data root rule
    g4 = text[text.index("## Gate G4"):text.index("## Gate G5")] if "## Gate G4" in text else ""
    need19 = ["control-data root", "read", "disjoint"]
    miss19 = [n for n in need19 if n.lower() not in g4.lower()]
    check(19, "BLOCKER-02 — G4 states the read-only NAS rule and the control-root rule",
          not miss19, f"missing from the G4 section: {miss19}")

    # 20 — the ladder defers to the path policy rather than restating an absolute ban
    policy = REPO / "docs/05-governance/path-policy.md"
    bad20 = []
    if not policy.exists():
        bad20.append("docs/05-governance/path-policy.md missing")
    if "path-policy.md" not in text:
        bad20.append("ladder does not reference the path policy")
    for m in re.finditer(r"No live paths\*\* in code, configuration, tests, or fixtures", text):
        bad20.append("ladder still carries the unsatisfiable absolute live-path rule")
    check(20, "BLOCKER-01 — the ladder defers to the class-aware path policy",
          not bad20, "\n".join(bad20))

    print("=" * 78)
    print("RESULT: ALL CHECKS PASSED" if not fails else f"RESULT: {len(fails)} FAILING CHECK(S)")
    for f in fails:
        print(f"  - {f}")
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
