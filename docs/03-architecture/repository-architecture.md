# Repository Architecture

## Repository Intent
This repository is organized to separate product intent, architecture, executable surfaces, shared libraries, and test evidence. The layout is intentionally scaffolded so the blueprint can be reviewed before any implementation is written.

## Top-Level Structure
- `docs/`: product, specification, architecture, acceptance, governance, operations, and audit documentation.
- `apps/`: future user-facing entry points.
- `packages/`: reusable domain and infrastructure modules.
- `tests/`: planned verification layout and fixture organization.
- `scripts/` and `tools/`: future maintenance and operator helpers.

## Application Boundaries
- `apps/cli`: operator-facing command surface for inventory, planning, and controlled execution.
- `apps/review-console`: read-only review UI for approvals and evidence.
- `apps/sentinel`: lightweight monitoring and alerting process for the Raspberry Pi.

## Package Boundaries
- `contracts`: canonical types and request/response shapes.
- `inventory`: read-only discovery and cataloging.
- `metadata`: extraction and normalization.
- `classification`: rule-driven proposals and explanations.
- `planning`: destination and operation planning.
- `copy-engine`: approved copy and verification orchestration.
- `validation`: hash and state validation.
- `persistence`: SQLite and JSONL persistence boundaries.
- `adapters`: filesystem and storage adapters.
- `observability`: logs, metrics, traces, and audit sinks.

## Architectural Constraints
- The repository must preserve blueprint-only status until implementation authorization.
- Frontend code must not directly authorize filesystem mutation.
- Filesystem access must be adapter-based.
- Destructive behavior must remain behind approval and audit gates.
