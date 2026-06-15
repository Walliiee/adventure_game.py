"""
Exhibition system: pre-exhibition prep, scoring, narrative, and post-exhibition rewards.
"""
from __future__ import annotations

from game.cli import get_player_choice
from game.companions import pick_companion


# Strategy definitions
STRATEGIES = {
    "strength": {
        "name": "Impress with strength",
        "desc": "Power and dominance. Best with brave companions.",
        "personality_match": "brave",
    },
    "speed": {
        "name": "Show off speed",
        "desc": "Agility and quickness. Best with playful companions.",
        "personality_match": "playful",
    },
    "bond": {
        "name": "Demonstrate bond",
        "desc": "Trust and connection. Best with timid companions.",
        "personality_match": "timid",
    },
}

# Narrative beats per strategy
NARRATIVE_BEATS = {
    "strength": [
        "The crowd gasps as {companion} leaps forward with raw power, muscles rippling under the arena lights.",
        "{companion} slams through the obstacle course — walls crumble, gates fly off hinges!",
        "The judges stare in disbelief. {companion} stands tall, chest heaving, victorious.",
    ],
    "speed": [
        "The crowd gasps as {companion} blurs across the arena floor, a streak of motion.",
        "{companion} weaves through the agility rings so fast the timers can barely keep up!",
        "A hush falls — then erupts into applause. {companion} carved seconds off the record.",
    ],
    "bond": [
        "The crowd gasps as {companion} moves in perfect sync with you, reading every gesture.",
        "You and {companion} perform a unity display — every signal answered before it's given.",
        "Tears gleam in the front row. That kind of trust can't be trained — it's earned.",
    ],
}

# Crowd reactions by score tier
CROWD_REACTIONS = {
    (90, 100): "The crowd erupts! Chants of 'LEGEND! LEGEND!' shake the stadium.",
    (80, 89): "A standing ovation! The judges whisper among themselves — something special just happened.",
    (70, 79): "Loud applause fills the arena. Solid, impressive, memorable.",
    (60, 69): "Polite clapping and nods. A good showing, if not spectacular.",
    (50, 59): "Scattered applause. The crowd expected more.",
    (0, 49): "Stunned silence. The crowd looks away, uncomfortable.",
}


# Score at/above which a showing counts as legendary (a "perfect" win) and unlocks
# the Legend ending. Reachable with a maxed, well-matched companion and a healthy
# roster — it no longer requires hitting an exact 100.
LEGEND_SCORE = 95


def _get_crowd_reaction(score: int) -> str:
    for (lo, hi), text in CROWD_REACTIONS.items():
        if lo <= score <= hi:
            return text
    return "The crowd is unsure what to make of it."


def _compute_exhibition_score(companion: dict, strategy: str, num_companions: int) -> int:
    """
    Compute exhibition score (0-100):
      - Bond level (0-5) → up to 50 points (bond * 10)
      - Strategy-personality match → up to 30 points
      - Number of companions caught → up to 20 points (1 per, max 20)
    """
    # Bond score: bond 0-5 → 0-50
    bond = min(companion.get("bond", 0), 5)
    bond_score = bond * 10

    # Strategy match score
    strat_data = STRATEGIES[strategy]
    personality = companion.get("personality", "brave")
    if personality == strat_data["personality_match"]:
        match_score = 30
    elif personality in STRATEGIES:
        # Partial match — personality matches a different strategy
        match_score = 10
    else:
        match_score = 0

    # Companions count score
    count_score = min(num_companions, 20)

    total = bond_score + match_score + count_score
    return min(total, 100)


def run_exhibition_prep(state: dict) -> dict | None:
    """
    Pre-exhibition prep phase. Player picks companion, skill to highlight, and strategy.
    Returns a dict with choices or None if cancelled.
    """
    captured = state.get("captured", [])
    if len(captured) < 2:
        print("\n⚠️ You need at least 2 companions to compete in the exhibition.")
        return None

    # Step 1: Pick companion to feature
    print("\n🏟️ RIDGECAMP EXHIBITION — Prep Phase")
    print("=" * 45)
    print("\nChoose which companion to feature in the exhibition:")
    companion = pick_companion(state, "feature in exhibition")
    if not companion:
        return None

    # Step 2: Pick skill to highlight
    skills = []
    if state.get("primary_skill"):
        skills.append(state["primary_skill"])
    skills.extend(state.get("supplementary_skills", []))
    if not skills:
        skills = ["None"]

    print(f"\nWhich skill will {companion['name']} highlight?")
    if len(skills) == 1 and skills[0] == "None":
        print("  No Act 1 skills trained — proceeding without a skill highlight.")
        chosen_skill = None
    else:
        skill_options = [s for s in skills if s != "None"] + ["Skip skill highlight"]
        idx = get_player_choice(skill_options)
        chosen_skill = skill_options[idx] if idx < len(skills) else None
        if chosen_skill == "Skip skill highlight":
            chosen_skill = None

    # Step 3: Pick strategy
    print(f"\nChoose {companion['name']}'s exhibition strategy:")
    strat_keys = list(STRATEGIES.keys())
    strat_options = [f"{STRATEGIES[k]['name']} — {STRATEGIES[k]['desc']}" for k in strat_keys]
    idx = get_player_choice(strat_options)
    chosen_strategy = strat_keys[idx]

    return {
        "companion": companion,
        "skill": chosen_skill,
        "strategy": chosen_strategy,
    }


def run_exhibition(state: dict) -> tuple[bool, bool]:
    """
    Run the full exhibition with prep, scoring, narrative, and rewards.
    Returns tuple[won: bool, action_performed: bool].
    """
    # Prep phase
    prep = run_exhibition_prep(state)
    if prep is None:
        return False, False

    companion = prep["companion"]
    strategy = prep["strategy"]
    chosen_skill = prep["skill"]

    # Compute score
    num_companions = len(state["captured"])
    score = _compute_exhibition_score(companion, strategy, num_companions)

    # Skill bonus: +5 if highlighted skill matches strategy
    if chosen_skill:
        skill_strat_map = {"Strength": "strength", "Agility": "speed", "Spirit": "bond", "Smarts": "bond"}
        mapped = skill_strat_map.get(chosen_skill)
        if mapped == strategy:
            score = min(100, score + 5)

    # Narrative
    print("\n🏟️ RIDGECAMP EXHIBITION MATCH")
    print("=" * 45)
    beats = NARRATIVE_BEATS[strategy]
    for beat in beats:
        print(f"\n  {beat.format(companion=companion['name'])}")

    # Score reveal
    print(f"\n  📊 Exhibition Score: {score}/100")
    print(f"  {_get_crowd_reaction(score)}")

    # Determine win (80+ = win)
    won = score >= 80

    if won:
        print("\n  🎉 You are crowned Exhibition Champion!")
        coins_awarded = max(1, round(score / 10))
        state["coins"] = state.get("coins", 0) + coins_awarded
        print(f"  💰 +{coins_awarded} coins! (Total: {state['coins']})")
        state["exhibition_won"] = True

        if score >= LEGEND_SCORE:
            state["exhibition_perfect_win"] = True
            print("  ⭐ A legendary performance — the Legend ending is yours!")
    else:
        print(f"\n  😔 Score {score} — not enough to win. (Need 80+)")
        print("  Train harder, build stronger bonds, and try again.")

    return won, True
