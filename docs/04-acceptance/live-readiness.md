# Live Readiness Ladder

Distinguish stages carefully. Completing an earlier stage does **not** authorize a later stage.

Gate IDs and authorization semantics are defined once, in `docs/05-governance/gate-model.md`. This table restates only the mutation envelope of each gate.

| Gate | Meaning | Authorized mutations |
| --- | --- | --- |
| G1 `foundation` | Intent, specs, architecture, acceptance, playbooks, handoffs exist and are internally consistent | None |
| G2 `build_ladder` | Rung ladder generated and frozen as planning-only | None |
| G3 `implementation` | Named rung implemented and inspected per evidence standard | Synthetic fixture paths only |
| G4 `dry_run` | Engine evaluates rules and produces plans against confirmed roots | None — reads only, plans only. **First gate that touches the real NAS.** |
| G5 `pilot` | Copied pilot corpus runs the full workflow with verification and rollback drill | Isolated pilot zone only |
| G6 `live` | Bounded live batches under an approved plan, snapshots confirmed, thresholds set | Approved live copy batch only; no retirement |
| G7 `retirement` | Verified source items retired under an approved retention policy | Retirement of individually verified items; never deletion |
| G8 `migration_completion` | Every in-scope source item has a final disposition; reconciliation passes | Maintenance proposals still gated |

## Live-readiness acceptance (pre-batch)

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| LIVE-001 | Authorization records exist and are current for every prior gate G1 through G5. | Check the authorization ledger for one dated, operator-signed record per gate. | Authorization records, `FOUNDATION_VERSION.md` | BLOCKER | gate-model, definition-of-ready |
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

- Foundation approval (G1) ≠ Build Ladder generation authorization (G2)
- Build Ladder generation (G2) ≠ implementation authorization for any rung (G3)
- Implementation completeness on fixtures (G3) ≠ dry-run authorization against live mounts (G4)
- Dry-run success (G4) ≠ pilot authorization (G5)
- Pilot success (G5) ≠ live migration authorization (G6)
- Live batch success (G6) ≠ source-retirement authorization (G7)
- Source retirement (G7) ≠ migration-completion declaration (G8)
- Migration completion (G8) ≠ deletion, quarantine cleanup, or autonomous maintenance authorization
