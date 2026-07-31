# Handoff 001 — Foundation Audit

## Purpose

Instruct an **independent reviewer** (ChatGPT or equivalent) to audit the completed NAS Intelligence Platform blueprint before any implementation authorization.

Findings must be written to:

`docs/audits/foundation-v1-audit.md`

Severities: **BLOCKER**, **MAJOR**, **MINOR**, **NOTE**.

The reviewer must **not** implement code.

## Inputs

- Entire repository (active docs, config examples, prompts, handoffs)
- Especially: `docs/00-intent/`, `docs/01-product/`, `docs/02-specification/`, `docs/03-architecture/`, `docs/04-acceptance/`, `docs/05-governance/`, `docs/06-operations/`
- `docs/migration/source-inventory.md`
- `docs/migration/source-reconciliation.md`
- `docs/migration/traceability-matrix.md`
- `docs/05-governance/open-decisions.md`
- `docs/future-registry/`
- `FOUNDATION_VERSION.md`, `PROJECT_STATUS.md`, `README.md`

## Authority

- Read-only review
- May create/update only `docs/audits/foundation-v1-audit.md`
- No NAS access
- No implementation
- No silent “approval” of provisional rules

## Audit checklist (required)

Review at least:

1. Intent alignment with the canonical product identity
2. Destructive safety (copy-before-delete, retirement gating, overwrite bans)
3. Domain completeness (entities, invariants, states)
4. Lifecycle validity (allowed/forbidden transitions)
5. Rule semantics and conflict resolution
6. Taxonomy boundaries and share/vault protections
7. Restart / checkpoint / idempotency safety
8. Privacy and security model
9. Operational playbook adequacy
10. Acceptance traceability to specifications
11. Architecture complexity / overengineering risk
12. V1 scope leakage from Future Registry
13. Whether Claude Code would have enough precision to build correctly after approval
14. Live-migration readiness language (must not authorize live work yet)

## Required output format

```markdown
# Foundation V1 Audit

## Summary
## BLOCKER findings
## MAJOR findings
## MINOR findings
## NOTES
## Traceability gaps
## Overengineering assessment
## Recommendation (Approve / Approve with fixes / Reject)
## Stop
```

Each finding: ID, severity, location, problem, recommended remediation, whether it blocks Foundation approval.

## Prohibitions

- Do not write application code
- Do not authorize live execution
- Do not mark provisional rules as approved
- Do not resolve open decisions without operator input
- Do not hand work to Claude Code

## Stop condition

Audit report written to `docs/audits/foundation-v1-audit.md` and no further changes made by the reviewer.
