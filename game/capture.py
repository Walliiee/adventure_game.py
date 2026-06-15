"""
Capture mechanic: orb choice, success roll, state updates.
"""
import random

from game.constants import (
    CAPTURE_STORY_BONUS,
    CAPTURE_HARDCORE_PENALTY,
    WRONG_BALL_PENALTY,
    NPC_NAMES,
    BALLS_BY_DIFFICULTY,
)
from game.cli import get_player_choice
from game.skills import get_skill_bonus, CATCH_RATE, UNLIMITED_BALLS, HIGHLANDS_CATCH
from game.companions import get_brave_capture_bonus, pick_companion


def _get_max_balls(state: dict, ball_type: str) -> int:
    """Return max allowed balls for this type, capping Strength at 2x normal."""
    difficulty = state.get("difficulty", "classic")
    base_max = BALLS_BY_DIFFICULTY.get(difficulty, {}).get(ball_type, 6 if ball_type == "mini" else 3)
    unlimited_bonus = get_skill_bonus(state, UNLIMITED_BALLS)
    if unlimited_bonus >= 1.0:
        return base_max * 2  # Primary Strength: cap at 2x normal
    elif unlimited_bonus > 0:
        return int(base_max * 1.5)  # Supplementary: cap at 1.5x
    return base_max


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
        state["peaceful_leaves"] = state.get("peaceful_leaves", 0) + 1
        return

    chosen = ball_type if pick == 0 else alt_ball
    # Act 1 skill: Strength primary = balls up to 2x; supplementary = up to 1.5x with refund chance
    if state["balls"][chosen] <= 0:
        unlimited_bonus = get_skill_bonus(state, UNLIMITED_BALLS)
        max_balls = _get_max_balls(state, chosen)
        if state["balls"][chosen] < max_balls and unlimited_bonus >= 1.0:
            # Primary Strength: recover up to 2x cap
            state["balls"][chosen] += 1
            print(f"💪 Your Strength training kicks in — you find an extra {chosen.title()} Orb!")
        elif unlimited_bonus > 0 and random.random() < unlimited_bonus:
            # Supplementary Strength: 50% chance to recover one (capped)
            max_balls = _get_max_balls(state, chosen)
            if state["balls"][chosen] < max_balls:
                state["balls"][chosen] += 1
                print(f"💪 Your Strength training helps — you scrape together one more {chosen.title()} Orb!")
            else:
                print(f"No {chosen.title()} Orbs left! The creature escapes.")
                return
        else:
            print(f"No {chosen.title()} Orbs left! The creature escapes.")
            return

    state["balls"][chosen] -= 1
    chance = creature["catch_rate_base"]
    if chosen != ball_type:
        chance -= WRONG_BALL_PENALTY
    if state["difficulty"] == "story":
        chance += CAPTURE_STORY_BONUS
    elif state["difficulty"] == "hardcore":
        chance -= CAPTURE_HARDCORE_PENALTY

    # Act 1 skill bonus: Smarts boosts catch rate in all regions
    region = state.get("current_region", "")
    chance += get_skill_bonus(state, CATCH_RATE, region=region)

    # Spirit bonus for highlands
    chance += get_skill_bonus(state, HIGHLANDS_CATCH, region=region)

    # Companion bonus: Brave companion adds +10% capture rate when present
    if state["captured"]:
        companion = pick_companion(state, "bring to capture")
        if companion:
            brave_bonus = get_brave_capture_bonus(companion)
            if brave_bonus > 0:
                chance += brave_bonus
                print(f"🦁 {companion['name']} stands bravely by your side! +10% capture rate.")

    # Capture Charm (from inventory.use_item) — consume it on this attempt for +20%.
    if state.pop("_capture_charm_active", False):
        chance = min(0.99, chance + 0.20)
        print("✨ Your Capture Charm flares — +20% catch rate on this attempt!")

    roll = random.random()
    if roll <= chance:
        print(f"✨ Click! {creature['name']} was captured in your circular orb!")
        # Add personality from creatures data if creature doesn't have it
        if "personality" not in creature:
            from game.constants import CREATURES
            for c in CREATURES:
                if c["name"] == creature["name"]:
                    creature["personality"] = c.get("personality", "brave")
                    break
        creature.setdefault("personality", "brave")
        creature.setdefault("ability_used_today", False)
        state["captured"].append(creature)
        state["npc_bond"][NPC_NAMES[0]] += 1  # keeper (Eldra)
        # Add coins for successful capture
        state["coins"] = state.get("coins", 0) + 2
        print(f"💰 +2 coins! (Total: {state['coins']})")
    else:
        print(f"💨 {creature['name']} breaks free!")
        state["health"] -= 2 if creature["size"] == "big" else 1
