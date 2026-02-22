guess = 0
tries = 0

while guess != 6 and tries < 5:
  guess = int(input("Guess the number:  "))
  tries += 1
  if guess != 6:
    print("Not the right one. Try again.")
    print("You have " + str(5 - tries) + " tries left.")

if tries == 5:
    print("You are out of tries.")

else:
    print("You got it!!")


guess = 0
tries = 0
tries_left = 2

while guess != 6:
  guess = int(input("Guess the number:  "))
  tries +=1
  tries_left -=1
  print("You have used", tries, "tries and have", tries_left, "tries left")

  if tries_left == 0:
    print("You failed")

else:
  print("You got it!")