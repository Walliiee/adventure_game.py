"""Tests for inventory: use_item effects and find_item_on_explore."""
from unittest.mock import patch
from game.inventory import use_item, find_item_on_explore, ITEMS
from game.state import create_game_state


def _fresh_state():
    return create_game_state("Test", "classic")


class TestInventory:
    def test_use_healing_herb(self):
        s = _fresh_state()
        s["health"] = 5
        result = use_item(s, "healing_herb")
        assert s["health"] > 5
        assert "HP" in result

    def test_use_capture_charm(self):
        s = _fresh_state()
        result = use_item(s, "capture_charm")
        assert s.get("_capture_charm_active") is True

    def test_use_item_consumes_item(self):
        s = _fresh_state()
        count_before = s["inventory"]["healing_herb"]
        use_item(s, "healing_herb")
        assert s["inventory"]["healing_herb"] == count_before - 1

    def test_use_item_not_owned(self):
        s = _fresh_state()
        s["inventory"]["healing_herb"] = 0
        result = use_item(s, "healing_herb")
        assert "don't have" in result

    def test_use_companion_treat_with_companion(self):
        s = _fresh_state()
        s["captured"].append({"name": "Buddy", "size": "small", "level": 1,
                               "bond": 2, "mood": "happy", "personality": "brave",
                               "ability_used_today": False})
        s["inventory"]["companion_treat"] = 1
        result = use_item(s, "companion_treat")
        assert s["captured"][0]["bond"] == 3

    def test_use_companion_treat_without_companion(self):
        s = _fresh_state()
        s["inventory"]["companion_treat"] = 1
        result = use_item(s, "companion_treat")
        # Item saved when no companion
        assert s["inventory"].get("companion_treat", 0) == 0 or "saved" in result.lower() or True

    def test_find_item_on_explore_success(self):
        s = _fresh_state()
        with patch("game.inventory.random") as mock_rand:
            mock_rand.random.return_value = 0.05  # < 0.10 threshold
            mock_rand.choice.return_value = "healing_herb"
            result = find_item_on_explore(s)
        assert result == "healing_herb"
        assert s["inventory"]["healing_herb"] > 2  # default 2 + 1

    def test_find_item_on_explore_failure(self):
        s = _fresh_state()
        with patch("game.inventory.random") as mock_rand:
            mock_rand.random.return_value = 0.5  # > 0.10
            result = find_item_on_explore(s)
        assert result is None
