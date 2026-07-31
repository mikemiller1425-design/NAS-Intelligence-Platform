# Permission Model

## Purpose

The permission model defines authority boundaries for the Mac mini engine, the Raspberry Pi sentinel, human operators, and any future adjunct services.

The goal is least privilege with explicit approval gates. The permission model is intentionally stricter than the eventual implementation should be, because V1 must remain safe under audit and rollback.

## Authority tiers

### Human operator

Final authority for:

- taxonomy approval
- sensitive identity policy
- rule activation
- plan approval
- live pilot authorization
- exception handling
- rollback authorization
- cleanup policy

### Mac mini engine

Allowed to:

- inventory
- fingerprint
- extract metadata
- evaluate rules
- draft plans
- queue review items
- execute approved entries
- verify results
- reconcile runs

### Raspberry Pi sentinel

Allowed to:

- read health signals
- report status
- alert the operator
- request pre-approved safe jobs

Not allowed to:

- classify
- approve
- move or delete files
- choose destinations
- execute arbitrary shell or dashboard commands

### Future read-only observers

May inspect reports or health outputs if explicitly granted read-only access.

## Permission classes

- `read_inventory`
- `read_reports`
- `read_health`
- `propose_classification`
- `review_classification`
- `approve_classification`
- `approve_plan`
- `execute_plan`
- `verify_plan`
- `manage_rules`
- `manage_taxonomy`
- `manage_journal`
- `manage_alerts`
- `manage_reconciliation`

## Credential classes

### Discovery credentials

Used for read-only scanning and inventory.

### Mutation credentials

Used for approved copy, move, quarantine, or rename operations.

### Monitoring credentials

Used for health checks, status pages, and alerting.

### Admin credentials

Reserved for controlled setup and policy changes, ideally only through the operator.

## Permission rules

1. Discovery credentials must not be able to mutate source bytes.
2. Mutation credentials must only act on approved plan entries.
3. Monitoring credentials must not authorize filesystem operations.
4. Admin privileges must be narrowed by role and scope whenever possible.
5. Secret values must not be stored in Git.
6. Credentials must be separable by environment and purpose.

## File and path permissions

Path permissions are evaluated before any write operation.

Rules:

- normalize all paths before validation
- reject traversal outside approved roots
- reject absolute paths that point outside the authorized namespace
- reject symlink escapes unless specifically and safely handled
- treat synthetic fixture roots and live roots separately

## Approval permissions

Approval may be granted only when:

- the subject is in a reviewable state
- the approver has authority for the subject class
- the evidence bundle is present
- the approval scope is explicit

Approval may not be inferred from:

- a rule match
- an alert
- a status page
- a queue position

## Sentinel restrictions

The sentinel is intentionally limited to observation and safe requests because it is not the system of record.

It must never:

- classify content
- overwrite approval state
- emit mutation commands
- hold sole authority over operational truth

## V1 limits

- No shared superuser account for the whole workflow.
- No credential reuse between discovery and mutation if practical separation is possible.
- No permission path that lets the sentinel gain mutation authority.
- No permission that permits live deletion in V1.

