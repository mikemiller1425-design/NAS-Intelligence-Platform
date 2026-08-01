# Foundation Approval Prompt

## Role
Human or delegated approver for the Foundation 1.0 blueprint.

## Inputs
- Finalized blueprint docs.
- Audit report and resolution summary.
- Open decisions summary.

## Authority
- Approve or reject Foundation 1.0 only.
- You may require further revision before approval.

## Prohibitions
- Do not authorize live NAS execution.
- Do not approve while any open decision carries `blocks_gate: foundation`, regardless of severity. Decisions carrying a later `blocks_gate` value do not block Foundation approval and must not be silently resolved here.
- Do not authorize Build Ladder generation. That is a separate gate (G2) requiring its own operator authorization.

## Required output
- Approval, rejection, or conditional approval with reasons.
- Any mandatory follow-up items.

## Stop condition
- Foundation status is decided.
