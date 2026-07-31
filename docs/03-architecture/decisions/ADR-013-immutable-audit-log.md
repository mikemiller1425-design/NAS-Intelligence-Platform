# ADR 013: Immutable audit log

Status: Accepted (foundation candidate)

## Context
The system needs an evidence trail that cannot be casually rewritten after the fact. Auditability is a core safety property.

## Decision
Significant events are written to an append-only audit log that is treated as immutable evidence.

## Consequences
This supports post-incident review and accountability. It also places pressure on the persistence design to separate audit records from mutable working state.

## Alternatives considered
Mutable audit tables or logs that can be edited in place.
