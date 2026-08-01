# Definition of Done

"Done" is scoped to an artifact **and** the gate it belongs to.

**Done never means authorized.** A completed artifact at gate *N* is evidence submitted toward *considering* gate *N+1*, nothing more. Gate IDs are defined in `docs/05-governance/gate-model.md`.

## Universal done criteria (all gates)

- The artifact is written and linked from the correct section of the repository.
- The artifact does not authorize anything beyond its own gate, and says so explicitly.
- Provisional content is labeled provisional until the operator confirms it.
- Open decisions are captured in `docs/05-governance/open-decisions.md` with a `blocks_gate` value, never left implicit.
- The evidence named by the artifact is realistically collectable and conforms to `docs/05-governance/evidence-standard.md`.
- The artifact is understandable without chat history.

## Done for a Foundation document (`foundation`, G1)

- At least one acceptance requirement in `docs/04-acceptance/foundation-acceptance.md` can test it by inspection.
- It does not contradict any higher-authority document per `docs/05-governance/authority-order.md`.
- It states no destructive action without naming its approval and verification steps.
- It does not contradict `docs/source/` without recording the conflict.
- It references the one authoritative contract for its subject rather than restating it in a second form.

## Done for the Build Ladder (`build_ladder`, G2)

- Every rung has a stable ID and all fields required by `docs/handoffs/003-build-ladder.md`.
- Every rung's `live NAS access in scope` field is answered, and defaults to **no**.
- No rung bundles work that a later gate must authorize separately.
- The ladder is marked frozen and planning-only.

## Done for an implementation rung (`implementation`, G3)

- Only the named rung's files changed.
- Every `V1-ACC-*` row carrying `Gate = implementation` within the rung's scope passes on synthetic fixtures.
- No test, config, default, or fixture references a NAS path, mount, hostname, credential, or share name.
- The rung's evidence package is complete and hashed.
- An independent rung inspection verdict exists per `prompts/independent-rung-inspection.md`.
- Remaining blockers are stated, not deferred silently.

## Done for a dry run (`dry_run`, G4)

- Inventory manifest, dry-run plan, rule coverage report, conflict report, unresolved queue, and hashed evidence index all exist.
- A repeated scan demonstrates deterministic identity and zero source mutation.
- No filesystem write occurred anywhere outside control-data storage.
- Every stop condition in `docs/06-operations/dry-run-playbook.md` was evaluated, and none was silently passed.

## Done for a pilot (`pilot`, G5)

- All BLOCKER rows of `docs/04-acceptance/pilot-acceptance.md` are green; MAJOR rows are green or waived in governance.
- The rollback drill was executed and evidenced.
- Preservation-fidelity comparison reports exist for the pilot corpus.
- Originals are provably untouched.
- Exceptions are recorded with remediation items, not summarized away.

## Done for a live batch (`live`, G6)

- The batch executed exactly the approved immutable plan version.
- Preconditions were revalidated immediately before action.
- Every copied item is hash-verified.
- Journal and checkpoint entries are complete and append-only.
- No source item was retired, and no protected vault was overwritten.

## Done for a retirement action (`retirement`, G7)

- Every retired item has a named, verified destination copy.
- Preservation-fidelity comparison passed, not hash equality alone.
- A per-batch retirement approval record and retention policy version are attached.
- Nothing was permanently deleted.
- The action is reversible from evidence, or its irreversibility was explicitly approved in advance.

## Done for migration completion (`migration_completion`, G8)

- Reconciliation balances and every in-scope item has a final disposition.
- The exception inventory is published with owners.
- Final baseline manifests and the archive index are preserved.
- No maintenance automation was enabled as a side effect.

## Not done (any gate)

- An unresolved decision is left implicit or lacks a `blocks_gate` value.
- A destructive action is described without approval and verification.
- A helper document contradicts the source manual or a higher-authority document without recording the conflict.
- The artifact's language could be read as authorizing the next gate.
- Evidence is asserted rather than attached.
