#The Sorting Hat is a magical talking hat at Hogwarts School of Witchcraft and Wizardry.
#It's used to determine which of the four Houses each new student will belong to.
#The Sorting Hat is a program that will assign a Hogwarts House to a student based on their answers to a series of questions.
#The program will ask the user a series of questions and assign a House based on the answers.
#The four Houses are Gryffindor, Hufflepuff, Ravenclaw, and Slytherin.
#The program will assign a House based on the following criteria:
# 🦁 Gryffindor: Brave and chivalrous 
# 🦡 Hufflepuff: Loyal and hardworking 
# 🦅 Ravenclaw: Intelligent and creative 
# 🐍 Slytherin: Ambitious and cunning


print("Welcome to the Hogwarts Sorting Hat Quiz!")
print("Answer the following questions to determine your Hogwarts House.")

gryffindor_points = 0
hufflepuff_points = 0
ravenclaw_points = 0
slytherin_points = 0


print("Question 1 - Do you like Dawn or Dusk?\n 1) Dawn\n 2) Dusk")
answer1 = input("Enter 1 or 2: ")
while answer1 != "1" and answer1 != "2":
    print("Invalid input. Please enter 1 or 2.")
    answer1 = input("Enter 1 or 2: ")
if answer1 == "1":
        gryffindor_points += 1 
        hufflepuff_points += 1
elif answer1 == "2":
        ravenclaw_points += 1
        slytherin_points += 1


print("Question 2 - When I’m dead, I want people to remember me as:")
print(" 1) The Good\n 2) The Great\n 3) The Wise\n 4) The Bold")
answer2 = input("Enter 1-4: ")
while answer2 != "1" and answer2 != "2" and answer2 != "3" and answer2 != "4":
    print("Invalid input. Please enter 1-4:")
    answer2 = input("Enter 1-4: ")
if answer2 == "1":
        hufflepuff_points += 2
elif answer2 == "2":
        slytherin_points += 2
elif answer2 == "3":
        ravenclaw_points += 2
elif answer2 == "4":
        gryffindor_points += 2


print("Question 3 - Which kind of instrument most pleases your ear?")
print(" 1) The violin\n 2) The trumpet\n 3) The piano\n 4) The drum")
answer3 = input("Enter 1-4: ")
while answer3 != "1" and answer3 != "2" and answer3 != "3" and answer3 != "4":
        print("Invalid input. Please enter 1-4")
        answer3 = input("Enter 1-4: ")
if answer3 == "1":
        slytherin_points += 4
elif answer3 == "2":
        hufflepuff_points += 4
elif answer3 == "3":
        ravenclaw_points += 4
elif answer3 == "4":
        gryffindor_points += 4

# Determine the house with the most points
if gryffindor_points > hufflepuff_points and gryffindor_points > ravenclaw_points and gryffindor_points > slytherin_points:
    print("Congratulations! You belong in Gryffindor!")
elif hufflepuff_points > gryffindor_points and hufflepuff_points > ravenclaw_points and hufflepuff_points > slytherin_points:
    print("Congratulations! You belong in Hufflepuff!")
elif ravenclaw_points > gryffindor_points and ravenclaw_points > hufflepuff_points and ravenclaw_points > slytherin_points:
    print("Congratulations! You belong in Ravenclaw!")
elif slytherin_points > gryffindor_points and slytherin_points > hufflepuff_points and slytherin_points > ravenclaw_points:
    print("Congratulations! You belong in Slytherin!")
else:
    print("You belong in multiple houses! The Sorting Hat has chosen Gryffindor for you!")

