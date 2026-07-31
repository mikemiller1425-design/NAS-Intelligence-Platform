# Dry-Run Playbook

## Purpose
Validate classification, destination planning, collision detection, and evidence capture without mutating any live NAS path. Dry run is the default operating mode until a later authorization explicitly promotes a bounded phase.

## Operating rules
- Read-only inventory only.
- No live NAS writes, renames, deletes, or moves.
- No overwrite of protected vaults.
- No deletion of source data.
- Any source-retirement idea remains a proposal until hash verification and approval exist.

## Preconditions
- Source roots are confirmed.
- Read-only credentials are available.
- Control-data storage is outside recursively scanned source roots.
- Rule set version is frozen for the run.
- Snapshot and recovery posture are recorded, even though dry run does not depend on them for safety.

## Steps
1. Discover inventory scope and exclude out-of-scope paths.
2. Scan files and directories without mutation.
3. Capture hashes, metadata, and rule matches.
4. Produce proposed destinations and collision notes.
5. Route low-confidence, conflicting, sensitive, or unresolved items to review.
6. Emit a signed or hashed dry-run plan artifact.
7. Archive evidence and stop.

## Stop conditions
- Any path escapes an approved root.
- A rule produces conflicting destinations without a precedence rule.
- A source item lacks required evidence.
- The inventory cannot be repeated deterministically.
- A secret, private path, or unapproved live action appears in outputs.

## Required evidence
- Inventory manifest.
- Dry-run plan.
- Rule coverage report.
- Conflict report.
- Unresolved queue.
- Evidence index with hashes for generated artifacts.
