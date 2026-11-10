# My Hero Academia, partie 1 : tout le manga de Horikoshi, ch. 1-430 (fin le 4 août 2024 + épilogue), flash-back compris.
# Manga uniquement : pas de combats propres à l'anime, pas de films, pas de Vigilantes. "fight" est injecté par data.py.
# Sources de chapitres : My Hero Academia Wiki (fandom, pages d'arc : Joint Training, Star and Stripe, Paranormal
# Liberation War, Final War), TV Tropes (récapitulatif de la guerre du Paranormal, ch. 267-296), Sportskeeda (ch. 351-353,
# 354-357, 362, 383-385, 403-410), sinon mémoire du manga : "ch. ~N" = à quelques chapitres près.
# Repères de temps (t = années depuis le ch. 1) : vilain de boue 0.00, examen d'entrée 0.80, rentrée et USJ 0.95-0.97,
# festival sportif 1.00, Hosu 1.03-1.05, examens 1.20, camp 1.28, Kamino 1.31, licence 1.40, Deku contre Kacchan 1.42,
# stages et Overhaul 1.45-1.51, festival culturel 1.60, Nomu encapuchonné 1.65, entraînement commun 1.68-1.70,
# Deika 1.72-1.73, stage chez Endeavor 1.80, guerre du Paranormal 1.900-1.902, héros sombre 2.00-2.10,
# Star and Stripe 2.20, guerre finale 2.3000-2.3011 (une seule journée).
# Flash-back : mort de Nana Shimura -30 (All Might adolescent), premier duel All Might / All For One -6 (« il y a
# cinq-six ans », ch. 2, 59, 89) ; dates estimées.
# Bakugo : cœur arrêté par Shigaraki (ch. 362), réparé par Edgeshot, de retour contre All For One (ch. 403) : pas de mort.

CHARS_PART = {
    # ---------------------------------------------------------------- classe 1-A
    "deku": ("Izuku Midoriya (Deku)", "Classe 1-A", 0.2, None, None),
    "bakugo": ("Katsuki Bakugo (Dynamight)", "Classe 1-A", 1.5, None, None),
    "todoroki": ("Shoto Todoroki", "Classe 1-A", 1.8, None, None),
    "iida": ("Tenya Iida (Ingenium)", "Classe 1-A", 1.2, None, None),
    "uraraka": ("Ochaco Uraraka (Uravity)", "Classe 1-A", 0.9, None, None),
    "kirishima": ("Eijiro Kirishima (Red Riot)", "Classe 1-A", 1.2, None, None),
    "tokoyami": ("Fumikage Tokoyami (Tsukuyomi)", "Classe 1-A", 1.3, None, None),
    "yaoyorozu": ("Momo Yaoyorozu (Creati)", "Classe 1-A", 1.1, None, None),
    "tsuyu": ("Tsuyu Asui (Froppy)", "Classe 1-A", 1.0, None, None),
    "kaminari": ("Denki Kaminari (Chargebolt)", "Classe 1-A", 1.0, None, None),
    "jiro": ("Kyoka Jiro (Earphone Jack)", "Classe 1-A", 0.9, None, None),
    "mina": ("Mina Ashido (Pinky)", "Classe 1-A", 0.9, None, None),
    "sero": ("Hanta Sero (Cellophane)", "Classe 1-A", 0.8, None, None),
    "shoji": ("Mezo Shoji (Tentacole)", "Classe 1-A", 1.0, None, None),
    "ojiro": ("Mashirao Ojiro (Tailman)", "Classe 1-A", 0.9, None, None),
    "sato": ("Rikido Sato (Sugarman)", "Classe 1-A", 0.9, None, None),
    "koda": ("Koji Koda (Anima)", "Classe 1-A", 0.6, None, None),
    "aoyama": ("Yuga Aoyama (Can't Stop Twinkling)", "Classe 1-A", 0.8, None, None),
    "hagakure": ("Toru Hagakure (Invisible Girl)", "Classe 1-A", 0.4, None, None),
    "mineta": ("Minoru Mineta (Grape Juice)", "Classe 1-A", 0.5, None, None),
    "shinso": ("Hitoshi Shinso", "Classe 1-A", 0.7, None, None),
    # ---------------------------------------------------------------- classe 1-B, Big 3, autres écoles
    "kendo": ("Itsuka Kendo (Battle Fist)", "Classe 1-B", 1.1, None, None),
    "tetsutetsu": ("Tetsutetsu Tetsutetsu (Real Steel)", "Classe 1-B", 1.1, None, None),
    "shiozaki": ("Ibara Shiozaki (Vine)", "Classe 1-B", 1.1, None, None),
    "monoma": ("Neito Monoma (Phantom Thief)", "Classe 1-B", 0.9, None, None),
    "classe_1b": ("Élèves de la classe 1-B (groupe)", "Classe 1-B", 1.0, None, None),
    "hatsume": ("Mei Hatsume", "Yuei (autres sections)", 0.3, None, None),
    "mirio": ("Mirio Togata (Lemillion)", "Big 3", 3.5, None, None),
    "tamaki": ("Tamaki Amajiki (Suneater)", "Big 3", 3.0, None, None),
    "nejire": ("Nejire Hado (Nejire-chan)", "Big 3", 3.0, None, None),
    "inasa": ("Inasa Yoarashi", "Shiketsu", 2.2, None, None),
    "candidats": ("Candidats à la licence provisoire (groupe)", "Autres écoles", 1.2, None, None),
    # ---------------------------------------------------------------- héros pros
    "all_might": ("All Might (Toshinori Yagi)", "Héros pros", 6.8, None, None),
    "nana": ("Nana Shimura (7e détentrice)", "Héros pros", 5.0, -30.0, None),
    "gran_torino": ("Gran Torino", "Héros pros", 4.3, None, None),
    "endeavor": ("Endeavor (Enji Todoroki)", "Héros pros", 4.8, None, None),
    "hawks": ("Hawks (Keigo Takami)", "Héros pros", 4.6, None, None),
    "best_jeanist": ("Best Jeanist", "Héros pros", 4.2, None, None),
    "edgeshot": ("Edgeshot", "Héros pros", 4.2, None, None),
    "mirko": ("Mirko (Rumi Usagiyama)", "Héros pros", 4.3, None, None),
    "crust": ("Crust", "Héros pros", 3.9, 1.9007, None),
    "kamui": ("Kamui Woods", "Héros pros", 3.3, None, None),
    "mt_lady": ("Mt. Lady", "Héros pros", 3.0, None, None),
    "ryukyu": ("Ryukyu", "Héros pros", 3.8, None, None),
    "fatgum": ("Fatgum", "Héros pros", 3.6, None, None),
    "nighteye": ("Sir Nighteye", "Héros pros", 3.7, 1.511, None),
    "rock_lock": ("Rock Lock", "Héros pros", 2.8, None, None),
    "gang_orca": ("Gang Orca", "Héros pros", 3.8, None, None),
    "native": ("Native", "Héros pros", 1.8, None, None),
    "tiger": ("Tiger (Wild Wild Pussycats)", "Héros pros", 2.8, None, None),
    "mandalay": ("Mandalay (Wild Wild Pussycats)", "Héros pros", 2.4, None, None),
    "pixie_bob": ("Pixie-Bob (Wild Wild Pussycats)", "Héros pros", 2.4, None, None),
    "star": ("Star and Stripe (Cathleen Bate)", "Héros pros (États-Unis)", 6.0, 2.2001, None),
    "lady_nagant": ("Lady Nagant (Kaina Tsutsumi)", "Évadés de Tartarus", 4.0, None, None),
    # ---------------------------------------------------------------- professeurs de Yuei
    "aizawa": ("Shota Aizawa (Eraser Head)", "Professeurs de Yuei", 3.3, None, None),
    "present_mic": ("Present Mic", "Professeurs de Yuei", 2.6, None, None),
    "midnight": ("Midnight", "Professeurs de Yuei", 2.6, 1.9004, None),
    "cementoss": ("Cementoss", "Professeurs de Yuei", 3.0, None, None),
    "ectoplasm": ("Ectoplasm", "Professeurs de Yuei", 3.0, None, None),
    "thirteen": ("Thirteen", "Professeurs de Yuei", 2.7, None, None),
    "snipe": ("Snipe", "Professeurs de Yuei", 2.7, None, None),
    "vlad": ("Vlad King", "Professeurs de Yuei", 2.9, None, None),
    "power_loader": ("Power Loader", "Professeurs de Yuei", 2.2, None, None),
    "nezu": ("Nezu (directeur)", "Professeurs de Yuei", 2.0, None, None),
    # ---------------------------------------------------------------- All For One et la Ligue des vilains
    "afo": ("All For One", "Ligue des vilains", 7.0, 2.3009, None),
    "shigaraki": ("Tomura Shigaraki", "Ligue des vilains", 2.3, 2.3011, None),
    "kurogiri": ("Kurogiri", "Ligue des vilains", 3.0, 2.3010, None),
    "dabi": ("Dabi (Toya Todoroki)", "Ligue des vilains", 3.2, None, None),
    "toga": ("Himiko Toga", "Ligue des vilains", 2.0, 2.3008, None),
    "twice": ("Twice (Jin Bubaigawara)", "Ligue des vilains", 2.3, 1.9003, None),
    "spinner": ("Spinner (Shuichi Iguchi)", "Ligue des vilains", 1.4, None, None),
    "compress": ("Mr. Compress", "Ligue des vilains", 2.4, None, None),
    "magne": ("Magne", "Ligue des vilains", 2.3, 1.4521, None),
    "muscular": ("Muscular", "Ligue des vilains", 3.3, None, None),
    "moonfish": ("Moonfish", "Ligue des vilains", 2.4, None, None),
    "mustard": ("Mustard", "Ligue des vilains", 1.2, None, None),
    "copies_twice": ("Doubles de Twice (groupe)", "Ligue des vilains", 2.0, None, None),
    "stain": ("Stain (le Tueur de héros)", "Vilains", 3.6, 2.30074, None),
    "gigantomachia": ("Gigantomachia", "Ligue des vilains", 5.0, 2.3006, None),
    "sludge": ("Le vilain de boue", "Vilains", 1.3, None, None),
    "vilains_usj": ("Voyous de l'USJ (groupe)", "Vilains", 0.8, None, None),
    "nomu_usj": ("Nomu de l'USJ (anti-All Might)", "Nomu", 4.8, None, None),
    "nomus_hosu": ("Nomu de Hosu (groupe)", "Nomu", 3.0, None, None),
    "nomus_kamino": ("Nomu de Kamino (groupe)", "Nomu", 3.0, None, None),
    "hood": ("Le Nomu encapuchonné (haut de gamme)", "Nomu", 5.0, 1.6501, None),
    "nomus_haut": ("Nomu haut de gamme (groupe)", "Nomu", 4.3, None, None),
    "robots": ("Robots de l'examen et du festival (groupe)", "Robots", 0.5, None, None),
    "robot_zero": ("Robot à zéro point", "Robots", 2.0, None, None),
    # ---------------------------------------------------------------- Shie Hassaikai
    "overhaul": ("Overhaul (Kai Chisaki)", "Shie Hassaikai", 4.0, None, None),
    "chronostasis": ("Chronostasis", "Shie Hassaikai", 2.0, None, None),
    "mimic": ("Mimic (Joi Irinaka)", "Shie Hassaikai", 2.6, None, None),
    "rappa": ("Rappa", "Shie Hassaikai", 3.2, None, None),
    "tengai": ("Tengai", "Shie Hassaikai", 2.8, None, None),
    "trio_hassaikai": ("Hojo, Sakaki et Tabe (Huit Préceptes)", "Shie Hassaikai", 2.2, None, None),
    "rikiya": ("Rikiya Katsukame", "Shie Hassaikai", 2.8, None, None),
    # ---------------------------------------------------------------- autres vilains
    "gentle": ("Gentle Criminal", "Vilains", 2.2, None, None),
    "re_destro": ("Re-Destro (Rikiya Yotsubashi)", "Armée de libération du Méta", 4.5, None, None),
    "geten": ("Geten", "Armée de libération du Méta", 3.3, None, None),
    "curious": ("Curious", "Armée de libération du Méta", 2.0, None, None),
    "soldats_mla": ("Soldats de l'Armée de libération (groupe)", "Armée de libération du Méta", 1.5, None, None),
    "ending": ("Ending", "Vilains", 2.4, None, None),
    "evades": ("Évadés de Tartarus (groupe)", "Évadés de Tartarus", 2.5, None, None),
    "kunieda": ("Kunieda", "Vilains", 2.6, None, None),
}

GENERIC_PART = {"classe_1b", "candidats", "vilains_usj", "copies_twice", "nomus_hosu", "nomus_kamino", "nomus_haut",
                "robots", "trio_hassaikai", "soldats_mla", "evades"}

# gains et pertes permanents : (perso, temps, changement moyen en échelons, écart-type, libellé)
JUMPS_PART = [
    # Deku : One For All, pourcentages et Quirks des anciens détenteurs
    ("deku", 0.79, 1.6, 0.6, "Reçoit One For All d'All Might, 100 % incontrôlé qui brise ses membres (ch. 4)"),
    ("deku", 1.035, 0.6, 0.4, "Full Cowl à 5 % avec Gran Torino (ch. 48-49)"),
    ("deku", 1.38, 0.4, 0.3, "Shoot Style, Full Cowl à 8 % (ch. 101-102)"),
    ("deku", 1.46, 0.4, 0.3, "Full Cowl à 20 % pendant les stages (ch. ~130-150)"),
    ("deku", 1.699, 0.4, 0.3, "Éveil de Blackwhip, le Quirk du 5e détenteur (ch. 213-214)"),
    ("deku", 1.79, 0.5, 0.3, "Stage chez Endeavor : Blackwhip maîtrisé en parallèle, Full Cowl 30 % (ch. 247-252)"),
    ("deku", 1.8999, 0.6, 0.4, "Float et One For All à 45 % puis 100 % contre Shigaraki (ch. ~280-286)"),
    ("deku", 1.995, 0.6, 0.4, "Six Quirks des détenteurs : Danger Sense, Smokescreen, Fa Jin (ch. 295-308)"),
    ("deku", 2.29, 0.5, 0.4, "Entraînement final avec All Might et les anciens détenteurs (ch. ~338-342)"),
    ("deku", 2.30035, 0.5, 0.4, "Gearshift et Transmission contre Shigaraki (ch. ~367-371)"),
    # Bakugo
    ("bakugo", 1.79, 0.4, 0.3, "Stage chez Endeavor : AP Shot Auto-Cannon, explosions sans perte de vitesse (ch. 247-249)"),
    ("bakugo", 2.29, 0.3, 0.3, "Préparation de la guerre finale (ch. ~338-342)"),
    ("bakugo", 2.3007, 0.5, 0.4, "Éveil express à son retour : Explosions par la sueur à distance, Rapid (ch. 403-406)"),
    # Todoroki et les autres élèves
    ("todoroki", 1.79, 0.4, 0.3, "Stage chez Endeavor : Flashfire Fist, contrôle des flammes (ch. 247-249)"),
    ("todoroki", 2.30005, 0.4, 0.3, "Flashfire Fist : Phosphor, qui éteint les flammes de Dabi (ch. 351-352)"),
    ("tokoyami", 1.79, 0.4, 0.3, "Stage chez Hawks : Black Ankh et vol (ch. ~248, 268)"),
    ("iida", 1.79, 0.3, 0.3, "Recipro Extend (ch. ~269-280)"),
    ("shinso", 1.69, 0.5, 0.4, "Arme de capture et entraînement avec Aizawa (ch. 194-195)"),
    ("uraraka", 2.30065, 0.5, 0.4, "Éveil de Zero Gravity contre Toga (ch. ~392)"),
    ("mirio", 1.512, -3.0, 0.6, "Perte de Permeation par la balle anti-Quirk de Chronostasis (ch. 149-150 ; datée après l'arc pour que l'état « Overhaul » de Mirio reste celui d'avant la balle)"),
    ("mirio", 2.25, 2.6, 0.6, "Permeation rendue par le Rewind d'Eri (ch. ~333-341)"),
    # All Might et All For One
    ("all_might", -5.99, -0.8, 0.4, "Blessé par All For One : estomac et poumon détruits, limite de temps (ch. 2, 59, 89)"),
    ("all_might", -0.5, -0.3, 0.3, "Limite d'environ trois heures par jour (ch. 2)"),
    ("all_might", 0.9, -0.3, 0.3, "Limite réduite à moins d'une heure après le vilain de boue (ch. 12-13)"),
    ("all_might", 1.3101, -4.2, 0.6, "Braises de One For All éteintes après Kamino : retraite (ch. 94-95)"),
    ("all_might", 2.29, 1.0, 0.6, "Armure Armored All Might et équipements des Quirks (ch. ~397-398)"),
    ("afo", -5.99, -1.2, 0.5, "Visage détruit par All Might, maintien en vie artificiel (ch. 59, 89)"),
    ("afo", 2.29, 1.2, 0.6, "Rajeuni par Rewind, corps restauré pour la guerre finale (ch. ~341-354)"),
    # Shigaraki
    ("shigaraki", 1.7299, 1.3, 0.6, "Éveil de Decay contre Re-Destro : propagation au sol (ch. 237-238)"),
    ("shigaraki", 1.85, 2.0, 0.8, "Opération du docteur Ujiko : Super Régénération, corps de Nomu, achevé à 75 % (ch. 240, 270)"),
    ("shigaraki", 2.0, 0.7, 0.5, "Fusion progressive avec All For One, corps achevé (ch. 306-329)"),
    ("shigaraki", 2.2001, -0.3, 0.3, "New Order se retourne en lui, Reflect détruit (ch. 333-334)"),
    ("shigaraki", 2.29, 0.5, 0.4, "Nouveaux Quirks et Overhaul greffés par All For One (ch. ~340-343)"),
    # autres
    ("hawks", 1.9006, -0.7, 0.4, "Ailes brûlées par Dabi (ch. ~268-269)"),
    ("hawks", 2.25, 0.4, 0.3, "Ailes en partie repoussées (ch. ~316, 340)"),
    ("hawks", 2.30022, -1.5, 0.5, "Fierce Wings volé par All For One (ch. ~376)"),
    ("endeavor", 2.30021, -0.4, 0.3, "Bras perdu contre All For One (ch. ~357-358)"),
    ("mirko", 1.9003, -0.5, 0.4, "Bras perdu contre les Nomu haut de gamme (ch. ~266)"),
    ("aizawa", 1.9008, -0.6, 0.4, "Jambe amputée et œil abîmé contre Shigaraki (ch. ~277-290)"),
    ("gran_torino", 1.9007, -1.2, 0.5, "Thorax percé par Shigaraki, soins intensifs (ch. ~276)"),
    ("toga", 1.7249, 0.5, 0.4, "Éveil : elle copie les Quirks de ceux dont elle prend l'apparence (ch. 226-227)"),
    ("toga", 2.29, 0.5, 0.4, "Copie de Twice : armée de doubles (ch. ~374-384)"),
    ("twice", 1.729, 0.8, 0.5, "Éveil : Sad Man's Parade, armée de doubles (ch. 231-232)"),
    ("dabi", 1.85, 0.6, 0.4, "Flammes bleues poussées à leur maximum, corps calciné (ch. ~268-291)"),
    ("dabi", 2.3005, 0.3, 0.3, "Recrée Phosphor dans son propre corps (ch. 363)"),
    ("spinner", 2.29, 2.5, 0.8, "Quirks greffés par All For One, corps géant (ch. ~342-357)"),
]

# ============================================================== Flash-back
fight(-30.0, "nana", "afo", "nana", "A", 2,
      note="All For One tue Nana Shimura sous les yeux du jeune Toshinori, que Gran Torino emmène (récit ch. 89-92)", flags="?")
fight(-6.0, "apogee", "all_might", "afo", "A", 1,
      note="Premier duel il y a cinq-six ans : All Might détruit le visage d'All For One mais garde une blessure mortelle (ch. 2, 59, 89)")

# ============================================================== Le vilain de boue et l'examen d'entrée
fight(-0.001, "debut", "sludge", "deku", "A", 3, note="Deku, encore sans Alter, englouti par le vilain de boue (ch. 1)")
fight(0.0, "debut", "all_might", "sludge", "A", 3, note="All Might capture le vilain de boue d'un coup de poing (ch. 1)")
fight(0.01, "debut", "sludge", "bakugo", "A", 1, ta=["surprise"],
      note="Bakugo prisonnier du vilain de boue, les héros sur place n'osent pas intervenir (ch. 2)")
fight(0.0101, "debut", "all_might", "sludge", "A", 3, note="Detroit Smash : le vilain de boue dispersé, la pluie se met à tomber (ch. 2)")
fight(0.8, "debut", "deku", "robot_zero", "A", 3, note="Premier Smash de Deku : le robot à zéro point détruit, bras et jambes brisés (ch. 3-4)")
fight(0.8001, "debut", "bakugo", "robots", "A", 3, note="Bakugo premier de l'examen d'entrée, 77 points de combat (ch. 3-4)")

# ============================================================== Rentrée et USJ
fight(0.95, "usj", "bakugo", "deku", "D",
      note="Exercice de combat : Bakugo domine, Deku perce le plafond d'un Smash et son équipe gagne l'exercice (ch. 8-10)", flags="i")
fight(0.951, "usj", ["todoroki", "shoji"], ["ojiro", "hagakure"], "A", 3,
      note="Todoroki gèle tout le bâtiment, exercice gagné en quelques secondes (ch. 11)")
fight(0.97, "usj", "aizawa", "vilains_usj", "A", 3, note="Eraser Head seul contre la foule de voyous (ch. 14-15)")
fight(0.9701, "usj", "kurogiri", "thirteen", "A", 2, note="Kurogiri renvoie le trou noir de Thirteen contre lui-même (ch. 15-16)")
fight(0.9702, "usj", ["deku", "tsuyu", "mineta"], "vilains_usj", "A", 2,
      note="Zone du naufrage : Smash de Deku sur l'eau, boules de Mineta (ch. 15-16)", flags="e")
fight(0.9703, "usj", "todoroki", "vilains_usj", "A", 3, note="Todoroki gèle tous les voyous de la zone (ch. 17)")
fight(0.9704, "usj", ["bakugo", "kirishima"], "vilains_usj", "A", 3, note="Zone de l'incendie (ch. 17-18)", flags="e")
fight(0.9705, "usj", ["kaminari", "jiro", "yaoyorozu"], "vilains_usj", "A", 3,
      note="Zone de la montagne : décharge de Kaminari sous la couverture isolante de Yaoyorozu (ch. 18)", flags="e")
fight(0.9706, "usj", "ojiro", "vilains_usj", "A", 2, note="Ojiro seul dans la zone de l'incendie (ch. 17)")
fight(0.9707, "usj", "nomu_usj", "aizawa", "A", 3, note="Le Nomu brise les bras d'Aizawa et lui écrase la tête au sol (ch. 16)")
fight(0.9708, "usj", "nomu_usj", "deku", "A", 2,
      note="Deku frappe le Nomu, choc absorbé, son bras n'est même pas brisé (ch. 16-17)", flags="i")
fight(0.9709, "usj", "bakugo", "kurogiri", "A", 1, ta=["surprise"],
      note="Bakugo plaque Kurogiri en visant son armure (ch. 18-19)", flags="i?")
fight(0.971, "usj", "all_might", "nomu_usj", "A", 2,
      note="Trois cents coups au-delà de l'absorption de chocs, le Nomu envoyé hors du dôme ; All Might au bout de son temps (ch. 19-20)")
fight(0.9711, "usj", "snipe", "shigaraki", "A", 2, note="Les professeurs arrivent, Snipe crible Shigaraki qui fuit (ch. 20)", flags="i")

# ============================================================== Festival sportif
fight(1.0, "festival", "todoroki", "robots", "A", 3, note="Todoroki gèle un Robot Inferno dès la première épreuve (ch. 24)")
fight(1.0001, "festival", "deku", "shinso", "A", 2,
      note="Lavage de cerveau brisé par les anciens détenteurs, Deku pousse Shinso hors du ring (ch. 33-34)")
fight(1.0002, "festival", "todoroki", "sero", "A", 3, note="Glacier géant contre Sero (ch. 34)")
fight(1.0003, "festival", "shiozaki", "kaminari", "A", 2, note="Les lianes de Shiozaki absorbent la décharge (ch. 34)")
fight(1.0004, "festival", "iida", "hatsume", "A", 2,
      note="Hatsume fait la démonstration de ses inventions puis sort d'elle-même (ch. 34)", flags="?")
fight(1.0005, "festival", "mina", "aoyama", "A", 2, note="Mina bat Aoyama (ch. 34)")
fight(1.0006, "festival", "tokoyami", "yaoyorozu", "A", 2, note="Dark Shadow pousse Yaoyorozu hors du ring (ch. 35)")
fight(1.0007, "festival", "kirishima", "tetsutetsu", "A", 1, note="Double K.-O., Kirishima gagne le bras de fer (ch. 35)")
fight(1.0008, "festival", "bakugo", "uraraka", "A", 2, note="Pluie de météores d'Uraraka annulée d'une explosion (ch. 35-37)")
fight(1.0009, "festival", "todoroki", "deku", "A", 1,
      note="Deku se brise les doigts pour pousser Todoroki à utiliser sa flamme ; Deku sort du ring (ch. 38-40)")
fight(1.001, "festival", "iida", "shiozaki", "A", 2, note="Iida bat Shiozaki (ch. 40)")
fight(1.0011, "festival", "tokoyami", "mina", "A", 2, note="Tokoyami bat Mina (ch. 40)")
fight(1.0012, "festival", "bakugo", "kirishima", "A", 1, note="Explosions continues jusqu'à percer le durcissement (ch. 40)")
fight(1.0013, "festival", "todoroki", "iida", "A", 2, note="Todoroki gèle Iida en demi-finale (ch. 41)")
fight(1.0014, "festival", "bakugo", "tokoyami", "A", 2, note="La lumière des explosions affaiblit Dark Shadow (ch. 41)")
fight(1.0015, "festival", "bakugo", "todoroki", "A", 2, tb=["retenue"],
      note="Finale : Todoroki éteint sa flamme au dernier moment, Howitzer Impact (ch. 42-43)")

# ============================================================== Stages et Hosu
fight(1.03, "stain", "gran_torino", "deku", "A", 2, ta=["retenue"],
      note="Entraînement chez Gran Torino, Deku découvre le Full Cowl (ch. 47-49)")
fight(1.05, "stain", "stain", "native", "A", 2, note="Native paralysé par le sang (ch. 51)")
fight(1.0501, "stain", "stain", "iida", "A", 2, note="Iida, venu venger son frère, battu et paralysé (ch. 51-52)")
fight(1.0502, "stain", "stain", "deku", "A", 2, note="Deku Full Cowl 5 % tient puis est paralysé (ch. 52-53)")
fight(1.0503, "stain", ["deku", "todoroki", "iida"], "stain", "A", 1,
      note="Glace et flammes de Todoroki, coups de Deku et d'Iida ; Stain blessé est assommé (ch. 53-55)", flags="e")
fight(1.0504, "stain", "endeavor", "nomus_hosu", "A", 3, note="Endeavor brûle les Nomu de Hosu (ch. 53-56)")
fight(1.0505, "stain", "stain", "nomus_hosu", "A", 2, note="Stain, à bout, tue le Nomu ailé qui avait enlevé Deku (ch. 56)")

# ============================================================== Examens de fin de semestre (professeurs lestés ou retenus)
fight(1.2, "examens", ["deku", "bakugo"], "all_might", "A", 1, tb=["retenue"],
      note="All Might lesté de poids ; Deku frappe All Might et porte Bakugo inconscient jusqu'à la sortie (ch. 64-68)", flags="e?")
fight(1.2001, "examens", ["todoroki", "yaoyorozu"], "aizawa", "A", 1, tb=["retenue"],
      note="Le canon à filets de Yaoyorozu capture Aizawa (ch. 63-64)", flags="e")
fight(1.2002, "examens", "cementoss", ["kirishima", "sato"], "A", 2, ta=["retenue"],
      note="Kirishima et Sato échouent, submergés de béton (ch. 62)")
fight(1.2003, "examens", ["tokoyami", "tsuyu"], "ectoplasm", "A", 1, tb=["retenue"],
      note="Tokoyami et Asui menottent un clone d'Ectoplasm (ch. 62)", flags="e")
fight(1.2004, "examens", ["uraraka", "aoyama"], "thirteen", "A", 1, tb=["retenue"],
      note="Uraraka et Aoyama passent (ch. 62)", flags="e?")
fight(1.2005, "examens", "nezu", ["kaminari", "mina"], "A", 2, ta=["prepa"],
      note="Nezu les écrase sous les décombres calculés d'avance (ch. 62)")
fight(1.2006, "examens", ["jiro", "koda"], "present_mic", "A", 1, tb=["retenue"],
      note="Les insectes de Koda, Jiro passe la porte (ch. 62)", flags="e?")
fight(1.2007, "examens", ["mineta", "sero"], "midnight", "A", 1, tb=["retenue"],
      note="Mineta porte Sero endormi jusqu'à la sortie (ch. 62)", flags="?")
fight(1.2008, "examens", ["shoji", "hagakure"], "snipe", "A", 1, tb=["retenue"], note="Ils passent (ch. 62)", flags="e?")
fight(1.2009, "examens", ["iida", "ojiro"], "power_loader", "A", 1, tb=["retenue"], note="Ils passent (ch. 62)", flags="e?")

# ============================================================== Camp en forêt
fight(1.28, "camp", "magne", "pixie_bob", "A", 3, ta=["surprise"], note="Magne assomme Pixie-Bob par surprise (ch. 72)")
fight(1.2801, "camp", ["mandalay", "tiger"], ["spinner", "magne"], "D",
      note="Les Wild Wild Pussycats retiennent Spinner et Magne (ch. 73-77)", flags="i")
fight(1.2802, "camp", "vlad", "copies_twice", "A", 2, note="Vlad King détruit un double de Dabi (ch. 73-74)", flags="?")
fight(1.2803, "camp", "deku", "muscular", "A", 1,
      note="Smash à 1 000 000 % pour protéger Kota, les deux bras de Deku brisés (ch. 75-77)")
fight(1.2804, "camp", ["tetsutetsu", "kendo"], "mustard", "A", 2, note="Ils neutralisent Mustard dans le gaz (ch. 78-79)", flags="e")
fight(1.2805, "camp", "moonfish", "shoji", "A", 2, note="Moonfish tranche le bras de Shoji (ch. 79)")
fight(1.2806, "camp", "tokoyami", "moonfish", "A", 3, note="Dark Shadow déchaîné dans le noir écrase Moonfish (ch. 79-80)")
fight(1.2807, "camp", "toga", ["uraraka", "tsuyu"], "D", note="Toga blesse Uraraka et prend son sang, puis se retire (ch. 77-78)", flags="i")
fight(1.2808, "camp", "compress", ["deku", "todoroki", "shoji"], "A", 1,
      note="Compress enlève Bakugo ; les élèves reprennent Tokoyami (ch. 81-83)", flags="i")

# ============================================================== Kamino
fight(1.2999, "kamino", ["all_might", "edgeshot", "kamui", "gran_torino"],
      ["kurogiri", "dabi", "compress", "twice", "toga", "spinner", "magne"], "A", 3, ta=["surprise"],
      note="Raid du bar : Kamui Woods ligote la Ligue, Edgeshot assomme Kurogiri (ch. 84-85)")
fight(1.3001, "kamino", "afo", ["best_jeanist", "mt_lady", "gang_orca"], "A", 3, ta=["surprise"],
      note="Une seule attaque d'All For One anéantit les héros de l'entrepôt (ch. 86-87)")
fight(1.3002, "kamino", "afo", "gran_torino", "A", 2, note="Gran Torino transpercé (ch. 88-89)")
fight(1.3003, "kamino", "endeavor", "nomus_kamino", "A", 3, note="Endeavor brûle les Nomu de Kamino (ch. 90)")
fight(1.3004, "kamino", "all_might", "afo", "A", 1,
      note="United States of Smash : All Might, réduit à un bras, assomme All For One ; Endeavor, Edgeshot et Kamui Woods l'ont aidé un instant (ch. 88-94)")

# ============================================================== Licence provisoire et Deku contre Kacchan
fight(1.4, "licence", ["bakugo", "kirishima", "kaminari"], "candidats", "A", 3,
      note="Bakugo, Kirishima et Kaminari éliminent les candidats de Ketsubutsu (ch. ~105-107)")
fight(1.4001, "licence", ["todoroki", "inasa"], "gang_orca", "A", 1, tb=["retenue"],
      note="Flammes et vent combinés emprisonnent Gang Orca, l'examen s'arrête (ch. 108-111)", flags="ie")
fight(1.42, "licence", "bakugo", "deku", "A", 1, note="Deuxième duel de nuit au terrain Beta, Bakugo gagne de justesse (ch. 118-119)")

# ============================================================== Stages et Overhaul
fight(1.45, "overhaul", "mirio", ["deku", "tokoyami", "kirishima", "iida", "tsuyu", "uraraka"], "A", 3,
      note="Mirio seul écrase la classe 1-A (ch. 122-123)")
fight(1.452, "overhaul", "overhaul", ["magne", "compress"], "A", 3, ta=["surprise"],
      note="Overhaul fait exploser Magne et ampute Mr. Compress (ch. ~127-128)")
fight(1.5001, "overhaul", "tamaki", "trio_hassaikai", "A", 2, note="Chimère de Tamaki contre trois des Huit Préceptes (ch. 135-137)")
fight(1.5002, "overhaul", ["deku", "aizawa", "rock_lock"], "mimic", "A", 2, note="Mimic battu dans les couloirs (ch. ~137-138)", flags="?")
fight(1.50029, "overhaul", "fatgum", "tengai", "A", 2, note="Fatgum perce la barrière de Tengai (ch. 139-141)")
fight(1.5003, "overhaul", "kirishima", "rappa", "A", 1, note="Red Riot Unbreakable tient puis bat Rappa (ch. 141-142)")
fight(1.5004, "overhaul", ["ryukyu", "uraraka", "tsuyu", "nejire"], "rikiya", "A", 2,
      note="L'agence Ryukyu bat Rikiya, dopé au Quirk d'amplification (ch. 142-146)")
fight(1.5005, "overhaul", "mirio", "chronostasis", "A", 3, note="Mirio balaie Chronostasis et ses gardes (ch. 147-148)")
fight(1.5006, "overhaul", "overhaul", "mirio", "A", 1, tb=["protege"],
      note="Mirio protège Eri, touché par la balle anti-Quirk (ch. 148-150)", flags="i")
fight(1.5007, "overhaul", "overhaul", "nighteye", "A", 2, note="Sir Nighteye transpercé, il mourra (ch. 151-153)")
fight(1.5009, "overhaul", "deku", "overhaul", "A", 2, ta=["aide"],
      note="Deku à 100 % grâce au Rewind d'Eri contre Overhaul fusionné à Chronostasis (ch. 155-158)")
fight(1.51, "overhaul", "shigaraki", "overhaul", "A", 2, ta=["surprise"], tb=["epuise"],
      note="Embuscade du convoi : Shigaraki désintègre les bras d'Overhaul (ch. ~159-160)")

# ============================================================== Festival culturel
fight(1.6, "festival_ecole", "deku", "gentle", "A", 2, tb=["aide"],
      note="Deku bat Gentle Criminal, dopé par le Love de La Brava (ch. 176-180)")

# ============================================================== Le Nomu encapuchonné
fight(1.64, "hood", "hawks", "nomus_kamino", "A", 3, note="Hawks abat les Nomu ordinaires lâchés sur Fukuoka (ch. 186-187)")
fight(1.65, "hood", ["endeavor", "hawks"], "hood", "A", 1,
      note="Plus Ultra : Prominence Burn d'Endeavor porté par Hawks, Endeavor gravement blessé (ch. 186-191)")

# ============================================================== Entraînement commun A contre B
fight(1.68, "classeb", ["tsuyu", "kaminari", "kirishima", "koda", "shinso"], ["shiozaki", "classe_1b"], "A", 1,
      note="Premier match : 1-A gagne 4-2 (ch. 195-197)", flags="e")
fight(1.685, "classeb", ["kendo", "classe_1b"], ["yaoyorozu", "tokoyami", "hagakure", "aoyama"], "A", 2,
      note="Deuxième match : 1-B gagne 4-0, Kendo bat Yaoyorozu (ch. 198-201)", flags="e")
fight(1.69, "classeb", ["iida", "todoroki", "ojiro", "shoji"], ["tetsutetsu", "classe_1b"], "D",
      note="Troisième match : nul 1-1 au temps (ch. 202-205)", flags="e")
fight(1.695, "classeb", ["bakugo", "jiro", "sero", "sato"], "classe_1b", "A", 3,
      note="Quatrième match : 1-A gagne 4-0 en cinq minutes (ch. 206-208)")
fight(1.7, "classeb", ["deku", "uraraka", "mina", "mineta"], ["monoma", "shinso", "classe_1b"], "A", 2,
      note="Cinquième match : Blackwhip s'éveille, 1-A gagne 4-0 (ch. 209-216)")

# ============================================================== Armée de libération du Méta
fight(1.72, "mla", "gigantomachia", ["shigaraki", "dabi", "twice", "toga", "spinner", "compress"], "A", 1,
      note="Épreuve d'endurance de plusieurs semaines contre Gigantomachia, qui finit par accepter Shigaraki (ch. 220-223)",
      flags="i")
fight(1.725, "mla", "toga", "curious", "A", 2, note="Toga s'éveille et tue Curious (ch. 225-227)")
fight(1.729, "mla", "twice", "soldats_mla", "A", 3, note="Sad Man's Parade submerge les soldats de Deika (ch. 231-232)")
fight(1.7295, "mla", "dabi", "geten", "D", note="Duel de glace et de flammes, interrompu (ch. ~232-235)", flags="i?")
fight(1.73, "mla", "shigaraki", "re_destro", "A", 2,
      note="Shigaraki éveille Decay et rase Deika ; Re-Destro se soumet (ch. 234-239)")

# ============================================================== Stage chez Endeavor
fight(1.8, "agence", ["todoroki", "bakugo", "deku"], "ending", "A", 2,
      note="Les trois stagiaires sauvent Natsuo d'Ending (ch. 250-251)")

# ============================================================== Guerre de libération du Paranormal
fight(1.9, "guerre", "hawks", "twice", "A", 2, note="Hawks tue Twice à la villa de Gunga (ch. ~258-266)")
fight(1.9001, "guerre", "gigantomachia", ["mt_lady", "ryukyu", "kamui"], "A", 2,
      note="Gigantomachia s'éveille et fonce vers Jaku à travers les héros (ch. ~267-279)", flags="i")
fight(1.9002, "guerre", "mirko", "nomus_haut", "A", 2, note="Mirko détruit des Nomu haut de gamme et perd un bras (ch. ~263-267)")
fight(1.9005, "guerre", "dabi", "hawks", "A", 2, note="Dabi brûle Hawks (ch. ~266-267)")
fight(1.90051, "guerre", ["tokoyami", "hawks"], "dabi", "D", note="Tokoyami sauve Hawks des flammes de Dabi (ch. 267-268)", flags="i")
fight(1.9006, "guerre", "shigaraki", ["crust", "aizawa", "endeavor"], "A", 3,
      note="Réveil de Shigaraki : Decay rase Jaku, Crust meurt pour sauver Aizawa, Endeavor assommé (ch. ~270-274)")
fight(1.90065, "guerre", "shigaraki", "gran_torino", "A", 2, note="Shigaraki transperce Gran Torino (ch. ~275-276)")
fight(1.9007, "guerre", "shigaraki", ["deku", "bakugo", "todoroki"], "A", 1,
      note="Deku à 45 % puis 100 %, glacier de Todoroki ; Bakugo prend les pointes destinées à Deku (ch. ~278-286)", flags="i")
fight(1.9008, "guerre", ["endeavor", "mt_lady", "kirishima", "mina", "yaoyorozu"], "gigantomachia", "A", 1, ta=["prepa"],
      note="Sédatif de Yaoyorozu jeté par Kirishima, Endeavor l'assomme, l'anesthésie agit (ch. 279-292)")
fight(1.9009, "guerre", "dabi", "todoroki", "A", 1, note="Dabi révèle être Toya et domine Shoto (ch. 290-294)", flags="i")
fight(1.901, "guerre", ["deku", "endeavor", "bakugo", "mirio", "best_jeanist"], "shigaraki", "D",
      note="Corps achevé à 75 % seulement, All For One ordonne la retraite (ch. 291-296)", flags="i")

# ============================================================== Deku héros sombre
fight(2.0, "sombre", "deku", "evades", "A", 3, note="Deku seul arrête les évadés de Tartarus (ch. ~307-309)")
fight(2.05, "sombre", "deku", "lady_nagant", "A", 2, note="Deku bat Lady Nagant, que la bombe d'All For One blessera (ch. 310-313)")
fight(2.1, "sombre", ["bakugo", "todoroki", "iida", "uraraka", "kirishima", "tokoyami"], "deku", "A", 1, tb=["epuise"],
      note="La classe 1-A ramène Deku, épuisé, à Yuei (ch. 317-320)", flags="i")

# ============================================================== Star and Stripe
fight(2.2, "star", "shigaraki", "star", "A", 1,
      note="Star and Stripe meurt mais New Order se retourne contre les Quirks de Shigaraki (ch. 329-334)")

# ============================================================== Guerre finale
fight(2.3, "final", ["present_mic", "aizawa"], "kurogiri", "D", note="Mic et Aizawa contre Kurogiri (ch. ~343-347)", flags="i")
fight(2.3001, "final", "todoroki", "dabi", "A", 1, note="Phosphor éteint les flammes de Dabi (ch. 349-353)")
fight(2.3002, "final", "afo", ["endeavor", "hawks", "tokoyami", "jiro"], "A", 1,
      note="Masque brisé, Prominence Burn, mais All For One se reforme, coupe le bras d'Endeavor et vole les ailes de Hawks (ch. 354-376)",
      flags="i")
fight(2.30021, "final", "tokoyami", "afo", "D", note="Dark Shadow cloue All For One au sol, il se libère et fuit (ch. ~376)", flags="i")
fight(2.3003, "final", "shigaraki", ["bakugo", "best_jeanist", "edgeshot"], "A", 3,
      note="Le cœur de Bakugo s'arrête ; Edgeshot le recoud de l'intérieur (ch. 359-362, 369)")
fight(2.30031, "final", "shigaraki", ["mirio", "tamaki", "nejire"], "A", 2,
      note="Les Big 3 gagnent du temps mais sont décimés (ch. 363-366)")
fight(2.3004, "final", "deku", "shigaraki", "D",
      note="Gearshift : Deku jette Shigaraki hors de Yuei, la conscience de Tenko reprend le dessus un temps (ch. 367-372)", flags="i")
fight(2.30041, "final", ["shoji", "koda"], "spinner", "D", note="Shoji et Koda retiennent Spinner géant (ch. ~373-381)", flags="i")
fight(2.30042, "final", ["aoyama", "hagakure"], "kunieda", "A", 1,
      note="Lasers d'Aoyama réfractés par Hagakure contre Kunieda (ch. ~377-380)", flags="e")
fight(2.30045, "final", ["mina", "kirishima", "shinso", "mt_lady"], "gigantomachia", "A", 1,
      note="Acide de Mina, lavage de cerveau de Shinso sur Gigantomachia (ch. 380-384)", flags="i")
fight(2.3005, "final", "afo", "gigantomachia", "A", 3, note="All For One foudroie et détruit Gigantomachia (ch. 385)")
fight(2.3006, "final", ["todoroki", "iida"], "dabi", "A", 1, tb=["epuise"],
      note="Dabi ranimé se consume ; Great Glacial Aegir de Shoto avec Ingenium l'éteint (ch. 363, ~386-391)", flags="?")
fight(2.30069, "final", "uraraka", "toga", "A", 1,
      note="Zero Gravity stoppe l'armée de doubles ; Toga meurt en transfusant son sang à Uraraka (ch. 374-395)", flags="i?")
fight(2.3007, "final", "afo", "all_might", "A", 2,
      note="All Might en armure piège All For One sous un laser mais l'armure lâche ; il est paralysé (ch. 397-402)")
fight(2.30072, "final", "afo", "stain", "A", 2, note="Stain paralyse un instant All For One, qui le tue (ch. ~401-402)")
fight(2.3008, "final", ["bakugo", "hawks", "all_might"], "afo", "A", 1, tb=["epuise"],
      note="Bakugo revient, épaulé par Hawks ; All For One, usé par Rewind, régresse en fœtus et disparaît (ch. 403-410)")
fight(2.301, "final", "deku", "shigaraki", "A", 1,
      note="Dernier duel au mont Fuji : Deku transmet One For All dans le poing, Shigaraki s'effrite en poussière (ch. 411-423)")
