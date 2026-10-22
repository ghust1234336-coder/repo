"""Pip en découpage papier (version Vox) avec son chapeau d'explorateur à moustiquaire."""
import functools, math
from vox import *

PW, PH = 250, 300          # taille du sprite (avant bord blanc)
BX, BY, RX, RY = 125, 190, 56, 62   # corps

ARMS = {  # (épaule -> main) en coordonnées relatives au centre du corps, côté droit puis gauche
    "idle": [(46, 10, 66, 52), (-46, 10, -66, 52)],
    "point": [(46, 0, 98, -50), (-46, 10, -66, 52)],
    "surprised": [(44, -4, 88, -46), (-44, -4, -88, -46)],
    "happy": [(44, -4, 84, -56), (-44, -4, -84, -56)],
    "jump": [(44, -6, 82, -60), (-44, -6, -82, -60)],
    "run": [(44, 4, 82, -18), (-44, 8, -76, 46)],
    "wobble": [(46, 0, 100, 10), (-46, 0, -100, -14)],
    "hold": [(46, 6, 84, 6), (-46, 10, -66, 52)],
}


@functools.lru_cache(maxsize=None)
def pip_sprite(pose="idle", blink=False, breath=0, look=(0, 0), mood="smile", hat=True, leg=0):
    def dr(d, s):
        S = lambda *v: [x * s for x in v]
        bx, by = BX, BY - (8 if pose == "jump" else 0)
        rx, ry = RX + breath, RY - breath
        ink, pip, pd, pp, wh = C["ink"], C["pip"], C["pip_d"], C["pip_p"], C["white"]
        # jambes / pieds
        for dx in (-22, 22):
            ox = dx + (leg * (1 if dx > 0 else -1) * 10)
            d.ellipse(S(bx + ox - 17, by + ry - 12, bx + ox + 17, by + ry + 12), fill=pd)
        # bras arrière
        arms = ARMS[pose]
        for ax0, ay0, ax1, ay1 in arms:
            d.line(S(bx + ax0, by + ay0, bx + ax1, by + ay1), fill=pd, width=int(16 * s))
            d.ellipse(S(bx + ax1 - 11, by + ay1 - 11, bx + ax1 + 11, by + ay1 + 11), fill=pip)
        # corps + ombre en croissant
        d.ellipse(S(bx - rx, by - ry, bx + rx, by + ry), fill=pip)
        d.chord(S(bx - rx, by - ry, bx + rx, by + ry), 300, 120, fill=pd)
        d.ellipse(S(bx - rx + 6, by - ry + 2, bx + rx - 12, by + ry - 10), fill=pip)
        d.ellipse(S(bx - 34, by - 46, bx - 20, by - 32), fill=(190, 245, 236, 255))
        # yeux
        ey = by - 12
        for ex in (bx - 22, bx + 22):
            if blink:
                d.line(S(ex - 14, ey, ex + 14, ey), fill=ink, width=int(5 * s))
            else:
                big = 4 if pose == "surprised" else 0
                d.ellipse(S(ex - 16 - big, ey - 19 - big, ex + 16 + big, ey + 19 + big), fill=wh)
                px, py = ex + look[0] * 6, ey + 2 + look[1] * 6
                d.ellipse(S(px - 9, py - 10, px + 9, py + 10), fill=ink)
                d.ellipse(S(px - 6, py - 7, px - 1, py - 2), fill=wh)
        # bouche
        my = by + 22
        if mood == "smile":
            d.arc(S(bx - 14, my - 12, bx + 14, my + 8), 20, 160, fill=ink, width=int(5 * s))
        elif mood == "open":
            d.ellipse(S(bx - 10, my - 6, bx + 10, my + 14), fill=ink)
            d.ellipse(S(bx - 6, my + 5, bx + 6, my + 13), fill=pp)
        elif mood == "worried":
            d.arc(S(bx - 13, my, bx + 13, my + 18), 200, 340, fill=ink, width=int(5 * s))
        for cx in (bx - 38, bx + 38):
            d.ellipse(S(cx - 9, my - 10, cx + 9, my - 2), fill=tuple((a + b) // 2 for a, b in zip(pp, pip)))
        if hat:
            # voile de moustiquaire relevé sur les côtés (trame claire, jamais devant les yeux)
            for side in (-1, 1):
                x0 = bx + side * 62
                for k in range(7):
                    yk = by - ry + 6 + k * 9
                    d.line(S(x0, yk, x0 + side * 10, yk + 6), fill=(236, 240, 232), width=int(2 * s))
                d.line(S(x0, by - ry + 2, x0 + side * 12, by - ry + 66), fill=(236, 240, 232), width=int(2 * s))
            kr, kd = C["kraft"], C["kraft_d"]
            d.ellipse(S(bx - 74, by - ry - 4, bx + 74, by - ry + 20), fill=kd)          # bord
            d.rounded_rectangle(S(bx - 44, by - ry - 44, bx + 44, by - ry + 10), radius=int(18 * s), fill=kr)
            d.rectangle(S(bx - 44, by - ry - 8, bx + 44, by - ry + 6), fill=C["ink"])   # ruban
            fx_, fy_ = bx + 36, by - ry - 2                                               # fleur
            for a in range(5):
                an = a / 5 * 2 * math.pi
                d.ellipse(S(fx_ + 9 * math.cos(an) - 8, fy_ + 9 * math.sin(an) - 8,
                            fx_ + 9 * math.cos(an) + 8, fy_ + 9 * math.sin(an) + 8), fill=C["flower"])
            d.ellipse(S(fx_ - 6, fy_ - 6, fx_ + 6, fy_ + 6), fill=C["yellow"])
        # antenne (passe par un trou du chapeau)
        top = by - ry - (40 if hat else 0)
        pts = [(bx + 4 * math.sin(i / 6) + i * 0.9, top - i * 2.2) for i in range(0, 22 if not hat else 14)]
        d.line([(x * s, y * s) for x, y in pts], fill=pd, width=int(6 * s))
        tx, ty = pts[-1]
        d.ellipse(S(tx - 12, ty - 12, tx + 12, ty + 12), fill=pp)
    im = supersample(PW, PH, dr, 3)
    spr = Sprite(im, border=8, name=f"pip-{pose}")
    return spr


def pip(base, fx, fy, t, pose="idle", scale=1.0, flip=False, rot=0.0, look=(0, 0), mood="smile",
        hat=True, run=False, alpha=1.0):
    """Place Pip, pieds en (fx, fy). Renvoie sa boîte (x, y, w, h)."""
    tq = step_t(t)
    blink = (tq % 3.3) < 0.1 and pose != "surprised"
    breath = int(tq * 2) % 2 * 2
    leg = (int(tq * 10) % 2) * 2 - 1 if run else 0
    spr = pip_sprite(pose, blink, breath, look, mood, hat, leg)
    if flip:
        spr = _flipped(spr)
    w, h = spr.size
    feet = BY + RY + 12 + (h - PH) / 2          # y des pieds dans le sprite
    cy = fy - (feet - h / 2) * scale
    put(base, spr, fx, cy, scale, rot + boil(t, 3, 0.8), alpha)
    return (int(fx - w * scale / 2), int(cy - h * scale / 2), int(w * scale), int(h * scale))


@functools.lru_cache(maxsize=None)
def _flipped(spr):
    return Sprite(spr.im.transpose(Image.FLIP_LEFT_RIGHT), border=0)
