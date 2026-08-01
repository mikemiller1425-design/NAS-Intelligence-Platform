# Pilot Run Playbook

## Purpose
Validate the full workflow on copied data before any live NAS mutation is authorized.

## Operating rules
- Copy before any destructive retirement decision.
- Pilot data is isolated from originals.
- No permanent deletion.
- No source overwrite.
- No silent collision handling.
- Any cleanup proposal remains pending separate approval.

## Authorization required

This playbook describes **how** to run the copied-pilot stage. It does not authorize running it.

Executing anything in this document requires a current, dated, operator-signed authorization record for gate **G5 `pilot`**, per `docs/05-governance/gate-model.md`. Absence of an authorization record is a prohibition, not a gap.

## Preconditions
- Dry-run results are reviewed.
- Fixture tests pass.
- Pilot dataset is selected and documented.
- Destination roots for the pilot are isolated and non-authoritative.
- Rollback plan exists before the first pilot mutation.

## Steps
1. Copy the pilot sample into the isolated pilot zone.
2. Re-run inventory and classification on the copied corpus.
3. Execute approved copy-only or copy-then-verify operations.
4. Verify hashes, counts, and destination paths.
5. Compare pilot outcomes with expected plan outputs.
6. Record exceptions and remediation items.
7. Freeze evidence and decide whether to advance.

## Stop conditions
- Any hash mismatch.
- A copy lands outside the pilot zone.
- A collision would overwrite an existing item.
- Journal writes fail.
- The operator revokes approval or requests pause.

## Required evidence
- Pilot dataset manifest.
- Approved plan snapshot.
- Execution journal.
- Verification report.
- Exception list.
- Rollback drill record.
