# Source material

This directory holds original operator and blueprint source artifacts. Treat them as **intent input**, not automatically authoritative architecture.

Prefer Markdown when both Markdown and Word copies exist.

## Inventory

| Artifact | Form | Role |
| --- | --- | --- |
| `NAS_Organization_Operations_Manual_v1.0.md` | Markdown | Primary operations manual / blueprint baseline |
| `NAS_Organization_Operations_Manual_v1.0.docx` | Word | Same manual; Markdown preferred for editing |
| `CURSOR_NAS_Blueprint_Prompt.md` | Markdown | Earlier Cursor blueprint prompt (superseded where the foundation assignment is more specific) |

## Missing / not yet provided

The following were expected by the foundation assignment but were **not present** in the initial source drop. Tracked in `docs/05-governance/open-decisions.md` and `docs/migration/source-inventory.md`:

- Handwritten classification-rule transcriptions (beyond provisional examples in the operations manual)
- Folder diagrams / exported folder trees
- Synology share inventories confirming live `/volume1` structure
- Prior migration notes beyond the operations manual
- Screenshots of current shares

## Handling conflicts

If source material conflicts with active specifications, record the conflict and resolve only when latest intent is clear. Unresolved material decisions go to `docs/05-governance/open-decisions.md`.
