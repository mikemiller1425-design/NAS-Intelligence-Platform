# State and Persistence

## Purpose

This document defines the persistence model: state boundaries, storage responsibilities, and recovery guarantees. It intentionally avoids production schema code.

> **Authority.** The append-only Execution Journal is authoritative; SQLite is a derived, rebuildable projection. Where they disagree, the journal wins unconditionally. The write protocol, crash-state table, and restart reconciliation algorithm live in `docs/02-specification/durability-and-recovery-model.md`, which governs wherever this document is less specific.

## Recommendation

Use:

- **SQLite** for relational state, checkpoints, and queryable operational records.
- **JSONL** for append-only event, journal, and replay-friendly logs.

This combination is recommended because it supports local-first operation, restart safety, auditability, fixture-driven testing, and a clear separation between mutable working state and immutable history.

## Storage boundaries

### SQLite

Recommended for:

- file inventory records
- scan state
- classification decisions
- duplicate groups
- review items
- taxonomy records
- operation plans
- approvals (derived index; the authoritative approval is a journal record)
- verification summaries
- reconciliation summaries
- checkpoint pointers (derived; the authoritative checkpoint is a journal record pair)
- current health snapshots

### JSONL

Recommended for:

- event streams
- journal entries
- batch progress trails
- replay-safe audit logs
- exportable evidence bundles

### Filesystem artifacts

Recommended for:

- manifest snapshots
- report exports
- fixture bundles
- signed or hashed plan artifacts
- operator-facing evidence archives

## Persistence principles

1. Append-only history is preferred for anything used in audit or recovery.
2. Mutable current state is **derived from** immutable history. It is never a co-equal source of truth, and it is never reconciled *against* history as a peer: on disagreement the history wins and the projection is rebuilt.
3. A restart must not require trust in partially written records.
4. Checkpoints must be atomic.
5. Journal failure stops mutation.
6. Storage paths must remain under approved control roots.

## SQLite state model

SQLite holds the current **derived** state for query-heavy objects, plus pointers to the latest immutable history segments. It is rebuildable from the journal at any time, without operator approval. No fact required for safety, recovery, reconciliation, audit, or authorization may exist only here.

Recommended tables or logical buckets include:

- `source_roots`
- `file_records`
- `scans`
- `metadata_records`
- `hash_records`
- `rule_sets`
- `classification_rules`
- `classification_decisions`
- `duplicate_groups`
- `review_items`
- `taxonomy_nodes`
- `operation_plans`
- `operation_entries`
- `approvals`
- `batches`
- `checkpoints`
- `alerts`
- `system_health`
- `reconciliation_reports`

No production schema is defined here. The names above are logical storage responsibilities only.

## JSONL state model

JSONL should hold the immutable streams:

- events
- journal entries
- execution traces
- replay checkpoints

Each record should contain enough information to reconstruct:

- what happened
- when it happened
- who or what caused it
- what state transition occurred
- what evidence supported it

## Recovery strategy

### Startup reconciliation

On startup, the platform should:

1. read the latest checkpoint
2. verify journal completeness
3. compare current filesystem observations against expected state
4. resume only when the state is consistent
5. otherwise halt and surface a reconciliation requirement

### Partial write handling

If a write is interrupted:

- a truncated **final** record is discarded, its bytes preserved to a sidecar, and the discard recorded; a corrupt **mid-file** record halts the system and is never repaired or skipped
- sequence numbers must remain monotonic
- duplicated event delivery must not create duplicated effects
- a failed journal write stops mutation until resolved

### Replay

Replay rebuilds **all** derived state from the journal into SQLite-backed current state. There is no SQLite content that replay cannot reconstruct; if there were, SQLite would hold unique authority, which this model forbids.

Replay must be idempotent and must never authorize new live work.

## Retention

Recommended retention classes:

- hot: active working state
- warm: recent batches and audits
- cold: archived evidence and frozen reports
- frozen: final release evidence and audit handoff artifacts

Retention policy must be operator-approved and may not silently delete evidence in V1.

## Backup and restore

Backups should cover:

- SQLite state
- JSONL streams
- report artifacts
- manifests and checkpoints

Restore expectations:

- recover the latest safe checkpoint
- preserve immutable history
- reconcile against the filesystem before resuming

## V1 limits

- No production schema code in this specification.
- No live database connection is implied.
- No external service dependency is required for the recommended local-first design.

