# Lifecycle Model

## Purpose

This document defines the canonical lifecycle states for files and runs. It is the operational state machine used by the specification set. The model is intentionally strict: if a transition is not listed here, it is forbidden.

The platform remains dry-run by default and does not authorize live NAS mutation merely by defining these states.

## File states

The file lifecycle is the source of truth for `FileRecord.inventory_state` and related workflow flags.

### States

- `discovered`
- `inventoried`
- `fingerprinted`
- `metadata_extracted`
- `analysis_pending`
- `analyzed`
- `classification_proposed`
- `review_required`
- `approved`
- `operation_planned`
- `copied`
- `verified`
- `retirement_pending`
- `retired`
- `archived`
- `unresolved`
- `failed`

### State meaning

- `discovered`: the file path has been seen, but not yet normalized or counted.
- `inventoried`: stable identity and source ownership have been recorded.
- `fingerprinted`: at least one approved content hash exists.
- `metadata_extracted`: filesystem, media, document, or structured metadata has been extracted.
- `analysis_pending`: the file awaits rule evaluation or downstream enrichment.
- `analyzed`: metadata and evidence have been collected for classification.
- `classification_proposed`: at least one destination proposal exists.
- `review_required`: the file needs human review before a plan may be approved.
- `approved`: the classification or exception has been approved by policy.
- `operation_planned`: an immutable operation plan exists for the file.
- `copied`: the destination copy has been written.
- `verified`: post-operation verification has passed.
- `retirement_pending`: the approved retention or cleanup phase is pending.
- `retired`: the file has been retired according to a separately approved retention action.
- `archived`: the record has been summarized and archived.
- `unresolved`: the item could not be classified, verified, or otherwise finalized.
- `failed`: processing stopped because a required safety or technical check failed.

### Allowed transitions

#### Discovery and inventory

- `discovered` → `inventoried`
- `discovered` → `failed`

#### Fingerprinting and metadata

- `inventoried` → `fingerprinted`
- `inventoried` → `metadata_extracted`
- `fingerprinted` → `metadata_extracted`
- `fingerprinted` → `analysis_pending`
- `metadata_extracted` → `analysis_pending`

#### Analysis and classification

- `analysis_pending` → `analyzed`
- `analyzed` → `classification_proposed`
- `classification_proposed` → `review_required`
- `classification_proposed` → `approved`
- `analysis_pending` → `review_required`

#### Review and approval

- `review_required` → `approved`
- `review_required` → `unresolved`
- `approved` → `operation_planned`

#### Execution

- `operation_planned` → `copied`
- `operation_planned` → `failed`
- `copied` → `verified`
- `copied` → `failed`
- `verified` → `retirement_pending`

#### Retirement, archive, and closure

- `retirement_pending` → `retired`
- `retired` → `archived`
- `verified` → `archived` when no retirement step is needed

#### Exceptional paths

- Any non-terminal state may transition to `unresolved` when the item requires operator attention or when policy cannot yet be applied.
- Any non-terminal state may transition to `failed` when a hard stop, corruption, hash mismatch, journal failure, path escape, or other safety failure occurs.

### Forbidden transitions

- `approved` → `discovered`
- `operation_planned` → `approved`
- `copied` → `analysis_pending`
- `verified` → `copied`
- `retired` → `operation_planned`
- `archived` → any non-archived workflow state
- `failed` → `approved` without a fresh review and new evidence
- `unresolved` → `approved` without review resolution

### Transition rules

1. Transitions are monotonic with respect to evidence: once evidence is gathered, later states may refine or consume it, but they do not erase it.
2. Transitions are idempotent when repeated for the same observed event.
3. A transition requiring verification cannot be skipped by a higher-level process.
4. `unresolved` and `failed` are not success states.
5. A file can be revisited from `unresolved` or `failed` only through an explicit new scan, review, or operator-initiated reprocessing event.

## Run states

Run states apply to scans, batches, and reconciliation jobs. They are also used by the sentinel for health summaries.

### States

- `queued`
- `starting`
- `running`
- `checkpointed`
- `paused`
- `stalled`
- `completed`
- `completed_with_exceptions`
- `failed`
- `cancelled`

### Allowed transitions

- `queued` → `starting`
- `starting` → `running`
- `running` → `checkpointed`
- `checkpointed` → `running`
- `running` → `paused`
- `paused` → `running`
- `running` → `stalled`
- `checkpointed` → `stalled`
- `running` → `completed`
- `checkpointed` → `completed`
- `running` → `completed_with_exceptions`
- `checkpointed` → `completed_with_exceptions`
- any non-terminal state → `failed`
- any non-terminal state → `cancelled`

### Forbidden transitions

- `completed` → `running`
- `completed_with_exceptions` → `running`
- `failed` → `running` without a new run instance
- `cancelled` → `running` without a new run instance
- `stalled` → `completed` without resumed work and fresh checkpoints

### Run transition rules

1. A run may only advance when its checkpoint cursor, journal sequence, and metrics are internally consistent.
2. `checkpointed` does not mean finished; it only means restart-safe progress is recorded.
3. `stalled` indicates a lack of forward progress, not necessarily a hard failure.
4. The sentinel may report `stalled`, but it does not resolve the stall by itself.
5. `completed_with_exceptions` is allowed when the run reached the end of scope but left unresolved items, non-blocking errors, or policy exceptions.

## Operator and safety transitions

The following state changes are only possible through explicit operator action or approved automation.

- `review_required` → `approved`
- `operation_planned` → `failed` after a hard stop
- `paused` → `running`
- `cancelled` → new run instance only
- `retirement_pending` → `retired`
- `retired` → `archived`

These transitions require validated evidence and must be recorded in the journal or equivalent audit trail.

## Event coupling

State transitions should emit a single authoritative event for the transition and may emit auxiliary metrics or alerts. Repeated delivery of the same event must not create duplicate side effects.

## V1 boundary

V1 supports the states and transitions listed above and no others. If an implementation discovers a need for a new state, the need must be justified in a specification revision and reviewed before adoption.
