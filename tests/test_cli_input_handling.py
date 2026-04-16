import unittest
from unittest.mock import patch

from game.cli import ask_replay, get_player_choice


class TestCliInputHandling(unittest.TestCase):
    def test_get_player_choice_reprompts_then_accepts_alias(self):
        options = ("One", "Two")
        aliases = {"two": 1}
        with patch("builtins.input", side_effect=["invalid", "two"]):
            result = get_player_choice(options, aliases, prompt="Pick: ")
        self.assertEqual(result, 1)

    def test_get_player_choice_quit_exits(self):
        with patch("builtins.input", return_value="quit"):
            with self.assertRaises(SystemExit):
                get_player_choice(("One",), {}, prompt="Pick: ")

    def test_ask_replay_reprompts_until_valid(self):
        with patch("builtins.input", side_effect=["maybe", "yes"]):
            self.assertTrue(ask_replay())


if __name__ == "__main__":
    unittest.main()
