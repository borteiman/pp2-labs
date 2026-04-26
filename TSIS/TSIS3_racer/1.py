import pygame
import random
import sys
import time
import os

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Lab 2")

clock = pygame.time.Clock()
FPS = 60

font_big = pygame.font.SysFont("Verdana", 55)
font_small = pygame.font.SysFont("Verdana", 20)

# I use BASE_DIR because sometimes VS Code runs the file from another folder.
# This way Python still finds the resources folder correctly.
BASE_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

image_background = pygame.image.load(os.path.join(RESOURCES_DIR, "AnimatedStreet.png"))
image_player = pygame.image.load(os.path.join(RESOURCES_DIR, "Player.png"))
image_enemy = pygame.image.load(os.path.join(RESOURCES_DIR, "Enemy.png"))

pygame.mixer.music.load(os.path.join(RESOURCES_DIR, "background.wav"))
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound(os.path.join(RESOURCES_DIR, "crash.wav"))

SPEED = 5
SCORE = 0
COINS = 0

# After every N coin points, enemy speed will increase.
# I keep this value separate so it is easy to change later.
N_COINS_FOR_SPEED = 5
next_speed_coin_level = N_COINS_FOR_SPEED


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = image_player
        self.rect = self.image.get_rect()

        # Player starts near the bottom center of the road.
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT

        self.speed = 5

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # These checks do not let the car leave the window.
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        # Enemy starts above the screen and then moves down.
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

    def update(self):
        global SCORE

        self.rect.move_ip(0, SPEED)

        # If enemy passed the player, score increases.
        if self.rect.top > HEIGHT:
            SCORE += 1
            self.reset_position()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.value = 1
        self.radius = 12
        self.image = None
        self.rect = None

        self.choose_random_weight()
        self.reset_position()

    def choose_random_weight(self):
        # Coins have different weights.
        # Bigger value coins are rarer, so the game feels more balanced.
        self.value = random.choice([1, 1, 1, 2, 2, 3])

        if self.value == 1:
            self.radius = 11
            outer_color = (255, 215, 0)
            inner_color = (255, 240, 120)

        elif self.value == 2:
            self.radius = 14
            outer_color = (255, 140, 0)
            inner_color = (255, 210, 90)

        else:
            self.radius = 17
            outer_color = (180, 90, 255)
            inner_color = (220, 170, 255)

        size = self.radius * 2 + 4

        # I create the coin with pygame drawing tools, not with an extra image.
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, outer_color, (size // 2, size // 2), self.radius)
        pygame.draw.circle(self.image, inner_color, (size // 2, size // 2), self.radius - 5)
        pygame.draw.circle(self.image, (120, 90, 0), (size // 2, size // 2), self.radius, 2)

        # Small number inside the coin shows its weight.
        coin_font = pygame.font.SysFont("Verdana", 13)
        value_text = coin_font.render(str(self.value), True, (0, 0, 0))
        value_rect = value_text.get_rect(center=(size // 2, size // 2))
        self.image.blit(value_text, value_rect)

        old_center = None

        if self.rect is not None:
            old_center = self.rect.center

        self.rect = self.image.get_rect()

        if old_center is not None:
            self.rect.center = old_center

    def reset_position(self, enemy_rect=None):
        # Every time coin appears again, it can get a new weight.
        self.choose_random_weight()

        # I try several positions so the coin does not appear inside the enemy car.
        # This is not too complicated, but it fixes the ugly overlap problem.
        for attempt in range(30):
            self.rect.centerx = random.randint(35, WIDTH - 35)
            self.rect.bottom = random.randint(-600, -60)

            if enemy_rect is None:
                break

            # Coin starts above the screen, but still I check the distance from enemy.
            # It helps to avoid coin and enemy being in almost the same vertical line.
            too_close_x = abs(self.rect.centerx - enemy_rect.centerx) < 70

            if not too_close_x:
                break

    def update(self):
        self.rect.move_ip(0, SPEED)

        # If player missed the coin, it appears again later.
        if self.rect.top > HEIGHT:
            self.reset_position(enemy.rect)


player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

enemy_sprites = pygame.sprite.Group()
enemy_sprites.add(enemy)

coin_sprites = pygame.sprite.Group()
coin_sprites.add(coin)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()

    # Checking if player collected a coin.
    collected_coin = pygame.sprite.spritecollideany(player, coin_sprites)

    if collected_coin:
        COINS += collected_coin.value

        # Coin disappears and appears again with another random weight.
        collected_coin.reset_position(enemy.rect)

        # Speed increases only when player earns 5 coin points.
        
        if COINS >= next_speed_coin_level:
            SPEED += 1
            next_speed_coin_level += N_COINS_FOR_SPEED

    screen.blit(image_background, (0, 0))
    all_sprites.draw(screen)

    score_text = font_small.render(f"Score: {int(SCORE)}", True, "black")
    speed_text = font_small.render(f"Speed: {SPEED}", True, "black")
    coins_text = font_small.render(f"Coins: {COINS}", True, "black")

    screen.blit(score_text, (10, 10))
    screen.blit(speed_text, (10, 35))

    # Coins are shown in the top right corner, as the task asks.
    screen.blit(coins_text, (WIDTH - coins_text.get_width() - 10, 10))

    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        screen.fill("red")

        game_over_text = font_big.render("Game Over", True, "black")
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))

        final_score_text = font_small.render(f"Final score: {int(SCORE)}", True, "black")
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))

        final_coins_text = font_small.render(f"Collected coins: {COINS}", True, "black")
        final_coins_rect = final_coins_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

        final_speed_text = font_small.render(f"Final speed: {SPEED}", True, "black")
        final_speed_rect = final_speed_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(final_score_text, final_score_rect)
        screen.blit(final_coins_text, final_coins_rect)
        screen.blit(final_speed_text, final_speed_rect)

        pygame.display.flip()

        time.sleep(3)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(FPS)