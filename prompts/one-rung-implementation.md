# One Rung Implementation Prompt

## Role

Implement **exactly one** authorized rung from `docs/handoffs/build-ladder.md`.

## Preconditions — all must hold before any work begins

- A frozen Build Ladder exists (gate G2 complete).
- **This specific rung ID is explicitly authorized by the operator** at gate G3, recorded in `docs/05-governance/authorization-ledger.md`. Authorization of rung *N* never authorizes rung *N+1*.
- Every prerequisite rung named by this rung is complete and has passed independent inspection.
- No open decision listed in this rung's **Blocking open decisions** field is unresolved.
- The rung's **NAS access** field reads `none`.

If any precondition fails, stop and report. Do not proceed on the assumption that it will be satisfied later.

## Required inputs — the assignment must supply all of these

| Input | Why it is required |
| --- | --- |
| **Exact rung ID** | Scope is defined by the rung, not by judgement. |
| **Exact starting commit SHA** | So the diff is attributable and reviewable. |
| **Explicit authorization statement** | Naming the gate (G3) and this rung ID. |
| **Allowed scope** | Copied from the rung's *Allowed work* field. |
| **Prohibited scope** | Copied from the rung's *Prohibited work* field. |
| **Required tests** | Positive, negative, and failure-injection, from the rung. |
| **Required evidence** | Per `docs/05-governance/evidence-standard.md`. |

An assignment missing any of these is not a valid authorization. Ask for it rather than inferring it.

## Authority

- Implement only the named rung.
- Modify only files the rung's *Likely files affected* field anticipates, plus tests and evidence for that rung.
- Add only dependencies the rung explicitly names.

## Prohibitions

- Do not implement any other rung, including one that appears trivial or "already half done".
- Do not access, mount, scan, hash, or analyse any NAS path. Implementation is fixture-only at G3; live access is not available inside rung scope either.
- Do not use live NAS data as a fixture source.
- Do not reference a live path, hostname, share name, or credential in code, config, tests, or fixtures.
- Do not resolve an operator policy decision. If one blocks you, stop and report.
- Do not modify governance, acceptance, or specification documents. If the rung cannot be implemented as specified, that is a finding to report, not a document to edit.
- Do not weaken, skip, or mark pending any safety control to make a test pass.
- Do not authorize, imply, or prepare authorization for the following rung.

## Required output

- Summary of changes, file by file.
- Which acceptance IDs the rung addressed, and how each was verified.
- Test results: positive, negative, and failure-injection, each reported separately.
- The evidence package the rung requires.
- Remaining blockers, stated explicitly rather than deferred silently.
- A statement that no NAS was accessed.

## Stop condition

The rung is complete and ready for independent inspection.

**Stop after this rung.** Completing it authorizes nothing. The next rung requires its own operator authorization at G3, recorded in the ledger.
