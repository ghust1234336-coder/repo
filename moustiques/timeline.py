"""Calage commun sur audio/timings.json : scènes, mots, moments forts (images + sons)."""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
_T = json.load(open(os.path.join(ROOT, "audio", "timings.json")))
DURATION = _T["duration"]
SCENES = _T["scenes"]
N = len(SCENES)

# bornes des scènes : la scène i va de BOUNDS[i] à BOUNDS[i+1]
BOUNDS = [0.0] + [(SCENES[i]["end"] + SCENES[i + 1]["start"]) / 2 for i in range(N - 1)] + [DURATION]
TRANS = 0.45  # durée du volet « papier déchiré », centré sur la frontière


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
        ev.append((b - 0.1 - TRANS / 2, "paper"))
    cuts = [S(1, 1), S(1, 2), S(2, 1), S(2, 2), S(3, 1), S(3, 2), S(4, 1), S(4, 2), S(5, 1), S(6, 1)]
    ev += [(c - 0.08, "whoosh") for c in cuts]
    ev += [
        (0.02, "bzz"), (0.15, "pop"), (W(0, "effaçais") - 0.1, "wand"), (W(0, "planète"), "pop"),
        (W(1, "mortel"), "stamp"), (W(1, "mortel") + 0.1, "pop"),
        (W(1, "paludisme"), "count"), (W(1, "morts"), "stamp"),
        (W(1, "sept"), "pop"), (W(1, "stades"), "pop"), (W(1, "france"), "pop"), (W(1, "pleins"), "pop"),
        (W(1, "année"), "marker"),
        (W(2, "piqûre"), "pop"), (W(2, "tue"), "marker"), (W(2, "parasite"), "ding"),
        (W(2, "femelle"), "bzz"), (W(2, "l'aspire"), "sip"), (W(2, "pique"), "marker"),
        (W(2, "microbes"), "pop"), (W(2, "taxi"), "honk"), (W(2, "taxi") + 0.05, "stamp"),
        (W(3, "trois"), "tick"), (W(3, "peu"), "marker"),
        (W(3, "mâles"), "bzz_low"), (W(3, "nectar"), "sip"),
        (W(3, "regretter") - 0.2, "type"),
        (W(4, "presque"), "pop"), (W(4, "personne"), "ding"), (W(4, "personne") + 0.4, "bzz"),
        (W(4, "oiseaux"), "chirp"), (W(4, "poissons"), "pop"), (W(4, "libellules"), "pop"),
        (W(4, "mangeraient"), "marker"), (W(4, "insectes"), "marker"),
        (W(4, "sauverait"), "count"), (W(4, "vies"), "ding"),
        (W(5, "besoin"), "marker"), (W(5, "grand"), "wind"), (W(5, "grand") + 0.2, "bzz_low"),
        (W(5, "poussins"), "chirp"), (W(5, "régalent"), "chirp"),
        (W(6, "visent"), "tick"), (W(6, "dangereuses"), "marker"),
        (W(6, "lâchent"), "boxopen"), (W(6, "lâchent") + 0.15, "bzz_low"), (W(6, "filles"), "marker"),
        (W(6, "jeunes"), "marker"),
        (0.02 + S(7, 0), "bzz_low"), (W(7, "mâle"), "ding"),
        (W(7, "abonne"), "boing"), (W(7, "abonne") + 0.45, "bonk"), (W(7, "abonne") + 0.6, "bell"),
    ]
    return sorted(ev)


# fenêtres musicales
MUSIC_CUT = (S(4, 0) - 0.6, S(4, 0) - 0.05)    # silence avant « Réponse des biologistes »
WHISPER = (S(3, 0), S(3, 0, end=True))           # musique en sourdine (« Sauf que… peu nous piquent »)
FINAL = 6                                        # passage en majeur à partir de la scène 7
