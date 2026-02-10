class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        pi = 3.14159
        return pi * (self.radius ** 2)

r = int(input())
c = Circle(r)
print(f"{c.area():.2f}")