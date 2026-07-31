# Product Intent

## Mission

NAS Intelligence Platform is a safety-first file intelligence, migration, classification, organization, validation, and maintenance system for a Synology NAS.

The product exists to turn an accumulated file collection into a dependable information system without losing originals, provenance, recovery options, or human control.

## Core promise

The platform must:

- inventory everything in scope before it mutates anything;
- preserve source bytes and source paths during discovery and analysis;
- classify files with traceable evidence and versioned rules;
- propose destination placement without silent overwrite or silent deletion;
- require human review for ambiguity, conflict, and sensitive identity cases;
- verify every approved mutation with independent comparison and hash checks;
- keep the system maintainable after the initial consolidation.

## Operating model

- Synology is the protected storage authority and final library host.
- The Mac mini is the primary worker for inventory, analysis, planning, approved execution, and verification.
- The Raspberry Pi is a sentinel only: it monitors health, freshness, capacity, and queue state.
- The human operator is the final authority for taxonomy, policy, approval, and the transition from dry run to live execution.

## Intended outcome

The product should make the NAS:

- explainable to a human without relying on chat history;
- auditable from source material through final disposition;
- resilient to restarts, failures, and partial runs;
- safe to expand from a small pilot into continuous ingestion;
- explicit about what was classified, what was reviewed, what was copied, what was kept, and what still needs attention.

## Lifecycle intent

The platform is designed to move through these phases:

`Source Discovery -> Read-Only Inventory -> Provenance Capture -> File-Type Identification -> Metadata Extraction -> Content Analysis -> Rule Evaluation -> Conflict Detection -> Destination Proposal -> Human Review -> Approved Copy -> Source/Destination Comparison -> Integrity Validation -> Approved Source Retirement -> Deduplication and Normalization -> Continuous Ingestion`

These phases are not an authorization ladder. Each phase produces evidence for the next phase, but no phase automatically grants permission to mutate live NAS data.

## Design posture

This is a blueprint-first product.

- Dry-run is the default operating posture.
- Live NAS mutation is prohibited until independent audit, approved build ladder, and explicit operator authorization.
- Copy-and-verify is preferred over destructive operations.
- Uncertainty routes to review, not guesswork.
- Provisional rules remain provisional until confirmed by the operator.

## Success criteria

The product is successful when:

- every in-scope file has a stable identity and a final disposition;
- exact duplicates are recognized without confusing them with near-duplicates;
- exceptions are owned instead of being silently dropped;
- approved moves can be reconstructed and reversed from evidence;
- the taxonomy is understandable and maintainable by humans;
- new content can be ingested without reintroducing disorder.

## Open decisions carried forward

- Exact source and destination share boundaries still require final confirmation.
- Sensitive identity handling remains policy-bound and operator-controlled.
- Rollout thresholds, quarantine retention, and any future cleanup rules remain open until approved.
