# Build Ladder Stress Test

> **Non-authoritative.** This is an adversarial review of the Build Ladder at commit `8838ac6`. It
> records defects; it resolves none, and it changes no authoritative document. Nothing here
> authorizes any gate.

Method: an independent adversarial lane read all 79 rungs, both acceptance families, all governance
documents, and both enforcing scripts; the lead independently extracted the full
finding/decision/rung graph and cross-checked the ladder's two internal representations against
each other. Every BLOCKER and MAJOR below was verified directly against the files before being
recorded here.

**Several of these are defects in work produced during ladder generation and the subsequent
correction pass.** They are recorded with the same severity as any other.

| Severity | Count |
| --- | --- |
| BLOCKER | 8 |
| MAJOR | 13 |
| MINOR | 10 |
| NOTE | 2 |

## What survived the attack

Stated first, because a stress test that reports only failures is not calibrated.

- The prerequisite graph is genuinely acyclic and topologically monotone across all 79 rungs.
- `Enables` never claims an edge the target's `Prerequisites` does not confirm.
- All 70 G3 rungs declare `NAS access: none`.
- No permanent-deletion pathway exists anywhere in the repository.
- No control depends only on frontend behaviour — FBL-063 explicitly injects a forged command
  submitted directly to the backend.
- No automatic gate or batch progression wording survives.
- G1 and G2 are recorded as granted; **G3 through G8 are all recorded NOT AUTHORIZED.**

---

## BLOCKER

### BLT-B01 — Two rungs are blocked by a finding only their own deliverable can close

FBL-034 is `Blocked by: PF-15` (the taxonomy has no machine-readable schema). PF-15's routing is
"author a canonical taxonomy schema". FBL-034's own `Allowed work` is *authoring that schema*, and
its `Definition of Ready` requires PF-15 resolved. **The rung can never become ready without
someone first doing the rung's work**, and the implementation prompt forbids the implementer from
modifying specification documents.

FBL-021 has identical structure with PF-12 (the symbolic root registry).

**Resolution:** split each into a change-control deliverable (the canonical contract) and a rung
deliverable (the loader and its enforcement), and restate PF-12 and PF-15 to name only the contract
half.

### BLT-B02 — Six entity-changing findings do not block the only rung that can implement them

FBL-003 is the sole home for domain entities and forbids inventing any field the specification does
not define. It is blocked by PF-04, PF-05, PF-07, PF-08, PF-11. But **PF-10, PF-19, PF-20, PF-21,
PF-23, and PF-24 also add or change entities and fields**, and none names FBL-003.

FBL-003 sits at position 3; PF-24 resolves at FBL-053. Under the G3 Definition of Done ("only the
named rung's files changed") and the one-commit boundary, FBL-053 cannot legally add an entity to
the contracts package. **The rung would be built against a knowingly incomplete entity set and
reopened six times.**

**Resolution:** add the six findings to FBL-003's `Blocked by` and to their own `Blocks` columns, or
charter an explicit contract-amendment rung with its own authorization. Do not leave it implicit.

### BLT-B03 — The path policy makes G4–G8 evidence unproducible

`path-policy.md` places *generated artifacts — plans, commands, adapter inputs, manifests, and any
runtime output* in **Class B**, and states plainly that no executable artifact can be exempted.

But G4's required evidence is precisely a set of generated artifacts naming live NAS paths: a
confirmed root list, a control-data root declaration with its disjointness proof, an inventory
manifest. Both G4 rungs commit that evidence (`Git boundary: One commit: evidence only`).

**An inventory manifest of a live NAS root is a literal live path in a committed generated
artifact, with no exemption available.** The Definition of Done restates the path policy for G3
only, so its applicability at G4 and later is undefined rather than relieved.

As written, the path-policy check fails the first G4 commit and there is no legal fix. **This is the
same defect class as the FBL-001 baseline problem the previous review caught, recurring at every
live gate.**

**Resolution:** requires a new operator decision — see *Proposed new decisions* below.

### BLT-B04 — A BLOCKER safety row prohibits what FBL-073 does

`SAF-006` (BLOCKER) states: *No live NAS mutation is authorized at any gate before G6.*

FBL-073 is gate **G5**, `NAS access: bounded-write`, objective *"Characterize the destination — the
first legal write"*.

`authority-order.md` resolves conflicts in favour of the stricter safety rule. **SAF-006 is
stricter, so the ladder's assumed resolution of PF-25 is currently prohibited by a BLOCKER
acceptance row.** FBL-073 cannot be authorized until SAF-006 is amended through change control.
Neither FBL-073's `Blocked by` nor the planning-findings section records this conflict.

### BLT-B05 — No rung ever measures the authoritative destination descriptor

A descriptor is valid only if produced by a characterization run; a hand-written one is rejected.
The destination descriptor is frozen into the plan at approval, and FBL-061 makes descriptor drift
a **fatal** stop.

FBL-073 characterizes the destination *confined to the isolated pilot zone* — explicitly prohibited
from writing to any authoritative destination. FBL-075 is the first authoritative-destination write,
has no characterization deliverable, and is `Blocked by: none beyond the G6 authorization itself`.

So at FBL-075 the plan either carries the pilot-zone descriptor (measured against a different
destination, so FBL-061 fires fatally, or it is silently wrong) or carries none (invalid).

**PF-25's assumed resolution moves the defect from G4 to G6 rather than closing it, and no finding
records the G6 half.**

### BLT-B06 — Seven acceptance IDs are cited by the ladder but do not exist

Verified by diffing every ID cited in the ladder against `docs/04-acceptance/`:

| Phantom ID | Cited at ladder line |
| --- | --- |
| `V1-ACC-007` | 307, 336, 423, 1931, 2108 |
| `V1-ACC-060`, `V1-ACC-061` | 716 |
| `V1-ACC-067` | 774 |
| `SAF-016` | 249 |
| `PILOT-019` | 423 |
| `FND-ACC-008` | 365 |

**FBL-065's entire acceptance mapping is a single row that does not exist.** FBL-022's is two-thirds
phantom.

This is not caught by tooling: `validate_build_ladder.py` check 11 computes *defined minus cited*
only. The reverse direction is never checked, although the equivalent reverse check **is** performed
for planning findings in check 13.

**Resolution:** add the reverse direction to check 11 so it cannot recur, and either define the rows
or remap the eight rungs. The check is deliberately **not** added in this pass, because it would
fail immediately and the fix belongs in a change-control batch, not in a preparation commit.

### BLT-B07 — Independent inspection is mandatory only at G3, and disappears at every gate that touches the NAS

The Definition of Done requires an independent rung inspection verdict at G3. The G4, G5, G6, G7,
and G8 sections contain no equivalent, and no rung FBL-071…FBL-079 names an inspector in its
evidence package, operator validation, or Definition of Done.

Meanwhile `prompts/pilot-readiness-audit.md`, `live-readiness-audit.md`,
`migration-completion-audit.md`, and `safety-review.md` all exist and are referenced by **no rung**.

**Consequence: the same actor assembles the G4, G6, and G8 evidence bundle and is the only party
that checks it.** FBL-070 delivers an evidence assembler validated by a self-check it also
delivers. FBL-074 assembles the G6 package and evaluates its own rows. This is a builder approving
its own output at exactly the gates where the system first touches real data.

### BLT-B08 — The two newest operator decisions gate nothing

`OD-023` and `OD-024` were created during ladder generation. **Neither is named in any rung's
`Blocked by`.** The ladder's stated safety mechanism is that "a rung whose `Blocked by` field names
a decision must visibly stop" — so neither decision stops anything.

Compounding it:

- The ladder's table is headed **"The six G3 blockers"** and lists six; the register records
  **seven** for `blocks_gate: implementation`, including OD-024.
- FBL-071 states "all seven carry `blocks_gate: dry_run`"; the register records **eight**,
  including OD-023.
- OD-023 carries `blocks_gate: dry_run`, so it blocks **G4 entry — FBL-071 — not FBL-072** as the
  ladder's own decision map states.

---

## MAJOR

| ID | Finding |
| --- | --- |
| BLT-M01 | **"The last G3 rung" is false.** FBL-063 and FBL-064 are outside FBL-070's transitive prerequisite closure; they are pulled in only by FBL-074 at G6. G4 could be requested and executed with neither the console nor the Sentinel built, and FBL-070's self-check would still pass. |
| BLT-M02 | **PF-29 blocks nothing.** It lists FBL-045 and FBL-072; neither rung names it. It is the finding most likely to surface at exactly the moment G4 runs. |
| BLT-M03 | **Two more `Blocks` ↔ `Blocked by` breaks.** PF-13 lists FBL-072, which omits it. PF-25 lists FBL-073, which omits it — although FBL-073's `Why here` says it *is* the resolution of PF-25. A rung cannot be a finding's resolution and be free to start while it is open. |
| BLT-M04 | **`Definition of Ready` contradicts `Blocked by` in 13 rungs**, including FBL-013 omitting OD-014 and FBL-071 naming no decision at all. Several use the paraphrase "the named planning findings resolved", which is not machine-checkable — and the stopping mechanism depends on machine-checkability. |
| BLT-M05 | **The validator encodes a NAS-permission model no governance document states.** `validate_build_ladder.py` grants G8 `read-only`; the gate model grants G8 no NAS access at all. FBL-077 and FBL-079 declare `read-only` at G8 while their allowed work describes no NAS read. A second source of truth for gate permissions, living in an executable check, is itself a governance defect. |
| BLT-M06 | **FBL-073 asserts "originals provably untouched" with no verification method** and does not name PF-13, which establishes that hash comparison cannot prove non-mutation. FBL-026 and FBL-072 both handle this explicitly; FBL-073 does not. |
| BLT-M07 | **The implementation prompt keys on field names the ladder does not have.** The prompt reads "Blocking open decisions" and "Likely files affected"; the ladder's fields are `Blocked by` and `Files affected`. The ladder relies on this prompt as its stopping mechanism, so the preconditions cannot fire. |
| BLT-M08 | **The secret scanner has an undeclared exemption by file extension.** Class A secrets are "forbidden in every committed artifact without exception", but `check_path_policy.py` scans only nine suffixes. `.env`, `.sh`, `.ts`, `.js`, `Dockerfile`, `Makefile`, `.gitignore`, and lockfiles are never scanned. FBL-063 builds a console app; FBL-001 produces a lockfile and a Makefile. This is precisely the undeclared exemption FBL-001 prohibits, and it makes SAF-005 unprovable. |
| BLT-M09 | **The path policy's catch-all and its enforcing script disagree.** The policy says "any other path containing a literal live NAS path is a violation"; the script applies the live-path rule only inside Class B roots. Two committed files outside every declared Class C root carry a literal pattern and are silently unreported: `.gitignore:52` and `CHANGELOG.md:17`. **If a future implementer makes the guard faithful to the policy text, required test 3 — "the repository as it stands passes" — fails immediately.** That is the same self-defeating-baseline structure the previous review caught. |
| BLT-M10 | **FBL-071 is unimplementable without a policy violation.** It must configure a read-only mount naming the confirmed live root, but `config/` is Class B with no exemption, and the policy states that nothing in it authorizes a configuration default to name a live path. Its git boundary simultaneously says "evidence only, no code". No document states where live configuration may exist. |
| BLT-M11 | **G4's disjointness proof has no producer.** The proof is a G4 *entry* criterion, but the only rung that evaluates overlap is FBL-071, whose stop condition runs *after* G4 is granted. FBL-070's self-check has no fixture-legal way to construct the proof, and the proof artifact itself falls under BLT-B03. |
| BLT-M12 | **FBL-079, the terminal rung, has no executable acceptance row.** Its only acceptance is V1-ACC-054, which `v1-acceptance.md` lists among the relocated rows explicitly *not* evaluated there. FBL-078 has the same defect with V1-ACC-055. |
| BLT-M13 | **FBL-001 and FBL-070 are self-validating bootstraps.** FBL-001 says so outright: its own Definition of Done requires the evidence emitter that the rung itself builds. The path guard's only proof is a self-test inside the guard. The G3 case is covered by independent rung inspection; the FBL-070 → G4 case is not (see BLT-B07). |

---

## MINOR

| ID | Finding |
| --- | --- |
| BLT-N01 | The severity table undercounts: it says 3 MINOR and "thirty specification gaps"; there are **4 MINOR rows and 31 PF IDs defined** (30 open, 1 closed). |
| BLT-N02 | The G2 Definition of Done requires a `live NAS access in scope` field; the ladder's field is `NAS access`. The ladder cannot satisfy its own G2 exit criterion as literally written. Same stale name in the Definition of Ready. |
| BLT-N03 | The `Enables` field is declared as a rung field but abandoned after FBL-025; 55 rungs fold it into `Git boundary`. 41 real dependency edges appear in `Prerequisites` but in no `Enables`. Under-inclusive only, so not a safety defect, but unreliable for driving an authorization workflow. |
| BLT-N04 | FBL-050's rollback says "None needed — nothing was written" while its positive test is "a non-vault destination copies normally". |
| BLT-N05 | OD-009 and OD-020 are mapped in the decision map to FBL-075, which is `Blocked by: none`; **FBL-074** is the rung that actually names them. |
| BLT-N06 | The PF `Blocks` column is incomplete in the reverse direction: FBL-003 stops for five findings, none of which lists FBL-003. An operator closing PF-04 will not learn that FBL-003 was also waiting. |
| BLT-N07 | `migration-completion-audit.md` is cited under **Specifications** by FBL-068 and FBL-077; it is a prompt, which the authority order does not place in the specification tier. |
| BLT-N08 | FBL-072's rollback deletes artifacts inside the control-data root, while the Definition of Done requires every control-plane write to be journalled or included in evidence. |
| BLT-N09 | FBL-042 has `Failure-injection tests: none` although it is the plan-time overwrite and path-limit barrier, and its sibling FBL-040 tests the analogous fault. |
| BLT-N10 | The acceptance-family table says all 40 `V1-ACC-*` rows are verified "at G3 and later"; four are documentary and satisfied at G1. |

## NOTE

- The path-policy self-test prints its proofs in the order 1, 2, 5, 3, 4. Cosmetic, but an operator
  reading the transcript at FBL-001 inspection will read it as a skipped test.
- The evidence standard lists ten evidence *types*; many rung evidence packages name artifacts
  outside that list. Harmless if the list is non-exhaustive, but the standard does not say so.

---

## Proposed new operator decisions

Three defects above cannot be closed by change control alone, because they are choices about the
repository and the deployment rather than specification errors. **They are proposed, not made.**

| Proposed | Question | Forced by | Suggested `blocks_gate` |
| --- | --- | --- | --- |
| **OD-025** | Where may live-gate evidence and live adapter configuration exist, and what redaction applies before commit? | BLT-B03, BLT-M10 | `dry_run` |
| **OD-026** | May the G5 pilot zone reside on the NAS? If yes, SAF-006 must be amended; if no, FBL-073 cannot measure the real destination. | BLT-B04 | `pilot` |
| **OD-027** | When is the authoritative destination characterized, and under whose approval? | BLT-B05 | `live` |

OD-026 cannot be folded into OD-023, which is scoped to G4 plan promotability.

## Consistency with the readiness map

This report and `docs/proposals/g3-readiness-map.md` are consistent: the map reports the *stated*
blocking relationships, and this report records that several of those relationships are **missing**
(BLT-B02, BLT-B08, BLT-M02, BLT-M03). The map is therefore optimistic — the true blocked set is
larger than it shows. That discrepancy is itself finding BLT-B08 and is not a defect in the map.

## Recommended order of correction

1. **BLT-B03 and BLT-B04** — policy and safety contradictions that block the entire live path and
   cannot be fixed inside a rung.
2. **BLT-B01 and BLT-B02** — they change the ladder's shape.
3. **BLT-B06 and BLT-B08** — mechanical, and BLT-B06 should be closed by adding the reverse
   direction to the validator so it cannot recur.
4. Everything else.
