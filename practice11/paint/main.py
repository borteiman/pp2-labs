import pygame
import math

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mini Paint")
    clock = pygame.time.Clock()

    color = (0, 0, 255)
    mode = 'brush'
    radius = 8

    # this surface stores everything that is already drawn
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

            # normal ways to close the window
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # colors
                # just press key and current color changes
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

                # tools
                # p - brush
                # e - eraser
                # o - square
                # t - right triangle
                # q - equilateral triangle
                # h - rhombus
                elif event.key == pygame.K_p:
                    mode = 'brush'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_o:
                    mode = 'square'
                elif event.key == pygame.K_t:
                    mode = 'right_triangle'
                elif event.key == pygame.K_q:
                    mode = 'equilateral_triangle'
                elif event.key == pygame.K_h:
                    mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

                # wheel changes brush size
                elif event.button == 4:
                    radius = min(50, radius + 1)
                elif event.button == 5:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    end_pos = event.pos

                    # free drawing
                    if mode == 'brush':
                        pygame.draw.line(canvas, color, last_pos, end_pos, radius * 2)

                    # eraser works same as brush but with black color
                    elif mode == 'eraser':
                        pygame.draw.line(canvas, (0, 0, 0), last_pos, end_pos, radius * 2)

                    # draw square after mouse release
                    elif mode == 'square':
                        rect = make_square(start_pos, end_pos)
                        pygame.draw.rect(canvas, color, rect, 2)

                    # draw right triangle after mouse release
                    elif mode == 'right_triangle':
                        points = make_right_triangle(start_pos, end_pos)
                        pygame.draw.polygon(canvas, color, points, 2)

                    # draw equilateral triangle after mouse release
                    elif mode == 'equilateral_triangle':
                        points = make_equilateral_triangle(start_pos, end_pos)
                        pygame.draw.polygon(canvas, color, points, 2)

                    # draw rhombus after mouse release
                    elif mode == 'rhombus':
                        points = make_rhombus(start_pos, end_pos)
                        pygame.draw.polygon(canvas, color, points, 2)

                    drawing = False
                    start_pos = None
                    last_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    # brush draws while mouse moves
                    if mode == 'brush':
                        pygame.draw.line(canvas, color, last_pos, event.pos, radius * 2)
                        last_pos = event.pos

                    # eraser also works while mouse moves
                    elif mode == 'eraser':
                        pygame.draw.line(canvas, (0, 0, 0), last_pos, event.pos, radius * 2)
                        last_pos = event.pos

        screen.fill((0, 0, 0))
        screen.blit(canvas, (0, 0))

        # preview of shape while dragging mouse
        if drawing and start_pos and mode not in ['brush', 'eraser']:
            current_pos = pygame.mouse.get_pos()

            if mode == 'square':
                rect = make_square(start_pos, current_pos)
                pygame.draw.rect(screen, color, rect, 2)

            elif mode == 'right_triangle':
                points = make_right_triangle(start_pos, current_pos)
                pygame.draw.polygon(screen, color, points, 2)

            elif mode == 'equilateral_triangle':
                points = make_equilateral_triangle(start_pos, current_pos)
                pygame.draw.polygon(screen, color, points, 2)

            elif mode == 'rhombus':
                points = make_rhombus(start_pos, current_pos)
                pygame.draw.polygon(screen, color, points, 2)

        draw_ui(screen, mode, color, radius)

        pygame.display.flip()
        clock.tick(60)


def make_square(start, end):
    # make square with same width and height
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 >= x1:
        left = x1
    else:
        left = x1 - side

    if y2 >= y1:
        top = y1
    else:
        top = y1 - side

    return pygame.Rect(left, top, side, side)


def make_right_triangle(start, end):
    # simple right triangle inside dragged area
    x1, y1 = start
    x2, y2 = end

    return [(x1, y1), (x1, y2), (x2, y2)]


def make_equilateral_triangle(start, end):
    # here start point is top center of triangle
    # side length depends on mouse distance horizontally
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1) * 2
    if side < 2:
        side = 2

    height = (math.sqrt(3) / 2) * side

    # if mouse goes down, triangle goes down
    if y2 >= y1:
        top = (x1, y1)
        left = (x1 - side // 2, y1 + height)
        right = (x1 + side // 2, y1 + height)
    else:
        top = (x1, y1)
        left = (x1 - side // 2, y1 - height)
        right = (x1 + side // 2, y1 - height)

    return [top, left, right]


def make_rhombus(start, end):
    # rhombus is made from middle points
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    mid_x = (left + right) // 2
    mid_y = (top + bottom) // 2

    return [
        (mid_x, top),
        (right, mid_y),
        (mid_x, bottom),
        (left, mid_y)
    ]


def draw_ui(screen, mode, color, radius):
    font = pygame.font.SysFont("Arial", 18)

    text1 = font.render(f"Tool: {mode}", True, (255, 255, 255))
    text2 = font.render(f"Size: {radius}", True, (255, 255, 255))
    text3 = font.render("P-brush E-eraser O-square T-right Q-eq H-rhombus", True, (255, 255, 255))
    text4 = font.render("R G B Y W - colors | mouse wheel - size", True, (255, 255, 255))

    pygame.draw.rect(screen, (40, 40, 40), (0, 0, 640, 80))
    screen.blit(text1, (10, 5))
    screen.blit(text2, (10, 28))
    screen.blit(text3, (150, 10))
    screen.blit(text4, (150, 35))

    # small box to show current color
    pygame.draw.rect(screen, color, (590, 20, 30, 30))


main()