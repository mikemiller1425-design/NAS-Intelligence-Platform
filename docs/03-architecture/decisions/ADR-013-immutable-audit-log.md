# ADR 013: Immutable audit log

Status: Accepted (foundation candidate)

## Context
The system needs an evidence trail that cannot be casually rewritten after the fact. Auditability is a core safety property.

## Decision
Significant events are written to an append-only, hash-chained journal treated as immutable evidence **and as the authoritative record**. Each record carries a sequence number monotonic within its stream, a hash over its canonical serialization, and a link to its predecessor's hash. No record is ever edited in place. Any field describing the *processing status* of a record — a write state, or a checkpoint's open/persisted/sealed/invalidated state — is a **derived projection value** and must not appear as a mutable field inside the append-only record itself.

## Consequences
This supports post-incident review and accountability. Truncated tails become detectable and discardable; mid-file corruption, sequence gaps, and chain splices become detectable and halt the system rather than being silently repaired. It resolves the contradiction between a mutable write-state field and the append-only requirement: status is projected, never stored inside the record.

## Alternatives considered
Mutable audit tables or logs that can be edited in place.
