import random

symbols = [' 🍒',' 🍇', ' 🍉', ' 7️⃣']

results = random.choices(symbols, k=3)

print(results)

if results == ['7️⃣', '7️⃣', '7️⃣']:
    print("JACKPOT! 🎉")
else:
    while True:
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again == 'yes':
            results = random.choices(symbols, k=3)
            print(results)
        elif play_again == 'no':
            print("Thanks for playing! 🎰")
            break
        elif play_again != 'yes' or play_again != 'no':
            print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            break


symbols = [
  '🍒',
  '🍇',
  '🍉',
  '7️⃣'
]

def play():

  for i in range(1, 51):    
    results = random.choices(symbols, k=3)
    print(f'{results[0]} | {results[1]} | {results[2]}')
    win = results[0] == '7️⃣' and results[1] == '7️⃣' and results[2] == '7️⃣'

    if win:
      print('Jackpot!!! 💰')
      break
    else:
      results = random.choices(symbols, k=3)

answer = ''
while answer.upper() != 'N':
  play()
  answer = input('Keep playing? (Y/N) ')

print('Thanks for playing!')