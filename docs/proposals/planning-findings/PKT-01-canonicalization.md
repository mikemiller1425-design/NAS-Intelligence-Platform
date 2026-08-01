# PKT-01 — Digest and canonical serialization (PF-09)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-09 |
| Highest severity | BLOCKER |
| Change-control batch | BATCH-01 |
| Operator decision required | **OD-004** — hash algorithm |
| Blocked rungs | FBL-002, FBL-005, FBL-041, FBL-045 |
| Affected acceptance | V1-ACC-031, V1-ACC-039, FND-ACC-043, FND-ACC-045 |

## The exact contradiction

Only the precondition-set digest has a defined preimage. `subject_content_hash`, `evidence_bundle_hash`, `rule_set_hash`, `taxonomy_hash`, `config_modes_hash`, `session_binding_hash`, and `binding_digest` have no canonicalization rule — yet the backend authorization algorithm requires it to **recompute and compare** each of them (AUTHZ-10, AUTHZ-11, AUTHZ-12, AUTHZ-13, AUTHZ-23).

## Operational consequence if left unresolved

Two conforming implementations would compute different digests from the same logical content and disagree about whether an approval is valid. Because the comparison is the authorization gate, the failure mode is either a valid approval rejected (a stoppage) or — worse — a mismatch that goes undetected because both sides use the same buggy serializer.

## Affected domain entities and fields

`Approval` (every bound hash field), `OperationPlan.plan_content_hash`, `RuleSet`, `TaxonomyNode`, journal record `record_hash` and `prev_record_hash`

## Affected events, commands, reason codes, and persistence records

Every journal record type; `approval_granted`; the reason codes `APR-E11`, `APR-E12`, `APR-E13`, `APR-E14`, `APR-E15`

## Proposed normative resolution

Adopt **RFC 8785 JSON Canonicalization Scheme (JCS)** as the single canonical serialization for every content-addressed value, and state it once in `durability-and-recovery-model.md` with every other document referencing it.

Normative rules to add:

1. **Preimage construction.** For each bound value, the preimage is the JCS serialization of a named object whose members are enumerated explicitly in the specification. No implicit "all fields" rule — an added field must be a deliberate versioned change.
2. **Digest.** `sha256` over the UTF-8 bytes of the JCS output, rendered lowercase hex, prefixed `sha256:`.
3. **Exclusion rule.** A digest field is never part of its own preimage. `record_hash` is computed over the record with `record_hash` removed and `prev_record_hash` present.
4. **Stability requirement.** Serialization must be stable across dict insertion order, Unicode normalization form, platform, and language runtime. This is a **testable** property, not an aspiration.
5. **Versioning.** The canonicalization scheme carries `canonicalization_version: 1`. Changing it is a new version, never an in-place edit, because it invalidates every chain already written.

If OD-004 selects a digest other than SHA-256 for **content**, rule 2 still pins SHA-256 for the **chain and binding** digests unless the operator explicitly says otherwise — see the OD-004 brief, which recommends splitting the two.

## Alternatives considered

**Alternative: define a bespoke canonical form per value type.** Rejected — it multiplies the number of things that must be independently correct, and each one is a place two implementations can diverge.

**Alternative: hash the on-disk file bytes rather than a canonical structure.** Rejected for structured values: it makes the digest sensitive to formatting, so reflowing a YAML file would invalidate every approval bound to it.

## Safety implications

Touches the approval-binding invariant directly. A wrong canonicalization does not weaken a control visibly — it makes the control silently unable to detect the tampering it exists to detect.

## Migration and compatibility implications

**Irreversible once data exists.** Every journal chain, stored fingerprint, and approval binding is computed under this rule. Changing it later invalidates all of them, with no migration path short of re-hashing from source — which is impossible for a chain, because the chain's whole purpose is that it cannot be recomputed after the fact.

## Required tests

**Positive:** the same logical object serialized from different dict orderings, Unicode forms, and two language runtimes produces byte-identical output.
**Negative:** a digest field included in its own preimage is rejected; an unenumerated field silently added to a preimage is rejected.
**Failure-injection:** truncated serialization mid-write produces no digest rather than a short one.

## Required ADR changes

**ADR-004** — add a consequence stating that the approved hash family binds four distinct things (duplicate identification, post-copy content verification, content-addressed binding, and the journal chain), and that the canonicalization scheme is versioned separately from the digest choice.

## Operator policy, or pure specification defect?

**Operator policy required for the digest choice only (OD-004).** The canonicalization scheme is a pure specification defect and needs no decision. The question the operator must answer is stated in the OD-004 brief; it is not answered here.

## Atomicity

Must land with **OD-004** in BATCH-01. PF-21 (`EvidenceBundle`) and PF-19 (plan descriptor fields) cannot be written until this exists, because both define preimages.

## Verification procedure

Re-run `foundation_self_review.py` check 11 and `validate_rule_config.py`. Independently: serialize a fixture object under two runtimes and diff the digests.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for any decision named
above. **This packet is non-authoritative and confers no authority of its own.**
