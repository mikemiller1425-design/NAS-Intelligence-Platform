# Foundation Version

```text
NAS Intelligence Platform Foundation: 1.0-rc1
Status: Awaiting independent architecture and safety audit
Implementation status: Blocked
Live NAS execution: Prohibited
Dry-run engine execution: Prohibited until implementation authorization
Active mission: Produce a fully organized NAS through a tested, explainable, reversible migration system
```

## Meaning of this version

`1.0-rc1` is a foundation release candidate. It packages product intent, safety principles, specifications, architecture, operational playbooks, acceptance criteria, governance, configuration examples, and audit handoffs.

It is **not** authorization to:

- implement production engine code
- install classifier models against live data
- run dry-run or live engines against mounted shares
- mutate, rename, move, overwrite, or delete files on the Synology NAS
- hand work to Claude Code for Build Ladder generation before independent audit approval

## Promotion path

1. Independent ChatGPT foundation audit → `docs/audits/foundation-v1-audit.md`
2. Resolve all approved BLOCKER and MAJOR findings
3. Explicit Foundation 1.0 approval
4. Build Ladder generation authorization
5. Separate gates for dry-run, pilot, and live migration

## Related documents

- `PROJECT_STATUS.md`
- `docs/05-governance/definition-of-ready.md`
- `docs/handoffs/001-foundation-audit.md`
