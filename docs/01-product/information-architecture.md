# Information Architecture

This document defines how information is organized both in the product and in the repository.

## Architectural layers

### 1. Source materials

The source layer contains the original manual, blueprint prompt, and any additional operator notes. These documents define intent and constraints.

### 2. Intent layer

The intent layer explains why the product exists, what it values, and how it stays safe.

- `docs/00-intent/product-intent.md`
- `docs/00-intent/principles.md`
- `docs/00-intent/glossary.md`
- `docs/00-intent/role-charter.md`

### 3. Product layer

The product layer defines the visible outcomes, scope, exclusions, journeys, and information structure.

- `docs/01-product/product-definition.md`
- `docs/01-product/v1-scope.md`
- `docs/01-product/exclusions.md`
- `docs/01-product/operator-journeys.md`
- `docs/01-product/information-architecture.md`

### 4. Policy layer

The policy layer will eventually define rule priority, taxonomy, duplicate handling, privacy, retention, and quarantine behavior. It must remain traceable to source intent and operator approval.

### 5. Specification layer

The specification layer will define the domain model, inventory model, rule model, workflow model, operation plan model, monitoring model, and interface model.

### 6. Architecture layer

The architecture layer will define the system boundaries, worker split, storage model, security model, testing strategy, and recovery approach.

### 7. Governance layer

The governance layer will define authority, change control, open decisions, approval gates, stop conditions, and evidence standards.

### 8. Migration and evidence layer

The migration layer will record source inventory, reconciliation, and traceability. The evidence layer stores manifests, plans, reports, journals, and audit material.

## Product information domains

The platform organizes information into these domains:

- **Source zones**: read-only areas under analysis.
- **Migration control**: manifests, plans, logs, reports, checkpoints, and unresolved items.
- **Incoming**: new content awaiting intake.
- **Organized library**: approved destinations.
- **Manual review**: ambiguous, conflicting, risky, or low-confidence items.
- **Quarantine**: preserved exception handling for duplicates or policy issues.
- **Pilot**: isolated copied test data.
- **Archive**: completed evidence and historical records.

## Repository information architecture

The repository should make the path from source intent to implementation readiness obvious.

- `docs/source/` keeps source material and inventory.
- `docs/00-intent/` defines mission, principles, glossary, and roles.
- `docs/01-product/` defines the product and V1 boundaries.
- `docs/02-specification/` will describe the system model.
- `docs/03-architecture/` will describe the implementation shape.
- `docs/04-acceptance/` will define verification criteria.
- `docs/05-governance/` will define authority and open decisions.
- `docs/migration/` will track reconciliation and traceability.
- `docs/handoffs/` will define the foundation audit and build ladder.
- `docs/audits/` will store audit outputs.
- `docs/archive/` stores completed or superseded evidence and historical records.

## Naming and traceability rules

- Use stable names for zones, documents, and decisions.
- Keep provisional concepts labeled as provisional until approved.
- Do not bury important decisions inside code or ephemeral chat history.
- Preserve line-of-sight from source material to active blueprint documents.

## Open decisions reflected in the architecture

- Exact share names versus logical zone names.
- Whether some logical zones map to one share or many shares.
- Whether control data lives on Synology, Mac mini, or both.
- How much operational data the Mac mini may retain locally.
- Which review and archive paths are final versus illustrative.
