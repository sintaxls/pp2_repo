import pygame as pg
pg.init()

WIDTH = 800
HEIGHT = 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("red ball entertainment")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_radius = 25
ball_speed = 600

clock = pg.time.Clock()
running = True
fps = 60
move_speed = ball_speed / fps

while running:
    clock.tick(fps)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        ball_x -= move_speed
    if keys[pg.K_RIGHT]:
        ball_x += move_speed
    if keys[pg.K_UP]:
        ball_y -= move_speed
    if keys[pg.K_DOWN]:
        ball_y += move_speed

    ball_x = max(ball_radius, min(WIDTH - ball_radius, ball_x))
    ball_y = max(ball_radius, min(HEIGHT - ball_radius, ball_y))
    
    screen.fill(WHITE)
    pg.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pg.display.flip()

pg.quit()