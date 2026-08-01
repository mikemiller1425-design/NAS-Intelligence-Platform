# ADR 004: Cryptographic hashes for exact duplicates

Status: Accepted (foundation candidate)

## Context
Exact duplicate detection must be reliable enough to support safety decisions. Name, size, and timestamp alone are not sufficient.

## Decision
Use cryptographic hashes as the evidence for exact duplicate identification and copy verification.

## Consequences
This gives deterministic duplicate detection and verifiable post-copy content validation. Hashing can be compute-intensive on large corpora, so the Mac mini is the primary worker. The same approved hash family serves three purposes that must not be conflated: exact-duplicate identification, post-copy **content** verification, and content-addressed binding of plans, evidence bundles, rule sets, taxonomy versions, and journal records. Resolving OD-004 therefore also fixes the approval-binding and journal-chain algorithm. Hash equality verifies content only; preservation is verified separately.

## Alternatives considered
Heuristic duplicate matching based on filenames or metadata only.
