# ADR 009: Dry-run default

Status: Accepted (foundation candidate)

## Context
If the system can choose between simulating and acting, it should simulate first. This is essential while the blueprint is still foundation-only.

## Decision
All workflows default to dry-run unless an explicit, approved live mode is engaged.

## Consequences
This reduces accidental mutation and makes review the default behavior. It also means every proposal path must be capable of simulation.

## Alternatives considered
Live execution as the default or silent fallback.
