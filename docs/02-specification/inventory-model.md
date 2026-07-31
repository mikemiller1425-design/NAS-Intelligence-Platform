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

Every `FileRecord` should capture, when available:

- stable `file_id`
- `source_root_id`
- absolute synthetic or approved source path
- normalized relative path
- entry type
- size in bytes
- discovered timestamp
- modified timestamp
- created timestamp when supported
- content hash status
- content hash or hashes
- inode or platform file identifier when useful
- permissions and ownership when readable
- MIME type and extension
- media metadata
- document metadata
- structured-data metadata
- error state
- retry count
- current classification state
- current review state
- planned operation references

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
- Inventory may rely on synthetic fixtures for validation until live authorization exists.
- Inventory does not create or mutate live NAS credentials or mounts.

