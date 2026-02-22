# Step 1: Define a simple class named 'Robot'
class Robot:
    # Step 2: Use 'pass' to define an empty body temporarily
    pass

# Step 3: Create an instance of the Robot class
my_robot = Robot()

# Print the object to see its memory location and type
print(my_robot)

# Step 1: Define the class and the __init__ method
class User:
    def __init__(self, username, role):
        # Step 2: Assign arguments to instance variables using 'self'
        self.username = username
        self.role = role

# Step 3: Create an object with specific initial values
admin_user = User("alice_admin", "Administrator")

print(f"User created: {admin_user.username} | Role: {admin_user.role}")

# Step 1: Define a class with a method
class Calculator:
    def add_numbers(self, a, b):
        # Step 2: 'self' is required, though we only use 'a' and 'b' here
        return a + b
        
    def greet(self):
        print("Calculator is ready to compute!")

# Step 3: Create an object and call its methods
my_calc = Calculator()
my_calc.greet()

result = my_calc.add_numbers(15, 5)
print(f"The result is: {result}")

# Step 1: Define a class variable
class Employee:
    # This variable is shared among ALL instances of Employee
    company_name = "Tech Corp"

    def __init__(self, name):
        # This is an instance variable, unique to EACH object
        self.name = name

# Step 2: Access the class variable via the class
print(f"Company: {Employee.company_name}")

# Step 3: Create objects and access variables
emp1 = Employee("John")
emp2 = Employee("Sarah")

print(f"{emp1.name} works at {emp1.company_name}")
print(f"{emp2.name} works at {emp2.company_name}")