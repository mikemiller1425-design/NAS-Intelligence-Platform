# Definition of Ready

A phase is ready only when its own prerequisites are complete. Readiness for one phase does not authorize the next phase.

## Blueprint ready
- Source manual is in the repository.
- Active docs exist for intent, policy, specification, architecture, acceptance, governance, migration, handoffs, future registry, and prompts.
- No open BLOCKER decision prevents interpretation of the work.

## Dry-run ready
- Source roots are confirmed.
- Read-only inventory scope is defined.
- Rule set version is frozen.
- Control-data location is outside recursively scanned source paths.

## Pilot ready
- Dry-run output is reviewed.
- Fixture tests pass.
- Pilot dataset is selected and isolated.
- Rollback steps are written and checked.

## Live ready
- Copied pilot evidence exists.
- Recovery posture is documented.
- Thresholds and source-retirement conditions are approved.
- Exact roots and copy-versus-move behavior for the phase are frozen.
