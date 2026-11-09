"""Statuts officiels et classements canon (manga de Gotōge ch. 1-205 et fanbooks officiels).
t = années depuis le massacre de la famille Kamado ; échelle de tiers du docstring de data.py
(3 Lunes inférieures / Tsuguko, 4 Pilier, 5 Lunes supérieures 4 à 6, 6 Lunes supérieures 1 à 3, 7 Muzan / Yoriichi).
"""

STATUS = [
    # Piliers (réunion des Piliers, ch. 44-46)
    ("giyu", 2.21, 4.0, 0.4, "Pilier de l'Eau (réunion des Piliers, ch. 44-46)"),
    ("shinobu", 2.21, 3.9, 0.5, "Pilier de l'Insecte (réunion des Piliers, ch. 44-46)"),
    ("rengoku", 2.21, 4.1, 0.4, "Pilier de la Flamme (réunion des Piliers, ch. 44-46)"),
    ("tengen", 2.21, 4.0, 0.4, "Pilier du Son (réunion des Piliers, ch. 44-46)"),
    ("mitsuri", 2.21, 4.0, 0.4, "Pilier de l'Amour (réunion des Piliers, ch. 44-46)"),
    ("muichiro", 2.21, 4.0, 0.5, "Pilier de la Brume, devenu Pilier deux mois après avoir pris le sabre (ch. 44-46, ch. 118)"),
    ("gyomei", 2.21, 4.8, 0.4, "Pilier du Rocher (réunion des Piliers, ch. 44-46)"),
    ("gyomei", 2.7, 5.0, 0.5, "Pilier du Rocher, reconnu comme le plus fort des pourfendeurs (entraînement des Piliers, ch. 134-135)"),
    ("sanemi", 2.21, 4.0, 0.4, "Pilier du Vent (réunion des Piliers, ch. 44-46)"),
    ("iguro", 2.21, 4.0, 0.4, "Pilier du Serpent (réunion des Piliers, ch. 44-46)"),
    ("kanae", -2.0, 4.0, 0.5, "Pilier de la Fleur avant sa mort face à Doma (ch. 142-143)"),
    ("shinjuro", -5.0, 4.0, 0.6, "Ancien Pilier de la Flamme (ch. 55-56, ch. 68)"),
    ("urokodaki", -45.0, 4.0, 0.7, "Ancien Pilier de l'Eau, a capturé le démon aux mains il y a 47 ans (ch. 7-8)"),
    # Tsuguko
    ("kanao", 2.21, 3.0, 0.6, "Tsuguko de Shinobu Kocho (ch. 45, ch. 162)"),
    ("mitsuri", 1.5, 3.2, 0.8, "Ancienne Tsuguko de Kyojuro Rengoku (ch. 99-100, fanbook)"),
    # Rang Mizunoto
    ("tanjiro", 2.0, 1.0, 0.6, "Reçu à la Sélection finale, rang Mizunoto (le plus bas) (ch. 7-8)"),
    ("zenitsu", 2.0, 1.0, 0.6, "Reçu à la Sélection finale, rang Mizunoto (ch. 7-8, ch. 21)"),
    ("inosuke", 2.0, 1.0, 0.6, "Reçu à la Sélection finale, rang Mizunoto (ch. 7-8, ch. 21)"),
    ("genya", 2.0, 1.0, 0.7, "Reçu à la Sélection finale, rang Mizunoto (ch. 7-8)"),
    # Lunes supérieures (numérotation de Muzan)
    ("kokushibo", 2.8, 6.5, 0.4, "Lune supérieure 1 (ch. 98, ch. 163-176)"),
    ("doma", 2.8, 6.2, 0.4, "Lune supérieure 2 (ch. 98, ch. 141-163)"),
    ("akaza", 2.35, 6.0, 0.4, "Lune supérieure 3 (ch. 63-66, ch. 98)"),
    ("akaza", 2.8, 6.0, 0.4, "Lune supérieure 3 (ch. 147-157)"),
    ("hantengu", 2.6, 5.4, 0.5, "Lune supérieure 4 (ch. 98, ch. 106-126)"),
    ("gyokko", 2.6, 5.1, 0.5, "Lune supérieure 5 (ch. 98, ch. 108-122)"),
    ("gyutaro", 2.5, 4.9, 0.5, "Lune supérieure 6, le vrai pouvoir du duo avec Daki (ch. 81-97)"),
    ("daki", 2.5, 4.4, 0.8, "Lune supérieure 6 (rang partagé, la plus faible du duo) (ch. 70-97)"),
    ("kaigaku", 2.8, 4.4, 0.7, "Nouvelle Lune supérieure 6, promue depuis peu après la mort de Gyutaro (ch. 144-145)"),
    ("nakime", 2.8, 4.6, 0.9, "Nouvelle Lune supérieure 4, gardienne du château, non combattante (ch. 98, ch. 140)"),
    # Lunes inférieures
    ("enmu", 2.35, 3.3, 0.6, "Lune inférieure 1 (ch. 52-63)"),
    ("rui", 2.2, 3.0, 0.6, "Lune inférieure 5 (ch. 34-43)"),
    ("lunes_inferieures", 2.3, 3.0, 0.6, "Lunes inférieures 2 à 6, exécutées par Muzan (ch. 51-52)"),
    ("kyogai", 2.13, 2.5, 0.7, "Ancienne Lune inférieure 6, déchue par Muzan (ch. 24-25)"),
    # Muzan, Yoriichi
    ("muzan", 2.8, 7.3, 0.4, "Muzan Kibutsuji, le premier démon et roi des démons (ch. 13-14, ch. 183-204)"),
    ("muzan", -400.0, 7.3, 0.5, "Muzan Kibutsuji, roi des démons à l'ère Sengoku (ch. 186-187)"),
    ("yoriichi", -400.0, 8.5, 0.5, "Yoriichi Tsugikuni, le plus fort pourfendeur de l'histoire, créateur de la Respiration du Soleil (ch. 174-177, ch. 186-187)"),
    ("tanjiro_oni", 2.8121, 6.5, 0.8, "Muzan voit en Tanjiro démon le prochain roi des démons, capable de le surpasser (ch. 201-202)"),
]

NUMERIC = {}
NUMERIC_TRANSFORM = {}

ORDER = [
    # Classement officiel de Muzan : Lune supérieure 1 > 2 > 3 > 4 > 5 > 6
    ("muzan", 2.8, "kokushibo", 2.8, 1.5, 0.5, "Muzan, maître absolu des Lunes supérieures ; même empoisonné, il tient seul les Piliers que Kokushibo n'a pu affronter qu'à quatre (ch. 98, ch. 139, ch. 184-191)"),
    ("kokushibo", 2.8, "doma", 2.8, 0.5, 0.6, "Lune supérieure 1 au-dessus de la Lune supérieure 2 (classement de Muzan, ch. 98)"),
    ("doma", 2.8, "akaza", 2.8, 0.4, 0.6, "Doma, entré après Akaza, l'a dépassé au classement (ch. 98, ch. 154-155)"),
    ("akaza", 2.6, "hantengu", 2.6, 0.5, 0.6, "Lune supérieure 3 au-dessus de la Lune supérieure 4 (classement de Muzan, ch. 98)"),
    ("hantengu", 2.6, "gyokko", 2.6, 0.3, 0.6, "Lune supérieure 4 au-dessus de la Lune supérieure 5 (classement de Muzan, ch. 98)"),
    ("gyokko", 2.5, "gyutaro", 2.5, 0.3, 0.6, "Lune supérieure 5 au-dessus de la Lune supérieure 6 (classement de Muzan, ch. 98)"),
    ("akaza", 2.35, "rengoku", 2.35, 1.0, 0.6, "Les Lunes supérieures sont restées invaincues un siècle et ont tué de nombreux Piliers (ch. 63-66, ch. 98)"),
    ("yoriichi", -340.0, "kokushibo", -340.0, 1.2, 0.6, "Kokushibo n'a jamais pu égaler son frère Yoriichi, même âgé de plus de 80 ans (ch. 177-178)"),
    ("yoriichi", -400.0, "muzan", -400.0, 1.5, 0.5, "Muzan terrifié par Yoriichi, le seul à l'avoir mis au bord de la mort (ch. 186-187)"),
    ("yoriichi", -400.0, "muzan", 2.8, 1.0, 0.7, "Quatre siècles plus tard, Muzan n'a toujours pas surmonté la peur de Yoriichi ; Kokushibo le dit sans égal (ch. 175-178, ch. 187)"),
    ("gyomei", 2.7, "sanemi", 2.7, 0.4, 0.8, "Gyomei, le plus fort des Piliers (Tanjiro et Inosuke, ch. 134-135 ; Kokushibo, ch. 168-172)"),
    ("gyomei", 2.7, "giyu", 2.7, 0.5, 0.8, "Gyomei, le plus fort des Piliers (entraînement des Piliers, ch. 134-135)"),
    ("gyomei", 2.7, "iguro", 2.7, 0.5, 0.8, "Gyomei, le plus fort des Piliers (entraînement des Piliers, ch. 134-135)"),
    ("gyomei", 2.7, "muichiro", 2.7, 0.4, 0.8, "Gyomei, le plus fort des Piliers, au-dessus du prodige Muichiro (ch. 134-135, ch. 168-172)"),
    ("gyomei", 2.7, "mitsuri", 2.7, 0.5, 0.8, "Gyomei, le plus fort des Piliers (entraînement des Piliers, ch. 134-135)"),
    ("giyu", 2.8, "shinobu", 2.8, 0.4, 0.8, "Shinobu, la seule Pilier incapable de trancher la tête d'un démon (ch. 141-143)"),
]
