# Adventure Game Improvement Ideas

Here are some fun ways to make `adventure_game.py` more playable while keeping the original charm.

## Quick wins (1–2 hours)

1. **Replay loop** ✅ *(already implemented — `game/cli.py::ask_replay()` called in main loop)*
2. **Player name + simple stats** *(partially: name is asked in Act 1 via `ask_act1_name()`; courage/luck/health stats not yet tracked)*
3. **Input quality-of-life** ✅ *(already implemented — `q`/`quit` exits prompts; word aliases for choices work via `REGION_ALIASES` in `constants.py`; `help` shows options in CLI prompts)*
4. **Better pacing text** *(not yet implemented — no `time.sleep` pauses; `FAST_MODE` toggle not present)*

## Medium upgrades (half day)

5. **Inventory system** *(not yet implemented — no inventory list, items, or conditional paths)*
6. **Branch consequences** *(not yet implemented — no "scouted" knowledge or downstream choice effects)*
7. **Random encounters** *(not yet implemented — no random events during travel)*
8. **Multiple endings + ending summary** *(not yet implemented — no ending types or end-game summary screen)*

## Bigger Feature Ideas (weekend project)

9. **Save/load support** *(not yet implemented — no JSON persistence or checkpoint resume)*
10. **Map-based structure** *(not yet implemented — scenes are Python functions, not JSON data)*
11. **Difficulty modes** ✅ *(already implemented — `story`/`classic`/`hardcore` in `constants.py`; affects health, balls, capture odds, and exhibition threshold)*
12. **Companion character system** ✅ *(already implemented — `game/companions.py` with `train_companion`, `play_with_companion`, `run_exhibition`; companions have bond/level/mood; exhibition competition at Ridgecamp)*

## Polish and "wow" ideas

13. **ASCII art scene cards** *(not yet implemented — no ASCII title cards for major locations)*
14. **Sound hooks (optional)** *(not yet implemented — no beep/chime cues for win/lose)*
15. **Achievements** *(not yet implemented — no achievement tracking system)*

## Suggested build order

- **Phase 1**: Replay loop, input improvements, ending summary.
- **Phase 2**: Inventory + branch consequences.
- **Phase 3**: Scene data model + save/load.
- **Phase 4**: Content expansion (companions, endings, achievements).

## Optional "version 2" vision

If you want this to grow into a richer project, convert game content to a `scenes.json` file and keep the engine in Python. Then each scene is editable without touching code, making it easier to add new branches and collaborate.
