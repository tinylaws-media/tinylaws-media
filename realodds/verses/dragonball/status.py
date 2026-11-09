"""Preuves officielles de puissance (canon : manga de Toriyama, manga Dragon Ball Super de Toyotarō supervisé par
Toriyama, guides officiels Daizenshuu / Chōzenshū, numéros officiels Weekly Jump / V-Jump de Shūeisha).

STATUS  : (id, t, tier, sd, label) — titre ou rang officiel ramené à l'échelle de tiers de data.py.
NUMERIC : {"puissance": [(id, t, niveau de combat)]} — uniquement les chiffres donnés par le manga ou un guide officiel,
          en état de base (pas de Kaiōken, de charge d'attaque ni d'Ōzaru) ; transformés en log10 par le modèle.
ORDER   : (idA, tA, idB, tB, écart en tiers, sd, label) — déclarations canon « A est plus fort que B ».
Sources vérifiées : Kanzenshuu (kanzenshuu.com/battle-power/databook, relevés du manga par volume), Dragon Ball Wiki.
Temps t = année Age, alignés sur les combats de part_1.py / part_2.py.
"""

STATUS = [
    # Saiyans
    ("bardock", 737.1, 3.3, 0.8, "Guerrier saiyan de classe inférieure (Épisode de Bardock, manga 2011 ; Daizenshuu 7)"),
    ("raditz", 761.80, 3.6, 0.4, "Guerrier saiyan, frère de Goku, 1 500 unités (ch. 195-196 ; Daizenshuu 7)"),
    ("nappa", 762.40, 3.8, 0.4, "Saiyan d'élite, bras droit de Vegeta (ch. 216 ; Daizenshuu 7)"),
    ("vegeta", 762.42, 4.0, 0.3, "Prince des Saiyans, l'étalon du palier « Saiyans à leur arrivée » (ch. 219-220)"),
    # Armée de Freezer
    ("freeza", 762.866, 5.0, 0.5, "Empereur de l'univers, maître de l'armée de Freezer (ch. 245, 285 ; Daizenshuu 7)"),
    ("king_cold", 764.401, 5.0, 0.8, "Roi Cold, père de Freezer, souverain de l'empire (ch. 330-331)"),
    ("ginyu", 762.865, 4.5, 0.5, "Capitaine du Commando Ginyu, unité d'élite de Freezer (ch. 271, 283)"),
    ("recoome", 762.852, 4.3, 0.5, "Membre du Commando Ginyu, troupe d'élite spéciale (ch. 271-277)"),
    ("burter", 762.86, 4.2, 0.5, "Membre du Commando Ginyu, « le plus rapide de l'univers » (ch. 271, 281)"),
    ("jeice", 762.86, 4.2, 0.5, "Membre du Commando Ginyu (ch. 271, 281)"),
    ("guldo", 762.85, 3.6, 0.6, "Membre le plus faible du Commando Ginyu (ch. 271-274)"),
    ("zarbon", 762.83, 4.1, 0.4, "Officier supérieur de Freezer, ~23 000 unités (ch. 251 ; Daizenshuu 7 p. 69)"),
    ("dodoria", 762.811, 4.0, 0.4, "Officier supérieur de Freezer, 22 000 unités (ch. 252 ; Daizenshuu 7 p. 91)"),
    ("cui", 762.805, 3.9, 0.4, "Soldat de Freezer, rival de Vegeta, 18 000 unités (ch. 249 ; Daizenshuu 7 p. 63)"),
    ("soldats_freezer", 762.80, 2.5, 0.8, "Soldats de base de l'armée de Freezer, souvent < 1 500 (Daizenshuu 7 p. 105)"),
    # Dieux et démons
    ("kami", 753.6, 3.0, 0.6, "Kami-sama, dieu de la Terre, moitié bonne de Piccolo Daimaō (ch. 168-170)"),
    ("supreme_kai", 774.31, 5.5, 1.0, "Kaiōshin de l'Est, dieu suprême d'un quart de l'univers (ch. 449-452)"),
    ("dabura", 774.31, 6.0, 0.8, "Dabura, roi du monde des démons (ch. 449-454)"),
    ("zamasu_present", 779.62, 6.0, 1.0, "Zamasu, apprenti Kaiōshin de l'Univers 10 (DBS manga ch. 17-19)"),
    ("beerus", 778.0, 8.5, 0.5, "Beerus, dieu de la destruction de l'Univers 7 (DBS manga ch. 1-4 ; Chōzenshū)"),
    ("whis", 778.0, 10.0, 0.5, "Whis, ange de l'Univers 7, maître de Beerus (DBS manga ch. 1-5)"),
    ("merus", 780.52, 9.5, 0.7, "Merus, apprenti ange infiltré dans la Patrouille galactique (DBS manga ch. 52, 64)"),
    ("jaco", 778.5, 2.0, 1.0, "Jaco, patrouilleur galactique « d'élite » (Jaco the Galactic Patrolman ; DBS manga ch. 43)"),
    # Tournoi du Pouvoir
    ("toppo", 780.0, 8.0, 0.6, "Toppo, chef des Troupes de l'Orgueil et candidat dieu de la destruction (DBS manga ch. 29-30)"),
    ("jiren", 780.0, 9.0, 0.5, "Jiren, ancien candidat dieu de la destruction, puissance « au-delà des dieux » (DBS manga ch. 29-35)"),
    ("pride_troopers", 780.1, 6.0, 0.8, "Troupes de l'Orgueil, gardiens de la justice de l'Univers 11 (DBS manga ch. 33)"),
    ("hit", 779.5, 7.5, 0.8, "Hit, tueur légendaire de l'Univers 6, atout de Champa (DBS manga ch. 8-13)"),
    # Arcs récents
    ("moro", 780.5, 7.0, 1.0, "Moro, « mangeur de planètes » scellé par Kaiōshin, criminel n° 1 de la Patrouille (DBS manga ch. 43-44)"),
    ("granolah", 781.04, 8.5, 0.7, "Granolah, « guerrier le plus fort de l'univers » par vœu aux boules de Cérélia (DBS manga ch. 70)"),
    ("uub", 784.5, 6.5, 1.0, "Uub, réincarnation de Buu originel (ch. 517-519)"),
    # Paliers de transformation qui définissent l'échelle
    ("cell", 767.5, 6.0, 0.4, "Cell parfait, ancre du palier 6 (ch. 396 ; échelle du modèle)"),
    ("gohan", 767.506, 6.0, 0.4, "Gohan Super Saiyan 2, ancre du palier 6 (ch. 408 ; Chōzenshū : SSJ2 = 2 × SSJ)"),
    ("goku", 774.33, 7.0, 0.4, "Goku Super Saiyan 3, ancre du palier 7 (ch. 474 ; guide : SSJ3 = 4 × SSJ2)"),
    ("majin_buu", 774.32, 7.0, 0.4, "Majin Buu, ancre du palier 7 (ch. 460-463)"),
    ("goku", 778.02, 8.0, 0.5, "Goku Super Saiyan God, ancre du palier 8 (DBS manga ch. 4)"),
]

NUMERIC = {"puissance": [
    # Dragon Ball (Daizenshuu 7, p. 82-83 ; Weekly Jump 1989 « Final Warriors »)
    ("goku", 749.0, 10),            # première apparition (Daizenshuu 7)
    ("goku", 753.0, 180),           # 22e Championnat (Daizenshuu 7 ; Weekly Jump 1989, 15 ans)
    ("roshi", 753.0, 139),          # Jackie Chun / Tortue Géniale (Daizenshuu 7 ; scouter de Raditz, vol. 18)
    ("tien", 753.0, 180),           # 22e Championnat (Daizenshuu 7)
    ("tao_pai_pai", 750.3, 210),    # Weekly Jump 1989
    ("goku", 753.56, 260),          # contre Piccolo Daimaō (Daizenshuu 7)
    ("king_piccolo", 753.56, 260),  # Daizenshuu 7 ; Weekly Jump 1989
    ("kami", 756.0, 220),           # Weekly Jump 1989
    ("chi_chi", 756.0, 130),        # Weekly Jump 1989
    ("goku", 756.0, 910),           # 18 ans, 23e Championnat (Weekly Jump 1989)
    # Arrivée des Saiyans (manga vol. 17-19 ; Daizenshuu 7)
    ("krillin", 761.80, 206),       # scouter de Raditz (ch. 194, vol. 17-18)
    ("raditz", 761.80, 1500),       # ch. 196 ; Daizenshuu 7
    ("goku", 761.81, 416),          # lests retirés (ch. 199)
    ("piccolo", 761.81, 408),       # lests retirés (ch. 199)
    ("mr_popo", 762.2, 1030),       # Weekly Jump 1989
    ("saibaman", 762.40, 1200),     # lu par Nappa (ch. 214)
    ("nappa", 762.40, 4000),        # Daizenshuu 7 ; Weekly Jump 1989
    ("krillin", 762.40, 1770),      # Daizenshuu 7
    ("yamcha", 762.40, 1480),       # Daizenshuu 7
    ("chiaotzu", 762.40, 610),      # Daizenshuu 7
    ("tien", 762.40, 1830),         # Daizenshuu 7
    ("piccolo", 762.40, 3500),      # Daizenshuu 7
    ("yajirobe", 762.40, 970),      # Weekly Jump 1989
    ("goku", 762.415, 8000),        # « plus de 8 000 » (ch. 223 ; Daizenshuu 7)
    ("vegeta", 762.42, 18000),      # lu par Dodoria avant la Terre (ch. 252 ; Daizenshuu 7)
    # Namek (manga vol. 21-25 ; Daizenshuu 7 ; V-Jump 1990)
    ("gohan", 762.80, 14000),       # arrivée sur Namek (Daizenshuu 7)
    ("krillin", 762.80, 13000),     # arrivée sur Namek (Daizenshuu 7)
    ("cui", 762.805, 18000),        # Daizenshuu 7 p. 63
    ("vegeta", 762.805, 24000),     # lu par Kiwi (ch. 249, vol. 21)
    ("dodoria", 762.811, 22000),    # Daizenshuu 7 p. 91
    ("zarbon", 762.83, 23000),      # forme normale (Daizenshuu 7 p. 69)
    ("vegeta", 762.84, 30000),      # « près de 30 000 » (vol. 23 ; Daizenshuu 7)
    ("krillin", 762.85, 75000),     # après Guldo (V-Jump n° 1, 1990)
    ("gohan", 762.86, 200000),      # état normal après le Grand Doyen (V-Jump n° 1, 1990)
    ("goku", 762.86, 90000),        # base à l'arrivée, Ginyu (ch. 283, vol. 24 ; Daizenshuu 7)
    ("ginyu", 762.865, 120000),     # pleine puissance déclarée (vol. 24)
    ("nail", 762.866, 42000),       # pleine puissance (ch. 286, vol. 24)
    ("freeza", 762.866, 530000),    # 1re forme (ch. 286, vol. 24)
    ("vegeta", 762.87, 250000),     # après Recoome (V-Jump n° 1, 1990)
    ("freeza", 762.88, 1000000),    # 2e forme « plus d'un million » (ch. 292, vol. 25)
    ("piccolo", 762.882, 1000000),  # fusionné avec Nail, « plus d'un million » (Daizenshuu 7 p. 102)
    ("goku", 762.89, 3000000),      # contre Freezer (Daizenshuu 7)
    ("freeza", 762.89, 60000000),   # forme finale à 50 % (Daizenshuu 7)
    ("freeza", 762.90, 120000000),  # forme finale à 100 % (Daizenshuu 7)
    ("goku", 762.90, 150000000),    # Super Saiyan « plus de 150 millions » (Daizenshuu 7, glossaire)
]}

NUMERIC_TRANSFORM = {"puissance": "log10"}

ORDER = [
    # Dragon Ball
    ("goku", 761.81, "raditz", 761.81, 0.6, 0.4,
     "Goku (416) et Piccolo (408) très loin des 1 500 de Raditz, qui les juge sans chance (ch. 196-199)"),
    ("nappa", 762.40, "raditz", 761.80, 0.4, 0.4,
     "Vegeta et Nappa : Raditz était « un faible » par rapport à eux (ch. 204, 214)"),
    ("vegeta", 762.42, "nappa", 762.40, 0.5, 0.4,
     "Nappa terrifié par Vegeta, qui l'achève d'un geste ; 18 000 contre 4 000 (ch. 227 ; Daizenshuu 7)"),
    ("ginyu", 762.865, "recoome", 762.852, 0.3, 0.4,
     "Ginyu, capitaine, le plus fort du Commando, au-dessus de Recoome (ch. 271-283)"),
    ("freeza", 762.866, "ginyu", 762.865, 0.6, 0.4,
     "Freezer, 530 000 en 1re forme, loin au-dessus de Ginyu (120 000) (ch. 283-286, vol. 24)"),
    ("gohan", 767.506, "goku", 767.5, 0.4, 0.4,
     "Goku : la puissance de Gohan a déjà dépassé la sienne (ch. 402-404)"),
    ("gohan", 767.506, "cell", 767.5, 0.5, 0.4,
     "Gohan Super Saiyan 2 surclasse Cell parfait, dit Goku et constate Cell (ch. 408-409)"),
    ("goku", 774.315, "vegeta", 774.315, 0.5, 0.5,
     "Goku révèle à Majin Vegeta qu'il retenait le Super Saiyan 3 (ch. 474) ; Vegeta : « Kakarot, tu es le numéro un » (ch. 509)"),
    ("goku", 774.37, "vegeta", 774.37, 0.6, 0.4,
     "Vegeta reconnaît que Goku SSJ3 le surpasse : « Tu es le numéro un, Kakarot » (ch. 509)"),
    ("gohan", 774.34, "goku", 774.34, 0.3, 0.6,
     "Le vieux Kaiōshin et Goku : Gohan « Ultime » plus fort que Goku SSJ3 (ch. 499-501) ; Toriyama voulait faire de Gohan le héros"),
    ("majin_buu", 774.319, "supreme_kai", 774.319, 1.5, 0.5,
     "Kaiōshin : Majin Buu a autrefois tué ou absorbé les Kaiōshin, impossible pour lui de le vaincre (ch. 449, 460)"),
    # Dragon Ball Super
    ("whis", 778.0, "beerus", 778.0, 1.5, 0.5,
     "Whis est le maître de Beerus et plus fort que lui, dit Beerus (DBS manga ch. 1-5)"),
    ("beerus", 778.02, "goku", 778.02, 0.5, 0.4,
     "Beerus face à Goku SSG : jamais à pleine puissance, il reste au-dessus (DBS manga ch. 4)"),
    ("beerus", 780.0, "vegeta", 780.0, 0.5, 0.5,
     "Beerus et Whis jugent Goku et Vegeta encore loin d'un dieu de la destruction (DBS manga ch. 27-28)"),
    ("jiren", 780.11, "beerus", 780.0, 0.3, 0.6,
     "Belmod : la puissance de Jiren dépasse celle d'un dieu de la destruction (DBS manga, Tournoi du Pouvoir ch. 29-35)"),
    ("jiren", 780.11, "toppo", 780.11, 0.8, 0.5,
     "Toppo, candidat dieu de la destruction, reconnaît Jiren comme le plus fort de l'Univers 11 (DBS manga ch. 29-35)"),
    ("whis", 780.0, "jiren", 780.11, 1.0, 0.6,
     "Les anges dépassent de loin les dieux de la destruction et les mortels (DBS manga ch. 27-41 ; Chōzenshū)"),
    ("merus", 780.52, "goku", 780.52, 1.0, 0.5,
     "Merus, apprenti ange, entraîne Goku à l'Ultra Instinct en le surclassant (DBS manga ch. 52-53)"),
    ("freeza", 781.251, "goku", 781.251, 0.8, 0.5,
     "Black Freezer met Goku UI et Vegeta Ultra Ego au tapis d'un coup chacun (DBS manga ch. 87)"),
    ("freeza", 781.251, "vegeta", 781.251, 0.8, 0.5,
     "Black Freezer met Vegeta Ultra Ego KO d'un seul coup (DBS manga ch. 87)"),
    ("gohan", 781.6, "goku", 781.6, 0.0, 0.7,
     "Gohan Beast mis au niveau de Goku et Vegeta, voire au-delà (DBS manga ch. 99-101 ; Toriyama, interview Super Hero 2022)"),
]
