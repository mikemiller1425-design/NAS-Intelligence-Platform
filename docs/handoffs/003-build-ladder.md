# Handoff 003 — Build Ladder

## Purpose

Instruct Claude Code to generate the **implementation ladder** only after Foundation approval. This handoff is a planning artifact generator, not live-execution authorization.

## Preconditions

- Independent foundation audit complete and every finding carries a resolution status
- Independent verification of the audit resolutions complete
- Foundation 1.0 explicitly approved (gate G1)
- **Operator separately authorizes Build Ladder generation (gate G2).** Foundation approval alone is not sufficient
- No open decision carries `blocks_gate: build_ladder`

## Authority

- Claude Code may produce a detailed rung ladder document and supporting planning notes
- Claude Code may **not** implement rungs until each rung is separately authorized
- No rung may silently authorize destructive live execution

## Required rungs (minimum)

Generate separate rungs for at least:

1. Tooling and repository foundation
2. Contracts
3. Persistence and the execution journal
4. Fixture dataset
5. Adapter interface and capability characterization
6. File identity and change tokens
7. Read-only inventory
8. Checkpoints and crash recovery
9. Hashing
10. Metadata extraction
11. Rule engine and configuration validation
12. Taxonomy
13. Proposal engine
14. Review queue
15. Approval binding and authorization evaluation
16. Dry-run planner
17. Copy engine
18. Validation
19. Preservation comparison reports
20. Duplicate grouping
21. Protected-vault safety
22. Pilot workflow
23. Sentinel
24. Review console
25. Interruption recovery
26. Live-readiness audit
27. Controlled live migration
28. Post-migration verification
29. Maintenance mode

> Rungs 5, 6, 15, and 19 were added during audit resolution. The original list had no adapter rung
> despite ADR-012 and OD-016, no file-identity rung despite FND-M001, no approval-binding rung
> despite FND-M004, and folded preservation comparison into generic "comparison reports" despite
> FND-M002.

## Per-rung required fields

Each rung must define:

- objective
- prerequisites
- allowed work
- prohibited work
- deliverables
- tests
- operator validation
- evidence package (per `docs/05-governance/evidence-standard.md`)
- rollback / stop conditions
- whether live NAS access is in scope (**default: no**)

## Hard rules

- Dry-run remains default until a dedicated live gate
- Copy-before-delete remains mandatory
- Source retirement requires verification + approval
- Protected vaults cannot be overwritten by default
- Frontend never authorizes filesystem mutation
- Sentinel never authorizes destructive work
- Fixtures and synthetic paths first

## Status

**Satisfied.** The Build Ladder was generated under G2 on 2026-08-01 and is frozen at `docs/handoffs/build-ladder.md` — 79 rungs. Its structural integrity is verified by `scripts/validate_build_ladder.py`.

Generation surfaced thirty specification gaps and seven ordering defects in the required-rung list below; both are recorded in the ladder's **Planning findings** and **Deviations** sections. The required-rung list is retained here as the original instruction, not as the final sequence.

## Stop condition

Build Ladder document produced and frozen as planning-only. Implementation of rung N requires explicit authorization of rung N at gate G3, and authorization of rung N never authorizes rung N+1.
