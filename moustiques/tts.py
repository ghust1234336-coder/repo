"""Voix off ElevenLabs -> audio/voice.wav + audio/timings.json.

Une phrase = une synthèse (cache par phrase). Repli v3 -> multilingual_v2.
Usage : python tts.py [--only N] [--henri]
"""
import base64, hashlib, json, os, re, subprocess, sys, wave
import numpy as np
import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "audio")
SR = 44100
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "jsScnYkNNda9Q1NES5nn")  # Léo, FR
API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")  # le proxy l'injecte si absent

SCRIPT = [
    ["Et si tu effaçais tous les moustiques de la planète ?"],
    ["Bonne idée : c'est l'animal le plus mortel.",
     "Rien qu'avec le paludisme, près de six cent mille morts par an.",
     "Plus de sept Stades de France pleins, chaque année."],
    ["Mais ce n'est pas la piqûre qui tue : c'est un parasite.",
     "La femelle l'aspire chez un malade, puis pique quelqu'un d'autre.",
     "Pour les microbes, le moustique est un taxi."],
    ["Sauf que sur trois mille cinq cents espèces, peu nous piquent.",
     "Et les mâles ne piquent jamais : ils boivent du nectar.",
     "Alors si tu les effaces tous… qui va les regretter ?"],
    ["Réponse des biologistes : presque personne.",
     "Oiseaux, poissons et libellules mangeraient d'autres insectes.",
     "Et on sauverait des centaines de milliers de vies."],
    ["Mais alors, aucun animal n'en a besoin ?",
     "Si : dans le Grand Nord, les poussins d'oiseaux migrateurs s'en régalent."],
    ["Alors les scientifiques visent seulement les espèces dangereuses.",
     "Ils lâchent des mâles modifiés : leurs filles meurent jeunes."],
    ["Celui-là, tu peux le garder : c'est un mâle.",
     "Abonne-toi, y'a plein d'autres secrets !"],
]

# (balise v3, stabilité, vitesse) par scène
ELEVEN_EXPRESSION = {
    0: ("[curious]", 0.3, 1.10),
    1: ("[surprised]", 0.3, 1.10),
    2: ("[curious]", 0.5, 1.10),
    3: ("[whispers]", 0.5, 1.10),
    4: ("[playful]", 0.5, 1.10),
    5: ("[mischievously]", 0.3, 1.10),
    6: ("[excited]", 0.3, 1.10),
    7: ("[excited]", 0.3, 1.10),
}
# balise seulement sur certaines phrases (1 par phrase au plus)
TAG_ON = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (7, 1)}

SENT_GAP = 0.22
SCENE_GAP = 0.20
MUSIC_CUT_BEFORE = {(4, 0): 0.0}  # « Réponse des biologistes »  # la coupure musicale est gérée dans sfx.py


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def read_wav(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a


def write_wav(path, a):
    a = np.clip(a, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((a * 32767).astype(np.int16).tobytes())


def synth(text, prev, nxt, model, stability):
    body = {"text": text, "model_id": model, "language_code": "fr",
            "apply_text_normalization": "on",
            "voice_settings": {"stability": stability, "similarity_boost": 0.8,
                               "style": 0.45 if model != "eleven_v3" else 0.0}}
    if model != "eleven_v3":
        body["previous_text"], body["next_text"] = prev, nxt
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["xi-api-key"] = API_KEY
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
                      "?output_format=mp3_44100_128", json=body, headers=headers, timeout=120)
    r.raise_for_status()
    return r.json()


def words_from_alignment(al):
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    # retirer les balises [..]
    keep, depth = [], 0
    for i, c in enumerate(chars):
        if c == "[":
            depth += 1; continue
        if c == "]":
            depth -= 1; continue
        if depth == 0:
            keep.append(i)
    words, cur = [], None
    for i in keep:
        c = chars[i]
        if c.isspace():
            if cur: words.append(cur); cur = None
            continue
        if cur is None:
            cur = {"w": c, "s": st[i], "e": en[i]}
        else:
            cur["w"] += c; cur["e"] = en[i]
    if cur: words.append(cur)
    # coller la ponctuation isolée au mot précédent
    out = []
    for w in words:
        if out and re.fullmatch(r"[?!:;…,.]+", w["w"]):
            out[-1]["w"] += " " + w["w"] if w["w"] in "?!:;" else w["w"]
            out[-1]["e"] = w["e"]
        else:
            out.append(w)
    return out


def take(si, pi, henri=False):
    text = SCRIPT[si][pi]
    tag, stab, speed = ELEVEN_EXPRESSION[si]
    flat = [s for sc in SCRIPT for s in sc]
    k = sum(len(sc) for sc in SCRIPT[:si]) + pi
    prev = flat[k - 1] if k else ""
    nxt = flat[k + 1] if k + 1 < len(flat) else ""
    vt = (tag + " " if (si, pi) in TAG_ON else "") + text
    key = hashlib.sha1(f"{vt}|{stab}|{henri}".encode()).hexdigest()[:12]
    cdir = os.path.join(AUDIO, "takes", "henri" if henri else f"eleven/{VOICE_ID}")
    os.makedirs(cdir, exist_ok=True)
    base = os.path.join(cdir, f"s{si}_{pi}_{key}")
    if not os.path.exists(base + ".json"):
        if henri:
            import asyncio, edge_tts
            async def go():
                comm = edge_tts.Communicate(text, "fr-FR-HenriNeural", boundary="WordBoundary")
                ws, buf = [], b""
                async for ch in comm.stream():
                    if ch["type"] == "audio": buf += ch["data"]
                    elif ch["type"] == "WordBoundary":
                        ws.append({"w": ch["text"], "s": ch["offset"] / 1e7,
                                   "e": (ch["offset"] + ch["duration"]) / 1e7})
                return buf, ws
            buf, ws = asyncio.run(go())
            open(base + ".mp3", "wb").write(buf)
        else:
            try:
                d = synth(vt, prev, nxt, "eleven_v3", stab)
            except Exception as e:
                print("v3 KO, repli v2:", e)
                d = synth(text, prev, nxt, "eleven_multilingual_v2", stab)
            open(base + ".mp3", "wb").write(base64.b64decode(d["audio_base64"]))
            ws = words_from_alignment(d["alignment"])
        json.dump(ws, open(base + ".json", "w"), ensure_ascii=False)
        print("généré", si, pi, text)
    ws = json.load(open(base + ".json"))
    # décodage + vitesse
    wav = base + f"_x{speed}.wav"
    if not os.path.exists(wav):
        run(["ffmpeg", "-y", "-i", base + ".mp3", "-ac", "1", "-ar", str(SR),
             "-filter:a", f"atempo={speed}", wav])
    a = read_wav(wav)
    ws = [dict(w, s=w["s"] / speed, e=w["e"] / speed) for w in ws]
    # silences de bord -> 0,03 s
    env = np.abs(a) > 0.02
    idx = np.nonzero(env)[0]
    t0 = max(0, idx[0] - int(0.03 * SR)); t1 = min(len(a), idx[-1] + int(0.03 * SR))
    a = a[t0:t1]
    off = t0 / SR
    ws = [dict(w, s=max(0.0, w["s"] - off), e=min(len(a) / SR, w["e"] - off)) for w in ws]
    # silences internes <= 0,25 s
    a, ws = squeeze_silences(a, ws)
    return a, ws, text


def squeeze_silences(a, ws, maxgap=0.25):
    hop = int(0.01 * SR)
    loud = np.array([np.abs(a[i:i + hop]).max() > 0.015 for i in range(0, len(a), hop)])
    out, cuts, i = [], [], 0
    n = len(loud)
    while i < n:
        if not loud[i]:
            j = i
            while j < n and not loud[j]: j += 1
            if (j - i) * 0.01 > maxgap:
                keep = int(maxgap / 0.01)
                cuts.append(((i + keep) * hop / SR, (j - i - keep) * hop / SR))
                out.append(a[i * hop:(i + keep) * hop])
            else:
                out.append(a[i * hop:j * hop])
            i = j
        else:
            j = i
            while j < n and loud[j]: j += 1
            out.append(a[i * hop:j * hop]); i = j
    def shift(t):
        d = 0.0
        for at, ln in cuts:
            if t > at + ln: d += ln
            elif t > at: d += t - at
        return t - d
    return np.concatenate(out), [dict(w, s=shift(w["s"]), e=shift(w["e"])) for w in ws]


def main():
    henri = "--henri" in sys.argv
    os.makedirs(AUDIO, exist_ok=True)
    pieces, scenes, t = [], [], 0.1
    pieces.append(np.zeros(int(0.1 * SR)))
    for si, sc in enumerate(SCRIPT):
        if si:
            pieces.append(np.zeros(int(SCENE_GAP * SR))); t += SCENE_GAP
        scene = {"start": t, "sentences": []}
        for pi in range(len(sc)):
            if pi:
                pieces.append(np.zeros(int(SENT_GAP * SR))); t += SENT_GAP
            a, ws, text = take(si, pi, henri)
            scene["sentences"].append({"text": text, "start": t, "end": t + len(a) / SR,
                                       "words": [dict(w, s=w["s"] + t, e=w["e"] + t) for w in ws]})
            pieces.append(a); t += len(a) / SR
        scene["end"] = t
        scenes.append(scene)
    pieces.append(np.zeros(int(0.6 * SR)))
    voice = np.concatenate(pieces).astype(np.float32)
    raw = os.path.join(AUDIO, "voice_raw.wav")
    write_wav(raw, voice)
    run(["ffmpeg", "-y", "-i", raw, "-af",
         "deesser=i=0.3,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "1",
         os.path.join(AUDIO, "voice.wav")])
    json.dump({"duration": len(voice) / SR, "scenes": scenes},
              open(os.path.join(AUDIO, "timings.json"), "w"), ensure_ascii=False, indent=1)
    nw = sum(len(s["words"]) for sc in scenes for s in sc["sentences"])
    print(f"durée {len(voice)/SR:.2f}s, {nw} mots, {nw/(t-0.1):.2f} mots/s")
    for i, sc in enumerate(scenes):
        w = sum(len(s["words"]) for s in sc["sentences"])
        print(f"  scène {i+1}: {sc['end']-sc['start']:.2f}s  {w/(sc['end']-sc['start']):.2f} mots/s")


if __name__ == "__main__":
    main()
