import unittest

from game.state import create_game_state
from game.world import describe_region, get_npc_scene


class TestWorldNarrative(unittest.TestCase):
    def test_region_has_flavor(self):
        text = describe_region("meadow")
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 20)

    def test_npc_scene_marks_seen(self):
        state = create_game_state("Tester", "story")
        scene = get_npc_scene(state, "forest")
        self.assertIsNotNone(scene)
        self.assertIn(scene, state["seen_npc_scenes"])


if __name__ == "__main__":
    unittest.main()
