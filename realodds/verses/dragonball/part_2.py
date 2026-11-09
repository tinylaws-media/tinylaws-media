# Dragon Ball, partie 2 : le manga Dragon Ball Super (Toyotarō, supervisé par Toriyama), ch. 1 à 104.
# Manga uniquement : pas l'anime, pas GT, pas les films sauf ce que le manga adapte. "fight" est injecté par data.py.
# Dernier chapitre paru au 8 nov. 2026 : ch. 104 (one-shot « La naissance de Saiyaman X », V Jump fév. 2025) ;
# le ch. 105 est annoncé mais pas sorti. Sources : Kanzenshuu (wiki chapitre par chapitre et guide du manga),
# récapitulatifs Nerdtropolis / Final Weapon / ComicBook pour les ch. 78-104.
# Repères de temps (année Age, axe des ARCS) : Battle of Gods 778.0-778.1, retour de Freezer (évoqué) 778.5,
# tournoi Univers 6 779.50-779.55, Goku Black 779.58-779.70, préparation du TdP 780.00-780.05, Tournoi du Pouvoir
# 780.10-780.30, Moro 780.50-780.60, Granolah 781.00-781.25 (flash-back Bardock en 737.0), Super Hero 781.50-781.60,
# après Super Hero 781.70-781.75.
# Remarque : le manga saute « La Résurrection de F » (ch. 5 évoque seulement que Goku et Vegeta ont battu Golden Freezer).

CHARS_PART = {
    # ---- personnages déjà présents dans le manga original (tier à leur première apparition dans toute l'histoire)
    "goku": ("Son Goku", "Héros", 1.0, None, None),
    "vegeta": ("Vegeta", "Saiyans", 4.0, None, None),
    "gohan": ("Son Gohan", "Héros", 0.5, None, None),
    "piccolo": ("Piccolo (Ma Junior)", "Clan Piccolo", 3.0, None, None),
    "krillin": ("Krilin", "Héros", 1.0, None, None),
    "tien": ("Tenshinhan", "Héros", 2.0, None, None),
    "chiaotzu": ("Chaozu", "Héros", 1.6, None, None),
    "yamcha": ("Yamcha", "Héros", 1.2, None, None),
    "roshi": ("Tortue Géniale (Jackie Chun)", "Héros", 2.0, None, None),
    "android_17": ("C-17", "Cyborgs", 6.0, None, None),
    "android_18": ("C-18", "Cyborgs", 6.0, None, None),
    "freeza": ("Freezer", "Armée de Freezer", 5.0, None, None),
    "majin_buu": ("Majin Buu (gros)", "Majin Buu", 7.0, None, None),
    "trunks": ("Trunks (du futur)", "Héros", 5.4, None, None),
    "trunks_kid": ("Trunks (enfant)", "Héros", 5.6, None, None),
    "goten": ("Son Goten", "Héros", 5.5, None, None),
    "gotenks": ("Gotenks", "Héros", 6.5, None, None),
    "vegito": ("Vegito", "Héros", 7.9, None, None),
    # ---- dieux et anges
    "beerus": ("Beerus", "Dieux", 8.5, None, None),
    "whis": ("Whis", "Anges", 10.0, None, None),
    # ---- tournoi Univers 6
    "hit": ("Hit", "Univers 6", 7.5, None, None),
    "cabba": ("Cabba", "Univers 6", 5.5, None, None),
    "frost": ("Frost", "Univers 6", 6.0, None, None),
    "magetta": ("Magetta", "Univers 6", 5.5, None, None),
    "botamo": ("Botamo", "Univers 6", 5.0, None, None),
    # ---- Goku Black
    "goku_black": ("Goku Black", "Zamasu", 7.0, 779.701, None),
    "zamasu": ("Zamasu (du futur, immortel)", "Zamasu", 6.5, 779.701, None),
    "zamasu_present": ("Zamasu (présent)", "Zamasu", 6.0, 779.621, None),
    "fused_zamasu": ("Zamasu fusionné", "Zamasu", 8.5, 779.701, None),
    "dabura_futur": ("Dabura (futur de Trunks)", "Babidi", 6.0, 779.581, None),
    # ---- Tournoi du Pouvoir
    "toppo": ("Toppo", "Univers 11", 8.0, None, None),
    "jiren": ("Jiren", "Univers 11", 9.0, None, None),
    "dyspo": ("Dyspo", "Univers 11", 7.5, None, None),
    "pride_troopers": ("Troupes de l'Orgueil (groupe)", "Univers 11", 6.0, None, None),
    "casserale": ("Kahseral", "Univers 11", 4.5, None, None),
    "caulifla": ("Caulifla", "Univers 6", 6.0, None, None),
    "kale": ("Kale", "Univers 6", 6.5, None, None),
    "kefla": ("Kefla", "Univers 6", 8.0, None, None),
    "ribrianne": ("Ribrianne (et Rozie, Kakunsa)", "Univers 2", 6.0, None, None),
    "anilaza": ("Anilaza", "Univers 3", 6.0, None, None),
    "u9_combattants": ("Combattants de l'Univers 9 (groupe)", "Univers 9", 5.0, None, None),
    "u10_combattants": ("Combattants de l'Univers 10 (groupe)", "Univers 10", 5.5, None, None),
    "u4_combattants": ("Combattants de l'Univers 4 (groupe)", "Univers 4", 6.0, None, None),
    # ---- Moro
    "moro": ("Moro", "Bandits de Saganbo", 7.0, 780.601, None),
    "seven_three": ("Seven-Three (OG73-I)", "Bandits de Saganbo", 6.5, 780.562, None),
    "saganbo": ("Saganbo", "Bandits de Saganbo", 6.0, 780.546, None),
    "shimorekka": ("Shimorekka", "Bandits de Saganbo", 5.0, 780.561, None),
    "yunba": ("Yunba", "Bandits de Saganbo", 4.0, None, None),
    "zauyogi": ("Zauyogi", "Bandits de Saganbo", 4.0, None, None),
    "bikkura_koiter": ("Bikkura Koiter", "Bandits de Saganbo", 3.5, None, None),
    "iwaza_fusion": ("Iwaza, Miza et Kikaza (fusionnées)", "Bandits de Saganbo", 4.5, None, None),
    "yuzun": ("Yuzun", "Bandits de Saganbo", 4.0, 780.531, None),
    "macareni": ("Gang des Macareni (groupe)", "Bandits", 2.0, None, None),
    "merus": ("Merus", "Patrouille galactique", 9.0, 780.584, None),
    "jaco": ("Jaco", "Patrouille galactique", 2.0, None, None),
    # ---- Granolah
    "granolah": ("Granolah", "Céréaliens", 8.5, None, None),
    "gas": ("Gas", "Heeters", 4.0, 737.001, None),   # absent de 737 à 781 (REVIVE dans data.py), tué par Freezer ch. 87
    "elec": ("Elec", "Heeters", 5.5, 781.251, None),
    "oil": ("Oil", "Heeters", 3.5, None, None),
    "maki": ("Maki", "Heeters", 3.5, None, None),
    "bardock": ("Bardock", "Saiyans", 3.5, 737.1, None),
    # ---- Super Hero et après
    "gamma_1": ("Gamma 1", "Ruban rouge", 7.0, None, None),
    "gamma_2": ("Gamma 2", "Ruban rouge", 7.0, 781.575, None),
    "cell_max": ("Cell Max", "Ruban rouge", 8.5, 781.601, None),
    "hachimaru": ("Hachimaru (guêpe cyborg)", "Dr Hedo", 2.0, None, None),
    "robots_hedo": ("Robots du Dr Hedo et de Beta (groupe)", "Dr Hedo", 3.0, None, None),
    "carmine": ("Carmine et le soldat n° 15", "Ruban rouge", 0.5, None, None),
}

GENERIC_PART = {"pride_troopers", "u9_combattants", "u10_combattants", "u4_combattants", "macareni", "robots_hedo",
                "carmine"}

JUMPS_PART = [
    # Goku
    ("goku", 778.02, 1.0, 0.6, "Super Saiyan God, ki divin absorbé (ch. 4)"),
    ("goku", 778.5, 0.6, 0.5, "Super Saiyan Blue, entraînement chez Whis (évoqué ch. 5), avant Golden Freezer"),
    ("goku", 779.66, 0.3, 0.3, "Blue maîtrisé, puissance scellée (ch. 24)"),
    ("goku", 780.165, 0.5, 0.5, "Ultra Instinct (premier éveil contre Jiren, ch. 40-41)"),
    ("goku", 780.55, 0.3, 0.3, "Entraînement avec Merus, Ultra Instinct « Sign » (ch. 51-59)"),
    ("goku", 780.575, 0.7, 0.5, "Ultra Instinct maîtrisé (ch. 64)"),
    # Vegeta
    ("vegeta", 778.5, 1.5, 0.7, "Super Saiyan God puis Blue, entraînement chez Whis (évoqué ch. 5), avant Golden Freezer"),
    ("vegeta", 780.12, 0.4, 0.4, "Blue « parfait » (ch. 36)"),
    ("vegeta", 780.155, 0.3, 0.3, "Nouveau palier de Blue face à Jiren (ch. 40)"),
    ("vegeta", 780.53, 0.3, 0.3, "Entraînement sur Yardrat, fission spirituelle (ch. 52-61)"),
    ("vegeta", 781.025, 1.0, 0.6, "Ultra Ego, entraînement chez Beerus (ch. 74)"),
    # Freezer
    ("freeza", 778.5, 2.6, 0.8, "Résurrection et Golden Freezer (film non adapté, évoqué ch. 5)"),
    ("freeza", 781.24, 1.2, 0.6, "Black Freezer (dix ans dans une salle de l'Esprit et du Temps, ch. 87)"),
    # Gohan
    ("gohan", 780.0, 1.0, 0.6, "Reprise de l'entraînement avec Piccolo pour le TdP (ch. 31)"),
    ("gohan", 781.3, -0.4, 0.4, "De nouveau rouillé, pris par la recherche (Piccolo le lui reproche, ch. 88-94)"),
    ("gohan", 781.58, 2.5, 0.8, "Gohan Beast (ch. 99)"),
    # Piccolo
    ("piccolo", 780.0, 0.5, 0.5, "Entraînement pour le TdP"),
    ("piccolo", 781.5505, 2.5, 0.8, "Puissance de Shenron, Piccolo Orange (ch. 95-96)"),
    # autres
    ("trunks", 779.58, 1.0, 0.6, "Super Saiyan 2 et années de guerre contre Black (ch. 16)"),
    ("android_17", 780.0, 1.5, 0.7, "Entraînement solitaire de garde forestier (ch. 31)"),
    ("android_18", 780.0, 0.8, 0.6, "Remise en forme pour le TdP"),
    ("cabba", 780.0, 0.8, 0.5, "Progrès depuis le tournoi Univers 6"),
    ("gas", 780.0, 3.5, 1.0, "Quarante ans de croissance depuis le combat contre Bardock (ch. 68)"),
    ("gas", 781.05, 2.0, 0.8, "Vœu d'Elec : guerrier le plus fort de l'univers (ch. 78)"),
    ("granolah", 781.025, 0.5, 0.4, "Éveil du pouvoir latent, œil gauche (ch. 75)"),
    ("moro", 780.505, 1.0, 0.6, "Énergie de Goku et Vegeta absorbée, jeunesse retrouvée (ch. 46)"),
    ("moro", 780.562, 0.8, 0.5, "Absorbe Seven-Three (ch. 61)"),
    ("moro", 780.59, 0.8, 0.6, "Absorbe Merus et fusionne avec la Terre (ch. 65)"),
]

# ---------------------------------------------------------------- Battle of Gods (ch. 1-4)
fight(778.0, "dieux", "beerus", "goku", "A", 3, ta=["retenue"],
      note="Chez Kaiō du Nord, Goku passe SSJ1, 2 puis 3 ; une pichenette puis un coup sur la nuque (ch. 2)")
fight(778.01, "dieux", "beerus", ["gohan", "majin_buu"], "A", 3, ta=["retenue"],
      note="Fête de Bulma : Gohan et Buu déjà au tapis quand la scène reprend (ch. 3)", flags="?")
fight(778.011, "dieux", "beerus", "gotenks", "A", 3, ta=["retenue"], note="Gotenks SSJ3 balayé d'une pichenette (ch. 3)")
fight(778.012, "dieux", "beerus", "vegeta", "A", 3, ta=["retenue"],
      note="Vegeta furieux après la gifle à Bulma, ses attaques ne font rien, il concède (ch. 3)")
fight(778.02, "dieux", "beerus", "goku", "A", 2, ta=["retenue"],
      note="Goku Super Saiyan God ; Goku arrête la sphère finale au Kamehameha, Whis met fin au combat (ch. 4)")
fight(778.6, "dieux", ["goku", "vegeta"], "freeza", "A", 2,
      note="Golden Freezer battu : seulement évoqué, le manga n'adapte pas La Résurrection de F (ch. 5)", flags="?e")

# ---------------------------------------------------------------- tournoi Univers 6 contre Univers 7 (ch. 8-13)
fight(779.5, "univ6", "goku", "botamo", "A", 2, ta=["retenue"], note="Goku le soulève par les jambes, sortie de ring (ch. 9)")
fight(779.501, "univ6", "frost", "goku", "A", 1, ta=["contre"], tb=["malade"],
      note="Goku SSJ sorti du ring par un coup anodin : aiguille empoisonnée de Frost (ch. 10)", flags="?")
fight(779.502, "univ6", "frost", "piccolo", "A", 1, ta=["contre"], tb=["malade"],
      note="Piccolo poussé hors du ring, Frost disqualifié ensuite pour l'aiguille (ch. 10)", flags="?")
fight(779.503, "univ6", "vegeta", "frost", "A", 3, note="Vegeta SSJ, Frost sorti du ring sous une rafale (ch. 11)")
fight(779.504, "univ6", "vegeta", "magetta", "A", 1,
      note="Le ki n'a pas d'effet, Vegeta le fait tomber en le vexant (ch. 11)")
fight(779.505, "univ6", "vegeta", "cabba", "A", 3, ta=["retenue"],
      note="Vegeta pousse Cabba au Super Saiyan puis le met KO en Blue (ch. 12)")
fight(779.506, "univ6", "hit", "vegeta", "A", 3, tb=["epuise"], note="Vegeta Blue fauché par le saut temporel (ch. 12)")
fight(779.507, "univ6", "hit", "goku", "D", ta=["retenue"], tb=["retenue"],
      note="Goku passe SSG puis Blue et sort volontairement du ring sans être battu ; Hit ne peut pas tuer selon les règles (ch. 12-13)", flags="i")

# ---------------------------------------------------------------- Goku Black et Zamasu (ch. 14-26)
fight(779.55, "univ6", "goku_black", ["trunks"], "A", 2, note="Black écrase Trunks SSJ, qui fuit dans la machine (ch. 14-15)")
fight(779.551, "univ6", "goku", "trunks", "A", 3, ta=["retenue"],
      note="Combat d'essai au présent, Goku passe SSJ2, SSJ3 puis un instant SSG (ch. 15)")
fight(779.58, "univ6", "trunks", "dabura_futur", "A", 2, ta=["surprise"],
      note="Flash-back : Trunks atteint le SSJ2, Shin immobilise Dabura, Trunks le désintègre (ch. 16)")
fight(779.6, "univ6", "vegeta", "goku_black", "A", 2, ta=["retenue"],
      note="Vegeta Blue domine Black SSJ ; Zamasu l'emporte avant le Final Flash (ch. 19)", flags="i")
fight(779.62, "univ6", "beerus", "zamasu_present", "A", 3, note="Beerus efface le Zamasu du présent d'une main (ch. 19)")
fight(779.63, "univ6", "goku_black", "vegeta", "A", 2, ta=["boost"], tb=["epuise"],
      note="Soigné par Zamasu, Black passe Rosé et met Vegeta KO (ch. 20)")
fight(779.631, "univ6", "goku", "zamasu", "D", note="Goku domine mais Zamasu est immortel et détruit les senzu (ch. 20)", flags="i")
fight(779.64, "univ6", "goku_black", "trunks", "A", 2, ta=["retenue"], note="Black malmène Trunks avant la fuite (ch. 21)")
fight(779.65, "univ6", "vegeta", "goku_black", "A", 2,
      note="Vegeta en SSG avec pointes de Blue, Black envoyé dans un immeuble ; fusion juste après (ch. 22)", flags="i")
fight(779.651, "univ6", "goku", "zamasu", "A", 2, note="Goku SSG domine ; Mafūba raté faute de talisman (ch. 22)", flags="i")
fight(779.66, "univ6", "fused_zamasu", ["goku", "vegeta"], "A", 2, note="Kamehameha sans effet, double étranglement télékinétique (ch. 23)", flags="e")
fight(779.661, "univ6", "fused_zamasu", "goku", "A", 2, tb=["epuise"], note="Goku seul, pilonné par les blocs Katchin (ch. 23)")
fight(779.662, "univ6", "vegito", "fused_zamasu", "A", 2, ta=["boost"],
      note="Vegito Blue le découpe, Zamasu régénère ; la fusion Potara cède avant le Final Kamehameha (ch. 23-24)", flags="i")
fight(779.67, "univ6", "fused_zamasu", "vegeta", "A", 2, note="Vegeta assommé, sacrifié pour faire diversion (ch. 24)")
fight(779.671, "univ6", "fused_zamasu", "goku", "A", 1, tb=["epuise"],
      note="Goku Blue maîtrisé tient puis s'effondre ; le Hakai est paré avec Mai en bouclier (ch. 24-25)")
fight(779.68, "univ6", ["trunks", "vegeta"], "fused_zamasu", "D",
      note="La fusion se déchire, Trunks tranche, Vegeta lance le Gamma Burst Flash, Zamasu se multiplie ; Zeno efface tout (ch. 25-26)",
      flags="i")

# ---------------------------------------------------------------- avant le Tournoi du Pouvoir (ch. 27-32)
fight(780.0, "tdp", "beerus", "vegeta", "A", 3, ta=["retenue"], note="Entraînement : Vegeta Blue touche une fois, explosion de Beerus (ch. 27)")
fight(780.01, "tdp", "toppo", "goku", "A", 1, tb=["retenue"],
      note="Match d'exhibition devant les Zeno, Goku passe jusqu'au SSG, sorti du ring en voulant passer Blue (ch. 29)")
fight(780.02, "tdp", "android_17", "goku", "D", ta=["retenue"], tb=["retenue"],
      note="Goku masqué, jusqu'au SSJ3, 17 le bloque ; ils s'arrêtent pour parler (ch. 31)", flags="i")
fight(780.03, "tdp", "cabba", "caulifla", "A", 2, ta=["retenue"], note="Test de recrutement, Cabba SSJ (ch. 32)")

# ---------------------------------------------------------------- Tournoi du Pouvoir (ch. 33-42)
fight(780.1, "tdp", "goku", "pride_troopers", "A", 2, note="Les Troupes de l'Orgueil foncent sur Goku SSJ (ch. 33)")
fight(780.101, "tdp", "frost", ["krillin"], "A", 3, note="Krillin éliminé (ch. 34)")
fight(780.102, "tdp", "frost", ["tien"], "A", 3, note="Le Kikōhō ne fait rien, Tenshinhan éliminé (ch. 34)")
fight(780.103, "tdp", "frost", "u9_combattants", "A", 3, note="Frost à pleine puissance élimine six guerriers de l'Univers 9 (ch. 34)")
fight(780.104, "tdp", "gohan", "u9_combattants", "A", 2, ta=["retenue"], note="Gohan contre le Trio de Dangers, Piccolo le retient (ch. 34)", flags="i")
fight(780.105, "tdp", "freeza", "frost", "A", 3, ta=["surprise"], tb=["epuise"], note="Freezer trahit son allié et le jette hors du ring (ch. 34)")
fight(780.11, "tdp", ["toppo", "dyspo"], "goku", "A", 2, tb=["retenue"], note="Goku SSJ enfoncé dans le sol (ch. 35)")
fight(780.111, "tdp", "jiren", "hit", "A", 3, ta=["retenue"], note="Le saut temporel échoue, Hit éliminé d'un coup au dernier moment (ch. 35)")
fight(780.112, "tdp", "jiren", "goku", "A", 3, note="Goku Blue, le Kamehameha ne fait rien (ch. 35)", flags="i")
fight(780.12, "tdp", "android_17", "botamo", "A", 3, note="Coup au ventre, Botamo éjecté (ch. 36)")
fight(780.121, "tdp", "android_17", "u10_combattants", "A", 3, note="Dium, Napapa et Methiop sortis (ch. 36)")
fight(780.122, "tdp", "android_18", "ribrianne", "A", 2, note="18 se libère et force Ribrianne, Rozie et Kakunsa hors du ring (ch. 36)")
fight(780.123, "tdp", "vegeta", "toppo", "D", note="Vegeta Blue « parfait » surprend Toppo (ch. 36)", flags="i")
fight(780.13, "tdp", "freeza", "caulifla", "A", 2, ta=["retenue"], note="Freezer passe Golden après avoir été touché (ch. 37)")
fight(780.131, "tdp", "freeza", ["caulifla", "cabba"], "A", 3, note="Freezer Golden contre les deux Saiyans (ch. 37)")
fight(780.132, "tdp", "kale", "freeza", "A", 1, note="Kale berserk repousse Golden Freezer au bord (ch. 37)", flags="i")
fight(780.133, "tdp", "goku", "kale", "D", ta=["retenue"], tb=["boost"], note="Goku Blue arrête Kale, Freezer s'interpose (ch. 37)", flags="i")
fight(780.14, "tdp", "kale", ["u4_combattants", "u10_combattants", "magetta"], "A", 3, ta=["boost"],
      note="Rage de Kale : Univers 4 et 10 effacés, Magetta jeté dehors (ch. 38)")
fight(780.141, "tdp", "kale", "anilaza", "A", 3, ta=["boost"], note="Anilaza sorti d'un seul coup de poing, Univers 3 effacé (ch. 38)")
fight(780.142, "tdp", "dyspo", "cabba", "A", 2, note="Dyspo surclasse Cabba (ch. 38)", flags="i")
fight(780.143, "tdp", "kefla", "pride_troopers", "A", 2, note="Kefla met Tupper KO d'un coup et accule les Troupes (ch. 38)")
fight(780.15, "tdp", "gohan", "kefla", "D",
      note="Gohan sous sa forme ultime (sans Super Saiyan) ; double coup de poing, les deux éliminés, Univers 6 effacé (ch. 39)")
fight(780.151, "tdp", "roshi", "casserale", "A", 2, note="Rōshi l'attrape et le jette hors de l'arène (ch. 39)")
fight(780.152, "tdp", "jiren", "roshi", "A", 3, note="Rōshi esquive puis tombe sur un coup à la nuque (ch. 39)")
fight(780.153, "tdp", "jiren", "goku", "A", 2, ta=["retenue"], tb=["boost"],
      note="Goku Blue force ses réserves, effleure l'Ultra Instinct, projeté à travers l'arène (ch. 39)", flags="i")
fight(780.16, "tdp", "vegeta", "toppo", "A", 2, note="Toppo projeté hors de l'arène (ch. 40)")
fight(780.161, "tdp", "jiren", "vegeta", "A", 2, note="Vegeta au nouveau palier de Blue le touche puis est assommé (ch. 40)", flags="i")
fight(780.162, "tdp", ["freeza", "android_17"], ["toppo", "dyspo"], "A", 2, note="Freezer piège Toppo et Dyspo sur des rochers flottants (ch. 40)")
fight(780.163, "tdp", "jiren", ["freeza", "android_17"], "A", 2, tb=["retenue"],
      note="Jiren intervient, Dyspo et Toppo éliminés ; 17 fait semblant de s'autodétruire (ch. 40)")
fight(780.17, "tdp", "jiren", "goku", "A", 1, tb=["ultra"],
      note="Goku Ultra Instinct le touche, Kamehameha qui perce l'arène, puis l'Ultra Instinct s'épuise (ch. 41)")
fight(780.18, "tdp", "jiren", ["goku", "vegeta"], "A", 1, tb=["epuise"],
      note="Kamehameha + Gamma Burst Flash percés, Vegeta éliminé (ch. 42)")
fight(780.181, "tdp", ["freeza", "goku"], "jiren", "A", 1, ta=["epuise"],
      note="Freezer charge et sort Jiren avec Goku et lui-même ; 17 caché fait gagner l'Univers 7 (ch. 42)")

# ---------------------------------------------------------------- Moro (ch. 43-67)
fight(780.5, "moro", "moro", "vegeta", "A", 2, ta=["prepa"],
      note="Vegeta SSG puis Blue ; Moro aspire l'énergie de New Namek et des combattants (ch. 44-45)")
fight(780.51, "moro", "moro", ["goku", "vegeta"], "A", 3, ta=["prepa"], tb=["epuise"],
      note="Moro dévore le Galick Gun, vide leur énergie et retrouve sa jeunesse (ch. 46)")
fight(780.511, "moro", "majin_buu", "moro", "A", 2,
      note="Buu domine, le drainage n'a pas d'effet sur lui ; Porunga interrompt, Moro retrouve sa magie (ch. 47-48)", flags="i")
fight(780.512, "moro", "moro", "majin_buu", "A", 2,
      note="Buu sous le contrôle du Dai Kaiōshin hors de l'atmosphère, balayé (ch. 49)", flags="?")
fight(780.52, "moro", "merus", "goku", "D", ta=["retenue"], tb=["retenue"],
      note="Entraînement, Goku jusqu'au SSG ; arrêté quand la salle se fissure (ch. 51)", flags="i")
fight(780.521, "moro", "piccolo", "macareni", "A", 3, note="Le gang des Macareni ficelé (ch. 52)")
fight(780.522, "moro", "merus", "goku", "A", 2, ta=["retenue"], note="Entraînement sans transformation, Merus garde l'avantage (ch. 52-53)")
fight(780.53, "moro", "seven_three", "piccolo", "A", 1, ta=["prepa"],
      note="Seven-Three copie Piccolo, l'emporte au duel de Makankōsappō, Gohan le sauve (ch. 53)")
fight(780.531, "moro", "vegeta", "yuzun", "A", 3, note="Sur Yardrat, Vegeta en base ; Yuzun meurt de sa propre attaque (ch. 55)")
fight(780.532, "moro", "gohan", "seven_three", "A", 2,
      note="Gohan domine au Kamehameha ; Moro apparaît dans le cristal et lui donne ses pouvoirs (ch. 54)", flags="i")
fight(780.54, "moro", ["gohan", "piccolo"], "seven_three", "A", 1,
      note="Makankōsappō et Masenkōsappō, Seven-Three régénère et tente de les drainer (ch. 56)", flags="i")
fight(780.541, "moro", ["android_17", "android_18"], ["seven_three", "shimorekka"], "A", 2, note="Les deux jetés dans la poussière (ch. 56)")
fight(780.542, "moro", "krillin", "yunba", "A", 2, note="Kienzans, afterimage, Kamehameha (ch. 56-57)")
fight(780.543, "moro", ["tien", "chiaotzu"], "bikkura_koiter", "A", 2, note="Vaincu à coups d'insultes (ch. 57)")
fight(780.544, "moro", "zauyogi", "yamcha", "A", 2, note="Yamcha perd avant l'aide de Tenshinhan (ch. 57)", flags="i")
fight(780.545, "moro", "saganbo", ["android_17", "android_18", "gohan", "piccolo", "jaco"], "A", 2, ta=["emprunt"], tb=["epuise"],
      note="Saganbo dopé par le ki de Moro, ordre de les garder en vie (ch. 57-58)")
fight(780.5455, "moro", "goku", "iwaza_fusion", "A", 3, note="Assommée à distance à son arrivée (ch. 57-58)")
fight(780.546, "moro", "goku", "saganbo", "A", 3, tb=["emprunt"],
      note="Goku Blue le domine ; Saganbo meurt des injections de Moro (ch. 58)")
fight(780.55, "moro", "moro", "goku", "A", 2, ta=["retenue"], tb=["ultra"],
      note="Ultra Instinct « Sign » instable, Moro joue la montre puis l'écrase (ch. 59-60)")
fight(780.551, "moro", "moro", ["android_17", "android_18"], "A", 3, note="Le Chō Den'atsu Bakuretsu Zan ne fait rien (ch. 60)")
fight(780.56, "moro", "vegeta", "moro", "A", 2,
      note="Fission spirituelle forcée : Vegeta lui reprend l'énergie volée ; Moro absorbe alors Seven-Three (ch. 61)", flags="i")
fight(780.563, "moro", "moro", "vegeta", "A", 2, tb=["epuise"], note="Moro retourne le Big Bang Attack contre Vegeta Blue (ch. 62)")
fight(780.564, "moro", "moro", ["gohan", "piccolo"], "A", 2, note="Anneau d'énergie de Gohan sans effet durable (ch. 62)")
fight(780.565, "moro", "moro", "goku", "A", 2, tb=["epuise"], note="Goku Blue lui arrache un bras, Moro lui transperce la poitrine (ch. 62)")
fight(780.566, "moro", "moro", ["android_17", "android_18", "jaco"], "A", 3, note="Abattus sans se retourner (ch. 62)")
fight(780.57, "moro", "merus", "moro", "A", 2,
      note="Merus révèle ses pouvoirs d'ange et brise les cristaux de Moro, puis disparaît (ch. 63)", flags="i")
fight(780.571, "moro", "moro", "goku", "A", 2, tb=["ultra", "epuise"], note="Goku « Sign » renvoyé d'un coup (ch. 63)")
fight(780.58, "moro", "goku", "moro", "A", 3, ta=["ultra"],
      note="Ultra Instinct maîtrisé, God Bind, Moro enseveli et implorant (ch. 64)")
fight(780.59, "moro", "moro", "goku", "D", ta=["boost"], tb=["ultra", "retenue"],
      note="Moro absorbe Merus et fusionne avec la Terre, échanges indécis, Beerus reproche à Goku de jouer (ch. 65)", flags="i")
fight(780.595, "moro", "moro", "vegeta", "A", 2, tb=["epuise"], note="La fission forcée ne suffit plus, Vegeta à bout (ch. 66)")
fight(780.6, "moro", ["goku", "vegeta"], "moro", "A", 1, ta=["emprunt"],
      note="Énergie de Vegeta puis d'Uub et des Terriens : Goku brise le cristal du front (ch. 66)")

# ---------------------------------------------------------------- Granolah (ch. 68-87), flash-back de Bardock
fight(737.0, "avant", "bardock", "gas", "A", 1, ta=["epuise"],
      note="Flash-back sur Cereal, quarante ans plus tôt : Gas redevient enfant et s'évanouit ; Elec abat Bardock ensuite (ch. 82-83)")
fight(781.0, "granolah", "whis", "goku", "A", 3, ta=["retenue"], tb=["ultra"], note="Entraînement, les clones de Goku échouent (ch. 68)")
fight(781.001, "granolah", "gas", "granolah", "A", 2, note="Altercation au repaire des Heeters, clé de bras (ch. 68)", flags="?")
fight(781.01, "granolah", "beerus", "vegeta", "A", 3, ta=["retenue"], note="Hakai réglé pour ne détruire que l'armure (ch. 69)")
fight(781.011, "granolah", "granolah", ["oil", "maki"], "A", 3, ta=["retenue"], note="Une pichenette pour Oil, le foulard pour Maki (ch. 70)")
fight(781.012, "granolah", "whis", "goku", "A", 3, ta=["retenue"], note="Entraînement au bâton (ch. 71)")
fight(781.02, "granolah", "granolah", "goku", "A", 2, ta=["surprise", "prepa"], tb=["retenue"],
      note="Tir de sniper sur un point vital, Goku SSG + Ultra Instinct, Blue, puis UI argenté contre un clone (ch. 72-73)")
fight(781.03, "granolah", "granolah", "vegeta", "A", 1, tb=["epuise"],
      note="Vegeta passe Ultra Ego en fin de ch. 74 ; Granolah éveille son œil gauche et pulvérise la sphère finale (ch. 74-75)")
fight(781.04, "granolah", "granolah", "vegeta", "A", 1, tb=["ultra"], note="Ultra Ego brisé par des tirs rapides au cou (ch. 76)")
fight(781.041, "granolah", "granolah", "goku", "D", note="Goku Blue pare les coups mais ne peut pas gagner en défense ; Monaito interrompt (ch. 76)", flags="i")
fight(781.06, "granolah", "gas", "granolah", "A", 3, note="Gas après le vœu, Granolah broyé (ch. 78)")
fight(781.061, "granolah", "gas", ["goku", "vegeta"], "A", 3, tb=["epuise"], note="Armes de ki, Goku entravé aux quatre membres (ch. 78)")
fight(781.07, "granolah", "granolah", ["oil", "maki"], "A", 3, note="Envoyés dans une montagne pour avoir menacé Monaito (ch. 79)")
fight(781.08, "granolah", "gas", "granolah", "A", 3, ta=["boost"],
      note="Granolah domine en vitesse, puis Elec retire le limiteur : Gas berserk lui brise les bras (ch. 79-81)")
fight(781.09, "granolah", "goku", "gas", "D", note="Goku Blue l'emmène de planète en planète par téléportation (ch. 81-82)", flags="i")
fight(781.1, "granolah", "gas", ["goku", "vegeta"], "A", 2, tb=["ultra"], note="UI et Ultra Ego, Gas les tient tous les deux (ch. 84)", flags="i")
fight(781.11, "granolah", "gas", "vegeta", "A", 2, tb=["ultra"], note="Vegeta Ultra Ego s'évanouit (ch. 85)")
fight(781.12, "granolah", ["goku", "granolah"], "gas", "A", 2, ta=["ultra"],
      note="Goku « Sign » puis UI maîtrisé et avatar géant, rayon chargé de Granolah (ch. 85-86)")
fight(781.25, "granolah", "freeza", ["gas", "elec"], "A", 3, tb=["epuise"],
      note="Freezer les abat chacun d'un coup, Gas déjà vaincu par Goku et Granolah (ch. 87)")
fight(781.251, "granolah", "freeza", ["goku", "vegeta"], "A", 3, tb=["ultra", "epuise"],
      note="Black Freezer met UI Goku et Ultra Ego Vegeta au tapis d'un coup chacun, puis repart (ch. 87)")

# ---------------------------------------------------------------- Super Hero (ch. 88-100)
fight(781.5, "superhero", "trunks_kid", "robots_hedo", "A", 3, note="Saiyaman X-1, robots Alpha (ch. 88)")
fight(781.501, "superhero", "goten", "robots_hedo", "A", 3, note="Combinaison Beta n° 2 détruite au lycée (ch. 89)")
fight(781.502, "superhero", ["goten", "trunks_kid", "krillin"], "robots_hedo", "A", 2,
      note="Dinodroïde du Dr Hedo, Kienzan sur l'interrupteur puis SSJ (ch. 90)")
fight(781.51, "superhero", "hachimaru", "krillin", "A", 2, ta=["surprise"], note="Krillin semé pendant la poursuite (ch. 91)")
fight(781.52, "superhero", "gamma_2", "piccolo", "A", 2, tb=["retenue"],
      note="Piccolo s'en tire de justesse et se fait passer pour mort (ch. 91-92)")
fight(781.54, "superhero", "gamma_1", "gohan", "A", 2, tb=["surprise"], note="Gohan SSJ, rouillé, dominé (ch. 94)")
fight(781.55, "superhero", ["gamma_1", "gamma_2"], ["gohan", "piccolo"], "A", 1,
      note="Piccolo presque tué par Gamma 2 avant le vœu de Shenron (ch. 95)")
fight(781.551, "superhero", "piccolo", "gamma_2", "A", 3, note="Piccolo Orange encaisse sans bouger (ch. 96)")
fight(781.552, "superhero", "gohan", "gamma_1", "A", 1, note="Gohan Ultime contre Gamma 1, interrompu par la révélation de Gamma 2 (ch. 95-96)", flags="?")
fight(781.56, "superhero", "cell_max", ["goten", "trunks_kid", "gamma_1", "gamma_2"], "A", 2,
      note="Tornado Super Hurricane, Cell Max se remet aussitôt (ch. 97)")
fight(781.57, "superhero", "cell_max", ["krillin", "gamma_2", "piccolo"], "A", 2,
      note="Taiyōken de Krillin, Gamma 2 se sacrifie, Piccolo Orange tient jusqu'au réveil de Gohan (ch. 98)")
fight(781.6, "superhero", ["gohan", "piccolo"], "cell_max", "A", 2, ta=["ultra"],
      note="Gohan Beast, le coup de Cell Max ne passe pas son aura ; Makankōsappō dans la tête (ch. 99-100)")

# ---------------------------------------------------------------- après Super Hero (ch. 101-104)
fight(781.7, "superhero", "gohan", "carmine", "A", 3, ta=["ultra"], note="Carmine attaque la maison de Gohan, qui passe Beast (ch. 101)")
fight(781.71, "superhero", "gohan", ["goten", "trunks_kid"], "A", 3, note="Sur la planète de Beerus, la fusion échoue encore (ch. 102)")
fight(781.72, "superhero", "goku", "gohan", "D", ta=["ultra"], tb=["ultra"],
      note="UI contre Beast : Gohan fait sortir Goku de l'Ultra Instinct d'un coup au ventre, Goku arrête satisfait (ch. 102-103)")
