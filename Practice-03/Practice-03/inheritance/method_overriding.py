class Animal:
    def make_sound(self):
        # Default behavior for any animal
        print("Some generic animal sound")

class Dog(Animal):
    # Overriding the parent's make_sound method
    def make_sound(self):
        print("Woof! Woof!")

dog = Dog()
dog.make_sound() # Outputs: Woof! Woof!

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"Employee: {self.name}, Salary: ${self.salary}"

class Developer(Employee):
    def __init__(self, name, salary, programming_language):
        # Call the parent's __init__ to handle name and salary
        super().__init__(name, salary)
        self.programming_language = programming_language

    def get_details(self):
        # Get the original string and add new specific information
        base_details = super().get_details()
        return f"{base_details}, Language: {self.programming_language}"

dev = Developer("Aisha", 5000, "Python")
print(dev.get_details())

class Device:
    def turn_on(self):
        print("Device is now turning on.")

class Phone(Device):
    def turn_on(self):
        print("Phone screen is lighting up.")

class SmartPhone(Phone):
    def turn_on(self):
        # Overrides Phone's turn_on, but we can still call it if needed
        super().turn_on()
        print("Loading operating system and apps...")

my_phone = SmartPhone()
my_phone.turn_on()