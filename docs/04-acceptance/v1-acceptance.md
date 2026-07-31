# V1 Acceptance

Stable acceptance requirements for the NAS Intelligence Platform. Each requirement includes ID, behavior, verification method, expected evidence, severity, and related specification.

Blueprint completeness does **not** authorize implementation or live NAS mutation.

## Inventory and provenance

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| V1-ACC-001 | Read-only inventory never mutates source bytes or timestamps intentionally. | Repeat a scan; compare source samples before/after. | Inventory manifest, source sample hashes | BLOCKER | inventory-model, principles |
| V1-ACC-002 | Every in-scope file receives a stable identity or documented error/unreadable state. | Compare manifest completeness to source counts. | Manifest, exception log | BLOCKER | domain-model, inventory-model |
| V1-ACC-003 | Provenance captures source root, relative path, and discovery metadata. | Inspect FileRecord/ProvenanceRecord fields. | Inventory export | BLOCKER | domain-model, inventory-model |
| V1-ACC-004 | Permission errors and unreadable items are reported, never silently skipped. | Include permission-denied fixture. | Unresolved/error report | BLOCKER | inventory-model |

## Duplicates

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| V1-ACC-010 | Exact duplicates are hash-backed and grouped without deletion. | Identical-hash fixtures group; no auto-delete. | Duplicate group report | BLOCKER | duplicate-model, ADR-004 |
| V1-ACC-011 | Duplicate decisions cannot rely on filename alone. | Same-name different-hash fixtures remain distinct. | Duplicate report | BLOCKER | duplicate-model |
| V1-ACC-012 | Near-duplicates remain separate review candidates, not exact duplicates. | Visually similar byte-distinct fixtures. | Review queue / similarity notes | MAJOR | duplicate-model, FR-007 |

## Classification and rules

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| V1-ACC-020 | Every classification proposal references rule ID, rule version, evidence, confidence, and explanation. | Inspect dry-run outputs. | Rule-match report | BLOCKER | rule-model, ADR-006 |
| V1-ACC-021 | Conflicts and low-confidence items enter manual review. | Ambiguous/conflict fixtures. | Review queue, conflict report | BLOCKER | rule-model, lifecycle-model |
| V1-ACC-022 | Multi-destination matches follow documented conflict resolution; no silent multi-canonical ownership. | Multi-match fixtures. | Conflict report | BLOCKER | rule-model, domain invariants |
| V1-ACC-023 | Sensitive identity handling requires explicit policy and human confirmation; disabled by default until OD-003. | Identity-candidate fixtures. | Review hold, policy check | BLOCKER | privacy, open-decisions |
| V1-ACC-024 | AI/content detections are evidence only; confidence thresholds are configurable. | Threshold config change alters routing. | Thresholds config, reports | MAJOR | principles, rule-model |

## Dry-run, planning, and execution safety

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| V1-ACC-030 | Dry-run is default and produces plans with no filesystem mutation. | Run dry-run; destination tree unchanged. | Plan artifact, destination inventory | BLOCKER | ADR-009, operation-model |
| V1-ACC-031 | Operation plans are immutable after approval; edits require a new plan. | Attempt post-approval mutation. | Plan hash/version history | BLOCKER | operation-model |
| V1-ACC-032 | Execution revalidates source preconditions immediately before action. | Drift source between plan and execute. | Precondition failure log | BLOCKER | operation-model |
| V1-ACC-033 | Destination collisions never overwrite silently; protected vaults blocked by default. | Collision + protected-path fixtures. | Collision report, safety log | BLOCKER | ADR-011, operation-model |
| V1-ACC-034 | Successful copy requires post-operation hash verification. | Corrupt transfer fixture; confirm failure. | Verification report | BLOCKER | validation, ADR-002 |
| V1-ACC-035 | Source retirement requires verification + explicit approval; permanent deletion unavailable in V1. | Inspect gates and attempt unauthorized retire/delete. | Policy + rejection log | BLOCKER | safety-acceptance, live-data-policy |
| V1-ACC-036 | Operations are idempotent; resume does not duplicate completed copies. | Interrupt and resume batch. | Checkpoint + destination inventory | BLOCKER | lifecycle-model, ADR-013 |
| V1-ACC-037 | Failed operations remain inspectable with ErrorRecord/AuditEvent. | Inject failure; query state. | Error/audit export | BLOCKER | domain-model, observability |
| V1-ACC-038 | Frontend/console cannot authorize filesystem mutation. | Attempt UI-only approval path without backend authz. | Permission tests | BLOCKER | ADR-014, permission-model |

## Comparison, unresolved, privacy

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| V1-ACC-040 | Source/destination comparison reports exist for approved batches. | Produce comparison after pilot copy. | Comparison report | BLOCKER | operation-model, data-architecture |
| V1-ACC-041 | Unresolved items are visible and governed, never silently discarded. | Unknown-format fixtures. | Unresolved inventory | BLOCKER | product-intent, taxonomy |
| V1-ACC-042 | Secrets are absent from Git; logs redact sensitive paths when required. | Repo secret scan + log sample review. | Scan results, redaction samples | BLOCKER | security-and-privacy, git-policy |
| V1-ACC-043 | Private/explicit media stay within local processing and vault boundaries. | Review privacy policy and adapter defaults. | Privacy docs, config | MAJOR | security-and-privacy |

## Pilot, live readiness, topology, completion

| ID | Behavior | Verification | Evidence | Severity | Related spec |
| --- | --- | --- | --- | --- | --- |
| V1-ACC-050 | Copied pilot succeeds before any limited live pilot is considered. | Execute pilot acceptance (PILOT-*). | Pilot package | BLOCKER | pilot-acceptance, ADR-010 |
| V1-ACC-051 | Live migration readiness is a separate ladder stage (LIVE-*). | Confirm live-readiness distinctions. | live-readiness.md | BLOCKER | live-readiness |
| V1-ACC-052 | Raspberry Pi is Sentinel only; Mac mini (or equivalent) is primary worker. | Review topology ADRs and sentinel authority tests. | ADR-007/008, sentinel playbook | BLOCKER | execution-topology |
| V1-ACC-053 | Every source item reaches organized, retained, quarantined, unresolved, or failed disposition. | Reconciliation totals. | Reconciliation report | BLOCKER | lifecycle-model |
| V1-ACC-054 | Post-migration maintenance foundation is defined without unattended live watchers. | Review maintenance playbook vs FR-012. | post-migration-maintenance.md | MAJOR | operations, future-registry |
| V1-ACC-055 | Traceability covers significant source concepts; Future Registry does not leak into V1 scope. | Review matrix and v1-scope/exclusions. | traceability-matrix.md | BLOCKER | migration docs |

## Pass rule

All BLOCKER requirements must pass before Foundation approval can recommend implementation readiness. MAJOR items must pass or carry an explicit operator waiver.
