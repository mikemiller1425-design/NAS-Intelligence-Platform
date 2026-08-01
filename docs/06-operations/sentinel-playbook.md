# Sentinel Playbook

## Purpose
Define the Raspberry Pi sentinel's read-only monitoring role, alerting behavior, and strict authority limits.

## Operating rules
- Observe, do not classify.
- Alert, do not approve.
- Request safe predefined jobs only.
- Never mutate the NAS or source data.
- Never become the operational source of truth.

## Inputs
- Worker heartbeat.
- Mount status.
- Journal freshness.
- Queue length.
- Capacity thresholds.
- Manual-review backlog.
- Batch and phase state.

## Authorization required

The Sentinel observes and alerts. It never classifies, approves, or mutates, at any gate.

Running the Sentinel against real infrastructure requires an authorization record for the gate at which it is introduced, per `docs/05-governance/gate-model.md`. Nothing in this document authorizes running it.

## Actions
1. Check health signals on a schedule.
2. Display a read-only status view.
3. Raise alerts for completion, stall, disconnect, capacity risk, and mismatch.
4. Submit only predefined safe job requests.
5. Record status snapshots for auditability.

## Stop conditions
- The sentinel attempts to infer classifications.
- A dashboard control would imply mutation authority.
- A requested action is not on the approved safe list.

## Required evidence
- Health snapshots.
- Alert history.
- Safe-job request log.
- Heartbeat and freshness records.
