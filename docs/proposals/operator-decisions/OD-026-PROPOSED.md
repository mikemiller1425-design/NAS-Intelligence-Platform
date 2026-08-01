# OD-026 (PROPOSED) — May the G5 pilot zone reside on the NAS?

> **Non-authoritative, and not yet registered.** This decision does not exist in
> `docs/05-governance/open-decisions.md`. It is *proposed* here because a stress-test finding cannot
> be closed without it. Registering it is a governance act for the operator or Chief Systems
> Architect — **Claude has not decided it and has not registered it.**

| Field | Value |
| --- | --- |
| Proposed ID | OD-026 |
| Status | **Proposed, not registered** |
| Suggested `blocks_gate` | `pilot` |
| Forced by | BLT-B04 |
| Recorded in | `docs/audits/build-ladder-stress-test.md` |

## The decision being requested

May the G5 pilot zone reside on the NAS?

## Why it is needed

`SAF-006` is a BLOCKER acceptance row: *No live NAS mutation is authorized at any gate before G6.* FBL-073 is gate G5 with `NAS access: bounded-write`, described as "the first legal write".

The authority order resolves conflicts in favour of the stricter safety rule, so **SAF-006 currently prohibits FBL-073.** The Build Ladder's assumed resolution of PF-25 — that destination characterization opens G5 — is not presently permitted.

## Safe options

**1. Pilot zone is on the NAS; amend SAF-006**

Change SAF-006 to permit bounded writes into an isolated, non-authoritative pilot zone at G5.

*Tradeoff:* Makes the ladder's assumed resolution legal and lets G5 characterize a destination on the same storage as the real one — which is what makes the descriptor meaningful. Requires amending a BLOCKER safety row, which is an operator-authority act.

**2. Pilot zone is off the NAS; leave SAF-006 intact**

The copied corpus lives on local or other storage.

*Tradeoff:* No safety row changes. But the destination descriptor measured there does not describe the real destination, which hardens BLT-B05 rather than resolving it.

**3. Split: pilot corpus off-NAS, destination characterization deferred to G6 under its own approval**

Keeps G5 entirely off the NAS and moves characterization to where the authoritative write happens.

*Tradeoff:* Cleanest against SAF-006, but concentrates more first-time risk at G6.

## Recommendation

**No recommendation.** This is a genuine safety-posture trade the operator must make: Option 1 buys a meaningful descriptor at the cost of amending a BLOCKER safety row; Options 2 and 3 preserve the row and pay elsewhere. Recommending a safety-row amendment is not mine to do.

## What the operator must supply

Which option, and if Option 1, explicit authorization to amend SAF-006 through change control.

## If it is not registered

The finding that forces it stays open, and the gate it guards cannot be entered without knowingly
proceeding against a recorded contradiction.
