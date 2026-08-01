# Rule Model

## Purpose

This document defines the V1 rule semantics for classification. Rules are configuration, not code. They are versioned, reviewed, and evaluated against evidence gathered from inventory and metadata extraction.

## The canonical contract

> **`config/schemas/classification-rule-set.schema.json` is the single authoritative rule contract.**
>
> This document explains the semantics. The schema defines the structure. Where they appear to differ, the schema governs and this document is defective.

Audit finding **FND-B002** was raised because three incompatible rule vocabularies existed simultaneously: a nested shape in this document, a flat shape in the configuration example, and a third set of field names in the domain model. There is now exactly one file format. The domain model retains its own persistence field names, but it now states explicitly that they are an entity projection of this contract rather than a second wire format.

Retired field names — `enabled`, `applicable_file_types`, `metadata_conditions`, `visual_content_conditions`, `confidence_threshold`, `review_required` (as a rule-level field), `effective_date`, `provisional_sensitive`, `fallback_destination`, `priority_order` — are rejected by the schema as unknown fields. They must not reappear in any document or example.

Validate any rule set with:

```bash
python3 scripts/validate_rule_config.py
```

## Design goals

- Deterministic when evidence is deterministic.
- Explicitly traceable to rule version and evidence.
- Safe under conflict, ambiguity, and partial metadata.
- Structurally incapable of letting an unconfirmed rule act.
- Conservative with sensitive identity signals.

## File format

YAML, validated against the canonical JSON Schema. Two levels: a `rule_set` envelope and its `rules`.

### Rule-set envelope

| Field | Meaning |
| --- | --- |
| `schema_version` | Pinned to `1`. Any other value is rejected, never coerced. |
| `rule_set.id`, `name`, `version`, `owner` | Identity and ownership. `version` is semantic versioning and is distinct from `schema_version`. |
| `rule_set.status` | Rule-set lifecycle: `draft`, `reviewed`, `approved`, `active`, `disabled`, `superseded`, `retired`. |
| `rule_set.environment` | `fixture` or `pilot`. **`live` is deliberately absent from schema version 1**: a live rule set is not expressible without a new schema version and a separate governance decision. |
| `rule_set.destination_root_ref` | A **symbolic** root name. Literal or absolute filesystem paths are structurally rejected here, so no rule file can name a live share. |
| `rule_set.effective_from` | Date the set takes effect. |
| `rule_set.approval_state` | `none`, `requested`, `granted`, `revoked`. An `active` set must carry `granted`. |
| `rule_set.priority_scheme` | Pinned to `banded_v1`. |
| `rule_set.evaluation_order` | Pinned. Restated for readability; configuration cannot reorder pipeline stages. |
| `rule_set.conflict_resolution_order` | Pinned. Configuration cannot redefine conflict precedence. |
| `rule_set.defaults` | All pinned: conflict and low-confidence both resolve to manual review, explanations are required, dry-run only, and **`load_order_significance: none`**. |

### Rule fields

Required: `id`, `status`, `band`, `priority`, `kind`, `when`, `then`, `confidence`, `conflict`, `evidence`, `confirmation`, `tests`.

| Field | Meaning |
| --- | --- |
| `id` | Stable identifier. The numeric segment is an **ordinal for readability only** — it is not the priority and must not be read as one. |
| `status` | `proposed`, `provisional`, `active`, `disabled`, `retired`. This is the only activation switch; the retired `enabled` boolean is gone precisely because two switches for one concept guarantee drift. |
| `band` | `safety`, `deterministic`, `content_inference`, `ai_assisted`, `fallback`. |
| `priority` | Integer, constrained to its band's disjoint range, so a band can never be misread from a number. |
| `kind` | `deterministic`, `content_inference`, `ai_assisted`, `manual_override`. Cross-checked against `band`. |
| `applies_to` | Media kinds, extensions, and symbolic source-root references. |
| `privacy_classification` | `none`, `sensitive_identity`, `sensitive_content`. Orthogonal to `status`, so a rule can be both disabled and sensitive. |
| `policy_ref` | Open decisions blocking promotion. **Required for every provisional rule.** |
| `when` | Condition tree. |
| `then` | Outcome container. |
| `confidence.minimum` | Threshold in `[0.0, 1.0]`. A sub-threshold match is always a review candidate; `below_minimum_outcome` is pinned. |
| `conflict.mode` | `manual_review` or `skip`. Nothing else. |
| `collision` | Destination-path collision policy. Distinct from rule conflict. |
| `evidence.required` | Non-empty list of evidence types. |
| `confirmation.required` | Whether explicit operator confirmation is required even on a match. |
| `tests` | Positive, negative, boundary, conflict, and idempotency fixture references. All five are required, and all five must be non-empty for an `active` rule. |

## Condition grammar

A condition node carries **exactly one** combinator or leaf: `all`, `any`, `none`, `not`, `predicate`, or `always`.

A predicate is a closed object:

```yaml
predicate:
  field: extension          # closed vocabulary
  op: equals                # closed vocabulary
  value: ".csv"
  evidence_source: filesystem
```

The previous grammar used open-ended key names such as `path_prefix:` and `field_regex:`. That shape is **fundamentally incompatible with unknown-field rejection**: you cannot reject unknown fields while the field-name space is unbounded. The closed predicate form is what makes FND-B002's unknown-field requirement satisfiable.

`evidence_source` is required on every predicate. It records the provenance of the fact being tested, so an AI-derived signal can never masquerade as deterministic evidence.

`always: true` is legal **only** on a rule in the `fallback` band, and the loader permits exactly one such rule per set.

## Outcome semantics

`then` carries two independent safety levers:

| Field | Values | Meaning |
| --- | --- | --- |
| `outcome` | `propose_destination`, `route_to_review` | `route_to_review` can never become plan-eligible on its own. |
| `destination_authority` | `executable_candidate`, `advisory_only` | An `advisory_only` destination is recorded as evidence of intent and displayed in review, but can **never** be lifted into an operation-plan entry. |

`destination` is a template **relative** to `destination_root_ref`. Absolute paths, parent traversal, backslashes, and unapproved placeholders are structurally rejected.

`explanation_template` is required and non-trivial, because every proposal must be explainable.

Only a `safety`- or `deterministic`-band rule, in an approved rule set, with `status: active`, may ever be an `executable_candidate`.

## Provisional-rule restrictions

This is the structural resolution of audit finding **FND-B003**.

A rule with `status: provisional` is **structurally incapable** of an automatic or executable outcome. The schema requires all of:

- `then.outcome: route_to_review`
- `then.destination_authority: advisory_only`
- `then.review_state: review_required`
- `confirmation.required: true`
- `conflict.mode: manual_review`
- a non-empty `policy_ref` naming the open decision that blocks promotion

A configuration that sets a provisional rule to auto-approve, or to an executable destination, or that drops its confirmation requirement, **fails validation**. It is not a warning and not a lint; the file is rejected.

Two further structural locks apply regardless of status:

- A rule whose required evidence includes an AI suggestion can never yield an executable destination, and must require confirmation.
- A rule classified `sensitive_identity` can never carry `status: active`, must route to review, and must require confirmation.

**Promotion out of `provisional` is an operator decision**, recorded as a versioned rule-set change and reviewed under `prompts/rule-change-review.md`. Nothing in this document, and nothing a resolution engineer may do, promotes a rule. The Dogs, drone, CSV, and identity policies remain the operator's to decide (OD-012, OD-003).

## Evaluation semantics

### Input evidence

Rules evaluate only against validated inputs: normalized and raw paths, extension and MIME type, content hash and `content_identity_state`, size and timestamp facts, media and document metadata, structured-data metadata, duplicate status, manual review flags, and AI suggestions where enabled.

AI-derived evidence is always marked untrusted until validated by a deterministic or human-reviewed step. Only a `hashed_stable` content identity may serve as duplicate or verification evidence (see `file-identity-model.md`).

### Decision process

1. Build the candidate evidence set for the file.
2. Evaluate every rule whose `when` is satisfied and whose `status` is `active` or `provisional`.
3. Apply the resolution algorithm below.
4. Apply the outcome gate.
5. Emit a classification decision, or route to review.

## Conflict resolution

### Two different problems, two different mechanisms

Two mechanisms were previously conflated under the single word "conflict". They are now separate and may never substitute for one another.

- **Rule conflict** — two or more *rules* match the same file and disagree about its destination. Governed by `conflict.mode`. Legal values: `manual_review`, `skip`.
- **Destination collision** — a *single* agreed destination path is already occupied. Governed by `collision.policy`. Legal values: `route_to_review`, `skip`, `versioned_suffix`. Evaluated at plan time, never during rule evaluation.

### Removed conflict modes (FND-M005)

| Removed | Why |
| --- | --- |
| `keep_first` | Makes configuration file order and load order authoritative. Removed with no replacement. |
| `merge` | Fabricates a destination no rule authored, and implies content merging. Removed with no replacement. `conflict.merge_content` is pinned `false` as a machine-checkable prohibition marker. |
| `version` (bare) | Was imported from a *collision* sentence in the operations manual and mis-applied to *rule conflict*, where it means nothing. Destination versioning survives only as `collision.policy: versioned_suffix` with a fully specified template and maximum. |

### Priority bands

Every rule declares exactly one band. **A rule in a higher band always outranks a rule in a lower band, regardless of numeric priority.** Numeric priority is compared only within a band, and the schema constrains each band to a disjoint range.

| Rank | Band | Priority range | Permitted `kind` | Purpose |
| --- | --- | --- | --- | --- |
| 1 (highest) | `safety` | 900–1000 | `deterministic` | Unreadable or corrupt items, exclusions, protected-path stops. Safety always wins. |
| 2 | `deterministic` | 600–899 | `deterministic` | Extension, MIME type, source device, explicit path or filename. Verifiable facts. |
| 3 | `content_inference` | 300–599 | `content_inference` | Derived-from-content signals carrying a confidence value. |
| 4 | `ai_assisted` | 100–299 | `ai_assisted` | Untrusted model output. Can never be executable. |
| 5 (lowest) | `fallback` | 0–99 | `manual_override` | Terminal unresolved routing. |

Cross-band ties are impossible by construction.

### Resolution algorithm

Given the set of matching rules:

1. **Discard structurally ineligible matches.** A rule below its confidence minimum becomes a review candidate and leaves the destination contest. It is still recorded.
2. **Band filter.** Keep only the highest-ranked band present. Discarded rules remain recorded as candidates and are never deleted.
3. **Priority filter.** Within that band, keep only rules at the maximum priority. One survivor wins.
4. **Specificity tie-break.** If one rule has strictly maximal specificity, it wins.
5. **Lexical tie-break.** Sort remaining rule ids by Unicode code-point order and take the lowest. Deterministic and stable across machines and filesystems.
6. **Outcome gate.** The winner's outcome is emitted **only** if `then.outcome` is `propose_destination`, `then.destination_authority` is `executable_candidate`, `then.review_state` is `approved`, and `confirmation.required` is false. If any of these fail, the file routes to review with the winner recorded as the proposed candidate.
7. **Conflict record.** If more than one rule matched, write a conflict record listing every candidate with its band, priority, specificity score, confidence, and the numbered step at which it lost — whether or not a winner was found.

Steps 3–5 are pure functions of rule content. **At no point does the position of a rule within its file, the position of a file within a load set, or a rule set's timestamp participate in selection.**

### Specificity calculation

A single non-negative integer computed from the `when` tree. Higher is more specific.

Leaf score by operator:

| Operator | Score |
| --- | --- |
| `equals`, `not_equals` | 10 |
| `prefix`, `suffix` | 8 |
| `in`, `not_in`, `any_of`, `all_of`, `none_of` | `max(1, 10 − count(value))` |
| `gte`, `gt`, `lte`, `lt` | 5 |
| `regex` | 4 |
| `present`, `absent` | 2 |
| `always` | 0 |

Provenance multiplier applied to the leaf score:

| `evidence_source` | Multiplier |
| --- | --- |
| `filesystem`, `path`, `duplicate_index`, `operator` | ×3 |
| `media_metadata`, `document_metadata`, `structured_data` | ×2 |
| `ai_suggestion` | ×1 |

This makes a deterministic fact structurally more specific than a model guess of the same shape, even within a band.

Combinator aggregation:

- `all` → **sum** of child scores; each additional constraint narrows the match.
- `any` → **minimum** of child scores; a disjunction is only as specific as its weakest branch. This prevents authors from inflating specificity by adding alternatives.
- `none` → sum of child scores.
- `not` → the child's score.
- `always` → 0.

Bonuses applied once per rule: `+5` per key present in `applies_to`, and `+2` if `applies_to.media_kinds` is present and does not contain `any`.

Ties are expected; step 5 resolves them.

### Multi-destination behavior

If two or more surviving rules resolve to **different** destinations:

1. The file **never** receives a canonical destination automatically, regardless of band, priority, or specificity.
2. Steps 4 and 5 still run to produce a *recommended* candidate for the reviewer. The recommendation is advisory and is labelled as such.
3. A review item is opened with reason `multi_destination_conflict`, carrying every candidate destination and its evidence chain.
4. The decision state is `review_required`, never `approved`.
5. Every candidate destination is preserved. Losing candidates are never discarded.

If two or more rules resolve to the **same** destination, that is not a conflict but corroboration. The highest-band, highest-priority rule is recorded as deciding; the others are recorded as corroborating evidence, which raises reviewer confidence but changes no outcome.

### Explicit prohibitions

1. **No load-order winner.** File order, load sequence, and directory iteration order must not influence selection. An implementation whose output changes when the rules array is shuffled is non-conforming.
2. **No content merging.** Two matched destinations are never combined into a third, hyphenated, nested, or "both" path.
3. **No implicit versioning on rule conflict.** Disagreement between rules is never resolved by writing to two versioned destinations.
4. **No overwrite under any collision policy.** Under `versioned_suffix` the *new* copy receives the suffix; the pre-existing file is never renamed, moved, or replaced.
5. **No silent skip.** `conflict.mode: skip` means the rule withdraws from the contest, **not** that the file is dropped. If every matching rule skips, the fallback rule routes the file to review. Every file reaches a named disposition.
6. **No dashboard override** of band order.
7. **No AI winner.** An `ai_assisted` rule can never hold `executable_candidate`; the schema forbids it.

## Review semantics

When a file routes to review, the review item and the classification decision jointly carry:

- every candidate rule id with its band, priority, specificity score, and confidence;
- for each losing candidate, the numbered algorithm step at which it was eliminated;
- the rendered explanation of every candidate, not only the winner;
- the full evidence set with each item's provenance, AI-derived items flagged untrusted;
- every candidate destination, labelled `executable_candidate` or `advisory_only`;
- the open decisions blocking any provisional candidate.

An operator decision produces an approval bound to that specific file and rule-set version. It does not retroactively change the rule, does not promote the rule out of provisional, and does not apply to any other file.

## Re-evaluation semantics

- Re-evaluating the same file against the same rule-set version must be idempotent.
- A new rule-set version may produce a different proposal, but must not alter prior results in place.
- All re-evaluations preserve historical evidence and prior decision records.

## Provisional intent handling

The following intents are preserved as **provisional patterns only**, and are structurally advisory:

- dog / `Dogs`
- person identity
- drone
- CSV / structured data
- unresolved

Policy notes, none of which is an operator decision made here:

- Dog intent may influence a family-media taxonomy; it is not a live classification guarantee. The historical "Dogs wins over People" precedence is recorded as intent in the example's notes and is deliberately **not** encoded as an automatic override while OD-012 is open.
- Person identity is sensitive and requires explicit operator confirmation; the rule stays disabled pending OD-003.
- Drone intent may be inferred from source or device metadata, not from vague content alone.
- CSV intent may rely on extension plus structured-data validation.
- Unresolved intent is a routing fallback, not a destination endorsement.

## Loader checks beyond the schema

Some constraints cannot be expressed in JSON Schema and are enforced by the loader. Each has a stable identifier so failures are citable.

| Check | Rule |
| --- | --- |
| `VAL-RULE-DUPID` | Rule ids are unique within a set. |
| `VAL-RULE-DUPPRI` | No two rules share a band and priority slot. |
| `VAL-BAND-RANGE` | Priority lies inside its band's range. |
| `VAL-FALLBACK-ONE` | Exactly one rule matches unconditionally. |
| `VAL-ROOT-REF` | Symbolic root references resolve. |
| `VAL-TAXONOMY` | Destination first segments are known taxonomy nodes. |
| `VAL-FIXTURE-EXISTS` | Referenced fixture paths exist (from gate G3 onward). |
| `VAL-REGEX-LINEAR` | Regex values compile under a linear-time engine. |
| `VAL-POLICY-OPEN` | Every `policy_ref` names a still-open decision. |

## Examples

- **Positive:** `config/rules/classification-rules.example.yaml` — the canonical example, containing zero executable rules by design while OD-012 and OD-003 remain open.
- **Negative:** `tests/fixtures/rules/negative/` — 47 rule sets that must fail validation, each a single mutation of the positive example, with `expectations.yaml` naming the reason each must be rejected.

## V1 limits

- No rule may authorize permanent deletion.
- No rule may bypass path validation.
- No rule may turn AI output into trusted truth without validation.
- No rule may elevate the Raspberry Pi Sentinel into an approving authority.
- No rule set may declare a `live` environment under schema version 1.
