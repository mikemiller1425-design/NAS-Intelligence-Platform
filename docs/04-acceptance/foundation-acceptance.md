# Foundation Acceptance

## Purpose

This document holds the acceptance requirements for **gate G0 — Foundation Approval** (`docs/05-governance/gate-model.md`).

Every requirement here is verifiable **by reading and validating artifacts in this repository**. None requires implemented software, a running backend, a browser, restart testing, execution fixtures, or pilot evidence. That separation is the resolution of audit finding **FND-B001**.

Execution-verifiable requirements live in `docs/04-acceptance/v1-acceptance.md` and are consumed by gate G2 and later. They are **not** prerequisites for Foundation approval.

## How to read the columns

- **Verification** — the documentary check a reviewer performs. It must be performable with a text editor, a schema validator, and a link checker.
- **Evidence** — what the reviewer records.
- **Severity** — impact if wrong.
- **`blocks_gate`** — the earliest gate the requirement blocks. Every requirement in this file blocks `foundation` by construction; the column is retained so the two attributes stay visibly independent (FND-m003).

## Specification completeness

| ID | Requirement | Verification | Evidence | Severity | `blocks_gate` |
| --- | --- | --- | --- | --- | --- |
| FND-ACC-001 | Every documented domain entity has purpose, required fields, states, invariants, commands, emitted events, and V1 limits. | Read `docs/02-specification/domain-model.md` section by section. | Section checklist | BLOCKER | `foundation` |
| FND-ACC-002 | The event vocabulary is single-authority: every event name in `domain-model.md` appears in `event-model.md` and vice versa, with exactly one emitting aggregate per name. | Extract both name sets and diff them; check for duplicate emitters. | Diff output showing empty symmetric difference | BLOCKER | `foundation` |
| FND-ACC-003 | Every command in `command-model.md` is reachable from a documented actor with a documented authority. | Cross-read `command-model.md` against `permission-model.md`. | Cross-reference table | BLOCKER | `foundation` |
| FND-ACC-004 | Inventory field obligations are stated exactly once and agree across the domain and inventory specifications. | Compare field tables in `domain-model.md` and `inventory-model.md`. | Field obligation table | BLOCKER | `foundation` |
| FND-ACC-005 | Lifecycle transitions are enumerated, and forbidden transitions are stated explicitly. | Read `lifecycle-model.md`. | Transition table review | BLOCKER | `foundation` |

## Rule contract

| ID | Requirement | Verification | Evidence | Severity | `blocks_gate` |
| --- | --- | --- | --- | --- | --- |
| FND-ACC-010 | Exactly one canonical rule schema exists, published as a machine-readable JSON Schema. | Confirm `config/schemas/classification-rule-set.schema.json` exists and is the only rule schema in the repository. | Schema file, repository search | BLOCKER | `foundation` |
| FND-ACC-011 | The JSON Schema is syntactically valid and compiles under a draft 2020-12 validator. | Run a schema validator against the schema itself. | Validator output | BLOCKER | `foundation` |
| FND-ACC-012 | Every positive rule example in the repository validates against the canonical schema. | Validate each positive example. | Validator output per example | BLOCKER | `foundation` |
| FND-ACC-013 | Every negative rule example fails validation, and fails **for the intended reason**. | Validate each negative example and compare the reported error against the documented expected reason. | Validator output with error paths | BLOCKER | `foundation` |
| FND-ACC-014 | `rule-model.md`, `domain-model.md`, all YAML examples, fixture requirements, acceptance criteria, and traceability records describe the same contract. No obsolete field names survive. | Search the repository for retired field names; cross-read the documents. | Search results, cross-read notes | BLOCKER | `foundation` |
| FND-ACC-015 | The schema rejects unknown fields at every object level. | Validate an example carrying an unknown field at each level. | Validator output | BLOCKER | `foundation` |
| FND-ACC-016 | A rule with `status: provisional` cannot express an automatically executable outcome; the schema itself rejects the unsafe combination. | Validate the provisional-auto-approve negative example. | Validator rejection | BLOCKER | `foundation` |
| FND-ACC-017 | Conflict modes are restricted to deterministic, safe values. `keep_first` and `merge` are absent; destination versioning is precisely specified. | Search for retired conflict modes; read the conflict specification. | Search results | BLOCKER | `foundation` |
| FND-ACC-018 | Rule precedence is fully determined by documented priority bands, specificity, and tie-break — never by configuration load order. | Read the conflict-resolution specification for an explicit load-order prohibition and a total ordering. | Specification review | BLOCKER | `foundation` |

## Safety posture (documentary)

| ID | Requirement | Verification | Evidence | Severity | `blocks_gate` |
| --- | --- | --- | --- | --- | --- |
| FND-ACC-020 | No document authorizes live NAS access, mounting, or scanning at Foundation stage. | Search all documents for live-access authorization language. | Search results | BLOCKER | `foundation` |
| FND-ACC-021 | No document authorizes Build Ladder generation without a separate explicit gate. | Read `gate-model.md`, `PROJECT_STATUS.md`, `FOUNDATION_VERSION.md`, handoffs. | Cross-read notes | BLOCKER | `foundation` |
| FND-ACC-022 | Copy-before-delete, dry-run default, protected-vault overwrite prohibition, and unavailability of permanent deletion are stated consistently everywhere they appear. | Search for each rule and compare wording. | Search results | BLOCKER | `foundation` |
| FND-ACC-023 | The Raspberry Pi is Sentinel-only in every document; no document grants it classification, approval, or mutation authority. | Search all sentinel references. | Search results | BLOCKER | `foundation` |
| FND-ACC-024 | No Future Registry capability appears as a required V1 capability. | Compare `docs/future-registry/` against `v1-scope.md` and the specifications. | Comparison notes | BLOCKER | `foundation` |
| FND-ACC-025 | No secrets, credentials, tokens, live hostnames, or private share names are committed. | Run a credential-pattern scan across the repository. | Scan output | BLOCKER | `foundation` |
| FND-ACC-026 | No unresolved placeholder (`TODO`, `TBD`, `FIXME`, filler text) exists outside the formal open-decision register and the immutable source material. | Search the repository. | Search output | MAJOR | `foundation` |
| FND-ACC-027 | Every internal document link and referenced repository path resolves. | Run a link and path checker over all Markdown. | Checker output | MAJOR | `foundation` |

## Gate and governance coherence

| ID | Requirement | Verification | Evidence | Severity | `blocks_gate` |
| --- | --- | --- | --- | --- | --- |
| FND-ACC-030 | Exactly one gate model exists and every other document references it rather than restating it. | Read `gate-model.md`; search for competing gate lists. | Search results | BLOCKER | `foundation` |
| FND-ACC-031 | No gate is described anywhere as automatically authorizing the next gate. | Search for promotion language across governance, acceptance, operations, and handoffs. | Search results | BLOCKER | `foundation` |
| FND-ACC-032 | Every open decision carries both a severity and a `blocks_gate` value. | Read `docs/05-governance/open-decisions.md`. | Register review | BLOCKER | `foundation` |
| FND-ACC-033 | No open decision classified `blocks_gate: foundation` remains unresolved. | Filter the open-decision register. | Filtered list | BLOCKER | `foundation` |
| FND-ACC-034 | Every audit finding has a recorded resolution status; none is silently waived. | Read `docs/audits/foundation-v1-audit.md`. | Resolution register | BLOCKER | `foundation` |
| FND-ACC-035 | Definition of Ready and Definition of Done reference the gate model and do not define competing readiness rules. | Read both governance documents. | Cross-read notes | MAJOR | `foundation` |
| FND-ACC-036 | Foundation acceptance contains no requirement that needs executing software. | Read every row in this file and confirm the verification column is documentary. | Self-review record | BLOCKER | `foundation` |

## Implementability

| ID | Requirement | Verification | Evidence | Severity | `blocks_gate` |
| --- | --- | --- | --- | --- | --- |
| FND-ACC-040 | File identity is specified precisely enough to implement against fixtures without selecting a live adapter. | Read `docs/02-specification/file-identity-model.md`. | Specification review | BLOCKER | `foundation` |
| FND-ACC-041 | Preservation fidelity is specified per adapter class and content class, with every property classified `required`, `best_effort`, `normalized`, or `unsupported_reported`. | Read `docs/02-specification/preservation-model.md`. | Profile matrix review | BLOCKER | `foundation` |
| FND-ACC-042 | Hash equality is nowhere described as sufficient proof of preservation. | Search for preservation claims tied to hash equality alone. | Search results | BLOCKER | `foundation` |
| FND-ACC-043 | Exactly one durability and recovery protocol exists; it names the authoritative record, the derived state, and the write order. | Read `docs/02-specification/durability-and-recovery-model.md`. | Specification review | BLOCKER | `foundation` |
| FND-ACC-044 | A deterministic crash-state table covers interruption before and after every durable transition. | Read the crash-state table; confirm every protocol step has both a before and an after row. | Step-to-row mapping | BLOCKER | `foundation` |
| FND-ACC-045 | Approval binding is specified with all bound fields, a backend evaluation algorithm, invalidation triggers, one-time consumption, and anti-replay behavior. | Read `docs/02-specification/approval-binding-model.md`. | Specification review | BLOCKER | `foundation` |
| FND-ACC-046 | The frontend/backend trust boundary states that the frontend captures intent only and never evaluates authorization. | Read the approval and review-console documents and `ADR-014`. | Cross-read notes | BLOCKER | `foundation` |
| FND-ACC-047 | Fixture requirements are enumerated specifically enough to build the fixture corpus at G2 without further design decisions. | Read `tests/fixtures/README.md`. | Fixture list review | MAJOR | `foundation` |
| FND-ACC-048 | Adapter-dependent behavior is specified as a capability contract, so implementation can proceed against fixtures while OD-016 remains open. | Read `docs/03-architecture/adapter-architecture.md` and the preservation profiles. | Specification review | BLOCKER | `foundation` |

## Traceability

| ID | Requirement | Verification | Evidence | Severity | `blocks_gate` |
| --- | --- | --- | --- | --- | --- |
| FND-ACC-050 | Every significant source concept maps to an active document, a Future Registry entry, or an open decision. | Read `docs/migration/traceability-matrix.md`. | Matrix review | BLOCKER | `foundation` |
| FND-ACC-051 | Nothing safety-critical was dropped from the source material without an explicit recorded rejection and rationale. | Read `docs/migration/source-reconciliation.md`. | Reconciliation review | BLOCKER | `foundation` |
| FND-ACC-052 | Every acceptance requirement in `v1-acceptance.md` names the specification it tests, and that specification exists. | Cross-check the Related-spec column. | Cross-reference results | MAJOR | `foundation` |

## Requirements relocated from `v1-acceptance.md`

These four requirements were documentation-verifiable but were previously listed among the execution-verifiable rows, where the circular pass rule made them Foundation prerequisites alongside 25 rows that could never be met. They keep their original IDs so traceability is preserved; only their home changed.

| ID | Requirement | Verification | Evidence | Severity | `blocks_gate` |
| --- | --- | --- | --- | --- | --- |
| V1-ACC-043 | Private/explicit media stay within local processing and vault boundaries. | Review privacy policy and adapter defaults. | Privacy docs, config | MAJOR | `foundation` |
| V1-ACC-051 | Live migration readiness is a separate ladder stage, distinct from implementation completeness. | Confirm the distinction in `gate-model.md` and `live-readiness.md`. | Gate model, live-readiness.md | BLOCKER | `foundation` |
| V1-ACC-054 | A post-migration maintenance foundation is defined without unattended live watchers. | Review the maintenance playbook against FR-012. | post-migration-maintenance.md | MAJOR | `foundation` |
| V1-ACC-055 | Traceability covers significant source concepts; Future Registry does not leak into V1 scope. | Review the matrix against `v1-scope.md` and `exclusions.md`. | traceability-matrix.md | BLOCKER | `foundation` |

## Requirements with an execution half

Seven requirements had both a documentary half and an execution half. The documentary half is verified here under the `FND-ACC-*` ID shown; the execution half keeps its original `V1-ACC-*` ID in `v1-acceptance.md` and is verified at gate G3 or later.

| Documentary half (here) | Execution half (`v1-acceptance.md`) | Split |
| --- | --- | --- |
| FND-ACC-004 | V1-ACC-003 | Field set is defined vs. an export actually contains it |
| FND-ACC-018 | V1-ACC-022 | Precedence is documented and total vs. the engine obeys it |
| FND-ACC-016 | V1-ACC-023 | Identity rule is disabled by default in config vs. runtime review hold |
| FND-ACC-022 | V1-ACC-033 | Protected-vault list and collision policy exist vs. the copy engine enforces them |
| FND-ACC-022 | V1-ACC-035 | Retirement gating and no-permanent-deletion policy stated vs. attempts rejected at runtime |
| FND-ACC-025 | V1-ACC-042 | Repository secret scan vs. log-redaction samples |
| FND-ACC-023 | V1-ACC-052 | Sentinel authority limits documented vs. sentinel authority tests |

## Pass rule

Foundation approval (G0) may be recommended only when:

1. every **BLOCKER** requirement in **this file** passes;
2. every **MAJOR** requirement in this file passes or carries an explicit, recorded operator waiver;
3. every audit finding has a recorded resolution status;
4. no open decision classified `blocks_gate: foundation` remains unresolved.

**Requirements in `docs/04-acceptance/v1-acceptance.md` are explicitly not part of this pass rule.** They are evaluated at gate G2 and later, after implementation exists to evaluate.

Passing G0 does not authorize G1. Build Ladder generation requires its own explicit operator authorization.
