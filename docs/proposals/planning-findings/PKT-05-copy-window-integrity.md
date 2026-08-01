# PKT-05 — Copy-window integrity: token gate and bundle atomicity (PF-22, PF-14)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-22 (BLOCKER), PF-14 (BLOCKER) |
| Highest severity | BLOCKER |
| Change-control batch | BATCH-05 |
| Operator decision required | **None.** Both are pure specification defects. |
| Blocked rungs | FBL-031, FBL-048, FBL-052, FBL-054, FBL-055, FBL-056, FBL-057 |
| Affected acceptance | V1-ACC-006, V1-ACC-032, V1-ACC-034, V1-ACC-036, V1-ACC-037, V1-ACC-041, V1-ACC-044, **V1-ACC-045**, PILOT-004 |
| Hard prerequisite | **PKT-03** — PF-10's `HashRecord.scope = source_recheck` and PF-23's `VerificationResult` token fields |

This is the most consequential packet in the workbench for data safety. Both findings describe a
path in which a **torn or partial destination reaches `verified` with green evidence at every
checkpoint**, after which the original is retired.

## The exact contradiction

### PF-22 — the authoritative write protocol never captures the change tokens

The requirement is stated four times:

- `file-identity-model.md:200` — CM-4: "Copies are written to a temporary destination name and
  promoted by atomic rename only after **both** destination hash equality and
  `compare(T_precopy, T_postcopy) == EQUAL`."
- `file-identity-model.md:176` — CT-5: "A copy is eligible for `verified` only if
  `compare(T_precopy, T_postcopy) == EQUAL` **in addition to** destination hash equality."
- `file-identity-model.md:174` — CT-3: tokens are captured at five journalled points, including
  `T_precopy` and `T_postcopy`.
- `file-identity-model.md:266` — STOP-5: token `CHANGED` between them → fail the entry, quarantine
  the partial destination, never mark verified.

The authoritative protocol does none of it:

- `operation-model.md:94–97` — "The authoritative, numbered write protocol … is defined in
  `durability-and-recovery-model.md`. The summary below is a reader's overview and **must not be
  implemented in place of that protocol.**"
- `durability-and-recovery-model.md:164–173` — Phase C, steps C1–C6. **No token capture.**
- `durability-and-recovery-model.md:175–181` — Phase D. D2 reads in full: "Compare verification hash
  and size to plan preconditions." **No token comparison.**
- `durability-and-recovery-model.md:183–190` — Phase E. E1 re-checks destination absence; E2
  renames. **No token gate.**
- Record types (lines 113–117) carry "observed size and hash" and a "verification outcome". **No
  token field anywhere in the registry.**

Phase A4 (line 150) does say "compare change token" — but that is the *plan precondition*
revalidation, with failure code `SOURCE_DRIFT`, against a different operand (the plan's recorded
token, not `T_precopy`), at a different point, with a different failure branch. It does not bracket
the copy.

And `SourceMutatedDuringCopy` — the journal fact CM-3 mandates — appears in **no** record registry
and **no** event vocabulary, even though `event-model.md:39–44` declares that "any name appearing in
`domain-model.md` but not below, or below but not in `domain-model.md`, is a defect." The failure
branch itself has no home.

### PF-14 — no atomic promote protocol for multi-member bundles

- `preservation-model.md:85` — A-3: "Bundle copy is **all or nothing**. Partial bundle copy fails the
  entry, and the partial destination is removed or quarantined."
- `preservation-model.md:73` — PM-4: "P27 (bundle atomicity) is enforced by the **platform**, not by
  the adapter."
- Against `durability-and-recovery-model.md:98` — `temp_path` is **one** path; line 104 — same
  filesystem "so that same-directory rename is atomic"; Phase C writes **one** temp file; Phase E
  performs **one** rename; crash rows I3–I10 speak of "temp" and "destination" in the singular
  throughout.

There is no staging-directory concept, no multi-member intent record, and no crash row for a
half-promoted bundle.

## Operational consequence if left unresolved

**PF-22.** An implementer, told in the strongest wording in the repository not to substitute
anything for the authoritative protocol, implements C1–C6, D1–D3, E1–E4 exactly — and ships a copy
engine that **promotes on destination hash equality alone**. FX-17 fails by construction, and
FBL-048's own Definition of Done ("token-gated promote proven", `build-ladder.md:1463`) is
unreachable from its cited specification.

The loss path: the source is modified during the read, so the destination holds a torn mixture of
pre- and post-modification bytes — it "describes no coherent version of the file", in CM-1's phrase.
Its hash is compared at D2 against the *plan precondition* hash. In the general case that fails, and
the entry fails for the wrong reason but with the right outcome. **But it can pass** — a
modification written and reverted inside the copy window; a modification to a region already read; a
modification to a not-yet-read region whose original content is restored before the read arrives. In
each case D2 passes, E2 promotes, the entry is `verified`. ADR-002 then defines a verified copy as
hash equality plus a passing preservation comparison; the preservation comparison compares
*properties*, not *coherence*, so it passes too. `retirement_gate.eligible` computes `true`. **The
original is retired against a torn copy.**

**PF-14.** The implementer builds the only thing the protocol supports — a loop of single-file
operations, one `operation_id` and one `op_intent` per member, each renamed into the destination
bundle directory. Then:

- **A-1 is violated by construction** — members become independently planned and outcome-recorded.
- **A crash between member 3 and member 4 leaves a structurally valid-looking directory.** On macOS
  a partial `.app`, `.rtfd`, `.photoslibrary`, or `.fcpbundle` is not visibly broken; it opens, and
  misbehaves.
- **Recovery reports `CONSISTENT`.** R10 applies the crash-state table row by row. Members 1–3 are
  terminal `committed`; member 4 is row I3. Every row resolves cleanly and R12 emits `CONSISTENT`.
  **Nothing in the reconciliation algorithm knows those four operations were one bundle.**
- `PreservationComparisonReport.identity_evidence.bundles_copied_atomically`
  (`preservation-model.md:215`) is a field with no producer, so it is omitted or computed from
  per-member success — reporting the partial bundle as atomically copied.

This is the most silent failure in the finding set: every safety mechanism reports success.

## Affected domain entities and fields

`OperationEntry` — new `precopy_change_token_ref`, `postcopy_change_token_ref`, `token_comparison`;
`verification_state` semantics tightened. `HashRecord.scope = source_recheck` (PKT-03/PF-10 —
prerequisite). `VerificationResult` token evidence (PKT-03/PF-23 — prerequisite).
`FileRecord.content_identity_state` set to `hashed_stale` on the `CHANGED` branch.
`FileRecord.entry_type = bundle` and `bundle_manifest_digest`.
`PreservationComparisonReport.identity_evidence.bundles_total`, `.bundles_copied_atomically`,
`.bundles_failed`.

## Affected events, commands, reason codes, and persistence records

**New event** `SourceMutatedDuringCopy`, added to `event-model.md` §Operation events and
correspondingly listed in `domain-model.md:831–836` — this closes the parity violation above.

**Amended record types:** `op_intent`, `op_temp_durable`, `op_verify_result` (payload additions
below).

**New record types:** `op_bundle_intent`, `op_bundle_member_durable`, `op_bundle_staging_complete`,
`op_bundle_verify_result`, `op_bundle_finalized`. `op_outcome` is reused unchanged. Barrier B-INTENT
applies to `op_bundle_intent`; B-FINAL to `op_bundle_finalized`; `op_bundle_member_durable` joins
the group-commit class alongside `op_temp_durable`.

**New reason codes:** `SOURCE_MUTATED_DURING_COPY`, `TOKEN_CAPTURE_FAILED`,
`TOKEN_INDETERMINATE_UNRESOLVED`, `PROMOTE_GATE_NOT_SATISFIED`, `RECOVERY_TOKEN_GATE_UNPROVEN`,
`BUNDLE_MANIFEST_DRIFT`, `BUNDLE_MEMBER_UNSTABLE`, `BUNDLE_ATOMICITY_UNAVAILABLE`,
`BUNDLE_DESTINATION_EXISTS`, `RECOVERY_BUNDLE_DIGEST_MISMATCH`, `BUNDLE_PROMOTE_INDETERMINATE`,
`POST_FINALIZE_BUNDLE_DRIFT`.

## Proposed normative resolution — part 1: the single-file token gate

### Phase B — capture `T_precopy` **inside** the intent record

| Step | Action | Failure branch |
| --- | --- | --- |
| **B1a** *(new, after B1, before B2)* | Capture `T_precopy` — a full `ChangeToken` over the source object — **after** Phase A4 revalidation and **before** the first source read byte. | `TOKEN_CAPTURE_FAILED` → `op_outcome = failed`. No mutation has occurred; nothing to clean. |
| **B2** *(amended)* | Append `op_intent`. Payload gains **required** `precopy_change_token`. Barrier B-INTENT. | Unchanged. |

> **Why the intent record and not memory.** Placing `T_precopy` inside `op_intent` puts it under
> barrier B-INTENT, so it survives a crash. A resumed operation at row I6, I7, or I8 compares against
> the *original* `T_precopy` rather than a fresh capture. Were it re-captured, a modification during
> the crash window — possibly hours — would be invisible: the fresh `T_precopy'` and `T_postcopy`
> would both reflect the post-modification state and compare `EQUAL`. This placement is what makes
> resume safe, and the amended text should say so.

### Phase C — capture `T_postcopy` with the temp-durable fact

| Step | Action | Failure branch |
| --- | --- | --- |
| **C5a** *(new, after the C5 parent fsync, before C6)* | Capture `T_postcopy` over the source object. | `TOKEN_CAPTURE_FAILED` → `op_outcome = failed`; the temp is attributable and handled by the orphan policy. |
| **C6** *(amended)* | Append `op_temp_durable`. Payload gains **required** `postcopy_change_token` and `token_comparison ∈ {EQUAL, CHANGED, INDETERMINATE}`. | HALT `JOURNAL_APPEND_FAILED`. |

### Phase D — evaluate, with an exhaustive branch per outcome

| Step | Action |
| --- | --- |
| **D2a** *(new, after D2, before D3)* | Evaluate `compare(T_precopy, T_postcopy)`. Three outcomes, below. |
| **D3** *(amended)* | Append `op_verify_result`. Payload gains **required** `precopy_change_token_ref`, `postcopy_change_token`, `token_comparison`, `token_resolution ∈ {not_required, rehash_confirmed, rehash_failed}`, and nullable `source_recheck_hash_record_id`. |

| Outcome | Mandated behaviour |
| --- | --- |
| **`EQUAL`** | Proceed to D3 with `token_resolution = not_required`. |
| **`CHANGED`** | Append `op_verify_result` recording `CHANGED`, then `op_outcome = failed` with `SOURCE_MUTATED_DURING_COPY`. Emit the `SourceMutatedDuringCopy` event. **Quarantine the temp — never promote it, never permanently delete it** (V1 has no permanent deletion). Set the entry `failed`; set `FileRecord.content_identity_state = hashed_stale`; invalidate the approval for that entry. **The entry never reaches `verified` even though D2 passed** — and record that D2 passed, so the evidence shows the failure came from the token gate, not a hash mismatch. |
| **`INDETERMINATE`** | **Never treated as `EQUAL`** — no threshold, no flag, no configuration (CT-1). Resolve per CT-2: a full source re-read producing a `HashRecord` with `scope = source_recheck`, plus a fresh `T_postcopy'`. Proceed with `token_resolution = rehash_confirmed` **only if** the re-hash digest equals the precondition digest **and** `compare(T_precopy, T_postcopy') == EQUAL`. Otherwise treat exactly as `CHANGED`, with `rehash_failed`. If the re-hash is itself `unstable`, treat as `CHANGED`. Attempts are bounded by `identity.max_hash_restabilize_attempts`; exhaustion is `CHANGED` with `TOKEN_INDETERMINATE_UNRESOLVED`. |

### Phase E — gate the promote on the durable record, not on control flow

| Step | Action | Failure branch |
| --- | --- | --- |
| E1 | Unchanged — re-check `destination_path` absent. | `LATE_COLLISION`. |
| **E1a** *(new)* | Re-assert **from the durable `op_verify_result` for this `(operation_id, attempt_seq)`** that `token_comparison == EQUAL`, or `token_resolution == rehash_confirmed`. If no such record is durable, or it does not satisfy the gate, **do not rename**. | `PROMOTE_GATE_NOT_SATISFIED` → `op_outcome = failed`; quarantine the temp. |
| E2–E4 | Unchanged. | Unchanged. |

> **Why E1a is not redundant with D2a.** D2a is the *evaluation*; E1a is the *gate*. Separating them
> makes CM-4 structurally enforced rather than dependent on the executor's control flow reaching E2
> only along a path that passed D2a. It is also what makes the resumed path safe: row I8 instructs
> recovery to "re-run the E1 collision guard, then E2–E4" — E1a puts the token gate inside that
> re-run, sourced from the durable record rather than from process memory that no longer exists.

### Amendments to the existing crash-state table

- **I6** — append: "The `precopy_change_token` recorded in `op_intent` is the governing token. Do not
  re-capture it on resume."
- **I8** — append: "Re-run the E1 collision guard **and E1a**. If the durable `op_verify_result` does
  not satisfy the token gate, the temp is not promotable regardless of its verified bytes."
- **I9 branch (a)** — amend from "destination exists and re-read hash matches → adopt" to:
  "destination exists, re-read hash matches, **and the durable `op_verify_result` satisfies the token
  gate** → adopt. Destination exists and hash matches but the operation has no durable verify record
  satisfying the gate → quarantine, HALT `RECOVERY_TOKEN_GATE_UNPROVEN`." **This sub-branch is new
  and load-bearing:** without it, recovery adopts a destination the forward path would have refused,
  and the token gate is bypassable by crashing at the right moment.

`operation-model.md:119` already reads "the source change token was equal immediately before and
immediately after the copy" — it is *correct*, and is precisely the half the durability model omits.
The two documents agree in intent; only the authoritative one is defective, so the fix is additive
to one document rather than a reconciliation of two.

## Proposed normative resolution — part 2: bundle atomic promote

**Design principle:** a bundle's temporary artifact is a *directory*, and the single atomic act
remains exactly one same-parent `rename(2)`. This preserves the existing protocol's one-primitive
property rather than introducing a second atomicity mechanism.

```
bundle_staging_path = <dest_parent>/.nasip-tmp/<operation_id>.<attempt_seq>.partdir
```

`<dest_parent>` is the parent of `destination_path`, so the promote is a same-directory rename of a
directory, and every temp artifact remains attributable to one operation and attempt by filename
alone.

**Phase BA — preconditions** (no durable writes, no mutation). A1–A7 unchanged, plus: **BA1**
re-enumerate members and recompute the manifest digest (canonical ordering of member relative raw
path, size, content hash — A-2), compare to the plan precondition → `BUNDLE_MANIFEST_DRIFT`. **BA2**
confirm every member's `HashRecord` is consumable → `BUNDLE_MEMBER_UNSTABLE`. **BA3** confirm the
destination volume's `atomic_same_dir_rename` is verified `true` and `durability_class` is `strong`
→ `BUNDLE_ATOMICITY_UNAVAILABLE`. **No degraded mode.** **BA4** confirm `destination_path` absent — a
bundle is never merged into an existing directory → `BUNDLE_DESTINATION_EXISTS`.

**Phase BB — intent.** **BB1** compute ids and staging path; capture `T_precopy` over the bundle
root. **BB2** append `op_bundle_intent` carrying `operation_id`, `bundle_staging_path`,
`destination_path`, `manifest_digest`, `member_count`, `precopy_change_token`, and the **ordered
member list** — per member: relative raw path, size, expected content hash, and `member_kind ∈
{file, directory, symlink, hardlink_member}`. Barrier B-INTENT. Gate G applies unchanged.

**Phase BC — staging write.** **BC1** exclusive-create the staging directory; fsync its parent; an
existing one is a prior attempt's orphan — never reuse, increment `attempt_seq`. **BC2** write each
member in intent order per Phase C semantics; symlink and hard-link members follow PKT-04's entry-type
semantics and write no content stream. **BC3** append `op_bundle_member_durable` per member (group
commit permitted). **BC4** fsync every directory in the staging tree bottom-up. **BC5** append
`op_bundle_staging_complete` with the observed member count and staging-tree manifest digest.

**Phase BD — verify.** **BD1** independently re-walk the whole staging tree, recomputing every member
hash and the manifest digest. **BD2** compare digest, member count, **and the exact set of member
relative paths — no extra, no missing**. **BD3** capture `T_postcopy` over the source bundle root and
evaluate it per D2a above, including the `INDETERMINATE` re-hash applied to the manifest digest.
**BD4** append `op_bundle_verify_result` with both tokens, the comparison, and the recomputed digest.

**Phase BE — atomic promote.** **BE1** re-check `destination_path` absent → `LATE_COLLISION`; never
merge. **BE2** re-assert the gate from the durable `op_bundle_verify_result` →
`PROMOTE_GATE_NOT_SATISFIED`. **BE3** `rename(bundle_staging_path, destination_path)` — **one atomic
same-parent directory rename**. **BE4** fsync the destination parent. **BE5** append
`op_bundle_finalized`; barrier B-FINAL.

**Phase BF — outcome.** `op_outcome = committed`, barrier B-OUTCOME, then projection.

### Bundle rules

| ID | Rule |
| --- | --- |
| BR-1 | A bundle has exactly one `operation_id`, one intent record, one finalize record, and one outcome record. Members are never independently planned, approved, or outcome-recorded (A-1). A plan containing an `OperationEntry` whose `file_record_id` is a bundle member is rejected at lock. |
| BR-2 | The staging directory root is the only object renamed. Per-member renames into a live destination are prohibited. |
| BR-3 | **If `atomic_same_dir_rename` is not verified true, or `durability_class` is `weak` or `unknown`, bundle operations are blocked — not degraded.** PM-4 makes the platform responsible for atomicity and the platform's only atomicity primitive is directory rename. Degraded mode's mandatory post-finalize re-read does not restore atomicity; it only detects its absence afterwards. |
| BR-4 | A staging directory whose intent is non-terminal is an **attributable partial**; whose intent is terminal, an **attributable orphan**; with no intent naming it, `UNATTRIBUTABLE_ARTIFACT` → HALT. This extends the orphan table to directory artifacts, which it currently does not cover. |
| BR-5 | A partial staging tree is quarantined **as one unit**. Individual members are never adopted from it, and it is never permanently deleted. |

### Proposed crash-state rows I17–I24

Numbered from I17 so I0–I16 are not renumbered — renumbering would invalidate V1-ACC-045's existing
evidence artifact.

| # | Interruption point | Journal state | Interpretation | Required recovery | Next mutation? |
| --- | --- | --- | --- | --- | --- |
| I17 | During BA, before BB2 | No bundle intent | Nothing was attempted. | None. Re-evaluate approval; re-run BA. | Yes, after reconciliation |
| I18 | B-INTENT complete, before BC1 | Intent only | Intent declared, nothing done. | Confirm staging and destination absent. Append `abandoned`. | Yes, after reconciliation |
| I19 | During BC2 | Intent + 0..k member records | Partial staging tree, attributable. Destination untouched. | Verify destination absent. **Quarantine the entire tree as one unit; never adopt individual members.** Append abandoned. | Yes, after reconciliation |
| I20 | BC2/BC3 done, BC5 not durable | Intent + member records | Bytes may be good but tree completeness is unproven. Per-member records do not vouch for directory-entry durability across the tree; only `op_bundle_staging_complete` does. | Do not adopt. Quarantine as one unit; retry at a new attempt. | Yes, after reconciliation |
| I21 | BC5 durable, before BD1 | + staging-complete | Tree durable and attributable; verification outstanding. | Resume at BD1 against the existing tree. | Yes, after reconciliation |
| I22 | BD1–BD3 done, BD4 not durable | No verify record | An unrecorded verification did not happen. | Re-verify idempotently using the **intent's** `precopy_change_token`, not a fresh capture. Continue at BE1. | Yes, after reconciliation |
| I23 | Rename issued, through BE4, before BE5 | No finalize record | **The most dangerous bundle window.** Promote indeterminate; the journal claims no success. Deliberately folds BE3/BE4, matching the model's own reasoning at I9/I10. | Probe both paths. **(a)** destination exists and a full re-walk reproduces the intent's digest, member count and path set → adopt; append finalize + committed. **(b)** destination exists but any of the three differs → quarantine the destination tree **intact**; HALT `RECOVERY_BUNDLE_DIGEST_MISMATCH`. **(c)** destination absent, staging verified → resume at BE1. **(d)** both absent → abandon; retry at a new attempt. **(e)** **both present** → HALT `BUNDLE_PROMOTE_INDETERMINATE`; quarantine neither, delete neither, touch neither. | (a),(c),(d) yes; **(b),(e) no** until the operator clears |
| I24 | B-FINAL complete, outcome not durable | Finalize present | Promote durably claimed; disposition unrecorded. | Re-walk the destination; recompute the digest; append committed. Mismatch → HALT `POST_FINALIZE_BUNDLE_DRIFT`. | Yes, after reconciliation |

**Branch (e) has no single-file analogue.** For a single file, exclusive create plus rename makes
"both paths present" impossible. A directory rename that partially fails on a filesystem without true
atomic directory rename **can** leave both. That branch is precisely why BR-3 blocks bundles on weak
adapters rather than degrading them — it is the justification for the harshest rule in this proposal
and should be recorded as such.

## Alternatives considered

**PF-22 — capture both tokens but compare only at verification time, leaving the promote gated on
hash alone.** Rejected: CM-4 is explicit that *promotion* is gated. A promoted-then-failed artifact
is a live object at the final destination path that a concurrent reader, a backup job, or the
operator can consume before the failure is recorded. The entire purpose of temp-then-rename is that
nothing appears at the destination path until fully qualified.

**PF-22 — treat `INDETERMINATE` as grounds to re-copy.** Rejected: on any adapter whose
`mtime_resolution_ns` exceeds one millisecond — which is every non-local adapter, per AE-4 and the
network-limitations section — `INDETERMINATE` is the *common* case. Unbounded re-copy would livelock
the batch. CT-2 already prescribes a bounded re-hash producing an auditable `source_recheck` record.

**PF-14 — copy members into the final destination and mark completion with a sentinel file.**
Rejected: it makes the *absence of a marker* the only signal of a partial bundle, so the operating
system, Finder, the user, and any backup tool all see a mountable partial bundle. And it delegates
atomicity to a convention, which is what PM-4 forbids.

**PF-14 — stage, then rename members one-by-one into a pre-created destination directory.** Rejected:
N renames are N atomic acts, not one. The crash window merely moves from the copy phase to the
promote phase — and now with a *destination-resident* partial rather than a staging-resident one,
which is strictly worse.

**PF-14 — copy the bundle as a single archive stream and expand at the destination.** Rejected:
expansion is itself multi-step and non-atomic, and the archive format would have to preserve xattrs,
resource forks, ACLs, and internal symlinks losslessly — reintroducing every preservation property
as an archive-format capability question on top of the adapter capability questions the descriptor
model already answers.

## Safety implications

**Copy-before-delete** — the invariant most directly at risk in both findings: a torn copy, or a
partial bundle, reaching `verified` unlocks retirement of the original. **Retirement gating** — CT-5
makes token equality a precondition of `verified`; and `bundles_copied_atomically` must equal
`bundles_total` or `retirement_gate.eligible` is false, a rule that needs stating since that field
currently has no producer and no consumer. **No-permanent-deletion** — rows I19, I20, and I23(b)
quarantine trees, never delete them; BR-5 makes the unit explicit. **Read-only inventory** — the
`INDETERMINATE` re-hash performs an additional full source read whose access-time side effect must
be counted per CM-6 and disclosed, not treated as free. **Protected-vault** — BA4 and BE1 apply
ADR-011's pre-finalize existence check to a *directory* destination, which ADR-011 does not currently
contemplate.

## Migration and compatibility implications

Three record payload schemas change and five are added → `schema_version` bump. Only G3 fixture
journals exist, so the practical cost is nil, but the reader rule must be specified: **a pre-change
record lacking the token fields is read as `token_comparison: unavailable`, which is not
promotable.** Old records stay readable for audit; they cannot authorise a resumed promote. Stating
this explicitly is what prevents a lenient reader from treating a missing field as satisfied — the
same failure mode as treating `INDETERMINATE` as `EQUAL`.

**V1-ACC-045's evidence artifact grows**: the crash-recovery matrix goes from 17 rows to 25, and the
fault-injection fixture set must grow correspondingly. No existing row changes semantics.

## Required tests

**New fixture capability, required.** `tests/fixtures/README.md:63` lists six injection modes —
`fail_call`, `partial_write(n)`, `succeed_then_kill`, `fsync_error_once`, `lose_unflushed_data`,
`rename_indeterminate` — **none of which mutates the source**. Add `mutate_source_during_read(offset)`;
without it FX-17 cannot be driven at the adapter level. Add directory-level injection —
`partial_write` inside a staging tree and `rename_indeterminate` on a *directory* rename.

**Positive** — a clean copy: `op_intent.precopy_change_token` present; `op_temp_durable.
token_comparison == EQUAL`; `op_verify_result` carries both refs; promote occurs; entry `verified`.
FX-10: the bundle promotes via exactly one directory rename; assert exactly one `op_bundle_intent`,
one `op_bundle_finalized`, one `op_outcome`, and **zero** `op_intent` records for any member.

**Negative — FX-17, the decisive test.** Source mutated during copy → entry fails; temp quarantined,
not deleted; `SourceMutatedDuringCopy` emitted; destination never created. **And assert that D2
passed** — that the destination hash equals the precondition hash — proving the failure came from the
token gate and not incidentally from a hash mismatch. A test in which D2 also fails does not prove
the gate exists.

**Negative** — FX-20 on a coarse-mtime adapter: `INDETERMINATE` → a `source_recheck` `HashRecord`
exists → promote proceeds **only** with `rehash_confirmed`. An entry promoted on `INDETERMINATE`
without that record fails. No configuration value causes `INDETERMINATE` to satisfy E1a — enumerate
the config surface exhaustively. FX-21 and FX-22 still fail at D2 with the token gate `EQUAL`,
proving the two gates are independent and that adding one did not mask the other. FX-11: only the
outermost bundle is operable; a plan naming the inner bundle or any member is rejected at lock. A
single member's digest substituted for the manifest digest fails. BA3 on a `weak` destination: assert
**no degraded-mode path exists** by attempting to enable degraded mode and confirming bundles remain
blocked. BA4/BE1: an existing directory at `destination_path` is never merged into.

**Failure-injection** — kill after C6 before D3 (I7): resume must reuse the intent's `T_precopy`;
assert a fresh capture is *not* performed, and inject a source mutation during the crash window,
asserting it is still detected. Kill after E2 before E4 (I9) on an operation whose verify record does
not satisfy the gate: recovery must HALT `RECOVERY_TOKEN_GATE_UNPROVEN`, never adopt on hash match
alone. `mutate_source_during_read` at the beginning, the middle, and after the final byte read but
before C5a. Process kill at each of I17–I24 with the directory-aware adapter, with a **global
assertion across all eight: no destination bundle ever exists in a state whose manifest digest
differs from the intent's.**

## Required documentation changes

`durability-and-recovery-model.md` — Phases B, C, D, E amendments; Phases BA–BF; the record-type
registry; crash rows I6, I8, I9 amended and I17–I24 added; the orphan-artifact table extended to
directories. `event-model.md` and `domain-model.md` — `SourceMutatedDuringCopy`.
`tests/fixtures/README.md` — the new injection modes.

## Required ADR changes

**ADR-002** — amend: "A verified copy means destination content hash equality, **source change-token
equality across the copy window**, and a passing preservation comparison. Any one of the three alone
is insufficient, and a destination is promoted from its temporary name only after all three are
satisfied and durably recorded. Bundle atomicity is a platform guarantee, delivered by writing the
whole bundle into a staging directory on the destination filesystem and promoting it with a single
directory rename. A destination volume that cannot perform an atomic same-directory rename may not
receive bundle operations at all; there is no degraded-mode substitute."

**ADR-004** — amend: "Hash equality is evaluated inside a change-token bracket. A destination hash
that matches a source which changed during the copy is not verification evidence: the destination
describes no coherent version of the source."

**ADR-011** — append: "The pre-finalize existence check applies to directory destinations as well as
file destinations. A bundle is never merged into an existing directory at the destination path; an
existing directory is a collision, not a container."

**ADR-016** — note that the amended and new record types are journal-authoritative, that their token
fields are required rather than optional, and that a record lacking them cannot authorise a promote.

## Operator policy, or pure specification defect?

**Pure specification defects. No operator policy is required, and Claude proposes none.** BR-3 does
have an operational consequence — if the adapter chosen under OD-016 cannot perform an atomic
directory rename, bundles are out of scope for that adapter — but that is a *derived consequence of a
measured descriptor*, exactly the mechanism the capability model exists to provide, not a new
decision to register.

## Atomicity

**PF-22 and PF-14 must land together, and this is the point most at risk of being missed.** A
bundle's members are read over an extended window and can be mutated mid-read exactly as a single
file can; BD3 is the bundle's analogue of the single-file token gate. **If they are resolved in
separate change-control cycles, the bundle path will ship without the token gate** — reproducing
PF-22's defect in the newer protocol, in a code path with no fixture yet written to catch it. They
also amend the same crash-state table and the same record registry and both change `op_*` payload
schemas, so one `schema_version` bump serves both.

**PKT-03 is a hard prerequisite.** PF-22's `INDETERMINATE` branch names `HashRecord.scope =
source_recheck`, which does not exist until PF-10 closes; and the gate's outcome has no home in the
domain model until PF-23 extends `VerificationResult`. Resolving this packet first produces a gate
whose result is journalled but not projected. **PKT-04** is also required for bundles containing
internal symlinks (A-5).

## Verification procedure

Re-run `foundation_self_review.py` and `validate_build_ladder.py`. Independently: grep
`durability-and-recovery-model.md` for `precopy_change_token` and confirm it appears in the
`op_intent` payload description, in Phase B, and in the I6/I8 recovery text; count the crash-state
table rows and confirm 25; confirm `SourceMutatedDuringCopy` appears in both `event-model.md` and
`domain-model.md`, satisfying the parity rule.

## Change-control authority

Change control per `docs/05-governance/change-control.md`. No operator decision is required.
**This packet is non-authoritative and confers no authority of its own.**
