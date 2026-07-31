# FR-007 — Duplicate-photo review UI

## Purpose
Specialized UI for reviewing visual near-duplicates and burst series.

## Dependencies
Near-duplicate model beyond exact hashes; review console; non-destructive quarantine workflow.

## Risks
Operators confusing similarity with byte identity; accidental bulk discard.

## Reason excluded from V1
V1 includes exact-duplicate grouping and a general review queue. Specialized photo UI is enhancement.

## Promotion condition
Exact-duplicate workflow proven; near-duplicate analysis available; discard still approval-gated.
