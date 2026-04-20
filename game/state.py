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
    personality: str
    ability_used_today: bool


class GameState(TypedDict):
    name: str
    difficulty: str
    health: int
    captured: list[Companion]
    turn: int
    region_progress: set[str]
    balls: dict[str, int]
    npc_bond: dict[str, int]
    seen_npc_scenes: set[str]
    # Tracking for endings and achievements
    regions_visited: set[str]
    peaceful_leaves: int
    exhibition_perfect_win: bool
    exhibition_won: bool
    achievements_unlocked: list[str]
    # Act 1 skill choices carried into Act 2
    primary_skill: str | None
    supplementary_skills: list[str]
    inventory: dict[str, int]
    # Companion abilities and economy
    coins: int
    companion_energized: bool


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
        "seen_npc_scenes": set(),
        # Tracking for endings and achievements
        "regions_visited": set(),
        "peaceful_leaves": 0,
        "exhibition_perfect_win": False,
        "exhibition_won": False,
        "achievements_unlocked": [],
        # Act 1 skill choices carried into Act 2
        "primary_skill": None,
        "supplementary_skills": [],
        "inventory": {"healing_herb": 2, "capture_charm": 1},
        # Companion abilities and economy
        "coins": 10,
        "companion_energized": False,
    }
