# Operator Decision Session Guide

> **Non-authoritative.** This guide organises decisions for review. It decides nothing, and
> **Claude has not decided any of them.** A decision takes effect only when the operator records it
> in `docs/05-governance/open-decisions.md`.

24 open decisions, grouped into six sessions so they can be resolved in focused sittings rather
than by reading the whole repository. Sessions are ordered by the gate they unblock.

**No time estimate is given.** Complexity is marked low, medium, or high; how long that takes
depends on how much source information the operator already has to hand.

## Session order and what each unblocks

| Session | Focus | Gate unblocked | Decisions |
| --- | --- | --- | --- |
| 1 | The one decision that unblocks everything | `implementation` (G3) | OD-004 |
| 2 | Remaining G3 implementation blockers | `implementation` (G3) | OD-014, OD-017, OD-022, OD-024 |
| 3 | Before the first live read | `dry_run` (G4) | OD-001, OD-002, OD-003, OD-005, OD-011, OD-012, OD-016, OD-023 |
| 4 | Before the copied pilot | `pilot` (G5) | OD-007, OD-008 |
| 5 | Before limited live | `live` (G6) | OD-006, OD-009, OD-013, OD-015, OD-018, OD-019, OD-020 |
| 6 | Before retirement and completion | `retirement` (G7) and `migration_completion` (G8) | OD-010, OD-021 |

> **Read the sessions in order.** Later sessions assume earlier ones closed; resolving a G6
> decision while OD-004 is still open buys nothing, because no implementation can proceed.

---

## Session 1 — The one decision that unblocks everything

**Gate unblocked:** `implementation` (G3)
**Decisions:** 1
**Complexity:** medium

Resolving OD-004 is the single highest-leverage act available. Until it closes, only 3 of 70 G3 rungs are reachable and the entire contract chain is frozen.

### Prerequisite reading

- `docs/05-governance/open-decisions.md` — the register rows for the decisions below
- `docs/proposals/operator-decisions/` — one brief per decision, each with options and a recommendation
- `docs/proposals/g3-readiness-map.md` — what is currently reachable

### The exact questions

| Decision | Question | Complexity | Recommended default |
| --- | --- | --- | --- |
| **OD-004** | Which cryptographic hash algorithm does V1 use, and does the same choice govern the journal chain digest? | medium | Option 2 |

### What can proceed after this session

FBL-002 becomes specification-ready, which unfreezes the contract chain behind it. Combined with the planning findings, the reachable frontier grows from 3 rungs to 12.

### What still cannot proceed

Nothing is authorized by resolving a decision. Every gate still requires its own dated,
operator-signed authorization record in `docs/05-governance/authorization-ledger.md`. Absence of a
record remains a prohibition, not a gap.

---

## Session 2 — Remaining G3 implementation blockers

**Gate unblocked:** `implementation` (G3)
**Decisions:** 4
**Complexity:** high, low, medium  — includes high-complexity items: OD-022

These four decisions each block a specific G3 rung. None is on the critical path the way OD-004 is, but each stops its rung dead.

### Prerequisite reading

- `docs/05-governance/open-decisions.md` — the register rows for the decisions below
- `docs/proposals/operator-decisions/` — one brief per decision, each with options and a recommendation
- `docs/proposals/g3-readiness-map.md` — what is currently reachable

### The exact questions

| Decision | Question | Complexity | Recommended default |
| --- | --- | --- | --- |
| **OD-014** | Which migration-control directory schema is canonical — the assignment layout or the operations-manual layout? | low | Option 1 |
| **OD-017** | What are the default report formats — Markdown, CSV, JSON, or a combination? | low | Option 1 |
| **OD-022** | What operator authentication model does V1 use for approvals? | high | Option 1 |
| **OD-024** | Does V1 reproduce symbolic links and hard links faithfully, or declare link reproduction out of scope with a stop condition? | medium | Option 1 if the corpus contains meaningful link structure; Option 2 if it does not |

### What can proceed after this session

The control-plane, report-emitting, authentication, and link-scope rungs become specification-ready.

### What still cannot proceed

Nothing is authorized by resolving a decision. Every gate still requires its own dated,
operator-signed authorization record in `docs/05-governance/authorization-ledger.md`. Absence of a
record remains a prohibition, not a gap.

---

## Session 3 — Before the first live read

**Gate unblocked:** `dry_run` (G4)
**Decisions:** 8
**Complexity:** high, low, medium  — includes high-complexity items: OD-003, OD-012, OD-016

G4 is the first gate at which the system touches the real NAS, and then only to read. Seven decisions gate it. Two of them — identity privacy and derived-artifact retention — are privacy judgements rather than technical ones.

### Prerequisite reading

- `docs/05-governance/open-decisions.md` — the register rows for the decisions below
- `docs/proposals/operator-decisions/` — one brief per decision, each with options and a recommendation
- `docs/proposals/g3-readiness-map.md` — what is currently reachable

### The exact questions

| Decision | Question | Complexity | Recommended default |
| --- | --- | --- | --- |
| **OD-001** | Which Synology share roots are in and out of scope? | medium | see the brief |
| **OD-002** | Is the destination taxonomy frozen, and in what form? | medium | see the brief |
| **OD-003** | Is any person-identity assistance permitted, and under what confirmation requirements? | high | see the brief |
| **OD-005** | Where does control data live, and what is its backup policy? | low | see the brief |
| **OD-011** | May the worker retain thumbnails or extracted text from real media? | medium | see the brief |
| **OD-012** | Confirm the Dogs, drone, CSV, and identity-candidate rules. | high | see the brief |
| **OD-016** | Which adapter accesses the NAS? | high | see the brief |
| **OD-023** | May a dry-run plan generated without a measured destination descriptor ever be promoted to execution? | medium | Option 1 |

### What can proceed after this session

The dry run can be requested. Nothing is authorized by resolving these; G4 still needs its own operator authorization record.

### What still cannot proceed

Nothing is authorized by resolving a decision. Every gate still requires its own dated,
operator-signed authorization record in `docs/05-governance/authorization-ledger.md`. Absence of a
record remains a prohibition, not a gap.

---

## Session 4 — Before the copied pilot

**Gate unblocked:** `pilot` (G5)
**Decisions:** 2
**Complexity:** medium

The pilot runs against an isolated copy. These decisions size and select it.

### Prerequisite reading

- `docs/05-governance/open-decisions.md` — the register rows for the decisions below
- `docs/proposals/operator-decisions/` — one brief per decision, each with options and a recommendation
- `docs/proposals/g3-readiness-map.md` — what is currently reachable

### The exact questions

| Decision | Question | Complexity | Recommended default |
| --- | --- | --- | --- |
| **OD-007** | Which dataset is the copied pilot corpus? | medium | see the brief |
| **OD-008** | What are the batch-size and stop thresholds? | medium | see the brief |

### What can proceed after this session

The copied pilot can be requested.

### What still cannot proceed

Nothing is authorized by resolving a decision. Every gate still requires its own dated,
operator-signed authorization record in `docs/05-governance/authorization-ledger.md`. Absence of a
record remains a prohibition, not a gap.

---

## Session 5 — Before limited live

**Gate unblocked:** `live` (G6)
**Decisions:** 7
**Complexity:** low, medium

The first writes to authoritative destinations. Recovery posture is the load-bearing decision here.

### Prerequisite reading

- `docs/05-governance/open-decisions.md` — the register rows for the decisions below
- `docs/proposals/operator-decisions/` — one brief per decision, each with options and a recommendation
- `docs/proposals/g3-readiness-map.md` — what is currently reachable

### The exact questions

| Decision | Question | Complexity | Recommended default |
| --- | --- | --- | --- |
| **OD-006** | Is snapshot or equivalent recovery coverage confirmed? | medium | see the brief |
| **OD-009** | Copy-first or move, per phase? | medium | see the brief |
| **OD-013** | Confirm live structure versus intended structure. | medium | see the brief |
| **OD-015** | Where are the taxonomy edges and aliases? | medium | see the brief |
| **OD-018** | What exact wording and severity do Sentinel alerts use? | low | Option 1 |
| **OD-019** | Which stack does the review console use? | low | Option 1 |
| **OD-020** | When is the project path created on the NAS? | low | see the brief |

### What can proceed after this session

A bounded live batch can be requested. Retirement is still not authorized — that is G7.

### What still cannot proceed

Nothing is authorized by resolving a decision. Every gate still requires its own dated,
operator-signed authorization record in `docs/05-governance/authorization-ledger.md`. Absence of a
record remains a prohibition, not a gap.

---

## Session 6 — Before retirement and completion

**Gate unblocked:** `retirement` (G7) and `migration_completion` (G8)
**Decisions:** 2
**Complexity:** medium

Retirement is retention, not removal; permanent deletion is unavailable in V1 regardless of what is decided here.

### Prerequisite reading

- `docs/05-governance/open-decisions.md` — the register rows for the decisions below
- `docs/proposals/operator-decisions/` — one brief per decision, each with options and a recommendation
- `docs/proposals/g3-readiness-map.md` — what is currently reachable

### The exact questions

| Decision | Question | Complexity | Recommended default |
| --- | --- | --- | --- |
| **OD-010** | What is the quarantine retention and future deletion policy? | medium | see the brief |
| **OD-021** | What counts as migration completeness, and what residual-exception tolerance is acceptable? | medium | see the brief |

### What can proceed after this session

Source retirement and migration completion can be requested.

### What still cannot proceed

Nothing is authorized by resolving a decision. Every gate still requires its own dated,
operator-signed authorization record in `docs/05-governance/authorization-ledger.md`. Absence of a
record remains a prohibition, not a gap.

---

## A note on sequencing

Session 1 contains one decision. That is deliberate, and it is the most important structural fact
in this guide: **OD-004 alone gates 67 of the 70 G3 rungs.** Every other decision, and every one of
the 30 open planning findings, can be resolved without moving the implementation frontier past 3
rungs while OD-004 stays open.

If only one session happens, it should be Session 1.

