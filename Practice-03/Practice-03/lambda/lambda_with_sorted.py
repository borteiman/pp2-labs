# Step 1: Sort a list of tuples by the second element (age)
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

# Step 2: Sort a list of strings by their length
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)



# Example 1: Sort a list of tuples by the second element
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

# Example 2: Sort strings by length
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

# Example 3: Sort a list of dictionaries by a specific key
# Step 1: Define a list of dictionaries representing products
products = [{"name": "Laptop", "price": 1000}, {"name": "Mouse", "price": 25}, {"name": "Monitor", "price": 200}]
# Step 2: Sort the products by the 'price' key using a lambda function
sorted_products = sorted(products, key=lambda item: item["price"])
# Step 3: Print the sorted list
print(sorted_products)

# Example 4: Sort words by their last character
# Step 1: Define a list of words
animals = ["zebra", "lion", "bear", "fox"]
# Step 2: Sort using a lambda that returns the last character (index -1)
sorted_animals = sorted(animals, key=lambda word: word[-1])
# Step 3: Print the sorted animals
print(sorted_animals)