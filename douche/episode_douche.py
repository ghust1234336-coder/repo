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
    2: ("reagir", "se bouche le nez, puis les collègues reculent"),
    3: ("se_deplacer", "transporté en bus, la place d'à côté reste vide"),
    4: ("subir", "envahi par les champignons, se gratte (absent du plan téléphone)"),
    5: ("reagir", "seul, son chat part avec sa valise"),
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


# --- étapes : barre de progression + tampon « JOUR 2 / 1 MOIS / 3 MOIS / 1 AN » ---
STAGES = {1: ("JOUR 2", 0.08, "jour", "deux"), 2: ("1 MOIS", 0.33, "un", "mois"),
          3: ("3 MOIS", 0.62, "trois", "mois"), 4: ("1 AN", 1.0, "un", "an")}
TY = 38  # décalage des titres sous le bandeau d'étape


def stage_overlay(c, t, si):
    label, pos, w0, w1 = STAGES[si]
    prev = STAGES[si - 1][1] if si - 1 in STAGES else 0.0
    t0 = Wd(si, w0)
    t1 = Wd(si, w1, end=True) + 0.25
    p = prev + (pos - prev) * ease_out(prog(t, t0, t1))
    # barre
    x0, x1, y = 24, 336, 10
    rect(c, x0 - 2, y - 2, x1 - x0 + 4, 10, NIGHT); rect(c, x0, y, x1 - x0, 6, NIGHT3)
    rect(c, x0, y, int((x1 - x0) * p), 6, YELLOW)
    for k, (lab, q, *_r) in STAGES.items():
        mx = x0 + int((x1 - x0) * q) - 1
        rect(c, mx - 1, y - 3, 4, 12, NIGHT); rect(c, mx, y - 2, 2, 10, WHITE if q <= p + 1e-6 else GREY)
    # étiquette fixe sous la barre
    if t >= t1 - 0.05:
        badge(c, 180, 24, label, fg=NIGHT, bg=YELLOW, size=26)
    # tampon plein écran
    if t0 - 0.15 <= t < t1:
        dither(c, np.ones((H, W), bool), BLACK, 10)
        b = title_bounce(t, t0 - 0.15, dur=0.25, h=60) or 0
        draw_text(c, [(label, YELLOW, "shake")], W // 2, 250 + b, 64, t=t)
        rect(c, 70, 340 + b, 220, 4, YELLOW)


def cut(t, *starts):
    """Indice du plan en cours (coupes franches calées sur les phrases)."""
    return sum(t >= s for s in starts)


# ---------------- scène 2 : JOUR 2 — aisselle puis bureau ----------------
def s2(c, t):
    t_bur = Sd(1, 2)
    if t < t_bur:
        s2_loupe(c, t)
    else:
        s2_bureau(c, t)
    stage_overlay(c, t, 1)


def s2_loupe(c, t):
    skin_patch(c, t)
    t_b, t_eat, t_pue = Wd(1, "bact"), Wd(1, "mangent"), Wd(1, "pue")
    t0 = BOUNDS[1]
    for i, (x, y) in enumerate(DROPS):
        age = t - (t0 + 0.6 + i * 0.1)
        if age < 0: continue
        te = t_eat + i * 0.1
        k = 1 - prog(t, te, te + 0.3)
        if k <= 0: continue
        r = max(1, round(7 * min(1, age / 0.15) * k))
        m = mask_ellipse(x, y, r, r + 1) | (mask_circle(x, y - r, max(1, r // 2)) & (YY < y))
        c[dilate(m)] = NIGHT3; c[m] = WATER
        rect(c, x - r // 2, y - r // 2, 2, 2, WHITE)
        if t < t_b and (i + int(t * 4)) % 3 == 0: sparkle(c, x + r + 3, y - r - 3, t)
    for i, ((sx, sy, r), (dx, dy)) in enumerate(zip(BACTS, DROPS)):
        p = ease_out(prog(t, t_b + i * 0.07, t_b + i * 0.07 + 0.45))
        if p <= 0: continue
        x = sx + (dx - 10 - sx) * p; y = sy + (dy - sy) * p
        eating = t_eat + i * 0.1 - 0.1 < t < t_eat + i * 0.1 + 0.5
        bact(c, x, y, r + (2 if t > t_pue else 0), t, chomp=eating, lick=t > t_pue, seed=i)
        if t > t_pue: stink(c, int(x), int(y) - r - 4, t + i * 0.3, n=2, h=26)
    if t > t_pue:
        cloud(c, 180, 230 - 20 * prog(t, t_pue, t_pue + 2), 30, STINK, int(6 * prog(t, t_pue, t_pue + 0.3)))
    vignette(c, 180, 320, 140)
    draw_text(c, [("AISSELLE", WHITE)], 180, 455, 16, outline=NIGHT, shadow=False)
    pue = t > t_pue
    PIP_BOX["box"] = pip(c, 44, 532, t, pose="pinch" if pue else "idle",
                         mood="yuck" if pue else ("wow" if t > t_b else "smile"), look=(1, -1))
    if pue: stink(c, 44, 488, t, n=2, h=20)
    if Wd(1, "rien") - 0.25 < t < t_pue:
        title(c, t, Wd(1, "rien") - 0.25, [("0", YELLOW), (" ODEUR", WHITE)], 70 + TY, 34)
    if t >= t_pue:
        title(c, t, t_pue, [("ÇA ", WHITE), ("PUE", STINK, "shake"), (" !", WHITE)], 66 + TY, 44)


def s2_bureau(c, t):
    t0, t_rec = Sd(1, 2), Wd(1, "reculent")
    office(c, t)
    back = ease_out(prog(t, t_rec, t_rec + 0.35))
    person(c, 70 - int(40 * back), 470, t, flip=back > 0.3, clothespin=back > 0.5)
    person(c, 292 + int(40 * back), 470, t + 0.4, flip=back <= 0.3, col=NIGHT3 if False else GREY)
    if back > 0.3:
        draw_text(c, [("!", RED)], 70 - int(40 * back), 380, 22, t=t, shake="shake")
        draw_text(c, [("!", RED)], 292 + int(40 * back), 380, 22, t=t, shake="shake")
    PIP_BOX["box"] = pip(c, 172, 470, t, pose="happy" if t < t_rec else "surprised",
                         mood="smile" if t < t_rec else "wow", spots=0)
    stink(c, 172, 424, t, n=3, h=26)
    title(c, t, t0, [("AU BUREAU", WHITE)], 70 + TY, 30)
    if t > t_rec:
        title(c, t, t_rec, [("-1 PAS", RED, "shake")], 116 + TY, 26)


# ---------------- scène 3 : 1 MOIS — croûte, cheveux, bus ----------------
SURF = 250


def s3(c, t):
    k = cut(t, Sd(2, 2), Sd(2, 3))
    (s3_coupe, s3_cheveux, s3_bus)[k](c, t)
    stage_overlay(c, t, 2)


def s3_coupe(c, t):
    t0 = BOUNDS[2]
    t_30, t_seb, t_form, t_cr = Wd(2, "trente"), Wd(2, "sébum"), Wd(2, "forment"), Wd(2, "croûte")
    fast = t >= t_seb
    vgrad(c, 0, SURF, [NIGHT, NIGHT2, NIGHT3])
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
    line(c, 132, SURF + 150, 120, SURF - 70, NIGHT, 5); line(c, 132, SURF + 150, 120, SURF - 70, CRUST, 3)
    ellipse(c, 133, SURF + 152, 8, 10, SKIN_D, NIGHT)
    gland = 1 + (int(pose_t(t) * 4) % 2 if t > t_seb else 0)
    ellipse(c, 158, SURF + 80, 14 + gland, 11 + gland, SEBUM, NIGHT)
    rect(c, 152, SURF + 74, 3, 2, WHITE)
    if t > t_seb:
        for k in range(4):
            yy = SURF + 70 - ((t - t_seb) * 160 + k * 18) % 80
            rect(c, 140 - (SURF + 70 - yy) * 0.15, yy, 3, 3, SEBUM)
        spread = ease_out(prog(t, t_seb + 0.2, t_form + 0.4))
        x0, x1 = int(126 - 126 * spread), int(126 + 240 * spread)
        rect(c, x0, SURF - 4, x1 - x0, 4, SEBUM)
    stick = t > t_form
    for i in range(26):
        ph = (((t - t0) * 0.5 * (3 if fast else 1)) + i / 26) % 1
        x = (i * 53 + 17) % (W - 20) + 10
        if stick:
            y = SURF - 6 - (i % 3) * 3
        else:
            y = SURF - 4 - ph * 150; x += int(6 * np.sin(ph * 9 + i))
        if y < 60: continue
        rect(c, x - 1, y - 1, 10, 6, NIGHT if not stick else SKIN_M)
        rect(c, x, y, 8, 4, SKIN); rect(c, x, y, 8, 1, WHITE if not stick else SKIN)
    if stick:
        th = ease_io(prog(t, t_form, Sd(2, 2) - 0.1)) * 20
        if th >= 1:
            top = SURF - 2 - th - 3 * np.sin(XX / 11.0) - 2 * np.sin(XX / 5.0 + 1)
            m = (YY >= top) & (YY < SURF + 2)
            c[m] = CRUST
            dither(c, m & (YY < top + 3), SKIN_D, 8)
            dither(c, m & (YY > SURF - 4), SEBUM, 4)
    if t > t_seb:
        draw_text(c, [("SÉBUM", SEBUM)], 230, SURF + 72, 18, t=t)
        line(c, 196, SURF + 82, 176, SURF + 82, WHITE, 1)
    if t > t_cr:
        draw_text(c, [("CROÛTE", WHITE)], 270, SURF - 64, 20)
        line(c, 270, SURF - 40, 262, SURF - 22, WHITE, 1)
    if fast:
        badge(c, 312, 50, "×1000", size=16)
    if t > t_30 - 0.1:
        n = int(30000 * ease_out(prog(t, t_30, t_30 + 0.7)))
        title(c, t, t_30 - 0.1, [(f"{n:,}".replace(",", " "), YELLOW)], 54 + TY, 40)
        title(c, t, t_30 + 0.3, [("CELLULES / MIN", WHITE)], 100 + TY, 22)


def s3_cheveux(c, t):
    t0, t_br, t_fr = Sd(2, 2), Wd(2, "brillent"), Wd(2, "frite")
    vgrad(c, 0, H, [NIGHT2, NIGHT3, NIGHT2])
    # mèche de cheveux grasse (vue loupe)
    for k in range(9):
        x0 = 60 + k * 14
        for y in range(170, 480, 2):
            x = x0 + int(10 * np.sin(y / 40.0 + k * 0.6)) + (y - 170) // 12
            rect(c, x - 1, y, 6, 2, NIGHT); rect(c, x, y, 4, 2, CRUST)
            if (y + k * 7 + int(pose_t(t) * 24)) % 30 < 4 and t > t_br - 0.2:
                rect(c, x + 1, y, 2, 2, SEBUM if (y // 30) % 2 else WHITE)
    if t > t_br:
        for k, (sx, sy) in enumerate([(90, 220), (150, 300), (120, 400), (180, 260)]):
            sparkle(c, sx, sy, t + k * 0.2, WHITE)
        title(c, t, t_br, [("GRAS !", SEBUM, "drip")], 70 + TY, 34)
    else:
        title(c, t, t0, [("TES CHEVEUX", WHITE)], 70 + TY, 30)
    if t > t_fr - 0.1:
        b = title_bounce(t, t_fr - 0.1, h=40) or 0
        draw_text(c, [("=", WHITE)], 250, 300 + b, 40)
        fry(c, 300, 400 + b, 1.3)
        sparkle(c, 290, 330 + b, t, WHITE)


def s3_bus(c, t):
    t0, t_vide = Sd(2, 3), Wd(2, "vide")
    shake = int(pose_t(t) * 12) % 2
    bus(c, t)
    seat(c, 40, 440 + shake); seat(c, 88, 440 + shake)
    # les autres, tous serrés à droite
    for k, x in enumerate((215, 245, 275, 305, 335)):
        person(c, x, 470 + (shake if k % 2 else 0), t + k * 0.3, flip=True, clothespin=k % 2 == 0)
    PIP_BOX["box"] = pip(c, 62, 432 + shake, t, pose="idle" if t < t_vide else "surprised",
                         mood="smile" if t < t_vide else "sad", spots=3)
    stink(c, 62, 390, t, n=3, h=24)
    if t > t_vide - 0.2:
        sparkle(c, 110, 400, t, YELLOW); sparkle(c, 98, 380, t + 0.3, YELLOW)
        badge(c, 110, 350, "LIBRE", fg=RED, size=16)
    title(c, t, t0, [("DANS LE BUS", WHITE)], 70 + TY, 30)
    if t > t_vide:
        title(c, t, t_vide, [("PLACE ", WHITE), ("VIDE", RED, "shake")], 116 + TY, 26)


# ---------------- scène 4 : 3 MOIS — mycoses puis téléphone ----------------
def fold_y(x):
    """Deux bosses de peau qui se rejoignent en un pli au centre."""
    d = (abs(x - 180) - 90) / 90.0
    return 300 + 120 * d * d


def s4(c, t):
    if t < Sd(3, 3):
        s4_pli(c, t)
    else:
        s4_tel(c, t)
    stage_overlay(c, t, 3)


def s4_pli(c, t):
    t0 = BOUNDS[3]
    t_pire, t_plis, t_ch, t_champ, t_gr, t_rou, t_inf = (
        Wd(3, "pire"), Wd(3, "plis"), Wd(3, "chauds"), Wd(3, "champ"), Wd(3, "gratte"),
        Wd(3, "rougit"), Wd(3, "s'infecte"))
    vgrad(c, 0, H, [NIGHT, NIGHT2, NIGHT2])
    top = np.array([fold_y(x) for x in range(W)])
    m = YY >= top[None, :]
    c[m] = SKIN
    dither(c, m & (np.abs(XX - 180) < 70), SKIN_M, 6)
    dither(c, m & (np.abs(XX - 180) < 36), SKIN_M, 12)
    dither(c, m & (np.abs(XX - 180) < 14), SKIN_D, 10)
    edge = m & ~np.roll(m, 1, 0)
    c[dilate(edge) & ~m] = NIGHT
    yc = int(fold_y(180))
    rect(c, 179, yc - 2, 2, H - yc, SKIN_D); rect(c, 180, yc + 10, 1, H - yc, NIGHT2)
    for x in (60, 100, 260, 310):
        y = int(fold_y(x))
        rect(c, x - 8, y, 16, 4, CRUST); rect(c, x - 6, y - 1, 10, 1, CRUST)
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
    spots = [(160, 0.0), (200, 0.1), (140, 0.2), (222, 0.3), (118, 0.42), (244, 0.5), (60, 0.62), (316, 0.7)]
    for x, d in spots:
        mush(c, x, int(fold_y(x)) + 1, 8 + (x * 7) % 5, t - (t_champ + d))
    if t > t_gr:
        lvl = int(4 + 10 * prog(t, t_rou, t_rou + 0.5))
        red = m & (np.abs(XX - 180) < 20 + 40 * prog(t, t_rou, t_rou + 0.6)) & (YY < top[None, :] + 40)
        if int(pose_t(t) * 4) % 2 or t > t_rou: dither(c, red, RED, lvl)
    if t > t_inf:
        for i, x in enumerate((140, 220, 180)):
            p = ease_out(prog(t, t_inf + i * 0.1, t_inf + i * 0.1 + 0.25))
            if p > 0: bact(c, x, int(fold_y(x)) + 18, max(2, int(6 * p)), t, col=RED, dark=SKIN_D, angry=True, seed=i)
    px = 268; py = int(fold_y(px)) + 2
    sc = t > t_gr
    PIP_BOX["box"] = pip(c, px, py, t, pose="scratch" if sc else ("surprised" if t > t_champ else "idle"),
                         mood="yuck" if sc else ("wow" if t > t_champ else "smile"), look=(-1, 1), spots=5)
    mush(c, px - 1, py - 32, 6, t - (t_champ + 0.55))
    if sc:
        for k in range(3):
            if (int(pose_t(t) * 12) + k) % 3 == 0:
                line(c, px - 18 - k * 3, py - 20 + k * 5, px - 12 - k * 3, py - 26 + k * 5, WHITE, 1)
    if t_pire - 0.2 < t < t_champ:
        draw_text(c, [("!", YELLOW)], px, py - 64, 24, t=t)
    if t < t_champ:
        title(c, t, Wd(3, "la"), [("SAUF QUE…", MUSH)], 70 + TY, 30)
        if t > t_plis:
            draw_text(c, [("PLI", WHITE)], 180, int(fold_y(180)) - 90, 18)
            line(c, 180, int(fold_y(180)) - 66, 180, int(fold_y(180)) - 12, WHITE, 1)
    else:
        title(c, t, t_champ, [("MYCOSES", MUSH, "wave")], 62 + TY, 42)
        if t > t_gr:
            title(c, t, t_gr, [("ÇA GRATTE !", RED, "shake")], 114 + TY, 22)


def s4_tel(c, t):
    t0 = Sd(3, 3)
    t_po, t_rep, t_msg = Wd(3, "potes"), Wd(3, "répondent"), Wd(3, "messages")
    vgrad(c, 0, H, [NIGHT2, NIGHT3, NIGHT2])
    phone(c, 70, 160, 220, 380)
    draw_text(c, [("LES POTES (5)", WHITE)], 180, 168, 16, shadow=False)
    msgs = [("CINÉ CE SOIR ?", t0 + 0.05), ("ALLÔ ???", t_rep), ("J'AI CHANGÉ DE T-SHIRT !", t_msg - 0.1)]
    for k, (txt, tm) in enumerate(msgs):
        if t > tm:
            b = min(0, int(-10 * (1 - prog(t, tm, tm + 0.15))))
            chat_bubble(c, 280, 216 + k * 70 + b, txt, BACT, seen=t > tm + 0.35, size=14 if len(txt) > 16 else 16)
    # « en train d'écrire… » qui disparaît
    if t_po < t < t_rep:
        for k in range(3):
            if (int(pose_t(t) * 6) + k) % 3: rect(c, 90 + k * 8, 480, 4, 4, GREY)
    title(c, t, t0, [("0", RED), (" RÉPONSE", WHITE)], 70 + TY, 30)


# ---------------- scène 5 : 1 AN — réponse, la rue se vide, le chat part ----------------
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
    t_sv, t_mais, t_mal, t_monde, t_fuit, t_chat = (Wd(4, "survis"), Wd(4, "mais"), Wd(4, "malade"),
                                                     Wd(4, "monde"), Wd(4, "fuit"), Wd(4, "chat"))
    street(c, t)
    t_run = t_fuit - 0.25
    for i, (x, side) in enumerate(PEOPLE):
        if t < t_run:
            person(c, x, 492, t + i * 0.2, flip=(side == 0) if t > t_monde else (side == 1))
        else:
            xx = x + (t - t_run) * 520 * (-1 if side else 1)
            if -40 < xx < W + 40:
                person(c, xx, 492, t + i * 0.1, run=1, flip=(side == 1))
                for k in range(3):
                    circle(c, xx - (-1 if side else 1) * (16 + k * 9), 488, 3 - k, WHITE)
    spots = 5 + int(5 * prog(t, t_mal, t_mal + 0.4))
    mood = "sad" if t > t_fuit + 0.2 else ("stars" if t_sv <= t < t_mais else ("wow" if t > t_run else "smile"))
    PIP_BOX["box"] = pip(c, 180, 492, t, pose="happy" if t_sv <= t < t_mais else "idle", mood=mood,
                         spots=spots, look=(0, 0) if t < t_run else ((1, 0) if t > t_chat else (-1, 0)))
    stink(c, 180, 446, t, n=3, h=24)
    # le chat, valise à la main, quitte Pip
    if t > t_chat - 0.3:
        cx = 210 + (t - t_chat + 0.3) * 120
        cat(c, int(cx), 494, t, flip=False)
    if t < t_sv - 0.05:
        title(c, t, t0 + 0.6, [("PLUS TARD…", WHITE)], 74 + TY, 26)
    elif t < t_fuit:
        title(c, t, t_sv, [("TU SURVIS", YELLOW)], 60 + TY, 38)
        if t > t_mais: title(c, t, t_mais, [("MAIS…", RED)], 110 + TY, 26)
        if t_sv < t < t_mais:
            for k, (sx, sy) in enumerate([(60, 110), (300, 120), (80, 160), (285, 165)]):
                sparkle(c, sx, sy, t + k * 0.13, YELLOW)
    elif t < t_chat:
        title(c, t, t_fuit, [("ON TE ", WHITE), ("FUIT", RED, "shake"), (" !", WHITE)], 62 + TY, 40)
    else:
        title(c, t, t_chat, [("MÊME TON ", WHITE), ("CHAT", YELLOW, "shake")], 66 + TY, 34)
        if t > Wd(4, "valises"): title(c, t, Wd(4, "valises"), [("ADIEU !", RED)], 114 + TY, 24)
    stage_overlay(c, t, 4)


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
