import math # Нужен для функции sqrt (корень)

class Point:
    def __init__(self, x, y):
        # При создании "запоминаем" координаты
        self.x = x
        self.y = y

    def show(self):
        # Просто красиво выводим точку в скобочках
        print(f"({self.x}, {self.y})")

    def move(self, new_x, new_y):
        # Обновляем координаты — точка "переехала"
        self.x = new_x
        self.y = new_y

    def dist(self, other_point):
        # Вычисляем расстояние по формуле Евклида:
        # корень из суммы квадратов разностей координат
        return math.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)