import pygame
import sys
import random
import time
import os

# -------------------------
# Pygame initialization
# -------------------------
pygame.init()

try:
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except pygame.error:
    SOUND_AVAILABLE = False

# -------------------------
# Game settings
# -------------------------
FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GRAY = (180, 180, 180)

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# -------------------------
# Display
# -------------------------
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# -------------------------
# Fonts
# -------------------------
font_large = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_tiny = pygame.font.SysFont("Verdana", 14)

game_over_text = font_large.render("Game Over", True, BLACK)


# -------------------------
# Helper functions
# -------------------------
def find_asset(filename):
    """
    Try several possible locations for an asset file.
    This makes the game work even if the current working directory changes.
    """
    possible_paths = [
        os.path.join(ASSETS_DIR, filename),                  
        os.path.join(BASE_DIR, filename),                    
        os.path.join(os.getcwd(), filename),                 
        os.path.join(os.getcwd(), "assets", filename),       
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


def make_placeholder(size, color, label=""):
    """
    Create a simple fallback image so the game does not crash
    if some image file is missing.
    """
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)

    if label:
        text = font_tiny.render(label, True, BLACK)
        text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2))
        surface.blit(text, text_rect)

    return surface


def load_image(filename, fallback_size, fallback_color, label="", use_alpha=True):
    """
    Load image safely. If file is missing, return a placeholder surface.
    """
    path = find_asset(filename)

    if path is not None:
        try:
            image = pygame.image.load(path)
            return image.convert_alpha() if use_alpha else image.convert()
        except pygame.error:
            pass

    return make_placeholder(fallback_size, fallback_color, label)


def play_sound(filename):
    """
    Play sound safely. Does nothing if sound is unavailable or file is missing.
    """
    if not SOUND_AVAILABLE:
        return

    path = find_asset(filename)
    if path is None:
        return

    try:
        pygame.mixer.Sound(path).play()
    except pygame.error:
        pass


# -------------------------
# Load background
# -------------------------
background = load_image(
    "AnimatedStreet.png",
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    GRAY,
    "ROAD",
    use_alpha=False
)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves from top to bottom."""

    def __init__(self):
        super().__init__()
        self.image = load_image("Enemy.png", (50, 90), RED, "ENEMY")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

    def move(self):
        global SCORE

        self.rect.move_ip(0, int(SPEED))

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = -100
            self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)


class Player(pygame.sprite.Sprite):
    """Player car controlled with left and right arrow keys."""

    def __init__(self):
        super().__init__()
        self.image = load_image("Player.png", (50, 90), BLUE, "PLAYER")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if pressed_keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    """Coin that appears randomly and can be collected."""

    def __init__(self):
        super().__init__()

        # Use coin.png if it exists; otherwise draw a coin
        coin_path = find_asset("coin.png")

        if coin_path is not None:
            try:
                self.image = pygame.image.load(coin_path).convert_alpha()
            except pygame.error:
                self.image = self.create_coin_surface()
        else:
            self.image = self.create_coin_surface()

        self.rect = self.image.get_rect()
        self.reset()

    def create_coin_surface(self):
        surface = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(surface, GOLD, (12, 12), 12)
        pygame.draw.circle(surface, BLACK, (12, 12), 12, 2)
        return surface

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -30)

    def move(self):
        self.rect.move_ip(0, int(SPEED))

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# -------------------------
# Create game objects
# -------------------------
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# -------------------------
# Events
# -------------------------
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 2000)

# -------------------------
# Main game loop
# -------------------------
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == INC_SPEED:
            SPEED += 0.5

        elif event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Draw score
    score_surface = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(score_surface, (10, 10))

    # Draw coin counter
    coins_surface = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    coins_rect = coins_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    DISPLAYSURF.blit(coins_surface, coins_rect)

    # Move and draw sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Coin collection
    collected = pygame.sprite.spritecollide(P1, coins, True)
    if collected:
        COINS_COLLECTED += len(collected)

    # Collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        play_sound("crash.wav")

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30, 250))
        pygame.display.update()

        time.sleep(2)
        running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()