# Rollback Playbook

## Purpose
Restore a safe state after a failed dry run, pilot, or live batch without compounding loss.

## Operating rules
- Rollback is designed before execution.
- Repeatable rollback must be idempotent.
- The journal is the primary recovery guide.
- Snapshot restore is a last resort, not the normal path.
- No rollback step may depend on guessing file intent.

## Preconditions
- Mutation scope is known.
- Journal and checkpoints are available or an alternate recovery source is documented.
- Operator has authorized rollback.
- Recovery target is confirmed.

## Steps
1. Freeze further mutation.
2. Reconcile actual filesystem state against the journal.
3. Restore or re-copy items to their approved prior state.
4. Verify hashes and counts after each recovery slice.
5. Confirm unresolved items remain preserved and visible.
6. Record the recovery outcome and any residual exceptions.

## Stop conditions
- Recovery would overwrite protected data without approval.
- A rollback action cannot be verified.
- Source or destination state is ambiguous.
- The only remaining recovery path is not approved.

## Required evidence
- Failure summary.
- Recovery scope.
- Rollback actions taken.
- Verification results.
- Residual risk statement.
