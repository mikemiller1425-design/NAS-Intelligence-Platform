# ADR 005: SQLite plus JSONL manifests

Status: Accepted (foundation candidate)

## Context
The platform needs both queryable structured state and durable append-only evidence. One storage format is not ideal for both jobs.

## Decision
Use SQLite for coordination, lookups, and structured state; use JSONL manifests for immutable event and audit records.

## Consequences
This keeps operational queries fast while preserving a replayable history. It does require disciplined boundary management so the two stores do not drift.

## Alternatives considered
Only SQLite, only JSON, or a logless in-memory model.
