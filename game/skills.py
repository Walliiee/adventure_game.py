"""
Act 1 skill bonuses that carry into Act 2.

Act 1 skills: Strength, Agility, Smarts, Spirit.
Primary skill → full bonus. Supplementary skill → half bonus.

Mappings:
  - Smarts (tracking knowledge) → +10% catch rate in all regions (half: +5%)
  - Agility (speed) → 50% chance to avoid storm damage (half: 25%)
  - Strength → capture balls doubled, capped at 2x normal orb count (half: 1.5x)
  - Spirit (healing spirit) → healing_herb restores 35 HP instead of 15 (half: 25 HP)
  - Spirit (wild empathy) → +10% catch rate in highlands (half: +5%)
  - Agility (stealth) → wild creature sightings always trigger (half: +30% trigger chance)
"""
from __future__ import annotations

# Bonus context constants
CATCH_RATE = "catch_rate"
STORM_DAMAGE = "storm_damage"
HERB_HEAL = "herb_heal"
UNLIMITED_BALLS = "unlimited_balls"
WILD_SIGHTING = "wild_sighting"
HIGHLANDS_CATCH = "highlands_catch"

# Full bonus values
_BONUSES = {
    "Smarts": {
        CATCH_RATE: 0.10,       # +10% catch in all regions
    },
    "Agility": {
        STORM_DAMAGE: 0.50,    # 50% chance to avoid storm
        WILD_SIGHTING: 1.0,    # always trigger wild creature sightings
    },
    "Strength": {
        UNLIMITED_BALLS: 1.0,  # balls doubled (capped at 2x normal)
    },
    "Spirit": {
        HERB_HEAL: 35,         # herb heals 35 instead of 15
        HIGHLANDS_CATCH: 0.10,   # +10% catch rate in highlands
    },
}

# Regions where Smarts gives catch rate bonus (now all regions)
_CATCH_RATE_REGIONS = {"forest", "meadow", "ruins", "river", "canyon", "highlands"}


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
        context: one of CATCH_RATE, STORM_DAMAGE, HERB_HEAL, UNLIMITED_BALLS, WILD_SIGHTING, HIGHLANDS_CATCH
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

        # Region check for catch rate (now all regions)
        if context == CATCH_RATE:
            region = kwargs.get("region", "")
            if region not in _CATCH_RATE_REGIONS:
                continue

        # Region check for highlands catch bonus
        if context == HIGHLANDS_CATCH:
            region = kwargs.get("region", "")
            if region != "highlands":
                continue

        if level == "supplementary":
            value = value / 2.0

        bonus = max(bonus, value)

    return bonus
