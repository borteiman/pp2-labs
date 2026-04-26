import random
import pygame

from constants import (
    WIDTH,
    HEIGHT,
    HUD_HEIGHT,
    TILE,
    COLS,
    ROWS,
    BG_COLOR,
    GRID_COLOR,
    WHITE,
    BLACK,
    CYAN,
    MOVE_DELAY_START,
    MOVE_DELAY_MIN,
    POWERUP_DURATION,
    FOODS_PER_LEVEL,
)
from snake import Snake
from food import Food
from powerup import PowerUp
from wall import WallManager
from sound_manager import SoundManager


class SnakeGame:
    def __init__(self, username, personal_best, settings):
        self.username = username
        self.personal_best = personal_best
        self.settings = settings

        self.snake = Snake(tuple(settings["snake_color"]))
        self.wall = WallManager()

        self.food = Food(poison=False)
        self.poison = Food(poison=True)
        self.powerup = None

        self.sound = SoundManager(settings.get("sound", True))

        self.score = 0
        self.level = 1
        self.foods_eaten = 0

        self.move_delay = MOVE_DELAY_START
        self.last_move_time = pygame.time.get_ticks()

        self.active_power = None
        self.active_power_end = 0
        self.shield = False

        self.next_powerup_time = pygame.time.get_ticks() + random.randint(4000, 7000)

        self.game_over = False
        self.status = "Game Over"

        self.prepare_level()

    def blocked_points(self):
        blocked = set(self.snake.points)
        blocked.update(self.wall.points)

        return blocked

    def prepare_level(self):
        # Every new level refreshes obstacles and respawns food safely.
        blocked = set(self.snake.points)
        self.wall.generate_obstacles(self.level, self.snake.points, blocked)

        blocked = self.blocked_points()
        self.food.respawn(blocked)

        blocked = self.blocked_points()
        blocked.add(self.food.point)
        self.poison.respawn(blocked)

        self.powerup = None
        self.next_powerup_time = pygame.time.get_ticks() + random.randint(3500, 6500)

    def process_event(self, event):
        self.snake.process_input(event)

    def current_delay(self):
        delay = self.move_delay

        if self.active_power == "speed":
            delay = max(MOVE_DELAY_MIN, delay - 35)

        elif self.active_power == "slow":
            delay = delay + 60

        return delay

    def update_power_effects(self):
        now = pygame.time.get_ticks()

        if self.active_power in ["speed", "slow"] and now >= self.active_power_end:
            self.active_power = None

    def maybe_spawn_powerup(self):
        # Only one power-up can be active on the field at a time.
        # Also, I do not spawn a new one while speed/slow/shield is already active.
        now = pygame.time.get_ticks()

        if self.active_power is not None:
            return

        if self.powerup is not None:
            if self.powerup.expired():
                self.powerup = None
                self.next_powerup_time = now + random.randint(4000, 8000)

            return

        if now >= self.next_powerup_time:
            p = PowerUp()

            blocked = self.blocked_points()
            blocked.add(self.food.point)
            blocked.add(self.poison.point)

            p.respawn(blocked)
            self.powerup = p
            self.next_powerup_time = now + random.randint(6000, 10000)

    def activate_powerup(self, powerup):
        # Collected power-up effect. Speed and slow have 5 second duration.
        now = pygame.time.get_ticks()

        if powerup.kind == "speed":
            self.active_power = "speed"
            self.active_power_end = now + POWERUP_DURATION

        elif powerup.kind == "slow":
            self.active_power = "slow"
            self.active_power_end = now + POWERUP_DURATION

        elif powerup.kind == "shield":
            self.active_power = "shield"
            self.shield = True

        self.next_powerup_time = now + random.randint(6000, 10000)
        self.sound.play("power")

    def handle_collision(self, previous_points):
        # Shield protects from one wall/self/obstacle collision.
        # I restore the snake to its previous position, so it does not stay inside the wall.
        if self.shield:
            self.shield = False
            self.active_power = None
            self.snake.points = previous_points
            return

        self.game_over = True
        self.status = "Game Over"
        self.sound.play("crash")

    def check_collisions(self, previous_points):
        head = self.snake.head()

        if self.snake.hits_border():
            self.handle_collision(previous_points)
            return

        if self.snake.hits_self():
            self.handle_collision(previous_points)
            return

        if self.wall.hits(head):
            self.handle_collision(previous_points)
            return

    def eat_items_if_needed(self):
        head = self.snake.head()

        if head == self.food.point:
            self.score += self.food.weight * 10
            self.snake.grow(self.food.weight)
            self.foods_eaten += 1
            self.sound.play("eat")

            if self.foods_eaten % FOODS_PER_LEVEL == 0:
                self.level += 1
                self.move_delay = max(MOVE_DELAY_MIN, self.move_delay - 10)
                self.prepare_level()

            else:
                blocked = self.blocked_points()
                blocked.add(self.poison.point)

                if self.powerup is not None:
                    blocked.add(self.powerup.point)

                self.food.respawn(blocked)

        if head == self.poison.point:
            self.score = max(0, self.score - 15)
            self.snake.shrink(2)
            self.sound.play("crash")

            if len(self.snake.points) <= 1:
                self.game_over = True
                self.status = "Snake became too short"
                return

            blocked = self.blocked_points()
            blocked.add(self.food.point)

            if self.powerup is not None:
                blocked.add(self.powerup.point)

            self.poison.respawn(blocked)

        if self.powerup is not None and head == self.powerup.point:
            self.activate_powerup(self.powerup)
            self.powerup = None

    def update_food_timers(self):
        if self.food.expired():
            blocked = self.blocked_points()
            blocked.add(self.poison.point)

            if self.powerup is not None:
                blocked.add(self.powerup.point)

            self.food.respawn(blocked)

        if self.poison.expired():
            blocked = self.blocked_points()
            blocked.add(self.food.point)

            if self.powerup is not None:
                blocked.add(self.powerup.point)

            self.poison.respawn(blocked)

    def update(self):
        if self.game_over:
            return

        self.update_power_effects()
        self.update_food_timers()
        self.maybe_spawn_powerup()

        now = pygame.time.get_ticks()

        if now - self.last_move_time < self.current_delay():
            return

        self.last_move_time = now

        previous_points = [point.copy() for point in self.snake.points]

        self.snake.move(grow=False)
        self.check_collisions(previous_points)

        if not self.game_over:
            self.eat_items_if_needed()

    def draw_grid(self, screen):
        for c in range(COLS + 1):
            x = c * TILE
            pygame.draw.line(screen, GRID_COLOR, (x, HUD_HEIGHT), (x, HEIGHT))

        for r in range(ROWS + 1):
            y = HUD_HEIGHT + r * TILE
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

    def draw_hud(self, screen, font):
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HUD_HEIGHT))

        lines = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best: {self.personal_best}",
        ]

        x = 12

        for line in lines:
            text = font.render(line, True, WHITE)
            screen.blit(text, (x, 12))
            x += text.get_width() + 22

        if self.active_power == "speed":
            left = max(0, (self.active_power_end - pygame.time.get_ticks()) // 1000)
            power = f"Power: Speed {left}s"

        elif self.active_power == "slow":
            left = max(0, (self.active_power_end - pygame.time.get_ticks()) // 1000)
            power = f"Power: Slow {left}s"

        elif self.active_power == "shield":
            power = "Power: Shield"

        else:
            power = "Power: None"

        text = font.render(power, True, CYAN)
        screen.blit(text, (12, 46))

    def draw(self, screen, font):
        screen.fill(BG_COLOR)

        self.draw_hud(screen, font)

        if self.settings.get("grid", True):
            self.draw_grid(screen)

        self.wall.draw(screen, HUD_HEIGHT)
        self.food.draw(screen, HUD_HEIGHT)
        self.poison.draw(screen, HUD_HEIGHT)

        if self.powerup is not None:
            self.powerup.draw(screen, HUD_HEIGHT)

        self.snake.draw(screen, HUD_HEIGHT)

    def result(self):
        return {
            "username": self.username,
            "score": self.score,
            "level": self.level,
            "status": self.status,
            "personal_best": max(self.personal_best, self.score),
        }
