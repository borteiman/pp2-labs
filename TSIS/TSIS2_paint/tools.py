from collections import deque     #для заливки, очередь
from datetime import datetime     #для сохранения
from pathlib import Path          #папка созранения
import math                       #расчет расстояния между поз мыши
import pygame

from settings import SAVE_FOLDER, WHITE

#функции-инструменты

def draw_pencil_line(surface, start, end, color, size):
    # I draw many small circles between two mouse positions
    # This makes the pencil and eraser look round
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    distance = int(math.hypot(dx, dy))      #сколько кругов нарисовать между точками
    if distance == 0:
        pygame.draw.circle(surface, color, start, size)
        return

    for i in range(distance):
        x = int(x1 + dx * i / distance)
        y = int(y1 + dy * i / distance)
        pygame.draw.circle(surface, color, (x, y), size)



#1. Берём цвет пикселя, куда кликнули (old color)
#3. Все соседние пиксели такого же цвета меняем на new_color.
#4. Если пиксель другого цвета, значит это граница, дальше не идём.

def flood_fill(surface, start_pos, new_color):
    # Simple flood fill using get_at() and set_at(), as required in the task.
    width, height = surface.get_size()
    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    old_color = surface.get_at((x, y))
    fill_color = pygame.Color(new_color)

    if old_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), fill_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def save_canvas(canvas):
    # Timestamp keeps old saves safe from overwrite.
    folder = Path(SAVE_FOLDER)
    folder.mkdir(exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = folder / f"paint_{now}.png"

    pygame.image.save(canvas, str(filename))

    return filename


def draw_text(surface, text, position, color, font):
    # Text is rendered on canvas only after Enter.
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


def clear_canvas(surface):
    surface.fill(WHITE)
