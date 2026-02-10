class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

# Чтение входных данных (два целых числа)
try:
    line = input().split()
    if len(line) == 2:
        l, w = map(int, line)
        rect = Rectangle(l, w)
        print(rect.area())
except EOFError:
    pass