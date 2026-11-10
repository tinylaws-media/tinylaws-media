"""My Hero Academia (Boku no Hero Academia) fight database (canon: Horikoshi's manga ch. 1-430 incl. the epilogue,
official Ultra Analysis / Ultra Archive guides and author statements for stated results; no anime-only fights, no movies,
no Vigilantes spin-off).
Time axis t = years since chapter 1 (Izuku meets All Might, ten months before the UA entrance exam = 0); entrance exam
0.8, school year 1 starts 0.95, Paranormal Liberation War 1.9, Final War 2.3. Flashbacks negative (Nana Shimura's death
about -30, All Might's first duel with All For One about -6).
fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[...], tb=[...], note="... (ch. N)", flags="i"/"?"/"e").
Tags (external circumstances only): malade, epuise, retenue, protege, surprise, prepa (traps, sedatives, plans set up in
advance), aide (borrowed external power: Eri's Rewind for Deku, La Brava's Love for Gentle).
One For All percentages, Full Cowl, the vestiges' Quirks (Blackwhip, Float, Danger Sense, Smokescreen, Fa Jin),
Gearshift, Shigaraki's Decay awakening and Ujiko's upgrade, Phosphor, Toga's awakening are skills: dated JUMPS,
never fight tags. "e" = partners sharing credit.
Tier priors: 0 civil, 1 élève débutant / petit vilain, 2 élève confirmé / héros pro modeste, 3 héros pro confirmé / Big 3 /
vilain dangereux, 4 héros du top 10 / Nomu supérieur, 5 numéros 1-2 du classement (Endeavor, Hawks) / Gigantomachia /
Shigaraki éveillé, 6 All Might déclinant / Star and Stripe / All For One, 7 All Might à son apogée / Shigaraki fusionné
à All For One / Deku final.
"""
import glob
import importlib.util
import os

ARCS = [
    ("nana", "Flash-back : la mort de Nana Shimura", -30.0),
    ("apogee", "Flash-back : All Might contre All For One, il y a six ans", -6.0),
    ("debut", "Le vilain de boue et l'examen d'entrée", 0.5),
    ("usj", "Rentrée et attaque de l'USJ", 0.96),
    ("festival", "Festival sportif", 1.0),
    ("stain", "Stages et Tueur de héros Stain", 1.05),
    ("examens", "Examens de fin de semestre", 1.2),
    ("camp", "Camp d'entraînement en forêt", 1.28),
    ("kamino", "Kamino : All Might contre All For One", 1.31),
    ("licence", "Licence provisoire et Deku contre Kacchan", 1.41),
    ("overhaul", "Stages et Overhaul (Shie Hassaikai)", 1.5),
    ("festival_ecole", "Festival culturel et Gentle Criminal", 1.6),
    ("hood", "Endeavor contre le Nomu encapuchonné", 1.65),
    ("classeb", "Entraînement commun A contre B", 1.7),
    ("mla", "Armée de libération du Méta (Deika)", 1.73),
    ("agence", "Stage chez Endeavor", 1.8),
    ("guerre", "Guerre de libération du Paranormal", 1.9),
    ("sombre", "Deku héros sombre", 2.05),
    ("star", "Star and Stripe", 2.2),
    ("final", "Guerre finale", 2.3),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
REVIVE = {}   # Bakugo : cœur arrêté puis relancé dans la même bataille (ch. 362-369, 403) : pas de mort codée
EXTRA_TAGS = {"aide": (0.7, 0.7)}   # aide : pouvoir externe prêté (Rewind d'Eri pour Deku, Love de La Brava pour Gentle)
# vétérans dont la force ne bouge plus que par des sauts datés (âge, blessures)
SLOW = {"all_might", "afo", "gran_torino"}
BOOK_TIMES = {}


def fight(t, arc, a, b, res, m=2, ta=(), tb=(), note="", flags=""):
    a = [a] if isinstance(a, str) else list(a)
    b = [b] if isinstance(b, str) else list(b)
    F.append(dict(t=t, arc=arc, a=a, b=b, res=res, m=m, ta=list(ta), tb=list(tb), note=note, flags=flags))


# part_*.py each defines CHARS_PART, GENERIC_PART, JUMPS_PART and calls fight()
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


CHECKS = [("all_might", "apogee", "afo", "apogee"), ("all_might", "kamino", "afo", "kamino"),
          ("endeavor", "hood", "hood", "hood"), ("deku", "final", "shigaraki", "final"),
          ("star", "star", "shigaraki", "star"), ("bakugo", "final", "afo", "final")]
