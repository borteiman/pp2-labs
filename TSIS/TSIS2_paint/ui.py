import pygame

#рисует 
#  интерфейс

from settings import (
    TOOLBAR_WIDTH,
    SCREEN_HEIGHT,
    BLACK,
    WHITE,
    LIGHT_GRAY,
    GRAY,
    DARK_GRAY,
    COLORS,
    BRUSH_SIZES,
)

BUTTONS = [
    ("Pencil", "pencil"),
    ("Line", "line"),
    ("Rect", "rect"),
    ("Circle", "circle"),
    ("Square", "square"),
    ("R.Tri", "right_triangle"),
    ("E.Tri", "equilateral_triangle"),
    ("Rhombus", "rhombus"),
    ("Eraser", "eraser"),
    ("Fill", "fill"),
    ("Text", "text"),
]

SIZE_BUTTONS = [
    ("Small", BRUSH_SIZES["small"]),
    ("Medium", BRUSH_SIZES["medium"]),
    ("Large", BRUSH_SIZES["large"]),
]


def make_toolbar_rects():
    # All toolbar buttons are created here.
    # It is easier to control their positions from one place.
    tool_rects = []
    size_rects = []
    color_rects = []

    x = 15
    y = 15
    w = TOOLBAR_WIDTH - 30
    h = 28
    gap = 5

    for label, tool in BUTTONS:
        rect = pygame.Rect(x, y, w, h)
        tool_rects.append((rect, label, tool))
        y += h + gap

    y += 8

    for label, size in SIZE_BUTTONS:
        rect = pygame.Rect(x, y, w, h)
        size_rects.append((rect, label, size))
        y += h + gap

    y += 12

    color_size = 26
    color_gap = 7
    start_x = x

    for index, (name, color) in enumerate(COLORS):
        row = index // 4
        col = index % 4

        rect = pygame.Rect(
            start_x + col * (color_size + color_gap),
            y + row * (color_size + color_gap),
            color_size,
            color_size
        )

        color_rects.append((rect, name, color))

    return tool_rects, size_rects, color_rects


def draw_button(screen, rect, text, font, active=False):
    # Active button is dark, so we can see which tool is selected.
    if active:
        bg = DARK_GRAY
        fg = WHITE
    else:
        bg = WHITE
        fg = BLACK

    pygame.draw.rect(screen, bg, rect, border_radius=6)
    pygame.draw.rect(screen, GRAY, rect, 1, border_radius=6)

    label = font.render(text, True, fg)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def draw_toolbar(screen, font, small_font, current_tool, current_color, brush_size, saved_message):
    # Left panel for tools, brush sizes and colors.
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, TOOLBAR_WIDTH, SCREEN_HEIGHT))

    tool_rects, size_rects, color_rects = make_toolbar_rects()

    for rect, label, tool in tool_rects:
        draw_button(screen, rect, label, small_font, current_tool == tool)

    for rect, label, size in size_rects:
        draw_button(screen, rect, label, small_font, brush_size == size)

    for rect, name, color in color_rects:
        pygame.draw.rect(screen, color, rect, border_radius=4)

        if current_color == color:
            border_width = 3
        else:
            border_width = 1

        pygame.draw.rect(screen, BLACK, rect, border_width, border_radius=4)

    # Short hints under colors.
    # I keep them compact so they do not cover the color buttons.
    last_color_bottom = max(rect.bottom for rect, name, color in color_rects)
    hint_y = last_color_bottom + 12

    hints = [
        "1/2/3 size",
        "Ctrl+S save",
        "X clear canvas",
        "Esc cancel / exit",
    ]

    for hint in hints:
        text = small_font.render(hint, True, BLACK)
        screen.blit(text, (15, hint_y))
        hint_y += 17

    if saved_message:
        msg = small_font.render(saved_message, True, DARK_GRAY)
        screen.blit(msg, (15, SCREEN_HEIGHT - 20))


def check_toolbar_click(pos):
    # This checks what user clicked in the toolbar.
    tool_rects, size_rects, color_rects = make_toolbar_rects()

    for rect, label, tool in tool_rects:
        if rect.collidepoint(pos):
            return "tool", tool

    for rect, label, size in size_rects:
        if rect.collidepoint(pos):
            return "size", size

    for rect, name, color in color_rects:
        if rect.collidepoint(pos):
            return "color", color

    return None, None