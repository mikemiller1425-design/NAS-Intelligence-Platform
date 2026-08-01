# PKT-08 — The approval state machine has no event vocabulary (PF-06)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-06 (MAJOR) |
| Highest severity | MAJOR |
| Change-control batch | BATCH-08 |
| Operator decision required | **None.** |
| Blocked rungs | FBL-004 |
| Affected acceptance | V1-ACC-037, V1-ACC-039, V1-ACC-042, FND-ACC-002, SAF-009, PILOT-014 |
| Depends on | **PKT-02** — `ApprovalRequested` has no source record until PF-05's records exist |

## The exact contradiction

- **Nine states** — `domain-model.md:881–883`: `requested → granted → claimed → consumed`, plus
  `granted → revoked | expired | invalidated | superseded`, plus `claimed → released → granted`;
  enumerated at `:885–895`.
- **Six authoritative journal record types** — `durability-and-recovery-model.md:112`:
  `approval_granted`, `approval_consumption_claimed`, `approval_consumed`,
  `approval_consumption_released`, `approval_revoked`, `approval_invalidated`.
- **Four events** — `domain-model.md:916–919` and `event-model.md:131–134`: `ApprovalRequested`,
  `ApprovalGranted`, `ApprovalConsumed`, `ApprovalRevoked`.
- Events must derive from the journal — `durability-and-recovery-model.md:19`.

The gap runs in both directions. `approval_consumption_claimed`, `approval_consumption_released`, and
`approval_invalidated` have **no derived event**. `ApprovalRequested` has **no source record** (that
half is PF-05, in PKT-02). And `expired` and `superseded` are invalidation sub-cases —
`approval-binding-model.md:152` states every trigger "emits an `approval_invalidated` record", IT-10
is expiry — while **supersession has no IT code at all**, despite `:196` asserting the transition
(IT-01 covers the *subject* being superseded, not the approval).

**Why this passed G1.** FND-ACC-002 (`foundation-acceptance.md:23`) diffs `domain-model.md` against
`event-model.md` only. Both are consistently short, so the diff is empty. No acceptance row compares
the **record registry** to the event vocabulary. That is the structural lesson of this finding, and it
is why the resolution adds a rule rather than only three names.

## Operational consequence if left unresolved

FBL-004's negative test — "symmetric difference against `event-model.md` is empty" — **passes
today**. So an implementer ships an event stream that cannot express "approval claimed by run R" or
"approval invalidated because the rule set changed."

The review console (FBL-063) and Sentinel (FBL-064) observe only events. An operator watching a batch
sees `ApprovalGranted`, then silence until `ApprovalConsumed`. An approval invalidated mid-batch by
IT-03 halts the run with `APR-E05` and **no observable cause anywhere in the operator-facing
surface**. The four mandatory revocation checkpoints (`approval-binding-model.md:262–267`) fire into
silence.

V1-ACC-037 and V1-ACC-039 become satisfiable only by reading the journal directly — which the console
is architecturally forbidden from treating as an authorization source, and which operator tooling does
not do. Incident investigation has no timeline for the platform's most safety-relevant state machine.

## Affected domain entities and fields

`Approval` — no field changes; three new emitted events. The `invalidation_trigger` enum gains IT-17.

## Affected events, commands, reason codes, and persistence records

Three new events, added to `event-model.md:129–135` **and** `domain-model.md:916–919` simultaneously,
preserving the parity rule: `ApprovalConsumptionClaimed`, `ApprovalConsumptionReleased`,
`ApprovalInvalidated`. Seven names total, one emitter (`Approval`), one per record type. New reason
code `APR-E25_CLIENT_ASSERTED_AUTHORIZATION`. New invalidation trigger IT-17.

## Proposed normative resolution

### Three events, not five

Do **not** add `ApprovalExpired` and `ApprovalSuperseded`. `event-model.md:40` — "one event, one
name" — forbids two names for one journal fact, and expiry, supersession, and every other
invalidation are one record distinguished only by trigger code. Carry the discriminator in the
payload instead.

```
ApprovalInvalidated.payload := {
  approval_id             : string,    required, non-null
  invalidation_trigger    : enum "IT-01".."IT-17", required, non-null
  invalidated_at          : timestamp, required, non-null
  superseding_approval_id : ref,       NULLABLE — non-null IFF trigger == IT-17
  detail                  : string,    NULLABLE — redacted; no raw path bytes
}

ApprovalConsumptionClaimed.payload := {
  approval_id       : string,    required, non-null
  run_id            : string,    required, non-null
  claim_record_seq  : integer,   required, non-null, >= 0
  nonce_id          : string,    required, non-null   # the id only, NEVER the nonce
  subject_type      : enum,      required, non-null
  subject_id        : string,    required, non-null
  subject_version   : string,    required, non-null
  claimed_at        : timestamp, required, non-null
}

ApprovalConsumptionReleased.payload := {
  approval_id       : string,    required, non-null
  run_id            : string,    required, non-null
  claim_record_seq  : integer,   required, non-null, >= 0
  released_at       : timestamp, required, non-null
  release_reason    : enum { zero_intent_auto_release, operator_release }, required, non-null
}
```

### Add trigger IT-17

> **IT-17** — A later approval was granted for the same `(subject_type, subject_id)`; the earlier
> granted approval is auto-invalidated as superseded.

This closes the gap where `approval-binding-model.md:196` asserts a transition that no trigger code
expresses.

### Add the rule that closes the class

Into `event-model.md` after `:44`:

| ID | Rule |
| --- | --- |
| EP-1 | Every state-transition record type has exactly one derived event, **or** appears in an explicit `journal_only` register with a stated reason. Initial register membership: `op_temp_durable`, `segment_sealed`, `checkpoint`, `checkpoint_sealed`. |
| EP-2 | Every event has exactly one source record type. |
| EP-3 | Where one record type spans several domain states, the discriminator is a **required payload field**, never a second event name. |

### Commands

Add to `command-model.md`: claim, release, and invalidation are **backend-internal transitions, not
commands**. A surface submitting one is rejected with
`APR-E25_CLIENT_ASSERTED_AUTHORIZATION`.

## Alternatives considered

**Declare the transitions journal-only and publish only the register** — the ladder's second option.
Rejected as the whole answer, accepted as a complement: observability of authorization is a
safety-review requirement (V1-ACC-037, PILOT-014), so the transitions need events. But the register is
the mechanism that would have caught this at G1, so it is worth having regardless.

**Five events, one per missing state.** Rejected: it violates `event-model.md:40`, since expiry,
supersession, and other invalidations are one record distinguished only by trigger code. Five names
would make the event stream disagree with the journal about how many facts occurred.

## Safety implications

**Indirect but real.** Touches global invariant 8 (`domain-model.md:20`) and invariant 18 (`:30`,
failed operations remain inspectable), and SAF-009 — the Sentinel's authority boundary cannot be
audited if the approval state machine is unobservable.

It changes **no authorization decision**: events are authoritative for nothing
(`durability-and-recovery-model.md:19`). **State this explicitly in the change record**, so the fix is
not mistaken for a permission change during review.

## Migration and compatibility implications

Purely additive to the event vocabulary and the trigger enum. Events are authoritative for nothing, so
no chain, projection, or approval is affected. FND-ACC-002's symmetric-difference check must be re-run
against the updated pair, and EP-1/EP-2 add a *second* check that the current one does not perform.

## Required tests

**Positive** — `test_record_to_event_parity`: every record type maps to one event or to the
`journal_only` register. **This is the regression that would have caught the finding**, and it is the
single most valuable test in the packet. `test_event_to_record_parity`. `test_full_lifecycle_observable`:
request → grant → claim → consume emits four events in order with a matching `correlation_id`.
`test_invalidation_trigger_carried`: each of IT-01…IT-17 emits one `ApprovalInvalidated` with the
correct code — seventeen payloads, **one name**.

**Negative** — `ApprovalExpired` and `ApprovalSuperseded` are absent from the registry and rejected if
emitted. `claim_approval` / `release_approval` / `invalidate_approval` submitted from any surface is
rejected with `APR-E25` and journals a safety event. FND-ACC-002's symmetric-difference regression
against the **updated** pair. The claim payload carries `nonce_id` and **never the nonce**. `detail`
contains no raw path bytes (V1-ACC-042).

**Failure-injection** — drop 100% of events during a batch: authorization and the journal are
unchanged. Triple-deliver every event: consumer state is identical (`event-model.md:15`). Revoke at
operation 5 of 20: `ApprovalRevoked` is observable before the halt and correlatable to its reason code.

**Fixture coverage.** FBL-046's approval corpus (revocation before and mid-batch, consumed replay,
cross-run claim) supplies the revocation, command-rejection, and part of the lifecycle case. **No
fixture id is enumerated for the invalidation-trigger sweep** — FBL-045 must add one.

## Required documentation changes

`event-model.md:129–135` (three events) and after `:44` (EP-1, EP-2, EP-3 plus the `journal_only`
register); `domain-model.md:916–919` (the same three names, for parity);
`approval-binding-model.md` (IT-17); `command-model.md` (the backend-internal statement).

## Required ADR changes

**ADR-013** — append to Decision: "Every authoritative record type representing a state transition of
a domain entity has exactly one derived observability event, or is listed in an explicit journal-only
register with a stated reason. Where one record type spans several domain states, the discriminator is
a required payload field on the single event, never a second event name. Event parity is enforced in
both directions — domain-versus-event **and** record-registry-versus-event — because parity between
two consistently incomplete documents proves nothing."

**ADR-017** — append to Consequences: "The approval state machine is fully observable. Claim, release,
and invalidation are backend-internal transitions with derived events and no operator command."

## Operator policy, or pure specification defect?

**Pure specification defect. No operator decision is required, and Claude proposes none.**

## Atomicity

**PKT-02 is mandatory.** `ApprovalRequested` has no source record until PF-05's
`approval_request_issued` record exists, so publishing EP-2 first would make the specification fail its
own new rule on the day it is adopted.

**PKT-02 again, for PF-02.** Every record type PF-02's resolution adds inherits the
event-or-register obligation under EP-1. Resolving PF-02 first means reopening its output to classify
roughly twenty new types; resolving them together classifies each once.

**PKT-07** — CK-5 is an EP-1/EP-2 mapping for the two checkpoint events and should be drafted with
this parity rule rather than after it.

## Verification procedure

Re-run `foundation_self_review.py`. Independently: compute the symmetric difference between the record
registry at `durability-and-recovery-model.md:112` and the approval events in `event-model.md`, and
confirm it is empty modulo the `journal_only` register; confirm `event-model.md` contains exactly
seven approval event names; confirm `ApprovalExpired` and `ApprovalSuperseded` appear nowhere.

## Change-control authority

Change control per `docs/05-governance/change-control.md`. No operator decision is required.
**This packet is non-authoritative and confers no authority of its own.**
