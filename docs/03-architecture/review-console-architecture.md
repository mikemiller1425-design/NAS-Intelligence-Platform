# Review Console Architecture

## Purpose
The review console is a human decision surface, not an execution authority. It exists to present evidence, explain proposals, and capture approval intent for controlled workflows.

## Core Responsibilities
- Display inventory evidence and classification rationale.
- Show proposed operations with clear risk labeling.
- Present duplicate and conflict findings.
- Capture human approval, rejection, or request-for-review state.
- Link each decision to immutable audit records.

## Hard Limits
- The frontend never authorizes filesystem mutation.
- It may not directly issue destructive commands.
- It may not act as the source of truth for execution decisions.
- It only communicates human intent to the back end review and execution pipeline.

## Interaction Model
The console should emphasize explainability, not speed. Users should be able to inspect why a proposal exists, what evidence supports it, what safeguards are active, and what happens if they approve it.

## UI Posture
The console should remain read-only with respect to underlying file state. Its job is to help humans decide, not to bypass the gate.
