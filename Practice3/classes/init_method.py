# Initializing a subclass with specific parameters
class Square(Shape):
    def __init__(self, length):
        self.length = length
    
    def area(self):
        return self.length ** 2

# Initializing owner and balance data
class owner:
    def __init__(self, name):
        self.name = name

class Balance:
    def __init__(self, total = 0):
        self.total = total