"""Pip : sprite procédural (~26x42 px art) avec bonnet de douche."""
import numpy as np
from pixel import *


def _arm(c, x0, y0, x1, y1):
    line(c, x0, y0, x1, y1, NIGHT, 4)
    line(c, x0, y0, x1, y1, PIP, 2)
    circle(c, x1, y1, 2, PIP, NIGHT)


def pip(c, fx, fy, t, pose="idle", look=(0, 0), mood="smile", cap=True, spots=0,
        arm=None, flip=False, blink=True):
    """Dessine Pip, pieds en (fx, fy). pose : idle reach pinch scratch sniff jump surprised."""
    tq = pose_t(t)
    fx, fy = int(fx), int(fy)
    sgn = -1 if flip else 1
    breath = int(tq * 2) % 2
    shake = 0
    if pose == "scratch": shake = (int(tq * 12) % 2) * 2 - 1
    bx, by = fx + shake, fy - 16
    ry = 13 - breath + (2 if pose == "jump" else 0)
    rx = 11 + breath - (1 if pose == "jump" else 0)

    # pieds
    for dx in (-5, 5):
        ellipse(c, fx + dx, fy - 1, 3, 2, PIP_D, NIGHT)

    # bras arrière (gauche du sprite)
    arms = {
        "idle": [(-12, 2, -14, 10), (12, 2, 14, 10)],
        "reach": [(-12, 2, -14, 10), (12, -2, 22, -10)],
        "pinch": [(-12, 2, -14, 10), (11, 0, 3, -6)],
        "sniff": [(-11, -2, -18, -16), (12, 2, 14, 10)],
        "jump": [(-11, -2, -18, -14), (11, -2, 18, -14)],
        "surprised": [(-11, -2, -17, -10), (11, -2, 17, -10)],
        "scratch": [(-11, 0, -8 + (int(tq * 12) % 2) * 4, -12), (11, 2, 15, 6 + (int(tq * 12) % 2) * 4)],
        "happy": [(-11, -2, -17, -12), (11, -2, 17, -12)],
    }[pose]
    if arm is not None:
        arms = [arms[0], arm]

    body = mask_ellipse(bx, by, rx, ry)
    c[dilate(body)] = NIGHT
    c[body] = PIP
    dither(c, body & ((XX - bx) + (YY - by) > 9), PIP_D, 10)
    rect(c, bx - 6, by - 8, 2, 2, WHITE)

    for ax0, ay0, ax1, ay1 in arms:
        _arm(c, bx + sgn * ax0, by + ay0, bx + sgn * ax1, by + ay1)

    # boutons / taches (malade)
    rng = np.random.default_rng(5)
    for i in range(spots):
        sx, sy = rng.integers(-7, 8), rng.integers(-4, 10)
        rect(c, bx + sx, by + sy, 2, 2, RED if i % 3 else CRUST)

    # yeux
    ey = by - 2
    closed = blink and (tq % 3.1) < 0.09
    for ex in (-5, 5):
        x = bx + ex
        if mood == "squint":
            line(c, x - 2, ey - 1 + (0 if ex < 0 else 0), x + 2, ey + 1, NIGHT, 1)
            line(c, x - 2, ey + 1, x + 2, ey - 1, NIGHT, 1) if False else None
        elif mood == "stars":
            for d in (-2, -1, 0, 1, 2):
                rect(c, x + d, ey, 1, 1, YELLOW); rect(c, x, ey + d, 1, 1, YELLOW)
        elif closed:
            line(c, x - 2, ey, x + 2, ey, NIGHT, 1)
        else:
            big = 1 if mood == "wow" else 0
            ellipse(c, x, ey, 3 + big, 4 + big, WHITE, NIGHT)
            rect(c, x + look[0], ey + look[1] - 1, 2, 3, BLACK)

    # bouche
    my = by + 6
    if mood in ("smile", "stars"):
        line(c, bx - 3, my, bx - 1, my + 1, NIGHT, 1); line(c, bx - 1, my + 1, bx + 1, my + 1, NIGHT, 1)
        line(c, bx + 1, my + 1, bx + 3, my, NIGHT, 1)
    elif mood == "wow":
        ellipse(c, bx, my + 1, 2, 2, NIGHT)
    elif mood in ("squint", "yuck"):
        for i in range(-3, 4):
            rect(c, bx + i, my + (i % 2), 1, 1, NIGHT)
    elif mood == "sad":
        line(c, bx - 3, my + 1, bx - 1, my, NIGHT, 1); line(c, bx - 1, my, bx + 1, my, NIGHT, 1)
        line(c, bx + 1, my, bx + 3, my + 1, NIGHT, 1)

    # bonnet de douche
    top = by - ry
    if cap:
        dome = mask_ellipse(bx, top + 2, rx + 2, 7) & (YY <= top + 3)
        c[dilate(dome)] = NIGHT
        c[dome] = SOAP
        for i, dx in enumerate(range(-rx - 1, rx + 2, 2)):
            rect(c, bx + dx, top + 3, 2, 2, WHITE if i % 2 else SOAP)
        for dx, dy in ((-6, -1), (0, -3), (5, 0), (-2, 1)):
            rect(c, bx + dx, top + dy, 1, 1, WHITE)
        top -= 5
    # antenne
    sway = int(round(2 * np.sin(tq * 5)))
    line(c, bx, top, bx + sway, top - 7, NIGHT, 1)
    circle(c, bx + sway, top - 8, 2, PIP_P, NIGHT)
    return (bx - rx - 6, top - 12, 2 * rx + 12, fy - top + 12)  # boîte englobante


def pip_big(c, cx, fy, t, scale=2, **kw):
    """Pip agrandi (pour l'écran partagé) : dessiné sur un calque puis agrandi au plus proche voisin."""
    tmp = np.full_like(c, T_)
    pip(tmp, 40, 70, t, **kw)
    spr = tmp[0:75, 0:80]
    blit(c, spr, cx - 40 * scale, fy - 70 * scale, scale)
