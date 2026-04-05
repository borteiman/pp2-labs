"""
main.py
-------
Entry point for Mickey's Clock.

Run with:
    python main.py
"""

import os
import sys

import pygame

from clock import MickeyClock


# ── window settings ────────────────────────────────────────────────────────
WINDOW_W, WINDOW_H = 620, 650
FPS = 60
TITLE = "Mickey's Clock"
BG_COLOR = (0, 0, 0)   # black, matches the original image backgrounds


def _img_path(*parts: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "images", *parts)


def main() -> None:
    pygame.init()
    pygame.display.set_caption(TITLE)

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    fps_clock = pygame.time.Clock()

    # ── load assets ────────────────────────────────────────────────────────
    # clock face keeps its original background (no transparency needed)
    clock_face = pygame.image.load(_img_path("clock.png")).convert()

    # hand / Mickey images are RGBA with transparent background
    mickey_body = pygame.image.load(_img_path("mUmrP_rgba.png")).convert_alpha()
    left_hand   = pygame.image.load(_img_path("hand_left_rgba.png")).convert_alpha()   # seconds
    right_hand  = pygame.image.load(_img_path("hand_right_rgba.png")).convert_alpha()  # minutes

    clock_widget = MickeyClock(screen, clock_face, mickey_body,
                               left_hand, right_hand)

    # ── main loop ──────────────────────────────────────────────────────────
    running = True
    while running:
        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- draw ---
        screen.fill(BG_COLOR)
        clock_widget.draw()
        pygame.display.flip()

        fps_clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
