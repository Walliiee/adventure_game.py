"""
Game state: creation and structure.
"""
from __future__ import annotations

from typing import TypedDict

from game.constants import (
    BALLS_BY_DIFFICULTY,
    HEALTH_BY_DIFFICULTY,
    NPC_NAMES,
)


class Companion(TypedDict):
    name: str
    size: str
    level: int
    bond: int
    mood: str


class GameState(TypedDict):
    name: str
    difficulty: str
    health: int
    captured: list[Companion]
    turn: int
    region_progress: set[str]
    balls: dict[str, int]
    npc_bond: dict[str, int]


def create_game_state(player_name: str, difficulty: str) -> GameState:
    """Build a fresh game state for the given player and difficulty."""
    return {
        "name": player_name,
        "difficulty": difficulty,
        "health": HEALTH_BY_DIFFICULTY[difficulty],
        "captured": [],
        "turn": 1,
        "region_progress": set(),
        "balls": dict(BALLS_BY_DIFFICULTY[difficulty]),
        "npc_bond": {name: 0 for name in NPC_NAMES},
    }
