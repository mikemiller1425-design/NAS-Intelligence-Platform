# FR-012 — Automated ingest watchers

## Purpose
Watch incoming drops and continuously classify new files after migration.

## Dependencies
Post-migration maintenance mode; dry-run default for new proposals; Sentinel alerts optional.

## Risks
Unattended live moves; watchers pointed at live shares with unsafe defaults.

## Reason excluded from V1
V1 includes a maintenance *foundation* and continuous-ingestion *design*, not unattended live watchers.

## Promotion condition
Migration verified; ingest rules dry-run first; live auto-apply separately authorized per source.
