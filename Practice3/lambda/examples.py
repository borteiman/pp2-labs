# Step 1: Define a list of dictionaries representing people
people = [
    {"name": "Aisha", "age": 19}, 
    {"name": "Tama", "age": 20}, 
    {"name": "Borte", "age": 17}
]

# Step 2: Find the oldest person using max() and a lambda for the 'key' argument
oldest_person = max(people, key=lambda person: person["age"])

# Step 3: Print the result
print(f"The oldest person is: {oldest_person['name']}")

# Step 1: Create a dictionary where values are lambda functions
calculator = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b
}

# Step 2: Call the specific lambda function directly from the dictionary key
result_add = calculator["add"](10, 5)
result_multiply = calculator["multiply"](10, 5)

# Step 3: Print the results
print(f"Addition: {result_add}")
print(f"Multiplication: {result_multiply}")

# Step 1: Define a lambda that checks a condition using a single line if-else
check_number = lambda x: "Positive" if x > 0 else "Negative or Zero"

# Step 2: Call the lambda function with different values
result_1 = check_number(15)
result_2 = check_number(-5)

# Step 3: Print the results
print(f"15 is {result_1}")
print(f"-5 is {result_2}")

# Step 1: Import reduce from the functools module
from functools import reduce

# Step 2: Define a list of numbers
numbers = [1, 2, 3, 4, 5]

# Step 3: Use reduce and lambda to multiply all elements together sequentially
product = reduce(lambda x, y: x * y, numbers)

# Step 4: Print the final product
print(f"The total product of all numbers is: {product}")