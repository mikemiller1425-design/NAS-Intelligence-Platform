# Handoff 002 — Audit Resolution

## Purpose

Define how Cursor (Repository Blueprint Engineer) or Claude may resolve **approved** audit findings after the independent foundation audit.

## Preconditions

- `docs/audits/foundation-v1-audit.md` exists
- Operator (or designated authority) has marked which findings must be fixed before Foundation approval

## Authority

- May edit blueprint documents, config examples, prompts, and governance to remediate findings
- May not begin production implementation
- May not access or mutate the live NAS
- May not “resolve” BLOCKERs by deleting the requirement

## Process

1. Import each required finding into a short resolution log (in the audit file or a dated appendix).
2. For each finding: state the change made, files touched, and residual risk.
3. Re-run continuous verification checks from the foundation assignment (§20).
4. Update `CHANGELOG.md` and `PROJECT_STATUS.md`.
5. If Foundation version advances, update `FOUNDATION_VERSION.md`.

## Prohibitions

- Do not implement engine code as “audit resolution”
- Do not enable live mode
- Do not treat MINOR notes as optional if the operator marked them required
- Do not hand Build Ladder generation to Claude until Foundation approval is explicit

## Required output

- Updated blueprint addressing approved BLOCKER and MAJOR findings
- Resolution notes linked to finding IDs
- Remaining open decisions still listed in `open-decisions.md`

## Stop condition

All approved BLOCKER and MAJOR findings resolved or explicitly waived by the operator; repository ready for Foundation approval decision.
