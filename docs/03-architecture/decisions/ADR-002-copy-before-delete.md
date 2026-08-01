# ADR 002: Copy before delete

Status: Accepted (foundation candidate)

## Context
Source retirement is only acceptable after a verified copy exists at the destination, where "verified" means content hash equality **and** a passing preservation comparison. Delete-first workflows would make recovery far harder if an error occurred.

## Decision
The system copies approved content, verifies the copy, and only then considers source retirement. Delete is never the first action in a move workflow.

## Consequences
This preserves rollback options and lowers the chance of data loss. It can increase temporary storage usage during migration. Source retirement is a **separate journalled operation** with its own intent record, outcome record, and approval scope flag; it is never a trailing step of the copy operation. A verified copy means content hash equality **and** a passing preservation comparison — hash equality alone is never sufficient to retire an original (see `docs/02-specification/preservation-model.md`).

## Alternatives considered
Move-in-place or delete-first migration to save time or space.
