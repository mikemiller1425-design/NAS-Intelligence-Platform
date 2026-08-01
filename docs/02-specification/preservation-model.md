# Preservation Model

## Governing statement

> **Hash equality is necessary but NOT sufficient evidence of preservation.**
>
> A matching cryptographic digest proves only that the destination's *content stream* is byte-identical to the source's content stream as read at a single moment. It proves nothing about modification time, creation time, POSIX mode, ownership, ACLs, extended attributes, resource forks, Finder metadata, BSD flags, hard-link topology, symlink-versus-target semantics, sparse-region layout, filename byte sequence, filename Unicode normalization form, or package-bundle integrity.
>
> No document, report, acceptance criterion, or operator communication in this platform may describe a hash match alone as a "verified copy", a "preserved file", or evidence sufficient to authorize source retirement. Preservation evidence is a **preservation comparison report** evaluated against the declared preservation profile for the specific source adapter, destination adapter, and content class involved.

This document resolves audit finding **FND-M002**. It is adapter-aware but adapter-agnostic: adapters declare measured capabilities, and platform behavior is a function of those declarations. It is therefore implementable against fixtures while OD-016 remains open.

## Why this document exists

Before it, every preservation statement in the repository concerned *not mutating the source*. There was no destination-fidelity requirement anywhere. The consequence was a chain in which a hash match was the sole technical precondition standing between a copy and the retirement of the original.

## Property classification vocabulary

| Class | Meaning | Evidence obligation |
| --- | --- | --- |
| `required` | Must be reproduced exactly. Failure fails the entry. | Verified per file; mismatch is `blocked`. |
| `best_effort` | Reproduced when the destination supports it. Non-reproduction is recorded per file, does not fail the entry, but must be surfaced in the batch report and at the retirement gate. | Recorded per file. |
| `normalized` | Deliberately not reproduced; a defined transformation is applied. The transformation must be documented and reported. | Declared once per profile; counted per batch. |
| `unsupported_reported` | The destination or protocol cannot carry this property. It must be enumerated, counted, and shown at the retirement gate — never silently dropped. | Counted per batch; enumerable per file. |

| ID | Rule |
| --- | --- |
| PC-1 | These four classes are exhaustive. There is no fifth state and no "unknown". A property whose support has not been *measured* against fixtures is treated as `unsupported_reported` until characterization succeeds. |
| PC-2 | A `required` property that the destination cannot carry is a **capability mismatch**. It may not be silently demoted to `best_effort`. |

## Preservation profile matrix

Columns are destination adapter classes. **R** = required, **B** = best effort, **N** = normalized, **U** = unsupported and reported.

| # | Property | local-posix | smb | nfs (v3 / v4.x) | sftp | synology-api |
| --- | --- | :---: | :---: | :---: | :---: | :---: |
| P01 | File content bytes | R | R | R | R | R |
| P02 | Logical size | R | R | R | R | R |
| P03 | Modification time | R | R | B / R | B | B |
| P04 | Creation / birth time | B | B | U / B | U | U |
| P05 | Access time | N | N | N | N | N |
| P06 | Metadata change time | U | U | U | U | U |
| P07 | POSIX mode bits | R | B | R | B | U |
| P08 | setuid / setgid / sticky | N | U | N | U | U |
| P09 | Owner UID | B | U | B | B | U |
| P10 | Group GID | B | U | B | B | U |
| P11 | POSIX / NFSv4 ACL | B | B | B | U | B |
| P12 | Extended attributes | R | B | U / B | U | U |
| P13 | macOS Finder info | R | B | N | U | U |
| P14 | macOS resource fork | R | B | N | U | U |
| P15 | Quarantine attribute | N | N | N | N | N |
| P16 | BSD flags | B | U | U | U | U |
| P17 | Hard-link topology | R | U | B | U | U |
| P18 | Symlink reproduced as a link | R | B | R | B | U |
| P19 | Symlink target string, byte-exact | R | B | R | B | U |
| P20 | Sparse-region layout | B | B | B | U | U |
| P21 | Filename raw byte sequence | R | N | R | R | B |
| P22 | Filename Unicode normalization form | R | N | R | R | B |
| P23 | Filename case | R | N | R | R | B |
| P24 | Directory structure and nesting depth | R | R | R | R | R |
| P25 | Empty directories | R | R | R | R | B |
| P26 | Directory modification time | B | B | B | B | U |
| P27 | macOS package-bundle atomicity | R | R | R | R | R |
| P28 | Alternate data streams | U | B | U | U | U |
| P29 | Synology sidecar directories and recycle areas | N | N | N | N | N |
| P30 | Filesystem-level clones and compression | N | U | U | U | U |

| ID | Rule |
| --- | --- |
| PM-1 | Every `N` cell requires a named, documented transformation and a per-batch count in the comparison report. "Normalized" without a declared transformation is not a valid classification. |
| PM-2 | Every `U` cell requires a per-batch count of affected files, displayed at the source-retirement gate. A `U` property with a non-zero count is an operator decision point, not a footnote. |
| PM-3 | This matrix is a **default profile**. The effective profile for a run is the default profile intersected with the *measured* capability descriptors of both endpoints — never the assumed ones. |
| PM-4 | P27 (bundle atomicity) is enforced by the platform, not by the adapter. It is `required` on every adapter because the platform, not the filesystem, guarantees it. |

## Content-class overlays

Overlays apply after the base matrix and always tighten, never loosen.

### Overlay A — macOS package bundles

| ID | Rule |
| --- | --- |
| A-1 | A bundle is inventoried as a single logical file of entry type `bundle`, and its members are inventoried individually for evidence. The bundle is the unit of classification, planning, approval, copy, verification, and retirement. Members are never independently classified, planned, or copied. |
| A-2 | A bundle's content identity is a **manifest digest**: a canonical ordering of (member relative raw path, member size, member content hash), hashed. A single member digest is never the bundle's identity. |
| A-3 | Bundle copy is **all or nothing**. Partial bundle copy fails the entry, and the partial destination is removed or quarantined. |
| A-4 | The allowance that "directory entries may be represented minimally if the file tree is large" **does not apply to bundles**. Minimal representation of a bundle is prohibited. |
| A-5 | An adapter that cannot reproduce a bundle's internal structure exactly — including internal symlinks — is a capability mismatch for that content class. |

### Overlay B — Symlinks

| ID | Rule |
| --- | --- |
| B-1 | P18 and P19 are promoted to `required` for all adapters. An adapter that cannot recreate a symlink as a link may not process symlink entries; it must skip and report. |
| B-2 | Silently replacing a symlink with a copy of its target is **prohibited**. This is not a best-effort degradation; it is data-model corruption, because it can duplicate arbitrary amounts of data and break relative-path assumptions. |
| B-3 | A symlink's content hash is the hash of its target string, never the target file's content hash. |

### Overlay C — Sparse files

| ID | Rule |
| --- | --- |
| C-1 | Apparent size and allocated size are both recorded. A comparison checking only apparent size cannot detect densification. |
| C-2 | Densification is permitted only when P20 is declared `normalized` for the destination, and only with a per-file record and a per-batch byte-delta total. |
| C-3 | If densification would cross the critical free-space threshold, the batch stops before writing. |
| C-4 | Hash equality between a sparse source and a densified destination **is expected and proves nothing about layout**. This is the canonical illustration of the governing statement. |

### Overlay D — Hard-link sets

| ID | Rule |
| --- | --- |
| D-1 | A hard-link set is planned, copied, and verified as one unit. |
| D-2 | Where the destination supports links, the platform copies the first member and links the remainder; the comparison report asserts that destination link count equals source link count. |
| D-3 | Where the destination cannot enumerate or create links (P17 = `U`), the operation is **blocked** pending operator acknowledgement. Silent N-fold duplication is prohibited. |
| D-4 | Retiring any member requires the whole set to reach a final disposition. |

### Overlay E — Zero-byte and very large files

| ID | Rule |
| --- | --- |
| E-1 | Zero-byte files hash identically to one another. Duplicate grouping must not collapse distinct zero-byte files into a redundancy recommendation. |
| E-2 | Files exceeding the streaming threshold require the explicit hash-stability window, because long reads widen the concurrent-modification window proportionally. |

### Overlay F — Protected vaults

| ID | Rule |
| --- | --- |
| F-1 | Within vault-classified destinations, all `best_effort` properties are promoted to `required`. The protected-vault ADR implies this; it is made explicit here. |

## Adapter capability descriptor

```text
AdapterCapabilityDescriptor := {
  id, adapter_class, adapter_version, endpoint_ref,
  measured_at, measured_by_fixture_suite_version,
  properties: {
    <P01..P30>: { read_support, write_support, fidelity, resolution, notes }
  },
  filename_transform        : byte_transparent | normalizing
  case_sensitivity          : sensitive | insensitive_preserving | insensitive_folding
  normalization_sensitivity : sensitive | insensitive_preserving | insensitive_folding
  object_id_grade           : authoritative | advisory | unavailable
  mtime_resolution_ns       : integer
  atime_on_read             : updates | suppressible | not_updated
  durability_class          : strong | weak | unknown
  max_path_bytes, max_component_bytes : integer
  attestation_evidence_ref  : ref
}
```

| ID | Rule |
| --- | --- |
| CD-1 | A descriptor is valid only if produced by an actual fixture characterization run. **Assumed or hand-written descriptors are invalid** and may not gate any operation. |
| CD-2 | The descriptor id is embedded in every operation plan at approval time. A descriptor mismatch at execution stops the batch. |
| CD-3 | Descriptors expire. Re-characterization is required after any adapter version change, endpoint change, or mount-option change. |

## Capability-mismatch resolution protocol

Executed at **plan time**, before approval — never at execution time.

1. **Resolve.** `effective_profile` = base matrix ∩ source descriptor ∩ destination descriptor ∩ content-class overlays.
2. **Classify** each property:
   - `MM-0` no mismatch
   - `MM-1` required at source, best-effort at destination
   - `MM-2` required at source, unsupported at destination
   - `MM-3` property present at source, normalization applies at destination
   - `MM-4` property unreadable at source — cannot be preserved or verified
3. **Resolve each class:**
   - `MM-0` → proceed.
   - `MM-1` → proceed; per-file record; batch count; shown at the retirement gate.
   - `MM-2` → **block** the affected entries. Proceed only via (a) an operator-approved profile downgrade recorded as an approval whose scope names the specific property, (b) exclusion of the affected entries from the plan, or (c) a different destination adapter. **Automatic downgrade is prohibited.**
   - `MM-3` → proceed only if the transformation is declared in the profile; otherwise block.
   - `MM-4` → the property is recorded `unverifiable`. It may **never** be reported as preserved. If the property is `required`, block.
4. **Freeze.** The resolved profile and both descriptor ids are embedded in the operation plan and become immutable at approval.
5. **Gate.** Source retirement is blocked while any `MM-1`, `MM-2`, `MM-3`, or `MM-4` count is non-zero, unless a scoped operator waiver naming each affected property exists.

| ID | Rule |
| --- | --- |
| CM-P1 | A profile downgrade approval must name the specific properties. A blanket "accept all downgrades" approval is not a valid approval scope. |
| CM-P2 | The resolution protocol never runs at execution time. Discovering a mismatch during execution stops the batch, because the approved plan's assumptions are void. |

## Preservation comparison report

This artifact replaces "the hash matched" as preservation evidence.

```text
PreservationComparisonReport := {
  id, plan_id, plan_version, batch_id, generated_at,
  source_adapter_descriptor_id, destination_adapter_descriptor_id,
  effective_profile_id, content_class_overlays_applied[],

  scope: { entries_planned, entries_executed, entries_verified,
           entries_failed, entries_blocked, entries_skipped },

  content_evidence: {
    hash_algorithm, hash_matches, hash_mismatches,
    size_matches, size_mismatches,
    source_token_stable_count,
    source_token_changed_count,
    source_token_indeterminate_count
  },

  property_results: [
    { property_id, classification,
      compared_count, matched_count, mismatched_count,
      not_applicable_count, unverifiable_count,
      transformation_applied,
      sample_mismatch_file_ids[] }
  ],

  identity_evidence: {
    same_path_replacements_detected,
    hardlink_sets_total, hardlink_sets_preserved,
    hardlink_sets_expanded, hardlink_detection_unavailable_count,
    case_only_collisions, normalization_collisions, confusable_collisions,
    symlinks_recreated_as_link, symlinks_skipped, symlinks_resolved_to_target,
    bundles_total, bundles_copied_atomically, bundles_failed,
    sparse_files_total, sparse_files_densified, densification_bytes_added
  },

  capability_mismatches: [
    { property_id, mismatch_class, affected_count, resolution, approval_id }
  ],

  retirement_gate: {
    eligible                : boolean,
    blocking_conditions[]   : string,
    required_waivers[]      : { property_id, approval_id }
  },

  conclusion: {
    statement,
    hash_equality_disclaimer   # REQUIRED — the governing statement, verbatim
  }
}
```

| ID | Rule |
| --- | --- |
| CR-1 | `conclusion.hash_equality_disclaimer` is a required field carrying the governing statement verbatim. A report without it is invalid evidence. |
| CR-2 | `retirement_gate.eligible` is `false` whenever any `required` property has a non-zero mismatch or unverifiable count, or any `MM-2`/`MM-4` mismatch lacks a scoped waiver. |
| CR-3 | The report must be readable without conversation history and must satisfy the evidence standard. |

## Source-side preservation

The platform's read-only guarantee previously carried the loophole word "intentionally". That word is replaced here by explicit declaration:

- Adapters declare whether reading updates access time (`atime_on_read`).
- Where the platform cannot suppress an access-time update, it is reported as an **intentionally normalized source-side side effect**, counted per run, and disclosed. It is never described as "no mutation".
- Hash comparison of source samples before and after a scan **cannot** detect timestamp, extended-attribute, or permission mutation. Source-immutability evidence must therefore compare the same property set this document defines, not hashes alone.

## Related documents

- `docs/02-specification/file-identity-model.md`
- `docs/02-specification/durability-and-recovery-model.md`
- `docs/02-specification/operation-model.md`
- `docs/03-architecture/adapter-architecture.md`
- `docs/05-governance/gate-model.md`
