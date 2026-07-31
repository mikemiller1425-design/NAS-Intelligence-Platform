# ADR 002: Copy before delete

Status: Accepted (foundation candidate)

## Context
Source retirement is only acceptable after a verified copy exists at the destination. Delete-first workflows would make recovery far harder if an error occurred.

## Decision
The system copies approved content, verifies the copy, and only then considers source retirement. Delete is never the first action in a move workflow.

## Consequences
This preserves rollback options and lowers the chance of data loss. It can increase temporary storage usage during migration.

## Alternatives considered
Move-in-place or delete-first migration to save time or space.
