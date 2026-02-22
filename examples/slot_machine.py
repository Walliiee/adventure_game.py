import random

SYMBOLS = ["🍒", "🍇", "🍉", "7️⃣"]


def spin():
    """Return three random symbols and whether it's a jackpot."""
    results = random.choices(SYMBOLS, k=3)
    jackpot = results == ["7️⃣", "7️⃣", "7️⃣"]
    return results, jackpot


def play():
    results, jackpot = spin()
    print(f"{results[0]} | {results[1]} | {results[2]}")
    if jackpot:
        print("JACKPOT! 🎉")
    return jackpot


def main():
    while True:
        play()
        while True:
            answer = input("Play again? (yes/no): ").strip().lower()
            if answer in ("yes", "y"):
                break
            if answer in ("no", "n"):
                print("Thanks for playing! 🎰")
                return
            print("Invalid input. Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main()
