import unittest
from unittest.mock import patch

from game.loop import run_session
from game.state import create_game_state


class TestAct2TurnProgression(unittest.TestCase):
    @patch("game.loop.display_intro")
    @patch("game.loop.day_menu", side_effect=[1, 3, 5])
    def test_train_without_companion_does_not_advance_day(self, _menu, _intro):
        state = create_game_state("Test", "story")
        run_session(state)
        self.assertEqual(state["turn"], 1)

    @patch("game.loop.display_intro")
    @patch("game.loop.day_menu", side_effect=[4, 3, 5])
    def test_exhibition_not_ready_does_not_advance_day(self, _menu, _intro):
        state = create_game_state("Test", "story")
        run_session(state)
        self.assertEqual(state["turn"], 1)

    @patch("game.loop.display_intro")
    @patch("game.loop.day_menu", side_effect=[1, 5])
    @patch("game.companions.get_player_choice", return_value=0)
    def test_train_with_companion_advances_day(self, _pick, _menu, _intro):
        state = create_game_state("Test", "story")
        state["captured"].append(
            {"name": "Moss Bunny", "size": "small", "level": 1, "bond": 1, "mood": "curious"}
        )
        run_session(state)
        self.assertEqual(state["turn"], 2)


if __name__ == "__main__":
    unittest.main()
