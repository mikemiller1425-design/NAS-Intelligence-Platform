# PKT-12 — Authority classes and command ingress (PF-20, PF-28)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-20 (MAJOR), PF-28 (MAJOR) |
| Highest severity | MAJOR |
| Change-control batch | BATCH-12 |
| Operator decision required | **OD-022** — the authentication factor only. The class vocabulary proceeds without it. |
| Blocked rungs | FBL-044, FBL-063 |
| Affected acceptance | **V1-ACC-038**, V1-ACC-052, SAF-009 |
| Depends on | Nothing structural. Must land **before** FBL-044 populates a principal registry. |

Both findings are about the same question asked at two layers: *who may authorize what* (PF-20) and
*through which door may an authorization arrive* (PF-28). Each alone leaves the other unanswered, and
both block the same two rungs.

## The exact contradiction

### PF-20 — five approval subject types have no authority class

`approval-binding-model.md:43–45` enumerates **eight** subject types as a YAML comment:
`OperationPlan | RuleSet | TaxonomyNode | ReviewException | PilotGate | LiveGate | RollbackAuthority |
RetirementAuthority`. `domain-model.md:846` names **five** in prose.

AUTHZ-17 requires "The approver holds the required authority class for this subject type" →
`APR-E18_APPROVER_NOT_AUTHORIZED`, "Halt run" (`approval-binding-model.md:138,220`).

`permission-model.md:61–74` lists fourteen classes covering **three** of the eight —
`OperationPlan→approve_plan`, `RuleSet→manage_rules`, `TaxonomyNode→manage_taxonomy`. **Unmapped:
`ReviewException`, `PilotGate`, `LiveGate`, `RollbackAuthority`, `RetirementAuthority`.**

The document also contradicts itself: its operator tier names eight authorities (`:13–22`) — "taxonomy
approval, sensitive identity policy, rule activation, plan approval, live pilot authorization,
exception handling, rollback authorization, cleanup policy" — which are **not** the class list and are
never mapped to it.

**Why this passed G1.** FND-ACC-003 cross-read at *command* granularity. `grant_approval` is one
command whose required authority varies by subject type, and that dimension was never read.

### PF-28 — `grant_approval` on a plan is permitted while `approve_operation_plan` is a safety event

`review-console-architecture.md:41` — the console **MAY** submit `grant_approval`, "Submit approval
**intent**." `:52` — the console **MUST NOT** submit `approve_operation_plan`. `:60` — "Attempting any
of these from the console is a rejected request and a **recorded safety event**, not a permission
error to be relaxed."

But `approval-binding-model.md:46` makes `subject_type: "OperationPlan"` a legal `grant_approval`
target. `command-model.md:71,99` lists both as peer top-level commands with no stated relationship,
and `domain-model.md:766,773` / `:910,917` give them two commands and two events for one act.

**Two further instances the finding does not name, and both are live:** `approve_rule_set` is
forbidden (`:57`) while `grant_approval` may target `subject_type: RuleSet`; and
`approve_taxonomy_node` (`command-model.md:64`) appears on **neither** list, while
`propose_taxonomy_node` is explicitly allowed.

## Operational consequence if left unresolved

**PF-20.** AUTHZ-17 is unevaluable for five of eight types, forcing a choice. **Hard-fail them** —
then `RollbackAuthority` can never be granted, FBL-062's rollback drill is impossible, and G5, G6, and
G7 are unreachable. **Fall through to any operator principal** — then AUTHZ-17 is a no-op for the five
highest-consequence types, including `RetirementAuthority`, which `approval-binding-model.md:256`
calls "the highest-consequence action in V1". **The check is missing precisely where it matters
most.**

**PF-28.** The safety-event trigger is undecidable, and V1-ACC-038 (BLOCKER) plus FBL-063's defining
negative test rest on a distinction with no criterion. Reading (a): console `grant_approval` on a plan
is legal → the forbidden entry is decorative, the console has a working plan-approval path under
another name, and **V1-ACC-038 passes vacuously**. Reading (b): it is forbidden → the console cannot
approve a plan at all, contradicting its stated purpose, and "The thirteen allowed commands succeed"
fails. **Both readings are supportable from the text**, which is the defect.

## Affected domain entities and fields

`Approval.subject_type` — the eight-value enum, promoted from a YAML comment to a normative table.
The principal registry entry `{principal_id, display_name, authority_classes}`
(`approval-binding-model.md:235`). Every command *type* gains an ingress class.

## Affected events, commands, reason codes, and persistence records

Five new authority classes. New reason code `CMD-E01_BACKEND_INTERNAL_COMMAND_SUBMITTED`, registered
in FBL-005's registry. IT-13 acquires a new trigger case (authority-class change).

## Proposed normative resolution

### PF-20 — a total subject-to-class map

Replace `permission-model.md:59–74` with a normative *Authority classes* section. **One required
class per subject, no default, no fall-through:**

| Subject type | Required authority class |
| --- | --- |
| `OperationPlan` | `approve_plan` |
| `RuleSet` | `manage_rules` |
| `TaxonomyNode` | `manage_taxonomy` |
| `ReviewException` | `approve_review_exception` *(new)* |
| `PilotGate` | `authorize_pilot_gate` *(new)* |
| `LiveGate` | `authorize_live_gate` *(new)* |
| `RollbackAuthority` | `authorize_rollback` *(new)* |
| `RetirementAuthority` | `authorize_retirement` *(new)* |

| ID | Invariant |
| --- | --- |
| AC-1 | The map is **total**. An approval whose `subject_type` is absent from it rejects `APR-E09_SUBJECT_MISMATCH` at AUTHZ-08, **before AUTHZ-17 is reached**. This is the fail-closed default. |
| AC-2 | Classes are **flat**. No class implies or contains another; `authorize_retirement`, `authorize_live_gate`, and `authorize_rollback` are never granted implicitly by holding `approve_plan` or `execute_plan`. |
| AC-3 | The Sentinel principal may hold only `read_health` and `read_reports`. A registry entry granting it any class beginning `approve_`/`authorize_`, or equal to `execute_plan`, `manage_journal`, or `propose_classification`, **fails registry load**. |
| AC-4 | Any change to a principal's classes is journalled and fires IT-13. |
| AC-5 | Classes are held in the registry only — never carried on a request, never derived from a payload, never inferred from a rule match, alert, status page, or queue position. |

> **AC-3 gives V1-ACC-052, SAF-009, and the ladder's "The Sentinel principal holds no approve or
> execute authority class" their first machine-checkable form** — proven by the registry rather than
> by the Sentinel's restraint.

Also convert `approval-binding-model.md:43–45` from a YAML comment to a normative enum table, and
correct `domain-model.md:846` from five to eight. Otherwise the lists drift again.

### PF-28 — ingress class, not subject type

**The resolving distinction is origin and authorship of the record, not subject type.**

**Class F1 — backend-internal transitions, with no external ingress at all:** not the console, not the
CLI, not the Sentinel, not a direct backend call. They are the effect the backend applies to a subject
*after* an approval has been minted, bound, and evaluated. Members: `approve_operation_plan`,
`lock_operation_plan`, `supersede_operation_plan`; `approve_rule_set`, `activate_rule_set`,
`disable_rule_set`; `approve_taxonomy_node`, `deprecate_taxonomy_node`, `retire_taxonomy_node`;
`approve_duplicate_group`; `consume_approval`; `append_journal_entry`, `seal_journal`,
`replay_journal`; `write_checkpoint`, `seal_checkpoint`, `invalidate_checkpoint`. A request naming one
of these — **from any origin, at any authentication level, holding any authority class** — is rejected
and recorded as a safety event.

**Class F2 — externally submittable but not by the console:** the execution, batch, and scan commands,
plus any command that copies, moves, renames, quarantines, retires, overwrites, or deletes a file.

**Restate the allowed row** (`review-console-architecture.md:41`): `grant_approval` submits intent for
a subject the backend has **already issued an `approval_request_id` for**. The payload carries the
request id, the echoed nonce, the echoed subject id and version, `displayed_binding_digest` as
evidence of what the operator saw, and the affirmation text — **no minted record, no scope, no
approver identity, no hash asserted as authoritative** (those reject `APR-E25`). Submission with no
open request rejects `APR-E02_APPROVAL_NOT_FOUND`. **`grant_approval` never transitions the subject**:
the backend applies the Class F1 transition itself once the approval is minted, bound, and evaluated.

**Add a normative command ingress class** to `command-model.md` after `:130`, on every command *type*:
`operator_submittable` (authenticated loopback surface), `sentinel_safe_request` (predefined safe
list), `backend_internal` (no external ingress; a request naming one is rejected and recorded as a
safety event regardless of origin, authentication, or authority class). **An unclassified command is
`backend_internal` by default.** Ingress class is a property of the command *type*, never of the
request, and is never read from a payload.

> **This strengthens ADR-014 rather than merely clarifying it.** Today ADR-014 constrains only the
> frontend. Under Class F1 the transition commands are unreachable from *any* client, so a compromised
> CLI or a forged direct request is refused by the same rule.

## Alternatives considered

**PF-20 — collapse the five onto `approve_plan`.** Rejected: a plan approval would then authorize
retirement and the live gate — the escalation ADR-003 exists to prevent — and `RetirementAuthority`'s
one-hour single-batch TTL becomes meaningless beside a four-hour live approval from the same class.

**PF-20 — one `authorize_gate` class for both gates.** Rejected: "No gate authorizes the next gate…
Absence of an authorization record is a prohibition, not a gap" (`gate-model.md:24`). A shared class
lets a G5 authorization satisfy the G6 check.

**PF-28 — remove `approve_operation_plan` from the forbidden list and rely on AUTHZ-16/17.** Rejected:
it deletes the safety-event trigger for the highest-consequence transition and leaves V1-ACC-038's
negative test unwritable, since no forbidden command would remain to attempt.

**PF-28 — make the distinction subject-type-based.** **Rejected decisively.** `subject type and id` is
a **client-supplied envelope field** (`command-model.md:119`). A distinction that depends on a
client-supplied value to decide whether a request is a safety event is the exact trust inversion
ADR-014 forbids — **the attacker chooses whether their request is auditable.**

## Safety implications

**PF-20 — ADR-003's approval boundary.** AC-1's totality is the fail-closed default. AC-2 forecloses
privilege escalation by containment — the mechanism by which "approve this plan" would quietly become
"retire these sources". AC-3 converts the most important negative claim about the Sentinel from prose
into a registry-load-time check.

**PF-28 — global invariant 21**, "Frontend state cannot authorize filesystem mutations", and ADR-014.
Class F1 **removes an ingress surface rather than guarding it**, which is strictly stronger than any
per-surface allowlist. The fail-closed default means the command registry cannot grow an unguarded
hole, and `CMD-E01` firing regardless of authentication closes the compromised-operator-session
residual risk ADR-014 leaves open today.

## Migration and compatibility implications

Additive: five classes, one ingress-class property, one reason code. **Sequencing is the compatibility
concern:** adding classes to a principal registry that already holds principals would require a
re-grant ceremony and fire IT-13 against every outstanding approval. This must land **before FBL-044
populates a registry.**

## Required tests

**Positive** — a principal holding `authorize_retirement` grants a `RetirementAuthority` approval; each
of the eight subject types resolves to exactly one class. All thirteen allowed console commands
succeed. `grant_approval` on an `OperationPlan` with an open request produces exactly one
`ApprovalGranted` **plus** one backend-emitted `OperationPlanApproved`, in that order.

**Negative** — `approve_plan` used to grant `RetirementAuthority` → `APR-E18` (AC-2); an unmapped
`subject_type: "Batch"` → `APR-E09` at AUTHZ-08, **before AUTHZ-17** (AC-1); a registry entry granting
the Sentinel `approve_plan` fails registry load (AC-3); `authority_classes` in a `grant_approval`
payload → `APR-E25` (AC-5); an authority-class change emits IT-13 and invalidates outstanding
approvals (AC-4). `approve_operation_plan`, `approve_rule_set`, **and `approve_taxonomy_node`** from
the console → rejected plus safety event — the third is the case PF-28 does not name;
`grant_approval` with no open request → `APR-E02`; `grant_approval` carrying `approval_scope` or
`approver` → `APR-E25` plus halt plus incident; a console-constructed approval refused; a UI-only
approval path mutates nothing (V1-ACC-038).

**Failure-injection** — **`approve_operation_plan` forged directly against the backend, bypassing the
console, from a fully authenticated loopback session holding `approve_plan`, must still be rejected
and recorded**, because Class F1 is origin-independent. This is the test proving the fix is stronger
than a UI allowlist. Also: a Sentinel-originated request for `PilotGate` → `APR-E20` at AUTHZ-19
**and** AC-3 at registry load, both must fire (defence in depth); a principal whose classes are
revoked between grant and execution → AUTHZ-17 fails at execution time, not only at grant time; a
class name differing only by Unicode normalization must not match; a duplicate `principal_id` fails
load; a newly added unclassified command type is rejected as `backend_internal` by default; a request
whose command type and payload imply different actions is judged on the command type only.

## Required documentation changes

`permission-model.md:59–74` (the authority-class section) and `:13–22` (the operator tier, mapped to
the class list); `approval-binding-model.md:43–45` (normative enum table);
`domain-model.md:846` (five → eight); `review-console-architecture.md:41,47–60`;
`command-model.md` after `:130` (ingress classes).

## Required ADR changes

**ADR-003** — append to Decision: "Every approval subject type maps to exactly one required authority
class, and the map is total: an approval whose subject type has no mapped class is rejected before the
authority check is reached. Classes are flat — no class implies another or grants a higher-consequence
authority by containment. Holding a class is necessary and never sufficient."

**ADR-017** — append to Consequences: "A change to a principal's authority classes is itself an
invalidation trigger, so authority cannot be widened underneath a standing approval."

**ADR-014** — append to Decision: "The trust boundary is a command **ingress class**, not a
per-surface allowlist. The transition commands are `backend_internal` with no external ingress from
any surface, authenticated or not, holding any authority class. `grant_approval` is the sole
approval-intent ingress and never itself transitions the subject. An unclassified command type is
`backend_internal` by default."

**ADR-015** — append to Consequences: "Intent and effect are two records with two events, separated by
an ingress class rather than a naming convention."

## Operator policy, or pure specification defect?

**PF-28 is a pure specification defect.** No operator policy content, and no open decision is
implicated by the ambiguity. OD-019 (console stack) blocks FBL-063 independently and is unrelated:
resolving PF-28 does not close OD-019, and closing OD-019 does not resolve PF-28.

**PF-20 is a specification defect for the vocabulary and the total map.** The single operator
question, unanswered: **how a principal proves it holds a class** — the authentication mechanism, the
factor presented at approval time, and verifier storage (**OD-022**).

> *This packet names the classes; OD-022 decides the factor.* **FBL-044 remains hard-blocked by OD-022
> regardless**, so this unblocks the vocabulary only, not the rung. FBL-044's prohibited work is
> explicit: "Choosing the authentication mechanism — OD-022 is the operator's." **Claude has not
> decided it.**

## Atomicity

The subject type of a `grant_approval` submission determines which class AUTHZ-17 demands. Resolving
PF-20 alone leaves the ingress question open, so the class check can be reached through a door that
should not exist; resolving PF-28 alone leaves five of eight subject types with no class to check.
Both block FBL-044 and FBL-063.

**Sequencing:** publish the ingress classification before FBL-063's allowlist-enforcement matrix is
built, since the matrix is generated from it; and publish the authority classes before FBL-044
populates a principal registry. **PKT-13 (PF-29)** couples in — the console renders
`approval_scope.mode` as part of the bound subject, and an unresolved mode vocabulary means the
`displayed_binding_digest` covers a value the operator could not have understood.

## Verification procedure

Re-run `foundation_self_review.py`. Independently: confirm `permission-model.md` maps all eight
subject types with no default clause; confirm the eight operator-tier authorities at `:13–22` are each
mapped to a named class; confirm every command in `command-model.md` carries an ingress class or is
covered by the `backend_internal` default clause.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for OD-022 — the
authentication factor only. **This packet is non-authoritative and confers no authority of its own.**
