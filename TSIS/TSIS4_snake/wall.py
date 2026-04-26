import random
import pygame
from game_object import Point, GameObject
from constants import COLS, ROWS, TILE, DARK_GRAY, GRAY


class WallManager(GameObject):
    def __init__(self):
        super().__init__([], DARK_GRAY)
        self.level = 1

    def clear(self):
        self.points = []

    def generate_obstacles(self, level, snake_points, blocked):
        # Obstacles start from level 3.
        # I avoid the snake head area, so the player is not trapped immediately.
        self.level = level
        if level < 3:
            self.points = []
            return

        head = snake_points[0]
        obstacle_count = min(6 + level * 2, 28)
        new_points = []
        attempts = 0

        while len(new_points) < obstacle_count and attempts < 500:
            attempts += 1
            p = Point(random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
            near_head = abs(p.c - head.c) + abs(p.r - head.r) <= 4
            if near_head:
                continue
            if p in blocked or p in new_points:
                continue

            around_head = [Point(head.c + 1, head.r), Point(head.c - 1, head.r), Point(head.c, head.r + 1), Point(head.c, head.r - 1)]
            if p in around_head:
                continue
            new_points.append(p)

        self.points = new_points

    def hits(self, point):
        return point in self.points

    def draw(self, screen, offset_y=0):
        for point in self.points:
            rect = pygame.Rect(point.c * TILE, offset_y + point.r * TILE, TILE, TILE)
            pygame.draw.rect(screen, DARK_GRAY, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)
