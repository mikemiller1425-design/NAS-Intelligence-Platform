# FR-015 — Agent City visualization

## Purpose
Visualize workers, queues, and migration progress in an Agent City style dashboard.

## Dependencies
Observability events; non-authoritative UI; Foundry or local visualization host.

## Risks
Pretty dashboards mistaken for authorization; overengineering before core engine exists.

## Reason excluded from V1
CLI/reports are sufficient for V1 operability. Visualization is optional.

## Promotion condition
Core pipeline emits stable events; UI remains read-only for authorization.
