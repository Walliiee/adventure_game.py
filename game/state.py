"""
Game state: creation and structure. State is a dict for simplicity;
all keys are defined here.
"""
from game.constants import (
    BALLS_BY_DIFFICULTY,
    HEALTH_BY_DIFFICULTY,
    NPC_NAMES,
)


def create_game_state(player_name: str, difficulty: str) -> dict:
    """Build a fresh game state for the given player and difficulty."""
    return {
        "name": player_name,
        "difficulty": difficulty,
        "health": HEALTH_BY_DIFFICULTY[difficulty],
        "captured": [],
        "turn": 1,
        "region_progress": set(),
        "balls": dict(BALLS_BY_DIFFICULTY[difficulty]),  # mutable copy
        "npc_bond": {name: 0 for name in NPC_NAMES},
    }
