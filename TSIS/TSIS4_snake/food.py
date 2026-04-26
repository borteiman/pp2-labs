import random
import pygame
from game_object import Point, GameObject
from constants import COLS, ROWS, TILE, FOOD_LIFETIME, POISON_LIFETIME, DARK_RED, YELLOW, ORANGE, PURPLE


class Food(GameObject):
    def __init__(self, poison=False):
        super().__init__([])
        self.poison = poison
        self.weight = 1
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = POISON_LIFETIME if poison else FOOD_LIFETIME
        self.point = Point(5, 5)
        self.color = YELLOW

    def choose_weight(self):
        # Weighted food from Practice 11.
        self.weight = random.choice([1, 1, 1, 2, 2, 3])
        if self.weight == 1:
            self.color = YELLOW
        elif self.weight == 2:
            self.color = ORANGE
        else:
            self.color = PURPLE

    def respawn(self, blocked):
        if self.poison:
            self.color = DARK_RED
            self.weight = -2
        else:
            self.choose_weight()

        free = []
        for c in range(COLS):
            for r in range(ROWS):
                p = Point(c, r)
                if p not in blocked:
                    free.append(p)

        if len(free) > 0:
            self.point = random.choice(free)

        self.spawn_time = pygame.time.get_ticks()

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def draw(self, screen, offset_y=0):
        x = self.point.c * TILE
        y = offset_y + self.point.r * TILE
        rect = pygame.Rect(x, y, TILE, TILE)

        if self.poison:
            pygame.draw.rect(screen, self.color, rect, border_radius=5)
            pygame.draw.line(screen, (240, 240, 240), (x + 5, y + 5), (x + TILE - 5, y + TILE - 5), 3)
            pygame.draw.line(screen, (240, 240, 240), (x + TILE - 5, y + 5), (x + 5, y + TILE - 5), 3)
        else:
            pygame.draw.ellipse(screen, self.color, rect.inflate(-2, -2))
            font = pygame.font.SysFont("Verdana", 12)
            text = font.render(str(self.weight), True, (20, 20, 20))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
