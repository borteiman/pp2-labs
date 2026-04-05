import pygame
import sys
from player import MusicPlayer

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    player = MusicPlayer()

    font_big = pygame.font.SysFont("Arial", 22)
    font_small = pygame.font.SysFont("Arial", 17)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY  = (200, 200, 200)
    GREEN = (50, 180, 50)
    RED   = (200, 50, 50)
    BLUE  = (50, 50, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_q:
                    running = False

        screen.fill(WHITE)

        # Title
        title = font_big.render("🎵 Music Player", True, BLUE)
        screen.blit(title, (20, 20))

        # Track info
        track_name = player.get_current_track_name()
        status = player.get_status()
        track_text = font_big.render(f"Track: {track_name}", True, BLACK)
        status_text = font_small.render(f"Status: {status}", True, GREEN if status == "Playing" else RED)
        screen.blit(track_text, (20, 70))
        screen.blit(status_text, (20, 105))

        # Playlist
        playlist_label = font_small.render("Playlist:", True, BLACK)
        screen.blit(playlist_label, (20, 145))
        for i, name in enumerate(player.get_playlist_names()):
            color = BLUE if i == player.current_index else BLACK
            t = font_small.render(f"  {'> ' if i == player.current_index else '  '}{i+1}. {name}", True, color)
            screen.blit(t, (20, 165 + i * 22))

        # Progress bar
        progress = player.get_progress()
        pygame.draw.rect(screen, GRAY, (20, 255, 460, 15), border_radius=7)
        pygame.draw.rect(screen, GREEN, (20, 255, int(460 * progress), 15), border_radius=7)
        pos_text = font_small.render(f"{player.get_position_str()}", True, BLACK)
        screen.blit(pos_text, (20, 273))

        # Controls hint
        hint = font_small.render("P=Play  S=Stop  N=Next  B=Prev  Q=Quit", True, GRAY)
        screen.blit(hint, (20, 15 + 270))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()