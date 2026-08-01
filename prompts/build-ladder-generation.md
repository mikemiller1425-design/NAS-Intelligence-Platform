# Build Ladder Generation Prompt

## Role
Generate the implementation ladder after Foundation approval.

## Preconditions
- A current Foundation approval record (gate G1) exists.
- The operator has **separately** authorized Build Ladder generation (gate G2). Foundation approval alone is not sufficient.
- No open decision carries `blocks_gate: build_ladder`.

## Inputs
- Approved foundation blueprint.
- Audit resolution summary.
- Confirmed open-decisions closure status.

## Authority
- Produce a rung-by-rung build sequence.
- Reference the approved docs as the authority.

## Prohibitions
- Do not authorize destructive live execution.
- Do not merge multiple rungs into one unchecked phase.

## Required output
- Stable rung IDs.
- Each rung's objective, prerequisites, allowed work, prohibited work, deliverables, tests, evidence, rollback conditions, and hard stop.

## Stop condition
- The ladder is complete and explicitly non-authorizing.
