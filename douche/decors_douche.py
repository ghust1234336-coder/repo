"""Décors et petits personnages de l'épisode « douche »."""
import numpy as np
from pixel import *


# ---------- salle de bain ----------
def bathroom(c, t, water=0.0, tap_open=1.0):
    c[:] = TILE
    # carrelage : joints tous les 24 px, reflets
    for y in range(0, 470, 24): rect(c, 0, y, W, 1, TILE_D)
    for x in range(0, W, 24): rect(c, x, 0, 1, 470, TILE_D)
    for y in range(0, 470, 24):
        for x in range(0, W, 24):
            rect(c, x + 3, y + 3, 4, 1, WHITE); rect(c, x + 3, y + 4, 1, 3, WHITE)
    dither(c, (YY < 470) & (XX > 300), TILE_D, 4)
    # sol
    rect(c, 0, 470, W, H - 470, NIGHT3)
    for y in range(470, H, 16): rect(c, 0, y, W, 1, NIGHT2)
    for x in range(8, W, 32): rect(c, x, 470, 1, H - 470, NIGHT2)
    dither(c, YY > 540, NIGHT2, 8)
    rect(c, 0, 468, W, 3, NIGHT)
    # bac de douche
    rect(c, 190, 462, 130, 10, WHITE); rect(c, 190, 470, 130, 2, GREY)
    rect(c, 190, 461, 130, 1, NIGHT)
    # tuyau + pommeau
    rect(c, 252, 0, 6, 150, GREY); rect(c, 251, 0, 1, 150, NIGHT); rect(c, 258, 0, 1, 150, NIGHT)
    rect(c, 254, 0, 1, 150, WHITE)
    ellipse(c, 255, 156, 18, 7, GREY, NIGHT)
    rect(c, 240, 158, 30, 2, NIGHT3)
    # robinet
    rect(c, 246, 410, 18, 12, GREY); rect(c, 246, 410, 18, 1, WHITE)
    rect(c, 245, 409, 20, 1, NIGHT); rect(c, 245, 422, 20, 1, NIGHT)
    a = tap_open * np.pi / 2
    hx, hy = 255, 404
    for s in (-1, 1):
        line(c, hx, hy, hx + s * round(9 * np.cos(a)), hy + s * round(9 * np.sin(a)), NIGHT, 4)
        line(c, hx, hy, hx + s * round(9 * np.cos(a)), hy + s * round(9 * np.sin(a)), RED, 2)
    circle(c, hx, hy, 2, WHITE, NIGHT)
    # eau
    if water > 0:
        rng = np.random.default_rng(1)
        n = int(90 * water)
        for i in range(n):
            x0 = rng.uniform(-15, 15); sp = rng.uniform(380, 520); ph = rng.uniform(0, 1)
            y = 164 + ((t * sp + ph * 300) % 296)
            x = 255 + x0 * (1 + (y - 164) / 260)
            rect(c, x, y, 2, 6, WATER); rect(c, x, y, 2, 1, WHITE)
        for i in range(int(8 * water)):
            sx = 210 + (i * 37 + int(t * 30)) % 90
            rect(c, sx, 458 - (int(t * 20 + i) % 4), 2, 2, WHITE)


def calendar(c, x, y, day):
    rect(c, x - 1, y - 1, 66, 62, NIGHT)
    rect(c, x, y, 64, 60, WHITE); rect(c, x, y, 64, 14, RED)
    for k in (14, 46): rect(c, x + k, y - 4, 3, 8, GREY)
    draw_text(c, [(f"J+{day}", NIGHT)], x + 32, y + 18, 22 if day < 100 else 18,
              outline=None, shadow=False)


# ---------- bactéries, champignons, odeur ----------
def bact(c, x, y, r, t, col=BACT, dark=BACT_D, chomp=False, lick=False, angry=False, seed=0):
    tq = pose_t(t)
    wob = int(round(np.sin(tq * 9 + seed)))
    x, y = int(x), int(y) + wob
    m = mask_circle(x, y, r)
    c[dilate(m)] = NIGHT
    c[m] = col
    dither(c, m & ((XX - x) + (YY - y) > r * 0.6), dark, 8)
    for a in range(0, 360, 60):  # cils
        ax = x + round((r + 2) * np.cos(np.radians(a + tq * 90)))
        ay = y + round((r + 2) * np.sin(np.radians(a + tq * 90)))
        rect(c, ax, ay, 1, 1, NIGHT)
    e = max(1, r // 4)
    ey = y - r // 4
    for s in (-1, 1):
        ex = x + s * (r // 2 - 0)
        rect(c, ex - e, ey - e, 2 * e, 2 * e + 1, WHITE)
        rect(c, ex - (e // 2), ey - (e // 2) + 1, max(1, e), max(1, e), BLACK)
        if angry: line(c, ex - e - 1, ey - e - 2 + (s < 0) * 2, ex + e, ey - e - 2 + (s > 0) * 2, NIGHT, 1)
    my = y + r // 3
    if chomp and int(tq * 8) % 2:
        ellipse(c, x, my, max(2, r // 3), max(1, r // 4), BLACK)
    else:
        line(c, x - r // 3, my, x + r // 3, my, NIGHT, 1)
    if lick:
        rect(c, x + r // 4, my, 2, 2 + int(tq * 6) % 2, PIP_P)


def mush(c, x, y, size, age):
    """Champignon qui « pop » : age en secondes depuis l'apparition."""
    if age < 0: return
    k = min(1.0, age / 0.12) * (1 + 0.25 * max(0, 1 - age / 0.3))
    s = max(1, round(size * k))
    x, y = int(x), int(y)
    rect(c, x - s // 3 - 1, y - s, 2 * (s // 3) + 2, s + 1, NIGHT)
    rect(c, x - s // 3, y - s, 2 * (s // 3), s, WHITE)
    cap = mask_ellipse(x, y - s, s, max(2, s * 0.7)) & (YY <= y - s + 1)
    c[dilate(cap)] = NIGHT
    c[cap] = MUSH
    for dx, dy in ((-s // 2, -s // 3), (s // 3, -s // 2), (0, -s // 5 - 1)):
        rect(c, x + dx, y - s + dy, max(1, s // 4), max(1, s // 4), WHITE)


def stink(c, x, y, t, n=3, h=30, col=STINK):
    tq = pose_t(t)
    for i in range(n):
        ph = (tq * 0.9 + i / n) % 1
        bx = x + (i - (n - 1) / 2) * 8
        for k in range(10):
            yy = y - ph * h - k * 2
            xx = bx + 3 * np.sin(k * 0.8 + tq * 6 + i)
            if ph < 0.9: rect(c, xx, yy, 2, 2, col if k % 4 else BACT_D)


def cloud(c, x, y, r, col=STINK, level=10):
    for dx, dy, rr in ((0, 0, r), (-r * 0.7, r * 0.2, r * 0.7), (r * 0.7, r * 0.25, r * 0.65)):
        dither(c, mask_circle(int(x + dx), int(y + dy), rr), col, level)


def sparkle(c, x, y, t, col=WHITE):
    k = int(pose_t(t) * 6) % 3
    s = (1, 2, 3)[k]
    rect(c, x - s, y, 2 * s + 1, 1, col); rect(c, x, y - s, 1, 2 * s + 1, col)


# ---------- gens ----------
def person(c, x, fy, t, run=0.0, flip=False, scale=1, clothespin=False, faint=0.0, col=GREY):
    tmp = np.full_like(c, T_)
    ox, oy = 30, 70
    tq = pose_t(t)
    step = int(tq * 12) % 2 if run else 0
    lean = 4 if run else 0
    # jambes
    for s in (-1, 1):
        lx = ox + s * (3 + (5 * s if step else -2 * s) * (1 if run else 0))
        line(tmp, ox + s * 3, oy - 20, lx, oy, NIGHT, 4); line(tmp, ox + s * 3, oy - 20, lx, oy, col, 2)
    body = mask_ellipse(ox + lean // 2, oy - 30, 8, 13)
    tmp[dilate(body)] = NIGHT; tmp[body] = col
    for s in (-1, 1):
        ax = ox + s * 12 + (lean if run else 0); ay = oy - 22 - (8 if run and (step ^ (s > 0)) else 0)
        line(tmp, ox, oy - 36, ax, ay, NIGHT, 4); line(tmp, ox, oy - 36, ax, ay, col, 2)
    hx, hy = ox + lean, oy - 50
    head = mask_circle(hx, hy, 8)
    tmp[dilate(head)] = NIGHT; tmp[head] = col
    if faint > 0.5:
        for s in (-1, 1):
            ex = hx + s * 3 + 2
            line(tmp, ex - 1, hy - 2, ex + 1, hy, NIGHT, 1); line(tmp, ex - 1, hy, ex + 1, hy - 2, NIGHT, 1)
    else:
        for s in (-1, 1):
            rect(tmp, hx + s * 3 + 1, hy - 2, 2, 2 if not clothespin else 1, NIGHT)
    if clothespin:
        rect(tmp, hx + 6, hy - 1, 6, 3, SOAP); rect(tmp, hx + 6, hy - 1, 6, 1, NIGHT)
        rect(tmp, hx + 9, hy - 4, 2, 9, SOAP)
        line(tmp, hx - 2, hy + 4, hx + 3, hy + 3, NIGHT, 1)
    else:
        line(tmp, hx - 1, hy + 4, hx + 4, hy + 4, NIGHT, 1)
    spr = tmp[0:oy + 2, 0:60]
    if faint > 0:
        k = int(faint * 3)
        spr = np.rot90(spr, -1) if k >= 2 else spr
    blit(c, spr, x - (30 if spr.shape[1] == 60 else spr.shape[1] // 2) * scale,
         fy - spr.shape[0] * scale + (0 if spr.shape[1] == 60 else 0), scale, flip)


def tumbleweed(c, x, y, t):
    a = t * 8
    circle(c, x, y, 9, CRUST, NIGHT)
    for k in range(4):
        aa = a + k * np.pi / 4
        line(c, x - 8 * np.cos(aa), y - 8 * np.sin(aa), x + 8 * np.cos(aa), y + 8 * np.sin(aa), SKIN_D, 1)
    circle(c, x, y, 3, SKIN_D)


def soap(c, x, y):
    m = mask_ellipse(x, y, 16, 9)
    c[dilate(m)] = NIGHT; c[m] = SOAP
    rect(c, x - 9, y - 5, 8, 2, WHITE)


def bubble(c, x, y, r):
    m = mask_circle(int(x), int(y), r)
    c[m & ~mask_circle(int(x), int(y), r - 1)] = TILE_D
    rect(c, x - r // 2, y - r // 2, 1, 1, WHITE)


def badge(c, x, y, txt, fg=RED, bg=WHITE, size=18):
    w = text_width(txt, size) + 12
    rect(c, x - w // 2 - 1, y - 2, w + 2, size + 6, NIGHT)
    rect(c, x - w // 2, y - 1, w, size + 4, bg)
    draw_text(c, [(txt, fg)], x, y - 2, size, outline=None, shadow=False)
