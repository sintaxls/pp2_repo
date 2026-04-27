import pygame as pg
import random
import sys
pg.init()

# SCREEN
WIDTH, HEIGHT = 600, 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("drive drunk!")

clock = pg.time.Clock()

# COLORS
white = (255, 255, 255)
dark_green = (0, 102, 0)
yellow_gr = (104, 104, 0)
grey = (98, 98, 98)

# ROAD SURF
main_surf = pg.Surface((600, 400), pg.SRCALPHA)

# CAR COORDINATES
cx = 0
cy = 200

cx2 = 0
cy2 = 100

# FPS
fps = 180
pg.draw.rect(main_surf, dark_green, (0, 0, 600, 400))

# Road lines
pg.draw.line(main_surf, yellow_gr, (0, 100), (600, 100), width=10)
pg.draw.line(main_surf, yellow_gr, (0, 300), (600, 300), width=10)

# Road
pg.draw.rect(main_surf, grey, (0, 105, 600, 191))
# ROAD SPEED
lspeed = 150

# CAR
car_path = 'TSIS3/assets/pixel_car_100.png'
car_img = pg.image.load(car_path)

car_path2 = 'TSIS3/assets/pixel_car2_100.png'
car_img2 = pg.image.load(car_path2)
# CAR SPEEDS
x_speed = 1
y_speed = 0.7

x_speed2 = 1
y_speed2 = 0.7

# ROAD TILE
tile_width = 110
tile_height = 400
tile_surf = pg.Surface((tile_width, tile_height), pg.SRCALPHA)
pg.draw.line(tile_surf, white, (0, 200), (90, 200), width=10)
x_line_offset = 0

# MENU
inmenu = True

GREEN = (84, 146, 23)
BLACK = (0, 0, 0)
YELLOW = (255, 189, 46)
WHITE = (240, 240, 240)
GRAY = (148, 148, 148)

font = pg.font.SysFont("Comic Sans MS", 30)
button_font = pg.font.SysFont("Comic Sans MS", 24)

# OBSTACLE LIST AND PROPS
obstacles = []
obstacle_width = 40
obstacle_height = 40
base_obstacle_speed = 150

coins = []
coin_width = 22
coin_height = 25


# MANHOLE
manhole = pg.image.load('TSIS3/assets/manhole.png')
manhole = pg.transform.scale(manhole, (65, 65))
score = 0
max_score = 0
last_score = 0

# COINS
coin = pg.image.load('TSIS3/assets/coin.png')
coin = pg.transform.scale(coin, (coin_width, coin_height))
coin2 = pg.image.load('TSIS3/assets/coin2.png')
coin2 = pg.transform.scale(coin2, (coin_width, coin_height))

blue_score = 0
pink_score = 0
last_blue_score = 0
last_pink_score = 0
blue_coins = 0
pink_coins = 0
last_blue_coins = 0
last_pink_coins = 0

# DIFFICULTY
difficulty = 0.5

# DRAW BUTTON
def draw_button(x, y, width, height, color, hover_color, text, text_color):
    mouse_x, mouse_y = pg.mouse.get_pos()
    clicked = False
    button_rect = pg.Rect(x, y, width, height)
    # HOVER
    if button_rect.collidepoint((mouse_x, mouse_y)):
        pg.draw.rect(screen, hover_color, button_rect, border_radius=15)
        if pg.mouse.get_pressed()[0]:
            clicked = True
    else:
        pg.draw.rect(screen, color, button_rect, border_radius=15)

    # CREATE BUTTON WITH TEXT
    text_surface = button_font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

    return clicked

setts = False
dragging = False
firstwin = None
def settings_page():
    global difficulty, dragging, inmenu, setts
    settings_running = True
    while settings_running:
        screen.fill(GREEN)
        text_surface = font.render("settings", True, BLACK)
        screen.blit(text_surface, (230, 30))
        # BACK
        if draw_button(20, 10, 95, 30, YELLOW, GRAY, "back", BLACK):
            inmenu = True
            setts = False
            return

        # DRAW SLIDER
        pg.draw.rect(screen, WHITE, (150, 150, 300, 10))
        slider_x = 150 + int(difficulty * 300)
        pg.draw.circle(screen, BLACK, (slider_x, 155), 10)

        # DIFFICULTY TEXT
        if 0 <= difficulty < 0.4:
            text_diff = 'easy'
        elif 0.4 <= difficulty < 0.7:
            text_diff = 'medium'
        else:
            text_diff = 'hard'

        # SHOW DIFFICULTY TEXT
        difficulty_text = button_font.render(f"difficulty: {text_diff}", True, BLACK)
        screen.blit(difficulty_text, (250, 180))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings_running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                # CHECK FOR CLICK ON CIRCLE
                if slider_x - 10 <= event.pos[0] <= slider_x + 10 and 145 <= event.pos[1] <= 165:
                    dragging = True
            elif event.type == pg.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pg.MOUSEMOTION and dragging:
                # CHANGE DIFFICULTY
                difficulty = max(0, min(1, (event.pos[0] - 150) / 300))
        pg.display.update()

######################################################################################################
running = True
while running:
    # MENU
    if inmenu and not setts:
        screen.fill(GREEN)

        text_surface = font.render("drive drunk!", True, BLACK)
        screen.blit(text_surface, (190, 30))

        text_max_score = font.render(f"max score: {int(max_score)}", True, BLACK)
        screen.blit(text_max_score, (190, 80))

        text_max_score = font.render(f"last score: {int(last_score)}", True, BLACK)
        screen.blit(text_max_score, (190, 120))

        text_blue_score = button_font.render(f"blue score: {int(last_blue_score)}", True, BLACK)
        screen.blit(text_blue_score, (190, 165))

        text_pink_score = button_font.render(f"pink score: {int(last_pink_score)}", True, BLACK)
        screen.blit(text_pink_score, (190, 195))

        text_blue_coins = button_font.render(f"blue coins: {int(last_blue_coins)}", True, BLACK)
        screen.blit(text_blue_coins, (190, 225))

        text_pink_coins = button_font.render(f"pink coins: {int(last_pink_coins)}", True, BLACK)
        screen.blit(text_pink_coins, (190, 255))

        if firstwin == True:
            text_max_score = font.render(f"blue wins!", True, BLACK)
            screen.blit(text_max_score, (190, 305))
        elif firstwin == False:
            text_max_score = font.render(f"pink wins!", True, BLACK)
            screen.blit(text_max_score, (190, 305))

        # START
        if draw_button(20, 180, 95, 30, YELLOW, GRAY, "start", BLACK):
            inmenu = False
        # SETTINGS
        if draw_button(20, 220, 95, 30, WHITE, GRAY, "settings", BLACK):
            setts = True
        # QUIT
        if draw_button(20, 260, 95, 30, WHITE, GRAY, "quit", BLACK):
            sys.exit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        pg.display.update()

    # GAME
    elif not inmenu and not setts:
        screen.fill((0, 0, 0))
        screen.blit(main_surf, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # ROAD MOVEMENT
        x_line_offset = (x_line_offset + lspeed / fps / (1.05 - difficulty)) % tile_width
        for i in range(-1, WIDTH // tile_width + 2):
            screen.blit(tile_surf, (i * tile_width - x_line_offset, 0))

        # CAR MOVEMENT
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and cy > -25:
            cy -= y_speed
        elif keys[pg.K_DOWN]and cy < WIDTH - 270:
            cy += y_speed

        if keys[pg.K_LEFT] and cx > -25:
            cx -= x_speed
        elif keys[pg.K_RIGHT] and cx < WIDTH - 70:
            cx += x_speed

        # CAR 2
        if keys[pg.K_w] and cy2 > -25:
            cy2 -= y_speed
        elif keys[pg.K_s] and cy2 < WIDTH - 270:
            cy2 += y_speed

        if  keys[pg.K_a] and cx2 > -25:
            cx2 -= x_speed
        elif keys[pg.K_d] and cx2 < WIDTH - 70:
            cx2 += x_speed

        # CAR RECTS
        car_rect = car_img.get_rect(topleft=(cx+10, cy+45))
        car_rect.width = 80
        car_rect.height = 20

        car_rect2 = car_img2.get_rect(topleft=(cx2+10, cy2+45))
        car_rect2.width = 80
        car_rect2.height = 20

        # TOP RECT
        #car_top_rect = car_img.get_rect(topleft=(cx+25, cy+30))
        #car_top_rect.width = 40
        #car_top_rect.height = 10

        # DRAW RECTS
        # pg.draw.rect(screen, (255, 0, 0), car_rect, 2)
        #pg.draw.rect(screen, (0, 255, 0), car_top_rect, 2)

        # OBSTACLE SPAWN
        if random.random() < difficulty * 0.02:
            obs_y = random.randint(105, 105 + 191 - obstacle_height)
            obstacles.append({
                'x': float(WIDTH),
                'y': obs_y,
                'width': obstacle_width,
                'height': obstacle_height
            })

        # COIN SPAWN
        if random.random() < difficulty * 0.02:
            coin_y = random.randint(105, 105 + 191 - coin_height)
            coin_value = 1
            if random.randint(1, 5) == 1:
                coin_value = 2

            coin_rect = pg.Rect(WIDTH, coin_y, coin_width, coin_height)
            can_spawn = True
            for obstacle in obstacles:
                obstacle_rect = pg.Rect(obstacle['x'] - 15, obstacle['y'] - 15, 65, 65)
                if coin_rect.colliderect(obstacle_rect):
                    can_spawn = False

            if can_spawn:
                coins.append({
                    'x': float(WIDTH),
                    'y': coin_y,
                    'width': coin_width,
                    'height': coin_height,
                    'value': coin_value
                })

        # MOVE OBSTACLE
        obstacle_speed = base_obstacle_speed / fps / (1.05 - difficulty)
        for obstacle in obstacles:
            obstacle['x'] -= obstacle_speed
            obstacle_rect = pg.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
            # pg.draw.rect(screen, (255, 0, 0), obstacle_rect)
            # DRAW MANHOLE
            screen.blit(manhole, (obstacle['x']-15, obstacle['y']-15))

            # COLLISION
            if car_rect.colliderect(obstacle_rect): #or car_top_rect.colliderect(obstacle_rect):
                inmenu = True
                obstacles = []
                coins = []
                last_blue_score = blue_score
                last_pink_score = pink_score
                last_blue_coins = blue_coins
                last_pink_coins = pink_coins
                last_score = score
                score = 0
                blue_score = 0
                pink_score = 0
                blue_coins = 0
                pink_coins = 0
                cx = 0
                cy = 200

                cx2 = 0
                cy2 = 100
                firstwin = False

            if car_rect2.colliderect(obstacle_rect): #or car_top_rect.colliderect(obstacle_rect):
                inmenu = True
                obstacles = []
                coins = []
                last_blue_score = blue_score
                last_pink_score = pink_score
                last_blue_coins = blue_coins
                last_pink_coins = pink_coins
                last_score = score
                score = 0
                blue_score = 0
                pink_score = 0
                blue_coins = 0
                pink_coins = 0
                cx = 0
                cy = 200
                cx2 = 0
                cy2 = 100
                firstwin = True

            # ADD SCORE, REMOVE OBSTACLE
            if obstacle_rect.x + obstacle['width'] < 0:
                obstacles.remove(obstacle)
                if 50 < cy < 250:
                    blue_score += 2
                if 50 < cy2 < 250:
                    pink_score += 2
                score = blue_score + pink_score
                if max_score < score:
                    max_score = score

        # MOVE COINS
        for one_coin in coins:
            one_coin['x'] -= obstacle_speed
            coin_rect = pg.Rect(one_coin['x'], one_coin['y'], one_coin['width'], one_coin['height'])

            if one_coin['value'] == 2:
                screen.blit(coin2, (one_coin['x'], one_coin['y']))
            else:
                screen.blit(coin, (one_coin['x'], one_coin['y']))

            if car_rect.colliderect(coin_rect):
                blue_coins += one_coin['value']
                blue_score += one_coin['value']
                score = blue_score + pink_score
                coins.remove(one_coin)
            elif car_rect2.colliderect(coin_rect):
                pink_coins += one_coin['value']
                pink_score += one_coin['value']
                score = blue_score + pink_score
                coins.remove(one_coin)
            elif coin_rect.x + one_coin['width'] < 0:
                coins.remove(one_coin)

            if max_score < score:
                max_score = score

        # MINUS SCORE FOR CHEATING
        if cy < 50 or cy > 250:
            blue_score -= (2 / fps) * (difficulty * 10)

        if cy2 < 50 or cy2 > 250:
            pink_score -= (2 / fps) * (difficulty * 10)

        score = blue_score + pink_score

        # BACK BUTTON
        if draw_button(20, 10, 95, 30, YELLOW, GRAY, "back", BLACK):
            inmenu = True
            obstacles = []
            coins = []
            last_blue_score = blue_score
            last_pink_score = pink_score
            last_blue_coins = blue_coins
            last_pink_coins = pink_coins
            last_score = score
            score = 0
            blue_score = 0
            pink_score = 0
            blue_coins = 0
            pink_coins = 0
            cx = 0
            cy = 200

        # SHOW SCORE
        score_text = button_font.render(f"blue score: {int(blue_score)}", True, YELLOW)
        screen.blit(score_text, (390, 10))

        score_text = button_font.render(f"pink score: {int(pink_score)}", True, YELLOW)
        screen.blit(score_text, (390, 40))

        # DRAW CAR
        screen.blit(car_img, (cx, cy))
        screen.blit(car_img2, (cx2, cy2))

        pg.display.flip()
        clock.tick(fps)

    else:
        settings_page()

pg.quit()
