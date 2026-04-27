import pygame as pg
import random
import sys
import json
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
top10 = False

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

powerups = []
power_width = 30
power_height = 30


# MANHOLE
manhole = pg.image.load('TSIS3/assets/manhole.png')
manhole = pg.transform.scale(manhole, (65, 65))
traffic_car = pg.image.load('TSIS3/assets/pixel_car3_100.png')
score = 0
max_score = 0
last_score = 0
distance = 0
last_distance = 0

# COINS
coin = pg.image.load('TSIS3/assets/coin.png')
coin = pg.transform.scale(coin, (coin_width, coin_height))
coin2 = pg.image.load('TSIS3/assets/coin2.png')
coin2 = pg.transform.scale(coin2, (coin_width, coin_height))

# POWERUPS
nitro = pg.image.load('TSIS3/assets/nitro.png')
nitro = pg.transform.scale(nitro, (power_width, power_height))
shield = pg.image.load('TSIS3/assets/shield.png')
shield = pg.transform.scale(shield, (power_width, power_height))
repair = pg.image.load('TSIS3/assets/repair.png')
repair = pg.transform.scale(repair, (power_width, power_height))

blue_score = 0
pink_score = 0
last_blue_score = 0
last_pink_score = 0
blue_coins = 0
pink_coins = 0
last_blue_coins = 0
last_pink_coins = 0

blue_nitro_time = 0
pink_nitro_time = 0
blue_shield_time = 0
pink_shield_time = 0
blue_repair_time = 0
pink_repair_time = 0
blue_shield = 0
pink_shield = 0
blue_repair = 0
pink_repair = 0

# DIFFICULTY
settings_file = 'TSIS3/settings.json'
leaderboard_file = 'TSIS3/leaderboard.json'

def load_settings():
    try:
        file = open(settings_file, 'r')
        data = json.load(file)
        file.close()
        return data.get('difficulty', 0.5)
    except:
        return 0.5

def save_settings():
    file = open(settings_file, 'w')
    json.dump({'difficulty': difficulty}, file)
    file.close()

def load_leaderboard():
    try:
        file = open(leaderboard_file, 'r')
        data = json.load(file)
        file.close()
        if type(data) == list:
            return data
        return data.get('scores', [])
    except:
        return []

def save_leaderboard():
    scores = load_leaderboard()
    scores.append({'name': blue_name, 'score': int(blue_score), 'distance': round(distance, 2)})
    scores.append({'name': pink_name, 'score': int(pink_score), 'distance': round(distance, 2)})
    scores = sorted(scores, key=lambda item: (item['score'], item['distance']), reverse=True)
    scores = scores[:10]
    file = open(leaderboard_file, 'w')
    json.dump(scores, file)
    file.close()

difficulty = load_settings()

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

def draw_text_box(x, y, width, height, text, active):
    if active:
        color = YELLOW
    else:
        color = WHITE
    pg.draw.rect(screen, color, (x, y, width, height), border_radius=8)
    pg.draw.rect(screen, BLACK, (x, y, width, height), 2, border_radius=8)
    text_surface = button_font.render(text, True, BLACK)
    screen.blit(text_surface, (x + 10, y - 1))

def top10_page():
    global top10, inmenu, running
    while top10:
        screen.fill(GREEN)
        text_surface = font.render("top 10", True, BLACK)
        screen.blit(text_surface, (245, 25))

        scores = load_leaderboard()
        y = 75
        scores = scores[:10]
        for i in range(len(scores)):
            item = scores[i]
            text = f"{i + 1}. {item['name']}  {item['score']}  {item['distance']} km"
            score_text = button_font.render(text, True, BLACK)
            screen.blit(score_text, (80, y))
            y += 28

        if draw_button(20, 10, 95, 30, YELLOW, GRAY, "back", BLACK):
            top10 = False
            inmenu = True
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                top10 = False
                running = False
                return

        pg.display.update()

setts = False
dragging = False
firstwin = None
active_name = 0
blue_name = "player 1"
pink_name = "player 2"
def settings_page():
    global difficulty, dragging, inmenu, setts
    settings_running = True
    while settings_running:
        screen.fill(GREEN)
        text_surface = font.render("settings", True, BLACK)
        screen.blit(text_surface, (230, 30))
        # BACK
        if draw_button(20, 10, 95, 30, YELLOW, GRAY, "back", BLACK):
            save_settings()
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
                save_settings()
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
    if inmenu and not setts and not top10:
        screen.fill(GREEN)

        text_surface = font.render("drive drunk!", True, BLACK)
        screen.blit(text_surface, (190, 30))

        text_max_score = font.render(f"max score: {int(max_score)}", True, BLACK)
        screen.blit(text_max_score, (190, 70))

        text_max_score = font.render(f"last score: {int(last_score)}", True, BLACK)
        screen.blit(text_max_score, (190, 105))

        text_distance = button_font.render(f"last distance: {round(last_distance, 2)} km", True, BLACK)
        screen.blit(text_distance, (190, 140))

        text_blue_score = button_font.render(f"blue score: {int(last_blue_score)}", True, BLACK)
        screen.blit(text_blue_score, (190, 175))

        text_pink_score = button_font.render(f"pink score: {int(last_pink_score)}", True, BLACK)
        screen.blit(text_pink_score, (190, 205))

        text_blue_coins = button_font.render(f"blue coins: {int(last_blue_coins)}", True, BLACK)
        screen.blit(text_blue_coins, (190, 235))

        text_pink_coins = button_font.render(f"pink coins: {int(last_pink_coins)}", True, BLACK)
        screen.blit(text_pink_coins, (190, 265))

        if firstwin == True:
            text_max_score = font.render(f"blue wins!", True, BLACK)
            screen.blit(text_max_score, (190, 315))
        elif firstwin == False:
            text_max_score = font.render(f"pink wins!", True, BLACK)
            screen.blit(text_max_score, (190, 315))

        player_text = button_font.render("blue name", True, BLACK)
        screen.blit(player_text, (20, 70))
        draw_text_box(20, 95, 140, 30, blue_name, active_name == 1)

        player_text = button_font.render("pink name", True, BLACK)
        screen.blit(player_text, (20, 135))
        draw_text_box(20, 160, 140, 30, pink_name, active_name == 2)

        # START
        if draw_button(20, 205, 95, 30, YELLOW, GRAY, "start", BLACK):
            if blue_name == "":
                blue_name = "player 1"
            if pink_name == "":
                pink_name = "player 2"
            distance = 0
            inmenu = False
        # SETTINGS
        if draw_button(20, 245, 95, 30, WHITE, GRAY, "settings", BLACK):
            setts = True
        # TOP 10
        if draw_button(20, 285, 95, 30, WHITE, GRAY, "top 10", BLACK):
            top10 = True
        # QUIT
        if draw_button(20, 325, 95, 30, WHITE, GRAY, "quit", BLACK):
            sys.exit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if 20 <= event.pos[0] <= 160 and 95 <= event.pos[1] <= 125:
                    active_name = 1
                elif 20 <= event.pos[0] <= 160 and 160 <= event.pos[1] <= 190:
                    active_name = 2
                else:
                    active_name = 0
            elif event.type == pg.KEYDOWN:
                if active_name == 1:
                    if event.key == pg.K_BACKSPACE:
                        blue_name = blue_name[:-1]
                    elif len(blue_name) < 10:
                        blue_name += event.unicode.lower()
                elif active_name == 2:
                    if event.key == pg.K_BACKSPACE:
                        pink_name = pink_name[:-1]
                    elif len(pink_name) < 10:
                        pink_name += event.unicode.lower()

        pg.display.update()

    # TOP 10
    elif top10:
        top10_page()

    # GAME
    elif not inmenu and not setts and not top10:
        screen.fill((0, 0, 0))
        screen.blit(main_surf, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # ROAD MOVEMENT
        x_line_offset = (x_line_offset + lspeed / fps / (1.05 - difficulty)) % tile_width
        distance += (lspeed / fps / (1.05 - difficulty)) / 1000
        for i in range(-1, WIDTH // tile_width + 2):
            screen.blit(tile_surf, (i * tile_width - x_line_offset, 0))

        # CAR MOVEMENT
        now = pg.time.get_ticks()
        blue_speed = 1
        pink_speed = 1
        if blue_nitro_time > now:
            blue_speed = 1.5
        if pink_nitro_time > now:
            pink_speed = 1.5

        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and cy > -25:
            cy -= y_speed * blue_speed
        elif keys[pg.K_DOWN]and cy < WIDTH - 270:
            cy += y_speed * blue_speed

        if keys[pg.K_LEFT] and cx > -25:
            cx -= x_speed * blue_speed
        elif keys[pg.K_RIGHT] and cx < WIDTH - 70:
            cx += x_speed * blue_speed

        # CAR 2
        if keys[pg.K_w] and cy2 > -25:
            cy2 -= y_speed * pink_speed
        elif keys[pg.K_s] and cy2 < WIDTH - 270:
            cy2 += y_speed * pink_speed

        if  keys[pg.K_a] and cx2 > -25:
            cx2 -= x_speed * pink_speed
        elif keys[pg.K_d] and cx2 < WIDTH - 70:
            cx2 += x_speed * pink_speed

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
            if random.random() < 0.7:
                obs_y = random.randint(105, 105 + 191 - obstacle_height)
                obstacles.append({
                    'x': float(WIDTH),
                    'y': obs_y,
                    'width': obstacle_width,
                    'height': obstacle_height,
                    'type': 'manhole'
                })
            else:
                obs_y = random.randint(105, 105 + 191 - 20)
                obstacles.append({
                    'x': float(WIDTH),
                    'y': obs_y,
                    'width': 80,
                    'height': 20,
                    'type': 'traffic'
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
                if obstacle['type'] == 'manhole':
                    obstacle_rect = pg.Rect(obstacle['x'] - 15, obstacle['y'] - 15, 65, 65)
                else:
                    obstacle_rect = pg.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
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

        # POWERUP SPAWN
        if random.random() < difficulty * 0.01:
            power_y = random.randint(105, 105 + 191 - power_height)
            power_type = random.choice(['nitro', 'shield', 'repair'])

            power_rect = pg.Rect(WIDTH, power_y, power_width, power_height)
            can_spawn = True
            for obstacle in obstacles:
                if obstacle['type'] == 'manhole':
                    obstacle_rect = pg.Rect(obstacle['x'] - 15, obstacle['y'] - 15, 65, 65)
                else:
                    obstacle_rect = pg.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
                if power_rect.colliderect(obstacle_rect):
                    can_spawn = False

            if can_spawn:
                powerups.append({
                    'x': float(WIDTH),
                    'y': power_y,
                    'width': power_width,
                    'height': power_height,
                    'type': power_type
                })

        # MOVE OBSTACLE
        obstacle_speed = base_obstacle_speed / fps / (1.05 - difficulty)
        for obstacle in obstacles:
            obstacle['x'] -= obstacle_speed
            obstacle_rect = pg.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
            # pg.draw.rect(screen, (255, 0, 0), obstacle_rect)
            # DRAW OBSTACLE
            if obstacle['type'] == 'manhole':
                screen.blit(manhole, (obstacle['x']-15, obstacle['y']-15))
            else:
                screen.blit(traffic_car, (obstacle['x']-10, obstacle['y']-45))

            # COLLISION
            if car_rect.colliderect(obstacle_rect): #or car_top_rect.colliderect(obstacle_rect):
                if blue_repair == 1 and blue_repair_time > now and obstacle['type'] == 'manhole':
                    blue_repair = 0
                    obstacles.remove(obstacle)
                    continue
                elif blue_shield == 1 and blue_shield_time > now:
                    blue_shield = 0
                    obstacles.remove(obstacle)
                    continue
                else:
                    inmenu = True
                    obstacles = []
                    coins = []
                    powerups = []
                    last_blue_score = blue_score
                    last_pink_score = pink_score
                    last_blue_coins = blue_coins
                    last_pink_coins = pink_coins
                    last_score = score
                    last_distance = distance
                    save_leaderboard()
                    score = 0
                    distance = 0
                    blue_score = 0
                    pink_score = 0
                    blue_coins = 0
                    pink_coins = 0
                    blue_nitro_time = 0
                    pink_nitro_time = 0
                    blue_shield_time = 0
                    pink_shield_time = 0
                    blue_repair_time = 0
                    pink_repair_time = 0
                    blue_shield = 0
                    pink_shield = 0
                    blue_repair = 0
                    pink_repair = 0
                    cx = 0
                    cy = 200

                    cx2 = 0
                    cy2 = 100
                    firstwin = False
                    continue

            if car_rect2.colliderect(obstacle_rect): #or car_top_rect.colliderect(obstacle_rect):
                if pink_repair == 1 and pink_repair_time > now and obstacle['type'] == 'manhole':
                    pink_repair = 0
                    obstacles.remove(obstacle)
                    continue
                elif pink_shield == 1 and pink_shield_time > now:
                    pink_shield = 0
                    obstacles.remove(obstacle)
                    continue
                else:
                    inmenu = True
                    obstacles = []
                    coins = []
                    powerups = []
                    last_blue_score = blue_score
                    last_pink_score = pink_score
                    last_blue_coins = blue_coins
                    last_pink_coins = pink_coins
                    last_score = score
                    last_distance = distance
                    save_leaderboard()
                    score = 0
                    distance = 0
                    blue_score = 0
                    pink_score = 0
                    blue_coins = 0
                    pink_coins = 0
                    blue_nitro_time = 0
                    pink_nitro_time = 0
                    blue_shield_time = 0
                    pink_shield_time = 0
                    blue_repair_time = 0
                    pink_repair_time = 0
                    blue_shield = 0
                    pink_shield = 0
                    blue_repair = 0
                    pink_repair = 0
                    cx = 0
                    cy = 200
                    cx2 = 0
                    cy2 = 100
                    firstwin = True
                    continue

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

        # MOVE POWERUPS
        for powerup in powerups:
            powerup['x'] -= obstacle_speed
            power_rect = pg.Rect(powerup['x'], powerup['y'], powerup['width'], powerup['height'])

            if powerup['type'] == 'nitro':
                screen.blit(nitro, (powerup['x'], powerup['y']))
            elif powerup['type'] == 'shield':
                screen.blit(shield, (powerup['x'], powerup['y']))
            else:
                screen.blit(repair, (powerup['x'], powerup['y']))

            if car_rect.colliderect(power_rect):
                if powerup['type'] == 'nitro':
                    blue_nitro_time = now + 3000
                elif powerup['type'] == 'shield':
                    blue_shield_time = now + 3000
                    blue_shield = 1
                else:
                    blue_repair_time = now + 5000
                    blue_repair = 1
                powerups.remove(powerup)
            elif car_rect2.colliderect(power_rect):
                if powerup['type'] == 'nitro':
                    pink_nitro_time = now + 3000
                elif powerup['type'] == 'shield':
                    pink_shield_time = now + 3000
                    pink_shield = 1
                else:
                    pink_repair_time = now + 5000
                    pink_repair = 1
                powerups.remove(powerup)
            elif power_rect.x + powerup['width'] < 0:
                powerups.remove(powerup)

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
            powerups = []
            last_blue_score = blue_score
            last_pink_score = pink_score
            last_blue_coins = blue_coins
            last_pink_coins = pink_coins
            last_score = score
            last_distance = distance
            save_leaderboard()
            score = 0
            distance = 0
            blue_score = 0
            pink_score = 0
            blue_coins = 0
            pink_coins = 0
            blue_nitro_time = 0
            pink_nitro_time = 0
            blue_shield_time = 0
            pink_shield_time = 0
            blue_repair_time = 0
            pink_repair_time = 0
            blue_shield = 0
            pink_shield = 0
            blue_repair = 0
            pink_repair = 0
            cx = 0
            cy = 200

        # SHOW SCORE
        score_text = button_font.render(f"blue score: {int(blue_score)}", True, YELLOW)
        screen.blit(score_text, (390, 10))

        score_text = button_font.render(f"pink score: {int(pink_score)}", True, YELLOW)
        screen.blit(score_text, (390, 40))

        distance_text = button_font.render(f"distance: {round(distance, 2)} km", True, YELLOW)
        screen.blit(distance_text, (390, 70))

        # DRAW CAR
        screen.blit(car_img, (cx, cy))
        screen.blit(car_img2, (cx2, cy2))

        pg.display.flip()
        clock.tick(fps)

    else:
        settings_page()

pg.quit()
