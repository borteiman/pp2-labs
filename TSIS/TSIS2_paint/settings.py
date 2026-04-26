# main project settings are here so main is not too crowded.
# файл с константами проекта

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
TOOLBAR_WIDTH = 180

CANVAS_WIDTH = SCREEN_WIDTH - TOOLBAR_WIDTH
CANVAS_HEIGHT = SCREEN_HEIGHT

#frames per second  программа не грузила сильно, интерфейс плавно
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (230, 230, 230)
GRAY = (180, 180, 180)
DARK_GRAY = (70, 70, 70)

RED = (230, 57, 70)
GREEN = (42, 157, 143)
BLUE = (69, 123, 157)
YELLOW = (255, 183, 3)
PURPLE = (131, 56, 236)
ORANGE = (251, 133, 0)

COLORS = [
    ("Black", BLACK),
    ("White", WHITE),
    ("Red", RED),
    ("Green", GREEN),
    ("Blue", BLUE),
    ("Yellow", YELLOW),
    ("Purple", PURPLE),
    ("Orange", ORANGE),
]

BRUSH_SIZES = {
    "small": 2,
    "medium": 7,
    "large": 14,
}

#по умолчанию 

DEFAULT_TOOL = "pencil"
DEFAULT_COLOR = BLACK
DEFAULT_SIZE = BRUSH_SIZES["medium"]

SAVE_FOLDER = "saved_images"
