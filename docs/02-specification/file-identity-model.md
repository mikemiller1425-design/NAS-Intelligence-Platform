# File Identity Model

## Purpose

This document defines what it means for the platform to say "this is the same file." It resolves audit finding **FND-M001**.

Identity is a safety primitive. Every duplicate decision, every resume, every precondition revalidation, and every retirement gate depends on it. Identity is therefore **evidence-graded**, never assumed.

This specification is **adapter-aware but adapter-agnostic**. It is implementable against synthetic fixtures before OD-016 (adapter choice) is resolved: adapters declare capabilities, and the platform's behavior is a function of those declarations rather than of any particular product choice.

## Logical file identity

A **`LogicalFile`** is the platform's durable notion of one distinct filesystem object under an approved `SourceRoot`. It is addressed by `logical_file_id`: an opaque, stable, platform-assigned identifier minted exactly once at first successful registration and **never recomputed, never derived from path, and never reused**.

| ID | Invariant |
| --- | --- |
| LFI-1 | `logical_file_id` is assigned at the `discovered → inventoried` transition and is immutable thereafter. |
| LFI-2 | A `logical_file_id` is never reassigned to a different filesystem object. If the object behind an identity changes, the platform mints a new `logical_file_id` and records a `superseded_by_logical_file_id` link. It does not mutate the old record. |
| LFI-3 | Two `logical_file_id` values may reference the same underlying object (hard links). Identity is per-name; object identity is tracked separately by `object_identity_key`. |
| LFI-4 | Byte-content equality (hash) **never** establishes logical identity. It establishes content equivalence only, which is input to duplicate grouping, not to identity. |
| LFI-5 | No stage may derive `logical_file_id` from `normalized_path`. Path is *locating* evidence, not *identifying* evidence. |

## Identity key composition

Every `FileRecord` carries an `IdentityKey` with independently graded components:

```text
IdentityKey := {
  root_identity     : RootIdentity
  path_identity     : PathIdentity
  object_identity   : ObjectIdentity      # may be unavailable
  content_identity  : ContentIdentity     # hash + size
  change_token      : ChangeToken
}
```

### Evidence grades

| Grade | Meaning | Permitted use |
| --- | --- | --- |
| `authoritative` | The adapter guarantees uniqueness and stability for the lifetime of the run and across remounts. | May be used alone to assert sameness. |
| `advisory` | The adapter supplies the value but does not guarantee stability across remount, reconnect, or server restart. | May corroborate. May **never** be the sole basis for asserting sameness. |
| `unavailable` | The adapter does not supply the value. | Must be recorded as `unavailable`, never as a default or zero. |
| `indeterminate` | A value was supplied but failed an internal consistency check. | Treated as a stop condition. |

| ID | Rule |
| --- | --- |
| IK-1 | `evidence_grade` is a required field per component. Absence of a value is recorded as `unavailable`; it is never silently coerced to `null` or `0`. |
| IK-2 | The composite `identity_confidence` of a `FileRecord` is the **minimum** grade across `root_identity` and (`object_identity` OR `path_identity` + `change_token`). Never the maximum, never an average. |
| IK-3 | `content_identity_state` is defined below. It was previously declared but never defined. |
| IK-4 | Only `hashed_stable` may satisfy exact-duplicate grouping or post-operation verification. `hashed_unstable` and `hashed_stale` are review-routing conditions, never verification evidence. |

### `content_identity_state`

| Value | Meaning |
| --- | --- |
| `unhashed` | No approved hash exists. |
| `hashed_unstable` | A hash exists, but the change token before and after the hash read did not match, or was indeterminate. |
| `hashed_stable` | A hash exists and the change token was equal immediately before and immediately after the full read. |
| `hashed_stale` | A previously `hashed_stable` hash whose change token no longer matches current observation. |
| `unreadable` | Read failed; error recorded. |

## Root identity

A `SourceRoot` carries `root_identity_evidence`:

```text
RootIdentity := {
  adapter_class            : local-posix | smb | nfs | sftp | synology-api | fixture
  volume_identifier        : string | unavailable
  volume_identifier_kind   : st_dev | volume_uuid | share_uac | export_fsid | none
  mount_or_endpoint_ref    : opaque
  capability_descriptor_id : ref
  observed_at              : timestamp
  evidence_grade           : authoritative | advisory | unavailable
}
```

| ID | Rule |
| --- | --- |
| RI-1 | A root whose `volume_identifier` is `unavailable` may still be scanned, but every `FileRecord` beneath it inherits `identity_confidence` no higher than `advisory`, and same-path replacement detection becomes **mandatory rather than optional**. |
| RI-2 | If `volume_identifier` observed at the start of a scan differs from the value observed at any checkpoint, the run stops. Remount under a different device, or a re-exported share, is not a resumable condition. |
| RI-3 | `evidence_grade` may be `authoritative` only when the root's `authority` is `confirmed_live` **and** the capability descriptor was measured rather than assumed. Roots at `intended_structure` or `unresolved_assumption` are capped at `advisory`. |

## Path identity — raw versus normalized

```text
PathIdentity := {
  raw_path_bytes        : byte string     # exact octets returned by the adapter
  raw_path_encoding     : utf8 | utf8_lossy | opaque_bytes
  normalized_path       : string
  normalization_profile : ref
  segment_count         : integer
  nfc_form              : nfc | nfd | mixed | not_applicable
  case_form_observed    : preserved | lowered | uppered
}
```

| ID | Rule |
| --- | --- |
| NP-1 | **`raw_path_bytes` is canonical.** It is stored verbatim and is the value used for every filesystem operation. `normalized_path` is a derived index key and must never be used to open, read, copy, or write a file. |
| NP-2 | Normalization is lossy and declared. Exactly one profile produces `normalized_path`. |
| NP-3 | `normalized_path` is never written to a destination. Destination paths derive from taxonomy templates and are validated separately. |
| NP-4 | Collision is defined below. |
| NP-5 | Collision evaluation uses the **destination's** case- and normalization-sensitivity, not the source's. |

### Normalization profile `NP/1` (V1)

1. Decode to Unicode using `raw_path_encoding`; on failure mark `utf8_lossy` and route to review.
2. Apply Unicode **NFC**.
3. Apply full Unicode **case folding** to produce the *comparison form only*.
4. Collapse repeated separators; strip trailing separators except at root.
5. Resolve `.` segments; **reject** `..` segments.
6. Do **not** resolve symlinks.

### Collision definition

Two entries **collide** under `NP/1` if their `normalized_path` values are equal while their `raw_path_bytes` differ. Three classes are distinguished and reported separately:

| Class | Trigger | Example |
| --- | --- | --- |
| `case_only_collision` | Raw bytes differ only by case. | `Photo.JPG` vs `photo.jpg` |
| `normalization_collision` | Raw bytes differ only by Unicode normalization form. | `Café` (NFC) vs `Café` (NFD) |
| `confusable_collision` | Normalized forms are equal after confusable folding but not after NFC and case folding alone. | Cyrillic `а` vs Latin `a` |

The existing rule "destination collisions never overwrite silently" is hereby scoped to include all three classes.

## Adapter-specific identity evidence

This table is the **normative capability contract**. Adapters must publish a capability descriptor asserting these grades, and the descriptor must be validated against fixtures before the adapter is trusted.

| Identity evidence | local-posix | smb | nfs (v3 / v4.x) | sftp | synology-api | fixture |
| --- | --- | --- | --- | --- | --- | --- |
| Volume identifier | `st_dev` — authoritative within a mount lifetime; advisory across remount | Share UNC + server GUID — advisory | Export `fsid` — advisory | none — unavailable | none — unavailable | synthetic — authoritative |
| Filesystem object id | `st_ino` — authoritative | SMB2 `FileId` — advisory; may be absent or recycled | v3 filehandle — advisory; v4.x `fileid` — advisory | unavailable | unavailable | synthetic — authoritative |
| Link count | `st_nlink` — authoritative | unavailable | advisory | unavailable | unavailable | synthetic |
| mtime | nanosecond — authoritative | 100 ns — authoritative | v3 1 s — advisory; v4 ns — authoritative | v3 1 s — advisory | 1 s — advisory | synthetic |
| ctime | authoritative (read-only) | advisory | advisory | unavailable | unavailable | synthetic |
| birthtime | authoritative | authoritative | v3 unavailable; v4 advisory | unavailable | unavailable | synthetic |
| Size | authoritative | authoritative | authoritative | authoritative | advisory | authoritative |
| Filename byte transparency | byte-transparent | **not byte-transparent** — NFC/NFD conversion occurs | byte-transparent | byte-transparent | UTF-8 API | byte-transparent |

| ID | Rule |
| --- | --- |
| AE-1 | No evidence graded `advisory` or `unavailable` may be the sole basis for asserting that two observations refer to the same object. |
| AE-2 | For any adapter whose object-id grade is `advisory` or `unavailable` — that is, **every non-local adapter** — same-path replacement detection is mandatory, and the change token is the primary identity-continuity mechanism. |
| AE-3 | For `sftp` and `synology-api`, the maximum achievable `identity_confidence` is `advisory`. These adapters may not source a run that will authorize source retirement without an explicit, separately recorded operator waiver. |
| AE-4 | Every adapter publishes `mtime_resolution_ns`. Where resolution is coarser than one millisecond, a same-window modification is undetectable by timestamp, and the platform must fall back to full content re-verification rather than trusting the token. |

## Change-token semantics

A `ChangeToken` answers "has this object changed since I last looked?"

```text
ChangeToken := {
  size_bytes, mtime_ns, mtime_resolution_ns, ctime_ns,
  object_id, link_count, native_token, observed_at_ns,
  grade : authoritative | advisory | unavailable
}
```

Comparison is **ternary**:

| Result | Condition |
| --- | --- |
| `EQUAL` | Every available component matches, **and** at least one component is graded `authoritative`, **and** `mtime_resolution_ns` is fine enough to exclude a same-window write. |
| `CHANGED` | Any available component differs. |
| `INDETERMINATE` | All available components match but none is `authoritative`; or `mtime_resolution_ns` cannot exclude a same-window write; or any component is `indeterminate`. |

| ID | Rule |
| --- | --- |
| CT-1 | **`INDETERMINATE` must never be treated as `EQUAL`** — by any component, at any point, under any threshold setting. No configuration flag collapses `INDETERMINATE` into `EQUAL`. |
| CT-2 | `INDETERMINATE` at a precondition gate is resolved only by a full content re-hash of the source, producing a fresh hash record with scope `source_recheck`. |
| CT-3 | A change token is captured at five journalled points: `T_discover`, `T_prehash`, `T_posthash`, `T_precopy`, `T_postcopy`. |
| CT-4 | `content_identity_state` becomes `hashed_stable` only if `compare(T_prehash, T_posthash) == EQUAL`. |
| CT-5 | A copy is eligible for `verified` only if `compare(T_precopy, T_postcopy) == EQUAL` **in addition to** destination hash equality. |

## Detection rules

### Same-path replacement

| Observation | Mandated behavior |
| --- | --- |
| Token `EQUAL` and `object_id` matches | Continue with the same `logical_file_id`. |
| Token `EQUAL` but `object_id` **differs** | Same-path replacement confirmed. Retire the old `logical_file_id` to unresolved, mint a new one, route to review. Byte-identity does not rescue this: the object is different. |
| Token `CHANGED` | Mark old content evidence `hashed_stale`; mint a new `logical_file_id`; route to review if the old record is referenced by any approved or locked plan. |
| Token `INDETERMINATE` | Re-hash. If the hash differs, treat as `CHANGED`. If it matches, record `identity_continuity: unproven` and route to review before any operation referencing the record. |

A `logical_file_id` referenced by a **locked** plan that undergoes same-path replacement causes the plan entry to fail. It is never silently re-bound to the new object; rebinding requires a new plan version.

Size-and-hash equality after a `CHANGED` token is **not** grounds to conclude nothing happened. It is recorded as `content_unchanged_object_replaced` and is an explicit review condition, because metadata, ACLs, extended attributes, and link topology may all differ.

### Concurrent modification during hashing or copying

| ID | Rule |
| --- | --- |
| CM-1 | A hash read spanning a `CHANGED` or `INDETERMINATE` token boundary describes **no coherent version of the file**. Such a hash is recorded with status `unstable` and must not be used for duplicate grouping, plan preconditions, or verification. |
| CM-2 | Up to `identity.max_hash_restabilize_attempts` (default 2) full re-reads are permitted. If stability is not achieved, the file becomes `unresolved` with reason `source_unstable`. It is never silently accepted. |
| CM-3 | A copy whose source token changed between `T_precopy` and `T_postcopy` fails the entry, removes or quarantines the partial destination artifact, and journals `SourceMutatedDuringCopy`. It is never marked `verified`, even if the destination hash matches the precondition hash. |
| CM-4 | Copies are written to a temporary destination name and promoted by atomic rename only after **both** destination hash equality and `compare(T_precopy, T_postcopy) == EQUAL`. |
| CM-5 | A source observed with an open write handle, an advisory lock, or an adapter-reported in-use state at `T_precopy` is a stop condition for that entry, not a retry condition. |
| CM-6 | Reading must not be assumed non-mutating. Adapters declare whether reading updates access time. Where the platform cannot suppress that update, it is reported as an intentionally normalized source-side side effect. |

### Hard links

| ID | Rule |
| --- | --- |
| HL-1 | Where `link_count` is authoritative and greater than one, the entry belongs to a **hard-link set**. Members sharing `(volume_identifier, object_id)` form one `HardLinkSet`. |
| HL-2 | **A `HardLinkSet` is not a `DuplicateGroup`.** Duplicate detection must exclude within-set members from exact-duplicate grouping. Reporting them as duplicates is a defect. |
| HL-3 | Where `link_count` is unavailable, hard-link topology is undetectable. The platform must not assert that no hard links exist; it records `hardlink_detection: unavailable` and raises a run-level warning. |
| HL-4 | Copying a hard-link set with an adapter that cannot detect links silently converts N links into N independent copies. This is a capability mismatch requiring operator acknowledgement or a stop. |
| HL-5 | A hard-link set may not be partially retired. Retiring any member requires the whole set to be accounted for. |

### Case-only collisions

Two entries differing only by case are two distinct files on a case-sensitive source and one path on a case-insensitive destination. Risk is evaluated against the **destination's** case sensitivity. A case-only collision may **never** be resolved by destination versioning without review, because the two files are semantically distinct originals rather than versions of one another.

### Unicode-normalization collisions

This is the macOS-to-Synology hazard the blueprint previously had no vocabulary for.

| ID | Rule |
| --- | --- |
| UN-1 | Every `FileRecord` records `nfc_form` per path segment. |
| UN-2 | Two entries in one directory whose NFC forms are equal but whose raw bytes differ form a `normalization_collision`. On a normalization-sensitive filesystem these are two distinct files; on a normalization-insensitive one they cannot coexist. |
| UN-3 | Any adapter that is not byte-transparent for filenames — notably `smb` — declares `filename_transform: normalizing`. Under such an adapter the platform must not assert that a destination filename is byte-identical to the source filename. It may assert only NFC-equivalence, and the comparison report must record the transform. |
| UN-4 | A normalization collision at a destination is a mandatory stop and review. It is never auto-resolved. |
| UN-5 | A round-trip check — write an NFD name, read it back, compare raw bytes — is a required adapter characterization test, and its result is a required field of the capability descriptor. |

### Symlinks

| ID | Rule |
| --- | --- |
| SL-1 | Symlinks are inventoried and **never** followed during enumeration, hashing, or size accounting by default. |
| SL-2 | A symlink's identity is the link itself. Its content identity is the hash of the **link target string**, not the target's bytes. Hashing the target silently converts a link into a copy of its referent. |
| SL-3 | Operation entry types must include `recreate_symlink`, or symlink handling must be explicitly declared out of scope with a stop condition. |
| SL-4 | A symlink whose resolved target escapes an approved root remains a valid inventory record but is a hard stop for any operation. This supplies the definition of "specifically and safely handled" that the permission model defers. |

## Network filesystem identity limitations

Over `smb`, `nfs`, `sftp`, and `synology-api`, the platform **cannot** obtain authoritative object identity. Every identity assertion under these adapters is at best `advisory`.

Specific limitations that must be stated in operator-facing reports:

- SMB `FileId` may be absent, may not be unique across a DFS namespace, and may be recycled after deletion.
- NFSv3 filehandles are opaque and may change across server restart or export re-creation.
- SFTP has no object identifier at all; identity is path-only.
- The Synology DSM API exposes no inode; identity is path-only.
- Coarse `mtime` resolution makes sub-second modification invisible.
- Client-side caching (SMB oplocks, NFS attribute caches, the macOS unified buffer cache) can return **stale attributes**, producing false `EQUAL` tokens.

Consequently, under any non-`local-posix` adapter the platform must treat an `EQUAL` token whose only authoritative component is size as `INDETERMINATE`, disable attribute caching where permitted and record whether it could, and re-hash rather than trust the token whenever `mtime_resolution_ns` exceeds one millisecond.

**Connection loss, remount, or reconnect invalidates all in-flight change tokens for that root.** Tokens captured before a reconnect may not be compared against tokens captured after; this is a checkpoint-invalidating event.

## Required stop and review behavior

Severity values reuse the existing inventory vocabulary: `soft`, `blocked`, `fatal`.

| # | Condition | Mandated behavior | Severity |
| --- | --- | --- | --- |
| STOP-1 | Root volume identifier changes mid-run | Stop the run. Invalidate checkpoints for that root. Require operator re-confirmation before resume. | fatal |
| STOP-2 | Same-path replacement confirmed | Block the item. Retire old identity, mint new, route to review. Fail any locked plan entry referencing it. | blocked |
| STOP-3 | Token `CHANGED` between `T_prehash` and `T_posthash` | Mark hash unstable; bounded re-read; on failure route to unresolved. Never publish the hash. | soft → blocked |
| STOP-4 | Token `INDETERMINATE` at the precondition gate | Do not proceed on the token. Force a full source re-hash. | blocked |
| STOP-5 | Token `CHANGED` between `T_precopy` and `T_postcopy` | Fail the entry. Remove or quarantine the partial destination. Never mark verified. | blocked |
| STOP-6 | Source reports open write handle, lock, or in-use at `T_precopy` | Skip the entry with reason `source_in_use`; route to review. Not a retry. | blocked |
| STOP-7 | `link_count > 1` and the adapter cannot enumerate the full link set | Block the entry. Copying would silently multiply the file. | blocked |
| STOP-8 | Hard-link set member selected for retirement while other members are unaccounted for | Block retirement of the entire set. | blocked |
| STOP-9 | Case-only collision at a case-insensitive destination | Route to review. Versioning and skip strategies are prohibited. | blocked |
| STOP-10 | Normalization collision at destination | Route to review. No auto-resolution. | blocked |
| STOP-11 | Confusable collision detected | Route to review with both raw byte sequences displayed. | blocked |
| STOP-12 | Adapter declares `filename_transform: normalizing` and a destination filename read-back differs in raw bytes from what was written | Fail the entry. Report the transform. Do not mark verified. | blocked |
| STOP-13 | `raw_path_encoding` is `utf8_lossy` | Soft at inventory; blocked for any operation until review. | soft → blocked |
| STOP-14 | Symlink whose target escapes an approved root, selected for any operation | Fail the entry. Never follow. | fatal |
| STOP-15 | Connection loss, remount, or reconnect during a batch | Stop the batch. Invalidate in-flight tokens. Resume only after fresh root-identity confirmation. | blocked |
| STOP-16 | Measured adapter capability descriptor differs from the descriptor recorded in the approved plan | Stop the batch. The plan's preservation assumptions no longer hold. | fatal |
| STOP-17 | `identity_confidence` is `advisory` or lower and the operation would authorize source retirement | Block retirement. Requires an explicit, separately recorded operator waiver. | blocked |
| STOP-18 | `content_identity_state` is not `hashed_stable` and the record is used as duplicate or verification evidence | Reject the evidence. Route to review. | blocked |

## Relationship to other specifications

- `docs/02-specification/inventory-model.md` — field obligations, including the definitive obligation table
- `docs/02-specification/preservation-model.md` — what must survive a copy, and why hash equality is insufficient
- `docs/02-specification/duplicate-model.md` — hard-link sets are excluded from duplicate grouping
- `docs/02-specification/durability-and-recovery-model.md` — token capture points are journalled
- `docs/03-architecture/adapter-architecture.md` — capability descriptors
