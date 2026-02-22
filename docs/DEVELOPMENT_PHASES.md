# Wildlands: Development Phases (Project Memory)

**Purpose:** This is the canonical order of work. Do not skip ahead. Each layer builds on the one below. When suggesting or implementing features, align with the current phase and do not add content that belongs to a later phase before the current one is in good shape.

---

## Layer 1: Core Gameplay Mechanic ✅

- **Goal:** Establish a core loop that is fun and proven.
- **Status:** Done. Explore → capture (orbs) → train/play companions → exhibition match.
- **Do not:** Rebuild the core loop unless it’s clearly broken. New features must support it, not replace it.

---

## Layer 2: Story That Supports the Mechanic 🔄

- **Goal:** Define a clear narrative that supports the full game. The story is **two acts:** Act 1 = training (ages 7→10, skills, player-facing learning, consult parents/mentors/teachers/pets or solo); Act 2 = Keeper loop at 10 (existing explore/catch/exhibition). All characters start at ground zero.
- **Status:** Narrative is locked in NARRATIVE_DESIGN.md. In progress: design and implement the **training phase (Act 1)** so it runs before the existing game loop.
- **Before moving on:** Act 1 is designed (skills, learning, consultation, flow 7→10) and a minimal training phase is playable and leads into Act 2. In-game copy reflects the two-act story.
- **Do not:** Add a lot of Act 2 world content or Layer 4 systems before the two-act structure (Act 1 → Act 2) is in place.

---

## Layer 3: World, Levels, Secondary Mechanics

- **Goal:** Build out the world (regions as places, not just names), level/scene design, and secondary mechanics that serve the story and core loop.
- **Status:** Not started. Regions have no flavor text; NPCs are stat labels only.
- **Includes:** Region descriptions, NPC scenes (Mira, Sol, Ari), consequences that tie to the story, optional light encounters (e.g. herbs, hazards).
- **Do not:** Start this layer until Layer 2 (story) is clearly defined and at least partially reflected in the game.

---

## Layer 4: Systems

- **Goal:** Add systems that support the world and mechanics: progression, inventory (if needed), save/load, etc.
- **Status:** Not started. Only basic difficulty/balls/health exist.
- **Includes:** Save/load (e.g. JSON), optional inventory, optional map/scene data (e.g. JSON) for easier content addition.
- **Do not:** Prioritize systems over world and story. Systems exist to support the experience defined in Layers 2–3.

---

## Layer 5: Polish

- **Goal:** Pacing, atmosphere, multiple endings, quality-of-life, achievements.
- **Status:** Not started.
- **Includes:** Optional pacing (e.g. `time.sleep`, FAST_MODE), ending summary, multiple endings, achievements.
- **Do not:** Spend large effort on polish until Layers 2–4 are in place.

---

## Principle

**Every new feature should support the core loop and the current story.** Avoid scope creep. When in doubt, check `docs/NARRATIVE_DESIGN.md` and `docs/PROJECT_STATUS.md` and suggest the next step that fits the current phase.
