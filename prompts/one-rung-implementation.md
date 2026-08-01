# One Rung Implementation Prompt

## Role
Implement exactly one approved rung from the build ladder.

## Preconditions
- A frozen Build Ladder exists (gate G2 complete).
- **This specific rung ID is explicitly authorized** by the operator (gate G3). Authorization of rung N never authorizes rung N+1.
- The rung's `live NAS access in scope` field reads **no**.
- No open decision carries `blocks_gate: implementation` for this rung's subject matter.

## Inputs
- One rung definition.
- Its prerequisites and evidence requirements.
- Current repository state.

## Authority
- Implement only the named rung.
- Update only files required by that rung.

## Prohibitions
- Do not jump ahead to later rungs.
- Do not access, mount, scan, or mutate any live NAS path. Rung implementation is fixture-only at gate G3; live access is not available inside rung scope either.
- Do not modify unrelated docs or policy.

## Required output
- A summary of changes.
- Verification performed.
- Remaining blockers.

## Stop condition
- The rung is complete and ready for inspection.
