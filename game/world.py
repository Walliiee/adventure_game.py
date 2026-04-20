"""
World and spawning: regions, creature discovery, and light narrative beats.
"""
from __future__ import annotations

import random
from copy import deepcopy

from game.constants import (
    CREATURES,
    REGION_IDS,
    REGION_DISPLAY,
    REGION_ALIASES,
    REGION_FLAVOR,
    NPC_SCENES_BY_REGION,
)
from game.cli import get_player_choice


def choose_region(state: dict) -> str:
    """Let the player pick a region; update state's region_progress and return region id."""
    print("\nChoose a region to explore:")
    idx = get_player_choice(REGION_DISPLAY, REGION_ALIASES)
    region = REGION_IDS[idx]
    state["region_progress"].add(region)
    # Also track for achievements/endings
    state["regions_visited"] = state.get("regions_visited", set())
    state["regions_visited"].add(region)
    return region


def describe_region(region: str) -> str:
    """Return flavor text for the chosen region."""
    return REGION_FLAVOR.get(region, "You enter a quiet stretch of wild terrain.")


def get_npc_scene(state: dict, region: str) -> str | None:
    """Return one narrative NPC line per region, without repeating the same scene in a run."""
    candidates = NPC_SCENES_BY_REGION.get(region, [])
    if not candidates:
        return None

    unseen = [line for line in candidates if line not in state["seen_npc_scenes"]]
    pool = unseen or candidates
    scene = random.choice(pool)
    state["seen_npc_scenes"].add(scene)
    return scene


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
