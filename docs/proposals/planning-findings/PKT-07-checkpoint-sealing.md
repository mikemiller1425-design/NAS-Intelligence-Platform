# PKT-07 — Checkpoint sealing is defined only for mutation scopes (PF-03)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-03 (MAJOR) |
| Highest severity | MAJOR |
| Change-control batch | BATCH-07 |
| Operator decision required | **None.** Checkpoint *cadence* is adjacent to OD-008; the sealing *rule* is not a policy question. |
| Blocked rungs | FBL-019 |
| Affected acceptance | V1-ACC-036, PILOT-012 |
| Depends on | **PKT-03** — CK-4 compares a `SourceRoot` field that PF-11 adds |

## The exact contradiction

The sealing preconditions are mutation-shaped:

- `durability-and-recovery-model.md:241` — `checkpoint_sealed` is "appended only after every record
  through the checkpoint sequence is durable; **no operation is in a non-terminal state** at that
  sequence; the SQLite projection has been advanced to exactly that sequence and fsynced; and the
  chain verifies from the previous sealed checkpoint."
- `durability-and-recovery-model.md:240` — the `checkpoint` record itself carries "cursor, chain head
  hash, counts, **plan and approval binding**."

The scope set is not:

- `domain-model.md:1130` — a `Checkpoint` "References a **`Scan`**, `Batch`, or
  `ReconciliationReport`", with `scope_type` / `scope_id` required.
- `domain-model.md:191` — `Scan` carries `checkpoint_cursor`; `:203` — its lifecycle includes a
  `checkpointed` state.
- `domain-model.md:1152` — "**Only a sealed checkpoint may be used as a resume point.** An unsealed
  checkpoint is ignored."

**A scan has zero operations**, so "no operation is in a non-terminal state" is **vacuously true** —
a scan checkpoint seals trivially, sealing nothing. **And a scan has no plan and no approval**, so
the record's required binding is **unconstructible**. The two sides make a scan checkpoint
simultaneously trivially sealable and impossible to write.

A third loose end: `event-model.md:165` — "Scan-progress checkpoints emit `ScanCheckpointed`; durable
checkpoint records emit `CheckpointWritten`" — establishes that two mechanisms exist without stating
their relationship to the one `Checkpoint` entity.

## Operational consequence if left unresolved

FBL-019 must implement atomic sealing for three scope types under one rule. The implementer picks
one of two paths, and both are bad:

**Never seal scan checkpoints.** Then `domain-model.md:1152` makes them unusable as resume points, so
an interrupted scan restarts from zero. This is not hypothetical: `file-identity-model.md:254` makes
connection loss, remount, or reconnect "a checkpoint-invalidating event", and STOP-15 stops the batch
on each. On any network adapter — every non-`local-posix` option in OD-016 — a multi-hour G4 inventory
over a real corpus is interrupted routinely and **can never make forward progress**.
`Scan.checkpoint_cursor` and the `checkpointed` state become dead fields.

**Seal them with null plan and approval bindings.** This introduces a nullable-binding checkpoint
path — and the same path is then reachable for *batch* checkpoints, silently weakening B-CHECKPOINT
for mutation, which is the barrier that makes crash row I14 safe.

Either way the resume-correctness property V1-ACC-036 and PILOT-012 assert is proven only for
batches, while the scan half is untested. **And more sharply:** with no scan-specific seal
precondition, nothing forces a resuming scan to re-confirm root volume identity, so a scan resumed
across a remount produces one inventory silently spanning two different volumes — exactly what RI-2
(`file-identity-model.md:82`) and STOP-1 exist to prevent.

## Affected domain entities and fields

`Checkpoint` — nine field additions or clarifications (below). `Scan.checkpoint_cursor`,
`Scan` lifecycle state `checkpointed`. `SourceRoot.root_identity_evidence.volume_identifier` (PF-11,
PKT-03) — the operand CK-4 compares.

## Affected events, commands, reason codes, and persistence records

Record types `checkpoint` and `checkpoint_sealed` gain a discriminator and per-kind payload. Events
`ScanCheckpointed` and `CheckpointWritten` acquire a stated source-record mapping (CK-5). New reason
codes: `CHECKPOINT_KIND_PAYLOAD_INVALID`, `CHECKPOINT_ROOT_CURSOR_MISSING`,
`CHECKPOINT_VOLUME_IDENTITY_CHANGED`, `CHECKPOINT_CONNECTION_EPOCH_CHANGED`.

## Proposed normative resolution

Introduce a discriminator, with per-kind required payload and per-kind sealing preconditions.

### Field additions to `Checkpoint`

| Field | Type | Required | Nullable | Notes |
| --- | --- | --- | --- | --- |
| `checkpoint_kind` | enum `scan \| batch \| reconciliation` | yes | no | Must match `scope_type`. |
| `chain_head_hash` | string `<alg>:<hex>` | yes | no | |
| `counts` | object | yes | no | Per-kind shape. |
| `plan_id` | ref | conditional | yes | Non-null **iff** `checkpoint_kind == batch`. |
| `plan_version` | string | conditional | yes | Same condition. |
| `approval_id` | ref | conditional | yes | Same condition. |
| `root_enumeration_cursors` | map `source_root_id → opaque` | conditional | yes | Non-null and **non-empty** iff kind is `scan`. |
| `root_volume_identifiers` | map `source_root_id → bytes \| "unavailable"` | conditional | yes | Non-null iff kind is `scan`. **Never null-coerced** — absence is the explicit token `unavailable` (IK-1). |
| `adapter_connection_epoch` | integer ≥ 0 | yes | no | Incremented on every reconnect, remount, or connection loss. |

### Replace the single sealing rule with a per-kind table

| `checkpoint_kind` | `checkpoint_sealed` may be appended only when |
| --- | --- |
| `batch` | *(unchanged)* every record through the sequence is durable; **no operation is non-terminal**; the projection is advanced to exactly that sequence and fsynced; the chain verifies from the previous sealed checkpoint. |
| `scan` | Every record through the sequence is durable; **every in-scope source root has a recorded, resumable enumeration cursor**; **every in-scope root's `volume_identifier` is byte-equal to the value in the previous sealed checkpoint** (or this is the first); `adapter_connection_epoch` is unchanged since that checkpoint; the projection is advanced and fsynced; the chain verifies. |
| `reconciliation` | Every record through the sequence is durable; **no recovery finding is unresolved** and no operation is non-terminal at that sequence; the projection is advanced and fsynced; the chain verifies. |

### Invariants

| ID | Rule |
| --- | --- |
| CK-1 | Exactly one `checkpoint_kind` per checkpoint, matching `scope_type`. |
| CK-2 | `plan_id`, `plan_version`, and `approval_id` are non-null **if and only if** the kind is `batch`. A null triple on a batch checkpoint is unconstructible — this is what prevents the nullable-binding path from leaking into mutation. |
| CK-3 | The "only sealed checkpoints resume" rule (`domain-model.md:1152`) applies unchanged to all three kinds. It is now *satisfiable* for scans rather than vacuous. |
| CK-4 | A scan checkpoint is invalidated by any change to an in-scope root's `volume_identifier` or to `adapter_connection_epoch` (RI-2, STOP-1, STOP-15). Resume from an invalidated checkpoint is **refused explicitly**, not silently ignored. |
| CK-5 | `ScanCheckpointed` is the derived event of a `checkpoint_sealed` record whose kind is `scan`; `CheckpointWritten` is the derived event of the `checkpoint` record. This is the relationship `event-model.md:165` leaves unstated, and it satisfies PKT-08's EP-1 and EP-2. |

## Alternatives considered

**Forbid scan checkpoints entirely and restart scans from zero.** Rejected: `Scan.checkpoint_cursor`
and the `checkpointed` state already exist, and STOP-15 makes interruption routine on every network
adapter, so a G4 inventory over a real corpus could never complete.

**Exempt scan checkpoints from sealing.** Rejected: `domain-model.md:1152` renders unsealed
checkpoints unusable, so this is the first alternative plus wasted records — and it removes the
volume-identity re-confirmation that is the thing making resume safe.

## Safety implications

Touches global invariant 17 (`domain-model.md:29`, resume without incorrectly repeating) and, more
sharply, the identity invariant RI-2 — "Remount under a different device, or a re-exported share, is
not a resumable condition." Without a scan-kind seal precondition that compares volume identifiers, a
resumed scan can span two volumes and produce an inventory whose `logical_file_id` assignments
reference objects on a device that is no longer present. It does not touch a mutation invariant
directly.

## Migration and compatibility implications

Additive to a record type. No checkpoints exist. The `checkpoint` payload is a `record_hash` preimage,
so this must land before FBL-019 writes the first checkpoint; afterwards it changes canonical
serialization and breaks every chain already written.

## Required tests

**Positive** — seal a scan checkpoint with all roots cursored and volume identifiers stable; resume
yields no re-enumeration of completed subtrees and **no duplicate `logical_file_id` minting**. Seal a
batch checkpoint: unchanged behaviour, all four original preconditions enforced. Seal a reconciliation
checkpoint only after every finding is resolved.

**Negative** — a batch checkpoint with a null `plan_id` is unconstructible (CK-2). A scan checkpoint
whose root cursor map is empty cannot seal. A scan checkpoint sealed under volume identifier V1
**refuses** resume when the root now reports V2, and the refusal is explicit rather than a silent
ignore (CK-4, STOP-1). Resume from an unsealed checkpoint of any kind is refused.

**Failure-injection** — crash row **I14**: SIGKILL between `checkpoint` and `checkpoint_sealed` for
each of the three kinds; the unsealed checkpoint is ignored and resume falls back to the prior sealed
one. Force a reconnect mid-scan so `adapter_connection_epoch` increments: the in-flight checkpoint
cannot seal and in-flight change tokens are invalidated (`file-identity-model.md:254`, STOP-15). Kill
mid-seal, restart, confirm the seal is re-derived and not resumed from partial state (row I16).

**A fixture gap this packet surfaces.** FBL-007's injection harness supplies the crash cases and the
identity fixtures behind V1-ACC-005 supply the remount case — but **no scan-checkpoint fixture family
is enumerated anywhere in the ladder.** FBL-019 must add one, and that gap should be recorded as part
of adopting this packet rather than discovered during implementation.

## Required documentation changes

`domain-model.md` `Checkpoint` required fields and invariants; `durability-and-recovery-model.md:240–241`
(record payload and the per-kind sealing table); `event-model.md:165` (the CK-5 mapping).

## Required ADR changes

**ADR-013** — append to Decision: "A checkpoint's sealing preconditions are a function of its kind.
Scan, batch, and reconciliation checkpoints seal under different conditions, and the preconditions for
one kind are never applied vacuously to another — a precondition that is trivially satisfied for a
scope with no operations seals nothing. The four projection states remain derived values in every
case."

**ADR-016** — append to Consequences: "Advancing the projection to exactly the checkpoint sequence is
a sealing precondition for every checkpoint kind, including read-only scans."

## Operator policy, or pure specification defect?

**Pure specification defect.** Checkpoint *cadence* is operator-calibrated and adjacent to OD-008, but
the sealing *rule* is not a policy question. **Claude proposes no cadence value.**

## Atomicity

**PKT-03 is a hard prerequisite** — `root_volume_identifiers` compares a `SourceRoot` field that PF-11
reports does not exist on the entity, so CK-4 is unimplementable until PKT-03 lands.

**PKT-02** — the checkpoint payload gains fields, and PF-02's choice of whether scan-progress facts
are journal-derived or re-derivable determines how much a scan checkpoint's resume value is worth.

**PKT-01** — the checkpoint record preimage.

**PKT-08** — CK-5 is an EP-1/EP-2 mapping and should be drafted with the parity rule, not after it.

## Provenance note

This finding's analysis was produced outside the analysis lane that owns FBL-019, and its claims were
independently re-verified against the repository at commit `8838ac6` before being written here:
`domain-model.md:1130`, `:1152`, `:191`, `:203`, `durability-and-recovery-model.md:240–241`, and
`event-model.md:165` were each read and match the quotations above. It has **not** been cross-checked
against any parallel proposal for FBL-019, and reviewers should treat overlap with one as possible.

## Verification procedure

Re-run `foundation_self_review.py` and `validate_build_ladder.py`. Independently: confirm the sealing
section lists three kinds; confirm no sealing precondition for `scan` mentions operations; confirm
`event-model.md:165` now names the source record for each of the two events.

## Change-control authority

Change control per `docs/05-governance/change-control.md`. No operator decision is required.
**This packet is non-authoritative and confers no authority of its own.**
