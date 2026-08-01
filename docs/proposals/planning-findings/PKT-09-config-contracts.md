# PKT-09 — Root registry, taxonomy contract, and placeholder registry (PF-12, PF-15, PF-30)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-12 (BLOCKER), PF-15 (BLOCKER), PF-30 (MINOR) |
| Highest severity | BLOCKER |
| Change-control batch | BATCH-09 |
| Operator decision required | **OD-001/OD-013** (which real shares exist), **OD-002/OD-014/OD-015** (taxonomy content). All are *field values*; none is a schema decision. |
| Blocked rungs | FBL-021, FBL-022, FBL-023, FBL-034, FBL-035 |
| Affected acceptance | V1-ACC-025, FND-ACC-004, FND-ACC-010, FND-ACC-013 |
| Depends on | **PKT-01** (`taxonomy_hash` canonicalization), **PKT-03** (the shared `SourceRoot` edit) |

`config/schemas/` contains exactly one schema — the classification rule set. The rule contract was
made canonical during Foundation audit resolution; the root registry, the taxonomy, and the
placeholder vocabulary were not. **These three findings are one pattern, not three coincidences**, and
the shared remedy is that every config artifact has a schema and a negative-fixture set, as
`tests/fixtures/rules/negative/` already provides for rules.

## The exact contradiction

**PF-12 — a symbolic root registry is asserted but does not exist.**
`classification-rule-set.schema.json:30–34` defines `symbolicRootRef` as a "Symbolic root name
resolved from `config/examples/thresholds.example.yaml`. Literal filesystem paths are structurally
rejected here." That file (`:33–36`) is a three-key map of name → literal path, stamped
`status: non_production_example` (`:5`) — **no root ids, no authority tags, no vocabulary**.
`rule-model.md:299` states `VAL-ROOT-REF | Symbolic root references resolve` without defining
"resolve". The ladder requires roots carrying `confirmed_live` / `intended_structure` /
`unresolved_assumption` (`build-ladder.md:679`); the target file carries none. And `SourceRoot`
(`domain-model.md:57–67`) has no symbolic-name field, no `destination` member in `root_type`, and its
only path field is `synthetic_root_path` — which by its own name cannot hold the confirmed live root
G4 requires. **Compounding it:** `path-policy.md:19–30` Class B forbids a literal live path in
`config/` with **no exemption**, so no registry living in `config/` can ever name the root it must
resolve to. No document addresses that constraint.

**PF-15 — the taxonomy has no machine contract, and the example contradicts the model.** Four
incompatible shapes: `taxonomy-model.md:30–37` requires `slug, display_name, path_template,
parent_slug, authority, status, intended_use, notes`; `domain-model.md:663–672` requires `id, slug,
display_name, **parent_id**, path_template, authority, status, **retention_notes**`;
`config/taxonomy/taxonomy.example.yaml:8–115` supplies `shares`/`categories`/`unresolved_destinations`
with **no nodes, no authority, no status, no slug, no path_template**; and
`taxonomy-model.md:208–232`'s own example is a fifth shape. Five further defects, each verified:
that example uses `status: provisional` (`:222`) and `status: unresolved` (`:229`), neither in the
allowed enum (`domain-model.md:685–689`); the share table uses `intended + sensitive` (`:85–87`) as an
`authority` value absent from the authority enum (`:9–11`); the vault classification that Overlay F-1
(`preservation-model.md:126`) and `domain-model.md:23` require exists only as
`protected_from_overwrite` in a non-production example; three version formats coexist; and
`taxonomy-model.md` has **no subordination clause** answering `rule-model.md:9–11`.

**PF-30 — two placeholder vocabularies.** `taxonomy-model.md:42` lists five placeholders "**or
operator-approved equivalents**" — open. `classification-rule-set.schema.json:58` compiles six,
closed. `rule-model.md:103` calls unapproved placeholders structurally rejected without defining
"approved". Supporting: `predicateField` includes `capture_year` and `capture_date` but **not**
`capture_month`, so a rule may template on a value it cannot predicate on.

## Operational consequence if left unresolved

**PF-12.** FBL-021 cannot start; FBL-022, FBL-023, FBL-034, FBL-035 are transitively blocked. If
improvised, a file stamped `non_production_example` becomes the artifact deciding which roots are
writable — and with no `authority` field at load time, FBL-021's negative test
"`unresolved_assumption` used as an execution destination rejected" has no field to evaluate. IT-07
("Approved-root set changed") has no artifact whose change is observable.

**PF-15.** FBL-034 cannot start, and since it precedes the rule loader by design, FBL-035 is blocked.
**`taxonomy_hash` has no preimage**, so AUTHZ-13 can never pass deterministically and IT-04 can
observe nothing. OD-002 is unclosable in practice: there is no artifact shape for the operator to
freeze.

**PF-30.** Minor alone; load-bearing the moment PF-15 lands. The taxonomy owns `path_template` and
rules own `then.destination` — two placeholder-bearing template systems, only one schema-governed. A
taxonomy authored against "operator-approved equivalents" produces `path_template` values
`VAL-TAXONOMY` can never match, because the rule side structurally cannot express the placeholder.

## Affected domain entities and fields

`SourceRoot` — `root_ref`, `binding_mode`, `path_binding_key`, `authority_evidence_ref`, and
`destination` added to `root_type`. **`synthetic_root_path` is deliberately not renamed**: a rename
breaks FND-ACC-004 and the traceability matrix. `TaxonomyNode` — the full field set below.

## Affected events, commands, reason codes, and persistence records

New reason codes: `VAL-ROOT-REF-UNKNOWN`, `-DISABLED`, `-AUTHORITY`, `-TYPE`, `-LITERAL`;
`VAL-TX-DUPSLUG`, `-DUPID`, `-PARENT`, `-ACYCLIC`, `-PATHPREFIX`, `-SEGMENT`, `-ROOTREF`,
`-PLACEHOLDER`, `-RETIRE`, `-SUPERSEDE`, `-VAULT`; `VAL-TAXONOMY-UNKNOWN-ROOT-SEGMENT`,
`-NO-MATCHING-NODE`, `-NOT-A-DESTINATION`, `-AUTHORITY-ESCALATION`. All registered in FBL-005's
registry.

## Proposed normative resolution

### PF-12 — a root registry, with Class B enforced structurally

This packet proposes a new canonical contract, `config/schemas/root-registry.schema.json`, together
with a proposed fixture instance `config/roots/roots.example.yaml`. Neither exists today.

Per root: `root_ref` (string, `^[a-z][a-z0-9_]{2,63}$`, required — **identical pattern to
`symbolicRootRef`**); `label`; `root_type` (`source|destination|incoming|organized|review|quarantine|
pilot|archive|control`); `authority` (`confirmed_live|intended_structure|unresolved_assumption`);
`binding_mode` (`synthetic_literal|operator_binding_ref`); `synthetic_root_path` (present **iff**
`synthetic_literal`, `not: "\\.\\."`); `path_binding_key` (`^[A-Z][A-Z0-9_]{2,63}$`, present **iff**
`operator_binding_ref`); `enabled`; `read_only_expected`; `scan_scope` (`recursive|top_level|none`);
`status` (`proposed|confirmed|active|retired`); `authority_evidence_ref` (required iff
`confirmed_live`); `adapter_descriptor_id` (optional); `policy_ref` (optional).

| ID | Invariant |
| --- | --- |
| RR-1 | `confirmed_live` ⇒ `binding_mode: operator_binding_ref`, `path_binding_key` and `authority_evidence_ref` required, **`synthetic_root_path` forbidden**. This is path-policy Class B enforced structurally — the registry is designed so a live path *cannot* be written into it, and the real value arrives from outside the repository via `path_binding_key`. |
| RR-2 | `synthetic_literal` ⇒ `synthetic_root_path` required, `path_binding_key` forbidden. |
| RR-3 | `unresolved_assumption` ⇒ `status ∈ {proposed, retired}`, `enabled: false`, `policy_ref` required. Machine-unusable rather than merely discouraged. |
| RR-4 | `root_type: source` ⇒ `read_only_expected: true`. |
| RR-5 | `root_type: control` ⇒ `scan_scope: none` (machine form of `domain-model.md:88`). |

Root refs compare as raw ASCII byte sequences after the pattern check — no case folding, no Unicode
normalization, since the pattern already excludes non-ASCII.

### PF-15 — a taxonomy contract

This packet proposes a new canonical contract, `config/schemas/taxonomy.schema.json`, which does not
exist today.

*Node*, all required unless noted: `id` (`^txn-[a-z0-9][a-z0-9-]{2,62}$`); `slug`; `display_name`;
`parent_slug` (slug **or null** — null means top-level; the literal `"root"` used at
`taxonomy-model.md:213` is corrected away); `path_segment` (single component, no `/`);
`path_template` (**byte-identical pattern to `destinationTemplate`**, relative, `not: "\\.\\."`);
`authority`; `status` (`proposed|approved|active|deprecated|retired` — the domain enum governs, which
removes `provisional` and `unresolved`); `destination_authority` (`executable_candidate|advisory_only|
not_a_destination`); `sensitivity` (`none|sensitive_content|sensitive_identity`); `vault_class`
(`none|protected_vault`); `overwrite_policy` (`const: "never"`); `intended_use`; `retention_notes`.

*Envelope*: `id`, `name`, `version` (**semver — this is what `Approval.taxonomy_version` binds
exactly**), `status`, `environment` (`fixture|pilot`), `destination_root_ref`, `owner`,
`effective_from`, `approval_state`, `nodes`, `version_history`.

| ID | Invariant |
| --- | --- |
| TX-1 | `unresolved_assumption` ⇒ `status ∈ {proposed, deprecated, retired}`, `destination_authority ∈ {advisory_only, not_a_destination}`, `policy_ref` required. |
| TX-2 | `executable_candidate` ⇒ `authority ∈ {confirmed_live, intended_structure}` ∧ `status: active`. |
| TX-3 | `sensitive_identity` ⇒ `advisory_only`, `status ≠ active`, `policy_ref` required. |
| TX-4 | `status: retired` ⇒ `retired_at` required ∧ `not_a_destination`. |
| TX-5 | Envelope `status: active` ⇒ `approval_state: granted`. |
| TX-6 | `approval_state ∈ {none, requested, revoked}` ⇒ no node is `executable_candidate`. |

`VAL-TAXONOMY` restated: a rule's destination first segment equals some null-parent node's
`path_segment`; the full destination equals or is prefixed by some node's `path_template` whose
`destination_authority ≠ not_a_destination`; **and if the matched node is `advisory_only`, the rule's
`then.destination_authority` must also be `advisory_only`** — this closes the last route by which a
validated rule set could name an unapproved destination as executable.

Canonicalization for `taxonomy_hash`: digest over the envelope with `nodes` sorted by `slug` in
Unicode code-point order, keys sorted, no insignificant whitespace, NFC-normalized strings. This must
be specified in the same change or PKT-01's defect is compounded rather than resolved.

**Mechanical reconciliation of the shipped example** — no operator content decided:
`root: "/fixtures/destination/"` → `destination_root_ref: fixture_destination_root`; `shares[].id` →
`slug`; `shares[].path` → `path_segment` **and** top-level `path_template` (these are the values
`VAL-TAXONOMY` matches); `sensitive: true` → `sensitivity: sensitive_content`;
`protected_from_overwrite: true` → **`vault_class: protected_vault`, the field ADR-011 and Overlay
F-1 needed**; `purpose` → `intended_use`; `categories.dogs.canonical` → a child node `advisory_only`
with `policy_ref: ["OD-012"]`; `unresolved_destinations[]` → four nodes
`intended_structure`/`proposed`/**`advisory_only`** — *not* `not_a_destination`, because the shipped
fallback rule routes there (`classification-rules.example.yaml:372`) and must keep validating;
`aliases` dropped (alias resolution is OD-015). **Every destination in the shipped rule file resolves
with no edit to that file.**

### PF-30 — one shared placeholder registry

A shared registry, proposed at `config/schemas/destination-placeholder-registry.json`, `$ref`'d by
both the rule schema's `destinationTemplate` and the new taxonomy schema's `pathTemplate`, so the
pattern **cannot drift between contracts**.

| Placeholder | Resolution | Absent-value behaviour |
| --- | --- | --- |
| `{capture_year}` | `YYYY` from the capture timestamp | route to review; **never** substitute a filesystem mtime |
| `{capture_month}` | `MM`, zero-padded | route to review |
| `{capture_date}` | `YYYY-MM-DD` | route to review |
| `{source_root}` | the `root_ref` of the resolved `SourceRoot` — **never a filesystem path** | fail; an unresolvable root is `VAL-ROOT-REF` |
| `{media_kind}` | a member of the `applies_to.media_kinds` enum | `unknown` |
| `{document_kind}` | closed enum, enumerated at FBL-032 | `unknown` |

| ID | Rule |
| --- | --- |
| PH-1 | The registry is **closed**. "Operator-approved equivalents" is not an extension mechanism; adding a placeholder is a schema version change under change control. |
| PH-2 | A placeholder resolving to an empty string, `null`, or a value containing `/`, `\`, `..`, or any path separator is a **hard failure**, never a silent substitution. This is a path-escape control, not a formatting nicety. |
| PH-3 | `{source_root}` resolves to a symbolic `root_ref`, never a filesystem path. Expanding it to a literal would place a live path into a plan artifact, which path-policy Class B forbids for generated artifacts **without exemption**. |
| PH-4 | Every registry member that can be tested appears in `predicateField`; `capture_month` is added for symmetry. |
| PH-5 | The registry is shared verbatim by both contracts; divergence between the two compiled patterns is a repository-consistency failure checked at Foundation acceptance. |

Placeholder names compare as exact ASCII byte sequences — no case or Unicode folding — so
`{Capture_Year}` is rejected rather than normalized.

**And insert after `taxonomy-model.md:5`** the subordination clause the rule model already has: the
taxonomy schema is the single authoritative contract; where document and schema differ, the schema
governs and the document is defective. **That one insertion is what PF-15 and PF-30 both actually
need**, and its absence is why `taxonomy-model.md:42` is currently governed by nothing.

## Alternatives considered

**PF-12 — extend `thresholds.example.yaml`'s `paths:` map.** Rejected: it promotes a declared
non-production example into the authorization artifact, and has no slot for `authority` or
`binding_mode` without becoming a registry inside a tuning file.

**PF-12 — derive roots from the taxonomy.** Rejected: source roots have no taxonomy node, and it makes
`VAL-ROOT-REF` and `VAL-TAXONOMY` mutually circular.

**PF-15 — write a schema for the existing `shares`/`categories` shape.** Rejected: no parent relation,
so `VAL-TX-PATHPREFIX` and the tree invariant are inexpressible; and no `status`, so IT-04 observes
nothing.

**PF-15 — make the domain entity canonical with no config schema.** Rejected: FND-ACC-010's standard
for rules is a machine-readable contract with fixtures. Prose gives FBL-034's loader nothing to
validate and `taxonomy_hash` nothing to digest.

**PF-30 — allow an operator-declared extension list in config.** Rejected: an unbounded name space
cannot be closed against unknown values, and a placeholder is a substitution *into a path* — the one
place where an unbounded vocabulary is a path-escape surface.

## Safety implications

**Global invariant 20** — "Paths cannot escape approved roots" (`domain-model.md:32`). RR-1 is the
structural enforcement of Class B for the one config file that would otherwise need a live path; PH-2
is the control that prevents `30_DRONE/{capture_year}/{capture_date}` with absent metadata silently
collapsing to `30_DRONE`, **quietly relocating files one directory up — possibly inside a protected
vault**. **Global invariant 11** — protected vaults get their first machine-checkable form via
`vault_class`. TX-3 extends the rule contract's sensitive-identity lock to the destination side.

## Migration and compatibility implications

`domain-model.md`'s `SourceRoot` edit is **additive**, and `synthetic_root_path` is not renamed.
`classification-rules.example.yaml` uses only `{capture_year}` and `{capture_date}` — **no change
required**, and all 47 negative fixtures are unchanged. Refactoring the rule schema's inline pattern
into a `$ref` is a structural edit with **no semantic change** — the accepted string set is
byte-identical — but it is still a change to frozen Foundation content, requiring re-validation of all
48 files to prove the accepted set did not move.

## Required tests

**Positive** — `fixture_source_root` resolves with its authority tag; `fixture_destination_root`
resolves for `destination_root_ref`; the reconciled taxonomy example loads and
`02_FAMILY_VAULT/Dogs/{capture_year}` resolves; a decision made under taxonomy `1.0.0` stays
interpretable under `1.1.0`; the same template string validates identically against both schemas
(PH-5).

**Negative** — `tests/fixtures/rules/negative/literal-destination-root.yaml:12` now rejects as
`VAL-ROOT-REF-LITERAL` rather than by pattern alone; `confirmed_live` carrying `synthetic_root_path`
(RR-1); `control` with `scan_scope: recursive` (RR-5); `unresolved_assumption` + `executable_candidate`
(TX-1); `sensitive_identity` + `executable_candidate` (TX-3); a node deleted without retirement
(`VAL-TX-RETIRE`); a non-prefixed child (`VAL-TX-PATHPREFIX`); **`status: provisional` — the value
`taxonomy-model.md:222` currently uses — rejected by the enum**; `parent_slug: "root"`;
`vault_class: none` under a protected ancestor; an unapproved envelope containing an executable node
(TX-6); `{operator_home}` in a `path_template`; an "operator-approved equivalent" rejected regardless
of any config declaring it (PH-1); `{Capture_Year}` rejected rather than folded.

**Failure-injection** — a registry load refused if `check_path_policy.py` would flag any field; a
`path_binding_key` naming a binding that overlaps the control-data root is an immediate stop; **a ref
that is simultaneously a valid ref and a valid relative path (`data_vault`) must resolve as a ref,
never be joined as a path**; a reordered node array must produce a byte-identical `taxonomy_hash`; two
nodes with identical `path_template` under different slugs flagged as an ambiguous `VAL-TAXONOMY`
match; `{capture_year}` resolving to empty → hard failure, not empty substitution (PH-2);
`{capture_date}` whose metadata value is `../../..` must fail PH-2 **before any path join occurs**;
the two compiled placeholder patterns proven byte-identical in CI (PH-5).

## Required documentation changes

`domain-model.md:57–67` (`SourceRoot`, additive); `taxonomy-model.md:5` (subordination clause),
`:39–44` (template rules), `:208–232` (the example, corrected to the schema);
`rule-model.md:299–300` (restated `VAL-ROOT-REF` and `VAL-TAXONOMY`), `:103`, `:42`.

## Required ADR changes

**ADR-006** — append to Decision: "The rule contract and the taxonomy are each published as a
canonical machine-readable schema under `config/schemas/`, with each explanatory document subordinate
to its schema; an explanation terminating in an unversioned path string is not an explanation."
Append to Consequences: "Destination templates draw from one closed, shared placeholder registry used
identically by the rule contract and the taxonomy contract; an unresolvable placeholder is a hard
failure, never an empty substitution, because a silently collapsed path segment relocates a file with
no record that it happened."

**ADR-011** — append to Consequences: "Protected-vault status is the declared, inherited field
`vault_class: protected_vault`, read by Overlay F-1 and the collision policy, never inferred from a
folder name."

**ADR-012** — append to Decision: "Adapters accept a resolved root handle carrying `authority`,
`root_type`, and `read_only_expected` — never a path string from a rule set, taxonomy, plan, or
client. An adapter presented with an unresolved path refuses the call."

**ADR-001** — append to Consequences: "A root's `authority` is inventory evidence, not
configuration."

## Operator policy, or pure specification defect?

**Specification defect for every structural element** — the two schemas, the shared registry, the
enums, `binding_mode`, the resolution algorithm, RR-1…RR-5, TX-1…TX-6, PH-1…PH-5, the eleven
`VAL-TX-*` codes, the `VAL-TAXONOMY` restatement, the version-format pin, the subordination clause,
and the mechanical reconciliation. **Every value the operator owns is a field value, never a schema
decision.**

**The operator questions, unanswered here:**

- *Which real shares exist, are in scope, and carry which authority* — **OD-001**, **OD-013**. The
  registry is deliberately designed so those values arrive from outside the repository via
  `path_binding_key`, which is why the schema can be written before the answer exists.
- *What the taxonomy contains and where its boundaries fall* — **OD-002**, with **OD-014**
  (control-directory names) and **OD-015** (edges and aliases). FBL-034's prohibited work is explicit:
  "Freezing operator taxonomy content."
- Whether `02_FAMILY_VAULT/Dogs` ever becomes `executable_candidate` is **OD-012**'s outcome.

**Claude has not decided any of these and proposes no value for any of them.**

One correction worth stating plainly: `taxonomy-model.md:42`'s "or operator-approved equivalents"
**misrepresents a structural contract question as an operator decision.** Removing that clause
*returns* a specification question to the specification; it takes nothing from the operator.

## Atomicity

All three must land together. PF-30's registry must be `$ref`'d by PF-15's taxonomy schema **at the
moment that schema is authored** — publishing it with an independently written pattern would encode
the five-versus-six split in **two machine contracts instead of one prose sentence**, which is
strictly worse than the present state. PF-12's root registry is what `{source_root}` resolves through
(PH-3) and what `VAL-TX-ROOTREF` resolves against.

**PKT-03 is a prerequisite** for the `SourceRoot` edit — PF-11 and PF-12 modify the same entity, and
two separate edits break FND-ACC-004 twice. **PKT-01** is a prerequisite for `taxonomy_hash`.
**PKT-10** (PF-16) couples in: taxonomy nodes acquire `policy_ref` and inherit the decision-closure
trap. **PKT-13** (PF-29) supplies the envelope `environment` semantics.

## Verification procedure

Re-run `validate_rule_config.py` (all 48 rule files must still validate byte-for-byte),
`foundation_self_review.py`, and `check_path_policy.py`. Independently: confirm
`config/schemas/` now holds four schemas; diff the two compiled placeholder patterns and confirm they
are byte-identical; confirm every destination in `classification-rules.example.yaml` resolves against
the reconciled taxonomy with no edit to the rule file.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for OD-001, OD-002,
OD-012, OD-013, OD-014, and OD-015 — **for their field values only**.
**This packet is non-authoritative and confers no authority of its own.**
