# Pipeline Architecture

## Pipeline Principle
The pipeline is a gated progression from discovery to proposal to approved execution. It must remain dry-run by default and never skip the inventory or review stages.

## Stages
1. Read-only discovery and inventory.
2. Metadata extraction and normalization.
3. Cryptographic hashing and duplicate detection.
4. Rule-driven classification and explanation.
5. Destination and operation planning.
6. Human review and approval.
7. Approved copy execution.
8. Verification and reconciliation.
9. Optional retirement after confirmed safety checks.
10. Ongoing monitoring and maintenance.

## Control Points
- Dry-run is the default output mode for every pipeline stage.
- A classification result is only a proposal, not an execution order.
- Destructive actions require explicit approval and an auditable trail.
- Protected-vault overwrite is prohibited unless a future governance decision explicitly changes that rule.

## Duplicate Handling
Exact duplicates are identified by cryptographic hash comparison. Near-duplicates or ambiguous cases do not receive automatic destructive handling and must be surfaced for review.

## Migration Posture
The pipeline supports pilot-before-live behavior. A pilot can validate assumptions on a narrow scope, but full migration must not begin until the pilot proves the controls, evidence, and rollback path.
