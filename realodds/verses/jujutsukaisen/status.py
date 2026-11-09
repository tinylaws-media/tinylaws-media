"""Statuts officiels et classements canon (manga d'Akutami, JJK 0 et fanbook officiel).
t = années depuis que Yuji avale le doigt de Sukuna (juin 2018 = 0) ; échelle de tiers du docstring de data.py
(1 grade 4, 2 grade 2, 3 grade 1, 4 grade spécial humain, 5 fléau de grade spécial de haut niveau, 6 Sukuna partiel / Toji,
7 Gojo / Sukuna à pleine puissance). Grade 3 = 1.5, semi-grade 1 = 2.7.
"""

STATUS = [
    # Grade spécial / titres
    ("gojo", 0.0, 7.0, 0.4, "Exorciste de grade spécial, « le plus fort » (ch. 1-2, ch. 14-15)"),
    ("gojo", -11.5, 6.8, 0.6, "« Je suis le plus fort » : éveil après le combat contre Toji (ch. 75-76)"),
    ("sukuna", 0.6, 7.3, 0.4, "Ryomen Sukuna, le Roi des fléaux, à pleine puissance (ch. 1, ch. 212-236)"),
    ("sukuna", -1000.0, 7.3, 0.5, "Sukuna, le plus fort exorciste de l'âge d'or de Heian (ch. 1, ch. 228)"),
    ("yuta", -1.0, 4.0, 0.5, "Exorciste de grade spécial après la Nuit des cent démons (JJK 0, ch. 4)"),
    ("yuta", 0.45, 4.2, 0.5, "Exorciste de grade spécial, l'un des quatre (ch. 137, ch. 179)"),
    ("geto", -1.0, 4.0, 0.5, "Exorciste maudit de grade spécial (JJK 0, ch. 1-4)"),
    ("yuki", 0.5, 4.0, 0.5, "Exorciste de grade spécial (ch. 77, ch. 137, ch. 204-208)"),
    # Fléaux de grade spécial
    ("jogo", 0.3, 4.8, 0.6, "Fléau de grade spécial (fléau calamiteux) (ch. 14-15, ch. 116)"),
    ("hanami", 0.3, 4.8, 0.6, "Fléau de grade spécial (fléau calamiteux) (ch. 14-15, ch. 46-53)"),
    ("dagon", 0.3, 4.6, 0.7, "Fléau de grade spécial (fléau calamiteux) (ch. 108-113)"),
    ("mahito", 0.2, 4.6, 0.7, "Fléau de grade spécial (fléau calamiteux) (ch. 19-30, ch. 120-126)"),
    ("kurourushi", 0.5, 4.2, 0.8, "Fléau de grade spécial (cafard) du jeu d'abattage (ch. 154)"),
    ("fleau_detention", 0.04, 4.0, 0.8, "Fléau de grade spécial du centre de détention (ch. 6-9)"),
    ("fleau_yasohachi", 0.29, 4.0, 0.8, "Fléau de grade spécial porteur de doigt, pont Yasohachi (ch. 55-59)"),
    ("choso", 0.3, 4.0, 0.7, "Peinture de la mort n° 1, objet maudit de grade spécial (ch. 60-62)"),
    ("eso", 0.3, 3.0, 0.9, "Peinture de la mort n° 2, objet maudit de grade spécial (ch. 60-62)"),
    ("kechizu", 0.3, 2.8, 0.9, "Peinture de la mort n° 3, objet maudit de grade spécial (ch. 60-62)"),
    # Grade 1 et semi-grade 1
    ("nanami", 0.1, 3.0, 0.5, "Exorciste de grade 1 (ch. 18-20)"),
    ("mei_mei", 0.25, 3.0, 0.5, "Exorciste de grade 1 (ch. 32, ch. 98)"),
    ("todo", 0.25, 3.0, 0.5, "Exorciste de grade 1, élève de Kyoto (ch. 32-36)"),
    ("kusakabe", 0.35, 3.0, 0.6, "Exorciste de grade 1, « le plus fort sans technique héritée » (ch. 82, ch. 225)"),
    ("naobito", 0.4, 3.2, 0.6, "Chef du clan Zen'in, exorciste de grade spécial 1 (ch. 93-94, ch. 110)"),
    ("naoya", 0.45, 3.0, 0.6, "Exorciste de grade spécial 1 du clan Zen'in (ch. 138, ch. 150)"),
    ("ogi", 0.45, 3.0, 0.7, "Exorciste de grade 1, membre du Hei du clan Zen'in (ch. 149-150)"),
    ("toge", 0.25, 2.7, 0.6, "Exorciste de semi-grade 1 (ch. 17, ch. 47)"),
    ("noritoshi", 0.25, 2.7, 0.6, "Exorciste de semi-grade 1, élève de Kyoto (ch. 32-38)"),
    ("mechamaru", 0.25, 2.7, 0.7, "Exorciste de semi-grade 1, élève de Kyoto (ch. 32, ch. 74)"),
    # Grades 2 à 4
    ("megumi", 0.0, 2.0, 0.6, "Exorciste de grade 2 dès son entrée à l'école (ch. 2)"),
    ("panda", 0.25, 2.0, 0.6, "Exorciste de grade 2 (ch. 17)"),
    ("momo", 0.25, 2.0, 0.6, "Exorciste de grade 2, élève de Kyoto (ch. 32)"),
    ("ino", 0.35, 2.2, 0.7, "Exorciste de grade 2 candidat au grade 1 (ch. 87, ch. 199)"),
    ("nobara", 0.05, 1.5, 0.6, "Exorciste de grade 3 (ch. 4-5)"),
    ("mai", 0.25, 1.5, 0.6, "Exorciste de grade 3, élève de Kyoto (ch. 32)"),
    ("miwa", 0.25, 1.5, 0.6, "Exorciste de grade 3, élève de Kyoto (ch. 32)"),
    ("maki", 0.25, 1.5, 1.0, "Exorciste de grade 4, grade bloqué par le clan Zen'in malgré sa force (ch. 17, ch. 32)"),
]

NUMERIC = {}
NUMERIC_TRANSFORM = {}

ORDER = [
    ("gojo", 0.35, "hakari", 0.35, 1.5, 0.8, "Gojo : « Hakari et Okkotsu… ils seront aussi forts que moi un jour » (monologue de Gojo ; récap : ch. 114)"),
    ("gojo", 0.35, "yuta", 0.35, 1.5, 0.8, "Gojo : Okkotsu et Hakari atteindront un jour son niveau (monologue de Gojo ; récap : ch. 114)"),
    ("hakari", 0.45, "yuta", 0.45, 0.3, 0.8, "Yuta : quand il est lancé, Hakari est plus fort que moi (jeu d'abattage, ch. 146 selon récap)"),
    ("gojo", -11.5, "geto", -11.5, 1.0, 0.7, "Geto constate que Gojo est devenu « le plus fort », seul (ch. 76-77)"),
    ("gojo", 0.05, "jogo", 0.05, 1.5, 0.6, "Geto (Kenjaku) prévient Jogo qu'il ne peut pas battre Gojo (ch. 14-15)"),
    ("sukuna", 0.35, "jogo", 0.35, 1.5, 0.6, "Sukuna (15 doigts) : « Tu es fort, Jogo », après l'avoir surclassé (ch. 116-117)"),
    ("gojo", 0.0, "megumi", 0.0, 1.5, 0.5, "Gojo, le plus fort, est le professeur de Megumi, grade 2 (ch. 2-3)"),
    # ---- audit
    ("gojo", 0.6, "sukuna", 0.6, -0.4, 0.5, "Gojo vs Sukuna (corps de Megumi, 20 doigts) : duel des plus forts, au fil du rasoir ; « Je gagnerais » (ch. 221) mais Sukuna l'emporte (ch. 236)"),
    ("sukuna", 0.6, "gojo", 0.6, -0.4, 0.5, "Gojo vs Sukuna : quasi-égalité au sommet, Sukuna ne gagne que grâce à l'adaptation de Mahoraga (ch. 223-236)"),
    ("sukuna", 0.6, "sukuna", 0.3555, 0.5, 0.5, "Sukuna à 20 doigts et Dix Ombres au-dessus du Sukuna à 15 doigts dans le corps de Yuji, qui n'était pas à pleine puissance (ch. 116-117, ch. 212-221)"),
]
