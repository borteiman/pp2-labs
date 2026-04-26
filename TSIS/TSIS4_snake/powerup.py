import random
import pygame
from game_object import Point, GameObject
from constants import COLS, ROWS, TILE, POWERUP_LIFETIME, CYAN, BLUE, GREEN, BLACK

POWERUP_TYPES = ["speed", "slow", "shield"]


class PowerUp(GameObject):
    def __init__(self):
        super().__init__([])
        self.kind = random.choice(POWERUP_TYPES)
        self.point = Point(10, 10)
        self.spawn_time = pygame.time.get_ticks()

    def respawn(self, blocked):
        self.kind = random.choice(POWERUP_TYPES)
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
        return pygame.time.get_ticks() - self.spawn_time > POWERUP_LIFETIME

    def draw(self, screen, offset_y=0):
        x = self.point.c * TILE
        y = offset_y + self.point.r * TILE
        rect = pygame.Rect(x, y, TILE, TILE)

        if self.kind == "speed":
            color = CYAN
            label = "B"
        elif self.kind == "slow":
            color = BLUE
            label = "S"
        else:
            color = GREEN
            label = "H"

        pygame.draw.rect(screen, color, rect.inflate(-2, -2), border_radius=5)
        font = pygame.font.SysFont("Verdana", 12)
        text = font.render(label, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
