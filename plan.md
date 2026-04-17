# Wildlands MVP Playability Plan

## Objective
Ship a minimal, stable version that is immediately playable end-to-end so you can test the experience quickly and iterate with confidence.

## MVP Definition (What “Playable” Means)
- A new player can start from the root command and complete a short session without confusion.
- Act 1 training and transition into Act 2 both work in one run.
- Core Act 2 loop is accessible (explore, capture attempt, at least one companion interaction, exhibition attempt or clean exit).
- Invalid input does not break flow.
- Basic tests pass and the run instructions are clear.

## Scope for MVP (Include)
1. **Reliable startup and onboarding**
   - Confirm one clear command to run the game.
   - Keep intro and prompts short enough for first-time playtesting.
2. **Act 1 baseline loop quality**
   - Ensure skill progression feels finishable in a short test session.
   - Ensure readiness/transition messaging is clear.
3. **Act 2 baseline loop quality**
   - Ensure the day menu and action outcomes are understandable.
   - Ensure players can quit and replay without broken state.
4. **Input robustness**
   - Handle invalid choices consistently in both acts.
5. **Playtest readiness**
   - Provide a simple “quick test path” (`--test`) and full path notes.

## Scope for MVP (Exclude for Now)
- Save/load systems.
- Inventory/map systems.
- Large narrative expansion.
- Major 3D UI expansion beyond existing prototypes.
- AI-driven content generation.

## Execution Plan

### Phase 1 — Playability Baseline Check
- Run existing quality checks (lint, type check, tests) to confirm baseline health.
- Do one guided manual smoke run for:
  - Full flow: Act 1 → Act 2.
  - Quick flow: `--test` into Act 2.
- Capture friction points (unclear prompts, pacing pain, dead ends).

### Phase 2 — MVP Stabilization Pass
- Prioritize only blockers to first playable experience:
  - Confusing prompts that stall players.
  - Progression gates that feel too slow/unclear.
  - Input handling issues that interrupt flow.
- Keep changes surgical and phase-aligned (Layer 2).
- Add/update targeted tests only for changed behavior.

### Phase 3 — First Playtest Package
- Update README run section with two clearly labeled paths:
  - “Play full journey”
  - “Quick Act 2 test”
- Add a short playtest checklist (start game, reach Act 2, perform key actions, exit/replay).
- Verify the same checklist works locally without developer knowledge.

### Phase 4 — Tight Iteration Loop
- After first playtest, collect top 3 pain points only.
- Convert pain points into small issues/tasks.
- Repeat short cycle: fix highest-value issue → run checks → replay smoke test.

## Acceptance Criteria
- Game starts from documented command with no setup confusion.
- Player can complete a full MVP session (Act 1 then Act 2) without crashes.
- Invalid input handling works in key menus/prompts.
- Existing checks pass (`ruff`, `mypy` targets, unit tests).
- README gives enough instructions for someone else to run and test immediately.

## Immediate Next Actions
1. Run one full manual play session and note top friction points.
2. Fix only the highest-severity blocker(s) to first-time playability.
3. Re-run checks and confirm no regressions.
4. Update docs for playtest instructions if behavior changed.
5. Start a second play session and collect iteration notes.

## Iteration Tracking

- [x] Iteration 1: Clarify Act 1 Year-3 readiness gate guidance and fix year-complete message numbering.
- [x] Iteration 1 checks: `ruff`, `mypy` targets, `unittest`, parallel validation.
- [x] Iteration 2: Prevent day/turn advancement when player picks an unavailable Act 2 action (no companion to train/play, exhibition not ready).
- [x] Iteration 2 checks: `ruff`, `mypy` targets, `unittest`, parallel validation.

## Iteration Notes

### Iteration 1 (completed)
- Fixed Act 1 confusion when skill thresholds were met before age gate.
- Added explicit remaining-actions guidance to reach Year 3 (age 10).
- Corrected year completion banner text to reference completed year.
- Added targeted tests and README MVP checklist.

### Iteration 2 (completed)
- Prioritized blocker: selecting an unavailable action in Act 2 still consumed a day, which penalized first-time players.
- Implemented fix: day/turn now advances only when an action actually executes.
- Added targeted regression tests for no-companion and not-ready exhibition day behavior.
- Re-ran checks and parallel validation successfully.
