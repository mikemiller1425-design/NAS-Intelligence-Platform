# Domain Model

## Purpose

This document defines the V1 domain objects for the NAS Intelligence Platform. The model is intentionally conservative: it supports read-only inventory, dry-run classification, immutable planning, copy-first pilot execution, verification, and reconciliation without authorizing live NAS mutation.

All identifiers are opaque and stable. All file-system paths in examples are synthetic and non-sensitive. The system is **dry-run by default** and implementation is blocked until the foundation audit and subsequent approvals occur.

## Global invariants

These invariants apply across all entities unless a narrower entity-level rule is stricter.

1. Inventory is read-only.
2. A file’s bytes are never changed by classification.
3. Every proposed destination must include evidence, explanation, and the rule version used for the decision.
4. Low-confidence or conflicting decisions enter manual review.
5. A conflict must remain unresolved until an explicit decision.
6. A file cannot silently belong to multiple canonical destinations.
7. A plan is immutable after approval; changes create a new version.
8. A destructive operation requires explicit human approval.
9. Execution revalidates source hash, size, and path preconditions.
10. Destination collisions never overwrite silently.
11. Existing protected vault content cannot be overwritten by default.
12. Successful copy or move requires post-operation hash verification.
13. A source file cannot be retired before destination verification and approved retirement.
14. Permanent deletion is unavailable in V1.
15. Exact duplicates require cryptographic hash equality; a duplicate decision cannot rely on filename alone.
16. Repeated events and reruns are idempotent; retrying cannot create duplicate destination copies.
17. A run can resume from checkpoints without incorrectly repeating completed operations.
18. Failed operations remain inspectable.
19. Journal failure stops mutation.
20. Paths cannot escape approved roots.
21. Frontend state cannot authorize filesystem mutations.
22. The sentinel cannot authorize mutations.
23. AI output is untrusted until validated.
24. No live NAS action is authorized by this specification alone.

## Entity overview

### Common supporting fields

Most entities use some combination of the following fields:

- `id`: opaque stable identifier.
- `created_at`, `updated_at`: UTC timestamps.
- `version`: monotonic version number or semantic version tag.
- `source_ref`: provenance pointer back to a source file, scan, rule, or command.
- `status`: lifecycle state for the entity.
- `notes`: human-readable explanation or operator commentary.

## SourceRoot

### Purpose

Defines an approved root that may be scanned or referenced by the system.

### Required fields

- `id`
- `label`
- `synthetic_root_path`
- `root_type` with values `source`, `incoming`, `organized`, `review`, `quarantine`, `pilot`, `archive`, or `control`
- `authority` with values `confirmed_live`, `intended_structure`, or `unresolved_assumption`
- `enabled`
- `read_only_expected`
- `scan_scope`

### Relationships

- Owns many `FileRecord` entries.
- Participates in one or more `Scan` runs.
- Constrains `OperationPlan` source and destination paths.

### Lifecycle

`proposed` → `confirmed` → `active` → `retired`

### Allowed states

- `proposed`
- `confirmed`
- `active`
- `retired`

### Invariants

- A `confirmed_live` source root must be backed by verified operator evidence.
- A `SourceRoot` marked `control` must never recursively include a scanned source tree.
- Roots tagged `unresolved_assumption` are allowed for specification work but must not be treated as live truth.

### Commands

- `propose_source_root`
- `confirm_source_root`
- `retire_source_root`

### Emitted events

- `SourceRootProposed`
- `SourceRootConfirmed`
- `SourceRootRetired`

### V1 limits

- No automatic discovery of live NAS mounts.
- No mutation of root definitions from runtime behavior.

## FileRecord

### Purpose

Represents a discovered file or directory entry under inventory. File bytes are never modified by this record.

### Required fields

- `id`
- `source_root_id`
- `relative_path`
- `normalized_path`
- `entry_type` with values `file`, `directory`, or `symlink`
- `size_bytes`
- `discovered_at`
- `inventory_state`
- `content_identity_state`
- `path_authority` with values `confirmed_live`, `intended_structure`, or `unresolved_assumption`

### Relationships

- Belongs to one `SourceRoot`.
- May have one or more `MetadataRecord` entries.
- May have one or more `HashRecord` entries.
- May be referenced by many `ClassificationDecision`, `DuplicateGroup`, `OperationEntry`, `VerificationResult`, and `ReconciliationReport` records.

### Lifecycle

`discovered` → `inventoried` → `fingerprinted` → `metadata_extracted` → `analysis_pending` → `analyzed` → `classification_proposed` → `review_required` → `approved` → `operation_planned` → `copied` → `verified` → `retirement_pending` → `retired` → `archived`

`unresolved` and `failed` are terminal or pause states that can occur at multiple points in the pipeline.

### Allowed states

See `lifecycle-model.md`.

### Invariants

- A `FileRecord` does not itself prove file content; `HashRecord` does.
- Inventory must remain source-preserving and repeatable.
- A path that escapes an approved root is rejected before mutation.

### Commands

- `record_discovery`
- `record_inventory`
- `mark_fingerprinted`
- `attach_metadata`
- `propose_classification`
- `mark_review_required`
- `approve_record`

### Emitted events

- `FileDiscovered`
- `FileInventoried`
- `FileFingerprinted`
- `MetadataExtracted`
- `FileAnalysisCompleted`
- `ClassificationProposed`
- `ReviewRequired`
- `FileApproved`
- `FileArchived`

### V1 limits

- Directory entries may be represented minimally if the file tree is large.
- Sparse or unreadable metadata is accepted as a first-class result.

## Scan

### Purpose

Represents one read-only pass over a bounded set of roots or filters.

### Required fields

- `id`
- `source_root_ids`
- `scan_mode` with values `inventory`, `dry_run`, `fixture`, `pilot`, `reconcile`
- `started_at`
- `completed_at`
- `status`
- `checkpoint_cursor`
- `totals`
- `error_summary`

### Relationships

- Produces many `FileRecord` updates.
- Produces many `MetadataRecord`, `HashRecord`, and `JournalEntry` records.
- May seed `ReconciliationReport`.

### Lifecycle

`queued` → `running` → `checkpointed` → `completed`

`paused`, `stalled`, and `failed` are allowed interruption states.

### Invariants

- A scan is idempotent for already-seen inputs.
- A failed scan never implies successful completeness.

### Commands

- `start_scan`
- `pause_scan`
- `resume_scan`
- `complete_scan`

### Emitted events

- `ScanStarted`
- `ScanCheckpointed`
- `ScanPaused`
- `ScanResumed`
- `ScanCompleted`
- `ScanFailed`

### V1 limits

- No direct live NAS write is permitted from a `Scan`.

## MetadataRecord

### Purpose

Stores extracted metadata, parse findings, and extraction provenance.

### Required fields

- `id`
- `file_record_id`
- `extraction_kind` with values `filesystem`, `media`, `document`, `structured_data`, `ai_suggestion`
- `extractor_name`
- `extractor_version`
- `payload`
- `confidence`
- `extracted_at`

### Relationships

- Belongs to one `FileRecord`.
- May inform many `ClassificationDecision` records.

### Lifecycle

`pending` → `extracted` → `validated` → `superseded`

### Allowed states

- `pending`
- `extracted`
- `validated`
- `superseded`
- `failed`

### Invariants

- Metadata extraction must not alter source bytes.
- AI-generated metadata is always marked as untrusted until validated.

### Commands

- `extract_metadata`
- `validate_metadata`
- `supersede_metadata`

### Emitted events

- `MetadataExtractionRequested`
- `MetadataExtracted`
- `MetadataValidated`
- `MetadataSuperseded`

### V1 limits

- GPS, thumbnails, OCR text, and identity hints are all optional and may be disabled.

## HashRecord

### Purpose

Captures a hash or checksum of file bytes for exact duplicate detection and post-copy verification.

### Required fields

- `id`
- `file_record_id`
- `algorithm`
- `digest`
- `calculated_at`
- `scope` with values `source_precheck`, `inventory`, `post_copy`, `verification`
- `status`

### Relationships

- Belongs to one `FileRecord`.
- May be used by `DuplicateGroup`, `OperationPlan`, `VerificationResult`, and `ReconciliationReport`.

### Lifecycle

`pending` → `calculated` → `validated`

### Allowed states

- `pending`
- `calculated`
- `validated`
- `failed`

### Invariants

- Exact duplicates require matching hashes under the chosen V1 algorithm family.
- A post-copy hash must match before an operation is considered verified.

### Commands

- `calculate_hash`
- `validate_hash`
- `compare_hash`

### Emitted events

- `HashCalculationRequested`
- `HashCalculated`
- `HashValidated`
- `HashMismatchDetected`

### V1 limits

- Multiple algorithms may be stored, but exactly one approved comparison algorithm governs exact duplicate decisions in V1.

## RuleSet

### Purpose

Versioned container for classification rules.

### Required fields

- `id`
- `name`
- `version`
- `status`
- `priority_scheme`
- `rules`
- `effective_from`
- `owner`
- `approval_state`

### Relationships

- Contains many `ClassificationRule` records.
- Is referenced by every `ClassificationDecision`.

### Lifecycle

`draft` → `reviewed` → `approved` → `active` → `superseded` → `retired`

### Allowed states

- `draft`
- `reviewed`
- `approved`
- `active`
- `disabled`
- `superseded`
- `retired`

### Invariants

- A decision must retain the exact rule set version that produced it.
- A new rule version never rewrites prior outcomes in place.

### Commands

- `create_rule_set`
- `approve_rule_set`
- `activate_rule_set`
- `disable_rule_set`
- `supersede_rule_set`

### Emitted events

- `RuleSetCreated`
- `RuleSetApproved`
- `RuleSetActivated`
- `RuleSetDisabled`
- `RuleSetSuperseded`

### V1 limits

- Rule sets are configuration artifacts, not code.

## ClassificationRule

### Purpose

Encodes a single deterministic or AI-assisted classification rule.

### Required fields

- `id`
- `rule_set_id`
- `priority`
- `status`
- `kind` with values `deterministic`, `content_inference`, `ai_assisted`, `manual_override`
- `conditions`
- `destination_template`
- `minimum_confidence`
- `conflict_policy`
- `human_confirmation_required`
- `test_case_refs`
- `rationale`

### Relationships

- Belongs to one `RuleSet`.
- Can trigger one or more `ClassificationDecision` records.

### Lifecycle

`proposed` → `reviewed` → `active` → `disabled` → `retired`

### Allowed states

- `proposed`
- `provisional`
- `active`
- `disabled`
- `retired`

### Invariants

- Provisional rules for dog, person/Voss identity, drone, CSV, and unresolved categories remain provisional until operator confirmation.
- Higher-priority deterministic rules outrank lower-priority rules.
- Human confirmation is mandatory for sensitive identity intent.

### Commands

- `propose_rule`
- `review_rule`
- `activate_rule`
- `disable_rule`
- `retire_rule`

### Emitted events

- `ClassificationRuleProposed`
- `ClassificationRuleReviewed`
- `ClassificationRuleActivated`
- `ClassificationRuleDisabled`
- `ClassificationRuleRetired`

### V1 limits

- Rules cannot silently elevate their own authority.
- Rules cannot authorize permanent deletion in V1.

## ClassificationDecision

### Purpose

Represents the output of evaluating rules against a file.

### Required fields

- `id`
- `file_record_id`
- `rule_set_id`
- `candidate_rule_ids`
- `proposed_destination`
- `confidence`
- `evidence`
- `decision_state`
- `review_reason`
- `created_at`

### Relationships

- Belongs to one `FileRecord`.
- References one `RuleSet` and one or more `ClassificationRule` records.
- May spawn one `ReviewItem` and one `OperationPlan`.

### Lifecycle

`proposed` → `review_required` → `approved` → `planned` → `rejected`

### Allowed states

- `proposed`
- `review_required`
- `approved`
- `planned`
- `rejected`

### Invariants

- Any conflict, low confidence, or sensitive identity scenario must route to manual review.
- The decision must include the evidence used, not just the final path.

### Commands

- `propose_decision`
- `request_review`
- `approve_decision`
- `reject_decision`

### Emitted events

- `ClassificationDecisionProposed`
- `ClassificationDecisionReviewRequested`
- `ClassificationDecisionApproved`
- `ClassificationDecisionRejected`

### V1 limits

- No decision may become executable until approved and planned.

## DuplicateGroup

### Purpose

Collects exact-duplicate candidates and, separately, near-duplicate candidates for review.

### Required fields

- `id`
- `group_type` with values `exact`, `near`, `mixed`
- `canonical_file_record_id`
- `member_file_record_ids`
- `hash_fingerprint`
- `similarity_basis`
- `review_state`
- `risk_level`

### Relationships

- References many `FileRecord` entries.
- May lead to a `ReviewItem`, `OperationPlan`, or `QuarantineRecommendation`.

### Lifecycle

`identified` → `reviewed` → `approved` → `closed`

### Allowed states

- `identified`
- `review_required`
- `reviewed`
- `approved`
- `closed`

### Invariants

- Exact duplicates are hash-backed.
- Near duplicates are never treated as equality.
- No duplicate group authorizes deletion in V1.

### Commands

- `identify_duplicate_group`
- `review_duplicate_group`
- `approve_duplicate_group`
- `close_duplicate_group`

### Emitted events

- `DuplicateGroupIdentified`
- `DuplicateGroupReviewed`
- `DuplicateGroupApproved`
- `DuplicateGroupClosed`

### V1 limits

- Quarantine is allowed only with explicit approval and evidence.

## ReviewItem

### Purpose

Tracks manual review work for low-confidence, conflicting, sensitive, or exceptional cases.

### Required fields

- `id`
- `subject_type`
- `subject_id`
- `reason`
- `priority`
- `assigned_to`
- `review_state`
- `due_hint`

### Relationships

- May refer to `FileRecord`, `ClassificationDecision`, `DuplicateGroup`, `OperationPlan`, or `RuleSet`.

### Lifecycle

`open` → `in_review` → `resolved` → `closed`

### Allowed states

- `open`
- `in_review`
- `resolved`
- `closed`

### Invariants

- A review item is required when evidence is ambiguous or a policy exception exists.

### Commands

- `open_review_item`
- `assign_review_item`
- `resolve_review_item`
- `close_review_item`

### Emitted events

- `ReviewItemOpened`
- `ReviewItemAssigned`
- `ReviewItemResolved`
- `ReviewItemClosed`

### V1 limits

- Review items do not themselves authorize mutation.

## TaxonomyNode

### Purpose

Represents a durable human-readable destination category in the target library.

### Required fields

- `id`
- `slug`
- `display_name`
- `parent_id`
- `path_template`
- `authority`
- `status`
- `retention_notes`

### Relationships

- Forms a tree with other `TaxonomyNode` entries.
- Is referenced by `ClassificationRule` and `OperationPlan`.

### Lifecycle

`proposed` → `approved` → `active` → `deprecated` → `retired`

### Allowed states

- `proposed`
- `approved`
- `active`
- `deprecated`
- `retired`

### Invariants

- The taxonomy must be explainable to a human without the software.
- A node path must remain under an approved root.

### Commands

- `propose_taxonomy_node`
- `approve_taxonomy_node`
- `deprecate_taxonomy_node`
- `retire_taxonomy_node`

### Emitted events

- `TaxonomyNodeProposed`
- `TaxonomyNodeApproved`
- `TaxonomyNodeDeprecated`
- `TaxonomyNodeRetired`

### V1 limits

- Taxonomy growth requires operator review for structural changes.

## OperationPlan

### Purpose

Immutable plan that turns approved classifications into execution-ready filesystem operations.

### Required fields

- `id`
- `version`
- `batch_id`
- `plan_state`
- `source_root_id`
- `destination_root_id`
- `entries`
- `approval_id`
- `preconditions`
- `postconditions`
- `collision_policy`
- `rollback_strategy`
- `created_at`

### Relationships

- Contains many `OperationEntry` records.
- References `Approval`, `FileRecord`, and `ClassificationDecision`.
- Produces many `JournalEntry` and `VerificationResult` records.

### Lifecycle

`draft` → `review_required` → `approved` → `locked` → `executing` → `completed` → `superseded`

### Allowed states

- `draft`
- `review_required`
- `approved`
- `locked`
- `executing`
- `completed`
- `superseded`
- `cancelled`

### Invariants

- A plan is immutable after approval.
- Any change after approval creates a new version.
- No entry may exceed approved roots or bypass collision policy.

### Commands

- `draft_operation_plan`
- `approve_operation_plan`
- `lock_operation_plan`
- `supersede_operation_plan`

### Emitted events

- `OperationPlanDrafted`
- `OperationPlanApproved`
- `OperationPlanLocked`
- `OperationPlanSuperseded`

### V1 limits

- Plans may propose copy, move, quarantine, or skip; permanent deletion remains absent.

## OperationEntry

### Purpose

Single atomic step within an operation plan.

### Required fields

- `id`
- `plan_id`
- `file_record_id`
- `entry_type` with values `copy`, `move`, `rename`, `quarantine`, `skip`
- `source_path`
- `destination_path`
- `precondition_hash`
- `precondition_size`
- `execution_state`
- `verification_state`

### Relationships

- Belongs to one `OperationPlan`.
- References one `FileRecord`.

### Lifecycle

`planned` → `queued` → `executing` → `verified` → `closed`

### Allowed states

- `planned`
- `queued`
- `executing`
- `verified`
- `failed`
- `skipped`
- `closed`

### Invariants

- Destination collisions must not overwrite silently.
- Source revalidation is required immediately before execution.

### Commands

- `queue_operation_entry`
- `execute_operation_entry`
- `verify_operation_entry`
- `close_operation_entry`

### Emitted events

- `OperationEntryQueued`
- `OperationEntryExecuting`
- `OperationEntryVerified`
- `OperationEntryFailed`

### V1 limits

- A `move` is permitted only when the approved phase authorizes source removal.

## Approval

### Purpose

Records explicit human approval for a plan, rule set, taxonomy node, review exception, or pilot gate.

### Required fields

- `id`
- `subject_type`
- `subject_id`
- `approver`
- `approved_at`
- `approval_scope`
- `approval_state`
- `evidence_refs`

### Relationships

- References the approved object.
- May gate one or more `OperationPlan` versions.

### Lifecycle

`requested` → `granted` → `consumed` → `superseded`

### Allowed states

- `requested`
- `granted`
- `consumed`
- `revoked`
- `superseded`

### Invariants

- Approval must be explicit and tied to evidence.
- Sentinel-originated requests are not approvals.

### Commands

- `request_approval`
- `grant_approval`
- `consume_approval`
- `revoke_approval`

### Emitted events

- `ApprovalRequested`
- `ApprovalGranted`
- `ApprovalConsumed`
- `ApprovalRevoked`

### V1 limits

- Approvals are not transferrable across unrelated subjects.

## Batch

### Purpose

Groups inventory, classification, or execution work into an auditable unit.

### Required fields

- `id`
- `batch_type`
- `status`
- `scope`
- `planned_count`
- `processed_count`
- `failed_count`
- `checkpoint_id`
- `plan_id`

### Relationships

- May contain many `FileRecord`, `OperationEntry`, and `JournalEntry` references.

### Lifecycle

`queued` → `running` → `checkpointed` → `completed`

### Allowed states

- `queued`
- `running`
- `paused`
- `checkpointed`
- `completed`
- `failed`
- `cancelled`

### Invariants

- Batch processing must be restartable from checkpoint.
- A failed batch never implies a successful final disposition.

### Commands

- `start_batch`
- `pause_batch`
- `resume_batch`
- `complete_batch`

### Emitted events

- `BatchStarted`
- `BatchCheckpointed`
- `BatchPaused`
- `BatchCompleted`
- `BatchFailed`

### V1 limits

- Batch size thresholds are operator-calibrated, not self-tuned.

## JournalEntry

### Purpose

Append-only mutation log for plan execution, recovery, and reconciliation.

### Required fields

- `id`
- `journal_type`
- `subject_type`
- `subject_id`
- `payload`
- `sequence_number`
- `written_at`
- `write_state`

### Relationships

- References `Batch`, `OperationEntry`, `VerificationResult`, or `ReconciliationReport`.

### Lifecycle

`pending` → `written` → `sealed`

### Allowed states

- `pending`
- `written`
- `sealed`
- `failed`

### Invariants

- Journal failure stops mutation.
- The journal must be append-only.

### Commands

- `append_journal_entry`
- `seal_journal`
- `replay_journal`

### Emitted events

- `JournalEntryAppended`
- `JournalSealed`
- `JournalReplayCompleted`
- `JournalWriteFailed`

### V1 limits

- Journals must be stored outside the mutable data path.

## VerificationResult

### Purpose

Captures post-operation checks proving copy/move correctness.

### Required fields

- `id`
- `operation_entry_id`
- `verification_type`
- `source_hash`
- `destination_hash`
- `result`
- `verified_at`

### Relationships

- Belongs to one `OperationEntry`.
- May feed `ReconciliationReport`.

### Lifecycle

`pending` → `passed` → `recorded`

### Allowed states

- `pending`
- `passed`
- `failed`
- `recorded`

### Invariants

- Successful copy or move requires verification.
- A mismatch must stop the batch or trigger a hard stop per policy.

### Commands

- `request_verification`
- `record_verification`
- `finalize_verification`

### Emitted events

- `VerificationRequested`
- `VerificationPassed`
- `VerificationFailed`
- `VerificationRecorded`

### V1 limits

- Verification may be hash-only in V1 unless policy demands additional checks.

## Checkpoint

### Purpose

Records restart-safe progress for scans, batches, and reconciliation runs.

### Required fields

- `id`
- `scope_type`
- `scope_id`
- `cursor`
- `sequence_number`
- `created_at`
- `state`

### Relationships

- References a `Scan`, `Batch`, or `ReconciliationReport`.

### Lifecycle

`open` → `persisted` → `sealed`

### Allowed states

- `open`
- `persisted`
- `sealed`
- `invalidated`

### Invariants

- Checkpoints must support idempotent resume.
- A checkpoint never implies completion by itself.

### Commands

- `write_checkpoint`
- `seal_checkpoint`
- `invalidate_checkpoint`

### Emitted events

- `CheckpointWritten`
- `CheckpointSealed`
- `CheckpointInvalidated`

### V1 limits

- No checkpoint may be placed inside a recursively scanned source root.

## Alert

### Purpose

Represents a notification or escalation generated by the sentinel or core engine.

### Required fields

- `id`
- `severity`
- `category`
- `message`
- `source`
- `status`
- `created_at`

### Relationships

- May reference `SystemHealth`, `Batch`, `Scan`, `ReviewItem`, or `ReconciliationReport`.

### Lifecycle

`raised` → `acknowledged` → `resolved`

### Allowed states

- `raised`
- `acknowledged`
- `resolved`
- `suppressed`

### Invariants

- Alerts must not expose credentials or sensitive filenames unnecessarily.

### Commands

- `raise_alert`
- `acknowledge_alert`
- `resolve_alert`

### Emitted events

- `AlertRaised`
- `AlertAcknowledged`
- `AlertResolved`

### V1 limits

- Alerts are advisory and never substitute for plan approval.

## SystemHealth

### Purpose

Captures the operational state of the Mac mini engine and Raspberry Pi sentinel.

### Required fields

- `id`
- `component`
- `heartbeat_at`
- `reachability`
- `queue_depth`
- `free_space`
- `last_checkpoint_id`
- `health_state`

### Relationships

- May reference `Alert`, `Batch`, and `Scan`.

### Lifecycle

`unknown` → `healthy` → `degraded` → `stalled` → `offline`

### Allowed states

- `unknown`
- `healthy`
- `degraded`
- `stalled`
- `offline`

### Invariants

- The sentinel can observe, alert, and request safe predefined jobs only.
- The sentinel cannot choose classifications, approve plans, or mutate files.

### Commands

- `record_health`
- `mark_degraded`
- `mark_stalled`
- `mark_offline`

### Emitted events

- `SystemHealthRecorded`
- `SystemMarkedDegraded`
- `SystemMarkedStalled`
- `SystemMarkedOffline`

### V1 limits

- Health telemetry is read-only.

## ReconciliationReport

### Purpose

Documents post-run accounting between source inventory, planned operations, executed operations, and observed destination state.

### Required fields

- `id`
- `scope`
- `report_state`
- `source_totals`
- `destination_totals`
- `exception_totals`
- `mismatch_summary`
- `generated_at`

### Relationships

- Aggregates `FileRecord`, `DuplicateGroup`, `OperationPlan`, `OperationEntry`, `VerificationResult`, and `JournalEntry`.

### Lifecycle

`draft` → `review_required` → `finalized`

### Allowed states

- `draft`
- `review_required`
- `finalized`
- `superseded`

### Invariants

- Every source item must end in a final disposition or an explicitly owned exception.
- Totals must reconcile or the report must disclose why not.

### Commands

- `draft_reconciliation_report`
- `finalize_reconciliation_report`
- `supersede_reconciliation_report`

### Emitted events

- `ReconciliationReportDrafted`
- `ReconciliationReportFinalized`
- `ReconciliationReportSuperseded`

### V1 limits

- Reconciliation reports are evidence artifacts, not operational commands.

## Entity-level V1 summary

V1 includes the entities above and excludes any entity that would require live NAS mutation authority, automatic deletion, autonomous identity recognition, or hidden side effects. Any additional implementation detail must be justified against this domain model and the foundation audit before it is considered executable.
