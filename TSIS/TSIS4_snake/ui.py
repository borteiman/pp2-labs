import pygame
from constants import WIDTH, HEIGHT, WHITE, BLACK, LIGHT_GRAY, GRAY, GREEN, RED, BLUE, YELLOW, CYAN

BUTTONS = {
    "play": pygame.Rect(200, 250, 200, 48),
    "leaderboard": pygame.Rect(200, 315, 200, 48),
    "settings": pygame.Rect(200, 380, 200, 48),
    "quit": pygame.Rect(200, 445, 200, 48),
}

GAME_OVER_BUTTONS = {
    "retry": pygame.Rect(135, 485, 150, 46),
    "menu": pygame.Rect(315, 485, 150, 46),
}

BACK_BUTTON = pygame.Rect(210, 650, 180, 40)

SETTINGS_BUTTONS = {
    "grid": pygame.Rect(180, 210, 240, 42),
    "sound": pygame.Rect(180, 270, 240, 42),
    "green": pygame.Rect(130, 390, 90, 42),
    "blue": pygame.Rect(255, 390, 90, 42),
    "red": pygame.Rect(380, 390, 90, 42),
    "save": pygame.Rect(190, 550, 220, 46),
}

COLOR_OPTIONS = {
    "green": [60, 180, 95],
    "blue": [70, 130, 210],
    "red": [210, 60, 70],
}


def center_text(screen, text, font, color, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH // 2, y))
    screen.blit(img, rect)


def draw_button(screen, rect, text, font, active=False):
    color = CYAN if active else LIGHT_GRAY
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def draw_main_menu(screen, fonts, username, db_status):
    big, medium, small = fonts
    screen.fill((28, 31, 35))
    center_text(screen, "Snake TSIS 4", big, WHITE, 90)
    center_text(screen, "Enter username and press Play", small, LIGHT_GRAY, 145)
    input_rect = pygame.Rect(155, 175, 290, 42)
    pygame.draw.rect(screen, WHITE, input_rect, border_radius=8)
    shown = username + "|"
    text = medium.render(shown, True, BLACK)
    screen.blit(text, (input_rect.x + 12, input_rect.y + 8))
    draw_button(screen, BUTTONS["play"], "Play", medium)
    draw_button(screen, BUTTONS["leaderboard"], "Leaderboard", medium)
    draw_button(screen, BUTTONS["settings"], "Settings", medium)
    draw_button(screen, BUTTONS["quit"], "Quit", medium)
    status_color = GREEN if db_status else RED
    status_text = "DB: connected" if db_status else "DB: not connected"
    center_text(screen, status_text, small, status_color, 600)


def main_menu_action(pos):
    for name, rect in BUTTONS.items():
        if rect.collidepoint(pos):
            return name
    return None


def draw_leaderboard(screen, fonts, rows, db_error):
    big, medium, small = fonts
    screen.fill((28, 31, 35))
    center_text(screen, "Leaderboard", big, WHITE, 60)
    header = small.render("Rank  Username          Score   Level   Date", True, YELLOW)
    screen.blit(header, (50, 120))
    y = 160
    if len(rows) == 0:
        center_text(screen, "No scores yet or database is not connected", small, LIGHT_GRAY, 250)
        if db_error:
            center_text(screen, db_error[:55], small, RED, 285)
    for index, row in enumerate(rows, start=1):
        line = f"{index:<5} {row['username'][:14]:<16} {row['score']:<7} {row['level']:<6} {row['date']}"
        text = small.render(line, True, WHITE)
        screen.blit(text, (50, y))
        y += 35
    draw_button(screen, BACK_BUTTON, "Back", medium)


def draw_game_over(screen, fonts, result, saved_ok):
    big, medium, small = fonts
    screen.fill((28, 31, 35))
    center_text(screen, "Game Over", big, RED, 105)
    center_text(screen, result["status"], medium, LIGHT_GRAY, 165)
    lines = [
        f"Player: {result['username']}",
        f"Final score: {result['score']}",
        f"Level reached: {result['level']}",
        f"Personal best: {result['personal_best']}",
        "Saved to DB" if saved_ok else "DB save failed",
    ]
    y = 235
    for line in lines:
        center_text(screen, line, medium, WHITE, y)
        y += 45
    draw_button(screen, GAME_OVER_BUTTONS["retry"], "Retry", medium)
    draw_button(screen, GAME_OVER_BUTTONS["menu"], "Main Menu", medium)


def game_over_action(pos):
    for name, rect in GAME_OVER_BUTTONS.items():
        if rect.collidepoint(pos):
            return name
    return None


def draw_settings(screen, fonts, settings):
    big, medium, small = fonts
    screen.fill((28, 31, 35))
    center_text(screen, "Settings", big, WHITE, 80)
    grid_text = "Grid: ON" if settings["grid"] else "Grid: OFF"
    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
    draw_button(screen, SETTINGS_BUTTONS["grid"], grid_text, medium, settings["grid"])
    draw_button(screen, SETTINGS_BUTTONS["sound"], sound_text, medium, settings["sound"])
    center_text(screen, "Snake color", medium, LIGHT_GRAY, 355)
    for name in ["green", "blue", "red"]:
        active = settings["snake_color"] == COLOR_OPTIONS[name]
        draw_button(screen, SETTINGS_BUTTONS[name], name.capitalize(), small, active)
    center_text(screen, "Changes are saved to settings.json", small, GRAY, 500)
    draw_button(screen, SETTINGS_BUTTONS["save"], "Save & Back", medium)


def settings_action(pos):
    for name, rect in SETTINGS_BUTTONS.items():
        if rect.collidepoint(pos):
            return name
    return None


def back_clicked(pos):
    return BACK_BUTTON.collidepoint(pos)
