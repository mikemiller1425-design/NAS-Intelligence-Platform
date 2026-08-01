# Review Console Architecture

## Purpose

The review console is a **non-executing decision surface**. It presents evidence, explains proposals, and captures operator decision intent. It never executes or authorizes filesystem work.

### Why "non-executing decision surface" and not "read-only approval console"

The earlier phrase "read-only approval console" was misleading in two directions at once (audit finding FND-m002):

- It implied the console is read-only in *all* respects. It is not — it legitimately writes **application state** such as review items, decisions, and approval-intent records.
- It implied the console *performs* approval. It does not — it captures an operator's expressed intent. Whether that intent authorizes any execution is decided exclusively by the trusted backend.

The accurate statement is:

> The review console is **read-only toward underlying file data** and **write-capable toward a bounded set of application state**. It is **non-executing**: no console action, alone, causes a filesystem mutation.

## Trust boundary

| Layer | Responsibility |
| --- | --- |
| Console (frontend) | Render evidence. Capture operator intent. Submit bounded application-state commands. |
| Backend (trusted) | Authenticate the operator, bind the approval, validate it against the immutable plan and evidence hashes, evaluate authorization, and only then permit execution. |

The backend never treats a console-submitted field as proof of authorization. See `docs/02-specification/approval-binding-model.md` and `ADR-014`.

## Commands the console MAY submit

These change **application state only**. None of them mutates file data.

| Command | Effect |
| --- | --- |
| `open_review_item` | Create a review work item. |
| `assign_review_item` | Assign a review item to an operator. |
| `resolve_review_item` | Record a review outcome. |
| `close_review_item` | Close a resolved review item. |
| `request_review` | Route a classification decision to manual review. |
| `approve_decision` | Record operator acceptance of a **classification** decision. Does not plan or execute anything. |
| `reject_decision` | Record operator rejection of a classification decision. |
| `request_approval` | Ask the backend to mint an approval request for a named subject. |
| `grant_approval` | Submit approval **intent**. The backend mints, binds, and validates the approval record; the console never constructs one. |
| `revoke_approval` | Submit revocation intent for a previously granted approval. |
| `propose_taxonomy_node` | Propose a taxonomy node for operator review. |
| `acknowledge_alert` | Acknowledge an alert. |
| `resolve_alert` | Mark an alert resolved. |

## Commands the console MUST NOT submit

The console has no path — direct or indirect — to any of these:

- `execute_operation_entry`, `queue_operation_entry`, `verify_operation_entry`, `close_operation_entry`
- `approve_operation_plan`, `lock_operation_plan`, `supersede_operation_plan`
- `start_batch`, `pause_batch`, `resume_batch`, `complete_batch`
- `write_checkpoint`, `seal_checkpoint`, `invalidate_checkpoint`
- `append_journal_entry`, `seal_journal`, `replay_journal`
- `confirm_source_root`, `start_scan`, `pause_scan`, `resume_scan`, `complete_scan`
- `approve_rule_set`, `activate_rule_set`, `disable_rule_set`
- any command that would copy, move, rename, quarantine, retire, overwrite, or delete a file

Attempting any of these from the console is a rejected request and a recorded safety event, not a permission error to be relaxed.

## Read-only toward file data

The console:

- never opens, reads, writes, or streams source or destination file bytes for the purpose of mutation;
- may display derived evidence (hashes, extracted metadata, thumbnails where privacy policy permits) produced by the backend;
- may not present any control that implies direct file manipulation.

## Core responsibilities

- Display inventory evidence and classification rationale.
- Show proposed operations with clear risk labeling.
- Present duplicate and conflict findings.
- Capture operator approval, rejection, or request-for-review intent.
- Link each decision to immutable audit records.

## Interaction model

The console emphasizes explainability, not speed. An operator must be able to inspect why a proposal exists, what evidence supports it, what safeguards are active, and what happens if they express approval.

Approval-intent capture must show the operator the exact bound subject — plan ID, plan version, plan content hash, and evidence-bundle hash — that their intent will be tied to. If any of those change, the previously captured intent is invalidated by the backend and must be re-expressed.

## Related documents

- `docs/02-specification/approval-binding-model.md`
- `docs/02-specification/command-model.md`
- `docs/02-specification/permission-model.md`
- `docs/03-architecture/decisions/ADR-014-frontend-never-authorizes-mutation.md`
- `docs/03-architecture/decisions/ADR-015-proposal-vs-execution-separation.md`
