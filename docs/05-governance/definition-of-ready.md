# Definition of Ready

Readiness is **per gate**. A gate is ready only when its own entry criteria are met and the previous gate has a signed authorization record.

**Readiness is not authorization, and readiness for one gate never implies readiness for the next.**

Gate IDs are defined in `docs/05-governance/gate-model.md` and match the `blocks_gate` values used in `docs/05-governance/open-decisions.md` and `docs/04-acceptance/`.

## Foundation ready (`foundation`, G1)

- Source material is in the repository and reconciled (`docs/migration/source-inventory.md`, `docs/migration/source-reconciliation.md`).
- Active documents exist for intent, product, specification, architecture, acceptance, governance, operations, migration, handoffs, future registry, and prompts.
- The independent foundation audit is recorded in `docs/audits/foundation-v1-audit.md` and every finding has a resolution status.
- Every requirement in `docs/04-acceptance/foundation-acceptance.md` and `docs/04-acceptance/safety-acceptance.md` passes by document inspection.
- Every entry in `docs/05-governance/open-decisions.md` carries a `blocks_gate` value, and none carries `blocks_gate: foundation`.
- The gate model is stated once, in `gate-model.md`, and referenced — not restated — elsewhere.

## Build Ladder ready (`build_ladder`, G2)

- A current Foundation authorization record exists.
- No open decision carries `blocks_gate: build_ladder`.
- The required rung list and per-rung field set of `docs/handoffs/003-build-ladder.md` are confirmed complete.
- The operator has separately authorized ladder generation. **Foundation approval alone is not sufficient.**

## Implementation ready — fixture-only, per rung (`implementation`, G3)

- A frozen Build Ladder exists and the specific rung ID is explicitly authorized.
- The rung's declared prerequisite rungs are complete and independently inspected.
- No open decision carries `blocks_gate: implementation` for this rung's subject matter.
- Synthetic fixtures for the rung exist or are within the rung's scope, and **no fixture derives from live NAS data**.
- The rung's `live NAS access in scope` field reads **no**.

## Dry-run ready (`dry_run`, G4)

- All rungs the dry run exercises are complete on fixtures and independently inspected.
- Source roots are confirmed (OD-001, OD-013) and read-only inventory scope is defined.
- Rule set and taxonomy versions are frozen (OD-002, OD-012) and validate against `config/schemas/classification-rule-set.schema.json`.
- One control-data root is approved and **proven disjoint** from every NAS mount, source root, destination root, and recursive scan boundary (OD-005, OD-014). Uncertainty about overlap is a stop, not a warning.
- Read-only credentials are issued and are distinct from any mutation-capable credential.
- Adapter selection is resolved for the environment in use (OD-016).
- Identity handling and derived-artifact retention policies are resolved (OD-003, OD-011), or the corresponding features are provably disabled.
- No open decision carries `blocks_gate: dry_run`.

## Pilot ready (`pilot`, G5)

- A current dry-run authorization record exists and its output has been reviewed by the operator.
- Fixture tests pass.
- The pilot dataset is selected, copied, and isolated in a non-authoritative zone (OD-007).
- Batch-size and stop thresholds are set for the pilot (OD-008).
- Rollback steps are written, checked, and drillable **before** the first pilot write.
- Preservation-fidelity comparison reporting exists and passes on fixtures.
- No open decision carries `blocks_gate: pilot`.

## Live ready (`live`, G6)

- A current pilot authorization record exists and all BLOCKER rows of `docs/04-acceptance/pilot-acceptance.md` are green.
- All BLOCKER rows of `docs/04-acceptance/live-readiness.md` are green.
- Snapshot or equivalent recovery coverage is documented and confirmed (OD-006).
- Exact source and destination roots are confirmed for this batch (OD-001, OD-013, OD-015).
- Copy-versus-move behavior for this phase is frozen (OD-009).
- Batch thresholds are calibrated and approved for live volumes (OD-008).
- Source retirement is disabled in the plan flags for this batch.
- No open decision carries `blocks_gate: live`.

## Retirement ready (`retirement`, G7)

- A current live authorization record exists and the batch's live evidence is green.
- Every candidate item has a verified destination copy with matching hash and size.
- Preservation-fidelity comparison passed for every candidate item. **Hash equality alone is not sufficient** — see `docs/02-specification/preservation-model.md`.
- Quarantine retention and cleanup policy are approved (OD-010).
- A per-batch retirement approval record exists, bound per `docs/02-specification/approval-binding-model.md`, naming the items and the retention policy version.
- Permanent deletion remains unavailable; retirement is retention, not removal.
- No open decision carries `blocks_gate: retirement`.

## Migration completion ready (`migration_completion`, G8)

- Every in-scope source item has a final disposition: organized, retained, quarantined, unresolved, or failed.
- Reconciliation totals balance against the baseline inventory.
- Residual exceptions are enumerated with named owners and are not hidden inside aggregate counts.
- Completion criteria and residual-exception tolerance are agreed (OD-021).
- No open decision carries `blocks_gate: migration_completion`.
