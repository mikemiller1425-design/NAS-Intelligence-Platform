# V1 Acceptance — Execution-Verifiable Requirements

Requirements that can only be verified by **running software**. Each row carries the gate it blocks (`implementation`, `dry_run`, `pilot`, `live`, `retirement`, `migration_completion`), per `docs/05-governance/gate-model.md`.

Documentation-verifiable requirements live in `docs/04-acceptance/foundation-acceptance.md`. **No row in this file blocks Foundation approval** — that separation is the resolution of audit finding FND-B001. Requiring these rows at Foundation stage was circular: they need implemented software, and implementation was blocked until Foundation approval.

Blueprint completeness authorizes nothing. Neither does completing this file.

Where a requirement had a documentary half and an execution half, the documentary half moved to `foundation-acceptance.md` and the execution half kept its original ID here. No requirement was deleted.

## Inventory and provenance

| ID | Behavior | Verification | Evidence | Severity | Gate | Related spec |
| --- | --- | --- | --- | --- | --- | --- |
| V1-ACC-001 | Read-only inventory never mutates source bytes or timestamps intentionally. | Repeat a scan; compare source samples before/after. | Inventory manifest, source sample hashes | BLOCKER | `implementation` | inventory-model, principles |
| V1-ACC-002 | Every in-scope file receives a stable identity or documented error/unreadable state. | Compare manifest completeness to source counts. | Manifest, exception log | BLOCKER | `implementation` | domain-model, inventory-model, file-identity-model |
| V1-ACC-003 | Provenance captures source root, relative path, and discovery metadata. | Inspect FileRecord/ProvenanceRecord fields in a produced export. | Inventory export | BLOCKER | `implementation` | domain-model, inventory-model |
| V1-ACC-004 | Permission errors and unreadable items are reported, never silently skipped. | Include permission-denied fixture. | Unresolved/error report | BLOCKER | `implementation` | inventory-model |
| V1-ACC-005 | Identity-hazard conditions stop and route to review rather than guessing. | Case-collision, Unicode-normalization, hard-link, and same-path-replacement fixtures. | Stop/review log | BLOCKER | `implementation` | file-identity-model |
| V1-ACC-006 | Concurrent source modification during hashing or copying is detected and the item is failed, not silently accepted. | Concurrent-modification fixture. | Change-token mismatch report | BLOCKER | `implementation` | file-identity-model |

## Duplicates

| ID | Behavior | Verification | Evidence | Severity | Gate | Related spec |
| --- | --- | --- | --- | --- | --- | --- |
| V1-ACC-010 | Exact duplicates are hash-backed and grouped without deletion. | Identical-hash fixtures group; no auto-delete. | Duplicate group report | BLOCKER | `implementation` | duplicate-model, ADR-004 |
| V1-ACC-011 | Duplicate decisions cannot rely on filename alone. | Same-name different-hash fixtures remain distinct. | Duplicate report | BLOCKER | `implementation` | duplicate-model |
| V1-ACC-012 | Near-duplicates remain separate review candidates, not exact duplicates. | Visually similar byte-distinct fixtures. | Review queue / similarity notes | MAJOR | `implementation` | duplicate-model, FR-007 |

## Classification and rules

| ID | Behavior | Verification | Evidence | Severity | Gate | Related spec |
| --- | --- | --- | --- | --- | --- | --- |
| V1-ACC-020 | Every classification proposal references rule ID, rule set version, evidence, confidence, and explanation. | Inspect dry-run outputs. | Rule-match report | BLOCKER | `implementation` | rule-model, ADR-006 |
| V1-ACC-021 | Conflicts and low-confidence items enter manual review. | Ambiguous/conflict fixtures. | Review queue, conflict report | BLOCKER | `implementation` | rule-model, lifecycle-model |
| V1-ACC-022 | Multi-destination matches follow the documented conflict resolution; no silent multi-canonical ownership. | Multi-match fixtures. | Conflict report | BLOCKER | `implementation` | rule-model, domain invariants |
| V1-ACC-023 | Sensitive identity handling requires explicit policy and human confirmation; disabled by default until OD-003. | Identity-candidate fixtures. | Review hold, policy check | BLOCKER | `implementation` | privacy, open-decisions |
| V1-ACC-024 | AI/content detections are evidence only; confidence thresholds are configurable. | Threshold config change alters routing. | Thresholds config, reports | MAJOR | `implementation` | principles, rule-model |
| V1-ACC-025 | A rule set whose ordering differs in file order but not in priority/specificity produces byte-identical decisions. | Reorder rules in the file; re-evaluate the same fixtures. | Decision diff showing no change | BLOCKER | `implementation` | rule-model |
| V1-ACC-026 | An attempt to activate a provisional rule with an auto-executable outcome is rejected at config load. | Load each negative example rule set. | Validation rejection log with reason codes | BLOCKER | `implementation` | rule-model, FND-B003 |

## Dry-run, planning, and execution safety

| ID | Behavior | Verification | Evidence | Severity | Gate | Related spec |
| --- | --- | --- | --- | --- | --- | --- |
| V1-ACC-030 | Dry-run is default and produces plans with no filesystem mutation. | Run dry-run; destination tree unchanged. | Plan artifact, destination inventory | BLOCKER | `implementation` | ADR-009, operation-model |
| V1-ACC-031 | Operation plans are immutable after approval; edits require a new plan. | Attempt post-approval mutation. | Plan hash/version history | BLOCKER | `implementation` | operation-model |
| V1-ACC-032 | Execution revalidates source preconditions immediately before action. | Drift source between plan and execute. | Precondition failure log | BLOCKER | `implementation` | operation-model, file-identity-model |
| V1-ACC-033 | Destination collisions never overwrite silently; protected vaults blocked by default. | Collision + protected-path fixtures. | Collision report, safety log | BLOCKER | `implementation` | ADR-011, operation-model |
| V1-ACC-034 | Successful copy requires post-operation hash verification. | Corrupt transfer fixture; confirm failure. | Verification report | BLOCKER | `implementation` | validation, ADR-002 |
| V1-ACC-035 | Source retirement requires verification and explicit approval; permanent deletion unavailable in V1. | Attempt unauthorized retire/delete. | Policy + rejection log | BLOCKER | `implementation`, re-verified at `retirement` | safety-acceptance, live-data-policy |
| V1-ACC-036 | Operations are idempotent; resume does not duplicate completed copies. | Interrupt and resume batch at every documented interruption point. | Checkpoint + destination inventory | BLOCKER | `implementation` | durability-and-recovery-model, ADR-013 |
| V1-ACC-037 | Failed operations remain inspectable with ErrorRecord/AuditEvent. | Inject failure; query state. | Error/audit export | BLOCKER | `implementation` | domain-model, observability |
| V1-ACC-038 | Frontend/console cannot authorize filesystem mutation. | Attempt UI-only approval path without backend authorization. | Permission tests | BLOCKER | `implementation` | ADR-014, permission-model, approval-binding-model |
| V1-ACC-039 | A replayed, expired, revoked, or already-consumed approval is rejected with a specific reason code. | Replay each approval-failure fixture. | Rejection log with reason codes | BLOCKER | `implementation` | approval-binding-model |

## Persistence and recovery

| ID | Behavior | Verification | Evidence | Severity | Gate | Related spec |
| --- | --- | --- | --- | --- | --- | --- |
| V1-ACC-045 | Every row of the crash-state table reproduces the documented recovery outcome. | Fault-inject at each interruption point. | Crash-recovery matrix results | BLOCKER | `implementation` | durability-and-recovery-model |
| V1-ACC-046 | A truncated or corrupt journal record is detected and does not silently vanish. | Truncated-tail and corrupt-mid-file journal fixtures. | Recovery log | BLOCKER | `implementation` | durability-and-recovery-model |
| V1-ACC-047 | Derived SQLite state can be rebuilt from the authoritative journal alone. | Delete the database; replay. | Rebuilt-state comparison | BLOCKER | `implementation` | durability-and-recovery-model, ADR-005 |

## Comparison, unresolved, privacy

| ID | Behavior | Verification | Evidence | Severity | Gate | Related spec |
| --- | --- | --- | --- | --- | --- | --- |
| V1-ACC-040 | Source/destination comparison reports exist for approved batches, covering preservation fidelity and not hash equality alone. | Produce comparison after pilot copy. | Comparison report | BLOCKER | `pilot` | operation-model, preservation-model |
| V1-ACC-041 | Unresolved items are visible and governed, never silently discarded. | Unknown-format fixtures. | Unresolved inventory | BLOCKER | `implementation` | product-intent, taxonomy |
| V1-ACC-042 | Logs redact sensitive paths when required. | Log sample review. | Redaction samples | BLOCKER | `implementation` | security-and-privacy, git-policy |
| V1-ACC-044 | Preservation-profile properties marked `required` are verified per item; `unsupported_reported` properties are reported, not silently dropped. | Run the preservation comparison across the fidelity fixture set. | Preservation comparison report | BLOCKER | `implementation` | preservation-model |

## Pilot, live readiness, topology, completion

| ID | Behavior | Verification | Evidence | Severity | Gate | Related spec |
| --- | --- | --- | --- | --- | --- | --- |
| V1-ACC-050 | Copied pilot succeeds before any limited live pilot is considered. | Execute pilot acceptance (PILOT-*). | Pilot package | BLOCKER | `live` | pilot-acceptance, ADR-010 |
| V1-ACC-052 | Raspberry Pi is Sentinel only; Mac mini (or equivalent) is primary worker. | Sentinel authority tests. | Authority test results | BLOCKER | `implementation` | execution-topology |
| V1-ACC-053 | Every source item reaches organized, retained, quarantined, unresolved, or failed disposition. | Reconciliation totals. | Reconciliation report | BLOCKER | `migration_completion` | lifecycle-model, OD-021 |

## Relocated requirements

These rows were documentation-verifiable and moved to `docs/04-acceptance/foundation-acceptance.md` under their original IDs. They are **not** deleted, and they are **not** evaluated here.

| ID | New home | Reason |
| --- | --- | --- |
| V1-ACC-043 | foundation-acceptance | "Review privacy policy and adapter defaults" — document review |
| V1-ACC-051 | foundation-acceptance | "Confirm live-readiness distinctions" — document review |
| V1-ACC-054 | foundation-acceptance | "Review maintenance playbook vs FR-012" — document review |
| V1-ACC-055 | foundation-acceptance | "Review matrix and v1-scope/exclusions" — document review |

## Pass rules by gate

This document is **not** a Foundation-approval checklist.

- **Foundation (G1)** is governed by `docs/04-acceptance/foundation-acceptance.md` and `docs/04-acceptance/safety-acceptance.md`. No row in this file blocks Foundation approval.
- **Implementation (G3):** every row with `Gate = implementation` must pass on synthetic fixtures before the corresponding rung is inspected as complete. MAJOR rows must pass or carry an explicit operator waiver recorded in `docs/05-governance/open-decisions.md`.
- **Dry-run (G4), Pilot (G5), Live (G6), Retirement (G7), Migration completion (G8):** rows carrying those gate values are verified at that gate and at no earlier one.

Passing every row in this file authorizes no gate. Authorization is a separate, dated, operator-signed record naming the gate ID.
