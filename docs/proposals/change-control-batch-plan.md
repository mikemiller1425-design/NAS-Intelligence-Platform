# Change-control batch plan

> **Non-authoritative.** This plan proposes a sequence in which the unresolved planning findings and
> stress-test findings could be resolved. It resolves nothing, authorizes nothing, and changes no
> specification. Adopting any batch requires change-control approval, and every operator decision
> named below remains the operator's.

Fifteen batches. **Batches 01 through 13 correspond one-to-one with the remediation packets under
`docs/proposals/planning-findings/`** — batch *N* is packet *N*. Batches 14 and 15 carry the
stress-test findings from `docs/audits/build-ladder-stress-test.md`, which have no planning-finding
packet.

The ordering is a dependency order, not a priority order. Where two batches have no dependency
between them they may run concurrently, with one exception stated in BATCH-03 and BATCH-05.

## Why BATCH-01 is first

Measured against the ladder's own blocking graph:

| Scenario | Reachable G3 rungs |
| --- | --- |
| Today | **3 of 70** |
| Every decision resolved, no finding resolved | 4 of 70 |
| Every finding resolved, no decision resolved | 3 of 70 |
| OD-004 plus every finding resolved | 12 of 70 |
| Everything resolved | 70 of 70 |

**OD-004 alone gates 67 of 70 G3 rungs**, because it blocks FBL-002 — the prerequisite of the entire
contract chain. No other single resolution moves the frontier. That is why the hash-algorithm
decision, which reads like a detail, is the first thing on this plan.

## Batches

## BATCH-01 — Digest and canonical serialization

| Field | Value |
| --- | --- |
| Packet | `PKT-01-canonicalization` |
| Findings resolved | PF-09 |
| Decisions required | **OD-004** — hash algorithm |
| Documents changed | `durability-and-recovery-model.md` (the canonicalization section), `approval-binding-model.md`, ADR-004 |
| Prerequisites | None. **This batch is first**, and nothing else can be correct before it. |
| Why atomic | OD-004 alone gates 67 of 70 G3 rungs, because it blocks FBL-002 — the prerequisite of the entire contract chain. This is the only batch that moves the reachable frontier on its own. |
| Acceptance impact | V1-ACC-031, V1-ACC-039, FND-ACC-043, FND-ACC-045 |
| Ladder impact | Unblocks FBL-002, and through it FBL-005 and FBL-045. |
| Validation | `validate_rule_config.py`, `foundation_self_review.py` check 11. Independently: serialize one fixture object under two runtimes and diff the digests. |
| Review authority | Chief Systems Architect. The operator answers OD-004 only. |
| Rollback | Documentation-only until a digest is written. **After any journal exists this batch is irreversible** — see the packet's migration section. |

## BATCH-02 — Journal authority and record vocabulary

| Field | Value |
| --- | --- |
| Packet | `PKT-02-journal-authority` |
| Findings resolved | PF-01, PF-02, PF-05 |
| Decisions required | None registered. **PF-02 has two legitimate resolutions with materially different consequences and warrants architect sign-off.** |
| Documents changed | `durability-and-recovery-model.md` (authority statement and record registry), ADR-005, ADR-016 |
| Prerequisites | BATCH-01 (record preimages). |
| Why atomic | One authority rule, one record registry, one read discipline, across the same two normative surfaces. PF-01's recommended resolution presupposes nonce record types PF-05 says do not exist, so sequential resolution produces intermediate self-contradicting states. |
| Acceptance impact | V1-ACC-039, V1-ACC-046, **V1-ACC-047**, FND-ACC-043 |
| Ladder impact | Unblocks FBL-005, FBL-017, FBL-018, FBL-047. |
| Validation | `foundation_self_review.py` checks 10 and 11. Confirm the golden-journal fixture pair matches whichever rebuild scope is chosen. |
| Review authority | Chief Systems Architect must sign off the PF-02 branch explicitly. It is an architecture trade, not a defect with one answer. |
| Rollback | Option B is documentation-only and reversible. Option A grows the journal format and requires a version bump. |

## BATCH-03 — Domain entity completion

| Field | Value |
| --- | --- |
| Packet | `PKT-03-domain-entities` |
| Findings resolved | PF-04, PF-07, PF-10, PF-11, PF-19, PF-21, PF-23, PF-24, PF-27 |
| Decisions required | None |
| Documents changed | `domain-model.md`, `inventory-model.md`, `preservation-model.md`, ADR-012, ADR-017 |
| Prerequisites | BATCH-01 (`EvidenceBundle` and report hashing). |
| Why atomic | FBL-003 is the sole home for domain entities and forbids inventing any field the specification omits. Under the G3 Definition of Done a later rung cannot legally add an entity to the contracts package, so every one of these must land before FBL-003 is authorized. This is stress-test finding BLT-B02. |
| Acceptance impact | V1-ACC-002, V1-ACC-003, V1-ACC-005, V1-ACC-031, V1-ACC-034, V1-ACC-039, V1-ACC-044, FND-ACC-001, FND-ACC-004 |
| Ladder impact | Unblocks FBL-003 and, downstream, FBL-008, FBL-025, FBL-028, FBL-040, FBL-041, FBL-045, FBL-052, FBL-053. |
| Validation | `foundation_self_review.py` checks 1 and 22; `validate_build_ladder.py`. |
| Review authority | Chief Systems Architect. |
| Rollback | Cheap now, expensive after FBL-003 is built — which is the entire argument for this batch's grouping. |

## BATCH-04 — Link and content-class operation semantics

| Field | Value |
| --- | --- |
| Packet | `PKT-04-link-and-content-class` |
| Findings resolved | PF-08, PF-26 |
| Decisions required | **OD-024** — link reproduction scope. It sets **one enum value**; everything else proceeds without it. |
| Documents changed | `domain-model.md`, `operation-model.md`, `permission-model.md`, `config/exclusions/exclusions.example.yaml`, ADR-002, ADR-012 |
| Prerequisites | BATCH-03 (`HardLinkSet`, the `bundle` enum value). |
| Why atomic | The legal value set of `symlink_operation_policy` is exactly PF-08's `link_reproduction_mode`. Defining them in two cycles risks two vocabularies for one switch. |
| Acceptance impact | V1-ACC-005, V1-ACC-041, V1-ACC-044, V1-ACC-053 |
| Ladder impact | Unblocks FBL-031 and FBL-049. **Also proposes moving OD-024's block off FBL-029**, which the packet argues is fully implementable on the specification half alone. |
| Validation | `validate_build_ladder.py`, `validate_proposals.py`. Confirm both models list seven identical entry types. |
| Review authority | Change control, plus the operator for OD-024's value only. |
| Rollback | Documentation and example-config only; `status: non_production_example` confirms nothing production derives from it. |

## BATCH-05 — Copy-window integrity

| Field | Value |
| --- | --- |
| Packet | `PKT-05-copy-window-integrity` |
| Findings resolved | PF-14, PF-22 |
| Decisions required | None |
| Documents changed | `durability-and-recovery-model.md` (phases B–E, phases BA–BF, record registry, crash-state table), `event-model.md`, `domain-model.md`, `tests/fixtures/README.md`, ADR-002, ADR-004, ADR-011, ADR-016 |
| Prerequisites | BATCH-03 (`source_recheck` scope, `VerificationResult` token fields), BATCH-04 (bundle-internal symlinks). |
| Why atomic | A bundle's members are read over an extended window and can be mutated mid-read exactly as a single file can. **Resolved in separate cycles, the bundle path ships without the token gate** — reproducing PF-22's defect in a newer protocol with no fixture yet written to catch it. Both also amend the same crash-state table and the same record registry. |
| Acceptance impact | V1-ACC-006, V1-ACC-032, V1-ACC-034, V1-ACC-036, V1-ACC-037, V1-ACC-041, V1-ACC-044, **V1-ACC-045**, PILOT-004 |
| Ladder impact | Unblocks FBL-031, FBL-048, FBL-052, FBL-054 through FBL-057. |
| Validation | `foundation_self_review.py`, `validate_build_ladder.py`. Count the crash-state rows and confirm 25; confirm `SourceMutatedDuringCopy` appears in both the domain and event models. |
| Review authority | Chief Systems Architect. **This is the batch with the most direct data-loss consequence in the set.** |
| Rollback | Documentation-only while no journal exists. **Must land adjacent to BATCH-03** — see that packet's cross-packet constraint. |

## BATCH-06 — Proving read-only inventory

| Field | Value |
| --- | --- |
| Packet | `PKT-06-read-only-proof` |
| Findings resolved | PF-13 |
| Decisions required | None. OD-008 is adjacent and does not block. |
| Documents changed | `v1-acceptance.md:15`, `safety-acceptance.md:7`, `preservation-model.md` (a new report schema), `build-ladder.md` FBL-026 and FBL-072 evidence packages, ADR-001 |
| Prerequisites | None. **Deliberately decoupled** from BATCH-03 so an early G3 rung does not inherit a late G3 rung's blockage. |
| Why atomic | Single finding. The packet records the decoupling as a design decision rather than an omission. |
| Acceptance impact | **V1-ACC-001** (rewritten), **SAF-001**, V1-ACC-044 |
| Ladder impact | Unblocks FBL-026 and FBL-072. |
| Validation | `foundation_self_review.py`, `validate_build_ladder.py`. Grep `v1-acceptance.md` for "intentionally" and confirm zero occurrences in V1-ACC-001. |
| Review authority | Change control. |
| Rollback | Acceptance-row and evidence-package edit; fully reversible. |

## BATCH-07 — Checkpoint sealing for read-only scans

| Field | Value |
| --- | --- |
| Packet | `PKT-07-checkpoint-sealing` |
| Findings resolved | PF-03 |
| Decisions required | None. Checkpoint *cadence* is adjacent to OD-008; the sealing *rule* is not a policy question. |
| Documents changed | `domain-model.md` (`Checkpoint`), `durability-and-recovery-model.md:240–241`, `event-model.md:165`, ADR-013, ADR-016 |
| Prerequisites | BATCH-03 (`SourceRoot.volume_identifier`, which CK-4 compares), BATCH-01 (checkpoint preimage). |
| Why atomic | Single finding, but it surfaces a fixture gap: **no scan-checkpoint fixture family is enumerated anywhere in the ladder**, and FBL-019 must add one. |
| Acceptance impact | V1-ACC-036, PILOT-012 |
| Ladder impact | Unblocks FBL-019. |
| Validation | `foundation_self_review.py`, `validate_build_ladder.py`. Confirm the sealing section lists three kinds and that no `scan` precondition mentions operations. |
| Review authority | Chief Systems Architect. **The analysis originated outside the lane that owns FBL-019 and may overlap a parallel proposal** — reviewers should check for one. |
| Rollback | Documentation-only while no checkpoint exists. |

## BATCH-08 — Approval event vocabulary

| Field | Value |
| --- | --- |
| Packet | `PKT-08-approval-event-vocabulary` |
| Findings resolved | PF-06 |
| Decisions required | None |
| Documents changed | `event-model.md`, `domain-model.md`, `approval-binding-model.md` (IT-17), `command-model.md`, ADR-013, ADR-017 |
| Prerequisites | BATCH-02 (`ApprovalRequested` has no source record until PF-05's records exist). |
| Why atomic | Single finding, but EP-1 obliges every record type BATCH-02 adds to be classified event-or-register. Landing this before BATCH-02's registry is final would mean reopening it to classify roughly twenty new types. |
| Acceptance impact | V1-ACC-037, V1-ACC-039, V1-ACC-042, FND-ACC-002, SAF-009, PILOT-014 |
| Ladder impact | Unblocks FBL-004. |
| Validation | `foundation_self_review.py` check 22. Independently: symmetric-difference the record registry against the approval events. |
| Review authority | Change control. **State in the record that this changes no authorization decision**, so the fix is not mistaken for a permission change. |
| Rollback | Additive to a vocabulary that is authoritative for nothing; fully reversible. |

## BATCH-09 — Root registry, taxonomy contract, and placeholder registry

| Field | Value |
| --- | --- |
| Packet | `PKT-09-config-contracts` |
| Findings resolved | PF-12, PF-15, PF-30 |
| Decisions required | **OD-001/OD-013** (which shares exist), **OD-002/OD-014/OD-015** (taxonomy content). All are field values; none is a schema decision. |
| Documents changed | Three new files under `config/schemas/`, one new fixture instance, `taxonomy-model.md`, `rule-model.md`, `domain-model.md` (`SourceRoot`, additive), ADR-001, ADR-006, ADR-011, ADR-012 |
| Prerequisites | BATCH-01 (`taxonomy_hash`), BATCH-03 (the shared `SourceRoot` edit). |
| Why atomic | PF-30's registry must be `$ref`'d by PF-15's taxonomy schema **at the moment that schema is authored**. Publishing it with an independently written pattern would encode the five-versus-six placeholder split in two machine contracts instead of one prose sentence — strictly worse than the present state. |
| Acceptance impact | V1-ACC-025, FND-ACC-004, FND-ACC-010, FND-ACC-013 |
| Ladder impact | Unblocks FBL-021, FBL-022, FBL-023, FBL-034, FBL-035. |
| Validation | `validate_rule_config.py` — **all 48 rule files must still validate byte-for-byte**. `check_path_policy.py`. Diff the two compiled placeholder patterns and confirm they are byte-identical. |
| Review authority | Chief Systems Architect for the contracts; the operator for field values only. |
| Rollback | New schemas are additive. The `SourceRoot` edit is additive and does not rename `synthetic_root_path`, so FND-ACC-004 is unaffected. |

## BATCH-10 — Decision closure change

| Field | Value |
| --- | --- |
| Packet | `PKT-10-decision-closure` |
| Findings resolved | PF-16 |
| Decisions required | **OD-012**, **OD-003** — their *contents*. The closure machinery proceeds without them. |
| Documents changed | Two new files under `config/governance/` and `config/schemas/`, `rule-model.md:303`, `change-control.md`, `gate-model.md:121`, `open-decisions.md`, ADR-006, ADR-017 |
| Prerequisites | BATCH-09 (taxonomy nodes acquire `policy_ref` and inherit the same trap). |
| Why atomic | Single finding, but it defines a *coupled change* type that BATCH-09's taxonomy work will immediately need. |
| Acceptance impact | FND-ACC-010, FND-ACC-013 |
| Ladder impact | Unblocks FBL-035. |
| Validation | `validate_rule_config.py` — all 48 files unchanged, because the pin field is optional. Confirm the register YAML and `open-decisions.md` agree row for row. |
| Review authority | Chief Systems Architect **and** the operator, because it changes how their decisions are recorded. |
| Rollback | Additive. The reopening prohibition is the one clause that must not be softened during review — it is the anti-laundering control. |

## BATCH-11 — Classification decision lifecycle and the unresolved queue

| Field | Value |
| --- | --- |
| Packet | `PKT-11-decision-lifecycle-and-unresolved` |
| Findings resolved | PF-17, PF-18 |
| Decisions required | **OD-017** (report format), **OD-021** (tolerable unresolved count at G8). Neither blocks the structure. |
| Documents changed | `domain-model.md`, `event-model.md`, `rule-model.md` (the reason vocabulary), `interface-model.md:39`, ADR-015 |
| Prerequisites | BATCH-09 (RI-2 references `TaxonomyNode.destination_authority`), BATCH-02 (journal rebuildability). |
| Why atomic | They share the `review_reason` field, the `rejected`-versus-`routed_unresolved` distinction must be drawn once, and both add events — so FND-ACC-002 is re-run once rather than twice. |
| Acceptance impact | V1-ACC-025, **V1-ACC-041**, **V1-ACC-053**, FND-ACC-002 |
| Ladder impact | Unblocks FBL-037 and FBL-038. |
| Validation | `foundation_self_review.py` check 22 with the two new names present on both sides. |
| Review authority | Change control, plus the operator for OD-017 and OD-021. |
| Rollback | Additive; no decisions or review items exist. |

## BATCH-12 — Authority classes and command ingress

| Field | Value |
| --- | --- |
| Packet | `PKT-12-authority-and-ingress` |
| Findings resolved | PF-20, PF-28 |
| Decisions required | **OD-022** — the authentication factor only. The class vocabulary proceeds without it. |
| Documents changed | `permission-model.md`, `approval-binding-model.md:43–45`, `domain-model.md:846`, `review-console-architecture.md`, `command-model.md`, ADR-003, ADR-014, ADR-015, ADR-017 |
| Prerequisites | None structural. **Must land before FBL-044 populates a principal registry** — adding classes afterwards requires a re-grant ceremony and fires IT-13 against every outstanding approval. |
| Why atomic | The subject type of a `grant_approval` submission determines which class AUTHZ-17 demands. PF-20 alone leaves the ingress question open; PF-28 alone leaves five of eight subject types with no class to check. Both block FBL-044 and FBL-063. |
| Acceptance impact | **V1-ACC-038**, V1-ACC-052, SAF-009 |
| Ladder impact | Unblocks FBL-063's allowlist matrix and the FBL-044 vocabulary. **FBL-044 itself remains hard-blocked by OD-022.** |
| Validation | `foundation_self_review.py`. Confirm all eight subject types map with no default clause, and that every command carries an ingress class or is covered by the `backend_internal` default. |
| Review authority | Chief Systems Architect. AC-3 and the Class F1 origin-independence clause are the two provisions that must not be softened. |
| Rollback | Additive, but sequencing-sensitive as above. |

## BATCH-13 — G4 semantics: runtime mode and descriptor completeness

| Field | Value |
| --- | --- |
| Packet | `PKT-13-g4-semantics` |
| Findings resolved | PF-25, PF-29 |
| Decisions required | **OD-023** — one question, and the packet states it precisely without answering it. |
| Documents changed | `approval-binding-model.md`, `rule-model.md:42`, `domain-model.md:720–734`, `preservation-model.md` (CD-4, CM-P3), `gate-model.md:116`, `durability-and-recovery-model.md:110–111`, ADR-009, ADR-012, ADR-015 |
| Prerequisites | BATCH-03 (PF-19 and PF-04), BATCH-09 (the taxonomy envelope needs the same `environment` semantics). |
| Why atomic | PF-25's rule PL-D4 is written in terms of `runtime_mode` — an enum PF-29 shows is defined nowhere. **PL-D4 is literally unwritable until PF-29 lands.** |
| Acceptance impact | V1-ACC-030, V1-ACC-034 |
| Ladder impact | Unblocks FBL-045, FBL-072, FBL-073. |
| Validation | `foundation_self_review.py`, `validate_rule_config.py` — all 48 files unchanged, because `environment` keeps its enum and only its meaning is pinned. Grep for a `runtime_mode` definition and confirm exactly one normative enum exists. |
| Review authority | Chief Systems Architect, plus the operator for OD-023. |
| Rollback | **Journal sequencing is the irreversible part**: `descriptor_completeness`, `promotability`, and `runtime_mode` must enter `plan_bound` and `run_open` at FBL-005/FBL-041, because append-only hash-chained records cannot gain a field afterwards. |

## BATCH-14 — Gate boundary and live-path policy

| Field | Value |
| --- | --- |
| Packet | `— (stress-test findings; no planning-finding packet)` |
| Findings resolved | Stress-test BLT-B03, BLT-B04, BLT-B05, BLT-M09, BLT-M10, BLT-M11 |
| Decisions required | **Proposed OD-025, OD-026, OD-027**, plus an operator-authorized amendment to **SAF-006** |
| Documents changed | `safety-acceptance.md` (SAF-006), `path-policy.md`, `scripts/check_path_policy.py`, `.gitignore`, `CHANGELOG.md` |
| Prerequisites | BATCH-13 (the G4/G5 boundary must be settled first). |
| Why atomic | SAF-006 forbids live NAS mutation before G6 while FBL-073 is a G5 `bounded-write` rung described as "the first legal write" — and `authority-order.md` makes the stricter rule win. **Resolving the scanner gaps without resolving SAF-006 would leave the ladder self-contradictory in the same place.** |
| Acceptance impact | SAF-006, and the path-policy self-test |
| Ladder impact | Unblocks FBL-073's characterization as written, or forces it to be re-scoped. |
| Validation | `check_path_policy.py` and its self-test; `validate_build_ladder.py`. |
| Review authority | **Operator authorization is required**, because amending SAF-006 changes a safety acceptance row. The three proposed decisions are carried in `operator-decisions/OD-025-PROPOSED.md` through `OD-027-PROPOSED.md` and are deliberately **not** added to the authoritative register. |
| Rollback | Documentation and tooling only, but SAF-006 is a BLOCKER safety row and its amendment is not a routine edit. |

## BATCH-15 — Ladder traceability repairs

| Field | Value |
| --- | --- |
| Packet | `— (stress-test findings; no planning-finding packet)` |
| Findings resolved | Stress-test BLT-B01, BLT-B02, BLT-B06, BLT-B07, BLT-B08, BLT-M01 through BLT-M08, BLT-M12, BLT-M13, BLT-N01 through BLT-N10 |
| Decisions required | None |
| Documents changed | `docs/handoffs/build-ladder.md`, `prompts/one-rung-implementation.md`, `scripts/validate_build_ladder.py` |
| Prerequisites | **All prior batches.** The seven phantom acceptance IDs cannot be repaired until the batches that define the missing requirements have landed. |
| Why atomic | These are bookkeeping defects between two representations of the same graph. Repairing them piecemeal as each batch lands would mean touching the ladder fifteen times; repairing them once at the end means the reverse acceptance-ID check can be added to the validator **and pass**. |
| Acceptance impact | Every acceptance ID the ladder cites — including the seven that are cited and undefined: `V1-ACC-007` (five sites), `V1-ACC-060`, `V1-ACC-061`, `V1-ACC-067`, `SAF-016`, `PILOT-019`, `FND-ACC-008`. **FBL-065's entire acceptance mapping is phantom.** |
| Ladder impact | Repairs the ladder's internal consistency. Adds the reverse acceptance-ID check to `validate_build_ladder.py`, which **cannot be added before this batch** because it would fail immediately on the phantom IDs. |
| Validation | `validate_build_ladder.py` with the new check enabled; `validate_proposals.py` checks 1, 2, 7. |
| Review authority | Change control. |
| Rollback | Documentation and tooling only; fully reversible. |

## What this plan does not do

It does not resolve any finding, answer any operator decision, or authorize any gate. It does not
freeze the Build Ladder. Every batch above is a proposal whose adoption is a separate act of change
control, and the operator decisions named in batches 01, 04, 09, 10, 11, 12, 13, and 14 remain
entirely the operator's — **Claude has not decided any of them.**

Batch 14 additionally requires operator authorization rather than change control alone, because
amending SAF-006 changes a BLOCKER safety acceptance row.
