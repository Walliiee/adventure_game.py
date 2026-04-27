"""Tests for encounter handling with mocked random."""
from unittest.mock import patch
from game.encounters import roll_encounter, handle_encounter
from game.state import create_game_state


def _fresh_state():
    return create_game_state("Test", "classic")


class TestEncounters:
    def test_handle_nothing(self):
        s = _fresh_state()
        result = handle_encounter("nothing", s)
        assert "quiet" in result.lower()

    def test_handle_healing_spring(self):
        s = _fresh_state()
        s["health"] = 5
        result = handle_encounter("healing_spring", s)
        assert s["health"] > 5
        assert "spring" in result.lower()

    def test_handle_storm(self):
        s = _fresh_state()
        hp_before = s["health"]
        result = handle_encounter("storm", s)
        assert s["health"] < hp_before
        assert "storm" in result.lower()

    def test_handle_lost_traveler(self):
        s = _fresh_state()
        with patch("game.encounters.random") as mock_rand:
            mock_rand.choice.return_value = "healing_herb"
            result = handle_encounter("lost_traveler", s)
        assert "healing_herb" in s["inventory"] or "traveler" in result.lower()

    def test_roll_encounter_no_skill_bonus(self):
        s = _fresh_state()
        with patch("game.encounters._weighted_encounter", return_value="nothing"):
            result = roll_encounter(s)
        assert result == "nothing"

    def test_roll_encounter_wild_sight_with_agility(self):
        s = _fresh_state()
        s["primary_skill"] = "Agility"
        result = roll_encounter(s)
        assert result == "wild_creature"
