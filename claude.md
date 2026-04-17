# Claude Collaboration Guide (MVP Phase)

## Purpose
Keep AI-assisted work focused on making Wildlands quickly playable as an MVP and iterating in small, safe steps.

## Current Priority
- Align to **Layer 2**: complete and harden the two-act playable flow (Act 1 training → Act 2 keeper loop).

## Working Rules
- Prefer smallest viable changes that remove player-facing friction.
- Do not jump to later-layer systems (save/load, inventory, deep content expansion) during MVP stabilization.
- Preserve existing architecture and tests; add targeted tests when behavior changes.
- Keep onboarding and prompts clear for first-time players.

## MVP Implementation Focus
1. Startup and run flow clarity.
2. Act 1 pacing/readiness clarity.
3. Act 2 menu/action clarity.
4. Input error handling consistency.
5. Quick smoke-testability (`--test` plus full flow).

## Definition of Done for Each Iteration
- A specific friction point is resolved.
- Relevant checks pass.
- Manual smoke run still reaches playable state quickly.
- Docs remain accurate for the current behavior.

## Non-Goals During MVP
- Large refactors.
- New platform/system architecture.
- Broad narrative rewrites.
- Expanding 3D UI scope beyond current MVP needs.
