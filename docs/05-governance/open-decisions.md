# Open Decisions

Unresolved decisions from the operations manual and foundation assignment. Classify as BLOCKER, MAJOR, or MINOR. Do not treat unresolved items as approval to mutate live data.

## BLOCKER

| ID | Decision | Notes |
| --- | --- | --- |
| OD-001 | Exact Synology share roots in and out of scope | Intended `/volume1` names are documented; live confirmation missing. |
| OD-002 | Destination taxonomy freeze | Existing vs proposed taxonomy; folder boundaries; naming. |
| OD-003 | Identity-recognition privacy policy | Whether any person-identity assistance is allowed; confirmation requirements. |
| OD-004 | Hash algorithm and performance strategy | Provisional recommendation: SHA-256. |
| OD-005 | Database location and backup policy | SQLite + JSONL recommended; path and backup unset. |
| OD-006 | Snapshot / versioning readiness | Must be confirmed before any destructive live gate. |
| OD-007 | Pilot dataset selection | Representative copied corpus not yet approved. |
| OD-008 | Batch-size and stop thresholds | Defaults exist in examples only. |
| OD-009 | Copy-first versus move behavior per phase | Must be frozen before live batches. |
| OD-010 | Quarantine retention and future deletion policy | No permanent deletion in V1; retention window unset. |
| OD-011 | Mac mini temporary thumbnails / extracted text | Privacy decision required. |

## MAJOR

| ID | Decision | Notes |
| --- | --- | --- |
| OD-012 | Confirm Dogs / drone / CSV / identity-candidate rules | Handwritten transcriptions missing; examples are provisional. |
| OD-013 | Confirmed live structure vs intended structure | Distinguish known intended, confirmed live, unresolved assumptions. |
| OD-014 | Migration-control directory schema | Operations manual suggests `01_Inventory…08_Checkpoints`; assignment documents `00_Consolidation_Source`, `01_Migration_Manifests`, `02_Analysis_Reports`, `03_Copy_Logs`, `04_Comparison_Reports`, `05_Unresolved`, `configs`, `database`, `logs`. Merge into one canonical control schema. |
| OD-015 | Destination taxonomy edges and aliases | Ambiguous boundaries between vaults, media, personal, archive. |
| OD-016 | Adapter choice for NAS access | Local mount vs SMB vs NFS vs SSH/SFTP vs Synology API—justify per environment. |

## MINOR

| ID | Decision | Notes |
| --- | --- | --- |
| OD-017 | Report format defaults | Markdown vs CSV vs JSON packaging. |
| OD-018 | Alert wording | Exact Pushover phrasing. |
| OD-019 | Review console stack detail | FastAPI + React/Next vs simpler local UI—direction set, details open. |
| OD-020 | Project path `90_Project/nas-intelligence-platform` | Intended location concept; creation timing unset. |

## Required follow-up

1. Record operator answers in the affected policy/spec documents.
2. Reclassify provisional rules only after explicit confirmation.
3. Update this file’s status when each ID is resolved (Resolved / Won’t-do with rationale).
4. Independent auditor should treat unresolved BLOCKERs as live-migration blockers, not blueprint-population blockers, unless they create internal contradiction.
