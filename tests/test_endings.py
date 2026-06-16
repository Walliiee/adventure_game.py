"""Tests for the 6 ending conditions."""
from game.constants import REGION_IDS
from game.endings import determine_ending
from game.state import create_game_state


def _state_with(captured=0, bond=0, regions=None, peaceful=0, perfect_win=False):
    state = create_game_state("Test", "classic")
    for _ in range(captured):
        state["captured"].append({"name": f"Pet{_}", "size": "small", "level": 1,
                                   "bond": bond, "mood": "happy", "personality": "brave",
                                   "ability_used_today": False})
    if regions:
        state["region_progress"] = set(regions)
    state["peaceful_leaves"] = peaceful
    state["exhibition_perfect_win"] = perfect_win
    return state


class TestEndings:
    def test_legend_ending_perfect_exhibition(self):
        s = _state_with(perfect_win=True)
        assert determine_ending(s) == "legend"

    def test_master_keeper_8_creatures_max_bond(self):
        s = _state_with(captured=8, bond=5)
        assert determine_ending(s) == "master_keeper"

    def test_master_keeper_requires_all_max_bond(self):
        s = _state_with(captured=8, bond=3)
        assert determine_ending(s) != "master_keeper"

    def test_explorer_all_regions(self):
        s = _state_with(regions=set(REGION_IDS))
        assert determine_ending(s) == "explorer"

    def test_gentle_one_more_leaves_than_catches(self):
        s = _state_with(captured=2, peaceful=5)
        assert determine_ending(s) == "gentle_one"

    def test_dropout_fewer_than_3_creatures(self):
        s = _state_with(captured=2)
        assert determine_ending(s) == "dropout"

    def test_default_ending(self):
        s = _state_with(captured=4, regions={"meadow", "ruins"})
        assert determine_ending(s) == "default"

    def test_priority_legend_over_master_keeper(self):
        s = _state_with(captured=8, bond=5, perfect_win=True)
        assert determine_ending(s) == "legend"
