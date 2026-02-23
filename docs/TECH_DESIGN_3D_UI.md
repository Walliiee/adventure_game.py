# Wildlands 3D UI — Technical Design (Phase-Aligned Start)

**Status:** Proposed start plan (Layer 2 aligned).  
**Purpose:** Define a practical architecture to evolve `web/character3d.html` + `web/character3d.js` from a movement sandbox into an interactive 3D Act 1 experience.

---

## 1) Goals and non-goals

### Goals (now)

1. Build a **3D interaction shell** for Act 1 with:
   - Objective HUD (what to do next)
   - Context prompt (e.g., "Press E to talk")
   - NPC interaction triggers for Teacher/Mentor/Parent/Pet
2. Keep scope aligned to **Layer 2**: improve training delivery, do not jump into save/load or deep world systems.
3. Preserve current no-build deployment style (static web files) while organizing code for growth.

### Non-goals (for this start)

- Full Act 2 in 3D
- Backend services or account systems
- Inventory/save system design

---

## 2) Current baseline

- 3D page has a playable scene with third-person movement, pointer-lock camera, and a lightweight design panel (color/height).  
- Act 1 web gameplay exists separately in `web/act1.html` and does not currently drive the 3D page.

This design bridges those two tracks with minimal risk.

---

## 3) Proposed architecture

Create small modules in `web/3d/` and keep `character3d.js` as the entry orchestrator.

```
web/
  character3d.html
  character3d.js                # entry, wiring only
  3d/
    state.js                    # single source of truth for 3D session
    hud.js                      # objective, prompt, notifications
    controls.js                 # keyboard/mouse + pointer lock state
    world.js                    # scene setup + interactable registration
    interaction.js              # range checks + interaction dispatch
    act1_bridge.js              # maps interaction outcomes to Act 1 skill/question flow
```

### State model (browser)

`state.js` should hold:
- player customization (color/height)
- current objective id
- nearby interactable id
- active dialog/question payload
- light Act 1 progress mirror (skills/actions/focus)

Use a small pub/sub (`subscribe(listener)`) to update HUD and interaction UI when state mutates.

---

## 4) Interaction loop (vertical slice)

1. Player moves in 3D world.
2. Proximity/raycast detects nearest interactable (Teacher etc.).
3. HUD shows prompt: `Press E to interact with Teacher`.
4. On interact:
   - open focused dialog panel (overlay)
   - present one Act 1 question mapped to selected source+skill
   - apply result to Act 1 state mirror
   - show toast (`+1 Smarts`) and update objective

This is the first vertical slice and should be completed before broader content work.

---

## 5) UI/UX requirements (MVP)

- **Top-left objective card:** concise current goal.
- **Bottom-center interaction prompt:** appears only when interactable is valid.
- **Right-side mini-stats:** 4 skills + actions/year progress.
- **Transient toasts:** success/failure feedback.
- **Input fallback:** if pointer lock unavailable, still allow interaction via click + key.

Accessibility baseline:
- color contrast > WCAG AA target where practical
- keyboard-operable overlays
- motion-reduced toggle (camera smoothing/blur off)

---

## 6) 3D content and assets plan

### Stage A (immediate)
- Keep primitive geometry for NPC markers (colored totems/icons).
- Keep current character mesh for speed.

### Stage B (next)
- Swap player to GLTF avatar with idle/walk animation.
- Swap NPC markers to simple stylized GLTF stand-ins.

Asset constraints:
- compressed textures where possible
- target < 10MB total initial payload for first load

---

## 7) Performance budget and instrumentation

Targets (desktop baseline):
- 55–60 FPS at 1080p medium settings
- first interactive frame < 3s on local static host

Add dev instrumentation toggle:
- frame time + FPS readout
- interactable count
- draw call estimate (if available)

Quality settings:
- `low|medium|high` controlling shadow size, fog distance, and post effects (if added later)

---

## 8) Delivery milestones

### Milestone 1 — 3D Interaction Shell (start here)
- HUD primitives (objective/prompt/toast)
- Interactable registry (Teacher/Mentor/Parent/Pet)
- "Press E" interaction + one question flow
- Basic tests/manual checklist

### Milestone 2 — Act 1 3D Vertical Slice
- Source-specific question routing for all 5 sources
- Skill updates + readiness checks mirrored in 3D HUD
- Transition message into Act 2 handoff

### Milestone 3 — Visual quality pass
- animated avatar integration
- camera polish and accessibility options
- mobile/touch fallback controls

---

## 9) Acceptance criteria for Milestone 1

1. Player can approach Teacher and get interaction prompt.
2. Pressing `E` opens one question interaction.
3. Answer updates stats and shows toast feedback.
4. Objective updates after completion.
5. System remains playable if pointer lock is denied.

---

## 10) Risks and mitigations

- **Risk:** scope creep into Act 2/world systems.  
  **Mitigation:** lock milestones to Layer 2 outcomes only.

- **Risk:** duplicated logic divergence between Python Act 1 and Web Act 1/3D.  
  **Mitigation:** keep shared constants/questions in mirrored schema and add parity checks.

- **Risk:** input complexity across desktop/mobile.  
  **Mitigation:** desktop-first for M1, touch fallback in M3.

---

## 11) Immediate implementation tasks (next PR)

1. Add `web/3d/` module skeleton and migrate non-render logic out of `character3d.js`.
2. Add HUD elements in `character3d.html` for objective/prompt/toast.
3. Implement interactable registry + nearest-interactable prompt.
4. Implement one source question flow (Teacher → Smarts) end-to-end.
5. Update `docs/PROJECT_STATUS.md` after M1 lands.

