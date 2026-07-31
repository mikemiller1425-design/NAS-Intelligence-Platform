# FR-001 — Semantic search

## Purpose
Enable natural-language search across inventoried files using extracted text and metadata.

## Dependencies
Stable inventory, metadata extraction, privacy policy for text retention, search index storage outside live shares.

## Risks
Privacy leakage from indexed private content; incorrect relevance treated as classification authority; index drift from filesystem reality.

## Reason excluded from V1
V1 prioritizes inventory, explainable placement, and safe migration. Search is a post-organization capability.

## Promotion condition
Organized baseline exists; text-retention privacy decision approved; acceptance tests prove index never authorizes mutation.
