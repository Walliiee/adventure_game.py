# Wildlands: Orb Catcher Adventure

**A creature-catching CLI adventure** — train your skills, catch wild creatures, build your team, and earn your place as a Keeper.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

---

## Quick Demo

```
$ python adventure_game.py

  ╔═══════════════════════════════════════╗
  ║   WILDLANDS: ORB CATCHER ADVENTURE    ║
  ╚═══════════════════════════════════════╝

  What's your name, young Trainer? █
```

---

## Features

- **Two-act structure** — grow your character (Act 1: ages 7–10 with skill training) then enter the Wildlands (Act 2: capture loop).
- **Persistent save/load** — game auto-saves on exit; save slots accessible from the camp menu.
- **6 distinct endings** — determined by difficulty, creature bonds, and narrative choices.
- **8 achievements** — unlock milestones for captures, exhibitions, companions, and exploration.
- **4-slot inventory** — equip rare items that modify encounters or capture odds.
- **5 random encounter types** — weather, creature sightings, travelers, NPC events, and treasure.
- **Skill transfer** — abilities trained in Act 1 carry forward as modifiers in Act 2.
- **Companion system** — three unique companions (Emberfang, Shadowmite, Stormcrest) with daily abilities.
- **NPC shop + coin economy** — earn coins by catching creatures and winning exhibitions; spend them at the camp shop.
- **JSON-driven content** — creatures, regions, NPCs, and encounters defined in `data/` for easy editing.
- **No dependencies** — pure Python 3.9+ standard library; runs anywhere.

---

## How to Play

### Install

```bash
# No installation needed — just clone and run
git clone https://github.com/Walliiee/adventure_game.py.git
cd adventure_game.py
```

### Run

```bash
# Full game (Act 1 → Act 2)
python adventure_game.py

# Skip Act 1, jump straight to Act 2 (for testing)
python adventure_game.py --test
```

### Controls

| Action | Input |
|---|---|
| Select menu option | Type number (1, 2, 3…) |
| Confirm / continue | `y` or `enter` |
| Quit / cancel | `q` |
| Save game | Choose "Save" from camp menu |
| Load game | Choose "Load" on the title screen |

---

## Game Mechanics

### Act 1 — Training (Ages 7–10)

Answer questions to train four skills — **Speed, Strength, Smarts, Stealth**. At age 10, choose:
- **1 primary skill** (significant bonus in Act 2)
- **2 supplementary skills** (moderate bonus)

These bonuses carry forward, affecting capture odds, encounter difficulty, and companion performance.

### Act 2 — The Wildlands (Keeper Loop)

Arrive at **Ridgecamp** and choose a difficulty. Each day you can:
- **Explore** — travel to regions, encounter wild creatures
- **Capture** — attempt to catch creatures (capture odds depend on skill bonuses + item bonuses)
- **Camp** — rest (restores companion ability), save/load, visit NPCs, view achievements
- **Companion activities** — train for exhibitions, play for mood, enter exhibitions for coin rewards

### Companions

| Name | Personality | Daily Ability |
|---|---|---|
| Ember the Emberfang | Enthusiastic & bold | Embolden — next capture has +15% bonus |
| Zaph the Shadowmite | Laid-back & clever | Scout — guarantees a rare creature in next explore |
| Lira the Stormcrest | Graceful & cautious | Calm — next random encounter is always positive |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local dev setup, quality checks, and PR process.

## Roadmap

Current ideas and planned features are tracked in [GAME_IMPROVEMENT_IDEAS.md](GAME_IMPROVEMENT_IDEAS.md).
