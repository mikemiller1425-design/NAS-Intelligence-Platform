# Configuration examples (NON-PRODUCTION)

All files under `config/` are **illustrative only**.

- Paths use synthetic fixtures such as `/fixtures/source/` and `/fixtures/destination/`.
- No credentials, private filenames, or live NAS IPs belong here.
- Rules marked `provisional` require operator confirmation before any engine evaluation against real data.
- Dry-run remains the default in all examples.
- These files are not production classifiers and must not be pointed at live shares by default.

## Layout

| Path | Purpose |
| --- | --- |
| `rules/` | Example classification rules |
| `taxonomy/` | Example destination taxonomy |
| `exclusions/` | Example inventory exclusions and protected destinations |
| `examples/` | Thresholds, dry-run settings, fake source roots |

## Safety

```text
live_mode: false
dry_run_default: true
allow_source_retirement: false
allow_overwrite_protected_vaults: false
```
