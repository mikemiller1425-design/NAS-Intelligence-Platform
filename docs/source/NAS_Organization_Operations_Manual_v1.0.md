# NAS Organization Operations Manual

**Version:** 1.0-rc1  
**Status:** Blueprint baseline; live reorganization is not authorized  
**Primary outcome:** A fully inventoried, safely classified, deduplicated, organized, auditable, and maintainable Synology NAS.

## Executive operating decision

The NAS will be organized by a controlled system, not by an improvised bulk-move script.

- **Synology NAS:** protected source storage, snapshots, version history, shared folders, and final organized library.
- **Mac mini:** primary NAS Intelligence Engine for scanning, hashing, metadata extraction, classification, reporting, and approved file operations.
- **Raspberry Pi:** NAS Operations Sentinel for health checks, queue watching, stall detection, lightweight scheduling, dashboarding, and phone alerts.
- **Human operator:** final authority for taxonomy, ambiguous classifications, destructive actions, and promotion from dry run to live execution.

The Raspberry Pi is not the primary classification or migration engine. It should not become the throughput bottleneck or the sole holder of operational state.

## 1. Mission and definition of success

The mission is to transform the Synology NAS from an accumulated collection of files into a dependable information system without losing originals, provenance, or reversibility.

Success means:

1. Every in-scope file is inventoried with a stable identity and source path.
2. Exact duplicates are identified with hashes; near-duplicates are reviewed separately.
3. Classification decisions are traceable to a rule, evidence, confidence score, and engine version.
4. Ambiguous or conflicting items go to review rather than being guessed into place.
5. No destructive action occurs implicitly.
6. Every approved move is journaled and reversible.
7. A small copied-data pilot proves the workflow before any live NAS mutation.
8. The final taxonomy is understandable to a human without the software.
9. New files can be ingested continuously without recreating disorder.
10. The system can demonstrate completeness with pre/post manifests, exception reports, and reconciliation totals.

## 2. Non-negotiable safety laws

### 2.1 Source preservation

- Inventory and analysis are read-only by default.
- Never alter file contents during classification.
- Never operate first against the only copy of important data.
- Confirm Synology snapshot or equivalent recovery coverage before live moves.
- Prefer copy-and-verify during pilot and early production; delete source copies only through a separately approved cleanup phase.

### 2.2 No silent destruction

- No automatic permanent deletion in V1.
- Exact duplicates may be proposed for quarantine, never silently removed.
- Near-duplicates are not duplicates and require explicit review.
- Conflicting filenames never overwrite an existing destination.
- Unsupported, unreadable, encrypted, or corrupted files remain preserved and are reported.

### 2.3 Evidence before mutation

Every proposed operation must record:

- file identity and cryptographic hash;
- source and proposed destination;
- matched rule and rule version;
- classification evidence and confidence;
- conflict, duplicate, and risk status;
- planned operation;
- approval status;
- execution and verification result.

### 2.4 Small blast radius

Progression is gated:

`fixtures → copied pilot → limited live pilot → staged batches → full operation`

Failure at any gate pauses expansion.

### 2.5 Separation of concerns

- Classification recommends where an item belongs.
- The planner converts approved recommendations into an operation plan.
- The executor performs only approved plan entries.
- The verifier independently checks outcomes.
- The UI or dashboard never authorizes an operation merely by animating it.

## 3. Scope

### In scope for V1

- Read-only discovery of selected Synology shares.
- File and directory inventory.
- Size, timestamp, extension, MIME, and available media metadata extraction.
- Stable hashing and exact-duplicate grouping.
- Configurable rule-based classification.
- Optional AI-assisted media/document suggestions with confidence thresholds.
- Destination preview and conflict detection.
- Dry-run plans with no filesystem mutation.
- Manual review queue.
- Copied-data pilot.
- Approved copy/move batches with verification.
- Append-only operation journal and rollback plan.
- Pre/post reconciliation reports.
- Continuous ingestion design.
- Raspberry Pi monitoring and Pushover alerts.

### Explicitly out of scope until separately approved

- Permanent deletion.
- Automated near-duplicate deletion.
- Unreviewed face identification.
- Broad live reorganization from the first run.
- Destructive renaming based only on an AI guess.
- Modification of photo/video payloads.
- Autonomous cloud uploads or third-party publishing.
- Credentials stored in Git.
- Direct filesystem mutation from the Raspberry Pi sentinel.
- Training models on private media without an explicit privacy decision.

## 4. System architecture

```text
Synology shares (source + snapshots)
            │ read-only discovery
            ▼
Mac mini: NAS Intelligence Engine
  inventory → metadata → hashes → rules/AI suggestions
            │
            ├── inventory database and manifests
            ├── proposed operation plans
            ├── review queue and reports
            └── approved executor → verification → journal
            │
            ▼
Synology organized destinations + quarantine/review zones

Raspberry Pi: NAS Operations Sentinel
  mount checks · heartbeats · log freshness · space · alerts · status page
            │
            └── observes and requests; does not classify or mutate originals
```

### 4.1 Synology responsibilities

- Host source and destination shares.
- Provide snapshots, recycle-bin/versioning features where available, and access controls.
- Preserve authoritative file bytes.
- Expose capacity, health, and share availability.

### 4.2 Mac mini responsibilities

- Run the inventory, hashing, metadata, classification, planning, execution, and verification workers.
- Maintain the authoritative operational database and append-only logs.
- Generate human-readable reports.
- Execute only scoped, approved batches.
- Resume safely from checkpoints.

### 4.3 Raspberry Pi responsibilities

- Confirm required shares are mounted and reachable.
- Check worker heartbeat and log freshness.
- Detect stalled queues and low free space.
- Send alerts for completion, failure, blocked review, and capacity risk.
- Optionally expose a read-only local status page.
- Trigger a predefined safe job request, but never invent paths or execute unrestricted shell commands.

## 5. Canonical data zones

Exact share names should be confirmed during blueprinting. The logical zones are mandatory even if physical paths differ.

1. **Source zones:** existing content under analysis; read-only during inventory.
2. **Migration control:** manifests, databases, reports, plans, logs, and checkpoints.
3. **Incoming:** new content awaiting intake.
4. **Organized library:** approved destinations by durable human taxonomy.
5. **Manual review:** ambiguous, conflicting, unsupported, or low-confidence items.
6. **Quarantine:** suspected duplicates, corruption, unsafe names, or policy exceptions; preserved, not deleted.
7. **Pilot:** copied test corpus isolated from originals.
8. **Archive:** completed manifests, decisions, and batch evidence.

Suggested control structure:

```text
00_MIGRATION_CONTROL/
├── 01_Inventory/
├── 02_Manifests/
├── 03_Plans/
├── 04_Reports/
├── 05_Unresolved/
├── 06_Quarantine/
├── 07_Journals/
└── 08_Checkpoints/
```

This is a logical recommendation, not authorization to create or move live folders before path review.

## 6. Inventory model

Every discovered filesystem object receives a record. Minimum fields:

- `file_id`: stable internal UUID.
- `source_root` and `relative_path`.
- `filename`, extension, MIME, and normalized type.
- byte size.
- created, modified, and discovered timestamps when available.
- cryptographic content hash and hashing status.
- inode/file identifier when useful, without treating it as portable identity.
- owner/permissions when readable.
- media metadata: dimensions, duration, codecs, capture time, camera/drone identifiers, GPS presence.
- document metadata: page count, author/title fields, text-extraction status.
- structured-data metadata: delimiter, encoding, headers, row count sample.
- error and retry status.
- classification, confidence, matched rules, and review state.
- planned and executed operation references.

Inventory must be resumable. A restart must not require trusting partially written output; checkpoints and atomic writes are required.

## 7. Classification policy

### 7.1 Rules are configuration, not buried code

Rules belong in a versioned configuration file with:

- stable rule ID;
- priority;
- enabled state;
- scope;
- conditions;
- destination template;
- minimum confidence;
- required evidence;
- conflict behavior;
- risk level;
- test cases;
- owner and rationale.

Example shape:

```yaml
rules:
  - id: media-dog
    priority: 100
    status: provisional
    conditions:
      media_type: [image, video]
      detected_objects_any: [dog]
    destination: "Family_Vault/Dogs/{capture_year}"
    minimum_confidence: 0.90
    on_conflict: manual_review

  - id: media-drone
    priority: 95
    status: provisional
    conditions:
      source_or_metadata_any: [known_drone_camera, drone_folder, drone_filename_pattern]
    destination: "Media/Drone/{capture_year}/{capture_date}"
    minimum_confidence: 0.95
    on_conflict: manual_review

  - id: data-csv
    priority: 80
    status: provisional
    conditions:
      extensions: [.csv]
    destination: "Data/Structured/CSV/{capture_year}"
    follow_up: profile_structured_data

  - id: media-single-female-voss-candidate
    priority: 50
    status: provisional_sensitive
    conditions:
      person_count: 1
      operator_confirmed_identity: Voss
    destination: "Family_Vault/Voss/{capture_year}"
    minimum_confidence: 0.98
    requires_human_confirmation: true

  - id: unresolved
    priority: 0
    status: active
    destination: "00_MIGRATION_CONTROL/05_Unresolved/Needs-Manual-Review"
```

The Dogs, Voss, drone, and CSV examples reflect prior intent but remain **provisional** until the operator confirms source signals, destination paths, privacy boundaries, and representative test cases.

### 7.2 Rule evaluation order

1. Safety exclusions and unreadable/corrupt conditions.
2. Exact duplicate status.
3. High-certainty source/device metadata.
4. Explicit folder or filename rules.
5. Deterministic file-type rules.
6. Content-derived or AI-assisted classifications.
7. Sensitive identity rules requiring confirmation.
8. Fallback to manual review.

### 7.3 Conflict behavior

- Multiple matching destinations are a conflict unless an explicit precedence rule resolves them.
- Low confidence never becomes a live move.
- Existing destination names generate a collision plan: skip, version, content-compare, or operator decision.
- A rule change never silently rewrites prior decisions; it creates a new rule version and re-evaluation proposal.

## 8. Duplicate policy

### Exact duplicates

Files with matching cryptographic hashes are exact-byte duplicate candidates. The engine may group them and recommend a canonical copy based on approved policy, but it does not delete extras in V1.

### Near duplicates

Similar photos, transcoded videos, resized images, edited documents, and files with matching names are not exact duplicates. They require separate similarity analysis and review.

### Quarantine workflow

1. Identify the group.
2. Preserve every original path in the manifest.
3. Recommend canonical and redundant candidates.
4. Copy or move approved redundant candidates to quarantine only after a dedicated approval.
5. Verify hashes and counts.
6. Retain the quarantine for a defined cooling-off period.
7. Permanent cleanup is a future separately authorized operation.

## 9. Workflow gates

### Gate 0 — Readiness

- Confirm in-scope shares and excluded paths.
- Confirm backups/snapshots and recovery procedure.
- Confirm service account and least-privilege access.
- Confirm control-data location is not inside a recursively scanned source.
- Confirm sufficient destination and temporary capacity.
- Freeze Classification Rules v1 for the test cycle.

### Gate 1 — Read-only inventory

- Crawl without changing files.
- Produce counts, total bytes, extension/MIME distributions, unreadable paths, path-length risks, and suspected duplicates.
- Re-run a sample to demonstrate deterministic identity and no source mutation.

### Gate 2 — Dry run

- Evaluate all active rules.
- Produce proposed destinations and explanations.
- Detect collisions, conflicts, low-confidence items, and risky operations.
- Generate a signed/hashed plan artifact; do not move anything.

### Gate 3 — Fixture tests

- Use synthetic and representative copied files.
- Test every rule with positive, negative, boundary, conflict, and idempotency cases.
- Confirm unsupported and ambiguous items land in review.

### Gate 4 — Copied pilot

- Select a small, diverse, non-critical sample.
- Copy it into the isolated pilot zone.
- Run the complete workflow.
- Review destinations and reports manually.
- Demonstrate rollback without touching originals.

### Gate 5 — Limited live pilot

- Use one bounded folder or small batch.
- Prefer copy-and-verify.
- Require operator approval of the exact operation plan.
- Compare source counts/hashes and destination counts/hashes.
- Stop on unexpected errors, capacity thresholds, or conflict-rate limits.

### Gate 6 — Staged production

- Expand in fixed-size batches.
- Checkpoint between batches.
- Preserve batch-specific evidence.
- Never allow a failed batch to trigger automatic expansion.

### Gate 7 — Reconciliation and steady state

- Prove every source item is organized, intentionally retained, quarantined, or unresolved.
- Produce exception inventory.
- Activate monitored incoming-file ingestion.
- Preserve final baseline manifests and operational documentation.

## 10. Operation planning and execution

Every filesystem change must originate from an immutable plan record containing:

- plan and batch IDs;
- source and destination roots;
- precondition hash and size;
- operation type: copy, move, rename, quarantine, or skip;
- collision policy;
- approval identity and time;
- expected postconditions;
- rollback action;
- maximum batch size and stop thresholds.

Execution rules:

1. Revalidate source preconditions immediately before action.
2. Create required destination directories safely.
3. Copy to a temporary destination name when needed.
4. Verify bytes with cryptographic hash.
5. Atomically finalize the destination where supported.
6. For moves, remove the source only after destination verification and only when the approved phase permits it.
7. Append the outcome to the journal.
8. Emit progress and exception events.
9. Stop the batch when a safety threshold is exceeded.

## 11. Rollback and recovery

Rollback is designed before execution, not after failure.

- Every successful mutation has an inverse record.
- The journal is append-only and stored separately from the data being moved.
- Recovery is idempotent: repeating it does not compound changes.
- Partial operations are identifiable by temporary names and incomplete journal state.
- A restart reconciles filesystem reality against the journal before continuing.
- Snapshot restoration is the last-resort safety net, not the normal rollback mechanism.

## 12. Monitoring and Raspberry Pi sentinel

### Required health signals

- NAS reachability and mount status.
- Free capacity and configured warning/critical thresholds.
- Mac mini worker heartbeat.
- Current phase, batch, and last successful checkpoint.
- Log and journal freshness.
- Queue length and oldest waiting item.
- Error/retry counts.
- Manual-review backlog.
- Estimated completion only when based on measured throughput.

### Alerts

Send phone notifications for:

- batch completed;
- operator approval required;
- worker stalled;
- NAS share disconnected;
- free-space warning/critical state;
- repeated processing failure;
- reconciliation mismatch;
- pilot or production gate ready for review.

Notifications contain project, phase, batch ID, severity, short reason, and the safest next action. They never contain credentials or sensitive filenames unnecessarily.

### Sentinel authority

The Pi may restart a predefined non-destructive monitoring service or submit a known job request. It may not choose destinations, approve moves, delete files, or execute arbitrary commands received from a dashboard.

## 13. Security and privacy

- Use a dedicated NAS service account with only required share access.
- Separate read-only discovery credentials from mutation-capable execution where practical.
- Store secrets outside Git and outside logs.
- Treat filenames, paths, media metadata, thumbnails, and extracted text as sensitive.
- Prefer local processing for private media.
- Sanitize all external AI/tool output before using it as a path or shell argument.
- Never interpolate untrusted filenames into shell commands.
- Normalize and validate destination paths; prohibit traversal outside approved roots.
- Maintain a complete audit trail for approvals and mutations.
- Sensitive identity classification requires explicit policy and human confirmation.

## 14. Reports and operator interface

V1 must remain operable from reports/CLI even before a dashboard exists. Required outputs:

- inventory summary;
- classification coverage and confidence distribution;
- rule-match report;
- conflicts and unresolved items;
- exact-duplicate groups;
- collision report;
- dry-run operation plan;
- pilot verification report;
- batch progress and failure report;
- pre/post reconciliation;
- rollback readiness report;
- final completion certificate with exceptions.

A later dashboard may display these records, but it must not become the sole source of truth.

## 15. Acceptance criteria

### Inventory

- All in-scope roots are represented in the manifest.
- Repeated scans do not create duplicate file identities.
- Unreadable items are reported, not skipped silently.
- Inventory does not modify source content or timestamps intentionally.

### Classification

- Every active rule has automated positive and negative tests.
- Each recommendation identifies its matched rule and evidence.
- Conflicting or low-confidence classifications enter review.
- Sensitive identity rules never auto-execute without approved policy.

### Execution

- No live operation occurs without an approved immutable plan.
- Destination content is hash-verified.
- Name collisions never overwrite silently.
- Re-running a completed batch does not duplicate output.
- The operation journal can reconstruct what happened.

### Safety and recovery

- A copied pilot is completed before live mutation.
- A rollback drill succeeds on pilot data.
- Snapshot/recovery readiness is documented.
- Permanent deletion remains disabled.

### Completion

- Source and destination totals reconcile.
- Every source item has a final disposition.
- Exceptions are enumerated and owned.
- Continuous incoming-file behavior is defined and monitored.
- Final taxonomy and operating instructions are understandable without chat history.

## 16. Stop conditions

Pause the current batch immediately when any of these occur:

- snapshot/recovery protection is unavailable;
- source or destination mount changes unexpectedly;
- destination free space crosses the critical threshold;
- hash verification fails;
- the operation plan no longer matches source preconditions;
- collision or error rate exceeds the approved limit;
- journal writes fail;
- path validation detects an escape from approved roots;
- the worker loses authoritative state;
- the operator issues pause or emergency stop.

## 17. Required repository blueprint

The NAS project repository should contain:

```text
NAS-Intelligence-Platform/
├── README.md
├── PROJECT_STATUS.md
├── FOUNDATION_VERSION.md
├── CHANGELOG.md
├── docs/
│   ├── source/
│   ├── 00-intent/
│   ├── 01-policy/
│   ├── 02-specification/
│   ├── 03-architecture/
│   ├── 04-acceptance/
│   ├── 05-governance/
│   ├── audits/
│   ├── handoffs/
│   └── future-registry/
├── config/
│   ├── classification-rules.example.yaml
│   ├── paths.example.yaml
│   └── thresholds.example.yaml
├── fixtures/
├── apps/
├── packages/
├── scripts/
├── tests/
└── archive/
```

Blueprinting must not create live NAS credentials or execute against mounted shares.

## 18. Decisions required before implementation

1. Exact Synology share roots in and out of scope.
2. Existing destination taxonomy versus proposed taxonomy.
3. Confirmation of Dogs, Voss, drone, CSV, and other handwritten rules.
4. Whether identity recognition is allowed and under what privacy controls.
5. Hash algorithm and performance strategy.
6. Database location and backup policy.
7. Snapshot/versioning readiness.
8. Pilot dataset selection.
9. Batch-size and stop thresholds.
10. Copy-first versus move behavior for each rollout phase.
11. Quarantine retention and future deletion policy.
12. Whether the Mac mini may hold temporary thumbnails or extracted text.

## 19. Definition of ready

Implementation may begin only after:

- this manual and the operator’s handwritten rules are in the repository;
- Cursor has produced the full blueprint and a traceability matrix;
- an independent audit resolves all blockers and meaningful major findings;
- Foundation 1.0 is approved;
- the Build Ladder exists;
- FBL-001 is explicitly authorized.

Live NAS execution has a separate readiness gate and is not authorized merely because software implementation is complete.

## 20. Operating principle

The finish line is not “files moved.” The finish line is a NAS whose contents are accounted for, safely organized, recoverable, explainable, and maintainable—and a system that prevents disorder from returning.

