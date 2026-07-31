# Observability

## Purpose
Observability exists so operators can understand what the platform did, why it did it, and whether safety constraints held.

## Observability Signals
- Structured logs for inventory, proposal, approval, execution, and verification events.
- Metrics for scan volume, classification counts, approval latency, verification success, and failure rates.
- Trace or correlation identifiers for linking proposal to approval to execution.
- Immutable audit log entries for decisions and outcomes.

## Log Design
- Logs should be structured and machine-readable.
- Dry-run and live-mode outcomes must be distinguishable.
- Every destructive proposal should carry an explanation and stable identifier.
- Audit evidence must be append-only and durable.

## Operational Views
- Health view for overall pipeline liveness.
- Safety view for blocked or rejected actions.
- Review view for pending approvals and unresolved ambiguities.
- Sentinel view for alert status and watch conditions.

## Constraint
Observability is for understanding and governance. It is not a back door around approval or filesystem policy.
