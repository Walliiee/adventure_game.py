# Wildlands Architecture Overview

This document explains where core responsibilities live.

## Runtime entry points

- `adventure_game.py`: launcher script from repo root.
- `game/main.py`: main runtime flow (`Act 1 -> Act 2`, replay loop).
- `game/__main__.py`: module entry (`python -m game`).

## Core game package (`game/`)

- `game/act1/`: training phase state, questions, CLI, and loop.
- `game/loop.py`: Act 2 session loop.
- `game/world.py`: region selection, narrative flavor, creature spawning.
- `game/capture.py`: capture attempt rules.
- `game/companions.py`: train/play/exhibition actions.
- `game/cli.py`: shared prompts/menus and display helpers.
- `game/state.py`: Act 2 game-state construction and typing.
- `game/constants.py`: centralized content and tuning values.

## Tests (`tests/`)

- Focused unit tests for smoke flow, state gates, questions, and world/narrative behavior.
- New gameplay changes should include targeted tests for branching behavior and edge cases.

## Web experience (`web/`)

- Static files for visual exploration (`index.html`, `act1.html`, `character3d.html`).
- Deployed via GitHub Pages workflow.

## Documentation and project memory (`docs/`)

- `DEVELOPMENT_PHASES.md`: required order of work.
- `NARRATIVE_DESIGN.md`: story canon.
- `PROJECT_STATUS.md`: current state and next steps.

## Non-core scripts (`examples/`)

- Standalone demos/learning scripts, not part of Wildlands runtime.
- Keep experimental scripts here to avoid root-level clutter.
