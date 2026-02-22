todo = ['🏦 Get quarters.', 
'🧺 Do laundry.', 
'🌳 Take a walk.', 
'💈 Get a haircut.', 
'🍵 Make some tea.', 
'💻 Complete Lists chapter.', 
'💖 Call mom.', 
'📺 Watch My Hero Academia.']

print(todo)
print("--------------------------------------")
print(todo[0])
print(todo[1])
print("--------------------------------------")
print(todo[3 : 6])

for i, item in enumerate(todo, 1):
    print(f"{i}. {item}")