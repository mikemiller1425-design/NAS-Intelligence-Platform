# FR-002 — Vector indexing

## Purpose
Store embeddings for similarity search across documents and media descriptions.

## Dependencies
FR-001 semantic search policy; local embedding model choice; storage capacity; privacy controls for embeddings derived from private media.

## Risks
Sensitive content reconstructability; embedding model licensing; treating similarity as duplicate equality.

## Reason excluded from V1
Exact-hash duplicates and rule-based classification cover V1; vector similarity is not required for safe organization.

## Promotion condition
Privacy review complete; similarity never auto-deletes; operator-approved model runs locally by default.
