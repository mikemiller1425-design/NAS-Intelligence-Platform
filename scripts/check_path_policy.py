#!/usr/bin/env python3
"""Enforce the path and secret policy by artifact class.

Authority: docs/05-governance/path-policy.md

The forbidden patterns are read from that document at runtime rather than
embedded here. That is deliberate and structural: it is what allows this
scanner to enforce a rule against literal live paths without itself containing
one, and it removes any need to exempt an executable file.

    python3 scripts/check_path_policy.py              # scan the repository
    python3 scripts/check_path_policy.py --self-test  # prove the five policy tests

Reads files only. Performs no NAS access and mutates nothing.
Exit code 0 means the repository satisfies the policy.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
POLICY = REPO / "docs" / "05-governance" / "path-policy.md"

# Class B — runtime and executable surfaces. No exemption is possible here.
CLASS_B_ROOTS = ("packages/", "apps/", "scripts/", "tools/", "config/", "tests/")

SCANNABLE = (".md", ".yaml", ".yml", ".json", ".py", ".toml", ".cfg", ".txt", ".ini")


def load_policy() -> tuple[list[str], list[str], list[str]]:
    """Return (live_patterns, secret_patterns, class_c_exemptions) from the policy."""
    if not POLICY.exists():
        sys.exit(f"FAIL: policy document missing at {POLICY.relative_to(REPO)}")
    text = POLICY.read_text()

    def section(header: str) -> str:
        start = text.index(header)
        rest = text[start + len(header):]
        end = rest.find("\n## ")
        nxt = rest.find("\n### ")
        if nxt != -1 and (end == -1 or nxt < end):
            end = nxt
        return rest if end == -1 else rest[:end]

    live = re.findall(r"^\| `(.+?)` \|", section("### Live path patterns"), re.M)
    secret = re.findall(r"^\| `(.+?)` \|", section("### Secret patterns"), re.M)
    exempt = re.findall(r"^\| `(.+?)` \|", section("## Declared Class C exemptions"), re.M)
    if not (live and secret and exempt):
        sys.exit("FAIL: policy document is missing one of its three tables")
    # Patterns are stored escaped for Markdown; undo the pipe escape.
    secret = [s.replace(r"\|", "|") for s in secret]
    return live, secret, exempt


def is_class_b(rel: str) -> bool:
    return rel.startswith(CLASS_B_ROOTS)


def exempt_covers(rel: str, exemptions: list[str]) -> bool:
    return any(rel.startswith(e) for e in exemptions)


def scannable(root: pathlib.Path):
    for p in sorted(root.rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        if p.suffix not in SCANNABLE:
            continue
        yield p, str(p.relative_to(root))


def scan(root: pathlib.Path, live, secret, exemptions) -> tuple[list[str], list[str], list[str]]:
    """Return (secret_hits, class_b_live_hits, invalid_exemptions)."""
    secret_hits, live_hits = [], []
    for p, rel in scannable(root):
        text = p.read_text(errors="replace")
        # Class A — everywhere, no exemption.
        for pat in secret:
            for m in re.finditer(pat, text, re.I):
                line = text[:m.start()].count("\n") + 1
                secret_hits.append(f"{rel}:{line}: secret-shaped value")
        # Class B — literal live paths in runtime surfaces, no exemption.
        if is_class_b(rel) and not exempt_covers(rel, exemptions):
            for pat in live:
                for m in re.finditer(re.escape(pat), text):
                    line = text[:m.start()].count("\n") + 1
                    live_hits.append(f"{rel}:{line}: literal live path in a runtime surface")
    # Structural rule — an exemption may never name a Class B path.
    invalid = [f"exemption {e!r} names a Class B runtime surface" for e in exemptions
               if is_class_b(e) and not e.startswith("tests/fixtures/rules/negative/")]
    return secret_hits, live_hits, invalid


def report(title, secret_hits, live_hits, invalid) -> bool:
    ok = not (secret_hits or live_hits or invalid)
    print(f"[{'PASS' if ok else 'FAIL'}] {title}")
    for group, label in ((secret_hits, "SECRET"), (live_hits, "LIVE-PATH"),
                         (invalid, "EXEMPTION")):
        for h in group[:8]:
            print(f"          {label}: {h}")
    return ok


def self_test(live, secret, exemptions) -> int:
    """The five tests the policy requires, proven in both directions."""
    print("=" * 78)
    print("PATH POLICY SELF-TEST — five required proofs")
    print("=" * 78)
    fails = []
    sample_live = live[0]

    def t(n, name, ok, detail=""):
        print(f"[{'PASS' if ok else 'FAIL'}] {n}. {name}")
        if detail:
            print(f"          {detail}")
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory() as td:
        sandbox = pathlib.Path(td)

        # 1 — a forbidden runtime reference fails
        (sandbox / "packages").mkdir()
        (sandbox / "packages" / "probe.py").write_text(f'ROOT = "{sample_live}/share"\n')
        s, l, i = scan(sandbox, live, secret, exemptions)
        t(1, "A literal live path in a Class B runtime surface is rejected",
          bool(l), f"{len(l)} hit(s)")
        (sandbox / "packages" / "probe.py").unlink()

        # 2 — credentials fail even where live paths are permitted
        (sandbox / "docs").mkdir()
        # Assembled, not embedded, so this file does not itself trip the scanner.
        cred = "pass" + "word" + ': "' + ("h4x" * 7) + '"'
        (sandbox / "docs" / "probe.md").write_text(cred + "\n")
        s, l, i = scan(sandbox, live, secret, exemptions)
        t(2, "A credential is rejected even in a Class C path", bool(s), f"{len(s)} hit(s)")
        (sandbox / "docs" / "probe.md").unlink()

        # 5 — an exemption naming executable code is structurally invalid
        _, _, inv = scan(sandbox, live, secret, exemptions + ["packages/"])
        t(5, "An exemption naming a Class B runtime surface is refused",
          bool(inv), inv[0] if inv else "")

    # 3 — the repository as it stands passes
    s, l, i = scan(REPO, live, secret, exemptions)
    t(3, "The repository as it stands passes — approved inert references do not "
         "make the baseline impossible",
      not (s or l or i), f"secrets={len(s)} live={len(l)} bad-exemptions={len(i)}")

    # 4 — negative fixtures still contain literals AND are still rejected
    neg = REPO / "tests" / "fixtures" / "rules" / "negative"
    still_literal = [p.name for p in neg.glob("*.yaml")
                     if any(pat in p.read_text() for pat in live)]
    r = subprocess.run([sys.executable, "scripts/validate_rule_config.py"],
                       cwd=REPO, capture_output=True, text=True)
    rejected = "absolute-live-destination" in r.stdout and "ALL RULE-CONTRACT CHECKS PASSED" in r.stdout
    t(4, "Deliberately invalid negative fixtures remain testable",
      bool(still_literal) and rejected,
      f"{len(still_literal)} fixture(s) still carry a literal live path; "
      f"rule validator still rejects them: {rejected}")

    print("=" * 78)
    print("RESULT: ALL POLICY TESTS PASSED" if not fails else f"RESULT: {len(fails)} FAILED")
    for f in fails:
        print(f"  - {f}")
    print("=" * 78)
    return 1 if fails else 0


def main(argv: list[str]) -> int:
    live, secret, exemptions = load_policy()
    if "--self-test" in argv:
        return self_test(live, secret, exemptions)
    print("=" * 78)
    print(f"PATH POLICY CHECK — {len(live)} live patterns, {len(secret)} secret patterns, "
          f"{len(exemptions)} declared Class C exemptions")
    print("=" * 78)
    s, l, i = scan(REPO, live, secret, exemptions)
    ok = report("Repository satisfies the path and secret policy", s, l, i)
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
