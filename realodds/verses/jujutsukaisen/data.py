"""Jujutsu Kaisen fight database (canon: Akutami's manga, ch. 0-271, plus Jujutsu Kaisen 0; official fanbook
statements only for stated results; no anime-only fights).
Time axis t = years since Yuji eats Sukuna's finger (June 2018 = 0). Flashbacks negative (Gojo vs Toji 2006 = -12,
Heian era about -1000). fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[...], tb=[...], note="... (ch. N)",
flags="i"/"?"/"e"). Tags: malade, epuise, retenue, protege, surprise, prepa (binding vows, traps), boost (temporary
power: Black Flash streak, Sukuna's control...), contre, age, plus extras below. "e" = partners sharing credit.
Sukuna in Yuji's body, in Megumi's body and in his true form are one id "sukuna" with JUMPS; Yuji's own fights are "yuji".
Tier priors: 0 civil, 1 exorciste de grade 4, 2 grade 2, 3 grade 1, 4 grade spécial humain (Yuta, Geto, Kenjaku),
5 fléau de catégorie spéciale de haut niveau, 6 Sukuna partiel / Toji, 7 Gojo, Sukuna à pleine puissance.
"""
import glob
import importlib.util
import os

ARCS = [
    ("heian", "Ère Heian", -1000.0),
    ("passe", "Passé de Gojo et Geto", -12.0),
    ("jjk0", "Jujutsu Kaisen 0", -1.0),
    ("debut", "Débuts de Yuji", 0.0),
    ("kyoto", "Rencontre d'échange avec Kyoto", 0.25),
    ("bouddha", "Peinture de la mort", 0.3),
    ("shibuya", "Incident de Shibuya", 0.35),
    ("culling", "Jeu d'abattage", 0.45),
    ("shinjuku", "Bataille de Shinjuku", 0.6),
    ("modulo", "Jujutsu Kaisen Modulo (2086)", 68.4),   # audit : 68.0→68.4, sinon les personnages de Modulo (1er combat 68.4) n'avaient aucun nœud affiché   # suite officielle (Akutami / Iwasaki, WSJ 2025-2026)
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
REVIVE = {}
EXTRA_TAGS = {"domaine": (1.0, 0.8), "emprunt": (1.0, 0.7)}   # emprunt : pouvoir/corps d'autrui (Yuta dans le corps de Gojo), pas la force propre
BOOK_TIMES = {}


def fight(t, arc, a, b, res, m=2, ta=(), tb=(), note="", flags=""):
    a = [a] if isinstance(a, str) else list(a)
    b = [b] if isinstance(b, str) else list(b)
    F.append(dict(t=t, arc=arc, a=a, b=b, res=res, m=m, ta=list(ta), tb=list(tb), note=note, flags=flags))


# parts written by the research agents: part_*.py each defines CHARS_PART, GENERIC_PART, JUMPS_PART and calls fight()
_here = os.path.dirname(os.path.abspath(__file__))
for _p in sorted(glob.glob(os.path.join(_here, "part_*.py"))):
    _spec = importlib.util.spec_from_file_location(os.path.basename(_p)[:-3], _p)
    _m = importlib.util.module_from_spec(_spec)
    _m.fight = fight
    _spec.loader.exec_module(_m)
    for _k, _v in getattr(_m, "CHARS_PART", {}).items():
        CHARS.setdefault(_k, _v)
    GENERIC |= set(getattr(_m, "GENERIC_PART", set()))
    JUMPS += list(getattr(_m, "JUMPS_PART", []))


CHECKS = [("gojo", "shinjuku", "sukuna", "shinjuku"), ("yuta", "culling", "geto", "jjk0"), ("toji", "passe", "gojo", "passe")]
