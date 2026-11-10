"""Chainsaw Man fight database (canon: Fujimoto's manga, Part 1 ch. 1-97 and Part 2 ch. 98-232; the series ended with
ch. 232 on 25 March 2026, no Part 3 announced as of November 2026). No anime-only scenes, no film additions.
Time axis t = years since Denji joins Public Safety (ch. 1-2 = 0). Part 1 runs 0.0-0.85; Part 2 (Academy Saga) starts
about a year later (1.5-1.85). The ch. 232 epilogue happens in the world rewritten by Pochita (t = 2.5).
fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[...], tb=[...], note="... (ch. N)", flags="i"/"?"/"e")
Tags (external circumstances only): malade, epuise, retenue, protege, surprise, prepa (traps, prior plans, tricks),
contre, aide (borrowed contract power that is not the fighter's own: Makima's immortality contract with the Prime
Minister, which sends her wounds to random Japanese citizens; sacrifices of prisoners lent by the government).
A character's own devil contracts and hybrid forms (Aki's Fox, Curse and Future, Santa Claus's contract with Darkness,
Yoru's children Tank and Gun, the return of nuclear weapons, Denji Man) are dated JUMPS, never fight tags.
Pochita taking control of Denji's body (true / black Chainsaw Man) is a separate character "pochita".
Tier priors: 0 civil, 1 agent humain sans contrat, 2 chasseur de démons / démon mineur, 3 hybride ou démon notable
(Katana Man, Chauve-souris), 4 hybride d'élite / démon dangereux (Reze, Santa Claus, Kishibe, Quanxi),
5 démon de premier plan (Démon du Fusil, Démon de l'Éternité au sommet ?), 6 démons primordiaux et Cavaliers
(Ténèbres, Chute, Vieillissement, Contrôle), 7 Pochita au sommet / Cavaliers au sommet.
"""
import glob
import importlib.util
import os

ARCS = [
    ("debut", "Débuts de Denji (Zombie, Chauve-souris)", 0.0),
    ("eternite", "Démon de l'Éternité (hôtel)", 0.1),
    ("katana", "Katana Man et entraînement de Kishibe", 0.2),
    ("reze", "Reze, la fille bombe", 0.4),
    ("assassins", "Assassins internationaux", 0.6),
    ("fusil", "Démon du Fusil", 0.75),
    ("controle", "Démon du Contrôle (fin de la partie 1)", 0.8),
    ("justice", "Académie : Asa, Yoru et la Justice", 1.5),
    ("chute", "Aquarium et Démon de la Chute", 1.55),
    ("eglise", "Église de Chainsaw Man", 1.6),
    ("evasion", "Évasion et Chainsaw Man noir", 1.65),
    ("vieillesse", "Monde du Démon du Vieillissement", 1.7),
    ("mort", "Démon de la Mort et retour de la Chute", 1.75),
    ("guerre", "Guerre : Yoru contre Chainsaw Man", 1.8),
    ("epilogue", "Épilogue : le monde réécrit (ch. 232)", 2.5),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
REVIVE = {}
# aide : pouvoir prêté par un contrat extérieur au combattant (immortalité de Makima liée au Premier ministre,
# prisonniers sacrifiés fournis par le gouvernement)
EXTRA_TAGS = {"aide": (0.7, 0.7)}
SLOW = {"kishibe"}   # vétéran d'une cinquantaine d'années : changements par sauts datés seulement
BOOK_TIMES = {}


def fight(t, arc, a, b, res, m=2, ta=(), tb=(), note="", flags=""):
    a = [a] if isinstance(a, str) else list(a)
    b = [b] if isinstance(b, str) else list(b)
    F.append(dict(t=t, arc=arc, a=a, b=b, res=res, m=m, ta=list(ta), tb=list(tb), note=note, flags=flags))


# parts: part_*.py each defines CHARS_PART, GENERIC_PART, JUMPS_PART and calls fight()
_here = os.path.dirname(os.path.abspath(__file__))
for _p in sorted(glob.glob(os.path.join(_here, "part_*.py"))):
    _spec = importlib.util.spec_from_file_location(os.path.basename(_p)[:-3], _p)
    _m = importlib.util.module_from_spec(_spec)
    _m.fight = fight
    _spec.loader.exec_module(_m)
    for _k, _v in getattr(_m, "CHARS_PART", {}).items():
        CHARS.setdefault(_k, _v)
    CHARS.update(getattr(_m, "CHARS_FIX", {}))   # corrections d'une partie sur un personnage déclaré plus tôt
    REVIVE.update(getattr(_m, "REVIVE_PART", {}))
    GENERIC |= set(getattr(_m, "GENERIC_PART", set()))
    JUMPS += list(getattr(_m, "JUMPS_PART", []))


CHECKS = [("makima", "controle", "pochita", "controle"), ("kishibe", "katana", "denji", "katana"),
          ("yoru", "guerre", "pochita", "guerre"), ("quanxi", "assassins", "kishibe", "katana"),
          ("reze", "reze", "katana_man", "katana")]
