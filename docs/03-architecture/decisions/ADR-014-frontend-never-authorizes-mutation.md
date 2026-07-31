# ADR 014: Frontend never authorizes filesystem mutation

Status: Accepted (foundation candidate)

## Context
A user interface can present evidence and capture intent, but it should not hold direct authority over filesystems. UI compromise or logic bugs must not become destructive write paths.

## Decision
The frontend can propose or submit decisions, but it cannot authorize filesystem mutation on its own.

## Consequences
This keeps the trust boundary behind back-end policy checks. It also means the review console must remain intentionally limited in scope.

## Alternatives considered
Allowing UI actions to directly sign off on or trigger filesystem mutation without back-end policy gates.
