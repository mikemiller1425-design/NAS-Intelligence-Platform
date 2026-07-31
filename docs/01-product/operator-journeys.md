# Operator Journeys

These journeys describe how the human operator experiences the platform from blueprint through steady state.

## Journey 1: Readiness and audit preparation

The operator starts by confirming the source material, repository structure, and safety posture.

What the operator expects:

- the manual and prompt are present under `docs/source/`;
- the blueprint documents explain the mission, principles, scope, and roles;
- implementation is still blocked pending independent audit;
- no live NAS action is authorized.

Outcome:

- the repository is ready for audit rather than execution.

## Journey 2: Read-only inventory

The operator reviews a dry, read-only discovery cycle.

What happens:

- selected shares are inventoried without mutation;
- file identities, hashes, and metadata are collected;
- unreadable or risky items are reported, not hidden;
- repeated scans confirm determinism.

Outcome:

- the operator receives a trustworthy baseline inventory and exception list.

## Journey 3: Dry-run classification

The operator reviews proposed classifications before any filesystem change.

What happens:

- rules evaluate files and propose destinations;
- conflicts, low-confidence cases, and sensitive items are routed to review;
- destination collisions are detected in advance;
- no file is moved.

Outcome:

- the operator can inspect the rule behavior without risk to the NAS.

## Journey 4: Fixture testing

The operator or reviewer validates the rules against synthetic or representative files.

What happens:

- the platform runs on copied fixtures, not live originals;
- positive, negative, boundary, conflict, and idempotency cases are tested;
- unsupported cases are expected to land in review.

Outcome:

- the operator sees whether the rules behave as intended before a pilot.

## Journey 5: Copied pilot

The operator approves a small copied corpus for a controlled end-to-end trial.

What happens:

- a small sample is copied into an isolated pilot zone;
- the full workflow runs on the copied data;
- rollback is demonstrated against pilot data;
- the original source remains untouched.

Outcome:

- the operator gets proof that the workflow works on representative data.

## Journey 6: Limited live pilot

The operator authorizes a bounded real-world batch.

What happens:

- a small live batch is approved through an immutable plan;
- the executor revalidates preconditions before action;
- hash verification confirms the outcome;
- any error or threshold breach stops the batch.

Outcome:

- live mutation is proven on a narrow slice, not the whole library.

## Journey 7: Staged production

The operator expands rollout in fixed batches.

What happens:

- batches are checkpointed and individually evidenced;
- progress is reviewed between batches;
- the system never auto-expands after a failure.

Outcome:

- the operator controls pace and can stop expansion at any point.

## Journey 8: Reconciliation and steady state

The operator reviews the final accounting and then ongoing intake behavior.

What happens:

- source and destination totals are reconciled;
- unresolved and exception items are enumerated;
- final baseline manifests are preserved;
- new files enter through monitored continuous ingestion.

Outcome:

- the NAS stays organized instead of drifting back into chaos.

## Friction points the journeys must surface

- ambiguous classification;
- sensitive identity questions;
- collisions between source and destination names;
- missing snapshots or recovery coverage;
- capacity pressure;
- worker stalls or stale logs;
- gaps in proof that a batch completed safely.

## Operator expectations

- The operator should never have to infer what the system did.
- Every journey should produce evidence, not just a status light.
- If the system cannot explain itself, it is not ready to advance.
