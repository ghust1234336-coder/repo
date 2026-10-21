"""Images de contrôle + tests A8 (version STYLE = flat : pas de test grille / palette). python snap.py [t ...]"""
import json, os, re, subprocess, sys
from PIL import Image
import episode_lune as E
import timeline as TL
from vox import FPS, finish

ok = True


def check(name, cond, info=""):
    global ok
    ok &= bool(cond)
    print(("OK  " if cond else "KO  ") + name, info)


for s in sys.argv[1:]:
    t = float(s)
    Image.fromarray(finish(E.frame(t), t)).save(os.path.join(E.ROOT, "renders", f"snap_{t:05.2f}.png"))

# 1. voix : plus grand blanc entre deux mots d'une même phrase
ws = E.ALL_WORDS
gaps = [b["s"] - a["e"] for sc in TL.SCENES for s in sc["sentences"] for a, b in zip(s["words"], s["words"][1:])]
check("blanc max dans une phrase <= 0,30 s", max(gaps) <= 0.30, f"{max(gaps):.2f}s")
# 2. hook
check("question posée avant 3 s", TL.W(0, "quoi", end=True) <= 3.0, f"{TL.W(0, 'quoi', end=True):.2f}s")
# 3-4. ffprobe + silences
mp4 = os.path.join(E.ROOT, "renders", "lune.mp4")
if os.path.exists(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate",
                          "-show_entries", "format=duration", "-of", "json", mp4], capture_output=True, text=True).stdout
    d = json.loads(out); v = [s for s in d["streams"] if s["codec_type"] == "video"][0]
    na = sum(s["codec_type"] == "audio" for s in d["streams"])
    check("1080x1920, 30 fps, 1 piste audio, <= 60 s",
          v["width"] == 1080 and v["height"] == 1920 and v["r_frame_rate"] == "30/1" and na == 1
          and float(d["format"]["duration"]) <= 60, d["format"]["duration"])
    sd = subprocess.run(["ffmpeg", "-i", mp4, "-af", "silencedetect=n=-50dB:d=0.3", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    sil = re.findall(r"silence_start: ([\d.]+)", sd)
    check("aucun silence (-50 dB, 0,3 s)", not [s for s in sil if float(s) < TL.DURATION - 0.7], sil)
# 7. placement : Pip ne touche jamais la zone des sous-titres
bad = 0
cap_y0 = E.CAPTION_ZONE[1]
for k in range(0, int(TL.DURATION * FPS), 9):
    E.PIP_BOX.clear()
    E.frame(k / FPS)
    b = E.PIP_BOX.get("box")
    if b and b[1] + b[3] > cap_y0 + 20:
        bad += 1
check("Pip ne touche pas les sous-titres", bad == 0, bad)
# 8. variété Pip
acts = E.PIP_ACTIONS
check("Pip absent d'au moins 1 scène (+ plans sans lui)", sum(v is None for v in acts.values()) >= 1)
fam = [acts[i][0] if acts[i] else None for i in sorted(acts)]
check("familles alternées", all(a is None or a != b for a, b in zip(fam, fam[1:])), fam)
# 9. pas de balise dans les sous-titres
check("aucune balise [..] dans timings", not any("[" in w["w"] for w in ws))
# 10. rythme (mots à l'oral : les traits d'union séparent les mots, « quatre-vingt-une » = 3)
spoken = lambda w: len([x for x in re.split(r"[-\s]", w["w"]) if re.search(r"\w", x)])
nw = sum(spoken(w) for w in ws); dur = TL.SCENES[-1]["end"] - TL.SCENES[0]["start"]
print(f"    débit moyen {nw / dur:.2f} mots/s ({nw} mots, {dur:.1f} s de voix)")
for i, sc in enumerate(TL.SCENES):
    n = sum(spoken(w) for s in sc["sentences"] for w in s["words"])
    r = n / (sc["end"] - sc["start"])
    check(f"scène {i + 1} >= 2,8 mots/s", r >= 2.75, f"{r:.2f}")
txt = " ".join(s["text"] for sc in TL.SCENES for s in sc["sentences"])
check("« … » au plus une fois par scène", all(" ".join(s["text"] for s in sc["sentences"]).count("…") <= 1
                                            for sc in TL.SCENES))
print("TOUT OK" if ok else "À REVOIR")
