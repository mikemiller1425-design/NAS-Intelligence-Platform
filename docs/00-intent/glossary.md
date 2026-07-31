# Glossary

Canonical terms for the NAS Intelligence Platform. Prefer these definitions in specifications, plans, and reports.

## Core platform terms

- **NAS Intelligence Platform**: safety-first file intelligence, migration, classification, organization, validation, and maintenance system for Synology NAS content.
- **Synology**: protected storage authority hosting source data, snapshots/versioning, shares, and the final organized library.
- **Mac mini worker**: primary analysis and orchestration worker for scanning, hashing, metadata, classification, planning, approved execution, and verification.
- **Sentinel**: Raspberry Pi (or equivalent) monitoring component for heartbeats, mounts, space, stalled runs, and alerts; never authorizes destructive work.
- **Human Operator**: final authority for taxonomy, ambiguity, destructive actions, rollout gates, and policy.
- **Blueprint**: documentation/design layer before production implementation.
- **Foundation audit**: independent review required before implementation authorization.

## Sources and destinations

- **Source**: origin filesystem object or root under analysis; treated as immutable until approved retirement.
- **Destination**: proposed or approved target path/category for an organized copy.
- **Share**: Synology shared folder (for example an intended `/volume1/...` root).
- **Vault**: sensitive protected share (private, family, intel, etc.) with stricter overwrite and privacy controls.
- **Canonical Path**: normalized, approved destination path within taxonomy boundaries.
- **Taxonomy**: versioned human-readable category tree mapping to destination paths.

## Lifecycle and workflow

- **Ingestion**: intake of new or existing content into the controlled workflow.
- **Consolidation**: gathering dispersed sources into controlled consolidation areas (Phase 1).
- **Inventory**: read-only discovery producing durable file records without mutation.
- **Manifest**: portable durable listing (often JSONL) of inventory, plans, batches, or results.
- **Provenance**: recorded origin history (source root, relative path, device/export signals, observation time).
- **Fingerprint**: stable identity aids (size, timestamps, inode hints); not a substitute for cryptographic hash.
- **Hash**: cryptographic content digest used for exact-duplicate detection and copy verification.
- **Classification**: rule/evidence-driven proposal of semantic category and destination.
- **Rule**: versioned configuration entry that evaluates conditions and proposes outcomes.
- **Evidence**: observations supporting a classification or operation (metadata, hashes, detections, operator notes).
- **Confidence**: quantified strength of an inference or detection; thresholds are configurable.
- **Proposal**: non-executing recommendation (classification or operation) awaiting review/approval.
- **Review Item**: work item requiring human decision (conflict, low confidence, sensitive, unresolved).
- **Operation Plan**: immutable approved batch of filesystem actions with preconditions and rollback design.
- **Copy Operation**: approved copy from source to destination with logging and verification.
- **Move Operation**: approved relocation that still obeys copy-before-delete / retirement gating in V1 policy.
- **Retirement**: approved removal or archival of a source after destination verification.
- **Archive**: cold storage of completed structures, evidence, or retired materials.
- **Quarantine**: preserved holding area for duplicates, risky items, or policy exceptions—not deletion.
- **Unresolved**: governed holding for items that cannot yet be safely classified; visible, not discarded.
- **Validation**: independent check that outcomes match plan (hashes, counts, comparisons).
- **Rollback**: designed inverse or recovery path for mutations; idempotent where possible.
- **Checkpoint**: persisted restart point for safe resume after interruption.
- **Resume Token**: identifier allowing continuation without incorrectly repeating completed work.
- **Dry Run**: full evaluation producing plans/reports with **no** filesystem mutation.
- **Pilot Run**: end-to-end workflow on isolated copied corpus.
- **Live Run**: bounded approved mutation against live NAS paths under a separate readiness gate.
- **Run**: tracked execution instance (inventory, dry-run, pilot, or live) with state and events.

## Duplicates

- **Duplicate**: candidate redundancy relationship between files.
- **Exact duplicate / byte-identical duplicate**: cryptographic hash equality (and size agreement).
- **Near-Duplicate**: similar but not byte-identical (edits, transcodes, resizes); requires separate review.
- **Derivative**: transformed version of another file (export, compress, edit).
- **Alternate encoding**: same logical media in a different container/codec.
- **Burst-series media**: near-in-time capture sequences that may look similar.
- **Ambiguous duplicate**: insufficient evidence to decide canonical vs redundant.

## Safety and policy

- **Sensitive Data**: private, personal, family, explicit, business, or otherwise elevated-risk content.
- **Read-only**: observation without mutation.
- **Immutable plan**: plan that cannot change after approval; changes require a new plan version.
- **Copy-and-verify**: copy, hash-verify, then finalize; source retirement is separate.
- **Provisional rule**: reflects intent but is not final approved policy.
- **Protected vault overwrite prohibition**: existing vault content cannot be overwritten by default.

## Domain record shorthand

Terms such as `FileRecord`, `HashRecord`, `ClassificationRule`, `OperationPlan`, `Checkpoint`, `PilotRun`, `LiveRun`, and `SentinelCheck` are defined fully in `docs/02-specification/domain-model.md`.
