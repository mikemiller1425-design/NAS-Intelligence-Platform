# Non-Negotiable Safety Principles

These principles are the safety floor for the NAS Intelligence Platform. They are not preferences; they are operating constraints. Violating any principle requires an explicit operator decision recorded in governance—not a convenience exception in code or chat.

## Core principles (canonical list)

1. **Inventory is read-only.** Discovery and analysis must not mutate source bytes, timestamps intentionally, or directory structure.
2. **Source files are immutable until an approved retirement stage.** Classification and planning never rewrite originals.
3. **Copy before delete.** Prefer copy-and-verify; source removal is a separately approved retirement phase.
4. **No deletion based only on path, filename, or inferred identity.** Exact duplicates require cryptographic hash equality; near-duplicates require review.
5. **Every proposed move has an explainable reason.** Rule ID, evidence, confidence, and explanation are mandatory.
6. **Every action has a stable operation ID.** Plans, copies, validations, and retirements are addressable and journaled.
7. **Every operation is idempotent.** Retrying must not create duplicate destination copies or silent loss.
8. **Every move or copy is logged.** Append-only journals record intent, approval, execution, and verification.
9. **Every destination collision is explicit.** Conflicting names never overwrite silently.
10. **Every ambiguity goes to review.** Low confidence and multi-destination conflicts do not auto-resolve into live mutation.
11. **Every destructive action requires human approval.** Frontend presentation cannot authorize filesystem mutation.
12. **Hash verification is required before source retirement.** Destination must match expected hash and size.
13. **Snapshots or backups must be confirmed before destructive migration.** Recovery coverage is a live gate, not an assumption.
14. **Dry-run is the default.** Live mode must be deliberately enabled under a separate readiness gate.
15. **Live NAS paths must not be hardcoded into unsafe defaults.** Examples use fixture paths; live roots are configured and reviewed.
16. **The engine must support pause, resume, checkpoint, and restart.** Partial runs must remain inspectable and safe.
17. **Failures remain inspectable.** Failed operations stay visible with error records; they are not erased.
18. **Partial runs must not create silent duplication or loss.** Restart reconciles filesystem reality against the journal.
19. **AI classifications are evidence, not unquestionable truth.** Confidence thresholds are configurable; AI cannot bypass review.
20. **Confidence thresholds must be configurable.** Sensitive destinations use stricter thresholds.
21. **Sensitive vaults receive stricter controls.** Existing vault content cannot be overwritten by default.
22. **The Raspberry Pi may monitor and trigger safe checks, but is not the primary heavy-analysis engine.** It cannot authorize destructive work.
23. **The Mac mini or another capable worker performs heavy scanning, hashing, media analysis, and orchestration.**
24. **Synology remains the protected storage authority.** Snapshots, shares, and authoritative bytes live there.

## Supporting operating rules

### Preserve source data

- Never operate first against the only copy of important data.
- Unsupported, unreadable, encrypted, or corrupted files remain preserved and reported.

### Avoid silent destruction

- Permanent deletion is not allowed in V1.
- Exact duplicates may be proposed for quarantine, never silently removed.
- Near-duplicates are not duplicates.

### Evidence before mutation

Every proposed operation must capture file identity, cryptographic hash when available, source and destination, matched rule and version, evidence and confidence, conflict/duplicate/risk status, planned operation, approval status, and execution/verification result.

### Small blast radius

Progression is gated:

```text
fixtures → copied pilot → limited live pilot → staged batches → full operation
```

Failure at any gate pauses expansion. A successful dry run does not authorize live mutation.

### Separation of concerns

- Classification recommends.
- Planner converts approved recommendations into an operation plan.
- Executor performs only approved plan entries.
- Verifier independently checks outcomes.
- UI never authorizes by animation or display alone.

### Least privilege and safe handling

- Dedicated NAS service accounts with only required share access.
- Separate read-only discovery credentials from mutation-capable execution where practical.
- Secrets outside Git and logs.
- Normalize and validate destination paths; prohibit traversal outside approved roots.
- Never interpolate untrusted filenames into shell commands.
- Treat filenames, paths, media metadata, thumbnails, and extracted text as sensitive.

### Prefer recovery over heroics

- Rollback is designed before execution.
- Journals are append-only and stored separately from data being moved.
- Snapshot restoration is last-resort, not normal rollback.
- If the system cannot prove safety, it stops.
