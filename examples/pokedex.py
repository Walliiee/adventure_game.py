class Pokemon:
  def __init__(self, entry, name, types, level, description, height, is_caught):
    self.entry = entry
    self.name = name
    self.types = types
    self.level = level
    self.description = description
    self.height = height
    self.is_caught = is_caught

  def speak(self):
    print(self.name + ' ' + self.name)

  def display_details(self):
    print(f'Entry: {self.entry}')
    print(f'Name: {self.name}')
    print(f'Types: {self.types}')
    print(f'Level: {self.level}')
    print(f'Description: {self.description}')
    print(f'Height: {self.height}')
    print(f'Is Caught: {self.is_caught}')

    
Pikachu = Pokemon (25, 'Pikachu', 'Electric', 55, 'It has small electric sacs on both its cheeks. If threatened, it looses electric charges from the sacs.',63.5, 'Pikachu has already been caught')

Pikachu.speak()
Pikachu.display_details()

