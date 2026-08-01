# ADR 017: Approvals are content-bound, single-use, and backend-evaluated

Status: Accepted (foundation candidate). Added during audit resolution of FND-M004.

## Context

The approval entity bound an approval to a subject **id**, not to subject **content**. Because a superseding plan version reuses the plan lineage, an approval granted for a plan was textually satisfiable by a later version of that plan.

Compounding this: `consumed` existed as a state name with no mechanism defining consumption as atomic, one-time, or a precondition of mutation; `revoked` appeared in the allowed states but in no transition; approvals were declared "not transferrable across *unrelated* subjects", which affirmatively permitted transfer across related ones; the command envelope carried `authorization_status` as an inbound field, so a client could assert it; and no operator authentication model existed anywhere in V1.

The single pre-execution check standing behind all of it was "confirm the plan has a valid approval", where "valid" was undefined.

## Decision

An approval is valid only when it is bound to:

- an authenticated operator identity and session;
- the exact subject type, id, version, and **content hash**;
- the evidence-bundle version and hash;
- the rule-set and taxonomy versions and hashes;
- the source-precondition digest;
- the adapter capability descriptors and preservation profile;
- an explicit scope, a grant time, and an expiry;
- a single-use nonce and a single-use consumption claim bound to one run.

An approval that is not so bound authorizes nothing.

Authorization does not travel across the stage boundary as a token, a flag, or client-held state. It is **re-derived at execution time from the authoritative Journal, on every attempt**. The only artifact that crosses the boundary is an approval id; every value that gives it meaning is recomputed by the executor.

A request carrying an authorization status, a validation status, an approval state, or a payload-supplied actor is **rejected**, not ignored.

## Consequences

Approvals become single-use, content-bound, expiring, revocable, and invalidated by upstream change. Replay is structurally impossible while restart-resume remains possible, because a claim is bound to a run id: the same run resumes, a different run is refused.

Rule-set and taxonomy changes now invalidate outstanding approvals, which makes the change-control rule "a plan, policy, or rule set becomes immutable once approved" enforceable rather than aspirational.

The cost is operational friction: an approval expires, and a plan edit voids it. That friction is the point — an unbounded standing authorization over a drifting filesystem is precisely the hazard.

This ADR introduces an operator authentication requirement that V1 scope did not previously state. It is recorded as OD-022 for operator decision rather than settled here.

## Alternatives considered

- **ID-referenced approvals.** Rejected: this is the version-confusion hole that produced the finding.
- **Frontend-held approval state.** Rejected by ADR-014 and by the domain invariant that frontend state cannot authorize mutation.
- **No expiry.** Rejected: a standing authorization over data that can change underneath it is not an authorization, it is a standing risk.

## Related

- `docs/02-specification/approval-binding-model.md`
- `docs/02-specification/durability-and-recovery-model.md`
- `ADR-003`, `ADR-014`, `ADR-015`
