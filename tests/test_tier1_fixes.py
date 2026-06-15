"""Regression tests for the Tier-1 "stop it feeling broken" fixes.

Each test pins a behavior that was previously broken or unreachable:
  - Capture Charm now applies on the main capture path (was a no-op there).
  - Explorer Map detects creatures (list-vs-string comparison was always false).
  - Wild-sighting peaceful release counts toward peaceful_leaves.
  - Save/load tolerates older saves missing newer fields, and save never crashes.
  - Legend / Master Keeper endings are reachable; Completionist needs every region.
  - The shop spends coins (coin sink works once npcs.json loads).
"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from game.constants import REGION_IDS
from game.endings import determine_ending
from game.exhibition import LEGEND_SCORE, _compute_exhibition_score
from game.achievements import check_achievements
from game.capture import attempt_capture
from game.encounters import handle_encounter
from game.inventory import use_item
from game.save import save_game, load_game
from game.state import create_game_state


def _creature(size="small", catch_rate_base=0.1, name="Test Beast"):
    return {"name": name, "size": size, "temperament": "calm",
            "catch_rate_base": catch_rate_base, "level": 1, "bond": 0, "mood": "curious"}


class TestCaptureCharm(unittest.TestCase):
    @patch("game.capture.get_player_choice", return_value=0)
    @patch("game.capture.random.random", return_value=0.3)
    def test_charm_applies_and_is_consumed_on_main_path(self, _rand, _choice):
        state = create_game_state("Tester", "story")  # +0.1 story bonus
        state["_capture_charm_active"] = True
        # base 0.1 + story 0.1 = 0.2; without charm roll 0.3 fails. With charm -> 0.4, succeeds.
        attempt_capture(state, _creature(catch_rate_base=0.1))
        self.assertEqual(len(state["captured"]), 1)
        self.assertNotIn("_capture_charm_active", state)  # popped

    @patch("game.capture.get_player_choice", return_value=0)
    @patch("game.capture.random.random", return_value=0.3)
    def test_without_charm_same_roll_fails(self, _rand, _choice):
        state = create_game_state("Tester", "story")
        attempt_capture(state, _creature(catch_rate_base=0.1))
        self.assertEqual(len(state["captured"]), 0)


class TestExplorerMap(unittest.TestCase):
    def test_map_detects_creatures(self):
        state = create_game_state("Tester", "story")
        state["inventory"] = {"explorer_map": 1}
        result = use_item(state, "explorer_map")
        # meadow has Moss Bunny; the old `== rid` bug reported "nothing detected" everywhere.
        self.assertIn("Moss Bunny", result)
        self.assertNotIn("nothing detected", result)


class TestPeacefulRelease(unittest.TestCase):
    @patch("game.cli.get_player_choice", return_value=1)  # "Let it go peacefully"
    def test_wild_sighting_release_counts(self, _choice):
        state = create_game_state("Tester", "story")
        state["current_region"] = "meadow"
        before = state["peaceful_leaves"]
        handle_encounter("wild_creature", state)
        self.assertEqual(state["peaceful_leaves"], before + 1)


class TestSaveHardening(unittest.TestCase):
    def test_old_save_missing_fields_loads(self):
        old_save = {
            "name": "Old", "difficulty": "classic", "health": 12, "captured": [], "turn": 3,
            "region_progress": ["meadow"], "seen_npc_scenes": [], "regions_visited": ["meadow"],
        }  # no coins/inventory/balls/npc_bond/skills — written by an older build
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "save.json"
            path.write_text(json.dumps(old_save), encoding="utf-8")
            state = load_game(path)
        self.assertIsNotNone(state)
        for key in ("coins", "inventory", "balls", "npc_bond", "primary_skill", "supplementary_skills"):
            self.assertIn(key, state)
        self.assertEqual(state["balls"], {"mini": 0, "mega": 0})

    def test_save_does_not_crash_on_io_error(self):
        state = create_game_state("Tester", "story")
        bad_path = Path("/this_dir_does_not_exist_xyz") / "save.json"
        save_game(state, bad_path)  # must swallow OSError, not raise


class TestReachableEndings(unittest.TestCase):
    def test_master_keeper_needs_only_a_bonded_core(self):
        state = create_game_state("Tester", "story")
        for i in range(8):
            state["captured"].append({"name": f"C{i}", "size": "small",
                                      "bond": 5 if i < 4 else 1, "personality": "brave"})
        self.assertEqual(determine_ending(state), "master_keeper")

    def test_master_keeper_excluded_without_enough_bonded(self):
        state = create_game_state("Tester", "story")
        for i in range(8):
            state["captured"].append({"name": f"C{i}", "size": "small",
                                      "bond": 5 if i < 3 else 1, "personality": "brave"})
        self.assertNotEqual(determine_ending(state), "master_keeper")

    def test_legend_score_is_reachable(self):
        # bond 5 (50) + matched personality (30) + 15 companions (15) = 95 >= LEGEND_SCORE
        companion = {"bond": 5, "personality": "brave"}
        score = _compute_exhibition_score(companion, "strength", num_companions=15)
        self.assertGreaterEqual(score, LEGEND_SCORE)


class TestCompletionistRegions(unittest.TestCase):
    def test_requires_every_region_including_highlands(self):
        state = create_game_state("Tester", "story")
        state["region_progress"] = set(REGION_IDS) - {"highlands"}
        self.assertNotIn("completionist", check_achievements(state))
        state["region_progress"] = set(REGION_IDS)
        self.assertIn("completionist", check_achievements(state))


class TestCoinSink(unittest.TestCase):
    @patch("game.npc.get_player_choice", return_value=0)  # buy the first shop item
    def test_shop_spends_coins(self, _choice):
        from game.npc import show_shop
        state = create_game_state("Tester", "story")
        state["coins"] = 10
        show_shop(state)
        self.assertLess(state["coins"], 10)
        self.assertTrue(any(v > 0 for v in state["inventory"].values()))


if __name__ == "__main__":
    unittest.main()
