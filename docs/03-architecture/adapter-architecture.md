# Adapter Architecture

> **Adapters publish measured capability descriptors.** Platform behavior is a function of what an
> adapter *demonstrates it can do*, not of which product it is. This is what lets implementation
> proceed against fixtures while the live adapter choice (OD-016) remains open.
>
> A descriptor covers identity evidence grades, preservation-property support, filename byte
> transparency, case and normalization sensitivity, timestamp resolution, access-time behavior, path
> limits, and a per-volume durability class. It is valid **only** if produced by an actual fixture
> characterization run; hand-written or assumed descriptors are invalid and may not gate any
> operation. The descriptor id is bound into every approved plan, and a mismatch at execution stops
> the batch.
>
> See `docs/02-specification/file-identity-model.md`,
> `docs/02-specification/preservation-model.md`, and
> `docs/02-specification/durability-and-recovery-model.md`.

## Purpose
Adapters isolate the platform from direct filesystem assumptions and keep low-level I/O behind explicit boundaries.

## Adapter Rules
- All filesystem access goes through adapters.
- The core domain does not talk directly to storage APIs.
- Adapter implementations may vary by source, destination, or environment.
- The frontend never bypasses the adapter layer to authorize mutation.

## Adapter Types
- Source filesystem adapters for read-only discovery.
- Destination adapters for approved copy targets.
- Verification adapters for post-copy comparison.
- Sentinel-facing adapters for monitoring and status gathering.

## Benefits
- Easier review of unsafe operations.
- Clear separation between domain logic and I/O behavior.
- Simpler testing through mockable boundaries.
- Stronger control over protected-vault policies and overwrite prohibitions.

## Design Constraint
Adapter interfaces must remain narrow and intention-revealing so the rest of the system cannot accidentally acquire unrestricted filesystem authority.
