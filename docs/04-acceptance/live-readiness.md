# Live Readiness Ladder

Distinguish stages carefully. Completing an earlier stage does **not** authorize a later stage.

| Stage | Meaning | Authorized mutations |
| --- | --- | --- |
| Blueprint complete | Intent, specs, architecture, acceptance, playbooks, handoffs exist and are internally consistent | None |
| Implementation complete | Build Ladder rungs implemented and inspected per evidence standard | Fixture paths only unless a later gate says otherwise |
| Dry-run ready | Engine can evaluate rules and produce plans without filesystem mutation | None (plans only) |
| Pilot ready | Copied pilot corpus can run full workflow with verification and rollback drill | Pilot zone only |
| Live migration ready | Bounded live batches allowed under approved plan, snapshots confirmed, thresholds set | Approved live batch only |
| Migration complete | Every in-scope source item has a final disposition; reconciliation passes | Maintenance proposals still gated |
| Operationally trustworthy | Continuous ingestion/maintenance proven under monitoring | Per maintenance policy |

## Live-readiness acceptance (pre-batch)

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| LIVE-001 | Foundation approval exists and is current. | Check approval ledger and version marker. | Approval record, `FOUNDATION_VERSION.md` | BLOCKER | Definition of ready |
| LIVE-002 | Snapshot or equivalent recovery coverage is documented. | Review recovery readiness. | Recovery checklist | BLOCKER | Live-data policy |
| LIVE-003 | Exact source and destination roots are confirmed. | Compare inventory with OD-001 resolution. | Source inventory, open-decisions | BLOCKER | Migration docs |
| LIVE-004 | Batch thresholds are calibrated and approved. | Review threshold config and sign-off. | Threshold sheet | BLOCKER | Change control |
| LIVE-005 | Control-data locations are outside recursive source scans. | Validate path topology. | Paths document | BLOCKER | Storage / taxonomy |
| LIVE-006 | Copy-first behavior is defined per phase. | Inspect live-data policy and playbook. | Policy docs | BLOCKER | Live migration playbook |
| LIVE-007 | Quarantine retention is defined before any cleanup. | Review retention policy. | Retention policy | MAJOR | Live-data policy |
| LIVE-008 | Operator confirms live structure versus intended structure. | Compare planned and intended taxonomy. | OD-013 record | MAJOR | Governance |
| LIVE-009 | Copied pilot acceptance (PILOT-*) is green. | Review pilot evidence bundle. | Pilot reports | BLOCKER | Pilot acceptance |
| LIVE-010 | Protected vault overwrite remains disabled by default. | Inspect config and attempt collision fixture. | Safety test evidence | BLOCKER | ADR-011 |
| LIVE-011 | Source retirement remains separately gated. | Confirm retirement disabled unless approved. | Thresholds / plan flags | BLOCKER | Operation model |
| LIVE-012 | Sentinel cannot authorize the live batch. | Review sentinel authority docs and config. | Sentinel playbook | BLOCKER | Sentinel architecture |

## Explicit non-authorization

- Blueprint completeness ≠ implementation authorization
- Implementation completeness ≠ dry-run authorization against live mounts
- Dry-run success ≠ pilot authorization
- Pilot success ≠ live migration authorization
- Live batch success ≠ unrestricted reorganization or deletion authorization
