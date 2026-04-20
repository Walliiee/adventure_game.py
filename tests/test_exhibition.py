"""Tests for the exhibition system."""
from game.exhibition import _compute_exhibition_score, STRATEGIES
from game.state import create_game_state


class TestExhibitionScoring:
    def test_max_bond_gives_50(self):
        score = _compute_exhibition_score({"bond": 5, "personality": "brave"}, "strength", 5)
        assert score >= 50  # at least bond portion

    def test_zero_bond_gives_0_bond_points(self):
        score = _compute_exhibition_score({"bond": 0, "personality": "brave"}, "strength", 0)
        assert score == 30  # 0 bond + 30 match + 0 companions

    def test_strategy_match_brave_strength(self):
        score = _compute_exhibition_score({"bond": 0, "personality": "brave"}, "strength", 0)
        assert score == 30

    def test_strategy_match_playful_speed(self):
        score = _compute_exhibition_score({"bond": 0, "personality": "playful"}, "speed", 0)
        assert score == 30

    def test_strategy_match_timid_bond(self):
        score = _compute_exhibition_score({"bond": 0, "personality": "timid"}, "bond", 0)
        assert score == 30

    def test_strategy_mismatch_no_match(self):
        score = _compute_exhibition_score({"bond": 0, "personality": "brave"}, "speed", 0)
        assert score == 0  # no match

    def test_companion_count_capped_at_20(self):
        score = _compute_exhibition_score({"bond": 0, "personality": "brave"}, "strength", 30)
        # 0 bond + 30 match + 20 capped = 50
        assert score == 50

    def test_perfect_score(self):
        score = _compute_exhibition_score({"bond": 5, "personality": "brave"}, "strength", 20)
        assert score == 100

    def test_strategies_defined(self):
        assert len(STRATEGIES) == 3
        assert "strength" in STRATEGIES
        assert "speed" in STRATEGIES
        assert "bond" in STRATEGIES
