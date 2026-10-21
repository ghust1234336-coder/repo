"""Musique chiptune + bruitages synthétisés (numpy) + voix -> audio/mix.wav"""
import os, wave
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


def square(f, t, duty=0.5):
    ph = np.cumsum(np.broadcast_to(f, t.shape) / SR) % 1.0
    return np.where(ph < duty, 1.0, -1.0)


def tri(f, t):
    ph = np.cumsum(np.broadcast_to(f, t.shape) / SR) % 1.0
    return 4 * np.abs(ph - 0.5) - 1


def sine(f, t):
    return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, t.shape) / SR))


def noise(n):
    return rng.uniform(-1, 1, n)


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


# ---------- bruitages ----------
def s_whoosh():
    t = tt(0.35); n = noise(len(t))
    x = np.zeros_like(n)
    for i, k in enumerate(np.linspace(30, 3, 6)):
        seg = slice(i * len(t) // 6, (i + 1) * len(t) // 6)
        x[seg] = lowpass(n, int(k))[seg]
    return 0.6 * x * np.sin(np.pi * t / t[-1])

def s_pop():
    t = tt(0.08); return 0.5 * square(np.linspace(400, 1400, len(t)), t) * env(len(t), r=0.06)

def s_mushpop():
    t = tt(0.1); return 0.5 * square(np.linspace(220, 700, len(t)), t, 0.25) * env(len(t), r=0.08)

def s_ding():
    t = tt(0.6); return 0.35 * (square(1318, t, 0.25) * 0.5 + sine(2637, t) * 0.5) * np.exp(-t * 7)

def s_buzzer():
    t = tt(0.4); return 0.35 * square(110, t) * env(len(t), r=0.05)

def s_buzzer_soft():
    t = tt(0.25); return 0.22 * square(np.linspace(180, 120, len(t)), t) * env(len(t), r=0.05)

def s_ticktack():
    out = np.zeros(int(1.2 * SR))
    for i in range(16):
        t = tt(0.02); c = 0.35 * square(2000 if i % 2 else 1500, t, 0.3) * np.exp(-t * 200)
        p = int(i * 0.07 * SR); out[p:p + len(c)] += c
    return out

def s_squeak():
    t = tt(0.3); f = 900 + 250 * np.sin(2 * np.pi * 18 * t) + np.linspace(0, 300, len(t))
    return 0.2 * square(f, t, 0.3) * env(len(t), r=0.1)

def s_plic():
    t = tt(0.12); return 0.5 * sine(np.linspace(1800, 500, len(t)), t) * np.exp(-t * 30)

def s_slurp():
    t = tt(0.3); f = np.linspace(300, 900, len(t)) + 80 * np.sin(2 * np.pi * 30 * t)
    return 0.25 * square(f, t, 0.2) * np.sin(np.pi * t / t[-1])

def s_fart():
    t = tt(0.55); f = 75 + 20 * np.sin(2 * np.pi * 11 * t) + rng.normal(0, 4, len(t))
    return 0.45 * square(f, t, 0.35) * env(len(t), a=0.02, r=0.2)

def s_scratch():
    out = np.zeros(int(0.5 * SR))
    for i in range(6):
        b = lowpass(noise(int(0.05 * SR)), 2) * 0.35
        p = int(i * 0.08 * SR); out[p:p + len(b)] += b * env(len(b), r=0.03)
    return out

def s_zip():
    t = tt(0.25); return 0.3 * square(np.linspace(300, 2400, len(t)), t, 0.25) * env(len(t), r=0.05)

def s_wind():
    t = tt(1.4); x = lowpass(noise(len(t)), 40) * 3
    return 0.4 * x * np.sin(np.pi * t / t[-1]) * (0.7 + 0.3 * np.sin(2 * np.pi * 1.5 * t))

def s_bubbles():
    out = np.zeros(int(0.7 * SR))
    for i in range(9):
        t = tt(0.05); f = rng.uniform(900, 2000)
        b = 0.3 * sine(np.linspace(f, f * 1.8, len(t)), t) * np.exp(-t * 60)
        p = int(rng.uniform(0, 0.6) * SR); out[p:p + len(b)] += b
    return out

def s_shower():
    t = tt(0.9); x = noise(len(t)) - lowpass(noise(len(t)), 3)
    return 0.12 * x * env(len(t), a=0.05, r=0.3)

def s_boing():
    t = tt(0.35); f = 300 + 200 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 6)
    return 0.3 * tri(f, t) * np.exp(-t * 5)

def s_bonk():
    t = tt(0.15); return 0.5 * square(np.linspace(200, 80, len(t)), t) * np.exp(-t * 25)

def s_bell():
    t = tt(1.0)
    return 0.3 * (square(1568, t, 0.25) * 0.5 + square(2093, t, 0.125) * 0.3) * np.exp(-t * 4) * \
        (np.sin(2 * np.pi * 22 * t) > -0.3)


SFX = {k[2:]: v for k, v in globals().items() if k.startswith("s_")}

# ---------- musique ----------
BPM = 120
BEAT = 60 / BPM
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)
# la mineur, 2 mesures x 4 temps en croches (16 pas)
MEL_A = [69, 0, 72, 69, 76, 0, 74, 72, 69, 0, 67, 69, 72, 0, 71, 0,
         69, 0, 72, 76, 79, 0, 77, 76, 74, 72, 71, 0, 69, 0, 0, 0]
MEL_C = [72, 0, 76, 72, 79, 0, 77, 76, 72, 0, 74, 76, 79, 0, 84, 0]  # do majeur (fin)
BASS = [45, 45, 52, 45, 41, 41, 48, 41, 43, 43, 50, 43, 40, 40, 47, 40]


def music(dur):
    out = np.zeros(int(dur * SR) + SR)
    step = BEAT / 2
    nsteps = int(dur / step) + 1
    for i in range(nsteps):
        t0 = i * step
        oct_ = 12 if TL.FAST[0] <= t0 < TL.FAST[1] else 0
        final = t0 >= TL.BOUNDS[7]
        m = (MEL_C[i % 16] if final else MEL_A[i % 32])
        p = int(t0 * SR)
        if m:
            t = tt(step * 0.9)
            out[p:p + len(t)] += 0.22 * square(NOTE(m + oct_), t, 0.25) * env(len(t), r=0.05)
        b = BASS[(i // 2) % 16] + (5 if final else 0)
        t = tt(step * 0.95)
        out[p:p + len(t)] += 0.3 * tri(NOTE(b + oct_), t) * env(len(t), r=0.02)
        if i % 2 == 1 or oct_:
            t = tt(0.04); out[p:p + len(t)] += 0.12 * noise(len(t)) * np.exp(-t * 90)
        if i % 4 == 0:
            t = tt(0.12)
            out[p:p + len(t)] += 0.35 * sine(np.linspace(150, 40, len(t)), t) * np.exp(-t * 25)
    out = out[:int(dur * SR)]
    # volumes : sourdine, coupure, fondu final
    g = np.ones_like(out)
    tg = np.arange(len(out)) / SR
    g[(tg >= TL.WHISPER[0]) & (tg < TL.WHISPER[1])] = 0.45
    g[(tg >= TL.MUSIC_CUT[0]) & (tg < TL.MUSIC_CUT[1])] = 0.0
    g = lowpass(g, int(0.03 * SR))
    g[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))
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
    mix = voice + mus + fx * rms(voice) / 0.25 * 0.35
    peak = np.abs(mix).max()
    if peak > 0.98:
        mix *= 0.98 / peak
    write_wav(os.path.join(TL.ROOT, "audio", "mix.wav"), mix)
    print(f"mix.wav {dur:.2f}s, pic {peak:.2f}")


if __name__ == "__main__":
    main()
