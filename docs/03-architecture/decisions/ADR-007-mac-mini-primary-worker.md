# ADR 007: Mac mini primary worker

Status: Accepted (foundation candidate)

## Context
Scanning, hashing, and analysis are heavier workloads that should run on the most capable general-purpose machine available in this blueprint.

## Decision
The Mac mini is the primary worker for orchestration, analysis, and verification tasks.

## Consequences
This concentrates compute where it is practical and leaves smaller devices free for support roles. It also simplifies performance assumptions for planning.

## Alternatives considered
Spreading heavy analysis across the Pi or treating every node as interchangeable.
