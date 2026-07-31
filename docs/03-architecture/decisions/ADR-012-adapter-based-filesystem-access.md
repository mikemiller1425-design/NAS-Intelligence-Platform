# ADR 012: Adapter-based filesystem access

Status: Accepted (foundation candidate)

## Context
Direct filesystem coupling makes policy enforcement harder to audit. The architecture needs narrow boundaries.

## Decision
All filesystem access must flow through adapter interfaces rather than scattered direct calls.

## Consequences
This improves testability, policy enforcement, and reviewability. It also makes source, destination, and verification behaviors easier to swap or isolate.

## Alternatives considered
Direct filesystem access from many layers of the application.
