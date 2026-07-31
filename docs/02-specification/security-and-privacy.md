# Security and Privacy

## Purpose

This document specifies the security and privacy constraints for the NAS Intelligence Platform. The platform handles potentially sensitive file names, paths, metadata, thumbnails, OCR text, and identity-adjacent signals, so the default posture must be local-first, least-privilege, and audit-aware.

## Security principles

1. Least privilege by default.
2. Read-only discovery is separated from mutation-capable execution.
3. Secrets do not live in Git.
4. Untrusted inputs must be normalized and validated before use.
5. AI output is untrusted until validated.
6. The Raspberry Pi sentinel is not an authority to mutate content.
7. No shell interpolation of untrusted paths.
8. No silent overwrite.
9. No permanent deletion in V1.

## Credential model

### Discovery credentials

Used for inventory and read-only inspection only.

### Mutation credentials

Used only for approved copy, move, quarantine, or rename operations.

### Monitoring credentials

Used for health checks, alert delivery, and status reporting.

### Admin credentials

Used sparingly for configuration and policy changes.

## Secret handling

- Store secrets outside Git.
- Do not print secrets in reports or logs.
- Do not embed credentials in examples.
- Rotate secrets according to operator policy.
- Keep live and fixture credentials strictly separate.

## Path safety

Every input path must undergo:

1. normalization
2. root validation
3. traversal check
4. symlink policy check
5. collision check
6. final approved-root confirmation

Traversal prevention rules:

- reject `..` escapes
- reject absolute paths outside approved roots
- reject unexpected symlink jumps unless explicitly handled
- treat normalized and raw paths separately in audit output

## Filename safety

Hostile filenames may include:

- shell metacharacters
- control characters
- Unicode confusables
- extremely long segments
- reserved device names
- deceptive extensions

Handling rules:

- never interpolate raw filenames into shell commands
- sanitize display output
- preserve original filenames in audit logs when safe
- store normalized forms separately from raw forms

## Metadata privacy

The following metadata categories should be treated as sensitive by default:

- thumbnails
- extracted text
- GPS coordinates
- face or person hints
- device identifiers
- camera or drone identifiers
- OCR output
- file ownership details
- path history

Privacy handling:

- minimize extraction to what is necessary
- prefer local processing
- redact sensitive details in alerts and summaries
- require explicit policy for identity-adjacent analysis

## Sensitive identity handling

Identity-adjacent classification is always provisional until explicitly approved.

Requirements:

- explicit operator policy
- human confirmation when matching identity intent
- separate review queues for sensitive content
- no automatic publication or renaming based on identity guess alone

The example intent around `Voss` remains provisional and must not be treated as confirmed identity policy without a separate decision.

## AI and external tool safety

- Treat AI output as advisory only.
- Validate AI-derived paths before use.
- Sanitize all external output before it becomes a file path, command, or approval hint.
- Do not allow an external model to override deterministic rules or operator policy.

## Logging and redaction

Logs should include enough evidence for audit without leaking sensitive content.

Redaction should cover:

- secrets
- full private paths when not needed
- file contents
- thumbnails
- identity-related labels where not necessary

## Sentinel security

The sentinel should authenticate only to approved read-only or request-only interfaces.

It must not:

- store primary operational secrets
- receive mutation credentials
- execute arbitrary dashboard commands
- rewrite authoritative state

## Incident posture

Security incidents include:

- unexpected path traversal
- unauthorized mutation attempt
- secret exposure
- proof of overwrite risk
- hash mismatch after copy
- suspicious identity classification request
- sentinel authority creep

When an incident occurs, the system should stop mutation, record evidence, and require operator review.

## V1 limits

- No live NAS credentials in repository files.
- No permanently destructive operation.
- No unreviewed identity automation.
- No external AI output may be trusted without validation.
- No security model element may grant the sentinel mutation authority.

