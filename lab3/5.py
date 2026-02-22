# Базовый класс (Родитель)
class Shape:
    def area(self):
        return 0

# Дочерний класс (Ребенок)
class Square(Shape):
    def __init__(self, length):
        # Сохраняем длину стороны
        self.length = length

    # ПЕРЕОПРЕДЕЛЕНИЕ: заменяем родительский area() своим
    def area(self):
        return self.length ** 2

# Использование
n = int(input())
square = Square(n)
print(square.area())