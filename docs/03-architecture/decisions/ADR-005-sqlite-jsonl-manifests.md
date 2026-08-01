# ADR 005: SQLite plus JSONL manifests

Status: Accepted (foundation candidate)

## Context
The platform needs both queryable structured state and durable append-only evidence. One storage format is not ideal for both jobs.

## Decision
The append-only JSONL Execution Journal is the **authoritative** durable record of intent and outcome. SQLite is a **derived, rebuildable projection** used for coordination, lookups, and structured queries. Where the two disagree, the Journal wins unconditionally. Every SQLite row must be reconstructible by replaying the Journal from genesis; no fact required for safety, recovery, reconciliation, audit, or authorization may exist only in SQLite. See `ADR-016` and `docs/02-specification/durability-and-recovery-model.md`.

## Consequences
This keeps operational queries fast while preserving a replayable history. Drift is not prevented by discipline; it is made harmless by construction — a divergent or corrupt projection is discarded and rebuilt from the Journal without operator approval. Rebuildability is a tested property, not an aspiration.

## Alternatives considered
Only SQLite, only JSON, or a logless in-memory model.
