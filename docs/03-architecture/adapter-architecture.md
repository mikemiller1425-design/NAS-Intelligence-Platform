# Adapter Architecture

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
