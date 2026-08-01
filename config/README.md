# Configuration examples (NON-PRODUCTION)

All files under `config/` are **illustrative only**.

- Paths use synthetic fixtures such as `/fixtures/source/` and `/fixtures/destination/`.
- No credentials, private filenames, or live NAS IPs belong here.
- Rules marked `provisional` are **structurally advisory-only**: the canonical schema makes it impossible for a provisional rule to express an automatically approved or executable outcome, and validation rejects any configuration that tries. Promotion out of provisional is an operator decision (OD-012, OD-003).
- Dry-run remains the default in all examples.
- These files are not production classifiers and must not be pointed at live shares by default.

## Layout

| Path | Purpose |
| --- | --- |
| `rules/` | Example classification rules |
| `taxonomy/` | Example destination taxonomy |
| `exclusions/` | Example inventory exclusions and protected destinations |
| `examples/` | Thresholds, dry-run settings, fake source roots |
| `schemas/` | **Canonical machine-readable contracts.** `classification-rule-set.schema.json` is the single authoritative rule contract. |

## Safety

```text
live_mode: false
dry_run_default: true
allow_source_retirement: false
allow_overwrite_protected_vaults: false
load_order_significance: none
```

## Validation

```bash
python3 scripts/validate_rule_config.py
```

This validates the canonical schema itself, validates every rule set under `config/rules/`, and
confirms that every negative example in `tests/fixtures/rules/negative/` is rejected for its
intended reason. Some constraints (unique rule ids, unique band/priority slots, single
unconditional rule, cross-file reference resolution) cannot be expressed in JSON Schema and are
enforced as named loader checks by the same script.
