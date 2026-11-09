"""Demon Slayer (Kimetsu no Yaiba) fight database (canon: Gotōge's manga ch. 1-205 and official fanbooks only for
stated results; no anime-only fights, no movies beyond what the manga shows).
Time axis t = years since the massacre of Tanjiro's family (= 0); Final Selection about 2.0. Flashbacks negative
(Yoriichi vs Muzan about -400). fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[...], tb=[...],
note="... (ch. N)", flags="i"/"?"/"e"). Tags: malade, epuise, retenue, protege, surprise, prepa, boost (temporary
power: Mark, Transparent World, red blade, Nezuko's awakening...), contre, age, plus extras. "e" = partners sharing credit.
Tier priors: 0 civil, 1 pourfendeur débutant, 2 pourfendeur confirmé, 3 démon des Lunes inférieures / Tsuguko,
4 Pilier, 5 Lunes supérieures 4 à 6, 6 Lunes supérieures 1 à 3, 7 Muzan / Yoriichi.
"""
import glob
import importlib.util
import os

ARCS = [
    ("sengoku", "Ère Sengoku (Yoriichi)", -400.0),
    ("avant", "Avant l'histoire", -5.0),
    ("selection", "Sélection finale", 2.0),
    ("asakusa", "Asakusa et le manoir Tsuzumi", 2.1),
    ("natagumo", "Mont Natagumo", 2.2),
    ("mugen", "Train de l'infini", 2.35),
    ("yuukaku", "Quartier des plaisirs", 2.5),
    ("forgerons", "Village des forgerons", 2.6),
    ("entrainement", "Entraînement des Piliers", 2.7),
    ("chateau", "Château de l'infini", 2.8),
    ("aube", "Aube contre Muzan", 2.81),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
REVIVE = {}
EXTRA_TAGS = {"marque": (1.2, 0.8)}
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


CHECKS = [("yoriichi", "sengoku", "muzan", "sengoku"), ("rengoku", "mugen", "akaza", "mugen"), ("gyomei", "chateau", "kokushibo", "chateau")]
