# Event Model

## Purpose

This document defines the event vocabulary used to make inventory, classification, planning, execution, verification, and monitoring observable and replayable.

Events are append-only facts. They are not commands and they are not approvals.

## Event design rules

1. Every event has a unique identifier.
2. Every event has a timestamp.
3. Every event names the subject it describes.
4. Every event is idempotent when replayed.
5. Duplicate delivery must not create duplicate side effects.
6. Events must preserve enough context to reconstruct the major audit trail.
7. Sensitive values should be redacted or minimized in emitted payloads.

## Event envelope

```yaml
event_id: evt_demo_001
event_type: FileInventoried
occurred_at: "2026-07-31T23:00:00Z"
source: mac-mini-engine
subject:
  type: FileRecord
  id: file_123
correlation_id: run_456
causation_id: cmd_789
schema_version: 1
payload:
  source_root_id: root_demo
  relative_path: "Demo/Incoming/example.jpg"
```

## Canonical event vocabulary

This section is the **single authority** for event names (audit finding FND-m001). `docs/02-specification/domain-model.md` lists which aggregate emits each event; it does not define new names. Two rules govern the vocabulary:

1. **One event, one name.** No fact may be expressible under two different event names.
2. **One event, one emitter.** Each event name has exactly one emitting aggregate.

Any name appearing in `domain-model.md` but not below, or below but not in `domain-model.md`, is a defect.

### Source-root events

- `SourceRootProposed`
- `SourceRootConfirmed`
- `SourceRootRetired`

### Scan events

- `ScanStarted`
- `ScanPaused`
- `ScanResumed`
- `ScanCheckpointed`
- `ScanCompleted`
- `ScanFailed`

### Inventory events

- `FileDiscovered`
- `FileInventoried`
- `FileFingerprinted`
- `FileAnalysisCompleted`
- `ReviewRequired`
- `FileApproved`
- `FileArchived`

### Metadata events

- `MetadataExtractionRequested`
- `MetadataExtracted`
- `MetadataValidated`
- `MetadataSuperseded`

### Hash events

- `HashCalculationRequested`
- `HashCalculated`
- `HashValidated`
- `HashMismatchDetected`

### Rule events

- `RuleSetCreated`
- `RuleSetApproved`
- `RuleSetActivated`
- `RuleSetDisabled`
- `RuleSetSuperseded`
- `ClassificationRuleProposed`
- `ClassificationRuleReviewed`
- `ClassificationRuleActivated`
- `ClassificationRuleDisabled`
- `ClassificationRuleRetired`

### Classification decision events

- `ClassificationDecisionProposed`
- `ClassificationDecisionReviewRequested`
- `ClassificationConflictDetected`
- `ClassificationDecisionApproved`
- `ClassificationDecisionRejected`

> There is no `ClassificationProposed` event. It was a second name for `ClassificationDecisionProposed` and has been removed.

### Duplicate events

- `DuplicateGroupIdentified`
- `DuplicateGroupReviewed`
- `DuplicateGroupApproved`
- `DuplicateGroupClosed`

### Review events

- `ReviewItemOpened`
- `ReviewItemAssigned`
- `ReviewItemResolved`
- `ReviewItemClosed`

### Taxonomy events

- `TaxonomyNodeProposed`
- `TaxonomyNodeApproved`
- `TaxonomyNodeDeprecated`
- `TaxonomyNodeRetired`

### Approval events

- `ApprovalRequested`
- `ApprovalGranted`
- `ApprovalConsumed`
- `ApprovalRevoked`

### Operation events

- `OperationPlanDrafted`
- `OperationPlanApproved`
- `OperationPlanLocked`
- `OperationPlanSuperseded`
- `OperationEntryQueued`
- `OperationEntryExecuting`
- `OperationEntryVerified`
- `OperationEntryFailed`

### Batch events

- `BatchStarted`
- `BatchCheckpointed`
- `BatchPaused`
- `BatchCompleted`
- `BatchFailed`

### Journal and checkpoint events

- `JournalEntryAppended`
- `JournalSealed`
- `JournalWriteFailed`
- `JournalReplayCompleted`
- `CheckpointWritten`
- `CheckpointSealed`
- `CheckpointInvalidated`

> There is no `InventoryCheckpointWritten` event. Scan-progress checkpoints emit `ScanCheckpointed`; durable checkpoint records emit `CheckpointWritten`.

### Verification and reconciliation events

- `VerificationRequested`
- `VerificationRecorded`
- `VerificationPassed`
- `VerificationFailed`
- `ReconciliationReportDrafted`
- `ReconciliationReportFinalized`
- `ReconciliationReportSuperseded`

### Health and alert events

- `SystemHealthRecorded`
- `SystemMarkedDegraded`
- `SystemMarkedStalled`
- `SystemMarkedOffline`
- `AlertRaised`
- `AlertAcknowledged`
- `AlertResolved`

## Payload rules

- Payloads must be minimal but sufficient.
- Payloads should include the source of truth references needed for audit.
- Payloads must not contain credentials.
- Payloads should avoid unnecessary private filenames in alerts.
- Payloads must not encode hidden mutation authority.

## Ordering semantics

- Events are ordered per stream, not necessarily globally.
- Within a stream, sequence numbers must be monotonic.
- Cross-stream correlation uses `correlation_id` and `causation_id`.

## Replay semantics

Replaying events should rebuild derived state without duplicating side effects.

Replay rules:

1. First-write-wins for immutable records.
2. Idempotent application of repeated events.
3. No replay may authorize new live mutation.
4. Replay failures stop mutation and require intervention.

## Event storage expectations

The persistent store should preserve:

- raw event envelope
- normalized event type
- schema version
- sequence number
- correlation and causation links
- hash or checksum for tamper detection

## V1 limits

- Events do not replace state snapshots when restart safety requires both.
- Events are not a substitute for approvals.
- Events emitted by the sentinel are observational unless they refer to safe predefined requests.

