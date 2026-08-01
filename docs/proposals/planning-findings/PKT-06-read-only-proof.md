# PKT-06 — Proving read-only inventory (PF-13)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-13 (MAJOR) |
| Highest severity | MAJOR |
| Change-control batch | BATCH-06 |
| Operator decision required | **None.** OD-008 is adjacent but does not block — see below. |
| Blocked rungs | FBL-026, FBL-072 |
| Affected acceptance | **V1-ACC-001** (rewritten), **SAF-001**, V1-ACC-044 |
| Depends on | Nothing. Deliberately decoupled — see *Atomicity*. |

PF-13 is the only finding in the set where the *proof* of an invariant is defective rather than its
implementation. Everything else in the workbench describes a control that is missing; this describes
a control whose test cannot fail for the failure it exists to catch.

## The exact contradiction

- `docs/04-acceptance/v1-acceptance.md:15` — V1-ACC-001. Behaviour: "Read-only inventory never
  mutates source bytes or timestamps intentionally." Verification: "**Repeat a scan; compare source
  samples before/after.**" Evidence: "Inventory manifest, **source sample hashes**". Severity
  BLOCKER, gate `implementation`.
- Against `docs/02-specification/preservation-model.md:248` — "Hash comparison of source samples
  before and after a scan **cannot** detect timestamp, extended-attribute, or permission mutation.
  Source-immutability evidence must therefore compare the same property set this document defines,
  not hashes alone."

Two further defects sit in the same row:

- `preservation-model.md:244` — "The platform's read-only guarantee previously carried the loophole
  word 'intentionally'. That word is replaced here by explicit declaration." **V1-ACC-001 still
  contains the word "intentionally."** The acceptance row preserves the loophole the specification
  removed.
- `preservation-model.md:41` — P05 (access time) is `N` (normalized) on **every** adapter column;
  and CM-6 (`file-identity-model.md:202`) — "Reading must not be assumed non-mutating." So a scan
  *does* mutate a timestamp on any adapter whose `atime_on_read` is `updates`. Read literally against
  the specification, the row's behaviour statement is false.

`docs/04-acceptance/safety-acceptance.md:7` — SAF-001 "Inventory is read-only", BLOCKER — is mapped
to this row as its executable counterpart by `build-ladder.md:2561`, so the defect propagates.

## Operational consequence if left unresolved

The row passes trivially. Content hashes of unmodified files match whether or not the scanner
cleared extended attributes, reset mode bits, stripped a resource fork, or triggered a
Finder-metadata write. **A BLOCKER safety row is proven by a method that cannot fail for the failure
it exists to catch.** FBL-026 (`build-ladder.md:817–843`) is then inspected as complete on that
evidence — and note that FBL-026's own operator-validation line (837) already says "comparing the
preservation property set, not hashes alone", so the rung and the acceptance row it cites disagree
with each other today.

The consequence compounds at G4. FBL-072 (`build-ladder.md:2140`) carries V1-ACC-001 into the
dry-run evidence bundle — **the first time the platform reads real, irreplaceable data.** A scanner
that strips extended attributes on a live share would produce a green G4 bundle. On macOS-origin
corpora, extended attributes routinely carry `com.apple.metadata:kMDItemWhereFroms`, Finder tags, and
quarantine state; on a photo corpus they can be the only surviving provenance. That is silent,
unrecoverable, un-alarmed loss of metadata across the entire scanned corpus — certified as
"read-only".

## Affected domain entities and fields

No entity changes. The compared set is `FileRecord` fields 3 (`raw_path_bytes`), 14 (`mtime_ns`), 16
(`ctime_ns`), 17 (`birthtime_ns`), 18 (`atime_ns`), 22 (`link_count`), 30 (`posix_mode`), 31
(`owner_uid`, `group_gid`), 32 (`acl_present`, `acl_payload_ref`), 33 (`xattr_keys`,
`xattr_payload_ref`), 34 (`has_resource_fork`, `has_finder_info`), 35 (`bsd_flags`) — every one
already required at stage D, I, or M in `inventory-model.md`. Plus
`AdapterCapabilityDescriptor.atime_on_read` (`preservation-model.md:142`).

## Affected events, commands, reason codes, and persistence records

New evidence artifact `SourceImmutabilityReport` (see below for why it is separate from
`PreservationComparisonReport`). New reason codes: `SOURCE_MUTATION_DETECTED` (fatal — FBL-026's stop
condition at `build-ladder.md:840` is "Any source mutation is observed"), `SOURCE_CTIME_ADVANCED`
(blocked), `SOURCE_ATIME_NORMALIZED` (counted, **not** a failure). No new events; the report is an
artifact, not a stream fact.

## Proposed normative resolution

### Replacement row for `v1-acceptance.md:15`

| ID | Behaviour | Verification | Evidence | Severity | Gate |
| --- | --- | --- | --- | --- | --- |
| V1-ACC-001 | Read-only inventory leaves the source property set unchanged. The sole permitted change is to properties the effective preservation profile declares `normalized`; each such change is counted and disclosed, never described as "no mutation". | Capture the source property set before the scan and again after; compare per property. Report the count of normalized side effects separately from mismatches. Pass requires **zero** mismatches outside the declared normalized set. | Source immutability report: per-property compared / matched / mismatched / unverifiable counts, the normalized side-effect count, and the sampling frame | BLOCKER | `implementation` |

The word "intentionally" is gone, and the pass rule is a count a mutating scanner cannot satisfy.

### The compared property set, split by capture cost

**Tier 1 — compared at 100% coverage.** All obtainable from the same `stat` call already made during
discovery, so the marginal cost is one extra pass: `raw_path_bytes`, `size_bytes`, `mtime_ns`,
**`ctime_ns`**, `birthtime_ns`, `posix_mode`, `owner_uid`, `group_gid`, `link_count`, `entry_type`,
`symlink_target_raw`.

**Tier 2 — compared across a declared sampling frame.** Expensive to read: `xattr_keys` and the
`xattr_payload_ref` digest, `acl_present` and the `acl_payload_ref` digest, `has_resource_fork` /
`has_finder_info` and their payload digests, `bsd_flags`, `allocated_bytes`.

**Excluded and counted, not compared:** `atime_ns` — P05 is `N` on every adapter. Its delta is
counted and reported as an intentionally normalized source-side side effect
(`preservation-model.md:247`), never as a mismatch and never as "no mutation".

### The sampling frame

Required, declared in the report, and **not implementer-chosen**: every fixture in the identity and
fidelity hazard set (FX-04, FX-12, FX-13, FX-14, FX-15, FX-24) at 100%; plus a minimum of one file
per content class per source root; plus `max(N_min, ceil(p × entries))`, where `N_min` and `p` carry
fixture defaults and are tunable alongside the batch thresholds.

### SI-1 — the load-bearing rule

> **SI-1.** A `ctime_ns` advance on any source entry between the pre-scan and post-scan capture,
> unaccompanied by an authorized operation, is `SOURCE_CTIME_ADVANCED` — a blocked condition —
> regardless of whether any other property differs. Metadata change time cannot be set by the
> platform or by any adapter; its advance therefore proves a write occurred.

`preservation-model.md:42` marks P06 (metadata change time) `U` on every destination, and
`inventory-model.md:46` says "Never settable". Because it is unsettable, a source-side `ctime`
advance is **unforgeable evidence that a metadata write occurred**, even when the writing process
restored the original mtime, mode, and extended attributes afterwards. It is the only property in the
set that detects a *reverted* mutation, and the row must say so.

### Why `SourceImmutabilityReport` is a separate artifact

It could have been a section of `PreservationComparisonReport` — but that entity does not exist yet
(PF-24, PKT-03) and lands at FBL-053, twenty-seven rungs after FBL-026. Coupling them would make an
early G3 inventory rung wait on a late G3 verification rung and inherit its blockage. The two
artifacts also answer different questions — *did the source change* versus *did the destination
faithfully reproduce the source* — and their pass rules differ. Keep them separate and
cross-reference.

## Alternatives considered

**Keep the hash method and add "spot-check permissions manually."** Rejected: not machine-verifiable,
produces no artifact satisfying `evidence-standard.md`, cannot scale to a G4 live corpus, and —
decisively — leaves the row's *stated method* unchanged, so the row continues to self-certify.

**Compare the full property set across the entire tree at 100%.** Rejected as the required method, on
cost: Tier 2 reads are per-file syscall storms on a multi-million-entry corpus, and a round trip each
on a network adapter. The tiered method still fails on real mutation — a scanner that strips extended
attributes strips them everywhere, so any nonempty sample catches it, and Tier 1's 100% `ctime`
coverage catches even a single-file metadata write. The tiering buys cost without buying back the
failure mode.

## Safety implications

**Read-only inventory** is the invariant, and this is the only finding where its *proof* rather than
its *implementation* is defective. Secondary: **retirement gating** — a source silently mutated
during inventory has drifted from the plan preconditions later bound against it, and drift detected
at Phase A4 would be attributed to an external actor rather than to the platform itself.

## Migration and compatibility implications

An acceptance-row edit plus an evidence-package change. FBL-026's evidence package
(`build-ladder.md:838`) gains the source immutability report; FBL-072's negative-test line (2140)
already anticipates this and needs only the artifact named. No entity or contract change.

## Required tests

**Positive** — a clean scan over the full fixture corpus produces zero Tier 1 and Tier 2 mismatches,
and a non-zero counted `atime` normalization figure on an adapter whose `atime_on_read = updates`;
the report states the count and **does not use the phrase "no mutation"**.

**Negative** — inject an adapter that writes an extended attribute during metadata extraction: FX-12
must fail the row. **The current hash-only method passes this injection; that contrast is itself the
regression test for PF-13.** Run both methods and assert the old passes and the new fails. Inject a
mode-bit change: FX-14 fails with `SOURCE_MUTATION_DETECTED`. FX-24: `raw_path_bytes` compared
byte-for-byte; a scanner that normalizes a filename in place fails.

**Negative — the test that earns SI-1 its place.** Inject a metadata write that is fully reverted
(write an extended attribute, remove it, restore mtime): every property matches **except `ctime_ns`**,
and the row must still fail with `SOURCE_CTIME_ADVANCED`.

**Failure-injection** — a source whose `atime_on_read = suppressible` but whose suppression fails at
runtime: the count is reported, the run does not fail, and the report must not describe the result as
"no mutation" (`preservation-model.md:247`). **Assert on the report's wording, not only its numbers.**

## Required documentation changes

`v1-acceptance.md:15` (the row); `safety-acceptance.md:7` (SAF-001, to match); a new
`SourceImmutabilityReport` schema section, placed in `preservation-model.md` alongside the comparison
report schema; `build-ladder.md` FBL-026 evidence package and FBL-072 evidence bundle.

## Required ADR changes

**ADR-001** — replace/extend Consequences: "Read-only means the source property set defined by the
preservation model is unchanged after a scan, with the sole exception of properties the effective
profile declares `normalized` — access time — whose changes are counted and disclosed. Hash equality
of source samples is **not** evidence of read-only inventory: a matching digest proves nothing about
timestamps, permissions, ownership, ACLs, extended attributes, or resource forks. Metadata change
time is unsettable and its advance is therefore proof that a write occurred."

## Operator policy, or pure specification defect?

**Pure specification defect** — specifically an acceptance defect, the only one in the workbench.

One operator-adjacent hook: the Tier 2 sampling-frame parameters `N_min` and `p` are threshold values
that naturally belong on the approved threshold sheet under **OD-008**. But defaults can be specified
now, and the mandatory-100%-hazard-fixture clause plus Tier 1's 100% coverage makes the row fully
verifiable at fixture defaults. **OD-008 does not block PF-13**, and this packet neither proposes nor
implies a value for it.

**A scoping note the correction must not over-apply.** PILOT-004 (`pilot-acceptance.md:26`, "Compare
pre/post hashes") is a *destination content* row and is correct as written. Do not touch it. The
defect is specific to using hash comparison as *source-immutability* evidence.

## Atomicity

**None required — and that is a design decision, not an omission.** By specifying
`SourceImmutabilityReport` as an artifact separate from `PreservationComparisonReport`, PF-13 is
deliberately decoupled from PF-24 so that FBL-026 (early G3) does not inherit a blockage owned by
FBL-053 (late G3). The instinct is to fold the source-side comparison into the existing report
schema; this packet declines to, and records why.

## Verification procedure

Re-run `foundation_self_review.py` and `validate_build_ladder.py`. Independently: grep
`v1-acceptance.md` for the word "intentionally" and confirm zero occurrences in V1-ACC-001; confirm
V1-ACC-001 and SAF-001 state the same method; confirm the FBL-026 and FBL-072 evidence packages name
the source immutability report.

## Change-control authority

Change control per `docs/05-governance/change-control.md`. No operator decision is required.
**This packet is non-authoritative and confers no authority of its own.**
