# ADR 001: Read-only inventory first

Status: Accepted (foundation candidate)

## Context
Read-only inventory is the foundation for every later decision. Any proposal or execution without inventory evidence would weaken traceability and safety.

## Decision
Inventory must happen before classification, planning, approval, or execution. The system treats inventory as immutable evidence, not a side effect of analysis.

## Consequences
This improves provenance and reduces accidental mutation. It also means early runs may feel slower because they must collect evidence before acting.

## Alternatives considered
Start with direct mutation or opportunistic file moves; derive proposals without a complete inventory.
