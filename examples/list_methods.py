# dna = ['AUG', 'AUC', 'UCG']

# dna.append('UAA')     # ['AUG', 'AUC', 'UCG', 'UAA']
# dna.insert(2, 'GAU')  # ['AUG', 'AUC', 'GAU', 'UCG', 'UAA']
# dna.remove('AUC')     # ['AUG', 'GAU', 'UCG', 'UAA']
# dna.pop(0)            # ['GAU', 'UCG', 'UAA']

# print(dna)


# # Built-in functions

# stock1_prices = [2.52, 2.44, 2.32, 2.41, 2.51, 2.50, 2.44]
# stock2_prices = [8.36, 8.31, 8.21, 8.21, 8.25, 8.11, 8.13]

# print(len(stock1_prices))      # Output: 7
# print(max(stock1_prices))      # Output: 2.52
# print(min(stock2_prices))      # Output: 8.11

# lego_parts = [8980, 7323, 5343, 82700, 92232, 1203, 7319, 8903, 2328, 1279, 679, 589]

# print(len(lego_parts))
# print(max(lego_parts))
# print(min(lego_parts))


books = ['Zero to One',
'The Lean Startup',
'The Mom Test',
'Make It Stick',
'Life in Code']

books.append("Zero to Sold") 
books.remove("Zero to One")
books.pop(1)
books.insert(2, "The Lean Startup")
books.extend(["The Lean Startup", "The Lean Startup"]) # Add multiple items to the list. It is different from append which adds a single item to the list at the end.
books.sort() # Sort the list in place
books.index("The Lean Startup") # Find the index of the first occurrence of the item in the list

print(books)

# Comment out all ctrl + '
# List Method	Description
# .append()	Add an item to the end of the list
# .clear()	Remove all items from the list
# .copy()	Return a shallow copy of the list
# .count()	Return the number of times the value appears in the list
# .extend()	Appends another list to the current list by extending it
# .index()	Returns the index of a value inside the list
# .insert()	Insert an item at a specified position in the list
# .pop()	Remove an item from a specified position in the list
# .remove()	Remove an item from the list based on the value of the item
# .reverse()	Reverses the list in place
# .sort()	Sorts the list in place 