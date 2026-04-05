import pygame

RADIUS = 25

class Ball:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = RADIUS
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Ignore move if it takes the ball out of bounds
        if new_x - self.radius < 0 or new_x + self.radius > self.screen_width:
            return
        if new_y - self.radius < 0 or new_y + self.radius > self.screen_height:
            return

        self.x = new_x
        self.y = new_y

    def draw(self, surface):
        pygame.draw.circle(surface, (220, 30, 30), (self.x, self.y), self.radius)