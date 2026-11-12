"""Exploits mesurables (canon) de One Piece pour la comparaison inter-œuvres. Valeurs en log10 de l'unité SI.

Révision (vérification 2026-11) : chaque ligne d'origine porte « # vérifié », « # corrigé : ... » ou « # supprimé : ... ».
Règle suivie pour les fruits du démon : l'énergie qu'une attaque DÉLIVRE sur une cible (feu d'Ace, magma d'Akainu,
séisme de Barbe Blanche) compte comme énergie d'attaque, comme un jutsu ailleurs. En revanche un pouvoir qui retire de
l'énergie (gel d'Aokiji) ou qui détourne une énergie extérieure (météorite attirée par Fujitora) ne mesure pas la puissance
du personnage : supprimé. Les tailles ne sont presque jamais chiffrées dans le manga : les dimensions sont estimées sur les
planches, d'où des sd de 1,0 à 1,5. Les coupes de sabreurs sont calculées par « saignée » (largeur 0,1-1 m pulvérisée),
ce qui donne des énergies basses : c'est une limite connue des exploits de coupe.
"""
FB = "https://onepiece.fandom.com/wiki/"
FEATS = [
    # (id_perso, id_arc, type, log10_valeur, log10_sd, exploit, réf. canon, calcul et hypothèses, url)

    # ---- lignes d'origine, revues
    # corrigé : chapitre exact 93 ; calcul refait (l'effondrement final est surtout gravitaire) : 10,0 ± 0,8 -> 9,5 ± 1,0
    ("luffy", "eastblue", "energie", 9.5, 1.0, "Gomu Gomu no Ono : Luffy écrase Arlong à travers les cinq étages d'Arlong Park, qui s'effondre",
     "ch. 93",
     "bâtiment de 5 étages (wiki), emprise ~15 × 15 m, ~20 m de haut ; ~1e3 m³ de maçonnerie fissurée à 2-8 MJ/m³ ≈ 2e9-8e9 J ; "
     "une partie de la ruine est due à la gravité, d'où sd 1,0",
     FB + "Chapter_93 ; " + FB + "Arlong_Park"),
    # corrigé : chapitre exact 159 ; nombre de navires non dit par le texte (« many Billions ships ») ; calcul refait : 11,5 -> 10,3
    ("ace", "alabasta", "energie", 10.3, 1.0, "Hiken : Ace détruit seul la flottille des Billions qui poursuit le Vogue Merry",
     "ch. 159 (premier Hiken)",
     "~5 petits voiliers (ceux de la planche ; le texte dit seulement « plusieurs ») ; colonne de feu ~100 m × 10-20 m à ~1 000 K : "
     "~1,6e4 m³ d'air × 1,2e6 J/m³ ≈ 2e10 J, plus ~400 m³ de bois brisé à ~3 MJ/m³ ≈ 1e9 J ; total ≈ 2e10 J",
     FB + "Chapter_159 ; " + FB + "Portgas_D._Ace/Abilities_and_Powers"),
    # corrigé : les vagues se forment ch. 552 (gelées ch. 553) ; énergie refaite avec un modèle de mur d'eau : 17,5 -> 14,5
    ("whitebeard", "marineford", "energie", 14.5, 1.0, "Séisme : deux tsunamis géants convergent de part et d'autre de Marineford",
     "ch. 552-553",
     "taille non chiffrée (« huge ») ; murs d'eau estimés H ≈ 100-250 m, épaisseur ~H, front 3-10 km ; "
     "par vague ρ g (H/2) × H² × L ≈ 1000·9,8·75·(150²·5000) ≈ 8e13 J, ×2 (cinétique) ×2 vagues ≈ 3e14 J (fourchette 3e13-2e15)",
     FB + "Chapter_552 ; " + FB + "Chapter_553"),
    # supprimé : gel des tsunamis par Aokiji (Ice Age, ch. 553). Le logia RETIRE de la chaleur sans rien détruire :
    #   l'« énergie » de 1e16 J est une enthalpie évacuée par un pouvoir, pas une attaque qui frappe ; Aokiji gèle aussi
    #   la mer de façon décontractée ailleurs. Ce n'est pas une mesure de puissance brute.
    # ("aokiji", "marineford", "energie", 16.0, 0.8, "Il gèle les deux tsunamis et la baie d'un coup", "ch. 553", "...", ""),
    # corrigé : Ryûsei Kazan (ch. ~564, sol de glace d'épaisseur inconnue) n'est pas chiffrable ; remplacé par le même
    #   pouvoir sur une cible mesurable : Dai Funka vaporise l'iceberg lancé par Jozu (ch. 554). 14,0 ± 1,0 -> 14,0 ± 1,0
    ("akainu", "marineford", "energie", 14.0, 1.0, "Dai Funka : un poing de magma vaporise l'iceberg que Jozu lance sur les géants",
     "ch. 554",
     "iceberg « bien plus grand que les géants » de la Marine : ~40 m de côté, ~5e7 kg (fourchette 1e7-1e8) ; "
     "fondre + chauffer + vaporiser la glace ≈ 3e6 J/kg ⇒ ~1e14 J ; vaporisation peut-être partielle, d'où sd 1,0",
     FB + "Chapter_554 ; " + FB + "Magu_Magu_no_Mi"),
    # supprimé : météorite de Fujitora (ch. 713, arc punkhazard et non gear4). L'énergie vient de la chute d'un corps
    #   extérieur attiré par le fruit Zushi Zushi : elle ne mesure pas la force de Fujitora ; taille non donnée.
    # ("fujitora", "gear4", "energie", 14.5, 1.2, "Il fait tomber une météorite sur Dressrosa", "ch. ~709", "...", ""),
    # corrigé : chapitre exact 1045 ; Luffy est en Gigant ; masse refaite (dragon de Kaido plus gros) : 6,5 ± 1,0 -> 8,3 ± 1,3
    ("luffy", "wano5", "force", 8.3, 1.3, "Gear 5, en géant : Luffy fait tournoyer le corps de dragon de Kaido comme une corde à sauter",
     "ch. 1045",
     "aucune taille officielle du dragon ; Luffy en Gear 4 est plus petit que son œil : tête ~50 m, corps ~20-40 m de diamètre "
     "sur 0,5-1 km ⇒ 2e5-1e6 m³ × 1 000 kg/m³ ≈ 2e8-1e9 kg ; borne basse 1e7 kg ; Gear 5 suit une physique de cartoon, d'où sd 1,3",
     "https://daddyjim.com/one-piece/manga-chapter/Chapter-1045 ; https://tvtropes.org/pmwiki/pmwiki.php/Characters/OnePieceKaido"),

    # ---- ajouts (bas de l'échelle)
    ("mr_4", "alabasta", "force", 3.6, 0.3, "Mr. 4 manie en combat sa batte de base-ball de 4 tonnes",
     "ch. 184-186",
     "batte de 4 t (poids donné dans l'œuvre) : 4 000 kg",
     FB + "Babe"),
    ("usopp", "alabasta", "resistance", 4.8, 0.7, "Usopp prend un coup de la batte de 4 t de Mr. 4 sur la tête et continue le combat",
     "ch. 186",
     "masse effective ~1/3 de 4 t au point d'impact, ~5-15 m/s (Mr. 4 est lent) : ½ · 1 300 · 10² ≈ 7e4 J (fourchette 1e4-5e5)",
     FB + "Babe"),
    ("luffy", "alabasta", "energie", 9.7, 1.0, "Gomu Gomu no Storm : Crocodile traverse la roche du tombeau royal jusqu'au ciel d'Alubarna",
     "ch. 209",
     "profondeur non donnée : colonne de roche ~10-30 m × ~2,5 m de diamètre ≈ 20-150 m³ pulvérisés à 20-100 MJ/m³ ≈ 5e9 J",
     FB + "Chapter_209"),
    ("luffy", "skypiea", "force", 4.3, 0.6, "Luffy combat Enel avec une énorme boule d'or soudée au bras (Gomu Gomu no Ogon Rifle)",
     "ch. 297-298",
     "boule « large », taille non chiffrée : ~1,0-1,5 m de diamètre sur les planches ⇒ 0,5-1,8 m³ × 19 300 kg/m³ ≈ 1e4-3,4e4 kg",
     FB + "Chapter_297 ; " + FB + "Chapter_298"),

    # ---- ajouts (milieu et haut)
    ("jozu", "marineford", "force", 7.7, 0.8, "Jozu soulève et lance un iceberg sur l'escouade des géants de la Marine",
     "ch. 554",
     "iceberg ~40 m de côté (plus grand que les géants) : 6e4 m³ × 920 kg/m³ ≈ 5e7 kg (fourchette 1e7-1e8)",
     FB + "Chapter_554"),
    ("mihawk", "marineford", "energie", 10.2, 1.5, "D'un coup horizontal, Mihawk tranche la vague gelée : la moitié haute s'écrase sur Marineford",
     "ch. 561",
     "coupe d'une vague gelée de ~20-50 m d'épaisseur sur ~100-500 m : ~1e4 m² ; saignée 0,1-1 m de glace pulvérisée "
     "à ~5 MJ/m³ ⇒ ~1,5e10 J ; modèle de coupe très incertain, d'où sd 1,5",
     "https://daddyjim.com/one-piece/manga-chapter/Chapter-561"),
    ("zoro", "punkhazard", "energie", 10.0, 1.5, "Zoro tranche en deux le géant de pierre de Pica (« grand comme une montagne ») puis Pica lui-même",
     "ch. 777-778",
     "section coupée ~100-3 000 m² de roche (taille non chiffrée) ; saignée 0,1-1 m pulvérisée à 20-100 MJ/m³ ⇒ ~1e10 J ; sd 1,5",
     FB + "Pica ; https://daddyjim.com/one-piece/manga-chapter/Chapter-777"),
    ("garp", "water7", "force", 6.3, 1.0, "Garp lance à la main un boulet de canon énorme, enchaîné, sur le Thousand Sunny",
     "ch. 439",
     "taille non chiffrée (« enormous ») : sphère de fer ~5-10 m de diamètre ⇒ 65-520 m³ × 7 800 kg/m³ ≈ 5e5-4e6 kg",
     FB + "Chapter_439 ; https://tvtropes.org/pmwiki/pmwiki.php/Recap/OnePieceReturnToWaterSevenArc"),
    ("garp", "egghead", "energie", 12.8, 1.2, "Galaxy Impact : un poing de Haki des rois, sans toucher le sol, rase un quartier de Hachinosu",
     "ch. 1080",
     "rayon de destruction non chiffré, estimé 300-1 000 m (bâtiments soufflés, ~35 kPa) ; loi des explosions : 0,3-10 kt ≈ 1e12-4e13 J ; "
     "Garp a 78 ans",
     "https://www.opfanpage.com/garp-finally-shows-his-true-power/ ; https://dexerto.com/anime/one-piece-over-the-top-change-garp-galaxy-impact-2850038"),
    ("kaido", "wci", "resistance", 7.6, 0.6, "Kaido saute d'une île céleste (10 km, tentative de suicide) et en sort presque indemne",
     "ch. 795",
     "Kaido 7,1 m (databook) ⇒ ~5 t ; la vitesse plafonne à la vitesse limite 75-200 m/s ; ½ · 5 000 · (75-200)² ≈ 1,4e7-1e8 J",
     FB + "Chapter_795 ; https://tvtropes.org/pmwiki/pmwiki.php/Characters/OnePieceKaido"),
]

ANCHORS = [
    # rencontres canon avec des êtres réels : (perso, arc, entité, résultat, exploit, réf.)
    ("zoro", "eastblue", "loup", "A", "Zoro tue le loup de compagnie d'Helmeppo qui terrorise Shells Town (juste avant l'histoire)", "ch. 3"),
    ("luffy", "eastblue", "lion", "A", "Luffy assomme Richie, le grand lion de Mohji (avec Mohji)", "ch. 13"),
    ("luffy", "eastblue", "soldat_arme*10", "A", "Les Marines de Morgan tirent : les balles ne font rien, la charge au sabre échoue, Morgan tombe", "ch. 6-7"),
    ("zoro", "alabasta", "soldat_arme*100", "A", "Whisky Peak : seul contre les 100 agents de Baroque Works (fusils, sabres), il les bat tous", "ch. 107-109"),
    ("benn_beckman", "avant", "soldat_arme*10", "A", "Beckman met seul hors de combat la bande de Higuma (fusil, sabres)", "ch. 1"),
]

ANCHOR_ENTITIES = {
    # combattants du modèle qui sont de simples humains armés : (u = log10 « × humain », incertitude)
    "marines_ordinaires": (1.6, 0.7),   # vérifié : Marines armés de fusils et sabres, toujours en groupe dans les données
    "pirates_ordinaires": (1.6, 0.7),   # ajouté : même nature (groupe de pirates armés sans pouvoir), même valeur
    "higuma": (1.1, 0.4),               # vérifié : bandit au sabre sans pouvoir (bat Luffy enfant, écrasé par Beckman, ch. 1)
}
