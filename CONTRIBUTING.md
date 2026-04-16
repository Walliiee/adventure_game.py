# Contributing to Wildlands

Thanks for contributing to Wildlands: Orb Catcher Adventure.

## Local setup

1. Use Python 3.10+.
2. From `/home/runner/work/adventure_game.py/adventure_game.py`, install optional dev tools:
   - `python -m pip install --upgrade pip`
   - `pip install -e ".[dev]"`
3. Run the game:
   - `python adventure_game.py`

## Quality checks (required before PR)

- `python -m ruff check .`
- `python -m mypy game/state.py game/act1/state.py`
- `python -m unittest discover -s tests -p "test_*.py"`

## Architecture and scope alignment

- Read `/home/runner/work/adventure_game.py/adventure_game.py/docs/README.md`.
- Keep changes aligned with the current phase in `docs/DEVELOPMENT_PHASES.md`.
- Respect the two-act narrative flow in `docs/NARRATIVE_DESIGN.md`.
- For code layout, see `docs/ARCHITECTURE.md`.

## Definition of done

- Feature/fix is scoped to current phase.
- Tests added or updated for behavior changes.
- Quality checks pass locally.
- Relevant docs updated (README/docs/PROJECT_STATUS.md as needed).

## Branching and commit guidance

- Keep PRs focused and small.
- Use clear commit messages (imperative mood).
- Avoid mixing gameplay features with unrelated refactors.
