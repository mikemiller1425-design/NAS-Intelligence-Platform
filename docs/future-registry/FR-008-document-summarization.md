# FR-008 — Document summarization

## Purpose
Summarize documents to aid classification and discovery.

## Dependencies
Text extraction; privacy policy for retained summaries; local processing preference.

## Risks
Prompt injection from document content; inaccurate summaries steering wrong destinations.

## Reason excluded from V1
Classification uses rules and metadata first; summarization is not required for safe placement.

## Promotion condition
Summaries are evidence only; injection defenses tested; private vaults opt-in.
