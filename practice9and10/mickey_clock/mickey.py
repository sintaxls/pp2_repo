from datetime import datetime
from pathlib import Path

import pygame as pg

pg.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("mikimausklok")
clock = pg.time.Clock()

BASE = Path(__file__).resolve().parent
IMGDIR = BASE / "images"


def load_image(filename):
    image_path = IMGDIR / filename
    return pg.image.load(image_path).convert_alpha()


def blit_rotated_hand(surface, image, center, angle):
    rotated_image = pg.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=center)
    surface.blit(rotated_image, rotated_rect)


clock_image = load_image("clock.png")
mickey_image = load_image("mickey.png")
minute_hand = load_image("hourshand_c.png")
second_hand = load_image("minuteshand_c.png")

clock_rect = clock_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
clock_center = clock_rect.center
mickey_rect = mickey_image.get_rect(center=clock_center)

running = True
while running:
    clock.tick(FPS)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    now = datetime.now()
    minute_angle = (now.minute + now.second / 60) * 6
    second_angle = now.second * 6

    screen.blit(clock_image, clock_rect)
    screen.blit(mickey_image, mickey_rect)
    blit_rotated_hand(surface=screen, image=minute_hand, center=clock_center, angle=-minute_angle)
    blit_rotated_hand(surface=screen, image=second_hand, center=clock_center, angle=-second_angle)
    pg.display.flip()

pg.quit()