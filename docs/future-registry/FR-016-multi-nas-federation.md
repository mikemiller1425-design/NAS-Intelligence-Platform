# FR-016 — Multi-NAS federation

## Purpose
Coordinate inventory and migration across multiple NAS devices.

## Dependencies
Per-NAS adapters; identity of files across devices; conflict policy.

## Risks
Cross-device deletion mistakes; inconsistent snapshots; network partitions mid-copy.

## Reason excluded from V1
Single Synology target is the V1 mission.

## Promotion condition
Single-NAS V1 complete and trustworthy; federation plans are per-device gated.
