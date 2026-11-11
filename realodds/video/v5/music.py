"""Musique de fond originale, composée et synthétisée ici (aucun extrait d'OST : pas de souci de droits ni de Content ID).
Vibe « lo-fi shinobi » : 80 BPM, la mineur, koto pincé (Karplus-Strong), nappe douce, basse ronde,
batterie lo-fi avec swing, flûte façon shakuhachi rare, craquement de vinyle. Sortie : music.wav (stéréo, 83 s)."""
import numpy as np, wave
from scipy.signal import lfilter, butter, sosfilt
SR = 48000; DUR = 83.0; BPM = 80; BEAT = 60 / BPM; BAR = 4 * BEAT
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(11)
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)

def put(sig, t, gain=1.0, pan=0.0):
    i = max(0, int(t * SR)); j = min(N, i + len(sig))
    if i >= N or j <= i: return
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:j] += gain * l * sig[: j - i]; R[i:j] += gain * r * sig[: j - i]
def lowpass(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def highpass(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bandpass(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)

def koto(m, d=2.2, bright=0.6):
    f = mtof(m); P = SR / f; Ni = int(P); n = int(SR * d)
    exc = np.zeros(n); burst = rng.uniform(-1, 1, Ni); exc[:Ni] = lowpass(burst, 1500 + 6000 * bright)
    rho = 0.996; a = np.zeros(Ni + 2); a[0] = 1; a[Ni] = -rho * .5; a[Ni + 1] = -rho * .5
    y = lfilter([1], a, exc)
    t = np.arange(n) / SR; y *= np.minimum(1, (d - t) / .3)
    return y / (np.abs(y).max() + 1e-9) * .5
def pad(ms, d):
    n = int(SR * d); t = np.arange(n) / SR; y = np.zeros(n)
    for k, m in enumerate(ms):
        for det in (-.07, .07):
            f = mtof(m + det); y += np.sin(2 * np.pi * f * t + k) * (.6 + .4 * np.sin(2 * np.pi * .23 * t + k))
            y += .25 * np.sin(4 * np.pi * f * t)
    y = lowpass(y, 1400); y *= np.minimum(1, t / .6) * np.minimum(1, (d - t) / .6)
    return y / len(ms) * .22
def bass(m, d):
    n = int(SR * d); t = np.arange(n) / SR; f = mtof(m)
    y = np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)
    return y * np.minimum(1, t / .01) * np.exp(-t / .9) * .5
def kick():
    n = int(SR * .45); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (48 + 90 * np.exp(-t * 30)) * t) * np.exp(-t / .16) * .9
def snare():
    n = int(SR * .3); t = np.arange(n) / SR
    return (bandpass(rng.standard_normal(n), 900, 5000) * np.exp(-t / .07) * .5 + np.sin(2 * np.pi * 190 * t) * np.exp(-t / .04) * .3)
def hat(open_=False):
    n = int(SR * (.25 if open_ else .06)); t = np.arange(n) / SR
    return highpass(rng.standard_normal(n), 7000) * np.exp(-t / (.09 if open_ else .015)) * .22
def flute(ms, durs, t0):
    t = t0
    for m, dd in zip(ms, durs):
        n = int(SR * dd * BEAT); tt = np.arange(n) / SR; f = mtof(m) * (1 + .006 * np.sin(2 * np.pi * 5.2 * tt) * np.minimum(1, tt / .4))
        ph = 2 * np.pi * np.cumsum(f) / SR
        y = np.sin(ph) + .15 * np.sin(2 * ph) + .25 * bandpass(rng.standard_normal(n), mtof(m) * .8, mtof(m) * 3)
        e = np.minimum(1, tt / .12) * np.minimum(1, (dd * BEAT - tt) / .15); put(y * e * .16, t, pan=.25); t += dd * BEAT

# progression (la mineur) : Fmaj7 – G6 – Em7 – Am9, une mesure chacun
PROG = [([53, 57, 60, 64], 41, [65, 69, 72, 76, 72]), ([55, 59, 62, 64], 43, [67, 71, 74, 76, 74]),
        ([52, 55, 59, 62], 40, [64, 67, 71, 74, 71]), ([57, 60, 64, 67, 71], 45, [69, 72, 76, 79, 76])]
nbars = int(np.ceil(DUR / BAR))
for b in range(nbars):
    t0 = b * BAR; ch, bs, arp = PROG[b % 4]
    put(pad(ch, BAR + .6), t0, 1.0, 0)
    put(bass(bs, BEAT * 1.6), t0, .9); put(bass(bs, BEAT * 1.2), t0 + 2.5 * BEAT, .6); put(bass(bs + 7, BEAT), t0 + 3.5 * BEAT, .45)
    # koto : arpège pincé, un peu humanisé, alterné gauche/droite
    pattern = [0, 1, 2, 3, 4, 2, 3, 1] if b % 2 == 0 else [4, 3, 2, 1, 2, 3, 0, 2]
    for k, idx in enumerate(pattern):
        if b % 4 == 3 and k in (5, 7): continue
        tt = t0 + k * BEAT / 2 + (BEAT * .06 if k % 2 else 0) + rng.uniform(-.008, .008)
        put(koto(arp[idx], 1.8, .5 + .2 * rng.random()), tt, .55 - .03 * (k % 2), pan=-.35 if k % 2 else .35)
    # batterie lo-fi (swing), absente sur la mesure 0 et sur la carte de fin
    if 1 <= b < nbars - 1:
        for k in range(8):
            tt = t0 + k * BEAT / 2 + (BEAT * .1 if k % 2 else 0)
            put(hat(k == 7), tt, .9 if k % 2 == 0 else .6, pan=.2)
        put(kick(), t0, 1); put(kick(), t0 + 2.5 * BEAT, .8)
        put(snare(), t0 + BEAT, .7, pan=-.1); put(snare(), t0 + 3 * BEAT, .7, pan=-.1)
# flûte façon shakuhachi : deux phrases seulement
flute([69, 72, 74, 76, 74, 72, 69], [1, .5, .5, 2, .5, .5, 3], 4 * BAR)
flute([76, 79, 81, 79, 76, 74, 76], [1, .5, .5, 2, .5, .5, 3], 16 * BAR)
# craquement de vinyle
cr = np.zeros(N); idx = rng.integers(0, N, 2500); cr[idx] = rng.uniform(-.6, .6, len(idx)); cr = highpass(cr, 2000) + .004 * lowpass(rng.standard_normal(N), 3000)
L += cr * .25; R += cr * .25

# couleur lo-fi : passe-bas global doux, légère saturation, fondu d'entrée et de sortie
mix = np.stack([L, R]); mix = lowpass(mix, 7500); mix = np.tanh(mix * 1.4) / 1.4
t = np.arange(N) / SR; fade = np.minimum(1, t / .4) * np.clip((DUR - t) / 2.5, 0, 1); mix *= fade
mix = mix / np.abs(mix).max() * .8
w = wave.open("music.wav", "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix.T * 32767).astype(np.int16).tobytes()); w.close(); print("music.wav", DUR, "s")
