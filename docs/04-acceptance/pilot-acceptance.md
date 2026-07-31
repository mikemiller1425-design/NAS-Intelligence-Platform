# Pilot Acceptance

Pilot acceptance defines measurable success for a **copied-data** pilot before any limited live pilot.

## Required pilot corpus characteristics

The pilot dataset should include (synthetic fixtures preferred for sensitive cases):

- common images
- common videos
- documents
- structured data (e.g., CSV/JSON samples)
- duplicate samples (exact-hash pairs)
- conflicting classification samples
- unknown formats
- permission-error sample
- sensitive sample using synthetic fixtures where possible

## Acceptance table

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| PILOT-001 | Pilot uses copied data, not authoritative originals. | Review dataset provenance and storage location. | Pilot dataset manifest | BLOCKER | Pilot-run playbook |
| PILOT-002 | Pilot corpus is isolated from production sources. | Confirm location and access separation. | Path inventory | BLOCKER | Pilot-run playbook |
| PILOT-003 | Every pilot operation comes from an approved immutable plan. | Attempt post-approval edit; confirm rejection. | Plan hash, approval snapshot | BLOCKER | Operation model |
| PILOT-004 | Hash verification succeeds for all copied items. | Compare pre/post hashes. | Verification report | BLOCKER | Validation / duplicate model |
| PILOT-005 | Collisions are reported and never overwrite. | Introduce name-collision fixture. | Collision report | BLOCKER | Operation model |
| PILOT-006 | Rollback is demonstrated on pilot data. | Execute rollback drill. | Rollback evidence bundle | MAJOR | Rollback playbook |
| PILOT-007 | Operator reviews exact plan and exceptions before expansion. | Capture approval and review notes. | Approval log | BLOCKER | Change control |
| PILOT-008 | Pilot stops on threshold breach or unexpected state. | Simulate error-threshold breach. | Stop-condition log | BLOCKER | Live/incident playbooks |
| PILOT-009 | Conflicts and low-confidence items land in review, not silent destinations. | Include conflict fixtures. | Review queue export | BLOCKER | Rule model |
| PILOT-010 | Exact duplicates group by cryptographic hash, not filename. | Include same-name different-hash and same-hash different-name fixtures. | Duplicate report | BLOCKER | Duplicate model |
| PILOT-011 | Protected destination overwrite remains blocked. | Attempt write into protected fixture vault path. | Safety test log | BLOCKER | ADR-011 |
| PILOT-012 | Restart/resume does not duplicate completed copies. | Interrupt mid-batch and resume. | Checkpoint + destination inventory | BLOCKER | Lifecycle / operation model |
| PILOT-013 | Unresolved/unknown formats remain preserved and listed. | Include unknown extension fixture. | Unresolved report | MAJOR | Inventory / taxonomy |
| PILOT-014 | Reports are understandable without chat history. | Independent reader review. | Pilot completion package | MAJOR | Evidence standard |

## Pass rule

All BLOCKER rows must pass. MAJOR rows must pass or have an explicit operator waiver recorded in governance before any live gate is considered.
