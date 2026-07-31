# Handoff 003 — Build Ladder

## Purpose

Instruct Claude Code to generate the **implementation ladder** only after Foundation approval. This handoff is a planning artifact generator, not live-execution authorization.

## Preconditions

- Independent foundation audit complete
- Approved BLOCKER and MAJOR findings resolved
- Foundation 1.0 explicitly approved
- Operator authorizes Build Ladder generation

## Authority

- Claude Code may produce a detailed rung ladder document and supporting planning notes
- Claude Code may **not** implement rungs until each rung is separately authorized
- No rung may silently authorize destructive live execution

## Required rungs (minimum)

Generate separate rungs for at least:

1. Tooling and repository foundation
2. Contracts
3. Persistence
4. Fixture dataset
5. Read-only inventory
6. Checkpoints
7. Hashing
8. Metadata extraction
9. Rule engine
10. Taxonomy
11. Proposal engine
12. Review queue
13. Dry-run planner
14. Copy engine
15. Validation
16. Comparison reports
17. Duplicate grouping
18. Protected-vault safety
19. Pilot workflow
20. Sentinel
21. Review console
22. Interruption recovery
23. Live-readiness audit
24. Controlled live migration
25. Post-migration verification
26. Maintenance mode

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

## Stop condition

Build Ladder document produced and frozen as planning-only. Implementation of rung N requires explicit authorization of rung N.
