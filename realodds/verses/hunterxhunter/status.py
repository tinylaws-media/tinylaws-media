"""Statuts officiels et classements canon (manga de Togashi uniquement).
t = années depuis le 287e examen Hunter ; échelle de tiers du docstring de data.py
(4 Hunter pro fort / Brigade, 5 Hisoka / Chrollo / Zoldyck adultes, 6 Gardes royaux / Netero âgé, 7 Meruem / Netero au sommet).
"""

STATUS = [
    # Association Hunter
    ("netero", 0.0, 6.0, 0.6, "Président de l'Association Hunter, examinateur final de l'examen 287 (ch. 9, ch. 31-34)"),
    ("netero", 0.8, 6.0, 0.5, "Président Netero, choisi pour affronter seul le roi Meruem (ch. 198, ch. 257)"),
    ("netero", -50.0, 7.0, 0.7, "Netero à son apogée il y a un demi-siècle, le plus fort du monde selon la narration (ch. 316-317)"),
    ("ging", 1.1, 5.5, 0.6, "Hunter double étoile et Zodiaque (Sanglier) ; Netero : l'un des cinq meilleurs utilisateurs de Nen au monde (ch. 320-337, arc de l'élection)"),
    ("biscuit", 0.6, 4.6, 0.6, "Hunter double étoile (Hunter de pierres précieuses), maîtresse de Gon et Killua (ch. 126-128)"),
    ("morel", 0.8, 4.4, 0.7, "Hunter pro choisi par Netero pour l'assaut du palais (ch. 198-199)"),
    ("knov", 0.8, 4.2, 0.7, "Hunter pro choisi par Netero pour l'assaut du palais (ch. 198-199)"),
    ("knuckle", 0.8, 3.8, 0.8, "Hunter pro, disciple de Morel, recruté pour l'invasion des Fourmis (ch. 201)"),
    ("shoot", 0.8, 3.7, 0.8, "Hunter pro, disciple de Morel, recruté pour l'invasion des Fourmis (ch. 201)"),
    ("kite", 0.8, 4.2, 0.8, "Hunter pro, disciple de Ging (ch. 186-188)"),
    ("tsezguerra", 0.6, 3.3, 0.8, "Hunter pro (chasseur de primes) engagé par Battera (ch. 132-136)"),
    ("hanzo", 0.1, 1.8, 0.8, "Ninja reçu au 287e examen Hunter (ch. 33-37)"),
    ("kurapika", 1.3, 4.0, 0.9, "Hunter de la liste noire devenu Zodiaque (Rat), garde du prince Woble (arc de la succession, ch. 340-360)"),
    ("leorio", 1.1, 2.3, 0.8, "Hunter pro débutant en Nen (émission apprise en un an, ch. 325-345) ; son siège de Zodiaque est politique, pas un niveau de puissance"),
    ("razor", 0.6, 4.6, 0.8, "Maître du jeu de Greed Island recruté par Ging (ch. 162-167)"),
    # Brigade fantôme
    ("chrollo", 0.5, 5.0, 0.6, "Chef (n° 0) de la Brigade fantôme (ch. 64-120)"),
    ("uvogin", 0.5, 4.2, 0.5, "Membre n° 11 de la Brigade fantôme (ch. 64-80)"),
    ("nobunaga", 0.5, 4.0, 0.5, "Membre n° 1 de la Brigade fantôme (ch. 64-120)"),
    ("feitan", 0.5, 4.2, 0.5, "Membre n° 2 de la Brigade fantôme (ch. 64-120)"),
    ("machi", 0.5, 4.0, 0.5, "Membre n° 3 de la Brigade fantôme (ch. 64-120)"),
    ("phinks", 0.5, 4.2, 0.5, "Membre n° 5 de la Brigade fantôme (ch. 64-120)"),
    ("shalnark", 0.5, 3.8, 0.6, "Membre n° 6 de la Brigade fantôme (ch. 64-120)"),
    ("franklin", 0.5, 4.1, 0.5, "Membre n° 7 de la Brigade fantôme (ch. 64-120)"),
    ("shizuku", 0.5, 3.9, 0.5, "Membre n° 8 de la Brigade fantôme (ch. 64-120)"),
    ("pakunoda", 0.5, 3.8, 0.6, "Membre n° 9 de la Brigade fantôme (ch. 64-112)"),
    ("kortopi", 0.5, 3.4, 0.7, "Membre n° 10 de la Brigade fantôme (combat faible, rôle de soutien) (ch. 64-120)"),
    ("hisoka", 0.5, 4.8, 0.7, "Membre n° 4 (faux) de la Brigade fantôme, infiltré pour affronter Chrollo (ch. 64, ch. 117)"),
    # Zoldyck
    ("zeno", 0.5, 5.5, 0.6, "Grand-père de la famille d'assassins Zoldyck, la plus redoutée du monde (ch. 37, ch. 89-91)"),
    ("silva", 0.5, 5.3, 0.6, "Chef de la famille d'assassins Zoldyck (ch. 41-43, ch. 89-91)"),
    ("illumi", 0.0, 4.6, 0.7, "Fils aîné Zoldyck, assassin professionnel et Hunter de l'examen 287 (ch. 33-36)"),
    # Fourmis-chimères
    ("meruem", 0.9, 7.2, 0.5, "Roi des Fourmis-chimères, né pour dominer le monde (ch. 213, ch. 316-318)"),
    ("pitou", 0.85, 6.0, 0.5, "Garde royal du roi (ch. 186-200)"),
    ("youpi", 0.85, 6.0, 0.5, "Garde royal du roi (ch. 213-286)"),
    ("pouf", 0.85, 5.8, 0.5, "Garde royal du roi (ch. 213-286)"),
    ("zazan", 0.8, 3.6, 0.8, "Chef d'escouade des Fourmis-chimères (ch. 190-230)"),
    ("leol", 0.8, 3.7, 0.8, "Chef d'escouade des Fourmis-chimères (ch. 190-230)"),
    ("cheetu", 0.8, 3.4, 0.8, "Chef d'escouade des Fourmis-chimères (ch. 190-230)"),
    # Tour céleste / mafia
    ("gido", 0.2, 2.2, 0.8, "Combattant du 200e étage de la Tour céleste (ch. 48-54)"),
    ("sadaso", 0.2, 2.0, 0.8, "Combattant du 200e étage de la Tour céleste (ch. 48-54)"),
    ("riehlvelt", 0.2, 2.2, 0.8, "Combattant du 200e étage de la Tour céleste (ch. 48-54)"),
    ("kastro", 0.2, 2.8, 0.7, "Candidat Floor Master du 200e étage, ex-adversaire d'Hisoka (ch. 49-55)"),
    ("owl", 0.5, 3.0, 0.8, "Membre des Bêtes de l'ombre, élite des Dix Parrains de la mafia (ch. 75-80)"),
]

NUMERIC = {}
NUMERIC_TRANSFORM = {}

ORDER = [
    ("meruem", 0.95, "netero", 0.95, 1.0, 0.6, "Netero reconnaît que Meruem le dépasse de loin et recourt à la Rose du pauvre (ch. 316-317)"),
    ("meruem", 0.9, "pitou", 0.9, 1.2, 0.6, "Les Gardes royaux se soumettent à l'aura du roi qui dépasse la leur (ch. 213-215)"),
    ("pitou", 0.85, "kite", 0.85, 1.2, 0.7, "Kite juge Pitou hors de sa portée et ordonne à Gon et Killua de fuir (ch. 186)"),
    ("pitou", 0.85, "knov", 0.85, 1.5, 0.8, "Knov s'effondre en percevant l'aura des Gardes royaux : impossible de gagner (ch. 222)"),
    ("netero", 0.85, "morel", 0.85, 1.2, 0.7, "Netero seul est désigné pour le roi, Morel et Knov pour les Gardes (ch. 257)"),
    ("netero", 0.93, "pitou", 0.93, 0.2, 0.6, "Netero seul réservé au roi, les Gardes laissés à Morel et Knov ; il écarte Pitou d'un coup (ch. 257, 263-265)"),
    ("chrollo", 0.6, "hisoka", 0.6, 0.4, 0.8, "Machi : le chef est nettement au-dessus d'Hisoka (ch. 170)"),
    ("illumi", 0.05, "killua", 0.05, 1.5, 0.8, "Killua n'ose pas affronter Illumi et abandonne l'examen (ch. 35-36)"),
    ("netero", 0.0, "gon", 0.0, 1.5, 0.5, "Gon et Killua ne parviennent pas à prendre la balle de Netero (ch. 31-32)"),
    ("morel", 0.85, "knuckle", 0.85, 0.3, 0.6, "Morel, maître de Knuckle et Shoot, choisi avec Knov pour les Gardes royaux (ch. 201, 257)"),
    ("illumi", 1.105, "killua", 1.105, 0.3, 0.5, "Killua fuit en Godspeed plutôt que d'affronter Illumi, qui garde l'ascendant sur son frère (ch. 326)"),
    ("ging", 1.1, "leorio", 1.1, 1.5, 0.7, "Ging, l'un des cinq meilleurs utilisateurs de Nen selon Netero ; Leorio débutant en Nen (ch. 320-345)"),
]
