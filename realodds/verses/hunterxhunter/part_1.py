# Hunter x Hunter, partie 1 : tout le manga de Togashi, ch. 1-420 (dernier chapitre paru : ch. 420 « Rencontre »,
# Weekly Shōnen Jump n° 41 de 2026, avant la pause annoncée le 3 sept. 2026). Manga uniquement : pas de combats propres
# à l'anime (Kurapika contre son maître, etc.), pas de films. "fight" est injecté par data.py.
# Sources : Hunterpedia (hunterxhunter.fandom.com, pages d'arc et de chapitre), critiques chapitre par chapitre de
# Comic Watch pour les ch. 411-420, Sportskeeda pour les ch. 409-410. "ch. ~N" = à un ou deux chapitres près.
# Repères de temps (t = années depuis le 287e examen) : examen 0.00-0.04, Zoldyck 0.05, Tour céleste 0.15-0.40,
# York New 0.49-0.52 (1er-10 septembre), Greed Island 0.60-0.75, Fourmis 0.80-1.00, élection 1.10-1.15,
# succession 1.30-1.40 (traversée du Black Whale, jours 1-11).
# Les clones de Pouf sont codés sous "pouf" avec "retenue" (fraction de sa puissance).

CHARS_PART = {
    # ---------------------------------------------------------------- héros
    "gon": ("Gon Freecss", "Héros", 1.0, None, None),
    "killua": ("Killua Zoldyck", "Héros", 1.8, None, None),
    "kurapika": ("Kurapika", "Héros", 1.0, None, None),
    "leorio": ("Leorio Paladiknight", "Héros", 0.8, None, None),
    "biscuit": ("Biscuit Krueger", "Association Hunter", 4.6, None, None),
    "ging": ("Ging Freecss", "Association Hunter", 5.0, None, None),
    # ---------------------------------------------------------------- examen Hunter
    "hisoka": ("Hisoka Morow", "Hisoka", 5.0, None, None),
    "illumi": ("Illumi Zoldyck (Gittarackur)", "Zoldyck", 4.8, None, None),
    "hanzo": ("Hanzo", "Association Hunter", 1.8, None, None),
    "pokkle": ("Pokkle", "Candidats", 0.9, 0.82, None),
    "bodoro": ("Bodoro", "Candidats", 1.0, 0.04, None),
    "ponzu": ("Ponzu", "Candidats", 1.0, 0.81, None),
    "barbon": ("Barbon (Bourbon)", "Candidats", 1.0, 0.025, None),
    "geretta": ("Geretta", "Candidats", 0.9, 0.024, None),
    "tonpa": ("Tonpa", "Candidats", 0.5, None, None),
    "sedokan": ("Sedokan (prisonnier)", "Prisonniers", 0.3, None, None),
    "majitani": ("Majitani (prisonnier)", "Prisonniers", 0.3, None, None),
    "johness": ("Johness l'Éventreur (prisonnier)", "Prisonniers", 0.7, 0.013, None),
    "ancien_examinateur": ("Ancien examinateur défiguré par Hisoka", "Prisonniers", 1.0, 0.013, None),
    "amori": ("Les frères Amori (Amori, Imori, Umori)", "Candidats", 0.7, None, None),
    "candidats": ("Candidats de l'examen (groupe)", "Candidats", 0.6, None, None),
    "netero": ("Isaac Netero", "Association Hunter", 6.0, 0.99, None),
    # ---------------------------------------------------------------- Zoldyck, Tour céleste
    "canary": ("Canary", "Zoldyck", 1.6, None, None),
    "zushi": ("Zushi", "Tour céleste", 1.4, None, None),
    "gido": ("Gido", "Tour céleste", 2.2, None, None),
    "sadaso": ("Sadaso", "Tour céleste", 2.0, None, None),
    "riehlvelt": ("Riehlvelt", "Tour céleste", 2.2, None, None),
    "kastro": ("Kastro", "Tour céleste", 2.8, 0.3, None),
    # ---------------------------------------------------------------- York New
    "chrollo": ("Chrollo Lucilfer", "Brigade fantôme", 5.0, None, None),
    "uvogin": ("Uvogin", "Brigade fantôme", 4.5, 0.505, None),
    "nobunaga": ("Nobunaga Hazama", "Brigade fantôme", 4.2, None, None),
    "feitan": ("Feitan Portor", "Brigade fantôme", 4.5, None, None),
    "phinks": ("Phinks Magcub", "Brigade fantôme", 4.4, None, None),
    "machi": ("Machi Komacine", "Brigade fantôme", 4.0, None, None),
    "shalnark": ("Shalnark", "Brigade fantôme", 3.8, 1.301, None),
    "franklin": ("Franklin Bordeau", "Brigade fantôme", 4.3, None, None),
    "shizuku": ("Shizuku Murasaki", "Brigade fantôme", 4.0, None, None),
    "pakunoda": ("Pakunoda", "Brigade fantôme", 3.8, 0.512, None),
    "kortopi": ("Kortopi", "Brigade fantôme", 3.3, 1.301, None),
    "silva": ("Silva Zoldyck", "Zoldyck", 5.4, None, None),
    "zeno": ("Zeno Zoldyck", "Zoldyck", 5.6, None, None),
    "owl": ("Owl (Bêtes de l'ombre)", "Mafia", 3.0, None, None),
    "betes_ombre": ("Ver, Sangsue, Chien enragé et Porc-épic (Bêtes de l'ombre)", "Mafia", 3.0, 0.502, None),
    "betes_ombre2": ("Les cinq dernières Bêtes de l'ombre", "Mafia", 3.0, 0.503, None),
    "dalzollene": ("Dalzollene", "Nostrade", 1.6, 0.5031, None),
    "squala": ("Squala", "Nostrade", 1.8, 0.51, None),
    "mafia": ("Mafieux et gardes (groupe)", "Mafia", 0.5, None, None),
    "assassins_mafia": ("Tueurs engagés par les Dix Parrains (groupe)", "Mafia", 2.0, None, None),
    "dix_parrains": ("Les Dix Parrains de la mafia", "Mafia", 0.3, 0.508, None),
    "agresseurs_nostrade": ("Agresseurs encapuchonnés de l'épreuve Nostrade", "Mafia", 1.2, None, None),
    # ---------------------------------------------------------------- Greed Island
    "binolt": ("Binolt", "Joueurs de Greed Island", 2.2, None, None),
    "genthru": ("Genthru (Bomber)", "Bomber", 3.6, None, None),
    "sub": ("Sub", "Bomber", 3.0, None, None),
    "bara": ("Bara", "Bomber", 3.0, None, None),
    "jispa": ("Jispa", "Joueurs de Greed Island", 2.4, 0.622, None),
    "puhat": ("Puhat", "Joueurs de Greed Island", 2.0, 0.623, None),
    "alliance_nickes": ("Alliance de Nickes (groupe)", "Joueurs de Greed Island", 2.5, None, None),
    "razor": ("Razor", "Maîtres du jeu", 4.6, None, None),
    "pirates_razor": ("Pirates de Razor (les 14 démons)", "Maîtres du jeu", 2.5, None, None),
    "bopobo": ("Bopobo", "Maîtres du jeu", 2.5, 0.651, None),
    "tsezguerra": ("Tsezguerra", "Joueurs de Greed Island", 3.3, None, None),
    "goreinu": ("Goreinu", "Joueurs de Greed Island", 2.8, None, None),
    "maitre_port": ("Le maître du port", "Maîtres du jeu", 2.5, None, None),
    # ---------------------------------------------------------------- Fourmis-chimères
    "kite": ("Kite", "Association Hunter", 4.3, 0.82, None),
    "fourmis": ("Fourmis-chimères soldats (groupe)", "Fourmis-chimères", 2.3, None, None),
    "zazan": ("Zazan", "Fourmis-chimères", 3.8, 0.88, None),
    "rammot": ("Rammot", "Fourmis-chimères", 2.8, 0.87, None),
    "pitou": ("Neferpitou", "Fourmis-chimères", 6.0, 0.99, None),
    "youpi": ("Menthuthuyoupi", "Fourmis-chimères", 6.0, 0.995, None),
    "pouf": ("Shaiapouf", "Fourmis-chimères", 5.8, 0.995, None),
    "meruem": ("Meruem", "Fourmis-chimères", 7.3, 0.995, None),
    "morel": ("Morel Mackernasey", "Association Hunter", 4.5, None, None),
    "knov": ("Knov", "Association Hunter", 4.3, None, None),
    "knuckle": ("Knuckle Bine", "Association Hunter", 4.0, None, None),
    "shoot": ("Shoot McMahon", "Association Hunter", 3.8, None, None),
    "palm": ("Palm Siberia", "Association Hunter", 3.8, None, None),
    "cheetu": ("Cheetu", "Fourmis-chimères", 3.5, None, None),
    "leol": ("Leol", "Fourmis-chimères", 3.9, 0.92, None),
    "ikalgo": ("Ikalgo", "Fourmis-chimères", 3.0, None, None),
    "ortho": ("Les Ortho (frère et sœur)", "Fourmis-chimères", 3.0, None, None),
    "meleoron": ("Meleoron", "Fourmis-chimères", 3.5, None, None),
    "bloster": ("Bloster", "Fourmis-chimères", 3.5, None, None),
    "welfin": ("Welfin", "Fourmis-chimères", 4.0, None, None),
    # ---------------------------------------------------------------- élection
    "gotoh": ("Gotoh", "Zoldyck", 3.0, 1.11, None),
    "teradein": ("Teradein Neutral", "Association Hunter", 2.5, 1.121, None),
    "hunters": ("Hunters envoyés contre Illumi (groupe)", "Association Hunter", 3.0, None, None),
    # ---------------------------------------------------------------- succession (Black Whale)
    "sayird": ("Sayird", "Kakin", 2.0, None, None),
    "vincent": ("Vincent", "Kakin", 3.0, 1.32, None),
    "bill": ("Bill", "Kakin", 2.6, None, None),
    "tuffdy": ("Tuffdy", "Kakin", 2.5, 1.33, None),
    "camilla": ("Camilla Hui Guo Rou", "Kakin", 1.5, None, None),
    "musse": ("Musse", "Kakin", 2.5, 1.335, None),
    "wolfe": ("Wolfe", "Kakin", 2.2, 1.3351, None),
    "benjamin": ("Benjamin Hui Guo Rou", "Kakin", 3.2, None, None),
    "furykov": ("Furykov", "Kakin", 4.0, None, None),
    "halkenburg": ("Halkenburg Hui Guo Rou", "Kakin", 2.2, None, None),
    "shikaku": ("Shikaku", "Kakin", 3.0, 1.342, None),
    "rihan": ("Rihan", "Kakin", 3.0, None, None),
    "bete_sale_sale": ("Bête gardienne de Salé-salé", "Kakin", 3.0, None, None),
    "yushohi": ("Yushohi", "Kakin", 2.5, None, None),
    "sale_sale": ("Salé-salé Hui Guo Rou", "Kakin", 0.5, 1.341, None),
    "tserriednich": ("Tserriednich Hui Guo Rou", "Kakin", 3.0, None, None),
    "theta": ("Theta", "Kakin", 2.5, None, None),
    "hinrigh": ("Hinrigh Biganduffno", "Xi-Yu", 4.0, None, None),
    "soldats_kakin": ("Soldats et gardes royaux de Kakin (groupe)", "Kakin", 1.2, None, None),
    "padaille": ("Padaille", "Heil-Ly", 2.5, 1.362, None),
    "tevelares": ("Tevelares et Quorolle", "Heil-Ly", 2.2, None, None),
    "zakuro": ("Zakuro Custard", "Cha-R", 2.8, None, None),
    "lynch": ("Lynch Fullbokko", "Cha-R", 2.5, None, None),
    "heil_ly": ("Membres de la famille Heil-Ly (groupe)", "Heil-Ly", 2.0, None, None),
    "luini": ("Luini", "Heil-Ly", 2.5, 1.37, None),
    "gateaume": ("Gateaume (double de Nen)", "Kakin", 2.5, None, None),
    "bille": ("Bille", "Heil-Ly", 2.0, None, None),
    "tassi": ("Tassi", "Xi-Yu", 1.5, 1.375, None),
}

GENERIC_PART = {"candidats", "mafia", "assassins_mafia", "dix_parrains", "agresseurs_nostrade", "alliance_nickes",
                "pirates_razor", "fourmis", "hunters", "soldats_kakin", "heil_ly", "betes_ombre", "betes_ombre2",
                "amori", "tevelares"}

JUMPS_PART = [
    # Gon
    ("gon", 0.30, 1.5, 0.6, "Apprentissage du Nen avec Wing (Tour céleste)"),
    ("gon", 0.66, 1.0, 0.5, "Entraînement de Biscuit à Greed Island"),
    ("gon", 0.86, 0.5, 0.4, "Entraînement pendant l'arc des Fourmis"),
    ("gon", 0.997, -4.0, 1.0, "Perte de son Nen après la transformation adulte (contrainte)"),
    # Killua
    ("killua", 0.30, 1.5, 0.6, "Apprentissage du Nen avec Wing (Tour céleste)"),
    ("killua", 0.66, 1.0, 0.5, "Entraînement de Biscuit à Greed Island"),
    ("killua", 0.925, 0.6, 0.4, "Retrait de l'aiguille d'Illumi"),
    ("killua", 0.94, 0.6, 0.4, "Acquisition de Godspeed (Kanmuru)"),
    # autres
    ("kurapika", 0.30, 2.8, 1.0, "Entraînement de Nen, chaînes et Emperor Time"),
    ("leorio", 0.80, 1.8, 0.8, "Apprentissage du Nen (entre York New et l'élection)"),
    ("hanzo", 0.50, 2.2, 1.0, "Nen appris après l'examen"),
    ("ponzu", 0.50, 1.0, 0.8, "Hunter professionnelle (Nen)"),
    ("pokkle", 0.50, 1.0, 0.8, "Hunter professionnel (Nen)"),
    ("tserriednich", 1.337, 2.0, 1.0, "Éveil et apprentissage fulgurant du Nen avec Theta"),
    ("meruem", 0.993, 0.6, 0.5, "Absorbe les cellules de Youpi et Pouf"),
]

# ================================================================ avant l'histoire (flashbacks)
fight(-13.0, "avant", "uvogin", ["franklin", "shalnark", "chrollo"], "D",
      note="Enfants à Meteor City : Uvogin frappe Shalnark, échange avec Franklin, Chrollo s'enfuit avec la cassette (ch. 395)",
      flags="i")
fight(-2.0, "avant", "hisoka", "kastro", "A", 3, ta=["retenue"], note="Premier duel deux ans plus tôt : Hisoka l'épargne (flashback, ch. ~52)")

# ================================================================ examen Hunter
fight(0.003, "examen", "hisoka", "candidats", "A", 3, note="Massacre dans le brouillard des marais de Numere (ch. 9)")
fight(0.004, "examen", "hisoka", "leorio", "A", 3, ta=["retenue"], note="Leorio assommé, Gon frappe Hisoka à la canne à pêche (ch. 9-10)")
fight(0.008, "examen", "netero", ["gon", "killua"], "A", 3, ta=["retenue"], note="Jeu du ballon dans le dirigeable ; Gon force Netero à utiliser la main droite (ch. 13-14)")
fight(0.0085, "examen", "killua", "candidats", "A", 3, note="Killua tue deux candidats après le jeu du ballon (ch. 14)")
fight(0.012, "examen", "gon", "sedokan", "A", 2, note="Duel des bougies, Tour de la Ruse (ch. 17)")
fight(0.0121, "examen", "kurapika", "majitani", "A", 3, note="Majitani assommé d'un coup (il feignait l'évanouissement) (ch. 18)")
fight(0.0122, "examen", "hisoka", "ancien_examinateur", "A", 3, note="Hisoka le décapite (ch. 19)")
fight(0.0123, "examen", "killua", "johness", "A", 3, note="Killua lui arrache le cœur (ch. 19-20)")
fight(0.02, "examen", ["kurapika", "leorio"], "tonpa", "A", 3, note="Île de Zevil : Tonpa et son partenaire capturés (ch. 26)", flags="e")
fight(0.021, "examen", "illumi", "candidats", "A", 3, note="Gittarackur tue un candidat qui attaquait Hisoka (ch. 27)")
fight(0.022, "examen", "hisoka", "candidats", "A", 3, note="Hisoka tue sa cible pendant que Gon lui vole sa plaque (ch. 27-28)")
fight(0.023, "examen", "hisoka", "geretta", "A", 3, note="Geretta, qui avait empoisonné Gon, tué par Hisoka (ch. 28)")
fight(0.024, "examen", "ponzu", "barbon", "A", 1, note="Barbon meurt, Ponzu reste coincée par ses serpents (ch. 30)")
fight(0.025, "examen", "gon", "ponzu", "A", 2, note="Gaz soporifique dans la grotte (ch. 31)")
fight(0.026, "examen", "killua", "amori", "A", 3, note="Imori puis Amori et Umori dépouillés de leurs plaques (ch. 29)")
fight(0.035, "examen", "hanzo", "gon", "A", 3, ta=["retenue"], note="Hanzo lui casse le bras puis déclare forfait, Gon gagne officiellement (ch. 33-34)")
fight(0.036, "examen", "hisoka", "kurapika", "D", ta=["retenue"], note="Hisoka chuchote et abandonne (ch. 35)", flags="i")
fight(0.037, "examen", "hanzo", "pokkle", "A", 3, note="Pokkle maîtrisé, menacé de torture, abandonne (ch. 35)")
fight(0.038, "examen", "hisoka", "bodoro", "A", 3, ta=["retenue"], note="Bodoro dominé, abandonne après un chuchotement (ch. 35)")
fight(0.039, "examen", "killua", "bodoro", "A", 3, ta=["surprise"], tb=["epuise"], note="Sous l'emprise d'Illumi, Killua tue Bodoro (ch. 36)")

# ================================================================ Zoldyck
fight(0.055, "zoldyck", "canary", "gon", "A", 3, tb=["retenue"], note="Gon refuse de frapper, Canary ne peut plus le frapper (ch. 41)")

# ================================================================ Tour céleste
fight(0.16, "arene", "killua", "zushi", "A", 2, note="Zushi se relève sans cesse ; Killua le sort du ring (ch. 45)")
fight(0.22, "arene", "gido", "gon", "A", 2, note="Gon esquive en Zetsu jusqu'à l'acculement et perd ; Wing lui interdit de combattre deux mois (ch. 50-51)")
fight(0.30, "arene", "hisoka", "kastro", "A", 2, note="Hisoka perce l'astuce du double et tue Kastro (ch. 52-54)")
fight(0.33, "arene", "killua", "sadaso", "A", 3, note="Sadaso déclare forfait sous la menace (ch. 57 ; l'anime le fait abandonner face à Gon)", flags="?")
fight(0.34, "arene", "gon", "gido", "A", 3, note="Revanche : Gon brise sa jambe de métal (ch. 58)")
fight(0.345, "arene", "killua", "riehlvelt", "A", 3, note="Électrocuté par son propre fouet (ch. 59)")
fight(0.346, "arene", "gon", "riehlvelt", "A", 2, note="Fouets enroulés autour du cou, Riehlvelt abandonne (ch. 59)")
fight(0.40, "arene", "hisoka", "gon", "A", 3, ta=["retenue"], note="Victoire 6-2 aux points ; Gon lui rend sa plaque d'un coup de poing (ch. 61-63)")

# ================================================================ York New
fight(0.495, "yorknew", "kurapika", "agresseurs_nostrade", "A", 2, note="Épreuve d'embauche des Nostrade (ch. 67-68)")
fight(0.500, "yorknew", ["feitan", "franklin", "shizuku"], "mafia", "A", 3, note="Massacre de la salle des ventes (ch. 73)")
fight(0.501, "yorknew", "uvogin", "mafia", "A", 3, note="Désert de Gordeau, Uvogin seul contre la mafia (ch. 75)")
fight(0.502, "yorknew", "uvogin", "betes_ombre", "A", 3, tb=["surprise"],
      note="Ver, Sangsue, Chien enragé, Porc-épic tués ; les sangsues l'empoisonnent (ch. 75-76)")
fight(0.5025, "yorknew", "kurapika", "uvogin", "A", 2, ta=["surprise"], tb=["epuise"],
      note="Chain Jail : Kurapika enlève Uvogin paralysé par le poison (ch. 77)")
fight(0.5026, "yorknew", "owl", "nobunaga", "A", 1, ta=["surprise"], note="Fun Fun Cloth enveloppe la voiture (ch. 77)", flags="i")
fight(0.503, "yorknew", ["phinks", "feitan", "machi"], ["betes_ombre2", "owl"], "A", 3,
      note="La Brigade anéantit en une nuit les cinq Bêtes restantes, Owl capturé (ch. 78 ; membres exacts non précisés)", flags="?")
fight(0.5031, "yorknew", "phinks", "dalzollene", "A", 3, note="Phinks tue Dalzollene en libérant Uvogin (ch. 78)")
fight(0.505, "yorknew", "kurapika", "uvogin", "A", 2, ta=["prepa", "contre"],
      note="Duel en tête-à-tête : Chain Jail puis Judgment Chain, Uvogin meurt (ch. 80-81)")
fight(0.506, "yorknew", ["phinks", "pakunoda"], ["gon", "killua"], "A", 3, note="Gon et Killua capturés (ch. 91)")
fight(0.5061, "yorknew", ["gon", "killua"], "nobunaga", "D", note="Ils s'échappent en défonçant les murs (ch. 93)", flags="i")
fight(0.507, "yorknew", "chrollo", "assassins_mafia", "A", 3, note="Tueurs engagés par les Dix Parrains (ch. 96-97)")
fight(0.5071, "yorknew", ["nobunaga", "phinks", "feitan", "franklin", "shizuku", "machi", "shalnark"], "mafia", "A", 3,
      note="Quelque 2 000 mafieux et policiers devant l'immeuble du cimetière (ch. 97)")
fight(0.5072, "yorknew", "chrollo", ["silva", "zeno"], "D",
      note="Chrollo coincé ; les Zoldyck s'arrêtent quand la mort des Dix Parrains rend le contrat caduc (ch. 98-99)", flags="i")
fight(0.508, "yorknew", "illumi", "dix_parrains", "A", 3, ta=["surprise"], note="Illumi élimine les Dix Parrains (ch. 100)")
fight(0.509, "yorknew", ["chrollo", "machi", "shizuku"], ["gon", "killua"], "A", 3, note="Nouvelle capture (ch. 111)")
fight(0.5095, "yorknew", "nobunaga", "squala", "A", 3, ta=["surprise"], note="Nobunaga décapite Squala qui menaçait Pakunoda (ch. 112)")
fight(0.5096, "yorknew", ["machi", "nobunaga"], ["gon", "killua"], "A", 3, note="Évasion manquée pendant la panne (ch. 113)")
fight(0.5097, "yorknew", "kurapika", "chrollo", "A", 2, ta=["surprise", "prepa"],
      note="Panne provoquée, la chaîne attrape Chrollo (ch. 113-114)")
fight(0.5098, "yorknew", "shizuku", "nobunaga", "A", 2, ta=["surprise"], note="Shizuku assomme Nobunaga pour faire respecter la règle (ch. 115)")

# ================================================================ Greed Island
fight(0.62, "greedisland", "biscuit", "binolt", "A", 3, tb=["surprise"], note="Binolt l'attaque en embuscade (ch. 137)")
fight(0.621, "greedisland", ["gon", "killua"], "binolt", "A", 2, note="Il abandonne au 10e jour de la poursuite (ch. 138-139)", flags="e")
fight(0.622, "greedisland", "genthru", "jispa", "A", 3, tb=["surprise"], note="Little Flower (ch. 142)")
fight(0.623, "greedisland", "genthru", "puhat", "A", 3, note="(ch. 143)")
fight(0.624, "greedisland", ["genthru", "sub", "bara"], "alliance_nickes", "A", 3, ta=["prepa"],
      note="Bombe de Countdown : seuls Abengane et Cuzco survivent (ch. 144)")
fight(0.625, "greedisland", "razor", ["phinks", "feitan", "nobunaga", "shalnark", "franklin", "shizuku", "kortopi"], "D",
      ta=["retenue"], note="Razor expulse la Brigade, Phinks fait sauter le bateau (ch. 144-145)", flags="i")
fight(0.626, "greedisland", "killua", "maitre_port", "A", 3, note="Killua quitte le jeu pour l'examen (ch. 145)")
fight(0.63, "greedisland", "killua", "candidats", "A", 3, note="288e examen Hunter (ch. 148)")
fight(0.645, "greedisland", "killua", "bopobo", "A", 2, note="Anneau de feu (ch. 155)")
fight(0.65, "greedisland", ["gon", "killua", "biscuit", "hisoka", "goreinu", "tsezguerra"], "pirates_razor", "A", 3,
      note="Revanche aux sports contre les pirates (ch. 159-160)")
fight(0.651, "greedisland", "razor", "bopobo", "A", 3, note="Bopobo tué d'une balle de Nen (ch. 160)")
fight(0.655, "greedisland", ["gon", "killua", "hisoka", "biscuit", "goreinu", "tsezguerra"], "razor", "A", 1, tb=["retenue"],
      note="Balle au prisonnier : Gon frappe avec la balle relancée par Killua et Hisoka (ch. 161-168)")
fight(0.70, "greedisland", "tsezguerra", "genthru", "D", note="Escarmouches sans issue (ch. 171)", flags="i")
fight(0.73, "greedisland", "biscuit", "bara", "A", 3, ta=["boost"], note="Vraie forme, un seul coup (ch. 177)")
fight(0.731, "greedisland", "killua", "sub", "A", 2, note="Yo-yo et électricité (ch. 178)")
fight(0.732, "greedisland", "gon", "genthru", "A", 1, ta=["prepa"],
      note="Gon sacrifie sa main gauche, essence et Jajanken (ch. 176-181)")

# ================================================================ Fourmis-chimères
fight(0.80, "fourmis", ["zazan", "fourmis"], ["pokkle", "ponzu"], "A", 3, note="Ponzu tuée, Pokkle capturé (ch. ~190)")
fight(0.805, "fourmis", ["gon", "killua"], "rammot", "A", 2, note="Rammot récupéré par Colt (ch. 191)", flags="e")
fight(0.81, "fourmis", ["kite", "gon", "killua"], "fourmis", "A", 3, note="Escouade de Yunju (ch. 192-193)")
fight(0.811, "fourmis", ["kite", "gon", "killua"], "fourmis", "A", 3, note="Escouade de Hagya, Silent Waltz de Kite (ch. 194-196)")
fight(0.82, "fourmis", "pitou", "kite", "A", 3, ta=["surprise"], tb=["protege"],
      note="Pitou tranche le bras de Kite, Killua emmène Gon ; Kite tué (ch. 198-200)")
fight(0.84, "fourmis", ["netero", "morel", "knov"], "fourmis", "A", 3, note="Assaut contre la base de NGL (ch. ~206)")
fight(0.85, "fourmis", "knuckle", "gon", "A", 3, ta=["retenue"], note="Premier affrontement (ch. ~206)")
fight(0.86, "fourmis", "knuckle", "gon", "A", 2, note="Duel aux plaquettes : Gon en faillite d'aura (ch. ~210)")
fight(0.861, "fourmis", "shoot", "killua", "A", 2, note="Killua fuit, inhibé par l'aiguille d'Illumi (ch. ~211-212)")
fight(0.87, "fourmis", "killua", "rammot", "A", 3, note="Rammot tué (ch. ~218-219)")
fight(0.875, "fourmis", ["knuckle", "morel"], "cheetu", "D", note="Cheetu s'enfuit (ch. ~220-221)", flags="ie")
fight(0.88, "fourmis", "feitan", "zazan", "A", 2, note="Pain Packer : Rising Sun (ch. ~224-229)")
fight(0.89, "fourmis", "gon", "fourmis", "A", 3, note="Officiers et soldats de l'ex-escouade de Meleoron (ch. ~231-233)")
fight(0.90, "fourmis", "killua", "ikalgo", "A", 2, note="Killua épargne Ikalgo (ch. ~238)")
fight(0.901, "fourmis", "killua", "ortho", "A", 1, ta=["prepa"], note="Fléchettes : Killua feint la mort et les décapite, grièvement blessé ; Ikalgo l'emporte (ch. 239-241)")
fight(0.91, "fourmis", "morel", "cheetu", "D", note="Cheetu marque Morel, pas de vainqueur (ch. ~244)", flags="i")
fight(0.911, "fourmis", "morel", "cheetu", "A", 2, ta=["prepa"], note="Prison de fumée (ch. ~247)")
fight(0.92, "fourmis", "morel", "leol", "A", 2, ta=["prepa"], note="Église abandonnée, Leol asphyxié au CO2 (ch. ~248-254)")
fight(0.93, "fourmis", "netero", "pitou", "A", 2, ta=["surprise"],
      note="Dragon Dive de Zeno : Netero projette Pitou au loin (ch. ~263-265)", flags="i")
fight(0.931, "fourmis", "knuckle", "youpi", "D", ta=["surprise"], note="Knuckle frappe Youpi dans l'escalier du palais (ch. ~265-266)", flags="i")
fight(0.932, "fourmis", "pouf", "morel", "A", 2, note="Pouf aspire le Nen de Morel (ch. ~270)", flags="i")
fight(0.933, "fourmis", "youpi", "shoot", "A", 3, note="Shoot presque tué, Knuckle intervient (ch. ~272)")
fight(0.94, "fourmis", "knuckle", "youpi", "A", 1, note="Youpi paralysé, Knuckle cogne puis fuit (ch. 281)", flags="i")
fight(0.941, "fourmis", "killua", "youpi", "D", ta=["boost"], note="Godspeed ; à court d'électricité, Killua s'éclipse (ch. 281)", flags="i")
fight(0.942, "fourmis", "ikalgo", "bloster", "A", 2, ta=["prepa"], note="Bloster endormi par sédatif (ch. ~279-283)")
fight(0.95, "fourmis", "youpi", ["morel", "knuckle"], "A", 1, ta=["boost"],
      note="Morel blessé ; Youpi part avec Pouf quand Knuckle relâche son Nen (ch. ~284-289)", flags="ie")
fight(0.96, "fourmis", "ikalgo", "welfin", "A", 1, note="Ikalgo tire sur Welfin, qui survit (ch. ~294)", flags="i")
fight(0.961, "fourmis", "palm", "pouf", "A", 3, tb=["retenue"], note="Palm tue un mini-clone de Pouf (ch. ~294)")
fight(0.97, "fourmis", "meruem", "netero", "A", 2,
      note="Zero Hand impuissant ; Netero déclenche la Poor Man's Rose et meurt (ch. ~290-298)")
fight(0.98, "fourmis", "knuckle", "pouf", "A", 2, tb=["retenue"], note="Clone de Pouf détruit, APR transféré au corps principal (ch. ~301)")
fight(0.981, "fourmis", "killua", "pouf", "A", 3, tb=["retenue"], note="Clone écrasé, Komugi sauvée (ch. ~302-305)")
fight(0.99, "fourmis", "gon", "pitou", "A", 3, ta=["boost"],
      note="Transformation adulte ; Pitou tué, Gon perd son bras droit à cause de Terpsichora (ch. 305-307)")
fight(0.991, "fourmis", "meruem", ["knuckle", "meleoron"], "A", 3, note="Assommés tous les deux (ch. 308)")

# ================================================================ élection
fight(1.10, "election", "leorio", "ging", "A", 1, ta=["surprise"], tb=["retenue"], note="Un coup de poing téléporté (ch. 325)", flags="i")
fight(1.105, "election", "illumi", "killua", "D", ta=["prepa"], note="Collision provoquée, Killua fuit en Godspeed (ch. 326)", flags="i")
fight(1.11, "election", "hisoka", "gotoh", "A", 3, note="Gotoh décapité, Canary et Amane s'enfuient (ch. 327)")
fight(1.12, "election", "illumi", "hunters", "A", 3, ta=["prepa"], note="Les marionnettes à aiguilles tuent plus de cent Hunters, dont Bushidora (ch. 329-330)")
fight(1.121, "election", "hisoka", "teradein", "A", 3, note="(ch. 330)")

# ================================================================ guerre de succession
fight(1.30, "succession", "chrollo", "hisoka", "A", 2, ta=["prepa"],
      note="Tour céleste : marionnettes et bombes, Hisoka meurt puis se ranime grâce au Bungee Gum (ch. 352-357)")
fight(1.301, "succession", "hisoka", ["shalnark", "kortopi"], "A", 3, ta=["surprise"], note="Les deux tués (ch. 357)")
fight(1.3011, "succession", "hisoka", "machi", "A", 3, ta=["retenue"], note="Machi ligotée et épargnée comme messagère (ch. 357)")
fight(1.31, "succession", "kurapika", "sayird", "A", 3, ta=["contre"], note="Steal Chain, Sayird arrêté (ch. 361)")
fight(1.32, "succession", ["kurapika", "bill"], "vincent", "A", 2, ta=["contre", "boost"],
      note="Steal Chain sous Emperor Time ; Vincent se suicide au poison (ch. 364)")
fight(1.33, "succession", "hanzo", "tuffdy", "A", 3, ta=["surprise", "prepa"], note="Le meurtrier de Momoze étranglé, suicide maquillé (ch. 372)")
fight(1.335, "succession", "camilla", "musse", "A", 1, ta=["contre"],
      note="Abattue, Camilla ressuscite par Cat's Name et Musse meurt (ch. ~374-376)")
fight(1.3351, "succession", "camilla", "wolfe", "A", 3, ta=["contre"], note="(ch. ~374-376)")
fight(1.3352, "succession", ["benjamin", "furykov"], "camilla", "A", 2, note="La bête de Benjamin arrête les balles, Furykov la maîtrise (ch. ~375-376)")
fight(1.34, "succession", "rihan", "bete_sale_sale", "A", 3, note="Predator dévore la bête gardienne (ch. 381)")
fight(1.3401, "succession", "halkenburg", "shikaku", "A", 2, ta=["prepa"], note="La flèche perce le Culdcept et brise sa volonté (ch. 382)")
fight(1.3402, "succession", "yushohi", "sale_sale", "A", 3, ta=["surprise"], note="(ch. 382)")
fight(1.345, "succession", "tserriednich", "theta", "A", 2, ta=["contre"], note="La balle traverse une illusion, Theta s'évanouit (ch. 386)")
fight(1.346, "succession", "tserriednich", "theta", "A", 2, ta=["contre"], note="Esquive par prescience, Theta tenue en joue (ch. 387)")
fight(1.36, "succession", "hinrigh", "soldats_kakin", "A", 3, note="Canons changés en serpents, deux soldats tués (ch. 390)")
fight(1.3601, "succession", "zakuro", "heil_ly", "A", 2, note="Bloody Mary (ch. 390)")
fight(1.361, "succession", "hinrigh", "padaille", "A", 3, note="(ch. 391)")
fight(1.3611, "succession", "hinrigh", "tevelares", "D", note="Tevelares et Quorolle s'enfuient (ch. 391)", flags="i")
fight(1.362, "succession", "hisoka", "lynch", "A", 3, note="Contre réflexe (ch. 392)")
fight(1.363, "succession", "nobunaga", "luini", "A", 3, note="(ch. 393)")
fight(1.3631, "succession", "hisoka", ["zakuro", "lynch"], "A", 3, ta=["retenue"], note="Tous deux assommés, Hisoka disparaît (ch. 393)")
fight(1.364, "succession", "hinrigh", "gateaume", "D", note="Le double blessé à la cuisse disparaît (ch. 394)", flags="i")
fight(1.3641, "succession", "bille", "tassi", "A", 3, ta=["surprise"], note="(ch. 394)")
fight(1.39, "succession", "tserriednich", "benjamin", "D", ta=["prepa"],
      note="Benjamin croit l'abattre ; c'était une mise en scène de Tserriednich (ch. 416-418)", flags="i")
fight(1.395, "succession", "tserriednich", "soldats_kakin", "A", 3, note="Fuite à travers le navire en état de siège (ch. 419)")
fight(1.396, "succession", "hisoka", "soldats_kakin", "A", 3, note="Gardes de Tserriednich tranchés au casino (ch. 420)")
fight(1.397, "succession", "hisoka", "tserriednich", "A", 2, ta=["retenue"],
      note="Tserriednich se voit tué en vision ; Hisoka le laisse filer (ch. 420)", flags="i")
