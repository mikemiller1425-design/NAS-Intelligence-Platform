# ADR 003: Human approval for destructive actions

Status: Accepted (foundation candidate)

## Context
Destructive filesystem actions can permanently remove or alter data. Automated confidence is not sufficient to justify that level of risk.

## Decision
The execution path must require explicit human approval before any destructive step. An approval is valid only when bound to an authenticated operator identity and session; the exact subject type, id, version, and content hash; the evidence-bundle version and hash; the rule-set and taxonomy versions and hashes; the source-precondition digest; an explicit scope; a grant time and an expiry; a single-use nonce; and a single-use consumption claim bound to one run. An approval that is not so bound authorizes nothing. See `ADR-017`.

## Consequences
This creates a clear accountability boundary and reduces the impact of model or rule mistakes. It also adds friction to the workflow, which is intentional.

## Alternatives considered
Fully automated destructive cleanup based only on classification confidence.
