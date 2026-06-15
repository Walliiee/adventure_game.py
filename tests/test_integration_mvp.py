"""End-to-end MVP guards.

These tests load the REAL data/*.json content (not hand-built creature dicts) and
drive one full Explore -> capture turn. They exist because the unit suite injected
synthetic creatures with a `size` key, so it stayed green while the shipped game
crashed on the first Explore (KeyError: 'size') and the NPC system was silently
disabled by malformed JSON. Keep these passing and that class of bug can't return.
"""
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from game.capture import attempt_capture
from game.constants import CREATURES, REGION_IDS, NPC_NAMES
from game.skills import CATCH_RATE, get_skill_bonus
from game.state import create_game_state
from game.world import find_creature

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class TestDataFilesValid(unittest.TestCase):
    def test_all_data_files_are_valid_json(self):
        """Every shipped data file must parse — a typo here silently disables systems."""
        for path in sorted(_DATA_DIR.glob("*.json")):
            with self.subTest(file=path.name):
                with open(path) as f:
                    json.load(f)  # raises on malformed JSON

    def test_npcs_json_exposes_authored_npcs(self):
        """npcs.json must actually load (it was invalid JSON, falling back silently)."""
        with open(_DATA_DIR / "npcs.json") as f:
            npcs = json.load(f)
        names = {n["name"] for n in npcs}
        self.assertEqual(names, {"Eldra", "Torv", "Mira"})


class TestCreatureSchema(unittest.TestCase):
    REQUIRED_KEYS = ("name", "habitat", "catch_rate_base", "size", "temperament")

    def test_every_loaded_creature_has_engine_keys(self):
        """The engine reads these keys directly; missing any one is a crash."""
        self.assertTrue(CREATURES, "no creatures loaded")
        for creature in CREATURES:
            for key in self.REQUIRED_KEYS:
                self.assertIn(key, creature, f"{creature.get('name')} missing {key}")
            self.assertIn(creature["size"], ("small", "big"))

    def test_find_creature_real_data_for_every_region(self):
        for region in REGION_IDS:
            with self.subTest(region=region):
                creature = find_creature(region)
                self.assertIn(creature["size"], ("small", "big"))
                self.assertIn("temperament", creature)


class TestFullCaptureTurn(unittest.TestCase):
    @patch("game.capture.get_player_choice", return_value=0)
    @patch("game.capture.random.random", return_value=0.01)
    def test_explore_then_capture_from_real_data(self, _rand, _choice):
        """The exact flow loop.py runs on Explore — must not raise."""
        state = create_game_state("Tester", "story")
        creature = find_creature(REGION_IDS[0])
        # mirrors the discovery line in loop.py that used to KeyError
        _ = f"{creature['size']} {creature['name']} ({creature['temperament']})"
        attempt_capture(state, creature)
        self.assertEqual(len(state["captured"]), 1)


class TestSkillTransfer(unittest.TestCase):
    def test_create_game_state_stores_act1_skills(self):
        state = create_game_state("Tester", "story", "Smarts", ["Agility", "Spirit"])
        self.assertEqual(state["primary_skill"], "Smarts")
        self.assertEqual(state["supplementary_skills"], ["Agility", "Spirit"])

    def test_primary_skill_produces_a_bonus(self):
        trained = create_game_state("Tester", "story", "Smarts", ["Agility", "Spirit"])
        untrained = create_game_state("Tester", "story")
        region = REGION_IDS[0]
        self.assertGreater(
            get_skill_bonus(trained, CATCH_RATE, region=region),
            get_skill_bonus(untrained, CATCH_RATE, region=region),
        )

    def test_npc_bond_keyed_by_loaded_npc_names(self):
        state = create_game_state("Tester", "story")
        for name in NPC_NAMES:
            self.assertIn(name, state["npc_bond"])


if __name__ == "__main__":
    unittest.main()
