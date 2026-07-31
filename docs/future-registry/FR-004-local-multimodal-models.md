# FR-004 — Local multimodal models

## Purpose
Run local vision/language models for richer media and document understanding.

## Dependencies
Capable worker hardware (Mac mini class); model licensing; offline preference for private media; prompt-injection defenses.

## Risks
Hallucinated labels treated as truth; high compute cost; privacy if models phone home.

## Reason excluded from V1
Optional AI assistance may exist later; V1 classification is rule-driven with AI as evidence only. Full multimodal stacks are out of scope.

## Promotion condition
Local-only processing default; confidence thresholds enforced; fixture tests for false positives.
