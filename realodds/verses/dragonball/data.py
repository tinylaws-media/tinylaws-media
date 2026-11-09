"""Dragon Ball fight database (canon: Toriyama's Dragon Ball manga and the Dragon Ball Super manga by Toyotarō,
supervised by Toriyama; official guidebooks only for stated results. No GT, no anime filler, no movie-only fights
unless the Super manga adapted them).

Time axis t = the in-universe Age year (Goku born Age 737, story starts Age 749).
fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[tags], tb=[tags], note="... (ch. N)", flags="i"/"?")
Tags: malade, epuise, retenue, protege, surprise, prepa, boost (Kaiōken, temporary form, potion), contre, age,
ultra (Ultra Instinct / Beast-type peak state used in a fight). A fusion (gogeta, vegito, gotenks) is its own character.
Permanent new forms (first Super Saiyan, SSJ2, Ultra Instinct mastery, Beast…) are JUMPS.
Tier priors (status at first fight): 0 humain ordinaire, 1 artiste martial, 2 Tortue Géniale / Tao Pai Pai,
3 Piccolo Daimaō / Tenshinhan adulte, 4 Saiyans à leur arrivée sur Terre, 5 Freezer, 6 Cell parfait / SSJ2,
7 Majin Buu / SSJ3, 8 dieux de la destruction / Super Saiyan God, 9 Jiren / Ultra Instinct, 10 Zeno, anges.
"""
import glob
import importlib.util
import os

ARCS = [
    ("avant", "Avant l'histoire (Bardock, Freezer, Saiyans)", 737.0),
    ("pilaf", "Pilaf et le 21e Championnat", 749.0),
    ("ruban", "Armée du Ruban rouge", 750.0),
    ("tournoi22", "22e Championnat", 753.0),
    ("daimao", "Piccolo Daimaō", 753.5),
    ("tournoi23", "23e Championnat (Piccolo junior)", 756.0),
    ("saiyan", "Arrivée des Saiyans", 762.0),
    ("namek", "Namek et Freezer", 762.8),
    ("cyborgs", "Cyborgs et Cell", 767.0),
    ("cellgame", "Cell Game", 767.5),
    ("buu", "Majin Buu", 774.0),
    ("dieux", "Beerus et la résurrection de Freezer", 778.0),
    ("univ6", "Tournoi contre l'univers 6 et Goku Black", 779.5),
    ("tdp", "Tournoi du Pouvoir", 780.0),
    ("moro", "Moro", 780.5),
    ("granolah", "Granolah", 781.0),
    ("superhero", "Super Hero et après", 781.5),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
REVIVE = {}
EXTRA_TAGS = {"ultra": (2.0, 1.0)}
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


CHECKS = [("goku", "tdp", "jiren", "tdp"), ("vegeta", "granolah", "goku", "granolah"), ("gohan", "cellgame", "cell", "cellgame")]
