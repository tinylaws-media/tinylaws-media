# Dragon Ball, partie 1 : tout le manga original de Toriyama (ch. 1-519), Dragon Ball puis Dragon Ball Z.
# Manga uniquement : pas de filler, pas de films, pas de GT. "fight" est injecté par data.py.
# Numéros de chapitre en numérotation japonaise continue (DBZ Viz n = ch. n + 194), vérifiés sur la liste
# des titres de chapitres (Wikipedia), Kanzenshuu (21e Championnat) et Dragon Ball Wiki (fandom).
# "ch. ~N" = à un ou deux chapitres près.
# Repères de temps (année Age) : Pilaf 749.0-749.2, 21e Championnat 749.6, Ruban rouge 750.0-750.4,
# Baba 750.5-750.6, 22e Championnat 753.3, Piccolo Daimaō 753.5, 23e Championnat 756.3, Raditz 761.8,
# Saiyans 762.4, Namek 762.80-762.90, Trunks contre Freezer 764.4, cyborgs et Cell 767.36-767.45,
# Cell Game 767.50-767.52, futur de Trunks 767.6, Buu 774.30-774.38, Uub 784.5.
# Morts annulées par les Dragon Balls (Krillin, Roshi, Chaozu, Yamcha, Tenshinhan, Goku, Piccolo, Vegeta,
# Gohan, Freezer en Super...) : death = None, la mort est signalée dans la note.

CHARS_PART = {
    # ---------------------------------------------------------------- héros
    "goku": ("Son Goku", "Héros", 1.0, None, None),
    "krillin": ("Krilin", "Héros", 1.0, None, None),
    "yamcha": ("Yamcha", "Héros", 1.2, None, None),
    "roshi": ("Tortue Géniale (Jackie Chun)", "Héros", 2.0, None, None),
    "tien": ("Tenshinhan", "Héros", 2.3, None, None),
    "chiaotzu": ("Chaozu", "Héros", 1.6, None, None),
    "yajirobe": ("Yajirobe", "Héros", 2.2, None, None),
    "gohan": ("Son Gohan", "Héros", 2.4, None, None),
    "piccolo": ("Piccolo (Ma Junior)", "Clan Piccolo", 3.0, None, None),
    "kami": ("Kami-sama (Shen)", "Dieux", 3.2, None, None),
    "mr_popo": ("Mr. Popo", "Dieux", 3.0, None, None),
    "chi_chi": ("Chichi", "Héros", 1.4, None, None),
    "trunks": ("Trunks (du futur)", "Héros", 5.4, None, None),
    "trunks_kid": ("Trunks (enfant)", "Héros", 5.6, None, None),
    "goten": ("Son Goten", "Héros", 5.5, None, None),
    "gotenks": ("Gotenks", "Héros", 6.5, None, None),
    "vegito": ("Vegito", "Héros", 7.9, None, None),
    "videl": ("Videl", "Héros", 1.3, None, None),
    "mr_satan": ("Mr. Satan", "Héros", 1.0, None, None),
    "uub": ("Uub", "Héros", 6.0, None, None),
    "arale": ("Arale Norimaki", "Village Pingouin", 2.6, None, None),
    "bora": ("Bora (père d'Upa)", "Karin", 1.5, None, None),
    "grandpa_gohan": ("Son Gohan (grand-père, revenant)", "Héros", 1.8, None, None),
    "supreme_kai": ("Shin (Kaiōshin de l'Est)", "Dieux", 5.0, None, None),
    "nail": ("Nail", "Namek", 4.3, None, None),
    "dende": ("Dende", "Namek", 0.5, None, None),
    "namek_villageois": ("Guerriers et villageois nameks (groupe)", "Namek", 2.5, None, None),
    # ---------------------------------------------------------------- Pilaf, 21e, Baba
    "oolong": ("Oolong", "Bandits", 0.3, None, None),
    "pilaf": ("Pilaf, Shu et Mai (et leurs machines)", "Pilaf", 0.8, None, None),
    "bacterian": ("Bacterian", "21e Championnat", 0.8, None, None),
    "giran": ("Giran", "21e Championnat", 1.1, None, None),
    "nam": ("Namu", "21e Championnat", 1.2, None, None),
    "ranfan": ("Ranfan", "21e Championnat", 0.8, None, None),
    "fangs": ("Dracula Man (Fangs)", "Combattants de Baba", 1.1, None, None),
    "invisible_man": ("L'homme invisible", "Combattants de Baba", 0.9, None, None),
    "bandages": ("La Momie", "Combattants de Baba", 1.4, None, None),
    "spike": ("Akkuman (Spike)", "Combattants de Baba", 1.4, None, None),
    # ---------------------------------------------------------------- Ruban rouge
    "colonel_silver": ("Colonel Silver", "Ruban rouge", 1.0, None, None),
    "soldats_ruban": ("Soldats du Ruban rouge (groupe)", "Ruban rouge", 0.5, None, None),
    "metallitron": ("Sergent Metallitron", "Ruban rouge", 1.0, None, None),
    "murasaki": ("Ninja Murasaki (et ses frères)", "Ruban rouge", 1.0, None, None),
    "buyon": ("Buyon", "Ruban rouge", 1.2, 750.05, None),
    "general_white": ("Général White", "Ruban rouge", 0.8, None, None),
    "android_8": ("C-8 (Hatchan)", "Ruban rouge", 1.6, None, None),
    "robot_pirate": ("Robot pirate", "Ruban rouge", 1.0, None, None),
    "general_blue": ("Général Blue", "Ruban rouge", 1.7, 750.22, None),
    "tao_pai_pai": ("Tao Pai Pai", "Ruban rouge", 2.0, None, None),
    "commander_red": ("Commandant Red", "Ruban rouge", 0.2, 750.34, None),
    "staff_black": ("Colonel Black", "Ruban rouge", 1.5, 750.35, None),
    # ---------------------------------------------------------------- 22e Championnat, Piccolo Daimaō
    "chappa": ("Roi Chappa", "22e Championnat", 1.3, None, None),
    "man_wolf": ("L'homme-loup", "22e Championnat", 1.0, None, None),
    "panpoot": ("Pampoot", "22e Championnat", 0.9, None, None),
    "tambourine": ("Tambourine", "Clan Piccolo", 2.4, 753.51, None),
    "cymbal": ("Cymbal", "Clan Piccolo", 2.2, 753.505, None),
    "drum": ("Drum", "Clan Piccolo", 2.5, 753.551, None),
    "king_piccolo": ("Piccolo Daimaō", "Clan Piccolo", 2.6, 753.56, None),
    "artistes_martiaux": ("Artistes martiaux (groupe)", "Divers", 1.0, None, None),
    # ---------------------------------------------------------------- Saiyans, Freezer
    "raditz": ("Raditz", "Saiyans", 3.3, 761.811, None),
    "saibaman": ("Saibaimen", "Saiyans", 3.0, None, None),
    "nappa": ("Nappa", "Saiyans", 3.55, 762.416, None),
    "vegeta": ("Vegeta", "Saiyans", 4.0, None, None),
    "cui": ("Kiwi (Cui)", "Armée de Freezer", 3.9, 762.805, None),
    "dodoria": ("Dodoria", "Armée de Freezer", 4.0, 762.82, None),
    "zarbon": ("Zabon (Zarbon)", "Armée de Freezer", 4.1, 762.84, None),
    "soldats_freezer": ("Soldats de Freezer (groupe)", "Armée de Freezer", 2.5, None, None),
    "guldo": ("Guldo", "Commando Ginyu", 3.6, 762.851, None),
    "recoome": ("Recoome", "Commando Ginyu", 4.3, 762.862, None),
    "burter": ("Barta (Burter)", "Commando Ginyu", 4.2, 762.862, None),
    "jeice": ("Jeice", "Commando Ginyu", 4.2, 762.87, None),
    "ginyu": ("Capitaine Ginyu", "Commando Ginyu", 4.5, None, None),
    "freeza": ("Freezer", "Armée de Freezer", 4.5, 764.40, None),   # tué par Trunks, ressuscité (REVIVE)
    "king_cold": ("Roi Cold", "Armée de Freezer", 4.8, 764.401, None),
    # ---------------------------------------------------------------- cyborgs, Cell
    "android_19": ("C-19", "Cyborgs", 5.2, 767.362, None),
    "android_20": ("C-20 (Dr. Gero)", "Cyborgs", 5.0, 767.37, None),
    "android_17": ("C-17", "Cyborgs", 5.7, None, None),
    "android_18": ("C-18", "Cyborgs", 5.6, None, None),
    "android_16": ("C-16", "Cyborgs", 5.9, 767.503, None),
    "cell": ("Cell", "Cyborgs", 5.4, 767.512, None),
    "cell_jr": ("Cell juniors (groupe)", "Cyborgs", 5.8, 767.506, None),
    "armee": ("Armée terrienne (groupe)", "Divers", 0.5, None, None),
    "android_17_futur": ("C-17 (futur de Trunks)", "Cyborgs", 5.7, 767.6, None),
    "android_18_futur": ("C-18 (futur de Trunks)", "Cyborgs", 5.6, 767.6, None),
    "cell_futur": ("Cell (futur de Trunks)", "Cyborgs", 5.4, 767.61, None),
    # ---------------------------------------------------------------- Buu
    "criminels": ("Criminels et gangsters (groupe)", "Divers", 0.3, None, None),
    "pintar": ("Pintar", "25e Championnat", 1.0, None, None),
    "spopovich": ("Spopovich", "Babidi", 3.3, 774.306, None),
    "yamu": ("Yamu", "Babidi", 3.3, None, None),
    "babidi": ("Babidi", "Babidi", 3.0, 774.331, None),
    "pui_pui": ("Pui Pui", "Babidi", 4.5, 774.307, None),
    "yakon": ("Yakon", "Babidi", 5.2, 774.308, None),
    "dabura": ("Dabura", "Babidi", 6.0, 774.321, None),
    "majin_buu": ("Majin Buu (gros)", "Majin Buu", 7.0, None, None),
    "super_buu": ("Super Buu (Buu maléfique)", "Majin Buu", 7.2, 774.369, None),
    "kid_buu": ("Buu originel (Kid Buu)", "Majin Buu", 7.2, 774.38, None),
}

GENERIC_PART = {"soldats_ruban", "artistes_martiaux", "namek_villageois", "soldats_freezer", "armee", "criminels",
                "saibaman", "cell_jr"}

JUMPS_PART = [
    # Goku
    ("goku", 749.4, 0.5, 0.4, "Entraînement de huit mois chez Tortue Géniale"),
    ("goku", 750.28, 0.3, 0.3, "Eau sacrée de Karin (entraînement à la tour)"),
    ("goku", 752.0, 0.6, 0.4, "Trois ans de voyage et d'entraînement"),
    ("goku", 753.53, 0.4, 0.3, "Super Eau Sacrée (ch. 151)"),
    ("goku", 755.0, 0.6, 0.4, "Trois ans d'entraînement chez Kami-sama"),
    ("goku", 762.2, 0.7, 0.4, "Entraînement chez Kaiō du Nord"),
    ("goku", 762.7, 0.4, 0.3, "Gravité x100 en route pour Namek"),
    ("goku", 762.875, 0.2, 0.2, "Guérison après le combat contre Ginyu (zenkai)"),
    ("goku", 762.895, 0.7, 0.4, "Premier Super Saiyan (ch. 317-318)"),
    ("goku", 763.5, 0.3, 0.3, "Yardrat, Super Saiyan à volonté (ch. 333-334)"),
    ("goku", 767.42, 0.3, 0.3, "Super Saiyan maîtrisé, salle de l'Esprit et du Temps"),
    ("goku", 770.0, 0.5, 0.4, "Super Saiyan 2 et entraînement dans l'au-delà"),
    ("goku", 772.0, 0.5, 0.3, "Super Saiyan 3, acquis dans l'au-delà avant son retour (révélé ch. 474)"),
    # Vegeta
    ("vegeta", 762.6, 0.2, 0.2, "Zenkai après la défaite sur Terre"),
    ("vegeta", 762.835, 0.2, 0.2, "Zenkai après Zabon (ch. ~265)"),
    ("vegeta", 762.88, 0.2, 0.2, "Zenkai après Recoome"),
    ("vegeta", 766.0, 0.7, 0.4, "Super Saiyan (révélé ch. 342)"),
    ("vegeta", 767.398, 0.3, 0.3, "Super Vegeta, salle de l'Esprit et du Temps"),
    ("vegeta", 772.0, 0.5, 0.4, "Super Saiyan 2 (entraînement des sept ans)"),
    ("vegeta", 777.0, 0.3, 0.4, "Quatre ans d'entraînement après Buu (salle de gravité, DBS ch. 1-3)"),
    # Gohan
    ("gohan", 762.3, 0.7, 0.4, "Entraînement chez Piccolo"),
    ("gohan", 762.83, 0.4, 0.3, "Potentiel libéré par le Grand Doyen (ch. ~269)"),
    ("gohan", 762.89, 0.2, 0.2, "Zenkai après Recoome"),
    ("gohan", 767.42, 1.0, 0.4, "Super Saiyan, salle de l'Esprit et du Temps"),
    ("gohan", 767.505, 0.6, 0.3, "Super Saiyan 2 (ch. 408)"),
    ("gohan", 773.0, -0.5, 0.4, "Sept ans sans entraînement"),
    ("gohan", 774.34, 1.4, 0.4, "Pouvoir ultime libéré par le vieux Kaiōshin"),
    ("gohan", 776.0, -0.5, 0.4, "Études puis travail de chercheur, plus d'entraînement (DBS ch. 27, 31)"),
    # Piccolo
    ("piccolo", 761.0, 0.3, 0.3, "Entraînement après le 23e Championnat"),
    ("piccolo", 762.2, 0.3, 0.3, "Entraînement avant les Saiyans"),
    ("piccolo", 762.7, 0.5, 0.4, "Entraînement chez Kaiō du Nord dans l'au-delà (ch. ~285)"),
    ("piccolo", 762.875, 1.0, 0.4, "Fusion avec Nail, « plus d'un million » comme Freezer 2e forme (ch. 295-300)"),
    ("piccolo", 767.38, 0.8, 0.4, "Fusion avec Kami-sama (ch. 360)"),
    # autres héros
    ("krillin", 749.4, 0.4, 0.3, "Entraînement chez Tortue Géniale"),
    ("krillin", 752.0, 0.5, 0.4, "Entraînement avant le 22e Championnat"),
    ("krillin", 762.2, 0.6, 0.4, "Entraînement chez Kami-sama"),
    ("krillin", 762.83, 0.4, 0.3, "Potentiel libéré par le Grand Doyen (ch. 259)"),
    ("yamcha", 752.0, 0.5, 0.4, "Entraînement chez Tortue Géniale"),
    ("yamcha", 762.2, 0.6, 0.4, "Entraînement chez Kami-sama"),
    ("tien", 762.2, 0.6, 0.4, "Entraînement chez Kami-sama"),
    ("tien", 763.0, 0.4, 0.4, "Entraînement chez Kaiō du Nord dans l'au-delà (ch. ~285, 330)"),
    ("yamcha", 763.0, 0.4, 0.4, "Entraînement chez Kaiō du Nord dans l'au-delà (ch. ~285, 330)"),
    ("chiaotzu", 763.0, 0.4, 0.4, "Entraînement chez Kaiō du Nord dans l'au-delà (ch. ~285, 330)"),
    ("chiaotzu", 762.2, 0.6, 0.4, "Entraînement chez Kami-sama"),
    ("trunks", 767.398, 0.3, 0.3, "Salle de l'Esprit et du Temps"),
    ("gotenks", 774.346, 0.7, 0.3, "Super Saiyan 3 (ch. ~494)"),
    ("vegito", 778.5, 0.6, 0.5, "Goku et Vegeta passés au Super Saiyan Blue (Vegito Blue, DBS ch. 23)"),
    # trois ans d'entraînement avant les cyborgs (ch. 336-338)
    ("goku", 766.0, 0.3, 0.3, "Trois ans d'entraînement avant les cyborgs, avec Piccolo et Gohan (ch. 336-338)"),
    ("piccolo", 766.0, 0.4, 0.3, "Trois ans d'entraînement avant les cyborgs (ch. 336-338)"),
    ("gohan", 766.0, 0.3, 0.3, "Trois ans d'entraînement avec Goku et Piccolo (ch. 336-338)"),
    ("tien", 766.0, 0.3, 0.3, "Trois ans d'entraînement solitaire (ch. 336-338)"),
    ("krillin", 766.0, 0.2, 0.3, "Trois ans d'entraînement (ch. 336-338)"),
    ("yamcha", 766.0, 0.2, 0.3, "Trois ans d'entraînement (ch. 336-338)"),
    # méchants
    ("king_piccolo", 753.522, 0.4, 0.3, "Rajeunissement par Shenron (ch. 147)"),
    ("tao_pai_pai", 756.0, 0.3, 0.3, "Corps de cyborg"),
    ("freeza", 762.879, 0.2, 0.15, "Deuxième forme (ch. 296)"),
    ("freeza", 762.885, 0.2, 0.15, "Troisième forme (ch. 302)"),
    ("freeza", 762.886, 0.3, 0.2, "Forme finale (ch. 304)"),
    ("cell", 767.394, 0.4, 0.3, "Absorption de C-17, forme semi-parfaite (ch. 373)"),
    ("cell", 767.403, 0.4, 0.3, "Absorption de C-18, forme parfaite (ch. 382)"),
    ("cell", 767.509, 0.3, 0.3, "Retour après l'autodestruction (ch. 413)"),
    ("super_buu", 774.351, 0.5, 0.3, "Absorption de Gotenks et Piccolo (ch. 500)"),
    ("super_buu", 774.353, 0.4, 0.3, "Absorption de Gohan (ch. 502)"),
]

# ============================================================== Pilaf (749)
fight(749.05, "pilaf", "goku", "oolong", "A", 3, note="Oolong et ses transformations ne font pas le poids (ch. 5-6)")
fight(749.08, "pilaf", "goku", "yamcha", "D", ta=["epuise"],
      note="Goku affamé est malmené puis se reprend ; Yamcha fuit à la vue de Bulma (ch. 7-8)", flags="i")
fight(749.2, "pilaf", "goku", "pilaf", "A", 3, ta=["boost"], note="Goku en Oozaru dévaste le château de Pilaf (ch. 21)")

# ============================================================== 21e Championnat (749)
fight(749.60, "tournoi21", "krillin", "bacterian", "A", 2, note="Quart de finale, abandon de Bacterian (ch. 36)")
fight(749.601, "tournoi21", "roshi", "yamcha", "A", 3, ta=["retenue"], note="Jackie Chun sort Yamcha du ring (ch. 37)")
fight(749.602, "tournoi21", "nam", "ranfan", "A", 2, note="Quart de finale, KO (ch. 38)")
fight(749.603, "tournoi21", "goku", "giran", "A", 2, note="Giran abandonne, Goku se sert de sa queue (ch. 39-40)")
fight(749.61, "tournoi21", "roshi", "krillin", "A", 2, ta=["retenue"], note="Demi-finale, KO (ch. 41-43)")
fight(749.611, "tournoi21", "goku", "nam", "A", 1, note="Demi-finale, Nam sort du ring (ch. 44-45)")
fight(749.62, "tournoi21", "roshi", "goku", "A", 1, tb=["boost"],
      note="Finale : double KO, Jackie Chun se relève le premier ; Goku brièvement en Oozaru (ch. 46-53)")

# ============================================================== Ruban rouge (750)
fight(750.00, "tourmuscle", "goku", "colonel_silver", "A", 3, note="Dans la forêt (ch. 55-56)")
fight(750.01, "tourmuscle", "goku", "soldats_ruban", "A", 3, note="Village de Jingle, puis l'assaut de la Muscle Tower (ch. 57)")
fight(750.02, "tourmuscle", "goku", "metallitron", "A", 2, note="Muscle Tower : le robot tient jusqu'à épuisement des piles (ch. 58-59)")
fight(750.03, "tourmuscle", "goku", "murasaki", "A", 2, note="Ninja Murasaki et ses frères (ch. 60-62)")
fight(750.05, "tourmuscle", "goku", "buyon", "A", 2, note="Goku gèle Buyon en ouvrant le mur (ch. 64-65)")
fight(750.06, "tourmuscle", "android_8", "general_white", "A", 3, note="C-8 éjecte White de la tour (ch. 66)")
fight(750.15, "ruban", ["goku", "krillin"], "robot_pirate", "A", 2, note="Grotte des pirates (ch. 74-75)")
fight(750.16, "ruban", "general_blue", "krillin", "A", 3, note="Paralysie télékinétique (ch. ~77)")
fight(750.17, "ruban", "general_blue", "goku", "D",
      note="Blue paralyse Goku ; une souris le distrait, Goku le frappe, la grotte s'effondre (ch. 77-79)", flags="i")
fight(750.20, "ruban", "general_blue", "goku", "A", 2, note="Village Pingouin : Blue domine avant l'intervention d'Arale (ch. 81-83)",
      flags="i")
fight(750.201, "ruban", "arale", "general_blue", "A", 3, note="Coup de tête d'Arale, Blue s'envole ; scène gag de crossover Dr Slump (ch. 82-83)", flags="?")
fight(750.215, "ruban", "tao_pai_pai", "bora", "A", 3, note="Tao tue Bora (ressuscité par Shenron au ch. 112) (ch. 85)")
fight(750.22, "ruban", "tao_pai_pai", "general_blue", "A", 3, note="Tao tue Blue avec sa langue (ch. 85)")
fight(750.23, "ruban", "tao_pai_pai", "goku", "A", 2, note="Dodonpa, Goku laissé pour mort (ch. 85-86)")
fight(750.30, "ruban", "goku", "tao_pai_pai", "A", 2, note="Revanche après la tour de Karin (ch. 90-92)")
fight(750.33, "ruban", "goku", "soldats_ruban", "A", 3, note="Assaut du QG (ch. 93-94)")
fight(750.34, "ruban", "staff_black", "commander_red", "A", 3, tb=["surprise"], note="Black abat Red (ch. 95)")
fight(750.35, "ruban", "goku", "staff_black", "A", 2, note="Black en armure de combat (ch. 95-96)")

# ============================================================== Baba (750)
fight(750.50, "baba", "fangs", "krillin", "A", 2, note="Dracula Man suce le sang de Krilin (ch. 100)")
fight(750.51, "baba", "yamcha", "invisible_man", "A", 2,
      note="Le saignement de nez de Tortue Géniale révèle l'homme invisible (ch. ~101)")
fight(750.52, "baba", "bandages", "yamcha", "A", 2, note="Yamcha suspendu au-dessus du bassin, abandonne (ch. 101-102)")
fight(750.53, "baba", "goku", "bandages", "A", 3, note="Un seul coup (ch. 102-103)")
fight(750.54, "baba", "goku", "spike", "A", 3, note="Akkuman projeté dans le mur (ch. 104-105)")
fight(750.55, "baba", "goku", "grandpa_gohan", "A", 1, tb=["retenue"],
      note="Le grand-père masqué concède le combat (ch. 105-107)", flags="?")
fight(750.60, "baba", "goku", "pilaf", "A", 2, note="Les Pilaf Machines (ch. 109-110)")

# ============================================================== 22e Championnat (753)
fight(753.30, "tournoi22", "goku", "chappa", "A", 2, note="Éliminatoires (ch. 115)")
fight(753.31, "tournoi22", "tien", "yamcha", "A", 3, note="Tenshinhan brise la jambe de Yamcha (ch. 117-118)")
fight(753.311, "tournoi22", "roshi", "man_wolf", "A", 3, note="Jackie Chun recrée la pleine lune pour le guérir (ch. 119)")
fight(753.312, "tournoi22", "krillin", "chiaotzu", "A", 2, note="Krilin déjoue la télépathie de Chaozu (ch. 120-121)")
fight(753.313, "tournoi22", "goku", "panpoot", "A", 3, note="(ch. 122)")
fight(753.32, "tournoi22", "tien", "roshi", "A", 1, tb=["retenue"],
      note="Jackie Chun sort volontairement après avoir dissuadé Tenshinhan du mal (ch. 123-124)", flags="?")
fight(753.321, "tournoi22", "goku", "krillin", "A", 2, note="Demi-finale (ch. 125-127)")
fight(753.33, "tournoi22", "tien", "goku", "A", 1,
      note="Finale : Goku touche le sol en second après le camion (ch. 128-134)")

# ============================================================== Piccolo Daimaō (753)
fight(753.50, "daimao", "tambourine", "krillin", "A", 3, tb=["surprise"],
      note="Krilin tué (ressuscité par Shenron, ch. 165) (ch. 135)")
fight(753.505, "daimao", "yajirobe", "cymbal", "A", 3, note="Yajirobe tranche Cymbal et le mange (ch. 138-139)")
fight(753.506, "daimao", "tambourine", "artistes_martiaux", "A", 3, note="Chasse aux artistes martiaux (ch. 140)")
fight(753.51, "daimao", "goku", "tambourine", "A", 2, note="(ch. 141)")
fight(753.511, "daimao", "king_piccolo", "goku", "A", 2, tb=["epuise"], note="Goku laissé pour mort (ch. 142-144)")
fight(753.52, "daimao", "king_piccolo", "roshi", "A", 1, tb=["prepa"],
      note="Mafūba : le sceau rate l'autocuiseur, Roshi meurt d'épuisement (ressuscité ch. 165) (ch. 146)", flags="?")
fight(753.521, "daimao", "king_piccolo", "chiaotzu", "A", 3, note="Chaozu tué (ressuscité ch. 165) (ch. ~146-147)")
fight(753.55, "daimao", "drum", "tien", "A", 2, note="Drum domine Tenshinhan quand Goku arrive (ch. 154)", flags="i")
fight(753.551, "daimao", "goku", "drum", "A", 3, note="Un coup de pied (ch. 155)")
fight(753.56, "daimao", "goku", "king_piccolo", "A", 1,
      note="Goku, bras et jambe brisés, transperce Piccolo Daimaō ; Tenshinhan aide d'un Kikōhō (ch. 156-161)")
fight(753.7, "daimao", "mr_popo", "goku", "A", 2, ta=["retenue"],
      note="Au palais de Kami, Goku ne peut toucher Mr. Popo (ch. ~164)", flags="?")

# ============================================================== 23e Championnat (756)
fight(756.30, "tournoi23", "tien", "tao_pai_pai", "A", 3, note="Tao cyborg (ch. 169-170)")
fight(756.301, "tournoi23", "goku", "chi_chi", "A", 3, ta=["retenue"], note="Goku promet de l'épouser (ch. 171)")
fight(756.302, "tournoi23", "piccolo", "krillin", "A", 2, note="(ch. 172-173)")
fight(756.303, "tournoi23", "kami", "yamcha", "A", 2, ta=["retenue"], note="Kami sous le nom de Shen (ch. 174-175)")
fight(756.31, "tournoi23", "goku", "tien", "A", 1, note="Goku exploite les faiblesses du Shishin no ken (ch. 176-179)")
fight(756.311, "tournoi23", "piccolo", "kami", "A", 2, note="Mafūba renvoyé, Kami enfermé dans un flacon (ch. 180-181)")
fight(756.32, "tournoi23", "goku", "piccolo", "A", 1, ta=["epuise"], tb=["epuise"],
      note="Finale : coup de tête et sortie de ring (ch. 182-193)")

# ============================================================== Raditz (761)
fight(761.80, "raditz", "raditz", "piccolo", "A", 2, note="Raditz renvoie l'attaque de Piccolo, qui fuit (ch. 195)", flags="i")
fight(761.801, "raditz", "raditz", "goku", "A", 3, tb=["surprise"], note="Un coup, Gohan enlevé (ch. 196)")
fight(761.81, "raditz", "gohan", "raditz", "A", 2, ta=["boost", "surprise"],
      note="Coup de tête de colère de Gohan (ch. 202)", flags="i")
fight(761.811, "raditz", ["goku", "piccolo"], "raditz", "A", 1, ta=["prepa"],
      note="Makankōsappō à travers Raditz et Goku (Goku ressuscité, ch. 220) (ch. 197-204)")

# ============================================================== Saiyans (762)
fight(762.40, "saiyan", "tien", "saibaman", "A", 2, note="Premier Saibaimen (ch. 214)")
fight(762.401, "saiyan", "saibaman", "yamcha", "A", 3, ta=["surprise"],
      note="Autodestruction, Yamcha tué (ressuscité ch. ~323) (ch. 215)")
fight(762.402, "saiyan", "krillin", "saibaman", "A", 3, note="Krilin balaie les Saibaimen (ch. 216)")
fight(762.403, "saiyan", "piccolo", "saibaman", "A", 3, note="(ch. 216)")
fight(762.404, "saiyan", "nappa", "tien", "A", 3, note="Nappa tranche le bras de Tenshinhan (ch. 216-217)")
fight(762.405, "saiyan", "nappa", "chiaotzu", "A", 3, note="Autodestruction inutile de Chaozu (ressuscité) (ch. 217)")
fight(762.406, "saiyan", "nappa", "tien", "A", 3, ta=["epuise"], tb=["epuise"],
      note="Dernier Kikōhō, Tenshinhan meurt (ressuscité) (ch. 218)")
fight(762.41, "saiyan", "nappa", ["piccolo", "gohan", "krillin"], "A", 2,
      note="Piccolo meurt en protégeant Gohan (ressuscité) (ch. 219-223)")
fight(762.415, "saiyan", "goku", "nappa", "A", 3, note="Nappa achevé ensuite par Vegeta (ch. 224-227)")
fight(762.42, "saiyan", "goku", "vegeta", "A", 1, ta=["boost"],
      note="Kaiōken x3 : le Kamehameha l'emporte sur le Galick Ho (ch. 228-231)", flags="i")
fight(762.421, "saiyan", "vegeta", "goku", "A", 3, ta=["boost"], tb=["epuise"],
      note="Vegeta en Oozaru (lune artificielle) broie Goku (ch. 232-236)")
fight(762.43, "saiyan", ["goku", "gohan", "krillin", "yajirobe"], "vegeta", "A", 1, ta=["boost", "epuise"],
      note="Yajirobe coupe la queue, Genki Dama renvoyé par Gohan, Gohan en Oozaru écrase Vegeta qui fuit (ch. 236-241)")

# ============================================================== Namek (762)
fight(762.80, "namek", ["gohan", "krillin"], "soldats_freezer", "A", 3, note="À l'atterrissage (ch. ~247-248)", flags="?")
fight(762.805, "namek", "vegeta", "cui", "A", 3, note="(ch. 249)")
fight(762.81, "namek", "zarbon", "namek_villageois", "A", 3, note="Massacre d'un village (ch. ~251-252)")
fight(762.811, "namek", "dodoria", "namek_villageois", "A", 3, note="Village de Moori, devant Freezer (ch. 252-253)")
fight(762.815, "namek", ["gohan", "krillin"], "dodoria", "D", ta=["surprise"],
      note="Gohan projette Dodoria, les deux fuient au Taiyōken (ch. 254-256)", flags="i")
fight(762.82, "namek", "vegeta", "dodoria", "A", 3, note="(ch. 257)")
fight(762.825, "namek", "vegeta", "soldats_freezer", "A", 3, note="Autour du vaisseau de Freezer (ch. ~260-261)", flags="?")
fight(762.83, "namek", "zarbon", "vegeta", "A", 2, ta=["boost"], note="Zabon transformé (ch. 262-263)")
fight(762.84, "namek", "vegeta", "zarbon", "A", 3, tb=["boost"], note="Vegeta lui transperce le ventre (ch. 268)")
fight(762.85, "namek", "guldo", ["gohan", "krillin"], "A", 1, note="Paralysie, interrompu par Vegeta (ch. 273-274)", flags="i")
fight(762.851, "namek", "vegeta", "guldo", "A", 3, note="(ch. 274)")
fight(762.852, "namek", "recoome", "vegeta", "A", 2, note="(ch. 275-277)")
fight(762.853, "namek", "recoome", ["gohan", "krillin"], "A", 3, note="(ch. 277-278)")
fight(762.86, "namek", "goku", "recoome", "A", 3, note="Un seul coup (ch. 280)")
fight(762.861, "namek", "goku", ["burter", "jeice"], "A", 3, note="Barta mis KO, Jeice fuit (ch. 281)")
fight(762.862, "namek", "vegeta", ["recoome", "burter"], "A", 3, tb=["epuise"], note="Vegeta les achève (ch. 282)")
fight(762.865, "namek", "goku", "ginyu", "A", 2,
      note="Goku domine ; Ginyu se blesse et échange les corps (ch. 283-287)", flags="i")
fight(762.866, "namek", "freeza", "nail", "A", 2, ta=["retenue"], note="Freezer en 1re forme (ch. 285-291)")
fight(762.87, "namek", "vegeta", "jeice", "A", 3, note="(ch. ~289)")
fight(762.871, "namek", "vegeta", "ginyu", "A", 2, tb=["epuise"],
      note="Ginyu dans le corps de Goku, qu'il maîtrise mal ; il finit en grenouille (ch. 288-290)", flags="?")
fight(762.88, "freezer", "freeza", "krillin", "A", 3, note="2e forme : Krilin empalé, soigné par Dende (ch. 296)")
fight(762.881, "freezer", "freeza", ["gohan", "vegeta", "krillin"], "A", 2, tb=["boost"],
      note="Rage de Gohan, Freezer reprend le dessus (ch. 297-299)")
fight(762.882, "freezer", "piccolo", "freeza", "A", 1, note="Piccolo fusionné avec Nail domine la 2e forme (ch. 300-301)",
      flags="i")
fight(762.885, "freezer", "freeza", ["piccolo", "gohan"], "A", 2, note="3e forme ; Masenko en rafale inefficace (ch. 302-303)")
fight(762.886, "freezer", "freeza", "dende", "A", 3, tb=["surprise"], note="Forme finale, Dende tué (ressuscité) (ch. 304)")
fight(762.887, "freezer", "freeza", ["piccolo", "gohan", "krillin"], "A", 3, note="Forme finale (ch. 304-305)")
fight(762.888, "freezer", "freeza", "vegeta", "A", 3, note="Vegeta tué (ressuscité ch. ~329) (ch. 305-308)")
fight(762.89, "freezer", "freeza", "goku", "A", 1, ta=["retenue"], tb=["boost"],
      note="Freezer à 50 % ; Kaiōken x20 puis Genki Dama sans effet décisif (ch. 307-316)")
fight(762.891, "freezer", "freeza", "piccolo", "A", 3, ta=["surprise"], note="Rayon dans le torse (ch. 316)")
fight(762.892, "freezer", "freeza", "krillin", "A", 3, note="Krilin explosé (ressuscité) (ch. 317)")
fight(762.90, "freezer", "goku", "freeza", "A", 2, tb=["boost"],
      note="Goku Super Saiyan contre Freezer à 100 %, coupé en deux par son propre disque (ch. 318-326)")

# ============================================================== Trunks contre Freezer (764)
fight(764.399, "retourfreezer", "trunks", "soldats_freezer", "A", 3, note="(ch. 331)")
fight(764.40, "retourfreezer", "trunks", "freeza", "A", 3, note="Freezer mécanisé tranché (ch. 331)")
fight(764.401, "retourfreezer", "trunks", "king_cold", "A", 3, note="(ch. 332)")
fight(764.41, "retourfreezer", "goku", "trunks", "D", ta=["retenue"], tb=["retenue"],
      note="Test : Goku Super Saiyan arrête du doigt l'épée de Trunks Super Saiyan (ch. 333-334)", flags="i")

# ============================================================== cyborgs et Cell (767)
fight(767.360, "cyborgs", "android_20", "yamcha", "A", 3, ta=["surprise"], note="Main dans la poitrine de Yamcha (ch. 339)")
fight(767.361, "cyborgs", "android_19", "goku", "A", 1, tb=["malade"],
      note="La maladie du cœur se déclare, Goku absorbé en partie (ch. 340-341)")
fight(767.362, "cyborgs", "vegeta", "android_19", "A", 3, note="Premier Super Saiyan de Vegeta (ch. 342-343)")
fight(767.363, "cyborgs", "piccolo", "android_20", "A", 2, note="Gero s'enfuit (ch. 344)")
fight(767.37, "cyborgs", "android_17", "android_20", "A", 3, ta=["surprise"], note="C-17 décapite Gero (ch. 350)")
fight(767.371, "cyborgs", "android_18", "vegeta", "A", 2, note="(ch. 352-353)")
fight(767.372, "cyborgs", ["android_17", "android_18"], ["trunks", "tien", "piccolo"], "A", 3,
      note="C-16 reste spectateur (ch. 353-354)", flags="e")
fight(767.381, "cyborgs", "piccolo", "cell", "A", 1, note="Ginger Town ; Cell s'enfuit au Taiyōken (ch. 362-364)", flags="i")
fight(767.39, "cyborgs", "piccolo", "android_17", "D", note="Égalité, Cell intervient (ch. 367-369)", flags="i")
fight(767.391, "cyborgs", "cell", "piccolo", "A", 3, tb=["epuise"], note="(ch. 369-370)")
fight(767.392, "cyborgs", "android_16", "cell", "A", 2, note="C-16 domine, Cell lui échappe (ch. 371-372)", flags="i")
fight(767.393, "cyborgs", "cell", "android_17", "A", 2, tb=["surprise"],
      note="C-17 absorbé par surprise pendant que C-16 est à terre, pas un vrai duel (ch. 372-373)", flags="?")
fight(767.395, "cyborgs", "cell", "android_16", "A", 2, note="Cell semi-parfait (ch. 374)")
fight(767.396, "cyborgs", "cell", "tien", "A", 2, tb=["boost"],
      note="Le Shin Kikōhō retarde Cell mais Tenshinhan s'effondre (ch. 375-376)")
fight(767.401, "cyborgs", "vegeta", "cell", "A", 3, note="Super Vegeta (ch. 377-381)")
fight(767.402, "cyborgs", "vegeta", "trunks", "A", 2, tb=["surprise"],
      note="Vegeta abat Trunks pour laisser Cell absorber C-18 (ch. ~381)", flags="?")
fight(767.404, "cyborgs", "cell", "vegeta", "A", 2, note="Cell parfait encaisse le Final Flash (ch. 383-384)")
fight(767.405, "cyborgs", "cell", "trunks", "A", 2, ta=["retenue"],
      note="Trunks en Super Saiyan musculeux trop lent, abandonne (ch. 385-387)")
fight(767.45, "cyborgs", "cell", "armee", "A", 3, note="(ch. 392)")

# ============================================================== Cell Game (767)
fight(767.500, "cellgame", "cell", "mr_satan", "A", 3, ta=["retenue"], note="Satan projeté contre la falaise (ch. 396)")
fight(767.501, "cellgame", "cell", "goku", "A", 1, note="Goku abandonne (ch. 397-403)")
fight(767.502, "cellgame", "cell", "gohan", "A", 2, ta=["retenue"], tb=["retenue"], note="(ch. 404-406)")
fight(767.503, "cellgame", "cell", "android_16", "A", 3, tb=["epuise"], note="Tête de C-16 écrasée (ch. 406-407)")
fight(767.504, "cellgame", "cell_jr", ["piccolo", "vegeta", "trunks", "krillin", "tien", "yamcha"], "A", 2,
      note="Les Cell juniors (ch. 407)")
fight(767.506, "ssj2", "gohan", "cell_jr", "A", 3, note="Super Saiyan 2 (ch. 408)")
fight(767.507, "ssj2", "gohan", "cell", "A", 3, note="Cell recrache C-18, se fait exploser ; Goku meurt (ch. 409-412)")
fight(767.510, "ssj2", "cell", "trunks", "A", 3, tb=["surprise"], note="Trunks tué (ressuscité ch. 418) (ch. 413)")
fight(767.511, "ssj2", "cell", "vegeta", "A", 3, note="Gohan perd un bras en protégeant Vegeta (ch. 414)")
fight(767.512, "ssj2", "gohan", "cell", "A", 1, ta=["epuise"],
      note="Kamehameha père-fils, Vegeta distrait Cell (ch. 415-417)")

# ============================================================== futur de Trunks (767)
fight(767.60, "ssj2", "trunks", ["android_17_futur", "android_18_futur"], "A", 3, note="(ch. 419)")
fight(767.61, "ssj2", "trunks", "cell_futur", "A", 3, note="(ch. 419-420)")

# ============================================================== Majin Buu (774)
fight(774.29, "buu", "videl", "criminels", "A", 3, note="(ch. 421)")
fight(774.291, "buu", "gohan", "criminels", "A", 3, ta=["retenue"], note="Great Saiyaman (ch. 423-425)")
fight(774.301, "buu", "trunks_kid", "goten", "A", 1, note="Finale junior (ch. 433-435)")
fight(774.302, "buu", "trunks_kid", "mr_satan", "A", 3, ta=["retenue"], note="Exhibition (ch. 436)")
fight(774.303, "buu", "krillin", "pintar", "A", 3, note="(ch. 439)")
fight(774.304, "buu", "spopovich", "videl", "A", 3, note="(ch. 441)")
fight(774.305, "buu", ["spopovich", "yamu"], "gohan", "A", 2, tb=["surprise"],
      note="Énergie de Gohan volée (ch. 443-444)", flags="?")
# Babidi fait exploser Spopovich par magie (ch. ~447) : exécution d'un serviteur, pas un combat, retiré.
fight(774.307, "buu", "vegeta", "pui_pui", "A", 3, note="(ch. 449)")
fight(774.308, "buu", "goku", "yakon", "A", 3, note="Yakon explose en absorbant la lumière (ch. 450-451)")
fight(774.309, "buu", "dabura", ["krillin", "piccolo"], "A", 3, ta=["surprise"], note="Pétrifiés (ch. ~452)")
fight(774.31, "buu", "dabura", "gohan", "D", note="Interrompu par Babidi (ch. 452-454)", flags="i")
fight(774.311, "buu", "android_18", ["goten", "trunks_kid"], "A", 1,
      note="Mighty Mask démasqué et disqualifié (ch. 452-453)", flags="?")
fight(774.315, "buu", "vegeta", "goku", "D", tb=["retenue"],
      note="Majin Vegeta (puissance accrue par la magie de Babidi) contre Goku SSJ2 qui cache le SSJ3 ; il assomme Goku par surprise (ch. 456-463)", flags="i")
fight(774.319, "buu", "majin_buu", "supreme_kai", "A", 3, note="(ch. 460-461)")
fight(774.320, "buu", "majin_buu", "gohan", "A", 3, note="Gohan laissé pour mort (ch. 461-462)")
fight(774.321, "buu", "majin_buu", "dabura", "A", 3, note="Dabura changé en biscuit (ch. 462-463)")
fight(774.324, "buu", "vegeta", ["goten", "trunks_kid"], "A", 3, ta=["surprise"], note="Assommés (ch. ~465)")
fight(774.325, "buu", "majin_buu", "vegeta", "A", 2,
      note="Autodestruction de Vegeta, Buu se régénère (Vegeta ressuscité) (ch. 464-467)")
fight(774.330, "buu", "goku", "majin_buu", "D", note="Super Saiyan 3, Goku s'arrête (ch. 474-476)", flags="i")
fight(774.331, "buu", "majin_buu", "babidi", "A", 3, note="(ch. 475)")
fight(774.335, "buu", "majin_buu", "criminels", "A", 3, note="Les tireurs qui ont blessé Bee (ch. ~482)", flags="?")
fight(774.34, "superbuu", "super_buu", "majin_buu", "A", 2, note="Le Buu maléfique absorbe le gros Buu (ch. 485-486)")
fight(774.345, "superbuu", "super_buu", "gotenks", "A", 2, tb=["retenue"], note="Salle de l'Esprit et du Temps, Gotenks normal puis SSJ (ch. ~489-491)")
fight(774.347, "superbuu", "gotenks", "super_buu", "A", 1, note="Gotenks SSJ3 domine jusqu'à la défusion (ch. 494-496)", flags="i")
fight(774.350, "superbuu", "gohan", "super_buu", "A", 2, note="Buu absorbe Gotenks et Piccolo par ruse (ch. 497-500)", flags="i")
fight(774.352, "superbuu", "super_buu", "gohan", "A", 2, note="(ch. 500-501)")
fight(774.354, "superbuu", "goku", "super_buu", "D", note="2e revue : Goku SSJ3 coupe Super Buu en deux au Kienzan, Buu se reforme ; Goku juge la fusion seule issue, Buu absorbe Gohan (ch. 502)", flags="i?")
fight(774.36, "superbuu", "vegito", "super_buu", "A", 3, note="Vegito se laisse absorber (ch. 503-506)")
fight(774.37, "superbuu", "goku", "kid_buu", "D", ta=["retenue"], note="Goku SSJ3 contre Buu originel (ch. 510-511)", flags="i")
fight(774.371, "superbuu", "kid_buu", "vegeta", "A", 3, note="(ch. 512-513)")
fight(774.372, "superbuu", "kid_buu", "majin_buu", "A", 2, note="(ch. 513-514)")
fight(774.38, "superbuu", "goku", "kid_buu", "A", 2, ta=["emprunt"], note="Genki Dama de l'énergie de toute la Terre (ch. 515-516)")

# ============================================================== 28e Championnat (784)
fight(784.5, "epilogue", "goku", "uub", "D", ta=["retenue"], note="Goku part entraîner Uub (ch. 518-519)", flags="i")
