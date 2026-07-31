# Git Policy

## Rules
- Do not commit secrets, credentials, tokens, or private infrastructure details.
- Keep blueprint changes reviewable and documented.
- Prefer small, versioned commits for discrete blueprint updates.
- Never use Git to authorize live data actions.
- Do not rewrite committed history unless explicitly directed.

## Branching and review
- Work on a focused branch for blueprint updates.
- Keep handoff and audit artifacts versioned alongside the docs they reference.
- Separate implementation from blueprint-only preparation.

## Output hygiene
- Avoid paths, hostnames, usernames, or share names that are not approved for the repository.
- Do not encode operational secrets in examples.
