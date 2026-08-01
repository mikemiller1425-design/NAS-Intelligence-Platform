# Foundation Resolution Verification

## Provenance of this document

An independent verification pass was performed against commit `34620db3b765cf757329b28b715f818d069e02d4`, which carried the resolution of the twelve findings in `docs/audits/foundation-v1-audit.md`.

At the time this correction began, this file did not exist in the repository, on disk, or anywhere in Git history. As with the original audit, the verifier's findings were delivered to the resolution engineer out-of-band rather than committed. This document therefore records **only** the finding that was delivered — **VER-B001** — together with its correction.

**It does not record a verdict on the verification pass as a whole.** No statement here should be read as the verifier having cleared any other finding, nor as an overall pass. The verifier's full report, if one exists, has not been seen by the resolution engineer.

**This document does not approve Foundation 1.0.**

## VER-B001 — Stale gate numbering in Foundation acceptance

**Severity:** BLOCKER
**Raised against:** `34620db`
**Status:** RESOLVED
**Gate affected:** `foundation`
**Ready for independent re-review:** yes

### Problem

`docs/04-acceptance/foundation-acceptance.md` referenced gates under a superseded numbering scheme. It described Foundation acceptance as **gate G0**, which does not exist in the canonical ladder, and assigned execution validation and fixture construction to **G2**, which is Build Ladder Generation rather than Fixture-Only Implementation.

The canonical mapping in `docs/05-governance/gate-model.md` is:

| Gate | Name | `blocks_gate` |
| --- | --- | --- |
| G1 | Foundation Approval | `foundation` |
| G2 | Build Ladder Generation | `build_ladder` |
| G3 | Fixture-Only Implementation | `implementation` |
| G4 | Dry-Run Readiness | `dry_run` |
| G5 | Copied-Pilot Readiness | `pilot` |
| G6 | Limited-Live Readiness | `live` |
| G7 | Source-Retirement Readiness | `retirement` |
| G8 | Migration Completion | `migration_completion` |

### Cause

The gate ladder was authored initially as a G0-based scheme (G0 = Foundation through G7 = Migration Completion) and renumbered to the canonical G1-based scheme during audit resolution. `gate-model.md` was renumbered; `foundation-acceptance.md` had already been written against the old scheme and was not re-checked afterwards.

The document was therefore internally mixed: its earlier sections used the old numbering, while sections appended after the renumbering used the new one. That mixture is why the defect survived the original self-review — the file contained both correct and incorrect numbering, and no check compared gate references against the canonical mapping.

### Correction

Six references corrected in `docs/04-acceptance/foundation-acceptance.md`:

| Line | Before | After |
| --- | --- | --- |
| 5 | "gate G0 — Foundation Approval" | "gate G1 — Foundation Approval" |
| 9 | "consumed by gate G2 and later" | "consumed by gate G3 (fixture-only implementation) and later" |
| 78 | "build the fixture corpus at G2" | "build the fixture corpus at G3" |
| 116 | "Foundation approval (G0)" | "Foundation approval (G1)" |
| 123 | "evaluated at gate G2 and later" | "evaluated at gate G3 and later" |
| 125 | "Passing G0 does not authorize G1" | "Passing G1 does not authorize G2" |

Line 102 already used the canonical numbering and was left unchanged.

The whole document was then re-read against `gate-model.md`, and all active documentation was swept for unknown gate tokens and mismatched gate name/number pairs.

### Prevention

Four checks were added to `scripts/foundation_self_review.py` so that a future renumbering cannot pass review unnoticed:

| Check | Purpose |
| --- | --- |
| 25 | `gate-model.md` reproduces the canonical G1–G8 mapping exactly, in both its summary table and its section headings. |
| 26 | No unknown gate token (`G0`, `G9`, …) appears in any active document. **This is the check that rejects G0.** |
| 27 | No gate number is bound to another gate's slug or name. |
| 28 | High-signal activity phrases cite the gate that authorizes them — the check that catches a *valid* token used in a semantically wrong place, such as "fixture corpus at G2". |

### Verification evidence

Checks 25–28 were regression-tested in both directions:

- Against the corrected repository: all four pass.
- Against the pre-fix `foundation-acceptance.md` restored from `34620db`: check 26 fails on the three `G0` references and check 28 fails on "fixture corpus at G2". Checks 25 and 27 correctly stay green, since `gate-model.md` was never wrong and no name/slug binding was mismatched.

A check that cannot fail proves nothing, so the failing direction was demonstrated explicitly rather than assumed.

Full suite at the corrected commit: **28/28 pass**, plus the rule contract (schema valid, positive example validates, 47 negative fixtures each rejected for its intended reason).

### Known limits of the added checks

Stated so a re-reviewer does not over-trust them:

- Check 28 judges only the **forward** binding — phrase, then gate token, within one clause. A phrase that *follows* its gate token in reverse order is not covered, because the reverse reading produced false positives on legitimate non-authorization lines such as "Foundation approval (G1) ≠ Build Ladder generation authorization (G2)".
- Check 28 covers a deliberately small phrase set. A valid gate token used in a semantically wrong place, with wording outside that set, remains detectable only by human review.
- `scripts/foundation_self_review.py` is excluded from checks 26–28 over itself, since it must be able to name the tokens it rejects.
- `CHANGELOG.md` and `docs/audits/` are exempt from **check 26 only**, because a changelog and an audit record must be able to quote the superseded token they describe — this document names `G0` a dozen times for exactly that reason. Every normative document remains covered: governance, acceptance, specification, architecture, operations, prompts, config, and the three top-level status files.
- `docs/source/` is excluded throughout as immutable operator source material, and `docs/audits/` is additionally excluded from check 28 because audit prose quotes historical wording verbatim.

The exemptions were verified not to hollow out the check: injecting `gate G0 authorizes nothing` into `gate-model.md` — a normative document — makes check 26 fail as intended.

### Remaining risk

The canonical mapping now lives in two places: `gate-model.md` (authoritative prose) and the `CANON_GATES` table inside the self-review script. Check 25 compares them, so a divergence is caught — but if both were edited together in the same wrong direction, the checks would agree with each other and stay green. The gate model remains the authority; the script is a guard, not a second source of truth.

## Stop

This document is evidence, not authorization. Foundation 1.0 is **not** approved by this file, and no Build Ladder is authorized by it.
