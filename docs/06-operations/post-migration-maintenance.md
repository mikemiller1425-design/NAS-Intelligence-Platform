# Post-Migration Maintenance

## Purpose
Define the steady-state maintenance pattern after the initial migration phases are complete.

## Operating rules
- Continuous ingestion remains read-first and approval-bound where required.
- Maintenance never reintroduces silent overwrite or deletion.
- Rule changes are versioned and traceable.
- Source retirement remains gated by hash verification and approval.

## Maintenance activities
- Review new incoming files.
- Reconcile inventory deltas.
- Re-check hashes for any retried or resumed batch.
- Monitor capacity, stalls, and backlog.
- Refresh evidence bundles and archive completed batches.
- Review unresolved and future-registry items on a schedule.

## Stop conditions
- A maintenance task would mutate a protected vault by default.
- Evidence no longer reconciles.
- A rule revision is unreviewed or unversioned.

## Required evidence
- Maintenance log.
- Reconciliation delta report.
- Alert history.
- Current rule version set.
- Archive index for completed batches.
