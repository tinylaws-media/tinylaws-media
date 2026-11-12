"""Musique épique originale (synthèse, sans aucun extrait existant) calée sur la voix de Minato vs Itachi.
Ré mineur, 96 BPM : taikos, cordes en ostinato, cuivres, chœur, shamisen pincé, flûte façon shakuhachi.
Les sections suivent la vidéo (temps de la voix) et les gros coups tombent sur les tampons. Sortie : music_epic.wav."""
import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; DUR = 83.0; N = int(SR * DUR); BPM = 96; BEAT = 60 / BPM; BAR = 4 * BEAT
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N); RV = np.zeros((2, N))       # bus sec + envoi de réverbération
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, min(f, SR / 2 - 100), 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def put(sig, t, g=1.0, pan=0.0, rev=0.3):
    i = max(0, int(t * SR)); j = min(N, i + len(sig))
    if j <= i: return
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4); s = g * sig[: j - i]
    L[i:j] += l * s; R[i:j] += r * s; RV[0, i:j] += rev * l * s; RV[1, i:j] += rev * r * s
def adsr(n, a, d, s, r):
    t = np.arange(n) / SR; T = n / SR
    e = np.where(t < a, t / max(a, 1e-4), np.where(t < a + d, 1 - (1 - s) * (t - a) / max(d, 1e-4), s))
    return e * np.clip((T - t) / max(r, 1e-4), 0, 1)
def saws(f, n, voices=5, det=0.12):
    t = np.arange(n) / SR; y = np.zeros(n)
    for k in range(voices):
        fk = f * 2 ** (det * (k - (voices - 1) / 2) / 12 / max(1, (voices - 1) / 2)); ph = rng.random()
        y += 2 * ((fk * t + ph) % 1) - 1
    return y / voices

# ---- instruments
def taiko(big=1.0):
    n = int(SR * 1.4); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (52 + 70 * np.exp(-t * 25)) * t) * np.exp(-t / (0.35 * big))
    skin = bp(rng.standard_normal(n), 80, 900) * np.exp(-t / 0.06)
    return (body + 0.5 * skin) * 0.9
def rim():
    n = int(SR * .12); t = np.arange(n) / SR; return bp(rng.standard_normal(n), 1500, 6000) * np.exp(-t / .02) * .5
def strings_note(m, d, short=False):
    n = int(SR * d); y = saws(mtof(m), n, 7, 0.18); y = lp(y, 2200 if short else 1800)
    return y * (adsr(n, .01, .08, .5, .05) if short else adsr(n, .35, .2, .9, .4)) * .5
def brass(ms, d):
    n = int(SR * d); t = np.arange(n) / SR; y = sum(saws(mtof(m), n, 3, 0.08) for m in ms) / len(ms)
    k = np.minimum(1, t / .25) * np.exp(-t / 1.5)                          # le filtre s'ouvre : attaque cuivrée
    out = lp(y, 450) + (lp(y, 3000) - lp(y, 450)) * k
    return out * adsr(n, .06, .3, .8, .3) * .7
def choir(ms, d):
    n = int(SR * d); t = np.arange(n) / SR; y = np.zeros(n)
    for m in ms:
        vib = 1 + .005 * np.sin(2 * np.pi * 5 * t + rng.random() * 6)
        ph = 2 * np.pi * np.cumsum(mtof(m) * vib) / SR; y += sum(np.sin(k * ph) / k for k in range(1, 12))
    y = bp(y, 600, 900) * 1.0 + bp(y, 1000, 1300) * .6 + bp(y, 2400, 2800) * .25   # voyelle « ah »
    return y * adsr(n, .8, .3, .9, .8) * .35 / len(ms)
def shamisen(m):
    f = mtof(m); P = int(SR / f); n = int(SR * 1.0)
    exc = np.zeros(n); exc[:P] = rng.uniform(-1, 1, P); a = np.zeros(P + 2); a[0] = 1; a[P] = -.497; a[P + 1] = -.497
    from scipy.signal import lfilter
    y = lfilter([1], a, exc); y = hp(y, 300); return y / (np.abs(y).max() + 1e-9) * .45
def flute(m, d):
    n = int(SR * d); t = np.arange(n) / SR; f = mtof(m) * (1 + .007 * np.sin(2 * np.pi * 5.3 * t) * np.minimum(1, t / .5))
    ph = 2 * np.pi * np.cumsum(f) / SR; y = np.sin(ph) + .12 * np.sin(2 * ph) + .3 * bp(rng.standard_normal(n), mtof(m) * .9, mtof(m) * 3)
    return y * adsr(n, .15, .2, .85, .3) * .22
def riser(d):
    n = int(SR * d); t = np.arange(n) / SR; x = rng.standard_normal(n); y = np.zeros(n)
    for k in range(0, n, 2400):
        fc = 300 + 6000 * (k / n) ** 2; y[k:k + 2400] = bp(x[k:k + 2400 + 1], fc * .8, fc * 1.2)[:len(y[k:k + 2400])]
    return y * (t / d) ** 2 * .5
# ---- harmonie (ré mineur épique) : Dm – Bb – C – Am, une mesure chacun
PROG = [(50, [62, 65, 69]), (46, [58, 62, 65]), (48, [60, 64, 67]), (45, [57, 60, 64])]
SEC = [(0.0, 7.0, 'hook'), (7.0, 12.9, 'build'), (12.9, 42.3, 'dossiers'), (42.3, 58.7, 'toile'), (58.7, 68.1, 'verdict'),
       (68.1, 75.6, 'respect'), (75.6, 80.6, 'cta'), (80.6, 83.0, 'fin')]
def section(t):
    for a, b, s in SEC:
        if a <= t < b: return s
    return 'fin'
nb = int(DUR / BEAT) + 1
for k in range(nb):
    t = k * BEAT; s = section(t); bar = int(t / BAR); root, ch = PROG[bar % 4]; inbar = k % 4
    if s in ('dossiers', 'verdict', 'cta'):
        if inbar in (0, 2): put(taiko(), t, 1.0, -.1, .25)
        if inbar == 3: put(taiko(.7), t + BEAT / 2, .7, .1, .25)
        put(rim(), t + BEAT / 2, .5, .3, .1)
        for e in range(2):                                         # cordes en croches
            put(strings_note(root + (12 if e else 0) + (7 if inbar == 3 and e else 0), BEAT / 2 * .95, True), t + e * BEAT / 2, .55, -.4, .2)
    if s == 'build':
        for e in range(2): put(strings_note(root + 12 * e, BEAT / 2 * .9, True), t + e * BEAT / 2, .35 + .4 * (t - 7) / 6, -.3, .2)
        if inbar == 0: put(taiko(.8), t, .6 + .4 * (t - 7) / 6, 0, .3)
    if s == 'toile':
        if inbar == 0: put(taiko(1.2), t, .55, 0, .5)
        put(shamisen(ch[(k * 2) % 3] + 12), t, .35, .35, .3)
    if s in ('dossiers', 'cta') and k % 2 == 0: put(shamisen(ch[(k // 2) % 3] + 12), t + BEAT * .5, .4, .4, .25)
for bar in range(int(DUR / BAR) + 1):
    t = bar * BAR; s = section(t + .01); root, ch = PROG[bar % 4]
    if s in ('dossiers', 'verdict', 'toile', 'cta', 'build'):
        put(strings_note(root - 12, BAR, False), t, .6, 0, .3)               # basses tenues
    if s in ('dossiers', 'verdict', 'cta') and bar % 2 == 0: put(brass([root, root + 7, root + 12], BAR * 1.6), t, .55, .15, .35)
    if s in ('toile', 'verdict', 'respect'): put(choir(ch, BAR + .5), t, .9 if s != 'respect' else .6, 0, .6)
    if s == 'hook': put(choir([50, 57], BAR + .5), t, .5, 0, .6)
# phrases de flûte (respect et dossiers)
for t0, mel in [(68.3, [74, 72, 69, 67, 69]), (20.0, [69, 72, 74, 77, 74]), (33.0, [77, 74, 72, 69, 67])]:
    tt = t0
    for m, d in zip(mel, [1, .5, .5, 1.5, 2]):
        put(flute(m, d * BEAT), tt, 1.0, .25, .5); tt += d * BEAT
# accroche : coups sur les tampons de la voix ; montée vers le verdict ; gros coups
for t in (0.3, 1.2, 3.5, 6.1): put(taiko(1.4), t, 1.1, 0, .5); put(brass([38, 45], 1.2), t, .5, 0, .4)
put(riser(5.0), 53.6, .9, 0, .4); put(riser(2.0), 61.3, .7, 0, .4)
for t in (58.7, 63.3, 69.9, 75.9): put(taiko(1.8), t, 1.3, 0, .6); put(brass([38, 45, 50], 2.0), t, .8, 0, .5)
put(taiko(2.2), 80.6, 1.4, 0, .8); put(choir([50, 57, 62, 65], 3.0), 80.6, 1.0, 0, .8)

# réverbération de salle (réponse impulsionnelle synthétique, 2,4 s)
ir_n = int(SR * 2.4); ti = np.arange(ir_n) / SR
IR = [lp(rng.standard_normal(ir_n), 6000) * np.exp(-ti / .55) for _ in range(2)]
wet = np.stack([fftconvolve(RV[c], IR[c])[:N] for c in range(2)]) * .08
mix = np.stack([L, R]) + wet
mix = hp(mix, 30); mix = np.tanh(mix * 1.2) / 1.2
t = np.arange(N) / SR; mix *= np.minimum(1, t / .05) * np.clip((DUR - t) / 1.2, 0, 1)
mix = mix / np.abs(mix).max() * .85
w = wave.open("music_epic.wav", "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix.T * 32767).astype(np.int16).tobytes()); w.close(); print("music_epic.wav", DUR, "s")
