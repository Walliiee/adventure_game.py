"""
NPC interactions, shop, and daily tips.
"""
import json
import random
from pathlib import Path
from typing import Optional

from game.constants import REGION_IDS
from game.cli import get_player_choice


# NPC data path
_NPC_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "npcs.json"


def _load_npcs() -> list:
    """Load NPC data from JSON."""
    try:
        with open(_NPC_DATA_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _get_npc_by_id(npc_id: str) -> Optional[dict]:
    """Get NPC data by ID/name."""
    npcs = _load_npcs()
    for npc in npcs:
        if npc.get("name", "").lower() == npc_id.lower():
            return npc
    return None


def _get_preferred_region(state: dict) -> str:
    """Analyze player's preferred region based on visits."""
    visits = state.get("regions_visited", set())
    if visits:
        # Return the most visited region, or first in set
        return list(visits)[0]
    return "the meadows"


def _get_suggested_region(preferred: str) -> str:
    """Suggest a different region than the preferred one."""
    all_regions = list(REGION_IDS)
    if preferred in all_regions:
        all_regions.remove(preferred)
    return random.choice(all_regions) if all_regions else "meadow"


def _get_rare_creature_region(state: dict) -> str:
    """Get the region with the rarest creature today (rotates based on turn)."""
    # Use turn number to deterministically rotate the rare creature region
    turn = state.get("turn", 1)
    rare_regions = ["forest", "canyon", "highlands", "ruins", "river", "meadow"]
    return rare_regions[turn % len(rare_regions)]


def interact_with_npc(npc_id: str, state: dict) -> None:
    """Handle dialogue and interactions with an NPC."""
    npc = _get_npc_by_id(npc_id)
    if not npc:
        print(f"NPC {npc_id} not found.")
        return
    
    role = npc.get("role", "")
    dialogue = npc.get("dialogue", {})
    
    print(f"\n{npc.get('display', npc_id)}")
    
    if role == "keeper":
        # Eldra gives daily tips based on playstyle
        print(f"💬 {dialogue.get('greeting', 'Hello, Keeper.')}")
        preferred = _get_preferred_region(state)
        suggested = _get_suggested_region(preferred)
        tip = dialogue.get("daily_tip", "Keep exploring!")
        tip = tip.replace("{preferred_region}", preferred)
        tip = tip.replace("{suggested_region}", suggested)
        print(f"📜 Eldra: \"{tip}\"")
        
    elif role == "merchant":
        # Torv runs the shop
        print(f"💬 {dialogue.get('greeting', 'Welcome to my shop!')}")
        show_shop(state)
        print(f"👋 {dialogue.get('farewell', 'Come again!')}")
        
    elif role == "scout":
        # Mira gives intel on rare creatures
        print(f"💬 {dialogue.get('greeting', 'Need intel?')}")
        rare_region = _get_rare_creature_region(state)
        intel = dialogue.get("rare_creature", "Something rare is out there.")
        intel = intel.replace("{region}", rare_region)
        print(f"📍 Mira: \"{intel}\"")
        print(f"👋 {dialogue.get('farewell', 'Stay sharp!')}")
    
    else:
        print(f"💬 {dialogue.get('greeting', 'Hello there!')}")


def show_shop(state: dict) -> None:
    """Display shop items and handle purchases."""
    npc = _get_npc_by_id("Torv")
    if not npc:
        print("Shop is closed.")
        return
    
    shop = npc.get("shop", {})
    if not shop:
        print("No items available.")
        return
    
    coins = state.get("coins", 0)
    print(f"\n🛒 Torv's Shop (You have: {coins} coins)")
    print("-" * 40)
    
    items = list(shop.items())
    options = []
    for item_id, item_data in items:
        price = item_data.get("price", 0)
        name = item_data.get("name", item_id)
        desc = item_data.get("description", "")
        owned = state.get("inventory", {}).get(item_id, 0)
        options.append(f"{name} — {price} coins ({desc}) [Owned: {owned}]")
    
    options.append("Leave shop")
    
    choice = get_player_choice(options, {"leave": len(options) - 1})
    
    if choice == len(options) - 1:
        print("You leave the shop.")
        return
    
    item_id, item_data = items[choice]
    price = item_data.get("price", 0)
    name = item_data.get("name", item_id)
    
    if coins < price:
        print(f"❌ Not enough coins! You need {price} coins for {name}.")
        return
    
    # Deduct coins and add item
    state["coins"] = coins - price
    state.setdefault("inventory", {})
    state["inventory"][item_id] = state["inventory"].get(item_id, 0) + 1
    
    print(f"✅ Purchased {name} for {price} coins! (Remaining: {state['coins']})")


def get_shop_sell_price(item_id: str) -> int:
    """Get sell price for an item (50% of buy price)."""
    npc = _get_npc_by_id("Torv")
    if not npc:
        return 0
    
    shop = npc.get("shop", {})
    item_data = shop.get(item_id, {})
    buy_price = item_data.get("price", 0)
    return max(1, buy_price // 2)  # At least 1 coin, 50% of buy price


def sell_item(state: dict, item_id: str) -> str:
    """Sell an item to the merchant. Returns result message."""
    inventory = state.get("inventory", {})
    
    if inventory.get(item_id, 0) <= 0:
        return "You don't have that item to sell."
    
    sell_price = get_shop_sell_price(item_id)
    
    # Remove item and add coins
    inventory[item_id] -= 1
    if inventory[item_id] <= 0:
        del inventory[item_id]
    
    state["coins"] = state.get("coins", 0) + sell_price
    
    npc = _get_npc_by_id("Torv")
    item_name = npc.get("shop", {}).get(item_id, {}).get("name", item_id) if npc else item_id
    
    return f"💰 Sold {item_name} for {sell_price} coins!"


def get_available_npcs(state: dict) -> list:
    """Get list of available NPCs for interaction."""
    return ["Eldra", "Torv", "Mira"]


def npc_menu(state: dict) -> bool:
    """Display NPC interaction menu. Returns True if interaction occurred."""
    npcs = get_available_npcs(state)
    
    print("\n🏕️ Ridgecamp NPCs — who would you like to speak with?")
    options = []
    for npc_id in npcs:
        npc = _get_npc_by_id(npc_id)
        if npc:
            options.append(npc.get("display", npc_id))
    options.append("Return to camp")
    
    choice = get_player_choice(options, {"back": len(options) - 1, "return": len(options) - 1})
    
    if choice == len(options) - 1:
        return False
    
    interact_with_npc(npcs[choice], state)
    return True
