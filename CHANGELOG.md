# Changelog

All notable foundation and architectural decisions for the NAS Intelligence Platform are recorded here.

## [1.0-rc1] — 2026-07-31

### Foundation generation

- Populated complete blueprint repository for independent architecture and safety audit.
- Canonical product identity established as a safety-first file intelligence, migration, classification, organization, validation, and maintenance system.
- Documented controlled engine lifecycle and mapped it to high-level migration phases (Consolidate → Scaffold → Analyze → Organize → Validate/Archive → Normalize/Dedupe).
- Codified non-negotiable safety principles: read-only inventory, copy-before-delete, dry-run default, human approval for destructive actions, hash verification before retirement, protected-vault overwrite prohibition.
- Defined configuration-oriented classification rule model with stable IDs, priority, confidence thresholds, conflict resolution, and explainability requirements.
- Preserved known Synology share and migration-control intent while distinguishing intended structure from confirmed live structure.
- Established execution topology: Synology storage authority, Mac mini primary worker, Raspberry Pi Sentinel (monitor only).
- Recommended technology direction: Python pipeline, SQLite + JSONL manifests, Pydantic contracts, pytest, local API for review console, no mandatory Docker or heavy task queue in V1.
- Created acceptance criteria, operational playbooks, governance, migration traceability, Future Registry, and audit/build handoffs.
- Added non-production configuration examples under `config/` using synthetic fixture paths only.
- Implementation remains blocked; live NAS execution remains prohibited.

### Architectural decisions (ADR summary)

- Read-only inventory first
- Copy-before-delete
- Human approval for destructive actions
- Cryptographic hashes for exact duplicates
- SQLite plus JSONL manifests
- Rule-driven explainable classification
- Mac mini as primary worker
- Raspberry Pi Sentinel role
- Dry-run as default
- Pilot before live migration
- Protected-vault overwrite prohibition
- Adapter-based filesystem access
- Immutable audit log
- Frontend never authorizes filesystem mutation
- Separation of classification proposal from operation execution
