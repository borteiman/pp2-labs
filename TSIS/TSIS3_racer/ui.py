import pygame

WIDTH, HEIGHT = 500, 700
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (95, 95, 95)
LIGHT_GRAY = (220, 220, 220)
DARK_BLUE = (45, 90, 130)
RED = (210, 70, 70)
YELLOW = (240, 190, 80)

BUTTON_RECTS = {
    "play": pygame.Rect(150, 235, 200, 48),
    "leaderboard": pygame.Rect(150, 300, 200, 48),
    "settings": pygame.Rect(150, 365, 200, 48),
    "quit": pygame.Rect(150, 430, 200, 48),
}

SETTINGS_RECTS = {
    "sound": pygame.Rect(130, 185, 240, 44),
    "blue": pygame.Rect(95, 300, 90, 42),
    "red": pygame.Rect(205, 300, 90, 42),
    "green": pygame.Rect(315, 300, 90, 42),
    "easy": pygame.Rect(75, 425, 100, 42),
    "normal": pygame.Rect(200, 425, 100, 42),
    "hard": pygame.Rect(325, 425, 100, 42),
    "back": pygame.Rect(165, 570, 170, 46),
}

BACK_RECT = pygame.Rect(160, 610, 180, 45)
GAME_OVER_RECTS = {
    "retry": pygame.Rect(105, 555, 130, 45),
    "menu": pygame.Rect(265, 555, 130, 45),
}


def draw_center_text(screen, text, font, color, y):
    image = font.render(text, True, color)
    rect = image.get_rect(center=(WIDTH // 2, y))
    screen.blit(image, rect)


def draw_button(screen, rect, text, font, active=False):
    # Active button is darker, so selected setting is easy to see.
    if active:
        bg = DARK_BLUE
        fg = WHITE
    else:
        bg = LIGHT_GRAY
        fg = BLACK
    pygame.draw.rect(screen, bg, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    label = font.render(text, True, fg)
    screen.blit(label, label.get_rect(center=rect.center))


def draw_name_entry(screen, font_big, font_medium, font_small, username):
    draw_center_text(screen, "Racer Game", font_big, WHITE, 150)
    draw_center_text(screen, "Enter your name", font_medium, LIGHT_GRAY, 250)
    input_rect = pygame.Rect(110, 315, 280, 50)
    pygame.draw.rect(screen, WHITE, input_rect, border_radius=8)
    text = font_medium.render(username + "|", True, BLACK)
    screen.blit(text, (input_rect.x + 15, input_rect.y + 10))
    draw_center_text(screen, "Press Enter to continue", font_small, LIGHT_GRAY, 405)
    draw_center_text(screen, "Max 12 characters", font_small, GRAY, 435)


def draw_main_menu(screen, font_big, font_medium, username):
    draw_center_text(screen, "Main Menu", font_big, WHITE, 135)
    player_text = font_medium.render(f"Player: {username}", True, LIGHT_GRAY)
    screen.blit(player_text, (25, 25))
    draw_button(screen, BUTTON_RECTS["play"], "Play", font_medium)
    draw_button(screen, BUTTON_RECTS["leaderboard"], "Leaderboard", font_medium)
    draw_button(screen, BUTTON_RECTS["settings"], "Settings", font_medium)
    draw_button(screen, BUTTON_RECTS["quit"], "Quit", font_medium)


def handle_main_menu_click(pos):
    for action, rect in BUTTON_RECTS.items():
        if rect.collidepoint(pos):
            return action
    return None


def draw_settings_screen(screen, font_big, font_medium, font_small, settings):
    draw_center_text(screen, "Settings", font_big, WHITE, 100)
    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
    draw_button(screen, SETTINGS_RECTS["sound"], sound_text, font_medium, settings["sound"])

    draw_center_text(screen, "Car color", font_medium, LIGHT_GRAY, 270)
    draw_button(screen, SETTINGS_RECTS["blue"], "Blue", font_small, settings["car_color"] == "blue")
    draw_button(screen, SETTINGS_RECTS["red"], "Red", font_small, settings["car_color"] == "red")
    draw_button(screen, SETTINGS_RECTS["green"], "Green", font_small, settings["car_color"] == "green")

    draw_center_text(screen, "Difficulty", font_medium, LIGHT_GRAY, 395)
    draw_button(screen, SETTINGS_RECTS["easy"], "Easy", font_small, settings["difficulty"] == "easy")
    draw_button(screen, SETTINGS_RECTS["normal"], "Normal", font_small, settings["difficulty"] == "normal")
    draw_button(screen, SETTINGS_RECTS["hard"], "Hard", font_small, settings["difficulty"] == "hard")
    draw_button(screen, SETTINGS_RECTS["back"], "Back", font_medium)


def handle_settings_click(pos):
    if SETTINGS_RECTS["sound"].collidepoint(pos):
        return "sound", None
    for color in ["blue", "red", "green"]:
        if SETTINGS_RECTS[color].collidepoint(pos):
            return "car_color", color
    for difficulty in ["easy", "normal", "hard"]:
        if SETTINGS_RECTS[difficulty].collidepoint(pos):
            return "difficulty", difficulty
    if SETTINGS_RECTS["back"].collidepoint(pos):
        return "back", None
    return None, None


def draw_leaderboard_screen(screen, font_big, font_medium, font_small, leaderboard):
    draw_center_text(screen, "Leaderboard", font_big, WHITE, 70)
    header = font_small.render("Rank   Name        Score     Distance", True, YELLOW)
    screen.blit(header, (60, 130))
    y = 170
    if len(leaderboard) == 0:
        draw_center_text(screen, "No scores yet", font_medium, LIGHT_GRAY, 260)
    for index, item in enumerate(leaderboard[:10], start=1):
        line = f"{index:<5} {item['name'][:10]:<10} {item['score']:<8} {item['distance']} m"
        text = font_small.render(line, True, WHITE)
        screen.blit(text, (60, y))
        y += 38
    draw_button(screen, BACK_RECT, "Back", font_medium)


def handle_back_button(pos):
    return BACK_RECT.collidepoint(pos)


def draw_game_over_screen(screen, font_big, font_medium, font_small, result):
    draw_center_text(screen, "Game Over", font_big, RED, 120)
    if result is None:
        result = {"name": "Player", "score": 0, "distance": 0, "coins": 0, "status": "Run ended"}
    draw_center_text(screen, result["status"], font_medium, LIGHT_GRAY, 185)
    lines = [
        f"Player: {result['name']}",
        f"Score: {result['score']}",
        f"Distance: {result['distance']} m",
        f"Coins: {result['coins']}",
    ]
    y = 270
    for line in lines:
        draw_center_text(screen, line, font_medium, WHITE, y)
        y += 45
    draw_button(screen, GAME_OVER_RECTS["retry"], "Retry", font_medium)
    draw_button(screen, GAME_OVER_RECTS["menu"], "Menu", font_medium)


def handle_game_over_click(pos):
    for action, rect in GAME_OVER_RECTS.items():
        if rect.collidepoint(pos):
            return action
    return None
