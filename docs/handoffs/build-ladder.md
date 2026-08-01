# Build Ladder

Generated under gate **G2 — Build Ladder Generation**, authorized 2026-08-01 at commit `54ec3a8ba12f6e4b8a2ba9d2af423f259e8e5051`. See `docs/05-governance/authorization-ledger.md`.

## Status

> **This document is planning only. It is frozen and it authorizes nothing.**
>
> Implementation of rung *N* requires an explicit operator authorization for rung *N* at gate **G3**, recorded in the authorization ledger. **Authorization of rung *N* never authorizes rung *N+1*.**
>
> No rung below G4 may access, mount, scan, hash, or analyse any NAS path. Gate G4 is the first at which the system touches the real NAS, and then only to read.

## How to read a rung

Every rung carries the same field set, so a rung can be handed to an implementer, an inspector, or an operator without translation.

| Field | Meaning |
| --- | --- |
| **Gate** | The authorization gate under which this rung is performed. |
| **NAS access** | `none`, `read-only`, or `bounded-write`. Default and overwhelming majority: `none`. **This field describes access to NAS data paths only.** Writes to an approved local control-data root are governed separately by the gate model and are never NAS access. |
| **Objective** | What the rung is for, in one sentence. |
| **Why here** | The specific artifact or invariant that forces this position. Not "it makes sense" — the forcing dependency. |
| **Prerequisites** | Rungs that must be complete and inspected first. |
| **Blocked by** | Open decisions that must close before this rung may be implemented. |
| **Allowed work** | The precise scope. Anything outside it is a scope violation at inspection. |
| **Prohibited work** | What this rung must not touch, including work that looks adjacent. |
| **Specifications** | The specification documents this rung implements. |
| **ADRs** | The architecture decisions this rung realises. |
| **Acceptance** | Acceptance IDs this rung addresses. |
| **Files affected** | Anticipated files and packages, so unexpected changes are visible at inspection. |
| **Deliverables** | The artifacts that must exist when the rung is done. |
| **Positive tests** | Behaviour that must work. |
| **Negative tests** | Behaviour that must be **rejected**, and for the intended reason. |
| **Failure-injection tests** | Faults that must be survived or safely refused. `none` only where genuinely inapplicable. |
| **Operator validation** | What the operator personally checks before the rung counts as done. |
| **Evidence package** | Artifacts per `docs/05-governance/evidence-standard.md`. |
| **Rollback / recovery** | How to undo or recover from this rung. |
| **Stop conditions** | Conditions under which the implementer must halt rather than continue. |
| **Definition of Ready** | Entry criteria, per `docs/05-governance/definition-of-ready.md`. |
| **Definition of Done** | Exit criteria, per `docs/05-governance/definition-of-done.md`. |
| **Git boundary** | The expected shape of the commit. |
| **Enables** | Rungs that become reachable once this one is inspected and authorized. |

## Standing rules for every G3 rung

Every rung at gate G3 carries these without restating them:

- **Synthetic fixtures only.** No fixture may derive from live NAS data.
- **No NAS access.** The running system contacts no mount, share, or endpoint.
- **Path and secret policy applies**, per `docs/05-governance/path-policy.md`: secrets are forbidden everywhere with no exemption; literal live NAS paths are forbidden in executable code, configuration, positive fixtures, and generated artifacts, also with no exemption; approved inert documentation and the deliberately invalid negative fixtures may contain such patterns solely to document or prove rejection.
- **No authorization of the next rung.** Completing a rung produces evidence; it grants nothing.

Where a rung restates one of these, it is because that rung is the one most likely to be tempted.

## Gate distribution

| Gate | Rungs | Count | Character |
| --- | --- | --- | --- |
| G3 `implementation` | FBL-001 … FBL-070 | 70 | Fixture-only. **No NAS contact of any kind.** |
| G4 `dry_run` | FBL-071 … FBL-072 | 2 | First real NAS contact. **NAS paths strictly read-only.** Local writes confined to one approved control-data root, outside every NAS boundary. |
| G5 `pilot` | FBL-073 | 1 | Isolated copied corpus. Never the authoritative source. |
| G6 `live` | FBL-074 … FBL-075 | 2 | Bounded, approved copies. **No retirement.** |
| G7 `retirement` | FBL-076 | 1 | Verified source retirement. **Never deletion.** |
| G8 `migration_completion` | FBL-077 … FBL-079 | 3 | Reconciliation, completion, maintenance. |
| **Total** | | **79** | |

70 of 79 rungs — 89 percent of the ladder — complete before the system reads a single byte from the NAS.

## Deviations from the requested coverage order

The assignment listed 47 required topics "in safe dependency order". Seven were re-sequenced because the stated order is not implementable. Each correction is forced by a specific invariant, not by preference.

1. **Fault-injection harness moved much earlier** — listed 34th, placed at **FBL-007**. Crash-state recovery and interruption recovery cannot be *tested* without it. A journal rung inspected without fault injection is inspected against the happy path only, which is exactly the aspiration ADR-016 rejected. Retrofitting injection points later also places them where the code happens to be seam-able rather than where the protocol says they are.
2. **Taxonomy moved before the rule engine** — `VAL-TAXONOMY` is a *rule-loader* check requiring known taxonomy nodes, so a loader built first cannot satisfy its own specified check set. Taxonomy is **FBL-034**, the loader **FBL-035**.
3. **Duplicate handling split, with status moved much earlier.** `exact_duplicate_status` is pinned as stage 2 of 8 in the evaluation order and `duplicate_status` is a rule predicate field, so per-file status (**FBL-033**) must precede rule evaluation. Grouping and canonical recommendation stay late (**FBL-039**), after the review queue.
4. **Planner moved before approval binding.** An approval binds the content hash of a plan that must already exist and be sealed; the first approval fixture is a matched plan/approval pair. Planning is **FBL-041**, binding **FBL-045**.
5. **Live adapter split in two.** Writing the adapter is code and belongs at G3 (**FBL-065**, exercised against a local endpoint); *measuring it against the NAS* is the first real read and belongs at G4 (**FBL-071**). A measured descriptor cannot be produced under G3, and a hand-written one is invalid.
6. **Preservation split** into the profile-resolution contract (**FBL-040**, needed by the copy engine at plan time) and comparison reporting (**FBL-053**, needed by verification and retirement).
7. **Review console and Sentinel moved late** — **FBL-063** and **FBL-064**. Both have acceptance criteria that are *negative* claims, provable only once backend authorization exists and is the only thing that authorizes. Built early, each would pass vacuously, and the console's rendering needs would shape the records rather than the reverse.

Every one of the 47 topics is covered. The mapping is in **Coverage of the required topics** at the end of this document, along with six rungs added because the required list had no owner for work the specifications demand.
---

## Gate G3 — Fixture-Only Implementation

Every rung in this section is `NAS access: none`.

### Group 1 — Tooling, contracts, and harnesses

### FBL-001 — Repository tooling, evidence emitter, and CI safety guards

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Reproducible toolchain, one test entry point, a hashed evidence-package emitter, and a **class-aware** path guard enforcing `docs/05-governance/path-policy.md` — secrets forbidden everywhere, literal live paths forbidden in runtime surfaces, approved inert documentation and negative fixtures permitted to carry them. |
| Why here | Rung 1's own Definition of Done requires "the rung's evidence package is complete and hashed", so the emitter must exist to satisfy the rung that builds it. The path guard is the only mechanical barrier against an accidental pre-G4 live touch; every later rung inherits it. It must be **class-aware from the outset** — a guard that scans every file for every pattern cannot produce a green baseline on this repository. |
| Prerequisites | none |
| Blocked by | none |
| Allowed work | Project scaffold; dependency manifest and lockfile (this rung's authorization is what first makes a lockfile legal); lint, type-check, test runners; single entry point; evidence emitter producing stable ID, timestamp, source of truth, integrity marker, phase, conclusion; a **class-aware** path guard enforcing `docs/05-governance/path-policy.md`; wire in `validate_rule_config.py`, `foundation_self_review.py`, and `check_path_policy.py`. |
| Prohibited work | Any domain logic. Docker, task queues, or distributed infrastructure. **Widening the path policy, or adding any exemption not declared in `docs/05-governance/path-policy.md`.** A guard that scans every file for every pattern — that is the defect this rung exists to avoid. |
| Specifications | `evidence-standard.md`, `path-policy.md` |
| ADRs | ADR-007 |
| Acceptance | SAF-005, SAF-006, SAF-007 (policy half), V1-ACC-042 (repo half), PILOT-014 (emitter half) |
| Files affected | `pyproject.toml`, lockfile, `Makefile`, CI config, `scripts/`, `packages/observability/` |
| Deliverables | Reproducible env; evidence emitter; class-aware path guard enforcing `path-policy.md`; green baseline on the repository as it stands. |
| Positive tests | Fresh clone reaches green; emitter output satisfies the evidence standard's six fields. |
| Negative tests | All five path-policy tests pass in both directions: a literal live path planted in a Class B runtime surface fails; a credential fails even in a Class C path; the repository as it stands passes; the negative rule fixtures still contain literal live paths and are still rejected by the rule validator; and an attempted exemption for executable code is refused. A malformed rule set fails the pipeline non-zero. |
| Failure-injection tests | Missing dependency and missing lockfile fail loudly rather than degrading silently. |
| Operator validation | Operator runs the entry point on a clean machine and gets the same result. |
| Evidence package | Tool versions; lockfile hash; baseline output; CI guard demonstration. |
| Rollback / recovery | Revert; no persistent state. |
| Stop conditions | A dependency cannot be pinned reproducibly. |
| Definition of Ready | G3 authorization for FBL-001; ladder frozen. |
| Definition of Done | One command runs lint, types, tests, every validator, and the path guard, green — **including a green path-policy baseline on the repository exactly as it stands**, with its approved inert documentation and its deliberately invalid negative fixtures untouched. |
| Git boundary | One commit: tooling only. |
| Enables | FBL-002, FBL-006 |

### FBL-002 — Identifier, envelope, and state-machine contracts

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Opaque ID types, UTC time type, digest type, and every documented lifecycle state machine as an executable transition table. |
| Why here | The lifecycle model states that a transition not listed is forbidden — enforceable only if the table is a data structure, not prose. Every entity contract references these states. Split from entity contracts to keep both reviewable. |
| Prerequisites | FBL-001 |
| Blocked by | **OD-004** (digest type and width) |
| Allowed work | ID/time/digest types; transition tables for file, run, scan, decision, plan, entry, approval, checkpoint; forbidden-transition assertions. |
| Prohibited work | Entity definitions. Persistence. |
| Specifications | `lifecycle-model.md`, `domain-model.md` |
| ADRs | ADR-015 |
| Acceptance | FND-ACC-005 (executable regression) |
| Files affected | `packages/contracts/` |
| Deliverables | Primitive types; transition tables. |
| Positive tests | Every documented transition is permitted. |
| Negative tests | Every undocumented transition is refused. A terminal state accepts no outgoing transition. |
| Failure-injection tests | none |
| Operator validation | Operator confirms the tables match the lifecycle model exactly. |
| Evidence package | Transition-table-to-specification diff. |
| Rollback / recovery | Revert. |
| Stop conditions | A documented transition graph is internally inconsistent. |
| Definition of Ready | FBL-001 inspected; OD-004 resolved. |
| Definition of Done | All state machines executable; forbidden transitions refused. |
| Git boundary | One commit in `packages/contracts/`. |
| Enables | FBL-003 |

### FBL-003 — Domain entity contracts

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Typed contracts for every domain entity, field-for-field, with the inventory field-obligation table enforced. |
| Why here | Every later rung produces or consumes these. Building a consumer first would fix a shape the domain model does not sanction. |
| Prerequisites | FBL-002 |
| Blocked by | OD-004; **PF-04, PF-05, PF-07, PF-08, PF-11** (missing entities and fields — see Planning findings) |
| Allowed work | All documented entities; the 41-field inventory obligation table including adapter-conditional obligations; `content_identity_state` with its five values. |
| Prohibited work | Persistence. Business logic. **Inventing any field the specification does not define** — a missing field is a planning finding, not an implementation decision. |
| Specifications | `domain-model.md`, `inventory-model.md` |
| ADRs | ADR-015 |
| Acceptance | FND-ACC-001, FND-ACC-004, V1-ACC-002, V1-ACC-003 |
| Files affected | `packages/contracts/` |
| Deliverables | Typed entities; obligation metadata. |
| Positive tests | Every entity constructs with valid input. |
| Negative tests | Required field omitted is rejected. A nullable field set to `null` or `0` where the adapter cannot supply it is **rejected** — only explicit `unavailable` is accepted. Undocumented state rejected. |
| Failure-injection tests | none |
| Operator validation | Operator confirms the entity list matches the domain model with nothing added. |
| Evidence package | Entity-to-specification cross-reference. |
| Rollback / recovery | Revert. |
| Stop conditions | An entity cannot be represented without inventing a field. |
| Definition of Ready | FBL-002 inspected; the named planning findings resolved through change control. |
| Definition of Done | All entities typed; obligation table enforced; no extra fields. |
| Git boundary | One commit in `packages/contracts/`. |
| Enables | FBL-004|

### FBL-004 — Command and event contracts

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The command envelope — with `validation_status`, `authorization_status`, `approval_state`, and `actor` server-computed only — and the 89-name event vocabulary with one emitter each. |
| Why here | The trust-boundary inversion closed by FND-M004 lives in the envelope. Building it permissively means every later consumer inherits the hole. |
| Prerequisites | FBL-003 |
| Blocked by | **PF-06** (approval state machine has no event vocabulary) |
| Allowed work | Command registry; envelope with mandatory dedup key, correlation and causation ids; rejection of client-asserted authorization fields; actor derived from session; 89 events; emitter map. |
| Prohibited work | Handling commands. Authorization logic. Emitting or persisting events. |
| Specifications | `command-model.md`, `event-model.md` |
| ADRs | ADR-014, ADR-015 |
| Acceptance | FND-ACC-002, FND-ACC-003, V1-ACC-038 (envelope half) |
| Files affected | `packages/contracts/` |
| Deliverables | Command registry; envelope; event registry; emitter map. |
| Positive tests | Every documented command and event constructs; symmetric difference against `event-model.md` is empty. |
| Negative tests | A command carrying `authorization_status` is **rejected** with `APR-E25`, not ignored — likewise `validation_status`, `approval_state`, payload `actor`. Missing dedup key rejected. `ClassificationProposed` and `InventoryCheckpointWritten` rejected. Two emitters for one event rejected. |
| Failure-injection tests | none |
| Operator validation | Operator confirms a forged authorization field produces a rejection, not a silent drop. |
| Evidence package | Rejection-code matrix; event parity diff. |
| Rollback / recovery | Revert. |
| Stop conditions | The envelope cannot reject a client-asserted field without breaking a documented caller. |
| Definition of Ready | FBL-003 inspected; PF-06 resolved. |
| Definition of Done | Client-asserted fields rejected; 89 events with one emitter each. |
| Git boundary | One commit in `packages/contracts/`. |
| Enables | FBL-005|

### FBL-005 — Journal record contracts and the reason-code registry

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Journal record envelope, record-type registry, canonical serialization, digest function, `operation_id` derivation, and the single machine-readable registry of HALT, `APR-E*`, `VAL-*`, and `STOP-*` codes. |
| Why here | These are **pure functions with no I/O** and must be frozen before a writer exists: changing canonicalization later invalidates every chain already written. Journal records are authoritative; events are authoritative for nothing — so this is a separate contract from FBL-004. |
| Prerequisites | FBL-004 |
| Blocked by | OD-004 (chain digest); **PF-02** (record vocabulary cannot reconstruct the projection); **PF-05** (nonce ledger has no record type); **PF-09** (no canonical serialization rule for bound hashes) |
| Allowed work | Record envelope; record-type registry; canonical serialization; digest; `operation_id` and `idempotency_key` derivation; reason-code registry. |
| Prohibited work | Writing records. **Any mutable status field inside a record** — processing status is a projection value. |
| Specifications | `durability-and-recovery-model.md`, `approval-binding-model.md`, `rule-model.md`, `file-identity-model.md` |
| ADRs | ADR-013, ADR-016, ADR-004 |
| Acceptance | FND-ACC-043, FND-ACC-044, V1-ACC-046 (partial) |
| Files affected | `packages/persistence/`, `packages/contracts/` |
| Deliverables | Record contracts; canonical serializer; reason-code registry. |
| Positive tests | Canonical serialization is stable across dict ordering, Unicode form, and platform. `operation_id` is identical across process restarts. |
| Negative tests | A record carrying `write_state` is rejected. An unregistered record type is rejected. An unregistered reason code is rejected. |
| Failure-injection tests | none |
| Operator validation | Operator confirms every reason code in the four source documents appears in the registry. |
| Evidence package | Serialization stability report; code-registry coverage. |
| Rollback / recovery | Revert. |
| Stop conditions | Canonical serialization is not deterministic across platforms. |
| Definition of Ready | FBL-004 inspected; named planning findings resolved. |
| Definition of Done | Records, serializer, and registry frozen and independently reviewed. |
| Git boundary | One commit. |
| Enables | FBL-013 |

### FBL-006 — Fixture generator framework and expectations contract

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | A deterministic committed generator plus the `expectations` contract every fixture directory must satisfy. |
| Why here | Every later rung's Definition of Done is "passes on synthetic fixtures". A rung with no fixture framework cannot be inspected complete, and per-rung ad-hoc fixtures are how coverage silently diverges. |
| Prerequisites | FBL-001 |
| Blocked by | none |
| Allowed work | Generator framework; expectations schema naming acceptance IDs and assertions; determinism harness. |
| Prohibited work | **Any use of live NAS data.** Opaque blobs of unknown provenance. Secrets, private filenames, real share names. |
| Specifications | `tests/fixtures/README.md`, `testing-strategy.md` |
| ADRs | none — tooling and fixtures carry no architecture decision |
| Acceptance | FND-ACC-047, SAF-016 |
| Files affected | `tests/fixtures/`, `scripts/` |
| Deliverables | Generator framework; expectations contract. |
| Positive tests | Regeneration is byte-identical. |
| Negative tests | A fixture directory without expectations fails. The generator refuses a source path outside the fixture tree. |
| Failure-injection tests | Partial generation leaves no half-built corpus claimed complete. |
| Operator validation | Operator confirms no fixture derives from real data. |
| Evidence package | Corpus manifest with per-fixture hashes. |
| Rollback / recovery | Delete and regenerate. |
| Stop conditions | Determinism cannot be achieved. |
| Definition of Ready | FBL-001 inspected. |
| Definition of Done | Framework and contract exist; determinism proven. |
| Git boundary | One commit under `tests/fixtures/` plus generator. |
| Enables | FBL-007, FBL-011 |

### FBL-007 — Fault-injection adapter and process-kill harness

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Named injection points at every write-protocol step, six injection modes, declarable durability class, and a **real** process-kill harness. |
| Why here | **Moved far earlier than the requested topic order.** The journal's entire correctness claim is about crash behaviour; a journal inspected without fault injection is inspected against the happy path only. Retrofitting injection points later places them where the code is seam-able rather than where the protocol says they are. |
| Prerequisites | FBL-006 |
| Blocked by | none |
| Allowed work | Injecting adapter with points for protocol steps A1–F3; modes `fail_call`, `partial_write(n)`, `succeed_then_kill`, `fsync_error_once`, `lose_unflushed_data`, `rename_indeterminate`; declarable `strong`/`weak`/`unknown`; real SIGKILL harness. |
| Prohibited work | Simulating process death in-process. Any real NAS path. |
| Specifications | `durability-and-recovery-model.md`, `tests/fixtures/README.md` |
| ADRs | ADR-012 |
| Acceptance | Enables V1-ACC-045, V1-ACC-046, V1-ACC-036 |
| Files affected | `tests/fixtures/durability/`, `packages/adapters/` |
| Deliverables | Injecting adapter; kill harness; durability-class declaration. |
| Positive tests | Each mode produces its documented effect at each named point. |
| Negative tests | An injection point named in the protocol but absent from the harness fails the rung. |
| Failure-injection tests | The harness itself survives being killed. |
| Operator validation | Operator confirms process death is real, not simulated. |
| Evidence package | Injection-point-to-protocol-step coverage matrix. |
| Rollback / recovery | Revert; sandboxed only. |
| Stop conditions | `fsync_error_once` semantics — reported once, dirty pages discarded — cannot be emulated. |
| Definition of Ready | FBL-006 inspected. |
| Definition of Done | Every protocol step has an injection point; all six modes work; kill is real. |
| Git boundary | One commit. |
| Enables | FBL-013, FBL-048 |

### FBL-008 — Adapter capability contract

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The adapter interface and `AdapterCapabilityDescriptor` type, constructible **only** by a characterization run. |
| Why here | This is what makes OD-016 deferrable. Every filesystem-touching rung depends on it, and a hand-written descriptor is invalid — so the type must be impossible to hand-build, a decision made here or never. |
| Prerequisites | FBL-003 |
| Blocked by | **PF-04** (no domain entity, lifecycle, or persistence home for the descriptor) |
| Allowed work | Adapter interface; descriptor type covering identity grades, the 30 preservation properties, filename transparency, case and normalization sensitivity, timestamp resolution, access-time behaviour, path limits, per-volume durability class; validity rules; derived `max_achievable_identity_confidence` and `retirement_capable` flags. |
| Prohibited work | Implementing a concrete adapter. **Selecting a live adapter** — OD-016 is the operator's. Exporting a public descriptor constructor. |
| Specifications | `preservation-model.md`, `file-identity-model.md`, `adapter-architecture.md` |
| ADRs | ADR-012 |
| Acceptance | FND-ACC-048, V1-ACC-007 |
| Files affected | `packages/adapters/` |
| Deliverables | Interface; descriptor type; validity rules. |
| Positive tests | A descriptor from a characterization run validates. |
| Negative tests | A **hand-written** descriptor literal is rejected for missing attestation. An unverified capability defaults to `unknown` and is treated as `weak`, never as supported. |
| Failure-injection tests | none |
| Operator validation | Operator confirms no live adapter is named and OD-016 remains open; reviews the `retirement_capable` derivation, since choosing SFTP or a vendor API permanently waiver-gates G7. |
| Evidence package | Interface documentation; descriptor schema; the OD-016 consequence note. |
| Rollback / recovery | Revert. |
| Stop conditions | The interface cannot express a documented preservation property. |
| Definition of Ready | FBL-003 inspected; PF-04 resolved. |
| Definition of Done | Interface and descriptor exist; hand-written descriptors rejected; no adapter chosen. |
| Git boundary | One commit in `packages/adapters/`. |
| Enables | FBL-009 |

### FBL-009 — Adapter port and synthetic adapter

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The single narrow I/O boundary plus a synthetic adapter parameterised by capability grades. |
| Why here | Inventory, hashing, and copy all need a filesystem. Using the real local filesystem would bind them to macOS semantics and make weak-adapter behaviour untestable. |
| Prerequisites | FBL-008, FBL-007 |
| Blocked by | none |
| Allowed work | Adapter port; synthetic adapter emulating every grade combination in the identity table — local-posix, smb-like, nfs-like, sftp-like, vendor-api-like; simulated absence of object identity and link count; simulated case- and normalization-insensitivity. |
| Prohibited work | Any real NAS path or network protocol. Presenting simulated capabilities as measured ones for a real endpoint. |
| Specifications | `adapter-architecture.md`, `file-identity-model.md` |
| ADRs | ADR-012, ADR-001 |
| Acceptance | V1-ACC-007, V1-ACC-001 (read-only harness) |
| Files affected | `packages/adapters/` |
| Deliverables | Port; synthetic adapter with at least five profiles. |
| Positive tests | Each profile behaves as declared. |
| Negative tests | Requesting an undeclared capability fails rather than silently succeeding. Any path outside the sandbox is refused. |
| Failure-injection tests | Composed with FBL-007: each profile can fail fsync, report indeterminate rename, lose unflushed data. |
| Operator validation | Operator confirms the adapter cannot reach outside its sandbox. |
| Evidence package | Per-profile behaviour report. |
| Rollback / recovery | Revert. |
| Stop conditions | A documented adapter behaviour cannot be simulated — record as a G4 characterization gap. |
| Definition of Ready | FBL-008 and FBL-007 inspected. |
| Definition of Done | Port plus five profiles; sandbox enforced. |
| Git boundary | One commit in `packages/adapters/`. |
| Enables | FBL-010, FBL-012 |

### FBL-010 — Path normalization and raw-byte discipline

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Normalization profile `NP/1`, with `raw_path_bytes` canonical for all I/O and `normalized_path` an index key only. |
| Why here | This is a structural constraint on every later call site. Retrofitting it after inventory or copy exists means rewriting them. |
| Prerequisites | FBL-009 |
| Blocked by | none |
| Allowed work | `NP/1`: decode, NFC, full case folding for comparison form only, separator collapse, `.` resolution, `..` rejection, no symlink resolution; raw/normalized split. |
| Prohibited work | **Using `normalized_path` to open, read, or write any file.** Resolving symlinks. |
| Specifications | `file-identity-model.md`, `security-and-privacy.md` |
| ADRs | ADR-001 |
| Acceptance | V1-ACC-002, V1-ACC-003, FND-ACC-008 |
| Files affected | `packages/inventory/` |
| Deliverables | Normalizer; raw-byte I/O discipline. |
| Positive tests | Raw bytes survive a round trip verbatim; normalization is idempotent. |
| Negative tests | A `..` segment is rejected. Undecodable bytes mark `utf8_lossy`, route to review, and are **not** replaced. Any attempt to open by normalized path fails. |
| Failure-injection tests | none |
| Operator validation | Operator confirms raw bytes are canonical everywhere. |
| Evidence package | Normalization report over FX-24. |
| Rollback / recovery | Revert. |
| Stop conditions | Normalization is not idempotent. |
| Definition of Ready | FBL-009 inspected. |
| Definition of Done | `NP/1` implemented; raw bytes canonical; open-by-normalized-path impossible. |
| Git boundary | One commit in `packages/inventory/`. |
| Enables | FBL-011, FBL-021 |

### FBL-011 — Identity fixture corpus (FX-01 … FX-26)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Build the 26 identity, collision, concurrency, and encoding fixtures. |
| Why here | Consumers are identity, inventory, hashing, duplicates, and the copy engine. FX-05 and FX-19 are named regression tests for defects the audit found, so they must exist before the code that could reintroduce them. |
| Prerequisites | FBL-006, FBL-010 |
| Blocked by | none |
| Allowed work | FX-01 … FX-26 per the fixture README, each with expectations naming its acceptance IDs. |
| Prohibited work | Any live data. Any fixture without expectations. |
| Specifications | `tests/fixtures/README.md`, `file-identity-model.md` |
| ADRs | none — tooling and fixtures carry no architecture decision |
| Acceptance | FND-ACC-047 |
| Files affected | `tests/fixtures/identity/` |
| Deliverables | 26 fixtures with expectations. |
| Positive tests | Each fixture regenerates byte-identically. |
| Negative tests | A fixture whose expectations name an acceptance ID that does not exist fails. |
| Failure-injection tests | none |
| Operator validation | Operator spot-checks FX-05 and FX-19 against their documented defect. |
| Evidence package | Corpus manifest; expectations coverage. |
| Rollback / recovery | Regenerate. |
| Stop conditions | A fixture cannot be built synthetically — record as a platform limitation, never substitute real data. |
| Definition of Ready | FBL-006, FBL-010 inspected. |
| Definition of Done | FX-01 … FX-26 exist with expectations and regenerate identically. |
| Git boundary | One commit under `tests/fixtures/identity/`. |
| Enables | FBL-012|

### FBL-012 — Adapter characterization suite (FX-27 … FX-30)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The characterization run that emits the **only** valid capability descriptors, plus the drift and remount fixtures. |
| Why here | A descriptor is valid only if produced by this run. Nothing capability-conditional — collision evaluation, identity confidence, preservation profiles — may be implemented before this produces real output. |
| Prerequisites | FBL-011, FBL-009 |
| Blocked by | **OD-004** (the run emits hashed evidence and a generator manifest) |
| Allowed work | FX-27 exercising P01–P30 plus the NFD write/read-back round trip and the durability self-test; FX-28 mismatch; FX-29 drift; FX-30 connection loss. |
| Prohibited work | Emitting a descriptor by any other path. Any real endpoint. |
| Specifications | `preservation-model.md`, `file-identity-model.md` |
| ADRs | ADR-012 |
| Acceptance | V1-ACC-007, PILOT-019 (fixture half) |
| Files affected | `tests/fixtures/adapters/` |
| Deliverables | Characterization suite; measured descriptors per synthetic profile. |
| Positive tests | Each profile yields a complete descriptor with attestation evidence. |
| Negative tests | An unmeasured property is recorded `unsupported_reported`, never assumed supported. A descriptor missing the round-trip result is invalid. |
| Failure-injection tests | FX-29 descriptor drift; FX-30 volume identifier change. |
| Operator validation | Operator reviews `retirement_capable` per profile before OD-016 is decided. |
| Evidence package | Measured descriptors; attestation records. |
| Rollback / recovery | Re-run characterization. |
| Stop conditions | The suite cannot measure a property the profile matrix requires. |
| Definition of Ready | FBL-011, FBL-009 inspected; OD-004 resolved. |
| Definition of Done | FX-27 … FX-30 exist; descriptors produced only by the run. |
| Git boundary | One commit under `tests/fixtures/adapters/`. |
| Enables | FBL-022, FBL-040|
### Group 2 — Durable persistence

### FBL-013 — Journal writer and durability barriers

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Append + chain + the barrier primitive for a single segment, implementing B-INTENT, B-FINAL, B-OUTCOME, B-APPROVAL, B-CHECKPOINT. |
| Why here | **This rung is the hard gate on all mutation-capable code.** Gate G forbids any filesystem mutation before a durable intent record, so no copy engine may precede it. Writer before reader, because the reader's fixtures are writer output. |
| Prerequisites | FBL-005, FBL-007 |
| Blocked by | OD-005 (control-data location and durability class); **OD-014** (CONTROL layout — mitigable by config-driven fixture defaults, final names deferred) |
| Allowed work | Segment append; chain linking; the barrier — append, flush, fsync file, fsync directory on create, confirm; the five mandatory barriers; group commit for exactly the three permitted record types. |
| Prohibited work | Any filesystem mutation outside the journal. Group commit for any other record type. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-013, ADR-016, ADR-005 |
| Acceptance | V1-ACC-046 (partial), FND-ACC-043 |
| Files affected | `packages/persistence/` |
| Deliverables | Writer; barrier primitive. |
| Positive tests | Chain verifies; barriers complete before the next step is attempted. |
| Negative tests | Group commit refused for a record type outside the permitted three. A mutation attempted before B-INTENT completes fails. |
| Failure-injection tests | Append error — no mutation occurred, nothing to clean — versus fsync error — data loss, HALT, **never retried on the same descriptor, never inferred successful from a later fsync**. The two must take distinguishable branches. |
| Operator validation | Operator confirms a `strong` control volume is required and mutation is refused without it. |
| Evidence package | Barrier transcripts; the two error branches. |
| Rollback / recovery | Journal is disposable in fixture context. |
| Stop conditions | A `strong` durability class cannot be established. |
| Definition of Ready | FBL-005, FBL-007 inspected; OD-005 resolved. |
| Definition of Done | Writer with five barriers; error branches distinguishable. |
| Git boundary | One commit in `packages/persistence/`. |
| Enables | FBL-014 |

### FBL-014 — Journal segments, sealing, and the run lock

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Segment roll, index, seal, and the exclusive control-volume run lock. |
| Why here | One writer per run is a stated invariant; concurrent writers are forbidden. The segment-roll boundary must exist before crash row I15 can be tested. |
| Prerequisites | FBL-013 |
| Blocked by | none |
| Allowed work | Segment roll and index; `segment_sealed`; exclusive run lock. |
| Prohibited work | Multiple concurrent writers. Editing a rolled segment. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-013 |
| Acceptance | V1-ACC-046 |
| Files affected | `packages/persistence/` |
| Deliverables | Segment lifecycle; run lock. |
| Positive tests | Roll and seal produce a verifiable chain across the boundary. |
| Negative tests | A second writer is refused with `CONCURRENT_WRITER`. A segment index gap is detected. |
| Failure-injection tests | Kill mid-roll (row I15) — chain still verifies across the boundary. |
| Operator validation | Operator confirms two processes cannot both write. |
| Evidence package | Roll and lock transcripts. |
| Rollback / recovery | Disposable. |
| Stop conditions | Two writers can hold the lock. |
| Definition of Ready | FBL-013 inspected. |
| Definition of Done | Roll, seal, lock; I15 survivable. |
| Git boundary | One commit. |
| Enables | FBL-015 |

### FBL-015 — Journal fixture corpus

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Truncation, corruption, gap, duplicate, splice, reorder, unsealed-checkpoint, and unsealed-roll fixtures, plus the golden journal and its expected canonical database dump. |
| Why here | The reader's correctness is entirely about these cases. The golden-journal pair is the only construct that gives the rebuild requirement a failure signal. |
| Prerequisites | FBL-014, FBL-006 |
| Blocked by | none |
| Allowed work | All fixture families in the journal section of the fixture README. |
| Prohibited work | Live data. |
| Specifications | `tests/fixtures/README.md` |
| ADRs | ADR-016 |
| Acceptance | Enables V1-ACC-046, V1-ACC-047 |
| Files affected | `tests/fixtures/journal/` |
| Deliverables | Journal fixtures; golden journal + expected dump. |
| Positive tests | Fixtures regenerate identically. |
| Negative tests | A fixture claiming corruption that still validates fails the rung. |
| Failure-injection tests | none |
| Operator validation | Operator confirms the golden pair is genuinely paired. |
| Evidence package | Fixture manifest. |
| Rollback / recovery | Regenerate. |
| Stop conditions | A corruption class cannot be constructed. |
| Definition of Ready | FBL-014 inspected. |
| Definition of Done | All families present with expectations. |
| Git boundary | One commit under `tests/fixtures/journal/`. |
| Enables | FBL-016 |

### FBL-016 — Journal reader, chain verifier, and corruption branches

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Read and verify the chain; discard a truncated tail with sidecar preservation; **HALT** on mid-file corruption. |
| Why here | Truncated tail and mid-file corruption are asymmetric and cannot be one predicate. Sealing requires chain verification, so this precedes checkpoints. |
| Prerequisites | FBL-015 |
| Blocked by | none |
| Allowed work | Segment enumeration; chain verification; truncated-tail handling with sidecar, truncate, and `recovery_truncated_tail`; mid-file corruption HALT. |
| Prohibited work | **Repairing or skipping a corrupt mid-file record.** Deleting discarded tail bytes. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-013, ADR-016 |
| Acceptance | V1-ACC-046 |
| Files affected | `packages/persistence/` |
| Deliverables | Reader; verifier; both branches. |
| Positive tests | A valid chain verifies from genesis. |
| Negative tests | Truncated tail at byte, mid-token, and mid-record offsets → discarded, sidecar preserved, discard recorded. Bit flip in payload, in record hash, and in predecessor link → HALT `JOURNAL_CHAIN_BROKEN`, no repair, no skip, segment preserved untouched. Sequence gap, duplicate, splice, reorder → detected. |
| Failure-injection tests | Kill during verification. |
| Operator validation | Operator confirms discarded bytes are never deleted. |
| Evidence package | Branch transcripts; sidecar artifacts. |
| Rollback / recovery | Disposable. |
| Stop conditions | Any corrupt mid-file record is silently skipped. |
| Definition of Ready | FBL-015 inspected. |
| Definition of Done | Both branches correct; all journal fixtures handled. |
| Git boundary | One commit. |
| Enables | FBL-017 |

### FBL-017 — SQLite projection and idempotent apply

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The derived projection with an applied cursor, idempotent apply, and a `PROJECTION_GAP` hard stop. |
| Why here | The projection schema is a function of the record vocabulary, never the reverse. Sealing later requires the projection advanced to an exact sequence, so it precedes checkpoints. |
| Prerequisites | FBL-016 |
| Blocked by | **PF-01** (`PROJECTION_UNAVAILABLE` contradicts journal-only authorization); **PF-02** (record vocabulary cannot reconstruct all projected tables) |
| Allowed work | Projection tables; cursor with `applied_through_seq` and `applied_chain_head`; idempotent apply; gap detection. |
| Prohibited work | Storing any fact not derivable from the journal. Treating a projection write as durable. Reporting projection failure as a data-safety event. |
| Specifications | `state-and-persistence.md`, `durability-and-recovery-model.md` |
| ADRs | ADR-005, ADR-016 |
| Acceptance | FND-ACC-043 |
| Files affected | `packages/persistence/` |
| Deliverables | Projection; apply loop; cursor. |
| Positive tests | Apply is idempotent. |
| Negative tests | Apply at or below cursor is a no-op. Apply beyond cursor + 1 is a hard stop. A projection ahead of the journal is discarded, not trusted. |
| Failure-injection tests | Row I12 — kill after outcome, before projection; stale projection is normal and non-alarming. |
| Operator validation | Operator confirms no fact lives only in the projection. |
| Evidence package | Cursor transcripts; gap-stop demonstration. |
| Rollback / recovery | Rebuild from journal. |
| Stop conditions | Any projected fact proves non-reconstructible. |
| Definition of Ready | FBL-016 inspected; PF-01 and PF-02 resolved. |
| Definition of Done | Projection derived, idempotent, gap-stopping. |
| Git boundary | One commit. |
| Enables | FBL-018 |

### FBL-018 — Replay and rebuild from genesis

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Full replay and byte-identical rebuild, proven against the golden journal. |
| Why here | Rebuildability is a *tested* property, not an aspiration — this is the rung that makes ADR-016 falsifiable. |
| Prerequisites | FBL-017, FBL-015 |
| Blocked by | PF-02 |
| Allowed work | Replay; delete-and-rebuild; golden-dump comparison. |
| Prohibited work | Replay that emits a command or authorizes anything. |
| Specifications | `durability-and-recovery-model.md`, `state-and-persistence.md` |
| ADRs | ADR-005, ADR-016 |
| Acceptance | **V1-ACC-047** |
| Files affected | `packages/persistence/` |
| Deliverables | Replay; rebuild; comparison harness. |
| Positive tests | Delete the database, replay, byte-compare against the golden dump. Replay twice is identical. |
| Negative tests | Replay must authorize nothing and emit no command. |
| Failure-injection tests | Kill mid-replay; restart reproduces the same result. |
| Operator validation | Operator deletes the database and confirms identical rebuild. |
| Evidence package | Rebuild comparison hashes. |
| Rollback / recovery | Rebuild is itself the recovery. |
| Stop conditions | Rebuild is not byte-identical. |
| Definition of Ready | FBL-017 inspected. |
| Definition of Done | Byte-identical rebuild proven. |
| Git boundary | One commit. |
| Enables | FBL-019 |

### FBL-019 — Atomic checkpoints and sealing

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Checkpoints as two immutable journal records, where only a sealed checkpoint is a resume point. |
| Why here | Sealing requires **both** chain verification and the projection advanced to exactly that sequence — the one place a derived store gates an authoritative record, and easy to invert. |
| Prerequisites | FBL-018 |
| Blocked by | **PF-03** (sealing undefined for read-only scan checkpoints) |
| Allowed work | `checkpoint` and `checkpoint_sealed`; seal preconditions; projection of the four checkpoint states. |
| Prohibited work | A mutable checkpoint object. Resuming from an unsealed checkpoint. Self-tuning cadence. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-013, ADR-016 |
| Acceptance | FND-ACC-044 |
| Files affected | `packages/persistence/` |
| Deliverables | Checkpoint writer; seal protocol; state projection. |
| Positive tests | A sealed checkpoint is a valid resume point. |
| Negative tests | An unsealed checkpoint is ignored (row I14). Sealing with a non-terminal operation in scope is refused. Sealing with the projection behind is refused. |
| Failure-injection tests | Rows I13 and I14. |
| Operator validation | Operator confirms resume never selects an unsealed checkpoint. |
| Evidence package | Seal transcripts including interrupted cases. |
| Rollback / recovery | Resume from the previous sealed checkpoint. |
| Stop conditions | An unsealed checkpoint is ever selected. |
| Definition of Ready | FBL-018 inspected; PF-03 resolved. |
| Definition of Done | Two-record checkpoints; unsealed ignored. |
| Git boundary | One commit. |
| Enables | FBL-020 |

### FBL-020 — Restart reconciliation, journal side (R1–R8, R12–R14)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Run lock, adapter self-test hook, enumeration, chain verify, resume-point selection, operation and approval folds, projection compare-or-rebuild, verdict, fresh sealed checkpoint, and the approval re-evaluation seam. |
| Why here | No mutation-capable rung may run without a defined restart path. The filesystem-probing steps R9–R11 are deliberately **excluded** — they reason about temp files and rename indeterminacy that do not exist until the copy engine does. |
| Prerequisites | FBL-019, FBL-008 |
| Blocked by | none |
| Allowed work | R1–R8, R12, R13, R14. |
| Prohibited work | **R9, R10, R11** — those belong to the crash-matrix rungs. Resuming on `INCONSISTENT`. Reusing a cached authorization verdict across restart. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-016 |
| Acceptance | V1-ACC-036 (partial), V1-ACC-047 |
| Files affected | `packages/persistence/` |
| Deliverables | Reconciliation R1–R8, R12–R14; verdict. |
| Positive tests | Clean restart reaches `CONSISTENT`, seals a fresh checkpoint, and resumes. |
| Negative tests | `INCONSISTENT` **halts**. A second live writer is refused. Resume without a fresh sealed checkpoint is refused. A cached authorization verdict surviving restart fails. |
| Failure-injection tests | Row I16 — crash during recovery; recovery restarts from R1 and is idempotent. |
| Operator validation | Operator confirms no resume after `INCONSISTENT`. |
| Evidence package | Reconciliation transcripts for both verdicts. |
| Rollback / recovery | This rung is the recovery path. |
| Stop conditions | Reconciliation resumes on `INCONSISTENT`. |
| Definition of Ready | FBL-019, FBL-008 inspected. |
| Definition of Done | R1–R8, R12–R14 implemented; both verdicts exercised. |
| Git boundary | One commit. |
| Enables | FBL-021 |

### Group 3 — Identity, inventory, and content evidence

### FBL-021 — Symbolic root registry and path authority

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Resolve symbolic root references to fixture roots carrying `confirmed_live` / `intended_structure` / `unresolved_assumption`, and enforce approved-root and traversal checks. |
| Why here | Every destination template is relative to a symbolic root, and `VAL-ROOT-REF` is a rule-loader check. Nothing downstream can resolve a path until this exists. |
| Prerequisites | FBL-010, FBL-020 |
| Blocked by | **PF-12** (the symbolic root registry is asserted by the schema but does not exist) |
| Allowed work | Root registry; authority tags; approved-root and traversal enforcement. |
| Prohibited work | Any real root. Treating `unresolved_assumption` as an execution destination. |
| Specifications | `inventory-model.md`, `taxonomy-model.md`, `security-and-privacy.md` |
| ADRs | ADR-001 |
| Acceptance | V1-ACC-003 (partial), V1-ACC-042 |
| Files affected | `packages/inventory/`, `config/` |
| Deliverables | Root registry; authority resolution. |
| Positive tests | A symbolic ref resolves to a fixture root with its authority tag. |
| Negative tests | Literal path as a root ref rejected. Unresolvable ref rejected. Traversal outside an approved root rejected. `unresolved_assumption` used as an execution destination rejected. |
| Failure-injection tests | none |
| Operator validation | Operator confirms no live root is registrable. |
| Evidence package | Registry contents; rejection matrix. |
| Rollback / recovery | Revert. |
| Stop conditions | The registry cannot express an authority tag. |
| Definition of Ready | FBL-010, FBL-020 inspected; PF-12 resolved. |
| Definition of Done | Registry with authority tags; traversal enforced. |
| Git boundary | One commit. |
| Enables | FBL-022, FBL-034 |

### FBL-022 — Collision detection and classification

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Classify `case_only`, `normalization`, and `confusable` collisions, evaluated against the **destination's** measured sensitivity. |
| Why here | **The first rung that cannot be built without a measured descriptor** — collision risk is a function of destination case and normalization sensitivity, which exist only as measured fields. |
| Prerequisites | FBL-021, FBL-012 |
| Blocked by | none |
| Allowed work | Three collision classes, reported separately, evaluated against the destination descriptor. |
| Prohibited work | Evaluating against the source's sensitivity. Auto-resolving any class. |
| Specifications | `file-identity-model.md` |
| ADRs | ADR-011 |
| Acceptance | V1-ACC-005, V1-ACC-060, V1-ACC-061 |
| Files affected | `packages/inventory/` |
| Deliverables | Collision classifier. |
| Positive tests | FX-01, FX-02, FX-03 classify correctly. |
| Negative tests | Classification against the source's sensitivity fails. Any auto-resolution fails. |
| Failure-injection tests | none |
| Operator validation | Operator confirms destination sensitivity drives the decision. |
| Evidence package | Classification report over FX-01…FX-03. |
| Rollback / recovery | Revert. |
| Stop conditions | Classification requires an unmeasured property. |
| Definition of Ready | FBL-021, FBL-012 inspected. |
| Definition of Done | Three classes distinguished against measured destination capability. |
| Git boundary | One commit. |
| Enables | FBL-023 |

### FBL-023 — Identity keys, evidence grades, and logical file identity

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Mint `logical_file_id` once; compose `identity_confidence` as the **minimum** grade. |
| Why here | Grading `authoritative` requires a *measured* descriptor, so this follows characterization. Duplicates, preconditions, and retirement all rest on identity. |
| Prerequisites | FBL-022 |
| Blocked by | **PF-11** (`SourceRoot` lacks its identity-evidence fields) |
| Allowed work | Identity minting at `discovered → inventoried`, immutable thereafter, never derived from path; per-component evidence grades; minimum-composition. |
| Prohibited work | Deriving identity from path or hash. Reassigning an identity. Maximum or average composition. |
| Specifications | `file-identity-model.md` |
| ADRs | ADR-001, ADR-012 |
| Acceptance | V1-ACC-002, V1-ACC-005, FND-ACC-040 |
| Files affected | `packages/inventory/` |
| Deliverables | Identity minting; grading. |
| Positive tests | Stable identity across repeated scans. |
| Negative tests | Composition takes the minimum, never the maximum. Absent evidence records `unavailable`, never `0` or `null`. `authoritative` refused when the descriptor was not measured. |
| Failure-injection tests | Adapter without object identity caps confidence at `advisory`. |
| Operator validation | Operator confirms identity is never path-derived. |
| Evidence package | Identity report with grades. |
| Rollback / recovery | Revert. |
| Stop conditions | Identity can be derived from path. |
| Definition of Ready | FBL-022 inspected; PF-11 resolved. |
| Definition of Done | Identity minted once; minimum composition enforced. |
| Git boundary | One commit. |
| Enables | FBL-024 |

### FBL-024 — Change tokens and same-path replacement detection

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The ternary change token — `EQUAL`, `CHANGED`, `INDETERMINATE` — captured at the five journalled points, with same-path replacement detection. |
| Why here | Tokens are captured at journalled points, so the journal must exist. Where volume identity is unavailable, replacement detection is **mandatory**, so this cannot be deferred past inventory for any non-local adapter. |
| Prerequisites | FBL-023, FBL-020 |
| Blocked by | none |
| Allowed work | Ternary comparison; five capture points; replacement detection rules. |
| Prohibited work | **Any configuration flag that collapses `INDETERMINATE` into `EQUAL`.** |
| Specifications | `file-identity-model.md` |
| ADRs | ADR-001, ADR-016 |
| Acceptance | V1-ACC-006, V1-ACC-067, V1-ACC-032 (partial) |
| Files affected | `packages/inventory/` |
| Deliverables | Change token; comparison; replacement detection. |
| Positive tests | Unchanged fixture yields `EQUAL`. |
| Negative tests | **FX-19**: identical content, different object id → replacement, not equality. **FX-20**: coarse timestamp → `INDETERMINATE`. **FX-18**: replacement with different content → new identity, old marked stale, locked plan entry fails and never rebinds. No flag makes `INDETERMINATE` behave as `EQUAL`. |
| Failure-injection tests | Volume identifier change mid-run is not resumable. |
| Operator validation | Operator confirms the ternary is genuinely three-valued in all paths. |
| Evidence package | Token comparison matrix. |
| Rollback / recovery | Revert. |
| Stop conditions | `INDETERMINATE` is ever treated as `EQUAL`. |
| Definition of Ready | FBL-023, FBL-020 inspected. |
| Definition of Done | Ternary enforced; five capture points; replacement detected. |
| Git boundary | One commit. |
| Enables | FBL-025 |

### FBL-025 — Hashing and content identity state

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Hash reads bracketed by change tokens, producing the five-valued `content_identity_state`. |
| Why here | `hashed_stable` exists **only if** the token was equal immediately before and after the read. A hash produced before tokens exist has no defined state and therefore no legal consumer anywhere. |
| Prerequisites | FBL-024 |
| Blocked by | **OD-004**; **PF-10** (`HashRecord` cannot represent `source_recheck` scope or `unstable` status) |
| Allowed work | Streaming hash; bracket capture; the five states; bounded restabilization attempts. |
| Prohibited work | Publishing a hash whose bracket was not `EQUAL`. Using a non-`hashed_stable` hash as duplicate or verification evidence. |
| Specifications | `file-identity-model.md`, `inventory-model.md` |
| ADRs | **ADR-004** |
| Acceptance | V1-ACC-004, V1-ACC-006, V1-ACC-010, V1-ACC-011 |
| Files affected | `packages/inventory/`, `packages/metadata/` |
| Deliverables | Hashing; state machine; restabilization. |
| Positive tests | Stable read yields `hashed_stable`. |
| Negative tests | **FX-16**: modification during hashing → `unstable`, bounded retry, then `unresolved`; the unstable hash **never** enters a duplicate group or plan precondition. FX-15: unreadable → `unreadable`, reported not skipped. |
| Failure-injection tests | Read interrupted at multiple offsets. |
| Operator validation | Operator confirms an unstable hash cannot be consumed anywhere. |
| Evidence package | State-transition report. |
| Rollback / recovery | Revert. |
| Stop conditions | An unstable hash reaches a consumer. |
| Definition of Ready | FBL-024 inspected; OD-004 and PF-10 resolved. |
| Definition of Done | Five states; bracket enforced; unstable hashes quarantined from consumers. |
| Git boundary | One commit. |
| Enables | FBL-026, FBL-028 |
### FBL-026 — Read-only inventory

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Discover and register file records with the 41 canonical fields and adapter-conditional obligations, never mutating source. |
| Why here | If an item is not inventoried correctly it cannot be safely classified or executed; `discovered → inventoried` is the only entry into the lifecycle graph. |
| Prerequisites | FBL-025, FBL-021 |
| Blocked by | **PF-13** (V1-ACC-001's hash-based verification cannot detect the mutation it claims to exclude) |
| Allowed work | Traversal via the adapter port; record registration; obligation enforcement; error and unreadable reporting; resumable scan. |
| Prohibited work | Any write. Following symlinks. Choosing destinations. |
| Specifications | `inventory-model.md`, `domain-model.md` |
| ADRs | ADR-001 |
| Acceptance | V1-ACC-001, V1-ACC-002, V1-ACC-003, V1-ACC-004 |
| Files affected | `packages/inventory/` |
| Deliverables | Scanner; record registration; error reporting. |
| Positive tests | Repeat scan is deterministic; resumed scan creates no second identity. |
| Negative tests | Any write attempt during inventory fails the rung. FX-15 permission-denied reported, not skipped. FX-24 undecodable filename soft at inventory, blocked for operations. A nullable field asserted as `null`/`0` instead of `unavailable` fails. |
| Failure-injection tests | Interrupt mid-scan; resume without duplicate identities. |
| Operator validation | Operator confirms source property set is unchanged — comparing the preservation property set, not hashes alone. |
| Evidence package | Inventory manifest; exception log; determinism record. |
| Rollback / recovery | Delete fixture inventory; re-scan. |
| Stop conditions | Any source mutation is observed. |
| Definition of Ready | FBL-025, FBL-021 inspected; PF-13 resolved. |
| Definition of Done | Deterministic, resumable, non-mutating inventory with obligations enforced. |
| Git boundary | One commit. · **Enables** FBL-027, FBL-032 |

### FBL-027 — Inventory manifests and reconciliation totals

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Portable manifests and per-scan totals that later reconciliation balances against. |
| Why here | Totals must be captured at inventory time; reconstructing them later cannot prove completeness. |
| Prerequisites | FBL-026 |
| Blocked by | **OD-017** (report format) |
| Allowed work | JSONL manifests; counts and byte totals; coverage of unreadable and excluded items. |
| Prohibited work | Aggregating away exceptions. |
| Specifications | `inventory-model.md`, `data-architecture.md` |
| ADRs | ADR-001 |
| Acceptance | V1-ACC-002, V1-ACC-041 |
| Files affected | `packages/inventory/`, `packages/observability/` |
| Deliverables | Manifest writer; totals. |
| Positive tests | Totals equal the record count; manifest round-trips. |
| Negative tests | An exception hidden inside an aggregate fails. |
| Failure-injection tests | Interrupted manifest write leaves no partial claimed complete. |
| Operator validation | Operator reconciles totals by hand on a small fixture. |
| Evidence package | Manifest; totals report. |
| Rollback / recovery | Regenerate. |
| Stop conditions | Totals cannot be reconciled. |
| Definition of Ready | FBL-026 inspected; OD-017 resolved. |
| Definition of Done | Manifests and balancing totals. |
| Git boundary | One commit. · **Enables** FBL-068 |

### FBL-028 — Hard-link sets

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Form hard-link sets and exclude their members from duplicate grouping. |
| Why here | **Must precede duplicate grouping**, or that rung ships the exact defect FX-05 exists to regression-test: N links copied as N independent files. |
| Prerequisites | FBL-025 |
| Blocked by | **PF-07** (no `HardLinkSet` entity) |
| Allowed work | Set formation from volume identifier plus object id; exclusion from duplicate grouping; partial-retirement block. |
| Prohibited work | Asserting "no hard links" where link count is unavailable. |
| Specifications | `file-identity-model.md`, `duplicate-model.md` |
| ADRs | ADR-004, ADR-002 |
| Acceptance | V1-ACC-005, V1-ACC-010 (exclusion) |
| Files affected | `packages/inventory/` |
| Deliverables | Hard-link set formation. |
| Positive tests | FX-04 forms one set of three. |
| Negative tests | FX-05 yields exactly two logical members, not four. Unavailable link count records `hardlink_detection: unavailable`, never "none". Partial retirement blocked. |
| Failure-injection tests | Adapter without link count. |
| Operator validation | Operator confirms sets are never duplicate groups. |
| Evidence package | Set report over FX-04, FX-05. |
| Rollback / recovery | Revert. |
| Stop conditions | A set is reported as a duplicate group. |
| Definition of Ready | FBL-025 inspected; PF-07 resolved. |
| Definition of Done | Sets formed; duplicate exclusion proven. |
| Git boundary | One commit. · **Enables** FBL-033 |

### FBL-029 — Symlinks

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Inventory symlinks without following them; content identity is the hash of the target **string**. |
| Why here | Hashing the target silently converts a link into a copy of its referent, so this must land with hashing rather than after copy. |
| Prerequisites | FBL-025 |
| Blocked by | **PF-08** (no operation entry type can express a symlink) |
| Allowed work | Link inventory; target-string hashing; escape detection. |
| Prohibited work | Following links during enumeration, hashing, or size accounting. Replacing a link with a copy of its target. |
| Specifications | `file-identity-model.md`, `permission-model.md` |
| ADRs | ADR-001 |
| Acceptance | V1-ACC-005, V1-ACC-041 |
| Files affected | `packages/inventory/` |
| Deliverables | Symlink handling. |
| Positive tests | FX-06 in-root link inventoried, not followed. FX-08 dangling link inventoried without error, not classified unreadable. |
| Negative tests | FX-07 escaping link — any operation on it fails. Hashing the target instead of the target string fails. |
| Failure-injection tests | none |
| Operator validation | Operator confirms no link is silently resolved. |
| Evidence package | Symlink report over FX-06…FX-08. |
| Rollback / recovery | Revert. |
| Stop conditions | A link is followed anywhere. |
| Definition of Ready | FBL-025 inspected; PF-08 resolved. |
| Definition of Done | Links inventoried, never followed, target-string hashed. |
| Git boundary | One commit. · **Enables** FBL-031 |

### FBL-030 — Sparse, zero-byte, and very large files

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Record apparent and allocated size separately; prevent zero-byte redundancy claims; widen the stability window for long reads. |
| Why here | Apparent-only comparison cannot detect densification, and hash equality between a sparse source and a densified destination proves nothing about layout — the canonical illustration of the preservation rule. |
| Prerequisites | FBL-025 |
| Blocked by | none |
| Allowed work | Dual size capture; `is_sparse` derivation; zero-byte handling; streaming threshold. |
| Prohibited work | Treating apparent size as authoritative for layout. |
| Specifications | `preservation-model.md`, `file-identity-model.md` |
| ADRs | ADR-004 |
| Acceptance | V1-ACC-010, V1-ACC-044 |
| Files affected | `packages/inventory/` |
| Deliverables | Sparse detection; size accounting. |
| Positive tests | FX-09 records distinct apparent and allocated sizes. |
| Negative tests | FX-23 three zero-byte files produce no redundancy recommendation. A hash match alone does not set preservation-verified. |
| Failure-injection tests | Long read interrupted; stability window enforced. |
| Operator validation | Operator confirms densification would be visible. |
| Evidence package | Size accounting report. |
| Rollback / recovery | Revert. |
| Stop conditions | Allocated size is unavailable and treated as equal to apparent. |
| Definition of Ready | FBL-025 inspected. |
| Definition of Done | Dual sizes; zero-byte and long-read rules enforced. |
| Git boundary | One commit. · **Enables** FBL-040 |

### FBL-031 — Package bundles

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Treat a bundle as one logical file with a manifest digest, planned and copied all-or-nothing. |
| Why here | Without this, a bundle is shredded into member files and classified independently — a latent defect the audit found. Needs symlinks first, since bundles contain internal links. |
| Prerequisites | FBL-029 |
| Blocked by | **PF-14** (no atomic promote protocol for multi-member bundles) |
| Allowed work | Bundle detection; manifest digest over ordered member path, size, hash; single-unit classification and planning. |
| Prohibited work | Independently classifying, planning, or copying a member. Minimal representation of a bundle. |
| Specifications | `preservation-model.md` |
| ADRs | ADR-002 |
| Acceptance | V1-ACC-005, V1-ACC-041, V1-ACC-044 |
| Files affected | `packages/inventory/` |
| Deliverables | Bundle detection; manifest digest. |
| Positive tests | FX-10 is one logical file with a manifest digest. |
| Negative tests | A member independently classified or planned fails. FX-11 nested bundle — only the outermost is operable. A single member digest used as bundle identity fails. |
| Failure-injection tests | Partial bundle copy fails the entry and removes the partial destination. |
| Operator validation | Operator confirms a bundle is never shredded. |
| Evidence package | Bundle manifest digests. |
| Rollback / recovery | Revert. |
| Stop conditions | Bundle atomicity cannot be expressed without PF-14. |
| Definition of Ready | FBL-029 inspected; PF-14 resolved. |
| Definition of Done | Bundles as single units with manifest digests. |
| Git boundary | One commit. · **Enables** FBL-040 |

### FBL-032 — Metadata extraction

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Produce metadata records with explicit extraction-failure flags and declared provenance. |
| Why here | Rules evaluate against validated metadata inputs, and the predicate grammar requires a provenance-tagged evidence source. |
| Prerequisites | FBL-026 |
| Blocked by | **OD-011** (derived-artifact retention) for any thumbnail or extracted-text handling |
| Allowed work | MIME and extension; media, document, and structured-data metadata; failure flags; provenance tagging. |
| Prohibited work | Silent empty metadata on failure. Asserting AI-derived values with a deterministic provenance. Retaining derived artifacts beyond the rung's scope. |
| Specifications | `inventory-model.md`, `rule-model.md` |
| ADRs | ADR-001 |
| Acceptance | V1-ACC-020 (evidence half), V1-ACC-024 (partial) |
| Files affected | `packages/metadata/` |
| Deliverables | Extractors; failure flags; provenance. |
| Positive tests | Each supported type extracts with provenance. |
| Negative tests | Extraction failure yields an explicit flag, never an empty record. An AI-derived field tagged `media_metadata` is rejected. |
| Failure-injection tests | Corrupt media; truncated document. |
| Operator validation | Operator confirms no derived artifact is retained beyond policy. |
| Evidence package | Extraction report with provenance. |
| Rollback / recovery | Revert. |
| Stop conditions | Provenance cannot be attributed. |
| Definition of Ready | FBL-026 inspected; OD-011 resolved. |
| Definition of Done | Extraction with failure flags and provenance. |
| Git boundary | One commit. · **Enables** FBL-036 |

### FBL-033 — Duplicate-status evidence

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Emit per-file `duplicate_status` from `hashed_stable` equality, excluding hard-link sets and zero-byte files. **No groups, no canonical, no recommendation.** |
| Why here | **Moved earlier than the requested topic order.** `exact_duplicate_status` is pinned as stage 2 of 8 in the evaluation order, and `duplicate_status` is a rule predicate field — so it must precede rule evaluation, not follow it. |
| Prerequisites | FBL-028 |
| Blocked by | OD-004 |
| Allowed work | Per-file duplicate status; exclusions. |
| Prohibited work | Forming groups. Recommending a canonical. Any deletion or quarantine implication. |
| Specifications | `duplicate-model.md`, `rule-model.md` |
| ADRs | ADR-004 |
| Acceptance | V1-ACC-010 (partial), V1-ACC-011 |
| Files affected | `packages/classification/` |
| Deliverables | Duplicate status evidence. |
| Positive tests | Identical-hash fixtures share status. |
| Negative tests | Non-`hashed_stable` hash produces no status. Hard-link members excluded. Zero-byte files excluded. Same-name different-hash remain distinct. |
| Failure-injection tests | none |
| Operator validation | Operator confirms no grouping or recommendation occurs here. |
| Evidence package | Status report. |
| Rollback / recovery | Revert. |
| Stop conditions | Status is derived from an unstable hash. |
| Definition of Ready | FBL-028 inspected; OD-004 resolved. |
| Definition of Done | Status only; exclusions proven. |
| Git boundary | One commit. · **Enables** FBL-036 |

### Group 4 — Classification and taxonomy

### FBL-034 — Taxonomy registry and node authority

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Load a versioned taxonomy tree with authority, status, and path templates, and answer "is this an approved node?". |
| Why here | **Moved before the rule engine.** `VAL-TAXONOMY` is a *rule-loader* check requiring known taxonomy nodes, so a loader built first cannot satisfy its own specified check set. |
| Prerequisites | FBL-021 |
| Blocked by | **PF-15** (taxonomy has no machine-readable schema and the example contradicts the model); **OD-002**, **OD-014** for final names |
| Allowed work | Author a canonical taxonomy schema under `config/schemas/`; node loader; authority and status; template resolution. |
| Prohibited work | Freezing operator taxonomy content. Treating `unresolved_assumption` as an execution destination. |
| Specifications | `taxonomy-model.md` |
| ADRs | ADR-006, ADR-011 |
| Acceptance | V1-ACC-041, V1-ACC-022 (partial) |
| Files affected | `packages/classification/`, `config/schemas/` |
| Deliverables | Canonical taxonomy schema (new file under `config/schemas/`); node registry. |
| Positive tests | A conforming taxonomy loads; templates resolve. |
| Negative tests | `unresolved_assumption` as an execution destination rejected. Unapproved placeholder rejected. A node deleted without retirement rejected. A decision made under version N remains interpretable under N+1. |
| Failure-injection tests | none |
| Operator validation | Operator confirms taxonomy content remains theirs to freeze. |
| Evidence package | Schema; load report. |
| Rollback / recovery | Revert. |
| Stop conditions | The example and the model cannot be reconciled without deciding operator content. |
| Definition of Ready | FBL-021 inspected; PF-15 resolved. |
| Definition of Done | Schema authored; nodes load with authority. |
| Git boundary | One commit. · **Enables** FBL-035 |

### FBL-035 — Rule loader and static validation

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Port the existing validator into the engine: schema validation plus the nine loader checks; reject, never coerce. |
| Why here | The engine must never receive an unvalidated rule set, and the loader is the only ingress. `VAL-TAXONOMY` and `VAL-ROOT-REF` need FBL-034 and FBL-021 first. |
| Prerequisites | FBL-034 |
| Blocked by | **PF-16** (`VAL-POLICY-OPEN` makes OD closure break the shipped example) |
| Allowed work | Draft 2020-12 validation; all nine `VAL-*` checks; typed rule set. |
| Prohibited work | Evaluating rules. Coercing a bad value. Changing the schema — frozen Foundation content. |
| Specifications | `rule-model.md` |
| ADRs | ADR-006 |
| Acceptance | **V1-ACC-026**, FND-ACC-010…018 |
| Files affected | `packages/classification/`, `packages/validation/` |
| Deliverables | Loader; nine checks. |
| Positive tests | The canonical example loads. |
| Negative tests | **All 47 negative fixtures rejected for their documented reason**, notably provisional auto-approve, `keep_first`, `merge`, bare `version`, `load_order_significance` other than `none`, unknown field at every level, `environment: live`, `sensitive-identity-active`, `ai-evidence-executable`. `schema_version` ≠ 1 rejected, never coerced. |
| Failure-injection tests | Truncated YAML rejected without partial application. |
| Operator validation | Operator confirms no edit makes a provisional rule executable while still loading. |
| Evidence package | Validation report over positive and all 47 negatives. |
| Rollback / recovery | Revert. |
| Stop conditions | Any negative fixture is accepted. |
| Definition of Ready | FBL-034 inspected; PF-16 resolved. |
| Definition of Done | Positive loads; 47 negatives rejected for the intended reasons. |
| Git boundary | One commit. · **Enables** FBL-036 |

### FBL-036 — Rule evaluation, conflict resolution, and determinism

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The seven-step resolution algorithm, specificity scoring, band filter, outcome gate, conflict records, and re-evaluation idempotency. |
| Why here | Steps 3–5 are pure functions of rule content; the outcome gate and conflict record are the same function as selection and cannot be deferred. Needs duplicate status and metadata as inputs. |
| Prerequisites | FBL-035, FBL-033, FBL-032 |
| Blocked by | none |
| Allowed work | Band filter; priority filter; specificity; lexical tie-break; outcome gate; conflict records; idempotent re-evaluation. |
| Prohibited work | Any load-order influence. Content merging. Auto-canonicalising a multi-destination match. |
| Specifications | `rule-model.md` |
| ADRs | **ADR-006**, ADR-015 |
| Acceptance | **V1-ACC-020, 021, 022, 024, 025** |
| Files affected | `packages/classification/` |
| Deliverables | Evaluator; conflict records. |
| Positive tests | Documented precedence produces the documented winner. |
| Negative tests | **Shuffling the rules array and the file-load order produces byte-identical decisions.** Cross-band tie impossible by construction. Specificity inflation via added `any` branches does not raise the score. Multi-destination never auto-canonicalises. All-skip still reaches the fallback, never drops the file. Sub-threshold match leaves the contest but stays recorded. |
| Failure-injection tests | none |
| Operator validation | Operator shuffles a rule file and confirms identical output. |
| Evidence package | Determinism report; conflict records. |
| Rollback / recovery | Revert. |
| Stop conditions | Output changes under shuffle. |
| Definition of Ready | FBL-035, FBL-033, FBL-032 inspected. |
| Definition of Done | Seven steps; determinism proven under shuffle. |
| Git boundary | One commit. · **Enables** FBL-037 |

### FBL-037 — Classification proposals

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Emit decisions carrying rule ids, rule-set version, provenance-tagged evidence, confidence, explanation, and state. |
| Why here | A proposal is not an action; it must exist as a record before review or planning can consume it. |
| Prerequisites | FBL-036 |
| Blocked by | **PF-17** (decision lifecycle misplaces `rejected`) |
| Allowed work | Decision records; evidence chains; rendered explanations. |
| Prohibited work | Presenting an `advisory_only` destination as executable. |
| Specifications | `domain-model.md`, `rule-model.md` |
| ADRs | ADR-006, **ADR-015** |
| Acceptance | V1-ACC-020, V1-ACC-023, V1-ACC-024 |
| Files affected | `packages/classification/` |
| Deliverables | Decision records. |
| Positive tests | Every proposal carries all six required elements. |
| Negative tests | A proposal missing rule id, rule-set version, evidence, confidence, or explanation fails. An `advisory_only` destination marked executable fails. An untrusted AI candidate not flagged fails. |
| Failure-injection tests | none |
| Operator validation | Operator reads a proposal and understands it without chat history. |
| Evidence package | Proposal samples. |
| Rollback / recovery | Revert. |
| Stop conditions | A proposal is executable without approval. |
| Definition of Ready | FBL-036 inspected; PF-17 resolved. |
| Definition of Done | Decisions with full evidence and explanation. |
| Git boundary | One commit. · **Enables** FBL-038 |

### FBL-038 — Review queue and unresolved disposition

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Open, assign, resolve, and close review items carrying full candidate chains, and guarantee every file reaches a named disposition. |
| Why here | Conflicts and low-confidence outcomes have nowhere to go until this exists, and "no silent skip" is unprovable without it. |
| Prerequisites | FBL-037 |
| Blocked by | **PF-18** (no unresolved-queue entity); OD-017 |
| Allowed work | Review item lifecycle; candidate chains with elimination steps; unresolved disposition. |
| Prohibited work | Discarding a losing candidate. Letting an operator decision promote a rule or apply to another file. |
| Specifications | `rule-model.md`, `domain-model.md` |
| ADRs | ADR-003, ADR-015 |
| Acceptance | V1-ACC-021, V1-ACC-023, V1-ACC-037, V1-ACC-041 |
| Files affected | `packages/classification/` |
| Deliverables | Review queue; unresolved queue. |
| Positive tests | Conflicts and low-confidence items enter review. |
| Negative tests | A review item missing a losing candidate, its elimination step, or its explanation fails. A decision that mutates the rule, promotes it out of provisional, or applies to a second file fails. A file with no named disposition fails. |
| Failure-injection tests | none |
| Operator validation | Operator resolves a fixture conflict and confirms the rule is unchanged. |
| Evidence package | Review queue export; unresolved inventory. |
| Rollback / recovery | Revert. |
| Stop conditions | Any file reaches no disposition. |
| Definition of Ready | FBL-037 inspected; PF-18 resolved. |
| Definition of Done | Queues with full chains; every file dispositioned. |
| Git boundary | One commit. · **Enables** FBL-039, FBL-041 |

### FBL-039 — Duplicate grouping and canonical recommendation

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Form duplicate groups and recommend a canonical without hiding alternates or implying deletion. |
| Why here | Needs the review queue, because conflicting cases must enter review rather than be collapsed. Hard-link exclusion must already be in force. |
| Prerequisites | FBL-038, FBL-028 |
| Blocked by | none |
| Allowed work | Exact, near, and mixed groups; canonical recommendation; review routing. |
| Prohibited work | Auto-delete. Auto-quarantine. Erasing alternates. Treating near-duplicates as exact. |
| Specifications | `duplicate-model.md` |
| ADRs | ADR-004, ADR-002, ADR-011 |
| Acceptance | V1-ACC-010, V1-ACC-011, V1-ACC-012 |
| Files affected | `packages/classification/` |
| Deliverables | Grouping; recommendation. |
| Positive tests | Identical-hash fixtures group without deletion. |
| Negative tests | Canonical selection hiding alternates fails. Any auto-delete or auto-quarantine path fails. Near-duplicate treated as exact fails. FX-05 yields two members, not four. |
| Failure-injection tests | none |
| Operator validation | Operator confirms recommendation is advisory. |
| Evidence package | Duplicate group report. |
| Rollback / recovery | Revert. |
| Stop conditions | Any automatic deletion path exists. |
| Definition of Ready | FBL-038, FBL-028 inspected. |
| Definition of Done | Groups formed; canonical advisory; alternates preserved. |
| Git boundary | One commit. · **Enables** FBL-068 |
### Group 5 — Planning, approval, and authorization

### FBL-040 — Preservation profile resolution and capability-mismatch protocol

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Resolve the effective profile as base ∩ source descriptor ∩ destination descriptor ∩ content-class overlays; classify MM-0…MM-4; freeze into the plan. |
| Why here | The protocol runs at **plan time, never at execution time** — discovering a mismatch during execution voids the plan. Needs the overlays from bundles, links, and sparse handling. |
| Prerequisites | FBL-031, FBL-030, FBL-012 |
| Blocked by | **PF-19** (`OperationPlan` has no descriptor or profile fields) |
| Allowed work | Profile intersection; overlays; MM classification; freeze into plan. |
| Prohibited work | **Automatic downgrade of a required property.** Assumed descriptors. Running the protocol at execution time. |
| Specifications | `preservation-model.md` |
| ADRs | ADR-011, ADR-012, ADR-015 |
| Acceptance | V1-ACC-044, V1-ACC-033 (partial) |
| Files affected | `packages/planning/`, `packages/adapters/` |
| Deliverables | Profile resolver; MM classifier. |
| Positive tests | A matching pair yields MM-0 throughout. |
| Negative tests | FX-28 required property unsupported at destination → entries blocked, proceeding only with a waiver naming that property; a blanket waiver rejected. Automatic downgrade fails. |
| Failure-injection tests | Descriptor changed between resolution and freeze. |
| Operator validation | Operator reviews a mismatch and its waiver requirement. |
| Evidence package | Effective profile; mismatch classification. |
| Rollback / recovery | Revert. |
| Stop conditions | A required property is silently downgraded. |
| Definition of Ready | FBL-031, FBL-030, FBL-012 inspected; PF-19 resolved. |
| Definition of Done | Profile resolved and frozen; MM classified; no auto-downgrade. |
| Git boundary | One commit. · **Enables** FBL-041 |

### FBL-041 — Immutable operation plan construction

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Build plans and entries from approved decisions, seal a content hash, and version rather than mutate. |
| Why here | **Moved before approval binding.** An approval binds `subject_content_hash` of a plan that must already exist and be sealed; the first approval fixture is a matched plan/approval pair. |
| Prerequisites | FBL-040, FBL-038 |
| Blocked by | OD-004; PF-19 |
| Allowed work | Plan and entry construction; content hashing; sealing; versioning and supersede; precondition capture including change tokens. |
| Prohibited work | Lifting an `advisory_only` or `route_to_review` outcome into an entry. Mutating a plan after approval. |
| Specifications | `operation-model.md`, `domain-model.md` |
| ADRs | **ADR-009**, ADR-015 |
| Acceptance | **V1-ACC-030, V1-ACC-031** |
| Files affected | `packages/planning/` |
| Deliverables | Plan builder; sealing; versioning. |
| Positive tests | A plan seals with a stable content hash. |
| Negative tests | Post-approval mutation rejected, forcing a new version. An `advisory_only` outcome lifted into an entry fails. An entry whose source is not `hashed_stable` fails. FX-18 locked entry referencing a stale identity fails and **never rebinds**. |
| Failure-injection tests | Kill during sealing. |
| Operator validation | Operator confirms a sealed plan cannot be edited. |
| Evidence package | Plan artifacts with hashes. |
| Rollback / recovery | Supersede with a new version. |
| Stop conditions | A sealed plan can be mutated. |
| Definition of Ready | FBL-040, FBL-038 inspected. |
| Definition of Done | Plans sealed, versioned, immutable. |
| Git boundary | One commit. · **Enables** FBL-042 |

### FBL-042 — Plan-time collision and destination safety

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Evaluate collision policy per entry, force review for case and Unicode collisions, and block path-limit and protected-root violations at plan time. |
| Why here | Over-limit paths must be a plan-time block, not an execution-time surprise. Collision evaluation is explicitly plan-time, never rule-evaluation time. |
| Prerequisites | FBL-041, FBL-022 |
| Blocked by | none |
| Allowed work | Collision policy evaluation; case and Unicode review forcing; path-limit checks; protected-root blocks. |
| Prohibited work | Auto-versioning a case-only or normalization collision. Overwriting under any policy. |
| Specifications | `operation-model.md`, `rule-model.md`, `file-identity-model.md` |
| ADRs | **ADR-011** |
| Acceptance | **V1-ACC-033**, V1-ACC-030 |
| Files affected | `packages/planning/` |
| Deliverables | Collision evaluator; safety blocks. |
| Positive tests | A clean destination plans without collision. |
| Negative tests | FX-01 and FX-02 force review, never `versioned_suffix`. `versioned_suffix` that renames or replaces the **pre-existing** file fails. FX-25 over-limit blocks at plan time. `never_overwrite: false` is unrepresentable. |
| Failure-injection tests | none |
| Operator validation | Operator confirms no silent overwrite is expressible. |
| Evidence package | Collision report. |
| Rollback / recovery | Revert. |
| Stop conditions | Any overwrite path exists. |
| Definition of Ready | FBL-041, FBL-022 inspected. |
| Definition of Done | Collisions evaluated at plan time; overwrite impossible. |
| Git boundary | One commit. · **Enables** FBL-043 |

### FBL-043 — Dry-run planner

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Produce complete plans and reports against fixtures with **zero** filesystem mutation. |
| Why here | Dry-run is the default posture and must be provable on fixtures before any real root is confirmed. |
| Prerequisites | FBL-042 |
| Blocked by | OD-017 |
| Allowed work | Plan artifact generation; rule coverage, conflict, and unresolved reports; hashed evidence index. |
| Prohibited work | Any write outside control-data storage. |
| Specifications | `operation-model.md`, `dry-run-playbook.md` |
| ADRs | **ADR-009** |
| Acceptance | **V1-ACC-030** |
| Files affected | `packages/planning/`, `apps/cli/` |
| Deliverables | Dry-run planner; report set. |
| Positive tests | Destination tree unchanged after a dry run. |
| Negative tests | Any attempted destination write fails the rung. |
| Failure-injection tests | Interrupted planning leaves no partial plan claimed complete. |
| Operator validation | Operator inspects a plan and the destination tree. |
| Evidence package | Plan artifact; report set; evidence index. |
| Rollback / recovery | Delete artifacts. |
| Stop conditions | Any mutation is observed. |
| Definition of Ready | FBL-042 inspected; OD-017 resolved. |
| Definition of Done | Plans and reports with zero mutation. |
| Git boundary | One commit. · **Enables** FBL-044 |

### FBL-044 — Operator principal registry and approval-time authentication

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | A principal registry with authority classes, loopback-only surfaces, and a fresh authentication factor at the moment of approval. |
| Why here | **This is the single rung OD-022 hard-blocks.** Splitting it isolates that block so binding and evaluation can be designed against a declared identity seam. |
| Prerequisites | FBL-043 |
| Blocked by | **OD-022** (operator authentication model — the operator's decision, not the implementer's); **PF-20** (no authority-class vocabulary for five approval subject types) |
| Allowed work | Principal registry on control storage; authority classes; loopback binding; approval-time re-authentication; journalled auth events; session binding. |
| Prohibited work | **Choosing the authentication mechanism** — OD-022 is the operator's. Storing a passphrase rather than a verifier. Remote access. |
| Specifications | `approval-binding-model.md`, `permission-model.md` |
| ADRs | **ADR-003, ADR-017** |
| Acceptance | V1-ACC-038 (identity half) |
| Files affected | `packages/persistence/`, `apps/cli/` |
| Deliverables | Principal registry; auth event journalling. |
| Positive tests | A registered principal with the right class authenticates at approval time. |
| Negative tests | A non-loopback approval channel rejected. An open session without a fresh factor rejected. A committed passphrase fails. An authority-class change emits invalidation. |
| Failure-injection tests | Session revoked mid-approval. |
| Operator validation | **Operator confirms the authentication shape matches their OD-022 decision.** |
| Evidence package | Registry; auth event samples. |
| Rollback / recovery | Revert. |
| Stop conditions | OD-022 is unresolved — this rung cannot start. |
| Definition of Ready | FBL-043 inspected; **OD-022 resolved**; PF-20 resolved. |
| Definition of Done | Registry, loopback binding, approval-time factor, journalled events. |
| Git boundary | One commit. · **Enables** FBL-045 |

### FBL-045 — Approval request, minting, and content binding

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Backend-issued request id and nonce; binding to subject, evidence, rule-set, taxonomy, precondition, and descriptor hashes; scope and expiry; the sixteen invalidation triggers. |
| Why here | Binding requires a sealed plan to bind to, so it follows planning. |
| Prerequisites | FBL-044, FBL-041 |
| Blocked by | **PF-21** (`EvidenceBundle` is bound everywhere and defined nowhere); **PF-09** (no canonical serialization for bound hashes) |
| Allowed work | Request minting; nonce issuance; full binding; scope and expiry; IT-01…IT-16. |
| Prohibited work | Trusting any client-supplied hash as the value. Binding a version range or `latest`. |
| Specifications | `approval-binding-model.md` |
| ADRs | **ADR-017**, ADR-013 |
| Acceptance | V1-ACC-031, **V1-ACC-039** (partial) |
| Files affected | `packages/persistence/`, `packages/planning/` |
| Deliverables | Approval minting; binding; invalidation. |
| Positive tests | An approval binds every documented field. |
| Negative tests | Client-supplied `subject_content_hash`, `rule_set_hash`, or `taxonomy_hash` treated as the value fails. Client-supplied scope or approver identity rejected. A version range or `latest` is unrepresentable. Each of IT-01…IT-16 produces an invalidation record. A second approval for the same subject auto-invalidates the earlier. |
| Failure-injection tests | Kill between minting and the barrier. |
| Operator validation | Operator confirms an approval names an exact commit-like content hash. |
| Evidence package | Approval records; invalidation transcripts. |
| Rollback / recovery | Revoke and re-mint. |
| Stop conditions | Any bound hash is client-determined. |
| Definition of Ready | FBL-044, FBL-041 inspected; PF-21 and PF-09 resolved. |
| Definition of Done | Full binding; sixteen triggers. |
| Git boundary | One commit. · **Enables** FBL-046 |

### FBL-046 — Approval fixture corpus

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The eight approval fixture families, including the malicious-client and Sentinel-originated cases. |
| Why here | The authorization evaluator's correctness is entirely about these negatives; they must exist before it. |
| Prerequisites | FBL-045, FBL-006 |
| Blocked by | none |
| Allowed work | Matched and mutated plan/approval pairs; consumed replay; nonce replay; cross-run claim; expiry and clock regression; revocation before and mid-batch; drift; malicious payloads; Sentinel-originated attempt; per-dimension scope overrun. |
| Prohibited work | Live data. |
| Specifications | `tests/fixtures/README.md`, `approval-binding-model.md` |
| ADRs | ADR-017 |
| Acceptance | Enables V1-ACC-039, V1-ACC-052 |
| Files affected | `tests/fixtures/approval/` |
| Deliverables | Eight fixture families. |
| Positive tests | Fixtures regenerate identically. |
| Negative tests | A fixture claiming tampering that still validates fails. |
| Failure-injection tests | none |
| Operator validation | Operator confirms the Sentinel-originated fixture exists. |
| Evidence package | Fixture manifest. |
| Rollback / recovery | Regenerate. |
| Stop conditions | A family cannot be constructed. |
| Definition of Ready | FBL-045, FBL-006 inspected. |
| Definition of Done | Eight families with expectations. |
| Git boundary | One commit. · **Enables** FBL-047 |

### FBL-047 — Backend authorization evaluation, consumption, and anti-replay

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The ordered AUTHZ-01…AUTHZ-25 evaluation, per entry, per attempt, with two-phase claim, nonce ledger, and revocation checkpoints. |
| Why here | **Must precede the copy engine.** The consumption claim is appended before the first intent record of the batch, and no mutation may precede that intent record. |
| Prerequisites | FBL-046 |
| Blocked by | PF-01, PF-05 |
| Allowed work | Ordered short-circuit evaluation; two-phase claim and settle; nonce ledger; revocation checks at batch start, per entry, before finalize, and at each checkpoint. |
| Prohibited work | Caching a verdict across restart or any upstream change. Proceeding past any failed check. |
| Specifications | `approval-binding-model.md` |
| ADRs | **ADR-017, ADR-014** |
| Acceptance | **V1-ACC-032, 035, 038, 039**, V1-ACC-052 (refusal half) |
| Files affected | `packages/persistence/`, `packages/planning/` |
| Deliverables | AUTHZ evaluator; consumption; nonce ledger. |
| Positive tests | A valid approval authorizes exactly one entry, one attempt, one run. |
| Negative tests | Consumed replay, nonce replay, and cross-run claim each reject with their specific code. A payload carrying `authorization_status`, `validation_status`, `approval_state`, or a forged actor is **rejected and journalled as a safety event**. A Sentinel-originated attempt rejects `APR-E20`. Expired, not-yet-valid, and clock-regressed reject. Rule-set, taxonomy, and source drift reject. Scope overrun rejects per dimension. A cached verdict surviving restart fails. **Same-run resume is permitted while different-run resume rejects** — both directions required. |
| Failure-injection tests | Revocation mid-batch drives the in-flight operation to a terminal outcome with no dangling temp file. |
| Operator validation | Operator attempts a replay and sees the specific rejection code. |
| Evidence package | Rejection-code matrix; claim and settle transcripts. |
| Rollback / recovery | Revoke; re-mint. |
| Stop conditions | Any check can be bypassed. |
| Definition of Ready | FBL-046 inspected; PF-01 and PF-05 resolved. |
| Definition of Done | Twenty-five checks ordered; replay structurally impossible; resume preserved. |
| Git boundary | One commit. · **Enables** FBL-048 |

### Group 6 — Execution, verification, and recovery

### FBL-048 — Copy execution: token-gated atomic promote and content verification

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The ordered write protocol against synthetic adapters: intent, temp write, flush, verify, atomic promote, outcome. |
| Why here | The first mutation-capable rung. Everything it depends on — journal barriers, identity, tokens, hashing, plan, approval, authorization — now exists. |
| Prerequisites | FBL-047, FBL-013, FBL-007 |
| Blocked by | **PF-22** (the authoritative write protocol never captures the pre- and post-copy tokens that CM-4 requires) |
| Allowed work | Phases A–F; temp naming attributable by filename alone; independent re-read; atomic promote only after **both** hash equality and token equality. |
| Prohibited work | **Any mutation before the intent barrier completes.** Promoting on hash equality alone. Overwriting. |
| Specifications | `durability-and-recovery-model.md`, `operation-model.md`, `file-identity-model.md` |
| ADRs | ADR-002, ADR-009, ADR-011, ADR-016 |
| Acceptance | **V1-ACC-034, V1-ACC-032, V1-ACC-037** |
| Files affected | `packages/copy-engine/` |
| Deliverables | Write protocol; temp management; promote. |
| Positive tests | A clean copy verifies and promotes. |
| Negative tests | FX-17 source changed during copy → entry fails, partial destination removed, **never verified even when the destination hash matches the precondition**. FX-21 truncated read → fails, temp never promoted. FX-22 corrupt transfer → fails. A mutation attempted before the intent barrier fails. |
| Failure-injection tests | All six injection modes at every protocol step. |
| Operator validation | Operator confirms no promote occurs on hash equality alone. |
| Evidence package | Journal transcripts; verification results. |
| Rollback / recovery | Quarantine partials; re-attempt at a new attempt sequence. |
| Stop conditions | Any mutation precedes the intent barrier. |
| Definition of Ready | FBL-047, FBL-013, FBL-007 inspected; PF-22 resolved. |
| Definition of Done | Protocol implemented; token-gated promote proven. |
| Git boundary | One commit in `packages/copy-engine/`. · **Enables** FBL-049, FBL-052 |

### FBL-049 — Property reproduction (preservation-aware copy)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Reproduce timestamps, mode, ownership, ACLs, extended attributes, resource forks, link topology, and symlink-as-link per the frozen profile. |
| Why here | Separated from content atomicity: different failure modes, different fixtures. Content correctness must be proven before fidelity is layered on. |
| Prerequisites | FBL-048, FBL-040 |
| Blocked by | PF-08 (no entry type can express a link) |
| Allowed work | Property reproduction per the frozen effective profile; vault promotion of best-effort to required; hard-link set copy-then-link. |
| Prohibited work | Silently dropping an unsupported property. Replacing a link with a copy. |
| Specifications | `preservation-model.md` |
| ADRs | ADR-002, ADR-011 |
| Acceptance | V1-ACC-044 |
| Files affected | `packages/copy-engine/` |
| Deliverables | Property reproduction. |
| Positive tests | FX-14 permissions and ownership reproduced where supported. |
| Negative tests | FX-12 and FX-13 unsupported properties **counted and reported**, never silently dropped. FX-09 densification reported with a byte delta. Vault destination promotes best-effort to required. |
| Failure-injection tests | Destination refuses a property mid-copy. |
| Operator validation | Operator reviews an unsupported-property count. |
| Evidence package | Per-property reproduction report. |
| Rollback / recovery | Re-copy. |
| Stop conditions | A required property is silently dropped. |
| Definition of Ready | FBL-048, FBL-040 inspected. |
| Definition of Done | Properties reproduced or reported per profile. |
| Git boundary | One commit. · **Enables** FBL-053 |

### FBL-050 — Protected-vault enforcement

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Block overwrite into protected destinations by default, at plan time and again immediately before finalize. |
| Why here | Collision safety derives from an explicit pre-finalize existence check plus exclusive create, never from rename semantics — which are unavailable on weak adapters. |
| Prerequisites | FBL-048, FBL-042 |
| Blocked by | none |
| Allowed work | Vault classification; pre-finalize existence check; exclusive create; refusal. |
| Prohibited work | Relying on rename atomicity for collision safety. Any default overwrite. |
| Specifications | `taxonomy-model.md`, `operation-model.md` |
| ADRs | **ADR-011** |
| Acceptance | **V1-ACC-033**, PILOT-011 |
| Files affected | `packages/copy-engine/` |
| Deliverables | Vault enforcement. |
| Positive tests | A non-vault destination copies normally. |
| Negative tests | Vault overwrite refused by default. Late collision between plan and finalize refused, never overwritten. Foreign destination content never touched. |
| Failure-injection tests | Weak adapter with indeterminate rename. |
| Operator validation | Operator attempts a vault overwrite and sees refusal. |
| Evidence package | Refusal log. |
| Rollback / recovery | None needed — nothing was written. |
| Stop conditions | Any overwrite succeeds. |
| Definition of Ready | FBL-048, FBL-042 inspected. |
| Definition of Done | Overwrite impossible by default on all adapter classes. |
| Git boundary | One commit. · **Enables** FBL-052 |

### FBL-051 — Threshold and stop-condition governor

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Evaluate and **record** every documented stop condition and batch threshold. |
| Why here | **A gap no required rung owned.** Playbook stop conditions, pilot thresholds, and the `THRESHOLD_EXCEEDED` branch all depend on a governor nothing built. Definition of Done requires each dry-run stop condition to have been *evaluated*, not silently passed. |
| Prerequisites | FBL-048 |
| Blocked by | **OD-008** for real values; fixture defaults suffice at G3 |
| Allowed work | Threshold evaluation; stop-condition recording; batch pause. |
| Prohibited work | Silently passing a stop condition. Self-tuning thresholds. |
| Specifications | `operation-model.md`, `dry-run-playbook.md`, `pilot-run-playbook.md` |
| ADRs | ADR-009, ADR-010 |
| Acceptance | PILOT-008, LIVE-004 |
| Files affected | `packages/copy-engine/`, `packages/observability/` |
| Deliverables | Governor; evaluation records. |
| Positive tests | Each threshold triggers at its boundary. |
| Negative tests | A stop condition passed without an evaluation record fails. |
| Failure-injection tests | Threshold breached mid-batch pauses cleanly. |
| Operator validation | Operator reviews the evaluation record for a completed run. |
| Evidence package | Stop-condition evaluation record. |
| Rollback / recovery | Resume after operator review. |
| Stop conditions | Any condition is passed unevaluated. |
| Definition of Ready | FBL-048 inspected. |
| Definition of Done | Every documented condition evaluated and recorded. |
| Git boundary | One commit. · **Enables** FBL-066 |

### FBL-052 — Copy verification

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Independent post-operation verification recording content, token, and count evidence. |
| Why here | Verification must be independent of the executor; it consumes copy output and feeds preservation comparison. |
| Prerequisites | FBL-050, FBL-048 |
| Blocked by | **PF-23** (`VerificationResult` carries no preservation or token evidence) |
| Allowed work | Destination existence; hash comparison; token comparison; count reconciliation. |
| Prohibited work | Repairing a mismatch by guessing. Declaring verified on hash alone. |
| Specifications | `operation-model.md`, `domain-model.md` |
| ADRs | ADR-004, ADR-002 |
| Acceptance | **V1-ACC-034**, PILOT-004 |
| Files affected | `packages/validation/` |
| Deliverables | Verifier; verification records. |
| Positive tests | A good copy verifies. |
| Negative tests | Hash mismatch fails and halts the batch. Token mismatch fails even with a matching hash. A verification claiming success without token evidence fails. |
| Failure-injection tests | Corrupt destination post-copy. |
| Operator validation | Operator confirms verification is independent of the executor. |
| Evidence package | Verification report. |
| Rollback / recovery | Re-copy or quarantine. |
| Stop conditions | Verified is reachable on hash alone. |
| Definition of Ready | FBL-050, FBL-048 inspected; PF-23 resolved. |
| Definition of Done | Content, token, and count evidence recorded. |
| Git boundary | One commit. · **Enables** FBL-053 |

### FBL-053 — Preservation comparison report and retirement-eligibility evaluator

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Emit the comparison report with its verbatim disclaimer and compute `retirement_gate.eligible`. **Evaluator only — retirement executes at G7.** |
| Why here | Must precede any gate-readiness rung: it is a G5 entry criterion and a G7 entry criterion, and a report without the disclaimer is invalid evidence. |
| Prerequisites | FBL-052, FBL-049 |
| Blocked by | **PF-24** (no `PreservationComparisonReport` entity) |
| Allowed work | Report generation; per-property counts; mismatch classification; eligibility computation; verbatim disclaimer field. |
| Prohibited work | Executing retirement. Emitting a report without the disclaimer. Declaring eligible with an unwaived required-property mismatch. |
| Specifications | `preservation-model.md` |
| ADRs | ADR-002, ADR-003 |
| Acceptance | **V1-ACC-040** (accepted at G5), V1-ACC-044, PILOT-004, PILOT-014 |
| Files affected | `packages/validation/` |
| Deliverables | Report; eligibility evaluator. |
| Positive tests | A clean copy yields eligible with all required properties matched. |
| Negative tests | A report missing the disclaimer is invalid evidence. FX-12 unsupported extended attributes → **not eligible** without a property-naming waiver. A blanket waiver rejected. Hash match alone never sets eligible. |
| Failure-injection tests | none |
| Operator validation | Operator reads a report and understands it without chat history. |
| Evidence package | Comparison report. |
| Rollback / recovery | Regenerate. |
| Stop conditions | Eligible is reachable on hash alone. |
| Definition of Ready | FBL-052, FBL-049 inspected; PF-24 resolved. |
| Definition of Done | Report with disclaimer; eligibility correct. |
| Git boundary | One commit. · **Enables** FBL-062, FBL-076 |
### Group 7 — Crash conformance and recovery

### FBL-054 — Crash matrix, pre-finalize rows I0–I8

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Reproduce the documented outcome for every interruption before the rename. |
| Why here | These rows reason about temp files and verification, which do not exist until the copy engine does. They all resolve to "never adopt unproven bytes". |
| Prerequisites | FBL-053, FBL-020, FBL-007 |
| Blocked by | none |
| Allowed work | Recovery steps R9–R11 restricted to rows I0, I2–I8; adopt-versus-abandon decisions; quarantine of partials. |
| Prohibited work | **Adopting a temp file lacking its durable record** (rows I4, I5). Full-tree walks — the probe is bounded to non-terminal operations. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-016, ADR-002 |
| Acceptance | V1-ACC-045 (rows I0, I2–I8) |
| Files affected | `packages/persistence/`, `packages/copy-engine/` |
| Deliverables | Row handlers I0, I2–I8. |
| Positive tests | Rows I6, I7, I8 resume forward from a durable, verified temp. |
| Negative tests | Rows I4 and I5 — a temp that *looks* complete but lacks its durable record is **never adopted**, regardless of what the directory listing shows. Row I3 partial temp quarantined, destination confirmed absent. |
| Failure-injection tests | `succeed_then_kill` and `partial_write(n)` at each named point. |
| Operator validation | Operator confirms unproven bytes are re-copied rather than adopted. |
| Evidence package | Per-row recovery transcript. |
| Rollback / recovery | Re-attempt at a new attempt sequence. |
| Stop conditions | Any unproven temp is adopted. |
| Definition of Ready | FBL-053, FBL-020, FBL-007 inspected. |
| Definition of Done | Eight rows reproduce their documented outcome. |
| Git boundary | One commit. · **Enables** FBL-055 |

### FBL-055 — Crash matrix, indeterminate finalize rows I9–I11

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Probe-and-adopt, or quarantine-and-halt, for the rename window. |
| Why here | **Its own rung, deliberately.** Row I9 is the most dangerous window; branch (b) is the only crash row whose answer to "may another mutation begin" is *no*; and rows I9 and I10 must be handled identically by construction because the journal cannot distinguish them. It deserves an isolated review. |
| Prerequisites | FBL-054 |
| Blocked by | none |
| Allowed work | Four-branch resolution for I9; identical handling for I10; I11 post-finalize confirmation. |
| Prohibited work | Distinguishing I9 from I10. Adopting on anything weaker than a re-read hash match. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-016 |
| Acceptance | V1-ACC-045 (rows I9–I11) |
| Files affected | `packages/persistence/` |
| Deliverables | I9 four-branch handler; I10; I11. |
| Positive tests | Branch (a) destination exists and re-read matches → adopt, append finalize and committed. Branch (c) destination absent, temp verified → resume at the collision guard. Branch (d) both absent → abandon and retry. |
| Negative tests | **Branch (b)** destination exists but hash mismatches → quarantine, HALT `RECOVERY_HASH_MISMATCH`, **no further mutation until the operator clears it**. Row I11 post-finalize drift → HALT. Any attempt to treat I10 differently from I9 fails. |
| Failure-injection tests | `rename_indeterminate` across all four branches. |
| Operator validation | Operator walks branch (b) and confirms mutation stops. |
| Evidence package | Four-branch transcript. |
| Rollback / recovery | Operator-cleared after adjudication. |
| Stop conditions | Branch (b) permits a subsequent mutation. |
| Definition of Ready | FBL-054 inspected. |
| Definition of Done | Four branches correct; I9 and I10 identical. |
| Git boundary | One commit. · **Enables** FBL-056 |

### FBL-056 — Crash matrix I12–I16, orphan sweep, and reconciliation R9–R11

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Projection and checkpoint rows, the bounded filesystem probe, and the four temp-file classifications. |
| Why here | Completes the crash table and the reconciliation steps deliberately deferred from the journal-side rung. |
| Prerequisites | FBL-055 |
| Blocked by | none |
| Allowed work | Rows I12–I16; R9 bounded probe; R10 row application; R11 orphan sweep; the four temp classifications. |
| Prohibited work | **Permanently deleting any temp file** — quarantine is the disposal path in V1. Full-tree walks. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-016 |
| Acceptance | V1-ACC-045 (rows I12–I16), V1-ACC-047 |
| Files affected | `packages/persistence/` |
| Deliverables | Remaining rows; orphan sweep. |
| Positive tests | Row I12 stale projection is normal and non-alarming; row I13 replay skips terminal operations so no duplicate copy occurs. |
| Negative tests | An **unattributable artifact** in staging → HALT `UNATTRIBUTABLE_ARTIFACT`. Foreign destination content never touched and never overwritten. A temp file permanently deleted fails the rung. |
| Failure-injection tests | Kill during recovery (row I16) — recovery restarts from the beginning, never resumes. |
| Operator validation | Operator confirms no temp file is ever deleted. |
| Evidence package | Orphan sweep report; row transcripts. |
| Rollback / recovery | Quarantine inventory. |
| Stop conditions | Any temp file is permanently deleted. |
| Definition of Ready | FBL-055 inspected. |
| Definition of Done | All 17 rows covered across FBL-054…056; orphans quarantined. |
| Git boundary | One commit. · **Enables** FBL-057 |

### FBL-057 — Batch interruption and resume conformance

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Interrupt and resume at **every** documented interruption point without duplicate copies. |
| Why here | The integration rung over the three crash rungs — not a substitute for them. |
| Prerequisites | FBL-056 |
| Blocked by | none |
| Allowed work | End-to-end interrupt-and-resume across all 17 points; duplicate-copy assertions. |
| Prohibited work | Sampling a subset of interruption points. |
| Specifications | `durability-and-recovery-model.md` |
| ADRs | ADR-016, ADR-013 |
| Acceptance | **V1-ACC-036**, PILOT-012 |
| Files affected | `tests/integration/` |
| Deliverables | Conformance suite over all 17 points. |
| Positive tests | Resume completes the batch exactly once. |
| Negative tests | Any duplicate destination copy fails. A skipped interruption point fails the rung. |
| Failure-injection tests | All 17 points, all applicable modes. |
| Operator validation | Operator interrupts a fixture batch and confirms clean resume. |
| Evidence package | 17-point conformance matrix; destination inventory diff. |
| Rollback / recovery | Re-run. |
| Stop conditions | Any duplicate copy. |
| Definition of Ready | FBL-056 inspected. |
| Definition of Done | All 17 points pass with no duplication. |
| Git boundary | One commit. · **Enables** FBL-062 |

### Group 8 — Observability, safety, and operator surfaces

### FBL-058 — Observability and redaction

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Structured logs distinguishing dry-run from live, correlation identifiers, and path redaction. |
| Why here | **A gap no required rung owned**, leaving two BLOCKER acceptance rows unimplemented. Must precede any gate-readiness rung, because a dry-run evidence index is a log and artifact product. |
| Prerequisites | FBL-052 |
| Blocked by | OD-017 |
| Allowed work | Structured logging; correlation and causation propagation; mode labelling; redaction of sensitive paths. |
| Prohibited work | Logging credentials. Logging unredacted private filenames in alerts. Reading the projection where the journal is authoritative. |
| Specifications | `observability.md`, `security-and-privacy.md` |
| ADRs | ADR-016 |
| Acceptance | **V1-ACC-037, V1-ACC-042** (redaction half) |
| Files affected | `packages/observability/` |
| Deliverables | Logger; redaction; correlation propagation. |
| Positive tests | Failure state is queryable after injection; correlation links a command to its events. |
| Negative tests | A sensitive path appears unredacted → fails. A log claiming live mode during a dry run → fails. |
| Failure-injection tests | Inject a failure and query the resulting state. |
| Operator validation | Operator reviews redaction samples. |
| Evidence package | Redaction samples; error and audit export. |
| Rollback / recovery | Revert. |
| Stop conditions | Redaction cannot be verified. |
| Definition of Ready | FBL-052 inspected; OD-017 resolved. |
| Definition of Done | Structured, correlated, redacted logs. |
| Git boundary | One commit. · **Enables** FBL-059 |

### FBL-059 — Incident and reason-code surface

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Surface every HALT and rejection reason code as an inspectable incident record. |
| Why here | **A gap no required rung owned.** Roughly twenty HALT codes and twenty-six approval rejection codes would otherwise be untested strings, and the incident playbook's required evidence would have no producer. |
| Prerequisites | FBL-058, FBL-047 |
| Blocked by | none |
| Allowed work | Incident record type; reason-code surfacing; incident classes from the playbook. |
| Prohibited work | Authorizing any live change from an incident channel. Collapsing distinct codes into a generic error. |
| Specifications | `incident-response.md`, `durability-and-recovery-model.md`, `approval-binding-model.md` |
| ADRs | ADR-013 |
| Acceptance | V1-ACC-037, PILOT-008 (support) |
| Files affected | `packages/observability/` |
| Deliverables | Incident records; reason-code coverage. |
| Positive tests | Every registered reason code can be produced and inspected. |
| Negative tests | A code in the registry with no producing path fails the rung. An incident channel that authorizes a change fails. |
| Failure-injection tests | Trigger each incident class. |
| Operator validation | Operator triggers a HALT and finds the incident record. |
| Evidence package | Reason-code coverage matrix. |
| Rollback / recovery | Revert. |
| Stop conditions | A documented code has no producer. |
| Definition of Ready | FBL-058, FBL-047 inspected. |
| Definition of Done | Every code surfaced and inspectable. |
| Git boundary | One commit. · **Enables** FBL-060 |

### FBL-060 — Hostile-path fixtures and the standing safety suite

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Execution-time path-escape fixtures, and a standing safety suite re-run on every later rung. |
| Why here | **A gap no required rung owned.** One safety acceptance row demands hostile-path testing that the fixture set never enumerated, and the path-escape HALT branch had no fixture behind it. |
| Prerequisites | FBL-059, FBL-011 |
| Blocked by | none |
| Allowed work | Traversal, escape, absolute-path, and UNC-style hostile fixtures; standing suite assembly with each entry naming its acceptance row. |
| Prohibited work | Using a real path as a hostile fixture. |
| Specifications | `security-and-privacy.md`, `permission-model.md`, `safety-acceptance.md` |
| ADRs | ADR-001 |
| Acceptance | **SAF-007** (executable half), SAF-001, SAF-004, SAF-009, SAF-010 |
| Files affected | `tests/safety/`, `tests/fixtures/hostile/` |
| Deliverables | Hostile fixtures; standing safety suite. |
| Positive tests | Legitimate in-root paths pass. |
| Negative tests | Traversal, escape, and absolute hostile paths each HALT with `PATH_ESCAPE`. |
| Failure-injection tests | Hostile path injected mid-batch. |
| Operator validation | Operator confirms the suite runs on every later rung. |
| Evidence package | Safety suite results; acceptance-row mapping. |
| Rollback / recovery | Revert. |
| Stop conditions | Any hostile path is accepted. |
| Definition of Ready | FBL-059, FBL-011 inspected. |
| Definition of Done | Hostile fixtures exist; suite is standing. |
| Git boundary | One commit. · **Enables** FBL-061 |

### FBL-061 — Descriptor drift and remount stop conditions

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Enforce descriptor-mismatch and connection-loss stop conditions across batches and checkpoints. |
| Why here | **The last capability rung that must be green before G4 may even be requested.** A descriptor mismatch is fatal because the plan's preservation assumptions no longer hold. |
| Prerequisites | FBL-060, FBL-012 |
| Blocked by | none |
| Allowed work | Descriptor comparison at execution; volume-identifier change detection; token invalidation on reconnect; checkpoint invalidation. |
| Prohibited work | Treating a remount as resumable. Proceeding on a descriptor mismatch. |
| Specifications | `file-identity-model.md`, `preservation-model.md` |
| ADRs | ADR-012, ADR-016 |
| Acceptance | V1-ACC-032, V1-ACC-036 |
| Files affected | `packages/adapters/`, `packages/copy-engine/` |
| Deliverables | Drift and remount enforcement. |
| Positive tests | A matching descriptor proceeds. |
| Negative tests | FX-29 descriptor drift → **fatal** stop. FX-30 volume identifier change → run stops, checkpoints invalidated, in-flight tokens discarded, not resumable. |
| Failure-injection tests | Reconnect mid-batch. |
| Operator validation | Operator confirms a remount is not silently resumed. |
| Evidence package | Stop-condition transcripts. |
| Rollback / recovery | Fresh root confirmation before resume. |
| Stop conditions | A remount resumes silently. |
| Definition of Ready | FBL-060, FBL-012 inspected. |
| Definition of Done | Drift fatal; remount non-resumable. |
| Git boundary | One commit. · **Enables** FBL-070 |

### FBL-062 — Rollback engine and drill harness

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Idempotent journal-guided restore, with a drill executable on fixtures. |
| Why here | **Must precede the pilot.** Rollback must be written, checked, and *drillable before the first pilot write*. It is a separately approved operation with its own authority subject, so it needs approval binding first. |
| Prerequisites | FBL-057, FBL-053, FBL-047 |
| Blocked by | none |
| Allowed work | Journal-guided restore; rollback authority subject; drill harness; idempotent replay of the inverse. |
| Prohibited work | Ad-hoc restore not derived from the journal. Rollback without its own approval. Guessing at a mismatch. |
| Specifications | `rollback-playbook.md`, `approval-binding-model.md` |
| ADRs | ADR-002, ADR-003 |
| Acceptance | PILOT-006 |
| Files affected | `packages/copy-engine/`, `packages/validation/` |
| Deliverables | Rollback engine; drill harness. |
| Positive tests | A bounded batch restores idempotently; a second run changes nothing further. |
| Negative tests | Rollback without a bound `RollbackAuthority` approval fails. Restoring beyond the journalled batch fails. |
| Failure-injection tests | Kill mid-rollback; resume idempotently. |
| Operator validation | Operator runs the drill on fixtures. |
| Evidence package | Rollback record; drill transcript. |
| Rollback / recovery | This rung is the recovery path. |
| Stop conditions | Rollback is not idempotent. |
| Definition of Ready | FBL-057, FBL-053, FBL-047 inspected. |
| Definition of Done | Idempotent restore; drill executable. |
| Git boundary | One commit. · **Enables** FBL-066 |

### FBL-063 — Review console

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | A non-executing decision surface that renders evidence, captures intent, and submits only the bounded allowlist. |
| Why here | **Deliberately late.** Its defining acceptance test is a negative one that needs backend authorization to already exist and to be the only thing that authorizes. Building it earlier would let its rendering needs shape the records rather than the reverse, and would leave the command allowlist unenforced. |
| Prerequisites | FBL-047, FBL-038, FBL-039 |
| Blocked by | **OD-019** (console stack); **PF-28** (`grant_approval` on a plan is permitted while `approve_operation_plan` is forbidden) |
| Allowed work | Evidence rendering; intent capture displaying the exact bound subject; the thirteen allowed commands. |
| Prohibited work | **Every command on the forbidden list.** Constructing, signing, or self-validating an approval. Reading file bytes for mutation. Becoming a source of truth. |
| Specifications | `review-console-architecture.md`, `interface-model.md` |
| ADRs | **ADR-014**, ADR-015 |
| Acceptance | **V1-ACC-038** |
| Files affected | `apps/review-console/` |
| Deliverables | Console; allowlist enforcement. |
| Positive tests | The thirteen allowed commands succeed. |
| Negative tests | Any forbidden command is a **rejected request and a recorded safety event**, not a relaxable permission error. A console-constructed approval is refused. A UI-only approval path with no backend authorization mutates nothing. Console state hiding an immutable record fails. |
| Failure-injection tests | Forged command submitted directly to the backend. |
| Operator validation | Operator attempts a forbidden command and sees a safety event. |
| Evidence package | Allowlist enforcement matrix. |
| Rollback / recovery | Revert. |
| Stop conditions | Any forbidden command succeeds. |
| Definition of Ready | FBL-047, FBL-038, FBL-039 inspected; OD-019 and PF-28 resolved. |
| Definition of Done | Non-executing surface; allowlist enforced. |
| Git boundary | One commit in `apps/review-console/`. · **Enables** FBL-064 |

### FBL-064 — Sentinel

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | A read-only health and alert surface with executable **negative** authority tests. |
| Why here | **Deliberately late.** Its acceptance is a negative claim, whose only executable form is the backend rejecting a Sentinel-originated request — so backend authorization must exist first, or the test proves only that an unwired component does nothing. Its inputs — heartbeat, journal freshness, queue length, thresholds — also do not exist until now. |
| Prerequisites | FBL-063, FBL-059, FBL-051 |
| Blocked by | **OD-018** (alert wording) |
| Allowed work | Health signals; alerts; predefined safe-list job requests only. |
| Prohibited work | Classifying, approving, or mutating anything. Issuing arbitrary commands. Choosing destinations. Becoming the primary worker. |
| Specifications | `sentinel-architecture.md`, `sentinel-playbook.md`, `permission-model.md` |
| ADRs | **ADR-008**, ADR-007 |
| Acceptance | **V1-ACC-052**, SAF-009, LIVE-012 (support) |
| Files affected | `apps/sentinel/` |
| Deliverables | Sentinel; six negative authority tests. |
| Positive tests | Health signals and alerts emit correctly. |
| Negative tests | A Sentinel-originated approval attempt rejects `APR-E20`. The Sentinel principal holds no approve or execute authority class. It cannot emit a classification proposal or mutate a record. Off-safe-list job requests rejected. It may report stalled but not resolve it. It cannot become primary worker when the Mac mini is unavailable — it reports instead. |
| Failure-injection tests | Mac mini unavailable; Sentinel must report, not take over. |
| Operator validation | Operator confirms all six negative tests. |
| Evidence package | Authority test results; alert history. |
| Rollback / recovery | Revert. |
| Stop conditions | The Sentinel gains any authority. |
| Definition of Ready | FBL-063, FBL-059, FBL-051 inspected; OD-018 resolved. |
| Definition of Done | Read-only surface; six negative tests pass. |
| Git boundary | One commit in `apps/sentinel/`. · **Enables** FBL-074 |

### FBL-065 — Live adapter implementation (unexercised)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Implement the chosen live adapter against the capability contract, exercised **only** against a local endpoint standing in for the real one. |
| Why here | **Split from characterization deliberately.** Writing the adapter is code and belongs at G3; *measuring it against the NAS* is the first real read and belongs at G4. A descriptor cannot be produced here, and a hand-written one is invalid. |
| Prerequisites | FBL-061, FBL-009 |
| Blocked by | **OD-016** (adapter choice — the operator's) |
| Allowed work | Adapter implementation against the port; capability self-test wiring; exercise against a local endpoint only. |
| Prohibited work | **Pointing the adapter at any NAS path, mount, share, or hostname.** Emitting a descriptor for a real endpoint. Any credential. |
| Specifications | `adapter-architecture.md`, `preservation-model.md`, `file-identity-model.md` |
| ADRs | **ADR-012** |
| Acceptance | V1-ACC-007 (implementation half) |
| Files affected | `packages/adapters/` |
| Deliverables | Live adapter implementation, unexercised against the NAS. |
| Positive tests | The adapter satisfies the port against a local endpoint. |
| Negative tests | Any configuration naming a NAS path, mount, share, or credential fails CI. A descriptor emitted without a characterization run is invalid. |
| Failure-injection tests | All six modes against the local endpoint. |
| Operator validation | Operator confirms no NAS endpoint is reachable from this code path. |
| Evidence package | Local-endpoint conformance results. |
| Rollback / recovery | Revert. |
| Stop conditions | Any NAS endpoint is contacted. |
| Definition of Ready | FBL-061 inspected; **OD-016 resolved**. |
| Definition of Done | Adapter implemented; provably unexercised against the NAS. |
| Git boundary | One commit in `packages/adapters/`. · **Enables** FBL-070 |

### FBL-066 — Copied-pilot orchestration (capability)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | The orchestration that will drive a copied-corpus run, proven end to end on fixtures. |
| Why here | The capability must be fixture-proven before the pilot gate is requested. This rung builds it; the G5 rung runs it. |
| Prerequisites | FBL-062, FBL-051 |
| Blocked by | none |
| Allowed work | End-to-end orchestration over fixtures; exception reporting; pilot evidence assembly. |
| Prohibited work | **Executing a pilot.** Touching authoritative data. |
| Specifications | `pilot-run-playbook.md`, `pilot-acceptance.md` |
| ADRs | **ADR-010** |
| Acceptance | PILOT-001…014 (fixture halves) |
| Files affected | `apps/cli/`, `packages/planning/` |
| Deliverables | Orchestration; evidence assembler. |
| Positive tests | Full workflow completes on the fixture corpus. |
| Negative tests | Orchestration pointed at anything other than an isolated copy fails. |
| Failure-injection tests | Interrupt mid-orchestration; resume cleanly. |
| Operator validation | Operator reviews a fixture pilot package. |
| Evidence package | Fixture pilot package. |
| Rollback / recovery | Rollback drill. |
| Stop conditions | Any authoritative path is reachable. |
| Definition of Ready | FBL-062, FBL-051 inspected. |
| Definition of Done | Workflow proven on fixtures. |
| Git boundary | One commit. · **Enables** FBL-067 |

### FBL-067 — Live-batch executor and governor (capability)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Bounded batch execution under an approved immutable plan, with degraded-mode enforcement, proven on fixtures. |
| Why here | Batch shape and degraded-mode rules are execution constraints testable on fixtures, and must exist before a live readiness package is meaningful. |
| Prerequisites | FBL-066 |
| Blocked by | **OD-008** for real thresholds; fixture defaults suffice here |
| Allowed work | Bounded batching; concurrency rules; degraded-mode enforcement — batch size one, no concurrency, sealed checkpoint per operation, **retirement forbidden for the whole run**. |
| Prohibited work | Any live execution. Expanding a batch after failure. Retirement. |
| Specifications | `durability-and-recovery-model.md`, `live-migration-playbook.md` |
| ADRs | ADR-009, ADR-010 |
| Acceptance | V1-ACC-036, LIVE-004 (support) |
| Files affected | `packages/copy-engine/` |
| Deliverables | Batch executor; degraded-mode governor. |
| Positive tests | A bounded batch completes within thresholds. |
| Negative tests | A weak or unknown destination forces batch size one, no concurrency, and **refuses retirement regardless of approval scope**. Automatic expansion after a failed batch fails. |
| Failure-injection tests | Durability class downgraded mid-run. |
| Operator validation | Operator confirms degraded mode cannot be overridden by approval. |
| Evidence package | Batch transcripts; degraded-mode demonstration. |
| Rollback / recovery | Rollback engine. |
| Stop conditions | Retirement is reachable in degraded mode. |
| Definition of Ready | FBL-066 inspected. |
| Definition of Done | Bounded batching and degraded mode proven. |
| Git boundary | One commit. · **Enables** FBL-074 |

### FBL-068 — Migration reconciliation (capability)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Source-to-disposition reconciliation with balancing totals and owned exceptions. |
| Why here | **Distinct from restart reconciliation** — a different algorithm at a different gate. The ladder never uses the bare word "reconciliation" for both. |
| Prerequisites | FBL-067, FBL-027, FBL-039 |
| Blocked by | **OD-021** blocks its G8 *package*, not this implementation; OD-017 |
| Allowed work | Disposition accounting across organized, retained, quarantined, unresolved, failed; totals; exception inventory with named owners. |
| Prohibited work | Hiding exceptions inside aggregate counts. |
| Specifications | `domain-model.md`, `migration-completion-audit.md` |
| ADRs | ADR-001, ADR-015 |
| Acceptance | **V1-ACC-053** (accepted at G8), V1-ACC-041 |
| Files affected | `packages/validation/`, `packages/observability/` |
| Deliverables | Reconciliation report generator. |
| Positive tests | Fixture totals balance. |
| Negative tests | An exception without a named owner fails. An item with no terminal disposition fails. |
| Failure-injection tests | Injected unresolved item must surface. |
| Operator validation | Operator reconciles a fixture corpus by hand. |
| Evidence package | Reconciliation report; exception inventory. |
| Rollback / recovery | Regenerate. |
| Stop conditions | Totals cannot balance. |
| Definition of Ready | FBL-067, FBL-027, FBL-039 inspected. |
| Definition of Done | Balancing totals; owned exceptions. |
| Git boundary | One commit. · **Enables** FBL-069 |

### FBL-069 — Maintenance mode (capability)

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Steady-state review and reconcile behaviour, with unattended watchers **structurally absent**. |
| Why here | Last capability rung. Definition of Done requires that no maintenance automation is enabled as a side effect. |
| Prerequisites | FBL-068 |
| Blocked by | none |
| Allowed work | Manual review and reconcile paths; delta detection; alerting via the Sentinel. |
| Prohibited work | **Any scheduler entry point for unattended watchers** — deferred as a Future Registry item. Enabling automation as a side effect. |
| Specifications | `post-migration-maintenance.md` |
| ADRs | ADR-008 |
| Acceptance | V1-ACC-054 (documentary half satisfied at G1) |
| Files affected | `apps/cli/` |
| Deliverables | Maintenance paths. |
| Positive tests | Manual reconcile detects a fixture delta. |
| Negative tests | **A negative test asserting no scheduler entry point exists** — mirroring how provisional rules are made structurally incapable rather than config-disabled. |
| Failure-injection tests | none |
| Operator validation | Operator confirms no watcher can be switched on. |
| Evidence package | Absence assertion; maintenance transcript. |
| Rollback / recovery | Revert. |
| Stop conditions | Any unattended watcher is reachable. |
| Definition of Ready | FBL-068 inspected. |
| Definition of Done | Manual maintenance; watchers structurally absent. |
| Git boundary | One commit. · **Enables** FBL-070 |

### FBL-070 — G4 dry-run readiness assembler

| Field | Value |
| --- | --- |
| Gate | G3 |
| NAS access | none |
| Objective | Assemble and self-check the G4 evidence bundle. **The assembler, not the bundle.** |
| Why here | The last G3 rung. Everything G4 will exercise must already be fixture-green before the gate is requested. |
| Prerequisites | FBL-069, FBL-065, FBL-061, FBL-058 |
| Blocked by | none |
| Allowed work | Bundle assembler; self-check against the G4 entry criteria and the dry-run playbook's evidence list. |
| Prohibited work | **Producing the actual G4 package** — that requires G4 authorization. Any NAS contact. |
| Specifications | `gate-model.md`, `dry-run-playbook.md`, `evidence-standard.md` |
| ADRs | ADR-009 |
| Acceptance | Assembles evidence for V1-ACC-030, V1-ACC-001 |
| Files affected | `apps/cli/`, `packages/observability/` |
| Deliverables | Evidence assembler; self-check. |
| Positive tests | The assembler produces a complete bundle from fixture inputs. |
| Negative tests | A missing evidence item fails the self-check rather than producing a partial bundle. |
| Failure-injection tests | Missing artifact. |
| Operator validation | Operator reviews a fixture bundle for readability without chat history. |
| Evidence package | Fixture G4 bundle. |
| Rollback / recovery | Regenerate. |
| Stop conditions | The assembler emits an incomplete bundle silently. |
| Definition of Ready | FBL-069, FBL-065, FBL-061, FBL-058 inspected. |
| Definition of Done | Assembler complete and self-checking. |
| Git boundary | One commit. · **Enables** FBL-071 |
---

## Gate G4 — Dry-Run Readiness

**The first gate at which the system touches the real NAS, and NAS paths may only be read.**

No create, update, delete, rename, or write-based probe on any NAS path — source or destination. Local writes are permitted **only** into one operator-approved control-data root proven disjoint from every NAS mount, source root, destination root, and scan boundary. Every such write is journalled or included in evidence. Any overlap, or uncertainty about overlap, is an immediate stop.

Destination capability characterization requires a write and therefore remains at G5 (PF-25, OD-023).

### FBL-071 — Controlled read-only NAS adapter enablement and source characterization

| Field | Value |
| --- | --- |
| Gate | **G4** |
| NAS access | read-only |
| Objective | First live contact: characterize the confirmed source root read-only, producing the live **source** capability descriptor. |
| Why here | The first live action must itself be a characterization run — read-only, therefore G4-legal — because every later behaviour is a function of a *measured* descriptor and a hand-written one is invalid. |
| Prerequisites | FBL-070 |
| Blocked by | **OD-001, OD-002, OD-003, OD-005, OD-011, OD-012, OD-016** — all seven carry `blocks_gate: dry_run` |
| Allowed work | Read-only mount or connection; source-root characterization; live source descriptor; identity-grade measurement; read-only credential use. |
| Prohibited work | **Any write to any NAS path**, source or destination, including a write-based probe. Any write outside the approved control-data root. Hashing beyond what characterization requires. Any mutation-capable credential. |
| Specifications | `preservation-model.md`, `file-identity-model.md`, `adapter-architecture.md` |
| ADRs | ADR-012, ADR-001 |
| Acceptance | LIVE-003 (support), V1-ACC-007 |
| Files affected | Evidence artifacts only |
| Deliverables | Live source capability descriptor with attestation. |
| Positive tests | The descriptor is complete for every measurable source-side property. |
| Negative tests | Any write to a NAS path fails and halts. A write outside the approved control-data root fails and halts. A control root overlapping any NAS mount, source root, destination root, or scan boundary is an immediate stop. A destination-side property is recorded `unsupported_reported`, not assumed — **see PF-25: the destination descriptor is not obtainable at G4 at all.** |
| Failure-injection tests | Connection loss mid-characterization. |
| Operator validation | Operator confirms read-only credentials and reviews `retirement_capable`. |
| Evidence package | Live source descriptor; attestation; read-only proof. |
| Rollback / recovery | Disconnect; nothing was written. |
| Stop conditions | Any write to a NAS path is attempted. The control root overlaps any NAS boundary, or its disjointness is uncertain. Any property requires a write to measure. |
| Definition of Ready | G4 authorization recorded in the ledger; all seven dry-run decisions resolved. |
| Definition of Done | Live source descriptor measured; zero writes. |
| Git boundary | One commit: evidence only, no code. · **Enables** FBL-072 |

### FBL-072 — Dry-run execution and evidence

| Field | Value |
| --- | --- |
| Gate | **G4** |
| NAS access | read-only |
| Objective | Read-only inventory and non-mutating plan generation against confirmed roots, producing the G4 evidence bundle. |
| Why here | The gate's purpose. Everything it exercises is already fixture-green. |
| Prerequisites | FBL-071 |
| Blocked by | **PF-25** (a G4 plan cannot carry a measured destination descriptor and is therefore not promotable) |
| Allowed work | Read-only inventory; hashing; metadata extraction; rule evaluation; destination proposal; conflict detection; hashed evidence index. |
| Prohibited work | **Any write to any NAS path**, including a write-based probe. Any write outside the approved control-data root. Treating a G4 plan as executable. Retirement proposals becoming actions. |
| Specifications | `dry-run-playbook.md`, `operation-model.md` |
| ADRs | **ADR-009** |
| Acceptance | **V1-ACC-001, V1-ACC-030**, V1-ACC-041 |
| Files affected | Evidence artifacts only |
| Deliverables | Inventory manifest; dry-run plan marked descriptor-incomplete; rule coverage, conflict, unresolved reports; evidence index. |
| Positive tests | Repeated scan is deterministic; destination tree unchanged. |
| Negative tests | Any write to a NAS path fails. Any write outside the approved control-data root fails. A G4 plan presented as promotable fails. Source property-set comparison shows no mutation — **hashes alone are insufficient here, per PF-13**. |
| Failure-injection tests | Interrupt mid-scan; resume without duplicate identities. |
| Operator validation | Operator reviews the plan and confirms the destination tree is untouched. |
| Evidence package | The full G4 bundle per the dry-run playbook, with stop-condition evaluation records. |
| Rollback / recovery | Delete artifacts inside the approved control-data root; NAS sources untouched. |
| Stop conditions | Any NAS mutation. Any write outside the approved control-data root. Any stop condition passed unevaluated. |
| Definition of Ready | FBL-071 complete; PF-25 resolved. |
| Definition of Done | Complete G4 bundle; determinism and zero-mutation proven. |
| Git boundary | One commit: evidence only. · **Enables** FBL-073 |

---

## Gate G5 — Copied-Pilot Readiness

Execution against an **isolated copied corpus**. The authoritative source is never the pilot target.

### FBL-073 — Destination characterization and copied pilot

| Field | Value |
| --- | --- |
| Gate | **G5** |
| NAS access | bounded-write |
| Objective | Characterize the destination — the first legal write, **confined to the isolated pilot zone** — then run the full workflow against the copied corpus. |
| Why here | Destination characterization requires a write and is therefore illegal until G5. This is the resolution of PF-25: the destination descriptor is the **first G5 activity**, before any pilot plan is approved. |
| Prerequisites | FBL-072, FBL-066, FBL-062 |
| Blocked by | **OD-007, OD-008** (`blocks_gate: pilot`) |
| Allowed work | Destination characterization in the isolated zone; full workflow over the copied corpus; rollback drill; preservation comparison. |
| Prohibited work | Writing to any authoritative destination. Touching originals. **Any source retirement.** Expanding beyond the approved corpus. |
| Specifications | `pilot-run-playbook.md`, `pilot-acceptance.md`, `preservation-model.md` |
| ADRs | **ADR-010**, ADR-002 |
| Acceptance | **PILOT-001…PILOT-014**, **V1-ACC-040**, V1-ACC-050 (source half) |
| Files affected | Evidence artifacts only |
| Deliverables | Live destination descriptor; pilot package; rollback drill record; preservation comparison report. |
| Positive tests | The workflow completes; hashes verify; the drill restores. |
| Negative tests | Originals provably untouched. Any retirement attempt refused. An exception summarized away rather than recorded fails. |
| Failure-injection tests | Interrupt mid-pilot; resume without duplication. |
| Operator validation | Operator reviews the pilot package and the drill record. |
| Evidence package | Full G5 bundle per the pilot playbook. |
| Rollback / recovery | Execute the rollback drill. |
| Stop conditions | Any original is modified. Any retirement is attempted. |
| Definition of Ready | G5 authorization recorded; OD-007 and OD-008 resolved; rollback drillable. |
| Definition of Done | All BLOCKER pilot rows green; originals untouched. |
| Git boundary | One commit: evidence only. · **Enables** FBL-074 |

---

## Gate G6 — Limited-Live Readiness

Bounded, approved **copy** operations. No retirement of any kind.

### FBL-074 — Live readiness package

| Field | Value |
| --- | --- |
| Gate | **G6** |
| NAS access | none |
| Objective | Evaluate every live-readiness row and assemble the G6 bundle. **Assembly and evaluation only — this rung performs no NAS access.** |
| Why here | Readiness must be evaluated before any live batch, and one row requires the Sentinel to exist in order to prove it *cannot* authorize. |
| Prerequisites | FBL-073, FBL-067, FBL-064 |
| Blocked by | **OD-006, OD-009, OD-013, OD-015, OD-020** (`blocks_gate: live`) |
| Allowed work | Row-by-row evaluation; bundle assembly; ledger verification for G1–G5. |
| Prohibited work | Authorizing the gate. Waiving a BLOCKER row. Any live write. |
| Specifications | `live-readiness.md`, `gate-model.md` |
| ADRs | ADR-010 |
| Acceptance | **LIVE-001…LIVE-012** |
| Files affected | Evidence artifacts only |
| Deliverables | G6 readiness package with per-row disposition. |
| Positive tests | Every BLOCKER row has an artifact behind it. |
| Negative tests | A row backed by an assertion rather than an artifact fails. A missing prior-gate ledger entry fails LIVE-001. |
| Failure-injection tests | none |
| Operator validation | Operator reviews the package and decides whether to authorize. |
| Evidence package | G6 bundle; recovery and threshold confirmations. |
| Rollback / recovery | Not applicable — nothing executed. |
| Stop conditions | Any BLOCKER row lacks evidence. |
| Definition of Ready | FBL-073 complete; the five live decisions resolved. |
| Definition of Done | All twelve rows dispositioned with artifacts. |
| Git boundary | One commit: evidence only. · **Enables** FBL-075 |

### FBL-075 — Limited live copying

| Field | Value |
| --- | --- |
| Gate | **G6** |
| NAS access | bounded-write |
| Objective | One bounded, approved, copy-only live batch under an immutable plan. |
| Why here | The first authoritative-destination write, after pilot proof and readiness evaluation. |
| Prerequisites | FBL-074 |
| Blocked by | none beyond the G6 authorization itself |
| Allowed work | One bounded copy batch; precondition revalidation; hash and preservation verification; journalling and checkpointing. |
| Prohibited work | **Source retirement — that is G7.** Protected-vault overwrite. Automatic expansion to a next batch. Deletion. |
| Specifications | `live-migration-playbook.md`, `operation-model.md` |
| ADRs | ADR-002, ADR-011 |
| Acceptance | **V1-ACC-050**, V1-ACC-034, V1-ACC-044 |
| Files affected | Evidence artifacts only |
| Deliverables | Executed batch; verification and preservation reports; journal and checkpoints. |
| Positive tests | Every copied item verifies on content and preservation. |
| Negative tests | Any retirement attempt refused. Any vault overwrite refused. Automatic expansion after the batch refused. |
| Failure-injection tests | Interrupt mid-batch; resume without duplication. |
| Operator validation | Operator reviews the batch evidence before considering a next batch. |
| Evidence package | Batch manifest; verification; preservation comparison; journal. |
| Rollback / recovery | Rollback engine, under its own approval. |
| Stop conditions | Threshold breach; hash mismatch; preservation failure; descriptor drift. |
| Definition of Ready | G6 authorization recorded; retirement flags off. |
| Definition of Done | Batch complete and verified; nothing retired. |
| Git boundary | One commit: evidence only. · **Enables** FBL-076 |

---

## Gate G7 — Source-Retirement Readiness

Retirement is **retention, not removal**. Permanent deletion is unavailable in V1 at any gate.

### FBL-076 — Source retirement

| Field | Value |
| --- | --- |
| Gate | **G7** |
| NAS access | bounded-write |
| Objective | Retire verified source items as a **separate journalled operation** with its own approval scope. |
| Why here | Retirement is never a trailing step of a copy. It requires per-item verification, a passing preservation comparison, and its own short-lived authority. |
| Prerequisites | FBL-075, FBL-053 |
| Blocked by | **OD-010** (`blocks_gate: retirement`) |
| Allowed work | Per-item retirement to a governed retained or quarantine state, each with its own intent and outcome records and a `RetirementAuthority` approval. |
| Prohibited work | **Permanent deletion — unavailable in V1.** Retiring on hash equality alone. Partial hard-link-set retirement. Retirement in degraded mode, regardless of approval scope. Retirement under advisory identity confidence without a recorded waiver. |
| Specifications | `live-data-policy.md`, `preservation-model.md`, `approval-binding-model.md` |
| ADRs | **ADR-002**, ADR-003 |
| Acceptance | **V1-ACC-035**, SAF-003, SAF-010, LIVE-011 |
| Files affected | Evidence artifacts only |
| Deliverables | Retirement records; per-item verification and preservation evidence. |
| Positive tests | A fully verified item with an eligible preservation report retires under a bound approval. |
| Negative tests | Retirement on hash equality alone refused. An ineligible preservation gate refused. A blanket waiver refused. Partial hard-link-set retirement refused. Any permanent deletion refused. |
| Failure-injection tests | Interrupt mid-retirement; no item left in an indeterminate state. |
| Operator validation | Operator approves each batch individually, with a short-lived authority. |
| Evidence package | Verification; preservation comparison with eligibility; bound approval; reconciliation. |
| Rollback / recovery | Restore from the retained state — nothing was deleted. |
| Stop conditions | Any eligibility failure. Any deletion path. |
| Definition of Ready | G7 authorization recorded; OD-010 resolved; retention policy versioned. |
| Definition of Done | Items retired and recoverable; nothing deleted. |
| Git boundary | One commit: evidence only. · **Enables** FBL-077 |

---

## Gate G8 — Migration Completion

### FBL-077 — Final reconciliation

| Field | Value |
| --- | --- |
| Gate | **G8** |
| NAS access | read-only |
| Objective | Prove every in-scope source item reached a terminal disposition and that totals balance. |
| Why here | Cannot be true while retirement batches are outstanding. |
| Prerequisites | FBL-076, FBL-068 |
| Blocked by | **OD-021** (`blocks_gate: migration_completion`) |
| Allowed work | Disposition accounting; totals; exception inventory with named owners. |
| Prohibited work | Hiding exceptions in aggregates. Any mutation. |
| Specifications | `migration-completion-audit.md`, `domain-model.md` |
| ADRs | ADR-001 |
| Acceptance | **V1-ACC-053** |
| Files affected | Evidence artifacts only |
| Deliverables | Final reconciliation report; exception inventory. |
| Positive tests | Totals balance against the baseline inventory. |
| Negative tests | An item with no terminal disposition fails. An unowned exception fails. |
| Failure-injection tests | none |
| Operator validation | Operator reviews the exception inventory by owner. |
| Evidence package | Reconciliation report; disposition totals; baseline manifests. |
| Rollback / recovery | Not applicable. |
| Stop conditions | Totals do not balance. |
| Definition of Ready | G8 authorization recorded; OD-021 resolved. |
| Definition of Done | Balanced totals; owned exceptions. |
| Git boundary | One commit: evidence only. · **Enables** FBL-078 |

### FBL-078 — Migration completion

| Field | Value |
| --- | --- |
| Gate | **G8** |
| NAS access | none |
| Objective | Declare the migration complete and preserve the final baseline and archive index. |
| Why here | Follows reconciliation; declaring completion before totals balance would be an unevidenced claim. |
| Prerequisites | FBL-077 |
| Blocked by | none |
| Allowed work | Completion declaration; final baseline manifests; archive index. |
| Prohibited work | Enabling any automation as a side effect. Any new destructive class of operation. |
| Specifications | `gate-model.md`, `post-migration-maintenance.md` |
| ADRs | ADR-001 |
| Acceptance | V1-ACC-053, V1-ACC-055 (documentary half at G1) |
| Files affected | Evidence artifacts only |
| Deliverables | Completion record; final manifests; archive index. |
| Positive tests | The completion record cites the reconciliation evidence. |
| Negative tests | Completion declared with outstanding exceptions fails. |
| Failure-injection tests | none |
| Operator validation | Operator signs the completion record. |
| Evidence package | Completion certificate; archive index. |
| Rollback / recovery | Not applicable. |
| Stop conditions | Any outstanding exception is unowned. |
| Definition of Ready | FBL-077 complete. |
| Definition of Done | Completion recorded with evidence. |
| Git boundary | One commit: evidence only. · **Enables** FBL-079 |

### FBL-079 — Maintenance mode activation

| Field | Value |
| --- | --- |
| Gate | **G8** |
| NAS access | read-only |
| Objective | Enter monitored steady state, with unattended watchers still structurally absent. |
| Why here | The terminal rung. Entry is gated on completion, and no automation may be enabled as a side effect. |
| Prerequisites | FBL-078, FBL-069 |
| Blocked by | none |
| Allowed work | Manual review and reconcile cadence; Sentinel monitoring; delta detection. |
| Prohibited work | **Unattended live watchers — deferred to the Future Registry.** Any automation enabled as a side effect of entering maintenance. |
| Specifications | `post-migration-maintenance.md` |
| ADRs | ADR-008 |
| Acceptance | V1-ACC-054 |
| Files affected | Evidence artifacts only |
| Deliverables | Maintenance readiness record. |
| Positive tests | Manual reconcile detects a real delta. |
| Negative tests | **The absence assertion still holds — no scheduler entry point exists.** |
| Failure-injection tests | none |
| Operator validation | Operator confirms no watcher was enabled. |
| Evidence package | Maintenance readiness record; absence assertion. |
| Rollback / recovery | Exit maintenance; nothing automated to unwind. |
| Stop conditions | Any unattended watcher becomes reachable. |
| Definition of Ready | FBL-078 complete. |
| Definition of Done | Steady state entered; watchers absent. |
| Git boundary | One commit: evidence only. · **Enables** — (terminal rung) |
---

## Planning findings

Generating this ladder required reading the Foundation as an implementer would. Doing so surfaced **thirty specification gaps and contradictions** that would block or mislead implementation. They are recorded here rather than silently worked around.

**None of these is resolved in this document.** Several are operator policy decisions, and G2 does not authorize resolving them. The rest are specification defects that must go through `docs/05-governance/change-control.md` before the rung that depends on them may be authorized.

A rung whose **Blocked by** field names a finding cannot start until that finding is closed. This is the mechanism that prevents a later rung from depending on an undefined contract.

| Severity | Count | Meaning |
| --- | --- | --- |
| BLOCKER | 18 | The named rung is unimplementable as specified. |
| MAJOR | 8 | Implementable, but with a real risk of divergent or unsafe implementation. |
| MINOR | 3 | Should be corrected; unlikely to cause harm alone. |
| NOTE | 1 | Recorded for awareness; already addressed by a rung deliverable. |

### Blocking findings

| ID | Severity | Finding | Blocks | Routing |
| --- | --- | --- | --- | --- |
| PF-01 | BLOCKER | `PROJECTION_UNAVAILABLE` permits halting when *authorization lookups* cannot be served — implying authorization reads from SQLite. But the durability model forbids SQLite being the only home of an authorization-required fact, and the revocation check must read the durable journal tail, never a cache. Either authorization reads from the journal (making that halt branch unreachable) or from the projection (violating the authority rule). | FBL-017, FBL-047 | Change control. Recommend: authorization reads are journal-tail reads; the halt branch is retained only for non-authorization query failure. |
| PF-02 | BLOCKER | The journal record-type registry contains no record type for inventory, metadata, hash, classification, duplicate, review, or taxonomy facts — yet those tables are in SQLite and replay is required to rebuild **all** derived state. The event stream cannot fill the gap; it is authoritative for nothing. As written, the rebuild acceptance requirement is unsatisfiable. | FBL-017, FBL-018 | Change control. Choose one: extend the record registry; or declare those tables rebuildable by re-scan and re-evaluate and scope the rebuild requirement to the execution subset. **Not left to the implementer.** |
| PF-04 | BLOCKER | `AdapterCapabilityDescriptor` is referenced by id from `Approval`, expires, and is fatal-on-mismatch — but has no domain entity, lifecycle, or persistence home. | FBL-008 | Change control: add the entity. |
| PF-05 | BLOCKER | The nonce ledger is placed on control storage and described as journalled, and the authorization algorithm requires the nonce to be in an *issued* ledger — but no `nonce_issued` or `nonce_spent` record type exists. Issued nonces have no authoritative home. | FBL-005, FBL-047 | Change control: add the record types. |
| PF-07 | BLOCKER | `HardLinkSet` is referenced by the inventory field table and the identity model but has no domain entity. | FBL-028 | Change control: add the entity. |
| PF-08 | BLOCKER | Operation entry types are `copy`, `move`, `rename`, `quarantine`, `skip`. The identity model requires `recreate_symlink` *or* an explicit out-of-scope declaration — neither exists — and the preservation model requires linking the remainder of a hard-link set, which no entry type can express. Two fixtures are unimplementable as written. | FBL-029, FBL-049 | Change control: add entry types, or declare symlink and hard-link reproduction out of V1 scope with a stop condition. |
| PF-09 | BLOCKER | Only the precondition-set digest has a defined preimage. `subject_content_hash`, `evidence_bundle_hash`, `rule_set_hash`, `taxonomy_hash`, `config_modes_hash`, `session_binding_hash`, and `binding_digest` have no canonicalization rule, yet the backend must recompute and compare them. Two conforming implementations would disagree. | FBL-005, FBL-045 | Change control: specify canonical serialization for every bound value. Compounds OD-004. |
| PF-10 | BLOCKER | `HashRecord.scope` lacks `source_recheck`, which the change-token rules mandate; `HashRecord` status lacks `unstable`, which the concurrent-modification rules mandate. | FBL-025 | Change control: extend both enums. |
| PF-11 | BLOCKER | `SourceRoot` lacks the identity-evidence fields the identity model states it carries — volume identifier, kind, mount reference, capability descriptor id, grade. Three stop conditions are unimplementable against the domain model as written. | FBL-023 | Change control: add the fields. |
| PF-12 | BLOCKER | The rule schema states symbolic roots resolve from the thresholds example, but that file has a three-key path map with no root ids, authority tags, or root-ref vocabulary. `VAL-ROOT-REF` has nothing to validate against. | FBL-021 | Change control: define the symbolic root registry. |
| PF-14 | BLOCKER | Bundle copy must be all-or-nothing and bundle atomicity is enforced by the platform, not the adapter — but the write protocol defines a single-file operation with one temp path and one rename. There is no staging-directory promote, no multi-member intent record, and no crash-state row for a half-promoted bundle. | FBL-031 | Change control: define a multi-member atomic promote protocol and its crash rows. |
| PF-15 | BLOCKER | The taxonomy model requires nodes with slug, authority, status, parent, and path template. The example config instead supplies shares with id, path, and purpose, plus a category map — no authority, no status, no node list — and no taxonomy schema exists. `VAL-TAXONOMY` has no artifact to validate against. The rule contract was made canonical during audit resolution; the taxonomy never received the same treatment. | FBL-034 | Change control: author a canonical taxonomy schema and reconcile the example. |
| PF-19 | BLOCKER | `OperationPlan` required fields omit `adapter_descriptor_ids` and `preservation_profile_id`, which appear only on `Approval`. But the preservation protocol freezes both **into the plan**, and the descriptor-drift stop condition compares against the descriptor recorded in the **plan**. | FBL-040, FBL-041 | Change control: add the fields to the plan. |
| PF-21 | BLOCKER | `EvidenceBundle` is bound by the approval record, recomputed by an authorization step, and invalidated by a trigger — but no document defines its membership, canonical serialization, versioning, or hash computation. That authorization step is unimplementable as written. | FBL-045 | Change control: define the evidence bundle. |
| PF-22 | BLOCKER | The write protocol is designated authoritative and must not be substituted — yet it never captures or compares the pre- and post-copy change tokens. This contradicts the identity model's requirement that promotion occur only after **both** destination hash equality and token equality. An implementer following the authoritative protocol ships the concurrent-modification fixture broken. | FBL-048 | Change control: add token capture and comparison to protocol phases C, D, and E. |
| PF-23 | BLOCKER | `VerificationResult` carries only source and destination hashes — no preservation-report reference and no token evidence — despite three documents requiring both before an operation may be called verified. | FBL-052 | Change control: extend the entity. |
| PF-24 | BLOCKER | `PreservationComparisonReport` has a defined schema in the preservation model but no domain entity; `VerificationResult` is a different shape. | FBL-053 | Change control: add the entity. |
| PF-25 | BLOCKER | **A measured destination descriptor cannot be produced at G4.** A descriptor is valid only if measured; measuring it requires an NFD write-and-read-back **to the destination**; and G4 authorizes no write to any NAS path, destination trees included. (G4 does permit local control-data writes — that is BLOCKER-02's correction — but a control-data write cannot characterize a NAS destination.) Yet G4 is where plans are generated, and a plan must carry the destination descriptor at approval. **G4 dry-run plans are therefore structurally incapable of carrying a valid destination descriptor.** | FBL-072, FBL-073 | Change control **and** operator decision — recorded as **OD-023**. This ladder assumes the resolution is: G4 plans are marked descriptor-incomplete and non-promotable, and destination characterization is the first G5 activity (FBL-073). That assumption is stated, not decided. |

### Major findings

| ID | Severity | Finding | Blocks | Routing |
| --- | --- | --- | --- | --- |
| PF-03 | MAJOR | Checkpoint sealing preconditions are stated in terms of *operations* being terminal — a mutation concept — but checkpoints also scope scans and reconciliation runs. What sealing means for a read-only scan with zero operations is unstated, as is whether a scan checkpoint must be sealed at all. | FBL-019 | Change control. |
| PF-06 | MAJOR | The approval state machine allows nine states, but the event vocabulary defines only four approval events. `claimed`, `released`, `invalidated`, `expired`, and `superseded` are authoritative journal facts with no derived event, so the observability stream cannot represent the approval state machine. Event parity is enforced between the domain and event models but not against journal records, which is why this slipped through. | FBL-004 | Change control: add the events, or state explicitly that these transitions are journal-only. |
| PF-13 | MAJOR | The read-only-inventory acceptance row prescribes verification by comparing source sample **hashes**, but the preservation model states plainly that hash comparison cannot detect timestamp, extended-attribute, or permission mutation. As written the row can pass while the corresponding safety row is unproven. | FBL-026, FBL-072 | Change control: change the verification method to a property-set comparison and count access-time side effects. |
| PF-16 | MAJOR | `VAL-POLICY-OPEN` requires every `policy_ref` to name a **still-open** decision. The four provisional rules cite two decisions. The moment either closes, the shipped example fails loader validation until every provisional rule is simultaneously promoted or edited — at exactly the moment the rule set must be frozen for G4. No document states that rule promotion and decision closure are one atomic change. | FBL-035 | Change control: define promotion and closure as a single governed change. |
| PF-18 | MAJOR | "Unresolved" is a file state and a taxonomy destination, but `ReviewItem` has no unresolved state, while an acceptance row requires unresolved items to be visible and governed and a report class requires an unresolved queue. Whether the queue is a review-item reason code, a file-state projection, or a distinct report is undefined. | FBL-038 | Change control. |
| PF-20 | MAJOR | Approval subject types include five kinds — pilot gate, live gate, rollback authority, retirement authority, review exception — for which the permission model defines no authority class. The authority-class check is unevaluable for them. | FBL-044 | Change control: extend the permission vocabulary. |
| PF-28 | MAJOR | The review console is permitted to submit `grant_approval` — which may target an operation plan — while `approve_operation_plan` is forbidden and attempting it is a recorded safety event. Console-originated `grant_approval` on a plan is plan approval by another name. Either the forbidden list is over-broad or the forbidden command must be redefined as a backend-internal transition. | FBL-063 | Change control: disambiguate. The distinction is load-bearing for a safety-event trigger. |
| PF-29 | MAJOR | The approval scope's mode vocabulary is fixture, dry-run, pilot, live, and the authorization algorithm requires runtime mode to equal approved mode. The rule-set environment vocabulary is fixture and pilot only, with **no dry-run value at all**. At G4 the runtime mode is dry-run while no rule set can declare it. | FBL-045, FBL-072 | Change control: pin the relationship between the two vocabularies. |

### Minor findings and notes

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| PF-17 | MINOR | The classification decision lifecycle is written as a chain ending in `rejected`, but `rejected` is reachable from `review_required`, not only after `planned`. The approval entity uses correctly branched notation; this one does not. | Change control. |
| PF-26 | MINOR | The exclusions example sets a bundle policy of "treat as directory with bundle flag" and a symlink policy of "skip and record", both of which contradict the preservation overlays. These are non-production examples, but they are the only concrete config shape an implementer has. | Change control. |
| PF-27 | MINOR | `entry_type` is `file, directory, symlink` in the domain model and adds `bundle` in the inventory model. The inventory obligation rule resolves it, but the domain model is what an implementer generates from. The unqualified "directory entries may be represented minimally" also conflicts with the bundle overlay. | Change control. |
| PF-30 | MINOR | Destination placeholder vocabularies differ: the taxonomy model lists five, the rule schema permits six. The schema governs, but the taxonomy document owns the templates. | Change control. |
| PF-31 | NOTE | No single machine-readable registry existed for halt codes, approval rejection codes, validation codes, and stop codes, while several acceptance rows demand rejection logs *with reason codes*. **Already addressed** — the registry is a deliverable of FBL-005. | Closed by FBL-005. |

### Findings that also imply new operator decisions

Two findings cannot be resolved by change control alone because they change what a gate means:

- **OD-023 — G4 plan promotability.** Arising from PF-25. Whether a dry-run plan generated without a measured destination descriptor may ever be promoted, or whether destination characterization must open G5. Proposed `blocks_gate: dry_run`.
- **OD-024 — Symlink and hard-link reproduction scope.** Arising from PF-08. Whether V1 reproduces links faithfully, or declares link reproduction out of scope with a stop condition. Proposed `blocks_gate: implementation`.

Both are registered in `docs/05-governance/open-decisions.md`. Neither is decided here.
---

## Open-decision map (OD-001 … OD-024)

Every decision mapped to the earliest rung it affects. **No decision is resolved here.**

A rung whose **Blocked by** field names a decision must visibly stop before implementation — the implementation prompt's preconditions refuse to start.

| OD | Decision | Earliest rung | Gate blocked | Earlier rungs proceed? | Evidence required to resolve | Re-confirm | Authority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OD-001 | Exact share roots in and out of scope | FBL-071 | `dry_run` | Yes — all of G3 | Confirmed root list with authority tags | `live` | Operator |
| OD-002 | Destination taxonomy freeze | FBL-034 (names), FBL-071 | `dry_run` | Yes — schema work proceeds on fixtures | Frozen taxonomy version and hash | `live` | Operator |
| OD-003 | Identity-recognition privacy policy | FBL-071 | `dry_run` | Yes — the identity rule stays disabled | Written privacy policy; confirmation requirements | `live` | Operator |
| **OD-004** | **Hash algorithm** | **FBL-002** | `implementation` | **No** — this is the earliest G3 blocker | Algorithm, width, and whether it also governs the journal chain digest | — | Operator |
| OD-005 | Database and control-data location | FBL-013 | `dry_run` | Yes — fixture control storage suffices | Path outside every scanned root; `strong` durability class | `live` | Operator |
| OD-006 | Snapshot and versioning readiness | FBL-074 | `live` | Yes | Recovery posture confirmation | `retirement` | Operator |
| OD-007 | Pilot dataset selection | FBL-073 | `pilot` | Yes | Isolated corpus manifest | — | Operator |
| OD-008 | Batch size and stop thresholds | FBL-067 (real values), FBL-073 | `pilot` | Yes — fixture defaults suffice | Approved threshold sheet | `live` | Operator |
| OD-009 | Copy-first versus move per phase | FBL-075 | `live` | Yes | Frozen per-phase behaviour | `retirement` | Operator |
| OD-010 | Quarantine retention and future deletion | FBL-076 | `retirement` | Yes | Retention policy version | `migration_completion` | Operator |
| OD-011 | Temporary thumbnails and extracted text | FBL-032 | `dry_run` | Yes — extraction without retention proceeds | Privacy decision on derived artifacts | — | Operator |
| OD-012 | Confirm Dogs / drone / CSV / identity rules | FBL-071 | `dry_run` | Yes — rules stay structurally advisory | Handwritten transcriptions or equivalent | — | Operator |
| OD-013 | Confirmed live structure vs intended | FBL-074 | `live` | Yes | Reconciled structure record | `migration_completion` | Operator |
| **OD-014** | **Migration-control directory schema** | **FBL-013** | `implementation` | Partially — config-driven fixture defaults let FBL-013…FBL-020 proceed; final names must precede real control-directory creation | Confirmed control layout names | `dry_run` | Operator |
| OD-015 | Taxonomy edges and aliases | FBL-074 | `live` | Yes | Boundary decisions | — | Operator |
| **OD-016** | **Adapter choice** | **FBL-065** | `dry_run` | Yes — the capability contract makes G3 adapter-agnostic | Justified choice, **reviewed against the `retirement_capable` derivation from FBL-008** | — | Operator |
| **OD-017** | **Report format defaults** | **FBL-027** | `implementation` | Yes — engine logic proceeds; only report emission blocks | Chosen packaging | — | Operator |
| **OD-018** | **Alert wording** | **FBL-064** | `implementation` | Yes | Exact phrasing | `pilot` | Operator |
| **OD-019** | **Review console stack** | **FBL-063** | `implementation` | Yes — the console is deliberately last | Chosen stack | — | Operator |
| OD-020 | Project path on the NAS | FBL-075 | `live` | Yes — creating it is itself a live write | Creation timing | — | Operator |
| OD-021 | Migration completeness criteria and residual-exception tolerance | FBL-077 | `migration_completion` | Yes — FBL-068 is implementable; only its G8 package blocks | Tolerance and ownership rules | — | Operator |
| **OD-022** | **Operator authentication model** | **FBL-044** | `implementation` | Yes — everything through the immutable plan proceeds; nothing that *authorizes* does | Accepted authentication shape | `live` | Operator |
| **OD-023** | **G4 plan promotability** *(new — from PF-25)* | **FBL-072** | `dry_run` | Yes | Decision on whether a descriptor-incomplete plan may ever be promoted | — | Operator |
| **OD-024** | **Symlink and hard-link reproduction scope** *(new — from PF-08)* | **FBL-029** | `implementation` | Yes | Reproduce faithfully, or declare out of V1 scope with a stop condition | — | Operator |

### The six G3 blockers, and where each stops the ladder

The assignment asked for particular attention to decisions carrying `blocks_gate: implementation`. Each has a rung that visibly stops:

| OD | Rung that stops | Consequence if started anyway |
| --- | --- | --- |
| OD-004 | **FBL-002** | The digest type is baked into every contract and stored fingerprint; changing it later invalidates every hash and every journal chain already written. This is the earliest possible stop, by design. |
| OD-014 | FBL-013 | Control-directory names would be created under a schema the operator has not confirmed. Mitigated: fixture defaults are config-driven. |
| OD-017 | FBL-027 | Report packaging would be chosen by the implementer. Engine logic is unaffected. |
| OD-018 | FBL-064 | Alert phrasing would be invented. Sentinel is late, so the cost is near zero. |
| OD-019 | FBL-063 | Console stack chosen by the implementer. The console is deliberately last, so the cost is near zero. |
| OD-022 | **FBL-044** | An authentication model would be invented for the component holding destructive authority. This is the correct cut: everything through the sealed immutable plan is buildable; nothing that *authorizes* is. |

Two new decisions — OD-023 and OD-024 — arise from planning findings and are registered for operator resolution.

---

## Acceptance coverage

### How the four acceptance families map

| Family | Count | Verified at | Mapping |
| --- | --- | --- | --- |
| `FND-ACC-*` | 41 | **G1, already satisfied** | Documentary. Satisfied by the Foundation approval at `54ec3a8`. Several are re-verified as executable regressions inside G3 rungs, noted per rung. **Not rung-blocking.** |
| `SAF-*` | 10 | G1 documentary; executable counterparts at G3 | See below. |
| `V1-ACC-*` | 40 | G3 and later | Every row mapped. |
| `PILOT-*` | 14 | G5 | FBL-073, plus fixture halves at FBL-066, FBL-062, FBL-057. |
| `LIVE-*` | 12 | G6 | FBL-074, sourced from earlier rungs. |

### V1-ACC coverage

| Row | Rung | Row | Rung |
| --- | --- | --- | --- |
| V1-ACC-001 | FBL-026, FBL-072 | V1-ACC-035 | FBL-047, FBL-076 |
| V1-ACC-002 | FBL-003, FBL-026 | V1-ACC-036 | **FBL-057** |
| V1-ACC-003 | FBL-003, FBL-026 | V1-ACC-037 | FBL-038, **FBL-058** |
| V1-ACC-004 | FBL-025, FBL-026 | V1-ACC-038 | FBL-047, **FBL-063** |
| V1-ACC-005 | FBL-022, FBL-023, FBL-028 | V1-ACC-039 | FBL-045, **FBL-047** |
| V1-ACC-006 | FBL-024, FBL-025 | V1-ACC-040 | FBL-053, **FBL-073** |
| V1-ACC-010 | FBL-025, FBL-033, FBL-039 | V1-ACC-041 | FBL-027, FBL-038 |
| V1-ACC-011 | FBL-033, FBL-039 | V1-ACC-042 | FBL-001, **FBL-058** |
| V1-ACC-012 | FBL-039 | V1-ACC-044 | FBL-049, FBL-053 |
| V1-ACC-020 | FBL-036, FBL-037 | V1-ACC-045 | **FBL-054, FBL-055, FBL-056** |
| V1-ACC-021 | FBL-036, FBL-038 | V1-ACC-046 | FBL-013, **FBL-016** |
| V1-ACC-022 | FBL-034, FBL-036 | V1-ACC-047 | **FBL-018** |
| V1-ACC-023 | FBL-037, FBL-038 | V1-ACC-050 | FBL-073, **FBL-075** |
| V1-ACC-024 | FBL-032, FBL-036 | V1-ACC-052 | **FBL-064** |
| V1-ACC-025 | FBL-036 | V1-ACC-053 | FBL-068, **FBL-077** |
| V1-ACC-026 | **FBL-035** | V1-ACC-054 | FBL-069, FBL-079 |
| V1-ACC-030 | FBL-041, **FBL-043** | V1-ACC-055 | G1 documentary |
| V1-ACC-031 | FBL-041, FBL-045 | V1-ACC-043 | G1 documentary (relocated) |
| V1-ACC-032 | FBL-024, FBL-047, FBL-061 | V1-ACC-051 | G1 documentary (relocated) |
| V1-ACC-033 | FBL-042, **FBL-050** | | |
| V1-ACC-034 | FBL-048, **FBL-052** | | |

### PILOT coverage

All fourteen rows are evaluated at G5 in **FBL-073**, sourced from earlier rungs:

| Row | Source rung | Row | Source rung |
| --- | --- | --- | --- |
| PILOT-001 | FBL-073 (dataset) | PILOT-008 | FBL-051 (thresholds) |
| PILOT-002 | FBL-073 (isolation) | PILOT-009 | FBL-073 (exceptions) |
| PILOT-003 | FBL-047 (approval) | PILOT-010 | FBL-039 (duplicates) |
| PILOT-004 | FBL-052, FBL-053 | PILOT-011 | FBL-050 (vault) |
| PILOT-005 | FBL-042 (collision) | PILOT-012 | FBL-057 (interruption) |
| PILOT-006 | FBL-062 (rollback drill) | PILOT-013 | FBL-038 (unresolved) |
| PILOT-007 | FBL-072 (dry-run review) | PILOT-014 | FBL-001, FBL-053 (readability) |

### LIVE coverage

All twelve rows are evaluated at G6 in **FBL-074**, sourced as:

| Row | Source | Row | Source |
| --- | --- | --- | --- |
| LIVE-001 | authorization ledger, G1–G5 entries | LIVE-007 | OD-010 retention policy |
| LIVE-002 | OD-006 recovery posture | LIVE-008 | OD-013 structure confirmation |
| LIVE-003 | FBL-072 confirmed roots | LIVE-009 | FBL-073 pilot package |
| LIVE-004 | FBL-051 thresholds | LIVE-010 | FBL-050 vault enforcement |
| LIVE-005 | FBL-072 control-data declaration | LIVE-011 | FBL-076 retirement flags off |
| LIVE-006 | OD-009 copy-versus-move | LIVE-012 | FBL-064 Sentinel authority |

All 40 rows are mapped. Sparse numbering (007–009, 013–019, 027–029, 048–049) is by design in the acceptance file, not a gap.

### SAF coverage — documentary at G1, executable at G3

| Row | Executable counterpart | Rung |
| --- | --- | --- |
| SAF-001 | Read-only inventory proven by property-set comparison | FBL-026 (see PF-13) |
| SAF-002 | Retirement as a separate journalled operation | FBL-076 |
| SAF-003 | Retirement gated on preservation, not hash alone | FBL-053, FBL-076 |
| SAF-004 | Protected-vault refusal | FBL-050 |
| SAF-005 | CI secret scan | **FBL-001** |
| SAF-006 | CI live-path guard | **FBL-001** |
| SAF-007 | Hostile-path fixtures | **FBL-060** |
| SAF-008 | AI evidence cannot yield an executable outcome | FBL-035, FBL-036 |
| SAF-009 | Sentinel authority refusal | FBL-064 |
| SAF-010 | No permanent deletion anywhere | FBL-056, FBL-076 |

Three of these — SAF-005, SAF-006, SAF-007 — had **no implementing rung** in the required list. They are now owned.

---

## Coverage of the required topics

All 47 topics the assignment required are covered. Re-sequenced items are marked.

| # | Topic | Rung(s) | # | Topic | Rung(s) |
| --- | --- | --- | --- | --- | --- |
| 1 | Reproducible repository tooling | FBL-001 | 25 | Immutable planning | FBL-041 |
| 2 | Typed contracts | FBL-002, FBL-003 | 26 | Approval binding | FBL-044, FBL-045 |
| 3 | Event contracts | FBL-004 | 27 | Backend authorization | FBL-047 |
| 4 | Canonical rule loader and validator | FBL-035 | 28 | Dry-run planner | FBL-043 |
| 5 | Fixture-corpus generator | FBL-006, FBL-011 | 29 | Synthetic copy engine | FBL-048 |
| 6 | Synthetic filesystem adapter | FBL-009 | 30 | Collision enforcement | FBL-042, FBL-050 |
| 7 | Adapter capability interface | FBL-008 | 31 | Protected-vault enforcement | FBL-050 |
| 8 | File identity and generation tokens | FBL-023, FBL-024 | 32 | Verification | FBL-052 |
| 9 | Read-only fixture inventory | FBL-026 | 33 | Preservation comparison | FBL-053 |
| 10 | Inventory manifests and totals | FBL-027 | 34 | Fault-injection harness | **FBL-007 — moved early** |
| 11 | Authoritative journal | FBL-013, FBL-014, FBL-016 | 35 | Interruption recovery | FBL-054…FBL-057 |
| 12 | SQLite projection | FBL-017 | 36 | Copied-pilot orchestration | FBL-066, FBL-073 |
| 13 | Atomic checkpoints | FBL-019 | 37 | Review console | **FBL-063 — moved late** |
| 14 | Restart and replay | FBL-018, FBL-020 | 38 | Sentinel | **FBL-064 — moved late** |
| 15 | Crash-state recovery | FBL-054, FBL-055, FBL-056 | 39 | Dry-run readiness | FBL-070, FBL-072 |
| 16 | Hashing | FBL-025 | 40 | Copied-pilot readiness | FBL-073 |
| 17 | Metadata extraction | FBL-032 | 41 | Live-readiness preparation | FBL-074 |
| 18 | Preservation profiles | **FBL-040 / FBL-053 — split** | 42 | Read-only NAS adapter enablement | **FBL-065 / FBL-071 — split** |
| 19 | Taxonomy contracts | **FBL-034 — moved before rules** | 43 | Limited live copying | FBL-075 |
| 20 | Rule evaluation | FBL-036 | 44 | Source-retirement readiness | FBL-076 |
| 21 | Deterministic conflict handling | FBL-036 | 45 | Final reconciliation | FBL-068, FBL-077 |
| 22 | Classification proposals | FBL-037 | 46 | Migration completion | FBL-078 |
| 23 | Review and unresolved queues | FBL-038 | 47 | Maintenance mode | FBL-069, FBL-079 |
| 24 | Duplicate grouping | **FBL-033 / FBL-039 — split** | | | |

### Rungs added beyond the required list

Six rungs exist because the required list had no owner for work the specifications demand:

| Rung | Why it was added |
| --- | --- |
| FBL-021 | Symbolic root registry — required by two loader checks, owned by nothing. |
| FBL-051 | Threshold and stop-condition governor — three acceptance rows and a halt branch depended on it. |
| FBL-058 | Observability and redaction — two BLOCKER acceptance rows were unowned. |
| FBL-059 | Incident and reason-code surface — ~46 reason codes were untested strings. |
| FBL-060 | Hostile-path fixtures — a safety row demanded fixtures the corpus never enumerated. |
| FBL-070 | G4 readiness assembler — the bundle had no producer. |
