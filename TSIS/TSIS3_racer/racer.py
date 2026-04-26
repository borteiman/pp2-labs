from pathlib import Path
import random
import pygame

WIDTH, HEIGHT = 500, 700

ROAD_LEFT = 50
ROAD_RIGHT = 450
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

LANE_COUNT = 4
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT
LANE_CENTERS = [ROAD_LEFT + LANE_WIDTH // 2 + i * LANE_WIDTH for i in range(LANE_COUNT)]

FINISH_DISTANCE = 3000

ASSETS_DIR = Path(__file__).parent / "assets"

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
ROAD_GRAY = (55, 55, 55)
DARK_GRAY = (35, 35, 35)

YELLOW = (250, 210, 90)
RED = (210, 70, 70)
BLUE = (70, 130, 190)
GREEN = (80, 170, 110)
ORANGE = (240, 140, 60)
PURPLE = (160, 95, 220)
CYAN = (70, 210, 220)

CAR_FILES = {
    "blue": "player_blue.png",
    "red": "player_red.png",
    "green": "player_green.png",
}

DIFFICULTY_DATA = {
    "easy": {
        "start_speed": 230,
        "traffic_time": 1.35,
        "obstacle_time": 1.70,
        "coin_time": 1.20,
        "power_time": 6.00,
    },
    "normal": {
        "start_speed": 270,
        "traffic_time": 1.10,
        "obstacle_time": 1.45,
        "coin_time": 1.15,
        "power_time": 5.50,
    },
    "hard": {
        "start_speed": 315,
        "traffic_time": 0.90,
        "obstacle_time": 1.20,
        "coin_time": 1.05,
        "power_time": 5.00,
    },
}


def load_player_car(color_name):
    # Player car is loaded from assets.
    # I use different image files for different colors from settings.
    filename = CAR_FILES.get(color_name, "player_blue.png")
    path = ASSETS_DIR / filename

    image = pygame.image.load(path).convert_alpha()

    # All player cars should have the same size in game.
    image = pygame.transform.smoothscale(image, (46, 72))

    return image


def make_traffic_car_surface(color, w=44, h=70):
    # Traffic cars are still drawn in pygame.
    # Only player car uses prepared images.
    surface = pygame.Surface((w, h), pygame.SRCALPHA)

    pygame.draw.rect(surface, color, (6, 12, w - 12, h - 18), border_radius=8)
    pygame.draw.rect(surface, (230, 240, 250), (13, 20, w - 26, 18), border_radius=4)

    pygame.draw.rect(surface, BLACK, (5, 20, 6, 16), border_radius=3)
    pygame.draw.rect(surface, BLACK, (w - 11, 20, 6, 16), border_radius=3)
    pygame.draw.rect(surface, BLACK, (5, h - 25, 6, 18), border_radius=3)
    pygame.draw.rect(surface, BLACK, (w - 11, h - 25, 6, 18), border_radius=3)

    return surface


def make_circle_surface(radius, outer_color, inner_color, text=None):
    # I use this function for coins and power-ups.
    size = radius * 2 + 6
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    pygame.draw.circle(surface, outer_color, (size // 2, size // 2), radius)
    pygame.draw.circle(surface, inner_color, (size // 2, size // 2), max(1, radius - 5))
    pygame.draw.circle(surface, BLACK, (size // 2, size // 2), radius, 2)

    if text is not None:
        font = pygame.font.SysFont("Verdana", 13)
        label = font.render(str(text), True, BLACK)
        label_rect = label.get_rect(center=(size // 2, size // 2))
        surface.blit(label, label_rect)

    return surface


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()

        self.image = load_player_car(color_name)
        self.rect = self.image.get_rect()

        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20

        self.speed = 320

    def update(self, dt):
        keys = pygame.key.get_pressed()

        dx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed * dt

        self.rect.x += int(dx)

        # Player cannot leave the road.
        if self.rect.left < ROAD_LEFT + 5:
            self.rect.left = ROAD_LEFT + 5

        if self.rect.right > ROAD_RIGHT - 5:
            self.rect.right = ROAD_RIGHT - 5


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        color = random.choice([RED, ORANGE, PURPLE, CYAN])
        self.image = make_traffic_car_surface(color)

        self.rect = self.image.get_rect()
        self.speed = speed

        self.place_at_top()

    def place_at_top(self):
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.bottom = random.randint(-250, -80)

    def update(self, dt):
        self.rect.y += int(self.speed * dt)

        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.speed = speed
        self.value = random.choice([1, 1, 1, 2, 2, 3])

        if self.value == 1:
            self.image = make_circle_surface(11, (255, 215, 0), (255, 240, 120), self.value)

        elif self.value == 2:
            self.image = make_circle_surface(14, ORANGE, (255, 210, 120), self.value)

        else:
            self.image = make_circle_surface(17, PURPLE, (220, 180, 255), self.value)

        self.rect = self.image.get_rect()
        self.place_at_top()

    def place_at_top(self):
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.bottom = random.randint(-350, -60)

    def update(self, dt):
        self.rect.y += int(self.speed * dt)

        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed, kind=None):
        super().__init__()

        self.kind = kind or random.choice(["barrier", "oil", "pothole"])
        self.speed = speed

        self.moving = False
        self.move_dir = random.choice([-1, 1])

        if self.kind == "barrier":
            self.image = pygame.Surface((70, 28), pygame.SRCALPHA)
            pygame.draw.rect(self.image, RED, (0, 0, 70, 28), border_radius=5)
            pygame.draw.rect(self.image, WHITE, (8, 7, 16, 6))
            pygame.draw.rect(self.image, WHITE, (35, 7, 16, 6))

        elif self.kind == "oil":
            self.image = pygame.Surface((58, 34), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, BLACK, (0, 3, 58, 28))
            pygame.draw.ellipse(self.image, (70, 70, 110), (14, 9, 25, 12))

        else:
            self.image = pygame.Surface((52, 34), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, DARK_GRAY, (0, 0, 52, 34))
            pygame.draw.ellipse(self.image, BLACK, (10, 7, 28, 18))

        self.rect = self.image.get_rect()
        self.place_at_top()

    def place_at_top(self):
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.bottom = random.randint(-420, -80)

    def update(self, dt):
        self.rect.y += int(self.speed * dt)

        # Dynamic road event: moving barrier.
        if self.moving:
            self.rect.x += int(self.move_dir * 90 * dt)

            if self.rect.left < ROAD_LEFT + 5 or self.rect.right > ROAD_RIGHT - 5:
                self.move_dir *= -1

        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.kind = random.choice(["nitro", "shield", "repair"])
        self.speed = speed

        # Power-ups disappear after timeout if not collected.
        self.life_time = 5.0

        if self.kind == "nitro":
            self.image = make_circle_surface(16, CYAN, (180, 250, 255), "N")

        elif self.kind == "shield":
            self.image = make_circle_surface(16, BLUE, (180, 210, 255), "S")

        else:
            self.image = make_circle_surface(16, GREEN, (190, 255, 205), "R")

        self.rect = self.image.get_rect()
        self.place_at_top()

    def place_at_top(self):
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.bottom = random.randint(-500, -120)

    def update(self, dt):
        self.life_time -= dt
        self.rect.y += int(self.speed * dt)

        if self.life_time <= 0 or self.rect.top > HEIGHT:
            self.kill()


class NitroStrip(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.speed = speed

        self.image = pygame.Surface((90, 26), pygame.SRCALPHA)
        pygame.draw.rect(self.image, CYAN, (0, 0, 90, 26), border_radius=5)

        pygame.draw.rect(self.image, WHITE, (8, 8, 15, 10))
        pygame.draw.rect(self.image, WHITE, (34, 8, 15, 10))
        pygame.draw.rect(self.image, WHITE, (60, 8, 15, 10))

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANE_CENTERS)
        self.rect.bottom = random.randint(-450, -80)

    def update(self, dt):
        self.rect.y += int(self.speed * dt)

        if self.rect.top > HEIGHT:
            self.kill()


class RacerGame:
    def __init__(self, settings, username):
        self.settings = settings
        self.username = username

        difficulty_name = settings.get("difficulty", "normal")
        self.difficulty = DIFFICULTY_DATA.get(difficulty_name, DIFFICULTY_DATA["normal"])

        self.base_speed = self.difficulty["start_speed"]
        self.road_speed = self.base_speed

        self.player = Player(settings.get("car_color", "blue"))

        self.all_sprites = pygame.sprite.Group()
        self.traffic_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()
        self.event_group = pygame.sprite.Group()

        self.all_sprites.add(self.player)

        self.coins = 0
        self.coin_points = 0
        self.score = 0
        self.power_bonus = 0

        self.distance = 0
        self.remaining_distance = FINISH_DISTANCE

        self.active_power = None
        self.power_timer = 0
        self.has_shield = False

        self.finished = False
        self.status = "Crashed"

        self.traffic_timer = 0
        self.obstacle_timer = 0
        self.coin_timer = 0
        self.power_timer_spawn = 0
        self.event_timer = 3.0

        self.spawn_traffic()
        self.spawn_coin()

    def current_speed(self):
        speed = self.road_speed

        if self.active_power == "nitro":
            speed *= 1.45

        return speed

    def scale_difficulty(self):
        # As the player drives farther, the game becomes harder.
        progress = self.distance / FINISH_DISTANCE
        scale = 1 + progress * 0.8

        self.road_speed = self.base_speed + progress * 130 + self.coin_points * 2

        return scale

    def safe_spawn_x(self):
        # Objects should not spawn directly above the player.
        possible_lanes = LANE_CENTERS.copy()

        for lane in LANE_CENTERS:
            if abs(lane - self.player.rect.centerx) < 55 and len(possible_lanes) > 1:
                possible_lanes.remove(lane)

        return random.choice(possible_lanes)

    def not_overlapping_top(self, new_rect):
        # This prevents new traffic/obstacles from spawning on top of each other.
        groups = [
            self.traffic_group,
            self.coin_group,
            self.obstacle_group,
            self.powerup_group,
            self.event_group,
        ]

        for group in groups:
            for sprite in group:
                if new_rect.colliderect(sprite.rect.inflate(20, 60)):
                    return False

        return True

    def spawn_traffic(self):
        car = TrafficCar(self.current_speed() + 70)
        car.rect.centerx = self.safe_spawn_x()

        if self.not_overlapping_top(car.rect):
            self.traffic_group.add(car)
            self.all_sprites.add(car)

    def spawn_coin(self):
        coin = Coin(self.current_speed())
        coin.rect.centerx = self.safe_spawn_x()

        if self.not_overlapping_top(coin.rect):
            self.coin_group.add(coin)
            self.all_sprites.add(coin)

    def spawn_obstacle(self):
        obstacle = Obstacle(self.current_speed())
        obstacle.rect.centerx = self.safe_spawn_x()

        if self.not_overlapping_top(obstacle.rect):
            self.obstacle_group.add(obstacle)
            self.all_sprites.add(obstacle)

    def spawn_powerup(self):
        power = PowerUp(self.current_speed())
        power.rect.centerx = self.safe_spawn_x()

        if self.not_overlapping_top(power.rect):
            self.powerup_group.add(power)
            self.all_sprites.add(power)

    def spawn_road_event(self):
        # Road event can be a moving barrier or a nitro strip.
        if random.random() < 0.55:
            event = Obstacle(self.current_speed(), "barrier")
            event.moving = True
        else:
            event = NitroStrip(self.current_speed())

        event.rect.centerx = self.safe_spawn_x()

        if self.not_overlapping_top(event.rect):
            self.event_group.add(event)
            self.all_sprites.add(event)

    def activate_powerup(self, power):
        # Only one active power-up can work at a time.
        if self.active_power is not None and power.kind != "repair":
            return

        if power.kind == "nitro":
            self.active_power = "nitro"
            self.power_timer = 4.0
            self.power_bonus += 50

        elif power.kind == "shield":
            self.active_power = "shield"
            self.has_shield = True
            self.power_timer = 0
            self.power_bonus += 35

        elif power.kind == "repair":
            # Repair is instant. It removes the nearest obstacle.
            nearest = None
            nearest_y = -10000

            for obstacle in self.obstacle_group:
                if obstacle.rect.y > nearest_y:
                    nearest_y = obstacle.rect.y
                    nearest = obstacle

            if nearest:
                nearest.kill()

            self.power_bonus += 25

    def handle_danger_collision(self, sprite):
        # Shield protects from one collision.
        if self.has_shield:
            self.has_shield = False
            self.active_power = None
            sprite.kill()
            return

        self.finished = True
        self.status = "Crashed"

    def update(self, dt):
        if self.finished:
            return

        scale = self.scale_difficulty()
        speed = self.current_speed()

        self.distance += speed * dt / 10
        self.remaining_distance = max(0, FINISH_DISTANCE - int(self.distance))

        if self.distance >= FINISH_DISTANCE:
            self.finished = True
            self.status = "Finished"
            return

        self.traffic_timer += dt
        self.obstacle_timer += dt
        self.coin_timer += dt
        self.power_timer_spawn += dt
        self.event_timer += dt

        traffic_interval = max(0.45, self.difficulty["traffic_time"] / scale)
        obstacle_interval = max(0.55, self.difficulty["obstacle_time"] / scale)
        coin_interval = max(0.70, self.difficulty["coin_time"])
        power_interval = max(3.50, self.difficulty["power_time"] / scale)

        if self.traffic_timer >= traffic_interval:
            self.spawn_traffic()
            self.traffic_timer = 0

        if self.obstacle_timer >= obstacle_interval:
            self.spawn_obstacle()
            self.obstacle_timer = 0

        if self.coin_timer >= coin_interval:
            self.spawn_coin()
            self.coin_timer = 0

        if self.power_timer_spawn >= power_interval:
            self.spawn_powerup()
            self.power_timer_spawn = 0

        if self.event_timer >= 5.0:
            self.spawn_road_event()
            self.event_timer = 0

        self.player.update(dt)

        for group in [
            self.traffic_group,
            self.coin_group,
            self.obstacle_group,
            self.powerup_group,
            self.event_group,
        ]:
            for sprite in group:
                if isinstance(sprite, TrafficCar):
                    sprite.speed = self.current_speed() + 70
                else:
                    sprite.speed = self.current_speed()

                sprite.update(dt)

        if self.active_power == "nitro":
            self.power_timer -= dt

            if self.power_timer <= 0:
                self.active_power = None
                self.power_timer = 0

        collected_coins = pygame.sprite.spritecollide(self.player, self.coin_group, True)

        for coin in collected_coins:
            self.coins += 1
            self.coin_points += coin.value

        collected_powers = pygame.sprite.spritecollide(self.player, self.powerup_group, True)

        for power in collected_powers:
            self.activate_powerup(power)

        nitro_hits = pygame.sprite.spritecollide(self.player, self.event_group, False)

        for event in nitro_hits:
            if isinstance(event, NitroStrip):
                if self.active_power is None:
                    self.active_power = "nitro"
                    self.power_timer = 3.0
                    self.power_bonus += 30

                event.kill()

            elif isinstance(event, Obstacle):
                self.handle_danger_collision(event)

        hit_traffic = pygame.sprite.spritecollide(self.player, self.traffic_group, False)

        for car in hit_traffic:
            self.handle_danger_collision(car)

        hit_obstacles = pygame.sprite.spritecollide(self.player, self.obstacle_group, False)

        for obstacle in hit_obstacles:
            if obstacle.kind == "oil":
                self.player.speed = 190
                obstacle.kill()

            else:
                self.handle_danger_collision(obstacle)

        if self.player.speed < 320:
            self.player.speed += int(80 * dt)

        self.score = int(self.coin_points * 10 + self.distance + self.power_bonus)

    def draw_road(self, screen):
        screen.fill((30, 125, 70))

        pygame.draw.rect(screen, ROAD_GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

        pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
        pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

        # Moving lane marks create scrolling road effect.
        offset = int((self.distance * 4) % 80)

        for lane_index in range(1, LANE_COUNT):
            x = ROAD_LEFT + lane_index * LANE_WIDTH

            for y in range(-80 + offset, HEIGHT, 80):
                pygame.draw.rect(screen, YELLOW, (x - 3, y, 6, 40))

    def draw_hud(self, screen, font):
        info = [
            f"Score: {self.score}",
            f"Coins: {self.coin_points}",
            f"Distance: {int(self.distance)} m",
            f"Left: {self.remaining_distance} m",
        ]

        y = 10

        for line in info:
            text = font.render(line, True, WHITE)
            screen.blit(text, (12, y))
            y += 24

        if self.active_power == "nitro":
            power_text = f"Power: Nitro {self.power_timer:.1f}s"

        elif self.active_power == "shield":
            power_text = "Power: Shield"

        else:
            power_text = "Power: None"

        text = font.render(power_text, True, CYAN)
        screen.blit(text, (12, y + 4))

        difficulty = self.settings.get("difficulty", "normal").capitalize()
        diff_text = font.render(f"Difficulty: {difficulty}", True, WHITE)
        screen.blit(diff_text, (WIDTH - diff_text.get_width() - 12, 10))

    def draw(self, screen, font):
        self.draw_road(screen)
        self.all_sprites.draw(screen)
        self.draw_hud(screen, font)

    def get_result(self):
        return {
            "name": self.username,
            "score": self.score,
            "distance": int(self.distance),
            "coins": self.coin_points,
            "status": self.status,
        }