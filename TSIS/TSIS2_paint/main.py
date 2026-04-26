import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TOOLBAR_WIDTH,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    FPS,
    BLACK,
    WHITE,
    DEFAULT_TOOL,
    DEFAULT_COLOR,
    DEFAULT_SIZE, 
    BRUSH_SIZES,
)
from shapes import (
    calculate_rect,
    calculate_square,
    calculate_circle,
    calculate_right_triangle,
    calculate_equilateral_triangle,
    calculate_rhombus,
)
from tools import draw_pencil_line, flood_fill, save_canvas, draw_text, clear_canvas
from ui import draw_toolbar, check_toolbar_click


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TSIS 2 Paint Application")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 18)
small_font = pygame.font.SysFont("arial", 14)
text_font = pygame.font.SysFont("arial", 28)

canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

current_tool = DEFAULT_TOOL
current_color = DEFAULT_COLOR
brush_size = DEFAULT_SIZE

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_pos = None
text_value = ""

saved_message = ""
saved_message_timer = 0


def screen_to_canvas(pos):
    # Mouse position on screen is not the same as position on canvas.
    x, y = pos
    return x - TOOLBAR_WIDTH, y


def is_on_canvas(pos):
    x, y = screen_to_canvas(pos)
    return 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT


def draw_shape(surface, tool, start, end, color, size):
    # One function for all preview and final shape drawing.
    if tool == "line":
        pygame.draw.line(surface, color, start, end, size)

    elif tool == "rect":
        rect = calculate_rect(start, end)
        pygame.draw.rect(surface, color, rect, size)

    elif tool == "circle":
        center, radius = calculate_circle(start, end)
        pygame.draw.circle(surface, color, center, radius, size)

    elif tool == "square":
        square = calculate_square(start, end)
        pygame.draw.rect(surface, color, square, size)

    elif tool == "right_triangle":
        points = calculate_right_triangle(start, end)
        pygame.draw.polygon(surface, color, points, size)

    elif tool == "equilateral_triangle":
        points = calculate_equilateral_triangle(start, end)
        pygame.draw.polygon(surface, color, points, size)

    elif tool == "rhombus":
        points = calculate_rhombus(start, end)
        pygame.draw.polygon(surface, color, points, size)


def finish_text():
    global text_mode, text_pos, text_value

    if text_mode and text_value != "":
        draw_text(canvas, text_value, text_pos, current_color, text_font)

    text_mode = False
    text_pos = None
    text_value = ""


def cancel_text():
    global text_mode, text_pos, text_value

    text_mode = False
    text_pos = None
    text_value = ""


running = True

while running:
    screen.fill(WHITE)

    # Canvas is drawn after toolbar offset.
    screen.blit(canvas, (TOOLBAR_WIDTH, 0))

    # Shape preview while dragging.
    if drawing and start_pos is not None:
        mouse_pos = pygame.mouse.get_pos()

        if is_on_canvas(mouse_pos):
            current_pos = screen_to_canvas(mouse_pos)

            if current_tool in [
                "line",
                "rect",
                "circle",
                "square",
                "right_triangle",
                "equilateral_triangle",
                "rhombus",
            ]:
                preview = canvas.copy()
                draw_shape(preview, current_tool, start_pos, current_pos, current_color, brush_size)
                screen.blit(preview, (TOOLBAR_WIDTH, 0))

    # Text preview before Enter.
    if text_mode and text_pos is not None:
        preview = text_font.render(text_value + "|", True, current_color)
        screen.blit(preview, (TOOLBAR_WIDTH + text_pos[0], text_pos[1]))

    if saved_message_timer > 0:
        saved_message_timer -= 1
    else:
        saved_message = ""

    draw_toolbar(screen, font, small_font, current_tool, current_color, brush_size, saved_message)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Ctrl + S saves the canvas.
            if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                filename = save_canvas(canvas)
                saved_message = "Saved: " + filename.name
                saved_message_timer = FPS * 2

            elif text_mode:
                # Text tool has its own keyboard logic.
                if event.key == pygame.K_RETURN:
                    finish_text()

                elif event.key == pygame.K_ESCAPE:
                    cancel_text()

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Size shortcuts from the task.
                elif event.key == pygame.K_1:
                    brush_size = BRUSH_SIZES["small"]

                elif event.key == pygame.K_2:
                    brush_size = BRUSH_SIZES["medium"]

                elif event.key == pygame.K_3:
                    brush_size = BRUSH_SIZES["large"]

                # Simple keyboard shortcuts for tools.
                elif event.key == pygame.K_p:
                    current_tool = "pencil"

                elif event.key == pygame.K_l:
                    current_tool = "line"

                elif event.key == pygame.K_r:
                    current_tool = "rect"

                elif event.key == pygame.K_c:
                    current_tool = "circle"

                elif event.key == pygame.K_s:
                    current_tool = "square"

                elif event.key == pygame.K_t:
                    current_tool = "text"

                elif event.key == pygame.K_e:
                    current_tool = "eraser"

                elif event.key == pygame.K_f:
                    current_tool = "fill"

                elif event.key == pygame.K_x:
                    clear_canvas(canvas)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[0] < TOOLBAR_WIDTH:
                    action, value = check_toolbar_click(event.pos)

                    if action == "tool":
                        current_tool = value
                        cancel_text()

                    elif action == "size":
                        brush_size = value

                    elif action == "color":
                        current_color = value

                elif is_on_canvas(event.pos):
                    canvas_pos = screen_to_canvas(event.pos)

                    if text_mode:
                        cancel_text()

                    if current_tool == "fill":
                        flood_fill(canvas, canvas_pos, current_color)

                    elif current_tool == "text":
                        text_mode = True
                        text_pos = canvas_pos
                        text_value = ""

                    else:
                        drawing = True
                        start_pos = canvas_pos
                        last_pos = canvas_pos

        elif event.type == pygame.MOUSEMOTION:
            if drawing and is_on_canvas(event.pos):
                canvas_pos = screen_to_canvas(event.pos)

                if current_tool == "pencil":
                    draw_pencil_line(canvas, last_pos, canvas_pos, current_color, brush_size)
                    last_pos = canvas_pos

                elif current_tool == "eraser":
                    draw_pencil_line(canvas, last_pos, canvas_pos, WHITE, brush_size)
                    last_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False

                if is_on_canvas(event.pos):
                    end_pos = screen_to_canvas(event.pos)

                    if current_tool in [
                        "line",
                        "rect",
                        "circle",
                        "square",
                        "right_triangle",
                        "equilateral_triangle",
                        "rhombus",
                    ]:
                        draw_shape(canvas, current_tool, start_pos, end_pos, current_color, brush_size)

                start_pos = None
                last_pos = None

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
