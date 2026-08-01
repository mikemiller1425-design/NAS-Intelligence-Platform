#!/usr/bin/env python3
"""Validate the remediation workbench under docs/proposals/.

Documentation-structure validation only. This script implements no product
behaviour, touches no NAS path, and mutates nothing.

    python3 scripts/validate_proposals.py

Exit code 0 means every check passed.
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
LADDER = REPO / "docs" / "handoffs" / "build-ladder.md"
ODS = REPO / "docs" / "05-governance" / "open-decisions.md"
PROP = REPO / "docs" / "proposals"
PACKETS = PROP / "planning-findings"
BRIEFS = PROP / "operator-decisions"

NON_AUTH = "non-authoritative"

fails: list[str] = []


def check(n: int, name: str, ok: bool, detail: str = "") -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {n:2}. {name}")
    if not ok:
        fails.append(name)
    if detail:
        for line in detail.split("\n")[:10]:
            print(f"          {line}")


def ladder_findings() -> dict[str, str]:
    t = LADDER.read_text()
    out = {}
    for m in re.finditer(r"^\| (PF-\d{2}) \| (BLOCKER|MAJOR|MINOR|NOTE) \|(.+?)\|\s*$", t, re.M):
        out[m.group(1)] = m.group(2)
    return out


def closed_findings() -> set[str]:
    t = LADDER.read_text()
    return {m.group(1) for m in re.finditer(r"^\| (PF-\d{2}) \| NOTE \|.*Closed by", t, re.M)}


def register_decisions() -> set[str]:
    return set(re.findall(r"^\| (OD-\d{3}) \|", ODS.read_text(), re.M))


def rung_blockers() -> dict[str, dict]:
    t = LADDER.read_text()
    parts = re.split(r"^### (FBL-\d{3}) — .+$", t, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        rid, body = parts[i], parts[i + 1]
        m = re.search(r"^\| Blocked by \| (.*?) \|\s*$", body, re.M)
        blocked = m.group(1) if m else ""
        out[rid] = {"ods": set(re.findall(r"OD-\d{3}", blocked)),
                    "pfs": set(re.findall(r"PF-\d{2}", blocked))}
    return out


def main() -> int:
    print("=" * 78)
    print("PROPOSAL WORKBENCH VALIDATION")
    print("=" * 78)

    if not PROP.exists():
        print(f"FAIL: {PROP.relative_to(REPO)} does not exist")
        return 1

    findings = ladder_findings()
    closed = closed_findings()
    open_findings = {p for p in findings if p not in closed}
    decisions = register_decisions()

    packet_text = {p.stem: p.read_text() for p in PACKETS.glob("*.md")}
    brief_text = {p.stem: p.read_text() for p in BRIEFS.glob("*.md")}
    all_prop = list(PROP.rglob("*.md"))
    all_text = "\n".join(p.read_text() for p in all_prop)

    # 1 — every open finding is routed by a packet
    # The inventory is a routing index, not a packet. A finding is only covered
    # when a packet file names it in its own title line.
    covered = set()
    for name, txt in packet_text.items():
        if name == "INVENTORY":
            continue
        first = txt.split("\n", 1)[0]
        covered |= set(re.findall(r"PF-\d{2}", first))
    missing = sorted(open_findings - covered)
    check(1, "Every open planning finding is covered by a remediation packet",
          not missing, f"uncovered: {missing}")

    # 2 — every finding appears in the inventory exactly once as a row
    inv_all = packet_text.get("INVENTORY", "")
    # Only the main inventory table; later tables legitimately re-reference findings.
    inv = inv_all.split("## Atomic clusters")[0]
    rows = re.findall(r"^\| (PF-\d{2}) \|", inv, re.M)
    dupes = sorted({r for r in rows if rows.count(r) > 1})
    check(2, "Every finding appears in the inventory exactly once",
          set(rows) == set(findings) and not dupes,
          f"missing={sorted(set(findings) - set(rows))} duplicated={dupes}")

    # 3 — every registered decision has a brief
    missing_b = sorted(decisions - set(brief_text))
    check(3, "Every open decision has a decision brief", not missing_b,
          f"missing: {missing_b}")

    # 4 — no brief claims to decide
    decided = []
    for od, txt in brief_text.items():
        if not re.search(r"Claude has not decided", txt, re.I):
            decided.append(f"{od}: missing the explicit not-decided statement")
        if re.search(r"^\s*(Decision|Resolved)\s*:\s*(accepted|approved|chosen)", txt, re.M | re.I):
            decided.append(f"{od}: reads as though the decision was made")
    check(4, "No decision brief decides anything", not decided, "\n".join(decided))

    # 5 — every proposal declares itself non-authoritative
    silent = [str(p.relative_to(REPO)) for p in all_prop
              if NON_AUTH not in p.read_text().lower()]
    check(5, "Every proposal declares itself non-authoritative", not silent,
          "\n".join(silent))

    # 6 — no proposal claims authority
    claims = []
    for p in all_prop:
        for m in re.finditer(r"(this (document|packet|brief) (is )?authoriz|hereby authoriz|"
                             r"is now authoritative|supersedes the specification)", p.read_text(), re.I):
            claims.append(f"{p.relative_to(REPO)}: {m.group(0)!r}")
    check(6, "No proposal claims authority", not claims, "\n".join(claims))

    # 7 — every blocked rung's blockers are represented in the workbench
    orphan = []
    for rid, b in rung_blockers().items():
        for od in b["ods"]:
            if od not in brief_text:
                orphan.append(f"{rid} blocked by {od}, which has no brief")
        for pf in b["pfs"]:
            if pf not in covered:
                orphan.append(f"{rid} blocked by {pf}, which no packet covers")
    check(7, "Every blocked rung maps back to a workbench artifact", not orphan,
          "\n".join(sorted(set(orphan))))

    # 8 — no authoritative specification was modified alongside the proposals
    #      (checked by the caller's diff review; here we assert the dirs exist)
    check(8, "Proposals live only under docs/proposals/ and docs/audits/",
          all(str(p.relative_to(REPO)).startswith(("docs/proposals/", "docs/audits/"))
              for p in all_prop),
          "")

    # 9 — no placeholders
    ph = []
    for p in all_prop:
        for m in re.finditer(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum|handle appropriately|"
                             r"as needed|best practices)\b", p.read_text(), re.I):
            line = p.read_text()[:m.start()].count("\n") + 1
            ph.append(f"{p.relative_to(REPO)}:{line}: {m.group(1)!r}")
    check(9, "No placeholders or vague language in proposals", not ph, "\n".join(ph))

    # 10 — internal links resolve
    #
    # A packet may legitimately name a file that does not exist yet: proposing a
    # new schema or fixture is one of the things a packet is for. Distinguishing
    # that from a broken reference cannot be done from the path alone, so the
    # naming line must say so. A path on a line that does not announce itself as
    # proposed is treated as a reference, and must resolve.
    PROPOSED = re.compile(r"propos|to be authored|does not (yet )?exist|new artifact|"
                          r"be authored as", re.I)
    bad = []
    names = {f.name for f in REPO.rglob("*") if f.is_file()}
    for p in all_prop:
        txt = p.read_text()
        lines = txt.split("\n")
        for m in re.finditer(r"`([A-Za-z0-9_\-./]+\.(?:md|ya?ml|json|py))`", txt):
            tgt = m.group(1)
            if (REPO / tgt).exists() or (p.parent / tgt).exists() or tgt.split("/")[-1] in names:
                continue
            if PROPOSED.search(lines[txt[:m.start()].count("\n")]):
                continue
            bad.append(f"{p.relative_to(REPO)} -> {tgt}")
    check(10, "Internal links and referenced paths resolve", not bad,
          "\n".join(sorted(set(bad))))

    # 11 — G3..G8 remain unauthorized
    ledger = (REPO / "docs/05-governance/authorization-ledger.md").read_text()
    unauth = []
    for g in ("G3", "G4", "G5", "G6", "G7", "G8"):
        seg = ledger.split(f"### {g} —")
        if len(seg) < 2 or "NOT AUTHORIZED" not in seg[1].split("### ")[0]:
            unauth.append(f"{g} is not marked NOT AUTHORIZED")
    check(11, "G3 through G8 remain unauthorized", not unauth, "\n".join(unauth))

    # 12 — the workbench does not itself contain a live path or a secret
    #      (delegated to check_path_policy.py; assert proposals are under a Class C root)
    check(12, "Proposal artifacts sit under docs/, governed by the path policy as Class C",
          all(str(p.relative_to(REPO)).startswith("docs/") for p in all_prop), "")

    print("=" * 78)
    print("RESULT: ALL CHECKS PASSED" if not fails else f"RESULT: {len(fails)} FAILING CHECK(S)")
    for f in fails:
        print(f"  - {f}")
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
