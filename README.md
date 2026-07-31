# NAS Intelligence Platform

Safety-first file intelligence, migration, classification, organization, validation, and maintenance for transforming a disorganized Synology NAS into a fully inventoried, explainable, reviewable, and sustainably organized digital environment.

This product is **not** merely a file mover, duplicate finder, folder script, media classifier, or one-time cleanup utility. It is intended to become an autonomous digital archivist that inventories files, preserves provenance, classifies content, detects duplicates, proposes destinations, requests human review, executes approved copies, verifies results, preserves rollback evidence, monitors future ingestion, and maintains the organized state over time.

## Why it exists

Years of downloads, device dumps, media, documents, and project files accumulate faster than manual organization can keep up. Improvised bulk moves risk irreversible loss of irreplaceable personal, private, family, business, and project data. This platform exists to organize the NAS through a gated, auditable, reversible process—not improvisation.

## Current phase

**Blueprint / Foundation Candidate `1.0-rc1` — ready for independent audit**

| Gate | Status |
| --- | --- |
| Blueprint complete | Candidate complete |
| Independent architecture & safety audit | **Required next** |
| Implementation | **Blocked** |
| Dry-run engine | **Prohibited until implementation authorization** |
| Live NAS execution | **Prohibited** |

See `FOUNDATION_VERSION.md` and `PROJECT_STATUS.md`.

## Safety posture

- Inventory is read-only.
- Source files are immutable until an approved retirement stage.
- Copy before delete.
- Dry-run is the default; live mode must be deliberately enabled.
- Every proposed move has an explainable reason and a stable operation ID.
- Every ambiguity goes to review; every destructive action requires human approval.
- Hash verification is required before source retirement.
- Protected vaults cannot be overwritten by default.
- AI classifications are evidence, not unquestionable truth.
- The Raspberry Pi may monitor and alert; it is **not** the primary heavy-analysis engine.
- The Mac mini (or equivalent capable worker) performs heavy scanning, hashing, media analysis, and orchestration.
- Synology remains the protected storage authority.

## Lifecycle

```text
Source Discovery
→ Read-Only Inventory
→ Provenance Capture
→ File-Type Identification
→ Metadata Extraction
→ Content Analysis
→ Rule Evaluation
→ Conflict Detection
→ Destination Proposal
→ Human Review
→ Approved Copy
→ Source/Destination Comparison
→ Integrity Validation
→ Approved Source Retirement
→ Deduplication and Normalization
→ Continuous Ingestion and Maintenance
```

High-level migration phases:

```text
Phase 1 — Consolidate
Phase 2 — Build scaffold
Phase 3 — Analyze
Phase 4 — Organize into scaffold
Phase 5 — Compare, validate, then archive old structure
After validation — Normalize and deduplicate
```

## Repository map

| Path | Responsibility |
| --- | --- |
| `docs/00-intent/` | Product intent, principles, glossary, roles |
| `docs/01-product/` | Product definition, scope, exclusions, journeys, IA |
| `docs/02-specification/` | Domain, lifecycle, rules, taxonomy, ops, security |
| `docs/03-architecture/` | System design, topology, ADRs, testing, observability |
| `docs/04-acceptance/` | V1, safety, pilot, and live-readiness acceptance |
| `docs/05-governance/` | Authority, change control, open decisions, DoR/DoD |
| `docs/06-operations/` | Dry-run, pilot, live, rollback, incident, Sentinel |
| `docs/source/` | Original operator source material |
| `docs/migration/` | Source inventory, reconciliation, traceability |
| `docs/handoffs/` | Audit and build-ladder handoffs |
| `docs/audits/` | Independent audit findings |
| `docs/future-registry/` | Explicitly deferred concepts |
| `config/` | Non-production example rules, taxonomy, exclusions |
| `apps/` | Future CLI, review console, Sentinel (placeholders) |
| `packages/` | Future library boundaries (placeholders) |
| `prompts/` | Reusable audit and implementation prompts |
| `tests/` | Future fixture and acceptance test layout |
| `scripts/`, `tools/` | Future tooling placeholders |

## Documentation authority order

1. Explicit operator decisions recorded in governance
2. Active specifications and principles
3. Architecture ADRs
4. Acceptance criteria
5. Operational playbooks
6. Product documents
7. Source material under `docs/source/` (intent input, not automatic architecture authority)
8. Future Registry (explicitly non-V1)
9. Archive

See `docs/05-governance/authority-order.md`.

## Implementation authorization status

**Blocked.** Do not begin production implementation. Do not generate a Build Ladder for Claude Code until Foundation approval after independent review.

## Exact next action

Submit the completed NAS Intelligence Platform blueprint for independent ChatGPT review. Do not hand it to Claude Code until that review is complete and all approved BLOCKER and MAJOR findings are resolved.
