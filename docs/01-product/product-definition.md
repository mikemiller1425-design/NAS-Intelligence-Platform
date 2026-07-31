# Product Definition

## What the product is

The NAS Intelligence Platform is a safety-first system for making a Synology NAS understandable, organized, verifiable, and maintainable.

It is not a bulk mover, not a silent deduper, and not a dashboard that pretends to be the source of truth. It is a controlled information system that turns raw file accumulation into a governed, auditable library.

## Why it exists

The platform exists to solve four problems at once:

1. The NAS contains valuable content that must not be lost.
2. The content lacks consistent organization, provenance, and final disposition.
3. Manual cleanup is too large and too risky to do casually.
4. The system must continue to ingest future files without recreating disorder.

## Product goals

- preserve originals while discovering and organizing them;
- create trustworthy inventory, metadata, and hash records;
- classify content using explicit versioned rules and traceable evidence;
- propose safe destinations and surface conflicts for human review;
- verify every approved mutation;
- maintain a durable record of what was done and why;
- support a future steady-state ingestion workflow.

## Users and stakeholders

- **Human operator**: owns final decisions and policy boundaries.
- **Mac mini worker**: performs the operational analysis and approved file operations.
- **Raspberry Pi Sentinel**: watches health and emits alerts.
- **Independent auditor**: checks blueprint completeness, safety, and readiness.

## System boundary

The product includes:

- source discovery and inventory;
- provenance capture;
- file-type identification and metadata extraction;
- hash-based exact duplicate grouping;
- rule-driven classification;
- manual review queues;
- dry-run plan generation;
- approved copy/move execution;
- verification and reconciliation;
- logs, manifests, and checkpoints;
- monitoring and alerting for safe operation.

The product excludes live NAS mutation until the blocked implementation gate is cleared.

## Quality attributes

The product must be:

- **safe**: no silent destruction, no accidental overwrite, no unauthorized mutation;
- **auditable**: every recommendation and action is traceable;
- **reversible**: rollback and recovery are designed before execution;
- **deterministic**: repeated scans and plans should be stable for the same inputs;
- **human-governed**: ambiguous or sensitive items are not guessed into place;
- **maintainable**: rules, reports, and operating instructions remain understandable over time.

## Product philosophy

The platform intentionally separates:

- discovery from mutation;
- recommendation from approval;
- execution from verification;
- monitoring from control;
- provisional intent from final policy.

This separation is the core reason the product can be trusted around valuable personal and family data.

## What success looks like

Success is not just "files moved." Success is:

- every in-scope file has a known disposition;
- every rule outcome is explainable;
- exact duplicates are identified without conflating them with near-duplicates;
- unresolved items are visible and owned;
- pilot results prove the workflow before broader rollout;
- the final structure makes ongoing use easier instead of harder.

## Open decisions

The following items remain decision points and are documented elsewhere as open decisions:

- exact source and destination share boundaries;
- final taxonomy mapping for logical zones to physical paths;
- identity and privacy handling rules for sensitive classifications;
- exact hash strategy and performance tradeoffs;
- rollout thresholds and batch sizing;
- quarantine retention and future cleanup policy;
- whether temporary thumbnails or extracted text may live on the Mac mini.
