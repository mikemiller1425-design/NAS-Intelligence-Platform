# Duplicate Model

## Purpose

The duplicate model defines how the platform identifies exact duplicates, separates them from near duplicates, preserves provenance, and prepares reviewable recommendations without deleting data in V1.

## Duplicate categories

### Exact duplicates

Files with matching approved cryptographic hashes and equal size are exact duplicates, provided both carry a `hashed_stable` content identity.

> **Hard-link sets are not duplicate groups.** Where link count is authoritative and greater than one, the entries share a single underlying object. Grouping them as exact duplicates and copying them independently would silently multiply the file and destroy link topology, so within-set members are excluded from exact-duplicate grouping. Where link count is unavailable, the platform records `hardlink_detection: unavailable` and must not assert that no hard links exist. See `file-identity-model.md`.

> **Zero-byte files hash identically to one another.** Hash equality on a zero-length file is not redundancy evidence, and such files must not be collapsed into a redundancy recommendation.

> **Byte-identical files may still differ** in extended attributes, ACLs, and resource forks. Hash equality establishes content equivalence only; it never establishes that two entries are interchangeable. See `preservation-model.md`.

### Near duplicates

Files that are visually, structurally, or semantically similar but not byte-identical are near duplicates.

### Mixed groups

Some groups contain both exact and near-duplicate candidates. These groups require careful reporting and separate decisions per member.

## Core invariants

1. Exact duplicates are hash-backed.
2. Near duplicates are not equal to exact duplicates.
3. No duplicate decision authorizes deletion in V1.
4. Duplicate grouping preserves every original path.
5. A canonical choice never erases the alternative evidence.
6. Quarantine is preservation, not destruction.
7. Duplicate analysis is idempotent.
8. Duplicate results must remain explainable after reruns.

## Detection pipeline

### Stage 1: exact-byte identity

The engine compares approved hashes to form exact duplicate candidates.

### Stage 2: structural similarity

The engine may compare metadata such as dimensions, duration, codecs, filenames, or content fingerprints to identify near duplicates.

### Stage 3: human review

The engine presents groupings with evidence, confidence, and risk so an operator can decide what to retain, quarantine, or ignore.

## Group fields

Each `DuplicateGroup` should include:

- `group_id`
- `group_type`
- `canonical_file_record_id`
- `member_file_record_ids`
- `hash_fingerprint`
- `similarity_basis`
- `risk_level`
- `review_state`
- `recommendation`

## Canonical selection rules

Canonical selection is a recommendation, not an automatic command.

Preferred ordering for canonical candidates:

1. approved authoritative source
2. earliest verified copy when policy allows
3. most complete metadata
4. best destination alignment
5. operator override

This ordering may influence the recommendation, but it must not hide alternates or imply deletion.

## Exact duplicate workflow

1. Detect matching hashes.
2. Create a duplicate group.
3. Preserve all source paths.
4. Recommend canonical and redundant candidates.
5. Route redundant candidates to quarantine only if approved.
6. Verify counts and hashes after any approved action.
7. Record the outcome in the journal.

## Near-duplicate workflow

1. Detect similarity evidence.
2. Separate from exact-byte identity.
3. Record the similarity basis and confidence.
4. Route to manual review.
5. Do not treat near duplicates as safely interchangeable.

## Quarantine policy

Quarantine is a holding action for retained items that require cooling-off, exception handling, or later cleanup authorization.

Quarantine requirements:

- explicit approval
- stable provenance references
- no silent deletion
- separate storage from active library content when possible
- future cleanup remains a separate decision

## Conflict behavior

Duplicate handling conflicts are resolved by evidence and policy, not by size, recency, or convenience.

Examples of conflicts:

- same hash, different names
- visually similar but different bytes
- canonical candidate also matches a sensitive identity rule
- duplicate candidate belongs to an unresolved taxonomy branch

When conflict exists, the item must enter review rather than being collapsed into a single outcome.

## V1 limits

- No automatic near-duplicate deletion.
- No automatic exact-duplicate deletion.
- No quarantine-to-delete workflow in V1.
- No duplication logic may override approval or path safety rules.

