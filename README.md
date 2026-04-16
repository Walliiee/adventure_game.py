# Wildlands: Orb Catcher Adventure

A creature-catching CLI game and a kid-friendly web adventure. The codebase is organized as a proper game project: core logic in a `game/` package, content in config, and a clear entry point.

## Project structure

```
├── game/                 # Main game package
│   ├── __init__.py
│   ├── __main__.py       # Entry: python -m game
│   ├── constants.py      # Creatures, difficulty, regions, NPCs
│   ├── state.py          # Game state creation
│   ├── world.py          # Regions, creature spawning
│   ├── capture.py        # Capture mechanic
│   ├── companions.py     # Train, play, exhibition
│   ├── cli.py            # Menus, prompts, display
│   ├── loop.py           # Main game loop
│   └── main.py           # Entry: setup + replay
├── web/                  # Forest Adventure + Act 1 Training UI (static)
├── examples/             # Standalone scripts (demos, exercises)
├── adventure_game.py     # Launcher (run from repo root)
├── requirements.txt
└── GAME_IMPROVEMENT_IDEAS.md
```

## How to run

**CLI game (Wildlands) — full journey (Act 1 then Act 2):**
```bash
python adventure_game.py
```
You create your character (name), train from age 7→10 (four skills, questions, choose primary + 2 supplementary), then go to Ridgecamp for the Keeper loop.

**Skip Act 1 (test Act 2 only):**
```bash
python adventure_game.py --test
```

## MVP playtest checklist

Use this quick loop for first-pass playability checks:

1. Run the full path (`python adventure_game.py`), enter a name, and confirm Act 1 starts.
2. Train until you select primary + supplementary skills, then confirm guidance remains clear.
3. Reach Ridgecamp (Act 2), choose a difficulty, and perform at least one camp action.
4. Quit from the camp menu and confirm replay prompt behaves correctly.
5. Run quick path (`python adventure_game.py --test`) and verify immediate Act 2 access.

**Web (visual):**  
- **Best:** run a local server so the page loads correctly. From the project root: `cd web && python -m http.server 8080` then open **http://localhost:8080/act1.html** (or index.html, character3d.html).
- Act 1 Training: `web/act1.html` is **self-contained** (CSS and JS inlined) so it can also be opened directly from the `web/` folder in your browser.
- Forest Adventure: `web/index.html` · 3D character: `web/character3d.html`. See `docs/VISUAL_INTERFACE.md`.

## Requirements

- **Python 3.10+** (standard library only for the CLI game)
- Optional deps in `requirements.txt` (e.g. for scripts in `examples/`).

## Development and quality

Install optional dev tooling:

```bash
pip install -e ".[dev]"
```

Run local quality checks:

```bash
python -m ruff check .
python -m mypy game/state.py game/act1/state.py
python -m unittest discover -s tests -p "test_*.py"
```

CI runs the same checks on pull requests and pushes.

## Other scripts

Standalone demos and exercises live in **`examples/`**. Run with `python examples/<script>.py` from the repo root. They are not part of the Wildlands game.

## Project memory (agents and humans)

**`docs/`** is the canonical project memory. It defines development phases, narrative design, and current status. When working on the game (or reviewing it), read `docs/README.md` first, then the other docs there. A Cursor rule instructs agents to read these and suggest improvements aligned with the current phase.

## Roadmap

See **GAME_IMPROVEMENT_IDEAS.md** for idea backlog. Execution order follows **`docs/DEVELOPMENT_PHASES.md`**.

## Contributing and release notes

- Contribution guide: `CONTRIBUTING.md`
- Architecture overview: `docs/ARCHITECTURE.md`
- Current version: `VERSION`
- Change history: `CHANGELOG.md`
