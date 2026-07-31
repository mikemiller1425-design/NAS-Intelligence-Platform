# One Rung Implementation Prompt

## Role
Implement exactly one approved rung from the build ladder.

## Inputs
- One rung definition.
- Its prerequisites and evidence requirements.
- Current repository state.

## Authority
- Implement only the named rung.
- Update only files required by that rung.

## Prohibitions
- Do not jump ahead to later rungs.
- Do not authorize live NAS mutation outside the rung scope.
- Do not modify unrelated docs or policy.

## Required output
- A summary of changes.
- Verification performed.
- Remaining blockers.

## Stop condition
- The rung is complete and ready for inspection.
