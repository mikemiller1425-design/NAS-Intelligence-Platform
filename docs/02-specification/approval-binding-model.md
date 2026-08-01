# Approval Binding Model

## Purpose

This document defines how an operator approval is bound, evaluated, consumed, invalidated, and revoked. It resolves audit finding **FND-M004**.

Before it, an approval bound to a *subject id* rather than to *content*, had a `consumed` state with no mechanism behind it, permitted transfer across "related" subjects, and carried its authorization status as an inbound field on the command envelope — meaning a client could assert it.

## Trust boundary

> **The frontend — review console, CLI prompt, or any future surface — captures approval INTENT only. It never produces, holds, transmits, or asserts an authorization decision. Only the trusted backend evaluates whether an exact approval authorizes an exact execution, and it does so by re-deriving every bound value from its own authoritative state.**

| Value | May the client supply it? | Backend obligation |
| --- | --- | --- |
| `approval_request_id` | Yes (echo) | Must match a request the backend itself issued and has not closed. |
| `nonce` | Yes (echo) | Must match the issued nonce; single use; checked against the nonce ledger. |
| `displayed_binding_digest` | Yes (echo) | Used **only** as evidence of what the operator saw. Compared against the backend's own recomputation. **Never an input to the decision.** |
| `subject_id`, `subject_version` | Yes (echo) | Recomputed and compared; mismatch rejects. |
| Plan, evidence, rule-set, taxonomy, and precondition hashes | Echo only | **Always recomputed server-side from authoritative state.** A client-supplied value is never trusted as the value. |
| `approval_scope` | No | Derived server-side from the plan and the active mode configuration. |
| Approver identity | No | Derived from the authenticated session, never from the payload. |
| `authorization_status`, `validation_status` | **No — rejected if present** | Server-computed only. |
| `approval_state` | No | Derived from the Journal only. |

Corollary obligations:

- The backend must re-evaluate authorization **at execution time**, not only at grant time.
- The backend must not cache an authorization verdict across a restart, a plan change, an evidence change, a rule or taxonomy change, or a source-state change.
- The backend must **reject** any request carrying an authorization assertion, rather than ignoring it. Silently ignoring hides either an attack or a client defect.

## Approval record schema

**The authoritative approval record is the `approval_granted` record in the Execution Journal.** The SQLite approvals table is a derived index.

```yaml
record_type: approval_granted
payload:
  approval_id: "apr_2026_0731_0007"
  approval_schema_version: 1
  approval_request_id: "areq_2026_0731_0007"    # backend-issued challenge

  # Subject binding — exact and content-addressed
  subject_type: "OperationPlan"                 # | RuleSet | TaxonomyNode | ReviewException
                                                # | PilotGate | LiveGate | RollbackAuthority
                                                # | RetirementAuthority
  subject_id: "plan_0042"
  subject_version: "3"                          # EXACT. Never a range, never "latest".
  subject_content_hash: "sha256:…"

  # Evidence binding
  evidence_bundle_id: "evb_0042_v3"
  evidence_bundle_version: "3"
  evidence_bundle_hash: "sha256:…"

  # Decision-input binding
  rule_set_id: "rs-fixture-example-001"
  rule_set_version: "1.0.0"
  rule_set_hash: "sha256:…"
  taxonomy_version: "2026.07"
  taxonomy_hash: "sha256:…"

  # Source-state binding
  precondition_set_hash: "sha256:…"             # digest over the ordered set of
                                                # (entry_id, normalized_source_path,
                                                #  precondition_hash, precondition_size,
                                                #  change_token)
  entry_count: 100
  total_bytes: 4823551122

  # Scope
  approval_scope:
    mode: "pilot"                               # fixture | dry_run | pilot | live
    operation_types: ["copy"]
    source_roots: ["root_pilot_src"]
    destination_roots: ["root_pilot_dst"]
    max_entries: 100
    max_bytes: 5000000000
    allows_source_retirement: false
    allows_protected_vault_overwrite: false     # MUST be false in V1
    allows_permanent_deletion: false            # MUST be false in V1
    config_modes_hash: "sha256:…"
    engine_identity: "mac-mini-engine"
    degraded_durability_permitted: false
    preservation_profile_id: "pp_local_to_smb_v1"
    adapter_descriptor_ids: ["acd_src_v1", "acd_dst_v1"]

  # Approver identity and authentication context
  approver:
    principal_id: "operator:primary"
    display_name: "Primary Operator"
    identity_source: "local_operator_registry"
    authority_classes: ["approve_plan", "execute_plan"]
  authentication_context:
    auth_method: "local_os_session+passphrase"
    auth_event_id: "auth_2026_0731_0031"
    authenticated_at: "2026-07-31T22:58:10Z"
    session_id: "sess_…"
    session_binding_hash: "sha256:…"
    channel: "review_console_localhost"
    remote_access: false

  # Temporal validity
  granted_at: "2026-07-31T23:00:00Z"
  not_before: "2026-07-31T23:00:00Z"
  expires_at: "2026-08-01T03:00:00Z"

  # Anti-replay
  nonce: "…"                                    # backend-generated, unpredictable, single use
  max_uses: 1
  binding_digest: "sha256:…"                    # digest over every field above
  operator_affirmation_text: "…"                # exact text shown at the moment of approval
```

Companion authoritative records: `approval_consumption_claimed`, `approval_consumed`, `approval_consumption_released`, `approval_revoked`, `approval_invalidated`.

## Backend authorization evaluation

Executed for **every entry**, on **every attempt**, including after every restart. Checks run in order and short-circuit on the first failure. Every failure emits its reject code into the Journal.

| Step | Check | Reject code |
| --- | --- | --- |
| AUTHZ-01 | Runtime mode is enabled and equals the approved mode; the modes-configuration hash matches. | `APR-E01_MODE_MISMATCH` |
| AUTHZ-02 | An `approval_granted` record with this approval id exists in the Journal. | `APR-E02_APPROVAL_NOT_FOUND` |
| AUTHZ-03 | The approval record's hash and chain position verify. | `APR-E03_APPROVAL_INTEGRITY_FAILED` |
| AUTHZ-04 | No revocation for this approval, read from the durable journal tail — never from cache. | `APR-E04_APPROVAL_REVOKED` |
| AUTHZ-05 | No invalidation for this approval. | `APR-E05_APPROVAL_INVALIDATED` |
| AUTHZ-06 | Not already consumed, and not claimed by a **different** run. | `APR-E06_APPROVAL_ALREADY_CONSUMED` |
| AUTHZ-07 | Within the validity window, using a clock anchored to a monotonic source. | `APR-E07_APPROVAL_EXPIRED` / `APR-E08_CLOCK_UNTRUSTED` |
| AUTHZ-08 | Subject type and id match the plan being executed. | `APR-E09_SUBJECT_MISMATCH` |
| AUTHZ-09 | Subject version matches **exactly**. | `APR-E10_SUBJECT_VERSION_MISMATCH` |
| AUTHZ-10 | Recomputed plan content hash matches the bound value. | `APR-E11_PLAN_HASH_MISMATCH` |
| AUTHZ-11 | Recomputed evidence-bundle hash matches. | `APR-E12_EVIDENCE_HASH_MISMATCH` |
| AUTHZ-12 | Active rule-set id, version, and hash match the bound values. | `APR-E13_RULESET_CHANGED` |
| AUTHZ-13 | Active taxonomy version and hash match. | `APR-E14_TAXONOMY_CHANGED` |
| AUTHZ-14 | Recomputed precondition-set hash matches. | `APR-E15_PRECONDITION_SET_CHANGED` |
| AUTHZ-15 | Live source revalidation for this entry: path, size, hash, and change token match the entry preconditions. | `APR-E16_SOURCE_DRIFT` |
| AUTHZ-16 | Operation type, roots, and running totals are within scope; retirement permitted only if the scope allows it. | `APR-E17_SCOPE_VIOLATION` |
| AUTHZ-17 | The approver holds the required authority class for this subject type. | `APR-E18_APPROVER_NOT_AUTHORIZED` |
| AUTHZ-18 | The authentication context resolves to a real auth event; the session was valid at grant time and has not been revoked; remote access is false in V1. | `APR-E19_AUTH_CONTEXT_INVALID` |
| AUTHZ-19 | The requesting actor is not the Sentinel and not any non-operator principal. | `APR-E20_ACTOR_NOT_PERMITTED` |
| AUTHZ-20 | The nonce is in the issued ledger and absent from the spent ledger. | `APR-E21_NONCE_REPLAY` |
| AUTHZ-21 | **One-time consumption reservation:** atomically append the consumption claim (barrier B-APPROVAL). A claim by a different run rejects; a claim by the same run is a legitimate resume. | `APR-E22_CLAIM_CONFLICT` |
| AUTHZ-22 | Durability gate: `CONTROL` is `strong`; if the destination is degraded, degraded durability must be explicitly permitted and the operation must not be a retirement. | `APR-E23_DURABILITY_NOT_PERMITTED` |
| AUTHZ-23 | The adapter capability descriptors and preservation profile match those bound at approval. | `APR-E26_CAPABILITY_DESCRIPTOR_MISMATCH` |
| AUTHZ-24 | The Journal is writable. | `APR-E24_JOURNAL_UNWRITABLE` |
| AUTHZ-25 | No client-supplied authorization, validation, or approval-state field is present in the request. | `APR-E25_CLIENT_ASSERTED_AUTHORIZATION` |

**Nothing proceeds past AUTHZ-25 without every check passing.** A pass authorizes exactly one entry, on exactly this attempt, under exactly this run.

## Invalidation triggers

Each emits an `approval_invalidated` record and causes AUTHZ-05 to reject thereafter.

| Code | Trigger |
| --- | --- |
| IT-01 | Plan content changed, re-versioned, or superseded |
| IT-02 | Evidence bundle regenerated or edited |
| IT-03 | Rule set activated, disabled, superseded, or edited |
| IT-04 | Taxonomy node approved, deprecated, retired, or path template changed |
| IT-05 | Source drift on any in-scope entry |
| IT-06 | Destination state change creating a new collision or protected-vault conflict |
| IT-07 | Approved-root set changed |
| IT-08 | Mode configuration changed |
| IT-09 | Operator revocation |
| IT-10 | Expiry reached |
| IT-11 | Adapter durability class downgraded on the control or any in-scope destination volume |
| IT-12 | Restart reconciliation returned `INCONSISTENT` |
| IT-13 | The approver's authority classes changed or were revoked |
| IT-14 | The authentication session was revoked or superseded |
| IT-15 | Engine identity changed |
| IT-16 | Adapter capability descriptor re-measured and changed, altering the preservation profile |

## One-time consumption, resume, and anti-replay

### Two-phase consumption

1. **Claim** — appended at AUTHZ-21, **before the first intent record of the batch**. Binds approval, nonce, and run.
2. **Settle** — exactly one of: `approval_consumed` after the last entry reaches a terminal outcome, or `approval_consumption_released` if the batch ended with **zero** intent records under the claim.

### Resume versus replay

For a claim with no settlement record, at restart:

| Condition | Verdict | Action |
| --- | --- | --- |
| Zero intent records exist under the claim | **Never used** | Auto-release. The approval returns to granted and may be claimed by a new run. |
| At least one intent exists and the resuming run id **equals** the claim's run id | **Resume** | Permitted. The same authorization continues the same batch. All checks re-run per entry. |
| At least one intent exists and the resuming run id **differs** | **Replay attempt** | Rejected `APR-E22_CLAIM_CONFLICT`. The approval is spent; a new run requires a new approval with a new nonce. |

This gives restart safety without giving replayability.

### Anti-replay mechanics

- **Nonce ledger** in the control volume, itself journalled. A nonce moves to spent at AUTHZ-21 and is never reusable.
- **Run binding** — an approval is bound to the run that claimed it.
- **Monotonic approval sequence per subject** — a new approval for the same subject supersedes any earlier granted approval, which is auto-invalidated.
- **Approvals are never transferable.** An approval authorizes exactly one `(subject_type, subject_id, subject_version, subject_content_hash)` tuple, including between versions of the same subject. "Related subject" is not a category that exists in this model.

## Rejection reason codes

| Code | Meaning | Batch effect |
| --- | --- | --- |
| `APR-E01_MODE_MISMATCH` | Runtime mode differs from the approved mode, or the modes configuration changed | Halt run |
| `APR-E02_APPROVAL_NOT_FOUND` | No authoritative approval record | Halt run |
| `APR-E03_APPROVAL_INTEGRITY_FAILED` | Record hash or chain invalid | Halt + incident |
| `APR-E04_APPROVAL_REVOKED` | Operator revoked | Halt run |
| `APR-E05_APPROVAL_INVALIDATED` | An invalidation trigger fired | Halt run |
| `APR-E06_APPROVAL_ALREADY_CONSUMED` | Approval spent | Halt run |
| `APR-E07_APPROVAL_EXPIRED` | Outside the validity window | Halt run |
| `APR-E08_CLOCK_UNTRUSTED` | Clock regression or unanchored clock | Halt + incident |
| `APR-E09_SUBJECT_MISMATCH` | Wrong subject type or id | Halt run |
| `APR-E10_SUBJECT_VERSION_MISMATCH` | Plan version differs | Halt run |
| `APR-E11_PLAN_HASH_MISMATCH` | Plan content changed after approval | Halt + incident |
| `APR-E12_EVIDENCE_HASH_MISMATCH` | Evidence bundle changed | Halt run |
| `APR-E13_RULESET_CHANGED` | Rule-set drift | Halt run |
| `APR-E14_TAXONOMY_CHANGED` | Taxonomy drift | Halt run |
| `APR-E15_PRECONDITION_SET_CHANGED` | Plan-level source digest drift | Halt run |
| `APR-E16_SOURCE_DRIFT` | Entry-level source changed | Entry fails to unresolved; batch stops per threshold |
| `APR-E17_SCOPE_VIOLATION` | Outside approved scope or budget | Entry fails; halt if systemic |
| `APR-E18_APPROVER_NOT_AUTHORIZED` | Approver lacks the authority class | Halt run |
| `APR-E19_AUTH_CONTEXT_INVALID` | Session invalid, revoked, or remote | Halt + incident |
| `APR-E20_ACTOR_NOT_PERMITTED` | Sentinel or non-operator principal | Halt + incident |
| `APR-E21_NONCE_REPLAY` | Nonce already spent | Halt + incident |
| `APR-E22_CLAIM_CONFLICT` | Claimed by a different run | Halt run |
| `APR-E23_DURABILITY_NOT_PERMITTED` | Degraded durability not approved | Halt run |
| `APR-E24_JOURNAL_UNWRITABLE` | Journal unavailable | Halt + incident |
| `APR-E25_CLIENT_ASSERTED_AUTHORIZATION` | Client supplied an authorization field | Halt + incident |
| `APR-E26_CAPABILITY_DESCRIPTOR_MISMATCH` | Adapter capabilities differ from those bound at approval | Halt run |

## V1 operator authentication (local single-user)

The blueprint previously required no operator authentication anywhere: the Sentinel, the lowest-privilege component, was the only component required to authenticate, while the operator holding destructive authority was not. This is the minimum viable model, sized for a local single-user deployment and deliberately not a full identity system.

1. **Local-only surfaces.** Review console and CLI bind to loopback only. A non-loopback approval channel is rejected.
2. **Operator principal registry** under the control volume, defining principal id, display name, and authority classes. Changes are journalled and trigger invalidation.
3. **Approval-time re-authentication.** Granting an approval requires a fresh authentication factor presented **at the moment of approval**, not merely an open session. An auth event is journalled.
4. **Session binding.** The approval carries the session id and binding hash; a new session cannot use a prior session's approval.
5. **Backend-issued challenge.** The nonce and request id are generated by the backend, never by the client.
6. **Secrets stay out of Git.** Passphrase verifiers, never passphrases.
7. **Explicitly deferred to the Future Registry:** multi-user, roles beyond the single operator, remote approval, and mobile approval.

> This introduces an authentication requirement that V1 scope did not previously state. It is recorded as **OD-022** so the operator, not the resolution engineer, decides its final shape.

## Expiration and revocation

### Expiration

Every approval carries an expiry. Recommended defaults, operator-calibrated:

| Scope mode | Default TTL | Rationale |
| --- | --- | --- |
| `fixture` | 7 days | No real data at risk |
| `dry_run` | 7 days | No mutation |
| `pilot` | 24 hours | Copied corpus; moderate drift risk |
| `live` | 4 hours | Bounded live batch; highest source-drift risk |
| Retirement authority | 1 hour, single batch | Highest-consequence action in V1 |

An approval also expires implicitly when its batch completes, regardless of remaining time.

### Revocation

Revocation takes effect immediately under barrier B-APPROVAL. Mandatory revocation-check points in the executor loop:

- at batch start;
- at the authorization step for every entry;
- immediately before finalize for every entry;
- at every checkpoint cadence.

On revocation mid-batch, the in-flight operation is driven to a terminal outcome using the crash-state rules — never abandoned with a dangling temporary file — then the run halts and no further intent is written. **Revocation never rolls anything back on its own;** rollback is a separately approved operation.

Revocation of an already-consumed approval is permitted and recorded. It does not undo completed work, but it invalidates any resumption and is a required audit signal.

## Related documents

- `docs/02-specification/durability-and-recovery-model.md`
- `docs/02-specification/permission-model.md`
- `docs/02-specification/command-model.md`
- `docs/03-architecture/review-console-architecture.md`
- `docs/03-architecture/decisions/ADR-014-frontend-never-authorizes-mutation.md`
- `docs/03-architecture/decisions/ADR-017-approval-binding-and-consumption.md`
