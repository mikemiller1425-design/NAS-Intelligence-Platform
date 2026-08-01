# OD-027 (PROPOSED) — When is the authoritative destination characterized, and under whose approval?

> **Non-authoritative, and not yet registered.** This decision does not exist in
> `docs/05-governance/open-decisions.md`. It is *proposed* here because a stress-test finding cannot
> be closed without it. Registering it is a governance act for the operator or Chief Systems
> Architect — **Claude has not decided it and has not registered it.**

| Field | Value |
| --- | --- |
| Proposed ID | OD-027 |
| Status | **Proposed, not registered** |
| Suggested `blocks_gate` | `live` |
| Forced by | BLT-B05 |
| Recorded in | `docs/audits/build-ladder-stress-test.md` |

## The decision being requested

When is the authoritative destination characterized, and under whose approval?

## Why it is needed

A capability descriptor is valid only if measured, and a hand-written one is rejected. The destination descriptor is frozen into the plan at approval, and descriptor drift is a **fatal** stop.

FBL-073 characterizes only the isolated pilot zone. FBL-075 is the first authoritative-destination write and has no characterization deliverable. So its plan either carries the pilot-zone descriptor — measured against a different destination, so drift fires fatally — or carries none, which is invalid.

**No rung in the ladder ever measures the authoritative destination.**

## Safe options

**1. Insert a characterization rung at G6, before FBL-075**

A dedicated rung whose only job is to characterize the authoritative destination under its own operator approval.

*Tradeoff:* Explicit and reviewable. Adds a rung and one more approval step. The characterization write is still a write to live data before any verified copy exists, which needs its own justification.

**2. Extend FBL-073 to characterize the authoritative destination**

Widen the pilot rung's scope.

*Tradeoff:* No new rung. But it reopens BLT-B04, because it means a G5 write to an authoritative destination — which SAF-006 forbids and the pilot's own prohibited work excludes.

**3. Accept the pilot-zone descriptor for the authoritative destination if they are provably on the same volume and filesystem**

Treat co-located storage as equivalent.

*Tradeoff:* Avoids a new write entirely. Requires a defensible equivalence proof, and the descriptor rules currently admit no notion of equivalence — only measurement.

## Recommendation

**Option 1**, contingent on OD-026. It is the only option that keeps the descriptor honest without reopening the SAF-006 conflict. The characterization write should be minimal, into a designated area, and journalled like any other mutation.

## What the operator must supply

Which option, the approval that governs the characterization write, and whether it needs its own gate entry.

## If it is not registered

The finding that forces it stays open, and the gate it guards cannot be entered without knowingly
proceeding against a recorded contradiction.
