# FR-018 — Advanced storage optimization

## Purpose
Optimize packing, compression, tiering, or block-level efficiency after organization.

## Dependencies
Synology features; non-destructive first; replacement of Synology backup systems explicitly out of scope.

## Risks
Corruption via aggressive recompression; defeating backups; silent format changes.

## Reason excluded from V1
Organization and accountability first. Storage optimization is a later ops concern and must not replace Synology backups.

## Promotion condition
Migration verified; optimization never alters canonical bytes without a verified derivative workflow.
