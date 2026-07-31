# Data Architecture

## Data Model Goals
The data architecture is designed for traceability, replayability, and safety. Every important decision should be reconstructable from stored evidence, without requiring access to mutable application state.

## Canonical Data Classes
- Inventory record: path, size, timestamps, discovered type, ownership hints, and source context.
- Metadata record: extracted technical and semantic metadata.
- Classification proposal: explainable suggestion with rule references and confidence cues.
- Plan record: proposed destination, operation type, and approval requirements.
- Execution record: approved step, verification result, and post-action state.
- Audit record: immutable timeline entry for every significant action.

## Storage Strategy
- SQLite is the primary query and coordination store for structured state.
- JSONL manifests are used for append-only evidence, audit trails, and replayable job history.
- Hashes are stored for exact duplicate detection and copy verification.
- The system avoids depending on ad hoc mutable blobs for core truth.

## Data Separation
- Proposal data is distinct from execution data.
- Review evidence is distinct from operational state.
- Source inventory is distinct from destination validation.
- Frontend state is never the authority for mutation.

## Safety Implications
The architecture keeps irreversible outcomes out of ephemeral memory and into durable records. This enables validation, rollback analysis, and independent review after the fact.
