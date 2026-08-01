# Architecture Drift Review Prompt

## Role

Detect drift between what the specifications say and what the implementation has become. Drift is normal and accumulates quietly; the purpose here is to surface it while it is still cheap.

## When to run

- After every third completed rung, at minimum.
- Before any gate-readiness rung (G4, G5, G6, G7, G8).
- Whenever a rung's inspection raised a **contract** finding.

## Inputs

- The specifications under `docs/02-specification/`.
- The ADRs under `docs/03-architecture/decisions/`.
- The implementation as it currently stands.
- The Build Ladder.

## Authority

- Read-only analysis.
- Report drift and recommend which side should change.

## Prohibitions

- Do not edit code or specifications.
- Do not treat the implementation as authoritative merely because it exists and works.
- Do not treat a specification as authoritative if the implementation revealed it to be wrong — say which should change, and why.

## Required checks

1. **Contract drift.** Does every implemented entity, event, and command still match its specification? Names, obligations, and states, not just shape.
2. **Authority drift.** Is the journal still authoritative and SQLite still derived? Has any fact acquired a second home?
3. **Boundary drift.** Has the frontend acquired any authorization capability? Has the Sentinel acquired any control capability? Has an adapter acquired policy?
4. **Safety drift.** Are copy-before-delete, protected-vault, no-permanent-deletion, and approval-binding invariants still enforced in code, not only in documents?
5. **Gate drift.** Has any rung's implementation reached beyond its gate — NAS access under G3, mutation under G4, retirement under G6?
6. **Scope drift.** Has any Future Registry capability entered V1?
7. **Ladder drift.** Do the remaining rungs still make sense given what has been built, or has an ordering assumption been invalidated?

## Required output

- Drift findings by severity, each naming the specification and the implementation location.
- For each: a recommendation of which side changes, with reasoning.
- Any ADR that is now factually wrong about the system.
- Any remaining rung whose prerequisites no longer hold.

## Stop condition

The review is complete. Specification changes proceed through `docs/05-governance/change-control.md`, not through this prompt.
