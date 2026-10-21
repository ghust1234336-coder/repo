"""Musique « documentaire » (pad + arpège + pulsation) et bruitages papier, synthétisés en numpy -> audio/mix.wav"""
import os
import numpy as np
import timeline as TL
from tts import read_wav, write_wav, SR

rng = np.random.default_rng(7)


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.005, r=None):
    e = np.ones(n)
    na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    if r:
        nr = min(n, int(r * SR)); e[-nr:] *= np.linspace(1, 0, nr)
    return e


def sine(f, t):
    return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, t.shape) / SR))


def square(f, t, duty=0.5):
    ph = np.cumsum(np.broadcast_to(f, t.shape) / SR) % 1.0
    return np.where(ph < duty, 1.0, -1.0)


def noise(n):
    return rng.uniform(-1, 1, n)


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def band(x, lo, hi):
    """Filtre passe-bande grossier par FFT."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


# ---------- bruitages ----------
def s_paper():   # feuille qui glisse (transition)
    t = tt(0.45); x = band(noise(len(t)), 1500, 9000)
    return 0.5 * x * np.sin(np.pi * t / t[-1]) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))

def s_whoosh():
    t = tt(0.3); x = band(noise(len(t)), 300, 3000)
    return 0.5 * x * np.sin(np.pi * t / t[-1]) ** 3

def s_pop():
    t = tt(0.09); return 0.45 * sine(np.linspace(500, 1300, len(t)), t) * env(len(t), r=0.07)

def s_snip():    # coup de ciseaux
    out = np.zeros(int(0.22 * SR))
    for p in (0.0, 0.11):
        t = tt(0.06); c = band(noise(len(t)), 2500, 12000) * np.exp(-t * 80)
        out[int(p * SR):int(p * SR) + len(c)] += 0.7 * c
    return out

def s_vanish():  # scintillement qui descend
    t = tt(0.7); f = np.linspace(2400, 300, len(t))
    return 0.25 * (sine(f, t) * 0.6 + sine(f * 1.5, t) * 0.4) * np.exp(-t * 3) * (np.sin(2 * np.pi * 30 * t) > -0.2)

def s_twinkle():
    out = np.zeros(int(0.9 * SR))
    for i, f in enumerate([1760, 2349, 2093, 2637, 3136]):
        t = tt(0.3); b = 0.14 * sine(f, t) * np.exp(-t * 14)
        p = int(i * 0.12 * SR); out[p:p + len(b)] += b
    return out

def s_marker():  # feutre sur papier
    t = tt(0.32); x = band(noise(len(t)), 2000, 7000)
    return 0.35 * x * env(len(t), a=0.02, r=0.08) * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * t))

def s_stamp():   # tampon / touche de machine lourde
    t = tt(0.3)
    return 0.6 * sine(np.linspace(140, 55, len(t)), t) * np.exp(-t * 16) + \
        0.3 * band(noise(len(t)), 800, 5000) * np.exp(-t * 60)

def s_type():    # machine à écrire, 6 frappes
    out = np.zeros(int(0.6 * SR))
    for i in range(6):
        t = tt(0.04); c = band(noise(len(t)), 1500, 8000) * np.exp(-t * 120) * 0.5
        p = int((i * 0.075 + rng.uniform(0, 0.02)) * SR); out[p:p + len(c)] += c
    return out

def s_ding():
    t = tt(0.8); return 0.3 * (sine(1318, t) * 0.6 + sine(2637, t) * 0.25 + sine(3951, t) * 0.15) * np.exp(-t * 5)

def s_buzzer():
    t = tt(0.4); return 0.28 * square(110, t) * env(len(t), r=0.05) * 0.8

def s_buzzer_soft():
    t = tt(0.3); return 0.25 * sine(np.linspace(220, 150, len(t)), t) * env(len(t), r=0.1)

def s_lights_off():
    t = tt(0.12); return 0.5 * band(noise(len(t)), 500, 4000) * np.exp(-t * 60)

def s_party():   # langue de belle-mère
    t = tt(0.6); f = 420 + 40 * np.sin(2 * np.pi * 7 * t)
    return 0.22 * square(f, t, 0.3) * env(len(t), a=0.03, r=0.2)

def s_wave():
    t = tt(1.1); x = lowpass(noise(len(t)), 12)
    return 0.6 * x * np.sin(np.pi * t / t[-1]) ** 2

def s_drain():
    t = tt(0.9); x = band(noise(len(t)), 300, 1600)
    return 0.4 * x * np.linspace(1, 0, len(t)) ** 2 + 0.15 * sine(np.linspace(600, 200, len(t)), t) * np.exp(-t * 4)

def s_stretch():  # élastique qui se tend
    t = tt(0.4); return 0.25 * sine(np.linspace(180, 420, len(t)), t) * env(len(t), r=0.1)

def s_bubbles():
    out = np.zeros(int(0.9 * SR))
    for i in range(12):
        t = tt(0.05); f = rng.uniform(700, 1800)
        b = 0.25 * sine(np.linspace(f, f * 1.9, len(t)), t) * np.exp(-t * 60)
        p = int(rng.uniform(0, 0.8) * SR); out[p:p + len(b)] += b
    return out

def s_growl():
    t = tt(0.8); f = 70 + 15 * np.sin(2 * np.pi * 6 * t)
    x = (square(f, t, 0.4) * 0.5 + band(noise(len(t)), 80, 600) * 0.8)
    return 0.4 * lowpass(x, 6) * env(len(t), a=0.08, r=0.3)

def s_wobble():
    t = tt(1.0); f = 200 + 60 * np.sin(2 * np.pi * 3 * t)
    return 0.22 * sine(f, t) * np.exp(-t * 1.5)

def s_spin():
    t = tt(0.8); f = 500 + 300 * t
    return 0.12 * sine(f, t) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * t)) * env(len(t), a=0.1, r=0.2)

def s_spray():
    t = tt(0.4); return 0.3 * band(noise(len(t)), 3000, 11000) * env(len(t), a=0.01, r=0.15)

def s_count():
    out = np.zeros(int(1.0 * SR))
    for i in range(8):
        t = tt(0.03); c = 0.25 * sine(1200 + i * 90, t) * np.exp(-t * 90)
        p = int(i * 0.1 * SR); out[p:p + len(c)] += c
    return out

def s_tick():
    out = np.zeros(int(0.6 * SR))
    for i in range(5):
        t = tt(0.02); c = 0.3 * band(noise(len(t)), 2000, 9000) * np.exp(-t * 200)
        p = int(i * 0.11 * SR); out[p:p + len(c)] += c
    return out

def s_boing():
    t = tt(0.35); f = 300 + 200 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 6)
    return 0.3 * sine(f, t) * np.exp(-t * 5)

def s_bonk():
    t = tt(0.15); return 0.5 * sine(np.linspace(220, 90, len(t)), t) * np.exp(-t * 25)

def s_bell():
    t = tt(1.1)
    return 0.3 * (sine(1568, t) * 0.5 + sine(2093, t) * 0.3 + sine(3136, t) * 0.2) * np.exp(-t * 3.5)


SFX = {k[2:]: v for k, v in globals().items() if k.startswith("s_")}

# ---------- musique ----------
BPM = 112
BEAT = 60 / BPM
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)
# ré mineur : Dm - Bb - F - C (une mesure chacun) ; fin en Fa majeur : F - C - Dm - Bb
CHORDS = [[50, 53, 57, 62], [46, 50, 53, 58], [53, 57, 60, 65], [48, 52, 55, 60]]
CHORDS_END = [[53, 57, 60, 65], [48, 52, 55, 60], [50, 53, 57, 62], [46, 50, 53, 58]]
ARP = [0, 1, 2, 3, 2, 1, 2, 3]


def pluck(f, d):
    t = tt(d)
    x = sine(f, t) + 0.35 * sine(2 * f, t) + 0.12 * sine(3 * f, t)
    return x * np.exp(-t * 7) * env(len(t), a=0.003, r=0.03)


def pad(notes, d):
    t = tt(d); x = np.zeros_like(t)
    for m in notes:
        for det in (-0.12, 0.12):
            f = NOTE(m + det)
            x += sine(f, t) * 0.6 + sine(2 * f, t) * 0.15
    return x / (2 * len(notes)) * env(len(t), a=0.4, r=0.4)


def music(dur):
    out = np.zeros(int(dur * SR) + 4 * SR)
    bar = 4 * BEAT
    for b in range(int(dur / bar) + 1):
        t0 = b * bar
        final = t0 >= TL.BOUNDS[6] - bar / 2
        ch = (CHORDS_END if final else CHORDS)[b % 4]
        p = int(t0 * SR)
        x = pad(ch, bar + 0.3) * 0.5; out[p:p + len(x)] += x
        x = 0.35 * sine(NOTE(ch[0] - 12), tt(bar)) * env(int(bar * SR), a=0.02, r=0.1)
        out[p:p + len(x)] += x
        reveal = t0 >= TL.MUSIC_CUT[1] - 0.1
        for k in range(8):
            q = int((t0 + k * BEAT / 2) * SR)
            m = ch[ARP[k]] + (24 if reveal else 12)
            x = 0.16 * pluck(NOTE(m), BEAT / 2 * 1.6); out[q:q + len(x)] += x
        for k in range(4):  # pulsation : grosse caisse douce sur 1 et 3, charleston en croches
            q = int((t0 + k * BEAT) * SR)
            if k % 2 == 0:
                t = tt(0.25); x = 0.5 * sine(np.linspace(110, 45, len(t)), t) * np.exp(-t * 14)
                out[q:q + len(x)] += x
            for h in (0, 0.5):
                qq = q + int(h * BEAT * SR); t = tt(0.05)
                x = 0.07 * band(noise(len(t)), 6000, 14000) * np.exp(-t * 80); out[qq:qq + len(x)] += x
    out = out[:int(dur * SR)]
    g = np.ones_like(out)
    tg = np.arange(len(out)) / SR
    g[(tg >= TL.WHISPER[0]) & (tg < TL.WHISPER[1])] = 0.45
    g[(tg >= TL.MUSIC_CUT[0]) & (tg < TL.MUSIC_CUT[1])] = 0.0
    g = lowpass(g, int(0.04 * SR))
    g[:int(0.05 * SR)] = np.linspace(0, 1, int(0.05 * SR))
    g[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))
    return out * g


def rms(x):
    return np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2))


def main():
    voice = read_wav(os.path.join(TL.ROOT, "audio", "voice.wav"))
    dur = len(voice) / SR
    mus = music(dur)
    mus *= rms(voice) / rms(mus) * 10 ** (-16.5 / 20)
    fx = np.zeros_like(voice)
    for t, name in TL.events():
        s = SFX[name]() * 0.55
        p = max(0, int(t * SR)); s = s[:len(fx) - p]
        fx[p:p + len(s)] += s
    mix = voice + mus + fx * rms(voice) / 0.25 * 0.3
    peak = np.abs(mix).max()
    if peak > 0.98:
        mix *= 0.98 / peak
    write_wav(os.path.join(TL.ROOT, "audio", "mix.wav"), mix)
    print(f"mix.wav {dur:.2f}s, pic {peak:.2f}")


if __name__ == "__main__":
    main()
