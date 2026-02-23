# Project Memory — Read This First

This folder is **authoritative project memory** for Wildlands. Any agent or human working on this codebase should use it to stay aligned and avoid backtracking.

---

## Required reading (in order)

1. **DEVELOPMENT_PHASES.md** — The order of work (Layer 1 → 2 → 3 → 4 → 5). Do not skip phases or add features from a later phase before the current one is in good shape.
2. **NARRATIVE_DESIGN.md** — The story that supports the full game (Act 1: training 7→10; Act 2: Keeper at 10). All content must align with this.
3. **ACT1_DESIGN.md** — Implementation spec for the training phase: skills, progression, player-facing learning, consultation, transition to Act 2. Read when working on Act 1.
4. **PROJECT_STATUS.md** — What’s done, what we’re doing now, and what comes next. Update it when we complete work or change priorities.
5. **TECH_DESIGN_3D_UI.md** — Technical start plan for a better interactive 3D UI, milestones, architecture, and constraints. Read when working on `web/character3d.*` or 3D UI scope.
6. **EXECUTION_CHECKLIST_WEEK1.md** — Short sprint checklist for immediate implementation sequencing of the 3D Milestone 1 vertical slice.

---

## What you must do

- **Before suggesting or implementing features:** Read the three docs above. Determine which development phase we’re in and what the next step is.
- **When suggesting improvements:** Propose work that fits the **current phase** and the **narrative design**. If the user asks for something that belongs to a later phase, say so and recommend the right next step from the current phase (or ask if they want to change the plan).
- **When you change the story or the plan:** Update `NARRATIVE_DESIGN.md` or `PROJECT_STATUS.md` so the next agent (or human) sees the latest state.
- **When you add or change a visual/UI (web or desktop):** Update `VISUAL_INTERFACE.md` and `PROJECT_STATUS.md` so the 3D character page, Act 1 web, and other interfaces are recorded.

---

## Why this exists

So we don’t jump ahead (e.g. inventory, save/load, lots of content) before the story is set and reflected in the game. Following the phases and the narrative doc keeps the project coherent and reduces rework.
