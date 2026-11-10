"""Dragon Ball fight database (canon: Toriyama's Dragon Ball manga and the Dragon Ball Super manga by Toyotarō,
supervised by Toriyama; official guidebooks only for stated results. No GT, no anime filler, no movie-only fights
unless the Super manga adapted them).

Time axis t = the in-universe Age year (Goku born Age 737, story starts Age 749).
fight(t, arc, sideA, sideB, "A"/"D", margin 1/2/3, ta=[tags], tb=[tags], note="... (ch. N)", flags="i"/"?")
Tags: malade, epuise, retenue, protege, surprise, prepa, boost (Kaiōken, temporary form, potion), contre, age,
ultra (Ultra Instinct / Beast-type peak state used in a fight). A fusion (gogeta, vegito, gotenks) is its own character.
Permanent new forms (first Super Saiyan, SSJ2, Ultra Instinct mastery, Beast…) are JUMPS.
Tier priors (status at first fight): 0 humain ordinaire, 1 artiste martial, 2 Tortue Géniale / Tao Pai Pai,
3 Piccolo Daimaō / Tenshinhan adulte, 4 Saiyans à leur arrivée sur Terre, 5 Freezer (1re forme), ~6,5 Cell parfait,
~7 Gohan SSJ2, ~7,3 Majin Buu / SSJ3, 8 dieux de la destruction / Super Saiyan God, 9 Jiren / Ultra Instinct, 10 Zeno, anges.
"""
import glob
import importlib.util
import os

ARCS = [
    # Chaque arc est daté à un instant où tous ses combattants sont en vie (ceux qui meurent dans l'arc compris),
    # sinon le modèle ne les classe pas dans cet arc : Raditz, Trunks contre Freezer et les Baba sont donc à part.
    ("avant", "Avant l'histoire (Bardock, Freezer, Saiyans)", 737.0),
    ("pilaf", "Pilaf et les Dragon Balls", 749.05),
    ("tournoi21", "21e Championnat", 749.6),
    ("tourmuscle", "Ruban rouge : la tour Muscle", 750.0),
    ("ruban", "Ruban rouge : Blue, Tao Pai Pai et le QG", 750.1),
    ("baba", "Uranai Baba", 750.5),
    ("tournoi22", "22e Championnat", 753.3),
    ("daimao", "Piccolo Daimaō", 753.5),
    ("tournoi23", "23e Championnat (Piccolo junior)", 756.3),
    ("raditz", "Raditz", 761.8),
    ("saiyan", "Arrivée des Saiyans (Nappa et Vegeta)", 762.4),
    # 2e revue : arcs scindés là où une transformation majeure tombe en cours d'arc (état d'arc = juste après le dernier
    # combat du personnage dans l'arc) : Goku avant / après le Super Saiyan, Gohan SSJ / SSJ2, Gohan avant / après le
    # pouvoir ultime, Goku avant / après l'Ultra Instinct, Gohan avant / après Beast, Gas avant / après son vœu.
    ("namek", "Namek : Dragon Balls et commando Ginyu", 762.8),
    ("freezer", "Namek : Freezer et le Super Saiyan", 762.876),
    ("retourfreezer", "Trunks contre Freezer et le roi Cold", 764.4),
    ("cyborgs", "Cyborgs et Cell", 767.36),
    ("cellgame", "Cell Game : Goku et Gohan contre Cell parfait", 767.5),
    ("ssj2", "Cell Game : Gohan Super Saiyan 2", 767.5055),
    ("buu", "Majin Buu : tournoi, Babidi et le gros Buu", 774.3),
    ("superbuu", "Majin Buu : Super Buu, Vegito et Buu originel", 774.338),
    ("dieux", "Beerus et la résurrection de Freezer", 778.0),
    ("univ6", "Tournoi contre l'univers 6 et Goku Black", 779.5),
    ("tdp1", "Tournoi du Pouvoir : avant l'Ultra Instinct", 780.0),
    ("tdp", "Tournoi du Pouvoir : Ultra Instinct et finale", 780.165),
    ("moro", "Moro", 780.5),
    ("granolah", "Granolah : Granolah contre Goku et Vegeta", 781.0),
    ("gas", "Granolah : le vœu de Gas, puis Black Freezer", 781.05),
    ("superhero", "Super Hero : Ruban rouge et Gamma", 781.5),
    ("beast", "Super Hero : Gohan Beast et après", 781.575),
    ("epilogue", "28e Championnat (Uub, dix ans après Buu)", 784.5),
]

CHARS = {}
F = []
GENERIC = set()
JUMPS = []
# Freezer, tué par Trunks (ch. 331), est ressuscité par les Dragon Balls (Résurrection de F, évoquée DBS ch. 5).
# Gas : « mort » fictive juste après le flash-back de Bardock et « retour » à l'arc Granolah, pour qu'il n'apparaisse
# pas dans les classements des arcs 749-780 où il n'est jamais montré (sa croissance de 40 ans reste modélisée).
REVIVE = {"freeza": 778.0, "gas": 780.95}
# Les états de compétence (ultra, boost) sont ignorés par model.py : ils font partie de la force du personnage.
# "emprunt" : puissance prêtée par un tiers pour ce combat (énergie de Moro injectée, Genki Dama de toute la Terre,
# magie de Babidi), qui n'est pas la force propre du personnage.
EXTRA_TAGS = {"emprunt": (1.0, 0.7)}
SLOW = {"whis", "beerus", "roshi", "kami", "mr_popo", "merus"}   # dieux, ange et vieux maître : pas de dérive libre
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
