"""Statuts officiels et hiérarchies canon de My Hero Academia (manga de Horikoshi ch. 1-430, Ultra Analysis).
t = années depuis le ch. 1 ; échelle de tiers du docstring de data.py (4 top 10, 5 numéros 1-2, 6 All Might déclinant /
Star and Stripe / All For One, 7 All Might à son apogée / Shigaraki fusionné).
Le Hero Billboard Chart JP compte aussi la popularité et le nombre d'affaires résolues : poids modéré (écart-type 0,6-0,8).
Le classement final du ch. 430 (huit ans après la guerre, Mirio n°1) tombe hors des arcs du modèle : non utilisé.
"""

STATUS = [
    # Classement d'avant Kamino (ch. 1-108)
    ("all_might", 1.0, 6.0, 0.6, "Héros n°1, le Symbole de la paix, depuis des décennies (ch. 1-2, 47)"),
    ("endeavor", 1.05, 4.8, 0.6, "Héros n°2, jamais parvenu à dépasser All Might (ch. 31, 47)"),
    ("hawks", 1.3, 4.5, 0.7, "Héros n°3 à 22 ans, avant Kamino (ch. 185-186)"),
    ("best_jeanist", 1.3, 4.3, 0.6, "Héros n°4 (ch. 44-46)"),
    ("edgeshot", 1.3, 4.2, 0.6, "Héros n°5 (ch. 84-85)"),
    ("gang_orca", 1.4, 3.8, 0.7, "Héros n°10, examinateur de la licence provisoire (ch. 108-109)"),
    ("mt_lady", 1.05, 2.8, 0.8, "Débutante classée 23e, surtout pour sa popularité (ch. 1, 44)"),
    # Classement de fin d'année après la retraite d'All Might (ch. 185-186)
    ("endeavor", 1.62, 5.0, 0.6, "Héros n°1 après la retraite d'All Might (Hero Billboard Chart JP, ch. 185)"),
    ("hawks", 1.62, 4.8, 0.6, "Héros n°2 (Hero Billboard Chart JP, ch. 185)"),
    ("best_jeanist", 1.62, 4.3, 0.7, "Héros n°3, absent car blessé à Kamino (Hero Billboard Chart JP, ch. 185)"),
    ("edgeshot", 1.62, 4.3, 0.6, "Héros n°4 (Hero Billboard Chart JP, ch. 185)"),
    ("mirko", 1.62, 4.3, 0.6, "Héroïne n°5 (Hero Billboard Chart JP, ch. 185)"),
    ("crust", 1.62, 4.1, 0.6, "Héros n°6 (Hero Billboard Chart JP, ch. 185)"),
    ("kamui", 1.62, 3.8, 0.7, "Héros n°7 (Hero Billboard Chart JP, ch. 185)"),
    ("ryukyu", 1.62, 3.7, 0.7, "Héroïne n°10 (Hero Billboard Chart JP, ch. 185)"),
    # Statuts d'entrée et de profession (poids faible : écart-type 0,8)
    ("deku", -0.001, 0.0, 0.5, "Collégien sans Alter, comme 20 % de la population (ch. 1)"),
    ("bakugo", 0.8, 2.0, 0.8, "Premier de l'examen d'entrée de Yuei, 77 points de combat (ch. 3-6)"),
    ("todoroki", 0.95, 2.1, 0.8, "Admis sur recommandation à Yuei (ch. 5, 24)"),
    ("aizawa", 0.97, 3.3, 0.6, "Héros pro, professeur principal de la classe 1-A, seul contre la foule de l'USJ (ch. 5, 14-15)"),
    ("cementoss", 1.2, 3.0, 0.8, "Héros pro, professeur de Yuei (ch. 62)"),
    ("ectoplasm", 1.2, 3.0, 0.8, "Héros pro, professeur de Yuei (ch. 62)"),
    ("present_mic", 1.2, 2.8, 0.8, "Héros pro, professeur de Yuei (ch. 62)"),
    ("midnight", 1.2, 2.8, 0.8, "Héroïne pro, professeure de Yuei (ch. 62)"),
    ("snipe", 1.2, 2.8, 0.8, "Héros pro, professeur de Yuei (ch. 62)"),
    ("thirteen", 0.97, 2.8, 0.8, "Héros pro, professeur de Yuei (ch. 14)"),
    # Autres titres
    ("star", 2.2, 6.0, 0.6, "Héroïne n°1 des États-Unis, élève d'All Might (ch. 329-331)"),
    ("all_might", -6.0, 7.0, 0.5, "All Might à son apogée, le plus fort héros de l'histoire (ch. 2, 89)"),
    ("mirio", 1.45, 4.0, 0.7, "Aizawa et Sir Nighteye : l'élève le plus proche du n°1, au-dessus de bien des pros (ch. 122-123)"),
    ("nighteye", 1.45, 3.7, 0.8, "Ancien acolyte d'All Might, héros pro de premier plan (ch. 124-125)"),
    ("afo", 1.31, 6.0, 0.6, "Le seigneur du monde souterrain, que seul All Might a pu affronter (ch. 86-92)"),
]

NUMERIC = {}
NUMERIC_TRANSFORM = {}

ORDER = [
    ("all_might", 1.0, "endeavor", 1.05, 1.0, 0.6,
     "Endeavor reconnaît qu'il n'a jamais pu rattraper All Might, même déclinant (ch. 31, 47, 95)"),
    ("all_might", -6.0, "afo", -6.0, 0.2, 0.6,
     "All Might à son apogée l'emporte de justesse sur All For One, au prix d'une blessure mortelle (ch. 59, 89)"),
    ("shigaraki", 2.3, "afo", 2.3, 0.3, 0.7,
     "All For One : Tomura, fusionné à lui, est destiné à le surpasser comme seigneur des démons (ch. 306-308, 340-343)"),
    ("gigantomachia", 1.72, "dabi", 1.72, 1.0, 0.7,
     "La Ligue entière ne vient pas à bout de Gigantomachia en plusieurs semaines (ch. 220-223)"),
    ("endeavor", 1.65, "hawks", 1.65, 0.3, 0.6,
     "Hawks reconnaît Endeavor comme n°1 et n'aurait pu abattre seul le Nomu encapuchonné (ch. 186-191)"),
]
