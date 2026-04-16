import io
import unittest
from contextlib import redirect_stdout

from game.act1 import cli as act1_cli
from game.act1.loop import year_completion_message
from game.act1.state import create_act1_state


class TestAct1MvpGuidance(unittest.TestCase):
    def test_year_completion_message_uses_completed_year_number(self):
        self.assertEqual(
            year_completion_message(10),
            "\n--- Year 1 of 3 complete. Keep training! ---",
        )
        self.assertEqual(
            year_completion_message(20),
            "\n--- Year 2 of 3 complete. Keep training! ---",
        )
        self.assertIsNone(year_completion_message(0))
        self.assertIsNone(year_completion_message(30))

    def test_guidance_shows_remaining_actions_when_skill_targets_met_early(self):
        state = create_act1_state("Kid")
        state["focus_chosen"] = True
        state["primary"] = "Strength"
        state["supplementary"] = ["Agility", "Smarts"]
        state["skills"].update({"Strength": 4, "Agility": 3, "Smarts": 3, "Spirit": 2})
        state["actions"] = 12

        with io.StringIO() as buf, redirect_stdout(buf):
            act1_cli.print_training_guidance(state)
            output = buf.getvalue()

        self.assertIn("skill targets met", output)
        self.assertIn("8 more action(s)", output)


if __name__ == "__main__":
    unittest.main()
