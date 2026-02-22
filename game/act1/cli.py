"""
Act 1 CLI: prompts for name, skill choice, questions, focus (primary + 2 supplementary).
"""
from game.act1.constants import SKILLS
from game.act1.state import current_year


def ask_act1_name() -> str:
    name = input("What is your name? ").strip()
    return name or "Keeper"


def choose_skill(state: dict) -> str | None:
    """Return skill name or None to quit."""
    print("\nWhat do you want to study?")
    for i, skill in enumerate(SKILLS, 1):
        val = state["skills"][skill]
        print(f"  {i}. {skill} (current: {val})")
    print("  q. Quit")
    while True:
        choice = input("Choice (1-4 or q): ").strip().lower()
        if choice in ("q", "quit"):
            return None
        if choice.isdigit() and 1 <= int(choice) <= 4:
            return SKILLS[int(choice) - 1]
        print("Enter 1, 2, 3, 4, or q.")


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


def choose_primary(state: dict) -> str | None:
    """After all at baseline: pick one primary skill."""
    print("\nYou're getting stronger in every way. Choose one PRIMARY skill (you must reach 4).")
    for i, skill in enumerate(SKILLS, 1):
        print(f"  {i}. {skill}")
    while True:
        choice = input("Primary (1-4): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 4:
            return SKILLS[int(choice) - 1]
        print("Enter 1, 2, 3, or 4.")


def choose_supplementary(state: dict) -> str | None:
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


def print_act1_stats(state: dict) -> None:
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


def print_ready_message(state: dict) -> None:
    print("\n" + "=" * 50)
    print("You've turned 10. You're ready.")
    print(f"Your primary skill, {state['primary']}, and your supplementary skills,")
    print(f"{state['supplementary'][0]} and {state['supplementary'][1]}, are strong enough.")
    print("You say goodbye and set out for Ridgecamp.")
    print("=" * 50)
