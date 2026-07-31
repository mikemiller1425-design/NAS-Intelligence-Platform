# Operation Model

## Purpose

The operation model defines how approved classification outcomes become immutable filesystem actions. It covers planning, execution, verification, rollback awareness, and batch control.

Operations are copy-first in V1 unless a later phase explicitly authorizes a different behavior. Permanent deletion is not available.

## Operation principles

1. Every operation originates from an approved immutable plan.
2. A plan is a forecast, not a mutation.
3. Execution revalidates source state immediately before acting.
4. Destination collisions never overwrite silently.
5. Post-operation verification is mandatory.
6. The journal is append-only and can stop mutation on failure.
7. Rollback must be designed before execution.

## Operation types

- `copy`
- `move`
- `rename`
- `quarantine`
- `skip`

### Type notes

- `copy`: preferred V1 mutation primitive.
- `move`: allowed only when the approved phase permits source removal.
- `rename`: must respect collision policy and approved roots.
- `quarantine`: preserves the item in a holding area.
- `skip`: records a deliberate non-action.

## Plan structure

An `OperationPlan` must define:

- plan identity and version
- batch identity
- source and destination roots
- immutable entry list
- approval reference
- preconditions
- collision policy
- rollback strategy
- verification expectations
- stop thresholds

## Execution lifecycle

### Draft

The plan is created from approved classification outputs and review decisions.

### Review required

Any plan with ambiguous destinations, low confidence, sensitive identity, or collision risk must be reviewed.

### Approved

The plan is approved by an explicit human authority.

### Locked

The approved plan is sealed against modification.

### Executing

Entries are executed in order, with source revalidation and journaling.

### Completed

All entries have been processed and verified or safely marked as exceptions.

### Superseded

A newer plan version replaces the old one; the old plan remains immutable for audit.

## Pre-execution checks

Before any filesystem action:

- confirm the source path is still under an approved root
- confirm the destination root is approved
- confirm the source hash and size still match the plan
- confirm free space and stop thresholds are acceptable
- confirm the plan has a valid approval
- confirm the journal is writable
- confirm collisions are handled by policy

## Execution checks

The executor must:

1. Create destination directories safely.
2. Write to a temporary destination name when needed.
3. Copy or rename according to plan.
4. Verify destination bytes against the expected hash.
5. Record the outcome in the journal.
6. Emit progress and failure events.
7. Stop the batch if a safety threshold is exceeded.

## Verification rules

Verification must prove:

- the destination exists
- the hash matches when required
- the observed counts reconcile with the plan
- the source path remains accounted for in the chosen phase

If verification fails, the item remains unresolved or failed and the batch stops according to policy.

## Rollback model

Rollback is a planned, bounded operation. It is not an ad hoc guess.

Rollback inputs:

- original plan version
- executed entry list
- journal records
- destination verification evidence
- approved rollback authority

Rollback may restore copied pilot data or revert a bounded batch if the approved phase and data state support it.

## Batch control

Operations run in batches so that failure has a small blast radius.

Batch controls include:

- maximum items per batch
- maximum bytes per batch
- error threshold
- mismatch threshold
- stall threshold
- checkpoint cadence

Batch progression must halt when the configured thresholds are exceeded.

## Collision handling

Collision behavior must be explicit and per-entry. Allowed strategies are:

- `skip`
- `version`
- `compare`
- `manual_review`

Collisions may never default to silent overwrite.

## V1 limits

- No permanent deletion.
- No automatic expansion after a failed batch.
- No execution without approval.
- No execution from dashboard animation or sentinel request alone.
- No mutation that is not traceable to a specific plan entry.

