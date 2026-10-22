"""Détoure la photo CDC d'Anopheles gambiae (fond bleu uni) -> assets/src/zezette_cut.png"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "assets", "src")

im = Image.open(os.path.join(SRC, "anopheles_gambiae.jpg")).convert("RGB")
a = np.asarray(im).astype(np.int32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
H, W = r.shape
bdiff = b - np.maximum(r, g)
alpha_col = np.clip((125 - bdiff) / 55.0, 0, 1)  # fond bleu (écart ~150-190) -> 0, corps et ailes -> 1
# bord de la peau, colonne par colonne : on remonte depuis le bas tant que c'est de la peau
skin = (r > b + 25) & (r > 110)
top = np.full(W, H)
for x in range(W):
    y = H - 1
    miss = 0
    while y > 0 and miss < 6:
        miss = 0 if skin[y, x] else miss + 1
        y -= 1
    top[x] = y - 2
# lissage (médiane glissante) pour ignorer les pattes posées sur la peau
k = 31
pad = np.pad(top, k // 2, mode="edge")
top = np.array([np.median(pad[i:i + k]) for i in range(W)]) - 3
yy = np.arange(H)[:, None]
keep = alpha_col * (yy < top[None, :])
m = Image.fromarray((keep * 255).astype(np.uint8), "L")
m = m.filter(ImageFilter.MedianFilter(3))
# désaturer légèrement le liseré bleu
arr = a.astype(np.float32)
fringe = np.asarray(m.filter(ImageFilter.MinFilter(5)), np.float32) < 128
arr[..., 2] = np.where(fringe, np.minimum(arr[..., 2], (arr[..., 0] + arr[..., 1]) / 2 + 10), arr[..., 2])
out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
out.putalpha(m)
bb = out.getbbox()
out = out.crop(bb)
out.save(os.path.join(SRC, "zezette_cut.png"))
print("zezette_cut.png", out.size)
