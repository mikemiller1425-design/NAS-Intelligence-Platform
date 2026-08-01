# PKT-03 — Domain entity completion (PF-04, PF-07, PF-10, PF-11, PF-19, PF-21, PF-23, PF-24, PF-27)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-04, PF-07, PF-10, PF-11, PF-19, PF-21, PF-23, PF-24, PF-27 |
| Highest severity | BLOCKER |
| Change-control batch | BATCH-03 |
| Operator decision required | None |
| Blocked rungs | **FBL-003** (all nine), plus FBL-008, FBL-025, FBL-028, FBL-040, FBL-041, FBL-045, FBL-052, FBL-053 |
| Affected acceptance | V1-ACC-002, V1-ACC-003, V1-ACC-005, V1-ACC-031, V1-ACC-034, V1-ACC-039, V1-ACC-044, FND-ACC-001, FND-ACC-004 |

## The exact contradiction

Nine findings each add or change a domain entity or field that other documents already reference:

- **PF-04** `AdapterCapabilityDescriptor` — referenced by id from `Approval`, expires, fatal on mismatch; no entity.
- **PF-07** `HardLinkSet` — referenced by the inventory field table and the identity model; no entity.
- **PF-24** `PreservationComparisonReport` — has a schema in the preservation model; no entity.
- **PF-21** `EvidenceBundle` — bound by every approval, recomputed by AUTHZ-11, invalidated by IT-02; membership, versioning, and hashing all undefined.
- **PF-10** `HashRecord` lacks the `source_recheck` scope and `unstable` status the identity model mandates.
- **PF-11** `SourceRoot` lacks the identity-evidence fields the identity model states it carries.
- **PF-19** `OperationPlan` omits `adapter_descriptor_ids` and `preservation_profile_id`, which the preservation protocol freezes *into the plan*.
- **PF-23** `VerificationResult` carries only two hashes — no preservation-report reference, no token evidence.
- **PF-27** `entry_type` disagrees between the domain and inventory models.

## Operational consequence if left unresolved

**This is the most consequential packet in the set, for a structural reason.** FBL-003 is the sole home for domain entities and forbids inventing any field the specification omits. Under the G3 Definition of Done — "only the named rung's files changed" — a later rung cannot legally add an entity to the contracts package. Today only five of these nine findings block FBL-003. The other four resolve at rungs 25, 40, 45, 52, and 53, by which time the contracts rung is frozen. **The rung would be built against a knowingly incomplete entity set and reopened once per finding.** This is stress-test finding BLT-B02.

## Affected domain entities and fields

`AdapterCapabilityDescriptor` (new), `HardLinkSet` (new), `PreservationComparisonReport` (new), `EvidenceBundle` (new), `HashRecord`, `SourceRoot`, `OperationPlan`, `VerificationResult`, `FileRecord.entry_type`

## Affected events, commands, reason codes, and persistence records

`approval_granted` (evidence-bundle binding); every verification record

## Proposed normative resolution

Add four entities and extend five, in one change. Exact shapes:

**`EvidenceBundle`** — the highest-value definition here, because AUTHZ-11 is unimplementable without it.
`{id: string (required), version: semver (required), members: [{artifact_id: string, artifact_type: enum, content_hash: digest}] (required, ordered, non-empty), created_at: timestamp (required), bundle_hash: digest (required)}`
`bundle_hash` is the canonical digest (PKT-01) over the ordered member list. Membership is **explicit and enumerated** — never "everything in a directory", because that is not reproducible.

**`AdapterCapabilityDescriptor`** — entity form of the schema already in the preservation model, plus lifecycle `measured → current → expired → superseded` and `attestation_evidence_ref` (required, non-null).

**`HardLinkSet`** — `{id, volume_identifier, object_identity_key, member_logical_file_ids: [ref] (required, min 2), link_count: integer, detection_grade: enum}`.

**`PreservationComparisonReport`** — the field schema at `preservation-model.md:185–233` stays
authoritative **by reference**, so the fields have one home, not two. What the domain entity adds is
everything that schema block lacks: identity, lifecycle, state, and invariants.

- `id` — `"pcr_" + first 32 lowercase hex of the canonical digest (PKT-01) of the report body`.
  **Content-addressed, so a regenerated report is a different report by construction.**
- `report_state` — `draft | review_required | finalized | superseded`, required.
  `finalized_at` non-null iff `finalized` or `superseded`; `superseded_by_report_id` non-null iff
  `superseded`.
- `property_results` — **exactly thirty elements**, one per P01…P30, sorted ascending. A property the
  platform did not compare is present with `compared_count: 0`, never omitted: PC-1 forbids
  "unknown" and PM-2 requires a per-batch count for every `U` cell.

| ID | Invariant |
| --- | --- |
| PCR-1 | `retirement_gate.eligible` may be `true` **only** when `report_state` is `finalized`. A draft has moving counts and cannot support a retirement determination. |
| PCR-2 | *(CR-2, made mechanical)* `eligible` is `false` whenever any `required`-classified property has `mismatched_count > 0` or `unverifiable_count > 0`, or any MM-2/MM-4 mismatch has `resolution != waived` or a null `approval_id`. Each contributes a distinct string to `blocking_conditions`; an `eligible: false` report with an empty `blocking_conditions` is invalid. |
| PCR-3 | *(CR-1)* A report whose `hash_equality_disclaimer` is not byte-identical to the governing statement is **invalid evidence**, rejected at construction rather than at review. |
| PCR-4 | Totals reconcile: `entries_planned == executed + failed + blocked + skipped`, and `verified <= executed`. A report whose totals do not reconcile must disclose why and may not be finalized. |
| PCR-5 | **Exactly one `finalized` report exists per `(plan_id, plan_version, batch_id)`.** Finalizing a second supersedes the first. **A superseded report may never be cited by a retirement approval.** |
| PCR-6 | A finalized report is immutable. Correction is by supersession; there is no edit path. |
| PCR-8 | Every waiver named in `required_waivers` or `capability_mismatches[].approval_id` must reference an approval whose scope **names the specific property** (CM-P1). A blanket waiver is not a valid reference. |
| PCR-9 | A finalized report is evidence, never a command. Finalizing authorizes nothing; retirement requires a separately bound `RetirementAuthority` approval (SAF-003). |

Lifecycle `draft → review_required → finalized`, any state → `superseded`, mirroring
`ReconciliationReport`. Commands `draft_` / `finalize_` / `supersede_preservation_comparison_report`;
events `…Drafted` / `…Finalized` / `…Superseded`, added to both models for FND-ACC-002 parity; journal
record `preservation_report_finalized` carrying the eligibility determination and its summary counts,
which is what the retirement gate reads under PKT-02's journal-read rule.

> **Why content-addressing rather than an assigned id.** With a mutable body and a stable id, a
> regenerated report keeps its id and a bound retirement approval silently points at different
> content. With no identity rule at all, two runs over one batch produce two reports and the
> implementer selects "latest" — which is exactly the selector `approval-binding-model.md:47` forbids
> ("EXACT. Never a range, never 'latest'"). This is the gate with the highest consequence in V1, and
> it is the one place an id rule cannot be left to implementation.

**Extensions:** `HashRecord.scope` gains `source_recheck` and `source_postcopy`; `HashRecord.status` gains `unstable`. `SourceRoot` gains `root_identity_evidence` and `capability_descriptor_id`. `OperationPlan` gains `adapter_descriptor_ids: [ref]` and `preservation_profile_id: ref`, both required at approval. `VerificationResult` gains `preservation_report_id: ref`, `source_token_precopy`, `source_token_postcopy`, `token_comparison_result`. `entry_type` becomes `file | directory | symlink | bundle` in both models.

## Alternatives considered

**Resolve each finding at its own rung.** Rejected — that is the current state, and it is exactly what BLT-B02 shows to be illegal under the Definition of Done.

**Charter a contract-amendment rung that may reopen the contracts package.** Viable, and worth considering if the operator prefers smaller change-control batches. Rejected as the primary recommendation because it creates a rung whose purpose is to violate the "only the named rung's files changed" rule, which weakens that rule generally.

## Safety implications

`EvidenceBundle` and the `VerificationResult` extensions both sit on the retirement gate. Leaving them undefined means "verified" is decided by whichever fields an implementer happens to populate.

## Migration and compatibility implications

Additive to entities that do not yet exist in code. Safe now; expensive after FBL-003 is built, which is the entire point of this packet.

## Required tests

**Positive:** every entity constructs; every new enum value is representable.
**Negative:** an `EvidenceBundle` with an unenumerated member is rejected; a `VerificationResult` claiming verified without token evidence is rejected; a `PreservationComparisonReport` without the disclaimer is rejected as invalid evidence.
**Failure-injection:** none — these are contracts.

## Required ADR changes

**ADR-012** — descriptor lifecycle and expiry. **ADR-017** — evidence-bundle membership as a bound value.

## Operator policy, or pure specification defect?

**Pure specification defects.** PF-08 is deliberately excluded from this packet and handled in PKT-04, because its scope half is an operator decision (OD-024).

## Atomicity

All nine must land together and **before FBL-003 is authorized**. Splitting them recreates BLT-B02. PF-21 additionally depends on PKT-01, since the bundle hash needs a canonicalization rule.

### A cross-packet constraint that two independent analyses raised separately

PF-23 makes the change-token fields on `VerificationResult` **required**; PKT-05 (PF-22) is what
makes them **obtainable**, by adding the captures to the authoritative write protocol. Likewise
PF-24's `PreservationComparisonReport` is the referent of PF-23's required
`preservation_comparison_report_id`, and the two aggregate from each other.

If this packet lands and PKT-05 does not, the specification mandates fields that nothing can
populate. If PKT-05 lands and this packet does not, the token gate's outcome is journalled but has
nowhere to be projected. **Neither ordering is safe on its own.**

This packet does not resolve that by merging the two — merging would put a protocol change inside the
contracts freeze, which is the constraint that forced this packet's grouping in the first place.
Instead it records the requirement:

> **BATCH-03 and BATCH-05 must land in adjacent change-control cycles, with no G3 rung authorized
> between them.** Specifically, FBL-052 and FBL-053 must not be authorized until both have landed.

That is a sequencing constraint on the change-control plan, not a specification statement, and it
belongs to the Chief Systems Architect to accept or replace. **Claude has not decided it.** The
alternative — defining PF-23's token fields as nullable in this packet and promoting them to required
in BATCH-05 — is viable and cheaper to sequence, but it means a `VerificationResult` can be
constructed without token evidence during the window between the two batches, which is precisely the
state PF-23 exists to make unconstructible.

## Verification procedure

`foundation_self_review.py` checks 1, 22; `validate_build_ladder.py`. Confirm FBL-003's `Blocked by` lists all nine — see BATCH-15.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for any decision named
above. **This packet is non-authoritative and confers no authority of its own.**
