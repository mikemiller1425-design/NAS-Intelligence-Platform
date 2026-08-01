# G3 Implementation Readiness Map

> **Non-authoritative.** This map reports the state of the Build Ladder; it does not change it,
> and it authorizes nothing.

Generated from the ladder at commit `8838ac6`, covering all 70 rungs at gate G3.

## Three states that must never be inferred from one another

| State | Meaning | Who establishes it |
| --- | --- | --- |
| **Specification ready** | The rung's specification is coherent: no unresolved planning finding, no unresolved operator decision. | Change control and the operator |
| **Authorized** | The operator has recorded a G3 authorization for **this specific rung** in `docs/05-governance/authorization-ledger.md`. | The operator, per rung |
| **Implemented** | The rung has been built, inspected, and its evidence accepted. | An implementer, then an independent inspector |

**None implies another.** A specification-ready rung is not authorized. An authorized rung is not
implemented. Today **no rung is authorized**, so the third column of every row below is "no".

## The earliest safe implementation frontier

**3 of 70 G3 rungs** are specification-ready *and* have a fully specification-ready
prerequisite chain:

- **FBL-001** — Repository tooling, evidence emitter, and CI safety guards
- **FBL-006** — Fixture generator framework and expectations contract
- **FBL-007** — Fault-injection adapter and process-kill harness

Everything else is blocked directly, or sits behind something that is.

> **The dominant constraint is OD-004.** It blocks FBL-002 (identifier and state-machine
> contracts), which is the prerequisite of the entire contract chain. Resolving every other
> decision without OD-004 moves the frontier from 3 rungs to 3. Resolving OD-004 alone moves it to
> 4. Resolving OD-004 **and every planning finding** moves it to 12.
>
> That number is worth sitting with: even with all 30 findings resolved, only 12 of 70 G3 rungs
> become reachable, because the remaining blockers are other operator decisions.

## Summary

| Category | Count |
| --- | --- |
| Specification-ready, no blockers of any kind | 29 |
| — of which are in the reachable frontier today | 3 |
| Blocked by operator decision only | 13 |
| Blocked by planning finding only | 20 |
| Blocked by **both** | 8 |
| **Total G3 rungs** | **70** |

## Blocked by both a decision and a finding

These are the most expensive to unblock and should be sequenced deliberately.

| Rung | Title | Blocking decisions | Blocking findings | Prerequisites |
| --- | --- | --- | --- | --- |
| FBL-003 | Domain entity contracts | OD-004 | PF-04, PF-05, PF-07, PF-08, PF-11 | FBL-002 |
| FBL-005 | Journal record contracts and the reason-code registry | OD-004 | PF-02, PF-05, PF-09 | FBL-004 |
| FBL-025 | Hashing and content identity state | OD-004 | PF-10 | FBL-024 |
| FBL-034 | Taxonomy registry and node authority | OD-002, OD-014 | PF-15 | FBL-021 |
| FBL-038 | Review queue and unresolved disposition | OD-017 | PF-18 | FBL-037 |
| FBL-041 | Immutable operation plan construction | OD-004 | PF-19 | FBL-038, FBL-040 |
| FBL-044 | Operator principal registry and approval-time authentication | OD-022 | PF-20 | FBL-043 |
| FBL-063 | Review console | OD-019 | PF-28 | FBL-038, FBL-039, FBL-047 |

## Blocked by operator decision only

| Rung | Title | Blocking decisions | Blocking findings | Prerequisites |
| --- | --- | --- | --- | --- |
| FBL-002 | Identifier, envelope, and state-machine contracts | OD-004 | — | FBL-001 |
| FBL-012 | Adapter characterization suite (FX-27 … FX-30) | OD-004 | — | FBL-009, FBL-011 |
| FBL-013 | Journal writer and durability barriers | OD-005, OD-014 | — | FBL-005, FBL-007 |
| FBL-027 | Inventory manifests and reconciliation totals | OD-017 | — | FBL-026 |
| FBL-032 | Metadata extraction | OD-011 | — | FBL-026 |
| FBL-033 | Duplicate-status evidence | OD-004 | — | FBL-028 |
| FBL-043 | Dry-run planner | OD-017 | — | FBL-042 |
| FBL-051 | Threshold and stop-condition governor | OD-008 | — | FBL-048 |
| FBL-058 | Observability and redaction | OD-017 | — | FBL-052 |
| FBL-064 | Sentinel | OD-018 | — | FBL-051, FBL-059, FBL-063 |
| FBL-065 | Live adapter implementation (unexercised) | OD-016 | — | FBL-009, FBL-061 |
| FBL-067 | Live-batch executor and governor (capability) | OD-008 | — | FBL-066 |
| FBL-068 | Migration reconciliation (capability) | OD-017, OD-021 | — | FBL-027, FBL-039, FBL-067 |

## Blocked by planning finding only

| Rung | Title | Blocking decisions | Blocking findings | Prerequisites |
| --- | --- | --- | --- | --- |
| FBL-004 | Command and event contracts | — | PF-06 | FBL-003 |
| FBL-008 | Adapter capability contract | — | PF-04 | FBL-003 |
| FBL-017 | SQLite projection and idempotent apply | — | PF-01, PF-02 | FBL-016 |
| FBL-018 | Replay and rebuild from genesis | — | PF-02 | FBL-015, FBL-017 |
| FBL-019 | Atomic checkpoints and sealing | — | PF-03 | FBL-018 |
| FBL-021 | Symbolic root registry and path authority | — | PF-12 | FBL-010, FBL-020 |
| FBL-023 | Identity keys, evidence grades, and logical file identity | — | PF-11 | FBL-022 |
| FBL-026 | Read-only inventory | — | PF-13 | FBL-021, FBL-025 |
| FBL-028 | Hard-link sets | — | PF-07 | FBL-025 |
| FBL-029 | Symlinks | — | PF-08 | FBL-025 |
| FBL-031 | Package bundles | — | PF-14 | FBL-029 |
| FBL-035 | Rule loader and static validation | — | PF-16 | FBL-034 |
| FBL-037 | Classification proposals | — | PF-17 | FBL-036 |
| FBL-040 | Preservation profile resolution and capability-mismatch protocol | — | PF-19 | FBL-012, FBL-030, FBL-031 |
| FBL-045 | Approval request, minting, and content binding | — | PF-09, PF-21 | FBL-041, FBL-044 |
| FBL-047 | Backend authorization evaluation, consumption, and anti-replay | — | PF-01, PF-05 | FBL-046 |
| FBL-048 | Copy execution: token-gated atomic promote and content verification | — | PF-22 | FBL-007, FBL-013, FBL-047 |
| FBL-049 | Property reproduction (preservation-aware copy) | — | PF-08 | FBL-040, FBL-048 |
| FBL-052 | Copy verification | — | PF-23 | FBL-048, FBL-050 |
| FBL-053 | Preservation comparison report and retirement-eligibility evaluator | — | PF-24 | FBL-049, FBL-052 |

## No direct blocker — gated only by prerequisite rungs

These rungs need no decision and no finding resolved. They become available as their prerequisite
chain completes.

| Rung | Title | Blocking decisions | Blocking findings | Prerequisites |
| --- | --- | --- | --- | --- |
| FBL-006 | Fixture generator framework and expectations contract | — | — | FBL-001 |
| FBL-007 | Fault-injection adapter and process-kill harness | — | — | FBL-006 |
| FBL-009 | Adapter port and synthetic adapter | — | — | FBL-007, FBL-008 |
| FBL-010 | Path normalization and raw-byte discipline | — | — | FBL-009 |
| FBL-011 | Identity fixture corpus (FX-01 … FX-26) | — | — | FBL-006, FBL-010 |
| FBL-014 | Journal segments, sealing, and the run lock | — | — | FBL-013 |
| FBL-015 | Journal fixture corpus | — | — | FBL-006, FBL-014 |
| FBL-016 | Journal reader, chain verifier, and corruption branches | — | — | FBL-015 |
| FBL-020 | Restart reconciliation, journal side (R1–R8, R12–R14) | — | — | FBL-008, FBL-019 |
| FBL-022 | Collision detection and classification | — | — | FBL-012, FBL-021 |
| FBL-024 | Change tokens and same-path replacement detection | — | — | FBL-020, FBL-023 |
| FBL-030 | Sparse, zero-byte, and very large files | — | — | FBL-025 |
| FBL-036 | Rule evaluation, conflict resolution, and determinism | — | — | FBL-032, FBL-033, FBL-035 |
| FBL-039 | Duplicate grouping and canonical recommendation | — | — | FBL-028, FBL-038 |
| FBL-042 | Plan-time collision and destination safety | — | — | FBL-022, FBL-041 |
| FBL-046 | Approval fixture corpus | — | — | FBL-006, FBL-045 |
| FBL-050 | Protected-vault enforcement | — | — | FBL-042, FBL-048 |
| FBL-054 | Crash matrix, pre-finalize rows I0–I8 | — | — | FBL-007, FBL-020, FBL-053 |
| FBL-055 | Crash matrix, indeterminate finalize rows I9–I11 | — | — | FBL-054 |
| FBL-056 | Crash matrix I12–I16, orphan sweep, and reconciliation R9–R11 | — | — | FBL-055 |
| FBL-057 | Batch interruption and resume conformance | — | — | FBL-056 |
| FBL-059 | Incident and reason-code surface | — | — | FBL-047, FBL-058 |
| FBL-060 | Hostile-path fixtures and the standing safety suite | — | — | FBL-011, FBL-059 |
| FBL-061 | Descriptor drift and remount stop conditions | — | — | FBL-012, FBL-060 |
| FBL-062 | Rollback engine and drill harness | — | — | FBL-047, FBL-053, FBL-057 |
| FBL-066 | Copied-pilot orchestration (capability) | — | — | FBL-051, FBL-062 |
| FBL-069 | Maintenance mode (capability) | — | — | FBL-068 |
| FBL-070 | G4 dry-run readiness assembler | — | — | FBL-058, FBL-061, FBL-065, FBL-069 |
| FBL-001 | Repository tooling, evidence emitter, and CI safety guards | — | — | none |
