import pygame
import sys

from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import (
    draw_main_menu, handle_main_menu_click,
    draw_settings_screen, handle_settings_click,
    draw_leaderboard_screen, handle_back_button,
    draw_name_entry,
    draw_game_over_screen, handle_game_over_click,
)
from racer import RacerGame

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")

clock = pygame.time.Clock()
FPS = 60

font_big = pygame.font.SysFont("Verdana", 42)
font_medium = pygame.font.SysFont("Verdana", 24)
font_small = pygame.font.SysFont("Verdana", 17)

settings = load_settings()
leaderboard = load_leaderboard()

current_screen = "name_entry"
username = ""
game = None
last_result = None


def start_new_game():
    # I create a new game object for Play and Retry.
    global game, current_screen, last_result
    game = RacerGame(settings, username)
    last_result = None
    current_screen = "game"


running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "name_entry":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip() != "":
                    current_screen = "main_menu"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    # event.unicode gives the real typed symbol.
                    if len(username) < 12 and event.unicode.isprintable():
                        username += event.unicode

        elif current_screen == "main_menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = handle_main_menu_click(event.pos)
                if action == "play":
                    if username.strip() == "":
                        username = "Player"
                    start_new_game()
                elif action == "leaderboard":
                    leaderboard = load_leaderboard()
                    current_screen = "leaderboard"
                elif action == "settings":
                    current_screen = "settings"
                elif action == "quit":
                    running = False

        elif current_screen == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action, value = handle_settings_click(event.pos)
                if action == "sound":
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)
                elif action == "car_color":
                    settings["car_color"] = value
                    save_settings(settings)
                elif action == "difficulty":
                    settings["difficulty"] = value
                    save_settings(settings)
                elif action == "back":
                    current_screen = "main_menu"

        elif current_screen == "leaderboard":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if handle_back_button(event.pos):
                    current_screen = "main_menu"

        elif current_screen == "game":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_screen = "main_menu"

        elif current_screen == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = handle_game_over_click(event.pos)
                if action == "retry":
                    start_new_game()
                elif action == "menu":
                    current_screen = "main_menu"

    screen.fill((25, 25, 25))

    if current_screen == "name_entry":
        draw_name_entry(screen, font_big, font_medium, font_small, username)

    elif current_screen == "main_menu":
        draw_main_menu(screen, font_big, font_medium, username)

    elif current_screen == "settings":
        draw_settings_screen(screen, font_big, font_medium, font_small, settings)

    elif current_screen == "leaderboard":
        leaderboard = load_leaderboard()
        draw_leaderboard_screen(screen, font_big, font_medium, font_small, leaderboard)

    elif current_screen == "game":
        game.update(dt)
        game.draw(screen, font_small)
        if game.finished:
            last_result = game.get_result()
            add_score(last_result["name"], last_result["score"], last_result["distance"], last_result["coins"])
            current_screen = "game_over"

    elif current_screen == "game_over":
        draw_game_over_screen(screen, font_big, font_medium, font_small, last_result)

    pygame.display.flip()

pygame.quit()
sys.exit()
