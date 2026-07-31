# Taxonomy Model

## Purpose

This document defines the human-readable destination taxonomy used by the NAS Intelligence Platform. The taxonomy is designed to be durable, explainable, and versioned so that every proposed destination can be traced to a stable human category.

The taxonomy distinguishes three authority levels:

- `confirmed_live`: verified existing NAS structure or operator-approved live structure.
- `intended_structure`: the proposed design for V1 and pilot work.
- `unresolved_assumption`: a placeholder used when source evidence is incomplete.

Only `confirmed_live` and approved `intended_structure` entries may become execution destinations. `unresolved_assumption` entries are for specification and review only.

## Taxonomy principles

1. The taxonomy must be understandable without the software.
2. Categories must be durable, not tied to a transient implementation detail.
3. Every category must have a clear owner, purpose, and promotion path.
4. Sensitive categories require explicit policy review.
5. Taxonomy changes are versioned and never retroactive by default.
6. No taxonomy entry implies deletion or retention policy by itself.

## Structural model

The taxonomy is a tree with optional cross-links for reporting and review. Each node is a `TaxonomyNode`.

### Required node attributes

- `slug`
- `display_name`
- `path_template`
- `parent_slug`
- `authority`
- `status`
- `intended_use`
- `notes`

### Path template rules

- Path templates use literal strings and controlled placeholders only.
- Placeholders may include `{capture_year}`, `{capture_date}`, `{source_root}`, `{media_kind}`, `{document_kind}`, or operator-approved equivalents.
- Templates may not interpolate raw untrusted input without normalization.
- A template must remain under an approved root.

## Authority levels

### Confirmed live

Use when a category maps to an actual, verified NAS folder or an operator-approved production destination.

Requirements:

- evidence of existence or approved creation plan
- no traversal outside approved roots
- traceability to a named source or policy decision

### Intended structure

Use when a category is the approved design target for blueprinting, fixtures, or pilot staging.

Requirements:

- explicitly documented in the blueprint
- approved by policy or pending review
- not confused with live authorization

### Unresolved assumption

Use when the category is a placeholder or guess.

Requirements:

- must be visibly marked unresolved
- must route to review
- must not be used as an execution destination until resolved

## Known Synology `/volume1` share intent

These names are **known intended structure** from operator context. They are **not** confirmed live structure until OD-001/OD-013 are resolved. They must not be hardcoded as unsafe mutation defaults.

| Share | Authority | Notes |
| --- | --- | --- |
| `00_MIGRATION_CONTROL` | intended | Control plane for manifests, reports, unresolved, configs, database, logs |
| `01_PRIVATE_VAULT` | intended + sensitive | Contains real material; never overwrite or destructively normalize by default |
| `02_FAMILY_VAULT` | intended + sensitive | Protected from overwrite by default |
| `03_INTEL_VAULT` | intended + sensitive | Protected from overwrite by default |
| `04_DATA_VAULT` | intended | Structured/semi-structured data |
| `05_BACKUPS` | intended | Not a classification dump target |
| `10_CORE` | intended | Core durable library content |
| `30_DRONE` | intended | Drone media |
| `40_MAKERLAB` | intended | Maker / fabrication projects |
| `50_MEDIA` | intended | General media library |
| `60_BUSINESS` | intended + sensitive | Business materials |
| `70_PERSONAL` | intended + sensitive | Personal non-vault materials |
| `80_ARCHIVE` | intended | Cold archive |
| `CHATGPT_EXPORTS` | intended | Export holdings; classify carefully |
| `homes` | intended | User home shares; treat with care |
| `photo` | intended | Synology Photos-related; confirm interaction policy |

Intended project location concept: `90_Project/nas-intelligence-platform` (OD-020).

### Migration-control intended children (assignment)

```text
00_MIGRATION_CONTROL/
├── 00_Consolidation_Source/
│   ├── From_Downloads/
│   ├── External_Drives/
│   ├── iPhone/
│   ├── Mac/
│   ├── Manual_Drops/
│   ├── Original_Folder_Structure/
│   └── Unknown_Source/
├── 01_Migration_Manifests/
├── 02_Analysis_Reports/
├── 03_Copy_Logs/
├── 04_Comparison_Reports/
├── 05_Unresolved/
│   ├── Unknown-Data/
│   ├── Unknown-Documents/
│   ├── Unknown-Media/
│   └── Needs-Manual-Review/
├── configs/
├── database/
└── logs/
```

The operations manual proposes an alternate control layout (`01_Inventory`…`08_Checkpoints`). See OD-014 — merge before implementation.

## Canonical top-level zones

The platform’s controlled zones are logical categories first and filesystem paths second.

### Migration control

Purpose: manifests, plans, journals, checkpoints, reports, and reconciliation evidence.

### Incoming

Purpose: newly ingested items awaiting inventory or classification.

### Organized

Purpose: approved durable destination library.

### Review

Purpose: ambiguous, conflicting, low-confidence, or policy-sensitive items.

### Quarantine

Purpose: preserved exception handling for exact duplicates, corruption, unsafe names, or policy exceptions.

### Pilot

Purpose: copied test corpus used to validate workflows safely.

### Archive

Purpose: completed evidence, historical manifests, batch outputs, and frozen records.

## Destination design rules

### Family and people media

- May use capture date, media kind, and operator-confirmed content categories.
- Sensitive identity categories require explicit confirmation and separate policy handling.
- Dog/person intent remains provisional until a rule is approved.

### Device media

- Drone media may be routed by source-device evidence and capture time.
- The rule must remain provisional until the source signal is validated.

### Structured data

- CSV and related structured files should route to a structured-data branch of the taxonomy.
- Structured-data destinations should preserve the original file and any derived profile artifacts separately.

### Unresolved items

- Unresolved items route to review or unresolved holding zones only.
- Unresolved is not a durable final destination unless specifically approved as an exception.

## Versioning

Taxonomy versions must be explicit. A taxonomy version includes:

- version identifier
- operator or policy owner
- effective date
- changed nodes
- superseded nodes
- migration notes

### Versioning rules

1. A node may be renamed only through a versioned change.
2. A path template change requires auditability.
3. Deleting a live node is disallowed unless a separately approved retirement process exists.
4. Historical decisions must remain interpretable against the taxonomy version active at the time of the decision.

## Examples

### Intended structure example

```yaml
taxonomy_version: 1
nodes:
  - slug: family
    display_name: Family
    parent_slug: root
    authority: intended_structure
    status: active
    path_template: "Demo/Organized/Family"
    intended_use: "General family media"
  - slug: family-dogs
    display_name: Dogs
    parent_slug: family
    authority: intended_structure
    status: provisional
    path_template: "Demo/Organized/Family/Dogs/{capture_year}"
    intended_use: "Provisional dog-related family media"
  - slug: people-voss
    display_name: Voss
    parent_slug: family
    authority: unresolved_assumption
    status: unresolved
    path_template: "Demo/Review/People/Voss"
    intended_use: "Sensitive identity placeholder requiring confirmation"
```

### Confirmed live example

```yaml
taxonomy_version: 1
nodes:
  - slug: control
    display_name: Migration Control
    parent_slug: root
    authority: confirmed_live
    status: active
    path_template: "Demo/Migration-Control"
    intended_use: "Plans, manifests, journals, and checkpoints"
```

## Relationships to other models

- `RuleSet` and `ClassificationRule` may target `TaxonomyNode.path_template`.
- `OperationPlan` must validate that destination paths resolve to approved taxonomy nodes.
- `ReconciliationReport` must summarize items by taxonomy node and authority level.

## V1 limits

- The taxonomy does not guarantee a live folder already exists.
- The taxonomy does not authorize mutation by itself.
- Any unresolved category must stay visibly unresolved until an operator resolves it.

