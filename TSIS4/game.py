import random
import pygame
import db
from config import cw, cn, ww, hh


pygame.init()

win = pygame.display.set_mode((ww, hh))
pygame.display.set_caption("snake")
clk = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big = pygame.font.SysFont("arial", 42)

WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
GREEN = (40, 170, 70)
DARK = (20, 100, 35)
RED = (210, 55, 55)
YELLOW = (230, 185, 45)
BLUE = (55, 120, 200)
GRAY = (80, 80, 80)

foods = [
    (1, RED, 180),
    (2, YELLOW, 140),
    (3, BLUE, 100),
]


def txt(s, x, y, f=font, col=WHITE):
    t = f.render(s, True, col)
    win.blit(t, (x, y))


def btn(s, r):
    pygame.draw.rect(win, GRAY, r)
    pygame.draw.rect(win, WHITE, r, 2)
    t = font.render(s, True, WHITE)
    win.blit(t, (r.x + (r.w - t.get_width()) // 2, r.y + 12))


def new_food(sn):
    while True:
        x = random.randint(1, cn - 2)
        y = random.randint(1, cn - 2)
        if (x, y) not in sn:
            w, col, tm = random.choice(foods)
            return {"p": (x, y), "w": w, "c": col, "t": tm}


def draw(sn, fd, sc, lv, bs):
    win.fill(BLACK)
    # draw wall
    for x in range(cn):
        pygame.draw.rect(win, GRAY, (x * cw, 0, cw, cw))
        pygame.draw.rect(win, GRAY, (x * cw, (cn - 1) * cw, cw, cw))
    for y in range(cn):
        pygame.draw.rect(win, GRAY, (0, y * cw, cw, cw))
        pygame.draw.rect(win, GRAY, ((cn - 1) * cw, y * cw, cw, cw))

    # draw snake
    for i, p in enumerate(sn):
        col = DARK
        if i == 0:
            col = GREEN
        pygame.draw.rect(win, col, (p[0] * cw, p[1] * cw, cw, cw))

    # draw food
    pygame.draw.rect(win, fd["c"], (fd["p"][0] * cw, fd["p"][1] * cw, cw, cw))
    txt("score " + str(sc), 10, ww + 10)
    txt("level " + str(lv), 145, ww + 10)
    txt("best " + str(bs), 280, ww + 10)
    pygame.display.update()


def menu():
    name = ""
    r1 = pygame.Rect(160, 250, 180, 55)
    r2 = pygame.Rect(160, 320, 180, 55)
    while True:
        win.fill(BLACK)
        txt("snake", 190, 90, big)
        txt("username", 120, 170)
        pygame.draw.rect(win, GRAY, (120, 200, 260, 38))
        pygame.draw.rect(win, WHITE, (120, 200, 260, 38), 2)
        txt(name, 130, 207)
        btn("play", r1)
        btn("leaderboard", r2)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit", name
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif e.key == pygame.K_RETURN and name:
                    return "play", name
                elif len(name) < 50 and e.unicode.isprintable():
                    name += e.unicode.lower()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if r1.collidepoint(e.pos) and name:
                    return "play", name
                if r2.collidepoint(e.pos):
                    return "lead", name


def lead():
    r = pygame.Rect(170, 445, 160, 45)
    rows = db.top()
    while True:
        win.fill(BLACK)
        txt("leaderboard", 145, 35, big)
        y = 100
        if not rows:
            txt("no scores", 190, y)
        for i, a in enumerate(rows):
            s = str(i + 1) + ". " + a[0] + " " + str(a[1]) + " lv " + str(a[2])
            txt(s.lower(), 40, y)
            y += 32
        btn("back", r)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "menu"
            if e.type == pygame.MOUSEBUTTONDOWN and r.collidepoint(e.pos):
                return "menu"


def over(sc, lv):
    r1 = pygame.Rect(150, 280, 200, 55)
    r2 = pygame.Rect(150, 350, 200, 55)
    while True:
        win.fill(BLACK)
        txt("game over", 135, 110, big)
        txt("score " + str(sc), 190, 185)
        txt("level " + str(lv), 190, 220)
        btn("play again", r1)
        btn("menu", r2)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if r1.collidepoint(e.pos):
                    return "play"
                if r2.collidepoint(e.pos):
                    return "menu"


def run(name):
    sn = [(10, 10), (9, 10), (8, 10)]
    dx = 1
    dy = 0
    sc = 0
    lv = 1
    eat = 0
    sp = 8
    bs = db.best(name)
    fd = new_food(sn)
    done = False

    while not done:
        clk.tick(sp)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and dy != 1:
                    dx = 0
                    dy = -1
                if e.key == pygame.K_DOWN and dy != -1:
                    dx = 0
                    dy = 1
                if e.key == pygame.K_LEFT and dx != 1:
                    dx = -1
                    dy = 0
                if e.key == pygame.K_RIGHT and dx != -1:
                    dx = 1
                    dy = 0

        hd = (sn[0][0] + dx, sn[0][1] + dy)

        # check hit
        if hd[0] <= 0 or hd[0] >= cn - 1 or hd[1] <= 0 or hd[1] >= cn - 1:
            done = True
        if hd in sn[:-1]:
            done = True

        if done:
            break

        sn.insert(0, hd)
        if hd == fd["p"]:
            sc += fd["w"]
            eat += 1
            if eat % 4 == 0:
                lv += 1
                sp += 2
            fd = new_food(sn)
        else:
            sn.pop()

        # food timer
        fd["t"] -= 1
        if fd["t"] <= 0:
            fd = new_food(sn)

        draw(sn, fd, sc, lv, bs)

    db.save(name, sc, lv)
    return over(sc, lv)


def start():
    db.make_db()
    st = "menu"
    name = ""
    while st != "quit":
        if st == "menu":
            st, name = menu()
        elif st == "lead":
            st = lead()
        elif st == "play":
            if not name:
                st = "menu"
            else:
                st = run(name)
    pygame.quit()
