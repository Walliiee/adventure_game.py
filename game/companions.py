"""
Companion actions: train, play, exhibition match.
"""
from game.constants import (
    MIN_COMPANIONS_FOR_EXHIBITION,
    EXHIBITION_THRESHOLD,
    NPC_NAMES,
)
from game.cli import get_player_choice


def pick_companion(state: dict, action: str):
    """Let player choose a companion for the given action; return companion or None."""
    if not state["captured"]:
        print(f"You need a companion before you can {action}.")
        return None
    print(f"\nChoose a companion to {action}:")
    options = [f"{c['name']} ({c['size']})" for c in state["captured"]]
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
    state["npc_bond"][NPC_NAMES[2]] += 1  # Ari
    return True


def play_with_companion(state: dict) -> bool:
    """Play with selected companion. Returns True if an action was performed."""
    companion = pick_companion(state, "play")
    if not companion:
        return False
    print(f"You play fetch and rhythm games with {companion['name']} at camp.")
    companion["bond"] += 2
    companion["mood"] = "happy"
    state["health"] += 1
    state["npc_bond"][NPC_NAMES[1]] += 1  # Sol
    return True


def run_exhibition(state: dict) -> tuple[bool, bool]:
    """Run the exhibition match. Returns tuple[won: bool, action_performed: bool]."""
    print("\n🏟️ Ridgecamp Exhibition Match begins!")
    if len(state["captured"]) < MIN_COMPANIONS_FOR_EXHIBITION:
        print("You needed at least 2 companions to compete. You are not ready yet.")
        return False, False

    team_power = sum(c["level"] + c["bond"] for c in state["captured"])
    bonus = len(state["region_progress"]) + sum(state["npc_bond"].values())
    threshold = EXHIBITION_THRESHOLD[state["difficulty"]]

    print(f"Team Power: {team_power} | Synergy Bonus: {bonus} | Target: {threshold}")
    if team_power + bonus >= threshold:
        print("🎉 Your companions perform brilliantly. Ridgecamp crowns you Champion Keeper!")
        return True, True
    print("Ari wins this season, but your team shows promise. Train harder and return.")
    return False, True
