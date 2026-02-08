# Storing dimensions as instance variables
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width

# Storing coordinates as instance variables
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y