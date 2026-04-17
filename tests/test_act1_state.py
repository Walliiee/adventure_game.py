import unittest

from game.act1.constants import ACTIONS_PER_YEAR
from game.act1.state import actions_until_year_three, create_act1_state, is_ready


class TestAct1State(unittest.TestCase):
    def test_ready_requires_year_three_and_thresholds(self):
        state = create_act1_state("Kid")
        state["focus_chosen"] = True
        state["primary"] = "Strength"
        state["supplementary"] = ["Agility", "Smarts"]
        state["skills"].update({"Strength": 4, "Agility": 3, "Smarts": 3, "Spirit": 2})

        state["actions"] = (ACTIONS_PER_YEAR * 2) - 1
        self.assertFalse(is_ready(state))

        state["actions"] = ACTIONS_PER_YEAR * 2
        self.assertTrue(is_ready(state))

    def test_state_initializes_stabilizer_fields(self):
        state = create_act1_state("Kid")
        self.assertEqual(state["wrong_streak"], 0)
        self.assertEqual(state["last_question_idx"], {})

    def test_actions_until_year_three_counts_down(self):
        state = create_act1_state("Kid")
        self.assertEqual(actions_until_year_three(state), ACTIONS_PER_YEAR * 2)

        state["actions"] = ACTIONS_PER_YEAR
        self.assertEqual(actions_until_year_three(state), ACTIONS_PER_YEAR)

        state["actions"] = ACTIONS_PER_YEAR * 2
        self.assertEqual(actions_until_year_three(state), 0)


if __name__ == "__main__":
    unittest.main()
