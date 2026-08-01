# System Architecture

## Purpose
This document defines the blueprint for the NAS Intelligence Platform. It is intentionally implementation-free: no production code, no live migration steps, and no Foundry stack copy.

## Architectural Intent
The platform is a safety-first file intelligence system for turning a disorganized Synology NAS into an inventoried, explainable, reviewable, and reversible archive. The architecture is built around five non-negotiables:

- Read-only inventory happens before any proposal.
- Dry-run is the default until explicit approval changes the mode.
- Human approval gates destructive work.
- Copy-before-delete is the only retirement path.
- Every action is auditable and explainable.

## System Boundaries
The platform is split into four logical domains:

- `apps/cli`: operator entry point for inventory, analysis, proposals, and controlled execution.
- `apps/review-console`: non-executing decision surface. Read-only toward file data; may submit only the bounded application-state commands listed in `docs/03-architecture/review-console-architecture.md`.
- `apps/sentinel`: Raspberry Pi-based watcher that monitors and alerts, but never authorizes destructive work.
- `packages/*`: shared contracts, adapters, persistence, validation, classification, planning, and observability building blocks.

## Trust Model
The architecture separates proposal from execution. Classification may suggest an operation, but only an approved execution path can perform a mutation. The frontend can display state, surface evidence, and capture approval intent, but it never authorizes filesystem mutation.

## Primary Hardware Roles
- Mac mini: primary worker for scanning, hashing, classification, planning, and verification.
- Raspberry Pi: Sentinel only, focused on monitoring, alerts, and lightweight supervision.
- Synology: protected storage authority and source of truth for stored files.

## Non-Goals
- No production implementation in this phase.
- No destructive migration automation.
- No direct filesystem mutation from the frontend.
- No copy of the Foundry stack as a baseline.
