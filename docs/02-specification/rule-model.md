# Rule Model

## Purpose

This document defines the exact V1 rule syntax and evaluation semantics for classification. Rules are configuration, not code. They are versioned, reviewed, and evaluated against evidence gathered from inventory and metadata extraction.

The system is dry-run by default. Provisional rules for dog, person/Voss identity, drone, CSV, and unresolved categories are intentionally preserved as provisional intent only.

## Design goals

- Deterministic when evidence is deterministic.
- Explicitly traceable to rule version and evidence.
- Safe under conflict, ambiguity, and partial metadata.
- Stable enough to support dry-run planning and manual review.
- Conservative with sensitive identity signals.

## Rule file format

The canonical file format is YAML.

### Top-level schema

```yaml
schema_version: 1
rule_set:
  id: rs-demo-001
  version: 1.0.0
  status: active
  owner: "operator"
  priority_order: deterministic_then_content_then_manual
  rules:
    - id: rule-id
      status: provisional
      priority: 100
      kind: deterministic
      when: {}
      then:
        destination: "Demo/Path/{capture_year}"
        review_state: review_required
      confidence:
        minimum: 0.95
      conflict:
        mode: manual_review
      evidence:
        required: [path, extension]
      confirmation:
        required: false
      tests:
        positive: []
        negative: []
        boundary: []
        conflict: []
        idempotency: []
```

### Required fields per rule

- `id`: stable unique rule identifier.
- `status`: one of `provisional`, `active`, `disabled`.
- `priority`: integer; higher numbers win within the same priority band.
- `kind`: one of `deterministic`, `content_inference`, `ai_assisted`, `manual_override`.
- `when`: condition object.
- `then.destination`: destination template or explicit manual-review bucket.
- `confidence.minimum`: minimum accepted confidence for live proposal.
- `conflict.mode`: `manual_review`, `skip`, `keep_first`, `version`, or `merge` depending on the rule’s intent.
- `evidence.required`: list of evidence types required to evaluate the rule.
- `confirmation.required`: boolean indicating whether explicit operator confirmation is required even if the rule matches.
- `tests`: references to fixture or synthetic test cases.

### Optional fields

- `description`
- `rationale`
- `owner`
- `tags`
- `applies_to`
- `fallback_destination`
- `source_refs`
- `retention_hint`
- `privacy_classification`

## Condition syntax

Rule conditions are a small declarative language represented as nested YAML values.

### Supported operators

- equality: `field: value`
- membership: `field: [a, b, c]`
- any-of: `field_any: [a, b]`
- all-of: `field_all: [a, b]`
- none-of: `field_none: [a, b]`
- prefix: `field_prefix: "text"`
- suffix: `field_suffix: ".ext"`
- regex: `field_regex: "^pattern$"`
- numeric comparison: `field_gte`, `field_gt`, `field_lte`, `field_lt`
- boolean: `field: true` or `false`
- existence: `field_present: true`
- structured predicates under `content`, `metadata`, `path`, `duplicate`, or `review`

### Example condition object

```yaml
when:
  all:
    - path_prefix: "source/photos/"
    - any:
        - extension: ".jpg"
        - extension: ".png"
    - metadata_present:
        - capture_date
  not:
    - duplicate_exact: true
```

## Evaluation semantics

### Input evidence

Rules evaluate only against validated inputs, which may include:

- normalized path and parent path
- file extension and MIME type
- content hash
- size and timestamp facts
- media metadata
- document metadata
- structured-data metadata
- AI suggestions, if enabled
- duplicate status
- manual review flags

AI-derived evidence is always marked as untrusted until validated by a deterministic or human-reviewed step.

### Decision process

1. Build the candidate evidence set for the file.
2. Evaluate all enabled rules whose `when` clauses are satisfied.
3. Partition matches by rule kind and priority band.
4. Apply conflict resolution order.
5. Require human review whenever confidence, policy, or identity rules demand it.
6. Emit a `ClassificationDecision` with the selected destination or manual-review outcome.

### Exact conflict resolution order

When more than one rule can apply, use the following order exactly:

1. Higher-priority deterministic rule.
2. Lower-priority deterministic rule.
3. High-confidence content inference.
4. Lower-confidence inference.
5. Manual review.

This order is final. It cannot be overridden by a low-confidence AI guess, a later loaded rule, or a dashboard action.

### Within-band tie breaking

If two rules remain tied within the same band:

1. Prefer the rule with the more specific condition set.
2. If specificity is equal, prefer the lower `id` in lexical order for determinism.
3. If still ambiguous, route to manual review.

### Confidence semantics

- Confidence is a bounded value in `[0.0, 1.0]`.
- A rule may require a higher confidence threshold than the system minimum.
- A rule match below threshold becomes a review candidate, not a live destination.
- Confidence never replaces missing evidence for deterministic rules.

### Review semantics

- If a rule sets `confirmation.required: true`, the outcome is always `review_required` unless and until an operator approves it.
- Sensitive identity intent is always provisional and review-gated.
- A manual override rule may exist only to encode operator judgment; it must not silently inherit automatic authority.

### Re-evaluation semantics

- Re-evaluating the same file against the same rule set version must be idempotent.
- A new rule set version may produce a different proposal, but it must not alter prior results in place.
- All re-evaluations must preserve historical evidence and prior decision records.

## Provisional intent handling

The following intents are preserved as provisional patterns only:

- `dog` or `Dogs`
- `person` or `Voss` identity intent
- `drone`
- `CSV`
- `unresolved`

### Policy for provisional intent

- Dog intent may influence a family-media taxonomy, but it is not a live classification guarantee.
- Person/Voss identity intent is sensitive and requires explicit operator confirmation.
- Drone intent may be inferred from source/device metadata, but not from vague content alone.
- CSV intent may rely on file extension and structured-data validation.
- Unresolved intent is a routing fallback, not a destination endorsement.

## YAML examples

### Example 1: deterministic dog-oriented media rule

```yaml
schema_version: 1
rule_set:
  id: rs-demo-001
  version: 1.0.0
  status: active
  rules:
    - id: media-dog-provisional
      status: provisional
      priority: 100
      kind: deterministic
      when:
        all:
          - media_kind: [image, video]
          - detected_object_any: [dog]
          - path_prefix: "fixture/incoming/family/"
      then:
        destination: "Demo/Family/Dogs/{capture_year}"
        review_state: review_required
      confidence:
        minimum: 0.90
      conflict:
        mode: manual_review
      evidence:
        required: [path, content_hash, media_metadata]
      confirmation:
        required: false
      tests:
        positive:
          - "fixtures/rules/media-dog/positive-001.jpg"
        negative:
          - "fixtures/rules/media-dog/negative-001.txt"
        boundary:
          - "fixtures/rules/media-dog/boundary-001.png"
        conflict:
          - "fixtures/rules/media-dog/conflict-001.jpg"
        idempotency:
          - "fixtures/rules/media-dog/idempotent-001.jpg"
```

### Example 2: sensitive identity intent requiring confirmation

```yaml
schema_version: 1
rule_set:
  id: rs-demo-001
  version: 1.0.0
  status: active
  rules:
    - id: person-voss-sensitive-provisional
      status: provisional
      priority: 95
      kind: content_inference
      when:
        all:
          - media_kind: [image]
          - person_count: 1
          - face_candidate_label: "Voss"
          - path_prefix: "fixture/review/"
      then:
        destination: "Demo/People/Voss/{capture_year}"
        review_state: review_required
      confidence:
        minimum: 0.98
      conflict:
        mode: manual_review
      evidence:
        required: [metadata, ai_suggestion, operator_confirmation]
      confirmation:
        required: true
      tests:
        positive:
          - "fixtures/rules/person-voss/positive-001.jpg"
        negative:
          - "fixtures/rules/person-voss/negative-001.jpg"
        boundary:
          - "fixtures/rules/person-voss/boundary-001.jpg"
        conflict:
          - "fixtures/rules/person-voss/conflict-001.jpg"
        idempotency:
          - "fixtures/rules/person-voss/idempotent-001.jpg"
```

### Example 3: CSV structured-data rule

```yaml
schema_version: 1
rule_set:
  id: rs-demo-001
  version: 1.0.0
  status: active
  rules:
    - id: data-csv-provisional
      status: provisional
      priority: 80
      kind: deterministic
      when:
        all:
          - extension: ".csv"
          - path_prefix: "fixture/data/"
      then:
        destination: "Demo/Data/CSV/{capture_year}"
        review_state: approved
      confidence:
        minimum: 0.85
      conflict:
        mode: version
      evidence:
        required: [extension, delimiter, row_count_sample]
      confirmation:
        required: false
      tests:
        positive:
          - "fixtures/rules/csv/positive-001.csv"
        negative:
          - "fixtures/rules/csv/negative-001.txt"
        boundary:
          - "fixtures/rules/csv/boundary-001.csv"
        conflict:
          - "fixtures/rules/csv/conflict-001.csv"
        idempotency:
          - "fixtures/rules/csv/idempotent-001.csv"
```

### Example 4: unresolved fallback

```yaml
schema_version: 1
rule_set:
  id: rs-demo-001
  version: 1.0.0
  status: active
  rules:
    - id: unresolved-fallback
      status: active
      priority: 0
      kind: manual_override
      when:
        any:
          - true
      then:
        destination: "Demo/Review/Unresolved"
        review_state: review_required
      confidence:
        minimum: 0.0
      conflict:
        mode: manual_review
      evidence:
        required: [path]
      confirmation:
        required: false
      tests:
        positive:
          - "fixtures/rules/unresolved/positive-001.bin"
        negative:
          - "fixtures/rules/unresolved/negative-001.bin"
        boundary:
          - "fixtures/rules/unresolved/boundary-001.bin"
        conflict:
          - "fixtures/rules/unresolved/conflict-001.bin"
        idempotency:
          - "fixtures/rules/unresolved/idempotent-001.bin"
```

## Conflict handling

When rules disagree:

1. Preserve all matched candidates.
2. Record the exact rule IDs and reasons for disagreement.
3. Apply the priority order documented above.
4. If a sensitive or contradictory path remains, route to review.
5. Never collapse a disagreement into a guessed destination.

## Versioning and change control

- Rules are versioned as part of a `RuleSet`.
- A new version requires explicit review and approval.
- Version history must remain queryable for audit and traceability.
- Reclassifying a previously decided file must preserve the original decision as a historical record.

## V1 limits

- No rule may authorize permanent deletion.
- No rule may bypass path validation.
- No rule may turn AI output into trusted truth without validation.
- No rule may elevate the Raspberry Pi sentinel into an approving authority.

