# Source Inventory

Inventory of available blueprint source material as of Foundation `1.0-rc1`.

## Present in repository

| ID | Artifact | Location | Form | Preference | Notes |
| --- | --- | --- | --- | --- | --- |
| SRC-001 | NAS Organization Operations Manual v1.0 | `docs/source/NAS_Organization_Operations_Manual_v1.0.md` | Markdown | Preferred | Primary intent + safety + architecture baseline |
| SRC-002 | NAS Organization Operations Manual v1.0 (Word) | `docs/source/NAS_Organization_Operations_Manual_v1.0.docx` | DOCX | Secondary | Same content family as SRC-001 |
| SRC-003 | Cursor NAS Blueprint Prompt | `docs/source/CURSOR_NAS_Blueprint_Prompt.md` | Markdown | Historical | Earlier prompt; foundation assignment supersedes where more specific |

## Expected but not provided in the initial drop

| ID | Expected artifact | Status | Impact |
| --- | --- | --- | --- |
| SRC-MISS-001 | Handwritten / transcribed classification rules | Missing | Provisional rules only; OD-012 |
| SRC-MISS-002 | Folder diagrams / exported folder trees | Missing | Taxonomy remains provisional; OD-002 |
| SRC-MISS-003 | Synology share inventories confirming live `/volume1` | Missing | Intended vs live structure unresolved; OD-001, OD-013 |
| SRC-MISS-004 | Prior migration notes beyond the operations manual | Missing | Consolidation history may be incomplete |
| SRC-MISS-005 | Screenshots of current shares | Missing | Visual confirmation deferred |

## Concepts extracted from present sources

From SRC-001 (operations manual), materially extracted:

- Mission and success definition
- Non-negotiable safety laws
- Synology / Mac mini / Raspberry Pi operating model
- Canonical data zones and suggested control structure
- Inventory field requirements
- Classification rule configuration shape and provisional examples (Dogs, drone, CSV, sensitive identity candidate, unresolved)
- Duplicate and quarantine policy
- Workflow gates 0–7
- Operation planning / execution rules
- Rollback and Sentinel responsibilities
- Security/privacy constraints
- Acceptance criteria and stop conditions
- Open decisions list (manual §18)

From the foundation assignment (operator instruction used to generate this repository):

- Expanded lifecycle and phase mapping
- Known intended `/volume1` share names and migration-control layout
- Consolidation-source and unresolved category names
- Detailed domain/spec/ADR/playbook/handoff requirements
- Future Registry deferrals
- Explicit prohibition on live NAS work and production implementation

## Handling

Source material is intent input. Conflicts are recorded; unresolved material decisions live in `docs/05-governance/open-decisions.md`. Traceability is in `traceability-matrix.md`.
