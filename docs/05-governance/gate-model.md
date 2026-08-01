# Gate Model

## Purpose

This document is the single authoritative definition of the authorization gates for the NAS Intelligence Platform. It exists to resolve audit finding **FND-B001** (circular Foundation acceptance gate) and **FND-m003** (decision severity conflated with the gate it blocks).

Before this document existed, Foundation approval required all BLOCKER V1 acceptance requirements to pass, but many of those requirements can only be verified by running implemented software — and implementation was itself blocked until Foundation approval. That circularity is removed here by separating **documentation acceptance** from **execution acceptance**, and by defining eight independent gates.

Any other document that describes authorization must reference this file rather than restate it.

## Two kinds of acceptance

| Kind | Question it answers | How it is verified | Gate that consumes it |
| --- | --- | --- | --- |
| **Foundation acceptance** (documentation acceptance) | Are the specifications complete, internally consistent, testable, and safe enough to authorize Build Ladder generation and fixture-only implementation? | By reading, cross-checking, and validating artifacts in this repository. No software execution required. | G1 |
| **Implementation / V1 acceptance** (execution acceptance) | Does the implemented system actually behave as specified? | By executing implemented software against fixtures, then against progressively less synthetic data under later gates. | G3 and later |

A requirement that can only be verified by executing software is **never** a Foundation-approval prerequisite. It is a prerequisite for the gate at which that execution first becomes authorized.

## Gate ladder

Gates are ordered. Each gate has its own entry criteria, evidence, and approval.

> **No gate authorizes the next gate.** Passing gate *N* produces evidence that gate *N+1* may be *considered*. It never grants gate *N+1*. Each gate requires its own explicit, dated, operator-signed authorization record naming the gate ID and the evidence bundle reviewed. **Absence of an authorization record is a prohibition, not a gap.**

**G4 is the first gate at which the system touches the real NAS at all**, and it may only read. Everything at G1–G3 is documents and synthetic fixtures.

| Gate ID | `blocks_gate` value | Name | Authorizes |
| --- | --- | --- | --- |
| G1 | `foundation` | Foundation Approval | Nothing executable. Marks the specification set as coherent enough to plan against. |
| G2 | `build_ladder` | Build Ladder Generation | Producing the rung-by-rung implementation ladder as a planning document. |
| G3 | `implementation` | Fixture-Only Implementation | Writing and running code against synthetic local fixtures only. |
| G4 | `dry_run` | Dry-Run Readiness | Read-only inventory and non-mutating plan generation against confirmed source roots. |
| G5 | `pilot` | Copied-Pilot Readiness | Execution against an isolated copied corpus. Never the authoritative source. |
| G6 | `live` | Limited-Live Readiness | Bounded, approved copy operations against live shares. |
| G7 | `retirement` | Source-Retirement Readiness | Retiring verified source items after hash verification and approval. |
| G8 | `migration_completion` | Migration Completion | Declaring the migration complete and entering maintenance. |

## Gate definitions

### G1 — Foundation Approval (`foundation`)

**Authorizes:** Nothing executable. G1 is a statement about documents.

**Explicitly does NOT authorize:**
- generating the Build Ladder (that is G2);
- writing any implementation code;
- mounting, scanning, or reading live NAS shares;
- dry-run execution of any kind;
- copying, moving, renaming, quarantining, retiring, overwriting, or deleting any file.

**Entry criteria:**
1. Every audit finding has a recorded resolution status; none is silently waived.
2. All artifacts required by `docs/05-governance/definition-of-done.md` exist and are linked.
3. Foundation-stage acceptance requirements pass (see `docs/04-acceptance/foundation-acceptance.md`).
4. One canonical rule contract exists and every example validates against it.
5. No open decision classified `blocks_gate: foundation` remains unresolved.
6. No document contradicts another on safety posture, authority order, or gate wording.

**Required evidence:** audit resolution register; Foundation-stage acceptance results; schema validation output; consistency-check results.

**Approver:** Operator, after independent verification of the audit resolutions.

**Does not authorize G2.** G2 requires its own operator authorization.

### G2 — Build Ladder Generation (`build_ladder`)

**Authorizes:** Producing `docs/handoffs/003-build-ladder.md` output — a frozen, planning-only rung ladder.

**Explicitly does NOT authorize:** implementing any rung; any filesystem mutation; any live access.

**Entry criteria:**
1. G1 passed.
2. Operator explicitly authorizes Build Ladder generation.
3. No open decision classified `blocks_gate: build_ladder` remains unresolved.

**Required evidence:** recorded operator authorization; G1 approval record.

**Approver:** Operator.

**Does not authorize G3.**

### G3 — Fixture-Only Implementation (`implementation`)

**Authorizes:** Writing implementation code and executing it **against synthetic local fixtures only**.

**Explicitly does NOT authorize:**
- pointing any adapter at a Synology share, mount, or network path;
- reading, listing, or hashing any live NAS file;
- any operation outside the fixture tree.

**Entry criteria:**
1. G2 passed and the ladder is frozen.
2. The specific rung is separately authorized. Rung *N* authorization does not authorize rung *N+1*.
3. Fixture corpus requirements are defined (see `tests/fixtures/README.md`).
4. No open decision classified `blocks_gate: implementation` remains unresolved for the rung in question.

**Required evidence:** per-rung authorization record; fixture test results; evidence package per `docs/05-governance/evidence-standard.md`.

**Approver:** Operator, per rung.

**Does not authorize G4.**

### G4 — Dry-Run Readiness (`dry_run`)

**Authorizes:**
- **Read-only** traversal of confirmed NAS source roots — inventory, hashing, metadata extraction, rule evaluation, destination proposal, conflict detection.
- Writes **confined to one operator-approved local control-data root**: manifests, plans, reports, queues, journals, checkpoints, and evidence artifacts.

> **The read-only guarantee is about NAS data paths, not about the machine.** A dry run that cannot persist local evidence cannot prove it ran. Earlier wording said "no write anywhere", which contradicted this gate's own entry criteria and the Definition of Done, and made the required evidence impossible to produce.

**Explicitly does NOT authorize:**
- any create, update, delete, rename, or **write-based probe** on **any NAS path**, source or destination;
- writing into destination trees;
- any write outside the approved control-data root;
- destination capability characterization, which requires a write and therefore remains at G5 (see PF-25 and OD-023).

**Entry criteria:**
1. G3 passed for all rungs required by the dry-run path, with fixture evidence.
2. Source roots are confirmed by the operator (OD-001, OD-013).
3. Rule set version is frozen and validates against the canonical schema.
4. **One control-data root is approved by the operator and proven disjoint** from every NAS mount, source root, destination root, and recursive scan boundary. Any overlap, or any uncertainty about overlap, is an immediate stop — not a warning.
5. Read-only credentials are issued and are distinct from any mutation-capable credential.
6. Adapter selection is resolved (OD-016) for the environment in use.
7. No open decision classified `blocks_gate: dry_run` remains unresolved.

**Required evidence:** fixture acceptance results; confirmed root list; frozen rule-set version and hash; control-data root declaration **with its disjointness proof**; a journal or evidence record of **every** local control-plane write.

**Approver:** Operator.

**Does not authorize G5.**

### G5 — Copied-Pilot Readiness (`pilot`)

**Authorizes:** Executing the pipeline against an **isolated copied corpus**. The pilot corpus is a copy; the authoritative source is never the pilot target.

**Explicitly does NOT authorize:** operating on authoritative live data; source retirement of any kind.

**Entry criteria:**
1. G4 passed and dry-run output reviewed.
2. Pilot dataset selected, isolated, and approved (OD-007).
3. Rollback steps written and checked.
4. Preservation-fidelity comparison reporting is implemented and passing on fixtures.
5. No open decision classified `blocks_gate: pilot` remains unresolved.

**Required evidence:** pilot dataset manifest; dry-run review record; rollback rehearsal record; preservation comparison report.

**Approver:** Operator.

**Does not authorize G6.**

### G6 — Limited-Live Readiness (`live`)

**Authorizes:** Bounded, approved **copy** operations against live shares, within an approved immutable plan.

**Explicitly does NOT authorize:** deleting or retiring any source; overwriting protected vaults; unbounded batch sizes.

**Entry criteria:**
1. G5 passed with copied-pilot evidence.
2. Recovery posture documented; snapshot/versioning readiness confirmed (OD-006).
3. Batch-size and stop thresholds approved (OD-008).
4. Copy-versus-move behavior frozen for the phase (OD-009).
5. Exact roots frozen.
6. No open decision classified `blocks_gate: live` remains unresolved.

**Required evidence:** pilot package; recovery/snapshot confirmation; approved thresholds; frozen root and behavior declaration.

**Approver:** Operator.

**Does not authorize G7.**

### G7 — Source-Retirement Readiness (`retirement`)

**Authorizes:** Retiring verified source items — moving them to a governed retained/quarantine state.

**Explicitly does NOT authorize:** permanent deletion. Permanent deletion is unavailable in V1 (`docs/05-governance/live-data-policy.md`).

**Entry criteria:**
1. G6 passed with verified copy evidence.
2. Hash verification passed for every candidate item.
3. Preservation-fidelity comparison passed for every candidate item; hash equality alone is not sufficient (see `docs/02-specification/preservation-model.md`).
4. Explicit per-batch operator approval, bound per `docs/02-specification/approval-binding-model.md`.
5. Quarantine retention policy resolved (OD-010).
6. No open decision classified `blocks_gate: retirement` remains unresolved.

**Required evidence:** verification report; preservation comparison report; bound approval record; reconciliation record.

**Approver:** Operator, per batch.

**Does not authorize G8.**

### G8 — Migration Completion (`migration_completion`)

**Authorizes:** Declaring migration complete and entering maintenance mode.

**Explicitly does NOT authorize:** unattended live watchers (FR-012 remains deferred); any new destructive class of operation.

**Entry criteria:**
1. G7 passed for all in-scope batches.
2. Every in-scope source item reaches a terminal disposition: organized, retained, quarantined, unresolved, or failed.
3. Reconciliation totals balance.
4. No open decision classified `blocks_gate: migration_completion` remains unresolved.

**Required evidence:** final reconciliation report; disposition totals; maintenance readiness record.

**Approver:** Operator.

## Relationship to the V1 operating gates

`docs/01-product/v1-scope.md` lists eight *operating* gates describing the runtime rollout. Those describe pipeline stages; the gates in this document describe **authorization**. They map as follows.

| V1 operating gate | Authorization gate that must already be passed |
| --- | --- |
| readiness | G3 |
| read-only inventory | G4 |
| dry run | G4 |
| fixture tests | G3 |
| copied pilot | G5 |
| limited live pilot | G6 |
| staged production | G6 |
| reconciliation and steady state | G8 |

Where the two lists appear to differ, this document governs authorization and `v1-scope.md` governs pipeline sequencing.

## `blocks_gate` classification

Every open decision, audit finding, and acceptance requirement carries two independent attributes:

- **Severity** — how bad it is if wrong (`BLOCKER`, `MAJOR`, `MINOR`).
- **`blocks_gate`** — the earliest gate it prevents (`foundation`, `build_ladder`, `implementation`, `dry_run`, `pilot`, `live`, `retirement`, `migration_completion`).

These are orthogonal. A BLOCKER-severity item that blocks only `live` does **not** block Foundation approval. A MINOR-severity item that creates a documentation contradiction may still block `foundation`.

An item blocks its named gate and every gate after it, unless resolved.

## Prohibitions that no gate lifts

The following hold at every gate in V1:

- Permanent deletion is unavailable.
- Copy before delete.
- Protected vaults are not overwritten by default.
- The frontend never authorizes filesystem mutation; it captures intent only.
- The Raspberry Pi Sentinel observes and alerts; it never classifies, approves, or mutates.
- AI output is evidence, never trusted truth.
- Near-duplicate similarity never implies deletion permission.

## Related documents

- `docs/04-acceptance/foundation-acceptance.md` — Foundation-stage (documentation) acceptance
- `docs/04-acceptance/v1-acceptance.md` — Implementation-stage (execution) acceptance
- `docs/05-governance/open-decisions.md` — open decisions with `blocks_gate`
- `docs/05-governance/definition-of-ready.md`
- `docs/05-governance/definition-of-done.md`
- `docs/audits/foundation-v1-audit.md`
