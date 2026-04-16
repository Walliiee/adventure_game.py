import unittest

from game.constants import CREATURES, NPC_SCENES_BY_REGION
from game.state import create_game_state
from game.world import find_creature, get_npc_scene


class TestWorldSpawning(unittest.TestCase):
    def test_find_creature_falls_back_for_unknown_region(self):
        creature = find_creature("unknown-region")
        valid_names = {c["name"] for c in CREATURES}
        self.assertIn(creature["name"], valid_names)
        self.assertEqual(creature["level"], 1)
        self.assertEqual(creature["bond"], 1)
        self.assertEqual(creature["mood"], "curious")

    def test_get_npc_scene_reuses_pool_after_all_seen(self):
        state = create_game_state("Tester", "story")
        candidates = NPC_SCENES_BY_REGION["forest"]
        state["seen_npc_scenes"] = set(candidates)
        scene = get_npc_scene(state, "forest")
        self.assertIn(scene, candidates)


if __name__ == "__main__":
    unittest.main()
