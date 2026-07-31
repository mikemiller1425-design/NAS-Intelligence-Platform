# Sentinel Architecture

## Purpose
The Sentinel is a Raspberry Pi role for continuous watching, alerting, and lightweight supervision. It is intentionally not the primary worker.

## Responsibilities
- Monitor pipeline health and job progress.
- Watch for stalled operations, validation failures, and policy breaches.
- Surface alerts to operators and the review surface.
- Maintain awareness of system status without taking destructive actions.

## Prohibitions
- The Pi may not authorize destructive work.
- The Pi may not become the main analysis engine.
- The Pi may not override approval gates.
- The Pi may not perform filesystem mutations that bypass the controlled workflow.

## Operational Posture
The Sentinel is a support role, not a decision role. If the Mac mini is unavailable, Sentinel should report the condition rather than attempt to take over unsafe work.

## Safety Rationale
This keeps the lightweight device focused on resilience and observability while the Mac mini handles the heavier scan, analysis, and orchestration workload.
