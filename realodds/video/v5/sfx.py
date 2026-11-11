"""Bruitages synthétisés (aucun sample externe), placés sur les événements de l'animation puis convertis en temps voix."""
import numpy as np, wave
from timing import old2new
SR = 48000; DUR = 83.0
out = np.zeros(int(SR * DUR)); rng = np.random.default_rng(3)

def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR; e = np.minimum(1, t / a) * np.exp(-t / r); return e
from scipy.signal import lfilter
def lp(x, k):  # passe-bas du 1er ordre
    c = np.exp(-2 * np.pi * k / SR); return lfilter([1 - c], [1, -c], x)
def bp(x, lo, hi): return lp(x, hi) - lp(x, lo)
def add(t_old, sig, g=1.0):
    i = int(old2new(t_old) * SR); j = min(len(out), i + len(sig)); out[i:j] += g * sig[: j - i]

def whoosh(d=0.35, up=True):
    n = int(SR * d); t = np.arange(n) / SR; x = rng.standard_normal(n)
    shape = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return (bp(x, 500, 5000) if up else bp(x, 300, 2500)) * shape * 0.5
def boom(d=1.2, f0=70):
    n = int(SR * d); t = np.arange(n) / SR; f = f0 * np.exp(-t * 2.2) + 32
    ph = 2 * np.pi * np.cumsum(f) / SR; y = np.sin(ph) * env(n, .003, .35) + 0.25 * lp(rng.standard_normal(n), 300) * env(n, .002, .12)
    return y * 0.9
def stamp():
    n = int(SR * .35); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (140 * np.exp(-t * 18) + 60) * t) * env(n, .001, .07)
    click = bp(rng.standard_normal(n), 1500, 7000) * env(n, .0005, .012)
    return 0.8 * thump + 0.5 * click
def shing():
    n = int(SR * .9); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(2637, 1), (3951, .6), (5274, .35), (7040, .2)]) * env(n, .002, .25)
    return 0.25 * y + 0.3 * whoosh(.25)[: n] if n <= int(SR * .25) else 0.25 * y + np.pad(0.3 * whoosh(.25), (0, n - int(SR * .25)))
def slash():
    n = int(SR * .22); t = np.arange(n) / SR; x = bp(rng.standard_normal(n), 2000, 9000)
    return x * np.sin(np.pi * t / .22) ** 3 * 0.6
def pop():
    n = int(SR * .12); t = np.arange(n) / SR; return np.sin(2 * np.pi * (500 + 900 * t / .12) * t) * env(n, .001, .04) * .45
def tick(f=1800):
    n = int(SR * .03); t = np.arange(n) / SR; return np.sin(2 * np.pi * f * t) * env(n, .0005, .008) * .35
def drop():
    n = int(SR * .06); t = np.arange(n) / SR; return np.sin(2 * np.pi * (900 - 4000 * t) * t) * env(n, .0005, .02) * .25
def shimmer(d=3.6):
    n = int(SR * d); t = np.arange(n) / SR; y = np.zeros(n)
    for k, f in enumerate([523, 659, 784, 1047, 1319]):
        y += np.sin(2 * np.pi * f * t + k) * (0.5 + 0.5 * np.sin(2 * np.pi * (3 + k) * t))
    return y * np.minimum(1, t / .8) * np.minimum(1, (d - t) / .6) * .06
def drone(d, f=55):
    n = int(SR * d); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.5 * t) + .3 * lp(rng.standard_normal(n), 200)
    return y * np.minimum(1, t / .5) * np.minimum(1, (d - t) / .5) * .18
def brush(d=1.4):
    n = int(SR * d); t = np.arange(n) / SR; return bp(rng.standard_normal(n), 800, 3500) * np.sin(np.pi * t / d) * .25

def slam(big=True):
    # arrivée d'une image : souffle court qui accélère, puis claque de papier + coup sourd
    pre = int(SR * .16); n = int(SR * .45); y = np.zeros(pre + n)
    t = np.arange(pre) / SR; y[:pre] = bp(rng.standard_normal(pre), 700, 6000) * (t / .16) ** 2 * .45
    tt = np.arange(n) / SR
    thump = np.sin(2 * np.pi * ((70 if big else 120) + 120 * np.exp(-tt * 40)) * tt) * env(n, .001, .09 if big else .05)
    slap = bp(rng.standard_normal(n), 900, 5000) * env(n, .0005, .025)
    y[pre:] += (.9 if big else .5) * thump + .6 * slap
    return y
def land(t, big=True, g=1.0): add(t - .16, slam(big), g)
def flick():
    n = int(SR * .14); t = np.arange(n) / SR; return bp(rng.standard_normal(n), 2000, 8000) * np.sin(np.pi * t / .14) ** 2 * .35

# ---- arrivées d'images (chaque case ou image qui entre a son bruitage)
land(.4); land(1.85, False); land(2.45, False); land(3.95); land(4.75, False); land(55.2); land(59.25, False, .8); land(63.0)
for t0, nf in [(11.7, 1), (14.7, 1), (17.7, 1), (21.1, 1), (25.1, 2), (28.7, 1), (32.5, 2)]:
    land(t0 + .3); land(t0 + .45, False)
    for i in range(nf): add(t0 + .55 + i * .12, flick(), .9)
import json, math
WEBN = json.load(open('../v4/web.json'))['nodes']
PORTS = ['kakashi','obito','a4','killer_b','madara','naruto','sasuke','jiraiya','orochimaru','nagato','kisame','hashirama','gai','tsunade']
land(36.3, True, .8)
for n in PORTS:
    if n in WEBN: px, py = WEBN[n][:2]; add(36.4 + math.hypot(px - 540, py - 930) / 700 * 1.6 + .12, pop(), .6)

# ---- accroche
add(0.05, boom(1.6, 55), .8); add(0.1, drone(3.3, 41), 1)
add(1.0, stamp(), 1); add(1.0, boom(.8, 90), .5)
for i in range(3): add(1.9 + i * .35, tick(1200 + 300 * i), 1)
add(3.5, shing(), .9); add(3.6, boom(1.0, 80), .6)
for s in (5.0, 5.25, 5.5): add(s, whoosh(.15), .5)
add(5.4, stamp(), 1.1)
# ---- méthode
add(6.85, whoosh(.4), .7)
for k in range(60): add(7.1 + k * .048, tick(2200 + 400 * (k % 3)), .5)
for s in (9.4, 10.2, 10.9): add(s, stamp(), .8)
# ---- dossiers
for t0, loss in [(11.7, 0), (14.7, 0), (17.7, 0), (21.1, 1), (25.1, 0), (28.7, 0), (32.5, 1)]:
    add(t0 + .55, slash(), .8)
    add(t0 + .8, stamp(), 1.0); add(t0 + .8, boom(.9, 45 if loss else 85), .45 if loss else .4)
    add(t0 + 1.0, tick(900 if loss else 1600), .8)
# ---- toile
add(36.0, whoosh(.5), .7); add(36.1, drone(13.3, 49), .9)
for k in range(40): add(36.3 + k * .07, tick(2600 + 200 * (k % 4)), .25)
add(40.9, shimmer(4.2), 1)
for h in range(7): add(41.0 + h * .62, tick(1000 + 220 * h), .9); add(41.0 + h * .62, tick(1320 + 220 * h), .6)
for s in (45.4, 46.4, 47.4): add(s, stamp(), .85)
# ---- verdict
add(49.5, whoosh(.45), .7)
r = np.random.default_rng(5)
for i in range(300):
    if r.random() < .45: add(49.9 + i * .009 + .4, drop(), .5)
add(51.8, stamp(), 1.1); add(51.8, boom(1.4, 70), .8)
add(55.0, whoosh(.4), .7); add(56.6, whoosh(.5, False), .6); add(57.3, stamp(), 1.1); add(57.3, boom(1.0, 85), .6)
add(59.0, whoosh(.4), .6); add(59.3, brush(1.4), 1); add(60.2, stamp(), .9)
add(62.85, whoosh(.4), .7); add(64.2, stamp(), 1.0); add(64.2, boom(1.0, 80), .6); add(65.0, pop(), 1)
add(67.5, boom(2.4, 45), 1.0)

out = out / max(1e-9, np.abs(out).max()) * 0.7
w = wave.open("sfx.wav", "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print("sfx.wav", DUR, "s")
