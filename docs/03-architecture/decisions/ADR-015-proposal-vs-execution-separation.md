# ADR 015: Separation of classification proposal from operation execution

Status: Accepted (foundation candidate)

## Context
A proposal is not an action. The system must preserve a clear gap between what the classifier suggests and what the executor is allowed to do.

## Decision
Classification, planning, approval, and execution are separate stages with distinct records and constraints.

## Consequences
This prevents accidental conflation of recommendation and authority. It makes it easier to audit why a change happened and who approved it.

## Alternatives considered
Treating classification output as executable instructions.
