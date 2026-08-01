# Authorization Ledger

The authoritative record of gate authorizations for the NAS Intelligence Platform.

`docs/05-governance/gate-model.md` requires that each gate carry **its own explicit, dated, operator-signed authorization record naming the gate ID and the evidence reviewed**. This ledger is that record. It is append-only: entries are never edited to reflect a later state, and a superseded authorization is marked superseded rather than rewritten.

> **Absence of an entry in this ledger is a prohibition, not a gap.** A gate with no entry here is not authorized, regardless of how much evidence exists for it.

## Ledger

### G1 — Foundation Approval (`foundation`)

| Field | Value |
| --- | --- |
| Gate | **G1 — Foundation Approval** |
| Status | **GRANTED** |
| Approved commit | `54ec3a8ba12f6e4b8a2ba9d2af423f259e8e5051` |
| Authority | Human operator (final authority per `docs/00-intent/role-charter.md`) |
| Date | 2026-08-01 |
| Evidence reviewed | `docs/audits/foundation-v1-audit.md` (12 findings, all with recorded resolutions, none waived); `docs/audits/foundation-resolution-verification.md` (VER-B001 raised and corrected); `docs/04-acceptance/foundation-acceptance.md`; `docs/04-acceptance/safety-acceptance.md`; `docs/05-governance/open-decisions.md` (no decision carries `blocks_gate: foundation`) |

**Exact scope of what G1 authorizes**

G1 is a statement about **documents**. It records that the specification set is complete, internally consistent, testable, and safe enough to be planned against.

It authorizes:

- treating the specifications at `54ec3a8` as the frozen authority baseline;
- requesting a separate Build Ladder generation authorization.

**Exact scope of what G1 does NOT authorize**

- Generating the Build Ladder. That is G2 and required its own authorization, recorded separately below.
- Writing any implementation code.
- Installing production dependencies.
- Mounting, accessing, scanning, hashing, or analysing any NAS path.
- Copying, moving, renaming, quarantining, retiring, overwriting, or deleting any file.
- Generating live configuration.
- Resolving any operator policy decision (OD-001 … OD-022).
- Any dry-run, pilot, live, retirement, or completion activity.

**Foundation 1.0 approval is not implementation authorization.** These are different gates with different evidence and different records.

### G2 — Build Ladder Generation (`build_ladder`)

| Field | Value |
| --- | --- |
| Gate | **G2 — Build Ladder Generation** |
| Status | **GRANTED** |
| Granted at commit | `54ec3a8ba12f6e4b8a2ba9d2af423f259e8e5051` |
| Authority | Human operator |
| Date | 2026-08-01 |
| Basis | Separate and explicit. Granted alongside G1 but as a distinct authorization, not as a consequence of it. |
| Entry criteria | G1 granted (above); no open decision carries `blocks_gate: build_ladder` — the register shows zero; the required rung list and per-rung field set of `docs/handoffs/003-build-ladder.md` confirmed complete |

**Exact scope of what G2 authorizes**

- Producing the rung-by-rung Build Ladder as a **planning document**, at the path required by `docs/handoffs/003-build-ladder.md`.
- Producing supporting planning notes, handoff prompts, and planning-validation tooling.
- Freezing that ladder as planning-only.

**Exact scope of what G2 does NOT authorize**

- Implementing any rung. Each rung requires its own G3 authorization, and authorization of rung *N* never authorizes rung *N+1*.
- Installing production dependencies.
- Any NAS access of any kind.
- Any filesystem mutation outside the repository.
- Generating live configuration.
- Resolving operator policy decisions.

### G3 — Fixture-Only Implementation (`implementation`)

| Field | Value |
| --- | --- |
| Status | **NOT AUTHORIZED** |

No rung is authorized for implementation. G3 is granted per rung, never wholesale.

### G4 — Dry-Run Readiness (`dry_run`)

| Field | Value |
| --- | --- |
| Status | **NOT AUTHORIZED** |

G4 is the first gate at which the system touches the real NAS at all, and then only to read. Live NAS access remains prohibited.

### G5 — Copied-Pilot Readiness (`pilot`)

| Field | Value |
| --- | --- |
| Status | **NOT AUTHORIZED** |

### G6 — Limited-Live Readiness (`live`)

| Field | Value |
| --- | --- |
| Status | **NOT AUTHORIZED** |

### G7 — Source-Retirement Readiness (`retirement`)

| Field | Value |
| --- | --- |
| Status | **NOT AUTHORIZED** |

### G8 — Migration Completion (`migration_completion`)

| Field | Value |
| --- | --- |
| Status | **NOT AUTHORIZED** |

## Standing prohibitions

These hold regardless of any entry above, and no gate in V1 lifts them:

- Permanent deletion is unavailable.
- Copy before delete.
- Protected vaults are not overwritten by default.
- The frontend never authorizes filesystem mutation; it captures intent only.
- The Raspberry Pi Sentinel observes and alerts; it never classifies, approves, or mutates.
- AI output is evidence, never trusted truth.
- Near-duplicate similarity never implies deletion permission.

## How to add an entry

1. Name the gate ID and its canonical slug from `docs/05-governance/gate-model.md`.
2. Name the exact commit the authorization applies to.
3. Name the authority granting it and the date.
4. List the evidence actually reviewed, not the evidence that exists.
5. State the exact scope authorized and the exact scope excluded.
6. Confirm that no open decision carries a `blocks_gate` value at or before that gate.

An authorization that does not name a commit authorizes nothing, because the artifact it approved cannot be identified afterwards.
