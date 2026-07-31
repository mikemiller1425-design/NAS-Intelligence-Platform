# ADR 006: Rule-driven explainable classification

Status: Accepted (foundation candidate)

## Context
Classification output must be explainable to humans and stable enough to review. Opaque recommendations do not fit the safety posture.

## Decision
Prefer a rule-driven classification engine that can explain its decision with explicit evidence and decision paths.

## Consequences
This makes reviews faster and safer because operators can inspect the reasoning. It may be less flexible than fully opaque model-first classification.

## Alternatives considered
Black-box classification with no durable explanation trail.
