# ADR 016: The journal is authoritative; SQLite is derived

Status: Accepted (foundation candidate). Added during audit resolution of FND-M003.

## Context

ADR-005 split responsibility between SQLite and JSONL manifests but never declared which one wins. It named the drift hazard — "disciplined boundary management so the two stores do not drift" — and left it unresolved. The persistence specification then contained three mutually incompatible readings: mutable state "derived from **or** reconciled against" immutable history; SQLite holding "the current durable state"; and replay rebuilding derived state "where appropriate". Checkpoints were assigned to both stores.

With no tiebreak rule, recovery had no defensible interpretation of a crash, and "restart reconciles filesystem reality against the journal" was unimplementable.

## Decision

The append-only, hash-chained Execution Journal is the **authoritative** durable record of intent and outcome. SQLite is a **derived, rebuildable projection** used for queries, indexes, and current-state summaries.

Where the two disagree, the Journal wins unconditionally and without operator discretion. Every SQLite row must be reconstructible by replaying the Journal from genesis. No fact required for safety, recovery, reconciliation, audit, or authorization may exist only in SQLite.

## Consequences

Drift is not prevented by discipline; it is made harmless by construction. A divergent or corrupt projection is discarded and rebuilt from the Journal without operator approval, because a projection that claims to know more than the Journal is corrupt by definition.

Rebuildability is a **tested property** — delete the database, replay, compare — rather than an aspiration. The previous formulation had no failure signal at all.

The cost is that every safety-relevant fact must be journalled before it is queryable, which adds a durability barrier to the write path. That cost buys the pre-mutation intent record that makes an interrupted copy attributable rather than orphaned.

## Alternatives considered

- **SQLite authoritative.** Rejected: a B-tree with a write-ahead log cannot survivably record that a mutation is *about to* happen, and its torn-page failure modes are opaque to the application.
- **Co-equal stores reconciled against each other.** Rejected: no tiebreak rule is decidable at recovery time, which is exactly the state that produced this finding.

## Related

- `docs/02-specification/durability-and-recovery-model.md`
- `ADR-005`, `ADR-013`
