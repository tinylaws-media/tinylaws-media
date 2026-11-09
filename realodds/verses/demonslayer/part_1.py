# Demon Slayer (Kimetsu no Yaiba), partie 1 : tout le manga de Gotōge (ch. 1-205), flash-back compris.
# Manga uniquement : pas de combats propres à l'anime ni aux films. "fight" est injecté par data.py.
# Numéros de chapitre vérifiés sur la liste des titres (Wikipedia) et les pages de chapitres du Kimetsu no Yaiba Wiki
# (fandom) ; "ch. ~N" = à un ou deux chapitres près.
# Repères de temps (t = années depuis le massacre de la famille Kamado) : entraînement chez Urokodaki 0.0-1.9,
# Sélection finale 2.0, marais 2.05, Asakusa 2.10, manoir Tsuzumi 2.13, Natagumo 2.20-2.21, rééducation 2.28,
# purge des Lunes inférieures 2.30, train de l'infini 2.35, Shinjuro 2.40, quartier des plaisirs 2.50,
# village des forgerons 2.60, entraînement des Piliers 2.70-2.79, manoir Ubuyashiki 2.7995,
# château de l'infini 2.800-2.8023, bataille finale 2.806-2.8106 (aube), Tanjiro démon 2.812.
# Flash-back : Yoriichi contre Muzan -400, Yoriichi contre Kokushibo -340 (Yoriichi a plus de 80 ans),
# passé d'Akaza (Hakuji) -120 (« plus d'un siècle » de démon, ch. 155), Urokodaki capture le démon aux mains
# -47 (« ère Keiō », ch. 7), Makomo -6.7 et Sabito -5.7 (Sélection finale de Giyu à 13 ans),
# Gyomei au temple -7, Sanemi et sa mère -6, mort de Kanae -1.8 (Shinobu avait 14 ans), jumeaux Tokito -0.5.
# Ces dates de flash-back sont des estimations (âges du fanbook), pas des dates données par le manga.
# Les morts des démons sont définitives. Les esprits de Sabito et Makomo gardent leur force à leur mort (edo_ref).

CHARS_PART = {
    # ---------------------------------------------------------------- pourfendeurs
    "tanjiro": ("Tanjiro Kamado", "Pourfendeurs", 0.2, None, None),
    "nezuko": ("Nezuko Kamado", "Kamado", 0.8, None, None),
    "zenitsu": ("Zenitsu Agatsuma", "Pourfendeurs", 1.3, None, None),
    "inosuke": ("Inosuke Hashibira", "Pourfendeurs", 1.5, None, None),
    "kanao": ("Kanao Tsuyuri", "Pourfendeurs", 2.8, None, None),
    "genya": ("Genya Shinazugawa", "Pourfendeurs", 1.0, 2.8019, None),
    "murata_corps": None,  # placeholder, retiré plus bas
    "pourfendeurs": ("Pourfendeurs et Kakushi (groupe)", "Pourfendeurs", 1.2, None, None),
    "giyu": ("Giyu Tomioka (Pilier de l'Eau)", "Piliers", 4.0, None, None),
    "shinobu": ("Shinobu Kocho (Pilier de l'Insecte)", "Piliers", 4.0, 2.8001, None),
    "rengoku": ("Kyojuro Rengoku (Pilier de la Flamme)", "Piliers", 4.2, 2.3503, None),
    "tengen": ("Tengen Uzui (Pilier du Son)", "Piliers", 4.0, None, None),
    "mitsuri": ("Mitsuri Kanroji (Pilier de l'Amour)", "Piliers", 4.0, 2.8112, None),
    "muichiro": ("Muichiro Tokito (Pilier de la Brume)", "Piliers", 1.0, 2.8019, None),
    "gyomei": ("Gyomei Himejima (Pilier du Rocher)", "Piliers", 2.5, 2.8112, None),
    "sanemi": ("Sanemi Shinazugawa (Pilier du Vent)", "Piliers", 1.0, None, None),
    "iguro": ("Obanai Iguro (Pilier du Serpent)", "Piliers", 4.0, 2.8112, None),
    "kanae": ("Kanae Kocho (Pilier de la Fleur)", "Piliers", 4.0, -1.8, None),
    "shinjuro": ("Shinjuro Rengoku (ancien Pilier de la Flamme)", "Piliers", 3.5, None, None),
    "urokodaki": ("Sakonji Urokodaki (ancien Pilier de l'Eau)", "Pourfendeurs", 4.0, None, None),
    "sabito": ("Sabito", "Pourfendeurs", 2.0, -5.7, -5.7),
    "makomo": ("Makomo", "Pourfendeurs", 1.5, -6.7, -6.7),
    "yoriichi": ("Yoriichi Tsugikuni", "Pourfendeurs (Sengoku)", 7.5, -339.99, None),
    # ---------------------------------------------------------------- alliés démons
    "tamayo": ("Tamayo", "Alliés démons", 2.5, 2.8065, None),
    "yushiro": ("Yushiro", "Alliés démons", 1.8, None, None),
    # ---------------------------------------------------------------- humains des flash-back
    "hakuji": ("Hakuji (Akaza humain)", "Humains", 1.5, None, None),
    "keizo": ("Keizo (dojo Soryu)", "Humains", 1.5, -120.05, None),
    "voyous": ("Voyous armés (groupe)", "Humains", 0.3, None, None),
    "dojo_rival": ("Élèves du dojo rival (67, groupe)", "Humains", 0.6, -120.0, None),
    # ---------------------------------------------------------------- Muzan et les Lunes
    "muzan": ("Muzan Kibutsuji", "Démons", 7.5, 2.8106, None),
    "kokushibo": ("Kokushibo (Lune supérieure 1)", "Lunes supérieures", 6.5, 2.8019, None),
    "doma": ("Doma (Lune supérieure 2)", "Lunes supérieures", 6.2, 2.8011, None),
    "akaza": ("Akaza (Lune supérieure 3)", "Lunes supérieures", 6.0, 2.8007, None),
    "hantengu": ("Hantengu (Lune supérieure 4)", "Lunes supérieures", 5.5, 2.6051, None),
    "gyokko": ("Gyokko (Lune supérieure 5)", "Lunes supérieures", 5.0, 2.6031, None),
    "gyutaro": ("Gyutaro (Lune supérieure 6)", "Lunes supérieures", 5.0, 2.5051, None),
    "daki": ("Daki (Lune supérieure 6)", "Lunes supérieures", 4.0, 2.5051, None),
    "kaigaku": ("Kaigaku (nouvelle Lune supérieure 6)", "Lunes supérieures", 4.5, 2.8004, None),
    "nakime": ("Nakime (Lune supérieure 4 de remplacement)", "Lunes supérieures", 4.0, 2.8023, None),
    "enmu": ("Enmu (Lune inférieure 1)", "Lunes inférieures", 3.5, 2.3501, None),
    "rui": ("Rui (Lune inférieure 5)", "Lunes inférieures", 3.3, 2.2091, None),
    "lunes_inferieures": ("Lunes inférieures 2 à 6 (Rokuro, Wakuraba, Mukago, Kamanue)", "Lunes inférieures", 3.0, 2.3001, None),
    "kyogai": ("Kyogai (ancienne Lune inférieure 6)", "Démons", 2.3, 2.1301, None),
    # ---------------------------------------------------------------- démons mineurs
    "demons_mineurs": ("Démons mineurs (groupe)", "Démons", 1.0, None, None),
    "demon_temple": ("Démon du temple (ch. 3)", "Démons", 0.8, 0.0101, None),
    "hand_demon": ("Démon aux mains", "Démons", 1.2, 2.0011, None),
    "swamp_demon": ("Démon du marais", "Démons", 1.3, 2.0501, None),
    "susamaru": ("Susamaru", "Démons", 2.0, 2.1001, None),
    "yahaba": ("Yahaba", "Démons", 2.0, 2.1001, None),
    "tongue_demon": ("Démon à la langue (manoir Tsuzumi)", "Démons", 1.0, 2.1201, None),
    "spider_mother": ("Mère araignée", "Famille araignée", 1.5, 2.2021, None),
    "spider_son": ("Frère araignée", "Famille araignée", 1.8, 2.2041, None),
    "spider_father": ("Père araignée", "Famille araignée", 2.6, 2.2071, None),
    "spider_sister": ("Sœur araignée", "Famille araignée", 1.6, 2.2101, None),
    "demon_gyomei": ("Démon du temple de Gyomei", "Démons", 1.5, -7.0, None),
    "mere_shinazugawa": ("Shizu Shinazugawa (mère démon)", "Démons", 0.8, -6.0, None),
    "demon_tokito": ("Démon des jumeaux Tokito", "Démons", 1.5, -0.5, None),
    "tanjiro_oni": ("Tanjiro, roi des démons", "Démons", 6.5, 2.8121, None),
}
del CHARS_PART["murata_corps"]

GENERIC_PART = {"pourfendeurs", "demons_mineurs", "lunes_inferieures", "voyous", "dojo_rival"}

# gains et pertes permanents : (perso, temps, changement moyen en échelons, écart-type, libellé)
JUMPS_PART = [
    ("tanjiro", 0.5, 0.7, 0.4, "Première année d'entraînement chez Urokodaki"),
    ("tanjiro", 1.6, 0.6, 0.4, "Respiration de l'Eau maîtrisée avec Sabito et Makomo, rocher tranché (ch. 5)"),
    ("tanjiro", 2.2085, 0.4, 0.3, "Découverte de la danse du dieu du feu (Hinokami Kagura, ch. 40)"),
    ("tanjiro", 2.285, 0.4, 0.3, "Concentration totale permanente (ch. 49-50)"),
    ("tanjiro", 2.5031, 0.3, 0.3, "Apparition de la Marque (ch. ~80-83)"),
    ("tanjiro", 2.75, 0.4, 0.3, "Entraînement des Piliers (ch. 129-136)"),
    ("nezuko", 1.9, 0.8, 0.5, "Deux ans de sommeil, adaptation de son corps de démon"),
    ("nezuko", 2.2081, 0.4, 0.3, "Éveil de son art démoniaque, le sang explosif (ch. 40)"),
    ("nezuko", 2.6052, 0.3, 0.3, "Nezuko surmonte le soleil (ch. 126-127)"),
    ("nezuko", 2.809, -2.0, 0.8, "Redevenue humaine grâce au remède de Tamayo (ch. ~196-197)"),
    ("zenitsu", 2.285, 0.4, 0.3, "Concentration totale permanente (ch. 50-51)"),
    ("zenitsu", 2.78, 0.5, 0.4, "Septième mouvement de la foudre créé seul (révélé ch. 145)"),
    ("inosuke", 2.285, 0.4, 0.3, "Concentration totale permanente (ch. 50-51)"),
    ("inosuke", 2.75, 0.3, 0.3, "Entraînement des Piliers"),
    ("zenitsu", 2.75, 0.3, 0.3, "Entraînement des Piliers"),
    ("kanao", 2.75, 0.3, 0.3, "Entraînement des Piliers"),
    ("genya", 2.4, 1.0, 0.6, "Dévoration de démons, fusil et entraînement auprès de Gyomei"),
    ("genya", 2.75, 0.3, 0.3, "Entraînement des Piliers et de Gyomei"),
    ("muichiro", 1.0, 2.5, 1.0, "Pilier deux mois après avoir pris le sabre"),
    ("muichiro", 2.6025, 0.6, 0.4, "Mémoire retrouvée et Marque (ch. 118-119)"),
    ("mitsuri", 2.6036, 0.3, 0.3, "Marque éveillée contre Zohakuten (ch. 123)"),
    ("giyu", 2.8008, 0.3, 0.3, "Marque éveillée contre Akaza (ch. 151)"),
    ("sanemi", 2.802, 0.3, 0.3, "Marque éveillée contre Kokushibo (ch. ~167-168)"),
    ("gyomei", 2.802, 0.3, 0.3, "Marque éveillée contre Kokushibo (ch. ~168)"),
    ("iguro", 2.8085, 0.3, 0.3, "Marque éveillée contre Muzan (ch. ~189)"),
    ("gyomei", -5.0, 1.5, 0.8, "Entré dans le corps grâce à Kagaya, devient Pilier du Rocher"),
    ("sanemi", -3.0, 2.5, 1.0, "Entraînement, devient Pilier du Vent"),
    ("tengen", 2.51, -1.5, 0.7, "Perte d'une main et d'un œil, retraite (ch. 97)"),
    ("kanao", 2.8012, -0.3, 0.3, "Œil droit abîmé par l'Œil du jardin d'équinoxe (ch. 162-163)"),
]

# ============================================================== Ère Sengoku (flash-back)
fight(-400.0, "sengoku", "yoriichi", "muzan", "A", 3,
      note="Treizième mouvement ; Muzan éclate en 1800 morceaux, Yoriichi en tranche 1500 et il s'enfuit (ch. 187)")
fight(-340.0, "sengoku", "yoriichi", "kokushibo", "A", 2, ta=["age"],
      note="Yoriichi, plus de 80 ans, tranche le cou de Kokushibo puis meurt debout avant le coup final (ch. 174)", flags="i")

# ============================================================== Avant l'histoire (flash-back)
fight(-120.3, "avant", "hakuji", "voyous", "A", 3, note="Hakuji assomme sept hommes armés à mains nues (ch. 154)")
fight(-120.2, "avant", "keizo", "hakuji", "A", 3, note="Keizo met Hakuji K.-O. d'un coup et le prend comme élève (ch. 154)")
fight(-120.0, "avant", "hakuji", "dojo_rival", "A", 3, note="Après l'empoisonnement du puits, il tue 67 élèves à mains nues (ch. 155)")
fight(-119.99, "avant", "muzan", "hakuji", "A", 3, note="Muzan lui transperce la tête et en fait Akaza (ch. 155)")
fight(-47.0, "avant", "urokodaki", "hand_demon", "A", 2, note="Urokodaki capture le démon aux mains à l'ère Keiō (ch. 7)")
fight(-7.0, "avant", "gyomei", "demon_gyomei", "A", 2,
      note="Moine aveugle sans entraînement, il écrase la tête du démon à coups de poing jusqu'à l'aube pour protéger Sayo (ch. 135)")
fight(-6.7, "avant", "hand_demon", "makomo", "A", 2,
      note="Makomo tuée à sa Sélection finale, avant Sabito (ch. 6-7) ; date estimée", flags="?")
fight(-6.0, "avant", "sanemi", "mere_shinazugawa", "A", 2,
      note="Sanemi, adolescent, tue sa mère changée en démon en la retenant jusqu'à l'aube (ch. 115) ; date estimée", flags="?")
fight(-5.71, "avant", "sabito", "demons_mineurs", "A", 3, note="Sabito tue presque tous les démons du mont Fujikasane (ch. 7)")
fight(-5.7, "avant", "hand_demon", "sabito", "A", 1, tb=["epuise"],
      note="La lame de Sabito se brise sur le cou du démon aux mains (ch. 7)")
fight(-1.8, "avant", "doma", "kanae", "A", 2,
      note="Doma tue Kanae, Shinobu arrive à sa mort (souvenirs ch. 141-143) ; date estimée")
fight(-0.5, "avant", "muichiro", "demon_tokito", "A", 2, ta=["boost"],
      note="Rage de Muichiro, 11 ans : il écrase le démon qui a blessé Yuichiro jusqu'à l'aube (ch. 118) ; date estimée")

# ============================================================== Massacre et entraînement (t 0-1.9)
fight(0.0, "avant", "giyu", ["tanjiro", "nezuko"], "A", 3, ta=["retenue"], tb=["surprise"],
      note="Hache lancée de derrière l'arbre ; Giyu assomme Tanjiro puis Nezuko et les épargne (ch. 1)")
fight(0.01, "avant", ["tanjiro", "nezuko"], "demon_temple", "A", 1,
      note="Tanjiro cloue la tête du démon à un arbre avec sa hache, Nezuko lui arrache la tête ; il brûle à l'aube (ch. 3)")
fight(1.3, "avant", "sabito", "tanjiro", "A", 3, ta=["retenue"],
      note="Esprit de Sabito, sabre de bois contre sabre réel ; il bat Tanjiro deux fois (ch. 5)")
fight(1.8, "avant", "tanjiro", "sabito", "A", 1,
      note="Six mois plus tard, Tanjiro frappe le premier et fend le masque de Sabito (ch. 5)")

# ============================================================== Sélection finale
fight(2.0, "selection", "tanjiro", "demons_mineurs", "A", 3, note="Deux démons tués d'entrée (ch. 6)")
fight(2.001, "selection", "tanjiro", "hand_demon", "A", 2, note="Tanjiro tranche le cou épais du démon aux mains (ch. 7-8)")
fight(2.002, "selection", "tanjiro", "genya", "A", 2,
      note="Tanjiro tord le poignet de Genya qui tirait les cheveux d'une jumelle Ubuyashiki (ch. 8)", flags="?")
fight(2.05, "selection", ["tanjiro", "nezuko"], "swamp_demon", "A", 2,
      note="Démon du marais à trois corps ; Nezuko tient l'un, Tanjiro tue les autres (ch. 10-12)")

# ============================================================== Asakusa et manoir Tsuzumi
fight(2.1, "asakusa", ["tanjiro", "yushiro"], "yahaba", "A", 2,
      note="Vision partagée de Yushiro, Tanjiro décapite Yahaba (ch. 16-18)", flags="e")
fight(2.1001, "asakusa", ["nezuko", "tamayo"], "susamaru", "A", 2, ta=["prepa"],
      note="Nezuko renvoie les temari, Tamayo pousse Susamaru à dire le nom de Muzan : la malédiction la tue (ch. 16-18)", flags="e")
fight(2.12, "asakusa", "zenitsu", "tongue_demon", "A", 2, note="Zenitsu endormi, premier mouvement (ch. 23)")
fight(2.13, "asakusa", "tanjiro", "kyogai", "A", 1, ta=["epuise"],
      note="Tanjiro, côtes et jambes blessées depuis Asakusa, décapite Kyogai (ch. 24-25)")
fight(2.131, "asakusa", "inosuke", "zenitsu", "A", 2, tb=["protege"],
      note="Zenitsu se laisse rouer de coups pour protéger la boîte de Nezuko (ch. 26)")
fight(2.132, "asakusa", "tanjiro", "inosuke", "A", 1,
      note="Combat à mains nues, coup de tête de Tanjiro, Inosuke s'évanouit (ch. 26-27)")

# ============================================================== Mont Natagumo
fight(2.201, "natagumo", "spider_mother", "pourfendeurs", "A", 2, ta=["prepa"],
      note="Pourfendeurs changés en marionnettes par les fils (ch. 29-30)")
fight(2.202, "natagumo", ["tanjiro", "inosuke"], "spider_mother", "A", 2,
      note="Tanjiro lui offre une mort douce (pluie bienfaisante) (ch. 31-32)")
fight(2.204, "natagumo", "zenitsu", "spider_son", "A", 1, ta=["malade"],
      note="Zenitsu empoisonné, foudre en six éclairs, il décapite le frère (ch. 33-35)")
fight(2.205, "natagumo", "spider_father", ["tanjiro", "inosuke"], "A", 1,
      note="Le père projette Tanjiro au loin (ch. 34-36)", flags="i")
fight(2.206, "natagumo", "spider_father", "inosuke", "A", 2, note="Le père mué brise les lames d'Inosuke et l'étrangle (ch. 36-37)", flags="i")
fight(2.207, "natagumo", "giyu", "spider_father", "A", 3, note="Giyu le tranche d'un coup (ch. 37)")
fight(2.208, "natagumo", "rui", ["tanjiro", "nezuko"], "A", 1, tb=["boost"],
      note="Danse du dieu du feu et sang explosif ; Rui s'était coupé la tête lui-même, Tanjiro à bout de forces (ch. 37-40)", flags="i")
fight(2.209, "natagumo", "giyu", "rui", "A", 3, note="Onzième mouvement, la mer d'huile ; Giyu décapite Rui (ch. 40)")
fight(2.21, "natagumo", "shinobu", "spider_sister", "A", 3, note="Shinobu tue la sœur au poison de glycine (ch. 41-42)")
fight(2.211, "natagumo", "giyu", "shinobu", "D", ta=["retenue"], tb=["retenue"],
      note="Giyu empêche Shinobu de tuer Nezuko (ch. 42-43)", flags="i")

# ============================================================== Rééducation et purge des Lunes inférieures
fight(2.28, "natagumo", "kanao", ["tanjiro", "zenitsu", "inosuke"], "A", 2,
      note="Poursuite et jeu des tasses ; aucun des trois ne la bat (ch. 49)")
fight(2.29, "natagumo", "tanjiro", "kanao", "A", 1,
      note="Après la concentration totale permanente, Tanjiro gagne la poursuite et les réflexes (ch. 50)")
fight(2.3, "mugen", "muzan", "lunes_inferieures", "A", 3, note="Muzan exécute les Lunes inférieures, seul Enmu est épargné (ch. 51-52)")

# ============================================================== Train de l'infini
fight(2.35, "mugen", ["tanjiro", "inosuke"], "enmu", "A", 1, tb=["prepa"],
      note="Enmu endort tout le train ; Zenitsu, Nezuko et Rengoku protègent les voitures, Tanjiro et Inosuke tranchent l'os du cou (ch. 55-63)",
      flags="e")
fight(2.3502, "mugen", "akaza", "rengoku", "A", 1,
      note="Rengoku mortellement blessé mais tient jusqu'à l'aube, Akaza fuit le soleil (ch. 63-66)")
fight(2.4, "mugen", "tanjiro", "shinjuro", "A", 1, tb=["malade"],
      note="Shinjuro ivre plaque et frappe Tanjiro, qui répond d'un coup de tête ; le K.-O. de Shinjuro n'est pas confirmé par le wiki (ch. 68)",
      flags="?")

# ============================================================== Quartier des plaisirs
fight(2.502, "yuukaku", "tanjiro", "daki", "D", ta=["boost", "marque"],
      note="Danse du dieu du feu, la Marque apparaît ; Tanjiro s'effondre au moment de la décapiter (ch. 80-83)", flags="i")
fight(2.503, "yuukaku", "nezuko", "daki", "A", 2, ta=["boost"],
      note="Nezuko éveillée domine Daki, qui ne peut mourir sans lame ; Tanjiro calme sa sœur (ch. 83-85)", flags="i")
fight(2.504, "yuukaku", "tengen", "daki", "A", 3, note="Tengen décapite Daki sans effort, Gyutaro surgit (ch. 86)")
fight(2.505, "yuukaku", ["tengen", "tanjiro", "zenitsu", "inosuke"], ["gyutaro", "daki"], "A", 1, ta=["prepa"],
      note="Partition de Tengen et kunai à la glycine de Hinatsuru ; Tengen et Tanjiro décapitent Gyutaro, Zenitsu et Inosuke Daki (ch. 86-95)",
      flags="e")

# ============================================================== Village des forgerons
fight(2.601, "forgerons", ["tanjiro", "genya", "nezuko"], "hantengu", "D",
      note="Tanjiro décapite le vieillard, qui se divise en Sekido, Karaku, Aizetsu et Urogi (ch. 106-115)", flags="i")
fight(2.602, "forgerons", "gyokko", "muichiro", "A", 1, tb=["protege"],
      note="Muichiro, protégeant Kotetsu et les forgerons, piégé dans la jarre d'eau (ch. 115-117)", flags="i")
fight(2.603, "forgerons", "muichiro", "gyokko", "A", 3, ta=["marque"],
      note="Mémoire retrouvée et Marque : Muichiro décapite Gyokko (ch. 118-122)")
fight(2.6035, "forgerons", "mitsuri", "hantengu", "D", ta=["marque"],
      note="Mitsuri tient tête à Zohakuten avec la Marque (ch. 122-125)", flags="i")
fight(2.605, "forgerons", ["tanjiro", "nezuko", "genya", "mitsuri"], "hantengu", "A", 1, ta=["marque", "boost"],
      note="Lame embrasée par le sang de Nezuko ; Tanjiro décapite le vrai corps, Nezuko surmonte le soleil (ch. 124-127)")

# ============================================================== Entraînement des Piliers
fight(2.73, "entrainement", "muichiro", "tanjiro", "D", ta=["retenue"],
      note="Assauts rapides chez Muichiro, Tanjiro tient le rythme, pas de vainqueur (ch. 132)", flags="?")
fight(2.74, "entrainement", "tanjiro", "iguro", "A", 1, tb=["retenue"],
      note="Au bout de quatre jours Tanjiro touche le vêtement d'Iguro et réussit l'épreuve (ch. 132)")
fight(2.75, "entrainement", "sanemi", "tanjiro", "A", 3, note="Sparring sans pitié, Tanjiro couvert d'ecchymoses (ch. 132)")
fight(2.76, "entrainement", "sanemi", "tanjiro", "D", ta=["retenue"],
      note="Bagarre quand Sanemi s'en prend à Genya ; Tanjiro le frappe au visage, on les sépare (ch. 133)", flags="i")

# ============================================================== Manoir Ubuyashiki et château de l'infini
fight(2.7995, "chateau", ["gyomei", "tamayo", "sanemi", "giyu", "iguro", "mitsuri", "muichiro", "tanjiro"], "muzan", "D",
      ta=["prepa"], note="Explosion de Kagaya, drogue de Tamayo, fléau de Gyomei ; Muzan absorbe Tamayo et précipite tout le monde dans le château (ch. 137-139)",
      flags="i")
fight(2.8, "chateau", "doma", "shinobu", "A", 2,
      note="Le poison de Shinobu ne suffit pas, Doma l'absorbe (ch. 141-143)")
fight(2.8003, "chateau", "zenitsu", "kaigaku", "A", 1, note="Septième mouvement, Honoikazuchi no Kami : Zenitsu décapite Kaigaku (ch. 144-145)")
fight(2.8006, "chateau", ["tanjiro", "giyu"], "akaza", "A", 1, ta=["marque", "boost"],
      note="Marque de Giyu, Monde transparent de Tanjiro qui décapite Akaza ; Akaza régénéré renonce et se détruit (ch. 147-156)",
      flags="e")
fight(2.8008, "chateau", "doma", "kanao", "D", note="Kanao seule face à Doma jusqu'à l'arrivée d'Inosuke (ch. 157-158)", flags="i")
fight(2.801, "chateau", ["kanao", "inosuke"], "doma", "A", 1, ta=["prepa", "boost"],
      note="Le poison du corps de Shinobu défait Doma ; Œil du jardin d'équinoxe de Kanao, Inosuke lance ses lames (ch. 158-163)",
      flags="e")
fight(2.8013, "chateau", "kokushibo", "muichiro", "A", 3, tb=["marque"],
      note="Muichiro perd un bras et est cloué à un pilier par son propre sabre (ch. 164-165)")
fight(2.8014, "chateau", "kokushibo", "genya", "A", 3, note="Genya perd ses bras et est coupé en deux (ch. 166)")
fight(2.8015, "chateau", "sanemi", "kokushibo", "D", ta=["marque"],
      note="Sanemi seul tient Kokushibo jusqu'à l'arrivée de Gyomei (ch. 166-168)", flags="i?")
fight(2.8016, "chateau", ["gyomei", "sanemi"], "kokushibo", "D", ta=["marque", "boost"],
      note="Marques et Monde transparent de Gyomei (ch. 168-172)", flags="i")
fight(2.8018, "chateau", ["gyomei", "sanemi", "muichiro", "genya"], "kokushibo", "A", 1, ta=["marque", "boost"],
      note="Lame rouge de Muichiro, balles et arbre démoniaques de Genya ; décapité, Kokushibo voit son reflet et se défait (ch. 173-177)")
fight(2.802, "chateau", ["iguro", "mitsuri"], "nakime", "D",
      note="Nakime déplace les pièces, ils ne l'atteignent pas (ch. 178-180)", flags="i")
fight(2.8022, "chateau", ["yushiro", "iguro", "mitsuri"], "nakime", "A", 2, ta=["prepa"],
      note="Yushiro prend le contrôle de son cerveau, Muzan l'écrase pour reprendre la main ; le château remonte (ch. 179-181)")

# ============================================================== Bataille finale contre Muzan, jusqu'à l'aube
fight(2.806, "aube", "muzan", ["giyu", "tanjiro"], "A", 2, ta=["malade"], tb=["marque"],
      note="Tanjiro empoisonné par le sang de Muzan s'effondre (ch. 181-183)", flags="i")
fight(2.807, "aube", "muzan", ["iguro", "mitsuri", "giyu", "pourfendeurs"], "A", 1, ta=["malade"],
      note="Iguro lui tranche le cou sans effet, Muzan fauche les pourfendeurs (ch. 184-185)", flags="i")
fight(2.808, "aube", "muzan", ["gyomei", "sanemi", "giyu", "iguro", "mitsuri", "kanao", "inosuke", "zenitsu"], "A", 1,
      ta=["malade"], tb=["marque", "boost"],
      note="Lames rouges et Monde transparent ; Mitsuri mise hors combat, Gyomei perd une jambe, Giyu un bras, tous à terre (ch. 186-191)",
      flags="i")
fight(2.809, "aube", "tanjiro", "muzan", "D", ta=["marque", "boost"], tb=["malade"],
      note="Tanjiro revient avec la danse du dieu du feu et le treizième mouvement ; la drogue de Tamayo vieillit et ronge Muzan (ch. 191-198)",
      flags="i")
fight(2.8105, "aube", ["tanjiro", "giyu", "gyomei", "sanemi", "iguro", "inosuke", "zenitsu", "kanao", "yushiro", "pourfendeurs"], "muzan",
      "A", 1, ta=["prepa", "marque", "boost"], tb=["malade"],
      note="Muzan retenu jusqu'au lever du soleil (chaîne de Gyomei, Kakushi, tramways) ; il se change en nourrisson géant et meurt au soleil (ch. 198-200)")
fight(2.812, "aube", ["kanao", "giyu", "nezuko", "inosuke", "zenitsu"], "tanjiro_oni", "A", 1, ta=["prepa", "boost"],
      tb=["retenue"],
      note="Muzan fait de Tanjiro le roi des démons ; Nezuko (humaine) le retient, Giyu pare, Kanao injecte le remède avec "
           "l'Œil du jardin d'équinoxe ; Tanjiro se retenait pour ne pas tuer Nezuko et redevient humain (ch. 201-204)",
      flags="?")
