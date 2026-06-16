"""
Companion actions: train, play, and daily abilities.
"""
import json
import random
from pathlib import Path

from game.constants import NPC_NAMES
from game.cli import get_player_choice


# Load companion dialogue data
_DIALOGUE_PATH = Path(__file__).resolve().parent.parent / "data" / "companion_dialogue.json"


def _load_dialogue():
    try:
        with open(_DIALOGUE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _get_bond_level(companion: dict) -> str:
    """Return bond level category: low, mid, or high."""
    bond = companion.get("bond", 0)
    if bond <= 3:
        return "low"
    elif bond <= 6:
        return "mid"
    else:
        return "high"


def _get_dialogue(companion: dict) -> str:
    """Get a random dialogue line based on personality, bond, and mood."""
    dialogue_data = _load_dialogue()
    personality = companion.get("personality", "brave")
    bond_level = _get_bond_level(companion)
    mood = companion.get("mood", "motivated")

    try:
        lines = dialogue_data[personality][bond_level][mood]
        return random.choice(lines)
    except (KeyError, IndexError):
        return "*looks at you expectantly*"


def _get_personality_bonus(companion: dict, action: str) -> dict:
    """Return bonus info for personality-based actions."""
    personality = companion.get("personality", "brave")

    if personality == "brave":
        return {"type": "capture", "bonus": 0.1, "desc": "Brave companion: +10% capture rate"}
    elif personality == "timid":
        return {"type": "healing", "bonus": 20, "desc": "Timid companion: +20 HP from healing springs"}
    elif personality == "playful":
        return {"type": "bond", "bonus": 1, "desc": "Playful companion: +1 extra bond from play"}
    return {}


def pick_companion(state: dict, action: str):
    """Let player choose a companion for the given action; return companion or None."""
    if not state["captured"]:
        print(f"You need a companion before you can {action}.")
        return None
    print(f"\nChoose a companion to {action}:")
    options = [f"{c['name']} ({c['size']}, {c.get('personality', 'brave')})" for c in state["captured"]]
    idx = get_player_choice(options)
    return state["captured"][idx]


def train_companion(state: dict) -> bool:
    """Train selected companion. Returns True if an action was performed."""
    companion = pick_companion(state, "train")
    if not companion:
        return False
    print(f"You run drills with {companion['name']}: agility loops, focus tests, and team signals.")
    companion["level"] += 1
    companion["bond"] += 1
    companion["mood"] = "motivated"

    # Show dialogue
    dialogue = _get_dialogue(companion)
    print(f"💬 {companion['name']}: \"{dialogue}\"")

    state["npc_bond"][NPC_NAMES[2]] = state["npc_bond"].get(NPC_NAMES[2], 0) + 1  # scout (Mira)
    return True


def play_with_companion(state: dict) -> bool:
    """Play with selected companion. Returns True if an action was performed."""
    companion = pick_companion(state, "play")
    if not companion:
        return False
    print(f"You play fetch and rhythm games with {companion['name']} at camp.")

    # Playful personality bonus: +1 extra bond from play
    personality = companion.get("personality", "brave")
    bonus = 2 if personality == "playful" else 1
    if personality == "playful":
        print(f"🎾 {companion['name']} is extra playful and bonds faster!")

    companion["bond"] += bonus
    companion["mood"] = "happy"

    # Show dialogue
    dialogue = _get_dialogue(companion)
    print(f"💬 {companion['name']}: \"{dialogue}\"")

    state["health"] += 1
    state["npc_bond"][NPC_NAMES[1]] = state["npc_bond"].get(NPC_NAMES[1], 0) + 1  # merchant (Torv)
    return True


def get_brave_capture_bonus(companion: dict) -> float:
    """Return capture rate bonus if companion is brave."""
    if companion.get("personality") == "brave":
        return 0.1
    return 0.0


def get_timid_healing_bonus(companion: dict) -> int:
    """Return extra healing if companion is timid."""
    if companion.get("personality") == "timid":
        return 20
    return 0


def use_companion_ability(state: dict, companion: dict) -> str:
    """Use companion's daily active ability. Returns result message."""
    personality = companion.get("personality", "brave")

    # Check if already used today
    used_today = companion.get("ability_used_today", False)
    if used_today:
        return f"{companion['name']} has already used their ability today."

    companion["ability_used_today"] = True

    if personality == "brave":
        return f"🦅 {companion['name']} scouts ahead! (Scout ability used)"
    elif personality == "timid":
        heal_amount = 10
        state["health"] = min(state["health"] + heal_amount, 20)  # Cap at reasonable max
        return f"💚 {companion['name']} comforts you, restoring {heal_amount} HP!"
    elif personality == "playful":
        state["companion_energized"] = True
        return f"⚡ {companion['name']} energizes you! Next action will skip fatigue penalty."

    return "Ability used."


def reset_daily_abilities(state: dict) -> None:
    """Reset all companion ability uses for a new day."""
    for companion in state.get("captured", []):
        companion["ability_used_today"] = False
    state.pop("companion_energized", None)
