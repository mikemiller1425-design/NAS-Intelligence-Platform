# Path and Secret Policy

The single authoritative, machine-testable policy governing where NAS-shaped paths, share names, and credential-shaped values may appear in this repository.

It exists because the previous rule — "no NAS path, mount, hostname, share name, or credential anywhere" — was unsatisfiable. The approved repository intentionally contains `/volume1` references in specifications and migration history, and deliberately invalid negative fixtures whose whole purpose is to contain a literal live path and prove it is rejected. A scanner enforcing the old rule would have failed its own baseline, or forced an implementer to delete authoritative evidence or add undocumented exclusions.

This policy replaces that rule everywhere. It is enforced by `scripts/check_path_policy.py`.

## The three artifact classes

### Class A — Secrets. Forbidden everywhere, no exemption

Credentials, passwords, tokens, API keys, private keys, session secrets, private hostnames, and private IP addresses are forbidden in **every committed artifact without exception**.

**No exemption mechanism exists for Class A.** An exemption entry naming a Class A pattern is itself a policy violation. This class is not weakened by anything below.

### Class B — Runtime and executable surfaces. Literal live paths forbidden, no exemption

A **literal live NAS path or share target** must not appear in:

| Surface | Roots |
| --- | --- |
| Executable code | `packages/`, `apps/`, `scripts/`, `tools/` |
| Production and default configuration | `config/` — except the declared negative-fixture roots below |
| Positive fixtures | `tests/` — except the declared negative-fixture roots below |
| Generated artifacts | plans, commands, adapter inputs, manifests, and any runtime output |

**Class B admits no exemptions.** This is structural, not procedural: a scanner or generator that needs to know a forbidden pattern **reads it from this document at runtime** rather than embedding a literal. That is why `scripts/check_path_policy.py` and `scripts/generate_negative_rule_fixtures.py` contain no literal live path even though both operate on them.

Consequently there is no path by which an executable artifact can be exempted — the exemption table below is validated to contain no Class B path, and a violation of that rule fails the check.

### Class C — Inert evidence. Literal patterns permitted, narrowly and by declaration

Approved specification, intent, governance, audit, and migration documents, and deliberately invalid negative fixtures, may contain a literal live path **solely** to document intended structure or to prove that such a path is rejected.

Class C material is inert: it is never loaded as configuration, never executed, and never supplies a runtime input.

## Declared Class C exemptions

Every exemption is narrow, declared here, and reviewable. An exemption grants **only** relief from Class B's literal-path rule. It never grants relief from Class A.

| Path | Why literal patterns are required | Reviewed |
| --- | --- | --- |
| `docs/00-intent/` | Glossary defines a share as an intended `/volume1` root. | Foundation 1.0 |
| `docs/02-specification/` | The taxonomy model documents known intended share names. | Foundation 1.0 |
| `docs/05-governance/` | Open decisions and this policy quote the patterns they govern. | Foundation 1.0 |
| `docs/migration/` | Source inventory, reconciliation, and traceability record the intended live structure as historical evidence. | Foundation 1.0 |
| `docs/audits/` | Audit and verification records quote the wording they assess. | Foundation 1.0 |
| `docs/handoffs/` | The Build Ladder quotes the patterns its rungs must reject. | G2 |
| `docs/source/` | Immutable operator source material. Never edited. | Foundation 1.0 |
| `tests/fixtures/rules/negative/` | Deliberately invalid rule sets that must contain an absolute live destination in order to prove the schema rejects it. | Foundation 1.0 |

Any other path containing a literal live NAS path is a violation.

## Forbidden pattern registry

Scanners read these from this table so that no executable artifact contains a literal. Adding a pattern here extends enforcement everywhere at once.

### Live path patterns (Class B)

| Pattern | Kind |
| --- | --- |
| `/volume1` | Synology volume root |
| `smb://` | SMB URL |
| `nfs://` | NFS URL |
| `afp://` | AFP URL |
| `ssh://` | SSH URL |
| `//192.168.` | Private network UNC prefix |

### Secret patterns (Class A)

| Pattern | Kind |
| --- | --- |
| `AKIA[0-9A-Z]{16}` | Cloud access key id |
| `-----BEGIN [A-Z ]*PRIVATE KEY-----` | Private key block |
| `(password\|passwd\|secret\|api[_-]?key\|token)\s*[:=]\s*['"]?[A-Za-z0-9/+_-]{12,}` | Assigned credential value |

## Required tests

`scripts/check_path_policy.py --self-test` proves all five, in both directions. A policy that can only pass proves nothing.

1. **A forbidden runtime reference fails.** A literal live path planted in a Class B surface is rejected.
2. **Credentials always fail.** A credential-shaped value is rejected even in a Class C path, where literal live paths are permitted.
3. **Approved inert references do not make the baseline impossible.** The repository as it stands passes.
4. **Deliberately invalid negative fixtures remain testable.** The negative fixtures still contain literal live paths, and the rule validator still rejects them for that reason.
5. **An exemption for executable code fails.** Adding a Class B path to the exemption table is rejected as structurally invalid.

## Relationship to the gate model

This policy governs the **repository**. It is distinct from, and does not relax, the gate model's rules about what the running system may touch:

- No gate before G4 permits any NAS access at all.
- G4 permits read-only access to NAS data paths, plus writes confined to one approved local control-data root.
- Nothing in this policy authorizes an adapter, a configuration default, or a runtime input to name a live path. Class B forbids exactly that, without exemption.

## Related documents

- `docs/05-governance/gate-model.md`
- `docs/05-governance/definition-of-done.md`
- `docs/05-governance/git-policy.md`
- `docs/02-specification/security-and-privacy.md`
- `docs/handoffs/build-ladder.md` — FBL-001 implements this policy
