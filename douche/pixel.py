"""Moteur pixel art HD : canevas 360x640 en indices de palette, agrandi x3 -> 1080x1920."""
import functools, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, SCALE, FPS = 360, 640, 3, 30
ROOT = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(ROOT, "assets", "PixelifySans.ttf")
T_ = 255  # transparent (sprites)

PALETTE_HEX = [
    # neutres / nuit / accents (fixes)
    "#ffffff", "#0a0a12", "#1b1838", "#2c2a5a", "#3d4f8f", "#ffd23f", "#e8333a",
    # Pip
    "#5fd4c4", "#2f9c99", "#ff6f91",
    # thème douche (14)
    "#bfe6f5", "#78b8db", "#3f8fd6", "#f5cba7", "#d99a6c", "#a8653f", "#6e4122",
    "#e6c34f", "#86d94f", "#3e9442", "#c7e04a", "#b56fe0", "#ff8fbf", "#8a8fa8",
]
(WHITE, BLACK, NIGHT, NIGHT2, NIGHT3, YELLOW, RED, PIP, PIP_D, PIP_P,
 TILE, TILE_D, WATER, SKIN, SKIN_M, SKIN_D, CRUST, SEBUM, BACT, BACT_D,
 STINK, MUSH, SOAP, GREY) = range(24)
PAL = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in PALETTE_HEX], np.uint8)

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
BAYER_FULL = np.tile(BAYER, (H // 4, W // 4))
YY, XX = np.mgrid[0:H, 0:W]


def canvas(col=NIGHT):
    return np.full((H, W), col, np.uint8)


def clamp(v, a, b):
    return max(a, min(b, v))


def ease_out(p):
    p = clamp(p, 0, 1); return 1 - (1 - p) ** 3


def ease_io(p):
    p = clamp(p, 0, 1); return p * p * (3 - 2 * p)


def prog(t, a, b):
    return clamp((t - a) / max(1e-6, b - a), 0.0, 1.0)


def pose_t(t, fps=12):
    """Temps quantifié à 12 images/s pour les poses."""
    return int(t * fps) / fps


# ---------- primitives ----------
def rect(c, x, y, w, h, col):
    x0, y0, x1, y1 = int(x), int(y), int(x + w), int(y + h)
    c[clamp(y0, 0, H):clamp(y1, 0, H), clamp(x0, 0, W):clamp(x1, 0, W)] = col


def mask_circle(cx, cy, r):
    return (XX - cx) ** 2 + (YY - cy) ** 2 <= r * r + r * 0.6


def mask_ellipse(cx, cy, rx, ry):
    rx, ry = max(rx, 0.5), max(ry, 0.5)
    return ((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2 <= 1.0


def fill(c, mask, col):
    c[mask] = col


def dither(c, mask, col, level):
    """level 0..16 : proportion de pixels col (Bayer 4x4)."""
    c[mask & (BAYER_FULL < level)] = col


def outline_shape(c, mask, fill_col, line_col=NIGHT):
    m = dilate(mask)
    c[m] = line_col
    c[mask] = fill_col


def dilate(m, n=1):
    for _ in range(n):
        d = m.copy()
        d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
        m = d
    return m


def circle(c, cx, cy, r, col, line=None):
    m = mask_circle(round(cx), round(cy), r)
    if line is None: c[m] = col
    else: outline_shape(c, m, col, line)


def ellipse(c, cx, cy, rx, ry, col, line=None):
    m = mask_ellipse(round(cx), round(cy), rx, ry)
    if line is None: c[m] = col
    else: outline_shape(c, m, col, line)


def line(c, x0, y0, x1, y1, col, w=1):
    x0, y0, x1, y1 = map(round, (x0, y0, x1, y1))
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        rect(c, x - w // 2, y - w // 2, w, w, col)


def vgrad(c, y0, y1, cols):
    """Bandes verticales de couleurs, raccordées par un tramage de Bayer."""
    n = len(cols) - 1
    for y in range(int(y0), int(y1)):
        f = (y - y0) / max(1, (y1 - y0)) * n
        i = min(int(f), n - 1); lvl = int((f - i) * 16)
        row = np.where(BAYER_FULL[y] < lvl, cols[i + 1], cols[i])
        c[y] = row


def vignette(c, cx, cy, r, col=BLACK):
    d = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2)
    c[d > r + 10] = col
    ring = (d > r) & (d <= r + 10)
    lvl = ((d - r) / 10 * 16).astype(int)
    c[ring & (BAYER_FULL < lvl)] = col


def stamp(c, m, x, y, col):
    """Pose un masque booléen local en (x, y), avec découpe aux bords."""
    h, w = m.shape
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0: return
    sub = m[y0 - y:y1 - y, x0 - x:x1 - x]
    c[y0:y1, x0:x1][sub] = col


def blit(c, spr, x, y, scale=1, flip=False):
    if flip: spr = spr[:, ::-1]
    if scale != 1: spr = np.repeat(np.repeat(spr, scale, 0), scale, 1)
    x, y = int(x), int(y)
    h, w = spr.shape
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(w, W - x), min(h, H - y)
    if sx1 <= sx0 or sy1 <= sy0: return
    sub = spr[sy0:sy1, sx0:sx1]
    dst = c[y + sy0:y + sy1, x + sx0:x + sx1]
    m = sub != T_
    dst[m] = sub[m]


# ---------- texte ----------
@functools.lru_cache(maxsize=None)
def font(size):
    return ImageFont.truetype(FONT, size)


@functools.lru_cache(maxsize=4096)
def glyph(ch, size):
    f = font(size)
    asc, desc = f.getmetrics()
    w = max(1, int(round(f.getlength(ch))))
    im = Image.new("1", (w + 4, asc + desc + 4), 0)
    d = ImageDraw.Draw(im); d.fontmode = "1"
    d.text((1, 1), ch, font=f, fill=1)
    return np.array(im, bool), w


@functools.lru_cache(maxsize=None)
def cedilla(size):
    """« Ç » redessiné : C + petite cédille détachée (celle de la police se lit comme un Q)."""
    m, adv = glyph("C", size)
    rows = np.nonzero(m.any(1))[0]; cols = np.nonzero(m.any(0))[0]
    b = rows[-1]; cx = (cols[0] + cols[-1]) // 2
    k = max(1, size // 14)
    out = np.zeros((m.shape[0] + 3 * k + 3, m.shape[1]), bool); out[:m.shape[0]] = m
    out[b + 2:b + 2 + 2 * k, cx:cx + k] = True
    out[b + 1 + 2 * k:b + 1 + 3 * k, cx - k:cx + k] = True
    return out, adv


def text_width(s, size, spacing=1):
    return sum(glyph(ch, size)[1] + spacing for ch in s) - spacing


def draw_text(c, segs, x, y, size, outline=NIGHT, shadow=True, center=True, shake=None,
              t=0.0, spacing=1, bounce=None):
    """segs : str ou liste de (texte, couleur[, effet]). effet : 'shake' / 'drip' / 'blink'."""
    if isinstance(segs, str): segs = [(segs, WHITE)]
    total = sum(text_width(s[0], size, spacing) + spacing for s in segs) - spacing
    cx = x - total // 2 if center else x
    tq = pose_t(t)
    rng = np.random.default_rng(int(tq * 12) + 17)
    k = 0
    for seg in segs:
        txt, col = seg[0], seg[1]
        fx = seg[2] if len(seg) > 2 else shake
        for ch in txt:
            m, adv = glyph(ch, size) if ch != "Ç" else cedilla(size)
            dx = dy = 0
            if fx == "shake": dx, dy = rng.integers(-1, 2, 2)
            if fx == "wave": dy = int(round(2 * np.sin(tq * 8 + k * 0.7)))
            if fx == "blink" and int(tq * 6) % 2: col_ = YELLOW
            else: col_ = col
            if bounce is not None: dy += bounce(k)
            gx, gy = cx + dx, int(y + dy)
            h, w = m.shape
            pm = np.zeros((h + 6, w + 6), bool); pm[2:2 + h, 2:2 + w] = m
            ol = dilate(pm)
            layers = []
            if shadow:
                sh = np.zeros_like(pm); sh[2:, 2:] = ol[:-2, :-2]; layers.append((sh, BLACK))
            if outline is not None: layers.append((ol, outline))
            layers.append((pm, col_))
            for lm, lc in layers:
                stamp(c, lm, gx - 2, gy - 2, lc)
            if True:
                if fx == "drip":
                    dy2 = int((tq * 20 + k * 3) % 14)
                    rect(c, gx + w // 2, gy + h - 2 + dy2, 2, 3, col)
            cx += adv + spacing; k += 1
    return total


def title_bounce(t, t0, dur=0.35, h=40):
    """Décalage vertical d'un titre qui tombe et rebondit (pixels entiers)."""
    p = (t - t0) / dur
    if p < 0: return None
    if p >= 1.4: return 0
    if p < 1: return int(-h * (1 - ease_out(p)) ** 2 * 1.0)
    return int(round(-3 * np.sin((p - 1) / 0.4 * np.pi)))


# ---------- sous-titres karaoké ----------
def caption_chunks(words, maxc=24):
    chunks, cur = [], []
    for w in words:
        txt = " ".join(x["w"] for x in cur + [w])
        if cur and (len(txt) > maxc):
            chunks.append(cur); cur = [w]
        else:
            cur.append(w)
        if w["w"].rstrip()[-1:] in ".?!" and cur:
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    return chunks


def draw_caption(c, chunks, t, y=572, size=16):
    cur = None
    for ch in chunks:
        if ch[0]["s"] - 0.05 <= t <= ch[-1]["e"] + 0.25:
            cur = ch
    if not cur: return
    segs = []
    for i, w in enumerate(cur):
        col = YELLOW if w["s"] - 0.03 <= t < (cur[i + 1]["s"] if i + 1 < len(cur) else w["e"] + 0.25) else WHITE
        segs.append((w["w"].upper() + (" " if i + 1 < len(cur) else ""), col))
    draw_text(c, segs, W // 2, y, size, outline=BLACK, shadow=False)


# ---------- transitions ----------
_PERM = np.random.default_rng(3).permutation((H // 8) * (W // 8)).reshape(H // 8, W // 8)


def mosaic_mix(a, b, p):
    """Volet mosaïque en blocs de 8 pixels : p=0 -> a, p=1 -> b."""
    thr = (_PERM < p * _PERM.size)
    m = np.repeat(np.repeat(thr, 8, 0), 8, 1)
    out = a.copy(); out[m] = b[m]
    return out


# ---------- sortie ----------
def to_rgb(c, scale=SCALE):
    rgb = PAL[c]
    if scale > 1:
        rgb = np.repeat(np.repeat(rgb, scale, 0), scale, 1)
    return rgb


class Writer:
    def __init__(self, path, scale, audio=None):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W * scale}x{H * scale}", "-r", str(FPS), "-i", "-"]
        if audio: cmd += ["-i", audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", path]
        self.scale = scale
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    def write(self, c):
        self.p.stdin.write(to_rgb(c, self.scale).tobytes())

    def close(self):
        self.p.stdin.close(); self.p.wait()
