import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"({self.x}, {self.y})")

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other_point):
        return math.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)

# Чтение данных
x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
x3, y3 = map(int, input().split())

# Логика программы
p1 = Point(x1, y1)
p1.show()

p1.move(x2, y2)
p1.show()

p2 = Point(x3, y3)
distance = p1.dist(p2)
print(f"{distance:.2f}")