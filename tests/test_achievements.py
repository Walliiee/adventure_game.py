"""Tests for achievement unlock conditions."""
from game.achievements import check_achievements, ACHIEVEMENTS
from game.state import create_game_state


def _state_with(captured=0, bond=0, regions=None, peaceful=0, exhibition_won=False):
    state = create_game_state("Test", "classic")
    for _ in range(captured):
        state["captured"].append({"name": f"Pet{_}", "size": "small", "level": 1,
                                   "bond": bond, "mood": "happy", "personality": "brave",
                                   "ability_used_today": False})
    if regions:
        state["region_progress"] = set(regions)
    state["peaceful_leaves"] = peaceful
    state["exhibition_won"] = exhibition_won
    return state


class TestAchievements:
    def test_first_catch(self):
        s = _state_with(captured=1)
        assert "first_catch" in check_achievements(s)

    def test_no_first_catch_without_creature(self):
        s = _state_with(captured=0)
        assert "first_catch" not in check_achievements(s)

    def test_explorer_3_regions(self):
        s = _state_with(regions={"meadow", "ruins", "river"})
        assert "explorer" in check_achievements(s)

    def test_completionist_all_regions(self):
        s = _state_with(regions={"meadow", "ruins", "river", "canyon", "forest"})
        assert "completionist" in check_achievements(s)

    def test_bonded_max_bond(self):
        s = _state_with(captured=1, bond=5)
        assert "bonded" in check_achievements(s)

    def test_collector_5_creatures(self):
        s = _state_with(captured=5)
        assert "collector" in check_achievements(s)

    def test_master_collector_10_creatures(self):
        s = _state_with(captured=10)
        assert "master_collector" in check_achievements(s)

    def test_peaceful_keeper(self):
        s = _state_with(peaceful=3)
        assert "peaceful_keeper" in check_achievements(s)

    def test_exhibition_champion(self):
        s = _state_with(exhibition_won=True)
        assert "exhibition_champion" in check_achievements(s)

    def test_no_duplicate_unlocks(self):
        s = _state_with(captured=1)
        check_achievements(s)
        s["achievements_unlocked"].extend(check_achievements(s))
        # Second call shouldn't re-unlock
        result = check_achievements(s)
        assert "first_catch" not in result

    def test_total_achievement_count(self):
        assert len(ACHIEVEMENTS) == 8
