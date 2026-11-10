"""Bleach fight database (canon: Kubo's manga ch. 1-686, Turn Back the Pendulum ch. -108 to -97 and the Thousand-Year
Blood War included; official databooks Souls., MASKED, UNMASKED and Kubo statements only for stated facts; no novels
(Can't Fear Your Own World...), no anime-only fillers, no anime-only additions of the TYBW adaptation, no films).
Time axis t = years since Ichigo meets Rukia (ch. 1 = 0). Soul Society 0.15-0.23, Arrancar 0.28-0.38, Hueco Mundo
0.40-0.45, fake Karakura 0.46-0.475, Fullbring 1.85-1.97 (17 months later), Thousand-Year Blood War 2.0-2.33.
Flashbacks negative: Yamamoto seals Yhwach -1000, young Zaraki vs Unohana about -150 (date unknown), Turn Back the
Pendulum -110 to -101, Kaien and Kiganjo about -45, Isshin and Masaki -20, Masaki's death -6.
fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[...], tb=[...], note="... (ch. N)", flags="i"/"?"/"e").
Tags (external circumstances only): malade, epuise, retenue (holding back, power limiter of the Gotei), protege,
surprise, prepa (traps, kido seals set in advance, the Still Silver arrowhead), contre, aide (borrowed external power:
a stolen Bankai used against its owner, Giselle's zombies). Shikai, Bankai, Hollow mask, Fullbring, Resurreccion,
Segunda Etapa, Vollstandig, the Hogyoku evolutions, Kenpachi's unsealing and The Almighty are skills: dated JUMPS,
never fight tags. "e" = partners sharing credit.
Ichigo's berserk full-Hollow form against Ulquiorra (ch. 348-353) is a separate id (ichigo_hollow), like
tanjiro_oni in Demon Slayer: a state he never controls and never regains.
Tier priors: 0 humain, 1 Hollow ordinaire / shinigami de base, 2 officier, Fullbringer, Privaron, 3 lieutenant /
Fracción forte / Sternritter de second rang, 4 capitaine / Espada / Sternritter, 5 capitaine d'élite / Espada 1-3 /
Schutzstaffel / Aizen avant le Hogyoku, 6 Yamamoto / Division zéro / Kenpachi libéré, 7 Aizen fusionné au Hogyoku /
Ichigo du Mugetsu / Yhwach, 8 Yhwach après l'absorption du Roi des âmes.
"""
import glob
import importlib.util
import os

ARCS = [
    ("fondation", "Il y a mille ans (Yamamoto contre Yhwach)", -1000.0),
    ("passe", "Passé lointain (le jeune Zaraki contre Unohana)", -150.0),
    ("pendule", "Turn Back the Pendulum (il y a 110 ans)", -101.0),
    ("avant", "Il y a un demi-siècle (Kaien, Kiganjo)", -45.0),
    ("isshin", "Il y a 20 ans (Isshin et Masaki)", -20.0),
    ("remplacant", "Shinigami remplaçant (pouvoirs de Rukia)", 0.0),
    ("soulsociety", "Soul Society : invasion (Shikai)", 0.15),
    ("bankai", "Soul Society : Bankai et trahison d'Aizen", 0.2),
    ("arrancar", "Arrancar : première invasion", 0.28),
    ("visored", "Arrancar : masque Hollow (Visored)", 0.35),
    ("huecomundo", "Hueco Mundo", 0.4),
    ("karakura", "Faux Karakura : Espada contre capitaines", 0.46),
    ("chrysalide", "Faux Karakura : chrysalide d'Aizen", 0.464),
    ("getsuga", "Getsuga Tenshō final (Mugetsu)", 0.47),
    ("fullbring", "Fullbring (Xcution)", 1.6),
    ("restauration", "Fullbring : pouvoirs restaurés", 1.95),
    ("invasion1", "Guerre de Mille Ans : première invasion", 2.0),
    ("zeroeme", "Guerre de Mille Ans : Division zéro (vrai Zanpakutō)", 2.155),
    ("seireitei", "Guerre de Mille Ans : seconde invasion", 2.2),
    ("palais", "Guerre de Mille Ans : palais du Roi des âmes", 2.24),
    ("final", "Guerre de Mille Ans : bataille finale contre Yhwach", 2.27),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
REVIVE = {}
# aide : pouvoir externe prêté (Bankai volé retourné contre son propriétaire, zombies de Giselle)
EXTRA_TAGS = {"aide": (0.7, 0.7)}
# vétérans dont la force ne bouge plus que par des sauts datés
SLOW = {"yamamoto", "unohana", "yhwach", "ichibe", "aizen", "urahara", "yoruichi", "kyoraku", "ukitake", "tessai",
        "oetsu", "kirinji", "hikifune", "tenjiro", "isshin", "byakuya", "mayuri", "shinji",
        "hachi", "lisa", "love", "rose", "kensei", "mashiro", "hiyori"}   # Visored : un siècle de recul, peu de dérive
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


CHECKS = [("yhwach", "final", "aizen", "final"), ("ichigo", "getsuga", "aizen", "getsuga"),
          ("yamamoto", "invasion1", "royd", "invasion1"), ("yhwach", "invasion1", "yamamoto", "invasion1"),
          ("kenpachi", "zeroeme", "unohana", "zeroeme"), ("kenpachi", "seireitei", "gremmy", "seireitei"),
          ("yhwach", "palais", "ichibe", "palais")]
