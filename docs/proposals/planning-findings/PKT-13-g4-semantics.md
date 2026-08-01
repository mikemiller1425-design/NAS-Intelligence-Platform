# PKT-13 — G4 semantics: runtime mode and descriptor completeness (PF-25, PF-29)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-25 (BLOCKER), PF-29 (MAJOR) |
| Highest severity | BLOCKER |
| Change-control batch | BATCH-13 |
| Operator decision required | **OD-023** — one question, stated below. The structural half proceeds without it. |
| Blocked rungs | FBL-045, FBL-072, FBL-073 |
| Affected acceptance | V1-ACC-030, V1-ACC-034 |
| Depends on | **PKT-03** (PF-19 — the plan has no descriptor fields), **PKT-01** |

These two are inseparable in a specific way: **PF-25's rule PL-D4 is written in terms of
`runtime_mode`, an enum PF-29 shows is defined nowhere.** PL-D4 is literally unwritable until PF-29
lands.

## The exact contradiction

### PF-25 — a G4 plan cannot carry a measured destination descriptor

- `preservation-model.md:151` (CD-1) — "A descriptor is valid only if produced by an actual fixture
  characterization run. **Assumed or hand-written descriptors are invalid** and may not gate any
  operation."
- `file-identity-model.md:228` (UN-5) — a round-trip check, "**write an NFD name, read it back**",
  is a required characterization test and a **required field** of the descriptor.
- `preservation-model.md:172,152` — the resolved profile and **both** descriptor ids are frozen into
  the plan at approval.
- Against `gate-model.md:113–116` — G4 does not authorize "any create, update, delete, rename, or
  **write-based probe** on **any NAS path**, source or destination… destination capability
  characterization, which requires a write and therefore remains at G5" — while `:107` makes
  destination proposal a G4 authorization.
- The ladder already assumes a marker no entity has: "dry-run plan **marked descriptor-incomplete**"
  (`build-ladder.md:2138`). Yet `OperationPlan` required fields (`domain-model.md:720–734`) contain
  **no descriptor fields at all.**

### PF-29 — approval scope mode and rule-set environment are unrelated vocabularies

- `approval-binding-model.md:72` — `mode: "pilot"  # fixture | dry_run | pilot | live`, with AUTHZ-01
  requiring "Runtime mode is enabled and **equals the approved mode**" → `APR-E01_MODE_MISMATCH`,
  "Halt run".
- Against `classification-rule-set.schema.json:570–573` and `rule-model.md:42` — `environment` is
  `fixture | pilot`. **No `dry_run` value at all.**
- G4's mode is `dry_run` (`gate-model.md:33`), and G4 requires the rule set to be frozen and to
  validate against the canonical schema (`:121`).
- A third vocabulary: `config/examples/thresholds.example.yaml:6–8` expresses modes as two booleans,
  `dry_run_default` / `live_mode`, which cannot represent `fixture` or `pilot` at all.
- **No document defines "runtime mode" as an enum anywhere** — a repository search returns only
  usages.
- **Fourth and worst:** `rule_set.environment` participates in **no AUTHZ step**. Nothing requires it
  to be compatible with the runtime mode, so a `fixture` rule set could today back a `live` approval
  and no check would notice. **The absence of a relationship is as much the defect as the mismatch.**

## Operational consequence if left unresolved

**PF-25 — sharper than the ladder states.** `preservation-model.md:28` (PC-1) forces every unmeasured
property to `unsupported_reported`; `:163` classifies that as MM-2; `:169` **blocks** MM-2 entries. A
G4 plan therefore contains **zero proceedable entries**, making V1-ACC-030's "produces plans" evidence
degenerate. And the ladder's own negative test — "A destination-side property is recorded
`unsupported_reported`, not assumed" (`:2112`) — **actively prescribes the state that blocks the
plan.** The alternative path is that the implementer fabricates a descriptor, violating CD-1, after
which AUTHZ-23 and `APR-E26` compare against a fabricated value.

**PF-29.** At G4 the runtime mode is `dry_run` while the frozen rule set can declare only `fixture` or
`pilot`, and `approval_scope` is "Derived server-side from the plan and the **active mode
configuration**" — a configuration with no `dry_run` value. Either every G4 approval halts on
`APR-E01_MODE_MISMATCH`, or the implementer invents an undocumented mapping. Taking the only
non-`fixture` value available labels the G4 rule set `pilot` — **mislabeling the very artifact whose
freeze is a G4 entry criterion and whose hash is bound into every approval.**

## Affected domain entities and fields

`OperationPlan` — five new required fields. `RuleSet.environment` and the taxonomy envelope's
`environment` — meaning pinned, enum unchanged. Journal records `plan_bound` and `run_open`.

## Affected events, commands, reason codes, and persistence records

New stop code `STOP-PLAN-NOT-PROMOTABLE`. New reject code
`APR-E27_RULESET_ENVIRONMENT_INCOMPATIBLE`, added to the table at `approval-binding-model.md:199–228`.
New authorization step AUTHZ-12a. New preservation rules CD-4 and CM-P3. New descriptor value
`unavailable_gate_prohibited`.

## Proposed normative resolution

### PF-29 — define runtime mode once; make `environment` a ceiling

Insert into `approval-binding-model.md` before `:116` a *Runtime mode* section:

> `runtime_mode` is the single authoritative operating-mode value, **derived by the backend from the
> authorized gate recorded in the authorization ledger** — never read from configuration, never
> supplied by a client, never inferred from a rule set.
>
> | Value | Gate | NAS access |
> | --- | --- | --- |
> | `fixture` | G3 | none |
> | `dry_run` | G4 | read-only |
> | `pilot` | G5 | bounded write to an isolated copied corpus |
> | `live` | G6+ | bounded write to live shares |
>
> `approval_scope.mode` takes a value from this enum and no other. The modes configuration digested
> into `config_modes_hash` is the set of operator-set switches that **constrain** the mode —
> `allow_source_retirement`, `allow_delete`, `allow_overwrite_protected_vaults` — **never the mode
> itself**; a modes configuration purporting to set the mode is rejected. `runtime_mode` is bound into
> the `run_open` journal record and is immutable for the life of the run; a mode change requires a new
> run.

Replace `rule-model.md:42`: `environment` declares the **highest-consequence runtime mode** under
which the set may be evaluated. `fixture` permits `{fixture, dry_run}`; `pilot` permits
`{fixture, dry_run, pilot}`; `live` remains deliberately absent from schema version 1. **Environment
is a ceiling, never an assertion about the current run.**

New authorization step after AUTHZ-12: **AUTHZ-12a** — "The active rule set's `environment` permits
the runtime mode per the compatibility matrix in `rule-model.md`; the active taxonomy's `environment`
permits it likewise." → `APR-E27_RULESET_ENVIRONMENT_INCOMPATIBLE`, batch effect "Halt run".

> **The decisive property: no schema change is required.** `environment` keeps its two-value enum;
> only its *meaning* is pinned. `classification-rules.example.yaml:16` (`environment: fixture`)
> becomes G4-legal **without edit**, so FBL-035's prohibition on changing the schema is respected.
> `thresholds.example.yaml`'s structure is unchanged; only its documented semantics are corrected to
> "constraint switches, not a mode selector."

### PF-25 — make a dry-run plan structurally distinguishable

Extend `OperationPlan` required fields:

| Field | Type | Required | Nullable | Notes |
| --- | --- | --- | --- | --- |
| `source_adapter_descriptor_id` | string | yes | **no** | |
| `destination_adapter_descriptor_id` | string | yes | yes | Null at G4 by PL-D4. |
| `preservation_profile_id` | string | yes | yes | |
| `descriptor_completeness` | enum `complete \| source_incomplete \| destination_incomplete \| incomplete` | yes | **no** | Never defaulted. |
| `promotability` | enum `promotable \| not_promotable` | yes | **no** | **Derived**, never client-supplied. |

| ID | Invariant |
| --- | --- |
| PL-D1 | `complete` requires both ids non-null **and** both referenced descriptors carrying `measured_at` and `attestation_evidence_ref`. An id resolving to a hand-written descriptor is rejected **at plan seal**, not at execution. |
| PL-D2 | `promotable` requires `complete`. Any other completeness yields `not_promotable` **by construction**, derived from the plan's contents, never asserted. |
| PL-D3 | A `not_promotable` plan may not be the `subject_id` of an `Approval` whose `approval_scope.mode ∈ {pilot, live}`. The attempt rejects `APR-E17_SCOPE_VIOLATION` at AUTHZ-16 **and is a recorded safety event.** |
| PL-D4 | A plan generated under `runtime_mode: dry_run` records `destination_adapter_descriptor_id: null` and `descriptor_completeness: destination_incomplete`, and may **never** record a destination descriptor obtained by any means other than a measured characterization run against that endpoint. |
| PL-D5 | Characterizing a destination produces a **new** descriptor; it never completes an existing plan. A `destination_incomplete` plan is **superseded** by a new version, never edited. |

New preservation rules:

> **CD-4** — A descriptor may be produced only under a gate authorizing a write to the endpoint being
> characterized. At G4 a run records `destination_descriptor: unavailable_gate_prohibited`, a value
> **distinct from `unsupported_reported` and from `unknown`**. Recording `unsupported_reported` for a
> property never probed is prohibited, because it asserts a measurement that did not occur.
>
> **CM-P3** — The mismatch-resolution protocol runs only against a `complete` plan. For
> `destination_incomplete` it is **not run**, and the plan records
> `mismatch_classification: deferred_pending_destination_characterization`. Deferral is not an MM
> class, never resolves to MM-0, and never satisfies the retirement gate.

**CD-4 and CM-P3 together are what prevent the degenerate all-blocked G4 plan.**

**Journal sequencing, and it is a hard constraint.** `plan_bound` must carry `descriptor_completeness`
and `promotability`, and `run_open` must carry `runtime_mode`, **from the first record written**.
Records are append-only and hash-chained (ADR-013:9), so a later field addition changes canonical
serialization and breaks every chain already written. **These land at FBL-005 and FBL-041, not
later.**

## Alternatives considered

**PF-25 — permit a hand-written descriptor marked provisional.** Rejected: CD-1 says assumed
descriptors "may not gate any operation", and a descriptor gating plan construction *is* gating an
operation. It also creates a second validity tier AUTHZ-23 would have to reason about, weakening a
check whose entire value is that it is binary.

**PF-25 — reuse the source descriptor when both endpoints share an adapter class.** Rejected: CD-3
requires re-characterization after any "**endpoint change**". Same class is not same endpoint, and
case and normalization sensitivity are per-volume.

**PF-29 — add `dry_run` to the `environment` enum.** Rejected: a schema change to frozen Foundation
content that implies a *fourth* vocabulary rather than eliminating one; it leaves `live` handling
asymmetric for reasons no reader could derive; and it conflates "which mode may evaluate this set"
with "which mode is running" — **the original error restated in the schema.**

**PF-29 — drop `mode` from `approval_scope` and derive it from `config_modes_hash`.** Rejected:
ADR-009:12 makes mode part of the bound scope by decision, and two booleans cannot express the
four-way ordering AUTHZ-01 compares or the four-row expiry table.

## Safety implications

**PF-25 — global invariant 12** (hash equality never sufficient) and **ADR-009's dry-run boundary**.
Without these fields a G4 plan and a G5 plan are **structurally identical**, and only the gate
ceremony — a procedural control — prevents executing an uncharacterized plan. PL-D3 treats "promote an
uncharacterized plan" as an attack signature, not a user error.

**PF-29 — ADR-009 and global invariant 24.** `environment` as a ceiling means a fixture rule set can
never be evaluated under `pilot` or `live` even by accident — a property **entirely absent before**,
since environment participated in no check. AUTHZ-12a sits immediately after the rule-set hash
comparison, so drift in *which* rule set and drift in *whether it may run here* are caught at adjacent
steps. Deriving `runtime_mode` from the ledger means the mode **cannot be widened by editing a config
file**; it requires a gate authorization record, which `gate-model.md:24` already makes mandatory and
non-inferable.

## Migration and compatibility implications

`environment` keeps its enum, so all 48 shipped rule files validate unchanged and
`thresholds.example.yaml` needs no structural edit. The `OperationPlan` fields and the two journal
payload additions are the migration cost, and they are free only if taken at FBL-005/FBL-041 — see the
sequencing constraint above.

## Required tests

**Positive** — a fixture pair with both measured descriptors yields `complete` / `promotable` and MM-0
throughout; a `dry_run` plan yields `destination_incomplete` / `not_promotable` **and still enumerates
entries with resolved destination paths**; `environment: fixture` under `runtime_mode: dry_run` passes
AUTHZ-12a; `runtime_mode` derived from the G4 authorization record matches `approval_scope.mode` at
AUTHZ-01.

**Negative** — `promotable` asserted with a null destination descriptor (PL-D2); a `not_promotable`
plan as the subject of a `pilot`-scoped approval → `APR-E17` **plus a safety event** (PL-D3); an id
resolving to `measured_at: null` rejected at plan seal (PL-D1); a `dry_run` plan recording any
destination descriptor (PL-D4); editing a `destination_incomplete` plan to add a descriptor —
supersession required (PL-D5); a `destination_incomplete` plan carrying MM classifications (CM-P3);
`environment: fixture` under `pilot` → `APR-E27` plus halt; any environment under `live` → `APR-E27`
plus halt; a modes configuration asserting a mode value rejected; `approval_scope.mode` supplied by a
client → `APR-E25`; a mid-run mode change refused.

**Failure-injection** — `promotability: promotable` supplied by a client → `APR-E25`; **a G4 run
attempting an NFD round-trip probe against a destination must fail and halt *before* the write**; a
descriptor re-measured between seal and execution fires IT-16 and `APR-E26`; a
`deferred_pending_destination_characterization` plan must never satisfy the retirement gate. Editing
`thresholds.example.yaml` to `live_mode: true` **must not change `runtime_mode`** and must fire IT-08,
invalidating outstanding approvals. A run whose `run_open` records `dry_run` attempting a
`pilot`-scoped approval → `APR-E01` at AUTHZ-01 **before** AUTHZ-12a — the coarser check must fire
first. A rule set whose `environment` was edited after the hash was bound → `APR-E13_RULESET_CHANGED`
at AUTHZ-12, **not** `APR-E27`.

## Required documentation changes

`approval-binding-model.md` before `:116` (runtime mode), `:133` (AUTHZ-12a), `:199–228` (`APR-E27`);
`rule-model.md:42` (the ceiling); `domain-model.md:720–734` (the five plan fields);
`preservation-model.md` (CD-4, CM-P3); `gate-model.md:116`;
`durability-and-recovery-model.md:110–111` (the two payload additions);
`config/examples/thresholds.example.yaml` documented semantics.

## Required ADR changes

**ADR-009** — append to Decision: "`runtime_mode` is a single four-value enum — `fixture`, `dry_run`,
`pilot`, `live` — derived by the backend from the authorized gate recorded in the authorization
ledger, never from configuration and never from a client. A rule set's and a taxonomy's `environment`
declares the highest-consequence runtime mode under which it may be evaluated: a ceiling rather than
an assertion about the current run, checked at authorization time." Append to Consequences: "A dry-run
plan is structurally distinguishable from an executable one — it records
`descriptor_completeness: destination_incomplete` and `promotability: not_promotable`, because a
destination descriptor is obtainable only by writing to that destination, which no dry-run gate
authorizes. The distinction is a field on the plan, not a convention of the run."

**ADR-012** — append to Decision: "A descriptor may be produced only under a gate authorizing a write
to the endpoint characterized. A property never probed is recorded as unprobed, never as
unsupported."

**ADR-015** — append to Consequences: "Promotability is derived from the plan's contents, not granted
by a stage transition."

## Operator policy, or pure specification defect?

**PF-29 is a pure specification defect.** The gate ladder and its `blocks_gate` values already exist;
this only names the enum they imply and connects two vocabularies that were never connected. The
*values* of the constraint switches remain the operator's, unchanged and untouched, and remain pinned
`false` in V1.

**PF-25's structural half is required whatever is decided** — the five fields, PL-D1…PL-D5, CD-4,
CM-P3, the stop code, the journal fields, and the `gate-model.md:116` amendment. Both candidate
answers need a machine-readable marker distinguishing characterized from uncharacterized plans.

**The single operator question, unanswered — OD-023:** *whether a `destination_incomplete` plan may
ever be promoted, or whether destination characterization must open G5.*

> One observation that **constrains without deciding**: because plans are immutable after approval
> (`domain-model.md:19,759`), "characterize at G5, then complete the existing G4 plan" is
> **structurally unavailable regardless of policy**. The coherent options are exactly two —
> never-promotable, or superseded-by-a-characterized-version. That is analysis of an existing
> invariant, not a decision, and **Claude has not decided between the two.**

**Separately surfaced and not answered:** OD-023's text does not cover whether the isolated pilot
zone's descriptor may stand in for the authoritative destination's at G6, given CD-3's endpoint-change
rule. FBL-073 characterizes the destination as "confined to the isolated pilot zone"
(`build-ladder.md:2162`), but G6 writes to live shares — a different endpoint. **This packet
recommends an OD-023 scope amendment or a new registered decision, and proposes neither answer.** It is
carried as a proposed decision in `OD-025-PROPOSED.md` rather than added to the authoritative register.

## Atomicity

PL-D4 is written in terms of `runtime_mode` and is unwritable until PF-29 defines that enum; PF-29's
compatibility matrix is what makes a G4 plan legally constructible at all. **PKT-03 (PF-19)** is a hard
prerequisite — the plan has no descriptor ids, so a completeness flag would be a flag over nothing.
**PKT-03 (PF-04)** supplies the `AdapterCapabilityDescriptor` entity whose fields PL-D1 references.
**PKT-09 (PF-15)** — the taxonomy envelope needs the identical `environment` field and matrix, or it
becomes the fourth vocabulary the instant it is published. **PKT-10 (PF-16)** — G4 evaluates register
state, rule-set freeze, and mode compatibility as one gate decision. **PKT-06 (PF-13)** — FBL-072's
verification method.

## Verification procedure

Re-run `foundation_self_review.py` and `validate_rule_config.py` (all 48 files unchanged).
Independently: grep for a definition of `runtime_mode` and confirm exactly one normative enum exists;
confirm `gate-model.md:113–116` and the new CD-4 agree that no G4 write-based probe is authorized;
confirm `plan_bound` and `run_open` payload descriptions list the new fields.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for OD-023.
**This packet is non-authoritative and confers no authority of its own.**
