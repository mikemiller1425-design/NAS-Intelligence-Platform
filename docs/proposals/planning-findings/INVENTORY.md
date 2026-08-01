# Planning Findings Inventory

> **Non-authoritative.** This inventory routes and cross-references the planning findings recorded
> in `docs/handoffs/build-ladder.md`. It resolves nothing and changes no specification.

Generated from the Build Ladder at commit `8838ac6`. **31 findings, 30 open, 1 closed.**

| Severity | Count |
| --- | --- |
| BLOCKER | 18 |
| MAJOR | 8 |
| MINOR | 4 |
| NOTE | 1 |

PF-31 is recorded in the ladder as **closed by FBL-005** and is not treated as open here.

## Inventory

| ID | Severity | State | Analysis lane | Blocked rungs | Related decisions | Cluster | Authority to resolve |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PF-01 | BLOCKER | open | A — domain & persistence | FBL-017, FBL-047 | — | CL-1 authority of authorization facts | change control |
| PF-02 | BLOCKER | open | A — domain & persistence | FBL-005, FBL-017, FBL-018 | OD-004 | independent | change control |
| PF-03 | MAJOR | open | A — domain & persistence | FBL-019 | — | independent | change control |
| PF-04 | BLOCKER | open | A — domain & persistence | FBL-003, FBL-008 | OD-004 | CL-3 missing domain entities | change control |
| PF-05 | BLOCKER | open | A — domain & persistence | FBL-003, FBL-005, FBL-047 | OD-004 | CL-1 authority of authorization facts | change control |
| PF-06 | MAJOR | open | A — domain & persistence | FBL-004 | — | independent | change control |
| PF-07 | BLOCKER | open | B — filesystem identity & preservation | FBL-003, FBL-028 | OD-004 | CL-3 missing domain entities | change control |
| PF-08 | BLOCKER | open | B — filesystem identity & preservation | FBL-003, FBL-029, FBL-049 | OD-004 | CL-6 link reproduction | operator + change control |
| PF-09 | BLOCKER | open | A — domain & persistence | FBL-005, FBL-045 | OD-004 | CL-2 canonical serialization and everything it binds | change control |
| PF-10 | BLOCKER | open | B — filesystem identity & preservation | FBL-025 | OD-004 | CL-4 copy correctness and its evidence | change control |
| PF-11 | BLOCKER | open | B — filesystem identity & preservation | FBL-003, FBL-023 | OD-004 | independent | change control |
| PF-12 | BLOCKER | open | C — rules, taxonomy & governance | FBL-021 | — | CL-5 rule and taxonomy contracts | change control |
| PF-13 | MAJOR | open | B — filesystem identity & preservation | FBL-026, FBL-072 | — | independent | change control |
| PF-14 | BLOCKER | open | B — filesystem identity & preservation | FBL-031 | — | independent | change control |
| PF-15 | BLOCKER | open | C — rules, taxonomy & governance | FBL-034 | OD-002, OD-014 | CL-5 rule and taxonomy contracts | change control |
| PF-16 | MAJOR | open | C — rules, taxonomy & governance | FBL-035 | — | CL-5 rule and taxonomy contracts | operator + change control |
| PF-17 | MINOR | open | C — rules, taxonomy & governance | FBL-037 | — | independent | change control |
| PF-18 | MAJOR | open | C — rules, taxonomy & governance | FBL-038 | OD-017 | independent | change control |
| PF-19 | BLOCKER | open | A — domain & persistence | FBL-040, FBL-041 | OD-004 | CL-2 canonical serialization and everything it binds | change control |
| PF-20 | MAJOR | open | C — rules, taxonomy & governance | FBL-044 | OD-022 | independent | change control |
| PF-21 | BLOCKER | open | A — domain & persistence | FBL-045 | — | CL-2 canonical serialization and everything it binds | change control |
| PF-22 | BLOCKER | open | B — filesystem identity & preservation | FBL-048 | — | CL-4 copy correctness and its evidence | change control |
| PF-23 | BLOCKER | open | A — domain & persistence | FBL-052 | — | CL-4 copy correctness and its evidence | change control |
| PF-24 | BLOCKER | open | A — domain & persistence | FBL-053 | — | CL-3 missing domain entities | change control |
| PF-25 | BLOCKER | open | C — rules, taxonomy & governance | FBL-072, FBL-073 | OD-007, OD-008 | CL-7 G4 semantics | operator + change control |
| PF-26 | MINOR | open | B — filesystem identity & preservation | — | — | independent | change control |
| PF-27 | MINOR | open | B — filesystem identity & preservation | — | — | CL-6 link reproduction | change control |
| PF-28 | MAJOR | open | C — rules, taxonomy & governance | FBL-063 | OD-019 | independent | change control |
| PF-29 | MAJOR | open | C — rules, taxonomy & governance | FBL-045, FBL-072 | — | CL-7 G4 semantics | change control |
| PF-30 | MINOR | open | C — rules, taxonomy & governance | — | — | independent | change control |
| PF-31 | NOTE | closed | closed | FBL-005 | OD-004 | independent | change control |

## Atomic clusters

Findings that share an underlying defect and must be resolved together. Resolving one alone would
leave the specification inconsistent in a different way.

**CL-1 authority of authorization facts** — PF-01, PF-05

**CL-2 canonical serialization and everything it binds** — PF-09, PF-21, PF-19

**CL-3 missing domain entities** — PF-04, PF-07, PF-24

**CL-4 copy correctness and its evidence** — PF-22, PF-23, PF-10

**CL-5 rule and taxonomy contracts** — PF-12, PF-15, PF-16

**CL-6 link reproduction** — PF-08, PF-27

**CL-7 G4 semantics** — PF-25, PF-29

Findings not listed above are independently resolvable.

## Findings requiring operator input as well as change control

| Finding | Operator decision | What is the operator's half |
| --- | --- | --- |
| PF-08 | OD-024 | Whether V1 reproduces links faithfully or declares them out of scope. The entry-type specification is change control; the scope choice is not. |
| PF-25 | OD-023 | Whether a descriptor-incomplete G4 plan may ever be promoted. The gate semantics are change control; the promotability rule is not. |
| PF-16 | OD-012 (timing) | The defect — that closing a decision breaks the shipped example — is pure change control. The operator's half is only *when* OD-012 closes. |

Every other finding is a specification defect resolvable through change control alone.

## Verification

Every finding recorded in the Build Ladder appears here exactly once, and every finding here
appears in the ladder. Verified mechanically by `scripts/validate_proposals.py`.

## Finding to packet routing

Every open finding is covered by exactly one packet. `PF-31` is recorded in the ladder as closed by
FBL-005 and is not routed.

| Finding | Packet | Batch |
| --- | --- | --- |
| PF-01 | [PKT-02-journal-authority](PKT-02-journal-authority.md) — Journal authority and record vocabulary | BATCH-02 |
| PF-02 | [PKT-02-journal-authority](PKT-02-journal-authority.md) — Journal authority and record vocabulary | BATCH-02 |
| PF-03 | [PKT-07-checkpoint-sealing](PKT-07-checkpoint-sealing.md) — Checkpoint sealing is defined only for mutation scopes | BATCH-07 |
| PF-04 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-05 | [PKT-02-journal-authority](PKT-02-journal-authority.md) — Journal authority and record vocabulary | BATCH-02 |
| PF-06 | [PKT-08-approval-event-vocabulary](PKT-08-approval-event-vocabulary.md) — The approval state machine has no event vocabulary | BATCH-08 |
| PF-07 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-08 | [PKT-04-link-and-content-class](PKT-04-link-and-content-class.md) — Link and content-class operation semantics | BATCH-04 |
| PF-09 | [PKT-01-canonicalization](PKT-01-canonicalization.md) — Digest and canonical serialization | BATCH-01 |
| PF-10 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-11 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-12 | [PKT-09-config-contracts](PKT-09-config-contracts.md) — Root registry, taxonomy contract, and placeholder registry | BATCH-09 |
| PF-13 | [PKT-06-read-only-proof](PKT-06-read-only-proof.md) — Proving read-only inventory | BATCH-06 |
| PF-14 | [PKT-05-copy-window-integrity](PKT-05-copy-window-integrity.md) — Copy-window integrity: token gate and bundle atomicity | BATCH-05 |
| PF-15 | [PKT-09-config-contracts](PKT-09-config-contracts.md) — Root registry, taxonomy contract, and placeholder registry | BATCH-09 |
| PF-16 | [PKT-10-decision-closure](PKT-10-decision-closure.md) — Decision closure breaks the shipped rule set | BATCH-10 |
| PF-17 | [PKT-11-decision-lifecycle-and-unresolved](PKT-11-decision-lifecycle-and-unresolved.md) — Classification decision lifecycle and the unresolved queue | BATCH-11 |
| PF-18 | [PKT-11-decision-lifecycle-and-unresolved](PKT-11-decision-lifecycle-and-unresolved.md) — Classification decision lifecycle and the unresolved queue | BATCH-11 |
| PF-19 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-20 | [PKT-12-authority-and-ingress](PKT-12-authority-and-ingress.md) — Authority classes and command ingress | BATCH-12 |
| PF-21 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-22 | [PKT-05-copy-window-integrity](PKT-05-copy-window-integrity.md) — Copy-window integrity: token gate and bundle atomicity | BATCH-05 |
| PF-23 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-24 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-25 | [PKT-13-g4-semantics](PKT-13-g4-semantics.md) — G4 semantics: runtime mode and descriptor completeness | BATCH-13 |
| PF-26 | [PKT-04-link-and-content-class](PKT-04-link-and-content-class.md) — Link and content-class operation semantics | BATCH-04 |
| PF-27 | [PKT-03-domain-entities](PKT-03-domain-entities.md) — Domain entity completion | BATCH-03 |
| PF-28 | [PKT-12-authority-and-ingress](PKT-12-authority-and-ingress.md) — Authority classes and command ingress | BATCH-12 |
| PF-29 | [PKT-13-g4-semantics](PKT-13-g4-semantics.md) — G4 semantics: runtime mode and descriptor completeness | BATCH-13 |
| PF-30 | [PKT-09-config-contracts](PKT-09-config-contracts.md) — Root registry, taxonomy contract, and placeholder registry | BATCH-09 |
| PF-31 | *closed by FBL-005; not routed* | — |
