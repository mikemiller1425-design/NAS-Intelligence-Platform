# ADR 009: Dry-run default

Status: Accepted (foundation candidate)

## Context
If the system can choose between simulating and acting, it should simulate first. This is essential while the blueprint is still foundation-only.

## Decision
All workflows default to dry-run unless an explicit, approved live mode is engaged.

## Consequences
This reduces accidental mutation and makes review the default behavior. It also means every proposal path must be capable of simulation. The runtime mode is part of an approval's bound scope: an approval granted under one mode configuration does not authorize execution under another, and a change to the modes configuration invalidates outstanding approvals.

## Alternatives considered
Live execution as the default or silent fallback.
