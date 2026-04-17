# Agent Coordination Notes (Optional but Recommended)

This file is included to make multi-agent or human+agent MVP iteration clearer.

## Suggested Roles
- **Planner agent:** Keeps `plan.md` aligned with current phase and reprioritizes based on playtest findings.
- **Implementation agent:** Makes small code/documentation fixes for the top MVP blocker.
- **Validation agent:** Runs lint/type/tests and performs manual smoke checks for full flow and `--test` flow.

## Handoff Checklist
- What blocker was targeted.
- What changed.
- What checks were run and results.
- What remains as the next highest-priority blocker.

## Priority Order for Work
1. Player-blocking bugs.
2. Confusing prompts and flow breaks.
3. Pacing friction in first playable session.
4. Nice-to-have polish.

## Guardrails
- Stay inside Layer 2 objectives.
- Keep changes reversible and incremental.
- Do not introduce unrelated feature scope.
