# Changelog

All notable foundation and architectural decisions for the NAS Intelligence Platform are recorded here.

## [1.1] — 2026-08-01

### Foundation 1.0 approved; Build Ladder generated

**Gate G1 — Foundation Approval: GRANTED** by the operator at commit `54ec3a8`.
**Gate G2 — Build Ladder Generation: GRANTED** separately, on the same date.

Both are recorded in the new `docs/05-governance/authorization-ledger.md`, which is now the
authoritative record of gate authorizations. Foundation approval is **not** implementation
authorization; G3 through G8 remain unauthorized.

### Added

- `docs/handoffs/build-ladder.md` — the Build Ladder: **79 rungs**, frozen and planning-only.
  70 of 79 complete before the system reads a single byte from the NAS.
- `docs/05-governance/authorization-ledger.md` — append-only gate authorization record.
- `scripts/validate_build_ladder.py` — 17 structural checks over the ladder.
- `prompts/rung-correction.md`, `prompts/architecture-drift-review.md`,
  `prompts/release-readiness-review.md`.
- `OD-023` (G4 plan promotability) and `OD-024` (symlink and hard-link reproduction scope),
  both arising from planning findings.

### Ordering defects corrected in the required-rung list

Generating the ladder against the specifications surfaced seven sequencing errors in the
required-rung list of handoff 003. Each correction is forced by a specific invariant:

- **Fault-injection harness moved from 34th to 7th.** A journal rung inspected without fault
  injection is inspected against the happy path only.
- **Taxonomy moved before the rule engine.** `VAL-TAXONOMY` is a rule-loader check, so a loader
  built first cannot satisfy its own specified check set.
- **Duplicate status split out and moved early.** `exact_duplicate_status` is pinned as stage 2
  of 8 in the evaluation order and is a rule predicate field.
- **Planner moved before approval binding.** An approval binds the content hash of a plan that
  must already be sealed.
- **Live adapter split.** Writing it is G3; measuring it against the NAS is the first real read
  and belongs at G4.
- **Preservation split** into plan-time profile resolution and post-copy comparison reporting.
- **Review console and Sentinel moved late.** Both have acceptance criteria that are negative
  claims, provable only once backend authorization exists.

### Planning findings

Thirty specification gaps and contradictions were found — 18 BLOCKER, 8 MAJOR, 3 MINOR, 1 NOTE.
They are recorded in the ladder's **Planning findings** section, each routed to change control or
to an operator decision, and each named in the **Blocked by** field of the rung it blocks. None is
resolved here; G2 does not authorize resolving them. Notable examples:

- The journal record vocabulary cannot reconstruct the projection, making the rebuild acceptance
  requirement unsatisfiable as written.
- The authoritative write protocol never captures the change tokens that the identity model
  requires before an atomic promote.
- `EvidenceBundle` is bound by the approval record and defined nowhere.
- A measured **destination** capability descriptor cannot be produced at G4, because measuring one
  requires a write and G4 authorizes none — so a G4 plan is structurally incapable of carrying one.

### Rungs added beyond the required list

Six rungs exist because the required list had no owner for work the specifications demand:
symbolic root registry, threshold governor, observability and redaction, incident and reason-code
surface, hostile-path fixtures, and the G4 readiness assembler. Three safety acceptance rows —
secret scanning, live-path guarding, and hostile-path testing — previously had no implementing rung.

### Changed

- `scripts/foundation_self_review.py` checks 19 and 20 now assert the *current* gate state: the
  ladder is generated and frozen, and G3–G8 remain unauthorized. They previously asserted the
  pre-approval state and would otherwise have been factually wrong.

### Unchanged

- No implementation code. No NAS access. No rung authorized. Live NAS execution prohibited.

## [1.0-rc2a] — 2026-08-01

### Verification correction

**VER-B001 — stale gate numbering in Foundation acceptance.** Independent verification of `34620db`
found that `docs/04-acceptance/foundation-acceptance.md` still referenced the superseded G0-based
gate scheme: it described Foundation acceptance as gate **G0**, which does not exist in the
canonical ladder, and assigned execution validation and fixture construction to **G2** (Build Ladder
Generation) rather than **G3** (Fixture-Only Implementation).

Cause: the ladder was renumbered from G0-based to G1-based during audit resolution.
`gate-model.md` was renumbered; `foundation-acceptance.md` had already been written against the old
scheme and was not re-checked. The file ended up internally mixed — earlier sections on the old
numbering, later-appended sections on the new — which is why the original self-review missed it.

- Six gate references corrected; "Passing G0 does not authorize G1" is now "Passing G1 does not
  authorize G2". The document was re-read in full against `gate-model.md`.
- All active documentation swept for unknown gate tokens and mismatched gate name/number pairs.
- `scripts/foundation_self_review.py` extended with four gate-mapping checks (25-28): canonical
  mapping reproduced exactly, no unknown gate token (this is what rejects G0), no mismatched
  name/slug binding, and activity phrases citing the gate that authorizes them.
- Checks 25-28 regression-tested in both directions: green on the corrected repository, and
  failing on the pre-fix file restored from `34620db` (26 on the G0 references, 28 on "fixture
  corpus at G2"). A check that cannot fail proves nothing.
- Verification finding and its known limits recorded in
  `docs/audits/foundation-resolution-verification.md`.

No specification content changed. Foundation 1.0 remains unapproved, the Build Ladder remains
ungenerated, and no NAS was accessed.

## [1.0-rc2] — 2026-07-31

### Audit resolution

Resolves the twelve findings of the independent Foundation audit of commit `840d72c8`. No finding was waived. Foundation 1.0 is **not** approved by this release; the repository is a release candidate awaiting independent verification of these resolutions.

**Blockers**

- **FND-B001** — Removed the circular Foundation acceptance gate. Foundation approval required all BLOCKER V1 acceptance requirements to pass, but 25 of them could only be verified by running software that was itself blocked until Foundation approval. Added `docs/05-governance/gate-model.md` defining eight independent authorization gates, and `docs/04-acceptance/foundation-acceptance.md` holding only documentary criteria. `v1-acceptance.md` now holds execution-verifiable criteria, each tagged with the gate it blocks, and explicitly blocks no Foundation approval.
- **FND-B002** — Replaced three incompatible rule vocabularies with one canonical contract at `config/schemas/classification-rule-set.schema.json` (JSON Schema draft 2020-12, unknown-field rejection at every level). Rewrote `rule-model.md` and the example rule set against it; recorded the domain model's field names as an entity projection rather than a second wire format.
- **FND-B003** — Provisional rules are now **structurally incapable** of automatic execution. The `enabled` switch is gone, `status` is the single activation control, and the schema forces every provisional rule to route to review, be advisory-only, require confirmation, and name the open decision blocking its promotion. The Dogs, drone, CSV, and identity policies remain the operator's decision (OD-012, OD-003).

**Major**

- **FND-M001** — Added `docs/02-specification/file-identity-model.md`: logical identity, evidence grades, a ternary change token in which indeterminate is never treated as equal, per-adapter identity evidence, and an eighteen-row stop/review table covering same-path replacement, concurrent modification, hard links, case-only and Unicode-normalization collisions, and network filesystem limits.
- **FND-M002** — Added `docs/02-specification/preservation-model.md`: a thirty-property preservation profile matrix by adapter class, content-class overlays for bundles, symlinks, sparse files, and hard-link sets, a capability-mismatch resolution protocol, and a comparison report schema. Corrected every document that implied hash equality proves preservation.
- **FND-M003** — Added `docs/02-specification/durability-and-recovery-model.md` and `ADR-016`: the journal is authoritative, SQLite is a derived rebuildable projection, with a numbered write protocol carrying a failure branch for every step, a durable intent record before any mutation, a seventeen-row crash-state table, a restart reconciliation algorithm, and an explicit statement of when the next mutation may begin.
- **FND-M004** — Added `docs/02-specification/approval-binding-model.md` and `ADR-017`: approvals bound to exact subject content, single-use, expiring, revocable, backend-evaluated on every attempt, with a twenty-five-step authorization algorithm and typed rejection codes. Closed the trust-boundary inversion in which the command envelope accepted an authorization status as inbound data.
- **FND-M005** — Removed `keep_first`, `merge`, and the vague `version` conflict mode. Separated rule conflict from destination collision, which had been conflated. Added priority bands, a specificity algorithm, deterministic tie-breaking, and a pinned prohibition on load-order-determined winners.

**Minor**

- **FND-m001** — Removed the duplicated classification event and reconciled the full event vocabulary; 89 events now match exactly across the domain and event models, with one emitter each.
- **FND-m002** — Replaced "read-only approval console" with "non-executing decision surface", and enumerated exactly which application-state commands it may submit.
- **FND-m003** — Separated severity from the gate it blocks; every open decision now carries an independent `blocks_gate` value.
- **FND-m004** — Reconciled inventory field obligations into one authoritative table with per-adapter conditions.

### Added

- `config/schemas/classification-rule-set.schema.json` — the canonical rule contract
- `scripts/validate_rule_config.py`, `scripts/generate_negative_rule_fixtures.py`
- `tests/fixtures/rules/negative/` — 47 rule sets that must fail validation, each with its expected reason
- `ADR-016`, `ADR-017`
- `OD-021` migration completeness criteria, `OD-022` operator authentication model
- Adapter, file-identity, approval-binding, and preservation-comparison rungs to the Build Ladder requirements

### Unchanged

- Implementation remains blocked; Build Ladder generation remains unauthorized; live NAS execution remains prohibited.

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
