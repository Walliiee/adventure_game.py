"""
Act 1 training loop: study skills with questions, choose focus when all at baseline,
advance time, check readiness. Returns (ready, player_name) or (False, name) if quit.
"""
from game.act1.state import (
    create_act1_state,
    current_year,
    all_at_baseline,
    is_ready,
)
from game.act1.constants import SKILLS, ACTIONS_PER_YEAR
from game.act1.questions import QUESTIONS
from game.act1 import cli as act1_cli


def run_act1(skip_intro: bool = False) -> tuple[bool, str]:
    """
    Run the training phase (ages 7→10). Returns (True, player_name) when ready
    to start Act 2, or (False, player_name) if the player quits.
    """
    if not skip_intro:
        print("\n" + "=" * 50)
        print("  WILDLANDS — Act 1: Training (Ages 7 to 10)")
        print("=" * 50)
        print("You're 7. In three years you can go out and catch friends.")
        print("Train hard: study each skill, then choose one primary and two supplementary.")
        print("When you're ready, you'll set out for Ridgecamp.")
        print("=" * 50)

    name = act1_cli.ask_act1_name()
    state = create_act1_state(name)

    while True:
        act1_cli.print_act1_stats(state)

        # After enough actions, advance "year" message
        if state["actions"] > 0 and state["actions"] % ACTIONS_PER_YEAR == 0:
            y = current_year(state)
            if y <= 3:
                print(f"\n--- Year {y} of 3 complete. Keep training! ---")

        # When all four at baseline, force focus choice if not yet chosen
        if all_at_baseline(state) and not state["focus_chosen"]:
            state["focus_chosen"] = True
            state["primary"] = act1_cli.choose_primary(state)
            while len(state["supplementary"]) < 2:
                sup = act1_cli.choose_supplementary(state)
                if sup and sup not in state["supplementary"]:
                    state["supplementary"].append(sup)
            print("\nFocus set. Keep training until primary reaches 4 and supplementaries reach 3.")
            continue

        skill = act1_cli.choose_skill(state)
        if skill is None:
            print("Training paused. Come back when you're ready.")
            return False, name

        q = QUESTIONS[skill]
        correct = act1_cli.ask_question(skill, q)
        if correct:
            state["skills"][skill] += 1
        state["actions"] += 1

        if is_ready(state):
            act1_cli.print_ready_message(state)
            return True, name
