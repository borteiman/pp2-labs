import pygame
import sys
from constants import WIDTH, HEIGHT, FPS
from settings_manager import load_settings, save_settings
import db
from game import SnakeGame
from ui import draw_main_menu, main_menu_action, draw_leaderboard, draw_game_over, game_over_action, draw_settings, settings_action, back_clicked, COLOR_OPTIONS

pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 Snake Game")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("Verdana", 42)
font_medium = pygame.font.SysFont("Verdana", 22)
font_small = pygame.font.SysFont("Verdana", 15)
fonts = (font_big, font_medium, font_small)
settings = load_settings()
db_status = db.init_db()
screen_name = "menu"
username = ""
game = None
last_result = None
saved_ok = False


def start_game():
    global game, screen_name
    name = username.strip()
    if name == "":
        name = "Player"
    best = db.get_personal_best(name)
    game = SnakeGame(name, best, settings)
    screen_name = "game"


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if screen_name == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    start_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif len(username) < 14 and event.unicode.isprintable():
                    username += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = main_menu_action(event.pos)
                if action == "play":
                    start_game()
                elif action == "leaderboard":
                    screen_name = "leaderboard"
                elif action == "settings":
                    screen_name = "settings"
                elif action == "quit":
                    running = False

        elif screen_name == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen_name = "menu"
                else:
                    game.process_event(event)

        elif screen_name == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = game_over_action(event.pos)
                if action == "retry":
                    start_game()
                elif action == "menu":
                    screen_name = "menu"

        elif screen_name == "leaderboard":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_clicked(event.pos):
                    screen_name = "menu"

        elif screen_name == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = settings_action(event.pos)
                if action == "grid":
                    settings["grid"] = not settings["grid"]
                elif action == "sound":
                    settings["sound"] = not settings["sound"]
                elif action in COLOR_OPTIONS:
                    settings["snake_color"] = COLOR_OPTIONS[action]
                elif action == "save":
                    save_settings(settings)
                    screen_name = "menu"

    if screen_name == "menu":
        draw_main_menu(screen, fonts, username, db_status)
    elif screen_name == "game":
        game.update()
        game.draw(screen, font_small)
        if game.game_over:
            last_result = game.result()
            saved_ok = db.save_game_session(last_result["username"], last_result["score"], last_result["level"])
            screen_name = "game_over"
    elif screen_name == "game_over":
        draw_game_over(screen, fonts, last_result, saved_ok)
    elif screen_name == "leaderboard":
        rows = db.get_top_scores(10)
        draw_leaderboard(screen, fonts, rows, db.get_last_error())
    elif screen_name == "settings":
        draw_settings(screen, fonts, settings)

    pygame.display.flip()

pygame.quit()
sys.exit()
