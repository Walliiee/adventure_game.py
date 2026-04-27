"""
Act 1 CLI: prompts for name, learning source, skill choice, questions, focus.
"""
from __future__ import annotations

from game.act1.constants import (
    SKILLS,
    BASELINE,
    PRIMARY_THRESHOLD,
    SUPPLEMENTARY_THRESHOLD,
)
from game.act1.questions import SOURCE_SKILLS
from game.act1.state import (
    Act1State,
    actions_until_year_three,
    current_year,
    focus_thresholds_met,
)


SOURCES = ("Solo", "Teacher", "Mentor", "Parent", "Pet")

COACHING_TIPS = {
    "Strength": "Tip: think safety + body mechanics first.",
    "Agility": "Tip: controlled movement beats rushing.",
    "Smarts": "Tip: use habitat clues and Keeper rules.",
    "Spirit": "Tip: calm, patience, and trust are strongest.",
}


def ask_act1_name() -> str:
    name = input("What is your name? ").strip()
    return name or "Keeper"


def choose_source() -> str | None:
    """Return source name or None to quit."""
    print("\nWho do you want to study with?")
    for i, source in enumerate(SOURCES, 1):
        print(f"  {i}. {source}")
    print("  q. Quit")
    while True:
        choice = input("Choice (1-5 or q): ").strip().lower()
        if choice in ("q", "quit"):
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(SOURCES):
            return SOURCES[int(choice) - 1]
        print("Enter 1, 2, 3, 4, 5, or q.")


def choose_skill_for_source(state: Act1State, source: str) -> str:
    """Return a skill supported by the chosen source."""
    options = SOURCE_SKILLS[source]
    print(f"\nWhat do you want to study with {source}?")
    for i, skill in enumerate(options, 1):
        print(f"  {i}. {skill} (current: {state['skills'][skill]})")
    while True:
        choice = input(f"Choice (1-{len(options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Enter a number from the list.")


def ask_question(skill: str, question: dict) -> bool:
    """Show multiple choice; return True if correct."""
    print(f"\n--- {skill} ---")
    print(question["text"])
    opts = question["options"]
    for i, opt in enumerate(opts, 1):
        print(f"  {i}. {opt}")
    correct_idx = question["correct_index"]
    letters = "abcd"[: len(opts)]
    prompt = f"Answer (1-{len(opts)} or a-{letters}): "
    while True:
        raw = input(prompt).strip().lower()
        idx = None
        if raw.isdigit() and 1 <= int(raw) <= len(opts):
            idx = int(raw) - 1
        if raw in letters:
            idx = letters.index(raw)
        if idx is not None:
            correct = idx == correct_idx
            if correct:
                print("Correct! +1", skill)
            else:
                print("Not quite. The right answer was:", opts[correct_idx])
            return correct
        print("Enter a number or letter for your choice.")


def print_stabilizer_feedback(state: Act1State, skill: str, correct: bool) -> None:
    """Provide light coaching to reduce frustration and guide progress."""
    if correct:
        print("Nice work. Keep momentum!")
        return
    if state["wrong_streak"] >= 2:
        print(f"Coach: {COACHING_TIPS[skill]}")


def print_training_guidance(state: Act1State) -> None:
    """Show clear next-step guidance after each action."""
    if not state["focus_chosen"]:
        missing = [s for s in SKILLS if state["skills"][s] < BASELINE]
        if missing:
            print(f"Guidance: bring these to baseline ({BASELINE}): {', '.join(missing)}")
        return

    if focus_thresholds_met(state):
        remaining = actions_until_year_three(state)
        if remaining > 0:
            print(
                f"Guidance: skill targets met. Keep training {remaining} more action(s) "
                f"to reach Year 3 (age 10)."
            )
        return

    primary = state["primary"]
    if primary is None:
        return
    primary_left = PRIMARY_THRESHOLD - state["skills"][primary]
    supp_left = {
        s: SUPPLEMENTARY_THRESHOLD - state["skills"][s]
        for s in state["supplementary"]
    }
    primary_msg = f"{primary} needs {max(0, primary_left)} more"
    supp_msg = ", ".join(f"{s} needs {max(0, left)}" for s, left in supp_left.items())
    remaining = actions_until_year_three(state)
    if remaining > 0:
        print(
            f"Guidance: {primary_msg}; {supp_msg}. "
            f"Year goal: {remaining} more action(s) to age 10."
        )
    else:
        print(f"Guidance: {primary_msg}; {supp_msg}.")


def choose_primary(state: Act1State) -> str | None:
    """After all at baseline: pick one primary skill."""
    print("\nYou're getting stronger in every way. Choose one PRIMARY skill (you must reach 4).")
    for i, skill in enumerate(SKILLS, 1):
        print(f"  {i}. {skill}")
    while True:
        choice = input("Primary (1-4): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 4:
            return SKILLS[int(choice) - 1]
        print("Enter 1, 2, 3, or 4.")


def choose_supplementary(state: Act1State) -> str | None:
    """Pick supplementary skill(s); need 2 total. Return chosen skill or None to skip."""
    need = 2 - len(state["supplementary"])
    if need <= 0:
        return None
    remaining = [s for s in SKILLS if s != state["primary"] and s not in state["supplementary"]]
    print(f"\nChoose supplementary skill {2 - need + 1} of 2 (each must reach 3). Remaining: {', '.join(remaining)}")
    for i, skill in enumerate(remaining, 1):
        print(f"  {i}. {skill}")
    while True:
        choice = input("Choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(remaining):
            return remaining[int(choice) - 1]
        print("Enter a number from the list.")


def print_act1_stats(state: Act1State) -> None:
    year = current_year(state)
    print(f"\n--- Year {year} of 3 | Actions: {state['actions']} ---")
    for skill in SKILLS:
        val = state["skills"][skill]
        tag = ""
        if state["primary"] == skill:
            tag = " (primary)"
        elif skill in state["supplementary"]:
            tag = " (supp)"
        print(f"  {skill}: {val}{tag}")


def print_ready_message(state: Act1State) -> None:
    print("\n" + "=" * 50)
    print("You've turned 10. You're ready.")
    print(f"Your primary skill, {state['primary']}, and your supplementary skills,")
    print(f"{state['supplementary'][0]} and {state['supplementary'][1]}, are strong enough.")
    print("You say goodbye and set out for Ridgecamp.")
    print("=" * 50)
