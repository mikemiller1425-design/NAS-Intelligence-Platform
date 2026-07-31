# Contributing

This repository is currently in **Foundation Candidate** status. Contributions must preserve safety, auditability, and documentation authority.

## Authority order

Follow `docs/05-governance/authority-order.md`. Do not treat chat history, Future Registry ideas, or archived drafts as authorization to change safety posture or V1 scope.

## Non-negotiable contributor rules

1. **No destructive defaults.** Dry-run is the default. Live mode requires deliberate enablement and documented approvals.
2. **No credentials.** Never commit NAS passwords, tokens, SSH keys, service-account secrets, or `.env` files with secrets.
3. **No live-path assumptions as unsafe defaults.** Use synthetic fixture paths in examples (`/fixtures/source/`, `/fixtures/destination/`). Document intended live share names as intent, not as hardcoded mutation targets.
4. **No production implementation** until Foundation 1.0 approval and Build Ladder authorization.
5. **No live NAS mutation** from scripts, tests, or docs unless a later live-data policy gate explicitly authorizes a scoped operation.
6. **Copy before delete.** Source retirement requires hash verification and human approval.
7. **Protected vaults.** Existing vault content must not be overwritten by default.
8. **Explainability.** Classification and destination proposals must record rule ID, evidence, confidence, and explanation.

## Tests

When implementation is authorized:

- Every active classification rule needs positive, negative, boundary, conflict, and idempotency fixture tests.
- Safety tests must cover overwrite prohibition, retirement gating, collision handling, and resume/idempotency.
- Acceptance evidence must map to `docs/04-acceptance/`.

## ADRs

Material architectural or safety changes require an ADR under `docs/03-architecture/decisions/` and an update to `CHANGELOG.md`.

## Auditability

- Prefer append-only audit concepts for mutations and approvals.
- Do not rewrite historical decision evidence when changing rules; version rules and re-propose.
- Keep handoff documents executable without chat history.

## Git

Follow `docs/05-governance/git-policy.md`. Do not force-push protected branches. Do not commit lockfiles until implementation tooling is authorized.
