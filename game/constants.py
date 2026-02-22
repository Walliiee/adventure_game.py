"""
Game data and configuration. Keeps content separate from logic.
"""

# -----------------------------------------------------------------------------
# Creatures (by habitat: meadow, ruins, river, canyon, highlands, forest)
# -----------------------------------------------------------------------------
CREATURES = [
    {"name": "Moss Bunny", "size": "small", "habitat": "meadow", "temperament": "gentle", "base_catch": 0.78},
    {"name": "Spark Finch", "size": "small", "habitat": "ruins", "temperament": "curious", "base_catch": 0.74},
    {"name": "Pebble Otter", "size": "small", "habitat": "river", "temperament": "playful", "base_catch": 0.72},
    {"name": "Iron Tusk", "size": "big", "habitat": "canyon", "temperament": "stubborn", "base_catch": 0.4},
    {"name": "Thunder Yak", "size": "big", "habitat": "highlands", "temperament": "proud", "base_catch": 0.36},
    {"name": "Moonclaw Lynx", "size": "big", "habitat": "forest", "temperament": "fierce", "base_catch": 0.34},
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
REGION_IDS = ("meadow", "ruins", "river", "canyon", "forest")
REGION_DISPLAY = (
    "🌾 Sunmeadow",
    "🏛️ Old Ruins",
    "🏞️ Silver River",
    "🪨 Storm Canyon",
    "🌲 Moonwood",
)
REGION_ALIASES = {"meadow": 0, "ruins": 1, "river": 2, "canyon": 3, "moonwood": 4, "forest": 4}

# -----------------------------------------------------------------------------
# NPCs (Ridgecamp crew)
# -----------------------------------------------------------------------------
NPC_NAMES = ("Mira", "Sol", "Ari")
NPC_DISPLAY = (
    "👩‍🌾 Ranger Mira  - animal tracker and care expert",
    "🛠️ Mechanic Sol   - builds stronger capture orbs",
    "🧢 Rival Ari      - bold challenger who pushes your growth",
)

# -----------------------------------------------------------------------------
# Capture rules
# -----------------------------------------------------------------------------
WRONG_BALL_PENALTY = 0.2
MIN_COMPANIONS_FOR_EXHIBITION = 2
