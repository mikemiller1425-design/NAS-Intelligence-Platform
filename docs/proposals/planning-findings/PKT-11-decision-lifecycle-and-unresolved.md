# PKT-11 — Classification decision lifecycle and the unresolved queue (PF-17, PF-18)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-17 (MINOR), PF-18 (MAJOR) |
| Highest severity | MAJOR |
| Change-control batch | BATCH-11 |
| Operator decision required | **OD-017** (report format), **OD-021** (tolerable unresolved count at G8). Neither blocks the structure. |
| Blocked rungs | FBL-037, FBL-038 |
| Affected acceptance | V1-ACC-025, **V1-ACC-041**, **V1-ACC-053**, FND-ACC-002 |
| Depends on | **PKT-09** — RI-2 references `TaxonomyNode.destination_authority` |

PF-17 is filed MINOR and PF-18 MAJOR, but they share one field (`review_reason`), one parity check
(FND-ACC-002), and one distinction that must be drawn in a single edit — **`rejected` is an operator's
refusal; `routed_unresolved` is a disposition.** Splitting them means running FND-ACC-002 twice and
risks the two terminal vocabularies being defined against each other.

## The exact contradiction

### PF-17 — the lifecycle misplaces `rejected`

`domain-model.md:511` states a **linear** chain: `proposed → review_required → approved → planned →
rejected`. But `reject_decision` is a **review-time** command (`domain-model.md:531`,
`command-model.md:52`), offered by the console on a classification decision, **pre-plan**
(`review-console-architecture.md:39`). Read literally, the chain requires planning before rejection —
which the file lifecycle forbids, since `operation_planned → approved` is a forbidden transition
(`lifecycle-model.md:104`).

The same document uses correct **branched** notation twelve pages later for `Approval`
(`domain-model.md:881–883`: "Plus: `granted` → `revoked`, `granted` → `expired`…"), so the notation
was available and simply not used here.

Two further defects: the decision state is `planned` (`:518`) while the file state is
`operation_planned` (`lifecycle-model.md:24`) with **no stated mapping**; and `rule-model.md:268`
requires that "A new rule-set version may produce a different proposal, but **must not alter prior
results in place**" — yet there is **no `superseded` state** (`domain-model.md:513–519`) and no
corresponding event, so the prior decision sits in `approved` forever, indistinguishable from the
current one.

### PF-18 — "unresolved" names four different things

- A **file** state — `lifecycle-model.md:30,50`; reachable from anywhere ("Any non-terminal state may
  transition to `unresolved`", `:98`).
- A **`ReviewItem`** state it is not — allowed states are `open`, `in_review`, `resolved`, `closed`
  (`domain-model.md:628–633`), **both terminals success-shaped**.
- A **report class** — required by `interface-model.md:39` and a Definition-of-Done artifact
  (`definition-of-done.md:42`).
- A **taxonomy destination branch** — `config/taxonomy/taxonomy.example.yaml:106–110`,
  `taxonomy-model.md:181–184`.

Four referents, one word. Supporting: `ClassificationDecision.review_reason` (`domain-model.md:500`)
and `ReviewItem.reason` (`:614`) are both **required fields with no value vocabulary anywhere** —
exactly one value is named in the entire corpus, `multi_destination_conflict`
(`rule-model.md:236`).

## Operational consequence if left unresolved

**PF-17.** An implementer generating a state machine from `:511` either refuses `reject_decision` on a
`review_required` decision — blocking the most common review-console action and failing FBL-038's
operator validation — or accepts it and emits `ClassificationDecisionRejected` for a transition no
document sanctions. Separately, re-evaluation under a new rule-set version cannot be non-destructive,
so **V1-ACC-025 cannot be evidenced without mutating prior decisions.**

**PF-18.** FBL-038's stop condition "Any file reaches no disposition" (`build-ladder.md:1178`) is
unprovable, because closing a review item does not record which disposition the file reached.
V1-ACC-041's evidence has **no defined source** — built from `review_items`, from
`file_records WHERE inventory_state='unresolved'`, or from a taxonomy-path scan, the three produce
**different totals**. So V1-ACC-053's "Reconciliation totals balance" cannot balance, and **G8 is
unreachable.**

The `ReviewItem`-based construction under-counts *by design*: a file can reach `unresolved` on a hard
policy stop with no review item ever opened (`lifecycle-model.md:98`). That is precisely the
population V1-ACC-041 exists to make visible.

## Affected domain entities and fields

`ClassificationDecision` — allowed states gain `superseded`; `review_reason` becomes conditionally
required. `ReviewItem` — four new fields, one new state. `FileRecord.inventory_state` — unchanged, but
becomes the authoritative source of the unresolved queue.

## Affected events, commands, reason codes, and persistence records

New events `ClassificationDecisionSuperseded` and `ReviewItemWithdrawn`, each added to **both**
`domain-model.md` and `event-model.md` in the same change — FND-ACC-002 enforces exact symmetric
difference, so a one-sided addition fails a BLOCKER Foundation row. A new fifth code family in
FBL-005's registry for the `review_reason` vocabulary.

## Proposed normative resolution

### PF-17 — branched lifecycle, plus supersession

Replace `domain-model.md:509–519`:

> `proposed` → `review_required` → `approved` → `planned`
>
> Plus: `proposed` → `approved` when the outcome gate passes with no review trigger; `proposed` →
> `rejected`; `review_required` → `rejected`; `approved` → `rejected` **while no `OperationPlan` entry
> references the decision**; and `proposed|review_required|approved|planned` → `superseded` when a new
> rule-set version produces a replacement decision for the same `file_record_id`.
>
> `planned` is terminal for the current version. **A planned decision is never rejected**: the plan is
> superseded and the decision transitions to `superseded`. `planned` corresponds to
> `FileRecord.inventory_state: operation_planned`; the two names denote one fact.

Allowed states: `proposed`, `review_required`, `approved`, `planned`, `rejected`, **`superseded`**.

Forbidden transitions, as a new subsection: `planned → rejected`; `planned → approved`;
`rejected → approved` without a new decision record; `superseded → *`; and **any transition on a
decision that an `Approval` has bound via a plan containing it** — the decision is immutable from the
moment `subject_content_hash` is computed over a plan referencing it.

New invariants: a decision is never edited in place across rule-set versions — re-evaluation emits a
new decision and supersedes the prior one, preserving its evidence and rendered explanation;
`review_reason` is required and non-null whenever `decision_state ∈ {review_required, rejected}`.

### PF-18 — the queue is a projection, not a review-item state

**The unresolved queue is a projection of `FileRecord.inventory_state`, not a `ReviewItem` state.**
That single sentence is the resolution; everything below implements it.

Extend `ReviewItem` required fields:

| Field | Type | Required | Nullable | Notes |
| --- | --- | --- | --- | --- |
| `reason` | enum | yes | no | The closed vocabulary below. |
| `candidate_chain` | array | conditional | no | Required when `subject_type` is `ClassificationDecision`. Every candidate rule id with band, priority, specificity score, confidence, rendered explanation, and the numbered elimination step. |
| `resolution_outcome` | enum | conditional | yes | Null while `open`/`in_review`. On `resolved`, exactly one of `classification_approved`, `classification_rejected`, `routed_unresolved`, `routed_quarantine`, `superseded`, `withdrawn`. |
| `resulting_file_state` | enum | conditional | yes | The `FileRecord.inventory_state` the resolution drove the subject to. Required and non-null whenever `resolution_outcome` is non-null. |

Lifecycle `open → in_review → resolved → closed`, plus `open → withdrawn` and `in_review → withdrawn`
when the subject is superseded before review concludes.

| ID | Invariant |
| --- | --- |
| RI-1 | No item reaches `closed` unless `resolution_outcome` **and** `resulting_file_state` are both non-null. This is the machine form of "Every file reaches a named disposition" (`rule-model.md:248`). |
| RI-2 | `routed_unresolved` requires `resulting_file_state: unresolved` **and** a `TaxonomyNode` whose `destination_authority ∈ {advisory_only, not_a_destination}`. An unresolved routing never targets an executable node. |
| RI-3 | Closing an item records the state the file reached; it never itself sets a file to a terminal success state. |
| RI-4 | An item never promotes a rule out of `provisional`, never mutates a rule, and never applies to a second file (`rule-model.md:263`). |

**Closed `review_reason` vocabulary**, a new subsection in `rule-model.md` after `:263`, shared by
`ReviewItem.reason` and `ClassificationDecision.review_reason`:
`multi_destination_conflict`, `below_confidence_minimum`, `confirmation_required`,
`provisional_rule_match`, `sensitive_identity_signal`, `sensitive_content_signal`,
`advisory_only_destination`, `ai_evidence_only`, `no_rule_matched`, `unreadable_or_corrupt`,
`destination_collision`, `duplicate_group_ambiguous`, `taxonomy_node_unapproved`,
`preservation_mismatch`, `policy_exception`. **An unregistered reason is rejected, not recorded.**

Replace `interface-model.md:39` with a normative definition: the unresolved queue is the set of
`FileRecord`s whose `inventory_state` is `unresolved`, joined to the `ReviewItem` whose
`resolution_outcome` was `routed_unresolved` **where one exists**, to the halt or stop record **where
the state was reached without a review item**, to the `review_reason`, to the taxonomy node routed to,
and to the blocking open decision where one applies. It is a **projection**: it holds no state, is
rebuildable from the journal, and authorizes nothing.

> **The "without a review item" clause is what makes the queue complete** against
> `lifecycle-model.md:98`. Omitting it reproduces the under-count that makes V1-ACC-041 unprovable.

## Alternatives considered

**PF-17 — add only `review_required → rejected` and keep the chain otherwise.** Rejected: it leaves
`planned → rejected` legal, permitting a rejected decision whose plan entry is already locked and
approved — against global invariant 7 — and leaves `rule-model.md:268` unsatisfiable.

**PF-17 — reuse `rejected` for supersession.** Rejected: `rejected` is an operator act with audit
meaning; supersession is a system consequence of a version bump with no operator involved. Collapsing
them makes it impossible to distinguish "the operator refused this destination" from "the rule set
changed."

**PF-18 — add `unresolved` as a `ReviewItem` state.** Rejected: a review item tracks *work*, a file
state records *disposition*. A file can reach `unresolved` with no item at all, so the queue would
systematically under-count exactly the items V1-ACC-041 exists to catch.

**PF-18 — make the queue a first-class entity.** Rejected: a second home for a fact the file record
already holds, against `state-and-persistence.md:68`, needing its own record type and rebuild path for
no gain.

## Safety implications

**PF-17 — global invariant 7**, "A plan is immutable after approval". The forbidden transition on
approval-bound decisions is load-bearing: without it, mutating a decision after plan approval changes
the recomputed `subject_content_hash` and surfaces as `APR-E11_PLAN_HASH_MISMATCH` — "Halt +
incident" — **caused by a legal-looking state change**. Making it forbidden converts a runtime
incident into a load-time rejection.

**PF-18** — RI-1 is the machine form of the no-silent-skip prohibition; without it that rule is
enforced by convention. RI-2 prevents an unresolved routing being retargeted at an executable
destination, which is the path by which an unclassifiable item could reach a real library folder.
Defining the queue as a rebuildable projection keeps it out of the authorization path, so no operator
action can be authorized by queue membership.

## Migration and compatibility implications

Additive: two states, two events, four `ReviewItem` fields, one reason vocabulary. No decisions or
review items exist. FND-ACC-002 must be re-run once — which is one of the reasons to land the two
findings together rather than separately.

## Required tests

**Positive** — `proposed → review_required → rejected` emits `ClassificationDecisionRejected`;
`proposed → approved` when the outcome gate passes; a rule-set version bump supersedes the prior
decision while its evidence and explanation remain readable. A multi-destination conflict opens with
`reason: multi_destination_conflict` and a full `candidate_chain`; resolving to unresolved sets
`routed_unresolved` plus `resulting_file_state: unresolved` and the file appears in the projection;
**a file driven to `unresolved` by a hard stop with no review item still appears.**

**Negative** — `planned → rejected` refused; `planned → approved` refused; `superseded → approved`
refused; `review_required` with `review_reason: null` refused; an event present in one model and
absent from the other fails FND-ACC-002. Closing with `resolution_outcome: null` (RI-1);
`routed_unresolved` with a different `resulting_file_state` (RI-2); `routed_unresolved` targeting an
`executable_candidate` node (RI-2); an item missing a losing candidate, its elimination step, or its
explanation; a resolution that mutates or promotes a rule, or applies to a second file (RI-4); an
unregistered `reason`.

**Failure-injection** — **mutate a decision that a bound approval's plan references: it must be
refused at the domain layer and never discovered only later as `APR-E11`.** Re-evaluate the same file
against the same rule-set version twice: the second run produces no new decision and no supersession
(V1-ACC-025). Concurrent `approve_decision` and `reject_decision` settle to exactly one terminal state
with the loser rejected. The projection rebuilt from the journal must equal the live projection
item-for-item. **Queue + organized + retained + quarantined + failed must equal the source inventory
count** (V1-ACC-053).

## Required documentation changes

`domain-model.md:509–519` (branched lifecycle, forbidden transitions), `:609–618` (`ReviewItem`
fields), `:628–633` (states), `:533–539` (events); `event-model.md:100–104`;
`rule-model.md` after `:263` (the reason vocabulary); `interface-model.md:39` (the projection
definition).

## Required ADR changes

**ADR-015** — append to Decision: "A classification decision is rejectable only while it is a
proposal. Once lifted into an operation plan the decision is immutable: the plan is superseded and a
new decision emitted. Rejection and supersession are distinct terminal states with distinct events,
because one records an operator's refusal and the other a rule-set version change." Append to
Consequences: "Every file reaches a named disposition recorded on the file record, and every review
item records which disposition its resolution produced. The unresolved queue is a projection over
those dispositions, never a separate authority — membership authorizes nothing and hides nothing."

**ADR-003** — **no change**, noted explicitly so that a review item does not acquire approval
semantics through this edit. `domain-model.md:655` is retained verbatim.

## Operator policy, or pure specification defect?

**Specification defect** for the entity fields, the states, the forbidden transitions, RI-1…RI-4, the
reason vocabulary, and the projection definition.

**Two operator questions, unanswered:** *how the queue is packaged* — **OD-017**, report format
defaults, which blocks FBL-038 independently; and *how many unresolved items are tolerable at G8 and
who owns them* — **OD-021**. **The projection makes the count visible; it does not set the threshold,
and Claude proposes no threshold.** Everything above proceeds without either.

## Atomicity

PF-17 and PF-18 share `review_reason`; the `rejected`-versus-`routed_unresolved` distinction must be
drawn once; and both add events, so FND-ACC-002 is re-run once rather than twice.

**PKT-09** — RI-2 references `TaxonomyNode.destination_authority`, which does not exist until the
taxonomy contract lands. **PKT-02** — the queue must be journal-rebuildable, and no review-item record
type is registered today. **PKT-08** — PF-06 is the same class of states-without-events defect against
the same parity check; adopting EP-1/EP-2 there covers the two events added here.

## Verification procedure

Re-run `foundation_self_review.py` check 22 (event-vocabulary symmetric difference) and confirm it is
still empty with the two new names present on both sides. Independently: confirm
`domain-model.md:511` no longer reads as a linear chain; confirm `interface-model.md:39` states the
queue holds no state.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for OD-017 and OD-021.
**This packet is non-authoritative and confers no authority of its own.**
