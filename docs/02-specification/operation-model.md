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
- confirm that the backend authorization evaluation passes for this exact entry, on this attempt, in this run (`docs/02-specification/approval-binding-model.md`)
- confirm the journal is writable
- confirm collisions are handled by policy

## Execution checks

> The authoritative, numbered write protocol — with a failure branch for every step, a durable
> intent record **before** any mutation, an atomic finalize step, and a deterministic crash-state
> table — is defined in `docs/02-specification/durability-and-recovery-model.md`. The summary below
> is a reader's overview and must not be implemented in place of that protocol.

The executor must:

1. Append a durable **intent** record and complete its durability barrier. **No filesystem mutation may be attempted before this completes**, so every possible on-disk artifact is attributable.
2. Create destination and staging directories safely.
3. Write to a temporary destination name, always — not "when needed" — on the same filesystem as the destination.
4. Flush and fsync the temporary file and its parent directory.
5. Independently re-read and verify the destination bytes against the expected hash.
6. Re-check that the destination path is still absent, then atomically finalize.
7. Record the finalize and then the terminal outcome in the journal, each with a durability barrier.
8. Emit progress and failure events.
9. Stop the batch if a safety threshold is exceeded.

The next filesystem mutation may not begin until the preceding operation's terminal outcome record is durable and no unresolved on-disk artifact remains.

## Verification rules

Verification must record:

- the destination exists
- the content hash matches
- the source change token was equal immediately before and immediately after the copy
- the observed counts reconcile with the plan
- the source path remains accounted for in the chosen phase
- a **preservation comparison report** covering every property the effective preservation profile marks `required`, `best_effort`, `normalized`, or `unsupported_reported`

> **Hash equality verifies content, not preservation.** It says nothing about timestamps,
> permissions, ownership, ACLs, extended attributes, resource forks, hard-link topology, symlink
> semantics, sparse layout, or filename byte sequence. A hash match alone is never sufficient to
> describe a copy as preserved, and never sufficient to authorize source retirement. See
> `docs/02-specification/preservation-model.md`.

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

Collision behavior must be explicit and per-entry. **Destination collision is distinct from rule conflict** and the two must never substitute for one another; see `rule-model.md`.

Allowed strategies are:

- `route_to_review`
- `skip`
- `compare`
- `versioned_suffix` — requires an exact version template and a maximum; the **new** copy receives the suffix, and the pre-existing file is never renamed, moved, or replaced

Collisions may never default to silent overwrite; `never_overwrite` is pinned true under every policy.

A collision arising from case-only or Unicode-normalization difference is a mandatory review, never an automatic versioning — the two files are semantically distinct originals rather than versions of one another. Collision risk is evaluated against the **destination's** case and normalization sensitivity, not the source's.

## V1 limits

- No permanent deletion.
- No automatic expansion after a failed batch.
- No execution without approval.
- No execution from dashboard animation or sentinel request alone.
- No mutation that is not traceable to a specific plan entry.

