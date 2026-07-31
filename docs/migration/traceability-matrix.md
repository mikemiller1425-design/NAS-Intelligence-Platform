# Traceability Matrix

Maps significant source concepts to authoritative active destinations. Status values: **Present**, **Provisional**, **Open**, **Deferred**, **Rejected**.

| Source concept | Origin | Authoritative destination | Status |
| --- | --- | --- | --- |
| Product mission / fully organized NAS | SRC-001 + assignment | `docs/00-intent/product-intent.md`, `docs/01-product/product-definition.md` | Present |
| Non-negotiable safety laws | SRC-001 + assignment §5 | `docs/00-intent/principles.md`, ADRs 001–015 | Present |
| Synology / Mac mini / Pi topology | SRC-001 | `docs/00-intent/role-charter.md`, `docs/03-architecture/execution-topology.md`, ADR-007, ADR-008 | Present |
| Canonical data zones | SRC-001 | `docs/02-specification/taxonomy-model.md`, `config/taxonomy/` | Provisional |
| Known `/volume1` share names | Assignment | `docs/02-specification/taxonomy-model.md`, `config/taxonomy/taxonomy.example.yaml`, OD-001/013 | Provisional / Open |
| Migration-control layout | Assignment + SRC-001 (variant) | `docs/02-specification/taxonomy-model.md`, open decision if structures differ | Open (MERGE) |
| Inventory model fields | SRC-001 | `docs/02-specification/inventory-model.md`, `docs/02-specification/domain-model.md` | Present |
| Classification rules as config | SRC-001 + assignment §6 | `docs/02-specification/rule-model.md`, `config/rules/` | Present |
| Dogs domain precedence | SRC-001 / assignment | `config/rules/classification-rules.example.yaml`, OD-012 | Provisional |
| Drone routing | SRC-001 | same | Provisional |
| CSV / structured routing | SRC-001 | same | Provisional |
| Sensitive identity candidate | SRC-001 / assignment | disabled example rule + OD-003 / FR-003 | Provisional / Deferred |
| Unresolved fallback | SRC-001 + assignment | rule model + taxonomy unresolved nodes | Present |
| Exact duplicate hashing | SRC-001 | `docs/02-specification/duplicate-model.md`, ADR-004 | Present |
| Near-duplicate deletion | SRC-001 | `docs/01-product/exclusions.md`, FR-007 | Rejected in V1 |
| Workflow gates 0–7 | SRC-001 | `docs/06-operations/*`, `docs/04-acceptance/*` | Present |
| Engine lifecycle mapping | Assignment §4 | `docs/02-specification/lifecycle-model.md`, product docs | Present |
| High-level phases 1–5 | Assignment | lifecycle + operations playbooks | Present |
| Operation plan immutability | SRC-001 | `docs/02-specification/operation-model.md`, ADR-015 | Present |
| Copy-before-delete | SRC-001 + assignment | principles, ADR-002 | Present |
| Dry-run default | Assignment | ADR-009, thresholds example | Present |
| Pilot before live | SRC-001 + assignment | ADR-010, pilot playbook/acceptance | Present |
| Protected vault overwrite ban | Assignment | ADR-011, exclusions config | Present |
| Frontend never authorizes mutation | SRC-001 + assignment | ADR-014, permission model | Present |
| Sentinel non-destructive authority | SRC-001 | sentinel architecture + playbook | Present |
| Stop conditions | SRC-001 | incident-response + live playbook | Present |
| Acceptance criteria | SRC-001 + assignment | `docs/04-acceptance/` | Present |
| Open decisions list | SRC-001 §18 + assignment | `docs/05-governance/open-decisions.md` | Present |
| Permanent deletion | SRC-001 | exclusions + safety acceptance | Rejected in V1 |
| Cloud upload | Assignment exclusions | FR-017 | Deferred |
| Semantic search | Assignment future | FR-001 | Deferred |
| Vector indexing | Assignment future | FR-002 | Deferred |
| Face recognition assistance | Assignment future | FR-003 | Deferred |
| Multimodal models | Assignment future | FR-004 | Deferred |
| Quality scoring / auto-delete low quality | Assignment | FR-005 + exclusions | Deferred / Rejected auto-delete |
| Media curation | Assignment future | FR-006 | Deferred |
| Duplicate-photo review UI | Assignment future | FR-007 | Deferred |
| Document summarization | Assignment future | FR-008 | Deferred |
| Family timeline | Assignment future | FR-009 | Deferred |
| Project knowledge extraction | Assignment future | FR-010 | Deferred |
| DataVault enrichment | Assignment future | FR-011 | Deferred |
| Automated ingest watchers | Assignment future | FR-012 (V1 has maintenance foundation only) | Deferred |
| Mobile review | Assignment future | FR-013 | Deferred |
| Foundry integration | Assignment future | FR-014 | Deferred |
| Agent City visualization | Assignment future | FR-015 | Deferred |
| Multi-NAS federation | Assignment future | FR-016 | Deferred |
| Advanced storage optimization | Assignment future | FR-018 | Deferred |
| Handwritten rule transcriptions | Expected source | Missing → OD-012 | Open |
| Confirmed live share inventory | Expected source | Missing → OD-001/013 | Open |

## Coverage rule

- Every significant manual or assignment concept must appear in an active document, Future Registry entry, or open decision.
- Nothing safety-critical may disappear silently.
- Future Registry concepts must not leak into V1 scope documents as required capabilities.
