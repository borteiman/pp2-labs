class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self, length, width):
        # У прямоугольника уже две стороны
        self.length = length
        self.width = width

    # Снова переопределяем метод под свою формулу
    def area(self):
        return self.length * self.width

# Чтение данных с обработкой ошибок
try:
    line = input().split()
    if len(line) == 2:
        # map превращает строки в числа
        l, w = map(int, line)
        rect = Rectangle(l, w)
        print(rect.area())
except EOFError:
    pass