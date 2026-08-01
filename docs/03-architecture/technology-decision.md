# Technology Decision

## Decision frame

Choose the smallest toolchain that supports approval gates, adapter boundaries, immutable evidence, fixture testing, and a future local review console—without copying Foundry’s stack or introducing unnecessary distributed complexity.

This document recommends direction for implementation, to be acted on only after a specific rung is authorized at gate G3 (`docs/05-governance/gate-model.md`). It authorizes nothing by itself — not dependency installation, not a Build Ladder, not implementation.

## Evaluated options

| Technology | Role | Recommendation | Rationale |
| --- | --- | --- | --- |
| Python | Filesystem/data/media pipeline, CLI, workers | **Adopt** | Excellent ecosystem for hashing, metadata, media tooling, adapters, and orchestration on Mac mini |
| SQLite | Local operational state | **Adopt** | Queryable, portable, backup-friendly, sufficient for single-worker V1 |
| JSONL manifests | Portable inventory/plans/journals | **Adopt** | Append-friendly, diffable, easy to archive and audit |
| Pydantic (or equivalent) | Contracts / validation | **Adopt** | Typed boundaries between packages; matches `packages/contracts` |
| pytest | Unit/integration/safety/acceptance | **Adopt** | Standard, fixture-friendly, strong for idempotency/safety tests |
| FastAPI (or equivalent) | Future local API behind review console | **Accept if needed** | Thin API for read models + approval commands; not required on day one if CLI/reports suffice |
| React / Next.js | Review console UI | **Accept with caution** | Fine if needed; prefer simpler local UI if it meets IA with less weight |
| Task queue (Celery/RQ/etc.) | Async jobs | **Defer unless justified** | Single Mac mini worker + checkpoints may be enough for V1; add only for proven backpressure needs |
| Docker | Packaging | **Defer unless justified** | Direct host execution is simpler/safer for NAS mounts; use containers only if reproducibility demands it |
| Synology as compute host | Run heavy analysis on NAS | **Reject for V1** | Keep Synology as storage authority; avoid turning it into the analysis bottleneck |
| Raspberry Pi as primary worker | Heavy scan/hash/media | **Reject** | Sentinel only (ADR-008) |

## Recommended V1 stack sketch

```text
Mac mini worker (Python)
  ├── adapters (local/SMB/NFS/SFTP as configured)
  ├── inventory / metadata / hash / rules / planning / copy / validation packages
  ├── SQLite operational DB + JSONL manifests/journals
  ├── CLI (primary operator interface initially)
  └── optional local FastAPI for review console

Raspberry Pi Sentinel
  └── heartbeat / mounts / space / stall checks / Pushover / read-only status

Synology NAS
  └── shares, snapshots, authoritative bytes
```

## Explicit non-goals for stack choice

- No mandatory microservices mesh
- No cloud-required control plane
- No Foundry stack copy
- No production classifiers or model downloads in the blueprint phase
- No lockfiles until a rung is authorized at gate G3

## Consequences

- Operators can inspect state with ordinary SQLite/JSONL tooling.
- Package boundaries stay language-homogeneous (Python-first) for the engine.
- UI technology remains swappable because authorization lives in the backend/CLI, not the frontend (ADR-014).
