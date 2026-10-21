"""Moteur « Vox motion » : collage papier en 1080x1920, anticrénelé (Pillow + numpy -> ffmpeg).

Tout ce qui est statique (découpages, papier, textes) est préparé une fois puis mis en cache ;
chaque image ne fait que placer, tourner et composer ces calques.
"""
import functools, math, os, subprocess
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")

# ---------- palette (fixes + thème Lune) ----------
HEX = dict(
    white="#ffffff", ink="#1b1b1f", night="#121a2e", night2="#1f2b4a", night3="#33456e",
    yellow="#ffe14d", red="#e8402f",
    pip="#5fd4c4", pip_d="#2f9c99", pip_p="#ff6f91",
    paper="#efe8dc", paper_d="#ddd2bf", grey="#8f8a82", grey_l="#c9c3b8",
    ocean="#2f7f8f", ocean_l="#8fc3c8", sand="#d9b98a", sand_d="#b8935f",
    coral="#ff7a6b", coral_l="#ffb3a1", lion="#c98a3c", lion_d="#8a5a22",
    moon="#d8d4cc", sun="#ffb23f", savanna="#3a2f2a",
)
C = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in HEX.items()}


def rgba(name, a=255):
    return C[name] + (a,)


# ---------- temps ----------
def clamp(v, a, b):
    return max(a, min(b, v))


def prog(t, a, b):
    return clamp((t - a) / max(1e-6, b - a), 0.0, 1.0)


def ease_out(p):
    p = clamp(p, 0, 1); return 1 - (1 - p) ** 3


def ease_io(p):
    p = clamp(p, 0, 1); return p * p * (3 - 2 * p)


def back_out(p, s=1.7):
    p = clamp(p, 0, 1) - 1; return 1 + p * p * ((s + 1) * p + s)


def step_t(t, fps=12):
    """Temps « stop motion » : les tremblements de papier vivent à 12 images/s."""
    return int(t * fps) / fps


def boil(t, seed, amp=0.6):
    """Petit tremblement d'angle façon animation papier (degrés)."""
    k = int(t * 8)
    return amp * math.sin(k * 2.3 + seed * 1.7)


# ---------- polices ----------
FONTS = dict(
    bold=os.path.join(ASSETS, "WorkSans-Bold.ttf"),
    reg=os.path.join(ASSETS, "WorkSans-Regular.ttf"),
    mono=os.path.join(ASSETS, "DMMono-Regular.ttf"),
    serif=os.path.join(ASSETS, "LibreBaskerville-Regular.ttf"),
    hand=os.path.join(ASSETS, "NothingYouCouldDo-Regular.ttf"),
)


@functools.lru_cache(maxsize=None)
def font(kind, size):
    return ImageFont.truetype(FONTS[kind], size)


def text_size(s, kind, size):
    f = font(kind, size)
    l, t, r, b = f.getbbox(s)
    return r - l, b - t


# ---------- calques ----------
def layer(w=W, h=H):
    return Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))


def supersample(w, h, draw_fn, ss=3):
    """Dessine à ss× puis réduit : formes nettes et lisses."""
    im = Image.new("RGBA", (int(w * ss), int(h * ss)), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(im), ss)
    return im.resize((int(w), int(h)), Image.LANCZOS)


class Sprite:
    """Découpage papier : image RGBA + bord blanc + ombre portée (pré-calculés)."""

    def __init__(self, im, border=10, shadow=True, name=""):
        if border:
            a = im.split()[3]
            pad = border + 4
            big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
            big.paste(im, (pad, pad))
            a = big.split()[3].point(lambda v: 255 if v > 40 else 0)
            # bord blanc un peu irrégulier, comme un découpage aux ciseaux
            edge = a.filter(ImageFilter.MaxFilter(2 * (border // 2) + 1))
            edge = edge.filter(ImageFilter.MaxFilter(2 * (border - border // 2) + 1))
            edge = edge.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 110 else 0)
            edge = edge.filter(ImageFilter.GaussianBlur(0.7))
            base = Image.new("RGBA", big.size, (250, 248, 243, 0))
            base.putalpha(edge)
            im = Image.alpha_composite(base, big)
        self.im = im
        self.name = name
        self.shadow = None
        if shadow:
            a = im.split()[3].filter(ImageFilter.GaussianBlur(9))
            sh = Image.new("RGBA", im.size, (20, 16, 30, 0))
            sh.putalpha(a.point(lambda v: int(v * 0.38)))
            self.shadow = sh
        self._cache = {}

    @property
    def size(self):
        return self.im.size

    def get(self, scale, rot):
        key = (round(scale, 3), round(rot * 5) / 5)
        if key in self._cache:
            return self._cache[key]
        def tf(im):
            if key[0] != 1:
                im = im.resize((max(1, int(im.width * key[0])), max(1, int(im.height * key[0]))),
                               Image.BICUBIC)
            if key[1]:
                im = im.rotate(key[1], resample=Image.BICUBIC, expand=True)
            return im
        out = (tf(self.im), tf(self.shadow) if self.shadow is not None else None)
        if len(self._cache) > 400:
            self._cache.clear()
        self._cache[key] = out
        return out


def put(base, spr, cx, cy, scale=1.0, rot=0.0, alpha=1.0, shadow=(10, 16)):
    """Place un Sprite centré en (cx, cy)."""
    if scale <= 0.01 or alpha <= 0.01:
        return
    im, sh = spr.get(scale, rot)
    x, y = int(round(cx - im.width / 2)), int(round(cy - im.height / 2))
    if alpha < 1:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
        if sh is not None:
            sh = sh.copy(); sh.putalpha(sh.split()[3].point(lambda v: int(v * alpha)))
    if sh is not None and shadow:
        base.alpha_composite(sh, *clip_dest(base, sh, x + int(shadow[0] * scale), y + int(shadow[1] * scale)))
    base.alpha_composite(im, *clip_dest(base, im, x, y))


def clip_dest(base, im, x, y):
    """Arguments (dest, source) d'alpha_composite avec découpe aux bords."""
    sx, sy = max(0, -x), max(0, -y)
    ex, ey = min(im.width, base.width - x), min(im.height, base.height - y)
    if ex <= sx or ey <= sy:
        return (0, 0), (0, 0, 0, 0)
    return (x + sx, y + sy), (sx, sy, ex, ey)


def paste(base, im, x, y):
    base.alpha_composite(im, *clip_dest(base, im, int(x), int(y)))


# ---------- papier, grain, vignette ----------
_rng = np.random.default_rng(11)


def _noise(w, h, cell, rng):
    small = rng.random((h // cell + 2, w // cell + 2)).astype(np.float32)
    im = Image.fromarray((small * 255).astype(np.uint8), "L").resize((w + 2 * cell, h + 2 * cell), Image.BICUBIC)
    return np.asarray(im, np.float32)[cell:cell + h, cell:cell + w] / 255.0


@functools.lru_cache(maxsize=None)
def paper(color="paper", strength=1.0):
    rng = np.random.default_rng(hash(color) % 1000)
    base = np.array(C[color], np.float32)
    n = (_noise(W, H, 260, rng) - 0.5) * 8 + (_noise(W, H, 30, rng) - 0.5) * 5
    fib = (rng.random((H, W)).astype(np.float32) - 0.5) * 6
    img = base[None, None, :] + (n + fib)[..., None] * strength
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")


_GRAIN = [(_rng.random((H // 2, W // 2)).astype(np.float32) - 0.5) for _ in range(4)]
_GRAIN = [np.repeat(np.repeat(g, 2, 0), 2, 1) for g in _GRAIN]
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_VIG = 1 - 0.12 * np.clip(((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H / 2) / (H * 0.62)) ** 2, 0, 1) ** 1.4


def finish(im, t):
    """Grain de film (12 i/s) + vignette légère -> octets RGB."""
    a = np.asarray(im.convert("RGB"), np.float32)
    g = _GRAIN[int(t * 12) % 4]
    a = a * _VIG[..., None] + g[..., None] * 16
    return np.clip(a, 0, 255).astype(np.uint8)


# ---------- texte ----------
def draw_text(base, s, cx, y, size, kind="bold", fill="ink", anchor="ma", stroke=0, stroke_fill="white",
              alpha=255):
    d = ImageDraw.Draw(base)
    col = C[fill] + (alpha,) if isinstance(fill, str) else fill
    sc = C[stroke_fill] + (alpha,) if isinstance(stroke_fill, str) else stroke_fill
    d.text((cx, y), s, font=font(kind, size), fill=col, anchor=anchor, stroke_width=stroke, stroke_fill=sc)


def highlight(base, x0, y0, x1, y1, p, color="yellow", seed=0, alpha=235):
    """Coup de surligneur de gauche à droite (p de 0 à 1), bords légèrement irréguliers."""
    if p <= 0:
        return
    xe = x0 + (x1 - x0) * ease_out(p)
    rng = np.random.default_rng(seed)
    j = rng.integers(-4, 5, 4)
    d = ImageDraw.Draw(base)
    d.polygon([(x0 - 6, y0 + j[0]), (xe + 4, y0 + j[1]), (xe + 8, y1 + j[2]), (x0 - 2, y1 + j[3])],
              fill=C[color] + (alpha,))


def text_block(lines, size, kind="bold", fill="ink", hl=(), hl_p=1.0, pad=(26, 14), paper_col="white",
               lead=1.18, align="center"):
    """Bande de papier avec texte ; hl = indices de mots surlignés (tous mots confondus)."""
    f = font(kind, size)
    asc, desc = f.getmetrics()
    lh = int(size * lead)
    ws = [f.getlength(l) for l in lines]
    bw, bh = int(max(ws) + 2 * pad[0]), int(lh * len(lines) + 2 * pad[1] - (lh - asc - desc) + 6)
    im = layer(bw, bh)
    d = ImageDraw.Draw(im)
    if paper_col:
        d.rectangle([0, 0, bw, bh], fill=C[paper_col] + (255,))
    k = 0
    for i, l in enumerate(lines):
        x = pad[0] + (0 if align == "left" else (max(ws) - ws[i]) / 2)
        y = pad[1] + i * lh
        for wd in l.split(" "):
            wl = f.getlength(wd)
            if k in hl:
                highlight(im, x, y + size * 0.12, x + wl, y + size * 1.02, hl_p, seed=k)
            k += 1
            x += wl + f.getlength(" ")
    for i, l in enumerate(lines):
        x = pad[0] + (0 if align == "left" else (max(ws) - ws[i]) / 2)
        d.text((x, pad[1] + i * lh), l, font=f, fill=C[fill] + (255,))
    return im


# ---------- traits au feutre ----------
def marker_path(base, pts, p, color="red", width=12, alpha=255):
    """Trace une polyligne jusqu'à la fraction p de sa longueur (feutre)."""
    if p <= 0 or len(pts) < 2:
        return
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(seg); goal = total * clamp(p, 0, 1)
    out, acc = [pts[0]], 0.0
    for (a, b), L in zip(zip(pts, pts[1:]), seg):
        if acc + L >= goal:
            r = (goal - acc) / max(L, 1e-6)
            out.append((a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r)); break
        out.append(b); acc += L
    d = ImageDraw.Draw(base)
    d.line(out, fill=C[color] + (alpha,), width=width, joint="curve")
    r = width / 2
    for q in (out[0], out[-1]):
        d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=C[color] + (alpha,))


def hand_ellipse(cx, cy, rx, ry, seed=0, turns=1.12, n=90):
    rng = np.random.default_rng(seed)
    ph, wob = rng.uniform(0, 6.28), rng.uniform(0.03, 0.06)
    pts = []
    for i in range(n + 1):
        a = ph + 2 * math.pi * turns * i / n
        k = 1 + wob * math.sin(3 * a + seed) + 0.04 * i / n
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


def arrow_pts(x0, y0, x1, y1, bend=0.15, n=24):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0) * bend, (x1 - x0) * bend
    pts = []
    for i in range(n + 1):
        u = i / n
        pts.append(((1 - u) ** 2 * x0 + 2 * u * (1 - u) * (mx + nx) + u * u * x1,
                    (1 - u) ** 2 * y0 + 2 * u * (1 - u) * (my + ny) + u * u * y1))
    return pts


def marker_arrow(base, x0, y0, x1, y1, p, color="red", width=12, bend=0.15):
    pts = arrow_pts(x0, y0, x1, y1, bend)
    marker_path(base, pts, prog(p, 0, 0.75), color, width)
    hp = prog(p, 0.75, 1)
    if hp > 0:
        (ax, ay), (bx, by) = pts[-3], pts[-1]
        a = math.atan2(by - ay, bx - ax)
        L = 34 * hp
        for s in (1, -1):
            marker_path(base, [(bx, by), (bx - L * math.cos(a + s * 0.5), by - L * math.sin(a + s * 0.5))], 1,
                        color, width)


def cross(base, cx, cy, r, p, color="red", width=16):
    marker_path(base, [(cx - r, cy - r), (cx + r, cy + r)], prog(p, 0, 0.5), color, width)
    marker_path(base, [(cx + r, cy - r), (cx - r, cy + r)], prog(p, 0.5, 1), color, width)


# ---------- trame (halftone) ----------
def halftone(w, h, intensity_fn, cell=16, color=(0, 0, 0, 255), ss=2):
    """Points de trame dont le rayon suit intensity_fn(x, y) dans [0, 1]."""
    def dr(d, s):
        for y in range(0, h + cell, cell):
            off = cell / 2 if (y // cell) % 2 else 0
            for x in range(0, w + cell, cell):
                xx = x + off
                v = intensity_fn(xx, y)
                if v > 0.02:
                    r = cell * 0.62 * math.sqrt(v)
                    d.ellipse([(xx - r) * s, (y - r) * s, (xx + r) * s, (y + r) * s], fill=color)
    return supersample(w, h, dr, ss)


# ---------- photos ----------
def photo_disc(path, size, crop_frac=0.96, tint=None):
    """Découpe une planète centrée sur fond noir en disque RGBA."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im.convert("L"), np.float32)
    ys, xs = np.nonzero(a > 28)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    r = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 * crop_frac
    im = im.crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r))).resize((size, size), Image.LANCZOS)
    if tint:
        im = Image.blend(im, Image.new("RGB", im.size, tint), 0.12)
    m = supersample(size, size, lambda d, s: d.ellipse([1 * s, 1 * s, (size - 1) * s, (size - 1) * s],
                                                        fill=(255, 255, 255, 255)))
    out = im.convert("RGBA"); out.putalpha(m.split()[3])
    return out


# ---------- transitions ----------
@functools.lru_cache(maxsize=None)
def _torn_edge():
    rng = np.random.default_rng(5)
    y = np.arange(H)
    e = np.zeros(H, np.float32)
    for k, a in ((3, 22), (11, 9), (37, 4), (97, 2)):
        e += a * np.sin(y / H * 2 * np.pi * k + rng.uniform(0, 6))
    return e


def torn_wipe(a, b, p):
    """Bande de papier déchiré qui balaie de droite à gauche : p=0 -> a, p=1 -> b."""
    if p <= 0: return a
    if p >= 1: return b
    e = _torn_edge()
    x = W * (1 - ease_io(p)) * 1.12 - 40
    edge = (x + e).astype(np.int32)
    xs = np.arange(W)[None, :]
    mb = xs >= edge[:, None]
    mw = (xs >= edge[:, None] - 14) & ~mb
    msh = (xs >= edge[:, None] - 44) & (xs < edge[:, None] - 14)
    A = np.asarray(a.convert("RGB")).copy()
    B = np.asarray(b.convert("RGB"))
    A[msh] = (A[msh] * 0.72).astype(np.uint8)
    A[mb] = B[mb]
    A[mw] = (250, 248, 243)
    return Image.fromarray(A, "RGB").convert("RGBA")


def camera(im, t, zoom=1.0, dx=0.0, dy=0.0):
    """Zoom lent façon banc-titre : recadre puis remet à la taille."""
    if zoom == 1 and dx == 0 and dy == 0:
        return im
    w, h = W / zoom, H / zoom
    x0, y0 = (W - w) / 2 + dx, (H - h) / 2 + dy
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BILINEAR)


# ---------- sortie ----------
class Writer:
    def __init__(self, path, size=(W, H), audio=None):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{size[0]}x{size[1]}", "-r", str(FPS), "-i", "-"]
        if audio: cmd += ["-i", audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
        cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", path]
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    def write(self, rgb):
        self.p.stdin.write(rgb.tobytes())

    def close(self):
        self.p.stdin.close(); self.p.wait()
