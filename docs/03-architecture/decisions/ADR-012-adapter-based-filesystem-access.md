# ADR 012: Adapter-based filesystem access

Status: Accepted (foundation candidate)

## Context
Direct filesystem coupling makes policy enforcement harder to audit. The architecture needs narrow boundaries.

## Decision
All filesystem access must flow through adapter interfaces rather than scattered direct calls. Every adapter must publish a **measured capability descriptor** covering identity evidence, preservation properties, filename transparency, case and normalization sensitivity, timestamp resolution, and a per-volume `durability_class` of `strong`, `weak`, or `unknown` backed by a startup self-test. Unverified capabilities are `unknown` and are treated as `weak`. Hand-written or assumed descriptors are invalid and may not gate any operation. The Execution Journal must reside on a `strong` volume; if none is available, filesystem mutation is prohibited. Destination volumes below `strong` force degraded mode: mandatory post-finalize re-read verification, batch size one, no concurrency, and no source retirement.

## Consequences
This improves testability, policy enforcement, and reviewability, and it lets implementation proceed against fixtures while the live adapter choice (OD-016) remains open: behavior is a function of declared capabilities, not of a particular product.

## Alternatives considered
Direct filesystem access from many layers of the application.
