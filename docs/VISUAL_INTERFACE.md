# Visual interface options (Wildlands)

**Purpose:** How to build or use a visual (non-CLI) interface for the game. The core logic lives in the `game/` package; interfaces can sit on top.

---

## What exists today

- **CLI (terminal):** Full flow. Run `python adventure_game.py` → Act 1 (train 7→10) → Act 2 (Ridgecamp, catch/train/exhibition). No extra dependencies. `--test` skips Act 1.
- **Web — Act 1 only:** `web/act1.html` + `web/act1.js` implement the training phase in the browser (name, 4 skills, questions, focus choice, “ready at 10”). Static HTML/JS; same rules as the Python Act 1. After completion, the page tells you to run the CLI for Act 2. Includes a link to the 3D character page.
- **Web — 3D character:** `web/character3d.html` + `web/character3d.js`. A 3D scene (Three.js from CDN via import map): character you can **design** (body color, height slider via **C**) and **walk around** with **WASD** and **mouse look** (click to lock pointer). Third-person camera; ground and obstacles. No build step; open in browser. Linked from Act 1 and `web/index.html`.
- **Web — Forest Adventure:** `web/index.html` is a separate kid-friendly story game; not the two-act Wildlands flow.

---

## How to build a visual interface

### Option A: Expand the web app (recommended for “visual”)

- **Act 1:** Already done at `web/act1.html`. You can open it in a browser (file:// or any static server) and play the training phase.
- **Act 2 in the browser:** To make the full game visual in the browser you would:
  1. Reimplement or mirror the Act 2 loop in JavaScript (explore, capture, train/play, exhibition), **or**
  2. Run a small Python backend (e.g. Flask/FastAPI) that exposes the existing `game/` logic as API endpoints and have the front end call them.
- **Single-page flow:** Link or embed Act 1 and Act 2 in one flow (e.g. after “You’re ready” in Act 1, load the Act 2 screen instead of saying “run the CLI”).

**Pros:** No install for players, works on any device with a browser.  
**Cons:** Act 2 in browser requires either rewriting game logic in JS or adding a backend.

### Option B: Desktop GUI (e.g. tkinter)

- Use Python’s built-in **tkinter** (or another GUI toolkit) to build windows with:
  - Text labels and buttons instead of `input()` prompts.
  - Same underlying calls: `game.act1.run_act1`, `game.state.create_game_state`, `game.loop.run_session`, etc.
- Flow: one window for Act 1 (name, skill choice, question/answer), then switch to Act 2 (menu, regions, capture, etc.).
- **Pros:** Single codebase (Python), no browser.  
**Cons:** More UI code; packaging (e.g. PyInstaller) if you want a standalone .exe.

### Option C: Hybrid

- Keep **Act 1 in the browser** as the main “visual” entry.
- After “You’re ready,” offer: “Download save” or “Continue in app” that launches the CLI (or a future desktop app) with the same player name. That way the visual part is the training; the rest stays CLI until you add a full visual Act 2.

---

## Recommendation

- For **testing and playing right now:** Use the **CLI** (`python adventure_game.py` for full journey, `python adventure_game.py --test` to skip Act 1).
- For a **visual experience:** Use **web/act1.html** for the training phase and **web/character3d.html** for the 3D character (design + WASD walk). Add either a web-based Act 2 (JS or backend API) or a tkinter (or other) desktop GUI when you’re ready to make Act 2 visual.

**Keep this doc updated** when you add a new visual front end or change how Act 1/Act 2 are exposed.

---

## AI (planned)

We plan to **add AI** to the project later. AI should help with **character building** (e.g. generating or suggesting appearance, personality, backstory) and with **diversity and change** in characters (more variety, dynamic traits, less repetition). See `PROJECT_STATUS.md` → “AI (planned)” for the full note. When we introduce AI, it should support the existing narrative and character design (Act 1 training, Act 2 companions) rather than replace it.
