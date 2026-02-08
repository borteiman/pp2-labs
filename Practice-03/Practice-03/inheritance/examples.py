# Step 1: Define the base class
class Animal:
    def eat(self):
        # Base method for eating
        print("This animal is eating.")

# Step 2: Define the derived class
class Dog(Animal):
    def bark(self):
        # Derived method specific to Dog
        print("The dog is barking.")

# Step 3: Create an object and use methods
my_dog = Dog()
my_dog.eat()  # Inherited from Animal
my_dog.bark() # Defined in Dog

# Step 1: Define the base class
class Vehicle:
    def start(self):
        # Base method to start the vehicle
        print("Vehicle started.")

# Step 2: Define the intermediate derived class
class Car(Vehicle):
    def drive(self):
        # Intermediate method to drive
        print("Car is driving.")

# Step 3: Define the final derived class
class ElectricCar(Car):
    def charge(self):
        # Final method to charge the battery
        print("Electric car is charging.")

my_tesla = ElectricCar()
my_tesla.start()  # Inherited from Vehicle
my_tesla.drive()  # Inherited from Car
my_tesla.charge() # Defined in ElectricCar

# Step 1: Define the base class
class Shape:
    def draw(self):
        # Common method for all shapes
        print("Drawing a shape.")

# Step 2: Define the first derived class
class Circle(Shape):
    def calculate_area(self):
        # Specific method for Circle
        print("Calculating circle area.")

# Step 3: Define the second derived class
class Square(Shape):
    def calculate_perimeter(self):
        # Specific method for Square
        print("Calculating square perimeter.")

my_circle = Circle()
my_circle.draw() # Inherited from Shape

my_square = Square()
my_square.draw() # Inherited from Shape

# Step 1: Define the first base class
class Flyable:
    def fly(self):
        # Method for flying capability
        print("Flying in the sky.")

# Step 2: Define the second base class
class Swimmable:
    def swim(self):
        # Method for swimming capability
        print("Swimming in the water.")

# Step 3: Define the derived class inheriting from both
class Duck(Flyable, Swimmable):
    def quack(self):
        # Method specific to Duck
        print("Duck is quacking.")

my_duck = Duck()
my_duck.fly()   # Inherited from Flyable
my_duck.swim()  # Inherited from Swimmable
my_duck.quack() # Defined in Duck