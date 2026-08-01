# scripts

Operator and maintenance scripts placeholder. Keep helper scripts small, explicit, and safe by default.

## Available now

| Script | Purpose |
| --- | --- |
| `check_path_policy.py` | Enforces `docs/05-governance/path-policy.md` by artifact class: secrets forbidden everywhere, literal live paths forbidden in runtime surfaces, declared inert-evidence exemptions. `--self-test` proves all five required policy tests in both directions. |
| `validate_build_ladder.py` | Validates the Build Ladder as a planning artifact: unique and contiguous rung IDs, dependency resolution, acyclicity, required-field completeness, acceptance and open-decision coverage, canonical gate numbering, and the safety invariant that no G3 rung declares NAS access. |
| `foundation_self_review.py` | 24 checks over the audit-resolution state: finding coverage, schema validity, provisional-rule safety, gate-wording consistency, persistence authority, approval binding, preservation language, placeholders, secrets, link resolution, Sentinel scope, live-access prohibition, Build Ladder status, and event-vocabulary parity. Re-runnable evidence for an independent verifier. |
| `validate_rule_config.py` | Validates the canonical rule schema, every rule set under `config/rules/`, and every negative fixture. Includes the loader checks JSON Schema cannot express. |
| `generate_negative_rule_fixtures.py` | Regenerates `tests/fixtures/rules/negative/` from the canonical positive example. |

Requires `pyyaml` and `jsonschema`. Neither is committed as a dependency; install them into a throwaway environment to run these checks.

All five read files only. None performs NAS access, and none mutates anything outside `tests/fixtures/rules/negative/`.

## Status
Blueprint placeholder.

## Planned contents
- Design notes and future implementation guidance.
- No production logic yet.
- Keep behavior aligned with the architecture docs and ADRs.
