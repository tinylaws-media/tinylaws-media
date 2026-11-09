# Jujutsu Kaisen, partie 1 : tout le manga d'Akutami (ch. 1-271), Jujutsu Kaisen 0 (ch. 0-1 à 0-4) et la suite
# officielle Jujutsu Kaisen Modulo (scénario Akutami, dessin Yuji Iwasaki, Weekly Shonen Jump, sept. 2025 - mars 2026,
# 3 volumes, ~25 ch.), située en 2086. Manga uniquement : aucun combat propre à l'anime. "fight" est injecté par data.py.
# Numéros de chapitre vérifiés sur les résumés de chapitres du Jujutsu Kaisen Wiki (miroir daddyjim.com, le fandom
# étant inaccessible) et, pour Modulo, sur Beebom / ComicBook / Soap Central. "ch. ~N" = à un ou deux chapitres près.
# Repères de temps (t = années depuis juin 2018) : passé 2006 = -12, JJK0 -1.0 à -0.92, débuts 0.0-0.2, Kyoto 0.25,
# Peinture de la mort 0.3-0.31, Shibuya 0.35-0.365, Jeu d'abattage 0.45-0.557, Shinjuku 0.6-0.602, Modulo 68.4-68.6.
# Les combats de Shinjuku sont ordonnés à 0.0001 près dans l'ordre des chapitres.
# Sukuna = un seul id ("sukuna") : dans Yuji, dans Megumi puis forme Heian, avec JUMPS pour les doigts et les corps.

CHARS_PART = {
    # ---------------------------------------------------------------- exorcistes de Tokyo
    "gojo": ("Satoru Gojo", "Exorcistes de Tokyo", 5.5, 0.6001, None),
    "geto": ("Suguru Geto", "Exorcistes / Fidèles de Geto", 4.0, -0.92, None),
    "yuta": ("Yuta Okkotsu", "Exorcistes de Tokyo", 4.0, None, None),
    "maki": ("Maki Zen'in", "Exorcistes de Tokyo", 2.0, None, None),
    "panda": ("Panda", "Exorcistes de Tokyo", 2.5, None, None),
    "toge": ("Toge Inumaki", "Exorcistes de Tokyo", 2.5, None, None),
    "yuji": ("Yuji Itadori", "Exorcistes de Tokyo", 1.5, None, None),
    "megumi": ("Megumi Fushiguro", "Exorcistes de Tokyo", 2.0, None, None),
    "nobara": ("Nobara Kugisaki", "Exorcistes de Tokyo", 1.8, None, None),
    "nanami": ("Kento Nanami", "Exorcistes de Tokyo", 3.0, 0.36, None),
    "mei_mei": ("Mei Mei", "Exorcistes", 3.0, None, None),
    "kusakabe": ("Atsuya Kusakabe", "Exorcistes de Tokyo", 3.0, None, None),
    "ino": ("Takuma Ino", "Exorcistes de Tokyo", 2.3, None, None),
    "yuki": ("Yuki Tsukumo", "Exorcistes", 4.0, 0.54, None),
    "hakari": ("Kinji Hakari", "Exorcistes de Tokyo", 3.5, None, None),
    "kirara": ("Kirara Hoshi", "Exorcistes de Tokyo", 2.0, None, None),
    "miguel": ("Miguel Oduol", "Fidèles de Geto / alliés", 3.0, None, None),
    "larue": ("Larue", "Fidèles de Geto / alliés", 2.8, None, None),
    # ---------------------------------------------------------------- exorcistes de Kyoto
    "todo": ("Aoi Todo", "Exorcistes de Kyoto", 3.5, None, None),
    "mai": ("Mai Zen'in", "Exorcistes de Kyoto", 1.5, 0.4555, None),
    "momo": ("Momo Nishimiya", "Exorcistes de Kyoto", 1.8, None, None),
    "miwa": ("Kasumi Miwa", "Exorcistes de Kyoto", 1.4, None, None),
    "noritoshi": ("Noritoshi Kamo", "Exorcistes de Kyoto", 2.8, None, None),
    "mechamaru": ("Mechamaru (Kokichi Muta)", "Exorcistes de Kyoto", 2.5, 0.35, None),
    # ---------------------------------------------------------------- clan Zen'in
    "naobito": ("Naobito Zen'in", "Clan Zen'in", 3.5, 0.44, None),
    "ogi": ("Ogi Zen'in", "Clan Zen'in", 3.0, 0.456, None),
    "zenin_hei": ("Hei et unité Kukuru du clan Zen'in (groupe)", "Clan Zen'in", 2.5, 0.457, None),
    "naoya": ("Naoya Zen'in", "Clan Zen'in", 3.0, 0.458, None),
    "naoya_fleau": ("Naoya Zen'in (fléau vengeur)", "Fléaux", 4.0, 0.53, None),
    # ---------------------------------------------------------------- tueurs, ennemis humains
    "toji": ("Toji Fushiguro", "Tueur de sorciers", 6.0, -11.993, -11.993),
    "kenjaku": ("Kenjaku (corps de Geto)", "Kenjaku", 4.5, 0.6004, None),
    "uraume": ("Uraume", "Kenjaku / Sukuna", 4.0, 0.6018, None),
    "junpei": ("Junpei Yoshino", "Utilisateurs maudits", 1.0, 0.2, None),
    "juzo": ("Juzo Kumiya", "Utilisateurs maudits", 1.5, None, None),
    "haruta": ("Haruta Shigemo", "Utilisateurs maudits", 2.0, None, None),
    "hasaba": ("Jumelles Hasaba (Mimiko et Nanako)", "Utilisateurs maudits", 2.0, 0.355, None),
    # ---------------------------------------------------------------- fléaux
    "sukuna": ("Ryomen Sukuna", "Fléaux", 7.5, 0.6018, None),
    "mahoraga": ("Mahoraga (Général divin des Dix Ombres)", "Shikigami", 5.5, None, None),
    "jogo": ("Jogo", "Fléaux", 5.0, 0.356, None),
    "hanami": ("Hanami", "Fléaux", 4.8, 0.3502, None),
    "dagon": ("Dagon", "Fléaux", 4.8, 0.353, None),
    "mahito": ("Mahito", "Fléaux", 4.5, None, None),   # absorbé par Kenjaku (ch. 133), réapparaît dans Modulo
    "choso": ("Choso", "Peintures de la mort", 4.0, 0.6011, None),
    "eso": ("Eso", "Peintures de la mort", 3.0, 0.31, None),
    "kechizu": ("Kechizu", "Peintures de la mort", 2.5, 0.31, None),
    "smallpox": ("Divinité de la variole (fléau)", "Fléaux", 3.8, 0.3515, None),
    "fleau_detention": ("Fléau du centre de détention (porteur de doigt)", "Fléaux", 4.3, 0.041, None),
    "fleau_yasohachi": ("Fléau du pont Yasohachi (porteur de doigt)", "Fléaux", 4.3, 0.3, None),
    "fleaux_divers": ("Fléaux divers (groupe)", "Fléaux", 1.5, None, None),
    "kurourushi": ("Kurourushi", "Fléaux", 3.5, 0.502, None),
    # ---------------------------------------------------------------- joueurs du Jeu d'abattage
    "higuruma": ("Hiromi Higuruma", "Joueurs du jeu d'abattage", 3.5, 0.6005, None),
    "reggie": ("Reggie Star", "Joueurs du jeu d'abattage", 2.5, 0.49, None),
    "charles": ("Charles Bernard", "Joueurs du jeu d'abattage", 2.5, None, None),
    "kashimo": ("Hajime Kashimo", "Joueurs du jeu d'abattage", 4.3, 0.6002, None),
    "dhruv": ("Dhruv Lakdawalla", "Joueurs du jeu d'abattage", 3.0, 0.5, None),
    "ryu_ishigori": ("Ryu Ishigori", "Joueurs du jeu d'abattage", 3.8, 0.557, None),
    "uro": ("Takako Uro", "Joueurs du jeu d'abattage", 3.5, None, None),
    "takaba": ("Fumihiko Takaba", "Joueurs du jeu d'abattage", 2.5, None, None),
    "hana_kurusu": ("Hana Kurusu (Angel)", "Joueurs du jeu d'abattage", 3.0, None, None),
    "yorozu": ("Yorozu (dans Tsumiki)", "Joueurs du jeu d'abattage", 4.3, 0.557, None),
    # ---------------------------------------------------------------- Modulo (2086)
    "tsurugi": ("Tsurugi Okkotsu", "Exorcistes (2086)", 3.5, None, None),
    "yuka": ("Yuka Okkotsu", "Exorcistes (2086)", 3.5, None, None),
    "usami": ("Usami (clan Inumaki)", "Exorcistes (2086)", 3.0, None, None),
    "masaki": ("Masaki Takeda", "Utilisateurs maudits (2086)", 3.0, None, None),
    "maru": ("Maru (Marulu Val Vol Yelvori)", "Simuriens", 4.5, None, None),
    "dabura": ("Dabura Karaba", "Simuriens", 6.0, None, None),
}

GENERIC_PART = {"fleaux_divers", "zenin_hei", "hasaba"}

# (personnage, temps, changement moyen en échelons, écart-type, description)
JUMPS_PART = [
    # Sukuna : un doigt dans Yuji, puis doigts, corps de Megumi, forme Heian
    ("sukuna", -999.0, -4.0, 1.0, "Mort et scellement en vingt doigts : il ne reste qu'un doigt dans Yuji (ch. 1)"),
    ("sukuna", 0.01, 0.3, 0.3, "Deuxième doigt donné par Gojo (ch. 3)"),
    ("sukuna", 0.041, 0.3, 0.3, "Doigt du fléau du centre de détention (ch. 8-9)"),
    ("sukuna", 0.32, 0.5, 0.4, "Doigts du pont Yasohachi et des Peintures de la mort (ch. 58-63)"),
    ("sukuna", 0.3545, 2.0, 0.8, "Jogo lui fait avaler dix doigts : quinze doigts (ch. 111-112)"),
    ("sukuna", 0.554, 0.8, 0.8, "Prend le corps de Megumi et les Dix Ombres (ch. 212)"),
    ("sukuna", 0.58, 0.4, 0.5, "Ingère les doigts restants avant Shinjuku (ch. ~221)"),
    ("sukuna", 0.60015, 1.0, 0.8, "Retrouve sa vraie forme de l'ère Heian (ch. 237)"),
    # Gojo
    ("gojo", -11.996, 1.5, 0.8, "Éveil après sa mort face à Toji : technique inversée, Violet (ch. 75)"),
    # Yuta
    ("yuta", -0.91, -0.6, 0.6, "Rika libérée de sa malédiction (fin de JJK0)"),
    ("yuta", 0.37, 1.0, 0.8, "Retour d'étranger : Rika extérieure, copie, domaine (ch. 139)"),
    # Yuji
    ("yuji", 0.2542, 0.6, 0.5, "Premier Éclair noir, contrôle de l'énergie occulte (ch. 48)"),
    ("yuji", 0.37, 0.6, 0.5, "Éclair noir maîtrisé après Shibuya (ch. 132)"),
    ("yuji", 0.59, 0.8, 0.6, "Manipulation du sang et Démantèlement de Sukuna (ch. 252-257)"),
    ("yuji", 0.6016, 0.4, 0.5, "Expansion du territoire (ch. 264)"),
    ("yuji", 68.0, 1.5, 1.0, "Ellipse de 68 ans : techniques de Sukuna maîtrisées (Modulo)"),
    # Megumi
    ("megumi", 0.3, 0.5, 0.4, "Ébauche d'Expansion du territoire : Jardin des ombres chimériques (ch. 58)"),
    # Maki
    ("maki", 0.4555, 2.0, 0.8, "Restriction céleste complète après la mort de Mai (ch. 149)"),
    # Todo
    ("todo", 0.364, -1.0, 0.6, "Perte de la main gauche face à Mahito (ch. 129)"),
    ("todo", 0.6, 0.5, 0.5, "Main prothétique pour Boogie Woogie (ch. 259)"),
    # Kenjaku
    ("kenjaku", 0.363, 0.5, 0.5, "Absorbe Mahito : Uzumaki et Transfiguration (ch. 133)"),
    # Mahito
    ("mahito", 0.3607, 1.0, 0.7, "Éveil : Corps instantané de la Transfiguration (ch. 125-126)"),
]

# ============================================================================== ère Heian
fight(-1000.0, "heian", "sukuna", "uro", "A", 3,
      note="Sukuna anéantit l'escouade des Cinq Généraux vides d'Uro, qui en réchappe de peu (évoqué ch. 216)", flags="?")

# ============================================================================== passé de Gojo et Geto (2006)
fight(-12.0, "passe", "toji", "gojo", "A", 3, ta=["surprise", "prepa"],
      note="Toji poignarde Gojo, épuisé par trois jours sans sommeil, avec la Lame inversée céleste (ch. 70)")
fight(-11.998, "passe", "toji", "geto", "A", 3, ta=["prepa"],
      note="Toji bat Geto et ses fléaux au Tombeau des étoiles (ch. 71)")
fight(-11.994, "passe", "gojo", "toji", "A", 3,
      note="Gojo éveillé revient et pulvérise Toji avec le Violet (ch. 73-75)")

# ============================================================================== Jujutsu Kaisen 0 (2017)
fight(-1.0, "jjk0", ["yuta", "maki"], "fleaux_divers", "A", 2,
      note="Yuta et Maki dans l'école ; Rika écrase le fléau (ch. 0-2)")
fight(-0.98, "jjk0", ["yuta", "toge"], "fleaux_divers", "A", 2,
      note="Yuta et Inumaki contre un fléau de grade 1 dans la galerie commerciale (ch. 0-3)", flags="?")
fight(-0.93, "jjk0", "geto", ["maki", "panda", "toge"], "A", 3,
      note="Défilé des cent démons : Geto balaie Maki, Panda et Inumaki à l'école (ch. 0-4)")
fight(-0.929, "jjk0", "gojo", "miguel", "A", 2, ta=["retenue"],
      note="Miguel retient Gojo à Shinjuku puis se replie (ch. 0-4)", flags="i?")
fight(-0.925, "jjk0", "yuta", "geto", "A", 2, ta=["boost"],
      note="Yuta offre sa vie à Rika (pleine puissance) et ampute Geto ; Gojo l'achève (ch. 0-4)")

# ============================================================================== débuts de Yuji (2018)
fight(0.0, "debut", "sukuna", "fleaux_divers", "A", 3,
      note="Yuji avale le doigt, Sukuna massacre les fléaux du lycée (ch. 1-2)")
fight(0.001, "debut", "gojo", "sukuna", "A", 3, ta=["retenue"],
      note="Gojo neutralise Sukuna (un doigt) d'une main, sans technique (ch. 2)")
fight(0.04, "debut", "fleau_detention", "yuji", "A", 3,
      note="Le fléau de grade spécial du centre de détention surclasse Yuji (ch. 7)")
fight(0.0405, "debut", "sukuna", "fleau_detention", "A", 3,
      note="Sukuna prend le contrôle et déchiquette le fléau (ch. 8)")
fight(0.042, "debut", "sukuna", "megumi", "A", 2, ta=["retenue"],
      note="Sukuna, sans cœur pour Yuji, joue avec Megumi ; Yuji reprend le contrôle avant Mahoraga (ch. 9)",
      flags="i")
fight(0.1, "debut", "gojo", "jogo", "A", 3, ta=["domaine"],
      note="Gojo humilie Jogo et l'enferme dans le Vide infini ; Hanami le sauve (ch. 14-15)")
fight(0.15, "debut", "todo", "megumi", "A", 2,
      note="Todo malmène Megumi ; la Parole d'Inumaki et Panda l'arrêtent (ch. 17)", flags="i")
fight(0.151, "debut", "nobara", "mai", "D",
      note="Mai tire sur Nobara, Maki s'interpose ; Nobara se relève et plaque Mai (ch. 17-18)", flags="i")
fight(0.18, "debut", "nanami", "mahito", "D",
      note="Premier choc dans les égouts ; Mahito s'enfuit, Nanami épargné par sa résistance (ch. 21-22)")
fight(0.2, "debut", "yuji", "junpei", "A", 2,
      note="Yuji maîtrise Junpei sans le blesser (ch. 25)")
fight(0.201, "debut", ["yuji", "nanami"], "mahito", "A", 1, tb=["domaine"],
      note="Yuji frappe l'âme de Mahito ; il ouvre son domaine sur Nanami, Yuji y entre et Mahito fuit (ch. 26-30)",
      flags="e")

# ============================================================================== rencontre d'échange avec Kyoto
fight(0.25, "kyoto", "todo", "yuji", "D", ta=["retenue"],
      note="Todo teste puis entraîne Yuji, le combat devient une leçon (ch. 36-38)", flags="i")
fight(0.2505, "kyoto", "panda", "mechamaru", "A", 1,
      note="Mode Gorille et Battement imparable contre Mechamaru ultime (ch. 38-39)")
fight(0.251, "kyoto", "maki", "miwa", "A", 3,
      note="Maki surclasse Miwa et lui prend son sabre (ch. 39-40)")
fight(0.2515, "kyoto", ["momo", "mai"], "nobara", "A", 1, ta=["surprise"],
      note="Nobara allait battre Momo quand Mai l'assomme d'une balle (ch. 40-41)")
fight(0.252, "kyoto", "noritoshi", "megumi", "D",
      note="Kamo contre Megumi, interrompu par l'irruption d'Hanami (ch. 42-43)", flags="i")
fight(0.2525, "kyoto", "maki", "mai", "A", 2,
      note="Maki bat sa jumelle (ch. 44-45)")
fight(0.253, "kyoto", "hanami", ["megumi", "toge", "noritoshi", "maki"], "A", 2,
      note="Hanami tient tête aux élèves et épuise la voix d'Inumaki (ch. 43-47)")
fight(0.254, "kyoto", ["yuji", "todo"], "hanami", "A", 2, ta=["boost"],
      note="Yuji découvre l'Éclair noir, Boogie Woogie de Todo ; Hanami fissuré (ch. 48-52)", flags="e")
fight(0.2545, "kyoto", "gojo", "juzo", "A", 3,
      note="Gojo efface Juzo Kumiya et la forêt avec le Violet (ch. 52)")
fight(0.255, "kyoto", "gojo", "hanami", "A", 2,
      note="Le Violet de Gojo frappe Hanami, qui s'échappe (ch. 52-53)", flags="i")

# ============================================================================== Peinture de la mort
fight(0.3, "bouddha", "megumi", "fleau_yasohachi", "A", 1, ta=["domaine"],
      note="Domaine incomplet de Megumi, il surgit de l'ombre du fléau et l'achève (ch. 57-58)")
fight(0.31, "bouddha", ["yuji", "nobara"], ["eso", "kechizu"], "A", 2,
      note="Résonance de Nobara et poings de Yuji ; Eso et Kechizu exorcisés (ch. 59-62)", flags="e")

# ============================================================================== incident de Shibuya (31 octobre)
fight(0.35, "shibuya", "mahito", "mechamaru", "A", 2, ta=["domaine"], tb=["prepa"],
      note="Mechamaru Mode Absolu blesse Mahito, qui gagne par son domaine (ch. 80-82)")
fight(0.3501, "shibuya", "gojo", ["jogo", "hanami"], "A", 3, ta=["domaine"], tb=["surprise"],
      note="Domaine de 0,2 s parmi les civils, Gojo tue Hanami et domine Jogo (ch. 83-89)")
fight(0.3503, "shibuya", ["kenjaku", "mahito", "choso"], "gojo", "A", 2, ta=["prepa", "surprise"], tb=["protege"],
      note="Gojo, troublé par le corps de Geto, est scellé dans le Royaume de la prison par Kenjaku (ch. 89-91 ; rôle de Mahito et Choso secondaire)", flags="?")
fight(0.351, "shibuya", ["nanami", "nobara"], "haruta", "A", 2,
      note="Nanami assomme Shigemo, Nobara cloue son arme (ch. 99-100)")
fight(0.3512, "shibuya", "mei_mei", "smallpox", "A", 2,
      note="Mei Mei tranche la Divinité de la variole, Bird Strike l'achève (ch. 101-102)")
fight(0.3515, "shibuya", "choso", "yuji", "A", 2,
      note="Choso bat Yuji dans les toilettes de la station, puis le faux souvenir l'arrête (ch. 102-104)")
fight(0.352, "shibuya", "dagon", ["nanami", "maki", "naobito"], "A", 2, ta=["domaine"],
      note="Domaine de Dagon : Nuée mortelle ; le domaine de Megumi brise l'impasse (ch. 107-108)", flags="i")
fight(0.3525, "shibuya", "toji", "dagon", "A", 3,
      note="Toji (corps de séance) exorcise Dagon avec le Nuage espiègle (ch. 109-111)")
fight(0.3526, "shibuya", "toji", "maki", "A", 2,
      note="Toji arrache le Nuage espiègle à Maki et l'écarte (ch. 110)", flags="?")
fight(0.3528, "shibuya", "jogo", ["nanami", "maki", "naobito"], "A", 3, ta=["surprise"], tb=["epuise"],
      note="Jogo surgit et brûle Nanami, Maki et Naobito (ch. 111)")
fight(0.353, "shibuya", "toji", "megumi", "A", 2,
      note="Toji domine son fils puis se suicide en apprenant son nom (ch. 112-113)", flags="i")
fight(0.355, "shibuya", "sukuna", "hasaba", "A", 3,
      note="Sukuna (quinze doigts) tue Mimiko et Nanako (ch. 112)")
fight(0.3555, "shibuya", "sukuna", "jogo", "A", 3, ta=["retenue"],
      note="Duel de feu : Sukuna laisse Jogo tout tenter puis le tue au Fuga (ch. 113-116)")
fight(0.356, "shibuya", "haruta", "megumi", "D", ta=["surprise"],
      note="Shigemo poignarde Megumi qui invoque Mahoraga ; Sukuna les sauve (ch. 114-117)", flags="?")
fight(0.357, "shibuya", "sukuna", "mahoraga", "A", 2, ta=["domaine"],
      note="Sukuna exorcise Mahoraga avec le Sanctuaire malveillant (ch. 117-118)")
fight(0.36, "shibuya", "mahito", "nanami", "A", 3, tb=["epuise"],
      note="Nanami, brûlé et épuisé, meurt sous la main de Mahito (ch. 120)")
fight(0.3605, "shibuya", "mahito", "nobara", "A", 3, ta=["surprise"],
      note="Mahito touche le visage de Nobara après qu'elle a battu son clone (ch. 125)")
fight(0.361, "shibuya", ["yuji", "todo"], "mahito", "A", 2, ta=["boost"],
      note="Éclairs noirs en série et Boogie Woogie ; Todo perd sa main (ch. 126-131)", flags="e")
fight(0.362, "shibuya", "yuji", "mahito", "A", 2, tb=["epuise"],
      note="Yuji abat Mahito, épuisé, dans la ruelle (ch. 131-132)")
fight(0.364, "shibuya", ["kenjaku", "uraume"], ["choso", "yuji", "kusakabe", "panda", "noritoshi", "momo"], "A", 2,
      note="Kenjaku absorbe Mahito ; Frost Calm d'Uraume gèle le groupe ; Yuki arrive (ch. 133-136)", flags="i")

# ============================================================================== Jeu d'abattage
fight(0.45, "culling", "yuta", "yuji", "A", 2, ta=["prepa"],
      note="Yuta « exécute » Yuji puis le soigne en secret (ch. 139-140)", flags="?")
fight(0.455, "culling", "ogi", ["maki", "mai"], "A", 2,
      note="Ogi bat ses filles ; Mai meurt en léguant son pouvoir à Maki (ch. 148-149)")
fight(0.456, "culling", "maki", "ogi", "A", 3,
      note="Maki, restriction céleste complète, décapite Ogi (ch. 149)")
fight(0.457, "culling", "maki", "zenin_hei", "A", 3,
      note="Maki massacre l'unité Kukuru et le Hei, dont Jinichi (ch. 150)")
fight(0.458, "culling", "maki", "naoya", "A", 2,
      note="Duel sur le pont : Maki bat Naoya, achevé par sa mère (ch. 151)")
fight(0.47, "culling", ["megumi", "panda"], "kirara", "A", 2,
      note="Megumi piège Kirara avec un Chien divin caché (ch. 155-156)")
fight(0.4705, "culling", "hakari", "yuji", "D",
      note="Hakari refuse de coopérer et attaque Yuji ; fin de l'échange sans vainqueur (ch. 155-157)", flags="i")
fight(0.48, "culling", "yuji", "higuruma", "A", 1, tb=["domaine"],
      note="Procès du domaine ; Higuruma désactive l'Épée du bourreau et accepte le coup (ch. 163-166)", flags="?")
fight(0.49, "culling", "megumi", "reggie", "A", 1, ta=["domaine"],
      note="Jardin des ombres chimériques, Max Elephant puis victoire de justesse (ch. 167-172)")
fight(0.5, "culling", "yuta", "dhruv", "A", 3,
      note="Yuta élimine Dhruv Lakdawalla à Sendai (ch. 176)")
fight(0.502, "culling", "yuta", "kurourushi", "A", 2,
      note="Rika et Yuta exterminent le fléau-cafard (ch. 176-177)")
fight(0.505, "culling", "yuta", ["uro", "ryu_ishigori"], "A", 2,
      note="Triple choc de domaines, Yuta copie Uro et renvoie le Granite Blast ; Ryu s'avoue vaincu (ch. 178-180)")
fight(0.51, "culling", "hakari", "charles", "A", 2, ta=["domaine"],
      note="Jackpot : Hakari brise le G Warstaff et assomme Charles (ch. 182-183)")
fight(0.511, "culling", "kashimo", "panda", "A", 3,
      note="Kashimo détruit les noyaux de Panda (ch. 184-185)")
fight(0.515, "culling", "hakari", "kashimo", "A", 1, ta=["domaine", "prepa"], tb=["retenue"],
      note="Hakari immortel en jackpot, sacrifie un bras par vœu ; Kashimo n'a pas usé de sa technique (ch. 185-190)")
fight(0.53, "culling", ["maki", "noritoshi"], "naoya_fleau", "A", 2, tb=["domaine"],
      note="Naoya revenu en fléau ; sans énergie occulte, Maki traverse son domaine et l'exorcise (ch. 191-198)")
fight(0.54, "culling", "kenjaku", ["yuki", "choso"], "A", 2, tb=["prepa"],
      note="Tombeau des étoiles : Yuki se change en trou noir, Kenjaku survit et prend Tengen (ch. 203-208)")
fight(0.555, "culling", "sukuna", "yuji", "A", 2,
      note="Sukuna dans Megumi envoie Yuji à travers un immeuble (ch. 213-214)")
fight(0.5551, "culling", "sukuna", "hana_kurusu", "A", 3, ta=["surprise"],
      note="Sukuna feint d'être Megumi et arrache bras et aile d'Angel (ch. 213-214)")
fight(0.5552, "culling", ["yuji", "maki"], "sukuna", "D",
      note="Yuji et Maki pressent Sukuna, freiné par Megumi ; Uraume intervient (ch. 215)", flags="i")
fight(0.5553, "culling", "uraume", ["yuji", "maki"], "A", 2,
      note="Frost Calm à pleine puissance : Sukuna s'enfuit sur Nue (ch. 215)", flags="i")
fight(0.556, "culling", "sukuna", "ryu_ishigori", "A", 3,
      note="Sukuna éventre Ryu et lui fend le crâne (ch. 216)")
fight(0.5565, "culling", "sukuna", "yorozu", "A", 2,
      note="Sphère parfaite et domaine de Yorozu percés par la roue de Mahoraga (ch. 216-219)")

# ============================================================================== bataille de Shinjuku (24 décembre)
fight(0.6, "shinjuku", "gojo", "mahoraga", "A", 2,
      note="Rouge et Bleu combinés désintègrent Mahoraga et blessent Sukuna (ch. 230-232)")
fight(0.6001, "shinjuku", "sukuna", "gojo", "A", 1, ta=["prepa"],
      note="Duel des plus forts : le Démantèlement adapté par Mahoraga tranche l'Infini (ch. 223-236)")
fight(0.6002, "shinjuku", "sukuna", "kashimo", "A", 3, tb=["boost"],
      note="Kashimo force la vraie forme de Sukuna puis meurt (ch. 237-238)")
fight(0.6003, "shinjuku", "takaba", "kenjaku", "A", 1,
      note="L'humoriste rend Takaba intouchable ; Kenjaku renonce (ch. 239-242)", flags="?")
fight(0.6004, "shinjuku", "yuta", "kenjaku", "A", 3, ta=["surprise"], tb=["epuise"],
      note="Yuta décapite Kenjaku distrait par Takaba (ch. 243)")
fight(0.6005, "shinjuku", "sukuna", ["higuruma", "yuji", "kusakabe"], "A", 3,
      note="Confiscation ratée (Kamutoke au lieu du Sanctuaire) ; Higuruma tué (ch. 244-247)")
fight(0.6006, "shinjuku", "sukuna", ["yuta", "yuji"], "A", 2,
      note="Domaine de Yuta, Rika et l'Épée ; Sukuna finit par mettre Yuta hors combat (ch. 248-251)")
fight(0.6007, "shinjuku", "sukuna", "maki", "A", 2, tb=["surprise"],
      note="L'embuscade de Maki blesse Sukuna, éjectée par un Éclair noir (ch. 252-253)")
fight(0.6008, "shinjuku", "sukuna", "ino", "A", 3,
      note="Ino et Kaichi balayés (ch. 253)")
fight(0.6009, "shinjuku", "sukuna", "kusakabe", "A", 2,
      note="Simple Domaine de Kusakabe ; Sukuna pince la lame et l'ouvre, Ui Ui le sauve (ch. 253-254)")
fight(0.601, "shinjuku", "sukuna", ["miguel", "larue"], "A", 2,
      note="Miguel et Larue harcèlent Sukuna ; Cutie Honey de Larue ouvre la voie à Yuji (ch. 254-256)", flags="?")
fight(0.6011, "shinjuku", "sukuna", ["choso", "yuji"], "A", 2,
      note="Flamme divine : Choso protège Yuji et meurt (ch. 258-259)")
fight(0.6012, "shinjuku", ["yuji", "todo", "ino"], "sukuna", "D", ta=["boost"],
      note="Sept Éclairs noirs d'affilée, Boogie Woogie de Todo (ch. 257, 259-260)", flags="i")
fight(0.6014, "shinjuku", "yuta", "sukuna", "D", ta=["boost"],
      note="Yuta dans le corps de Gojo : Violet amplifié, le pouvoir emprunté expire (ch. 261-263)", flags="i")
fight(0.6015, "shinjuku", "sukuna", ["hana_kurusu", "todo"], "A", 2,
      note="Échelle de Jacob puis Sukuna met Angel et Todo hors combat (ch. 263-264)")
fight(0.6016, "shinjuku", ["yuji", "nobara"], "sukuna", "A", 2, tb=["epuise"],
      note="Domaine de Yuji, Résonance de Nobara sur le dernier doigt, Éclair noir final ; Megumi libéré (ch. 264-268)")
fight(0.6017, "shinjuku", "hakari", "uraume", "A", 1, ta=["domaine"],
      note="Duel en marge de Shinjuku ; Uraume cède à la mort de Sukuna (ch. 244-268)")

# ============================================================================== Jujutsu Kaisen Modulo (2086)
fight(68.4, "modulo", "masaki", ["tsurugi", "yuka"], "A", 1,
      note="Masaki prend le dessus sur les Okkotsu sur le toit de l'école (Modulo ch. 4-5)", flags="i")
fight(68.401, "modulo", "maru", "masaki", "A", 3,
      note="Maru, inconscient et déchaîné, écrase Masaki ; Tsurugi l'arrête (Modulo ch. 6)")
fight(68.45, "modulo", "dabura", "usami", "A", 2,
      note="La Parole maudite d'Usami se retourne contre lui ; Dabura se retire (Modulo ch. 13, flash-back)")
fight(68.5, "modulo", "maru", "tsurugi", "A", 1, tb=["retenue"],
      note="Tsurugi fusionné à Rika domine, puis lâche son sabre et se laisse frapper (Modulo ch. 14-21)", flags="?")
fight(68.55, "modulo", "dabura", "mahoraga", "A", 1, ta=["domaine"],
      note="Mahoraga de Yuka s'adapte ; Dabura apprend technique inversée et domaine ; Maru arrête le duel (Modulo ch. 15-23)",
      flags="i")
fight(68.56, "modulo", "yuji", "mahito", "A", 3,
      note="Yuji découpe en cubes Mahito qui recréait Shibuya (Modulo ch. 22)")
