# Change Control

## Change principles
- All meaningful change is versioned.
- A plan, policy, or rule set becomes immutable once approved.
- Changes that alter live behavior require re-review and a new version.
- No silent edits to active policy.

## Change process
1. Propose the change with a stable ID.
2. State the reason, scope, impact, and rollback or fallback path.
3. Identify affected acceptance and migration artifacts.
4. Review evidence and unresolved decisions.
5. Approve or reject.
6. Publish the new version and archive the prior one.

## Prohibitions
- No untracked rule edits.
- No live-data shortcut that bypasses approval.
- No destructive change to protected vaults by default.
- No change that reclassifies source-retirement as deletion without hash verification and approval.
