# Rung Correction Prompt

## Role

Correct a rung that independent inspection **rejected**. You are repairing one rung against named findings — not reopening its design, and not continuing past it.

## Preconditions

- An independent inspection verdict of **not ready** exists, with named findings.
- The rung's original G3 authorization is still current, or the operator has reissued it.
- No open decision listed in the rung's **Blocking open decisions** field became unresolved in the meantime.

## Required inputs

| Input | Why |
| --- | --- |
| **Rung ID** | Scope is still the rung, not the findings' neighbourhood. |
| **Inspection verdict with findings** | Each finding is a unit of work with a defined end. |
| **Commit under correction** | So the correction diff is separable from the original. |

## Authority

- Address the named findings, and nothing else.
- Add or repair tests where a finding says a test was missing or ineffective.

## Prohibitions

- Do not fix unrelated defects you notice. Report them; a second finding is not a second authorization.
- Do not redesign the rung to avoid a finding. If the rung as specified is wrong, say so and stop — the ladder may be the defect.
- Do not weaken a test, an assertion, or a safety control so a finding disappears.
- Do not begin the next rung.
- Do not access any NAS path.

## Required output

- Finding-by-finding disposition: **fixed**, **not applicable with reasoning**, or **disputed with reasoning**. Every finding gets one; silence is not a disposition.
- The re-run test results, including the specific test that now covers each previously-missing case.
- Anything you found but deliberately did not fix, listed so it is not lost.

## Stop condition

All findings are dispositioned and the rung is ready for **re-inspection**. Correction does not itself advance the rung.
