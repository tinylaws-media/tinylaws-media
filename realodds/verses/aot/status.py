"""Statuts officiels et hiérarchies canon (manga d'Isayama ch. 1-139 et guides officiels).
t = années depuis la chute du mur Maria (845 = 0) ; échelle de tiers du docstring de data.py
(1 recrue / Titan pur, 3 élite, 4 Mikasa adulte / Mâchoire / Charrette, 5 Titans de combat, 6 Livaï, 8+ Originel).
"""

STATUS = [
    # Bataillon d'exploration
    ("levi", 5.0, 6.0, 0.5, "Livaï, « le soldat le plus fort de l'humanité », vaut à lui seul une brigade (ch. 19-20, ch. 26)"),
    ("levi", 9.0, 6.0, 0.6, "Livaï, toujours « le plus fort de l'humanité » quatre ans plus tard (ch. 100-105)"),
    ("mike", 5.1, 3.6, 0.5, "Chef d'escouade Mike Zacharias, deuxième soldat du Bataillon après Livaï (ch. 35, guide officiel)"),
    ("mikasa", 4.9, 3.6, 0.6, "Major de la 104e brigade, talent jamais vu selon les instructeurs (ch. 3-4)"),
    ("petra", 5.1, 2.8, 0.5, "Escouade d'opérations spéciales choisie par Livaï, élite du Bataillon (ch. 20-28)"),
    ("oruo", 5.1, 2.8, 0.5, "Escouade d'opérations spéciales, 39 Titans tués (ch. 20-28)"),
    ("eld", 5.1, 2.8, 0.5, "Escouade d'opérations spéciales, second de Livaï (ch. 20-28)"),
    ("gunther", 5.1, 2.7, 0.5, "Escouade d'opérations spéciales (ch. 20-28)"),
    ("hange", 5.1, 2.5, 0.6, "Chef d'escouade, puis 14e major du Bataillon (ch. 20, ch. 84)"),
    ("erwin", 5.1, 2.4, 0.7, "13e major du Bataillon, stratège plus que combattant (ch. 22-27)"),
    ("jean", 4.9, 1.6, 0.6, "6e de la promotion de la 104e brigade (ch. 3-4)"),
    ("connie", 4.9, 1.4, 0.6, "8e de la promotion de la 104e brigade (ch. 3-4)"),
    ("sasha", 4.9, 1.4, 0.6, "9e de la promotion de la 104e brigade (ch. 3-4)"),
    ("historia", 4.9, 1.2, 0.6, "10e de la promotion, place offerte par Ymir (ch. 3-4, ch. 40)"),
    ("gabi", 8.9, 1.2, 0.5, "Meilleure des candidats guerriers, désignée héritière du Cuirassé ; aucun pouvoir de Titan (ch. 91-93)"),
    ("falco", 8.9, 0.8, 0.6, "Candidat guerrier sans pouvoir de Titan (ch. 91-93)"),
    # Titans des guerriers
    ("reiner", 5.2, 4.8, 0.6, "Titan Cuirassé, guerrier de Mahr (ch. 42-46)"),
    ("annie", 5.1, 5.0, 0.6, "Titan Féminin, guerrière de Mahr, capable d'imiter les autres Titans (ch. 23-31, ch. 95)"),
    ("bertholdt", 5.8, 5.3, 0.6, "Titan Colossal, puissance d'une explosion (ch. 77-78)"),
    ("zeke", 5.8, 5.6, 0.5, "Titan Bestial, chef des guerriers ; projectiles et contrôle des Titans purs par le sang royal (ch. 35, 76-80, 92)"),
    ("zeke", 9.0, 5.5, 0.5, "Titan Bestial, chef des guerriers ; son bombardement coule la flotte du Moyen-Orient (ch. 92, ch. 100-104)"),
    ("marcel", -0.02, 3.5, 0.7, "Titan Mâchoire, guerrier de Mahr, dévoré sous forme humaine par surprise (ch. 95)"),
    ("hannes", 0.0, 1.0, 0.6, "Chef d'escouade de la Garnison de Shiganshina (ch. 1-2)"),
    ("porco", 8.9, 4.3, 0.6, "Titan Mâchoire, le plus rapide des Neuf (ch. 91-92)"),
    ("pieck", 8.9, 3.8, 0.6, "Titan Charrette, endurance et armement plus que combat (ch. 91-92)"),
    ("lara", 9.0, 5.0, 0.6, "Titan Marteau d'armes, détenu par la famille Tybur (ch. 101-103)"),
    ("armin", 9.0, 5.0, 0.7, "Titan Colossal hérité de Bertolt (ch. 102)"),
    ("falco", 9.3, 4.0, 0.8, "Titan Mâchoire ailé (ch. 133-134)"),
    # Titan Originel
    ("eren", 9.2, 8.5, 0.5, "Titan Originel : contrôle de tous les Eldiens et Titans, Grondement de tous les Titans des murs (ch. 122-131)"),
    ("uri", -24.0, 6.0, 0.8, "Uri Reiss, Titan Originel avec le sang royal (ch. 69)"),
    ("frieda", 0.0, 4.5, 0.8, "Frieda Reiss, Titan Originel, encore inexpérimentée (ch. 62-63, ch. 121)"),
    ("kenny", -24.0, 5.0, 0.6, "Kenny l'Éventreur, légende de la capitale, tueur de plus de cent membres de la Brigade spéciale (ch. 57, ch. 69)"),
    ("kenny", 5.4, 5.0, 0.6, "Capitaine de l'escouade anti-personnel de la Brigade spéciale (ch. 57-65)"),
]

NUMERIC = {}
NUMERIC_TRANSFORM = {}

ORDER = [
    ("levi", 5.1, "mike", 5.1, 1.5, 0.6, "Livaï, le plus fort de l'humanité, Mike seulement deuxième (ch. 19-20, ch. 35)"),
    ("levi", 5.1, "mikasa", 5.1, 0.6, 0.6, "Livaï au-dessus de Mikasa, qu'il doit protéger face au Titan Féminin (ch. 30-31)"),
    ("levi", 5.8, "mikasa", 5.8, 0.4, 0.6, "Livaï, le plus fort de l'humanité (ch. 72-82)"),
    ("mikasa", 5.8, "levi", 5.8, -1.2, 0.5, "Mikasa, Ackerman éveillée comme Livaï : Kenny explique leur force commune (ch. 68-69) ; elle suit Livaï contre le Cuirassé et le Bestial (ch. 75-82)"),
    ("mikasa", 9.0, "levi", 9.0, -0.8, 0.5, "Mikasa et Livaï, les deux Ackerman, fer de lance de l'Alliance jusqu'à la nuque d'Eren (ch. 103-104, ch. 134-138)"),
    ("uri", -24.0, "kenny", -24.0, 1.0, 0.6, "Uri maîtrise Kenny sans effort et l'épargne (ch. 69)"),
    ("eren", 9.2, "zeke", 9.2, 2.5, 0.6, "Le Titan Originel commande à tous les Eldiens, Zeke compris (ch. 120-123)"),
    ("eren", 9.2, "levi", 9.2, 2.0, 0.6, "Le Grondement : aucun soldat ne peut l'arrêter ; il écrase le monde à 80 % (ch. 123-139)"),
    ("eren", 9.3, "levi", 9.3, 1.5, 0.7, "L'Alliance ne l'arrête qu'avec l'aide des anciens détenteurs libérés et parce qu'Eren voulait être arrêté (ch. 137-139)"),
    ("eren", 9.1, "gabi", 9.1, 3.0, 0.5, "Gabi ne tue Eren que d'un tir surprise ; une enfant soldate sans pouvoir de Titan (ch. 119-120)"),
    ("sasha", 9.0, "gabi", 9.0, 0.5, 0.6, "Sasha, vétérane du Bataillon, abattue par surprise par une enfant (ch. 105)"),
    ("zeke", 5.8, "reiner", 5.8, 0.4, 0.6, "Zeke, chef des guerriers, Titan Bestial au-dessus du Cuirassé (ch. 76-80, 92)"),
    # rangs de la 104e brigade (ch. 3-4) : Mikasa 1re, Eren 5e, Jean 6e, Connie 8e, Sasha 9e, Historia 10e
    ("mikasa", 4.9, "eren", 4.9, 0.8, 0.6, "Mikasa 1re, Eren 5e de la 104e brigade (ch. 3-4)"),
    ("eren", 4.9, "jean", 4.9, 0.1, 0.5, "Eren 5e, Jean 6e de la 104e brigade (ch. 3-4)"),
    ("jean", 4.9, "connie", 4.9, 0.1, 0.5, "Jean 6e, Connie 8e de la 104e brigade (ch. 3-4)"),
    ("connie", 4.9, "sasha", 4.9, 0.05, 0.5, "Connie 8e, Sasha 9e de la 104e brigade (ch. 3-4)"),
    ("sasha", 4.9, "historia", 4.9, 0.1, 0.5, "Sasha 9e, Historia 10e de la 104e brigade (ch. 3-4)"),
]
