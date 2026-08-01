# Foundation V1 Audit

## Provenance of this document

An independent audit was performed against commit `840d72c8339dbc3c2a7ec76393745243df8dcaa4`.

At the time audit resolution began, this file in the repository contained only the placeholder line "Placeholder awaiting independent foundation audit findings." The audit findings had been delivered to the resolution engineer out-of-band rather than committed. This document therefore **reconstructs the independent audit register** — preserving the original finding IDs, severities, problems, and required outcomes exactly as issued — and then appends resolution data beneath each finding.

The reconstructed finding text is the auditor's. The resolution sections are the resolution engineer's. Original findings must not be edited to make a resolution look better; resolution data is appended, never substituted.

**This document does not approve Foundation 1.0.** It prepares the repository for independent verification of the resolutions.

## Summary

| Severity | Count | Resolved | Partially resolved | Operator decision required | Not resolved |
| --- | --- | --- | --- | --- | --- |
| BLOCKER | 3 | 2 | 0 | 1 | 0 |
| MAJOR | 5 | 5 | 0 | 0 | 0 |
| MINOR | 4 | 4 | 0 | 0 | 0 |
| **Total** | **12** | **11** | **0** | **1** | **0** |

No finding was waived. The single `OPERATOR DECISION REQUIRED` item (FND-B003) is resolved to the maximum extent available to a resolution engineer: the unsafe configuration is structurally prohibited and validation rejects it. Only the operator can supply the final classification policy, and the audit explicitly forbade deciding it on their behalf.

`blocks_gate` values below are defined in `docs/05-governance/gate-model.md`.

---

## BLOCKER findings

### FND-B001 — Circular Foundation acceptance gate

**Severity:** BLOCKER
**Original problem (auditor):**
Foundation approval currently requires all BLOCKER V1 acceptance requirements to pass, but many require implemented software, browser/backend checks, restart testing, execution fixtures, or pilot evidence. Implementation is simultaneously blocked until Foundation approval.

**Required outcome (auditor):**
Separate (1) Foundation acceptance — specifications are complete, internally consistent, testable, and safe enough to authorize Build Ladder generation and fixture-only implementation — from (2) Implementation/V1 acceptance — executable requirements pass after implementation. Preserve separate authorization gates for Build Ladder generation, fixture-only implementation, dry-run readiness, copied-pilot readiness, limited-live readiness, source-retirement readiness, and migration completion. No earlier gate automatically authorizes the next one.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `foundation` — resolving this is what makes G1 reachable at all
- **Ready for independent re-review:** yes

**Files changed**

- `docs/05-governance/gate-model.md` (new)
- `docs/04-acceptance/foundation-acceptance.md` (new)
- `docs/04-acceptance/v1-acceptance.md` (restructured)
- `docs/04-acceptance/live-readiness.md`, `safety-acceptance.md`
- `docs/05-governance/definition-of-ready.md`, `definition-of-done.md`, `open-decisions.md`
- `README.md`, `PROJECT_STATUS.md`, `FOUNDATION_VERSION.md`, `CONTRIBUTING.md`
- `docs/06-operations/dry-run-playbook.md`, `pilot-run-playbook.md`, `live-migration-playbook.md`, `sentinel-playbook.md`, `post-migration-maintenance.md`
- `prompts/foundation-approval.md`, `build-ladder-generation.md`, `one-rung-implementation.md`
- `docs/00-intent/glossary.md`, `docs/03-architecture/technology-decision.md`, `docs/02-specification/inventory-model.md`, `command-model.md`

**Resolution explanation**

The circularity was concrete and measurable. `v1-acceptance.md` previously ended with "All BLOCKER requirements must pass before Foundation approval", while 25 of its 31 rows required running software — a scan to repeat, a batch to interrupt and resume, a UI-plus-backend authorization path to attack, a completed pilot to compare against, a full migration to reconcile. Implementation was blocked until Foundation approval in six separate documents. The gate could not be passed by any sequence of legal actions.

Two kinds of acceptance are now separated. **Foundation acceptance** asks whether the specifications are complete, internally consistent, testable, and safe enough to authorize planning and fixture-only implementation; it is verified with a text editor, a schema validator, and a link checker. **Implementation acceptance** asks whether the built system behaves as specified; it is verified by execution, at the gate where that execution first becomes legal.

`gate-model.md` defines eight gates — `foundation`, `build_ladder`, `implementation`, `dry_run`, `pilot`, `live`, `retirement`, `migration_completion` — each with its own entry criteria, evidence, approver, and an explicit statement that passing it does not authorize the next. Absence of an authorization record is stated to be a prohibition, not a gap. Six competing gate ladders across the repository were replaced by references to this one.

No requirement was deleted. Four documentary rows moved to `foundation-acceptance.md` under their original IDs; seven hybrid rows kept their execution half under the original ID and gained a paired documentary check; the rest were tagged with the gate they block.

**Verification evidence**

- `docs/04-acceptance/v1-acceptance.md` now states "No row in this file blocks Foundation approval", and every row carries a `Gate` column.
- `docs/04-acceptance/foundation-acceptance.md` contains only documentary verification methods; FND-ACC-036 requires a reviewer to confirm that property row by row.
- Repository search for gate-promotion language returns only the explicit non-authorization statements.
- Every operations playbook now opens with an authorization-required section naming its gate.

**Remaining risk**

The gate model is only as strong as the discipline of recording authorizations. It defines the record but cannot enforce that one is created; that enforcement arrives with implementation at G3. The mapping between the eight authorization gates and the eight V1 *operating* gates in `v1-scope.md` is documented but remains two vocabularies a reader must hold at once.

### FND-B002 — Incompatible rule configuration contracts

**Severity:** BLOCKER
**Original problem (auditor):**
`docs/02-specification/rule-model.md` defines one nested schema using fields such as `schema_version`, `rule_set`, `when`, `then.destination`, `confidence.minimum`, `conflict.mode`, `evidence.required`, `confirmation.required`. `config/rules/classification-rules.example.yaml` defines another incompatible schema using `version`, `status`, `evaluation_order`, `defaults`, `enabled`, `applicable_file_types`, `metadata_conditions`, `visual_content_conditions`, `confidence_threshold`, `destination`, `review_required`, `fallback`.

**Required outcome (auditor):**
Select one canonical V1 rule schema. Create a machine-readable schema, preferably `config/schemas/classification-rule-set.schema.json`, defining supported schema version, required and optional properties, status values, condition grammar, destination templates, evidence requirements, confidence behavior, confirmation behavior, conflict behavior, unknown-field rejection, provisional-rule restrictions, and safe defaults. Update `rule-model.md`, `domain-model.md`, all YAML examples, fixtures/readme requirements, acceptance criteria, and traceability records so they all describe exactly the same contract. Provide representative examples that should validate and examples that must fail validation.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `foundation`
- **Ready for independent re-review:** yes

**Files changed**

- `config/schemas/classification-rule-set.schema.json` (new, canonical)
- `config/rules/classification-rules.example.yaml` (rewritten)
- `docs/02-specification/rule-model.md` (rewritten)
- `docs/02-specification/domain-model.md` (ClassificationRule projection note)
- `scripts/validate_rule_config.py`, `scripts/generate_negative_rule_fixtures.py` (new)
- `tests/fixtures/rules/negative/` — 47 fixtures plus `expectations.yaml` (new)
- `config/README.md`, `tests/README.md`, `tests/fixtures/README.md`
- `docs/migration/traceability-matrix.md`, `docs/03-architecture/decisions/ADR-006-rule-driven-classification.md`
- `prompts/rule-change-review.md`

**Resolution explanation**

The audit named two incompatible contracts. There were in fact **three**: the nested shape in `rule-model.md`, the flat shape in the configuration example, and a third set of field names in `domain-model.md` (`destination_template`, `minimum_confidence`, `conflict_policy`, `human_confirmation_required`, `test_case_refs`). Reconciling only the two named would have left the finding half-open.

The nested shape was selected as canonical because it already separates the four safety axes into named objects, separates match from outcome, and carries a `kind` discriminator without which the documented conflict-resolution order is unimplementable. The flat shape's genuinely useful contributions — `evaluation_order`, `conflict_resolution`, and `defaults` — were hoisted into the envelope and **pinned as constants**, so a configuration may restate them but can never reorder them.

One structural change was forced by the audit's own requirement. The old condition grammar used open-ended key names (`path_prefix:`, `field_regex:`). That is fundamentally incompatible with unknown-field rejection: you cannot reject unknown fields while the field-name space is unbounded. Conditions are now closed `{field, op, value, evidence_source}` predicates, which is what makes `additionalProperties: false` meaningful at every level.

Two safety properties fell out of the redesign. Destination templates are relative to a **symbolic** root reference, so no rule file can name an absolute live share path. And `environment` admits only `fixture` and `pilot` — a live rule set is not expressible under schema version 1 at all.

The domain model's field names are retained for the stored entity but are now explicitly labelled a projection of this contract, with a one-to-one mapping, rather than a second wire format.

**Verification evidence**

`python3 scripts/validate_rule_config.py` reports:

```
PASS  schema is valid JSON Schema draft 2020-12
Positive examples (1) — must validate:
  PASS  config/rules/classification-rules.example.yaml
Negative examples (47) — must be rejected:
  PASS  … all 47, each by its intended layer and for its intended reason
ALL RULE-CONTRACT CHECKS PASSED
```

Negative case `retired-flat-schema` confirms the old flat shape is rejected wholesale; `unknown-field-rule`, `unknown-field-ruleset`, `unknown-field-then`, and `unknown-field-confidence` confirm each retired field name is rejected at its own level.

**Remaining risk**

Eight constraints cannot be expressed in JSON Schema — unique rule ids, unique band/priority slots, single unconditional rule, cross-file reference resolution, fixture existence, and linear-time regex compilation. These are implemented as named loader checks in the validator and documented as such rather than left implicit, but they depend on the loader being the only ingress. That guarantee arrives with implementation.

Fixture paths referenced by the example do not exist yet; the validator reports this as a note rather than a failure, since the fixture corpus is built at G3.

### FND-B003 — Provisional rules enabled without mandatory review

**Severity:** BLOCKER
**Original problem (auditor):**
Dogs, drone, and CSV rules are provisional but enabled with `review_required` false. This conflicts with the policy that these rules remain unconfirmed until the operator supplies or confirms the actual classification rules.

**Required outcome (auditor):**
Until the applicable operator decision is resolved: provisional rules must never produce automatically approved or executable outcomes; they must either be disabled or always produce `review_required`; configuration validation must reject unsafe provisional combinations; activation/promotion requires explicit operator policy; tests and acceptance criteria must cover attempted unsafe activation. Do not decide the final Dogs, drone, CSV, or identity policies for the operator.

**Resolution**

- **Status:** OPERATOR DECISION REQUIRED
- **Gate affected:** `dry_run` — OD-012 and OD-003 both block G4; the structural fix itself blocks nothing further
- **Ready for independent re-review:** yes — for the structural resolution. The policy decision is the operator's and is not a re-review item.

**Files changed**

- `config/schemas/classification-rule-set.schema.json`
- `config/rules/classification-rules.example.yaml`
- `docs/02-specification/rule-model.md`, `domain-model.md`
- `tests/fixtures/rules/negative/provisional-*.yaml`
- `docs/05-governance/open-decisions.md` (OD-012, OD-003)
- `docs/04-acceptance/v1-acceptance.md` (V1-ACC-026)
- `config/README.md`, `docs/migration/traceability-matrix.md`

**Resolution explanation**

The root cause was two independent switches for one concept: `enabled: true` alongside `status: provisional`. Two switches for one concept guarantee drift, and they had already drifted — Dogs, drone, and CSV were all enabled with `review_required: false`, and the specification's own CSV example carried `review_state: approved` on a provisional rule.

`enabled` is **deleted**. `status` is the single activation control. The schema then makes the unsafe combination unrepresentable: a rule with `status: provisional` must carry `outcome: route_to_review`, `destination_authority: advisory_only`, `review_state: review_required`, `confirmation.required: true`, `conflict.mode: manual_review`, and a non-empty `policy_ref` naming the open decision blocking its promotion. A configuration violating any of these does not warn — the file is rejected.

Two further structural locks apply regardless of status: a rule whose required evidence includes an AI suggestion can never yield an executable destination, and a rule classified `sensitive_identity` can never carry `status: active`.

The mechanism that preserves the operator's intent while keeping it inert is `destination_authority: advisory_only`. The Dogs, drone, and CSV destinations are still recorded, still shown in review, still explainable — they simply cannot be lifted into an operation-plan entry. The intent survives; the execution does not.

**This finding is marked OPERATOR DECISION REQUIRED rather than RESOLVED, deliberately.** The structural half is complete and verified. The remaining half — what the Dogs, drone, CSV, and identity rules should actually say — is an operator policy decision the audit explicitly forbade making on their behalf. It is tracked as OD-012 and OD-003.

One judgement call is worth flagging: the source material claims Dogs outranks People when both appear. That claim is recorded in the example's `notes` as documented intent and is deliberately **not** encoded as an automatic override, because the handwritten transcriptions that would confirm it are the missing input in OD-012.

**Verification evidence**

- The rewritten example contains **zero** rules with `destination_authority: executable_candidate`. Verified: `authorities: ['advisory_only']`.
- `provisional-auto-approve` — rejected: "'route_to_review' was expected".
- `provisional-confirmation-false` — rejected: "True was expected".
- `provisional-missing-policy-ref` — rejected: "'policy_ref' is a required property".
- `sensitive-identity-active` — rejected: "'active' is not one of ['proposed','provisional','disabled','retired']".
- `ai-evidence-executable` — rejected.
- `unknown-field-rule` (reintroducing `enabled`) — rejected.
- V1-ACC-026 requires the runtime to reject these at config load once implementation exists.

**Remaining risk**

The structural lock is enforced by the schema and the loader. Until implementation exists (G3), nothing enforces that the loader is the only path by which a rule set reaches the engine; that is V1-ACC-026's job at G3.

The operator's actual classification policy remains unwritten. Until OD-012 and OD-003 close, the example rule set classifies nothing automatically — which is the safe state, but also means the rule corpus is not yet functionally useful. That is the correct trade and the audit's explicit instruction.

---

## MAJOR findings

### FND-M001 — File identity and concurrent source-change handling

**Severity:** MAJOR
**Original problem and required outcome (auditor):**
Define stable logical file identity; adapter-specific identity evidence; normalized and raw paths; root identity; device/inode or platform identifier when reliable; high-resolution timestamps; size and approved hash; source-generation/change token; same-path replacement detection; concurrent modification during hashing or copying; hard-link handling; case-only collisions; Unicode-normalization collisions; network filesystem identity limitations; required stop/review behavior. Add corresponding acceptance and fixture requirements.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `implementation` for the execution criteria; the specification itself blocks `foundation`
- **Ready for independent re-review:** yes

**Files changed**

- `docs/02-specification/file-identity-model.md` (new)
- `docs/02-specification/inventory-model.md` (field obligations)
- `docs/02-specification/domain-model.md` (`content_identity_state` defined)
- `docs/02-specification/duplicate-model.md` (hard-link exclusion)
- `docs/03-architecture/adapter-architecture.md` (capability contract)
- `tests/fixtures/README.md` (FX-01 … FX-30)
- `docs/04-acceptance/v1-acceptance.md` (V1-ACC-005, V1-ACC-006)

**Resolution explanation**

The blueprint contained no occurrence of inode, device identifier, change token, hard link, case sensitivity, Unicode normalization, or concurrency anywhere in its active documents. `content_identity_state` was declared as a required field and never defined. `normalized_path` was a field name that constituted the entire path-normalization specification. Identity was effectively `(source_root, relative_path)` plus a hash, which cannot distinguish a file from its replacement at the same path with the same size.

This produced two latent correctness defects, not merely omissions. First, with no link count, a hard-linked set of N names is classified as N exact duplicates and copied N times, silently inflating destination bytes and destroying link topology. Second, byte-identical files differing only in extended attributes or resource forks were merged as exact duplicates on the strength of "equivalent byte identity", a phrase that was never defined.

The new specification defines logical identity as platform-assigned, minted once, never derived from path, and never reused. Identity evidence is **graded** — authoritative, advisory, unavailable, indeterminate — with the composite confidence taken as the **minimum** across components, never the maximum. A per-adapter table grades every identity signal, and the load-bearing consequence is stated plainly: every non-local adapter yields at best advisory object identity, and SFTP and vendor APIs yield none at all.

The change token is **ternary**. `INDETERMINATE` must never be treated as `EQUAL`, by any component, under any threshold, with no configuration flag to collapse it. Tokens are captured at five journalled points, and a copy is eligible for `verified` only if the token was equal both immediately before and immediately after the source read — which is the check the old model could not even express.

An eighteen-row stop/review table maps each hazard to a mandated behavior using the repository's existing soft/blocked/fatal vocabulary rather than inventing new severity words.

**Verification evidence**

- `content_identity_state` now has five defined values, and only `hashed_stable` is admissible as duplicate or verification evidence.
- `duplicate-model.md` states that hard-link sets are not duplicate groups and that zero-byte hash equality is not redundancy evidence.
- 30 identity fixtures enumerated with expected assertions, including FX-19 (same-path replacement with identical content), the case the old model provably could not detect.
- V1-ACC-005 and V1-ACC-006 added as execution criteria at G3.

**Remaining risk**

Identity confidence over network adapters is capped at advisory by physics, not by specification quality. The mitigation is that retirement under an advisory-identity adapter requires an explicit recorded waiver — but a waiver is a human judgement, and the specification cannot make an unreliable identity reliable.

Adapter capability grades in the table are stated from protocol behavior and must be **confirmed by measurement** (FX-27) before any adapter is trusted. Until that fixture runs, the table is an informed expectation.

### FND-M002 — Preservation fidelity

**Severity:** MAJOR
**Original problem and required outcome (auditor):**
Define preservation profiles by adapter and content class. Address file bytes; modified, created, and accessed timestamps where supported; permissions; ownership; ACLs; extended attributes; resource forks; hard links; symbolic links; sparse files; Finder metadata; Synology metadata; macOS package bundles; unsupported metadata; source/destination capability mismatch. Classify each property as required, best effort, intentionally normalized, or unsupported and reported. Hash equality alone must not be described as complete preservation evidence. Add comparison reports, pilot fixtures, and acceptance criteria for preservation fidelity.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `implementation` for the execution criteria; `retirement` for the gate condition
- **Ready for independent re-review:** yes

**Files changed**

- `docs/02-specification/preservation-model.md` (new)
- `docs/02-specification/operation-model.md` (verification recording)
- `docs/02-specification/domain-model.md` (invariants 12 and 13, VerificationResult)
- `docs/00-intent/principles.md` (principles 1 and 12)
- `docs/03-architecture/data-architecture.md`, `ADR-002`, `ADR-004`
- `docs/04-acceptance/safety-acceptance.md` (SAF-003)
- `docs/06-operations/live-migration-playbook.md`, `dry-run-playbook.md`, `post-migration-maintenance.md`
- `docs/04-acceptance/v1-acceptance.md` (V1-ACC-040, V1-ACC-044)
- `tests/fixtures/README.md`

**Resolution explanation**

Every preservation statement in the repository concerned *not mutating the source*. There was **no destination-fidelity requirement anywhere**. The consequence was a chain — hashes stored "for copy verification", verification "may be hash-only in V1", a record "proving copy/move correctness", retirement gated on "hash verification" — in which a hash match was the sole technical precondition standing between a copy and the deletion of the original.

No single sentence claimed too much, which is why it had gone unnoticed. The overstatement was carried by the chain, not by any one link.

The new specification opens with a governing statement that must appear verbatim in every comparison report: hash equality is necessary but not sufficient, and proves nothing about timestamps, permissions, ownership, ACLs, extended attributes, resource forks, hard-link topology, symlink semantics, sparse layout, or filename bytes. Thirty properties are classified per adapter class as required, best-effort, intentionally normalized, or unsupported-and-reported. The four classes are exhaustive: there is no "unknown", and a property whose support has not been **measured** is treated as unsupported until characterization succeeds.

Content-class overlays tighten the base matrix for macOS bundles, symlinks, sparse files, hard-link sets, zero-byte files, and protected vaults. The bundle overlay closes a second latent defect: without it, a package bundle is shredded into member files, classified independently, and destroyed. The symlink overlay states that replacing a link with a copy of its target is prohibited outright — not a best-effort degradation but data-model corruption.

Capability mismatches are resolved at **plan time**, never at execution time, and a required property the destination cannot carry blocks the entries. Automatic downgrade is prohibited; a waiver must name the specific property, and a blanket waiver is invalid.

The word "intentionally" was also removed from the read-only principle. Access-time mutation on read is the archetypal *unintentional* timestamp change, and the acceptance criterion that verified it compared hashes — which cannot detect timestamp, attribute, or permission mutation at all.

**Verification evidence**

- Repository search confirms no document now describes hash equality alone as verified preservation or as grounds for retirement; each of the eleven previously overstating locations was amended.
- `retirement_gate.eligible` is specified false whenever any required property mismatches or is unverifiable without a scoped waiver.
- FX-09 (sparse), FX-12 (extended attributes), and FX-13 (resource fork) each assert explicitly that a hash match does not set preservation-verified.

**Remaining risk**

The profile matrix is stated from protocol capability and must be confirmed by measurement (FX-27) before it gates anything. Cells are an informed expectation until then.

Promoting best-effort properties to required inside protected vaults may make some adapter and destination combinations unusable for vault content. That is the intended conservative outcome, but it is a constraint the operator will meet in practice rather than a cost-free guarantee.

### FND-M003 — SQLite/JSONL authority and crash consistency

**Severity:** MAJOR
**Original problem and required outcome (auditor):**
Define one authoritative durability and recovery protocol spanning filesystem operations; SQLite transactions; append-only JSONL journals; operation IDs; sequence numbers; temporary destination files; flush/fsync behavior where supported; atomic destination finalization; verification; checkpoint creation and sealing; duplicated event delivery; truncated journal records; corrupt journal records; replay; restart reconciliation; every interruption point. Clearly state which record is authoritative; which state is derived; the write order; what happens when any individual write fails; when another filesystem mutation may safely begin.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `implementation` for the execution criteria; the specification itself blocks `foundation`
- **Ready for independent re-review:** yes

**Files changed**

- `docs/02-specification/durability-and-recovery-model.md` (new)
- `docs/03-architecture/decisions/ADR-016-journal-authoritative-sqlite-derived.md` (new)
- `docs/03-architecture/decisions/ADR-005-sqlite-jsonl-manifests.md`, `ADR-013-immutable-audit-log.md`, `ADR-012-adapter-based-filesystem-access.md`
- `docs/02-specification/state-and-persistence.md`, `operation-model.md`, `domain-model.md`, `lifecycle-model.md`, `command-model.md`
- `docs/04-acceptance/v1-acceptance.md` (V1-ACC-045 … V1-ACC-047)
- `tests/fixtures/README.md`

**Resolution explanation**

Authority was never declared. `ADR-005` split responsibility and named the drift hazard without resolving it; the persistence specification then said mutable state is "derived from **or** reconciled against" history, that SQLite holds "the current durable state", and that replay rebuilds derived state "where appropriate" — three mutually incompatible readings. Checkpoints were assigned to both stores. The word `fsync` appeared nowhere in the repository, so there was no defined moment at which anything was durable.

The most consequential gap was ordering. The documented executor wrote the journal at **step 5, after the copy at step 3**. A crash between them left an unattributable filesystem artifact, which falsifies the stated principle that restart reconciles filesystem reality against the journal — there would be nothing to reconcile against. Two further self-contradictions compounded it: a mutable `write_state` field stored *inside* an append-only record, and mutable checkpoint states on an artifact required to be atomic.

The journal is now authoritative and SQLite is a derived, rebuildable projection, justified on the ground that only an append-only log can record that a mutation is *about to* happen and survive a crash mid-mutation. Rebuildability is testable — delete the database, replay, compare — where "the two stores do not drift" had no failure signal at all.

**Gate G** is the load-bearing rule: no filesystem mutation may be attempted before the intent record's durability barrier completes. This is what makes every possible on-disk artifact attributable, and it holds across two independent filesystems because it needs only program order plus a completed barrier.

The crash-state table has seventeen rows, one per interruption point, each with observable filesystem state, journal state, database state, authoritative interpretation, required recovery action, and whether another mutation may begin. Rows I9 and I10 are deliberately handled identically: the journal cannot distinguish "rename issued" from "rename completed", and the specification says so rather than pretending otherwise — both resolve by re-reading and re-hashing.

Processing status became a projection value in both the journal-entry and checkpoint entities, resolving the append-only contradiction. Only a **sealed** checkpoint may be used as a resume point.

**Verification evidence**

- Every protocol step has a numbered failure branch; the crash table has a row for the interruption before and after each durable transition.
- The question the audit asked directly — when may another filesystem mutation begin — has its own normative subsection.
- `state-and-persistence.md` no longer contains the ambiguous disjunction, the "current durable state" claim, or the "where appropriate" qualifier.
- V1-ACC-045 through V1-ACC-047 added, including rebuilding the database from the journal alone.

**Remaining risk**

The protocol assumes durable file fsync, durable directory fsync, and atomic same-directory rename. On `weak` or `unknown` adapters none is guaranteed, and the conservative fallback — mandatory post-finalize re-read, batch size one, no concurrency, no retirement — is a real throughput cost the operator will feel.

An fsync error is treated as unrecoverable data loss, which is correct but means a single transient storage error halts the run and requires operator adjudication.

The specification is unvalidated until the crash-injection harness exists at G3. A seventeen-row table is a hypothesis until each row has been fault-injected.

### FND-M004 — Approval authenticity and binding

**Severity:** MAJOR
**Original problem and required outcome (auditor):**
Bind approval to authenticated operator identity; authentication/session context suitable for local single-user V1; exact subject type and ID; immutable plan ID; plan version and content hash; evidence-bundle version/hash; approval scope; timestamp; expiration where appropriate; revocation; one-time consumption; anti-replay behavior; invalidation when plan, evidence, rules, taxonomy, or relevant source state changes. The frontend captures approval intent. Only the trusted backend evaluates whether the exact approval authorizes execution.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `implementation` for the execution criteria; OD-022 blocks `implementation`
- **Ready for independent re-review:** yes

**Files changed**

- `docs/02-specification/approval-binding-model.md` (new)
- `docs/03-architecture/decisions/ADR-017-approval-binding-and-consumption.md` (new)
- `docs/03-architecture/decisions/ADR-014-frontend-never-authorizes-mutation.md`, `ADR-003-human-approval-destructive.md`, `ADR-015-proposal-vs-execution-separation.md`
- `docs/02-specification/domain-model.md` (Approval entity), `command-model.md`, `operation-model.md`, `interface-model.md`
- `docs/03-architecture/review-console-architecture.md`
- `docs/05-governance/open-decisions.md` (OD-022)
- `docs/04-acceptance/v1-acceptance.md` (V1-ACC-039)

**Resolution explanation**

The approval bound to a subject **id**, not to subject **content**. Because a superseding plan version reuses the plan lineage, an approval granted for a plan was textually satisfiable by a later version of that plan — a version-confusion hole sitting directly in front of the destructive path.

Around it: `consumed` was a state name with no mechanism making consumption atomic, one-time, or a precondition of mutation; `revoked` appeared in the allowed states but in no transition; approvals were "not transferrable across *unrelated* subjects", which affirmatively permitted transfer across related ones; a pilot stop condition depended on revocation stopping a run, but the executor loop had no revocation check; and the human operator — the only actor with destructive authority — was never required to authenticate anywhere, while the Sentinel was.

Sharpest of all, the command envelope carried `validation status` and `authorization status` as fields **on the inbound command**. As written, a client could submit `authorization_status: authorized`. That is a trust-boundary inversion, not a gap.

Approvals are now bound to authenticated identity and session, exact subject type, id, version, and **content hash**, evidence-bundle hash, rule-set and taxonomy hashes, source-precondition digest, adapter descriptors, explicit scope, grant time and expiry, a single-use nonce, and a single-use consumption claim bound to one run. The backend re-derives every bound value from its own state and evaluates a twenty-five-step ordered algorithm with typed rejection codes, at execution time, on every attempt.

Client-supplied authorization fields are **rejected**, not ignored — silently ignoring them hides either an attack or a client defect.

The resume-versus-replay distinction is what makes this safe without breaking restart safety: a claim with intent records resumes under the same run id and is refused under a different one.

Sixteen invalidation triggers make the change-control rule enforceable rather than aspirational: a rule-set or taxonomy change now voids outstanding approvals.

**Verification evidence**

- The approval entity lists every bound field; the lifecycle now includes `claimed`, `released`, `expired`, and `invalidated`, and `revoked` has an actual transition.
- `command-model.md` states that validation and authorization status are server-computed only and that a populated inbound field is rejected with a named code.
- `ADR-014` had its qualifier "on its own" deleted — the phrasing implied that the frontend plus some second factor could authorize.
- V1-ACC-039 requires replayed, expired, revoked, and already-consumed approvals each to be rejected with a specific reason code.

**Remaining risk**

The operator authentication model is a **scope addition**. V1 never stated an authentication requirement, and resolving this finding required one. Rather than decide it, it is recorded as **OD-022** with a proposed minimal local single-user shape for the operator to accept, tighten, or scope differently.

Approval expiry introduces real operational friction: a long-running batch can outlive its authorization, and a plan edit voids an approval. That friction is the intended trade, not a defect, but it will be felt.

Clock trust is assumed. A monotonic anchor is specified and regression is rejected, but a compromised host clock remains outside what this model can defend against.

### FND-M005 — Unsafe or incomplete rule conflict modes

**Severity:** MAJOR
**Original problem and required outcome (auditor):**
Remove or precisely restrict `keep_first`, `merge`, and vague `version` behavior. For V1, prefer explicit deterministic outcomes such as `manual_review`, `skip`, or safely specified destination versioning. Do not allow configuration load order to select a winner. Define priority bands; specificity calculation; tie-breaking; multi-destination behavior; manual-review behavior; prohibited content merging.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `foundation`
- **Ready for independent re-review:** yes

**Files changed**

- `config/schemas/classification-rule-set.schema.json`
- `docs/02-specification/rule-model.md` (conflict resolution rewritten)
- `docs/02-specification/operation-model.md` (collision handling)
- `docs/02-specification/domain-model.md` (ClassificationRule invariants)
- `tests/fixtures/rules/negative/conflict-mode-*.yaml`, `merge-content-true.yaml`, `load-order-significant.yaml`, `reordered-*.yaml`

**Resolution explanation**

Tracing the unsafe modes to their origin explained the whole finding. The operations manual says: *"Existing destination names generate a collision plan: skip, version, content-compare, or operator decision."* That sentence is about **destination-path collision**. It was imported into the rule model as a list of **rule-conflict** modes, where `version` means nothing and `content-compare` plausibly became `merge`.

So the fix is not to delete three enum values but to separate two mechanisms that were conflated. **Rule conflict** — two rules disagreeing about a destination — is now `manual_review` or `skip`, nothing else. **Destination collision** — one agreed destination already occupied — is a separate `collision` object with `route_to_review`, `skip`, or `versioned_suffix`, evaluated at plan time.

`keep_first` is removed with no replacement: it makes configuration load order authoritative, which is the exact failure the finding names. `merge` is removed with no replacement, and `conflict.merge_content` is pinned `false` as a machine-checkable prohibition marker, so writing `merge_content: true` is a validation failure rather than a silent no-op. Destination versioning survives only with an exact template and a maximum, and the **new** copy takes the suffix — the pre-existing file is never renamed, moved, or replaced.

Five priority bands with disjoint numeric ranges make cross-band ties impossible by construction, and the schema enforces the ranges so a band can never be misread from a number. Specificity is a defined integer computed from the condition tree, with two deliberate design choices: a provenance multiplier makes a deterministic fact structurally more specific than a model guess of the same shape, and `any` aggregates by **minimum** so authors cannot inflate specificity by adding alternatives.

Load order is pinned out of existence: `defaults.load_order_significance` is `none`, and a configuration claiming otherwise fails validation.

Renumbering the example into bands corrected a pre-existing inversion — drone and CSV are deterministic evidence and now outrank dog detection, which is content inference. The old flat numbering had content inference outranking deterministic evidence, contradicting the documented precedence order.

**Verification evidence**

- `conflict-mode-merge`, `conflict-mode-keep-first`, `conflict-mode-version` — all rejected.
- `merge-content-true` — rejected: "False was expected".
- `load-order-significant` — rejected: "'none' was expected".
- `reordered-conflict-resolution` and `reordered-evaluation-order` — rejected against pinned constants.
- `priority-outside-band`, `band-kind-mismatch`, `always-outside-fallback` — rejected.
- Repository search returns no remaining use of `keep_first`, `merge`, or a bare `version` conflict mode.

**Remaining risk**

The specificity algorithm is deterministic but its weights are a judgement. Two rules can still tie, which is why the lexical tie-break exists as a terminal guarantee — but a lexical tie-break means rule naming has a small, non-obvious effect on outcomes in genuinely ambiguous cases.

The load-order guarantee is testable only by shuffling the rules array and asserting identical decisions. That test cannot run until G3.

---

## MINOR findings

### FND-m001 — Duplicated classification event

**Severity:** MINOR
**Original problem and required outcome (auditor):**
Remove the duplicated `ClassificationDecisionProposed` event and perform an event-contract consistency pass.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `foundation`
- **Ready for independent re-review:** yes

**Files changed**

- `docs/02-specification/event-model.md` (canonical vocabulary)
- `docs/02-specification/domain-model.md` (FileRecord and ClassificationDecision emitted events)

**Resolution explanation**

The duplication was cross-file and semantic rather than a repeated line. `FileRecord` emitted `ClassificationProposed` while `ClassificationDecision` emitted `ClassificationDecisionProposed` — the same fact under two names, depending on which document a reader consulted. Only the second appeared in the event vocabulary, so a consumer built from the domain model would have subscribed to an event type that did not exist.

The consistency pass then found the problem was much larger than one name. The domain model declared **33 events absent from the canonical vocabulary**, including three entire families: every approval event, every hash event, and every checkpoint event. That is not cosmetic — the approval trail was not in the replayable audit log, `HashMismatchDetected` drives a documented hard stop, and `JournalWriteFailed` backs a global invariant. `MetadataExtracted` had two emitting aggregates, and `InventoryCheckpointWritten` was a second name for `CheckpointWritten`.

`ClassificationProposed` was removed in favour of the name that correctly identifies its subject. `event-model.md` is now declared the single authority for event names under two rules — one event one name, one event one emitter — and any asymmetry between the two documents is defined as a defect. `ClassificationConflictDetected` was added, since the conflict record required by the resolution algorithm had no event.

**Verification evidence**

Extracting both name sets and diffing them:

```
domain-only:   (empty)
event-only:    (empty)
total:         89 events
duplicate emitters in domain-model: (none)
```

Exact symmetric match in both directions, with exactly one emitting aggregate per name.

**Remaining risk**

Event payload schemas remain undefined per event type. The envelope carries `schema_version: 1`, and the store is required to preserve it, but no document defines what version 1 *is* for a given event or what the compatibility policy is. This is the same class of defect as FND-B002 — a version marker with no schema behind it — at smaller scale, and it is noted here rather than silently left.

The command envelope lacks correlation and causation ids, so command-originated events have nothing to point at for cross-stream correlation.

### FND-m002 — Misleading review-console terminology

**Severity:** MINOR
**Original problem and required outcome (auditor):**
Replace confusing "read-only approval console" terminology with "non-executing decision surface." State exactly which application-state commands it may submit and that it remains read-only toward underlying file data.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `foundation`
- **Ready for independent re-review:** yes

**Files changed**

- `docs/03-architecture/review-console-architecture.md` (rewritten)
- `docs/03-architecture/system-architecture.md`, `repository-architecture.md`
- `docs/02-specification/interface-model.md`
- `apps/review-console/README.md`

**Resolution explanation**

The old phrase was misleading in two directions at once. "Read-only" implied the console writes nothing, when it legitimately writes application state — review items, decisions, approval-intent records. "Approval console" implied the console *performs* approval, when it only captures an operator's expressed intent.

The document also contradicted itself within seven lines, describing the console as capturing approval **state** and then as communicating only **intent**.

The console is now a **non-executing decision surface**: read-only toward underlying file data, write-capable toward a bounded set of application state, and non-executing in that no console action alone causes a filesystem mutation. Thirteen permitted commands are enumerated, and the prohibited set is enumerated explicitly rather than left as a general principle — including every operation, batch, journal, checkpoint, scan, and rule-set command, and anything that would copy, move, rename, quarantine, retire, overwrite, or delete.

A backend-obligations section was added. The previous document stated only frontend prohibitions, and no document anywhere said the backend must independently re-derive the authorization decision. Prohibiting the client is not the same as binding the server.

**Verification evidence**

- Repository search returns no remaining instance of "read-only approval console" or its variants.
- The permitted and prohibited command lists cross-check against `command-model.md`.
- The interface model's console section carries the same constraint and adds that the console may never construct, sign, or self-validate an approval record.

**Remaining risk**

The command lists must stay synchronized with `command-model.md` as it evolves. This is a documentation-maintenance dependency, not a structural guarantee, until permission tests exist at G3 (V1-ACC-038).

### FND-m003 — Severity conflated with blocked gate

**Severity:** MINOR
**Original problem and required outcome (auditor):**
Separate decision severity from the gate it blocks. Add an explicit `blocks_gate` field or column using values such as `foundation`, `build_ladder`, `implementation`, `dry_run`, `pilot`, `live`, `retirement`, `migration_completion`.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `foundation`
- **Ready for independent re-review:** yes

**Files changed**

- `docs/05-governance/gate-model.md`
- `docs/05-governance/open-decisions.md` (restructured with `blocks_gate`)
- `docs/04-acceptance/v1-acceptance.md`, `foundation-acceptance.md`
- `prompts/foundation-approval.md`

**Resolution explanation**

Severity was doing the work a gate field should have done, and the repository held three mutually contradictory rules about what a BLOCKER blocks: open decisions said treat them as live-migration blockers and not blueprint blockers; the approval prompt said do not approve unresolved BLOCKER items; and the definition of ready said no open BLOCKER prevents interpretation of the work. With eleven BLOCKER-severity decisions in the register, the second rule made Foundation approval permanently unreachable while the first made all eleven irrelevant to it.

Severity and `blocks_gate` are now explicitly orthogonal attributes. Severity states consequence if wrong; `blocks_gate` states which gate is stopped. A BLOCKER may carry `blocks_gate: live`; a MINOR may carry `blocks_gate: implementation`.

All 22 open decisions carry a `blocks_gate` value, plus a **re-confirm at** column for answers that must be revalidated at a later gate. The approval prompt's rule was replaced: do not approve while any decision carries `blocks_gate: foundation`, regardless of severity — and decisions carrying a later value must not be silently resolved there.

The resulting distribution is the substantive outcome: **no open decision blocks `foundation`**. That is stated explicitly with its justification, because a reader is entitled to be suspicious of a register that conveniently blocks nothing. The reason is that none of these decisions creates an internal contradiction in the blueprint; every one is a decision about operating on real data, which no gate before G4 permits.

**Verification evidence**

- All 22 decisions carry both attributes; a gate-coverage table totals them.
- The audit register, foundation acceptance, and V1 acceptance all carry gate attribution.
- The three contradictory severity rules were each amended.

**Remaining risk**

`blocks_gate` values were assigned by analysis, not by operator confirmation. OD-014 in particular is classified as blocking `implementation` on the reading that the taxonomy model already names a canonical control layout and records the alternate — one reviewer could argue it blocks `foundation` as an internal contradiction. The reasoning is stated in the register so a verifier can disagree with it explicitly.

### FND-m004 — Inconsistent inventory field obligations

**Severity:** MINOR
**Original problem and required outcome (auditor):**
Reconcile required, nullable, optional, and adapter-conditional inventory fields across the domain and inventory specifications.

**Resolution**

- **Status:** RESOLVED
- **Gate affected:** `foundation`
- **Ready for independent re-review:** yes

**Files changed**

- `docs/02-specification/inventory-model.md` (field obligation table)
- `docs/02-specification/domain-model.md`
- `docs/03-architecture/data-architecture.md`

**Resolution explanation**

Three documents described the inventory field set with three different obligations: the domain model listed ten fields as required, the inventory model listed twenty-two as "when available", and the data architecture listed six informally. The same field carried opposite obligations depending on where a reader looked — `size_bytes` was required in one and optional in another.

Beyond the obligation conflict there were genuine structural errors. Six fields were placed on the wrong entity: content hashes belong to `HashRecord`, MIME and media metadata to `MetadataRecord`, classification and review state to their own aggregates, and the operation reference pointed the wrong way — operation entries reference file records, not the reverse.

There is now one authoritative table of 41 fields, each with type, nullability, the stage by which it is required, and adapter-conditional notes. Fields resolved by reference are listed separately with their authoritative home, so no fact has two homes.

Four obligation rules were added, of which one matters most: a nullable field must be present as an explicit `unavailable` when the adapter cannot supply it. Silence and `null` are not equivalent to `unavailable` — a distinction that carries real weight for identity evidence, where a missing object id and an unavailable one lead to different behavior.

**Verification evidence**

- The table declares that where another document appears to redefine an obligation, this table governs.
- Reference-resolved fields are enumerated with their authoritative entity.
- Adapter-conditional notes align with the identity evidence and preservation profile tables.

**Remaining risk**

The table adds fields introduced by the identity and preservation models, so it is larger than any of the three lists it replaces. Nothing yet enforces that a new field is added here rather than to one of the other documents; that discipline is a review obligation under the definition of done.

Several entities referenced by acceptance criteria still do not exist in the domain model — `ProvenanceRecord`, `ErrorRecord`, `AuditEvent`, `PilotRun`, `LiveRun`, `SentinelCheck`. That is outside this finding's scope and is noted as a residual observation rather than silently absorbed.

---

## Resolution status legend

- **RESOLVED** — the required outcome is fully met within the authority of a documentation-stage resolution engineer.
- **PARTIALLY RESOLVED** — some required sub-outcomes remain.
- **OPERATOR DECISION REQUIRED** — the structural/safety half is resolved; a policy choice reserved to the operator remains.
- **NOT RESOLVED** — no adequate resolution was produced.

## Stop

This document is evidence, not authorization. Foundation 1.0 is **not** approved by this file.
