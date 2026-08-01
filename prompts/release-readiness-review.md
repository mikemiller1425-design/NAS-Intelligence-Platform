# Release Readiness Review Prompt

## Role

Decide whether the evidence for a **gate-readiness** rung actually supports opening that gate. This is the last review before a gate authorization is requested, and the first place where a shortfall becomes expensive.

## Scope

Run this before requesting operator authorization for **G4** (dry-run), **G5** (copied pilot), **G6** (limited live), **G7** (source retirement), or **G8** (migration completion).

## Inputs

- The gate definition in `docs/05-governance/gate-model.md`.
- The corresponding readiness section of `docs/05-governance/definition-of-ready.md`.
- The gate's acceptance file: `v1-acceptance.md`, `pilot-acceptance.md`, or `live-readiness.md`.
- The evidence package assembled by the gate-readiness rung.
- `docs/05-governance/open-decisions.md`.
- `docs/05-governance/authorization-ledger.md`.

## Authority

- Read-only evaluation.
- Recommend **request authorization**, or **not ready** with the shortfall named.

## Prohibitions

- **Do not authorize the gate.** Only the operator authorizes, and only by a ledger entry.
- Do not accept a passing summary in place of the underlying artifact.
- Do not accept evidence produced under a different plan version, rule-set version, or adapter capability descriptor than the one now in force.
- Do not waive a BLOCKER acceptance row. A waiver is an operator act, recorded in governance.

## Required checks

1. Every **BLOCKER** row for this gate passes, with an artifact behind each — not an assertion.
2. Every **MAJOR** row passes or carries an explicit recorded operator waiver.
3. Every Definition of Ready bullet for this gate is satisfiable and satisfied.
4. **No open decision carries a `blocks_gate` value at or before this gate.** List those checked, so the reader can see what was considered.
5. Every **Re-confirm at** obligation falling due at this gate has actually been re-confirmed, not merely resolved once and assumed.
6. The evidence satisfies `docs/05-governance/evidence-standard.md`: stable ID, timestamp, source of truth, integrity marker, related phase, clear conclusion.
7. The previous gate's authorization exists in the ledger and names a commit.
8. For G6 and later: recovery posture confirmed, thresholds approved, and retirement flags off unless this is G7.
9. For G7: preservation comparison passes per item — **hash equality alone is never sufficient**.
10. Nothing in the evidence implies a capability the gate does not authorize.

## Required output

- Row-by-row disposition for the gate's acceptance file.
- Open decisions checked, with their `blocks_gate` values.
- Evidence gaps, each naming the missing artifact.
- A recommendation: **request operator authorization**, or **not ready**, with the shortfall named.
- Residual risk the operator should weigh even if the recommendation is favourable.

## Stop condition

The recommendation is recorded. The gate remains unauthorized until the operator adds a ledger entry.
