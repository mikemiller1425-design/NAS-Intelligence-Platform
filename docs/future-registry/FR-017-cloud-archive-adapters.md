# FR-017 — Cloud archive adapters

## Purpose
Archive selected cold data to cloud object storage while preserving manifests.

## Dependencies
Cloud credentials outside Git; encryption policy; irreversible-loss protections.

## Risks
Accidental cloud upload of private media; credential leakage; treating cloud copy as verified without hash checks.

## Reason excluded from V1
Assignment excludes cloud upload and broad external sharing from V1.

## Promotion condition
Explicit operator policy; encrypted transfer; hash verification; private vaults opt-in only.
