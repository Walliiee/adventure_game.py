# Act 1: Training Phase — Design (Project Memory)

**Purpose:** Enough detail to implement a minimal training phase (ages 7→10). All of this supports `NARRATIVE_DESIGN.md`. Update this doc when we change the design.

---

## 1. Skills

**Four skills.** The child must get "generally good" at all four, then choose **one primary** and **two supplementary** (the fourth is still trained but not a focus).

| Skill    | What it represents (for learning content)     |
|----------|-----------------------------------------------|
| **Strength** | Body, endurance, safe handling of gear       |
| **Agility**   | Coordination, reflexes, moving quietly       |
| **Smarts**    | Nature, rules, how orbs and creatures work    |
| **Spirit**    | Calm, focus, bonding with animals             |

- **All four** start at 0 (ground zero).
- **"Generally good"** = each skill reaches at least a **baseline** (e.g. level 2 or score 2). Exact number can be tuned.
- **Primary** = one skill chosen by the player; must reach a **focus threshold** (e.g. level 4) before "ready at 10."
- **Supplementary** = two other skills; must reach a **focus threshold** (e.g. level 3). The fourth skill only needs baseline.
- **When to choose:** Player chooses primary + supplementary at a defined moment (e.g. after all four hit baseline, or at the start of "Year 2" in-world). Until then they just train everything.

---

## 2. Progression and time (7 → 10)

**Simple model for v1:**

- **Time unit:** "Days" or "Weeks." Each training action (one learning moment, one consultation, etc.) costs 1 time unit.
- **Age:** Start at 7. After **N** time units (e.g. 30–60), the character turns 8; after another N, 9; after another N, 10. So 3 "years" of in-game time, each year = N actions. (N is tunable so the phase isn’t too long or short.)
- **Ready at 10:** When (a) the character has reached age 10 in the story, and (b) all four skills ≥ baseline, and (c) primary skill ≥ focus threshold and both supplementary skills ≥ focus threshold → **"You're ready. You leave for Ridgecamp."** → transition to Act 2.

**Alternative (even simpler):** No explicit "age 8, 9, 10" — just a total number of actions or "readiness points." When baseline + primary/supplementary thresholds are met, trigger "You're 10 and ready" and transition. We can add calendar flavour later.

**Recommendation for first implementation:** Use a **total action count** (e.g. 20–40 training actions) and three milestones: "Year 1 done," "Year 2 done," "Year 3 done" (each milestone after ~10–15 actions). At "Year 3 done" + thresholds met → transition to Act 2.

---

## 3. Player-facing learning: one concrete example

**Example: Smarts (nature question)**

- **Action:** "Study Smarts" (alone or with the teacher).
- **What the player does:** The game prints a short question and 2–4 multiple-choice answers. Example:
  - *"What do Moss Bunnies eat?"*  
    A) Berries  B) Insects  C) Grass and leaves  D) Seeds  
  - Player types A, B, C, or D (or 1–4).
- **Outcome:** Correct → +1 Smarts (or +1 level for that skill). Wrong → no gain; optionally "Try again" or "The teacher says: …" and show the right answer (so the player learns).
- **Content:** Questions live in a small data set (e.g. list of dicts: question, correct index, list of options). One question per "Study Smarts" action for v1; later we can randomise and avoid repeats.

**Same pattern for other skills:**

- **Strength:** "How many days should you rest a sore muscle?" / "What’s the safest way to carry a heavy orb?" (multiple choice).
- **Agility:** "What’s the best way to step so you don’t startle a creature?" or a tiny "press the right key in time" prompt (keep it simple for CLI).
- **Spirit:** "What should you do if a creature looks scared?" / "How do you show an animal you’re not a threat?" (multiple choice).

So: **one learning moment = one question or one micro-challenge; success = skill gain.** The player must engage (read and answer); it’s not just "click to train."

---

## 4. Consultation vs solo

**Who the child can learn from:**

| Source    | Role in v1 |
|-----------|------------|
| **Teacher** | Study Smarts (and maybe one other). Gives a question; optional hint if "study with teacher" (e.g. narrow to 2 options) or easier question. |
| **Parent**  | Study Spirit or Heart (e.g. "What does Mom say about being kind to animals?"). Different question set. |
| **Mentor**  | Study Strength or Agility (e.g. "The mentor asks: How do you prepare for a long hike?"). Different question set. |
| **Pet**     | Light practice: simple question or "play" that gives a small amount of any one skill (e.g. +1 to chosen skill with an easy question). |
| **Solo**    | Same questions as with help, but no hint; wrong answer = no gain (and optionally show correct answer). |

**Flow per "training action":**

1. Player chooses: "What do you want to do?" → Study Strength / Agility / Smarts / Spirit, and "With whom?" → Teacher / Parent / Mentor / Pet / Solo.
2. Not every source supports every skill (e.g. Teacher = Smarts, Mentor = Strength or Agility). Invalid combo = "You can’t study that with them. Choose again."
3. Game shows one question (or one micro-challenge) for that skill/source.
4. Player answers. Success → skill up; failure → no gain, maybe learn the answer.
5. Advance time by 1 unit. Show current skill levels and (if we use it) "Year 1 / 2 / 3" or "X actions until 10."

**v1 simplification:** We can ship with **one source per skill** (e.g. Teacher = Smarts only, Mentor = Strength only) and Solo for all. Add Parent and Pet in a follow-up.

---

## 5. Transition into Act 2 (current game)

**When "ready at 10" is met:**

1. **Story beat:** Print a short passage: e.g. "You’ve turned 10. You’re ready. You say goodbye and set out for Ridgecamp."
2. **Data handoff:** Call into the existing game with the same **player name**. Optionally pass:
   - **Primary skill name** (e.g. "Strength") so Act 2 can grant a small bonus (e.g. +1 health in Act 2, or +5% catch chance for "big" creatures if primary was Strength). For v1 we can skip bonus and only pass name.
3. **Start Act 2:** Run the existing `game` package (create_game_state, run_session) with that name. No need to change Act 2’s difficulty or rules for the first version; the "training" is the narrative prequel.

**Technical:** From the Act 1 module (or main entry point), when readiness is achieved, set a flag or return "act2" and the player name; the top-level runner then calls `game.main` or runs the existing loop with that name. Act 1 and Act 2 can share the same repo and launcher; we add an "Act 1" entry that, on completion, launches Act 2.

---

## 6. Minimal v1 scope (implementation checklist)

To get a playable two-act game without overbuilding:

- [ ] **Character pick:** Name only (and optionally "choose your character" from 2–3 presets that only change name/flavour text; all stats 0).
- [ ] **Skills:** Four skills (Strength, Agility, Smarts, Spirit), all start 0. Baseline = 2, primary threshold = 4, supplementary = 3.
- [ ] **Choose focus:** After all four ≥ baseline, prompt: "Pick your primary skill" then "Pick two supplementary." Fourth skill stays at baseline.
- [ ] **Time:** 30–40 "actions" total; every 10 actions = "Year 1 / 2 / 3" message; after Year 3 + thresholds met → "You're 10 and ready."
- [ ] **Learning:** One question per skill (4 questions total) stored in data; "Study [skill]" shows the question, multiple choice, success = +1. Solo only for v1 (no Teacher/Parent/Mentor/Pet yet).
- [ ] **Transition:** When ready, print story beat, then call existing `game` with player name and start Act 2.

After v1 works, add: more questions per skill, Teacher (Smarts), Mentor (Strength/Agility), then Parent and Pet.

---

## 7. Where this lives in the codebase

- **Act 1:** New module or subpackage, e.g. `game/act1/` or `game/training/`, with its own state (skills, time, focus choices), questions data, and a small loop: "choose action → run learning moment → update state → check readiness → loop or transition."
- **Entry point:** Launcher or main menu: "Start your journey" → run Act 1; when Act 1 returns "ready," run Act 2 (existing `game` loop). Optionally "Skip to Ridgecamp" for testing (go straight to Act 2).
- **Narrative doc:** `NARRATIVE_DESIGN.md` stays the single source of truth for story; this doc is the implementation spec for Act 1.

**Keep this doc updated when we change the training design.** It is the reference for building Act 1.
