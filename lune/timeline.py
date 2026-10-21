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
    cuts = [S(2, 1), S(2, 2), S(2, 3), S(3, 1), S(3, 3), S(4, 1), S(4, 2), S(4, 3), S(5, 1), S(1, 1)]
    ev += [(c - 0.08, "whoosh") for c in cuts]
    ev += [
        (0.05, "twinkle"), (0.2, "pop"),
        (W(0, "disparaît") - 0.05, "snip"), (W(0, "disparaît") + 0.15, "vanish"),
        (W(0, "quoi"), "marker"),
        (W(1, "première") - 0.15, "stamp"), (W(1, "nuit") + 0.25, "type"),
        (W(1, "noir"), "lights_off"), (W(1, "d'encre") + 0.1, "twinkle"),
        (W(1, "astronomes"), "pop"), (W(1, "fête"), "party"), (W(1, "fête") + 0.1, "pop"),
        (W(2, "six") - 0.15, "stamp"), (W(2, "heures") + 0.25, "type"),
        (W(2, "tsunami"), "marker"), (W(2, "rate"), "buzzer_soft"), (W(2, "marée"), "wave"),
        (W(2, "tirait"), "stretch"), (W(2, "aimant"), "ding"),
        (W(2, "petites"), "drain"), (W(2, "trois"), "pop"),
        (W(2, "mont"), "wave"), (W(2, "île"), "marker"),
        (W(3, "sauf") - 0.15, "stamp"), (W(3, "mois") + 0.2, "type"),
        (W(3, "dérègle"), "marker"),
        (W(3, "pondent"), "bubbles"), (W(3, "pleine"), "ding"),
        (W(3, "ratent"), "buzzer_soft"), (W(3, "rendez"), "marker"),
        (W(3, "lions"), "growl"), (W(3, "noir"), "pop"),
        (W(4, "des") - 0.15, "stamp"), (W(4, "d'années") + 0.3, "type"),
        (W(4, "tanguer"), "wobble"),
        (W(4, "toupie") - 0.2, "spin"),
        (W(4, "extrêmes"), "marker"),
        (W(4, "pingouins"), "pop"), (W(4, "crème"), "spray"),
        (W(5, "orbite"), "whoosh"), (W(5, "non"), "buzzer"), (W(5, "quatre"), "count"),
        (W(5, "légère"), "ding"),
        (W(6, "fou"), "pop"), (W(6, "va"), "stretch"), (W(6, "centimètres"), "tick"),
        (W(7, "regarde"), "twinkle"), (W(7, "abonne") - 0.25, "boing"),
        (W(7, "abonne"), "bonk"), (W(7, "abonne") + 0.15, "bell"),
    ]
    return sorted(ev)


# fenêtres musicales
MUSIC_CUT = (W(4, "la", 0) - 0.6, W(4, "la", 0) - 0.05)  # silence avant « La Terre se met à tanguer »
WHISPER = (S(3, 0), S(3, 0, end=True))                    # musique en sourdine (« Sauf qu'au bout d'un mois »)
