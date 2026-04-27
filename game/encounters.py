"""
Random encounters while traveling between regions.
"""
from __future__ import annotations

import random
from copy import deepcopy

from game.constants import CREATURES
from game.skills import get_skill_bonus, WILD_SIGHTING


# (encounter_type, weight)
ENCOUNTER_TYPES = [
    ("wild_creature", 0.20),    # 20%
    ("healing_spring", 0.30),   # 30%
    ("lost_traveler", 0.20),    # 20%
    ("storm", 0.15),            # 15%
    ("nothing", 0.15),          # 15%
]


def _weighted_encounter() -> str:
    """Roll a weighted random encounter type."""
    r = random.random()
    cumulative = 0.0
    for enc_type, weight in ENCOUNTER_TYPES:
        cumulative += weight
        if r <= cumulative:
            return enc_type
    return "nothing"


def roll_encounter(state: dict) -> str | None:
    """Decide if a random encounter fires when moving to a new region. Returns type or None."""
    # Act 1 skill bonus: Agility/Stealth makes wild creature sightings always trigger
    sight_bonus = get_skill_bonus(state, WILD_SIGHTING)
    if sight_bonus >= 1.0:
        return "wild_creature"
    elif sight_bonus > 0:
        # Supplementary: boost wild_creature weight significantly
        if random.random() < sight_bonus:
            return "wild_creature"
    return _weighted_encounter()


def handle_encounter(encounter_type: str, state: dict) -> str:
    """Process an encounter and return a description string."""
    if encounter_type == "nothing":
        return "The path is quiet. Nothing stirs."

    elif encounter_type == "healing_spring":
        old_hp = state["health"]
        state["health"] = min(99, state["health"] + 20)
        healed = state["health"] - old_hp
        return f"💧 You discover a hidden spring! Fresh water restores {healed} HP. (HP: {old_hp} → {state['health']})"

    elif encounter_type == "storm":
        state["health"] = max(0, state["health"] - 10)
        return f"⛈️ A sudden storm hits! You take 10 damage and retreat to camp. (HP: {state['health']})"

    elif encounter_type == "lost_traveler":
        from game.inventory import ITEMS, ITEM_FIND_POOL
        item_id = random.choice(ITEM_FIND_POOL)
        state.setdefault("inventory", {})
        state["inventory"][item_id] = state["inventory"].get(item_id, 0) + 1
        item_name = ITEMS[item_id]["name"]
        return f"🥾 A lost traveler shares their supplies — you receive 1x {item_name}!"

    elif encounter_type == "wild_creature":
        region = state.get("current_region", None)
        if region:
            candidates = [c for c in CREATURES if region in c["habitat"]]
        if not candidates:
            candidates = CREATURES
        creature = deepcopy(random.choice(candidates))
        creature["level"] = 1
        creature["bond"] = 1
        creature["mood"] = "curious"

        # Prompt the player inline (blocks until answered)
        from game.cli import get_player_choice
        options = [
            f"Try to catch it ({creature['name']}, {creature['size']})",
            "Let it go peacefully",
        ]
        pick = get_player_choice(options, {"catch": 0, "let": 1, "no": 1, "yes": 0})

        if pick == 0:
            from game.inventory import attempt_mini_capture
            success = attempt_mini_capture(state, creature)
            if success:
                return f"A wild {creature['name']} darts across your path — and you caught it!"
            else:
                return f"A wild {creature['name']} darts across your path — it got away."
        else:
            return f"A wild {creature['name']} darts across your path. You let it go."

    return "An odd feeling passes."
