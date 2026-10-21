"""Épisode « Un an sans douche, il se passe quoi ? » -> renders/douche.mp4

python episode_douche.py --preview | --final | --frame T [T...]
"""
import os, sys
import numpy as np
from PIL import Image
from pixel import *
from pip_pixel import pip, pip_big
from decors_douche import *
import timeline as TL
from timeline import W as Wd, S as Sd, BOUNDS

PIP_ACTIONS = {
    1: ("utiliser_objet", "ferme le robinet"),
    2: ("reagir", "se bouche le nez"),
    3: None,
    4: ("subir", "envahi par les champignons, se gratte"),
    5: ("reagir", "seul, cligne, boule d'herbe"),
    6: ("agir_corps", "renifle son aisselle"),
    7: None,
    8: ("agir_corps", "saute sur le bouton S'ABONNER"),
}
PIP_BOX = {}  # boîte de Pip par image (pour le test de placement)
TITLE_ZONE = (0, 40, W, 150)  # y de 40 à 190 : titres
CAPTION_ZONE = (0, 566, W, 30)


def title(c, t, t0, segs, y, size, **kw):
    b = title_bounce(t, t0)
    if b is None: return
    draw_text(c, segs, W // 2, y + b, size, t=t, **kw)


# ---------------- scène 1 : accroche ----------------
def s1(c, t):
    t_close = Wd(0, "douche")
    tap = 1 - prog(t, t_close - 0.05, t_close + 0.15)
    water = 1.0 if t < t_close + 0.15 else 0.0
    bathroom(c, t, water=water, tap_open=tap)
    # gouttes résiduelles
    if water == 0:
        for i in range(4):
            y = 168 + (t - t_close - 0.15 - i * 0.12) * 600
            if 168 < y < 460: rect(c, 252 + i * 3, y, 1, 4, WATER)
    t_q = Wd(0, "quoi")
    day = 0 if t < t_q else 1 + int(364 * ease_io(prog(t, t_q, t_q + 0.45)))
    calendar(c, 50, 230, day)
    if t >= t_q + 0.45: sparkle(c, 112, 230, t, YELLOW)
    pose = "reach" if t < t_close + 0.35 else ("surprised" if t >= t_q else "idle")
    mood = "wow" if t >= t_q else "smile"
    look = (-1, 0) if t >= t_q else (1, -1)
    px = 228 if t < t_close + 0.35 else 228 - int(18 * prog(t, t_close + 0.35, t_close + 0.8))
    PIP_BOX["box"] = pip(c, px, 462, t, pose=pose, mood=mood, look=look,
                         arm=(12, -2, 25, -30) if pose == "reach" else None)
    title(c, t, 0.05, [("UN AN", RED, "shake")], 62, 44)
    title(c, t, 0.2, [("SANS DOUCHE ?", WHITE)], 118, 28)


# ---------------- scène 2 : déclic (loupe aisselle) ----------------
DROPS = [(120, 300), (175, 260), (230, 310), (150, 360), (215, 380), (185, 320)]
BACTS = [(-30, 300, 6), (390, 250, 7), (380, 400, 6), (-20, 420, 7), (180, 680, 6), (390, 330, 12)]


def skin_patch(c, t):
    c[:] = NIGHT
    vgrad(c, 0, H, [NIGHT, NIGHT2, NIGHT])
    m = mask_circle(180, 320, 140)
    c[m] = SKIN
    dither(c, m & (YY > 380), SKIN_M, 6)
    dither(c, m & (YY > 430), SKIN_M, 12)
    rng = np.random.default_rng(2)
    for _ in range(40):  # pores
        x, y = rng.integers(50, 310), rng.integers(190, 450)
        if (x - 180) ** 2 + (y - 320) ** 2 < 130 ** 2: rect(c, x, y, 2, 1, SKIN_M)
    for k in range(9):  # poils
        x0, y0 = rng.integers(70, 290), rng.integers(210, 430)
        if (x0 - 180) ** 2 + (y0 - 320) ** 2 > 120 ** 2: continue
        for i in range(14):
            rect(c, x0 + i, y0 - int(4 * np.sin(i / 5 + k)), 1, 1, CRUST)


def s2(c, t):
    skin_patch(c, t)
    t_b, t_eat, t_pue, t_buf = Wd(1, "bact"), Wd(1, "mangent"), Wd(1, "puent"), Wd(1, "buffet")
    t0 = BOUNDS[1]
    for i, (x, y) in enumerate(DROPS):
        age = t - (t0 + 0.15 + i * 0.1)
        if age < 0: continue
        te = t_eat + i * 0.1
        k = 1 - prog(t, te, te + 0.3)
        if k <= 0: continue
        r = max(1, round(7 * min(1, age / 0.15) * k))
        m = mask_ellipse(x, y, r, r + 1) | (mask_circle(x, y - r, max(1, r // 2)) & (YY < y))
        c[dilate(m)] = NIGHT3; c[m] = WATER
        rect(c, x - r // 2, y - r // 2, 2, 2, WHITE)
        if t < t_b and (i + int(t * 4)) % 3 == 0: sparkle(c, x + r + 3, y - r - 3, t)
    # bactéries
    for i, ((sx, sy, r), (dx, dy)) in enumerate(zip(BACTS, DROPS)):
        p = ease_out(prog(t, t_b + i * 0.07, t_b + i * 0.07 + 0.45))
        if p <= 0: continue
        x = sx + (dx - 10 - sx) * p; y = sy + (dy - sy) * p
        eating = t_eat + i * 0.1 - 0.1 < t < t_eat + i * 0.1 + 0.5
        bact(c, x, y, r + (2 if t > t_pue else 0), t, chomp=eating, lick=t > t_buf, seed=i)
        if t > t_pue: stink(c, int(x), int(y) - r - 4, t + i * 0.3, n=2, h=26)
    if t > t_pue:
        cloud(c, 180, 230 - 20 * prog(t, t_pue, t_pue + 2), 30, STINK, int(6 * prog(t, t_pue, t_pue + 0.3)))
    # panneau buffet
    if t > t_buf:
        b = title_bounce(t, t_buf, h=30) or 0
        rect(c, 120, 196 + b, 2, 18, CRUST); rect(c, 238, 196 + b, 2, 18, CRUST)
        rect(c, 99, 212 + b, 162, 30, NIGHT); rect(c, 100, 213 + b, 160, 28, YELLOW)
        draw_text(c, [("BUFFET", RED)], 180, 213 + b, 24, outline=None, shadow=False)
    vignette(c, 180, 320, 140)
    # étiquette loupe
    draw_text(c, [("AISSELLE", WHITE)], 180, 455, 16, outline=NIGHT, shadow=False)
    # Pip, hors de la loupe
    pue = t > t_pue
    PIP_BOX["box"] = pip(c, 44, 532, t, pose="pinch" if pue else "idle",
                         mood="yuck" if pue else ("wow" if t > t_b else "smile"), look=(1, -1))
    if pue: stink(c, 44, 488, t, n=2, h=20)
    # titres
    if Wd(1, "rien") - 0.25 < t < t_pue:
        title(c, t, Wd(1, "rien") - 0.25, [("0", YELLOW), (" ODEUR", WHITE)], 70, 34)
    if t >= t_pue:
        title(c, t, t_pue, [("ÇA ", WHITE), ("PUE", STINK, "shake"), (" !", WHITE)], 66, 44)


# ---------------- scène 3 : mécanisme (coupe en accéléré) ----------------
SURF = 250


def s3(c, t):
    t0 = BOUNDS[2]
    t_30, t_seb, t_col, t_sem, t_cr = (Wd(2, "trente"), Wd(2, "sébum"), Wd(2, "collent"),
                                       Wd(2, "semaines"), Wd(2, "croûte"))
    fast = t >= t_sem
    vgrad(c, 0, SURF, [NIGHT, NIGHT2, NIGHT3])
    # couches
    rect(c, 0, SURF, W, 26, SKIN)
    for y in range(SURF, SURF + 26, 7):
        off = (y // 7) % 2 * 10
        for x in range(-off, W, 20): rect(c, x, y, 1, 7, SKIN_M)
        rect(c, 0, y, W, 1, SKIN_M)
    rect(c, 0, SURF + 26, W, 90, SKIN_M)
    rng = np.random.default_rng(4)
    for _ in range(40):
        x, y = rng.integers(0, W), rng.integers(SURF + 30, SURF + 112)
        ellipse(c, x, y, 5, 4, SKIN, None); rect(c, x - 1, y, 2, 2, SKIN_D)
    rect(c, 0, SURF + 116, W, H - SURF - 116, SKIN_D)
    dither(c, YY > SURF + 116, CRUST, 4)
    dither(c, YY > 520, CRUST, 10)
    # poil + glande sébacée
    line(c, 132, SURF + 150, 120, SURF - 70, NIGHT, 5); line(c, 132, SURF + 150, 120, SURF - 70, CRUST, 3)
    ellipse(c, 133, SURF + 152, 8, 10, SKIN_D, NIGHT)
    gland = 1 + (int(pose_t(t) * 4) % 2 if t > t_seb else 0)
    ellipse(c, 158, SURF + 80, 14 + gland, 11 + gland, SEBUM, NIGHT)
    rect(c, 152, SURF + 74, 3, 2, WHITE)
    # sébum qui remonte puis s'étale
    if t > t_seb:
        p = prog(t, t_seb, t_seb + 0.5)
        for k in range(4):
            yy = SURF + 70 - ((t - t_seb) * 160 + k * 18) % 80
            rect(c, 140 - (SURF + 70 - yy) * 0.15, yy, 3, 3, SEBUM)
        spread = ease_out(prog(t, t_seb + 0.3, t_col + 0.6))
        x0, x1 = int(126 - 126 * spread), int(126 + 240 * spread)
        rect(c, x0, SURF - 4, x1 - x0, 4, SEBUM)
        dither(c, (YY >= SURF - 6) & (YY < SURF - 4) & (XX >= x0) & (XX < x1), SEBUM, 8)
    # pellicules
    n_fl = 26
    stick = t > t_col
    for i in range(n_fl):
        speed = 3 if fast else 1
        ph = (((t - t0) * 0.5 * speed) + i / n_fl) % 1
        x = (i * 53 + 17) % (W - 20) + 10
        if stick:
            y = SURF - 6 - (i % 3) * 3 - (int(prog(t, t_sem, t_cr + 0.5) * 6) if fast else 0)
            x += 0
        else:
            y = SURF - 4 - ph * 160
            x += int(6 * np.sin(ph * 9 + i))
        if y < 30: continue
        rect(c, x - 1, y - 1, 10, 6, NIGHT if not stick else SKIN_M)
        rect(c, x, y, 8, 4, SKIN); rect(c, x, y, 8, 1, WHITE if not stick else SKIN)
    # croûte
    if fast:
        th = ease_io(prog(t, t_sem + 0.2, BOUNDS[3] - 0.3)) * 20
        if th >= 1:
            top = SURF - 2 - th - 3 * np.sin(XX / 11.0) - 2 * np.sin(XX / 5.0 + 1)
            m = (YY >= top) & (YY < SURF + 2)
            c[m] = CRUST
            dither(c, m & (YY < top + 3), SKIN_D, 8)
            dither(c, m & (YY > SURF - 4), SEBUM, 4)
    # étiquettes
    if t > t_seb:
        draw_text(c, [("SÉBUM", SEBUM)], 230, SURF + 72, 18, t=t)
        line(c, 196, SURF + 82, 176, SURF + 82, WHITE, 1)
    if t > t_cr:
        draw_text(c, [("CROÛTE", WHITE)], 270, SURF - 60, 20)
        line(c, 270, SURF - 36, 262, SURF - 18, WHITE, 1)
    # titres
    if t < t_sem:
        if t > t_30 - 0.1:
            n = int(30000 * ease_out(prog(t, t_30, t_30 + 0.7)))
            s = f"{n:,}".replace(",", " ")
            title(c, t, t_30 - 0.1, [(s, YELLOW)], 54, 40)
            title(c, t, t_30 + 0.3, [("CELLULES / MIN", WHITE)], 104, 22)
        else:
            title(c, t, t0 + 0.05, [("TA PEAU", WHITE)], 66, 30)
    else:
        d = 1 + int(29 * prog(t, t_sem, BOUNDS[3] - 0.3))
        title(c, t, t_sem, [(f"J+{d}", YELLOW)], 54, 44)
        badge(c, 312, 14, "×1000")
        # chrono
        cx, cy = 48, 30
        circle(c, cx, cy, 14, WHITE, NIGHT)
        a = (t - t_sem) * 20
        line(c, cx, cy, cx + 10 * np.cos(a), cy + 10 * np.sin(a), RED, 2)
        line(c, cx, cy, cx + 6 * np.cos(a / 12), cy + 6 * np.sin(a / 12), NIGHT, 2)


# ---------------- scène 4 : rebondissement (pli de peau) ----------------
def fold_y(x):
    """Deux bosses de peau qui se rejoignent en un pli au centre."""
    d = (abs(x - 180) - 90) / 90.0
    return 300 + 120 * d * d


def s4(c, t):
    t0 = BOUNDS[3]
    t_pire, t_plis, t_ch, t_champ, t_gr, t_rou, t_inf = (
        Wd(3, "pire"), Wd(3, "plis"), Wd(3, "chauds"), Wd(3, "champ"), Wd(3, "gratte"),
        Wd(3, "rougit"), Wd(3, "s'infecte"))
    vgrad(c, 0, H, [NIGHT, NIGHT2, NIGHT2])
    xs = np.arange(W)
    top = np.array([fold_y(x) for x in xs])
    m = YY >= top[None, :]
    c[m] = SKIN
    dither(c, m & (np.abs(XX - 180) < 70), SKIN_M, 6)
    dither(c, m & (np.abs(XX - 180) < 36), SKIN_M, 12)
    dither(c, m & (np.abs(XX - 180) < 14), SKIN_D, 10)
    edge = m & ~np.roll(m, 1, 0)
    c[dilate(edge) & ~m] = NIGHT
    yc = int(fold_y(180))
    rect(c, 179, yc - 2, 2, H - yc, SKIN_D); rect(c, 180, yc + 10, 1, H - yc, NIGHT2)
    # croûtes de la scène précédente
    for x in (60, 100, 260, 310):
        y = int(fold_y(x))
        a = 1 - prog(t, t_pire, t_pire + 0.4) * 0.0
        rect(c, x - 8, y, 16, 4, CRUST); rect(c, x - 6, y - 1, 10, 1, CRUST)
    # chaleur + humidité
    if t > t_ch:
        for i in range(5):
            ph = ((t - t_ch) * 0.8 + i / 5) % 1
            x = 150 + i * 15
            for k in range(8):
                yy = fold_y(180) - 10 - ph * 110 - k * 3
                rect(c, x + 3 * np.sin(k + t * 7 + i), yy, 1, 2, WHITE if k % 2 else TILE)
        for i in range(6):
            x = 160 + (i * 7) % 40; y = int(fold_y(x)) + 4 + (i * 13) % 30
            rect(c, x, y, 2, 3, WATER)
    # champignons
    spots = [(160, 0.0), (200, 0.1), (140, 0.2), (222, 0.3), (118, 0.42), (244, 0.5), (60, 0.62), (316, 0.7)]
    for x, d in spots:
        y = int(fold_y(x)) + 1
        mush(c, x, y, 8 + (x * 7) % 5, t - (t_champ + d))
    # rougeurs + « microbes fâchés »
    if t > t_gr:
        lvl = int(4 + 10 * prog(t, t_rou, t_rou + 0.5))
        red = m & (np.abs(XX - 180) < 20 + 40 * prog(t, t_rou, t_rou + 0.6)) & (YY < top[None, :] + 40)
        if int(pose_t(t) * 4) % 2 or t > t_rou: dither(c, red, RED, lvl)
    if t > t_inf:
        for i, x in enumerate((140, 220, 180)):
            p = ease_out(prog(t, t_inf + i * 0.1, t_inf + i * 0.1 + 0.25))
            if p > 0: bact(c, x, int(fold_y(x)) + 18, max(2, int(6 * p)), t, col=RED, dark=SKIN_D, angry=True, seed=i)
    # Pip sur la bosse de droite
    px = 268; py = int(fold_y(px)) + 2
    sc = t > t_gr
    PIP_BOX["box"] = pip(c, px, py, t, pose="scratch" if sc else ("surprised" if t > t_champ else "idle"),
                         mood="yuck" if sc else ("wow" if t > t_champ else "smile"), look=(-1, 1))
    mush(c, px - 1, py - 32, 6, t - (t_champ + 0.55))  # champignon sur le bonnet
    if sc:
        for k in range(3):
            if (int(pose_t(t) * 12) + k) % 3 == 0:
                line(c, px - 18 - k * 3, py - 20 + k * 5, px - 12 - k * 3, py - 26 + k * 5, WHITE, 1)
    if t_pire - 0.2 < t < t_champ:
        draw_text(c, [("!", YELLOW)], px, py - 64, 24, t=t)
    # titres
    if t < t_champ:
        title(c, t, t0 + 0.05, [("SAUF QUE…", MUSH)], 66, 30)
        if t > t_plis:
            draw_text(c, [("PLI", WHITE)], 180, int(fold_y(180)) - 90, 18)
            line(c, 180, int(fold_y(180)) - 66, 180, int(fold_y(180)) - 12, WHITE, 1)
    else:
        title(c, t, t_champ, [("MYCOSES", MUSH, "wave")], 62, 42)
        if t > t_gr:
            title(c, t, t_gr, [("ÇA GRATTE !", RED, "shake")], 118, 22)


# ---------------- scène 5 : réponse (rue vide) ----------------
PEOPLE = [(40, 1), (95, 1), (268, 0), (322, 0)]


def street(c, t):
    vgrad(c, 0, 470, [TILE, TILE, TILE_D])
    for i, (x, w, h) in enumerate([(0, 70, 230), (75, 60, 300), (140, 80, 200), (225, 65, 280), (295, 70, 240)]):
        rect(c, x, 470 - h, w, h, NIGHT3 if i % 2 else GREY); rect(c, x, 470 - h, w, 2, NIGHT)
        for yy in range(470 - h + 12, 450, 22):
            for xx in range(x + 8, x + w - 10, 16):
                rect(c, xx, yy, 8, 10, YELLOW if (xx + yy + i) % 3 == 0 else NIGHT2)
    rect(c, 0, 470, W, 30, GREY); rect(c, 0, 470, W, 1, NIGHT)
    for x in range(0, W, 30): rect(c, x, 470, 1, 30, NIGHT3)
    rect(c, 0, 500, W, H - 500, NIGHT3)
    for x in range(10, W, 60): rect(c, x, 540, 30, 4, WHITE)


def s5(c, t):
    t0 = BOUNDS[4]
    t_sv, t_mais, t_mal, t_monde, t_fuit = (Wd(4, "survis"), Wd(4, "mais"), Wd(4, "malade"),
                                             Wd(4, "monde"), Wd(4, "fuit"))
    street(c, t)
    t_run = t_fuit - 0.25
    for i, (x, side) in enumerate(PEOPLE):
        if t < t_run:
            person(c, x, 492, t + i * 0.2, flip=(side == 0) if t > t_monde else (side == 1))
        else:
            dx = (t - t_run) * 520 * (-1 if side else 1)
            xx = x + dx
            if -40 < xx < W + 40:
                person(c, xx, 492, t + i * 0.1, run=1, flip=(side == 1))
                for k in range(3):
                    circle(c, xx - (-1 if side else 1) * (16 + k * 9), 488, 3 - k, WHITE)
    # Pip
    spots = int(8 * prog(t, t_mal, t_mal + 0.4))
    mood = "sad" if t > t_fuit + 0.2 else ("stars" if t_sv <= t < t_mais else ("wow" if t > t_run else "smile"))
    PIP_BOX["box"] = pip(c, 180, 492, t, pose="happy" if t_sv <= t < t_mais else "idle", mood=mood,
                         spots=spots, look=(0, 0) if t < t_run else ((-1, 0) if int(t * 3) % 2 else (1, 0)))
    stink(c, 180, 446, t, n=3, h=24)
    if t > t_fuit + 0.3:
        tx = W + 20 - (t - t_fuit - 0.3) * 160
        tumbleweed(c, tx, 486 - abs(int(8 * np.sin((t - t_fuit) * 7))), t)
    # titres
    if t < t_sv - 0.05:
        title(c, t, t0 + 0.05, [("1 AN", YELLOW), (" PLUS TARD…", WHITE)], 70, 26)
    elif t < t_fuit:
        title(c, t, t_sv, [("TU SURVIS", YELLOW)], 60, 38)
        if t > t_mais: title(c, t, t_mais, [("MAIS…", RED)], 112, 26)
        if t_sv < t < t_mais:
            for k, (sx, sy) in enumerate([(60, 70), (300, 80), (80, 120), (285, 125)]):
                sparkle(c, sx, sy, t + k * 0.13, YELLOW)
    else:
        title(c, t, t_fuit, [("ON TE ", WHITE), ("FUIT", RED, "shake"), (" !", WHITE)], 62, 40)


# ---------------- scène 6 : objection (écran partagé) ----------------
def s6(c, t):
    t0 = BOUNDS[5]
    t_toi, t_od, t_non, t_hab, t_min, t_seul = (Wd(5, "toi"), Wd(5, "odeur"), Wd(5, "non"),
                                                Wd(5, "s'habitue"), Wd(5, "minutes", end=True),
                                                Wd(5, "seul"))
    # moitié gauche : TOI
    c[:, :180] = TILE
    for y in range(0, H, 24): rect(c, 0, y, 180, 1, TILE_D)
    for x in range(0, 180, 24): rect(c, x, 0, 1, H, TILE_D)
    rect(c, 0, 470, 180, H - 470, NIGHT3)
    # moitié droite : LES AUTRES
    c[:, 180:] = NIGHT2
    dither(c, XX >= 180, NIGHT3, 5)
    rect(c, 180, 470, 180, H - 470, NIGHT)
    rect(c, 178, 0, 4, H, BLACK); rect(c, 179, 0, 2, H, WHITE)
    draw_text(c, [("TOI", YELLOW)], 90, 172, 22)
    if t > t_od - 0.2: draw_text(c, [("LES AUTRES", WHITE)], 270, 172, 18)
    # Pip renifle son aisselle
    happy = t > t_seul
    PIP_BOX["box"] = (40, 380, 100, 92)
    pip_big(c, 90, 470, t, pose="sniff" if not happy else "happy",
            mood="stars" if (t < t_non or happy) else "smile", look=(-1, -1))
    stink(c, 90, 360, t, n=3, h=30)
    if t < t_non or happy:
        for k in range(3):
            ph = ((t - t0) * 0.7 + k / 3) % 1
            hx, hy = 50 + k * 30, 380 - ph * 70
            rect(c, hx, hy, 2, 2, PIP_P); rect(c, hx + 3, hy, 2, 2, PIP_P); rect(c, hx, hy + 2, 5, 2, PIP_P)
            rect(c, hx + 1, hy + 4, 3, 1, PIP_P)
    # jauge du nez
    if t > t_hab - 0.2:
        p = prog(t, t_hab, t_min)
        rect(c, 24, 500, 132, 16, WHITE); rect(c, 26, 502, 128, 12, NIGHT)
        wbar = int(126 * (1 - p))
        if wbar > 0: rect(c, 27, 503, wbar, 10, BACT if p < 0.5 else (YELLOW if p < 0.85 else RED))
        draw_text(c, [(f"TON NEZ {int(100 * (1 - p))}%", WHITE)], 90, 522, 14, shadow=False)
    # l'autre : pince à linge, nuage, s'évanouit
    faint = prog(t, t_seul, t_seul + 0.3)
    person(c, 270, 470, t, scale=2, clothespin=True, faint=faint)
    cloud(c, 225, 330 + int(3 * np.sin(t * 3)), 22, STINK, 9)
    if t > t_od and faint < 0.5:
        draw_text(c, [("BEURK", STINK)], 300, 250, 18, t=t, shake="shake")
    # titres
    if t < t_non:
        title(c, t, t_toi, [("ET TOI ?", WHITE)], 66, 32)
    else:
        title(c, t, t_non, [("NON !", RED, "shake")], 56, 48)


# ---------------- scène 7 : conseil ----------------
ITEMS = [("AISSELLES", "aisselles", 236), ("PIEDS", "pieds", 312), ("MAINS", "mains", 388)]


def s7(c, t):
    t0 = BOUNDS[6]
    t_dou, t_lave = Wd(6, "douche"), Wd(6, "lave")
    c[:] = TILE
    for y in range(0, H, 24): rect(c, 0, y, W, 1, TILE_D)
    for x in range(0, W, 24): rect(c, x, 0, 1, H, TILE_D)
    dither(c, YY > 470, TILE_D, 8)
    # titre : 1 douche / jour barré
    if t < t_lave - 0.05:
        title(c, t, t0 + 0.05, [("1 DOUCHE", WHITE)], 60, 32)
        title(c, t, t0 + 0.2, [("PAR JOUR ?", WHITE)], 104, 26)
        if t > t_dou:
            p = prog(t, t_dou, t_dou + 0.25)
            line(c, 60, 130, 60 + 240 * p, 62, RED, 5)
            line(c, 60, 62, 60 + 240 * p, 130, RED, 5)
            if t > t_dou + 0.2: draw_text(c, [("PAS OBLIGÉ", YELLOW)], 180, 150, 20, t=t)
    else:
        title(c, t, t_lave, [("LAVE SURTOUT :", WHITE)], 70, 28)
    # carte
    show = prog(t, t0 + 0.1, t0 + 0.4)
    if show > 0:
        y0 = 190 + int(300 * (1 - ease_out(show)))
        rect(c, 39, y0 - 1, 282, 262, NIGHT); rect(c, 40, y0, 280, 260, WHITE)
        rect(c, 40, y0 + 254, 280, 6, TILE)
        dy = y0 - 190
        soap_pos = None
        for k, (lab, key, y) in enumerate(ITEMS):
            yy = y + dy
            tk = Wd(6, key)
            rect(c, 60, yy, 26, 26, NIGHT); rect(c, 62, yy + 2, 22, 22, WHITE)
            if t > tk - 0.15:
                big = key == "mains"
                draw_text(c, [(lab, RED if big else NIGHT, "shake" if big and t < tk + 0.6 else None)],
                          100, yy, 26 if big else 24, outline=None if not big else NIGHT,
                          shadow=False, center=False, t=t)
            if t > tk:
                p = prog(t, tk, tk + 0.2)
                line(c, 65, yy + 13, 65 + 6 * min(1, p * 2), yy + 13 + 6 * min(1, p * 2), BACT_D, 3)
                if p > 0.5: line(c, 71, yy + 19, 71 + 12 * (p - 0.5) * 2, yy + 19 - 16 * (p - 0.5) * 2, BACT_D, 3)
            if tk - 0.3 < t: soap_pos = (73, yy + 13, tk)
        # savon glisse vers la case en cours
        if soap_pos:
            sx, sy, tk = soap_pos
            p = ease_out(prog(t, tk - 0.3, tk))
            x = 300 - (300 - sx - 8) * p
            soap(c, int(x), int(sy - 18))
            for b in range(4):
                bubble(c, x + 18 + b * 9, sy - 24 - (b % 2) * 6 - int(t * 10 + b) % 4, 3 + b % 2)
        # microbes sur les mains qui éclatent
        tm = Wd(6, "mains")
        for k, (bx, by) in enumerate([(250, 402), (282, 392), (298, 414), (230, 420)]):
            pop = tm + 0.15 + k * 0.08
            if t < pop:
                if t > t0 + 0.4:
                    bact(c, bx, by + dy, 6, t, col=(BACT, MUSH, SOAP, BACT)[k], dark=BACT_D, seed=k)
            elif t < pop + 0.5:
                r = 3 + int((t - pop) * 16)
                bubble(c, bx, by + dy, r)


# ---------------- scène 8 : fin ----------------
def s8(c, t):
    t_dou, t_ab = Wd(7, "douche"), Wd(7, "abonne")
    t0 = BOUNDS[7]
    water = 1.0 if t > t_dou - 0.1 else 0.0
    bathroom(c, t, water=water, tap_open=1.0 if water else 0.0)
    # Pip court sous la douche puis saute sur le bouton
    if t < t_dou:
        px = 60 + (230 - 60) * ease_io(prog(t, t0, t_dou)); py = 462; pose = "idle"; mood = "smile"
    elif t < t_ab - 0.35:
        px, py, pose, mood = 230, 462, "happy", "stars"
    else:
        p = prog(t, t_ab - 0.35, t_ab)
        px = 230 + (180 - 230) * p; py = 462 + (424 - 462) * p - 60 * np.sin(np.pi * p)
        pose, mood = ("jump", "wow") if p < 1 else ("happy", "stars")
    # bouton
    bt = t_ab - 0.5
    if t > bt:
        b = title_bounce(t, bt, h=20) or 0
        press = 2 if t_ab <= t < t_ab + 0.2 else 0
        rect(c, 99, 425 + b + press, 162, 40 - press, NIGHT)
        rect(c, 100, 426 + b + press, 160, 36 - press, RED)
        rect(c, 100, 426 + b + press, 160, 2, WHITE)
        draw_text(c, [("S'ABONNER", WHITE)], 180, 428 + b + press, 24, shadow=False)
        # cloche
        sw = int(round(3 * np.sin((t - t_ab) * 20))) if t > t_ab else 0
        bx, by = 300 + sw, 420 + b
        ellipse(c, bx, by, 10, 11, YELLOW, NIGHT); rect(c, bx - 13, by + 8, 27, 4, YELLOW)
        rect(c, bx - 14, by + 8, 29, 1, NIGHT); circle(c, bx, by + 14, 2, CRUST)
        if t > t_ab:
            for k in (-1, 1):
                line(c, bx + k * 16, by - 8, bx + k * 22, by - 12, WHITE, 1)
    py = min(py, 424) if t >= t_ab else py
    PIP_BOX["box"] = pip(c, px, int(py), t, pose=pose, mood=mood)
    if t >= t_ab - 0.35 and water:
        for k in range(3): bubble(c, px - 10 + k * 10, int(py) - 44 - k * 4, 3)
    if t < t_ab:
        title(c, t, t0 + 0.05, [("FILE SOUS LA ", WHITE), ("DOUCHE", WATER), (" !", WHITE)], 70, 26)
    else:
        title(c, t, t_ab, [("ABONNE", YELLOW), ("-TOI", WHITE)], 56, 36)
        title(c, t, t_ab + 0.15, [("POUR D'AUTRES ", WHITE), ("SECRETS", YELLOW, "blink"), (" !", WHITE)], 104, 22)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ALL_WORDS = [w for sc in TL.SCENES for s in sc["sentences"] for w in s["words"]]
CHUNKS = caption_chunks(ALL_WORDS)


def drift(c, t, i):
    dx = int(round(np.sin(t * 0.9 + i)))
    dy = int(round(np.sin(t * 0.7 + i * 2) * 0.6))
    if dx or dy:
        c = np.roll(np.roll(c, dy, 0), dx, 1)
    return c


def render_scene(i, t):
    c = canvas()
    SCENES[i](c, t)
    if i != 5: c = drift(c, t, i)
    return c


def frame(t):
    i = TL.scene_at(t)
    c = render_scene(i, t)
    # volet mosaïque centré sur chaque frontière
    for b_i in range(1, TL.N):
        b = BOUNDS[b_i]
        if abs(t - b) < TL.TRANS / 2:
            a = render_scene(b_i - 1, t); bb = render_scene(b_i, t)
            c = mosaic_mix(a, bb, (t - (b - TL.TRANS / 2)) / TL.TRANS)
    draw_caption(c, CHUNKS, t)
    return c


def main():
    args = sys.argv[1:]
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)
    if args and args[0] == "--frame":
        for s in args[1:]:
            t = float(s)
            Image.fromarray(to_rgb(frame(t))).save(os.path.join(ROOT, "renders", f"frame_{t:05.2f}.png"))
        return
    final = "--final" in args
    scale = 3 if final else 1
    out = os.path.join(ROOT, "renders", "douche.mp4" if final else "douche_preview.mp4")
    wr = Writer(out, scale, audio=os.path.join(ROOT, "audio", "mix.wav"))
    n = int(TL.DURATION * FPS)
    for k in range(n):
        wr.write(frame(k / FPS))
        if k % 150 == 0: print(f"{k}/{n}", flush=True)
    wr.close()
    print("->", out)


if __name__ == "__main__":
    main()
