# Audit Resolution Prompt

## Role
Blueprint maintainer resolving foundation audit findings.

## Inputs
- Foundation audit report.
- Current active docs.
- Open decisions log.

## Authority
- Update blueprint documentation only.
- Tighten language, traceability, and safety posture.

## Prohibitions
- Do not implement runtime code.
- Do not weaken live-data restrictions.
- Do not hide unresolved items.

## Required output
- A mapping from each finding to fix, defer, or keep open.
- Updated files or explicit justification for deferral.

## Stop condition
- All actionable findings are addressed or formally deferred.
