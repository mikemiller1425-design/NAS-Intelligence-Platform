#!/usr/bin/env python3
"""Foundation self-review: 24 checks over the audit-resolution state.

Re-runnable evidence for an independent verifier. Reads files only; performs no
NAS access and mutates nothing.

    python3 scripts/foundation_self_review.py

Requires PyYAML and jsonschema. Exit code 0 means every check passed.
"""
import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = "docs/source/"          # immutable operator source material
NEG = "tests/fixtures/rules/negative/"   # deliberately invalid fixtures

fails, warns = [], []


def active_md():
    for p in sorted(REPO.rglob("*.md")):
        rel = str(p.relative_to(REPO))
        if ".git" in p.parts or rel.startswith(SRC):
            continue
        yield p, rel


def grep(pattern, files=None, flags=re.I):
    rx = re.compile(pattern, flags)
    hits = []
    for p, rel in (files or active_md()):
        for n, line in enumerate(p.read_text(errors="replace").split("\n"), 1):
            if rx.search(line):
                hits.append((rel, n, line.strip()))
    return hits


def check(num, name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    (fails if not ok else []).append(name) if not ok else None
    print(f"[{status}] {num:2}. {name}")
    if detail:
        for d in detail.split("\n")[:8]:
            print(f"          {d}")


print("=" * 78)
print("STAGE 8 SELF-REVIEW")
print("=" * 78)

# 1 & 2 — every finding has a resolution; none waived
audit = (REPO / "docs/audits/foundation-v1-audit.md").read_text()
ids = ["FND-B001", "FND-B002", "FND-B003", "FND-M001", "FND-M002", "FND-M003",
       "FND-M004", "FND-M005", "FND-m001", "FND-m002", "FND-m003", "FND-m004"]
missing = [i for i in ids if f"### {i} " not in audit]
statuses = re.findall(r"\*\*Status:\*\* (.+)", audit)
check(1, "Every BLOCKER/MAJOR/MINOR finding has a resolution entry",
      not missing and len(statuses) == 12,
      f"missing={missing} statuses={len(statuses)}")
waived = [s for s in statuses if "WAIV" in s.upper() or s.strip() == "NOT RESOLVED"]
check(2, "No finding silently waived", not waived, f"waived={waived}")

# 3-5 — schema + examples
r = subprocess.run([sys.executable, "scripts/validate_rule_config.py"], cwd=REPO,
                   capture_output=True, text=True)
out = r.stdout
check(3, "JSON Schema syntax valid (draft 2020-12)",
      "PASS  schema is valid JSON Schema draft 2020-12" in out)
check(4, "Every positive YAML example validates against the canonical schema",
      "PASS  config/rules/classification-rules.example.yaml" in out)
nneg = out.count("PASS  ") - 2
check(5, "Every negative example fails for its intended reason",
      "ALL RULE-CONTRACT CHECKS PASSED" in out and r.returncode == 0,
      f"negative fixtures rejected: {nneg}")

# 6 — obsolete rule-schema field names
OBSOLETE = ["applicable_file_types", "metadata_conditions", "visual_content_conditions",
            "confidence_threshold", "provisional_sensitive",
            "fallback_destination", "priority_order"]
bad6 = []
for term in OBSOLETE:
    for rel, n, line in grep(re.escape(term)):
        if rel.startswith(NEG) or rel.startswith("docs/audits/"):
            continue
        if rel in ("docs/02-specification/rule-model.md", "CHANGELOG.md",
                   "scripts/generate_negative_rule_fixtures.py"):
            continue  # documented as retired
        bad6.append(f"{rel}:{n}: {line[:80]}")
for p in [REPO / "config/rules/classification-rules.example.yaml"]:
    t = p.read_text()
    for term in OBSOLETE + ["enabled:", "review_required:", "effective_date:"]:
        if term in t:
            bad6.append(f"config example still contains {term}")
check(6, "No obsolete rule-schema field names in active config/specs",
      not bad6, "\n".join(bad6))

# 7 — provisional rules that could bypass review
import yaml  # noqa: E402
doc = yaml.safe_load((REPO / "config/rules/classification-rules.example.yaml").read_text())
bad7 = []
for rule in doc["rule_set"]["rules"]:
    th = rule["then"]
    if rule["status"] == "provisional":
        if (th["outcome"] != "route_to_review" or th["destination_authority"] != "advisory_only"
                or th["review_state"] != "review_required"
                or not rule["confirmation"]["required"] or not rule.get("policy_ref")):
            bad7.append(f"{rule['id']} provisional but not fully locked")
    if th["destination_authority"] == "executable_candidate":
        bad7.append(f"{rule['id']} is an executable candidate")
check(7, "No provisional rule can bypass review", not bad7, "\n".join(bad7))

# 8 — contradictory Foundation/V1/live gate wording
bad8 = []
GATE_EXEMPT = ("docs/audits/", "docs/04-acceptance/foundation-acceptance.md",
               "docs/05-governance/gate-model.md", "CHANGELOG.md")
for rel, n, line in grep(r"prohibited until implementation authorization"):
    if not rel.startswith(GATE_EXEMPT):
        bad8.append(f"{rel}:{n}: {line[:80]}")
for rel, n, line in grep(r"(automatically|implicitly) authoriz"):
    if rel.startswith(GATE_EXEMPT):
        continue
    if re.search(r"\b(no|not|never|nothing|cannot|must not|does not)\b", line, re.I):
        continue
    bad8.append(f"{rel}:{n}: {line[:80]}")
check(8, "No contradictory Foundation/V1/live gate wording", not bad8, "\n".join(bad8))

# 9 — unsafe delete/overwrite/retirement/live implications
bad9 = []
UNSAFE = [r"\bpermanently delete\b(?!.*(never|not|prohibit|unavailable))",
          r"silently overwrite(?!.*(never|not|prohibit))",
          r"\bauto-?delete\b(?!.*(never|not|prohibit|reject))"]
for pat in UNSAFE:
    for rel, n, line in grep(pat):
        low = line.lower()
        if any(w in low for w in ("never", "not ", "no ", "prohibit", "unavailable",
                                  "reject", "excluded", "disabled", "cannot")):
            continue
        bad9.append(f"{rel}:{n}: {line[:80]}")
check(9, "No unsafe delete/overwrite/retirement/live implications", not bad9, "\n".join(bad9))

# 10 — ambiguous SQLite/JSONL authority
bad10 = []
PERSIST = [(REPO / "docs/02-specification/state-and-persistence.md",
            "docs/02-specification/state-and-persistence.md")]
for pat in [r"derived from or reconciled against",
            r"SQLite should hold the current durable state",
            r"rebuild derived state from JSONL streams into SQLite-backed current state where appropriate"]:
    for rel, n, line in grep(pat, PERSIST):
        bad10.append(f"{rel}:{n}: {line[:80]}")
for rel, n, line in grep(r"journal or equivalent"):
    if not rel.startswith(("docs/audits/", "CHANGELOG.md")):
        bad10.append(f"{rel}:{n}: {line[:80]}")
sp = (REPO / "docs/02-specification/state-and-persistence.md").read_text()
if "authoritative" not in sp.lower():
    bad10.append("state-and-persistence.md does not state authority")
check(10, "No ambiguous SQLite/JSONL authority", not bad10, "\n".join(bad10))

# 11 — unbound or replayable approvals
ab = REPO / "docs/02-specification/approval-binding-model.md"
need11 = ["subject_content_hash", "nonce", "expires_at", "APR-E21_NONCE_REPLAY",
          "APR-E22_CLAIM_CONFLICT", "APR-E25_CLIENT_ASSERTED_AUTHORIZATION",
          "one-time", "never transferable"]
t11 = ab.read_text()
miss11 = [k for k in need11 if k.lower() not in t11.lower()]
bad11 = list(miss11)
for rel, n, line in grep(r"not transferrable across unrelated"):
    bad11.append(f"{rel}:{n}: legacy transferability wording")
cm = (REPO / "docs/02-specification/command-model.md").read_text()
if "server-computed only" not in cm:
    bad11.append("command-model.md does not mark authorization status server-computed")
check(11, "No unbound or replayable approvals", not bad11, "\n".join(map(str, bad11)))

# 12 — preservation-fidelity language
pm = REPO / "docs/02-specification/preservation-model.md"
bad12 = []
if not pm.exists():
    bad12.append("preservation-model.md missing")
else:
    t12 = pm.read_text()
    for k in ["necessary but NOT sufficient", "unsupported_reported", "best_effort",
              "normalized", "required"]:
        if k not in t12:
            bad12.append(f"preservation-model missing {k}")
for rel, n, line in grep(r"verification may be hash-only|proving copy/move correctness|Verify bytes with cryptographic"):
    if not rel.startswith("docs/audits/"):
        bad12.append(f"{rel}:{n}: hash-sufficiency wording remains")
check(12, "Preservation-fidelity language present; no hash-sufficiency claims",
      not bad12, "\n".join(bad12))

# 13 — placeholders
bad13 = []
for rel, n, line in grep(r"\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b"):
    if rel.startswith(("docs/audits/", NEG, "docs/04-acceptance/foundation-acceptance.md")):
        continue
    if re.search(r"(search for|no unresolved|must not|placeholder)", line, re.I):
        continue  # a check that forbids placeholders, not a placeholder
    bad13.append(f"{rel}:{n}: {line[:80]}")
check(13, "No TODO/TBD/FIXME/lorem-ipsum outside the open-decision register",
      not bad13, "\n".join(bad13))

# 14 — secrets
bad14 = []
SECRET = [r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
          r"(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_-]{12,}"]
allf = [(p, str(p.relative_to(REPO))) for p in REPO.rglob("*")
        if p.is_file() and ".git" not in p.parts and p.suffix in
        (".md", ".yaml", ".yml", ".json", ".py", ".txt", ".toml", ".cfg")]
for pat in SECRET:
    for rel, n, line in grep(pat, allf):
        bad14.append(f"{rel}:{n}: {line[:70]}")
check(14, "No secrets or credential-shaped values", not bad14, "\n".join(bad14))

# 15 — markdown links and referenced paths
bad15 = []
BASENAMES = {}
for _f in REPO.rglob("*"):
    if _f.is_file() and ".git" not in _f.parts:
        BASENAMES.setdefault(_f.name, []).append(_f)
for p, rel in active_md():
    txt = p.read_text(errors="replace")
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", txt):
        tgt = m.group(1).split("#")[0].strip()
        if not tgt or tgt.startswith(("http://", "https://", "mailto:")):
            continue
        if not (p.parent / tgt).resolve().exists():
            bad15.append(f"{rel} -> {tgt} (md link)")
    for m in re.finditer(r"`([A-Za-z0-9_\-./]+\.(?:md|ya?ml|json|py))`", txt):
        tgt = m.group(1)
        if (REPO / tgt).exists() or (p.parent / tgt).exists():
            continue
        # A bare basename is valid shorthand when exactly one such file exists.
        if "/" not in tgt and BASENAMES.get(tgt):
            continue
        bad15.append(f"{rel} -> {tgt} (path ref)")
bad15 = sorted(set(bad15))
check(15, "All Markdown links and referenced paths resolve", not bad15, "\n".join(bad15))

# 16 — Future Registry not in V1
bad16 = []
FR = ["semantic search", "vector index", "face recognition", "multimodal model",
      "agent city", "multi-nas federation", "cloud archive"]
scope_files = [(p, str(p.relative_to(REPO))) for p in REPO.rglob("*.md")
               if any(str(p).find(d) >= 0 for d in
                      ["00-intent", "01-product", "02-specification",
                       "03-architecture", "04-acceptance"])
               and "future-registry" not in str(p)
               and "exclusions.md" not in str(p)]
for term in FR:
    for rel, n, line in grep(re.escape(term), scope_files):
        low = line.lower()
        if any(w in low for w in ("no ", "not ", "never", "exclud", "defer",
                                  "future", "fr-", "out of scope")):
            continue
        bad16.append(f"{rel}:{n}: {line[:80]}")
check(16, "No Future Registry feature entered V1 scope", not bad16, "\n".join(bad16))

# 17 — Raspberry Pi remains Sentinel-only
bad17 = []
for rel, n, line in grep(r"(sentinel|raspberry pi).{0,60}(may|can|shall|must) (approve|classify|mutate|delete|execute)"):
    if not re.search(r"(never|not|cannot|may not|must not|no )", line, re.I):
        bad17.append(f"{rel}:{n}: {line[:90]}")
check(17, "Raspberry Pi remains Sentinel-only", not bad17, "\n".join(bad17))

# 18 — no document authorizes live NAS access
bad18 = []
for rel, n, line in grep(r"(you may|is authorized to|we authorize|now authorized).{0,50}(mount|scan|live nas|live share)"):
    bad18.append(f"{rel}:{n}: {line[:90]}")
for f in ["README.md", "PROJECT_STATUS.md", "FOUNDATION_VERSION.md"]:
    t = (REPO / f).read_text()
    if "Prohibited" not in t and "prohibited" not in t:
        bad18.append(f"{f} lacks a live-execution prohibition")
check(18, "No document authorizes live NAS access", not bad18, "\n".join(bad18))

# 19 — Build Ladder remains ungenerated and unauthorized
bad19 = []
ladder_files = [p for p in REPO.rglob("*build-ladder*") if p.is_file()]
for p in ladder_files:
    rel = str(p.relative_to(REPO))
    if rel not in ("docs/handoffs/003-build-ladder.md", "prompts/build-ladder-generation.md"):
        bad19.append(f"unexpected build-ladder artifact: {rel}")
ps = (REPO / "PROJECT_STATUS.md").read_text()
if "Build Ladder generation | **Not authorized**" not in ps:
    bad19.append("PROJECT_STATUS.md does not mark Build Ladder unauthorized")
h3 = (REPO / "docs/handoffs/003-build-ladder.md").read_text()
if "frozen as planning-only" not in h3:
    bad19.append("handoff 003 lost its planning-only stop condition")
check(19, "Build Ladder remains ungenerated and unauthorized", not bad19, "\n".join(bad19))

# 20 — Foundation 1.0 not marked approved
bad20 = []
for rel, n, line in grep(r"foundation 1\.0"):
    plain = line.replace("**", "").replace("*", "").replace("`", "")
    if not re.search(r"\bapproved\b", plain, re.I):
        continue
    if re.search(r"(not approved|not granted|not been approved|does not approve|"
                 r"explicitly approved|until|before|requires|awaiting|unapproved|remains)",
                 plain, re.I):
        continue
    bad20.append(f"{rel}:{n}: {line[:90]}")
check(20, "Foundation 1.0 is NOT marked approved", not bad20, "\n".join(bad20))

# 21 — YAML/JSON parse of every config artifact
bad21 = []
for p in list(REPO.rglob("config/**/*.yaml")) + list(REPO.rglob("config/**/*.yml")):
    try:
        yaml.safe_load(p.read_text())
    except Exception as e:
        bad21.append(f"{p.relative_to(REPO)}: {e}")
for p in REPO.rglob("config/**/*.json"):
    try:
        json.loads(p.read_text())
    except Exception as e:
        bad21.append(f"{p.relative_to(REPO)}: {e}")
check(21, "All config YAML/JSON parses", not bad21, "\n".join(bad21))

# 22 — event vocabulary parity
dm = (REPO / "docs/02-specification/domain-model.md").read_text()
em = (REPO / "docs/02-specification/event-model.md").read_text()
dm_ev, cur = set(), False
for line in dm.split("\n"):
    if line.startswith("### Emitted events"):
        cur = True
        continue
    if line.startswith(("###", "##")):
        cur = False
    if cur:
        m = re.match(r"- `([A-Z]\w+)`", line)
        if m:
            dm_ev.add(m.group(1))
em_ev = set(re.findall(r"^- `([A-Z]\w+)`", em, re.M))
check(22, "Event vocabulary matches exactly between domain and event models",
      dm_ev == em_ev,
      f"domain-only={sorted(dm_ev - em_ev)} event-only={sorted(em_ev - dm_ev)} total={len(dm_ev)}")

# 23 — every open decision carries severity and blocks_gate
od = (REPO / "docs/05-governance/open-decisions.md").read_text()
rows = re.findall(r"^\| (OD-\d{3}) \|[^|]*\| (BLOCKER|MAJOR|MINOR) \| `(\w+)` \|", od, re.M)
check(23, "Every open decision carries a severity and a blocks_gate",
      len(rows) == 22, f"rows with both attributes: {len(rows)}/22")

# 24 — no open decision blocks foundation
fnd = [r for r in rows if r[2] == "foundation"]
check(24, "No open decision blocks `foundation`", not fnd, f"{fnd}")

# ---------------------------------------------------------------------------
# 25-28 — canonical gate mapping (verification finding VER-B001)
#
# The gate ladder was renumbered from a G0-based scheme to a G1-based one.
# foundation-acceptance.md was authored against the old scheme and kept stale
# G0/G1/G2 references, which made Foundation acceptance appear to be gate G0
# and assigned fixture construction to G2 instead of G3. These checks exist so
# that a renumbering can never again pass review unnoticed.
# ---------------------------------------------------------------------------

CANON_GATES = {
    "G1": ("foundation", "Foundation Approval"),
    "G2": ("build_ladder", "Build Ladder Generation"),
    "G3": ("implementation", "Fixture-Only Implementation"),
    "G4": ("dry_run", "Dry-Run Readiness"),
    "G5": ("pilot", "Copied-Pilot Readiness"),
    "G6": ("live", "Limited-Live Readiness"),
    "G7": ("retirement", "Source-Retirement Readiness"),
    "G8": ("migration_completion", "Migration Completion"),
}
VALID_GATES = set(CANON_GATES)
GATE_SLUGS = {s for s, _ in CANON_GATES.values()}
GATE_NAMES = {n for _, n in CANON_GATES.values()}
GATE_CTX = ("gate", "authoriz", "foundation", "ladder", "implementation",
            "dry-run", "dry_run", "pilot", "live", "retirement", "migration")

# Separator classes differ by direction, so an enumeration such as
# "...(G7), Migration completion (G8)" is not misread as binding G7 to
# "Migration completion". A comma or closing paren ends the item.
SEP_NUM_FIRST = r"[\s`\-—–:]{0,4}"
SEP_NAME_FIRST = r"[\s`\-—–:(]{0,4}"


SELF = "scripts/foundation_self_review.py"


def gate_source_files():
    for p in sorted(REPO.rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        rel = str(p.relative_to(REPO))
        if rel.startswith(SRC) or rel.startswith(NEG):
            continue
        # This file defines the canonical mapping and must be able to name the
        # tokens it rejects, so it is excluded from its own scan. Nothing else is.
        if rel == SELF:
            continue
        if p.suffix not in (".md", ".yaml", ".yml", ".json", ".py"):
            continue
        yield p, rel


# 25 — gate-model.md reproduces the canonical mapping exactly
gm = (REPO / "docs/05-governance/gate-model.md").read_text()
bad25 = []
declared = dict(re.findall(r"^\|\s*(G[1-8])\s*\|\s*`(\w+)`\s*\|", gm, re.M))
for num, (slug, name) in CANON_GATES.items():
    if declared.get(num) != slug:
        bad25.append(f"gate-model.md maps {num} -> {declared.get(num)!r}, canonical is {slug!r}")
    if not re.search(rf"^###\s+{num}\s+—\s+{re.escape(name)}\s+\(`{re.escape(slug)}`\)",
                     gm, re.M):
        bad25.append(f"gate-model.md lacks canonical section heading for {num} — {name} (`{slug}`)")
check(25, "gate-model.md reproduces the canonical G1-G8 mapping exactly",
      not bad25, "\n".join(bad25))

# 26 — no unknown gate token anywhere (this is what rejects G0)
#
# History documents are exempt: a changelog and an audit/verification record must
# be able to quote the superseded token they describe. The exemption is narrow and
# applies to this check only — every normative document (governance, acceptance,
# specification, architecture, operations, prompts, config, and the three
# top-level status files) remains fully covered.
HISTORY = ("CHANGELOG.md", "docs/audits/")
bad26 = []
for p, rel in gate_source_files():
    if rel.startswith(HISTORY):
        continue
    for n, line in enumerate(p.read_text(errors="replace").split("\n"), 1):
        low = line.lower()
        for m in re.finditer(r"\bG(\d+)\b", line):
            tok = "G" + m.group(1)
            if tok in VALID_GATES:
                continue
            if any(w in low for w in GATE_CTX):
                bad26.append(f"{rel}:{n}: unknown gate token {tok}: {line.strip()[:80]}")
check(26, "No unknown gate token (G0, G9, ...) in any normative document",
      not bad26, "\n".join(bad26))

# 27 — no mismatched gate name/number or slug/number binding
bad27 = []
for p, rel in gate_source_files():
    for n, line in enumerate(p.read_text(errors="replace").split("\n"), 1):
        for slug in GATE_SLUGS:
            want = next(k for k, v in CANON_GATES.items() if v[0] == slug)
            for pat in (rf"\b(G[1-8]){SEP_NUM_FIRST}`{re.escape(slug)}`",
                        rf"`{re.escape(slug)}`{SEP_NAME_FIRST}\b(G[1-8])\b"):
                for m in re.finditer(pat, line):
                    if m.group(1) != want:
                        bad27.append(f"{rel}:{n}: {m.group(1)} bound to `{slug}` "
                                     f"(canonical {want}): {line.strip()[:70]}")
        for name in GATE_NAMES:
            want = next(k for k, v in CANON_GATES.items() if v[1] == name)
            for pat in (rf"\b(G[1-8]){SEP_NUM_FIRST}{re.escape(name)}",
                        rf"{re.escape(name)}{SEP_NAME_FIRST}\b(G[1-8])\b"):
                for m in re.finditer(pat, line, re.I):
                    if m.group(1) != want:
                        bad27.append(f"{rel}:{n}: {m.group(1)} bound to '{name}' "
                                     f"(canonical {want}): {line.strip()[:70]}")
check(27, "No mismatched gate name/number or slug/number binding",
      not sorted(set(bad27)), "\n".join(sorted(set(bad27))))

# 28 — activity phrases cite the gate that actually authorizes them.
#
# Checks 26 and 27 cannot catch a *valid* gate token used in a semantically
# wrong place — which is half of what VER-B001 was ("build the fixture corpus
# at G2"). This check covers that class for a small set of high-signal phrases.
ACTIVITY_GATE = [
    (r"fixture corpus", "G3"),
    (r"fixture-only implementation", "G3"),
    (r"Build Ladder generation", "G2"),
]
# Same clause, short connectives allowed, never across clause punctuation.
ACT_GAP = r"[^,.;:|]{0,24}?"
bad28 = []
for p, rel in gate_source_files():
    if rel.startswith("docs/audits/"):
        continue  # audit prose quotes historical wording verbatim
    for n, line in enumerate(p.read_text(errors="replace").split("\n"), 1):
        for phrase, want in ACTIVITY_GATE:
            if not re.search(phrase, line, re.I):
                continue
            # Only the forward binding is judged: the phrase, then the gate token
            # in the same clause ("fixture corpus at G3", "Build Ladder
            # generation authorization (G2)"). The reverse order is weak evidence
            # — a line such as "Foundation approval (G1) != Build Ladder
            # generation authorization (G2)" would otherwise read as binding G1
            # to the second phrase. Consequence: a phrase that *precedes* its
            # gate token in reverse order is not covered here and relies on
            # checks 26 and 27 plus review.
            for m in re.finditer(rf"{phrase}{ACT_GAP}\b(G[1-8])\b", line, re.I):
                got = m.group(1)
                if got and got != want:
                    bad28.append(f"{rel}:{n}: '{phrase}' cites {got}, canonical is {want}: "
                                 f"{line.strip()[:70]}")
check(28, "Activity phrases cite the gate that authorizes them",
      not sorted(set(bad28)), "\n".join(sorted(set(bad28))))

print("=" * 78)
print(f"RESULT: {len(fails)} failing check(s)" if fails else "RESULT: ALL CHECKS PASSED")
if fails:
    for f in fails:
        print(f"  - {f}")
print("=" * 78)
sys.exit(1 if fails else 0)
