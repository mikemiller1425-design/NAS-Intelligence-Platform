# OD-025 (PROPOSED) — Where may live-gate evidence and live adapter configuration exist, and what redaction applies before commit?

> **Non-authoritative, and not yet registered.** This decision does not exist in
> `docs/05-governance/open-decisions.md`. It is *proposed* here because a stress-test finding cannot
> be closed without it. Registering it is a governance act for the operator or Chief Systems
> Architect — **Claude has not decided it and has not registered it.**

| Field | Value |
| --- | --- |
| Proposed ID | OD-025 |
| Status | **Proposed, not registered** |
| Suggested `blocks_gate` | `dry_run` |
| Forced by | BLT-B03, BLT-M10 |
| Recorded in | `docs/audits/build-ladder-stress-test.md` |

## The decision being requested

Where may live-gate evidence and live adapter configuration exist, and what redaction applies before commit?

## Why it is needed

The path policy places *generated artifacts — plans, commands, adapter inputs, manifests, and any runtime output* in Class B, with no exemption possible. But G4's required evidence is exactly that: a confirmed root list, a control-data root declaration with its disjointness proof, and an inventory manifest of a live NAS root. Both G4 rungs commit that evidence.

An inventory manifest of a live root **is** a literal live path in a committed generated artifact. As the policy stands, the path-policy check fails the first G4 commit and there is no legal fix.

Separately, FBL-071 must configure a read-only mount naming the confirmed live root — but `config/` is Class B, and the policy states that nothing in it authorizes a configuration default to name a live path. No document says where live configuration may exist.

## Safe options

**1. Live evidence stays in the control-data root; only redacted or hashed forms are committed**

The repository holds evidence *about* the run, never raw live paths. FBL-058's redaction is named as the mechanism in the G4+ Definition of Done.

*Tradeoff:* Keeps Class B absolute. Costs a redaction step and means the committed evidence is one step removed from the raw artifact — an auditor must trust the redaction.

**2. Add a gate-scoped Class D for post-G3 evidence artifacts**

A fourth class permitting literal live paths in committed evidence produced at G4 and later, narrowly scoped by path and gate.

*Tradeoff:* Simplest to implement and keeps evidence verbatim. Weakens the current guarantee that no committed artifact outside declared documentation carries a live path.

**3. Keep live evidence out of the repository entirely**

Evidence lives only in the control-data root and is never committed.

*Tradeoff:* Strongest privacy posture. But it breaks the evidence standard's reproducibility expectation and makes independent review much harder.

## Recommendation

**Option 1.** It preserves Class B without exception, which is the property that makes the policy trustworthy, and it gives the redaction rung a clear purpose. The cost — an auditor trusting the redaction — is addressable by hashing the raw artifact and committing the hash alongside.

## What the operator must supply

A choice among the three, plus the redaction rule if Option 1, plus a statement of where live adapter configuration may exist.

## If it is not registered

The finding that forces it stays open, and the gate it guards cannot be entered without knowingly
proceeding against a recorded contradiction.
