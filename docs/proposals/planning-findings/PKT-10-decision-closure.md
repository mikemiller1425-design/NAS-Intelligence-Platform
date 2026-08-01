# PKT-10 — Decision closure breaks the shipped rule set (PF-16)

> **Non-authoritative remediation packet.** It proposes a resolution; it does not apply one and
> changes no specification. Adopting it requires change-control approval, and where an operator
> decision is named, that decision remains the operator's.

| Field | Value |
| --- | --- |
| Findings | PF-16 (MAJOR) |
| Highest severity | MAJOR |
| Change-control batch | BATCH-10 |
| Operator decision required | **OD-012**, **OD-003** — their *contents*. The closure *machinery* proceeds without them. |
| Blocked rungs | FBL-035 |
| Affected acceptance | FND-ACC-010, FND-ACC-013 |
| Depends on | **PKT-09** — taxonomy nodes acquire `policy_ref` and inherit the same trap |

## The exact contradiction

- `rule-model.md:303` — `VAL-POLICY-OPEN | Every policy_ref names a still-open decision.`
- `classification-rule-set.schema.json:440–455` — `policy_ref` is **required** on every `provisional`
  rule.
- The shipped example cites OD-012 four times and OD-003 once
  (`classification-rules.example.yaml:118,180,242,304`). Both decisions carry
  `blocks_gate: dry_run` (`open-decisions.md:22,31`).
- `gate-model.md:125` — G4 entry criterion 7: "No open decision classified `blocks_gate: dry_run`
  remains unresolved."
- `gate-model.md:121` — G4 entry criterion 3: "Rule set version is frozen and **validates against the
  canonical schema**."

**Criteria 3 and 7 are jointly unsatisfiable.** This is not a race condition to be sequenced around;
it is a permanent contradiction. The moment either decision closes, the shipped example fails loader
validation — at exactly the moment the rule set must be frozen for G4.

The register compounds it by prescribing an ordering the check forbids: "Reclassify provisional rules
**only after** explicit confirmation (OD-012)" (`open-decisions.md:63`).

**And prior to all of that, there is no machine-readable register to read.**
`open-decisions.md:18`'s columns are `ID | Decision | Severity | blocks_gate | Re-confirm at | Notes`
— **no `state` column exists anywhere**. "Resolved" appears only as prose at `:65`. Accordingly
`scripts/validate_rule_config.py` implements four of nine checks, and this is not among them.
`change-control.md` defines a six-step linear process with no notion of a change whose intermediate
state is invalid.

## Operational consequence if left unresolved

FBL-035 cannot simultaneously satisfy "The canonical example loads" (`build-ladder.md:1088`) and "all
nine `VAL-*` checks" (`:1081`) once OD-012 closes. At G4 the frozen rule set is unloadable.

**The discovering implementer's cheapest fix is to relax or delete the check** — removing the only
structural link between the rule set and the governance register, and the only barrier to a rule
claiming a decision is still open in order to keep an unowned advisory destination alive.

## Affected domain entities and fields

None directly. `RuleSet` gains an optional `decision_register_version`. `TaxonomyNode.policy_ref`
(PKT-09) inherits the same mechanism.

## Affected events, commands, reason codes, and persistence records

Three checks replace one: `VAL-POLICY-OPEN` (restated), `VAL-POLICY-PROMOTED`, `VAL-POLICY-UNKNOWN`,
plus `VAL-POLICY-PIN`. All registered in FBL-005's registry. A new config artifact and its schema.

## Proposed normative resolution

### Three checks replace one

> **`VAL-POLICY-OPEN`** — every `policy_ref` on a `provisional` rule names a decision whose state,
> **in the register version pinned by `rule_set.decision_register_version`**, is `open`.
>
> **`VAL-POLICY-PROMOTED`** — every `policy_ref` on a `provisional` rule names a decision whose state
> **in the live register** is `open`. A cited `resolved` or `withdrawn` decision rejects with a
> message naming the decision and the required promotion.
>
> **`VAL-POLICY-UNKNOWN`** — every `policy_ref`, at any status, names a decision id present in the
> register.
>
> **`VAL-POLICY-PIN`** — `decision_register_version` is required when `status ∈ {approved, active}` or
> `environment: pilot`. Absent means the live register.

**The two-register-version split is the crux.** Pinned-version evaluation keeps archived rule sets
permanently loadable, satisfying `change-control.md:15` and keeping AUTHZ-12 / `APR-E13` re-verifiable
for historical approvals. Live-register evaluation is what forces promotion and yields an actionable
error. One check cannot do both jobs, which is why one check was the wrong shape.

### A new artifact: the machine-readable register

`config/governance/open-decisions.yaml`, proposed:

```yaml
register_schema_version: 1
register:
  version: "1.0.0"
  effective_from: "2026-07-31"
  decisions:
    - id: "OD-012"
      title: "Confirm Dogs / drone / CSV / identity-candidate rules"
      severity: "MAJOR"
      blocks_gate: "dry_run"
      state: "open"
      reconfirm_at: null
      resolved_at: null
      resolution_ref: null
      owner: "operator"
```

Its schema, proposed at `config/schemas/open-decision-register.schema.json`:
`register_schema_version` (`const: 1`); `register.version` (semver, required);
`register.effective_from` (ISO date, required); `register.decisions` (array, min 1, unique). Per
decision, all required unless noted: `id` (`^OD-[0-9]{3}$`); `title` (1–200); `severity`
(`BLOCKER|MAJOR|MINOR`); `blocks_gate` (the eight-gate enum); **`state` (`open|resolved|withdrawn`)**;
`reconfirm_at` (gate enum **or null**, nullable-required); `resolved_at` (ISO date or null);
`resolution_ref` (≤200 or null); `owner`; `notes` (optional).

| ID | Invariant |
| --- | --- |
| DR-1 | `state ≠ open` ⇒ `resolved_at` and `resolution_ref` both non-null. `state: open` ⇒ both null. |
| DR-2 | `id` is unique. |
| DR-3 | Register `version` is monotonically increasing; a published version is immutable. |
| DR-4 | A decision's `state` may transition `open → resolved` and `open → withdrawn` only. **Reversion is rejected.** |

`docs/05-governance/open-decisions.md` remains the human view, checked against the YAML at Foundation
acceptance. Canonicalization for pinning: decisions sorted by `id`, keys sorted, NFC.

### The Decision Closure Change

Insert into `change-control.md` after `:15` a *Coupled changes* section defining the **Decision
Closure Change (DCC)** — one change containing:

1. The register transition, with `resolved_at` and `resolution_ref`, and a register version increment.
2. For **every** rule citing that decision, an explicit disposition — `promote` (to `active`,
   requiring all five fixture classes non-empty per `classification-rule-set.schema.json:508–526`),
   `disable`, `retire`, or `re-point` to a named still-open successor. **A rule left `provisional`
   citing a closed decision is not a legal outcome.**
3. The same for every taxonomy node.
4. Rule-set and taxonomy version increments, with prior versions archived rather than edited.
5. Re-approval of any `granted` set, since promotion changes `then.destination_authority`.
6. The recorded consequence that `rule_set_hash` and `taxonomy_hash` change, firing IT-03 and IT-04
   against every outstanding approval.

Closing prohibition: **a decision may never be reopened, have its `state` reverted, or have its
`blocks_gate` weakened in order to make a rule set load.**

Amend `gate-model.md:121`: criteria 3 and 7 are evaluated against the post-DCC state only, never an
intermediate state.

### The migration property that makes this cheap

`decision_register_version` is added to `$defs/ruleSet` as **optional**, so **all 48 shipped rule
files validate byte-for-byte unchanged.** Making it required would invalidate all 48. It remains a
change-controlled edit to frozen Foundation content.

## Alternatives considered

**Delete `VAL-POLICY-OPEN`.** Rejected: it is the only check preventing a provisional rule from citing
an already-made decision, and deleting it severs the loader's only link to the governance register.

**Weaken it to "names a decision that exists."** Rejected: satisfiable but vacuous. It would accept a
G4-frozen rule set citing a decision closed months earlier, **while appearing to enforce
governance** — which is worse than no check, because it produces a green signal.

## Safety implications

The reopening prohibition is the anti-laundering control. Without it, the cheapest route past a
failing loader at G4 is to reopen the decision — converting the register from *a record of what was
decided* into *a lever for making validation pass*. That is the specific failure mode this packet
exists to foreclose.

## Migration and compatibility implications

All 48 shipped rule files validate unchanged, because the pin field is optional. The register YAML is
new. `open-decisions.md` gains no columns; it is reclassified as the human view of a machine artifact,
and a Foundation check compares the two.

## Required tests

**Positive** — the shipped example validates with all three checks active and OD-012 `open`; a
`v2.0.0` set pinning a register in which OD-012 is `resolved`, with all citing rules promoted,
validates; **`v1.0.0` pinning the older register still validates after closure** — this is the
property the two-version split exists to deliver.

**Negative** — a `provisional` rule citing a `resolved` decision → `VAL-POLICY-PROMOTED`; `OD-999` →
`VAL-POLICY-UNKNOWN`; an `active` set without a pin → `VAL-POLICY-PIN`; the existing fixture
`tests/fixtures/rules/negative/provisional-missing-policy-ref.yaml` is unchanged and still rejects.

**Failure-injection** — **a partially applied DCC (register flipped, rules untouched) must fail
`VAL-POLICY-PROMOTED` in CI**, proving the coupled change cannot be half-committed; a register edit
reverting `resolved → open` rejected by DR-4; a set pinning a nonexistent register version must fail
rather than fall back to live; two sets pinning different register versions must both load in one
process.

## Required documentation changes

`rule-model.md:303` (three checks); `change-control.md` after `:15` (the DCC);
`gate-model.md:121` (post-DCC evaluation); `open-decisions.md:63` (the ordering correction) and its
reclassification as the human view.

## Required ADR changes

**ADR-006** — append to Consequences: "`policy_ref` links into a versioned machine-readable decision
register. Closure is a coupled change covering the register, every citing rule, and every citing
taxonomy node. A rule set validates against the register version it pins, so archived sets remain
loadable after a decision closes."

**ADR-017** — append to Consequences: "A decision closure change necessarily changes `rule_set_hash`
and `taxonomy_hash` and therefore fires IT-03 and IT-04. Closing a decision is never paperwork-only:
it voids standing authorizations by design."

## Operator policy, or pure specification defect?

**Both, and the split is clean.**

*Specification and change-control half — proceeds now:* the three checks plus the pin check, the
register artifact and its schema, `decision_register_version`, the DCC definition, the
`gate-model.md:121` amendment, the `open-decisions.md:63` correction, and the fixtures.

*The single operator question, unanswered:* **what OD-012 and OD-003 decide.** For each of
`MEDIA-095-drone`, `DATA-080-csv`, and `MEDIA-100-dogs` — promote, disable, retire, or re-point;
whether `MEDIA-050-known-person-candidate` ever leaves `disabled`; whether "Dogs wins over People"
(`rule-model.md:283`) is ever encoded.

**The DCC machinery must exist before that decision can be executed safely. The contents are entirely
the operator's, and Claude has not decided any of them.**

## Atomicity

**PKT-09 (PF-15)** — taxonomy nodes acquire `policy_ref` and inherit the closure trap, so the DCC's
step 3 is unwritable until the taxonomy contract exists. **PKT-13 (PF-29)** — G4 evaluates register
state, rule-set freeze, and mode compatibility as one gate decision. **PF-31** — three new codes enter
FBL-005's registry.

## Verification procedure

Re-run `validate_rule_config.py` and confirm all 48 files still validate. Independently: confirm
`open-decisions.md` and the new YAML agree row-for-row; confirm the register schema rejects a
`resolved` decision with a null `resolved_at`; confirm `gate-model.md` criteria 3 and 7 now name the
post-DCC state.

## Change-control authority

Change control per `docs/05-governance/change-control.md`, plus the operator for the *contents* of
OD-012 and OD-003. **This packet is non-authoritative and confers no authority of its own.**
