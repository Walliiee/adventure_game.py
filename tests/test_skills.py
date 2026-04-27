"""Tests for skill bonus calculations."""
from game.skills import get_skill_bonus, CATCH_RATE, STORM_DAMAGE, HERB_HEAL, UNLIMITED_BALLS, WILD_SIGHTING
from game.state import create_game_state


def _state_with_skills(primary=None, supplementary=None):
    s = create_game_state("Test", "classic")
    s["primary_skill"] = primary
    s["supplementary_skills"] = supplementary or []
    return s


class TestSkills:
    def test_primary_smarts_catch_rate(self):
        s = _state_with_skills(primary="Smarts")
        bonus = get_skill_bonus(s, CATCH_RATE, region="forest")
        assert bonus == 0.10

    def test_supplementary_smarts_catch_rate(self):
        s = _state_with_skills(supplementary=["Smarts"])
        bonus = get_skill_bonus(s, CATCH_RATE, region="meadow")
        assert bonus == 0.05  # half of 0.15

    def test_no_skill_zero_bonus(self):
        s = _state_with_skills()
        assert get_skill_bonus(s, CATCH_RATE, region="forest") == 0.0

    def test_smarts_wrong_region(self):
        s = _state_with_skills(primary="Smarts")
        assert get_skill_bonus(s, CATCH_RATE, region="canyon") == 0.10

    def test_agility_storm_damage(self):
        s = _state_with_skills(primary="Agility")
        assert get_skill_bonus(s, STORM_DAMAGE) == 0.50

    def test_spirit_herb_heal(self):
        s = _state_with_skills(primary="Spirit")
        assert get_skill_bonus(s, HERB_HEAL) == 35

    def test_strength_unlimited_balls(self):
        s = _state_with_skills(primary="Strength")
        assert get_skill_bonus(s, UNLIMITED_BALLS) == 1.0

    def test_agility_wild_sighting(self):
        s = _state_with_skills(primary="Agility")
        assert get_skill_bonus(s, WILD_SIGHTING) == 1.0

    def test_supplementary_spirit_herb_heal(self):
        s = _state_with_skills(supplementary=["Spirit"])
        assert get_skill_bonus(s, HERB_HEAL) == 17.5  # half of 30
