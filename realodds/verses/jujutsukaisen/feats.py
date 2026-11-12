"""Exploits mesurables (canon) de Jujutsu Kaisen pour la comparaison inter-œuvres. Valeurs en log10 de l'unité SI.

Révision (vérification ligne à ligne) : chaque ligne d'origine porte « # vérifié », « # corrigé : … » ou
« # supprimé : … » (ligne commentée). Choix de méthode pour les domaines et techniques à effet garanti : un domaine
(Sanctuaire malveillant, Vide infini…) frappe à coup sûr et répète ses coups pendant toute sa durée ; l'effet total
n'est donc ni UNE attaque ni une mesure de puissance brute → retiré. On garde les attaques qui ne sont pas à effet
garanti (projectiles, explosions, coups), même portées par une technique, avec un sd large.
Pas de rencontre canon avec un animal réel trouvée (Panda et les shikigamis ne sont pas des espèces réelles).
"""
FEATS = [
    # (id_perso, id_arc, type, log10_valeur, log10_sd, "exploit (FR, court)", "réf. canon", "calcul et hypothèses", "url")

    # ------------------------------------------------------------------ bas de l'échelle : Yuji avant énergie occulte
    # corrigé : 3.0→3.1, sd 0.2→0.3 (minimum du guide) ; le poids se plante dans un but de football à « près de 30 m »
    # (le professeur Takagi lance 14 m) ; trajectoire tendue, donc vitesse > √(gR) ; masse du poids incertaine (6 kg lycée / 7,26 kg)
    ("yuji", "debut", "energie", 3.1, 0.3, "Lancer du poids à près de 30 m, planté dans un but de football (Takagi : 14 m)", "ch. 1",
     "R ≈ 30 m, lâcher ~2 m, angle 20-45° : v² = gR/sin2θ ≈ 290-460 m²/s² ; ½mv² avec m = 6-7,26 kg ≈ 0,9-1,7e3 J",
     "https://daddyjim.com/jujutsu-kaisen/manga-chapter/Chapter-1"),
    # corrigé : sd 0.1→0.3 ; chiffre « 50 m en 3 s » confirmé (wiki, RT), mais énoncé en dialogue, non chronométré à l'écran ;
    # chapitre exact non retrouvé dans les résumés consultés (ch. 1 probable)
    ("yuji", "debut", "vitesse", 1.22, 0.3, "Court le 50 m en 3 secondes", "ch. 1 (énoncé ; chapitre exact non vérifié)",
     "50 m / 3 s ≈ 16,7 m/s", "https://jujutsu-kaisen.fandom.com/wiki/Yuji_Itadori"),

    # ------------------------------------------------------------------ milieu de l'échelle
    # corrigé : ch. ~27 → ch. 23 (combat contre Mahito dans les égouts, débuts) ; « mur porteur » → paroi du collecteur ;
    # 7.0→7.3, sd 0.8→1.0 : le Ratio force un point faible et l'extension « Effondrement » charge les débris d'énergie occulte
    # (technique, pas seulement de la force brute), et le volume effondré n'est pas chiffré
    ("nanami", "debut", "energie", 7.3, 1.0, "Heures supplémentaires : d'un coup, il effondre la paroi de l'égout sur Mahito (Effondrement)",
     "ch. 23",
     "~10-50 m³ de béton fragmenté à 1-5 MJ/m³ ≈ 1e7-2,5e8 J ; technique de point faible → sd large",
     "https://jujutsu-kaisen.fandom.com/wiki/Chapter_23"),
    ("megumi", "debut", "resistance", 6.5, 1.0, "Projeté à travers un bâtiment par Sukuna, il continue le combat",
     "ch. 9",
     "trou ~1 m² dans 1-3 cloisons/murs de 0,15-0,2 m (0,2-0,6 m³ de béton pulvérisé à ~1e7 J/m³) + ½·60 kg·(30-60 m/s)² ≈ 2e6-1e7 J ; Sukuna « joue » (peu de doigts)",
     "https://reddit.sudovanilla.org/1awdpjn"),
    ("jogo", "shibuya", "resistance", 7.3, 1.0, "Sukuna l'expulse d'un immeuble et le fait traverser plusieurs étages",
     "ch. 114",
     "3-5 dalles de 0,2 m traversées, section ~1 m² : ~1 m³ de béton pulvérisé à 1e7-5e7 J/m³ ≈ 1e7-5e7 J ; Sukuna retenu (il joue avec Jogo)",
     "https://reddit.sudovanilla.org/1awdpjn"),
    ("yuji", "culling", "resistance", 7.0, 1.0, "Sukuna (corps de Megumi) l'envoie à travers tout un immeuble, cratère sur le toit ; Yuji se relève",
     "ch. 213-214",
     "plusieurs dalles traversées (~1 m³ de béton pulvérisé à 1e7-5e7 J/m³) ≈ 1e7 J ; sortie de Sukuna réduite (Megumi résiste), d'où sd 1.0",
     "https://daddyjim.com/jujutsu-kaisen/manga-chapter/Chapter-214"),
    ("yuji", "culling", "force", 3.3, 0.7, "Arrache et lance une dalle de béton sur Sukuna", "ch. 214",
     "dalle supposée ~2 × 2 × 0,2 m = 0,8 m³ × 2 400 kg/m³ ≈ 2 t (dimensions devinées) ; lancer en plein combat, pas un maximum : borne basse",
     "https://daddyjim.com/jujutsu-kaisen/manga-chapter/Chapter-214"),
    ("naoya", "culling", "vitesse", 2.4, 0.4, "Sorcellerie de projection : il accélère jusqu'à la limite du mur du son pour transpercer Maki",
     "ch. 151",
     "vitesse dite « subsonique », qu'il veut porter au-delà du son : ~150-340 m/s ; vitesse de déplacement réelle (la technique fixe la trajectoire, pas la physique du coup)",
     "https://jujutsu-kaisen.fandom.com/wiki/Naoya_Zenin"),
    ("maki", "culling", "resistance", 6.5, 0.6, "Encaisse en posture Shiranui la charge subsonique de Naoya (côtes brisées) puis le met K.-O.",
     "ch. 151",
     "½ · 70 kg · (150-340 m/s)² ≈ 8e5-4e6 J",
     "https://daddyjim.com/jujutsu-kaisen/manga-chapter/Chapter-151"),

    # ------------------------------------------------------------------ haut-milieu : grade spécial
    ("naoya_fleau", "culling", "vitesse", 3.05, 0.3, "Naoya en fléau vole à plus de Mach 3 (prises d'air et propulsion)",
     "ch. 193",
     "« au-delà du triple de la vitesse du son » : v ≥ 3 × 343 ≈ 1 030 m/s ; chiffre donné dans le manga",
     "https://daddyjim.com/jujutsu-kaisen/manga-chapter/Chapter-193"),
    ("maki", "culling", "resistance", 8.0, 0.7, "Percutée par Naoya-fléau à Mach 3, enfoncée dans la roche, gravement blessée mais encore combattante (elle le tue ensuite)",
     "ch. 193-194",
     "½ · m · v² avec v ≈ 1 030 m/s et m = 100-300 kg (fléau plus massif qu'un humain) ≈ 5e7-1,6e8 J",
     "https://jujutsu-kaisen.fandom.com/wiki/Naoya_Zenin"),
    # corrigé : 12.0→11.0, sd 1.0→1.5 : le manga ne donne aucune dimension (« un torrent qui percute Uzumaki et explose ») ;
    # « destruction de bâtiments sur ~100 m » n'est pas dans le texte ; estimation par explosion équivalente
    ("yuta", "jjk0", "energie", 11.0, 1.5, "Rayon d'amour pur de Rika (énergie sans limite) contre Uzumaki maximal de Geto, qui perd un bras",
     "JJK 0, ch. 0-4",
     "explosion dessinée sur ~50-150 m de rayon ; loi de Hopkinson R = Z·W^(1/3), Z ≈ 3,5-4,5 m/kg^(1/3) (bâtiments détruits) → W ≈ 1e3-8e4 kg TNT ≈ 5e9-3e11 J ; dimensions devinées",
     "https://daddyjim.com/jujutsu-kaisen/manga-chapter/Chapter-0-4"),

    # ------------------------------------------------------------------ sommet
    # corrigé : ch. ~116 → ch. 115 ; taille « un pâté de maisons entier » (≈ 100 m) au lieu de 50 m devinés ; 14.0→13.5,
    # sd 1.0→1.5 : la chaleur contenue (~2e15 J pour 100 m) n'est pas livrée (les restes brûlent encore au ch. 116) ;
    # l'énergie d'impact (chute) donne ~1e12-1e13 J ; valeur prise entre les deux. Le Météore rate Sukuna.
    ("jogo", "shibuya", "energie", 13.5, 1.5, "Météore maximal : une roche en fusion de la taille d'un pâté de maisons rase le quartier",
     "ch. 115",
     "D ≈ 60-120 m → m ≈ 3e8-2,5e9 kg ; impact mgh (h ~ 200-500 m) ≈ 6e11-1e13 J ; contenu thermique 1,5e6 J/kg ≈ 5e14-4e15 J (borne haute non livrée)",
     "https://reddit.sudovanilla.org/1awdpjn"),
    # supprimé : Sanctuaire malveillant (domaine à effet garanti, ch. 118-119) — voir la ligne commentée ci-dessous ;
    # remplacé par la flèche de feu tirée juste après (attaque unique, non garantie), qui rase un pâté de maisons avec Mahoraga
    # ("sukuna", "shibuya", "energie", 13.0, 0.8, "Sanctuaire malveillant : tout est tranché sur 200 m de rayon", "ch. 119",
    #  "rayon de 200 m donné dans le manga ; ~1e6 m³ de béton et d'acier découpés et fragmentés à ~1e7 J/m³ ≈ 1e13 J", ""),
    #  → supprimé : (1) domaine sans barrière à frappe garantie, coups répétés pendant toute sa durée = somme d'innombrables
    #    coupes, pas UNE attaque ; (2) le rayon est faux : 200 m est le MAXIMUM permis par le vœu, Sukuna le réduit à 140 m
    #    pour épargner Megumi (ch. 119) ; (3) 1e6 m³ « fragmentés » compte tout le volume urbain comme du béton plein (en
    #    réalité ~5-10 % de matière solide) et des découpes, pas une pulvérisation. Recalcul indicatif, non retenu :
    #    π·140² m² × ~25 m × ~7 % solide ≈ 1e5 m³ × 2e6 J/m³ (découpe) ≈ 2e11 J cumulés.
    ("sukuna", "shibuya", "energie", 10.7, 1.0, "Flèche de feu (Fuga) : colonne de flammes qui anéantit Mahoraga et le pâté de maisons alentour",
     "ch. 119",
     "zone détruite ~60-150 m de rayon ; Hopkinson Z ≈ 4,5 m/kg^(1/3) → W ≈ 2e3-4e4 kg TNT ≈ 1e10-1,6e11 J",
     "https://jujutsu-kaisen.fandom.com/wiki/Chapter_119"),
    # corrigé : ch. ~232-233 → ch. 223 (premier coup du duel, 24 décembre) ; zone : une tranchée de rues « de Shibuya à Shinjuku »
    # (~3,5-4,6 km), le gratte-ciel de Sukuna s'effondre, ses deux bras renforcés détruits ; 13.5→13.3, sd 1.0→1.5 (diamètre deviné).
    # Le Violet est un projectile qui « efface » la matière : pas à effet garanti (Sukuna l'encaisse en partie), gardé avec sd large.
    ("gojo", "shinjuku", "energie", 13.3, 1.5, "Violet imaginaire à 200 % : trace une tranchée de Shibuya à Shinjuku et rase le gratte-ciel de Sukuna",
     "ch. 223",
     "tube Ø 30-60 m × 3,5-4,6 km ≈ 3e6-1,3e7 m³, dont ~5 % de matière solide (immeubles) ≈ 1,5e5-6e5 m³ pulvérisés/effacés à 2e7-1e8 J/m³ ≈ 3e12-6e13 J",
     "https://jujutsu-kaisen.fandom.com/wiki/Chapter_223"),
    # supprimé : Kashimo, Bête mythique d'ambre (ch. 237-238, arc « shinjuku2 » et non « shinjuku ») — aucune destruction chiffrable
    # dans le manga (« combo de foudre » sans effet décrit) ; la valeur « plusieurs éclairs ≈ 1e10 J » était inventée ; sa résistance
    # à la foudre de Sukuna vient de l'immunité électrique de la technique, pas d'une résistance brute.
    # ("kashimo", "shinjuku", "energie", 10.0, 0.8, "Bête mythique d'ambre : décharge de foudre sur Sukuna", "ch. ~238",
    #  "décharge de l'ordre de plusieurs éclairs ≈ 1e10 J", ""),
]

ANCHORS = [
    # (id_perso, id_arc, entité, résultat, "exploit (FR)", "réf. canon")
    ("yuta", "jjk0", "humain*4", "A", "Rika enferme dans des casiers les quatre élèves qui harcelaient Yuta", "JJK 0, ch. 0-1"),
    ("geto", "passe", "humain*112", "A", "Geto massacre 112 villageois non-exorcistes (villageois qui séquestraient deux fillettes)", "ch. 77"),
    ("mahito", "debut", "humain*3", "A", "Mahito transfigure et tue trois spectateurs bruyants au cinéma", "ch. 19"),
    ("toji", "passe", "humain", "A", "Toji abat Riko Amanai (non-exorciste) d'une balle", "ch. ~72"),
    ("yuji", "culling", "soldat_arme*3", "A", "Yuji, Megumi, Hana et Takaba neutralisent sans peine des soldats étrangers armés (fusils, grenades) ; nombre exact non donné, 3 = minimum prudent",
     "ch. 209-210"),
]
ANCHOR_ENTITIES = {}
