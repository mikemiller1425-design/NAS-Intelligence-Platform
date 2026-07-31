# ADR 003: Human approval for destructive actions

Status: Accepted (foundation candidate)

## Context
Destructive filesystem actions can permanently remove or alter data. Automated confidence is not sufficient to justify that level of risk.

## Decision
The execution path must require explicit human approval before any destructive step is allowed.

## Consequences
This creates a clear accountability boundary and reduces the impact of model or rule mistakes. It also adds friction to the workflow, which is intentional.

## Alternatives considered
Fully automated destructive cleanup based only on classification confidence.
