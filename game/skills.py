"""
Act 1 skill bonuses that carry into Act 2.

Act 1 skills: Strength, Agility, Smarts, Spirit.
Primary skill → full bonus. Supplementary skill → half bonus.

Mappings:
  - Smarts (tracking knowledge) → +15% catch rate in Forest and Meadow (half: +7.5%)
  - Agility (speed) → 50% chance to avoid storm damage (half: 25%)
  - Strength → capture balls never run out (half: 50% chance to refund the ball)
  - Spirit (healing spirit) → healing_herb restores 30 HP instead of 15 (half: 22 HP)
  - Agility (stealth) → wild creature sightings always trigger (half: +30% trigger chance)
"""
from __future__ import annotations

# Bonus context constants
CATCH_RATE = "catch_rate"
STORM_DAMAGE = "storm_damage"
HERB_HEAL = "herb_heal"
UNLIMITED_BALLS = "unlimited_balls"
WILD_SIGHTING = "wild_sighting"

# Full bonus values
_BONUSES = {
    "Smarts": {
        CATCH_RATE: 0.15,       # +15% catch in forest/meadow
    },
    "Agility": {
        STORM_DAMAGE: 0.50,    # 50% chance to avoid storm
        WILD_SIGHTING: 1.0,    # always trigger wild creature sightings
    },
    "Strength": {
        UNLIMITED_BALLS: 1.0,  # balls never run out
    },
    "Spirit": {
        HERB_HEAL: 30,         # herb heals 30 instead of 15
    },
}

# Regions where Smarts gives catch rate bonus
_CATCH_RATE_REGIONS = {"forest", "meadow"}


def _has_skill(state: dict, skill: str) -> str | None:
    """Return 'primary' if skill is primary, 'supplementary' if supplementary, else None."""
    if state.get("primary_skill") == skill:
        return "primary"
    if skill in state.get("supplementary_skills", []):
        return "supplementary"
    return None


def get_skill_bonus(state: dict, context: str, **kwargs) -> float:
    """
    Return bonus value for a given context based on Act 1 skill choices.

    Args:
        state: GameState dict
        context: one of CATCH_RATE, STORM_DAMAGE, HERB_HEAL, UNLIMITED_BALLS, WILD_SIGHTING
        **kwargs: context-specific extra args (e.g. region for CATCH_RATE)

    Returns:
        Bonus value (float). 0.0 if no applicable skill.
    """
    bonus = 0.0

    for skill, skill_bonuses in _BONUSES.items():
        if context not in skill_bonuses:
            continue
        level = _has_skill(state, skill)
        if level is None:
            continue

        value = skill_bonuses[context]

        # Region check for catch rate
        if context == CATCH_RATE:
            region = kwargs.get("region", "")
            if region not in _CATCH_RATE_REGIONS:
                continue

        if level == "supplementary":
            value = value / 2.0

        bonus = max(bonus, value)

    return bonus
