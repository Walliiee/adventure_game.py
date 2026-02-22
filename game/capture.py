"""
Capture mechanic: orb choice, success roll, state updates.
"""
import random

from game.constants import (
    CAPTURE_STORY_BONUS,
    CAPTURE_HARDCORE_PENALTY,
    WRONG_BALL_PENALTY,
    NPC_NAMES,
)
from game.cli import get_player_choice


def attempt_capture(state: dict, creature: dict) -> None:
    """Run the capture flow: choose orb or leave, roll, update state."""
    ball_type = "mini" if creature["size"] == "small" else "mega"
    alt_ball = "mega" if ball_type == "mini" else "mini"

    options = [
        f"Use a {ball_type.title()} Orb (best fit)",
        f"Use a {alt_ball.title()} Orb",
        "Offer food and leave peacefully",
    ]
    aliases = {"best": 0, "alt": 1, "leave": 2, "food": 2}
    pick = get_player_choice(options, aliases)

    if pick == 2:
        print(f"You offer food to {creature['name']}. It relaxes and wanders away peacefully.")
        state["health"] += 1
        return

    chosen = ball_type if pick == 0 else alt_ball
    if state["balls"][chosen] <= 0:
        print(f"No {chosen.title()} Orbs left! The creature escapes.")
        return

    state["balls"][chosen] -= 1
    chance = creature["base_catch"]
    if chosen != ball_type:
        chance -= WRONG_BALL_PENALTY
    if state["difficulty"] == "story":
        chance += CAPTURE_STORY_BONUS
    elif state["difficulty"] == "hardcore":
        chance -= CAPTURE_HARDCORE_PENALTY

    roll = random.random()
    if roll <= chance:
        print(f"✨ Click! {creature['name']} was captured in your circular orb!")
        state["captured"].append(creature)
        state["npc_bond"][NPC_NAMES[0]] += 1  # Mira
    else:
        print(f"💨 {creature['name']} breaks free!")
        state["health"] -= 2 if creature["size"] == "big" else 1
