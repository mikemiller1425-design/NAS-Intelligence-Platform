# Interface Model

## Purpose

The interface model defines how operators and automation interact with the platform. V1 is CLI and report first; a graphical operator console may be added later if it does not weaken the source-of-truth boundary.

## Interface principles

1. Reports are evidence, not authority.
2. The dashboard never authorizes work independently.
3. CLI and report outputs must be sufficient to operate the system without a GUI.
4. Interfaces must never expose credentials.
5. Readable explanations matter more than decorative presentation.

## Interface surfaces

### CLI

The CLI is the primary operator surface in V1.

Responsibilities:

- start inventory or dry-run work
- inspect manifests and reports
- review conflicts and unresolved items
- approve or reject gated actions
- query progress and checkpoints
- request reconciliation summaries

### Reports

Reports are canonical readouts of system state.

Required report classes:

- inventory summary
- rule coverage
- conflict summary
- unresolved queue
- exact duplicate groups
- collision report
- dry-run plan
- pilot verification
- batch progress
- failure report
- reconciliation report
- rollback readiness
- final completion certificate

### Operator console (non-executing decision surface)

A later console may visualize the same records that the CLI and reports already produce. It is a **non-executing decision surface**: read-only toward underlying file data, write-capable only for a bounded set of application-state commands. `docs/03-architecture/review-console-architecture.md` is the authoritative list of those commands.

The console may:

- filter and browse records
- display charts and status summaries
- present review queues
- show batch and checkpoint progress
- capture operator decision and approval **intent**

The console may not:

- become the sole source of truth
- authorize mutation by animation
- hide immutable records behind mutable UI state
- construct, sign, or self-validate an approval record — the backend mints and binds every approval
- submit any command that copies, moves, renames, quarantines, retires, overwrites, or deletes file data

## Required views

### Inventory view

Shows:

- source root coverage
- file counts and byte totals
- unreadable or skipped items
- metadata completeness
- hash coverage
- inventory checkpoints

### Rule coverage view

Shows:

- active rule sets
- enabled and disabled rules
- rule matches
- unmatched items
- provisional rule usage

### Conflict view

Shows:

- destination collisions
- rule conflicts
- sensitive identity conflicts
- exact and near duplicate conflicts
- unresolved sources

### Dry-run plan view

Shows:

- immutable plan id and version
- source and destination roots
- entry counts
- collision handling
- review-required entries

### Pilot verification view

Shows:

- pilot dataset
- copy and verification results
- rollback readiness
- observed exceptions

### Reconciliation view

Shows:

- source totals
- destination totals
- expected versus observed counts
- unresolved items
- exception ownership

## Interaction rules

1. Any write action from the CLI or console must be explicitly confirmed.
2. Read operations are free unless they expose sensitive data that the user has not requested.
3. All actions must surface their target object and expected effect.
4. A request to “approve” must show the full approved subject.
5. A request to “run” must explain whether it is a dry run, fixture run, or authorized execution.

## Sentinel interface

The Raspberry Pi sentinel interface is read-only and intentionally narrow.

Allowed:

- read health summaries
- read queue freshness
- send alerts
- issue safe predefined job requests

Forbidden:

- classification editing
- plan approval
- file mutation
- arbitrary command execution

## Synthetic path policy

Interfaces used for specification, testing, or fixtures should prefer synthetic paths such as:

- `/Volumes/NAS-Demo/Source/Incoming`
- `/Volumes/NAS-Demo/Control`
- `/Volumes/NAS-Demo/Pilot`
- `/Volumes/NAS-Demo/Organized`
- `/Volumes/NAS-Demo/Review`

These are documentation-only examples unless separately approved in a live environment.

## V1 limits

- No interface may imply live authorization merely by being visible.
- No hidden admin action may bypass approval.
- No real credentials should appear in interface examples or screenshots.

