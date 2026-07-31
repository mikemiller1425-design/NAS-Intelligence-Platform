# ADR 004: Cryptographic hashes for exact duplicates

Status: Accepted (foundation candidate)

## Context
Exact duplicate detection must be reliable enough to support safety decisions. Name, size, and timestamp alone are not sufficient.

## Decision
Use cryptographic hashes as the evidence for exact duplicate identification and copy verification.

## Consequences
This gives deterministic duplicate detection and verifiable post-copy validation. Hashing can be compute-intensive on large corpora, so the Mac mini is the primary worker.

## Alternatives considered
Heuristic duplicate matching based on filenames or metadata only.
