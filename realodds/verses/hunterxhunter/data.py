"""Hunter x Hunter fight database (canon: Togashi's manga, chapters to the latest released; official guidebook
statements only for stated results; no anime-only fights or movies).
Time axis t = years since the 287th Hunter Exam (= 0). Flashbacks are negative.
fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[...], tb=[...], note="... (ch. N)", flags="i"/"?"/"e")
Tags: malade, epuise, retenue, protege, surprise, prepa (conditions/vows set in advance, traps), boost (temporary
power: Gon's adult transformation, Killua's Godspeed...), contre (ability counters the opponent), age, plus extras.
Flag "e" = partners who carried a fight together (credit shared evenly).
Tier priors: 0 civil, 1 candidat Hunter, 2 débutant en Nen, 3 utilisateur de Nen confirmé, 4 Hunter pro fort / membre de
la Brigade fantôme, 5 Hisoka / Chrollo / Zoldyck adultes, 6 Gardes royaux / Netero âgé, 7 Meruem / Netero à son apogée.
"""
import glob
import importlib.util
import os

ARCS = [
    ("avant", "Avant l'histoire", -10.0),
    ("examen", "Examen Hunter", 0.0),
    ("zoldyck", "Famille Zoldyck", 0.05),
    ("arene", "Tour céleste", 0.15),
    ("yorknew", "York New City", 0.5),
    ("greedisland", "Greed Island", 0.6),
    ("fourmis", "Fourmis-chimères", 0.8),
    ("election", "Élection du président", 1.1),
    ("succession", "Guerre de succession", 1.3),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
REVIVE = {}
EXTRA_TAGS = {"tenacite": (1.5, 1.0)}
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


CHECKS = [("netero", "fourmis", "meruem", "fourmis"), ("hisoka", "succession", "chrollo", "succession"), ("gon", "fourmis", "pitou", "fourmis")]
