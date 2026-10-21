"""Épisode « La Lune disparaît ce soir. Il se passe quoi ? » — style Vox (collage papier).

python episode_lune.py --preview   (540x960, sans grain)
python episode_lune.py --final     (1080x1920, 30 i/s, avec audio/mix.wav)
"""
import math, os, sys
import numpy as np
from vox import *
from decors_lune import *
from pip_vox import pip
import timeline as TL
from timeline import W as Wd, S as Sd

PIP_ACTIONS = {
    1: ("utiliser_objet", "regarde la Lune au télescope"),
    2: ("reagir", "seuls ses yeux restent visibles dans le noir"),
    3: ("utiliser_objet", "attend la mer avec sa bouée"),
    4: ("se_deplacer", "fuit le lion dans la savane"),
    5: ("subir", "perd l'équilibre sur la Terre qui tangue"),
    6: ("agir_corps", "saute sur le plateau de la balance"),
    7: None,
    8: ("agir_corps", "saute sur le bouton S'ABONNER"),
}

PIP_BOX = {}
CAPTION_ZONE = (0, 1500, W, 200)
STEP_LABELS = ["NUIT 1", "+6 H", "1 MOIS", "+1 M ANS"]
STAMPS = {1: (["PREMIÈRE NUIT"], "T + 0"), 2: (["6 HEURES", "PLUS TARD"], "T + 6 H"),
          3: (["SAUF QU'À", "1 MOIS…"], "T + 30 JOURS"), 4: (["DES MILLIONS", "D'ANNÉES"], "T + 1 000 000 ANS")}
STAMP_END = {1: ("nuit",), 2: ("tard",), 3: ("mois",), 4: ("tard",)}
STAMP_START = {1: "première", 2: "six", 3: "sauf", 4: "des"}


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


def label(base, t, t0, s, x, y, size=34, kind="mono", fill="ink", bg="yellow", rot=0, anchor_left=False):
    if t < t0:
        return
    p = prog(t, t0, t0 + 0.25)
    im = text_block([s], size, kind=kind, fill=fill, paper_col=bg, pad=(16, 8))
    spr = Sprite(im, border=0, name="label")
    cx = x + im.width / 2 if anchor_left else x
    put(base, spr, cx, y, 0.6 + 0.4 * back_out(p), rot, shadow=(6, 8))


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


def dashed_circle(base, cx, cy, r, p, col="red", width=8, dash=18):
    n = int(2 * math.pi * r / dash)
    d = ImageDraw.Draw(base)
    for i in range(int(n * p)):
        if i % 2: continue
        a0, a1 = i / n * 360, (i + 1) / n * 360
        d.arc([cx - r, cy - r, cx + r, cy + r], a0 - 90, a1 - 90, fill=C[col] + (255,), width=width)


def dashed_line(base, x0, y0, x1, y1, col="ink", width=5, dash=20, alpha=255):
    L = math.dist((x0, y0), (x1, y1)); n = max(1, int(L / dash))
    d = ImageDraw.Draw(base)
    for i in range(0, n, 2):
        a, b = i / n, min(1, (i + 1) / n)
        d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)],
               fill=C[col] + (alpha,), width=width)


def cut(t, *starts):
    """Indice du plan courant (coupes franches calées sur les phrases)."""
    k = 0
    for i, s in enumerate(starts):
        if t >= s - 0.04:
            k = i + 1
    return k


def confetti(base, t, t0, n=40, seed=3, area=(80, 600, 1000, 1300)):
    if t < t0:
        return
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(base)
    cols = ["red", "yellow", "pip", "pip_p", "white"]
    dt = t - t0
    for i in range(n):
        x = rng.uniform(area[0], area[2]) + 30 * math.sin(dt * 3 + i)
        y = area[1] + rng.uniform(-200, 0) + dt * rng.uniform(250, 500)
        if y > area[3]: continue
        a = dt * 6 + i
        w, h = 18 * abs(math.cos(a)) + 3, 10
        d.rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=C[cols[i % 5]] + (255,))


# ---------- C3 / C4 : tampon d'étape et barre de progression ----------
def stage_overlay(base, t, si):
    step = si  # scènes 1..4 = étapes 1..4
    # tampon plein écran
    if si in STAMPS:
        t0 = Wd(si, STAMP_START[si]) - 0.05
        t1 = Wd(si, STAMP_END[si][0], end=True) + 0.25
        if t0 <= t <= t1 + 0.15:
            fade = 1 - prog(t, t1, t1 + 0.15)
            dark = Image.new("RGBA", (W, H), (8, 10, 20, int(170 * fade)))
            base.alpha_composite(dark)
            big, sub = STAMPS[si]
            size = 118 if len(big) == 1 else 112
            p = prog(t, t0, t0 + 0.22)
            lines = big
            im = text_block(lines, size, hl=tuple(range(8)), hl_p=prog(t, t0 + 0.1, t0 + 0.45))
            spr = Sprite(im, border=0, name="stamp")
            sh = int(round(4 * math.sin(step_t(t) * 40))) if t < t0 + 0.35 else 0
            put(base, spr, W / 2 + sh, 860, (1.35 - 0.35 * back_out(p)) * fade, -3, alpha=fade)
            if t > t0 + 0.2:
                n = int(len(sub) * prog(t, t0 + 0.2, t0 + 0.5))
                draw_text(base, sub[:n], W / 2, 860 + im.height / 2 + 60, 46, kind="mono", fill="white",
                          alpha=int(255 * fade))
    # barre de progression
    if 1 <= si <= 4:
        bar = layer(W, 220)
        d = ImageDraw.Draw(bar)
        d.rectangle([40, 24, W - 40, 150], fill=(255, 255, 255, 245))
        x0, x1, y = 110, W - 110, 66
        xs = [x0 + (x1 - x0) * k / 3 for k in range(4)]
        t_in = TL.BOUNDS[si]
        cur = xs[step - 2] + (xs[step - 1] - xs[step - 2]) * ease_out(prog(t, t_in, t_in + 0.6)) if step > 1 else xs[0]
        d.line([(x0, y), (x1, y)], fill=C["grey_l"] + (255,), width=10)
        highlight(bar, x0 - 4, y - 9, cur, y + 9, 1.0, seed=1)
        for k, x in enumerate(xs):
            on = k < step
            d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=(C["red"] if on else C["grey_l"]) + (255,))
            d.text((x, y + 26), STEP_LABELS[k], font=font("mono", 32), fill=C["ink"] + (255 if on else 120,),
                   anchor="ma")
        paste(base, bar, 0, 20)


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
def s1(t, end=False):
    """Accroche : la Lune au-dessus du village, puis découpée et envolée."""
    base = night_bg(0).copy()
    base.alpha_composite(stars(1))
    t_dis = Wd(0, "disparaît")
    if end:  # scène 8 : boucle, la Lune revient
        t_dis = 1e9
    mx, my, ms = (800, 780, 0.45) if end else (720, 830, 0.55)
    moon_p = 1 if end else back_out(prog(t, 0.05, 0.35))
    gone = prog(t, t_dis + 0.25, t_dis + 0.7)
    if gone < 1:
        put(base, MOON(), mx + 260 * gone ** 2, my - 700 * gone ** 2, ms * moon_p * (1 - 0.4 * gone),
            boil(t, 1, 0.5) + 70 * gone)
    if t_dis - 0.15 < t < 1e8:
        p = prog(t, t_dis - 0.15, t_dis + 0.25)
        if gone < 1:
            dashed_circle(base, mx, my, 176, p)
        else:
            dashed_circle(base, mx, my, 176, 1, col="white", width=6)
            hand(base, t, t_dis + 0.7, "?", mx, my, 200, col="yellow", rot=0)
    base.alpha_composite(town(True))
    put(base, TELESCOPE(), 400, 1240, 1.0, 0)
    surprised = t > t_dis + 0.25
    if not (end and t > Wd(7, "abonne") - 0.6):  # en fin de vidéo, Pip part sauter sur le bouton
        PIP_BOX["box"] = pip(base, 230, 1310, t, pose="surprised" if surprised else "point",
                             mood="open" if surprised else "smile", look=(1, -1))
    if not end:
        if t < t_dis + 0.1:
            title(base, t, 0.12, ["La Lune", "disparaît."], 300, 104, hl=(1,))
        else:
            title(base, t, 0.12, ["La Lune"], 240, 104, hl=(1,))
            vanish_word(base, t, t_dis + 0.1, "disparaît.", 362, 104)
        title(base, t, Wd(0, "il") - 0.05, ["Il se passe quoi ?"], 530, 72, hl=(3, 4), rot=1.5)
    return base


def vanish_word(base, t, t0, word, y, size):
    """Mot-choc : les lettres de « disparaît » s'envolent une à une, dans le désordre."""
    f = font("bold", size)
    tw = f.getlength(word)
    lay = layer(int(tw + 80), int(size * 1.6))
    d = ImageDraw.Draw(lay)
    strip = 1 - prog(t, t0 + 0.55, t0 + 0.75)
    d.rectangle([0, 0, lay.width, lay.height - 10], fill=(255, 255, 255, int(255 * strip)))
    order = np.random.default_rng(4).permutation(len(word))
    for i, ch in enumerate(word):
        u = prog(t, t0 + order[i] * 0.05, t0 + order[i] * 0.05 + 0.2)
        if u >= 1: continue
        x = 40 + f.getlength(word[:i])
        d.text((x, 12 - 60 * u), ch, font=f, fill=C["ink"] + (int(255 * (1 - u)),))
    lay = lay.rotate(-1.5, resample=Image.BICUBIC, expand=True)
    paste(base, lay, W / 2 - lay.width / 2, y - lay.height / 2)


def s2(t):
    k = cut(t, Sd(1, 1))
    if k == 0:
        t_noir = Wd(1, "noir")
        dark = t >= t_noir
        base = night_bg(1 if dark else 0).copy()
        base.alpha_composite(stars(1))
        if dark:
            st = stars(2, 700, 24).copy()
            st.putalpha(st.split()[3].point(lambda v: int(v * prog(t, t_noir, t_noir + 0.5))))
            base.alpha_composite(st)
        base.alpha_composite(town(not dark))
        if not dark:
            PIP_BOX["box"] = pip(base, 260, 1310, t, pose="idle", look=(1, -1))
        else:  # gag : on ne voit plus que ses yeux
            tq = step_t(t)
            blink = (tq % 1.4) < 0.1
            d = ImageDraw.Draw(base)
            for ex in (238, 282):
                if blink:
                    d.line([ex - 14, 1218, ex + 14, 1218], fill=(255, 255, 255, 255), width=5)
                else:
                    d.ellipse([ex - 16, 1199, ex + 16, 1237], fill=(255, 255, 255, 255))
                    d.ellipse([ex - 8, 1212, ex + 10, 1232], fill=C["ink"] + (255,))
            PIP_BOX["box"] = (200, 1180, 120, 80)
            hand(base, t, t_noir + 0.2, "!", 330, 1100, 170, col="yellow", rot=0)
        title(base, t, t_noir - 0.05, ["Noir d'encre"], 360, 96, hl=(1,))
        label(base, t, Wd(1, "d'encre"), "LUMIÈRE LA NUIT : ÷ 100", W / 2, 520, 36)
        return base
    base = paper("paper").copy()
    t1 = Sd(1, 1)
    p = prog(t, t1, t1 + 0.3)
    put(base, CLIPPING(), W / 2, 720 + 500 * (1 - ease_out(p)), 1.0, -4 + boil(t, 2, 0.4))
    t_f = Wd(1, "fête")
    for i, (x, hat) in enumerate(((250, "red"), (540, "pip"), (830, "yellow"))):
        jump = 60 * abs(math.sin((t - t_f) * 9 + i)) if t > t_f - 0.2 else 0
        put(base, PARTY_PERSON(hat), x, 1260 - jump, 1.0, boil(t, i, 2))
    confetti(base, t, t_f - 0.1, 60, area=(60, 300, 1020, 1480))
    hand(base, t, Wd(1, "astronomes"), "enfin un ciel noir !", 540, 330, 76, rot=-3)
    return base


def tide_chart(base, t, t0, t_rate):
    d = ImageDraw.Draw(base)
    x0, x1, y0 = 120, 980, 900
    d.line([(x0, 560), (x0, 1240)], fill=C["ink"] + (255,), width=4)
    d.line([(x0, y0), (x1, y0)], fill=C["grey"] + (255,), width=3)
    for k, lab in enumerate(["0 h", "6 h", "12 h", "18 h"]):
        x = x0 + (x1 - x0) * k / 3
        d.text((x, 1260), lab, font=font("mono", 34), fill=C["ink"] + (255,), anchor="ma")
    draw_text(base, "NIVEAU DE LA MER", x0, 470, 40, kind="mono", anchor="la")
    A = 260
    def y_at(x, small):
        u = (x - x0) / (x1 - x0) * 1.5 * 2 * math.pi
        return y0 - A * (0.35 if small else 1) * math.cos(u)
    xm = x0 + (x1 - x0) / 3  # la Lune disparaît à 6 h
    # prévision en pointillés
    pts = [(x, y_at(x, False)) for x in np.linspace(xm, x1, 60)]
    if t > t_rate - 0.3:
        for a, b in zip(pts[::2], pts[1::2]):
            d.line([a, b], fill=C["grey"] + (255,), width=5)
    pts = [(x, y_at(x, False)) for x in np.linspace(x0, xm, 60)]
    marker_path(base, pts, prog(t, t0, t0 + 1.0), "ink", 9)
    pts = [(x, y_at(x, False) * 0 + (y0 + (y_at(xm, False) - y0) * (1 - u) + (y_at(x, True) - y0) * u))
           for x, u in zip(np.linspace(xm, x1, 80), np.linspace(0, 1, 80) ** 0.4)]
    marker_path(base, pts, prog(t, t_rate - 0.3, t_rate + 0.5), "red", 10)


def bulge(base, cx, cy, r, k, toward=(0, -1)):
    """Bosse d'océan : ellipse étirée vers la Lune (k = 0..1)."""
    ry = r * (1.0 + 0.32 * k)
    im = supersample(int(2.6 * r), int(2.6 * r), lambda d, s: d.ellipse(
        [(1.3 * r - r * 1.02) * s, (1.3 * r - ry) * s, (1.3 * r + r * 1.02) * s, (1.3 * r + ry) * s],
        fill=C["ocean_l"] + (150,)), 1)
    paste(base, im, cx - 1.3 * r, cy - 1.3 * r)


def s3(t):
    k = cut(t, Sd(2, 1), Sd(2, 2), Sd(2, 3))
    if k == 0:
        base = paper("paper").copy()
        t0 = Wd(2, "six")
        tide_chart(base, t, t0, Wd(2, "rate"))
        tt_ = Wd(2, "tsunami")
        label(base, t, tt_ - 0.1, "TSUNAMI ?", 790, 600, 44, kind="bold", bg="white", rot=4)
        if t > tt_ + 0.2:
            cross(base, 790, 600, 60, prog(t, tt_ + 0.2, tt_ + 0.5))
        hand(base, t, Wd(2, "rate"), "marée ratée", 760, 1120, 76)
        return base
    if k in (1, 2):
        base = night_bg(1).copy()
        base.alpha_composite(stars(3, 120, 4))
        ex, ey, er = (540, 1080, 260) if k == 1 else (540, 820, 190)
        t_t = Wd(2, "tirait")
        kk = ease_out(prog(t, t_t, t_t + 0.6)) if k == 1 else 1 - ease_out(prog(t, Sd(2, 2), Sd(2, 2) + 0.8))
        bulge(base, ex, ey, er, kk)
        put(base, EARTH(), ex, ey, 2 * er / 624, boil(t, 4, 0.3))
        if k == 1:
            put(base, MOON(), 540, 470, 0.28, boil(t, 1, 0.5))
            if t > t_t:
                for dx in (-150, 0, 150):
                    marker_arrow(base, ex + dx * 0.8, ey - er - 40, 540 + dx * 0.3, 600, prog(t, t_t + 0.1, t_t + 0.6),
                                 width=10, bend=0.05)
            ta = Wd(2, "aimant")
            if t > ta - 0.15:
                put(base, MAGNET(), 860, 470, back_out(prog(t, ta - 0.15, ta + 0.15)) * 0.9, -20)
                hand(base, t, ta, "comme un aimant", 330, 640, 64, col="yellow")
        else:
            t2 = Sd(2, 2)
            if t < t2 + 0.3:
                put(base, MOON(), 540, 470, 0.28 * (1 - prog(t, t2, t2 + 0.3)), 0)
            dashed_circle(base, 540, 470, 82, 1, col="white", width=5)
            # barres : amplitude avec / sans Lune
            tb = Wd(2, "marées")
            for i, (x, h, lab, col) in enumerate(((330, 380, "AVEC LUNE", "ocean_l"), (750, 135, "SOLEIL SEUL", "yellow"))):
                hh = h * ease_out(prog(t, tb + i * 0.4, tb + i * 0.4 + 0.5))
                d = ImageDraw.Draw(base)
                d.rectangle([x - 90, 1440 - hh, x + 90, 1440], fill=C[col] + (255,))
                draw_text(base, lab, x, 1452 - 0, 30, kind="mono", fill="white")
            label(base, t, Wd(2, "trois"), "÷ 2 à 3", 750, 1180, 54, kind="bold", bg="red", fill="white", rot=-4)
        return base
    # k == 3 : Mont-Saint-Michel, la mer ne monte plus
    base = paper("paper").copy()
    t3 = Sd(2, 3)
    sea_rise = 0.25 * ease_io(prog(t, t3, t3 + 2.4))
    d = ImageDraw.Draw(base)
    d.rectangle([0, 1180, W, H], fill=C["sand"] + (255,))
    put(base, MONT(), 720, 960, 1.0, boil(t, 5, 0.2))
    y_hi = 1150
    sea_top = 1440 - (1440 - y_hi) * sea_rise
    d.polygon([(0, sea_top)] + [(x, sea_top + 10 * math.sin(x / 60 + t * 3)) for x in range(0, W + 40, 40)]
              + [(W, H), (0, H)], fill=C["ocean"] + (255,))
    dashed_line(base, 40, y_hi, W - 40, y_hi, "red", 6)
    draw_text(base, "MARÉE HAUTE D'AVANT", 60, y_hi - 52, 32, kind="mono", fill="red", anchor="la")
    PIP_BOX["box"] = pip(base, 200, 1330, t, pose="hold", look=(1, 0), mood="worried" if t > Wd(2, "jamais") else "smile")
    put(base, RING(), 200, 1270, 0.9, boil(t, 6, 1))
    ti = Wd(2, "île")
    if t > ti - 0.1:
        marker_path(base, hand_ellipse(720, 900, 330, 300, 3), prog(t, ti - 0.1, ti + 0.4), "red", 10)
    title(base, t, t3 + 0.1, ["Plus jamais une île ?"], 300, 78, hl=(3,))
    return base


def s4(t):
    k = cut(t, Sd(3, 1), Sd(3, 2), Sd(3, 3))
    if k == 0:
        base = paper("paper").copy()
        put(base, CALENDAR(), W / 2, 960 + 6 * math.sin(step_t(t) * 30) * (t > Wd(3, "dérègle")), 1.0, 2 + boil(t, 8, 0.4))
        td = Wd(3, "dérègle")
        for i in range(0, 28, 3):
            if t > td + i * 0.03:
                cx, cy = CAL_CELL(i)
                c2 = math.cos(math.radians(2)), math.sin(math.radians(2))
                x, y = W / 2 + cx * c2[0] + cy * c2[1], 960 - cx * c2[1] + cy * c2[0]
                cross(base, x, y, 34, prog(t, td + i * 0.03, td + i * 0.03 + 0.2), width=10)
        title(base, t, Wd(3, "nature") - 0.05, ["La nature se dérègle"], 420, 74, hl=(3,))
        return base
    base = underwater().copy()
    synced = k == 1
    if synced:
        tm = Sd(3, 1)
        glow = layer()
        ImageDraw.Draw(glow).ellipse([540 - 180, 500 - 180, 540 + 180, 500 + 180], fill=(255, 255, 230, 90))
        base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(40)))
        put(base, MOON(), 540, 500, 0.3, boil(t, 1, 0.5))
    elif k == 2:
        dashed_circle(base, 540, 500, 84, 1, col="white", width=5)
    if k in (1, 2):
        corals = [(190, 1300, 0, "coral"), (540, 1340, 1, "coral_l"), (880, 1290, 2, "coral")]
        for i, (x, y, sd, col) in enumerate(corals):
            put(base, CORAL(sd, col), x, y - 120, 0.9, boil(t, sd, 0.6))
        d = ImageDraw.Draw(base)
        rng = np.random.default_rng(1)
        tp = Wd(3, "pondent") if synced else Sd(3, 2)
        for i in range(120):
            ci = i % 3
            delay = 0 if synced else [0.0, 0.7, 1.3][ci]
            dt = t - tp - delay - rng.uniform(0, 0.15)
            if dt < 0: continue
            x = corals[ci][0] + rng.uniform(-110, 110) + 20 * math.sin(dt * 2 + i)
            y = corals[ci][1] - 260 - dt * rng.uniform(140, 260)
            r = rng.uniform(5, 10)
            d.ellipse([x - r, y - r, x + r, y + r], fill=C["coral_l"] + (255,))
        if synced:
            label(base, t, Wd(3, "pleine"), "1 FOIS PAR AN · APRÈS LA PLEINE LUNE", W / 2, 660, 32)
            title(base, t, Sd(3, 1) + 0.05, ["Ponte géante"], 300, 80, hl=(1,))
        else:
            title(base, t, Sd(3, 2) + 0.05, ["Rendez-vous raté"], 300, 80, hl=(1,))
            tr = Wd(3, "rendez")
            if t > tr:
                cross(base, 540, 500, 70, prog(t, tr, tr + 0.3))
        return base
    # k == 3 : savane de nuit, le lion chasse ; Pip fuit
    base = savanna().copy()
    tl = Sd(3, 3)
    p = prog(t, tl, TL.BOUNDS[4])
    for i, gx in enumerate((150, 330)):
        put(base, GAZELLE(), gx - 260 * p - i * 40, 1180 - 30 * abs(math.sin(t * 9 + i)), 0.9, 0, shadow=None)
    lx = 900 - 300 * ease_io(p)
    put(base, LION(), lx, 1150, 1.1, 0, shadow=None)
    d = ImageDraw.Draw(base)
    for ex in (lx - 160, lx - 120):
        d.ellipse([ex - 9, 1080 - 6, ex + 9, 1080 + 6], fill=C["yellow"] + (255,))
    PIP_BOX["box"] = pip(base, 640 - 520 * ease_io(prog(t, tl + 0.2, tl + 2.0)), 1440, t, pose="run", run=True,
                         flip=True, mood="open", scale=0.8)
    label(base, t, Wd(3, "chassent"), "PLUS D'ATTAQUES LES NUITS NOIRES", W / 2, 640, 34)
    title(base, t, Wd(3, "lions") - 0.05, ["Les lions adorent"], 330, 80, hl=(2,))
    return base


def s5(t):
    k = cut(t, Sd(4, 1), Sd(4, 2), Sd(4, 3))
    if k == 0:
        base = night_bg(1).copy()
        base.alpha_composite(stars(6, 200, 8))
        tg = Wd(4, "tanguer")
        a = 0
        if t > tg - 0.1:
            u = t - tg + 0.1
            a = 24 * math.sin(u * 4.2) * (0.6 + 0.4 * math.sin(u * 1.3))
        ex, ey = 540, 1060
        put(base, EARTH(), ex, ey, 0.82, a)
        ra = math.radians(23.4 + a)
        L = 380
        dashed_line(base, ex + L * math.sin(ra), ey + L * math.cos(ra), ex - L * math.sin(ra), ey - L * math.cos(ra),
                    "white", 6)
        # Pip debout sur la Terre, il suit le roulis
        r = 262
        ang = math.radians(a)
        px, py = ex - r * math.sin(ang), ey - r * math.cos(ang)
        PIP_BOX["box"] = pip(base, px, py, t, pose="wobble" if t > tg - 0.1 else "idle", rot=a, scale=0.7,
                             mood="open" if t > tg else "smile")
        draw_text(base, f"{23.4 + a:4.1f}°".replace(".", ","), 860, 1350, 54, kind="mono", fill="yellow")
        if t > Sd(4, 0) + 1.0:
            p = prog(t, tg - 0.05, tg + 0.3)
            if p > 0:
                lines = ["La Terre", "se met à TANGUER"]
                im = text_block(lines, 88, hl=(4,), hl_p=prog(t, tg, tg + 0.3))
                spr = Sprite(im, border=0, name="t")
                put(base, spr, W / 2, 360, 0.7 + 0.3 * back_out(p), -a * 0.5)
        return base
    if k == 1:
        base = paper("paper").copy()
        t1 = Sd(4, 1)
        wob = 4 * math.sin(t * 5)
        put(base, TOUPIE(), W / 2, 1080, 1.4, wob)
        tl_ = Wd(4, "lune")
        put(base, MOON(), W / 2 + 6 * math.sin(math.radians(wob)) * 0, 760, 0.3 * back_out(prog(t, tl_ - 0.1, tl_ + 0.2)),
            boil(t, 1, 0.5))
        tm = Wd(4, "main")
        if t > tm - 0.1:
            marker_arrow(base, 860, 600, 640, 720, prog(t, tm - 0.1, tm + 0.3), width=10)
            hand(base, t, tm, "la main", 860, 540, 70)
        label(base, t, Wd(4, "axe"), "AXE STABLE", W / 2, 1450, 40)
        return base
    if k == 2:
        base = paper("paper").copy()
        t2 = Sd(4, 2)
        x0, x1, y0 = 120, 980, 1000
        d = ImageDraw.Draw(base)
        d.line([(x0, 560), (x0, 1360)], fill=C["ink"] + (255,), width=4)
        d.line([(x0, 1360), (x1, 1360)], fill=C["ink"] + (255,), width=4)
        draw_text(base, "INCLINAISON DE L'AXE", x0, 470, 40, kind="mono", anchor="la")
        draw_text(base, "temps (millions d'années)", x1, 1380, 30, kind="mono", anchor="ra")
        rng = np.random.default_rng(3)
        xs = np.linspace(x0, x1, 120)
        with_m = [(x, y0 - 30 * math.sin((x - x0) / 40)) for x in xs]
        wild = np.cumsum(rng.normal(0, 26, len(xs))); wild -= wild[0]
        wild = np.clip(wild * 1.0 + 120 * np.sin((xs - x0) / 110), -380, 330)
        no_m = [(x, y0 - w) for x, w in zip(xs, wild)]
        marker_path(base, with_m, prog(t, t2 - 0.1, t2 + 0.6), "ink", 8)
        marker_path(base, no_m, prog(t, t2 + 0.3, t2 + 1.5), "red", 9)
        draw_text(base, "AVEC LUNE", x1, y0 + 50, 32, kind="mono", anchor="ra")
        if t > t2 + 0.8:
            draw_text(base, "SANS LUNE", x1, 600, 32, kind="mono", fill="red", anchor="ra")
        te = Wd(4, "extrêmes")
        if t > te - 0.1:
            i = int(np.argmin(wild[60:])) + 60
            marker_path(base, hand_ellipse(xs[i], y0 - wild[i], 90, 70, 5), prog(t, te - 0.1, te + 0.35), "red", 9)
            hand(base, t, te + 0.1, "saisons extrêmes", 470, 640, 66)
        return base
    # k == 3 : le pingouin et sa crème solaire
    base = paper("paper").copy()
    hot = Image.new("RGBA", (W, H), C["sun"] + (60,))
    base.alpha_composite(hot)
    t3 = Sd(4, 3)
    put(base, SUN(), 840, 520, 0.9 + 0.04 * math.sin(t * 6), t * 20)
    d = ImageDraw.Draw(base)
    d.rectangle([0, 1250, W, H], fill=C["ocean"] + (255,))
    put(base, ICE(), 500, 1270, 1.2, 0)
    tc = Wd(4, "crème")
    put(base, PENGUIN(), 480, 1020 - 20 * abs(math.sin(step_t(t) * 6)) * (t > tc), 1.0, boil(t, 9, 1.5))
    put(base, BOTTLE(), 680, 1000, 0.9 * back_out(prog(t, tc - 0.3, tc)), -30 + 10 * math.sin(t * 12) * (t > tc))
    if t > tc:
        rng = np.random.default_rng(int(t * 12))
        for _ in range(16):
            x, y = 620 - rng.uniform(0, 120), 900 + rng.uniform(-60, 60)
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 255, 255, 230))
    title(base, t, Wd(4, "pingouins") - 0.05, ["Même les pingouins…"], 300, 80, hl=(2,))
    return base


def s6(t):
    k = cut(t, Sd(5, 1))
    if k == 0:
        base = night_bg(1).copy()
        base.alpha_composite(stars(7, 160, 6))
        put(base, SUN(120), 180, 960, 1.0, t * 10)
        d = ImageDraw.Draw(base)
        d.ellipse([180 - 640, 960 - 520, 180 + 640, 960 + 520], outline=(255, 255, 255, 120), width=4)
        to = Wd(5, "orbite")
        a = math.radians(-40 + (t - Sd(5, 0)) * 12)
        ex, ey = 180 + 640 * math.cos(a), 960 + 520 * math.sin(a)
        if t > to:
            p = prog(t, to, to + 0.6)
            ex, ey = ex + 380 * p, ey - 360 * p
            marker_arrow(base, 180 + 640 * math.cos(a), 960 + 520 * math.sin(a), ex, ey, p, width=10, bend=0.0)
            hand(base, t, to + 0.2, "?", ex + 90, ey - 40, 150, col="red", rot=0)
        put(base, EARTH(), ex, ey, 0.32, 0)
        title(base, t, Sd(5, 0) + 0.05, ["La Terre", "quitte son orbite ?"], 330, 80, hl=(3,))
        return base
    base = paper("paper").copy()
    tn, tq, tl = Wd(5, "non"), Wd(5, "quatre"), Wd(5, "légère")
    n = int(81 * ease_io(prog(t, tq, tl)))
    lvl = n / 81
    ang = -14 * (1 - lvl)
    cx, cy, L = W / 2, 1050, 300
    d = ImageDraw.Draw(base)
    d.polygon([(cx - 70, 1450), (cx + 70, 1450), (cx + 12, cy), (cx - 12, cy)], fill=C["ink"] + (255,))
    ra = math.radians(ang)
    lx, ly = cx - L * math.cos(ra), cy + L * math.sin(ra)
    rx, ry = cx + L * math.cos(ra), cy - L * math.sin(ra)
    d.line([(lx, ly), (rx, ry)], fill=C["ink"] + (255,), width=14)
    for px, py in ((lx, ly), (rx, ry)):
        d.line([(px, py), (px - 110, py + 170)], fill=C["grey"] + (255,), width=4)
        d.line([(px, py), (px + 110, py + 170)], fill=C["grey"] + (255,), width=4)
        d.rectangle([px - 140, py + 170, px + 140, py + 186], fill=C["ink"] + (255,))
    put(base, EARTH(), lx, ly + 170 - 110, 0.36, 0)
    for i in range(n):
        col, row = i % 9, i // 9
        x, y = rx - 120 + col * 30, ry + 160 - row * 26
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=C["moon"] + (255,), outline=C["grey"] + (255,), width=2)
    draw_text(base, f"× {n}", W / 2, 800, 80, kind="bold", fill="red")
    # Pip saute sur le plateau des Lunes, pour aider
    tj = tq - 0.3
    jy = -140 * abs(math.sin((t - tj) * 4)) if t > tj else 0
    top = ry + 160 - (math.ceil(n / 9) if n else 0) * 26 - 8
    PIP_BOX["box"] = pip(base, rx, top + jy, t, pose="jump" if jy < -10 else "happy", scale=0.55)
    if t > tn - 0.05:
        p = prog(t, tn - 0.05, tn + 0.2)
        im = text_block(["NON !"], 170, fill="white", paper_col="red")
        put(base, Sprite(im, border=0), W / 2, 440, 1.4 - 0.4 * back_out(p), -6)
    label(base, t, tl, "81 FOIS PLUS LÉGÈRE", W / 2, 680, 44, kind="bold")
    return base


def s7(t):
    base = night_bg(1).copy()
    base.alpha_composite(stars(8, 160, 6))
    t0, tv, tc = Sd(6, 0), Wd(6, "va"), Wd(6, "centimètres")
    p = ease_io(prog(t, tv - 0.1, TL.BOUNDS[7]))
    put(base, EARTH(), 230, 960, 0.5, 0)
    mx = 760 + 140 * p
    put(base, MOON(), mx, 960, 0.2, boil(t, 1, 0.5))
    # ruban de mesure
    d = ImageDraw.Draw(base)
    d.rectangle([400, 1150, mx + 20, 1210], fill=C["yellow"] + (255,))
    for i, x in enumerate(range(410, int(mx) + 20, 30)):
        d.line([(x, 1150), (x, 1150 + (26 if i % 5 == 0 else 14))], fill=C["ink"] + (255,), width=3)
    title(base, t, t0 + 0.05, ["Le plus fou ?"], 330, 90, hl=(2,))
    label(base, t, tc, "+ 3,8 cm PAR AN", W / 2, 640, 60, kind="bold", bg="yellow")
    hand(base, t, tc + 0.3, "comme tes ongles qui poussent", W / 2, 1320, 60, col="white")
    return base


def s8(t):
    base = s1(t, end=True)
    tr, ta = Wd(7, "regarde"), Wd(7, "abonne")
    title(base, t, Sd(7, 0) + 0.05, ["Regarde-la bien."], 300, 96, hl=(1,))
    if t > ta - 0.6:
        p = prog(t, ta - 0.6, ta - 0.3)
        press = 0.92 if ta <= t < ta + 0.15 else 1.0
        put(base, BUTTON(), W / 2, 1080, back_out(p) * press, -2)
        title(base, t, ta + 0.1, ["Abonne-toi", "pour d'autres secrets !"], 600, 66, hl=(0, 4), rot=1.5)
    return base


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ZOOM = 0.035


def render_scene(i, t):
    if i == 7:
        im = s8(t)
    else:
        im = SCENES[i](t)
    a, b = TL.BOUNDS[i], TL.BOUNDS[i + 1]
    return camera(im, t, 1 + ZOOM * prog(t, a, b))


def overlay_pip_s8(im, t):
    """Pip saute sur le bouton S'ABONNER (au-dessus du zoom pour rester net)."""
    ta = Wd(7, "abonne")
    if t > ta - 0.6:
        u = prog(t, ta - 0.55, ta)
        x = 230 + (W / 2 - 230) * u
        y = 1310 - 420 * math.sin(math.pi * u) + (1080 - 80 - 1310) * u
        if t > ta:
            y = 1080 - 80 - 40 * abs(math.sin((t - ta) * 6)) * math.exp(-(t - ta) * 2)
        PIP_BOX["box"] = pip(im, x, y, t, pose="jump" if t < ta else "happy", scale=0.8)


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
    stage_overlay(im, t, i)
    captions(im, t)
    return im


def render(path, scale, audio=None, t0=0.0, t1=None, grain=True):
    t1 = TL.DURATION if t1 is None else t1
    size = (int(W * scale), int(H * scale))
    wr = Writer(path, size, audio)
    n0, n1 = int(t0 * FPS), int(t1 * FPS)
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
    name = "lune.mp4" if final else "lune_preview.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-i", os.path.join(ROOT, "audio", "mix.wav"), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", os.path.join(out, name)], check=True)
    for p in parts + [lst]:
        os.remove(p)
    print("->", os.path.join(out, name))


if __name__ == "__main__":
    main()
