# PKT-04 — Link and content-class operation semantics (PF-08, PF-26)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-08 (MAJOR), PF-26 (MINOR) |
| Highest severity | MAJOR |
| Change-control batch | BATCH-04 |
| Operator decision required | **OD-024** — link reproduction scope. It decides **one value**; everything else here proceeds without it. |
| Blocked rungs | FBL-029, FBL-031, FBL-049 |
| Affected acceptance | V1-ACC-005, V1-ACC-041, V1-ACC-044, V1-ACC-053 |
| Depends on | **PKT-03** — `HardLinkSet` (PF-07) and the `bundle` enum value (PF-27) must exist first |

## Relationship to PKT-03

PKT-03 is the *contracts* commit: it defines the `HardLinkSet` entity, the `entry_type` enum
widening, and the `HashRecord` / `SourceRoot` field extensions. This packet is the *behavioural*
half — what an operation may legally do with those entities. The split is deliberate: PKT-03 must
land before FBL-003 freezes the contracts package, whereas this packet's content lands with the
planner and executor rungs. Resolving this packet without PKT-03 produces entry types that
reference entities which do not exist.

## The exact contradiction

**PF-08 — no operation entry type can express a symlink or a hard-link member.**

- `domain-model.md:792` and `operation-model.md:21–25` — `entry_type` is `copy`, `move`, `rename`,
  `quarantine`, `skip`. Five values.
- `file-identity-model.md:236` — SL-3: "Operation entry types **must include** `recreate_symlink`,
  or symlink handling must be explicitly declared out of scope with a stop condition." Neither has
  happened.
- `preservation-model.md:111` — D-2: "Where the destination supports links, the platform copies the
  first member and links the remainder." No entry type expresses "link the remainder."
- `preservation-model.md:93–94` — B-1 promotes P18 and P19 to `required` on **all** adapters; B-2:
  "Silently replacing a symlink with a copy of its target is **prohibited**. This is not a
  best-effort degradation; it is data-model corruption."
- The fixtures already assert the missing behaviour: `tests/fixtures/README.md:31,33,35` — FX-04
  "links preserved where supported", FX-06 "recreated as a link where supported", FX-08 "recreated
  as a dangling link, not resolved".

**PF-26 — the shipped example config contradicts the overlays.**

- `config/exclusions/exclusions.example.yaml:41` — `symlink_policy: skip_and_record`. B-1 makes
  skipping the capability-conditional *fallback*; this makes it the unconditional *policy*. And a
  key named `skip` reads as excluding symlinks from inventory, which SL-1 forbids outright.
- `config/exclusions/exclusions.example.yaml:42` — `package_bundle_policy:
  treat_as_directory_with_bundle_flag`. Against A-1 (`preservation-model.md:83`): "The bundle is the
  unit of classification, planning, approval, copy, verification, and retirement. Members are never
  independently classified, planned, or copied." Treating a bundle as a directory *is* the shredding
  A-1 forbids — a directory is traversed, and its children become independent `FileRecord`s.

## Operational consequence if left unresolved

**PF-08.** With only five entry types a planner meeting a symlink has two options and both are
wrong.

*Emit `copy`.* Phase C3 (`durability-and-recovery-model.md:170`) streams "source bytes" — for a
symlink opened without `O_NOFOLLOW` those are the *referent's* bytes. That is B-2's data-model
corruption: it can duplicate arbitrary volumes (a link to a 400 GB tree), breaks every relative-path
assumption inside the copied tree, and violates SL-2.

*Emit `skip`.* `operation-model.md:33` defines `skip` as "records a deliberate non-action" — a
**successful** terminal disposition. FX-06 and FX-08 fail; P18/P19 go unmet; and decisively, because
`skip` is not a failure, the retirement-gate computation (`preservation-model.md:239`, CR-2 keys on
*mismatch and unverifiable* counts) sees no mismatch and can return `eligible = true`.

The same applies to hard-link sets: D-2's copy-first-then-link has no entry type, so a three-member
set becomes three `copy` entries — HL-4's silent N-fold multiplication, blessed by three
individually-passing hash verifications.

**Loss path:** originals retired after their links were either replaced by full copies of their
referents or dropped entirely, with a green preservation report at every checkpoint.

**PF-26.** `config/exclusions/exclusions.example.yaml` is the **only concrete config shape an
implementer has** — `config/schemas/` contains exactly one schema, and it is the rule-set schema,
not this one. So there is no validator to reject these values. `treat_as_directory_with_bundle_flag`
makes FX-10 fail at FBL-031 while the config appears to be doing exactly what it says.
`symlink_policy: skip_and_record` makes FX-06 and FX-08 unimplementable while reading as a
deliberate conservative safety choice — the worst kind of wrong default, because it looks careful.

**PF-26 and PF-27 converge independently on the same wrong implementation** — bundle-as-flagged-
directory. Fixing either alone leaves the other's path to that defect open.

## Affected domain entities and fields

`OperationEntry.entry_type`; new `OperationEntry.link_target_raw` (byte string, required when
`entry_type = recreate_symlink`), `OperationEntry.hardlink_set_id` (ref, required when `entry_type =
link_hardlink_member`), `OperationEntry.hardlink_primary_entry_id` (ref, same condition).
`FileRecord.symlink_target_raw` (inventory field 24), `FileRecord.entry_type`, `HardLinkSet.id`.

## Affected events, commands, reason codes, and persistence records

Existing `OperationEntryQueued / Executing / Verified / Failed` (`event-model.md:142–145`) are reused
unchanged. The `op_intent` payload (`durability-and-recovery-model.md:113`) gains required
`entry_type` and conditionally-required `link_target_raw` / `hardlink_set_id`.

New reason codes: `LINK_RECREATE_UNSUPPORTED`, `LINK_TARGET_BYTES_MISMATCH`,
`HARDLINK_PRIMARY_NOT_COMMITTED`, `SYMLINK_TARGET_ESCAPES_ROOT` (the carrier for STOP-14,
`file-identity-model.md:275`, severity fatal), `LINK_REPRODUCTION_OUT_OF_SCOPE`,
`VAL-BUNDLE-POLICY-INVALID`, `VAL-SYMLINK-POLICY-INVALID`, `VAL-SYMLINK-OP-POLICY-INVALID`.

## Proposed normative resolution

### (a) Extend the entry-type enum to seven values

| Value | Semantics |
| --- | --- |
| `copy` | Unchanged. Content-stream reproduction of a `file` or `bundle` entry. |
| `move` | Unchanged. Permitted only when the approved phase authorises source removal. |
| `rename` | Unchanged. |
| `quarantine` | Unchanged. |
| `skip` | Unchanged **and narrowed**: not a legal disposition for an entry whose `FileRecord.entry_type` is `symlink`, or whose `hardlink_set_id` is non-null. See LR-3. |
| `recreate_symlink` | Create at `destination_path` a symbolic link whose target string is **byte-identical** to `link_target_raw`. The referent is never opened, read, hashed, stat-ed for size, or followed. Verification is byte-equality of the destination's readback target string — **not** a content hash. A dangling target is reproduced as dangling and is not an error. |
| `link_hardlink_member` | Create at `destination_path` an additional filesystem name for the object already committed at `hardlink_primary_entry_id`'s `destination_path`. Legal only when that primary has a durable `op_outcome = committed`; otherwise `HARDLINK_PRIMARY_NOT_COMMITTED`. No bytes are read or written. Verification is that both names share one destination object identity **and** that destination link count equals `HardLinkSet.declared_link_count` (D-2). |

### (b) Add the policy switch

A run-scoped configuration key, frozen into the plan at approval alongside the preservation profile:

```
link_reproduction_mode : reproduce | out_of_scope     # required, no default at plan time
```

- **`reproduce`** — the two new entry types are legal. A destination whose measured descriptor
  reports P18/P19 write support absent, or P17 unsupported, blocks the affected entries at plan time
  as MM-2 (`preservation-model.md:169`) with `LINK_RECREATE_UNSUPPORTED`.
- **`out_of_scope`** — the planner emits **no** entry for a symlink or hard-link-set member. Each
  such `FileRecord` is placed in `unresolved` with reason `LINK_REPRODUCTION_OUT_OF_SCOPE`, counted
  per batch, and surfaced at the retirement gate. This is the "explicit out-of-scope declaration
  with a stop condition" that SL-3 demands as its alternative.

### (c) Add four rules

| ID | Rule |
| --- | --- |
| LR-1 | An entry whose `FileRecord.entry_type = symlink` may carry only `recreate_symlink` or `quarantine` under `reproduce`, and no entry at all under `out_of_scope`. `copy` on a symlink is rejected at plan lock. |
| LR-2 | A symlink whose resolved target escapes an approved root is a **fatal** stop under either mode: `SYMLINK_TARGET_ESCAPES_ROOT` (STOP-14). This is the definition of "specifically and safely handled" that `permission-model.md:112` currently defers. |
| LR-3 | `skip` is never a legal disposition for a link entry under either mode. A skipped link is a *silent* non-reproduction; the required disposition is `blocked` or `unresolved`, both of which are non-zero retirement-gate blocking conditions. |
| LR-4 | Under either mode, a non-zero count of blocked or unresolved link entries sets `PreservationComparisonReport.retirement_gate.eligible = false` and appears in `blocking_conditions[]`. Clearing it requires a scoped waiver naming P17, P18, or P19 specifically; a blanket waiver is invalid (CM-P1, `preservation-model.md:177`). |

### (d) Correct the example config

Replace `config/exclusions/exclusions.example.yaml:41–44` with:

```yaml
# Content-class policy is pinned by the preservation-model overlays and is NOT
# adapter-configurable. Each key below has exactly one legal V1 value, except
# symlink_operation_policy, whose value is set by OD-024. A loader MUST reject
# any other value rather than falling back to a default.

symlink_inventory_policy: inventory_never_follow      # only legal V1 value (SL-1, SL-2)
symlink_operation_policy: blocked                     # blocked | recreate_as_link
                                                      # set by OD-024; `skip` is NOT legal (LR-3)
package_bundle_policy: single_logical_file_bundle     # only legal V1 value (A-1)
bundle_member_representation: full                    # `minimal` is prohibited (A-4)
hidden_files_policy: inventory_and_flag               # unchanged — consistent
permission_error_policy: record_unresolved_do_not_fail_silently   # unchanged
```

Bump `version` from `1.0.0-example` to `1.1.0-example`; `status: non_production_example` stays. The
rest of the file needs no change: `protected_destinations` is consistent with ADR-011, and the
exclusion patterns are consistent with P29.

**Additionally propose** that `config/schemas/exclusions.schema.json` be authored as a rung
deliverable. Pinning values in a comment is weaker than a validator that rejects them, and the
exclusions config has the identical gap PF-15 records for the taxonomy config.

## Alternatives considered

**Overload `copy` with a `link_mode : none | symlink | hardlink` flag instead of new entry types.**
Rejected. `entry_type` is what the crash-state table branches on. At row I9
(`durability-and-recovery-model.md:225`) recovery probes the destination and branch (a) says
"destination exists and re-read hash matches → adopt." For a symlink there *is* no content hash to
re-read — the correct check is target-string byte equality — and for `link_hardlink_member` there is
no independent object at all. A flag buried in the payload forces the recovery path to parse the
payload to know which crash-table semantics apply; an entry type makes the intent record's own type
field determine it.

**Declare all link handling out of scope and delete the fixtures.** Rejected. It discards FX-04,
FX-06, FX-07, FX-08 and P17/P18/P19's `required` classification, and it removes the vocabulary
needed to *report* what was not reproduced — which is exactly what makes the out-of-scope path safe.

**Delete the two contradicting config keys, letting the overlays govern implicitly.** Rejected. An
absent key is indistinguishable from an unimplemented one, and the next person needing bundle
handling will add it back with whatever value seems reasonable. A key pinned to a single legal value
with a rejecting loader converts a silent assumption into a validation failure.

## Safety implications

**Copy-before-delete** — a link replaced by a copy of its referent, or dropped, is not a verified
copy of the source object. **Retirement gating** — LR-3 and LR-4 are the mechanism; without them a
`skip`ped link is invisible to CR-2. **No-permanent-deletion** — indirect, via V1-ACC-053's
disposition accounting. **Protected-vault** — a `recreate_symlink` into a vault destination is a
write and is subject to the same pre-finalize existence check.

## Migration and compatibility implications

Additive enum widening plus three conditionally-required `OperationEntry` fields. `entry_type`
participates in the plan content hash bound at approval (`durability-and-recovery-model.md:112`
`plan_bound`), so **existing approved plans are not retroactively reinterpretable**. State
explicitly: a plan drafted before the change that contains a `copy` entry against a symlink
`FileRecord` must **fail validation at lock**, not be silently upgraded. The config change is an
example-file edit; `status: non_production_example` confirms nothing production derives from it.

## Required tests

**Positive** — FX-06 under `reproduce`: an in-root relative link is recreated as a link; assert at
the adapter level that the referent's inode was never opened; assert `link_target_raw` byte-equality
on readback. FX-04 under `reproduce`: member 1 emits `copy`, members 2–3 emit `link_hardlink_member`;
assert destination link count is 3 and **exactly one** content stream was written.

**Negative** — FX-07: any entry type targeting an escaping link fails fatal with
`SYMLINK_TARGET_ESCAPES_ROOT`; assert the link is still *inventoried* (SL-1) and only the *operation*
fails. FX-08: a dangling link is recreated as dangling; a run that resolves it, errors on it, or
classifies it `unreadable` fails. A plan containing `entry_type = copy` for a symlink is rejected at
lock. A plan containing `skip` for a link entry is rejected (LR-3). A config asserting
`package_bundle_policy: treat_as_directory_with_bundle_flag` is rejected at load with
`VAL-BUNDLE-POLICY-INVALID` — **ship the pre-correction file itself as the negative fixture**, which
makes the regression permanent. `symlink_operation_policy: skip` rejected. `bundle_member_
representation: minimal` rejected. An unrecognised value for any pinned key is rejected rather than
silently defaulted — assert the *absence* of a fallback path.

**Negative, `out_of_scope` mode** — FX-06 produces no operation entry, one `unresolved` record with
`LINK_REPRODUCTION_OUT_OF_SCOPE`, a non-zero batch count, and `retirement_gate.eligible = false`. A
run reporting `eligible = true` fails.

**Failure-injection** — the destination adapter refuses `symlink()` mid-batch: entry blocked with
`LINK_RECREATE_UNSUPPORTED`, no partial artifact at the destination path, count surfaced.
`link_hardlink_member` attempted before its primary's `op_outcome = committed` is durable →
`HARDLINK_PRIMARY_NOT_COMMITTED`.

## Required documentation changes

`domain-model.md:792`, `operation-model.md:21–25` (enum); `operation-model.md` (the four LR rules);
`config/exclusions/exclusions.example.yaml:41–44`; `permission-model.md:112` (replace the deferral
with a pointer to LR-2).

## Required ADR changes

**ADR-002** — append: "Source retirement requires every plan entry covering the source object to
reach a terminal disposition that is neither `blocked` nor `unresolved`. A link entry that could not
be reproduced is a retirement blocker, not a skip."

**ADR-012** — append to the Decision paragraph: "Link reproduction capability (preservation
properties P17, P18, P19) is a measured descriptor property. It is never assumed, and an adapter that
has not demonstrated it may not process link entries." Optionally also: "Content-class handling
policy — bundles, symlinks, hard-link sets — is pinned by the preservation overlays and is not
adapter-configurable. Adapter descriptors determine whether a policy can be *satisfied*, never what
the policy *is*."

## Operator policy, or pure specification defect?

**Both, and the boundary is precise.**

*Specification half — proceeds now, fully independent of OD-024:* the two new enum values and their
exact semantics, fields, and verification predicates; the `link_reproduction_mode` key, its two
values, and their plan-time behaviours; rules LR-1 through LR-4 (in particular LR-3 and LR-4, which
hold identically under both modes); the eight reason codes; the corrected config keys with `blocked`
as the shipped value; and the FX-04/06/07/08 expectation files written for **both** modes.

*Operator half — OD-024 decides exactly one thing:* the value of `link_reproduction_mode` for V1.
Nothing else. **Claude has not decided it and does not propose a value here.**

**Consequently the ladder's current blocking is over-broad, and one rung can be unblocked.**
FBL-029's objective (`build-ladder.md:907`) is "Inventory symlinks without following them; content
identity is the hash of the target **string**" — that is SL-1 and SL-2, unconditional, involving no
`OperationEntry` at all. Its negative test (line 919, "FX-07 escaping link — any operation on it
fails") is satisfied by LR-2, which is mode-independent. **FBL-029 can be fully implemented and
closed on the specification half alone.** What OD-024 genuinely gates is **FBL-049**
(`build-ladder.md:1475`, property reproduction). This packet proposes moving OD-024's block from
FBL-029 to FBL-049 and re-scoping FBL-029's `Blocked by` accordingly — see BATCH-15.

## Atomicity

PF-08 and PF-26 must land together: the legal value set of `symlink_operation_policy` is exactly
PF-08's `link_reproduction_mode`, and defining them in two cycles risks two vocabularies for one
switch. Both depend on **PKT-03** (the `HardLinkSet` entity and the `bundle` enum value). PF-08 also
couples to **PKT-05**: A-5 (`preservation-model.md:87`) requires a bundle's *internal* symlinks be
reproduced exactly, so `op_bundle_intent`'s member-kind enum needs the semantics defined here.

## Verification procedure

Re-run `validate_build_ladder.py` and `validate_proposals.py`. Independently: grep
`operation-model.md` and `domain-model.md` for the enum and confirm both now list seven identical
values; confirm `config/exclusions/exclusions.example.yaml` contains no value absent from the pinned
list.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for **OD-024** only.
**This packet is non-authoritative and confers no authority of its own.**
