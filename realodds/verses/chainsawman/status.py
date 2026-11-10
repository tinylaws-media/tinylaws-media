"""Statuts officiels et classements canon (manga de Fujimoto, ch. 1-232).
t = années depuis l'entrée de Denji à la Sécurité publique ; échelle de tiers du docstring de data.py
(3 hybride notable, 4 hybride d'élite / Kishibe / Quanxi, 5 démon de premier plan, 6 démons primordiaux et Cavaliers,
7 Pochita / Cavaliers au sommet). Pas de chiffres officiels de puissance : NUMERIC vide.
"""

STATUS = [
    # Sécurité publique
    ("makima", 0.2, 6.3, 0.7, "Chef de la Division spéciale 4 de la Sécurité publique, qui tue à distance (ch. 2, ch. 26-27)"),
    ("makima", 0.82, 6.6, 0.5, "Démon du Contrôle, l'un des quatre Cavaliers de l'Apocalypse (ch. 84-85)"),
    ("kishibe", 0.24, 4.3, 0.5, "Capitaine de la Division spéciale 1, présenté comme le plus fort chasseur de démons de la Sécurité publique (ch. 28-30)"),
    ("quanxi", 0.6, 4.6, 0.5, "« La première chasseuse de démons », envoyée par la Chine ; Kishibe la tient pour l'une des meilleures au corps à corps (ch. 55-61)"),
    ("himeno", 0.2, 2.6, 0.6, "Chasseuse de démons vétérane, partenaire d'Aki (ch. 10-25)"),
    ("aki", 0.1, 2.5, 0.6, "Chasseur de démons de la Division 4, trois ans d'expérience (ch. 3-14)"),
    ("yoshida", 1.6, 3.9, 0.7, "Chasseur de démons privé (contrat avec la Pieuvre), garde rapproché de Denji pour la Sécurité publique (ch. 101-150)"),
    # Hybrides et assassins
    ("reze", 0.4, 4.0, 0.6, "Hybride de la Bombe, arme secrète formée par l'Union soviétique (ch. 46-52)"),
    ("santa", 0.6, 3.9, 0.6, "Santa Claus, assassin allemande parmi les plus redoutées (ch. 55-57)"),
    ("katana_man", 0.2, 3.0, 0.6, "Hybride du Sabre, petit-fils du yakuza vendu par Denji (ch. 22-23)"),
    # Démons majeurs
    ("demon_fusil", 0.76, 5.8, 0.6, "Démon du Fusil : 1,2 million de morts en cinq minutes en 1997 (ch. ~16, ch. 75-77)"),
    ("tenebres", 0.635, 6.4, 0.5, "Démon des Ténèbres, démon primordial (peur jamais nommée) vivant en Enfer (ch. 64-65)"),
    ("pochita", 0.82, 6.6, 0.6, "Le Démon Chainsaw, « héros de l'Enfer » craint par les démons ; les démons qu'il mange disparaissent (ch. 84-85)"),
    ("chute", 1.57, 6.0, 0.5, "Démon de la Chute, démon primordial (ch. 123-131)"),
    ("vieillissement", 1.675, 6.1, 0.6, "Démon du Vieillissement, démon primordial (ch. 173-190)"),
    # Cavaliers
    ("yoru", 1.5, 4.0, 0.7, "Démon de la Guerre très affaibli : Chainsaw Man a mangé une part d'elle avec les armes nucléaires (ch. 98-99)"),
    ("fami", 1.65, 4.6, 0.8, "Démon de la Famine, l'une des quatre Cavaliers, qui combat par contrats et démons affamés (ch. 112-158)"),
    ("mort", 1.755, 6.3, 0.7, "Démon de la Mort, aînée des Cavaliers et le démon le plus redouté (ch. 196-199)"),
    ("nayuta", 1.555, 4.4, 0.8, "Nayuta, Démon du Contrôle réincarné, encore enfant (ch. 97, ch. 119-120)"),
]

NUMERIC = {}
NUMERIC_TRANSFORM = {}

ORDER = [
    ("makima", 0.81, "kishibe", 0.81, 2.0, 0.6, "Kishibe sait qu'il ne peut pas tuer Makima ; seul Chainsaw Man en est capable (ch. ~83-85)"),
    ("pochita", 0.82, "denji", 0.82, 1.8, 0.6, "Le vrai Chainsaw Man, sans commune mesure avec Denji, décapite sans blessure les hybrides de Makima (ch. 84-87)"),
    ("pochita", 1.67, "yoru", 1.5, 1.5, 0.6, "Chainsaw Man a mangé une part de la Guerre ; Yoru, affaiblie, veut le vaincre pour se reprendre (ch. 98-99)"),
    ("quanxi", 1.66, "denji", 1.66, 0.3, 0.6, "Quanxi : Chainsaw Man (Denji) est plus faible qu'elle, mais bien plus effrayant (ch. 162)"),
    ("tenebres", 0.635, "santa", 0.62, 1.5, 0.6, "Santa Claus doit sacrifier des poupées en Enfer pour obtenir le pouvoir des Ténèbres (ch. 63-66)"),
    ("mort", 1.755, "fami", 1.755, 1.0, 0.7, "La Mort, aînée des Cavaliers, asservit Famine (ch. 198-199)"),
    ("kishibe", 0.24, "denji", 0.24, 1.0, 0.6, "Denji et Power ne parviennent jamais à toucher Kishibe à l'entraînement ; il les tue à volonté (ch. 30-34)"),
    ("makima", 0.822, "pochita", 0.822, 0.0, 0.3, "Makima vient à bout du vrai Chainsaw Man et s'en empare ; elle prévoyait de le contrôler (ch. 89-90)"),
    ("makima", 0.8, "demon_fusil", 0.76, 0.5, 0.6, "Makima abat le Démon du Fusil réuni presque entier (ch. 75-77)"),
]
