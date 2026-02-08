# Step 1: Define a list of numbers
numbers = [1, 2, 3, 4, 5]

# Step 2: Double all numbers in the list using map() and lambda
doubled = list(map(lambda x: x * 2, numbers))

# Step 3: Output the result
print(doubled)


# Example 1: Double all numbers in the list
# Step 1: Define a list of numbers
numbers = [1, 2, 3, 4, 5]
# Step 2: Use map() and lambda to multiply each by 2
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

# Example 2: Convert strings to uppercase
# Step 1: Define a list of words
fruits = ["apple", "banana", "cherry"]
# Step 2: Use map() to apply a lambda that calls .upper() on each string
upper_fruits = list(map(lambda x: x.upper(), fruits))
# Step 3: Print the new list
print(upper_fruits)

# Example 3: Extract the first letter from strings
# Step 1: Define a list of names
names = ["Aisha", "Tamerlan", "Borte"]
# Step 2: Use map() to get the first character of each name using indexing
first_letters = list(map(lambda name: name[0], names))
# Step 3: Print the extracted letters
print(first_letters)