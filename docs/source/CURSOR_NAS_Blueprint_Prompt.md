# Cursor Prompt — NAS Intelligence Platform Blueprint

Paste this into Cursor after opening the empty `NAS-Intelligence-Platform` repository. Place `NAS_Organization_Operations_Manual_v1.0.md` and the operator’s handwritten rules under `docs/source/` first.

---

You are the Repository Blueprint Engineer for the NAS Intelligence Platform.

Work continuously until the repository is fully prepared for an independent foundation audit. Do not stop after creating folders. Do not begin production implementation. Do not connect to, scan, write to, rename, move, or delete anything on the live Synology NAS.

## Mission

Translate the source material into a complete, internally consistent, implementation-ready blueprint for a system that inventories, classifies, deduplicates, organizes, verifies, and continuously maintains a Synology NAS without losing data or provenance.

The intended operating model is:

- Synology NAS: protected source storage, snapshots/versioning, shared folders, and final organized library.
- Mac mini: primary NAS Intelligence Engine for inventory, hashing, metadata extraction, classification, planning, approved execution, and verification.
- Raspberry Pi: NAS Operations Sentinel for monitoring, health checks, scheduling safe predefined requests, dashboarding, and phone alerts.
- Human operator: final authority over taxonomy, ambiguous classifications, destructive actions, rollout gates, and policy changes.

The goal is a fully organized NAS, but the path is gated:

`read-only inventory → dry run → fixture tests → copied pilot → limited live pilot → staged production → reconciliation → continuous ingestion`

## Source authority

Read every artifact under `docs/source/` before writing active documents.

Expected sources include:

- `NAS_Organization_Operations_Manual_v1.0.md`
- the operator’s handwritten or transcribed classification rules
- any existing folder maps, scripts, reports, or NAS notes

Treat source material as intent input, not automatically authoritative implementation. Reconcile contradictions. Do not silently discard a rule or invent a sensitive classification policy.

If exact NAS paths, taxonomy choices, identity-recognition policy, snapshot status, or other material decisions are absent, record them in `docs/05-governance/open-decisions.md`. Classify them as BLOCKER, MAJOR, or MINOR. Continue around non-blockers.

## Non-negotiable constraints

- No live NAS access or commands.
- No application implementation beyond minimal structural placeholders.
- No dependency installation or lockfiles.
- No credentials, tokens, IP addresses, usernames, or private paths committed.
- No permanent deletion in V1.
- No silent overwrite.
- No classification-driven live move without an approved immutable plan.
- No near-duplicate deletion as if similarity meant equality.
- No sensitive identity auto-classification without explicit operator policy.
- No Raspberry Pi authority to classify, move, approve, or delete files.
- Archived or source documents never override active approved specifications.

## Required repository shape

Create and populate:

```text
/
├── README.md
├── PROJECT_STATUS.md
├── FOUNDATION_VERSION.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .gitignore
├── .editorconfig
├── .gitattributes
├── docs/
│   ├── source/
│   ├── 00-intent/
│   │   ├── mission.md
│   │   ├── principles.md
│   │   ├── glossary.md
│   │   └── operating-model.md
│   ├── 01-policy/
│   │   ├── classification-policy.md
│   │   ├── taxonomy-policy.md
│   │   ├── duplicate-policy.md
│   │   ├── retention-and-quarantine.md
│   │   └── privacy-policy.md
│   ├── 02-specification/
│   │   ├── domain-model.md
│   │   ├── inventory-model.md
│   │   ├── rule-model.md
│   │   ├── workflow-model.md
│   │   ├── event-model.md
│   │   ├── operation-plan-model.md
│   │   ├── reporting-model.md
│   │   ├── monitoring-model.md
│   │   └── interface-model.md
│   ├── 03-architecture/
│   │   ├── system-architecture.md
│   │   ├── storage-and-database.md
│   │   ├── worker-architecture.md
│   │   ├── raspberry-pi-sentinel.md
│   │   ├── security-architecture.md
│   │   ├── testing-strategy.md
│   │   ├── deployment-and-recovery.md
│   │   └── adrs/
│   ├── 04-acceptance/
│   │   ├── foundation-acceptance.md
│   │   ├── inventory-acceptance.md
│   │   ├── classification-acceptance.md
│   │   ├── pilot-acceptance.md
│   │   ├── live-execution-acceptance.md
│   │   └── final-reconciliation.md
│   ├── 05-governance/
│   │   ├── authority-order.md
│   │   ├── open-decisions.md
│   │   ├── change-control.md
│   │   ├── approval-gates.md
│   │   ├── stop-conditions.md
│   │   └── evidence-standard.md
│   ├── migration/
│   │   ├── source-inventory.md
│   │   ├── source-reconciliation.md
│   │   └── traceability-matrix.md
│   ├── audits/
│   ├── handoffs/
│   │   ├── 001-foundation-audit.md
│   │   └── 002-build-ladder.md
│   └── future-registry/
│       └── registry.md
├── config/
│   ├── classification-rules.example.yaml
│   ├── paths.example.yaml
│   ├── thresholds.example.yaml
│   └── README.md
├── fixtures/
│   └── README.md
├── apps/
│   ├── operator-console/
│   └── sentinel/
├── packages/
│   ├── contracts/
│   ├── inventory/
│   ├── classification/
│   ├── planner/
│   ├── executor/
│   ├── verifier/
│   ├── reporting/
│   └── adapters/
├── prompts/
├── scripts/
├── tests/
└── archive/
```

Use README or `.gitkeep` placeholders for empty implementation boundaries. Do not add product logic.

## Root documents

### `README.md`

Explain the mission, operating model, safety posture, repository map, authority order, current status, and exact next step.

### `PROJECT_STATUS.md`

State:

- current phase: blueprint;
- Foundation status: `1.0-rc1`;
- implementation blocked pending independent audit;
- live NAS execution separately blocked;
- active blockers and decisions;
- next required action.

### `FOUNDATION_VERSION.md`

Use:

```text
NAS Intelligence Platform Foundation: 1.0-rc1
Status: Awaiting independent foundation audit
Implementation: Blocked pending audit resolution and approval
Live NAS execution: Prohibited pending build, fixture validation, copied pilot, and explicit operator authorization
```

## Required policy content

Create explicit policies for:

- rule priority, confidence, evidence, conflict, and fallback behavior;
- durable human-readable destination taxonomy;
- exact versus near duplicates;
- quarantine without deletion;
- sensitive media and identity classification;
- versioned rule changes;
- copy-first pilot behavior;
- retention and future cleanup authorization.

Represent the previously discussed Dogs, Voss, drone-media, CSV, and unresolved categories as provisional rules. Do not silently mark them approved. Require operator confirmation, especially for Voss identity handling.

## Required domain entities

Define only entities justified by V1, including at minimum:

- SourceRoot
- FileRecord
- Scan
- MetadataRecord
- HashRecord
- RuleSet and ClassificationRule
- ClassificationDecision
- DuplicateGroup
- ReviewItem
- TaxonomyNode
- OperationPlan and OperationEntry
- Approval
- Batch
- JournalEntry
- VerificationResult
- Checkpoint
- Alert
- SystemHealth
- ReconciliationReport

For each define fields, relationships, lifecycle, invariants, commands, events, and V1 limitations. Do not write SQL.

## Required invariants

- Inventory is read-only.
- A file’s bytes are never changed by classification.
- Every proposed destination is traceable to evidence and a rule version.
- Low-confidence or conflicting decisions enter manual review.
- A plan is immutable after approval; changes create a new version.
- Execution revalidates source hash/size/path preconditions.
- Destination collisions never overwrite silently.
- Successful copy/move requires post-operation hash verification.
- Permanent deletion is unavailable in V1.
- Repeated events and reruns are idempotent.
- Journal failure stops mutation.
- Paths cannot escape approved roots.
- The sentinel cannot authorize mutations.
- AI output is untrusted until validated.

## Workflow specification

Define states, transitions, evidence, approvals, failures, retries, and stop conditions for:

1. readiness;
2. read-only inventory;
3. dry-run classification;
4. fixture tests;
5. copied pilot;
6. limited live pilot;
7. staged production;
8. reconciliation;
9. continuous ingestion.

No phase may imply authorization for the next phase.

## Architecture decisions

Create ADRs for at least:

- Mac mini as primary engine;
- Raspberry Pi as sentinel, not primary worker;
- Synology as protected storage authority;
- configuration-driven versioned classification rules;
- local-first processing of private data;
- read-only inventory first;
- immutable operation plans;
- copy-and-verify pilot;
- append-only journals and checkpoints;
- exact duplicate hashing versus separate near-duplicate analysis;
- no permanent deletion in V1;
- adapter boundaries for NAS, notifications, metadata extractors, and optional AI classifiers;
- persistence choice recommendation, with alternatives and revisit conditions.

## Example configuration

Create safe example YAML files with fake mount paths and no secrets.

`classification-rules.example.yaml` must demonstrate:

- stable IDs;
- priority;
- status (`provisional`, `active`, `disabled`);
- deterministic and AI-assisted conditions;
- minimum confidence;
- destination templates;
- conflict behavior;
- human-confirmation requirements;
- test-case references;
- fallback to manual review.

`paths.example.yaml` must distinguish source, control, incoming, organized, review, quarantine, pilot, and archive roots.

`thresholds.example.yaml` must include placeholder thresholds for capacity, batch size, error rate, confidence, stall time, retries, and checkpoint cadence. Clearly require operator calibration.

## Testing and acceptance

Define unit, property, fixture, contract, integration, filesystem-sandbox, recovery, security, performance, and acceptance tests.

Acceptance must prove:

- source immutability during inventory/dry run;
- deterministic repeat scans;
- every rule has positive, negative, boundary, conflict, and idempotency tests;
- exact duplicates are hash-backed;
- low-confidence items are reviewed;
- plans cannot change after approval;
- collisions cannot overwrite;
- execution verifies hashes;
- rollback succeeds on pilot data;
- restart resumes or reconciles safely;
- duplicate events do not duplicate effects;
- totals reconcile;
- every source item has a final disposition;
- alerts fire for completion, attention, stall, disconnect, capacity, repeated failure, and mismatch.

## Monitoring model

Define the Raspberry Pi sentinel’s inputs, health checks, schedule, read-only dashboard, alerts, authentication, failure behavior, and strict authority limits.

It may observe, alert, and submit predefined safe job requests. It may not choose classifications, approve plans, mutate files, or execute arbitrary dashboard commands.

## Security model

Specify:

- dedicated least-privilege NAS accounts;
- read-only discovery versus mutation credentials;
- secret storage outside Git;
- path normalization and traversal prevention;
- safe handling of hostile filenames and metadata;
- no shell interpolation of untrusted paths;
- privacy rules for thumbnails, extracted text, GPS, and identity;
- audit logging;
- destructive-action confirmation;
- local-first processing;
- external AI outputs treated as untrusted;
- redaction of sensitive values in reports and alerts.

## Reports and interface

Specify CLI/report-first operability and a later operator console. Required views/reports include inventory, rule coverage, conflicts, unresolved, exact duplicates, collisions, dry-run plan, pilot verification, batch progress, failures, reconciliation, rollback readiness, and final completion.

The dashboard is never the source of truth and cannot animate or authorize work independently.

## Migration and traceability

Inventory every source file. Create a reconciliation record classifying major concepts as ADOPT, REFINE, MERGE, FUTURE, REJECT, or UNRESOLVED. Map all significant manual/rule concepts into active documents. Nothing important may disappear silently.

## Foundation audit handoff

Create `docs/handoffs/001-foundation-audit.md` instructing an independent reviewer to:

- read all active documents and source reconciliation;
- write no application code;
- inspect contradictions, missing terms, unsafe assumptions, impossible workflows, untestable acceptance requirements, inadequate recovery, privacy gaps, Raspberry Pi authority creep, and premature live-execution authorization;
- classify findings as BLOCKER, MAJOR, MINOR, or NOTE;
- write `docs/audits/foundation-v1-audit.md`;
- modify no active specification;
- stop after the report.

## Build Ladder handoff

Create `docs/handoffs/002-build-ladder.md`, blocked pending approved Foundation 1.0. It must require stable rung IDs and separate rungs for:

- foundation resolution/freeze;
- repository/tooling foundation;
- contracts/domain core;
- filesystem sandbox and fixtures;
- inventory engine;
- hashing/exact duplicates;
- metadata extractors;
- rule engine;
- dry-run planner;
- reports/review queue;
- immutable approvals;
- copy-and-verify executor;
- verifier/journal/checkpoints;
- rollback drill;
- copied pilot;
- limited live pilot readiness;
- Raspberry Pi sentinel;
- alerts;
- operator console, if justified;
- staged rollout;
- reconciliation;
- continuous ingestion;
- final acceptance.

Every rung must state objective, prerequisites, authoritative docs, allowed work, prohibited work, deliverables, tests, operator validation, evidence, rollback/failure conditions, and hard stop. Generating the ladder must not authorize implementation or live NAS use.

## Reusable prompts

Create repository prompts for:

- foundation audit;
- audit resolution;
- Foundation approval;
- Build Ladder generation;
- one-rung implementation;
- independent rung inspection;
- classification-rule review;
- dry-run review;
- pilot authorization;
- live-batch authorization;
- recovery/rollback;
- final reconciliation.

Each prompt defines role, inputs, authority, prohibitions, required evidence, output, and stopping condition.

## Future Registry

Preserve but do not activate:

- near-duplicate visual clustering;
- advanced face/identity recognition;
- semantic search and knowledge extraction;
- richer AI media understanding;
- Foundry/Agent City integration;
- remote mobile approvals;
- distributed workers;
- automated lifecycle policies;
- predictive capacity planning;
- cloud archive integration;
- broader household/business data governance.

Each entry must include rationale for exclusion and promotion conditions.

## Continuous self-review

Before stopping:

1. Verify every required file exists.
2. Check internal paths and links.
3. Search for contradictory terms and phase names.
4. Search for TODO, TBD, FIXME, filler, or unowned placeholders.
5. Search for secrets and real private paths.
6. Verify every source concept has traceability.
7. Verify provisional rules are not presented as approved.
8. Verify V1 never permits permanent deletion.
9. Verify no live NAS action is authorized.
10. Verify acceptance maps to specifications and architecture.
11. Verify the Pi remains a sentinel.
12. Verify source immutability, idempotency, journaling, and recovery are testable.
13. Correct all non-blocking defects.
14. Run available Markdown/link/format checks.
15. Show the repository tree and Git status.
16. Commit the blueprint if Git identity is configured and the worktree is safe. Do not push unless explicitly authorized.

## Final report

When the entire blueprint is complete, report:

1. repository status and commit;
2. files created/modified;
3. interpretation of the NAS mission;
4. proposed architecture;
5. V1 boundaries;
6. provisional rules and decisions requiring operator confirmation;
7. BLOCKER/MAJOR/MINOR open decisions;
8. checks performed and anything not verified;
9. exact next action: run `docs/handoffs/001-foundation-audit.md`.

Stop. Do not implement the engine and do not touch the live NAS.

Begin now by inspecting `docs/source/`, inventorying the source material, and creating an internal work plan. Continue until the blueprint is complete and ready for independent review.

