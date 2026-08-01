# Command Model

## Purpose

Commands are intent-bearing requests that may change state if they pass validation, authorization, and safety checks. Commands are distinct from events; commands request action, events record facts.

The platform uses commands to keep write operations explicit, auditable, and approval-aware.

## Command rules

1. Commands must be validated before execution.
2. Commands must carry a deduplication key. Mutating commands must additionally be idempotent.
3. Commands must not bypass approvals.
4. Commands may not authorize permanent deletion in V1.
5. Commands must be traceable to an operator, rule, batch, or automated safe request.
6. The sentinel may issue only predefined safe requests.

## Canonical command families

### Inventory and scan commands

- `propose_source_root`
- `confirm_source_root`
- `start_scan`
- `pause_scan`
- `resume_scan`
- `complete_scan`

### Metadata and analysis commands

- `record_discovery`
- `record_inventory`
- `mark_fingerprinted`
- `attach_metadata`
- `extract_metadata`
- `validate_metadata`

### Rule commands

- `create_rule_set`
- `approve_rule_set`
- `activate_rule_set`
- `disable_rule_set`
- `propose_rule`
- `review_rule`

### Classification commands

- `propose_decision`
- `request_review`
- `approve_decision`
- `reject_decision`

### Duplicate commands

- `identify_duplicate_group`
- `review_duplicate_group`
- `approve_duplicate_group`
- `close_duplicate_group`

### Taxonomy commands

- `propose_taxonomy_node`
- `approve_taxonomy_node`
- `deprecate_taxonomy_node`
- `retire_taxonomy_node`

### Planning and execution commands

- `draft_operation_plan`
- `approve_operation_plan`
- `lock_operation_plan`
- `supersede_operation_plan`
- `queue_operation_entry`
- `execute_operation_entry`
- `verify_operation_entry`
- `close_operation_entry`

### Batch and recovery commands

- `start_batch`
- `pause_batch`
- `resume_batch`
- `complete_batch`
- `write_checkpoint`
- `seal_checkpoint`
- `invalidate_checkpoint`
- `append_journal_entry`
- `seal_journal`
- `replay_journal`

### Review and approval commands

- `open_review_item`
- `assign_review_item`
- `resolve_review_item`
- `close_review_item`
- `request_approval`
- `grant_approval`
- `consume_approval`
- `revoke_approval`

### Monitoring commands

- `record_health`
- `mark_degraded`
- `mark_stalled`
- `mark_offline`
- `raise_alert`
- `acknowledge_alert`
- `resolve_alert`

## Command envelope

Every command should include:

- command id
- command type
- subject type and id
- actor — **derived from the authenticated session, never read from the payload.** A payload-supplied actor is rejected.
- requested at
- deduplication key (required)
- correlation id and causation id
- payload

> **`validation status` and `authorization status` are server-computed only.** They are results the
> backend records, not inputs a client may supply. A command received with either field populated —
> or with an `approval_state` — must be **rejected** with `APR-E25_CLIENT_ASSERTED_AUTHORIZATION`,
> not silently ignored. Silently ignoring it hides either an attack or a client defect.
> See `docs/02-specification/approval-binding-model.md`.

## Validation semantics

Before execution, the command handler must verify:

- the subject exists or is safely creatable
- the user or process has authority
- the requested state transition is allowed
- the path is under an approved root
- the plan or action is compatible with the current lifecycle
- the command does not violate a global invariant

## Execution semantics

- If a command is valid and authorized, it may mutate the relevant record or emit a downstream event.
- If a command fails validation, it must be rejected without side effects.
- If a command fails after partial work, recovery must reconcile the partial state before retry.
- Retrying the same command must not create duplicate effects.

## Sentinel command restriction

The Raspberry Pi sentinel may only request or trigger predefined safe commands such as:

- heartbeat recording
- health status updates
- alert emission
- safe monitoring job requests

It may not issue commands that classify, approve, move, delete, or otherwise mutate content.

## V1 limits

- Commands are scoped to the approved blueprint and synthetic fixtures until the dry-run gate (G4) is authorized. There is no single "live authorization": G4 (read-only), G6 (bounded copy), and G7 (retirement) are separate gates, each with its own authorization record. See `docs/05-governance/gate-model.md`.
- No command may create an implicit approval.
- No command may bypass path validation or journal requirements.

