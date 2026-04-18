import pygame
import random
from color_palette import *

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

font = pygame.font.SysFont("Verdana", 24)
big_font = pygame.font.SysFont("Verdana", 48)

BASE_FPS = 5


def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]

    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(
                screen,
                colors[(x + y) % 2],
                (x * CELL, y * CELL, CELL, CELL)
            )


def get_wall_positions():
    walls = set()

    for x in range(COLS):
        walls.add((x, 0))
        walls.add((x, ROWS - 1))

    for y in range(ROWS):
        walls.add((0, y))
        walls.add((COLS - 1, y))

    return walls


WALLS = get_wall_positions()


def draw_walls():
    # these blue cells are borders, if snake touches them game ends
    for x, y in WALLS:
        pygame.draw.rect(screen, colorBLUE, (x * CELL, y * CELL, CELL, CELL))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def __str__(self):
        return f"{self.x}, {self.y}"


class Snake:
    def __init__(self):
        self.body = [Point(10, 10), Point(9, 10), Point(8, 10)]
        self.dx = 1
        self.dy = 0
        self.grow = False

    def set_direction(self, dx, dy):
        # this prevents snake from turning back into itself instantly
        if self.dx == -dx and self.dy == -dy:
            return

        self.dx = dx
        self.dy = dy

    def move(self):
        # make new head in the moving direction
        new_head = Point(self.body[0].x + self.dx, self.body[0].y + self.dy)
        self.body.insert(0, new_head)

        # if food was eaten, keep tail, otherwise remove last part
        if self.grow:
            self.grow = False
        else:
            self.body.pop()

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_food_collision(self, food):
        # if head and food are in same cell, snake eats food
        head = self.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:
            self.grow = True
            return True

        return False

    def check_wall_collision(self):
        # this checks if snake left the area or hit the border wall
        head = self.body[0]

        if head.x < 0 or head.x >= COLS or head.y < 0 or head.y >= ROWS:
            return True

        if (head.x, head.y) in WALLS:
            return True

        return False

    def check_self_collision(self):
        # if head touches body, also game over
        head = self.body[0]

        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True

        return False

    def get_positions(self):
        return {(segment.x, segment.y) for segment in self.body}


class Food:
    def __init__(self, snake):
        self.pos = Point(1, 1)
        self.generate_random_pos(snake)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake):
        # food should appear only in free place, not on snake and not on wall
        snake_positions = snake.get_positions()
        free_cells = []

        for y in range(1, ROWS - 1):
            for x in range(1, COLS - 1):
                if (x, y) not in snake_positions and (x, y) not in WALLS:
                    free_cells.append((x, y))

        if free_cells:
            x, y = random.choice(free_cells)
            self.pos = Point(x, y)


snake = Snake()
food = Food(snake)

# score counts eaten food
score = 0

# level starts from 1
level = 1

# every 4 foods snake goes to next level
foods_per_level = 4

# speed will grow when level grows
current_fps = BASE_FPS

clock = pygame.time.Clock()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RIGHT:
                snake.set_direction(1, 0)
            elif event.key == pygame.K_LEFT:
                snake.set_direction(-1, 0)
            elif event.key == pygame.K_DOWN:
                snake.set_direction(0, 1)
            elif event.key == pygame.K_UP:
                snake.set_direction(0, -1)

    if not game_over:
        snake.move()

        if snake.check_food_collision(food):
            score += 1
            food.generate_random_pos(snake)

            # level changes depending on score
            new_level = score // foods_per_level + 1

            # when level goes up, game becomes faster
            if new_level > level:
                level = new_level
                current_fps = BASE_FPS + (level - 1) * 2

        if snake.check_wall_collision() or snake.check_self_collision():
            game_over = True

    screen.fill(colorBLACK)
    draw_grid_chess()
    draw_walls()

    food.draw()
    snake.draw()

    # show current score
    score_text = font.render(f"Score: {score}", True, colorBLACK)

    # show current level
    level_text = font.render(f"Level: {level}", True, colorBLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    if game_over:
        game_over_text = big_font.render("Game Over", True, colorRED)
        final_text = font.render(f"Final Score: {score}", True, colorBLACK)

        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        final_rect = final_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(final_text, final_rect)

    pygame.display.flip()
    clock.tick(current_fps)

pygame.quit()