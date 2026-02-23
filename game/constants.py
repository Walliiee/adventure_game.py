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
REGION_FLAVOR = {
    "meadow": "Sunmeadow rolls like a green ocean. Wind bends the tall grass around hidden paths.",
    "ruins": "Old Ruins stand half-buried in moss. Echoes make every step feel like a story returning.",
    "river": "Silver River glitters under shifting light. Smooth stones mark safe crossings for careful Keepers.",
    "canyon": "Storm Canyon rumbles with distant thunder. Loose gravel punishes rushed movement.",
    "forest": "Moonwood is cool and shadowed. Quiet observation reveals life before noise ever will.",
}

# -----------------------------------------------------------------------------
# NPCs (Ridgecamp crew)
# -----------------------------------------------------------------------------
NPC_NAMES = ("Mira", "Sol", "Ari")
NPC_DISPLAY = (
    "👩‍🌾 Ranger Mira  - animal tracker and care expert",
    "🛠️ Mechanic Sol   - builds stronger capture orbs",
    "🧢 Rival Ari      - bold challenger who pushes your growth",
)
NPC_SCENES_BY_REGION = {
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
WRONG_BALL_PENALTY = 0.2
MIN_COMPANIONS_FOR_EXHIBITION = 2
