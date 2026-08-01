# ADR 015: Separation of classification proposal from operation execution

Status: Accepted (foundation candidate)

## Context
A proposal is not an action. The system must preserve a clear gap between what the classifier suggests and what the executor is allowed to do.

## Decision
Classification, planning, approval, and execution are separate stages with distinct records and constraints. Authorization does not travel across a stage boundary as a token, a flag, or client-held state: it is re-derived at the execution stage from the authoritative Journal on every attempt. The only artifact that crosses the boundary is an approval id; every value that gives it meaning is recomputed by the executor.

## Consequences
This prevents accidental conflation of recommendation and authority. It makes it easier to audit why a change happened and who approved it.

## Alternatives considered
Treating classification output as executable instructions.
