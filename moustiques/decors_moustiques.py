"""Décors et objets découpés de l'épisode moustiques (préparés une fois, mis en cache)."""
import functools, math
import numpy as np
from vox import *

SRC = os.path.join(ASSETS, "src")
ZEZ_EYE = (172, 225)      # œil de la photo détourée (coordonnées dans zezette_cut.png)
ZEZ_BELLY = (330, 110)    # abdomen
ZEZ_TIP = (30, 268)       # bout de la trompe


def googly(d, cx, cy, r, look=(-0.4, 0.2), s=1):
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=C["white"], outline=C["ink"],
              width=int(2 * s))
    px, py = cx + look[0] * r * 0.45, cy + look[1] * r * 0.45
    q = r * 0.48
    d.ellipse([(px - q) * s, (py - q) * s, (px + q) * s, (py + q) * s], fill=C["ink"])
    d.ellipse([(px - q * 0.5) * s, (py - q * 0.6) * s, (px - q * 0.05) * s, (py - q * 0.15) * s], fill=C["white"])


@functools.lru_cache(maxsize=None)
def ZEZETTE(eyes=True):
    """La vraie femelle Anopheles (photo CDC détourée) avec deux yeux en papier collés dessus."""
    im = Image.open(os.path.join(SRC, "zezette_cut.png")).convert("RGBA")
    if eyes:
        ex, ey = ZEZ_EYE
        def dr(d, s):
            googly(d, ex - 14, ey - 6, 21, s=s)
            googly(d, ex + 20, ey - 14, 21, s=s)
        im.alpha_composite(supersample(im.width, im.height, dr, 3))
    return Sprite(im, border=10, name=f"zezette{eyes}")


@functools.lru_cache(maxsize=None)
def ZEZ_FLIP():
    return Sprite(ZEZETTE().im.transpose(Image.FLIP_LEFT_RIGHT), border=0, name="zezette_flip")


@functools.lru_cache(maxsize=None)
def BZZ(big=False):
    """Le mâle : illustration papier, antennes plumeuses très visibles."""
    w, h = 360, 260
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        body, dark = C["mosq"], C["mosq_d"]
        # ailes
        for k, (dx, dy) in enumerate(((10, -70), (40, -60))):
            d.ellipse(P([(170 + dx, 60 + dy + 40), (300 + dx, 110 + dy + 40)]), fill=C["wing"] + (170,),
                      outline=(160, 190, 220, 255), width=int(2 * s))
        # pattes
        for x0, x1, y1 in ((150, 90, 250), (175, 175, 255), (205, 280, 250), (160, 40, 200), (215, 340, 210)):
            d.line(P([(x0, 140), ((x0 + x1) / 2, 170), (x1, y1)]), fill=dark, width=int(4 * s))
        # abdomen + thorax
        d.ellipse(P([(180, 110), (340, 150)]), fill=body)
        for k in range(5):
            d.line(P([(205 + k * 26, 112), (205 + k * 26, 148)]), fill=dark, width=int(3 * s))
        d.ellipse(P([(130, 100), (200, 160)]), fill=dark)
        # tête, trompe (inoffensive : il boit du nectar)
        d.ellipse(P([(96, 108), (140, 150)]), fill=body)
        d.line(P([(100, 132), (40, 158)]), fill=dark, width=int(4 * s))
        # antennes plumeuses, tournées vers l'avant et le haut
        for ang in (0.35, 0.8):
            x0, y0, L = 104, 116, 100
            ux, uy = -math.cos(ang), -math.sin(ang)
            nx, ny = -uy, ux
            x1, y1 = x0 + L * ux, y0 + L * uy
            d.line(P([(x0, y0), (x1, y1)]), fill=dark, width=int(3 * s))
            for k in range(1, 13):
                u = k / 13
                cx, cy = x0 + L * ux * u, y0 + L * uy * u
                fl = 20 * (1 - u * 0.55)
                for side in (-1, 1):
                    ex, ey = cx + side * nx * fl - ux * fl * 0.35, cy + side * ny * fl - uy * fl * 0.35
                    d.line(P([(cx, cy), (ex, ey)]), fill=dark, width=max(1, int(1.6 * s)))
        googly(d, 112, 122, 13, look=(-0.6, 0), s=s)
    im = supersample(w, h, dr, 3)
    if big:
        im = im.resize((w * 2, h * 2), Image.LANCZOS)
    return Sprite(im, border=8, name=f"bzz{big}")


# ---------- chambre de nuit ----------
@functools.lru_cache(maxsize=None)
def room():
    bg = paper("night2", 0.8).copy()
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.rectangle(P([(0, 1180), (W, H)]), fill=(26, 34, 58))                       # sol
        # fenêtre étoilée
        d.rectangle(P([(90, 470), (430, 880)]), fill=(250, 248, 243))
        d.rectangle(P([(104, 484), (416, 866)]), fill=C["night"])
        d.line(P([(260, 484), (260, 866)]), fill=(250, 248, 243), width=int(10 * s))
        d.line(P([(104, 675), (416, 675)]), fill=(250, 248, 243), width=int(10 * s))
        rng = np.random.default_rng(3)
        for _ in range(26):
            x, y = rng.uniform(112, 408), rng.uniform(492, 858)
            r = rng.choice([2, 3, 4])
            d.ellipse(P([(x - r, y - r), (x + r, y + r)]), fill=(255, 246, 214))
        # lit
        d.rounded_rectangle(P([(380, 1050), (1060, 1260)]), radius=int(30 * s), fill=C["snow"])
        d.rectangle(P([(380, 1150), (1060, 1300)]), fill=(150, 168, 210))
        d.rounded_rectangle(P([(860, 980), (1060, 1080)]), radius=int(40 * s), fill=(250, 248, 243))
        d.rectangle(P([(1040, 900), (1072, 1360)]), fill=C["kraft_d"])
        d.rectangle(P([(380, 1290), (400, 1360)]), fill=C["kraft_d"])
        # table de nuit + lampe
        d.rectangle(P([(150, 1060), (330, 1300)]), fill=C["kraft_d"])
        d.rectangle(P([(150, 1060), (330, 1090)]), fill=C["kraft"])
        d.rectangle(P([(232, 960), (248, 1062)]), fill=C["ink"])
        d.polygon(P([(180, 960), (300, 960), (270, 880), (210, 880)]), fill=C["lamp"])
    glow = layer()
    gd = ImageDraw.Draw(glow)
    for r, a in ((420, 26), (280, 34), (160, 44)):
        gd.ellipse([240 - r, 940 - r, 240 + r, 940 + r], fill=C["lamp"] + (a,))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(50)))
    bg.alpha_composite(supersample(W, H, dr, 2))
    return bg


@functools.lru_cache(maxsize=None)
def WAND():
    def dr(d, s):
        d.line([(10 * s, 150 * s), (120 * s, 40 * s)], fill=C["ink"], width=int(12 * s))
        d.line([(100 * s, 60 * s), (120 * s, 40 * s)], fill=C["white"], width=int(12 * s))
        cx, cy, R, r = 132, 28, 26, 11
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = R if i % 2 == 0 else r
            pts.append(((cx + rr * math.cos(a)) * s, (cy + rr * math.sin(a)) * s))
        d.polygon(pts, fill=C["yellow"])
    return Sprite(supersample(170, 170, dr, 3), border=6, name="wand")


def star(d, cx, cy, R, col="yellow", alpha=255, r_frac=0.42):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = R if i % 2 == 0 else R * r_frac
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=C[col] + (alpha,))


@functools.lru_cache(maxsize=None)
def EARTH():
    return Sprite(photo_disc(os.path.join(SRC, "earth_apollo17.jpg"), 420), border=10, name="earth")


# ---------- podium ----------
@functools.lru_cache(maxsize=None)
def PODIUM():
    w, h = 900, 420
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        for x0, top, n in ((300, 0, "1"), (0, 120, "2"), (600, 190, "3")):
            d.rectangle(P([(x0, top), (x0 + 300, h)]), fill=(250, 248, 243))
            d.rectangle(P([(x0, top), (x0 + 300, top + 22)]), fill=C["red"])
            d.text(((x0 + 150) * s, (top + 70) * s), n, font=font("bold", int(110 * s)), fill=C["ink"], anchor="ma")
    return Sprite(supersample(w, h, dr, 2), border=8, name="podium")


@functools.lru_cache(maxsize=None)
def SHARK():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        g = (110, 128, 150)
        d.polygon(P([(10, 90), (80, 50), (200, 40), (260, 70), (200, 110), (60, 115)]), fill=g)
        d.polygon(P([(130, 45), (165, 0), (175, 45)]), fill=g)
        d.polygon(P([(240, 70), (290, 30), (280, 75), (295, 115)]), fill=g)
        d.polygon(P([(120, 105), (150, 140), (165, 105)]), fill=g)
        d.polygon(P([(10, 90), (70, 112), (90, 100), (40, 92)]), fill=(240, 240, 240))
        d.ellipse(P([(54, 66), (66, 78)]), fill=C["ink"])
    return Sprite(supersample(300, 150, dr, 3), border=8, name="shark")


@functools.lru_cache(maxsize=None)
def SNAKE():
    def dr(d, s):
        pts = [(20 + i * 8, 90 + 40 * math.sin(i / 4)) for i in range(30)]
        d.line([(x * s, y * s) for x, y in pts], fill=(98, 150, 70), width=int(26 * s), joint="curve")
        hx, hy = pts[-1]
        d.ellipse([(hx - 20) * s, (hy - 18) * s, (hx + 26) * s, (hy + 18) * s], fill=(98, 150, 70))
        d.ellipse([(hx + 4) * s, (hy - 10) * s, (hx + 14) * s, (hy) * s], fill=C["ink"])
        d.line([((hx + 26) * s, hy * s), ((hx + 44) * s, (hy + 4) * s)], fill=C["red"], width=int(4 * s))
    return Sprite(supersample(300, 160, dr, 3), border=8, name="snake")


@functools.lru_cache(maxsize=None)
def PERSON(col=(70, 78, 96), w=150, h=270):
    def dr(d, s):
        S = lambda *v: [x * s for x in v]
        d.rounded_rectangle(S(20, 110, 120, 260), radius=int(40 * s), fill=col)
        d.ellipse(S(38, 46, 102, 110), fill=col)
    return Sprite(supersample(w, h, dr, 3), border=6, name=f"person{col}")


# ---------- stades ----------
@functools.lru_cache(maxsize=None)
def STADIUM(full=False):
    w, h = 300, 210
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.ellipse(P([(0, 0), (w, h)]), fill=(150, 146, 140))
        d.ellipse(P([(36, 30), (w - 36, h - 30)]), fill=(200, 196, 188))
        d.rounded_rectangle(P([(80, 64), (w - 80, h - 64)]), radius=int(30 * s), fill=(94, 160, 98))
        d.line(P([(w / 2, 64), (w / 2, h - 64)]), fill=(240, 240, 240), width=int(3 * s))
        if full:
            rng = np.random.default_rng(1)
            for _ in range(420):
                a = rng.uniform(0, 2 * math.pi); k = rng.uniform(0.62, 0.97)
                x, y = w / 2 + k * w / 2 * math.cos(a), h / 2 + k * h / 2 * math.sin(a)
                c = [C["red"], C["yellow"], C["pip"], C["white"], (60, 70, 120)][int(rng.integers(0, 5))]
                d.ellipse(P([(x - 4, y - 4), (x + 4, y + 4)]), fill=c)
    return Sprite(supersample(w, h, dr, 2), border=8, name=f"stade{full}")


# ---------- mécanisme ----------
@functools.lru_cache(maxsize=None)
def ARM(col=(150, 146, 160), flip=False):
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.rounded_rectangle(P([(0, 40), (380, 140)]), radius=int(50 * s), fill=col)
        d.ellipse(P([(330, 20), (470, 160)]), fill=col)
        for k in range(4):
            d.rounded_rectangle(P([(440, 34 + k * 30), (520 - k * 8, 58 + k * 30)]), radius=int(12 * s), fill=col)
    im = supersample(530, 180, dr, 2)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return Sprite(im, border=8, name=f"arm{flip}")


@functools.lru_cache(maxsize=None)
def PLASMO_DISC(size=300):
    """Photo du frottis (CDC) découpée en disque, comme sous une loupe."""
    im = Image.open(os.path.join(SRC, "plasmodium.jpg")).convert("RGB")
    cx, cy, r = 300, 290, 150      # zone avec un parasite en croissant
    im = im.crop((cx - r, cy - r, cx + r, cy + r)).resize((size, size), Image.LANCZOS)
    m = supersample(size, size, lambda d, s: d.ellipse([s, s, (size - 1) * s, (size - 1) * s],
                                                        fill=(255, 255, 255, 255)))
    out = im.convert("RGBA"); out.putalpha(m.split()[3])
    def ring(d, s):
        d.ellipse([3 * s, 3 * s, (size - 3) * s, (size - 3) * s], outline=C["ink"], width=int(12 * s))
    out.alpha_composite(supersample(size, size, ring, 2))
    return Sprite(out, border=8, name="plasmo")


@functools.lru_cache(maxsize=None)
def PARASITE(cap=False):
    """Le parasite version cartoon : croissant vert avec deux yeux (et une casquette de chauffeur)."""
    w, h = 220, 170
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.ellipse(P([(20, 40), (200, 160)]), fill=C["parasite"])
        d.ellipse(P([(40, 20), (190, 120)]), fill=(0, 0, 0, 0))
        d.chord(P([(20, 40), (200, 160)]), 10, 170, fill=C["parasite"])
        googly(d, 88, 118, 15, look=(0.3, 0), s=s)
        googly(d, 128, 118, 15, look=(0.3, 0), s=s)
        if cap:
            d.chord(P([(70, 60), (160, 130)]), 180, 360, fill=C["ink"])
            d.rectangle(P([(140, 90), (185, 98)]), fill=C["ink"])
            d.rectangle(P([(96, 70), (132, 80)]), fill=C["yellow"])
    return Sprite(supersample(w, h, dr, 3), border=8, name=f"parasite{cap}")


# ---------- planche d'entomologiste (3 500 cases) ----------
BOARD_COLS, BOARD_ROWS = 50, 70
BOARD_W, BOARD_H = 900, 980
BOARD_RED_ROWS = 6          # 300 cases sur 3 500 : « quelques centaines »


@functools.lru_cache(maxsize=None)
def BOARD(state=0):
    """state 0 : toutes les cases en couleur ; 1 : seules les premières rangées restent en couleur."""
    def dr(d, s):
        d.rectangle([0, 0, BOARD_W * s, BOARD_H * s], fill=(250, 248, 243))
        cw, ch = (BOARD_W - 40) / BOARD_COLS, (BOARD_H - 40) / BOARD_ROWS
        rng = np.random.default_rng(2)
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                x, y = 20 + c * cw + cw / 2, 20 + r * ch + ch / 2
                on = state == 0 or r < BOARD_RED_ROWS
                col = (C["mosq"] if rng.random() < 0.6 else C["mosq_d"]) if on else C["grey_l"]
                if state == 1 and on:
                    col = C["red"]
                d.ellipse([(x - 4.5) * s, (y - 2.6) * s, (x + 4.5) * s, (y + 2.6) * s], fill=col)
                d.line([(x - 1) * s, (y - 1) * s, (x - 4) * s, (y - 5) * s], fill=col, width=max(1, int(s)))
                d.line([(x + 1) * s, (y - 1) * s, (x + 4) * s, (y - 5) * s], fill=col, width=max(1, int(s)))
    return Sprite(supersample(BOARD_W, BOARD_H, dr, 2), border=12, name=f"board{state}")


@functools.lru_cache(maxsize=None)
def PHOTO_CARD(name, w=420):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    h = int(w * im.height / im.width)
    im = im.resize((w, h), Image.LANCZOS).convert("RGBA")
    card = Image.new("RGBA", (w + 28, h + 70), (250, 248, 243, 255))
    card.alpha_composite(im, (14, 14))
    return Sprite(card, border=0, name=f"card{name}")


# ---------- journal ----------
@functools.lru_cache(maxsize=None)
def CLIPPING():
    w, h = 860, 620
    im = paper("paper", 0.6).crop((0, 0, w, h)).copy()
    d = ImageDraw.Draw(im)
    d.text((w / 2, 28), "LE PETIT NATURALISTE", font=font("serif", 46), fill=C["ink"], anchor="ma")
    d.line([(30, 92), (w - 30, 92)], fill=C["ink"], width=3)
    d.line([(30, 100), (w - 30, 100)], fill=C["ink"], width=1)
    d.text((40, 124), "Moustiques :", font=font("serif", 62), fill=C["ink"])
    d.text((40, 200), "faut-il tous", font=font("serif", 62), fill=C["ink"])
    d.text((40, 276), "les effacer ?", font=font("serif", 62), fill=C["ink"])
    card = Image.open(os.path.join(SRC, "aedes_aegypti.jpg")).convert("L").convert("RGB").resize((380, 255))
    im.paste(card, (40, 370))
    for i in range(7):
        y = 372 + i * 36
        d.rectangle([450, y, w - 40 - (80 if i == 6 else 0), y + 12], fill=C["grey_l"])
    return Sprite(im, border=0, name="clipping")


# ---------- écosystème ----------
@functools.lru_cache(maxsize=None)
def BIRD():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.ellipse(P([(30, 50), (190, 160)]), fill=(214, 108, 70))
        d.ellipse(P([(40, 60), (150, 150)]), fill=(240, 196, 150))
        d.ellipse(P([(130, 20), (210, 100)]), fill=(214, 108, 70))
        d.polygon(P([(205, 55), (250, 66), (205, 76)]), fill=C["sun"])
        d.ellipse(P([(176, 44), (192, 60)]), fill=C["ink"])
        d.polygon(P([(30, 100), (0, 70), (0, 130)]), fill=(150, 76, 50))
        d.polygon(P([(70, 70), (150, 80), (110, 130)]), fill=(150, 76, 50))
        for x in (95, 125):
            d.line(P([(x, 158), (x, 190)]), fill=C["sun"], width=int(5 * s))
    return Sprite(supersample(260, 200, dr, 3), border=8, name="bird")


@functools.lru_cache(maxsize=None)
def FISH():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.ellipse(P([(40, 20), (230, 130)]), fill=C["pond"])
        d.polygon(P([(50, 75), (0, 25), (0, 125)]), fill=C["pond"])
        d.ellipse(P([(180, 50), (200, 70)]), fill=C["white"])
        d.ellipse(P([(186, 56), (196, 66)]), fill=C["ink"])
        d.arc(P([(110, 30), (170, 120)]), 250, 110, fill=C["pond_l"], width=int(5 * s))
    return Sprite(supersample(240, 150, dr, 3), border=8, name="fish")


@functools.lru_cache(maxsize=None)
def DRAGONFLY():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        for y0 in (40, 90):
            d.ellipse(P([(60, y0 - 26), (150, y0 + 6)]), fill=C["wing"] + (200,))
            d.ellipse(P([(150, y0 - 26), (240, y0 + 6)]), fill=C["wing"] + (200,))
        d.line(P([(150, 30), (150, 230)]), fill=(60, 140, 160), width=int(12 * s))
        d.ellipse(P([(132, 6), (168, 44)]), fill=(60, 140, 160))
        googly(d, 142, 22, 9, look=(0, 0.3), s=s)
        googly(d, 160, 22, 9, look=(0, 0.3), s=s)
    return Sprite(supersample(300, 240, dr, 3), border=8, name="dragonfly")


@functools.lru_cache(maxsize=None)
def MENU():
    w, h = 640, 700
    im = Image.new("RGBA", (w, h), (250, 248, 243, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 120], fill=C["ink"])
    d.text((w / 2, 26), "MENU", font=font("serif", 70), fill=C["white"], anchor="ma")
    for i, item in enumerate(["moustiques", "moucherons", "mouches", "éphémères", "pucerons"]):
        y = 170 + i * 100
        d.text((60, y), item, font=font("hand", 58), fill=C["ink"])
        d.line([(60, y + 76), (w - 60, y + 76)], fill=C["grey_l"], width=2)
    return Sprite(im, border=0, name="menu")


MENU_ROW_Y = [170 + i * 100 + 36 for i in range(5)]   # centre des lignes (dans le menu)


# ---------- Grand Nord ----------
@functools.lru_cache(maxsize=None)
def tundra():
    bg = paper("snow", 0.6).copy()
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.polygon(P([(0, 900), (180, 760), (330, 840), (520, 700), (720, 830), (900, 740), (W, 820), (W, 1000), (0, 1000)]),
                  fill=(176, 190, 204))
        d.polygon(P([(520, 700), (580, 745), (470, 742)]), fill=(250, 252, 255))
        d.polygon(P([(180, 760), (232, 800), (130, 800)]), fill=(250, 252, 255))
        d.rectangle(P([(0, 960), (W, H)]), fill=C["tundra"])
        rng = np.random.default_rng(6)
        for _ in range(60):
            x, y = rng.uniform(0, W), rng.uniform(980, 1500)
            rx, ry = rng.uniform(30, 110), rng.uniform(8, 22)
            d.ellipse(P([(x - rx, y - ry), (x + rx, y + ry)]),
                      fill=C["tundra_d"] if rng.random() < 0.6 else (122, 150, 92))
        for _ in range(14):
            x, y = rng.uniform(0, W), rng.uniform(1000, 1450)
            d.ellipse(P([(x - 60, y - 12), (x + 60, y + 12)]), fill=C["pond_l"])
        d.polygon(P([(0, 958)] + [(x, 958 - 10 * math.sin(x / 70)) for x in range(0, W + 20, 20)] + [(W, 975), (0, 975)]),
                  fill=C["tundra_d"])
    bg.alpha_composite(supersample(W, H, dr, 2))
    return bg


@functools.lru_cache(maxsize=None)
def meadow():
    bg = paper("paper", 0.6).copy()
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.rectangle(P([(0, 980), (W, H)]), fill=(140, 190, 110))
        rng = np.random.default_rng(8)
        for _ in range(40):
            x, y = rng.uniform(0, W), rng.uniform(1000, 1450)
            d.ellipse(P([(x - 8, y - 8), (x + 8, y + 8)]), fill=C["flower"] if rng.random() < .5 else C["yellow"])
    bg.alpha_composite(supersample(W, H, dr, 2))
    return bg


@functools.lru_cache(maxsize=None)
def CHICK():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.ellipse(P([(20, 60), (150, 160)]), fill=(196, 170, 120))
        for k in range(6):
            x = 40 + k * 18
            d.ellipse(P([(x, 80 + (k % 2) * 20), (x + 10, 90 + (k % 2) * 20)]), fill=(120, 96, 64))
        d.ellipse(P([(100, 20), (170, 90)]), fill=(196, 170, 120))
        d.polygon(P([(165, 50), (200, 58), (165, 66)]), fill=C["ink"])
        d.ellipse(P([(140, 40), (152, 52)]), fill=C["ink"])
        for x in (70, 100):
            d.line(P([(x, 158), (x - 4, 200)]), fill=(90, 80, 60), width=int(5 * s))
    return Sprite(supersample(210, 210, dr, 3), border=8, name="chick")


@functools.lru_cache(maxsize=None)
def SLED():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.rectangle(P([(20, 20), (300, 50)]), fill=C["red"])
        d.line(P([(10, 80), (300, 80), (330, 50)]), fill=C["ink"], width=int(8 * s))
        for x in (60, 250):
            d.line(P([(x, 50), (x, 80)]), fill=C["ink"], width=int(8 * s))
    return Sprite(supersample(340, 100, dr, 3), border=6, name="sled")


# ---------- labo ----------
@functools.lru_cache(maxsize=None)
def BOX():
    def dr(d, s):
        P = lambda pts: [(x * s, y * s) for x, y in pts]
        d.rectangle(P([(0, 80), (360, 300)]), fill=C["kraft"])
        d.polygon(P([(0, 80), (40, 10), (200, 10), (180, 80)]), fill=C["kraft_d"])
        d.polygon(P([(180, 80), (210, 10), (360, 10), (360, 80)]), fill=C["kraft_d"])
        d.ellipse(P([(130, 130), (230, 230)]), outline=C["red"], width=int(10 * s))
        d.text((180 * s, 182 * s), "M", font=font("bold", int(70 * s)), fill=C["red"], anchor="mm")
        d.text((180 * s, 270 * s), "MÂLES MODIFIÉS", font=font("mono", int(24 * s)), fill=C["ink"], anchor="mm")
    return Sprite(supersample(360, 300, dr, 3), border=10, name="box")


# ---------- fin ----------
@functools.lru_cache(maxsize=None)
def BUTTON():
    def dr(d, s):
        d.rounded_rectangle([0, 0, 640 * s, 150 * s], radius=int(36 * s), fill=C["red"])
        d.text((370 * s, 75 * s), "S'ABONNER", font=font("bold", int(66 * s)), fill=C["white"], anchor="mm")
        bx, by = 80, 72
        d.pieslice([(bx - 34) * s, (by - 40) * s, (bx + 34) * s, (by + 30) * s], 180, 360, fill=C["white"])
        d.rectangle([(bx - 34) * s, (by - 6) * s, (bx + 34) * s, (by + 24) * s], fill=C["white"])
        d.rectangle([(bx - 44) * s, (by + 18) * s, (bx + 44) * s, (by + 28) * s], fill=C["white"])
        d.ellipse([(bx - 10) * s, (by + 26) * s, (bx + 10) * s, (by + 44) * s], fill=C["white"])
    return Sprite(supersample(640, 150, dr, 2), border=10, name="button")


@functools.lru_cache(maxsize=None)
def LOUPE(r=190):
    def dr(d, s):
        c = r + 20
        d.ellipse([(c - r) * s, (c - r) * s, (c + r) * s, (c + r) * s], outline=C["ink"], width=int(22 * s))
        d.line([((c + r * 0.7) * s, (c + r * 0.7) * s), ((c + r * 1.25) * s, (c + r * 1.25) * s)], fill=C["ink"],
               width=int(40 * s))
    n = int(2 * r + 20 + r * 0.6)
    return Sprite(supersample(n, n, dr, 2), border=0, shadow=True, name=f"loupe{r}")
