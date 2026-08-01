# Open Decisions

Unresolved decisions from the operations manual and foundation assignment. Do not treat unresolved items as approval to mutate live data.

## How to read this register

Every decision carries **two independent attributes** (audit finding FND-m003):

- **Severity** — `BLOCKER`, `MAJOR`, or `MINOR`. How bad the consequence is if the decision is made wrongly.
- **`blocks_gate`** — the earliest authorization gate the decision prevents. Values are defined in `docs/05-governance/gate-model.md`: `foundation`, `build_ladder`, `implementation`, `dry_run`, `pilot`, `live`, `retirement`, `migration_completion`.

These are **orthogonal**. A `BLOCKER` may carry `blocks_gate: live`; a `MINOR` may carry `blocks_gate: implementation`. An auditor evaluating gate *G* must consider exactly those decisions whose `blocks_gate` is *G* or earlier, regardless of severity, and must ignore the rest for the purpose of authorizing *G*.

A decision blocks its named gate and every later gate until it is resolved. **Re-confirm at** names a later gate where the answer must be revalidated even if already resolved.

## Register

| ID | Decision | Severity | `blocks_gate` | Re-confirm at | Notes |
| --- | --- | --- | --- | --- | --- |
| OD-001 | Exact Synology share roots in and out of scope | BLOCKER | `dry_run` | `live` | Intended `/volume1` names are documented; live confirmation missing. First live read requires confirmed roots. |
| OD-002 | Destination taxonomy freeze | BLOCKER | `dry_run` | `live` | Existing vs proposed taxonomy; folder boundaries; naming. Dry run emits destination proposals, so the taxonomy must be frozen first. |
| OD-003 | Identity-recognition privacy policy | BLOCKER | `dry_run` | `live` | Whether any person-identity assistance is allowed; confirmation requirements. Identity signals would be extracted from real media at first live read. The identity rule stays disabled until this resolves. |
| OD-004 | Hash algorithm and performance strategy | BLOCKER | `implementation` | — | Provisional recommendation: SHA-256. The algorithm is baked into contracts and stored fingerprints; changing it later invalidates them. |
| OD-005 | Database location and backup policy | BLOCKER | `dry_run` | `live` | SQLite + JSONL recommended; path and backup unset. Control-data storage must sit outside every recursively scanned source root. |
| OD-006 | Snapshot / versioning readiness | BLOCKER | `live` | `retirement` | Must be confirmed before any destructive live gate. |
| OD-007 | Pilot dataset selection | BLOCKER | `pilot` | — | Representative copied corpus not yet approved. |
| OD-008 | Batch-size and stop thresholds | BLOCKER | `pilot` | `live` | Defaults exist in examples only. Pilot needs stop thresholds; live needs them recalibrated for real volumes. |
| OD-009 | Copy-first versus move behavior per phase | BLOCKER | `live` | `retirement` | Must be frozen before live batches. |
| OD-010 | Quarantine retention and future deletion policy | BLOCKER | `retirement` | `migration_completion` | No permanent deletion in V1; retention window unset. |
| OD-011 | Mac mini temporary thumbnails / extracted text | BLOCKER | `dry_run` | — | Privacy decision required. Derived artifacts from real media begin at first live read. |
| OD-012 | Confirm Dogs / drone / CSV / identity-candidate rules | MAJOR | `dry_run` | — | Handwritten transcriptions missing; examples are provisional. The rule set must be frozen and confirmed before evaluation against real data. This is the operator decision referenced by audit finding FND-B003. |
| OD-013 | Confirmed live structure vs intended structure | MAJOR | `live` | `migration_completion` | Distinguish known intended, confirmed live, and unresolved assumptions. |
| OD-014 | Migration-control directory schema | MAJOR | `implementation` | `dry_run` | `docs/02-specification/taxonomy-model.md` names the assignment layout (`00_Consolidation_Source` … `logs`) as the canonical default and records the operations manual's `01_Inventory`…`08_Checkpoints` layout as a recorded alternate. The blueprint is therefore internally consistent; what remains is the operator's confirmation of the final names before control directories are created. |
| OD-015 | Destination taxonomy edges and aliases | MAJOR | `live` | — | Ambiguous boundaries between vaults, media, personal, archive. Only becomes destructive when writing to real destinations. |
| OD-016 | Adapter choice for NAS access | MAJOR | `dry_run` | — | Local mount vs SMB vs NFS vs SSH/SFTP vs Synology API — justify per environment. Implementation may proceed against fixtures without this: `docs/03-architecture/adapter-architecture.md` and `docs/02-specification/preservation-model.md` define adapter behavior as a capability contract, not a product choice. |
| OD-017 | Report format defaults | MINOR | `implementation` | — | Markdown vs CSV vs JSON packaging. |
| OD-018 | Alert wording | MINOR | `implementation` | `pilot` | Exact Pushover phrasing. |
| OD-019 | Review console stack detail | MINOR | `implementation` | — | FastAPI + React/Next vs simpler local UI — direction set, details open. |
| OD-020 | Project path `90_Project/nas-intelligence-platform` | MINOR | `live` | — | Intended location concept. Creating this path on the NAS is itself a live write, so it cannot precede the live gate. |
| OD-021 | Migration completeness criteria and residual-exception tolerance | MAJOR | `migration_completion` | — | Added during audit resolution. `V1-ACC-053` requires every in-scope item to reach a terminal disposition, and `prompts/migration-completion-audit.md` requires residual exceptions to be owned — but nothing yet defines how many unresolved or failed items are tolerable, or who owns them. |
| OD-022 | Operator authentication model for approval | MAJOR | `implementation` | `live` | Added during audit resolution. Resolving FND-M004 required binding every approval to an authenticated operator identity and session, but V1 scope never stated an operator authentication requirement — the Sentinel was the only component required to authenticate. `docs/02-specification/approval-binding-model.md` proposes a minimal local single-user model (loopback-only surfaces, a principal registry, approval-time re-authentication, session binding, backend-issued challenge). The operator decides whether to adopt that shape, tighten it, or scope it differently. |

## Gate coverage

| `blocks_gate` | Count | IDs |
| --- | --- | --- |
| `foundation` | 0 | — |
| `build_ladder` | 0 | — |
| `implementation` | 6 | OD-004, OD-014, OD-017, OD-018, OD-019, OD-022 |
| `dry_run` | 7 | OD-001, OD-002, OD-003, OD-005, OD-011, OD-012, OD-016 |
| `pilot` | 2 | OD-007, OD-008 |
| `live` | 5 | OD-006, OD-009, OD-013, OD-015, OD-020 |
| `retirement` | 1 | OD-010 |
| `migration_completion` | 1 | OD-021 |

**No open decision carries `blocks_gate: foundation`.** That is the intended state, and it is what makes Foundation approval reachable. None of these decisions creates an internal contradiction in the blueprint, and none is required in order to judge whether the specifications are complete, consistent, testable, and safe. They are all decisions about *operating on real data*, which no gate before G4 permits.

## Required follow-up

1. Record operator answers in the affected policy and specification documents.
2. Reclassify provisional rules only after explicit confirmation (OD-012). Until then provisional rules are structurally incapable of automatic execution — see `docs/02-specification/rule-model.md` and `config/schemas/classification-rule-set.schema.json`.
3. Update this register when each ID is resolved (Resolved / Won't-do with rationale), and re-confirm at the gate named in the **Re-confirm at** column.
4. Severity states consequence if the decision is wrong. `blocks_gate` states which gate the decision stops. They are independent and must not be conflated.
