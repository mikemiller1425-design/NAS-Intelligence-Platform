# Live Migration Playbook

## Purpose
Define the narrow, approved process for a bounded live batch after dry run, fixtures, and copied pilot have proven the workflow.

## Operating rules
- Live execution is prohibited until explicit authorization exists.
- Copy-first is the default for early live phases.
- Source retirement requires hash verification and explicit approval.
- Protected vaults are not overwritten by default.
- No permanent deletion in V1.

## Preconditions
- Foundation approval exists.
- Live readiness acceptance is satisfied.
- Batch thresholds are calibrated.
- Snapshot and recovery readiness are documented.
- Exact source and destination roots are confirmed.
- Plan version, operator approval, and evidence bundle are frozen.

## Steps
1. Revalidate source preconditions immediately before action.
2. Create destination directories safely.
3. Copy to a temporary destination when required.
4. Verify bytes with cryptographic hashing.
5. Finalize the destination only after verification.
6. Retire the source only when the approved phase and approval explicitly allow it.
7. Append journal entries and checkpoint the batch.
8. Stop on threshold breach or unexpected state.

## Stop conditions
- Plan and source reality diverge.
- A collision would overwrite data.
- Hash verification fails.
- Recovery protection is unavailable.
- Journal writes fail.
- Capacity, error rate, or stall thresholds are crossed.

## Required evidence
- Approved immutable plan.
- Batch manifest.
- Precondition revalidation record.
- Hash verification results.
- Journal and checkpoint entries.
- Operator approval record.
