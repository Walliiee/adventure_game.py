import unittest

from game.act1.questions import QUESTION_BANKS, SOURCE_SKILLS, choose_question
from game.act1.state import create_act1_state


class TestAct1Questions(unittest.TestCase):
    def test_question_schema_valid(self):
        for source, skill_map in QUESTION_BANKS.items():
            for skill, questions in skill_map.items():
                self.assertIn(skill, SOURCE_SKILLS[source])
                self.assertGreater(len(questions), 0)
                for q in questions:
                    self.assertIn("text", q)
                    self.assertIn("options", q)
                    self.assertIn("correct_index", q)
                    self.assertIsInstance(q["options"], list)
                    self.assertTrue(0 <= q["correct_index"] < len(q["options"]))

    def test_choose_question_avoids_immediate_repeat_when_possible(self):
        state = create_act1_state("Test")
        first = choose_question(state, "Solo", "Strength")
        second = choose_question(state, "Solo", "Strength")
        self.assertNotEqual(first["text"], second["text"])


if __name__ == "__main__":
    unittest.main()
