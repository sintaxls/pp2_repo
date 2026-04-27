from datetime import datetime

import pygame


WIDTH, HEIGHT = 1100, 560
TOOLBAR_HEIGHT = 56
BACKGROUND_COLOR = (255, 255, 255)
PANEL_COLOR = (35, 35, 35)
PANEL_ACTIVE = (80, 120, 210)
TEXT_COLOR = (255, 255, 255)

COLORS = [
    ("black", (0, 0, 0), pygame.K_k),
    ("red", (220, 40, 40), pygame.K_r),
    ("green", (40, 160, 70), pygame.K_g),
    ("blue", (45, 100, 220), pygame.K_b),
]

STROKE_SIZES = [
    ("small", 2, pygame.K_1),
    ("medium", 5, pygame.K_2),
    ("large", 10, pygame.K_3),
]

TOOLS = [
    ("pencil", "pencil", pygame.K_p),
    ("line", "line", pygame.K_l),
    ("fill", "fill", pygame.K_f),
    ("text", "text", pygame.K_x),
    ("rectangle", "rect", pygame.K_t),
    ("circle", "circle", pygame.K_c),
    ("right_triangle", "r tri", pygame.K_y),
    ("equilateral_triangle", "e tri", pygame.K_u),
    ("rhombus", "rhomb", pygame.K_h),
    ("eraser", "eraser", pygame.K_e),
]


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "paint: p pencil, l line, f fill, x text, 1 small, 2 medium, 3 large"
    )
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    text_font = pygame.font.SysFont(None, 32)

    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(BACKGROUND_COLOR)

    stroke_size = 5
    tool = "pencil"
    color = COLORS[0][1]
    drawing = False
    start_pos = None
    last_pos = None
    current_pos = None
    text_active = False
    text_pos = None
    text_value = ""

    tool_buttons, color_buttons, size_buttons = build_toolbar_hitboxes(font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if text_active:
                    if event.key == pygame.K_RETURN:
                        draw_text(canvas, text_font, text_value, text_pos, color)
                        text_active = False
                        text_value = ""
                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_value = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]
                    elif event.unicode:
                        text_value += event.unicode
                    continue

                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    save_canvas(canvas)
                    continue

                selected_tool = tool_from_key(event.key)
                selected_size = size_from_key(event.key)
                selected_color = color_from_key(event.key)

                if selected_tool is not None:
                    tool = selected_tool
                elif selected_size is not None:
                    stroke_size = selected_size
                elif selected_color is not None:
                    color = selected_color
                    if tool == "eraser":
                        tool = "pencil"
                elif event.key == pygame.K_MINUS:
                    stroke_size = previous_size(stroke_size)
                elif event.key == pygame.K_EQUALS:
                    stroke_size = next_size(stroke_size)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4, 5):
                    stroke_size = resize_brush(stroke_size, event.button)
                    continue

                if event.button != 1:
                    continue

                if event.pos[1] < TOOLBAR_HEIGHT:
                    selected_tool, selected_color, selected_size = handle_toolbar_click(
                        event.pos, tool_buttons, color_buttons, size_buttons
                    )
                    if selected_tool is not None:
                        tool = selected_tool
                    if selected_color is not None:
                        color = selected_color
                        if tool == "eraser":
                            tool = "pencil"
                    if selected_size is not None:
                        stroke_size = selected_size
                    continue

                drawing = True
                start_pos = to_canvas_pos(event.pos)
                last_pos = start_pos
                current_pos = start_pos

                if tool == "fill":
                    flood_fill(canvas, start_pos, color)
                    drawing = False
                elif tool == "text":
                    text_active = True
                    text_pos = start_pos
                    text_value = ""
                    drawing = False
                elif tool == "pencil":
                    draw_pencil_line(canvas, start_pos, start_pos, stroke_size, color)
                elif tool == "eraser":
                    draw_stroke(
                        canvas, start_pos, start_pos, stroke_size, active_color(tool, color)
                    )

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button != 1 or not drawing:
                    continue

                end_pos = to_canvas_pos(event.pos)
                if tool == "line":
                    draw_pencil_line(canvas, start_pos, end_pos, stroke_size, color)
                elif tool == "rectangle":
                    draw_rectangle(canvas, start_pos, end_pos, color, stroke_size)
                elif tool == "circle":
                    draw_circle(canvas, start_pos, end_pos, color, stroke_size)
                elif tool == "right_triangle":
                    draw_polygon(
                        canvas, right_triangle_points(start_pos, end_pos), color, stroke_size
                    )
                elif tool == "equilateral_triangle":
                    draw_polygon(
                        canvas, equilateral_triangle_points(start_pos, end_pos), color, stroke_size
                    )
                elif tool == "rhombus":
                    draw_polygon(canvas, rhombus_points(start_pos, end_pos), color, stroke_size)

                drawing = False
                start_pos = None
                last_pos = None
                current_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                current_pos = to_canvas_pos(event.pos)
                if tool == "pencil":
                    draw_pencil_line(canvas, last_pos, current_pos, stroke_size, color)
                    last_pos = current_pos
                elif tool == "eraser":
                    draw_stroke(
                        canvas, last_pos, current_pos, stroke_size, active_color(tool, color)
                    )
                    last_pos = current_pos

        screen.fill(PANEL_COLOR)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        if drawing and start_pos is not None and current_pos is not None:
            draw_shape_preview(screen, tool, start_pos, current_pos, color, stroke_size)

        if text_active:
            draw_text_preview(screen, text_font, text_value, text_pos, color)

        draw_toolbar(
            screen, font, tool_buttons, color_buttons, size_buttons, tool, color, stroke_size
        )
        pygame.display.flip()
        clock.tick(60)


def build_toolbar_hitboxes(font):
    # here we build tool buttons
    tool_buttons = []
    x = 8
    for tool_name, label, _ in TOOLS:
        width = font.size(label)[0] + 18
        rect = pygame.Rect(x, 8, width, 32)
        tool_buttons.append((rect, tool_name, label))
        x += width + 6

    # here we build color buttons
    color_buttons = []
    x += 10
    for name, rgb, _ in COLORS:
        rect = pygame.Rect(x, 12, 24, 24)
        color_buttons.append((rect, name, rgb))
        x += 30

    # here we build size buttons
    size_buttons = []
    x += 10
    for name, size, _ in STROKE_SIZES:
        width = font.size(name)[0] + 18
        rect = pygame.Rect(x, 12, width, 32)
        size_buttons.append((rect, name, size))
        x += width + 6

    return tool_buttons, color_buttons, size_buttons


def draw_toolbar(screen, font, tool_buttons, color_buttons, size_buttons, tool, color, stroke_size):
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    for rect, tool_name, label in tool_buttons:
        fill = PANEL_ACTIVE if tool_name == tool else (58, 58, 58)
        pygame.draw.rect(screen, fill, rect, border_radius=4)
        pygame.draw.rect(screen, (120, 120, 120), rect, 1, border_radius=4)
        text = font.render(label, True, TEXT_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))

    for rect, _, rgb in color_buttons:
        pygame.draw.rect(screen, rgb, rect, border_radius=3)
        border = (255, 255, 255) if rgb == color else (120, 120, 120)
        pygame.draw.rect(screen, border, rect, 3 if rgb == color else 1, border_radius=3)

    for rect, name, size in size_buttons:
        fill = PANEL_ACTIVE if size == stroke_size else (58, 58, 58)
        pygame.draw.rect(screen, fill, rect, border_radius=4)
        pygame.draw.rect(screen, (120, 120, 120), rect, 1, border_radius=4)
        text = font.render(name, True, TEXT_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))

    size_text = font.render(f"size {stroke_size}", True, TEXT_COLOR)
    screen.blit(size_text, (WIDTH - size_text.get_width() - 12, 16))


def handle_toolbar_click(pos, tool_buttons, color_buttons, size_buttons):
    for rect, tool_name, _ in tool_buttons:
        if rect.collidepoint(pos):
            return tool_name, None, None

    for rect, _, rgb in color_buttons:
        if rect.collidepoint(pos):
            return None, rgb, None

    for rect, _, size in size_buttons:
        if rect.collidepoint(pos):
            return None, None, size

    return None, None, None


def tool_from_key(key):
    for tool_name, _, shortcut in TOOLS:
        if key == shortcut:
            return tool_name
    return None


def color_from_key(key):
    for _, rgb, shortcut in COLORS:
        if key == shortcut:
            return rgb
    return None


def size_from_key(key):
    for _, size, shortcut in STROKE_SIZES:
        if key == shortcut:
            return size
    return None


def resize_brush(stroke_size, mouse_button):
    if mouse_button == 4:
        return next_size(stroke_size)
    if mouse_button == 5:
        return previous_size(stroke_size)
    return stroke_size


def next_size(stroke_size):
    sizes = [size for _, size, _ in STROKE_SIZES]
    index = sizes.index(stroke_size)
    index = min(index + 1, len(sizes) - 1)
    return sizes[index]


def previous_size(stroke_size):
    sizes = [size for _, size, _ in STROKE_SIZES]
    index = sizes.index(stroke_size)
    index = max(index - 1, 0)
    return sizes[index]


def to_canvas_pos(pos):
    x = max(0, min(WIDTH - 1, pos[0]))
    y = max(0, min(HEIGHT - TOOLBAR_HEIGHT - 1, pos[1] - TOOLBAR_HEIGHT))
    return x, y


def active_color(tool, color):
    if tool == "eraser":
        return BACKGROUND_COLOR
    return color


def draw_stroke(surface, start, end, radius, color):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    steps = max(abs(dx), abs(dy), 1)

    for i in range(steps + 1):
        progress = i / steps
        x = round(start[0] + dx * progress)
        y = round(start[1] + dy * progress)
        pygame.draw.circle(surface, color, (x, y), radius)


def draw_pencil_line(surface, start, end, width, color):
    pygame.draw.line(surface, color, start, end, max(1, width))


def draw_rectangle(surface, start, end, color, width):
    rect = rect_from_points(start, end)
    if rect.width == 0 or rect.height == 0:
        return
    pygame.draw.rect(surface, color, rect, max(1, width))


def draw_circle(surface, start, end, color, width):
    rect = square_from_points(start, end)
    if rect.width == 0 or rect.height == 0:
        return
    pygame.draw.ellipse(surface, color, rect, max(1, width))


def draw_polygon(surface, points, color, width):
    if len(set(points)) < 3:
        return
    pygame.draw.polygon(surface, color, points, max(1, width))


def flood_fill(surface, start, color):
    width = surface.get_width()
    height = surface.get_height()
    old_color = surface.get_at(start)
    new_color = pygame.Color(color)

    if old_color == new_color:
        return

    stack = [start]
    while stack:
        x, y = stack.pop()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), new_color)
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))


def save_canvas(surface):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{timestamp}.png"
    pygame.image.save(surface, filename)


def draw_text(surface, font, text, pos, color):
    image = font.render(text, True, color)
    surface.blit(image, pos)


def draw_text_preview(screen, font, text, pos, color):
    x, y = pos
    y += TOOLBAR_HEIGHT
    image = font.render(text, True, color)
    screen.blit(image, (x, y))
    cursor_x = x + image.get_width() + 2
    pygame.draw.line(screen, color, (cursor_x, y), (cursor_x, y + font.get_height()), 1)


def draw_shape_preview(screen, tool, start, end, color, width):
    if tool == "line":
        start = (start[0], start[1] + TOOLBAR_HEIGHT)
        end = (end[0], end[1] + TOOLBAR_HEIGHT)
        draw_pencil_line(screen, start, end, width, color)
    elif tool == "rectangle":
        rect = rect_from_points(start, end).move(0, TOOLBAR_HEIGHT)
        pygame.draw.rect(screen, color, rect, max(1, width))
    elif tool == "circle":
        rect = square_from_points(start, end).move(0, TOOLBAR_HEIGHT)
        pygame.draw.ellipse(screen, color, rect, max(1, width))
    elif tool == "right_triangle":
        points = offset_points(right_triangle_points(start, end), 0, TOOLBAR_HEIGHT)
        draw_polygon(screen, points, color, width)
    elif tool == "equilateral_triangle":
        points = offset_points(equilateral_triangle_points(start, end), 0, TOOLBAR_HEIGHT)
        draw_polygon(screen, points, color, width)
    elif tool == "rhombus":
        points = offset_points(rhombus_points(start, end), 0, TOOLBAR_HEIGHT)
        draw_polygon(screen, points, color, width)


def rect_from_points(start, end):
    x1, y1 = start
    x2, y2 = end
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))


def square_from_points(start, end):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    x = x1 - side if x2 < x1 else x1
    y = y1 - side if y2 < y1 else y1
    return pygame.Rect(x, y, side, side)


def right_triangle_points(start, end):
    x1, y1 = start
    x2, y2 = end
    return [(x1, y1), (x1, y2), (x2, y2)]


def equilateral_triangle_points(start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    direction_x = -1 if dx < 0 else 1
    direction_y = -1 if dy < 0 else 1
    side = min(abs(dx), abs(dy) * 2 / 1.732)
    height = side * 0.866
    half_side = side / 2

    return [
        (round(x1), round(y1)),
        (round(x1 - direction_x * half_side), round(y1 + direction_y * height)),
        (round(x1 + direction_x * half_side), round(y1 + direction_y * height)),
    ]


def rhombus_points(start, end):
    rect = rect_from_points(start, end)
    if rect.width == 0 or rect.height == 0:
        return []

    center_x = rect.centerx
    center_y = rect.centery
    return [
        (center_x, rect.top),
        (rect.right, center_y),
        (center_x, rect.bottom),
        (rect.left, center_y),
    ]


def offset_points(points, dx, dy):
    return [(x + dx, y + dy) for x, y in points]


main()
