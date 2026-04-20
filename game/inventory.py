"""
Inventory system: items, effects, discovery, and use.
"""
from __future__ import annotations

import random
from copy import deepcopy

from game.constants import CREATURES

# -----------------------------------------------------------------------------
# Item definitions
# -----------------------------------------------------------------------------
ITEMS: dict[str, dict] = {
    "healing_herb": {
        "name": "Healing Herb",
        "description": "Restores 15 HP. A staple for cautious Keepers.",
        "effect": "heal_15",
    },
    "capture_charm": {
        "name": "Capture Charm",
        "description": "Adds +20% catch rate on the next capture attempt.",
        "effect": "capture_bonus",
    },
    "explorer_map": {
        "name": "Explorer Map",
        "description": "Reveals creature types in a region before you enter.",
        "effect": "reveal_region",
    },
    "companion_treat": {
        "name": "Companion Treat",
        "description": "Boosts bond by +1 with your chosen companion.",
        "effect": "bond_plus_1",
    },
}

# Item find pool (weights for random discovery)
ITEM_FIND_POOL = list(ITEMS.keys())


def show_inventory(state: dict) -> None:
    """Print the player's current inventory."""
    inv = state.get("inventory", {})
    if not inv:
        print("\n🎒 Your pack is empty.")
        return
    print("\n🎒 Inventory:")
    for item_id, count in inv.items():
        if count <= 0:
            continue
        item = ITEMS[item_id]
        print(f"  [{count}x] {item['name']} — {item['description']}")


def use_item(state: dict, item_id: str) -> str:
    """Apply an item's effect and return a result message. Consumes one of the item."""
    inv = state.get("inventory", {})
    if inv.get(item_id, 0) <= 0:
        return "You don't have that."

    effect = ITEMS[item_id]["effect"]

    if effect == "heal_15":
        old_hp = state["health"]
        state["health"] = min(99, state["health"] + 15)
        healed = state["health"] - old_hp
        inv[item_id] -= 1
        return f"🌿 You use a Healing Herb and recover {healed} HP. (HP: {old_hp} → {state['health']})"

    elif effect == "capture_bonus":
        inv[item_id] -= 1
        state["_capture_charm_active"] = True
        return "✨ You attune a Capture Charm — your next capture gains +20%!"

    elif effect == "reveal_region":
        inv[item_id] -= 1
        # Tell the player which regions they've visited and what creatures live there
        from game.constants import REGION_IDS
        lines = ["🗺️  Explorer Map reveals:"]
        for rid in REGION_IDS:
            creatures_in_region = [c["name"] for c in CREATURES if c["habitat"] == rid]
            if creatures_in_region:
                lines.append(f"  {rid.title()}: {', '.join(creatures_in_region)}")
            else:
                lines.append(f"  {rid.title()}: nothing detected")
        return "\n".join(lines)

    elif effect == "bond_plus_1":
        captured = state.get("captured", [])
        if not captured:
            inv[item_id] -= 1
            return "🎒 You use a Companion Treat, but have no companions yet. (Item saved.)"
        # Apply to the first companion in the list
        companion = captured[0]
        old_bond = companion.get("bond", 0)
        companion["bond"] = old_bond + 1
        inv[item_id] -= 1
        return f"🐾 {companion['name']} loves the treat! Bond: {old_bond} → {companion['bond']}"

    return "Item could not be used."


def find_item_on_explore(state: dict) -> str | None:
    """10% chance to discover a random item when exploring. Returns item_id or None."""
    if random.random() > 0.10:
        return None
    item_id = random.choice(ITEM_FIND_POOL)
    state.setdefault("inventory", {})
    state["inventory"][item_id] = state["inventory"].get(item_id, 0) + 1
    return item_id


def get_creatures_in_region(region: str) -> list[dict]:
    """Return creature definitions for a given region."""
    return [c for c in CREATURES if c["habitat"] == region]


def attempt_mini_capture(state: dict, creature: dict) -> bool:
    """Stripped-down single-attempt capture for wild creature sightings. Returns success."""
    from game.capture import CAPTURE_STORY_BONUS, CAPTURE_HARDCORE_PENALTY
    ball_type = "mini" if creature["size"] == "small" else "mega"

    if state["balls"][ball_type] <= 0:
        print(f"No {ball_type.title()} Orbs left — you can't attempt the catch!")
        return False

    state["balls"][ball_type] -= 1
    chance = creature["base_catch"]
    if state["difficulty"] == "story":
        chance += CAPTURE_STORY_BONUS
    elif state["difficulty"] == "hardcore":
        chance -= CAPTURE_HARDCORE_PENALTY

    # Apply capture charm if active
    if state.pop("_capture_charm_active", False):
        chance = min(0.99, chance + 0.20)

    roll = random.random()
    if roll <= chance:
        print(f"✨ Click! {creature['name']} was captured!")
        state["captured"].append(creature)
        return True
    else:
        print(f"💨 {creature['name']} darts away before you could seal the orb.")
        return False
