"""Calage commun sur audio/timings.json : scènes, mots, moments forts (images + sons)."""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
_T = json.load(open(os.path.join(ROOT, "audio", "timings.json")))
DURATION = _T["duration"]
SCENES = _T["scenes"]
N = len(SCENES)

# bornes des scènes : la scène i va de BOUNDS[i] à BOUNDS[i+1]
BOUNDS = [0.0] + [(SCENES[i]["end"] + SCENES[i + 1]["start"]) / 2 for i in range(N - 1)] + [DURATION]
TRANS = 0.4  # durée du volet mosaïque, centré sur la frontière


def _norm(w):
    return re.sub(r"[^a-zàâçéèêëîïôûùüÿœ'-]", "", w.lower())


def words(si):
    return [w for s in SCENES[si]["sentences"] for w in s["words"]]


def W(si, prefix, n=0, end=False):
    """Temps global du n-ième mot de la scène si qui commence par prefix."""
    hits = [w for w in words(si) if _norm(w["w"]).startswith(prefix)]
    w = hits[n]
    return w["e"] if end else w["s"]


def S(si, k, end=False):
    s = SCENES[si]["sentences"][k]
    return s["end"] if end else s["start"]


def scene_at(t):
    for i in range(N):
        if t < BOUNDS[i + 1]:
            return i
    return N - 1


# Moments forts partagés entre l'image et le son : (temps, bruitage)
def events():
    ev = []
    for b in BOUNDS[1:-1]:
        ev.append((b - 0.1 - TRANS / 2, "whoosh"))
    ev += [
        (0.05, "shower"), (0.15, "pop"),
        (W(0, "douche") - 0.05, "squeak"), (W(0, "douche") + 0.25, "plic"),
        (W(0, "quoi"), "ticktack"),
        (W(1, "rien"), "ding"),
        (W(1, "bact"), "pop"), (W(1, "mangent"), "slurp"), (W(1, "mangent") + 0.35, "slurp"),
        (W(1, "puent"), "fart"), (W(1, "puent") + 0.1, "pop"),
        (W(1, "buffet"), "pop"),
        (W(2, "trente"), "pop"), (W(2, "sébum"), "plic"), (W(2, "collent"), "slurp"),
        (W(2, "semaines"), "ticktack"),
        (W(3, "champ"), "mushpop"), (W(3, "champ") + 0.15, "mushpop"),
        (W(3, "champ") + 0.3, "mushpop"), (W(3, "champ") + 0.45, "mushpop"),
        (W(3, "gratte"), "scratch"), (W(3, "rougit"), "scratch"),
        (W(4, "survis"), "ding"), (W(4, "malade"), "buzzer_soft"),
        (W(4, "fuit") - 0.2, "zip"), (W(4, "fuit") + 0.4, "wind"),
        (W(5, "toi"), "pop"), (W(5, "non"), "buzzer"), (W(5, "nez"), "pop"),
        (W(5, "seul"), "ding"),
        (W(6, "douche"), "buzzer_soft"),
        (W(6, "aisselles"), "ding"), (W(6, "pieds"), "ding"), (W(6, "mains"), "bubbles"),
        (W(7, "douche"), "shower"), (W(7, "abonne") - 0.25, "boing"),
        (W(7, "abonne"), "bonk"), (W(7, "abonne") + 0.15, "bell"),
    ]
    return sorted(ev)


# fenêtres musicales
MUSIC_CUT = (W(4, "survis") - 0.75, W(4, "survis") - 0.15)  # silence avant la révélation
FAST = (W(2, "semaines"), BOUNDS[3])                         # accéléré : +1 octave
WHISPER = (S(3, 0), S(3, 0, end=True))                       # musique en sourdine
