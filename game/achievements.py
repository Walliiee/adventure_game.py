"""
Achievement system: 8 achievements that unlock during gameplay.
"""
from __future__ import annotations
from typing import TypedDict


class AchievementData(TypedDict):
    id: str
    title: str
    description: str
    unlocked: bool


ACHIEVEMENTS: dict[str, AchievementData] = {
    "first_catch": {
        "id": "first_catch",
        "title": "First Catch",
        "description": "Catch your first creature",
        "unlocked": False
    },
    "explorer": {
        "id": "explorer",
        "title": "Explorer",
        "description": "Visit 3 different regions",
        "unlocked": False
    },
    "completionist": {
        "id": "completionist",
        "title": "Completionist",
        "description": "Visit all regions",
        "unlocked": False
    },
    "bonded": {
        "id": "bonded",
        "title": "Bonded",
        "description": "Reach max bond (5+) with any companion",
        "unlocked": False
    },
    "collector": {
        "id": "collector",
        "title": "Collector",
        "description": "Catch 5+ creatures",
        "unlocked": False
    },
    "master_collector": {
        "id": "master_collector",
        "title": "Master Collector",
        "description": "Catch 10+ creatures",
        "unlocked": False
    },
    "peaceful_keeper": {
        "id": "peaceful_keeper",
        "title": "Peaceful Keeper",
        "description": "Leave 3 creatures peacefully",
        "unlocked": False
    },
    "exhibition_champion": {
        "id": "exhibition_champion",
        "title": "Exhibition Champion",
        "description": "Win the exhibition",
        "unlocked": False
    }
}


def check_achievements(state: dict) -> list[str]:
    """
    Check which achievements should be unlocked based on current state.
    Returns list of newly unlocked achievement IDs.
    """
    unlocked_ids = state.get("achievements_unlocked", [])
    newly_unlocked = []
    
    captured = state.get("captured", [])
    peaceful_leaves = state.get("peaceful_leaves", 0)
    region_progress = state.get("region_progress", set())
    exhibition_won = state.get("exhibition_won", False)
    
    # First Catch
    if "first_catch" not in unlocked_ids and len(captured) >= 1:
        newly_unlocked.append("first_catch")
    
    # Explorer (3 regions)
    if "explorer" not in unlocked_ids and len(region_progress) >= 3:
        newly_unlocked.append("explorer")
    
    # Completionist (all 5 regions)
    all_regions = {"meadow", "ruins", "river", "canyon", "forest"}
    if "completionist" not in unlocked_ids and region_progress >= all_regions:
        newly_unlocked.append("completionist")
    
    # Bonded (max bond 5+ with any companion)
    if "bonded" not in unlocked_ids:
        for c in captured:
            if c.get("bond", 0) >= 5:
                newly_unlocked.append("bonded")
                break
    
    # Collector (5+ creatures)
    if "collector" not in unlocked_ids and len(captured) >= 5:
        newly_unlocked.append("collector")
    
    # Master Collector (10+ creatures)
    if "master_collector" not in unlocked_ids and len(captured) >= 10:
        newly_unlocked.append("master_collector")
    
    # Peaceful Keeper (3+ peaceful leaves)
    if "peaceful_keeper" not in unlocked_ids and peaceful_leaves >= 3:
        newly_unlocked.append("peaceful_keeper")
    
    # Exhibition Champion
    if "exhibition_champion" not in unlocked_ids and exhibition_won:
        newly_unlocked.append("exhibition_champion")
    
    return newly_unlocked


def show_achievement(achievement_id: str) -> None:
    """Print achievement unlock notification."""
    ach = ACHIEVEMENTS.get(achievement_id)
    if ach:
        print(f"\n🏆 Achievement Unlocked: {ach['title']} - {ach['description']}")
