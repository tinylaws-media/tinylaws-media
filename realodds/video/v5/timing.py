"""Calage de la v4 (temps « ancien ») sur la voix enregistrée (temps « nouveau »).
Ancres (nouveau, ancien) : débuts de phrase repérés par transcription + pauses. Dans un segment rallongé,
la première seconde joue à vitesse réelle (entrées de cases nettes) puis le reste est étiré."""
import json
ANCH = [(0.0, 0.0), (0.3, 0.15), (1.2, 1.0), (3.5, 3.5), (6.1, 5.4), (7.0, 6.9), (12.9, 11.7), (17.85, 14.7), (20.85, 17.7),
        (24.0, 21.1), (28.5, 25.1), (33.7, 28.7), (37.55, 32.5), (42.3, 36.1), (49.6, 40.6), (53.5, 45.1), (58.7, 49.6),
        (63.3, 51.8), (68.1, 55.1), (69.9, 57.3), (70.7, 59.1), (75.6, 62.9), (75.9, 64.2), (80.6, 67.5), (83.0, 70.0)]
def pts():
    P = []
    for (n0, o0), (n1, o1) in zip(ANCH, ANCH[1:]):
        P.append((n0, o0))
        dn, do = n1 - n0, o1 - o0
        if dn > do + 0.3 and do > 1.2: P.append((n0 + 1.0, o0 + 1.0))
    P.append(ANCH[-1]); return P
P = pts()
def interp(v, A, B):
    for (a0, b0), (a1, b1) in zip(zip(A, B), zip(A[1:], B[1:])):
        if v <= a1: return b0 + (b1 - b0) * (v - a0) / (a1 - a0)
    return B[-1]
N = [p[0] for p in P]; O = [p[1] for p in P]
new2old = lambda t: interp(t, N, O); old2new = lambda t: interp(t, O, N)
if __name__ == "__main__":
    json.dump(dict(N=N, O=O), open("warp.json", "w"))
    print(len(P), "points")
