import pygame
import sys
from ball import Ball

WIDTH, HEIGHT = 600, 500

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    clock = pygame.time.Clock()

    ball = Ball(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    font = pygame.font.SysFont("Arial", 18)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -20)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 20)
                elif event.key == pygame.K_LEFT:
                    ball.move(-20, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(20, 0)

        screen.fill((255, 255, 255))
        ball.draw(screen)

        info = font.render(f"Position: ({ball.x}, {ball.y})   Use Arrow Keys to move", True, (100, 100, 100))
        screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()