"""Garantit que les bruitages restent sous la voix : sur chaque fenêtre de 50 ms où la voix est présente,
les bruitages sont ramenés au moins 6 dB sous la voix (gain lissé, avec anticipation de 30 ms)."""
import numpy as np, wave, sys
from scipy.ndimage import maximum_filter1d, uniform_filter1d
def rd(f):
    w = wave.open(f); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    return a.reshape(-1, w.getnchannels()).mean(1), w.getframerate()
s, sr = rd('sfx.wav'); v, _ = rd('../audio/voix_propre.wav'); G = float(sys.argv[1]) if len(sys.argv) > 1 else 1.6
s = s * G; n = len(s); v = np.pad(v, (0, max(0, n - len(v))))[:n]
win = int(sr * .05)
rms = lambda x: np.sqrt(uniform_filter1d(x ** 2, win) + 1e-12)
rv, rs = rms(v), rms(s)
speaking = uniform_filter1d((rv > 10 ** (-45 / 20)).astype(float), int(sr * .12)) > 0
target = np.where(speaking, rv * 10 ** (-6 / 20), np.inf)
g = np.minimum(1.0, target / rs)
g = -maximum_filter1d(-g, int(sr * .03))          # anticipation : on prend le gain mini sur 30 ms
g = uniform_filter1d(g, int(sr * .02))              # lissage
out = s * g
pk = 10 ** (-14 / 20); out = np.clip(out, -pk, pk) if np.abs(out).max() > pk else out
w = wave.open('sfx_ducked.wav', 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
h = int(sr * .1); S = np.array([np.sqrt((out[i:i+h]**2).mean()) for i in range(0, n - h, h)]); V = np.array([np.sqrt((v[i:i+h]**2).mean()) for i in range(0, n - h, h)])
sp = V > .02; db = lambda x: 20 * np.log10(x + 1e-9)
print('fenêtres où les bruitages >= voix :', int(((db(S) >= db(V)) & sp).sum()), '/', int(sp.sum()), '| max pendant la voix', round(db(S[sp]).max(), 1), 'dBFS')
