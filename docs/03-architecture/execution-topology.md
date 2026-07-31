# Execution Topology

## Topology Overview
The execution topology is designed around one primary worker, one sentinel device, and one protected storage system. The Mac mini performs the heavy lifting. The Raspberry Pi watches and alerts. The Synology stores the data and remains the protected storage authority.

## Node Responsibilities

### Mac mini
- Runs inventory collection.
- Computes cryptographic hashes.
- Evaluates classification and planning rules.
- Produces dry-run and approved execution plans.
- Coordinates copy, verification, and retirement workflows.

### Raspberry Pi Sentinel
- Monitors job and system health.
- Emits alerts for stuck runs, failed checks, and policy violations.
- Never performs or authorizes destructive work.
- Never becomes the primary worker.

### Synology
- Hosts the file corpus.
- Serves as the protected storage layer.
- Receives approved copies and verified archive placements.
- Remains outside any frontend authorization path.

## Flow Pattern
1. Discover and inventory from Synology.
2. Analyze files on the Mac mini.
3. Propose operations in dry-run mode.
4. Present evidence and reasoning in the review console.
5. Execute only after explicit approval.
6. Verify copies and record immutable audit evidence.

## Boundary Rules
- The frontend can request review and display evidence, but it does not authorize mutation.
- The Pi may warn, not decide.
- The Mac mini may execute, but only through policy checks and approval gates.
- Any destructive action must remain human-approved and logged.
