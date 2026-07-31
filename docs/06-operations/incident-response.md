# Incident Response

## Purpose
Provide a blueprint for handling unexpected operational failures, safety breaches, or readiness regressions without improvising destructive actions.

## Incident classes
- Hash mismatch.
- Journal failure.
- Capacity exhaustion.
- Mount disconnect.
- Source or destination drift.
- Sentinel alert escalation.
- Privacy or policy violation.
- Reconciliation mismatch.

## Operating rules
- Safety first, then evidence, then recovery.
- Do not expand the blast radius while investigating.
- Do not delete evidence.
- Do not override protected vaults by default.
- Do not authorize live changes from an incident channel.

## Response sequence
1. Pause the affected batch or workflow.
2. Preserve logs, manifests, and checkpoints.
3. Triage the class and severity.
4. Confirm whether rollback or hold is the safest next step.
5. Notify the operator with concise evidence.
6. Record the incident outcome and follow-up decision.

## Stop conditions
- The incident cannot be described with evidence.
- The proposed fix requires unapproved live mutation.
- The recovery plan conflicts with source-retirement policy.

## Required evidence
- Incident ID.
- Trigger condition.
- Scope and severity.
- Preservation steps.
- Decision log.
- Closure or escalation record.
