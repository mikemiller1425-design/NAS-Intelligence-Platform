# PKT-02 — Journal authority and record vocabulary (PF-01, PF-02, PF-05)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-01, PF-02, PF-05 |
| Highest severity | BLOCKER |
| Change-control batch | BATCH-02 |
| Operator decision required | None registered. **PF-02 has two legitimate resolutions with materially different consequences; the choice may warrant architect sign-off.** |
| Blocked rungs | FBL-005, FBL-017, FBL-018, FBL-047 |
| Affected acceptance | V1-ACC-039, V1-ACC-046, **V1-ACC-047**, FND-ACC-043 |

## The exact contradiction

**PF-01:** `PROJECTION_UNAVAILABLE` permits halting when *authorization lookups* cannot be served — implying authorization reads from SQLite. But the durability model forbids SQLite being the only home of an authorization-required fact, and AUTHZ-04 requires the revocation read to come from the durable journal tail, "never from cache".

**PF-02:** The journal record-type registry contains no record type for inventory, metadata, hash, classification, duplicate, review, or taxonomy facts — yet those tables live in SQLite and replay is required to rebuild **all** derived state. The observability event stream cannot fill the gap; it is "authoritative for nothing".

**PF-05:** The nonce ledger is placed on control storage and described as journalled, and AUTHZ-20 requires the nonce to be in an *issued* ledger — but no `nonce_issued` or `nonce_spent` record type exists.

## Operational consequence if left unresolved

An implementer reading PF-01 literally builds authorization reads against the projection, which the audit's own authority rule forbids. Under PF-02, `V1-ACC-047` — delete the database, replay, compare — is unsatisfiable as written, so the rung either ships a check that cannot pass or silently narrows what "all derived state" means. Under PF-05, issued nonces have no authoritative home, so anti-replay depends on a ledger that no record type can express.

## Affected domain entities and fields

`JournalEntry`, `Approval`, and every entity projected into SQLite

## Affected events, commands, reason codes, and persistence records

The complete record-type registry; proposed additions `nonce_issued`, `nonce_spent`; reason code `PROJECTION_UNAVAILABLE`

## Proposed normative resolution

**PF-01.** State that authorization reads are **journal-tail reads**. Delete the authorization clause from `PROJECTION_UNAVAILABLE` and retain that halt only for non-authorization query failure. Add to the authority statement: *no authorization decision may read the projection.*

**PF-05.** Add two record types with these exact shapes:

- `nonce_issued` — `{nonce: opaque, approval_request_id: string, issued_at: timestamp, expires_at: timestamp}`
- `nonce_spent` — `{nonce: opaque, approval_id: string, run_id: string, spent_at: timestamp}`

Both carry the standard envelope and are written under barrier **B-APPROVAL**.

**PF-02 — two options; the choice is not made here.**

*Option A — extend the registry.* Add record types for inventory, metadata, hash, classification, duplicate, review, and taxonomy facts. Replay then rebuilds everything and `V1-ACC-047` stands unchanged. Cost: a much larger journal, and every read-only scan becomes a journal writer.

*Option B — scope rebuildability.* Declare those tables **derived by re-derivation, not by replay**: rebuildable by re-scanning and re-evaluating rather than from the journal. Narrow `V1-ACC-047` to the execution subset (operations, approvals, checkpoints). Cost: `V1-ACC-047` no longer proves what it appears to, and its wording must say so explicitly.

**Recommendation: Option B**, because Option A makes a read-only inventory scan a mutation-capable operation, which conflicts with the read-only-inventory invariant. But this is an architecture call with a real trade, and it should be signed off rather than absorbed.

## Alternatives considered

**Promote the event stream to a second authoritative hash-chained log.** Rejected — it creates two authoritative records, which is precisely the ambiguity ADR-016 was written to remove.

## Safety implications

PF-01 touches the authorization gate. PF-02 touches recoverability: choosing Option B without rewording the acceptance row would leave a green check that no longer proves recovery.

## Migration and compatibility implications

Option A grows the journal format; applying it after any journal exists requires a format version bump. Option B changes only documentation. PF-05's additions are additive and safe before any nonce is issued.

## Required tests

**Positive:** delete the database, replay, byte-compare against the golden dump (scope depends on the PF-02 branch).
**Negative:** an authorization read served from the projection fails; a nonce absent from the issued ledger rejects with `APR-E21`.
**Failure-injection:** projection deleted mid-run; authorization must still succeed from the journal tail.

## Required ADR changes

**ADR-016** — add that authorization decisions read the journal, never the projection. **ADR-005** — record the PF-02 branch chosen and why.

## Operator policy, or pure specification defect?

**Pure specification defects.** No operator policy is required. PF-02's branch is an architecture decision, which the Chief Systems Architect should sign off; it is not an operator policy question and is not decided here.

## Atomicity

PF-01 cannot be resolved without PF-05, because its recommended resolution presupposes nonce record types PF-05 says do not exist. PF-02 must be chosen alongside, because the record registry is the thing all three modify.

## Verification procedure

`foundation_self_review.py` checks 10 and 11; `validate_rule_config.py`. Confirm the golden-journal fixture pair still matches whichever rebuild scope is chosen.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for any decision named
above. **This packet is non-authoritative and confers no authority of its own.**
