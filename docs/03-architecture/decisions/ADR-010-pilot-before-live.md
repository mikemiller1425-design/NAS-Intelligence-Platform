# ADR 010: Pilot before live migration

Status: Accepted (foundation candidate)

## Context
A narrow, controlled pilot reduces uncertainty before the platform is allowed to operate on the full corpus.

## Decision
Run a limited pilot and validate evidence, approvals, copy verification, and rollback assumptions before any live migration is considered.

## Consequences
This surfaces design gaps early and lowers operational risk. It can delay full rollout, but that delay is intentional and safer.

## Alternatives considered
Immediate full-scale live migration after blueprint approval.
