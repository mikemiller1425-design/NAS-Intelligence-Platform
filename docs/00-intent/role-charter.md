# Role Charter

This charter defines who may do what in the NAS Intelligence Platform. Authorization and execution are intentionally separated.

## Shared rule

No role except the human operator can authorize a live mutating action. Technical roles can recommend, prepare, execute, or verify only within the bounds of approved policy and immutable plans.

## Human operator

**Authority**

- Final authority over taxonomy, policy, ambiguity, destructive actions, rollout gates, and live execution approval.

**Execution rights**

- Approve or reject proposed plans.
- Decide how provisional rules should be finalized.
- Decide when a pilot may advance to the next gate.
- Decide how unresolved or sensitive items are handled.

**Limits**

- Does not need to write system internals to exercise authority.
- Should not be bypassed by automation, dashboards, or sentinel alerts.

## Mac mini primary worker

**Authority**

- No approval authority for live mutation.

**Execution rights**

- Run read-only inventory.
- Extract metadata and hashes.
- Evaluate rules and prepare proposed classifications.
- Build plans, journals, reports, and verification artifacts.
- Execute only approved plan entries.

**Limits**

- May not invent policy.
- May not self-authorize mutations.
- May not treat AI output as truth without validation.

## Synology storage authority

**Authority**

- Serves as the protected source and destination storage platform.

**Execution rights**

- Host source shares, destination shares, snapshots, versioning, and recovery features.
- Preserve authoritative file bytes.

**Limits**

- Does not decide taxonomy or policy.
- Does not authorize moves by itself.

## Raspberry Pi Sentinel

**Authority**

- No authority to approve, classify, move, rename, or delete files.

**Execution rights**

- Observe mount status, worker heartbeat, log freshness, free space, queue length, and other health signals.
- Send alerts.
- Optionally restart a predefined non-destructive monitoring service or submit a known safe job request.

**Limits**

- Must not choose destinations.
- Must not issue arbitrary shell commands.
- Must not mutate source or destination data.
- Must not become the primary engine for classification or migration.

## Planner

The planner is a logical role, usually performed by the Mac mini worker.

**Authority**

- No final approval authority.

**Execution rights**

- Convert approved or reviewable recommendations into an immutable operation plan.
- Encode stop thresholds, rollback requirements, and verification expectations.

**Limits**

- May not change a plan after approval.
- May not silently resolve conflicts.

## Classifier

The classifier is a logical role, usually performed by the Mac mini worker.

**Authority**

- No approval authority.

**Execution rights**

- Apply rules, metadata, and optional AI hints to propose destinations or review items.

**Limits**

- Must route low-confidence or conflicting cases to review.
- Must not treat identity-sensitive inference as automatic truth.

## Executor

The executor is a logical role, usually performed by the Mac mini worker.

**Authority**

- No independent approval authority.

**Execution rights**

- Perform only approved plan entries.
- Revalidate source preconditions immediately before action.
- Write journals and verification evidence.

**Limits**

- Must stop when hashes, mounts, paths, or thresholds fail validation.
- Must not expand scope on its own.

## Verifier

The verifier is a logical role, usually performed independently from the executor.

**Authority**

- No approval authority for new actions.

**Execution rights**

- Compare the observed filesystem state to the approved plan and expected postconditions.
- Confirm hashes, counts, and destinations.

**Limits**

- May not repair mismatches by guessing.
- May only report and trigger recovery or rollback paths that are already defined.

## Reviewer

The reviewer is the human or human-backed review process that resolves review items.

**Authority**

- May recommend disposition of ambiguous, sensitive, or conflicting cases.

**Execution rights**

- Accept, reject, or reroute items in the review queue.

**Limits**

- Cannot bypass the approval gate for live mutation.

## Auditor

The auditor is an independent reviewer of the blueprint and its implementation readiness.

**Authority**

- No operational authority over NAS data.

**Execution rights**

- Read documents, inspect contradictions, and produce findings.

**Limits**

- Must not modify active specifications or live data.

## Separation summary

- Authorization belongs to the human operator.
- Preparation belongs to the planner and classifier.
- Mutation belongs to the executor only after approval.
- Verification belongs to the verifier and must be independent.
- Observation belongs to the sentinel and never crosses into control.
