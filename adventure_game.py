import random
import sys


def choose_difficulty():
    print("Choose your difficulty:")
    options = ["Story (forgiving)", "Classic (default)", "Hardcore (dangerous)"]
    aliases = {"story": 0, "classic": 1, "hardcore": 2, "hard": 2}
    choice = get_player_choice(options, aliases)
    return ["story", "classic", "hardcore"][choice]


def create_game_state(player_name, difficulty):
    health_by_difficulty = {"story": 12, "classic": 10, "hardcore": 8}
    return {
        "name": player_name,
        "difficulty": difficulty,
        "health": health_by_difficulty[difficulty],
        "courage": 0,
        "luck": 0,
        "inventory": [],
        "choices": [],
        "ending": None,
        "scouted": False,
        "encounter_done": False,
        "achievements": [],
    }


def display_intro(state):
    print("\nWelcome to the Mini Adventure Game!")
    print(f"Adventurer: {state['name']} | Difficulty: {state['difficulty'].title()}")
    print("You find yourself at a crossroads in a mysterious forest.")
    print("Your choices will determine your fate. Choose wisely!\n")



def print_stats(state):
    inventory_text = ", ".join(state["inventory"]) if state["inventory"] else "none"
    print(
        f"\n[Stats] Health: {state['health']} | Courage: {state['courage']} | "
        f"Luck: {state['luck']} | Inventory: {inventory_text}"
    )


def get_player_choice(options, aliases=None):
    aliases = aliases or {}
    while True:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Enter your choice (number/keyword, help, quit): ").strip().lower()

        if choice in {"help", "h"}:
            shortcut_text = ", ".join(sorted(aliases.keys())) if aliases else "none"
            print(f"Type a number or shortcut keyword. Keywords here: {shortcut_text}")
            continue

        if choice in {"quit", "q", "exit"}:
            print("Thanks for playing!")
            sys.exit()

        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1

        if choice in aliases:
            return aliases[choice]

        print("Invalid choice. Please try again.")


def apply_random_encounter(state):
    if state["encounter_done"]:
        return

    events = ["herbs", "coin", "thorns"]
    event = random.choice(events)
    state["encounter_done"] = True

    if event == "herbs":
        state["health"] += 2
        state["luck"] += 1
        print("\nYou discover healing herbs on the trail (+2 health, +1 luck).")
    elif event == "coin":
        state["luck"] += 2
        state["inventory"].append("old coin")
        print("\nYou find an old coin tucked under a stone (+2 luck).")
    else:
        damage = 1 if state["difficulty"] == "story" else 2
        state["health"] -= damage
        print(f"\nHidden thorns scratch your leg (-{damage} health).")


def evaluate_achievements(state):
    if state.get("won"):
        state["achievements"].append("Survivor")
    if "climb_tree" in state["choices"] and "dark_path" in state["choices"] and "clear_trail" in state["choices"]:
        state["achievements"].append("Explorer")
    if state["won"] and len(state["choices"]) <= 3:
        state["achievements"].append("Speedrunner")


def finish_game(state, message, won=False):
    state["ending"] = message
    state["won"] = won
    evaluate_achievements(state)
    print(f"\n{message}")
    print("\n=== Adventure Summary ===")
    print(f"Player: {state['name']}")
    print(f"Difficulty: {state['difficulty'].title()}")
    print(f"Result: {'Victory' if won else 'Defeat'}")
    print(f"Choices made: {len(state['choices'])}")
    if state["achievements"]:
        print(f"Achievements: {', '.join(state['achievements'])}")
    print_stats(state)
    print("=========================\n")


def start_game(state):
    display_intro(state)

    print("You see two paths ahead and a tall tree nearby:")
    options = [
        "Take the dark, overgrown path",
        "Follow the well-lit, clear trail",
        "Climb a nearby tree to get a better view",
    ]
    aliases = {"dark": 0, "trail": 1, "tree": 2, "climb": 2}
    choice = get_player_choice(options, aliases)
    state["choices"].append("crossroads")

    if choice == 0:
        state["courage"] += 1
        dark_path(state)
    elif choice == 1:
        clear_trail(state)
    else:
        state["courage"] += 1
        state["luck"] += 1
        climb_tree(state)


def dark_path(state):
    print("\nYou venture into the dark, overgrown path.")
    print("As you push through the thick vegetation, you hear strange noises...")

    if state["scouted"]:
        print("Thanks to your earlier scouting, you notice fresh bear tracks and stay alert.")

    options = ["Investigate the noise", "Try to quietly backtrack"]
    aliases = {"investigate": 0, "noise": 0, "back": 1, "backtrack": 1}
    choice = get_player_choice(options, aliases)
    state["choices"].append("dark_path")

    if choice == 0:
        if state["scouted"]:
            print("You avoid the bear and discover a dropped lantern near the tracks!")
            state["inventory"].append("lantern")
            state["luck"] += 1
            clear_trail(state)
        else:
            damage = 8 if state["difficulty"] == "story" else 10
            state["health"] -= damage
            finish_game(state, "You disturb a sleeping bear. It doesn't end well.", won=False)
    else:
        print("\nYou successfully backtrack and return to safer ground.")
        state["luck"] += 1
        clear_trail(state)


def clear_trail(state):
    print("\nYou follow the well-lit, clear trail.")
    apply_random_encounter(state)
    print("After walking for a while, you come across a mysterious old house.")
    options = ["Enter the house", "Continue past the house"]
    aliases = {"enter": 0, "house": 0, "continue": 1, "past": 1}
    choice = get_player_choice(options, aliases)
    state["choices"].append("clear_trail")

    if choice == 0:
        enter_house(state)
    else:
        finish_game(
            state,
            "You continue past the house and eventually find your way out of the forest. You win!",
            won=True,
        )


def climb_tree(state):
    print("\nYou decide to climb the tall tree to get a better view.")
    print("After a challenging climb, you reach the top and survey the landscape.")
    print("\nFrom your vantage point, you can see:")
    print("1. The dark path leads into dense woods, and you spot movement near old ruins.")
    print("2. The clear trail winds through a meadow toward a small village.")
    if state["difficulty"] == "story":
        print("Hint: scouting made the dark path less risky this run.")
    print("\nArmed with this information, you climb back down.")

    state["scouted"] = True
    state["choices"].append("climb_tree")

    options = ["Take the dark path towards the mysterious ruins", "Follow the clear trail"]
    aliases = {"dark": 0, "ruins": 0, "clear": 1, "trail": 1}
    choice = get_player_choice(options, aliases)

    if choice == 0:
        dark_path(state)
    else:
        clear_trail(state)


def enter_house(state):
    print("\nYou enter the old house. It's dark and dusty inside.")
    print("You see a glinting object on a table and a staircase leading upstairs.")
    options = ["Examine the glinting object", "Go upstairs"]
    aliases = {"object": 0, "amulet": 0, "stairs": 1, "upstairs": 1}
    choice = get_player_choice(options, aliases)
    state["choices"].append("enter_house")

    if choice == 0:
        state["inventory"].append("magical amulet")
        state["luck"] += 2
        finish_game(state, "It's a magical amulet! Its power teleports you to safety. You win!", won=True)
    else:
        if "lantern" in state["inventory"]:
            state["courage"] += 1
            finish_game(
                state,
                "Your lantern reveals weak steps just in time. You find attic supplies and escape safely. You win!",
                won=True,
            )
        else:
            damage = 8 if state["difficulty"] == "story" else 10
            state["health"] -= damage
            finish_game(state, "The stairs collapse under you. Game over!", won=False)


def ask_replay():
    while True:
        response = input("Play again? (y/n): ").strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def main():
    print("Welcome back to your first real project. Let's make it an adventure!\n")
    player_name = input("What is your adventurer name? ").strip() or "Traveler"
    difficulty = choose_difficulty()

    while True:
        state = create_game_state(player_name, difficulty)
        start_game(state)
        if not ask_replay():
            print("Thanks for playing. See you next run!")
            break


if __name__ == "__main__":
    main()
