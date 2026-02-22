"""
Entry point: Act 1 (training 7→10) then Act 2 (Keeper loop), or skip to Act 2 for testing.
"""
from game.state import create_game_state
from game.cli import choose_difficulty, ask_replay
from game.loop import run_session
from game.act1 import run_act1


def main(quick_test: bool = False) -> None:
    print("Welcome to Wildlands: Orb Catcher Adventure!\n")

    if quick_test:
        # Skip Act 1: go straight to Ridgecamp (Act 2) for testing.
        player_name = "Test"
        difficulty = "story"
        print("(Test mode: skipping Act 1, name=Test, difficulty=story)\n")
    else:
        # Full journey: Act 1 (build character, train 7→10) then Act 2.
        ready, player_name = run_act1(skip_intro=False)
        if not ready:
            print("Thanks for playing. Come back when you're ready to train!")
            return
        print("\n--- Ridgecamp (Act 2) ---\n")
        difficulty = choose_difficulty()

    while True:
        state = create_game_state(player_name, difficulty)
        run_session(state)
        if not ask_replay():
            print("Thanks for playing Wildlands: Orb Catcher Adventure!")
            break


if __name__ == "__main__":
    main()
