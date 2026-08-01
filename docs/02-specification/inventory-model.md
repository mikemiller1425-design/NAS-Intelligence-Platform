# Inventory Model

## Purpose

The inventory model defines how the platform discovers, records, resumes, and reconciles files and directories. Inventory is read-only, repeatable, and provenance-preserving.

The inventory layer is the base of every later workflow. If an item is not inventoried correctly, it cannot be safely classified or executed.

## Inventory scope

The system may inventory:

- files
- directories
- symlinks, if explicitly allowed
- unreadable entries, as exceptions
- synthetic fixture trees

The system must not modify source bytes, rename source objects, or infer authority from a single pass.

## Canonical inventory fields

This table is the **single authority** for inventory field obligations. It resolves audit finding **FND-m004**, which was raised because three documents described the field set with three different obligations: the domain model listed them as required, this document listed them as "when available", and the data architecture listed a shorter informal set.

Stage abbreviations follow `lifecycle-model.md`: **D** discovered, **I** inventoried, **F** fingerprinted, **M** metadata extracted.

"Adapter-conditional" means the obligation depends on a *measured* adapter capability descriptor, never on an assumption. A value the adapter cannot supply is recorded as `unavailable` — never as `null`, `0`, or an omitted key.

| # | Field | Type | Nullable | Required at | Adapter-conditional notes |
| --- | --- | --- | :---: | :---: | --- |
| 1 | `logical_file_id` | opaque string | no | D | Assigned once; never derived from path. |
| 2 | `source_root_id` | ref | no | D | — |
| 3 | `raw_path_bytes` | byte string | no | D | Canonical for all I/O. Byte-transparent on local, NFS, and SFTP; **normalizing on SMB**. |
| 4 | `raw_path_encoding` | enum | no | D | `utf8_lossy` routes to review. |
| 5 | `relative_path` | string | no | D | Derived; display and index only. |
| 6 | `normalized_path` | string | no | I | Index key only. **Never used to open a file.** |
| 7 | `normalization_profile` | ref | no | I | `NP/1` in V1. |
| 8 | `nfc_form` | enum | no | I | Critical for macOS-to-Synology transfers. |
| 9 | `case_form_observed` | enum | no | I | Compared against the destination's case sensitivity. |
| 10 | `entry_type` | enum | no | D | `file`, `directory`, `symlink`, `bundle`. |
| 11 | `size_bytes` (apparent) | integer | no | D | Advisory grade on vendor APIs. |
| 12 | `allocated_bytes` | integer | yes | I (best effort) | Unavailable on SFTP and vendor APIs. Required to detect sparse files. |
| 13 | `discovered_at` | timestamp | no | D | System time, not file time. |
| 14 | `mtime_ns` | integer | yes | I | Nanosecond on local, SMB, NFSv4; **one-second on SFTP v3 and vendor APIs**. |
| 15 | `mtime_resolution_ns` | integer | no | I | From the capability descriptor; drives indeterminate change-token results. |
| 16 | `ctime_ns` | integer | yes | I (best effort) | Unavailable on SFTP and vendor APIs. Never settable. |
| 17 | `birthtime_ns` | integer | yes | I (best effort) | Unavailable on NFSv3, SFTP, vendor APIs. |
| 18 | `atime_ns` | integer | yes | I (best effort) | Recorded, but intentionally normalized on copy. Reading may mutate it. |
| 19 | `object_identity_key` | opaque | yes | I | Authoritative on local POSIX; advisory on SMB and NFS; **unavailable on SFTP and vendor APIs**. |
| 20 | `object_identity_grade` | enum | no | I | Never omitted; absence is recorded as `unavailable`. |
| 21 | `volume_identifier` | opaque | yes | I | Inherited from the root. |
| 22 | `link_count` | integer | yes | I | Unavailable on SMB, SFTP, vendor APIs → `hardlink_detection: unavailable`. |
| 23 | `hardlink_set_id` | ref | yes | I (conditional) | Non-null only when link count is above one and detectable. |
| 24 | `symlink_target_raw` | byte string | yes | I (conditional) | Required when `entry_type` is `symlink`. |
| 25 | `change_token` | struct | no | I | Composite; recomputed at five journalled points. |
| 26 | `identity_confidence` | enum | no | I | The **minimum** across components, never the maximum. Capped at `advisory` for SFTP and vendor APIs. |
| 27 | `inventory_state` | enum | no | D | Per `lifecycle-model.md`. |
| 28 | `content_identity_state` | enum | no | D | `unhashed` at discovery. Only `hashed_stable` is valid duplicate or verification evidence. |
| 29 | `path_authority` | enum | no | D | Same vocabulary as `SourceRoot.authority`. |
| 30 | `posix_mode` | integer | yes | M (best effort) | Unsupported for write on vendor APIs. |
| 31 | `owner_uid`, `group_gid` | integer | yes | M (best effort) | Unavailable on SMB and vendor APIs. |
| 32 | `acl_present`, `acl_payload_ref` | boolean, ref | yes | M (best effort) | Unsupported on SFTP. SMB carries NT ACLs, which are **not** POSIX-equivalent. |
| 33 | `xattr_keys`, `xattr_payload_ref` | list, ref | yes | M (best effort) | Unsupported on SFTP, vendor APIs, and NFSv3. |
| 34 | `has_resource_fork`, `has_finder_info` | boolean | yes | M (best effort) | Unsupported off local POSIX. |
| 35 | `bsd_flags` | integer | yes | M (best effort) | Unsupported off local POSIX. |
| 36 | `is_sparse` | boolean | yes | M (best effort) | Derived from apparent versus allocated size; unavailable where allocated size is null. |
| 37 | `bundle_manifest_digest` | string | yes | F (conditional) | Required when `entry_type` is `bundle`. |
| 38 | `error_state` | enum | yes | D | — |
| 39 | `retry_count` | integer | no (default 0) | D | — |
| 40 | `superseded_by_logical_file_id` | ref | yes | I (conditional) | Set on same-path replacement. |
| 41 | `updated_at` | timestamp | no | D | — |

### Fields resolved by reference, not stored on the record

These were previously listed as inventory fields. They belong to other entities and are resolved by reference, so that no fact has two homes:

| Concept | Authoritative home |
| --- | --- |
| Content hash and hashes | `HashRecord` |
| MIME type, extension, media, document, and structured-data metadata | `MetadataRecord` |
| Current classification state | `ClassificationDecision.decision_state` |
| Current review state | `ReviewItem.review_state` |
| Planned operation references | reverse of `OperationEntry.file_record_id` |

### Obligation rules

1. A field marked required at a stage must be present once that stage completes. Absence is an error, not an omission.
2. A nullable field must be present as an explicit `unavailable` when the adapter cannot supply it. Silence and `null` are not equivalent to `unavailable`.
3. Best-effort fields are captured when readable and reported when not. They are never silently dropped.
4. No field in this table may be redefined with a different obligation in another document. Where another document appears to do so, this table governs.

## Known, intended, and unresolved path context

Every inventory source and destination path must carry one of the following authority tags:

- `confirmed_live`: validated against observed or approved live structure.
- `intended_structure`: part of the blueprint’s proposed control model.
- `unresolved_assumption`: not yet confirmed and not safe for execution.

Inventory records should preserve this distinction explicitly so that live paths, intended paths, and assumptions never collapse into one another.

## Inventory phases

### 1. Discovery

The engine enumerates source entries under approved roots and creates provisional identifiers.

Output:

- `discovered` file records
- source totals
- path normalization warnings
- unreadable or skipped entries

### 2. Registration

The engine persists stable file identities, source roots, and first-seen facts.

Output:

- `inventoried` file records
- source manifest entries
- control checksums for manifests or checkpoints

### 3. Fingerprinting

The engine calculates approved hashes for exact duplicate detection and verification.

Output:

- `HashRecord` entries
- hash algorithm metadata
- mismatch warnings

### 4. Metadata extraction

The engine extracts filesystem, media, document, or structured-data metadata without altering the source.

Output:

- `MetadataRecord` entries
- validation flags
- extraction failures when parsing is partial

### 5. Analysis

The engine derives classification evidence and produces reviewable proposals.

Output:

- rule-evaluation inputs
- analysis artifacts
- review queues for low-confidence items

## Inventory rules

1. Inventory must be repeatable from the same inputs.
2. A resumed scan must not duplicate file identities.
3. Partially written records must be recoverable or safely ignored.
4. The same source item may be inventoried more than once, but it must not become multiple logical files.
5. Read-only inventory does not authorize plan approval.
6. The presence of a file in inventory does not imply it may be moved.
7. Hashing and metadata extraction may occur in any order that preserves immutability and auditability.

## Inventory outputs

### Manifests

Inventory emits manifest records suitable for audit and reconciliation.

Manifests should include:

- total entries
- total bytes
- source root coverage
- unreadable count
- duplicate count
- unresolved count
- confidence distribution
- checkpoint cursor

### Review queue

Items that lack strong evidence, contain policy-sensitive identity signals, or conflict with other evidence are routed to review.

### Reconciliation inputs

Inventory creates baseline data for later reconciliation:

- source totals by root
- path coverage
- exact-duplicate groups
- exception counts
- unstable or missing metadata counts

## Error handling

Inventory errors are classified as:

- `soft`: record the problem and continue.
- `blocked`: stop the batch and wait for operator intervention.
- `fatal`: stop the run and mark the item or run failed.

Examples:

- unreadable file name encoding: `soft`
- traversal outside approved roots: `fatal`
- source mount loss: `blocked` or `fatal` depending on context
- hash mismatch on an immutable file: `blocked`

## V1 limits

- Inventory is read-only and cannot choose destinations.
- Inventory does not infer sensitive identity without explicit policy.
- Inventory validation **must be restricted to** synthetic fixtures until the dry-run gate (G4) is authorized. No live path may be traversed before then.
- Inventory does not create or mutate live NAS credentials or mounts.

