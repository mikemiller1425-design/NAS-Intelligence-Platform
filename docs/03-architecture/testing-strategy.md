# Testing Strategy

## Strategy Goal
Testing must prove safety properties, not just functional behavior. The test strategy should be able to demonstrate that dry-run is the default, approvals are required for destructive actions, and evidence is retained.

## Test Layers
- Unit tests for pure decision logic, classification rules, and planning.
- Integration tests for adapters, persistence, and pipeline interactions.
- Safety tests for destructive-action gating, overwrite prohibition, and approval enforcement.
- Acceptance tests for review flows, dry-run behavior, and audit evidence.
- Fixture-based tests for representative NAS scenarios and edge cases.

## Required Themes
- Read-only inventory remains read-only.
- Exact duplicates resolve through hash evidence.
- Frontend actions cannot authorize filesystem mutation.
- Sentinel behavior stays alert-only.
- Every approved mutation records an audit trail.

## Test Data Posture
Fixtures should be representative but non-sensitive. They must support replayable scenarios without requiring live production data.

## Exit Criteria
The test suite should show that the architecture enforces the blueprint rules before any implementation is promoted toward live operation.
