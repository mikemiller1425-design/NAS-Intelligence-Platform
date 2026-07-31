# FR-013 — Mobile review

## Purpose
Review classifications and approve non-destructive plans from a mobile device.

## Dependencies
Review console API; strong authentication; no direct filesystem mutation from mobile UI.

## Risks
Approving destructive actions from a low-context mobile session; notification leakage of private filenames.

## Reason excluded from V1
V1 review console may be desktop/local first; mobile is enhancement.

## Promotion condition
Backend authorization model proven; mobile cannot escalate privileges; path redaction in push alerts.
