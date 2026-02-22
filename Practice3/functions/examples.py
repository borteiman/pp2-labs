# Step 1: Define the basic function
def greet_user():
    # Step 2: The action performed by the function
    print("Welcome to the system!")

# Step 3: Call the function
greet_user()

# Step 1: Define function with parameters (name, age)
def display_profile(name, age):
    # Step 2: Use parameters in the output
    print(f"User Profile: {name}, Age: {age}")

# Step 3: Call the function and pass arguments
display_profile("Alice", 28)
display_profile("Bob", 34)

# Step 1: Define a function to calculate the square of a number
def calculate_square(number):
    # Step 2: Return the mathematical result ($number^2$)
    result = number * number
    return result

# Step 3: Store the returned value in variables
square_of_five = calculate_square(5)
square_of_nine = calculate_square(9)

print(f"Square of 5 is: {square_of_five}")
print(f"Square of 9 is: {square_of_nine}")

# Step 1: Define function with a default parameter (status)
def create_task(task_name, status="Pending"):
    # Output the task details
    print(f"Task: '{task_name}' | Status: {status}")

# Step 2: Call without the second argument (uses default)
create_task("Update database")

# Step 3: Call with the second argument (overrides default)
create_task("Write report", "Completed")