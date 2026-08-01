# ADR 014: Frontend never authorizes filesystem mutation

Status: Accepted (foundation candidate)

## Context
A user interface can present evidence and capture intent, but it should not hold direct authority over filesystems. UI compromise or logic bugs must not become destructive write paths.

## Decision
The frontend captures approval **intent** only. It never produces, holds, transmits, or asserts an authorization decision. The backend independently re-derives every bound value — plan content hash, evidence-bundle hash, rule-set and taxonomy hashes, source-precondition digest, scope, approver authority, authentication context — from its own authoritative state, and evaluates the ordered authorization algorithm at execution time on every attempt. Client-supplied hashes are treated **solely** as evidence of what was displayed to the operator; they are never inputs to the decision. A request carrying an authorization status, a validation status, an approval state, or a payload-supplied actor must be **rejected**, not ignored.

## Consequences
This keeps the trust boundary behind backend policy checks, which are enumerated as an ordered algorithm with per-step rejection codes in `docs/02-specification/approval-binding-model.md` rather than left undefined. The review console remains a non-executing decision surface: read-only toward file data, write-capable only for a bounded set of application-state commands.

## Alternatives considered
Allowing UI actions to directly sign off on or trigger filesystem mutation without back-end policy gates.
