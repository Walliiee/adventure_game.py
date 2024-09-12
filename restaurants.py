class Restaurant:
    def __init__(self, name, cuisine, rating, is_vegan):
        self.name = name
        self.cuisine = cuisine
        self.rating = rating
        self.is_vegan = is_vegan

bobs_burgers = Restaurant("Bob's Burgers", "American Diner", 4.7, False)
favorite_spot1 = Restaurant("Favorite Spot 1", "Cuisine 1", 4.5, True)
favorite_spot2 = Restaurant("Favorite Spot 2", "Cuisine 2", 4.8, False)

print(vars(bobs_burgers))
print(vars(favorite_spot1))
print(vars(favorite_spot2))


class Restaurant1:
  name = ''
  type = ''
  rating = 0.0
  delivery = False

bobs_burgers = Restaurant1()
bobs_burgers.name = 'Bob\'s Burgers'
bobs_burgers.type = 'American Diner'
bobs_burgers.rating = 4.2
bobs_burgers.delivery = False

katz_deli = Restaurant1()
katz_deli.name = 'Katz\'s Deli'
katz_deli.type = 'Kosher Deli'
katz_deli.rating = 4.5
katz_deli.delivery = True

baekjeong = Restaurant1()
baekjeong.name = 'Baekjeong NYC'
baekjeong.type = 'Korean BBQ'
baekjeong.rating = 4.4
baekjeong.delivery = False

print(vars(bobs_burgers))

class Student:
  student_id = 0
  name = ''
  year = 0
  gpa = 0.0
  enrolled = False

ferris = Student()
ferris.student_id = 10837
ferris.name = 'Ferris Bueller'
ferris.year = 12
ferris.gpa = 3.81
ferris.enrolled = True

print(vars(ferris))

# Write code below 💖

class Student: 
  def __init__(self, name, year, gpa, enrolled):
    self.name = name
    self.year = year
    self.gpa = gpa
    self.enrolled = enrolled

daniel = Student('Daniel Li', 10, 4.0, True)
ladybird = Student('Christine McPherson', 12, 4.0, True)
kyle = Student('Kyle Scheible', 12, 3.4, True)

print(vars(ladybird))
print(vars(kyle))
print(vars(daniel))