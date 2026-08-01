# Remediation workbench

> **Everything under `docs/proposals/` is non-authoritative.** It proposes; it does not apply. No file
> here changes a specification, resolves an operator decision, freezes the Build Ladder, or authorizes
> any gate. Adopting anything here requires change control, and every operator decision named remains
> the operator's.

This directory exists so that the operator, the Chief Systems Architect, and an independent reviewer
can resolve the platform's specification defects **in coherent batches, without rediscovering the
contradictions each time**. It is a preparation package, not a change.

## What is here

| Path | What it is |
| --- | --- |
| `planning-findings/INVENTORY.md` | The routing index. All 31 planning findings, their severity, lane, blocked rungs, related decisions, atomic cluster, and which packet covers them. |
| `planning-findings/PKT-01…PKT-13` | Thirteen remediation packets covering all **30 open** findings. One packet per atomic cluster. |
| `operator-decisions/OD-001…OD-024` | A decision brief for each registered open decision. **Every brief states that Claude has not decided it.** |
| `operator-decisions/OD-025-PROPOSED…OD-027-PROPOSED` | Three decisions this analysis argues are needed but which are **deliberately not added** to `open-decisions.md`, because that register is authoritative and only the operator adds to it. |
| `operator-decision-session.md` | Six proposed decision sessions, grouped so related questions are answered together. |
| `change-control-batch-plan.md` | Fifteen batches. Batches 01–13 correspond one-to-one with the packets; 14 and 15 carry the stress-test findings. |
| `g3-readiness-map.md` | Which G3 rungs are specification-ready, which are authorized, and which are implemented — three states, none inferable from another. |

Two related artifacts live outside this directory:

- `docs/audits/build-ladder-stress-test.md` — an adversarial review of the Build Ladder, 8 BLOCKER /
  13 MAJOR / 10 MINOR / 2 NOTE findings, prefixed `BLT-`.
- `scripts/validate_proposals.py` — twelve documentation-structure checks over this directory. It
  implements no product behaviour, touches no NAS path, and mutates nothing.

## Where to start

**If you are the operator:** start with `operator-decision-session.md`. Session 1 contains only
OD-004. If only one session happens, it should be Session 1 — see below.

**If you are the Chief Systems Architect:** start with `change-control-batch-plan.md`, then read the
packets in batch order. Four items are flagged as needing your sign-off specifically rather than
routine change control: the PF-02 branch (BATCH-02), the BATCH-03/BATCH-05 adjacency constraint, the
PKT-07 provenance caveat, and AC-3 plus the Class F1 origin-independence clause in BATCH-12.

**If you are an independent reviewer:** start with `planning-findings/INVENTORY.md` for coverage, then
`docs/audits/build-ladder-stress-test.md` for what an adversarial pass found in the ladder itself.

## The one fact that shapes everything else

Measured against the ladder's own blocking graph:

| Scenario | Reachable G3 rungs |
| --- | --- |
| Today | **3 of 70** |
| Every decision resolved, no finding resolved | 4 of 70 |
| Every finding resolved, no decision resolved | 3 of 70 |
| OD-004 plus every finding resolved | 12 of 70 |
| Everything resolved | 70 of 70 |

**OD-004 — the hash algorithm — alone gates 67 of 70 G3 rungs**, because it blocks FBL-002, the
prerequisite of the entire contract chain. Resolving every other decision and leaving OD-004 open
moves the frontier by one rung. The ladder does not state this anywhere; it has to be derived, which
is why it is stated here.

## What this package deliberately does not do

- **It does not resolve any operator decision.** Every brief carries the literal statement that Claude
  has not decided it, and `validate_proposals.py` check 4 enforces that.
- **It does not add to `open-decisions.md`.** Three decisions this analysis argues are missing are
  carried as `-PROPOSED` files instead, because that register is a governance document.
- **It does not modify any authoritative specification.** Check 8 enforces that proposals live only
  under `docs/proposals/` and `docs/audits/`.
- **It does not authorize G3 or any later gate.** Check 11 asserts G3 through G8 remain marked
  NOT AUTHORIZED in the ledger.

## A caveat on line references

Packets cite `file:line` extensively, as of commit `8838ac6`. Those citations were spot-verified
against the repository, but they are **navigational anchors, not stable addresses** — any edit above a
cited line moves it. Where a citation and a section heading disagree, trust the heading and the quoted
text, both of which are reproduced in the packets for exactly this reason.

## Reading a packet

Each packet answers the same eighteen questions in the same order: the finding IDs and severity, the
exact contradiction with citations on both sides, the operational consequence if left unresolved, the
affected entities and fields, the affected events and records, the proposed normative resolution,
alternatives considered and why rejected, safety implications, migration implications, required tests
(positive, negative, failure-injection), required documentation changes, required ADR changes, whether
operator policy is required, atomicity, the verification procedure, and the change-control authority.

Where a packet proposes a schema or record, it gives exact field names, types, required and nullable
status, invariants, and canonicalization rules. Where it names a file that does not exist yet, the
sentence naming it says so — that is how `validate_proposals.py` check 10 distinguishes a proposed
artifact from a broken link.
