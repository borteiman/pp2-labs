import pygame
from game_object import Point, GameObject
from constants import COLS, ROWS


class Snake(GameObject):
    def __init__(self, color):
        start_c = COLS // 2
        start_r = ROWS // 2
        points = [Point(start_c, start_r), Point(start_c - 1, start_r), Point(start_c - 2, start_r)]
        super().__init__(points, color)
        self.dx = 1
        self.dy = 0
        self.next_dx = 1
        self.next_dy = 0

    def head(self):
        return self.points[0]

    def process_input(self, event):
        # Direction changes are saved first and applied on move.
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP and self.dy != 1:
            self.next_dx = 0
            self.next_dy = -1
        elif event.key == pygame.K_DOWN and self.dy != -1:
            self.next_dx = 0
            self.next_dy = 1
        elif event.key == pygame.K_LEFT and self.dx != 1:
            self.next_dx = -1
            self.next_dy = 0
        elif event.key == pygame.K_RIGHT and self.dx != -1:
            self.next_dx = 1
            self.next_dy = 0

    def move(self, grow=False):
        self.dx = self.next_dx
        self.dy = self.next_dy
        new_head = Point(self.head().c + self.dx, self.head().r + self.dy)
        self.points.insert(0, new_head)
        if not grow:
            self.points.pop()

    def grow(self, amount):
        # I add copies of the tail, then normal movement will stretch the snake.
        if len(self.points) == 0:
            return
        tail = self.points[-1]
        for _ in range(amount):
            self.points.append(tail.copy())

    def shrink(self, amount):
        # Poison removes body segments from the tail side.
        for _ in range(amount):
            if len(self.points) > 1:
                self.points.pop()

    def hits_self(self):
        return self.head() in self.points[1:]

    def hits_border(self):
        h = self.head()
        return h.c < 0 or h.c >= COLS or h.r < 0 or h.r >= ROWS
