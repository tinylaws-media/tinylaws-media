"""One Piece fight database (manga canon only, plus Oda-supervised official info such as Vivre Cards / SBS
when it states a result). Same format as the Naruto data.py: see fight() below.

Time axis t = years since Luffy sets sail (Romance Dawn = 0). Pre-story flashbacks are negative
(God Valley about -38, Roger's execution -22, Oden's death -20 ...). Post-timeskip starts at 2.0.
Fight: fight(t, arc, sideA, sideB, result "A"/"D", margin 1 serrée / 2 nette / 3 écrasante,
            ta=[tags side A], tb=[tags side B], note="... (ch. N)", flags="i" interrompu / "?" à vérifier)
Tags: malade, epuise, retenue, protege, surprise, prepa, boost, contre, age, plus One Piece extras below.
Tier priors (status at first fight): 0 civil, 1 pirate ou marine ordinaire, 2 boss d'East Blue / officier
Baroque Works, 3 Paradise fort / agent du CP9, 4 Shichibukai / vice-amiral / Supernova d'avant l'ellipse,
5 commandant d'élite d'un Empereur / Supernova après l'ellipse, 6 Calamité / amiral / Doyen, 7 Empereur /
amiral en chef, 8 légende (Roger, Rocks, Whitebeard à son apogée, Garp à son apogée, Joy Boy, Imu).
"""
import glob
import importlib.util
import os

ARCS = [
    ("godvalley", "Ère de Rocks et God Valley", -38.0),
    ("roger", "Ère de Roger", -24.0),
    ("oden", "Oden et la chute de Wano", -20.0),
    ("harald", "Elbaf : chute de Harald", -14.02),   # ch. 1169-1170
    ("avant", "Avant l'histoire : Shanks, Corazon, enfance de Luffy, Ace, Sabo", -10.0),
    ("cocoyashi", "Avant l'histoire : Arlong à Cocoyashi, Ace et Dadan", -8.0),
    ("ace_wb", "Avant l'histoire : Ace chez Barbe Blanche", -2.5),
    ("eastblue", "East Blue", 0.1),
    ("alabasta", "Alabasta", 0.4),
    ("skypiea", "Skypiea", 0.55),
    ("water7", "Water Seven et Enies Lobby", 0.7),
    ("thriller", "Thriller Bark", 0.8),
    ("marineford", "Sabaody, Impel Down, Marineford", 0.9),
    ("fishman", "Île des Hommes-Poissons", 2.1),
    ("punkhazard", "Punk Hazard et Dressrosa", 2.2),
    ("gear4", "Dressrosa : Gear 4 et chute de Doflamingo", 2.279),   # ch. 784-791
    ("wci", "Zou et Whole Cake Island", 2.3),
    ("wano", "Wano", 2.4),
    ("wano5", "Wano : Gear 5 et chute de Kaido", 2.4495),   # ch. 1044-1050
    ("egghead", "Egghead", 2.5),
    ("elbaf", "Elbaf", 2.6),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []      # (char, t, mean change in tiers, sd, label)
REVIVE = {}
# vétérans dont la force ne bouge plus que par des sauts datés (âge, maladie)
SLOW = {"rayleigh", "gaban", "roger", "garp", "whitebeard", "sengoku", "rocks"}
EXTRA_TAGS = {"eveil": (1.5, 0.8), "haki_roi": (0.8, 0.6), "possede": (2.0, 1.0)}   # possede : un corps prêté à Imu (Domi Reversi), pas la force propre du personnage   # éveil du fruit / Gear 5, Haki des rois imprégné
BOOK_TIMES = {}
CHECKS = []


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

CHECKS = [("luffy", "wano5", "kaido", "wano5"), ("luffy", "wano", "kaido", "wano"), ("shanks", "egghead", "kaido", "wano"), ("zoro", "wano", "sanji", "wano"),
          ("akainu", "punkhazard", "aokiji", "punkhazard"), ("mihawk", "marineford", "shanks", "marineford"),
          ("whitebeard", "roger", "roger", "roger"), ("luffy", "egghead", "kizaru", "egghead")]
