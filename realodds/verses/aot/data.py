"""Attack on Titan (L'Attaque des Titans) fight database (canon: Isayama's manga ch. 1-139, revised final pages included,
and the official guidebooks for stated facts; no anime-only scenes, no OAD, no spin-offs such as « No Regrets »).
Time axis t = years since the fall of Wall Maria (year 845 = 0). Trost 850 = 5.0, retaking of Wall Maria 5.8,
Mid-East war / Fort Slava 8.9, raid on Liberio 9.0, war for Paradis 9.1, Rumbling 9.2, Battle of Heaven and Earth 9.3.
Flashbacks are negative (Kenny vs Uri about -24, Kruger about -12, Mikasa's kidnapping -1).
fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[...], tb=[...], note="... (ch. N)", flags="i"/"?"/"e").
Tags (external circumstances only): malade, epuise, retenue, protege, surprise, prepa (traps, prepared plans, barrels),
aide (power lent by someone else: the Coordinate through Dina's royal blood, past holders freed by Ymir),
lances (thunder spears, anti-Armored weapons). Titan shifting, hardening, War Hammer, Founding Titan, Colossal
inheritance and Ackerman awakenings are part of the character's strength: dated JUMPS, never fight tags.
A shifter's human-form fights use the same id (his strength at that time includes his Titan).
Tier priors: 0 civil / enfant, 1 recrue, soldat ordinaire, Titan pur, 2 soldat aguerri du Bataillon, 3 élite
(escouade Livaï, Mike), Titan de soutien débutant, 4 Mikasa adulte, Titans Mâchoire / Charrette, Kenny,
5 Titans de combat (Cuirassé, Féminin, Colossal, Bestial, Marteau d'armes), 6 Livaï, Uri Reiss, 8+ Titan Originel du Grondement.
"""
import glob
import importlib.util
import os

ARCS = [
    ("kenny", "Jeunesse de Kenny l'Éventreur", -24.0),
    ("hibou", "Grisha et le Hibou", -12.0),
    ("avant", "Enfance à Shiganshina", -1.0),
    ("chute", "Chute du mur Maria", -0.02),
    ("entrainement", "104e brigade d'entraînement", 4.0),
    ("trost", "Bataille de Trost", 5.0),
    ("feminin", "57e expédition et Titan Féminin", 5.1),
    ("stohess", "District de Stohess", 5.15),
    ("utgard", "Mur Rose et château d'Utgard", 5.2),
    ("rose", "Clash des Titans", 5.21),
    ("insurrection", "Insurrection", 5.4),
    ("shiganshina", "Reconquête du mur Maria", 5.8),
    ("mahr", "Guerre de Mahr (fort Slava)", 8.9),
    ("liberio", "Raid sur Liberio", 9.0),
    ("paradis", "Guerre pour Paradis", 9.1),
    ("grondement", "Le Grondement", 9.2),
    ("ciel_terre", "Bataille du Ciel et de la Terre", 9.3),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
REVIVE = {}
# aide : pouvoir externe prêté ; lances : lances foudroyantes (armement anti-Cuirassé), circonstance d'équipement
EXTRA_TAGS = {"aide": (0.7, 0.7), "lances": (1.2, 0.6)}
# vétérans dont la force ne bouge plus que par des sauts datés
SLOW = {"levi", "kenny", "uri", "grisha", "kruger", "magath", "mike", "erwin", "hange"}
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
    GENERIC |= set(getattr(_m, "GENERIC_PART", set()))
    JUMPS += list(getattr(_m, "JUMPS_PART", []))


CHECKS = [("levi", "shiganshina", "zeke", "shiganshina"), ("levi", "paradis", "zeke", "paradis"),
          ("levi", "insurrection", "kenny", "insurrection"), ("eren", "liberio", "lara", "liberio"),
          ("eren", "rose", "reiner", "rose"), ("eren", "grondement", "zeke", "grondement"),
          ("levi", "feminin", "annie", "feminin")]
