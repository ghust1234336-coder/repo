"""Décors et objets découpés de l'épisode Lune (préparés une fois, mis en cache)."""
import functools, math
import numpy as np
from vox import *

SRC = os.path.join(ASSETS, "src")


@functools.lru_cache(maxsize=None)
def MOON():
    return Sprite(photo_disc(os.path.join(SRC, "moon_lro.jpg"), 560), border=12, name="moon")


@functools.lru_cache(maxsize=None)
def EARTH():
    return Sprite(photo_disc(os.path.join(SRC, "earth_apollo17.jpg"), 600), border=12, name="earth")


@functools.lru_cache(maxsize=None)
def night_bg(dark=0):
    """Ciel de nuit papier : dark=0 clair de lune, 1 noir d'encre."""
    bg = paper("night2" if not dark else "night", 0.8).copy()
    if not dark:
        glow = layer()
        d = ImageDraw.Draw(glow)
        for r, a in ((900, 18), (650, 22), (420, 26)):
            d.ellipse([700 - r, 650 - r, 700 + r, 650 + r], fill=C["night3"] + (a,))
        bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    else:
        bg.alpha_composite(Image.new("RGBA", (W, H), (5, 7, 14, 120)))
    return bg


@functools.lru_cache(maxsize=None)
def stars(seed=1, n=160, big=10):
    im = layer()
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y, r = rng.uniform(0, W), rng.uniform(0, 1500), rng.choice([1.2, 1.6, 2.2, 3.0], p=[.4, .3, .2, .1])
        a = int(rng.uniform(120, 255))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 235, a))
    for _ in range(big):
        x, y, s = rng.uniform(40, W - 40), rng.uniform(80, 1300), rng.uniform(10, 18)
        d.polygon([(x, y - s), (x + s * .22, y - s * .22), (x + s, y), (x + s * .22, y + s * .22), (x, y + s),
                   (x - s * .22, y + s * .22), (x - s, y), (x - s * .22, y - s * .22)], fill=(255, 246, 214, 240))
    return im


@functools.lru_cache(maxsize=None)
def town(lit=True):
    """Collines + village en silhouette (bas de l'écran)."""
    def dr(d, s):
        S = lambda pts: [(x * s, y * s) for x, y in pts]
        hill = C["night3"] if lit else (16, 22, 38)
        hill2 = (44, 62, 100) if lit else (10, 14, 26)
        d.polygon(S([(0, 1210)] + [(x, 1210 - 70 * math.sin(x / 300) - 30 * math.sin(x / 97)) for x in range(0, 1100, 20)]
                    + [(W, H), (0, H)]), fill=hill2)
        rng = np.random.default_rng(4)
        x = 470
        while x < 1060:
            w, h = rng.integers(70, 120), rng.integers(80, 170)
            base = 1300
            d.rectangle(S([(x, base - h), (x + w, base + 200)]), fill=hill)
            d.polygon(S([(x - 8, base - h), (x + w / 2, base - h - 50), (x + w + 8, base - h)]), fill=hill)
            for k in range(2):
                wx, wy = x + 16 + k * (w - 46), base - h + 30
                on = lit or (x + k) % 3 == 0
                d.rectangle(S([(wx, wy), (wx + 22, wy + 28)]), fill=(255, 214, 120) if on else (30, 38, 60))
            x += w + rng.integers(4, 22)
        d.polygon(S([(0, 1330)] + [(x, 1330 - 90 * math.exp(-((x - 260) / 260) ** 2)) for x in range(0, 1100, 20)]
                    + [(W, H), (0, H)]), fill=hill)
    return supersample(W, H, dr, 2)


@functools.lru_cache(maxsize=None)
def TELESCOPE():
    def dr(d, s):
        S = lambda *v: [x * s for x in v]
        for x0, x1 in ((90, 40), (90, 140), (90, 92)):
            d.line(S(x0, 150, x1, 260), fill=C["ink"], width=int(9 * s))
        tube = [(30, 170), (200, 40), (222, 70), (52, 200)]
        d.polygon([(x * s, y * s) for x, y in tube], fill=C["white"])
        d.polygon([(x * s, y * s) for x, y in [(160, 72), (200, 40), (222, 70), (182, 102)]], fill=C["red"])
        d.ellipse(S(78, 136, 104, 162), fill=C["ink"])
    return Sprite(supersample(240, 270, dr, 3), border=8, name="telescope")


@functools.lru_cache(maxsize=None)
def CLIPPING():
    """Coupure de journal : « Ciel parfait : les astronomes font la fête »."""
    w, h = 820, 640
    im = paper("paper", 0.6).crop((0, 0, w, h)).copy()
    d = ImageDraw.Draw(im)
    d.text((w / 2, 28), "LE PETIT ASTRONOME", font=font("serif", 46), fill=C["ink"], anchor="ma")
    d.line([(30, 92), (w - 30, 92)], fill=C["ink"], width=3)
    d.line([(30, 100), (w - 30, 100)], fill=C["ink"], width=1)
    d.text((40, 120), "Ciel parfait :", font=font("serif", 58), fill=C["ink"])
    d.text((40, 192), "les astronomes", font=font("serif", 58), fill=C["ink"])
    d.text((40, 264), "font la fête", font=font("serif", 58), fill=C["ink"])
    sky = night_bg(1).crop((100, 200, 100 + 380, 200 + 270)).copy()
    sky.alpha_composite(stars(9, 900, 6).crop((100, 200, 480, 470)))
    im.paste(sky.convert("RGB"), (40, 350))
    for i in range(9):
        y = 352 + i * 30
        d.rectangle([450, y, w - 40 - (60 if i == 8 else 0), y + 10], fill=C["grey_l"])
    return Sprite(im, border=0, name="clipping")


@functools.lru_cache(maxsize=None)
def PARTY_PERSON(hat="red"):
    def dr(d, s):
        S = lambda *v: [x * s for x in v]
        g = (70, 78, 96)
        d.rounded_rectangle(S(20, 110, 120, 260), radius=int(40 * s), fill=g)
        d.ellipse(S(38, 50, 102, 114), fill=g)
        d.polygon([(x * s, y * s) for x, y in [(44, 62), (96, 62), (70, 0)]], fill=C[hat])
        d.ellipse(S(62, -6, 78, 10), fill=C["yellow"])
        d.line(S(30, 140, 0, 70), fill=g, width=int(22 * s))
        d.line(S(110, 140, 140, 70), fill=g, width=int(22 * s))
    im = Image.new("RGBA", (150, 270), (0, 0, 0, 0))
    im.alpha_composite(supersample(150, 262, dr, 3), (0, 8))
    return Sprite(im, border=6, name="person")


@functools.lru_cache(maxsize=None)
def MONT():
    """Mont-Saint-Michel en silhouette découpée."""
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        stone, stone_d, roof = (176, 168, 156), (138, 128, 116), (64, 72, 92)
        d.polygon(P([(0, 520), (60, 430), (150, 380), (230, 330), (330, 320), (420, 360), (500, 440), (560, 520)]),
                  fill=stone_d)
        for x, y, w, h in ((90, 400, 90, 80), (170, 350, 110, 120), (300, 340, 120, 110), (400, 390, 80, 80)):
            d.rectangle(P([(x, y), (x + w, y + h)]), fill=stone)
            d.polygon(P([(x - 6, y), (x + w / 2, y - 30), (x + w + 6, y)]), fill=roof)
            for k in range(int(w // 30)):
                d.rectangle(P([(x + 10 + k * 30, y + 20), (x + 22 + k * 30, y + 40)]), fill=(90, 84, 78))
        d.rectangle(P([(200, 210), (360, 340)]), fill=stone)
        d.polygon(P([(190, 210), (280, 160), (370, 210)]), fill=roof)
        d.rectangle(P([(262, 100), (298, 170)]), fill=stone)
        d.polygon(P([(256, 100), (280, 0), (304, 100)]), fill=roof)
        d.line(P([(280, 0), (280, -20)]), fill=C["yellow"], width=int(5 * s))
        for k in range(4):
            d.rectangle(P([(214 + k * 38, 240), (230 + k * 38, 280)]), fill=(90, 84, 78))
    im = Image.new("RGBA", (560, 560), (0, 0, 0, 0))
    im.alpha_composite(supersample(560, 540, dr, 2), (0, 20))
    return Sprite(im, border=10, name="mont")


@functools.lru_cache(maxsize=None)
def RING():
    def dr(d, s):
        S = lambda *v: [x * s for x in v]
        d.ellipse(S(0, 0, 200, 90), fill=C["red"])
        for a in (20, 110, 200, 290):
            d.pieslice(S(0, 0, 200, 90), a, a + 40, fill=C["white"])
        d.ellipse(S(52, 24, 148, 66), fill=(0, 0, 0, 0))
    return Sprite(supersample(200, 90, dr, 3), border=6, name="ring")


def phase_icon(d, cx, cy, r, ph, s=1):
    """Phase de Lune : ph 0 = nouvelle, 0.5 = pleine."""
    lit, dark = (236, 232, 222), (60, 66, 84)
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=dark)
    k = math.cos(ph * 2 * math.pi)
    if ph < 0.5:
        d.pieslice([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], -90, 90, fill=lit)
        col = dark if k > 0 else lit
    else:
        d.pieslice([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], 90, 270, fill=lit)
        col = dark if k > 0 else lit
    rx = abs(k) * r
    d.ellipse([(cx - rx) * s, (cy - r) * s, (cx + rx) * s, (cy + r) * s], fill=col)


@functools.lru_cache(maxsize=None)
def CALENDAR():
    w, h = 820, 720
    im = Image.new("RGBA", (w, h), C["white"] + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 110], fill=C["red"])
    d.text((w / 2, 30), "CALENDRIER LUNAIRE", font=font("bold", 54), fill=C["white"], anchor="ma")
    ph = supersample(w, h - 120, lambda dd, s: [phase_icon(dd, 80 + (i % 7) * 110, 70 + (i // 7) * 140, 40,
                                                              i / 28, s) for i in range(28)], 2)
    im.alpha_composite(ph, (0, 130))
    for i in range(28):
        d.text((80 + (i % 7) * 110, 130 + 120 + (i // 7) * 140), str(i + 1), font=font("mono", 22),
               fill=C["grey"], anchor="ma")
    return Sprite(im, border=0, name="calendar")


def CAL_CELL(i):
    return 80 + (i % 7) * 110 - 410, 130 + 70 + (i // 7) * 140 - 360


@functools.lru_cache(maxsize=None)
def CORAL(seed=0, col="coral"):
    rng = np.random.default_rng(seed)
    def dr(d, s):
        def br(x, y, a, L, w, n):
            x2, y2 = x + L * math.cos(a), y - L * math.sin(a)
            d.line([(x * s, y * s), (x2 * s, y2 * s)], fill=C[col], width=int(w * s))
            d.ellipse([(x2 - w / 2) * s, (y2 - w / 2) * s, (x2 + w / 2) * s, (y2 + w / 2) * s], fill=C[col])
            if n:
                for da in (-0.45, 0.45):
                    br(x2, y2, a + da + rng.uniform(-.15, .15), L * 0.72, w * 0.78, n - 1)
        br(170, 330, math.pi / 2, 100, 38, 4)
        d.ellipse([110 * s, 300 * s, 230 * s, 350 * s], fill=C[col])
    return Sprite(supersample(340, 350, dr, 2), border=8, name=f"coral{seed}")


@functools.lru_cache(maxsize=None)
def underwater():
    bg = paper("ocean", 0.8).copy()
    rays = layer()
    d = ImageDraw.Draw(rays)
    for k, x in enumerate((180, 420, 640, 880)):
        d.polygon([(x - 40, 0), (x + 40, 0), (x + 180 - k * 30, 1500), (x - 20 - k * 30, 1500)],
                  fill=(255, 255, 255, 22))
    bg.alpha_composite(rays.filter(ImageFilter.GaussianBlur(20)))
    sand = supersample(W, 500, lambda d, s: d.polygon(
        [(x * s, (120 + 30 * math.sin(x / 140)) * s) for x in range(0, W + 20, 20)] + [(W * s, 500 * s), (0, 500 * s)],
        fill=C["sand"]), 2)
    bg.alpha_composite(sand, (0, 1180))
    return bg


@functools.lru_cache(maxsize=None)
def savanna():
    bg = paper("night2", 0.7).copy()
    hz = layer()
    ImageDraw.Draw(hz).ellipse([-300, 900, W + 300, 1600], fill=C["night3"] + (150,))
    bg.alpha_composite(hz.filter(ImageFilter.GaussianBlur(80)))
    bg.alpha_composite(stars(5, 240, 4))
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        g = (8, 10, 16)
        d.polygon(P([(0, 1250)] + [(x, 1250 - 20 * math.sin(x / 200)) for x in range(0, 1100, 20)] + [(W, H), (0, H)]),
                  fill=g)
        d.line(P([(170, 1250), (190, 980)]), fill=g, width=int(26 * s))
        d.ellipse(P([(20, 900), (380, 1010)]), fill=g)
        d.ellipse(P([(80, 860), (300, 950)]), fill=g)
    bg.alpha_composite(supersample(W, H, dr, 2))
    return bg


@functools.lru_cache(maxsize=None)
def LION():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        g = (20, 22, 30)
        d.ellipse(P([(60, 90), (330, 210)]), fill=g)
        for x in (90, 140, 260, 300):
            d.rectangle(P([(x, 180), (x + 26, 290)]), fill=g)
        d.line(P([(320, 130), (390, 80), (400, 50)]), fill=g, width=int(12 * s))
        d.ellipse(P([(385, 30), (415, 64)]), fill=g)
        rng = np.random.default_rng(2)
        pts = []
        for i in range(36):
            a = i / 36 * 2 * math.pi
            r = 92 + (16 if i % 2 else 0) + rng.uniform(-4, 4)
            pts.append((80 + r * math.cos(a), 100 + r * math.sin(a)))
        d.polygon(P(pts), fill=g)
        d.ellipse(P([(20, 60), (120, 160)]), fill=(26, 28, 38))
    im = supersample(430, 300, dr, 2)
    return Sprite(im, border=0, shadow=False, name="lion")


@functools.lru_cache(maxsize=None)
def GAZELLE():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        g = (24, 28, 40)
        d.ellipse(P([(40, 70), (200, 140)]), fill=g)
        for x in (60, 85, 160, 180):
            d.line(P([(x, 120), (x + 4, 230)]), fill=g, width=int(9 * s))
        d.line(P([(185, 95), (225, 25)]), fill=g, width=int(20 * s))
        d.ellipse(P([(205, 5), (255, 40)]), fill=g)
        d.line(P([(222, 10), (212, -30 + 30), (205, -10 + 20)]), fill=g, width=int(5 * s))
        d.line(P([(232, 10), (240, -20 + 20)]), fill=g, width=int(5 * s))
    return Sprite(supersample(270, 240, dr, 2), border=0, shadow=False, name="gazelle")


@functools.lru_cache(maxsize=None)
def TOUPIE():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        body = [(30, 120), (310, 120), (250, 250), (170, 380), (90, 250)]
        d.polygon(P(body), fill=C["yellow"])
        d.polygon(P([(30, 120), (310, 120), (290, 165), (50, 165)]), fill=C["red"])
        d.polygon(P([(70, 210), (270, 210), (250, 250), (90, 250)]), fill=C["pip"])
        d.polygon(P([(130, 310), (210, 310), (170, 380)]), fill=C["red"])
        d.ellipse(P([(30, 90), (310, 150)]), fill=(255, 236, 140))
        d.rectangle(P([(158, 10), (182, 110)]), fill=C["ink"])
        d.ellipse(P([(148, 0), (192, 30)]), fill=C["ink"])
    return Sprite(supersample(340, 390, dr, 3), border=10, name="toupie")


@functools.lru_cache(maxsize=None)
def PENGUIN():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.ellipse(P([(40, 60), (240, 380)]), fill=C["ink"])
        d.ellipse(P([(80, 130), (200, 370)]), fill=C["white"])
        d.ellipse(P([(70, 20), (210, 150)]), fill=C["ink"])
        d.polygon(P([(140, 90), (185, 106), (140, 118)]), fill=C["sun"])
        for x in (95, 160):
            d.ellipse(P([(x - 6, 360), (x + 34, 392)]), fill=C["sun"])
        # lunettes de soleil
        d.rounded_rectangle(P([(82, 60), (132, 92)]), radius=int(10 * s), fill=(30, 30, 40))
        d.rounded_rectangle(P([(142, 60), (192, 92)]), radius=int(10 * s), fill=(30, 30, 40))
        d.line(P([(130, 70), (144, 70)]), fill=(30, 30, 40), width=int(5 * s))
        d.line(P([(92, 66), (106, 66)]), fill=(120, 130, 160), width=int(4 * s))
        d.line(P([(40, 190), (0, 280)]), fill=C["ink"], width=int(26 * s))
    return Sprite(supersample(260, 400, dr, 3), border=10, name="penguin")


@functools.lru_cache(maxsize=None)
def BOTTLE():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.rounded_rectangle(P([(10, 40), (90, 200)]), radius=int(18 * s), fill=C["sun"])
        d.rectangle(P([(32, 0), (68, 44)]), fill=C["white"])
        d.text((50 * s, 100 * s), "SPF", font=font("bold", int(22 * s)), fill=C["white"], anchor="mm")
        d.text((50 * s, 130 * s), "50", font=font("bold", int(30 * s)), fill=C["white"], anchor="mm")
    return Sprite(supersample(100, 200, dr, 2), border=6, name="bottle")


@functools.lru_cache(maxsize=None)
def SUN(r=160):
    def dr(d, s):
        c = r + 60
        for i in range(16):
            a = i / 16 * 2 * math.pi
            d.polygon([((c + (r + 50) * math.cos(a)) * s, (c + (r + 50) * math.sin(a)) * s),
                       ((c + (r - 5) * math.cos(a + .14)) * s, (c + (r - 5) * math.sin(a + .14)) * s),
                       ((c + (r - 5) * math.cos(a - .14)) * s, (c + (r - 5) * math.sin(a - .14)) * s)], fill=C["sun"])
        d.ellipse([(c - r) * s, (c - r) * s, (c + r) * s, (c + r) * s], fill=C["yellow"])
        d.ellipse([(c - r * .78) * s, (c - r * .78) * s, (c + r * .78) * s, (c + r * .78) * s], fill=(255, 236, 120))
    return Sprite(supersample(2 * r + 120, 2 * r + 120, dr, 2), border=8, name="sun")


@functools.lru_cache(maxsize=None)
def ICE():
    def dr(d, s):
        d.polygon([(x * s, y * s) for x, y in [(0, 40), (80, 0), (520, 10), (600, 50), (560, 140), (40, 150)]],
                  fill=(236, 246, 255))
        d.polygon([(x * s, y * s) for x, y in [(40, 150), (560, 140), (600, 50), (590, 110), (500, 170), (60, 175)]],
                  fill=(170, 210, 236))
    return Sprite(supersample(600, 180, dr, 2), border=0, name="ice")


@functools.lru_cache(maxsize=None)
def BUTTON():
    def dr(d, s):
        d.rounded_rectangle([0, 0, 640 * s, 150 * s], radius=int(36 * s), fill=C["red"])
        d.text((370 * s, 75 * s), "S'ABONNER", font=font("bold", int(66 * s)), fill=C["white"], anchor="mm")
        # cloche
        bx, by = 80, 72
        d.pieslice([(bx - 34) * s, (by - 40) * s, (bx + 34) * s, (by + 30) * s], 180, 360, fill=C["white"])
        d.rectangle([(bx - 34) * s, (by - 6) * s, (bx + 34) * s, (by + 24) * s], fill=C["white"])
        d.rectangle([(bx - 44) * s, (by + 18) * s, (bx + 44) * s, (by + 28) * s], fill=C["white"])
        d.ellipse([(bx - 10) * s, (by + 26) * s, (bx + 10) * s, (by + 44) * s], fill=C["white"])
    return Sprite(supersample(640, 150, dr, 2), border=10, name="button")


@functools.lru_cache(maxsize=None)
def MAGNET():
    def dr(d, s):
        d.arc([10 * s, 10 * s, 150 * s, 150 * s], 0, 180, fill=C["red"], width=int(38 * s))
        d.rectangle([10 * s, 0, 48 * s, 82 * s], fill=C["red"])
        d.rectangle([112 * s, 0, 150 * s, 82 * s], fill=C["red"])
        d.rectangle([10 * s, 0, 48 * s, 28 * s], fill=C["grey_l"])
        d.rectangle([112 * s, 0, 150 * s, 28 * s], fill=C["grey_l"])
    im = supersample(160, 160, dr, 3).rotate(180)
    return Sprite(im, border=6, name="magnet")
