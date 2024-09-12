import random

def fortune():
    random_fortune = random.randint(0, 10)
    fortunes = ["Don't pursue happiness create it.",
    "All things are difficult before they are easy.",
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "Someone in your life needs a letter from you.",
    "Don't just think. Act!",
    "Your heart will skip a beat.",
    "The fortune you search for is in another cookie.",
    "Help! I'm being held prisoner in a Chinese bakery!",
    "Plan for many pleasures ahead.",
    "Your shoes will make you happy today.",
    "Land is always on the mind of a flying bird.",
    ]
    print("Your fortune cookie says: ", fortunes[random_fortune]) # prints the random fortune 
    print(random_fortune, fortunes[random_fortune]) # for testing purposes only to see the random number and fortune generated

fortune()
