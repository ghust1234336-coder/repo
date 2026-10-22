"""Épisode « Et si tu effaçais tous les moustiques ? » — style Vox (collage papier).

python episode_moustiques.py --preview   (540x960, sans grain)
python episode_moustiques.py --final     (1080x1920, 30 i/s, avec audio/mix.wav)
"""
import math, os, subprocess, sys
import numpy as np
from vox import *
from decors_moustiques import *
from pip_vox import pip
import timeline as TL
from timeline import W as Wd, S as Sd

PIP_ACTIONS = {
    1: ("utiliser_objet", "lève sa baguette magique sur Zézette"),
    2: ("reagir", "« ! » au pied du podium"),
    3: None,
    4: ("subir", "des mâles se posent sur la fleur de son chapeau, il vacille"),
    5: ("reagir", "yeux en étoiles"),
    6: ("se_deplacer", "traverse la toundra en luge"),
    7: None,
    8: ("agir_corps", "saute sur le bouton S'ABONNER"),
}

PIP_BOX = {}
CAPTION_ZONE = (0, 1500, W, 200)
PIP_FEET_Y = 264          # y des pieds dans le sprite de Pip (pip_vox : BY + RY + 12)


def pip_pt(fx, fy, scale, sx, sy):
    """Point (sx, sy) du sprite de Pip -> écran, pour Pip placé pieds en (fx, fy)."""
    return fx + (sx - 125) * scale, fy - (PIP_FEET_Y - sy) * scale


FLOWER = (161, 126)       # fleur du chapeau
HAND_R = (223, 140)       # main droite en pose « point »
EYES = ((103, 178), (147, 178))


# ---------- briques communes ----------
def title(base, t, t0, lines, y, size=86, hl=(), hl_delay=0.15, rot=-1.5, kind="bold", paper_col="white"):
    """Titre en bande de papier qui tombe (rebond), mot(s) surligné(s) ensuite."""
    if t < t0:
        return
    p = prog(t, t0, t0 + 0.32)
    im = text_block(lines, size, kind=kind, hl=hl, hl_p=prog(t, t0 + hl_delay, t0 + hl_delay + 0.35),
                    paper_col=paper_col)
    spr = Sprite(im, border=0, name="title")
    put(base, spr, W / 2, y - 60 * (1 - back_out(p)), 1.0, rot + boil(t, 7, 0.3), alpha=min(1, p * 3))


def label(base, t, t0, s, x, y, size=34, kind="mono", fill="ink", bg="yellow", rot=0):
    if t < t0:
        return
    p = prog(t, t0, t0 + 0.25)
    im = text_block([s], size, kind=kind, fill=fill, paper_col=bg, pad=(16, 8))
    put(base, Sprite(im, border=0, name="label"), x, y, 0.6 + 0.4 * back_out(p), rot, shadow=(6, 8))


def hand(base, t, t0, s, x, y, size=64, col="red", rot=-4):
    """Écriture à la main qui apparaît lettre à lettre."""
    if t < t0:
        return
    n = int(len(s) * prog(t, t0, t0 + 0.035 * len(s) + 0.05))
    if n <= 0:
        return
    tmp = layer(int(text_size(s, "hand", size)[0] + 40), int(size * 1.6))
    ImageDraw.Draw(tmp).text((20, 4), s[:n], font=font("hand", size), fill=C[col] + (255,))
    tmp = tmp.rotate(rot, resample=Image.BICUBIC, expand=True)
    paste(base, tmp, x - tmp.width / 2, y - tmp.height / 2)


def cut(t, *starts):
    """Indice du plan courant (coupes franches calées sur les phrases)."""
    k = 0
    for i, s in enumerate(starts):
        if t >= s - 0.04:
            k = i + 1
    return k


def flight(t, cx, cy, rx, ry, speed=1.6, seed=0):
    """Vol en huit, avec un petit zigzag de moustique. Renvoie (x, y, va_vers_la_droite)."""
    a = t * speed + seed
    x = cx + rx * math.sin(a) + 10 * math.sin(t * 23 + seed)
    y = cy + ry * math.sin(2 * a) + 8 * math.sin(t * 31 + seed)
    return x, y, math.cos(a) > 0


def mosquito(base, t, x, y, scale, right, seed=0, trail=True, kind="zez"):
    if trail:
        d = ImageDraw.Draw(base)
        for k in range(1, 9):
            tx, ty, _ = flight(t - k * 0.06, *trail) if isinstance(trail, tuple) else (x, y, 0)
            r = 5 - k * 0.4
            d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=(255, 255, 255, 150 - k * 14))
    if kind == "zez":
        spr = ZEZ_FLIP() if right else ZEZETTE()
    else:
        spr = _flip_cache(BZZ()) if right else BZZ()
    put(base, spr, x, y, scale, boil(t, seed, 3) + 4 * math.sin(t * 40))


_FLIPS = {}


def _flip_cache(spr):
    if spr.name not in _FLIPS:
        _FLIPS[spr.name] = Sprite(spr.im.transpose(Image.FLIP_LEFT_RIGHT), border=0, name=spr.name + "_f")
    return _FLIPS[spr.name]


def star_eyes(base, fx, fy, scale, t):
    d = ImageDraw.Draw(base)
    for ex, ey in EYES:
        x, y = pip_pt(fx, fy, scale, ex, ey)
        star(d, x, y, 24 * scale * (1 + 0.15 * math.sin(t * 14)), "yellow")


# ---------- sous-titres karaoké ----------
ALL_WORDS = [w for sc in TL.SCENES for s in sc["sentences"] for w in s["words"]]


def caption_chunks(words, maxc=22):
    chunks, cur = [], []
    for w in words:
        txt = " ".join(x["w"] for x in cur + [w])
        if cur and len(txt) > maxc:
            chunks.append(cur); cur = [w]
        else:
            cur.append(w)
        if w["w"].rstrip()[-1:] in ".?!" and cur:
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    return chunks


CHUNKS = caption_chunks(ALL_WORDS)


def captions(base, t):
    cur = None
    for ch in CHUNKS:
        if ch[0]["s"] - 0.05 <= t <= ch[-1]["e"] + 0.25:
            cur = ch
    if not cur:
        return
    f = font("bold", 66)
    words = [w["w"].upper() for w in cur]
    sp = f.getlength(" ")
    widths = [f.getlength(w) for w in words]
    tw = sum(widths) + sp * (len(words) - 1)
    x0, y = (W - tw) / 2, 1540
    d = ImageDraw.Draw(base)
    d.rectangle([x0 - 26, y - 14, x0 + tw + 26, y + 86], fill=(255, 255, 255, 240))
    x = x0
    for i, w in enumerate(cur):
        nxt = cur[i + 1]["s"] if i + 1 < len(cur) else w["e"] + 0.25
        if w["s"] - 0.03 <= t < nxt:
            highlight(base, x - 4, y + 2, x + widths[i] + 4, y + 74, 1.0, seed=i)
        x += widths[i] + sp
    x = x0
    for i, wd in enumerate(words):
        d.text((x, y), wd, font=f, fill=C["ink"] + (255,))
        x += widths[i] + sp


# ---------- scènes ----------
PIP_BED = (560, 1058, 0.9)   # Pip debout sur le lit (scènes 1 et 8)


def bedroom(t, end=False):
    base = room().copy()
    fx, fy, sc = PIP_BED
    if not end:
        x, y, right = flight(t, 760, 760, 190, 110, 1.7)
        mosquito(base, t, x, y, 0.5, right, trail=(760, 760, 190, 110, 1.7))
    hide_pip = end and t > Wd(7, "abonne") - 0.05
    if not hide_pip:
        lowered = end and t > Wd(7, "mâle") + 0.3
        pose = "idle" if lowered else "point"
        PIP_BOX["box"] = pip(base, fx, fy, t, pose=pose, scale=sc, look=(1, -1),
                             mood="open" if (not end and t > Wd(0, "effaçais")) else "smile")
        if not lowered:
            hx, hy = pip_pt(fx, fy, sc, *HAND_R)
            put(base, WAND(), hx + 40, hy - 40, 0.9, boil(t, 2, 2))
            if t % 0.25 < 0.13:  # la baguette grésille
                d = ImageDraw.Draw(base)
                rng = np.random.default_rng(int(t * 8))
                for _ in range(5):
                    sx, sy = hx + 90 + rng.uniform(-40, 40), hy - 95 + rng.uniform(-40, 40)
                    star(d, sx, sy, rng.uniform(8, 16), "yellow")
    return base


def s1(t):
    """Accroche : Zézette tourne au-dessus du lit, Pip lève sa baguette."""
    base = bedroom(t)
    title(base, t, 0.08, ["Et si tu effaçais", "tous les moustiques ?"], 330, 84, hl=(3,))
    tp = Wd(0, "planète")
    if t > tp - 0.05:
        p = back_out(prog(t, tp - 0.05, tp + 0.25))
        put(base, EARTH(), 860, 660, 0.42 * p, boil(t, 4, 0.5))
        d = ImageDraw.Draw(base)
        rng = np.random.default_rng(5)
        for i in range(36):
            a, k = rng.uniform(0, 2 * math.pi), math.sqrt(rng.uniform(0, 1)) * 76 * p
            x = 860 + k * math.cos(a) + 3 * math.sin(t * 30 + i)
            y = 660 + k * math.sin(a) + 3 * math.cos(t * 27 + i)
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=C["ink"] + (255,))
    return base


def s2(t):
    k = cut(t, Sd(1, 1), Sd(1, 2))
    base = paper("paper").copy()
    if k == 0:
        put(base, PODIUM(), 500, 1200, 0.86, 0)
        tm = Wd(1, "mortel")
        tic = 8 * math.sin(step_t(t) * 9) if t > tm else 0      # pattes arrière levées
        put(base, ZEZETTE(), 500, 930, 0.6 * back_out(prog(t, Sd(1, 0), Sd(1, 0) + 0.3)), tic)
        put(base, PERSON(), 242, 1010, 0.7, boil(t, 3, 1))
        put(base, SNAKE(), 758, 1095, 0.75, boil(t, 4, 1))
        label(base, t, tm + 0.2, "MOUSTIQUE", 500, 1300, 30)
        label(base, t, tm + 0.35, "HUMAIN", 242, 1330, 26, bg="white")
        label(base, t, tm + 0.5, "SERPENT", 758, 1350, 26, bg="white")
        PIP_BOX["box"] = pip(base, 990, 1450, t, pose="surprised" if t > tm else "idle", scale=0.5,
                             mood="open" if t > tm else "smile", look=(-1, -1))
        hand(base, t, tm, "!", 1000, 1200, 150, col="red", rot=0)
        title(base, t, Sd(1, 0) + 0.05, ["L'animal le plus", "mortel"], 340, 92, hl=(3,),
              hl_delay=max(0.15, tm - Sd(1, 0) - 0.05))
        return base
    if k == 1:
        tp = Wd(1, "paludisme")
        title(base, t, Sd(1, 1) + 0.03, ["Rien qu'avec", "le paludisme"], 340, 86, hl=(3,))
        n = int(600000 * ease_out(prog(t, tp, Wd(1, "morts") + 0.1)) / 1000) * 1000
        txt = "≈ " + f"{n:,}".replace(",", " ")
        draw_text(base, txt, W / 2, 760, 150, kind="bold", fill="red")
        label(base, t, Wd(1, "morts"), "MORTS PAR AN", W / 2, 1000, 52)
        put(base, ZEZETTE(), 760, 1260, 0.5, boil(t, 1, 2))
        return base
    ts = Wd(1, "sept")
    title(base, t, Sd(1, 2) + 0.03, ["× 7 Stades de France"], 330, 80, hl=(1, 2))
    pos = [(220, 700), (540, 700), (860, 700), (220, 950), (540, 950), (860, 950), (540, 1200)]
    for i, (x, y) in enumerate(pos):
        t0 = ts + i * 0.16
        if t < t0 - 0.1:
            continue
        p = back_out(prog(t, t0 - 0.1, t0 + 0.15))
        put(base, STADIUM(full=t > t0 + 0.25), x, y, 0.95 * p, boil(t, i, 0.8))
    hand(base, t, Wd(1, "chaque"), "chaque année !", 540, 1400, 70)
    return base


def s3(t):
    k = cut(t, Sd(2, 1), Sd(2, 2))
    base = paper("paper").copy()
    zw, zh = ZEZETTE().size
    if k == 0:
        cx, cy, sc = 520, 1000, 1.45
        put(base, ZEZETTE(), cx, cy, sc, boil(t, 1, 0.4))
        tq, tt_, tpz = Wd(2, "piqûre"), Wd(2, "tue"), Wd(2, "parasite")
        label(base, t, tq - 0.05, "LA PIQÛRE", 260, 600, 46, kind="bold", bg="white", rot=-3)
        if t > tt_:
            cross(base, 260, 600, 70, prog(t, tt_, tt_ + 0.3))
        if t > tpz - 0.1:
            bx, by = cx + (ZEZ_BELLY[0] - zw / 2 + 14) * sc, cy + (ZEZ_BELLY[1] - zh / 2 + 14) * sc
            put(base, PLASMO_DISC(), 800, 620, back_out(prog(t, tpz - 0.1, tpz + 0.2)), 0)
            marker_arrow(base, 760, 780, bx - 30, by - 10, prog(t, tpz, tpz + 0.4), width=10, bend=0.2)
            title(base, t, tpz - 0.05, ["un parasite"], 330, 92, hl=(1,))
        return base
    if k == 1:
        t1, tm, tpq = Sd(2, 1), Wd(2, "malade"), Wd(2, "pique")
        put(base, ARM(), 220, 1160, 0.75, 0)
        put(base, ARM(flip=True), 860, 1160, 0.75, 0)
        label(base, t, tm - 0.1, "MALADE", 200, 1290, 34, bg="white")
        label(base, t, tpq, "TOI", 880, 1290, 34, bg="white")
        u = ease_io(prog(t, tpq - 0.2, tpq + 0.9))
        x = 300 + 480 * u
        y = 1010 - 260 * math.sin(math.pi * u) + 6 * math.sin(t * 30)
        if t < tm:
            x, y = 300 + 160 * (1 - prog(t, t1, tm)), 1010 - 120 * (1 - prog(t, t1, tm))
        marker_path(base, arrow_pts(300, 1010, 780, 1010, -0.45), prog(t, tpq - 0.2, tpq + 0.9), "red", 8)
        put(base, ZEZETTE(), x, y, 0.55, -6 + boil(t, 2, 2))
        if t > Wd(2, "l'aspire"):
            d = ImageDraw.Draw(base)
            r = 14 * prog(t, Wd(2, "l'aspire"), Wd(2, "l'aspire") + 0.3)
            gx, gy = x + 50, y - 40
            d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=C["parasite"] + (255,), outline=C["ink"] + (255,), width=3)
        title(base, t, t1 + 0.03, ["La femelle"], 330, 92, hl=(1,))
        hand(base, t, tpq, "malade > toi", 540, 620, 78)
        return base
    tx = Wd(2, "taxi")
    cx, cy = 540, 980 + 10 * math.sin(t * 6)
    put(base, ZEZETTE(), cx, cy, 1.2, boil(t, 1, 1.5))
    put(base, PARASITE(cap=True), cx + 120, cy - 150, 0.85 * back_out(prog(t, Sd(2, 2), Sd(2, 2) + 0.3)), 6)
    if t > tx - 0.05:
        p = prog(t, tx - 0.05, tx + 0.15)
        im = text_block(["TAXI"], 120, fill="ink", paper_col="yellow")
        d = ImageDraw.Draw(im)
        for i in range(0, im.width, 24):
            d.rectangle([i, im.height - 16, i + 12, im.height - 8], fill=C["ink"] + (255,))
            d.rectangle([i + 12, im.height - 8, i + 24, im.height], fill=C["ink"] + (255,))
        put(base, Sprite(im, border=0), cx + 140, cy - 330, 1.35 - 0.35 * back_out(p), -8)
    title(base, t, Sd(2, 2) + 0.03, ["Pour les microbes…"], 330, 80, hl=(2,))
    return base


def s4(t):
    k = cut(t, Sd(3, 1), Sd(3, 2))
    base = paper("paper").copy()
    if k == 0:
        t0, tp = Sd(3, 0), Wd(3, "peu")
        zoom = 2.2 - 1.3 * ease_io(prog(t, t0, t0 + 1.0))
        put(base, BOARD(1 if t > tp else 0), 540, 1010 + 400 * (zoom - 0.9), zoom, 0)
        title(base, t, Wd(3, "trois") - 0.05, ["3 500 espèces"], 330, 92, hl=(0, 1))
        if t > tp:
            top = 1010 - BOARD_H * 0.9 / 2 + 20 * 0.9
            band = BOARD_RED_ROWS * (BOARD_H - 40) / BOARD_ROWS * 0.9
            marker_path(base, hand_ellipse(540, top + band / 2, 450, band / 2 + 26, 2), prog(t, tp, tp + 0.45), "red", 9)
            label(base, t, tp + 0.2, "QUELQUES CENTAINES NOUS PIQUENT", W / 2, 490, 32)
        return base
    if k == 1:
        t1 = Sd(3, 1)
        fx, fy, sc = 540, 1380, 1.25
        landed = [t1 + 0.25 + i * 0.32 for i in range(6)]
        n = sum(t > l + 0.35 for l in landed)
        wob = n * 2.2 * math.sin(t * 7)
        PIP_BOX["box"] = pip(base, fx, fy, t, pose="wobble" if n else "idle", scale=sc, rot=wob,
                             mood="worried" if n > 2 else "smile", look=(0.3, -1))
        flx, fly = pip_pt(fx, fy, sc, *FLOWER)
        starts = [(-150, 700), (1230, 820), (-150, 1100), (1230, 560), (540, 380), (1230, 1150)]
        spots = [(-60, -70), (60, -80), (-90, -20), (100, -20), (0, -120), (40, 30)]
        for i, l in enumerate(landed):
            if t < l - 0.6:
                continue
            u = ease_out(prog(t, l - 0.6, l + 0.35))
            sx, sy = starts[i]
            x = sx + (flx + spots[i][0] - sx) * u + (1 - u) * 20 * math.sin(t * 20 + i)
            y = sy + (fly + spots[i][1] - sy) * u
            right = sx < flx
            put(base, _flip_cache(BZZ()) if not right else BZZ(), x, y, 0.42, boil(t, i, 3) + wob * 0.5)
        label(base, t, Wd(3, "jamais"), "MÂLES : 0 PIQÛRE", W / 2, 520, 40)
        hand(base, t, Wd(3, "nectar"), "nectar !", 860, 760, 76)
        title(base, t, t1 + 0.03, ["Les mâles"], 330, 92, hl=(1,))
        return base
    t2 = Sd(3, 2)
    put(base, CLIPPING(), W / 2, 980 + 500 * (1 - ease_out(prog(t, t2, t2 + 0.3))), 1.0, -3 + boil(t, 2, 0.4))
    title(base, t, Wd(3, "qui") - 0.05, ["Qui va les regretter ?"], 330, 82, hl=(3,))
    return base


def flying_letters(base, t, t0, word, y, size):
    """Mot-choc : la bande « personne » tombe sur le mot, puis ses lettres s'envolent comme des moustiques."""
    f = font("bold", size)
    tw = f.getlength(word)
    lay = layer(int(tw + 80), int(size * 1.5))
    d = ImageDraw.Draw(lay)
    strip = 1 - prog(t, t0 + 1.1, t0 + 1.3)
    d.rectangle([0, 0, lay.width, lay.height], fill=(255, 255, 255, int(255 * strip)))
    highlight(lay, 34, size * 0.2, 46 + tw, size * 1.3, prog(t, t0 + 0.05, t0 + 0.35) * strip, seed=3,
              alpha=int(235 * strip))
    paste(base, lay, W / 2 - lay.width / 2, y - lay.height / 2)
    order = np.random.default_rng(4).permutation(len(word))
    x0 = W / 2 - tw / 2
    for i, ch in enumerate(word):
        st = t0 + 0.45 + order[i] * 0.09
        u = prog(t, st, st + 0.8)
        if u >= 1:
            continue
        x = x0 + f.getlength(word[:i]) + 120 * u * math.sin(i * 1.7) + 18 * u * math.sin(t * 25 + i)
        yy = y - size * 0.55 - 700 * u ** 1.6
        lay2 = layer(int(size * 1.2), int(size * 1.4))
        d2 = ImageDraw.Draw(lay2)
        d2.text((10, 0), ch, font=f, fill=C["ink"] + (int(255 * (1 - u ** 3)),))
        if u > 0:  # petites ailes
            a = int(150 * (1 - u))
            for side in (-1, 1):
                d2.ellipse([size * 0.3 + side * 22, 0, size * 0.55 + side * 22, size * 0.25], fill=C["wing"] + (a,))
        lay2 = lay2.rotate(30 * math.sin(t * 20 + i) * u, resample=Image.BICUBIC)
        paste(base, lay2, x - 10, yy)


def s5(t):
    k = cut(t, Sd(4, 1), Sd(4, 2))
    base = paper("paper").copy()
    if k == 0:
        t0 = Sd(4, 0)
        label(base, t, t0 + 0.02, "RÉPONSE DES BIOLOGISTES :", W / 2, 560, 40)
        tp, tn = Wd(4, "presque"), Wd(4, "personne")
        title(base, t, tp - 0.05, ["Presque"], 800, 100, rot=-2)
        if t > tn - 0.05:
            flying_letters(base, t, tn - 0.05, "PERSONNE", 990, 150)
        return base
    if k == 1:
        put(base, MENU(), 600, 960, 0.85, -2 + boil(t, 3, 0.3))
        mx0, my0 = 600 - 640 * 0.85 / 2, 960 - 700 * 0.85 / 2
        for spr, w_, y, sc in ((BIRD(), "oiseaux", 760, 0.8), (FISH(), "poissons", 1010, 0.85),
                               (DRAGONFLY(), "libellules", 1250, 0.7)):
            tw_ = Wd(4, w_)
            if t > tw_ - 0.1:
                put(base, spr, 160, y, sc * back_out(prog(t, tw_ - 0.1, tw_ + 0.2)), boil(t, y, 2))
        tmg, ti = Wd(4, "mangeraient"), Wd(4, "insectes")
        ym = my0 + MENU_ROW_Y[0] * 0.85
        marker_path(base, [(mx0 + 40, ym), (mx0 + 400, ym - 6)], prog(t, tmg - 0.2, tmg + 0.25), "red", 12)
        if t > ti - 0.1:
            yc = my0 + (MENU_ROW_Y[1] + MENU_ROW_Y[4]) / 2 * 0.85
            marker_path(base, hand_ellipse(mx0 + 230, yc, 230, 190, 4), prog(t, ti - 0.1, ti + 0.4), "red", 9)
            hand(base, t, ti + 0.2, "autres insectes", 600, 1390, 70)
        title(base, t, Sd(4, 1) + 0.03, ["Ils changent de menu"], 330, 80, hl=(3,))
        return base
    t2, tv = Sd(4, 2), Wd(4, "vies")
    cols, rows = 7, 5
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            on = t > t2 + 0.2 + i * 0.045
            col = [C["pip"], C["yellow"], C["red"], C["pip_p"], C["kraft"]][i % 5] if on else (150, 146, 160)
            put(base, PERSON(col), 160 + c * 118, 640 + r * 150, 0.5 * (1.12 if on and t < t2 + 0.35 + i * 0.045 else 1),
                0, shadow=(4, 6))
    title(base, t, Wd(4, "centaines") - 0.1, ["Des centaines de milliers", "de vies"], 340, 80, hl=(5,),
          hl_delay=max(0.15, tv - Wd(4, "centaines") + 0.1))
    fx, fy, sc = 975, 1450, 0.5
    PIP_BOX["box"] = pip(base, fx, fy, t, pose="happy", scale=sc, mood="open")
    if t > tv - 0.2:
        star_eyes(base, fx, fy, sc, t)
    return base


_CLOUD = {}


def cloud(phase):
    if phase not in _CLOUD:
        def fn(x, y, ph=phase):
            dx, dy = (x - 540) / 520, (y - 260) / 210
            r = dx * dx + dy * dy
            v = max(0.0, 1 - r) * (0.55 + 0.45 * math.sin(x / 37 + ph * 1.3) * math.sin(y / 29 - ph))
            return max(0.0, min(1.0, v))
        _CLOUD[phase] = halftone(W, 520, fn, cell=14, color=(40, 34, 30, 230))
    return _CLOUD[phase]


def s6(t):
    k = cut(t, Sd(5, 1))
    if k == 0:
        base = meadow().copy()
        right = tundra().crop((540, 0, W, H))
        base.alpha_composite(right, (540, 0))
        d = ImageDraw.Draw(base)
        d.line([(540, 440), (540, 1500)], fill=(250, 248, 243, 255), width=14)
        label(base, t, Sd(5, 0) + 0.2, "AILLEURS", 270, 900, 34, bg="white")
        label(base, t, Sd(5, 0) + 0.4, "GRAND NORD", 810, 900, 34, bg="white")
        title(base, t, Sd(5, 0) + 0.03, ["Aucun animal ?"], 330, 92, hl=(1,))
        return base
    base = tundra().copy()
    t1 = Sd(5, 1)
    base.alpha_composite(cloud(int(step_t(t, 6)) % 6), (0, 470 + int(8 * math.sin(t * 2))))
    tp = Wd(5, "poussins")
    d = ImageDraw.Draw(base)
    for i, x in enumerate((300, 560, 800)):
        bob = 18 * abs(math.sin(step_t(t) * 7 + i)) if t > tp else 0
        put(base, CHICK(), x, 1180 + bob, 0.8 * back_out(prog(t, tp - 0.3 + i * 0.1, tp + i * 0.1)), -8 * (bob > 8))
    rng = np.random.default_rng(int(step_t(t, 12) * 12))
    for _ in range(26):
        x, y = rng.uniform(150, 930), rng.uniform(1000, 1120)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(40, 34, 30, 255))
    label(base, t, tp, "BUFFET POUR POUSSINS", W / 2, 1330, 36)
    title(base, t, Wd(5, "grand") - 0.05, ["Grand Nord"], 330, 100, hl=(1,))
    # Pip traverse en luge
    u = prog(t, t1 + 0.2, TL.BOUNDS[6] + 0.2)
    fx, fy = -160 + 1400 * u, 1430
    put(base, SLED(), fx, fy + 22, 0.62, 0, shadow=(4, 6))
    PIP_BOX["box"] = pip(base, fx, fy, t, pose="happy", scale=0.6, look=(1, 0))
    return base


def s7(t):
    k = cut(t, Sd(6, 1))
    base = paper("paper").copy()
    if k == 0:
        put(base, BOARD(0), 540, 1010, 0.9, 0)
        te, tv = Wd(6, "espèces"), Wd(6, "visent")
        targets = [(330, 820), (740, 1170)]
        cards = ["anopheles_gambiae.jpg", "aedes_aegypti.jpg"]
        for i, ((x, y), c) in enumerate(zip(targets, cards)):
            t0 = te + i * 0.3
            if t > t0 - 0.1:
                put(base, PHOTO_CARD(c, 360), x, y, back_out(prog(t, t0 - 0.1, t0 + 0.2)) * 0.9, (-4, 5)[i])
        # réticule qui balaie puis verrouille
        u = prog(t, tv, te + 0.6)
        if u < 0.5:
            rx, ry = 200 + 700 * u * 2, 700 + 300 * math.sin(u * 9)
        else:
            j = 0 if u < 0.75 else 1
            rx, ry = targets[j]
        if t > tv:
            d = ImageDraw.Draw(base)
            locked = u >= 1
            for (x, y) in (targets if locked else [(rx, ry)]):
                d.ellipse([x - 150, y - 150, x + 150, y + 150], outline=C["red"] + (255,), width=10)
                for a in range(4):
                    ca, sa = math.cos(a * math.pi / 2), math.sin(a * math.pi / 2)
                    d.line([(x + ca * 120, y + sa * 120), (x + ca * 185, y + sa * 185)], fill=C["red"] + (255,), width=10)
        title(base, t, tv - 0.05, ["On vise juste"], 330, 96, hl=(1,))
        label(base, t, Wd(6, "dangereuses"), "ESPÈCES DANGEREUSES SEULEMENT", W / 2, 500, 32)
        return base
    t1, tf, tj = Sd(6, 1), Wd(6, "filles"), Wd(6, "jeunes")
    put(base, BOX(), 260, 1230, 0.9, boil(t, 3, 0.5))
    for i in range(5):
        st = Wd(6, "lâchent") + i * 0.18
        if t < st:
            continue
        u = prog(t, st, st + 1.4)
        x = 260 + 300 * u + 40 * math.sin(t * 9 + i * 2)
        y = 1120 - 520 * u + 30 * math.sin(t * 7 + i)
        put(base, BZZ(), x, y, 0.32, boil(t, i, 4))
    # arbre généalogique au feutre
    d = ImageDraw.Draw(base)
    rx_, ry_ = 760, 700
    p0 = prog(t, Wd(6, "mâles") - 0.1, Wd(6, "mâles") + 0.3)
    if p0 > 0:
        label(base, t, Wd(6, "mâles") - 0.1, "MÂLE M", rx_, ry_, 34)
        marker_path(base, [(rx_, ry_ + 30), (rx_, ry_ + 110), (600, ry_ + 110), (600, ry_ + 190)], prog(t, tf - 0.5, tf - 0.1), "ink", 7)
        marker_path(base, [(rx_, ry_ + 110), (920, ry_ + 110), (920, ry_ + 190)], prog(t, tf - 0.5, tf - 0.1), "ink", 7)
    if t > tf - 0.15:
        label(base, t, tf - 0.15, "FILS", 600, ry_ + 230, 34, bg="white")
        label(base, t, tf - 0.05, "FILLES", 920, ry_ + 230, 34, bg="white")
        marker_path(base, [(600, ry_ + 270), (600, ry_ + 400)], prog(t, tf, tf + 0.4), "ink", 7)
        hand(base, t, tf + 0.3, "vivent", 600, ry_ + 450, 56, col="ink", rot=0)
    if t > tj - 0.1:
        cross(base, 920, ry_ + 230, 80, prog(t, tj - 0.1, tj + 0.25))
        hand(base, t, tj + 0.15, "0 fille adulte", 820, ry_ + 420, 60)
    title(base, t, t1 + 0.03, ["Mâles modifiés"], 330, 92, hl=(0,))
    return base


def s8(t):
    base = bedroom(t, end=True)
    tc, tm, ta = Sd(7, 0), Wd(7, "mâle"), Wd(7, "abonne")
    x, y, right = flight(t, 760, 740, 170, 90, 1.5, seed=2)
    mosquito(base, t, x, y, 0.5, right, seed=2, trail=(760, 740, 170, 90, 1.5, 2), kind="bzz")
    tl = Wd(7, "c'est") - 0.1
    if tl < t < ta + 0.15:
        p = back_out(prog(t, tl, tl + 0.3)) * (1 - prog(t, ta - 0.05, ta + 0.15))
        zoom = BZZ(big=True).im
        crop = zoom.crop((0, 0, 360, 360)).resize((300, 300))
        m = supersample(300, 300, lambda d, s: d.ellipse([0, 0, 300 * s, 300 * s], fill=(255, 255, 255, 255)))
        disc = Image.new("RGBA", (300, 300), (250, 248, 243, 255))
        disc.alpha_composite(crop)
        disc.putalpha(m.split()[3])
        lx, ly = 760, 560
        put(base, Sprite(disc, border=0, shadow=False, name="zoom"), lx, ly, p, 0)
        put(base, LOUPE(150), lx + 22 * p, ly + 22 * p, p, 0)
        if t < ta - 0.05:
            marker_path(base, hand_ellipse(lx - 40, ly - 45, 85, 75, 7), prog(t, tm, tm + 0.3), "red", 7)
            label(base, t, tm, "ANTENNES PLUMEUSES = MÂLE", W / 2, 840, 30)
    if t < ta + 0.05:
        title(base, t, tc + 0.03, ["C'est un mâle"], 330, 96, hl=(2,), hl_delay=max(0.15, tm - tc))
    if t > ta - 0.1:
        p = prog(t, ta - 0.1, ta + 0.2)
        press = 0.92 if ta + 0.45 <= t < ta + 0.6 else 1.0
        put(base, BUTTON(), W / 2, 1300, back_out(p) * press, -2)
        title(base, t, ta + 0.1, ["Abonne-toi", "pour d'autres secrets !"], 420, 72, hl=(0, 4), rot=1.5)
    return base


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ZOOM = 0.035


def render_scene(i, t):
    im = SCENES[i](t)
    a, b = TL.BOUNDS[i], TL.BOUNDS[i + 1]
    return camera(im, t, 1 + ZOOM * prog(t, a, b))


def overlay_pip_s8(im, t):
    """Pip saute sur le bouton S'ABONNER (au-dessus du zoom pour rester net)."""
    ta = Wd(7, "abonne")
    if t > ta - 0.05:
        fx0, fy0, sc = PIP_BED
        tl = ta + 0.45                      # atterrissage sur le bouton
        u = prog(t, ta - 0.05, tl)
        x = fx0 + (W / 2 - fx0) * u
        y = fy0 - 380 * math.sin(math.pi * u) + (1300 - 75 - fy0) * u
        if t > tl:
            y = 1300 - 75 - 40 * abs(math.sin((t - tl) * 6)) * math.exp(-(t - tl) * 2)
        PIP_BOX["box"] = pip(im, x, y, t, pose="jump" if t < tl else "happy", scale=0.75)


def frame(t):
    i = TL.scene_at(t)
    im = render_scene(i, t)
    if i == 7:
        overlay_pip_s8(im, t)
    for b_i in range(1, TL.N):
        bnd = TL.BOUNDS[b_i]
        if bnd - TL.TRANS / 2 <= t < bnd + TL.TRANS / 2:
            p = prog(t, bnd - TL.TRANS / 2, bnd + TL.TRANS / 2)
            a = render_scene(b_i - 1, min(t, bnd - 0.01))
            b = render_scene(b_i, max(t, bnd))
            im = torn_wipe(a, b, p)
    captions(im, t)
    return im


def render(path, scale, audio=None, t0=0.0, t1=None, grain=True):
    t1 = TL.DURATION if t1 is None else t1
    size = (int(W * scale), int(H * scale))
    wr = Writer(path, size, audio)
    n0, n1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    for k in range(n0, n1):
        t = k / FPS
        im = frame(t)
        rgb = finish(im, t) if grain else np.asarray(im.convert("RGB"))
        if scale != 1:
            rgb = np.asarray(Image.fromarray(rgb).resize(size, Image.BILINEAR))
        wr.write(rgb)
        if k % 60 == 0:
            print(f"  {t:5.1f}s", flush=True)
    wr.close()


def main():
    import multiprocessing as mp
    final = "--final" in sys.argv
    scale = 1 if final else 0.5
    out = os.path.join(ROOT, "renders")
    os.makedirs(out, exist_ok=True)
    nproc = 4
    edges = np.linspace(0, TL.DURATION, nproc + 1)
    parts = [os.path.join(out, f"_part{k}.mp4") for k in range(nproc)]
    jobs = [mp.Process(target=render, args=(parts[k], scale, None, edges[k], edges[k + 1], final))
            for k in range(nproc)]
    for j in jobs: j.start()
    for j in jobs: j.join()
    lst = os.path.join(out, "_parts.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    name = "moustiques.mp4" if final else "moustiques_preview.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-i", os.path.join(ROOT, "audio", "mix.wav"), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", os.path.join(out, name)], check=True)
    for p in parts + [lst]:
        os.remove(p)
    print("->", os.path.join(out, name))


if __name__ == "__main__":
    main()
