import math
import pygame

#расчет координат/геометрии/размеров

def calculate_rect(start, end):
    # Makes rectangle normal even if I drag mouse to the left or up.
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)            #выбирает левый верхний угол прямоугольника.
    top = min(y1, y2)
    width = abs(x1 - x2)          #делает ширину и высоту всегда положительными.
    height = abs(y1 - y2)

    return pygame.Rect(left, top, width, height)

#каждая функция получает две точки

#math.hypot(dx, dy) считает расстояние между двумя точками

def calculate_square(start, end):
    # Square is based on one equal side.
    x1, y1 = start
    x2, y2 = end

    side = max(abs(x2 - x1), abs(y2 - y1))


#куда пользователь тянет мышку

    if x2 < x1:
        left = x1 - side
    else:
        left = x1

    if y2 < y1:
        top = y1 - side
    else:
        top = y1

    return pygame.Rect(left, top, side, side)

#возвращаем не просто координаты, а объект pygame.Rect.


def calculate_circle(start, end):
    # Mouse distance from start point becomes radius.
    x1, y1 = start
    x2, y2 = end
    radius = int(math.hypot(x2 - x1, y2 - y1))

    #расстояние между точками

    return start, radius


def calculate_right_triangle(start, end):
    # Right angle is made using start x and end y.
    x1, y1 = start
    x2, y2 = end

    return [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]


def calculate_equilateral_triangle(start, end):
    # I use the mouse distance as side length.
    x1, y1 = start
    x2, y2 = end

    side = int(math.hypot(x2 - x1, y2 - y1))
    height = int(side * math.sqrt(3) / 2)

    if y2 >= y1:
        direction = 1
    else:
        direction = -1

    return [
        (x1, y1),
        (x1 - side // 2, y1 + direction * height),
        (x1 + side // 2, y1 + direction * height)
    ]


def calculate_rhombus(start, end):
    # Rhombus is built from the middle points of rectangle sides.
    rect = calculate_rect(start, end)

    return [
        (rect.centerx, rect.top),
        (rect.right, rect.centery),
        (rect.centerx, rect.bottom),
        (rect.left, rect.centery)
    ]

#строит ромб внутри прямоугольной области
#готовая функция для невидимой фигуры как основы