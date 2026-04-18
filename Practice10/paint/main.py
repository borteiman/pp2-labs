import pygame

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mini Paint")
    clock = pygame.time.Clock()

    radius = 15
    mode = 'brush'
    color = (0, 0, 255)   # start with blue

    # this surface keeps all finished drawings
    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    drawing = False
    start_pos = None
    last_pos = None

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # close window
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # color selection
                # just press these keys to switch color fast
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)

                # tool selection
                # p = normal brush, e = eraser, c = circle, t = rectangle
                elif event.key == pygame.K_p:
                    mode = 'brush'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_t:
                    mode = 'rectangle'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

                # left and right click can still change brush size
                if event.button == 4:   # mouse wheel up
                    radius = min(200, radius + 1)
                elif event.button == 5: # mouse wheel down
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # when mouse released, we finish shape drawing
                    if mode == 'rectangle' and start_pos:
                        rect = make_rect(start_pos, event.pos)
                        pygame.draw.rect(canvas, color, rect, 2)

                    elif mode == 'circle' and start_pos:
                        center, circle_radius = make_circle(start_pos, event.pos)
                        if circle_radius > 0:
                            pygame.draw.circle(canvas, color, center, circle_radius, 2)

                    drawing = False
                    start_pos = None
                    last_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    # normal brush draws while mouse moves
                    if mode == 'brush':
                        pygame.draw.line(canvas, color, last_pos, event.pos, radius * 2)

                    # eraser just draws black, so it removes from black background
                    elif mode == 'eraser':
                        pygame.draw.line(canvas, (0, 0, 0), last_pos, event.pos, radius * 2)

                    last_pos = event.pos

        screen.fill((0, 0, 0))
        screen.blit(canvas, (0, 0))

        # preview for shapes before mouse release
        # this is only for showing shape while dragging
        if drawing and start_pos:
            current_pos = pygame.mouse.get_pos()

            if mode == 'rectangle':
                rect = make_rect(start_pos, current_pos)
                pygame.draw.rect(screen, color, rect, 2)

            elif mode == 'circle':
                center, circle_radius = make_circle(start_pos, current_pos)
                if circle_radius > 0:
                    pygame.draw.circle(screen, color, center, circle_radius, 2)

        draw_ui(screen, mode, color, radius)

        pygame.display.flip()
        clock.tick(60)


# makes rectangle correct even if user drags in any direction
def make_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return pygame.Rect(left, top, width, height)


# center is start point, radius depends on mouse distance
def make_circle(start, end):
    x1, y1 = start
    x2, y2 = end
    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    return start, radius


# small text on top so it is easy to see current tool and color
def draw_ui(screen, mode, color, radius):
    font = pygame.font.SysFont("Arial", 20)

    mode_text = font.render(f"Tool: {mode}", True, (255, 255, 255))
    size_text = font.render(f"Size: {radius}", True, (255, 255, 255))
    help_text = font.render("P-brush E-eraser T-rect C-circle | R/G/B/Y/W-colors", True, (255, 255, 255))

    pygame.draw.rect(screen, (40, 40, 40), (0, 0, 640, 60))
    screen.blit(mode_text, (10, 5))
    screen.blit(size_text, (10, 30))
    screen.blit(help_text, (160, 18))

    # current color preview
    pygame.draw.rect(screen, color, (590, 15, 30, 30))


main()