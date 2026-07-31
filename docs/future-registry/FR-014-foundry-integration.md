# FR-014 — Foundry integration

## Purpose
Connect NAS Intelligence workflows to Foundry / AI Engineering Operations tooling.

## Dependencies
Stable contracts; no shared unsafe defaults; separate authorization domains.

## Risks
Cross-product scope leakage; copying Foundry stack assumptions; automation bypassing NAS safety gates.

## Reason excluded from V1
NAS platform must stand alone with its own safety model. Foundry is optional later.

## Promotion condition
Foundation approved and implemented; integration cannot authorize NAS mutation without NAS gates.
