# Source Reconciliation

Classifies major source concepts for the blueprint.

| Source concept | Classification | Rationale |
| --- | --- | --- |
| Read-only inventory first | ADOPT | Required by operations manual and assignment. |
| Copy-before-delete / copy-first pilot | ADOPT | Preserves originals while validating workflow. |
| Synology as protected storage authority | ADOPT | Matches operating model. |
| Mac mini as primary engine | ADOPT | Heavy processing off the NAS. |
| Raspberry Pi as Sentinel only | ADOPT | Monitor/alert; no destructive authority. |
| Dry-run default | ADOPT | Assignment non-negotiable. |
| Human approval for destructive actions | ADOPT | Safety floor. |
| Rule-driven explainable classification | ADOPT | Config-oriented policy model. |
| Exact duplicate hashing | ADOPT | Cryptographic equality required. |
| Engine lifecycle + phase mapping | ADOPT | Assignment §4. |
| Suggested migration-control tree (manual §5) | MERGE | Merge with assignment’s known control layout; record differences as open if unresolved. |
| Known `/volume1` share list | REFINE | Intended names preserved; live confirmation required (OD-001/013). |
| Dogs / drone / CSV / identity-candidate rules | REFINE | Provisional until operator confirms signals, destinations, privacy (OD-012/003). |
| Manual unresolved buckets | ADOPT | Unknown-* and Needs-Manual-Review preserved. |
| Near-duplicate deletion | REJECT | Explicitly excluded in V1. |
| Permanent deletion in V1 | REJECT | Excluded. |
| Unreviewed face identification | REJECT / FUTURE | Rejected as auto behavior; assistance may return via FR-003 after policy. |
| Broad live reorganization from first run | REJECT | Gated rollout only. |
| Cloud upload / broad external sharing | REJECT in V1 / FUTURE | FR-017. |
| Raspberry Pi as primary processing engine | REJECT | ADR-007/008. |
| Semantic search, vectors, curation, mobile, Foundry, Agent City, multi-NAS, storage optimization | FUTURE | Future Registry FR-001–FR-018. |
| Automated ingest watchers (unattended live) | FUTURE | FR-012; V1 only designs maintenance foundation. |
| Database location / hash algorithm / batch thresholds / quarantine retention / thumbnail privacy | UNRESOLVED | Open decisions OD-004–OD-011. |
| Taxonomy root freeze and live structure confirmation | UNRESOLVED | OD-002, OD-013. |
| Quarantine cleanup policy | MERGE | Combine retention, approval, and future deletion into one governed policy. |
