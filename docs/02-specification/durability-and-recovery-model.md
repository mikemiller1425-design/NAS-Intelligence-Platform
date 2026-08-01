# Durability and Recovery Model

## Purpose

This document defines the **single authoritative durability and recovery protocol** for the NAS Intelligence Platform. It resolves audit finding **FND-M003**.

It supersedes any conflicting statement about storage authority, write ordering, partial-write handling, checkpoint atomicity, or restart behavior found elsewhere in the repository.

**This document authorizes no filesystem mutation.** It defines the conditions under which a separately authorized mutation may proceed.

## Authority statement

> **The append-only Execution Journal is the authoritative durable record. SQLite is a derived, rebuildable projection.**

1. The Execution Journal — JSONL, append-only, hash-chained, checksummed — is the **sole authoritative record of intent and outcome** for every filesystem mutation, approval, consumption, revocation, checkpoint, and recovery action.
2. SQLite holds **only derived state**: indexes, projections, query accelerators, current-state summaries. Every SQLite row must be reconstructible by replaying the Journal from the beginning.
3. Where the Journal and SQLite disagree, **the Journal wins, unconditionally and without operator discretion.**
4. SQLite must never be the only durable home of any fact required for safety, recovery, reconciliation, audit, or authorization. If a fact matters, it is in the Journal.
5. The observability event stream is **derived from the Journal** and is authoritative for nothing. Events may be lost, duplicated, or reordered without affecting correctness.
6. Filesystem state is **evidence, not authority**. The Journal states what was intended and what was reported; the filesystem states what currently exists. Reconciliation resolves the two. Neither may silently overrule the other.

### Why the journal and not the database

- **Recovery requires an intent record that predates the mutation.** A database can record that something happened; only an append-only log can record that something is *about to* happen and survive a crash mid-mutation. Without a durable pre-mutation intent, an interrupted copy is an unattributable artifact.
- **A single-writer append-only file has a far smaller crash-consistency surface** than a B-tree with a write-ahead log, page cache, and checkpointer. A truncated tail is detectable and discardable; a torn B-tree page is not.
- **The data architecture already requires it**: every important decision must be reconstructable from stored evidence *without requiring access to mutable application state*. SQLite is mutable application state. That requirement is only satisfiable if the Journal is authoritative.
- **Rebuildability is testable.** "SQLite is derived" is verified by deleting the database and rebuilding it from the Journal. "The two stores do not drift" is not testable and has no failure signal.

## Storage topology and durability classes

| Volume | Contents | Required durability class |
| --- | --- | --- |
| `CONTROL` | Journal segments, checkpoint records, nonce ledger, SQLite database, recovery sidecars | `strong` (mandatory) |
| `DEST` | Destination roots, temporary staging directories | `strong` preferred; `weak`/`unknown` triggers degraded mode |
| `SRC` | Source roots | read-only; no durability requirement |

`CONTROL` must not reside inside any recursively scanned source root, and must be outside the mutable data path.

Every adapter declares, per volume:

```yaml
durability_class: strong | weak | unknown
capabilities:
  fsync_file:             true | false | unverified
  fsync_directory:        true | false | unverified
  atomic_same_dir_rename: true | false | unverified
  exclusive_create:       true | false | unverified
  reports_fsync_errors:   true | false | unverified
```

`strong` requires all five verified true by a startup self-test. Anything unverified is `unknown`, and `unknown` is treated as `weak`.

## Journal structure

### Segments

One writer per run. Concurrent writers to a segment are forbidden. Segments roll at a configured size or at seal points; a rolled segment is immutable.

### Record framing

One record per line, UTF-8, newline-terminated. A record is **valid** if and only if:

1. the line is newline-terminated (an unterminated final line is a truncated tail);
2. the line parses as a single JSON object;
3. all required envelope fields are present and well-typed;
4. `record_hash` equals the digest over the canonical serialization of the record with `record_hash` removed;
5. `prev_record_hash` equals the `record_hash` of the immediately preceding valid record in the same stream, or the genesis constant;
6. `seq` equals the preceding record's `seq + 1`.

Rules 4–6 make the Journal a hash chain. Any in-place edit, reordering, deletion, or splice is detectable.

### Envelope

```yaml
stream_id: "jnl_run_2026_0731_a"
seq: 1041
record_type: "op_intent"
record_hash: "sha256:…"
prev_record_hash: "sha256:…"
written_at: "2026-07-31T23:00:00.123456Z"
writer: "mac-mini-engine/exec-1"
run_id: "run_456"
batch_id: "batch_012"
schema_version: 1
correlation_id: "run_456"
causation_id: "cmd_789"
payload: { }
```

> A record in the Journal is durable, or it does not exist. Any field describing the *processing status* of a record — a write state, or a checkpoint's open/persisted/sealed/invalidated state — is a **derived projection value** and must never appear as a mutable field inside the append-only record. A mutable status field inside an append-only log is a contradiction.

### Operation identity and idempotency

```text
idempotency_key = (plan_id, plan_version, entry_id)
operation_id    = "op_" + digest(canonical(idempotency_key))[0:32]
attempt_seq     = 0, 1, 2, …
temp_path       = <dest_dir>/.nasip-tmp/<operation_id>.<attempt_seq>.part
```

- `operation_id` is **deterministic and stable across restarts and retries**. This is the concrete satisfaction of "every action has a stable operation ID".
- Every temporary file on disk is attributable to exactly one operation and attempt **by filename alone**.
- Replaying the same plan version cannot produce a second destination copy.
- `temp_path` must be on the same filesystem as `destination_path` so that same-directory rename is atomic.

### Record types

| Record type | Meaning |
| --- | --- |
| `run_open` | Run begins; binds engine identity, adapter durability classes, config hash |
| `plan_bound` | Binds plan id, version, content hash, approval id, precondition-set hash |
| `approval_granted` / `approval_consumption_claimed` / `approval_consumed` / `approval_consumption_released` / `approval_revoked` / `approval_invalidated` | Authoritative approval records |
| `op_intent` | Declares operation, attempt, source, destination, temp path, preconditions, collision policy |
| `op_temp_durable` | Temp file fully written and flushed; observed size and hash |
| `op_verify_result` | Independent re-read verification outcome |
| `op_finalized` | Atomic finalize performed |
| `op_outcome` | Terminal disposition: `committed`, `failed`, `skipped`, `abandoned` |
| `checkpoint` / `checkpoint_sealed` | Restart cursor and its seal |
| `recovery_scan_started` / `recovery_finding` / `recovery_action` / `recovery_truncated_tail` / `recovery_completed` | Recovery is itself journalled |
| `segment_sealed` | Segment closed; chain head recorded |
| `run_halted` / `run_close` | Terminal run records |

### Durability barriers

A **barrier** is: append the record, flush and fsync the segment file, fsync the segment directory on segment creation, and confirm the write returned success.

Mandatory barriers — each must complete before the next protocol step is attempted:

| Barrier | After |
| --- | --- |
| **B-INTENT** | `op_intent`, before *any* filesystem mutation for that operation |
| **B-FINAL** | `op_finalized` |
| **B-OUTCOME** | `op_outcome` |
| **B-APPROVAL** | `approval_granted`, `approval_consumption_claimed`, `approval_consumed`, `approval_revoked` |
| **B-CHECKPOINT** | `checkpoint`, before `checkpoint_sealed` |

Group commit is permitted for `op_temp_durable`, `op_verify_result`, and `recovery_finding`, whose loss is recoverable by re-deriving state from the filesystem. They must nonetheless be durable before the next mandatory barrier.

## Ordered write protocol for a single file operation

**HALT** means: append `run_halted` with the reason code, stop issuing new intents, begin no further filesystem mutation, and surface an operator reconciliation requirement.

### Phase A — Preconditions (no durable writes, no mutation)

| Step | Action | Failure branch |
| --- | --- | --- |
| A1 | Journal writability probe: confirm `CONTROL` is `strong`; append and fsync a heartbeat. | HALT `JOURNAL_UNWRITABLE`. Mutation is forbidden. |
| A2 | Approval authorization evaluation (see `approval-binding-model.md`). | Record `op_outcome = failed` with the reject code. HALT if the code is in the halting class. |
| A3 | Path safety: normalize; confirm source and destination are under approved roots; reject traversal and symlink escape. | HALT `PATH_ESCAPE`. |
| A4 | Source revalidation: re-read size and hash; compare to plan preconditions; compare change token. | `SOURCE_DRIFT` → `op_outcome = failed`; entry to unresolved; approval invalidated for that entry. |
| A5 | Destination policy: confirm absent, or resolve by the plan's explicit collision policy; confirm not a protected vault. | `COLLISION_UNRESOLVED` / `PROTECTED_VAULT` → `op_outcome = failed`. Never overwrite. |
| A6 | Capacity and thresholds. | `THRESHOLD_EXCEEDED` → pause the batch; no mutation. |
| A7 | Idempotency check: look up `operation_id`. Terminal `committed` → skip. Non-terminal → this is a resume; enter recovery for that operation. | Ambiguous state → HALT `AMBIGUOUS_OPERATION_STATE`. |

### Phase B — Intent

| Step | Action | Failure branch |
| --- | --- | --- |
| B1 | Compute `operation_id`, select `attempt_seq`, compute `temp_path`. | HALT `IDENTITY_COMPUTATION_FAILED`. |
| B2 | Append `op_intent`. **Barrier B-INTENT.** | Append error → no mutation occurred, nothing to clean; HALT `JOURNAL_APPEND_FAILED`. fsync error → treat as data loss; HALT `JOURNAL_FSYNC_FAILED`; do not reuse the descriptor. |

> **Gate G.** No filesystem mutation for this operation may be attempted before B-INTENT completes. This is the rule that makes every possible on-disk artifact attributable.

### Phase C — Temp write

| Step | Action | Failure branch |
| --- | --- | --- |
| C1 | Create destination and staging directories; fsync the parent. | `DEST_DIR_CREATE_FAILED` → `op_outcome = failed`. |
| C2 | Create `temp_path` with exclusive create. If it exists, it is a prior attempt's orphan — do not reuse; increment `attempt_seq`. | `TEMP_CREATE_FAILED` → `op_outcome = failed`. |
| C3 | Stream source bytes to `temp_path`, hashing inline. | `SOURCE_READ_FAILED` / `TEMP_WRITE_FAILED` → `op_outcome = failed`; the partial temp is attributable and handled by the orphan policy. |
| C4 | fsync the temp file. | `TEMP_FSYNC_FAILED` → bytes are not durable → `op_outcome = failed`. |
| C5 | fsync the parent directory. | `DIR_FSYNC_FAILED` → `op_outcome = failed`; HALT `DURABILITY_CLASS_VIOLATION` if `strong` was declared. |
| C6 | Append `op_temp_durable`. | HALT `JOURNAL_APPEND_FAILED`. |

### Phase D — Verify

| Step | Action | Failure branch |
| --- | --- | --- |
| D1 | Re-open and independently re-read all bytes, recomputing the hash. Re-read is mandatory on `weak` destinations. | `VERIFY_READ_FAILED` → `op_outcome = failed`. |
| D2 | Compare verification hash and size to plan preconditions. | `HASH_MISMATCH` → `op_outcome = failed`; halt the batch. |
| D3 | Append `op_verify_result`. | HALT `JOURNAL_APPEND_FAILED`. |

### Phase E — Atomic finalize

| Step | Action | Failure branch |
| --- | --- | --- |
| E1 | Re-check immediately before finalize that `destination_path` does not exist. | `LATE_COLLISION` → do not overwrite; `op_outcome = failed`. |
| E2 | Atomically finalize by same-directory rename on a `strong` destination. Rename atomicity must not be assumed on `weak`/`unknown`. | `FINALIZE_FAILED` → re-probe the destination and record the observed state. Inconclusive probe → HALT `FINALIZE_INDETERMINATE`. |
| E3 | fsync the destination parent directory. | `DIR_FSYNC_FAILED` → do **not** claim success. HALT `DURABILITY_CLASS_VIOLATION` on `strong`; mark `durability: unproven` and force degraded mode on `weak`. |
| E4 | Append `op_finalized`. **Barrier B-FINAL.** | HALT `JOURNAL_APPEND_FAILED`. |

### Phase F — Outcome and projection

| Step | Action | Failure branch |
| --- | --- | --- |
| F1 | Append `op_outcome = committed`. **Barrier B-OUTCOME.** | HALT `JOURNAL_APPEND_FAILED`. |
| F2 | Apply the operation's records to the SQLite projection in one transaction that also advances the journal cursor. | SQLite is derived: a projection failure is **not** a data-safety event and must not be reported as one. Mark the projection stale and rebuild later. HALT `PROJECTION_UNAVAILABLE` only if authorization lookups cannot be served. |
| F3 | Source retirement, if and only if the approved phase and approval scope permit it, is a **separate operation** with its own intent and outcome records and its own approval scope flag. It is never a tail step of the copy. | Per the retirement gate. |

### When the next filesystem mutation may begin

> The next filesystem mutation must not be attempted until a terminal `op_outcome` record for the preceding operation has completed barrier **B-OUTCOME**, and the preceding operation has left no unresolved on-disk artifact — no temp file at a path named in a non-terminal `op_intent`.
>
> The SQLite projection is derived and may lag. A stale projection is **not** a reason to delay the next mutation, and an up-to-date projection is **not** a substitute for a durable terminal outcome record.
>
> **Default V1 concurrency is one in-flight mutation per run.** Bounded concurrency may be enabled only when every concurrent operation has its own durable intent before its own first mutation; the operations' source, destination, temp, and destination-parent paths are pairwise disjoint; the destination volume is `strong`; and the run is not degraded. Concurrency must be disabled for any run in which source retirement is permitted.
>
> After a HALT, **no** filesystem mutation may begin until restart reconciliation completes with status `CONSISTENT` and an operator has cleared the halt.

## Deterministic crash-state table

One row per interruption point. "Next mutation allowed?" means: may the engine begin *any* new filesystem mutation after the stated recovery action completes.

| # | Interruption point | Observable filesystem state | Journal state | SQLite state | Authoritative interpretation | Required recovery action | Next mutation allowed? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I0 | During Phase A, before B2 | Unchanged | No intent for this operation | Entry may show queued | **Nothing was attempted.** | None. Re-evaluate approval from scratch; re-run Phase A. | Yes, after reconciliation |
| I1 | Intent line written, fsync not returned | Unchanged | Tail absent, unterminated, or valid | Unchanged | **Indeterminate but safe** — Gate G forbids mutation before B-INTENT completes. | If the tail is invalid, discard it and record the discard. Treat as I0. | Yes, after reconciliation |
| I2 | B-INTENT complete, before C1/C2 | Unchanged; no temp file | Valid intent; no temp-durable; no terminal | Entry executing | **Intent declared, nothing done.** | Confirm temp and destination absent. Append `op_outcome = abandoned`. Re-eligible at a new attempt. | Yes, after reconciliation |
| I3 | During C3 streaming | Partial temp; destination absent | Valid intent; no temp-durable | Entry executing | **Partial temp, attributable.** Destination untouched. | Verify destination absent. Quarantine the partial temp. Append abandoned outcome. | Yes, after reconciliation |
| I4 | C3 complete, before C4 fsync | Temp may look complete but is **not durable** | Valid intent; no temp-durable | Entry executing | **Identical to I3.** Absence of the temp-durable record means the bytes are untrusted regardless of the directory listing. | Same as I3. Never adopt a temp lacking its durable record. | Yes, after reconciliation |
| I5 | C4/C5 complete, before C6 durable | Temp durable and complete; destination absent | Valid intent; no temp-durable | Entry executing | **Bytes may be good but unproven.** The Journal does not vouch for them. | Do not adopt. Quarantine, abandon, retry at a new attempt. Re-copying is cheap; adopting unproven bytes is not. | Yes, after reconciliation |
| I6 | C6 durable, before D1 | Temp durable; destination absent | Intent + temp-durable | Entry executing | **Temp durable and attributable; verification outstanding.** | Resume at D1 against the existing temp. | Yes, after reconciliation |
| I7 | D1/D2 complete, before D3 durable | Temp durable; destination absent | Intent + temp-durable; no verify record | Entry executing | **Same as I6** — an unrecorded verification did not happen. | Re-verify (idempotent), continue at E1. | Yes, after reconciliation |
| I8 | D3 durable, before E2 rename | Temp durable and verified; destination absent | Intent + temp-durable + verify pass | Entry executing | **Verified temp awaiting finalize.** | Re-run the E1 collision guard, then E2–E4. Resume; do not restart the copy. | Yes, after reconciliation |
| I9 | Rename issued, before E3 directory fsync | Destination **may or may not** exist; temp may or may not exist | No finalize record | Entry executing | **The most dangerous window.** Finalize is indeterminate; the Journal claims no success. | Probe both paths. (a) destination exists and re-read hash matches → adopt, append finalize + committed. (b) destination exists, hash mismatches → quarantine, HALT `RECOVERY_HASH_MISMATCH`. (c) destination absent, temp verified → resume at E1. (d) both absent → abandon, retry at a new attempt. | (a), (c), (d) yes after reconciliation; (b) **no** until operator clears |
| I10 | E3 complete, before E4 durable | Destination exists and is durable; temp gone | No finalize record | Entry executing | **Identical handling to I9** — the Journal cannot distinguish I9 from I10 and must not try. | Same branch (a): re-read and adopt on hash match. | Yes, after reconciliation |
| I11 | B-FINAL complete, before F1 durable | Destination exists and is durable | Finalize present; no terminal outcome | Entry executing | **Finalize durably claimed; disposition not recorded.** | Re-read the destination hash; append committed. Mismatch → HALT `POST_FINALIZE_DRIFT`. | Yes, after reconciliation |
| I12 | B-OUTCOME complete, before F2 projection | Destination exists and is durable | Terminal committed | Entry still executing (**stale**) | **Operation is complete.** SQLite is merely behind. Normal and expected. | Replay records after the applied cursor into SQLite. No filesystem action. | Yes |
| I13 | F2 applied, before the checkpoint record | Destination exists | Terminal outcome; no new checkpoint | Projection current | **Complete; resume cursor stale.** | Replay from the last sealed checkpoint forward; terminal operations are skipped by A7, so no duplicate copy is possible. | Yes |
| I14 | Checkpoint durable, before it is sealed | Unchanged | Checkpoint present, seal absent | May lag | **Checkpoint exists but is NOT usable for resume.** | Ignore the unsealed checkpoint; resume from the last sealed one; seal a fresh one after reconciliation. | Yes, after reconciliation |
| I15 | Mid segment-roll; prior segment unsealed | Unchanged | Two segments; chain head only in the old segment's last record | Any | **Chain still verifiable** by reading both segments in index order. | Verify the chain across the boundary; append the seal as a recovery action, never by editing the old segment. | Yes, after reconciliation |
| I16 | Crash during recovery itself | Any of the above | Partial recovery records | Any | **Recovery is journalled and idempotent.** | Restart recovery from the beginning. Findings are re-derived, not resumed. | Only after a `recovery_completed(CONSISTENT)` record |

## Checkpoints, sealing, and journal integrity

### Checkpoint creation and sealing

A checkpoint is **two journal records**, never a mutable object:

1. `checkpoint` — cursor, chain head hash, counts, plan and approval binding. **Barrier B-CHECKPOINT.**
2. `checkpoint_sealed` — appended only after every record through the checkpoint sequence is durable; no operation is in a non-terminal state at that sequence; the SQLite projection has been advanced to exactly that sequence and fsynced; and the chain verifies from the previous sealed checkpoint.

**Only a sealed checkpoint may be used as a resume point.** An unsealed checkpoint is ignored.

### Truncated final record

Detection: the last line is unterminated, fails to parse, or fails its hash.

1. Copy the raw trailing bytes to a recovery sidecar. **Never delete them.**
2. Truncate the segment to the end of the last valid record.
3. Append `recovery_truncated_tail` recording the discarded length, sidecar path, and digest of the discarded bytes.
4. Interpret the run as the state implied by the last valid record, then apply the crash-state table.

A truncated tail is the expected, benign crash signature of an append-only file. Discarding it is safe **only because** Gate G guarantees that no filesystem mutation can be authorized by a record that never became durable.

### Corrupt mid-file record

Detection: a record fails validation and is **not** the final record.

**HALT `JOURNAL_CHAIN_BROKEN`. Do not repair. Do not skip. Do not resume.**

- The authoritative record is untrustworthy, so no interpretation of filesystem state is defensible.
- Mid-file corruption implies media failure or unauthorized edit; both are incidents.
- Preserve the segment untouched and snapshot it; require operator adjudication.
- Recovery may, under explicit operator authorization, replay only the prefix up to the corrupt record and treat everything after as unknown — forcing every subsequent operation into the I9 indeterminate branch. This is an operator decision, never automatic.

Sequence gaps and chain splices are treated identically.

### Duplicated delivery

Three independent layers:

1. **Journal level** — a record is uniquely identified by `(stream_id, seq)`. Two records sharing that pair is a chain break.
2. **Projection level** — applying a record at or below the applied cursor is a **no-op**; applying one beyond cursor + 1 is a hard stop (`PROJECTION_GAP`). This makes replay exactly-once against SQLite.
3. **Effect level** — every side-effecting operation is keyed by `operation_id`, and Phase A7 short-circuits any operation with a terminal committed outcome.

Derived observability events may be duplicated freely and must be consumed idempotently by event id; they carry no authority and no side effects.

## Restart reconciliation algorithm

Executed before any mutation, on every start.

| Step | Action |
| --- | --- |
| R1 | Acquire the exclusive run lock on `CONTROL`. Another live writer → HALT `CONCURRENT_WRITER`. |
| R2 | Adapter self-test: re-derive durability classes. `CONTROL` not `strong` → HALT. Destination downgraded → degraded mode and approval invalidation. |
| R3 | Enumerate segments in index order; verify no index gaps. |
| R4 | Verify the chain from genesis or from the last sealed checkpoint's chain head. Truncated tail → discard and continue. Mid-file corruption, gap, or splice → HALT. |
| R5 | Select the resume point: the highest sealed checkpoint, or genesis. |
| R6 | Fold records forward into a per-operation state machine; classify each operation as terminal or as a crash-table row. |
| R7 | Fold approval records into per-approval state; resolve dangling claims. |
| R8 | Compare the SQLite cursor and chain head to the derived chain. Behind and consistent → replay forward. Chain-head mismatch, or ahead of the Journal → **discard and rebuild SQLite from genesis.** A projection that claims to know more than the Journal is corrupt by definition. |
| R9 | Bounded filesystem probe — for non-terminal operations only, never a full-tree walk. Record each observation. |
| R10 | Apply the crash-state table row by row, appending recovery actions and terminal outcomes. Any HALT branch aborts with an operator reason code. |
| R11 | Orphan sweep across staging directories named in intents since the resume point. |
| R12 | Emit a verdict: `CONSISTENT` (every operation terminal or safely resumable; no unattributable orphan; projection matches chain head) or `INCONSISTENT` → HALT with a reconciliation requirement. |
| R13 | After `CONSISTENT`, write and seal a fresh checkpoint before resuming. |
| R14 | **Approval re-evaluation.** Resuming does not reuse a stale authorization decision. Every entry re-enters the full authorization algorithm, including a fresh revocation read. |

## Temporary files: partial and orphaned

| Condition | Classification | Required action |
| --- | --- | --- |
| Temp exists; an intent names it; operation non-terminal | **Attributable partial** | Resolve via the crash-state row. Adopt only from I6, I7, I8; otherwise quarantine. |
| Temp exists; an intent names it; operation terminal | **Attributable orphan** | Move to quarantine; append a recovery action. |
| Temp exists in staging; **no** intent names it | **Unattributable artifact** | An integrity violation — Gate G makes this impossible under a correct implementation. Quarantine and **HALT `UNATTRIBUTABLE_ARTIFACT`**. |
| A file exists at the destination path; no intent names it | **Foreign destination content** | Not ours. Do not touch. Record as a collision input. Never overwrite. |

**Temporary files are never permanently deleted in V1.** Quarantine, not deletion, is the disposal path. Quarantine retention remains OD-010.

## Flush and fsync caveats

The protocol rests on three primitives a network filesystem or vendor API may not provide: durable file fsync, durable directory fsync, and atomic same-directory rename. OD-016 leaves the adapter unchosen, so behavior is conditional on the declared class.

### Journal volume

The Journal must live on a `strong` volume. **If no `strong` volume is available for the Journal, filesystem mutation is prohibited.** This is the precise meaning of "journal failure stops mutation". A local disk on the worker satisfies `strong`; SMB, NFS, SSHFS, and vendor HTTP APIs are `weak`/`unknown` for journal purposes unless a self-test proves otherwise.

### Destination volume in `weak` or `unknown` class

1. **No reliance on rename atomicity.** Collision safety comes from exclusive create plus the pre-finalize re-check, never from rename semantics alone.
2. **Mandatory post-finalize re-read.** Re-open, re-read, recompute, and compare. A finalize that cannot be re-verified is `FINALIZE_INDETERMINATE` → HALT.
3. **Degraded mode for the whole run:** batch size 1, no concurrency, a sealed checkpoint after every operation, and **source retirement forbidden for the entire run regardless of approval scope**.
4. **Approval scope must match.** An approval granted while the destination was `strong` is invalidated by a downgrade.
5. **Every outcome record is labelled** `durability: unproven`, and reconciliation reports must disclose the count of unproven finalizations.

### fsync error handling

An fsync error may be reported **exactly once**, and the affected dirty pages may be discarded by the operating system. Therefore:

- An fsync error is **data loss**, never a transient retryable condition.
- Never retry fsync on the same descriptor, and never infer success from a subsequent successful fsync.
- Seal the affected segment as suspect; append the halt record to a new segment if possible; otherwise stop without further writes.
- All mutation stops. Operator adjudication is required.

### Cross-filesystem ordering

The Journal and the data live on different filesystems, so no ordering primitive spans them. The protocol does not need one:

- **Journal-before-data** ordering (Gate G) is achieved by program order plus a completed barrier: the intent record is durable *before the mutation is issued at all*. This holds across any two independent filesystems.
- **Data-before-journal** ordering is deliberately **not** guaranteed. Rows I9 and I10 exist precisely because it cannot be, and both resolve by re-reading and re-hashing the destination rather than by trusting an ordering that does not exist.

## Related documents

- `docs/02-specification/approval-binding-model.md`
- `docs/02-specification/file-identity-model.md`
- `docs/02-specification/preservation-model.md`
- `docs/02-specification/state-and-persistence.md`
- `docs/03-architecture/decisions/ADR-005-sqlite-jsonl-manifests.md`
- `docs/03-architecture/decisions/ADR-013-immutable-audit-log.md`
- `docs/03-architecture/decisions/ADR-016-journal-authoritative-sqlite-derived.md`
