# ADR 011: Protected-vault overwrite prohibition

Status: Accepted (foundation candidate)

## Context
Some destinations must be treated as protected vaults. Overwriting them without explicit policy would defeat the preservation goal.

## Decision
Protected vaults are not overwritable by default. Any future exception would require deliberate governance and a documented policy change.

## Consequences
This preserves trust in archival destinations and avoids accidental replacement of curated content. It may require additional conflict resolution steps. Collision safety derives from an explicit pre-finalize existence check plus exclusive create — never from rename semantics alone — because rename atomicity is unavailable on `weak` or `unknown` destination adapters.

## Alternatives considered
Allowing overwrite into protected storage as a routine behavior.
