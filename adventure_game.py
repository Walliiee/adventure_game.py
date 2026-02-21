import random
import sys


CREATURES = [
    {
        "name": "Moss Bunny",
        "size": "small",
        "habitat": "meadow",
        "temperament": "gentle",
        "base_catch": 0.78,
    },
    {
        "name": "Spark Finch",
        "size": "small",
        "habitat": "ruins",
        "temperament": "curious",
        "base_catch": 0.74,
    },
    {
        "name": "Pebble Otter",
        "size": "small",
        "habitat": "river",
        "temperament": "playful",
        "base_catch": 0.72,
    },
    {
        "name": "Iron Tusk",
        "size": "big",
        "habitat": "canyon",
        "temperament": "stubborn",
        "base_catch": 0.4,
    },
    {
        "name": "Thunder Yak",
        "size": "big",
        "habitat": "highlands",
        "temperament": "proud",
        "base_catch": 0.36,
    },
    {
        "name": "Moonclaw Lynx",
        "size": "big",
        "habitat": "forest",
        "temperament": "fierce",
        "base_catch": 0.34,
    },
]


def get_player_choice(options, aliases=None, prompt="Enter your choice: "):
    aliases = aliases or {}
    while True:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input(prompt).strip().lower()
        if choice in {"quit", "q", "exit"}:
            print("Thanks for playing!")
            sys.exit()

        if choice in aliases:
            return aliases[choice]

        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1

        print("Invalid choice. Try a number or keyword.")


def choose_difficulty():
    print("Choose your difficulty:")
    options = ["Story", "Classic", "Hardcore"]
    aliases = {"story": 0, "classic": 1, "hardcore": 2, "hard": 2}
    return ["story", "classic", "hardcore"][get_player_choice(options, aliases)]


def create_game_state(player_name, difficulty):
    health_by_difficulty = {"story": 16, "classic": 12, "hardcore": 9}
    balls_by_difficulty = {
        "story": {"mini": 8, "mega": 5},
        "classic": {"mini": 6, "mega": 3},
        "hardcore": {"mini": 4, "mega": 2},
    }
    return {
        "name": player_name,
        "difficulty": difficulty,
        "health": health_by_difficulty[difficulty],
        "captured": [],
        "turn": 1,
        "region_progress": set(),
        "balls": balls_by_difficulty[difficulty],
        "npc_bond": {"Mira": 0, "Sol": 0, "Ari": 0},
    }


def print_banner():
    print("\n" + "=" * 58)
    print("🧭  WILDLANDS: ORB CATCHER ADVENTURE")
    print("=" * 58)
    print("  🌲 Forest   🌾 Meadow   🏛️ Ruins   🏞️ River   🪨 Canyon")
    print("=" * 58)


def show_characters():
    print("\nYour crew in Ridgecamp:")
    print("👩‍🌾 Ranger Mira  - animal tracker and care expert")
    print("🛠️ Mechanic Sol   - builds stronger capture orbs")
    print("🧢 Rival Ari      - bold challenger who pushes your growth")


def display_intro(state):
    print_banner()
    print(f"Welcome, {state['name']}! Difficulty: {state['difficulty'].title()}")
    print("You are an Orb Keeper. Catch small and big wild animals in circular capture orbs,")
    print("then train and play with them so they become trusted companions.")
    show_characters()
    print("\nGoal: build a balanced team and win the Ridgecamp Exhibition Match.\n")


def print_stats(state):
    mini = state["balls"]["mini"]
    mega = state["balls"]["mega"]
    print(f"\n[Day {state['turn']}] Health: {state['health']} | Mini Orbs: {mini} | Mega Orbs: {mega}")
    if state["captured"]:
        print("Companions:")
        for pet in state["captured"]:
            print(
                f" - {pet['name']} ({pet['size']}) Lv.{pet['level']} Bond:{pet['bond']} Mood:{pet['mood']}"
            )
    else:
        print("Companions: none yet")


def choose_region(state):
    print("\nChoose a region to explore:")
    options = ["🌾 Sunmeadow", "🏛️ Old Ruins", "🏞️ Silver River", "🪨 Storm Canyon", "🌲 Moonwood"]
    aliases = {"meadow": 0, "ruins": 1, "river": 2, "canyon": 3, "moonwood": 4, "forest": 4}
    idx = get_player_choice(options, aliases)
    regions = ["meadow", "ruins", "river", "canyon", "forest"]
    region = regions[idx]
    state["region_progress"].add(region)
    return region


def find_creature(region):
    candidates = [c for c in CREATURES if c["habitat"] == region]
    if not candidates:
        candidates = CREATURES
    creature = random.choice(candidates).copy()
    creature["level"] = 1
    creature["bond"] = 1
    creature["mood"] = "curious"
    return creature


def attempt_capture(state, creature):
    ball_type = "mini" if creature["size"] == "small" else "mega"
    alt_ball = "mega" if ball_type == "mini" else "mini"

    options = [
        f"Use a {ball_type.title()} Orb (best fit)",
        f"Use a {alt_ball.title()} Orb",
        "Offer food and leave peacefully",
    ]
    aliases = {"best": 0, "alt": 1, "leave": 2, "food": 2}
    pick = get_player_choice(options, aliases)

    if pick == 2:
        print(f"You offer food to {creature['name']}. It relaxes and wanders away peacefully.")
        state["health"] += 1
        return

    chosen = ball_type if pick == 0 else alt_ball
    if state["balls"][chosen] <= 0:
        print(f"No {chosen.title()} Orbs left! The creature escapes.")
        return

    state["balls"][chosen] -= 1
    chance = creature["base_catch"]
    if chosen != ball_type:
        chance -= 0.2

    if state["difficulty"] == "story":
        chance += 0.1
    elif state["difficulty"] == "hardcore":
        chance -= 0.08

    roll = random.random()
    if roll <= chance:
        print(f"✨ Click! {creature['name']} was captured in your circular orb!")
        state["captured"].append(creature)
        state["npc_bond"]["Mira"] += 1
    else:
        print(f"💨 {creature['name']} breaks free!")
        state["health"] -= 2 if creature["size"] == "big" else 1


def pick_companion(state, action):
    if not state["captured"]:
        print(f"You need a companion before you can {action}.")
        return None

    print(f"\nChoose a companion to {action}:")
    options = [f"{c['name']} ({c['size']})" for c in state["captured"]]
    idx = get_player_choice(options)
    return state["captured"][idx]


def train_companion(state):
    companion = pick_companion(state, "train")
    if not companion:
        return

    print(f"You run drills with {companion['name']}: agility loops, focus tests, and team signals.")
    companion["level"] += 1
    companion["bond"] += 1
    companion["mood"] = "motivated"
    state["npc_bond"]["Ari"] += 1


def play_with_companion(state):
    companion = pick_companion(state, "play")
    if not companion:
        return

    print(f"You play fetch and rhythm games with {companion['name']} at camp.")
    companion["bond"] += 2
    companion["mood"] = "happy"
    state["health"] += 1
    state["npc_bond"]["Sol"] += 1


def exhibition_match(state):
    print("\n🏟️ Ridgecamp Exhibition Match begins!")
    if len(state["captured"]) < 2:
        print("You needed at least 2 companions to compete. You are not ready yet.")
        return False

    team_power = sum(c["level"] + c["bond"] for c in state["captured"])
    bonus = len(state["region_progress"]) + sum(state["npc_bond"].values())
    threshold = 18 if state["difficulty"] == "story" else 22 if state["difficulty"] == "classic" else 26

    print(f"Team Power: {team_power} | Synergy Bonus: {bonus} | Target: {threshold}")
    if team_power + bonus >= threshold:
        print("🎉 Your companions perform brilliantly. Ridgecamp crowns you Champion Keeper!")
        return True

    print("Ari wins this season, but your team shows promise. Train harder and return.")
    return False


def day_menu(state):
    options = [
        "Explore wild region and attempt a capture",
        "Train a companion",
        "Play with a companion",
        "View stats",
        "Start exhibition match",
        "Quit adventure",
    ]
    aliases = {
        "explore": 0,
        "train": 1,
        "play": 2,
        "stats": 3,
        "match": 4,
        "quit": 5,
        "q": 5,
    }
    return get_player_choice(options, aliases, prompt="Choose your camp action: ")


def start_game(state):
    display_intro(state)

    while state["health"] > 0:
        choice = day_menu(state)

        if choice == 0:
            region = choose_region(state)
            creature = find_creature(region)
            print(
                f"\nYou discover a {creature['size']} wild animal: {creature['name']} "
                f"({creature['temperament']})."
            )
            attempt_capture(state, creature)
        elif choice == 1:
            train_companion(state)
        elif choice == 2:
            play_with_companion(state)
        elif choice == 3:
            print_stats(state)
            continue
        elif choice == 4:
            won = exhibition_match(state)
            if won:
                return
        else:
            print("You pack your gear and leave Ridgecamp. Adventure paused.")
            return

        state["turn"] += 1
        if state["health"] <= 0:
            print("\nYou collapse from exhaustion. Your companions guard you until help arrives.")
            return


def ask_replay():
    while True:
        response = input("\nPlay again? (y/n): ").strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def main():
    print("Welcome to your expanded creature-catching adventure!\n")
    player_name = input("What is your Keeper name? ").strip() or "Traveler"
    difficulty = choose_difficulty()

    while True:
        state = create_game_state(player_name, difficulty)
        start_game(state)
        if not ask_replay():
            print("Thanks for playing Wildlands: Orb Catcher Adventure!")
            break


if __name__ == "__main__":
    main()
