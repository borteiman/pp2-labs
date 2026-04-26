import pygame
from constants import TILE


class Point:
    def __init__(self, c, r):
        self.c = c
        self.r = r

    def copy(self):
        return Point(self.c, self.r)

    def __eq__(self, other):
        return isinstance(other, Point) and self.c == other.c and self.r == other.r

    def __hash__(self):
        return hash((self.c, self.r))


class GameObject:
    def __init__(self, points=None, color=(255, 255, 255)):
        self.points = points if points is not None else []
        self.color = color

    def draw_cell(self, screen, point, color=None, offset_y=0):
        use_color = color if color is not None else self.color
        rect = pygame.Rect(point.c * TILE, offset_y + point.r * TILE, TILE, TILE)
        pygame.draw.rect(screen, use_color, rect, border_radius=4)

    def draw(self, screen, offset_y=0):
        for point in self.points:
            self.draw_cell(screen, point, self.color, offset_y)
