"""
Game data and configuration. Keeps content separate from logic.
Data is loaded from JSON files in data/ at startup, with hardcoded fallbacks.
"""
from __future__ import annotations

import json
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_json(filename: str, fallback: list | dict) -> list | dict:
    """Load a JSON data file, returning fallback if file is missing or corrupt."""
    path = _DATA_DIR / filename
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback


def _load_creatures() -> list[dict]:
    data = _load_json("creatures.json", [])
    if data:
        return data
    # Fallback: hardcoded defaults
    return _CREATURES_FALLBACK


def _load_regions() -> tuple[list[dict], tuple, tuple, dict, dict]:
    """Returns (region_data, REGION_IDS, REGION_DISPLAY, REGION_ALIASES, REGION_FLAVOR)."""
    data = _load_json("regions.json", [])
    if data:
        ids = tuple(r["id"] for r in data)
        display = tuple(r["display"] for r in data)
        flavor = {r["id"]: r["flavor"] for r in data}
        aliases = {}
        for i, rid in enumerate(ids):
            aliases[rid] = i
            # Common alias: 'moonwood' -> 'forest'
            if rid == "forest":
                aliases["moonwood"] = i
        return data, ids, display, aliases, flavor
    return data, _REGION_IDS_FALLBACK, _REGION_DISPLAY_FALLBACK, _REGION_ALIASES_FALLBACK, _REGION_FLAVOR_FALLBACK


def _load_npcs() -> tuple[tuple, tuple, dict]:
    """Returns (NPC_NAMES, NPC_DISPLAY, NPC_SCENES_BY_REGION)."""
    data = _load_json("npcs.json", [])
    if data:
        names = tuple(n["name"] for n in data)
        display = tuple(n["display"] for n in data)
        scenes = {}
        for n in data:
            for region, lines in n.get("scenes_by_region", {}).items():
                if region not in scenes:
                    scenes[region] = []
                scenes[region].extend(lines)
        return names, display, scenes
    return _NPC_NAMES_FALLBACK, _NPC_DISPLAY_FALLBACK, _NPC_SCENES_FALLBACK

# -----------------------------------------------------------------------------
# Creatures (by habitat: meadow, ruins, river, canyon, highlands, forest)
# -----------------------------------------------------------------------------
_CREATURES_FALLBACK = [
    {"name": "Moss Bunny", "size": "small", "habitat": ["meadow"], "temperament": "gentle", "catch_rate_base": 0.78},
    {"name": "Spark Finch", "size": "small", "habitat": ["ruins"], "temperament": "curious", "catch_rate_base": 0.74},
    {"name": "Pebble Otter", "size": "small", "habitat": ["river"], "temperament": "playful", "catch_rate_base": 0.72},
    {"name": "Iron Tusk", "size": "big", "habitat": ["canyon"], "temperament": "stubborn", "catch_rate_base": 0.4},
    {"name": "Thunder Yak", "size": "big", "habitat": ["highlands"], "temperament": "proud", "catch_rate_base": 0.36},
    {"name": "Moonclaw Lynx", "size": "big", "habitat": ["forest"], "temperament": "fierce", "catch_rate_base": 0.34},
]

# -----------------------------------------------------------------------------
# Difficulty
# -----------------------------------------------------------------------------
DIFFICULTIES = ("story", "classic", "hardcore")
DIFFICULTY_DISPLAY = ("Story", "Classic", "Hardcore")
HEALTH_BY_DIFFICULTY = {"story": 16, "classic": 12, "hardcore": 9}
BALLS_BY_DIFFICULTY = {
    "story": {"mini": 8, "mega": 5},
    "classic": {"mini": 6, "mega": 3},
    "hardcore": {"mini": 4, "mega": 2},
}
# Capture chance modifiers by difficulty
CAPTURE_STORY_BONUS = 0.1
CAPTURE_HARDCORE_PENALTY = 0.08
# Exhibition win threshold (team_power + synergy_bonus >= threshold)
EXHIBITION_THRESHOLD = {"story": 18, "classic": 22, "hardcore": 26}

# -----------------------------------------------------------------------------
# World: regions
# -----------------------------------------------------------------------------
_REGION_IDS_FALLBACK = ("meadow", "ruins", "river", "canyon", "forest")
_REGION_DISPLAY_FALLBACK = (
    "🌾 Sunmeadow",
    "🏛️ Old Ruins",
    "🏞️ Silver River",
    "🪨 Storm Canyon",
    "🌲 Moonwood",
)
_REGION_ALIASES_FALLBACK = {"meadow": 0, "ruins": 1, "river": 2, "canyon": 3, "moonwood": 4, "forest": 4}
_REGION_FLAVOR_FALLBACK = {
    "meadow": "Sunmeadow rolls like a green ocean. Wind bends the tall grass around hidden paths.",
    "ruins": "Old Ruins stand half-buried in moss. Echoes make every step feel like a story returning.",
    "river": "Silver River glitters under shifting light. Smooth stones mark safe crossings for careful Keepers.",
    "canyon": "Storm Canyon rumbles with distant thunder. Loose gravel punishes rushed movement.",
    "forest": "Moonwood is cool and shadowed. Quiet observation reveals life before noise ever will.",
}

# -----------------------------------------------------------------------------
# NPCs (Ridgecamp crew)
# -----------------------------------------------------------------------------
_NPC_NAMES_FALLBACK = ("Mira", "Sol", "Ari")
_NPC_DISPLAY_FALLBACK = (
    "👩‍🌾 Ranger Mira  - animal tracker and care expert",
    "🛠️ Mechanic Sol   - builds stronger capture orbs",
    "🧢 Rival Ari      - bold challenger who pushes your growth",
)
_NPC_SCENES_FALLBACK = {
    "meadow": [
        "Mira kneels by bent grass: 'Tracks fork here. Watch the small signs before you throw an orb.'",
        "Ari grins: 'Easy terrain. Show me clean fundamentals, not luck.'",
    ],
    "ruins": [
        "Sol taps a cracked pillar: 'Stone reflects sound. Quiet steps matter more here.'",
        "Mira whispers: 'If birds go silent, pause. Something bigger is nearby.'",
    ],
    "river": [
        "Mira points at fresh prints by the bank: 'Water tells stories. Read them before moving.'",
        "Sol checks your orb latch: 'Humidity can jam mechanisms. Keep your gear dry.'",
    ],
    "canyon": [
        "Ari calls from above: 'Control your footing. One bad sprint and you lose the approach.'",
        "Sol studies the cliff walls: 'Echoes can spook creatures. Time your movements between gusts.'",
    ],
    "forest": [
        "Mira lowers her voice: 'Moonwood rewards patience. Let the creatures choose to reveal themselves.'",
        "Ari folds his arms: 'No shortcuts in deep cover. Earn every encounter.'",
    ],
}

# -----------------------------------------------------------------------------
# Capture rules
# -----------------------------------------------------------------------------
WRONG_BALL_PENALTY = 0.30
MIN_COMPANIONS_FOR_EXHIBITION = 2


# --- Loaded constants (from JSON with hardcoded fallback) ---
CREATURES = _load_creatures()
_region_data, REGION_IDS, REGION_DISPLAY, REGION_ALIASES, REGION_FLAVOR = _load_regions()
NPC_NAMES, NPC_DISPLAY, NPC_SCENES_BY_REGION = _load_npcs()
