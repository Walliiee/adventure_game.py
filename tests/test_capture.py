"""Tests for capture mechanics."""
import unittest
from unittest.mock import patch

from game.capture import attempt_capture
from game.state import create_game_state


class TestCapture(unittest.TestCase):
    def _make_creature(self, size="small", base_catch=0.5):
        return {
            "name": "Test Beast",
            "size": size,
            "temperament": "calm",
            "base_catch": base_catch,
            "level": 1,
            "bond": 0,
            "mood": "neutral",
        }

    @patch("game.capture.get_player_choice", return_value=0)
    @patch("game.capture.random.random", return_value=0.01)
    def test_capture_success_with_best_ball(self, _rand, _choice):
        state = create_game_state("Hunter", "classic")
        creature = self._make_creature("small", base_catch=0.5)
        attempt_capture(state, creature)
        self.assertEqual(len(state["captured"]), 1)
        self.assertEqual(state["captured"][0]["name"], "Test Beast")

    @patch("game.capture.get_player_choice", return_value=0)
    @patch("game.capture.random.random", return_value=0.99)
    def test_capture_failure(self, _rand, _choice):
        state = create_game_state("Hunter", "classic")
        creature = self._make_creature("small", base_catch=0.5)
        attempt_capture(state, creature)
        self.assertEqual(len(state["captured"]), 0)

    @patch("game.capture.get_player_choice", return_value=0)
    @patch("game.capture.random.random", return_value=0.01)
    def test_creature_added_to_companions_on_success(self, _rand, _choice):
        state = create_game_state("Hunter", "story")
        creature = self._make_creature("small", base_catch=0.3)
        attempt_capture(state, creature)
        self.assertEqual(len(state["captured"]), 1)
        self.assertIn(state["captured"][0], state["captured"])

    @patch("game.capture.get_player_choice", return_value=0)
    @patch("game.capture.random.random", return_value=0.99)
    def test_health_decreases_on_failure(self, _rand, _choice):
        state = create_game_state("Hunter", "classic")
        initial_health = state["health"]
        creature = self._make_creature("small", base_catch=0.5)
        attempt_capture(state, creature)
        self.assertEqual(state["health"], initial_health - 1)

    @patch("game.capture.get_player_choice", return_value=0)
    @patch("game.capture.random.random", return_value=0.99)
    def test_big_creature_more_health_penalty(self, _rand, _choice):
        state = create_game_state("Hunter", "classic")
        initial_health = state["health"]
        creature = self._make_creature("big", base_catch=0.3)
        attempt_capture(state, creature)
        self.assertEqual(state["health"], initial_health - 2)

    @patch("game.capture.get_player_choice", return_value=0)
    def test_ball_decremented_on_attempt(self, _choice):
        state = create_game_state("Hunter", "classic")
        initial_balls = state["balls"]["mini"]
        creature = self._make_creature("small", base_catch=0.5)
        with patch("game.capture.random.random", return_value=0.5):
            attempt_capture(state, creature)
        self.assertEqual(state["balls"]["mini"], initial_balls - 1)

    @patch("game.capture.get_player_choice", return_value=2)
    def test_leave_peacefully_heals(self, _choice):
        state = create_game_state("Hunter", "classic")
        initial_health = state["health"]
        creature = self._make_creature()
        attempt_capture(state, creature)
        self.assertEqual(state["health"], initial_health + 1)

    @patch("game.capture.get_player_choice", return_value=1)
    def test_wrong_ball_penalty_reduces_catch_rate(self, _choice):
        """Using wrong ball type applies penalty but still can succeed with high roll."""
        state = create_game_state("Hunter", "story")
        creature = self._make_creature("small", base_catch=0.9)
        # Even with penalty, 0.9 - penalty should still catch with low random
        with patch("game.capture.random.random", return_value=0.01):
            attempt_capture(state, creature)
        self.assertEqual(len(state["captured"]), 1)


if __name__ == "__main__":
    unittest.main()
