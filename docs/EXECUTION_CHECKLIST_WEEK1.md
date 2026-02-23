# Wildlands — 1-Week Execution Checklist (Next Sprint)

## Sprint goal
Ship a usable **3D Milestone 1 vertical slice** while keeping Act 1/Layer 2 stable and Layer 3 scope controlled.

## Day-by-day plan

### Day 1 — Baseline + acceptance checks
- [ ] Confirm milestone acceptance criteria from `TECH_DESIGN_3D_UI.md`.
- [ ] Verify current 3D page opens and controls work on local static server.
- [ ] Capture before/after screenshot baseline.

### Day 2 — HUD shell
- [ ] Add objective card, interaction prompt, and toast feedback.
- [ ] Ensure overlay does not block pointer-lock gameplay.

### Day 3 — Teacher interaction vertical slice
- [ ] Add Teacher marker/interactable in scene.
- [ ] Add `E` interaction flow with one Smarts question.
- [ ] Show feedback toast and objective completion state.

### Day 4 — Stability + edge cases
- [ ] Handle pointer lock denied / escape state.
- [ ] Ensure interaction panel and design panel do not conflict.
- [ ] Manual smoke pass for keyboard-only use.

### Day 5 — Narrative and docs sync
- [ ] Update project memory (`PROJECT_STATUS.md`) with milestone progress.
- [ ] Update visual docs if controls/UI changed.
- [ ] Record known issues and next-sprint carryover.

## Done criteria
- [ ] Player can find Teacher, press `E`, answer question, and see objective complete.
- [ ] Prompt/objective/toast are readable and update correctly.
- [ ] No major control lockups in common paths.
