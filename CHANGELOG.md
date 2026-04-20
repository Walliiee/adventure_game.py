# Changelog

All notable changes to this project should be documented in this file.

The format is inspired by Keep a Changelog and follows semantic-style versions.

## [0.2.0] - 2026-04-20

### Added
- **Python 3.9 compatibility fix** — removed use of `|` operator for dict type unions in `TypedDict` definitions.
- **JSON save/load with auto-save** — game state persists between sessions via automatic saves on exit and explicit save slots via the camp menu.
- **6 distinct endings** — multiple unique narrative conclusions tied to difficulty level, creature bonds, and choices.
- **8 achievements** — unlockable milestones tracking captures, exhibitions, companions, and exploration.
- **Inventory system** — 4-slot carry system for Items (rare tools that modify encounters or capture odds).
- **Random encounters (5 types)** — weather events, creature sightings, wandering travelers, NPC encounters, and treasure discoveries.
- **Act 1 skill bonuses in Act 2** — skills trained during character growth (age 7–10) carry forward as modifiers in the capture loop.
- **JSON data model for content** — creatures, companions, NPCs, regions, and encounters defined in `.json` files under `data/`.
- **Companion personalities + daily abilities** — three companion archetypes (Ember the Emberfang, Zaph the Shadowmite, Lira the Stormcrest) each with a unique passive ability usable once per in-game day.
- **NPC interactions + coin economy** — interact with NPCs in camp, spend coins at the shop for items and lore; earn 2 coins per capture and 1 per exhibition win.

### Changed
- Migrated type annotations from `dict[str, Any]` pattern to structured `TypedDict` classes for all core state objects.
- Refactored content data from Python constants into JSON files for easier editing and extension.

## [0.1.0] - 2026-04-16

### Added
- GitHub Actions CI workflow for lint, type checks, and tests.
- Canonical `pyproject.toml` for project and tooling configuration.
- Contributor guide with required local quality checks.
- Architecture overview (`docs/ARCHITECTURE.md`).
- Lightweight release artifacts: `VERSION` and this `CHANGELOG.md`.
- Additional tests for CLI input handling and world edge-case behavior.
