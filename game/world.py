"""
World and spawning: regions, creature discovery.
"""
import random
from copy import deepcopy

from game.constants import CREATURES, REGION_IDS, REGION_DISPLAY, REGION_ALIASES
from game.cli import get_player_choice


def choose_region(state: dict) -> str:
    """Let the player pick a region; update state's region_progress and return region id."""
    print("\nChoose a region to explore:")
    idx = get_player_choice(REGION_DISPLAY, REGION_ALIASES)
    region = REGION_IDS[idx]
    state["region_progress"].add(region)
    return region


def find_creature(region: str) -> dict:
    """Spawn a creature for the given region (level 1, bond 1, mood curious)."""
    candidates = [c for c in CREATURES if c["habitat"] == region]
    if not candidates:
        candidates = CREATURES
    creature = deepcopy(random.choice(candidates))
    creature["level"] = 1
    creature["bond"] = 1
    creature["mood"] = "curious"
    return creature
