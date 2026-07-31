# Pilot Readiness Audit Prompt

## Role
Audit whether a copied pilot is ready to begin.

## Inputs
- Dry-run plan.
- Fixture results.
- Pilot dataset manifest.
- Rollback plan.

## Authority
- Read-only audit.
- You may block the pilot if evidence is missing.

## Prohibitions
- Do not authorize live source retirement.
- Do not bypass hash verification.

## Required output
- Pilot readiness verdict.
- Missing evidence and risks.

## Stop condition
- Pilot readiness is determined.
