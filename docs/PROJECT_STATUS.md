# Wildlands: Project Status (Project Memory)

**Purpose:** Single place to see how far we are and what to do next. Update this when we complete work or change priorities. Agents should read this and suggest improvements that match the current phase.

**Last updated:** Engineering baseline hardening pass added (CI quality gates, canonical tooling config, contributor guide, architecture doc, and extra regression tests).

---

## Current phase: **Layer 2 — Story that supports the mechanic**

The narrative is **locked** in `NARRATIVE_DESIGN.md`. Next: implement or prototype the **training phase (Act 1)** so the full arc (7→10 then 10+ Keeper) exists in the game. The existing `game/` loop remains Act 2 (age 10+).

---

## Done ✅

- **Repo:** README, .gitignore, requirements.txt; non-game scripts in `examples/`.
- **Engineering baseline:** CI workflow now runs lint (`ruff`), type checks (`mypy` on typed state modules), and unit tests; canonical config added in `pyproject.toml`; `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `VERSION`, and `CHANGELOG.md` established.
- **Codebase:** `game/` package (constants, state, world, capture, companions, cli, loop, main); launcher `adventure_game.py`.
- **Act 1 (training 7→10):** `game/act1/` — create character (name), train 4 skills (Strength, Agility, Smarts, Spirit) with multi-question banks, source-based study (Solo/Teacher/Mentor/Parent/Pet), choose primary + 2 supplementary when all at baseline, Year 1/2/3 progression, readiness → transition to Act 2. Launcher runs Act 1 first; `--test` skips to Act 2.
- **Act 2 (Keeper loop):** Explore → capture → train/play companions → exhibition; difficulty; replay. Added region flavor + NPC scenes in Act 2 exploration (first Layer 3 narrative starter).
- **Narrative design:** Full story in `docs/NARRATIVE_DESIGN.md`: character pick (ground zero), 7→10 training, then Act 2 at 10.
- **Project memory:** `docs/` + Cursor rule; `docs/VISUAL_INTERFACE.md` for web vs desktop UI options.
- **Testing depth:** Added regression tests for CLI input error handling and world spawning/NPC scene edge behavior.
- **Web — 3D character:** `web/character3d.html` + `web/character3d.js` — Three.js (CDN, import map); design panel (body color, height slider); third-person character (cylinder + sphere); WASD + mouse look (PointerLock); ground and obstacles to walk around. Linked from `web/act1.html` and `web/index.html`.

---

## In progress / Next 🔄

1. **Harden and tune Act 1**
   - Balance question difficulty and progression pacing after consultation sources were added.
2. **Start 3D UI Milestone 1 (Layer 2 aligned)**
   - Implement the interaction shell from `TECH_DESIGN_3D_UI.md` (objective/prompt/toast + one Teacher interaction vertical slice).
   - Track daily delivery with `docs/EXECUTION_CHECKLIST_WEEK1.md`.
3. **Continue Layer 3 narrative seeding (small scope)**
   - Expand region flavor and short NPC moments with consequence hooks while keeping systems light.
4. **Do not yet**
   - Add inventory, save/load, or map data (Layer 4) before Act 1 is in place.
   - Add lots of Act 2 world content (Layer 3) until the two-act structure is running.

---

## After Layer 2 is solid (two-act structure playable)

- **Layer 3:** Region flavor, NPC scenes (Act 2: Mira, Sol, Ari); consequences; optional encounters.
- **Layer 4:** Save/load, optional inventory, optional scene data (e.g. JSON).
- **Layer 5:** Pacing, multiple endings, achievements, polish.

---

## AI (planned)

We want to **add AI to the project at some point**. The goal is to use AI to:

- **Character building:** Help players design or generate characters (e.g. appearance, personality, backstory suggestions).
- **Diversity and change:** Support more varied and dynamic characters — different looks, traits, and behavior over time so the world feels richer and less repetitive.

This is a stated future direction, not part of the current phase. When we get to it, AI should support the narrative (see `NARRATIVE_DESIGN.md`) and the existing character/training design (e.g. Act 1 skills, Act 2 companions).

---

## How agents should use this

1. **Read** `docs/README.md`, then `DEVELOPMENT_PHASES.md`, `NARRATIVE_DESIGN.md`, and this file.
2. **Decide** which layer we’re in and what’s done vs next (use this file and the phases doc).
3. **Suggest or implement** only what fits the current phase and the narrative. If the user asks for something out of phase, say so and recommend the right next step from the plan.
