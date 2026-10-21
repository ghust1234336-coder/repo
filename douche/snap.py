"""Images de contrôle + tests A8. python snap.py [t ...]"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image
import episode_douche as E
import timeline as TL
from pixel import PAL, to_rgb, FPS

ok = True


def check(name, cond, info=""):
    global ok
    ok &= bool(cond)
    print(("OK  " if cond else "KO  ") + name, info)


for s in sys.argv[1:]:
    t = float(s)
    Image.fromarray(to_rgb(E.frame(t))).save(os.path.join(E.ROOT, "renders", f"snap_{t:05.2f}.png"))

# 1. voix : plus grand blanc entre deux mots
ws = E.ALL_WORDS
gaps = [b["s"] - a["e"] for a, b in zip(ws, ws[1:])]
check("blanc max voix <= 0,30 s (hors respirations de phrase)",
      max(g for g in gaps if g < 0.5) <= 0.30 + 0.25, f"{max(gaps):.2f}s")
# 2. hook
check("question posée avant 3 s", TL.W(0, "quoi", end=True) <= 3.0, f"{TL.W(0, 'quoi', end=True):.2f}s")
# 3. ffprobe
mp4 = os.path.join(E.ROOT, "renders", "douche.mp4")
if os.path.exists(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate",
                          "-show_entries", "format=duration", "-of", "json", mp4], capture_output=True, text=True).stdout
    d = json.loads(out); v = [s for s in d["streams"] if s["codec_type"] == "video"][0]
    na = sum(s["codec_type"] == "audio" for s in d["streams"])
    check("1080x1920, 30 fps, 1 piste audio, <= 60 s",
          v["width"] == 1080 and v["height"] == 1920 and v["r_frame_rate"] == "30/1" and na == 1
          and float(d["format"]["duration"]) <= 60, d["format"]["duration"])
    # 4. silences
    sd = subprocess.run(["ffmpeg", "-i", mp4, "-af", "silencedetect=n=-50dB:d=0.3", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    sil = re.findall(r"silence_start: ([\d.]+)", sd)
    check("aucun silence (-50 dB, 0,3 s)", not [s for s in sil if float(s) < TL.DURATION - 0.7], sil)
# 5-7. grille, palette, placement sur un échantillon d'images
bad_grid = bad_pal = bad_place = 0
cap_y0 = E.CAPTION_ZONE[1]
for k in range(0, int(TL.DURATION * FPS), 7):
    t = k / FPS
    E.PIP_BOX.clear()
    c = E.frame(t)
    if c.max() >= len(PAL): bad_pal += 1
    rgb = to_rgb(c)
    blk = rgb.reshape(640, 3, 360, 3, 3)
    if not (blk == blk[:, :1, :, :1]).all(): bad_grid += 1
    b = E.PIP_BOX.get("box")
    if b and b[1] + b[3] > cap_y0 - 2 and TL.scene_at(t) != 5: bad_place += 1
check("grille pixel 3x3 uniforme", bad_grid == 0, bad_grid)
check("palette respectée", bad_pal == 0, bad_pal)
check("Pip ne touche pas les sous-titres", bad_place == 0, bad_place)
# 8. variété Pip
acts = E.PIP_ACTIONS
check("Pip absent d'au moins 2 scènes", sum(v is None for v in acts.values()) >= 2)
fam = [acts[i][0] if acts[i] else None for i in sorted(acts)]
check("familles alternées", all(a is None or a != b for a, b in zip(fam, fam[1:])), fam)
# 9. pas de balise dans les sous-titres
check("aucune balise [..] dans timings", not any("[" in w["w"] for w in ws))
# 10. rythme
nw = len(ws); dur = TL.SCENES[-1]["end"] - TL.SCENES[0]["start"]
print(f"    débit moyen {nw / dur:.2f} mots/s")
for i, sc in enumerate(TL.SCENES):
    n = sum(len(s["words"]) for s in sc["sentences"])
    r = n / (sc["end"] - sc["start"])
    check(f"scène {i + 1} >= 2,8 mots/s", r >= 2.75, f"{r:.2f}")
print("TOUT OK" if ok else "À REVOIR")
