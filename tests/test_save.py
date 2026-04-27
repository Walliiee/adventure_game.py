"""Tests for save/load system."""
import unittest
from pathlib import Path

from game.save import save_game, load_game
from game.state import create_game_state


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        self.path = Path("/tmp/test_wildlands_save.json")
        self.path.unlink(missing_ok=True)

    def tearDown(self):
        self.path.unlink(missing_ok=True)

    def test_save_creates_file(self):
        state = create_game_state("Tester", "classic")
        save_game(state, self.path)
        self.assertTrue(self.path.exists())

    def test_load_returns_correct_state(self):
        state = create_game_state("Tester", "classic")
        state["turn"] = 5
        state["region_progress"].add("forest")
        save_game(state, self.path)
        loaded = load_game(self.path)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["name"], "Tester")
        self.assertEqual(loaded["turn"], 5)
        self.assertIn("forest", loaded["region_progress"])

    def test_load_returns_none_for_missing_file(self):
        result = load_game(Path("/tmp/nonexistent_save_12345.json"))
        self.assertIsNone(result)

    def test_load_returns_none_for_corrupted_json(self):
        self.path.write_text("{invalid json!!!")
        result = load_game(self.path)
        self.assertIsNone(result)

    def test_round_trip_save_load_same_state(self):
        state = create_game_state("RoundTripper", "hardcore")
        state["region_progress"].add("ruins")
        state["region_progress"].add("river")
        state["seen_npc_scenes"].add("forest_mira")
        state["captured"].append(
            {"name": "Moss Bunny", "size": "small", "level": 2, "bond": 3, "mood": "happy"}
        )
        state["turn"] = 10
        save_game(state, self.path)
        loaded = load_game(self.path)
        self.assertEqual(loaded["name"], state["name"])
        self.assertEqual(loaded["difficulty"], state["difficulty"])
        self.assertEqual(loaded["health"], state["health"])
        self.assertEqual(loaded["turn"], state["turn"])
        self.assertEqual(loaded["captured"], state["captured"])
        self.assertEqual(loaded["region_progress"], state["region_progress"])
        self.assertEqual(loaded["seen_npc_scenes"], state["seen_npc_scenes"])
        self.assertEqual(loaded["balls"], state["balls"])
        self.assertEqual(loaded["npc_bond"], state["npc_bond"])


if __name__ == "__main__":
    unittest.main()
