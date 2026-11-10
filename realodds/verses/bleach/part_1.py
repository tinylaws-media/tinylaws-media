# Bleach, partie 1 : du passé lointain à la fin de l'arc Fullbring (ch. -108 à -97, ch. 1-479).
# Manga de Kubo uniquement (pas de fillers de l'anime, pas de films, pas de romans). "fight" est injecté par data.py.
# Numéros de chapitre : titres et résumés de volumes de la liste des chapitres (Wikipedia) et pages de combat du
# Bleach Wiki ; « ch. ~N » = à un ou deux chapitres près.
# Repères de temps (t = années depuis la rencontre d'Ichigo et Rukia, ch. 1) : remplaçant 0.00-0.12, entraînement
# chez Urahara 0.12-0.14, Soul Society 0.15-0.23, Grand Fisher arrancar 0.28, première invasion arrancar 0.30-0.32,
# Visored 0.35-0.37, Hueco Mundo 0.40-0.45, faux Karakura 0.46-0.475, Fullbring 1.85-1.97 (17 mois plus tard).
# Flash-back : Yamamoto contre Yhwach -1000 (« il y a mille ans », ch. 506-511), jeune Zaraki contre Unohana -150
# (date inconnue, ch. 527-528), Turn Back the Pendulum -110 à -101 (« il y a 110 ans » puis « 9 ans plus tard »),
# mort de Kaien vers -45 (Rukia entrée à la 13e division quelques décennies avant l'histoire), Kiganjo tué par Zaraki
# (date inconnue, placé à -45), Isshin contre White -20 (ch. 531-535), mort de Masaki -6 (Ichigo a 9 ans, ch. 19-20).

CHARS_PART = {
    # ---------------------------------------------------------------- Ichigo et ses amis
    "ichigo": ("Ichigo Kurosaki", "Karakura", 1.5, None, None),
    "ichigo_hollow": ("Ichigo, Hollow intégral (contre Ulquiorra)", "Karakura", 5.5, 0.4425, None),
    "rukia": ("Rukia Kuchiki", "Gotei 13", 2.0, None, None),
    "uryu": ("Uryū Ishida", "Quincy", 1.5, None, None),
    "chad": ("Yasutora Sado (Chad)", "Karakura", 1.2, None, None),
    "orihime": ("Orihime Inoue", "Karakura", 0.6, None, None),
    "ganju": ("Ganju Shiba", "Rukongai", 1.5, None, None),
    "kon": ("Kon (âme modifiée)", "Karakura", 1.0, None, None),
    # ---------------------------------------------------------------- Exilés et anciens capitaines
    "urahara": ("Kisuke Urahara", "Exilés", 5.0, None, None),
    "yoruichi": ("Yoruichi Shihōin", "Exilés", 4.8, None, None),
    "tessai": ("Tessai Tsukabishi", "Exilés", 4.0, None, None),
    "ururu": ("Ururu Tsumugiya", "Exilés", 1.8, None, None),
    "isshin": ("Isshin Kurosaki (Shiba)", "Gotei 13", 4.5, None, None),
    "masaki": ("Masaki Kurosaki", "Quincy", 3.5, -6.0, None),
    # ---------------------------------------------------------------- Gotei 13 : capitaines
    "yamamoto": ("Genryūsai Shigekuni Yamamoto (1re division)", "Gotei 13", 6.5, 2.0095, None),
    "soifon": ("Suì-Fēng (2e division)", "Gotei 13", 4.3, None, None),
    "gin": ("Gin Ichimaru (3e division)", "Gotei 13", 4.6, 0.4662, None),
    "unohana": ("Retsu Unohana (4e division, premier Kenpachi)", "Gotei 13", 5.5, 2.1706, None),
    "aizen": ("Sōsuke Aizen", "Gotei 13", 4.5, None, None),
    "byakuya": ("Byakuya Kuchiki (6e division)", "Gotei 13", 4.5, None, None),
    "komamura": ("Sajin Komamura (7e division)", "Gotei 13", 4.2, None, None),
    "kyoraku": ("Shunsui Kyōraku (8e division)", "Gotei 13", 4.9, None, None),
    "tosen": ("Kaname Tōsen (9e division)", "Gotei 13", 4.2, 0.4625, None),
    "hitsugaya": ("Tōshirō Hitsugaya (10e division)", "Gotei 13", 4.2, None, None),
    "kenpachi": ("Kenpachi Zaraki (11e division)", "Gotei 13", 3.8, None, None),
    "mayuri": ("Mayuri Kurotsuchi (12e division)", "Gotei 13", 4.4, None, None),
    "ukitake": ("Jūshirō Ukitake (13e division)", "Gotei 13", 4.6, 2.26, None),
    "kiganjo": ("Kenpachi Kiganjō (ancien capitaine de la 11e)", "Gotei 13", 4.0, -45.0, None),
    # ---------------------------------------------------------------- Gotei 13 : lieutenants et officiers
    "sasakibe": ("Chōjirō Sasakibe (lieutenant, 1re)", "Gotei 13", 3.5, 2.003, None),
    "omaeda": ("Marechiyo Ōmaeda (lieutenant, 2e)", "Gotei 13", 2.6, None, None),
    "kira": ("Izuru Kira (lieutenant, 3e)", "Gotei 13", 3.0, None, None),
    "hinamori": ("Momo Hinamori (lieutenant, 5e)", "Gotei 13", 3.0, None, None),
    "renji": ("Renji Abarai (lieutenant, 6e)", "Gotei 13", 3.2, None, None),
    "iba": ("Tetsuzaemon Iba (lieutenant, 7e)", "Gotei 13", 2.8, None, None),
    "nanao": ("Nanao Ise (lieutenant, 8e)", "Gotei 13", 2.6, None, None),
    "hisagi": ("Shūhei Hisagi (lieutenant, 9e)", "Gotei 13", 3.0, None, None),
    "rangiku": ("Rangiku Matsumoto (lieutenant, 10e)", "Gotei 13", 3.0, None, None),
    "yachiru": ("Yachiru Kusajishi (lieutenant, 11e)", "Gotei 13", 3.2, None, None),
    "nemu": ("Nemu Kurotsuchi (lieutenant, 12e)", "Gotei 13", 2.8, 2.2895, None),
    "kaien": ("Kaien Shiba (lieutenant, 13e)", "Gotei 13", 3.5, -45.0, None),
    "ikkaku": ("Ikkaku Madarame (3e siège, 11e)", "Gotei 13", 2.6, None, None),
    "yumichika": ("Yumichika Ayasegawa (5e siège, 11e)", "Gotei 13", 2.3, None, None),
    "jirobo": ("Jirōbō Ikkanzaka (4e siège, 7e)", "Gotei 13", 1.5, None, None),
    "jidanbo": ("Jidanbō Ikkanzaka (gardien de la porte)", "Gotei 13", 1.8, None, None),
    "shinigami": ("Shinigami anonymes (groupe)", "Gotei 13", 1.2, None, None),
    # ---------------------------------------------------------------- Visored
    "shinji": ("Shinji Hirako", "Visored", 4.6, None, None),
    "kensei": ("Kensei Muguruma", "Visored", 4.2, None, None),
    "rose": ("Rōjūrō Ōtoribashi (Rose)", "Visored", 4.0, None, None),
    "love": ("Love Aikawa", "Visored", 4.0, None, None),
    "lisa": ("Lisa Yadōmaru", "Visored", 3.5, None, None),
    "hiyori": ("Hiyori Sarugaki", "Visored", 3.4, None, None),
    "mashiro": ("Mashiro Kuna", "Visored", 3.5, None, None),
    "hachi": ("Hachigen Ushōda", "Visored", 3.8, None, None),
    # ---------------------------------------------------------------- Hollows du début
    "hollows": ("Hollows ordinaires (groupe)", "Hollows", 0.8, None, None),
    "fishbone": ("Fishbone D", "Hollows", 1.0, 0.0001, None),
    "sora": ("Acidwire (Sora Inoue)", "Hollows", 1.0, 0.0101, None),
    "shrieker": ("Shrieker", "Hollows", 1.2, 0.0201, None),
    "grand_fisher": ("Grand Fisher", "Hollows", 2.0, 0.2802, None),
    "numb_chandelier": ("Numb Chandelier", "Hollows", 1.3, 0.0651, None),
    "menos": ("Menos Grande (Gillian)", "Hollows", 2.2, None, None),
    "metastacia": ("Metastacia", "Hollows", 3.3, -45.0, None),
    "white": ("White (Hollow expérimental d'Aizen)", "Hollows", 4.2, -20.0, None),
    "runuganga": ("Runuganga", "Hollows", 2.0, None, None),
    # ---------------------------------------------------------------- Espada
    "stark": ("Coyote Stark (Espada 1)", "Espada", 5.3, 0.4625, None),
    "baraggan": ("Baraggan Louisenbairn (Espada 2)", "Espada", 5.1, 0.4618, None),
    "harribel": ("Tia Harribel (Espada 3)", "Espada", 5.0, None, None),
    "ulquiorra": ("Ulquiorra Cifer (Espada 4)", "Espada", 4.9, 0.4425, None),
    "nnoitra": ("Nnoitra Gilga (Espada 5)", "Espada", 4.7, 0.4247, None),
    "grimmjow": ("Grimmjow Jaegerjaquez (Espada 6)", "Espada", 4.5, None, None),
    "zommari": ("Zommari Rureaux (Espada 7)", "Espada", 4.2, 0.4245, None),
    "szayel": ("Szayelaporro Granz (Espada 8)", "Espada", 4.1, 0.4255, None),
    "aaroniero": ("Aaroniero Arruruerie (Espada 9)", "Espada", 3.9, 0.4135, None),
    "yammy": ("Yammy Llargo (Espada 10 / 0)", "Espada", 4.0, 0.4632, None),
    "luppi": ("Luppi Antenor (Espada 6 intérimaire)", "Espada", 3.8, 0.3712, None),
    "nelliel": ("Nelliel Tu Odelschwanck (ancienne Espada 3)", "Arrancar", 4.5, None, None),
    # ---------------------------------------------------------------- Arrancar et Fracciones
    "wonderweiss": ("Wonderweiss Margela", "Arrancar", 4.2, 0.4632, None),
    "hooleer": ("Hooleer", "Arrancar", 2.6, 0.4632, None),
    "ayon": ("Ayon", "Arrancar", 4.0, 0.4612, None),
    "tres_bestias": ("Tres Bestias (Apacci, Mila Rose, Sung-Sun)", "Fracción", 3.0, None, None),
    "poww": ("Choe Neng Poww", "Fracción", 3.4, None, None),
    "charlotte": ("Charlotte Chuhlhourne", "Fracción", 3.0, None, None),
    "avirama": ("Avirama Redder", "Fracción", 2.8, 0.4605, None),
    "findor": ("Findor Carias", "Fracción", 2.9, None, None),
    "ggio": ("Ggio Vega", "Fracción", 2.8, None, None),
    "nirgge": ("Nirgge Parduoc", "Fracción", 2.6, None, None),
    "shawlong": ("Shawlong Kū Fan", "Fracción", 3.1, 0.3105, None),
    "yylfordt": ("Yylfordt Granz", "Fracción", 3.0, 0.3105, None),
    "nakeem": ("Nakeem Grindina", "Fracción", 2.9, 0.3105, None),
    "edorad": ("Edrad Liones", "Fracción", 3.0, 0.3105, None),
    "droy": ("Di Roy Rinker", "Fracción", 2.0, 0.3101, None),
    "dordoni": ("Dordoni Alessandro Del Socaccio (Privaron)", "Arrancar", 3.0, None, None),
    "cirucci": ("Cirucci Sanderwicci (Privaron)", "Arrancar", 2.8, None, None),
    "gantenbainne": ("Gantenbainne Mosqueda (Privaron)", "Arrancar", 3.0, None, None),
    "demora": ("Demōra Zodd", "Arrancar", 2.0, None, None),
    "iceringer": ("Iceringer", "Arrancar", 1.8, None, None),
    "tesla": ("Tesla Lindocruz", "Fracción", 3.2, 0.4241, None),
    "rudbornn": ("Rudbornn Chelute (Exequias)", "Arrancar", 3.0, None, None),
    "exequias": ("Exequias (groupe)", "Arrancar", 2.0, None, None),
    "loly_menoly": ("Loly et Menoly", "Arrancar", 1.6, None, None),
    # ---------------------------------------------------------------- Xcution
    "ginjo": ("Kūgo Ginjō", "Xcution", 3.8, 1.9705, None),
    "tsukishima": ("Shūkurō Tsukishima", "Xcution", 3.6, None, None),
    "riruka": ("Riruka Dokugamine", "Xcution", 2.4, None, None),
    "jackie": ("Jackie Tristan", "Xcution", 2.7, None, None),
    "giriko": ("Giriko Kutsuzawa", "Xcution", 2.9, 1.9615, None),
    "yukio": ("Yukio Hans Vorarlberna", "Xcution", 2.9, None, None),
    "moe": ("Moe Shishigawara", "Xcution", 1.6, None, None),
}

GENERIC_PART = {"shinigami", "hollows", "menos", "exequias", "tres_bestias", "loly_menoly"}

# gains et pertes permanents : (perso, temps, changement moyen en échelons, écart-type, libellé)
JUMPS_PART = [
    # Ichigo
    ("ichigo", 0.13, 1.4, 0.5, "Entraînement chez Urahara : chaîne tranchée, pouvoirs propres retrouvés et Shikai Zangetsu (ch. 59-67)"),
    ("ichigo", 0.1855, 0.9, 0.4, "Apprend le nom de Zangetsu en plein combat contre Kenpachi (ch. 111-113)"),
    ("ichigo", 0.2, 0.8, 0.5, "Bankai Tensa Zangetsu en trois jours avec le Tenshintai (ch. 128-131, 155)"),
    ("ichigo", 0.355, 0.7, 0.4, "Masque Hollow maîtrisé chez les Visored (ch. 218-226)"),
    ("ichigo", 0.4195, 0.3, 0.3, "Masque tenu plus longtemps à Hueco Mundo (ch. 279-285)"),
    ("ichigo", 0.4705, 1.2, 0.5, "Trois mois d'entraînement dans le Dangai, fusion avec Zangetsu (ch. 405-412)"),
    ("ichigo", 0.4715, 1.2, 0.5, "Getsuga Tenshō final : Ichigo devient le Getsuga, Mugetsu (ch. 418-419)"),
    ("ichigo", 0.475, -6.5, 0.8, "Perte de ses pouvoirs de shinigami (ch. 420-423)"),
    ("ichigo", 1.92, 2.0, 0.6, "Fullbring appris auprès de Xcution (ch. 433-447)"),
    ("ichigo", 1.945, 0.5, 0.4, "Fullbring complet (ch. 453-455)"),
    ("ichigo", 1.952, 2.8, 0.7, "Pouvoirs de shinigami restaurés par l'épée imprégnée du reiatsu des capitaines (ch. 459-460)"),
    # Rukia, Renji, Uryu, Chad, Orihime
    ("rukia", 0.0002, -1.5, 0.5, "Transmet ses pouvoirs à Ichigo (ch. 1)"),
    ("rukia", 0.15, 1.3, 0.5, "Pouvoirs retrouvés en détention à la Soul Society (ch. 81-100)"),
    ("rukia", 0.3, 0.3, 0.3, "Gigai spécial d'Urahara, pouvoirs pleins (ch. 198-199)"),
    ("renji", 0.2, 0.8, 0.4, "Bankai Hihiō Zabimaru, entraîné avec Yoruichi (ch. 140-142)"),
    ("uryu", 0.1895, 1.2, 0.5, "Quincy Letzt Stil (ch. 124-125)"),
    ("uryu", 0.1905, -2.2, 0.6, "Perte de ses pouvoirs de Quincy après le Letzt Stil (ch. 126)"),
    ("uryu", 0.36, 2.5, 0.6, "Pouvoirs restaurés par Ryūken, Seele Schneider (ch. 214, ch. 243-258)"),
    ("chad", 0.06, 1.0, 0.4, "Éveil du bras droit du géant (ch. 38-39)"),
    ("chad", 0.14, 0.4, 0.3, "Entraînement de Yoruichi (ch. 65-69)"),
    ("chad", 0.36, 0.5, 0.4, "Entraînement avec Renji chez Urahara (ch. 214-243)"),
    ("chad", 0.4105, 0.6, 0.4, "Brazo Derecha de Gigante et Brazo Izquierda del Diablo (ch. 259-261)"),
    ("orihime", 0.065, 1.0, 0.4, "Éveil du Shun Shun Rikka (ch. 41-43)"),
    ("grand_fisher", 0.27, 1.2, 0.5, "Devenu arrancar (ch. 184-186)"),
    # Aizen et le Hogyoku
    ("aizen", 0.459, 1.2, 0.5, "Hōgyoku fusionné dans sa poitrine (révélé ch. 395-397)"),
    ("aizen", 0.4645, 0.8, 0.4, "Première transformation du Hōgyoku (ch. 399-403)"),
    ("aizen", 0.4655, 0.7, 0.4, "Fin de l'âge de la chrysalide, deuxième forme (ch. 405-406)"),
    ("aizen", 0.4712, 0.8, 0.4, "Troisième forme ailée, au-delà du shinigami et du Hollow (ch. 416-417)"),
    ("aizen", 0.4735, -2.0, 0.6, "Le Hōgyoku le rejette ; retour à la forme humaine, scellé par le kidō d'Urahara (ch. 420-422)"),
    # autres
    ("kenpachi", -149.9, -1.2, 0.5, "Après le combat contre Unohana, il bride inconsciemment sa force (ch. 527-528)"),
    ("kenpachi", 0.4245, 0.3, 0.3, "Kendō à deux mains contre Nnoitra (ch. 309-311)"),
    ("isshin", -19.9, -3.0, 0.7, "Pouvoirs de shinigami perdus en sauvant Masaki, réfugié dans un gigai (ch. 535-536)"),
    ("isshin", 0.27, 3.0, 0.7, "Pouvoirs de shinigami retrouvés (révélé ch. 185-186)"),
    ("masaki", -19.95, -0.3, 0.4, "Contaminée par White en le tuant (ch. 534-535)"),
    ("yammy", 0.4626, 1.3, 0.5, "Resurrección Ira, Espada 0 (ch. 382-386)"),
    ("yamamoto", -500.0, -0.4, 0.4, "Assagi après mille ans de paix selon Yhwach (ch. 510-511)"),
    ("ginjo", 1.9575, 1.0, 0.5, "Absorbe le Fullbring d'Ichigo, Fullbring de type Bankai (ch. 458-461)"),
]

# ============================================================== Il y a mille ans / passé lointain
fight(-1000.0, "fondation", "yamamoto", "yhwach", "A", 2,
      note="Yamamoto vainc Yhwach il y a mille ans et le scelle ; Yhwach le rappelle avant de le tuer (ch. 506-511)")
fight(-150.0, "passe", "unohana", "kenpachi", "D",
      note="Le jeune Zaraki affronte Unohana, le premier Kenpachi, et lui laisse la cicatrice de sa poitrine ; "
           "il bride ensuite sa force pour ne plus perdre un adversaire digne de lui (ch. 527-528) ; date inconnue", flags="i?")

# ============================================================== Turn Back the Pendulum (il y a 110 / 101 ans)
fight(-101.02, "pendule", ["kensei", "mashiro"], "shinigami", "A", 3, ta=["malade"],
      note="Kensei et Mashiro hollowifiés massacrent leur escouade (ch. -102 à -101)", flags="?")
fight(-101.01, "pendule", ["shinji", "rose", "love", "lisa", "hachi"], ["kensei", "mashiro", "hiyori"], "A", 2,
      tb=["malade"], note="Shinji et ses pairs maîtrisent Kensei, Mashiro et Hiyori en pleine hollowification (ch. -100)")
fight(-101.0, "pendule", "tosen", ["shinji", "rose", "love", "lisa", "hachi"], "A", 2, ta=["surprise"], tb=["malade"],
      note="Bankai de Tōsen dans le dos, les capitaines s'effondrent sous la hollowification (ch. -100 à -99)")
fight(-100.99, "pendule", ["urahara", "tessai"], "aizen", "D", tb=["retenue"],
      note="Urahara et Tessai interviennent avant qu'Aizen n'achève Shinji ; Aizen se retire (ch. -98 à -97)", flags="i")

# ============================================================== Il y a un demi-siècle
fight(-45.01, "avant", "kenpachi", "kiganjo", "A", 3,
      note="Zaraki tue le Kenpachi en titre devant 200 membres de la 11e division et prend son nom (databook Souls., "
           "évoqué ch. ~104) ; date inconnue", flags="?")
fight(-45.0, "avant", "metastacia", "kaien", "A", 2,
      note="Metastacia détruit le Zanpakutō de Kaien et possède son corps (ch. 133-136)")
fight(-44.999, "avant", "rukia", "kaien", "A", 2, tb=["malade"],
      note="Rukia transperce Kaien possédé par Metastacia (ch. 136)", flags="?")

# ============================================================== Il y a 20 ans (Isshin et Masaki)
fight(-20.01, "isshin", "white", "isshin", "A", 1, note="White, Hollow expérimental d'Aizen, prend l'ascendant sur Isshin (ch. 531-533)", flags="i")
fight(-20.0, "isshin", ["masaki", "isshin"], "white", "A", 2,
      note="Masaki intervient, White meurt mais la mord et la contamine (ch. 533-535)", flags="e")

# ============================================================== Shinigami remplaçant
fight(0.0, "remplacant", "fishbone", "rukia", "A", 2, tb=["protege"],
      note="Rukia blessée en protégeant Ichigo (ch. 1)")
fight(0.0001, "remplacant", "ichigo", "fishbone", "A", 3, note="Ichigo reçoit les pouvoirs de Rukia et tranche Fishbone D (ch. 1)")
fight(0.01, "remplacant", "ichigo", "sora", "A", 2, note="Ichigo affronte le Hollow de Sora, qui se purifie lui-même (ch. 3-6)")
fight(0.02, "remplacant", "ichigo", "shrieker", "A", 2, note="Ichigo tue Shrieker, Chad l'a retenu (ch. 8-12)")
fight(0.03, "remplacant", ["ichigo", "kon"], "hollows", "A", 3, note="Hollows de l'hôpital et de Karakura (ch. 13-16, ch. 26-33)")
fight(0.04, "remplacant", "ichigo", "grand_fisher", "A", 1,
      note="Ichigo blesse Grand Fisher, qui s'enfuit (ch. 17-25)", flags="i")
fight(0.06, "remplacant", "chad", "hollows", "A", 2, note="Chad éveille son bras pour sauver Karin (ch. 38-39)")
fight(0.065, "remplacant", "orihime", "numb_chandelier", "A", 2, note="Orihime éveille le Shun Shun Rikka (ch. 41-43)")
fight(0.07, "remplacant", ["ichigo", "uryu"], "menos", "A", 1,
      note="Dos à dos contre les Hollows attirés par Uryū ; Ichigo repousse le Menos Grande (ch. 44-48)", flags="e")
fight(0.1, "remplacant", "renji", "uryu", "A", 3, note="Renji abat Uryū (ch. 51-53)")
fight(0.1001, "remplacant", "ichigo", "renji", "D", tb=["retenue"],
      note="Ichigo, débordant de reiatsu, fait jeu égal et presque vaincre Renji (ch. 53-55)", flags="i")
fight(0.1002, "remplacant", "byakuya", "ichigo", "A", 3, ta=["retenue"],
      note="Byakuya écrase Ichigo et détruit ses chaînes de pouvoir (ch. 55-57)")

# ============================================================== Entraînement chez Urahara puis Soul Society (Shikai)
fight(0.125, "soulsociety", "ururu", "ichigo", "A", 2, note="Ichigo esquive Ururu puis la repousse d'un coup de poing (ch. 59-60)", flags="?")
fight(0.14, "soulsociety", "ichigo", "urahara", "A", 1, tb=["retenue"],
      note="Ichigo libère Zangetsu et fend le chapeau d'Urahara, fin du test (ch. 66-67)", flags="?")
fight(0.15, "soulsociety", "ichigo", "jidanbo", "A", 3, note="Ichigo brise la hache de Jidanbō (ch. 72-74)")
fight(0.1501, "soulsociety", "gin", "ichigo", "A", 2, ta=["retenue"], note="Shinsō repousse les intrus hors du Seireitei (ch. 75)")
fight(0.17, "soulsociety", "ichigo", "ikkaku", "A", 2, note="Ichigo bat Ikkaku, qui cachait son Bankai (ch. 86-89)")
fight(0.1701, "soulsociety", "ganju", "yumichika", "A", 1,
      note="Ganju vainc Yumichika avec ses feux d'artifice ; Yumichika cachait le vrai pouvoir de Fuji Kujaku (ch. 89-92)", flags="?")
fight(0.1702, "soulsociety", "uryu", "jirobo", "A", 3, note="Uryū écrase Jirōbō (ch. 91)")
fight(0.175, "soulsociety", "ichigo", "renji", "A", 1, note="Ichigo vainc Renji grâce à l'entraînement d'Urahara (ch. 94-98)")
fight(0.18, "soulsociety", "hinamori", "kira", "D", note="Hinamori et Kira s'affrontent, Hitsugaya les sépare (ch. 99-101)", flags="i")
fight(0.181, "soulsociety", "kyoraku", "chad", "A", 3, ta=["retenue"], note="Kyōraku met Chad hors combat sans dégainer pour de bon (ch. 105-108)")
fight(0.185, "soulsociety", "kenpachi", "ichigo", "A", 3, ta=["retenue"],
      note="Premier assaut : Kenpachi, cache-œil limiteur de Mayuri encore en place, transperce Ichigo (ch. 104-110) ; il l'ôte au second assaut")
fight(0.186, "soulsociety", "ichigo", "kenpachi", "A", 1,
      note="Ichigo, Zangetsu à pleine puissance, tranche Kenpachi ; les deux s'effondrent, Kenpachi se reconnaît vaincu (ch. 111-114)")
fight(0.19, "soulsociety", "byakuya", "ganju", "A", 3, note="Ganju presque tué par Byakuya, Ukitake intervient (ch. 116-118)")
fight(0.1901, "soulsociety", "byakuya", "ichigo", "D", ta=["retenue"],
      note="Brève passe, Yoruichi assomme Ichigo pour l'emmener s'entraîner (ch. 119-120)", flags="i")
fight(0.1895, "soulsociety", "uryu", "mayuri", "A", 2,
      note="Letzt Stil de Quincy : Uryū force Mayuri à se liquéfier pour fuir (ch. 121-126)")
fight(0.192, "soulsociety", "tosen", "uryu", "A", 3, tb=["epuise"], note="Uryū, privé de pouvoirs, est incarcéré par Tōsen (ch. 126-127)")

# ============================================================== Soul Society : Bankai et trahison d'Aizen
fight(0.2, "bankai", "hitsugaya", "gin", "D", note="Hitsugaya attaque Gin, Rangiku les sépare (ch. 131-132)", flags="i")
fight(0.205, "bankai", "byakuya", "renji", "A", 2, note="Bankai contre Bankai, Senbonzakura Kageyoshi domine Renji (ch. 140-145)")
fight(0.21, "bankai", "kenpachi", ["tosen", "komamura"], "A", 2,
      note="Kenpachi vainc Tōsen malgré son Bankai et Komamura malgré le sien (ch. 146-151)")
fight(0.212, "bankai", "yamamoto", ["kyoraku", "ukitake"], "D", ta=["retenue"], tb=["retenue"],
      note="Duel commencé après la destruction du Sōkyoku, interrompu par la révélation de la trahison (ch. 153-157, ch. 178)", flags="i?")
fight(0.214, "bankai", "yoruichi", "soifon", "A", 2, note="Shunkō de Yoruichi, Suì-Fēng s'effondre (ch. 154-161)")
fight(0.216, "bankai", "ichigo", "byakuya", "A", 1,
      note="Bankai contre Bankai ; le Hollow intérieur intervient, Ichigo l'emporte au dernier échange et Byakuya s'avoue vaincu (ch. 155-166)")
fight(0.218, "bankai", "aizen", "hitsugaya", "A", 3, note="Aizen tranche Hitsugaya en Bankai d'un coup (ch. 169-172)")
fight(0.2185, "bankai", "aizen", ["ichigo", "renji"], "A", 3, tb=["epuise"],
      note="Aizen pare Ichigo d'un doigt et tranche Ichigo et Renji, épuisés par leurs duels (ch. 173-175)")
fight(0.219, "bankai", "aizen", "komamura", "A", 3, note="Hadō 90 Kurohitsugi sur Komamura (ch. 175-176)")

# ============================================================== Arrancar : première invasion
fight(0.28, "arrancar", "isshin", "grand_fisher", "A", 3, note="Isshin pourfend Grand Fisher devenu arrancar d'un coup (ch. 184-186)")
fight(0.3, "arrancar", "yammy", ["chad", "orihime"], "A", 3, note="Yammy brise le bras de Chad et repousse Orihime (ch. 188-191)")
fight(0.3005, "arrancar", "yammy", "ichigo", "A", 1, note="Ichigo en Bankai mène puis se fige quand le Hollow intérieur se manifeste (ch. 191-193)", flags="i")
fight(0.301, "arrancar", ["urahara", "yoruichi"], "yammy", "A", 3, note="Urahara et Yoruichi écrasent Yammy, Ulquiorra l'emmène (ch. 193-195)", flags="e")
fight(0.31, "arrancar", "rukia", "droy", "A", 3, note="Sode no Shirayuki, Di Roy gelé (ch. 198-200)")
fight(0.3101, "arrancar", "grimmjow", "rukia", "A", 3, note="Grimmjow transperce Rukia (ch. 200-201)")
fight(0.3103, "arrancar", "ikkaku", "edorad", "A", 1, note="Ikkaku forcé d'utiliser son Bankai Ryūmon Hōzukimaru (ch. 202-206)")
fight(0.3104, "arrancar", "rangiku", "nakeem", "A", 2, note="Limitation levée, Rangiku l'emporte (ch. 207-210)")
fight(0.3104, "arrancar", "renji", "yylfordt", "A", 2, note="Limitation levée, Bankai de Renji (ch. 207-210)")
fight(0.3104, "arrancar", "hitsugaya", "shawlong", "A", 2, note="Limitation levée, Bankai de Hitsugaya (ch. 207-211)")
fight(0.312, "arrancar", "grimmjow", "ichigo", "A", 2, ta=["retenue"],
      note="Grimmjow domine Ichigo en Bankai sans se libérer, Tōsen le rappelle (ch. 201-211)", flags="i")

# ============================================================== Arrancar : masque Hollow (Visored)
fight(0.35, "visored", "hiyori", "ichigo", "D", note="Hiyori masquée affronte Ichigo, le Hollow intérieur prend le dessus et les Visored l'arrêtent (ch. 215-217)", flags="i")
fight(0.37, "visored", "ichigo", "grimmjow", "A", 1,
      note="Masque Hollow pendant onze secondes : Ichigo domine Grimmjow (ch. 229-232)", flags="i")
fight(0.3701, "visored", "grimmjow", "ichigo", "A", 2, note="Le masque se brise, Grimmjow reprend le dessus (ch. 232-236)", flags="i")
fight(0.3702, "visored", "luppi", ["rangiku", "ikkaku", "yumichika", "hitsugaya"], "A", 2,
      note="Resurrección de Luppi, ses tentacules capturent les shinigami (ch. 230-233)", flags="i")
fight(0.3703, "visored", "hitsugaya", "luppi", "A", 2, note="Hitsugaya libéré bat Luppi (ch. 234-235)")
fight(0.3704, "visored", "urahara", "yammy", "A", 1, note="Urahara tient Yammy en respect jusqu'au retrait (ch. 231-236)", flags="i")
fight(0.3705, "visored", "shinji", "grimmjow", "A", 2, note="Shinji masqué domine Grimmjow, Ulquiorra le rappelle (ch. 236-237)", flags="i")
fight(0.371, "visored", "grimmjow", "luppi", "A", 3, ta=["surprise"], note="Grimmjow, bras restauré, tue Luppi d'un Cero (ch. 240-241)")

# ============================================================== Hueco Mundo
fight(0.4, "huecomundo", "uryu", "iceringer", "A", 3, note="Uryū abat Iceringer (ch. 243-245)")
fight(0.4, "huecomundo", "chad", "demora", "A", 2, note="Chad abat Demōra (ch. 243-245)")
fight(0.401, "huecomundo", ["rukia", "renji"], "runuganga", "A", 1, note="Rukia et Renji sauvent le groupe de Runuganga (ch. 246-247)", flags="e")
fight(0.41, "huecomundo", "ichigo", "dordoni", "A", 2, ta=["retenue"],
      note="Ichigo, poussé, utilise son masque et vainc Dordoni sans le tuer (ch. 250-257)")
fight(0.4101, "huecomundo", "uryu", "cirucci", "A", 1, note="Seele Schneider, Uryū vainc Cirucci (ch. 254-259)")
fight(0.4106, "huecomundo", "chad", "gantenbainne", "A", 1, note="Chad transforme ses bras et vainc Gantenbainne (ch. 255-261)")
fight(0.412, "huecomundo", "nnoitra", "chad", "A", 3, tb=["epuise"], note="Nnoitra abat Chad d'un coup (ch. 262)")
fight(0.413, "huecomundo", "rukia", "aaroniero", "A", 1,
      note="Rukia, transpercée, plante son sabre dans la tête d'Aaroniero, qui meurt ; elle s'effondre (ch. 264-269)")
fight(0.414, "huecomundo", "ulquiorra", "ichigo", "A", 3, note="Ulquiorra, sans se libérer, perce la poitrine d'Ichigo en Bankai masqué (ch. 270-273)")
fight(0.415, "huecomundo", "grimmjow", "loly_menoly", "A", 3, note="Grimmjow écrase Loly et Menoly (ch. 274-275)")
fight(0.416, "huecomundo", "szayel", ["renji", "uryu"], "A", 1, note="Szayelaporro libéré, ses poupées vaudou paralysent Renji et Uryū (ch. 268-296)", flags="i")
fight(0.42, "huecomundo", "ichigo", "grimmjow", "A", 1, note="Revanche : Ichigo vainc Grimmjow libéré (ch. 279-286)")
fight(0.421, "huecomundo", "nnoitra", "ichigo", "A", 2, tb=["epuise"], note="Nnoitra attaque Ichigo épuisé (ch. 287-290)")
fight(0.4215, "huecomundo", "nelliel", "nnoitra", "A", 2, note="Nelliel adulte domine Nnoitra puis redevient enfant (ch. 290-296)", flags="i")
fight(0.4217, "huecomundo", "tesla", "ichigo", "A", 1, tb=["epuise"], note="Tesla libéré presque fatal à Ichigo, Kenpachi arrive (ch. 296-297)", flags="i")
fight(0.4235, "huecomundo", "byakuya", "zommari", "A", 2, note="Byakuya tue Zommari après le contrôle d'Amor sur Rukia (ch. 298-302)")
fight(0.424, "huecomundo", "unohana", "exequias", "A", 3, note="Unohana sauve Chad et Gantenbainne des Exequias (ch. 300-302)")
fight(0.424, "huecomundo", "kenpachi", "tesla", "A", 3, note="Kenpachi balaie Tesla (ch. 297-304)", flags="?")
fight(0.4246, "huecomundo", "kenpachi", "nnoitra", "A", 1, note="Kenpachi, près de la mort, achève Nnoitra au kendō à deux mains (ch. 297-312)")
fight(0.425, "huecomundo", "mayuri", "szayel", "A", 3, note="Bankai de Mayuri et drogue de surperception : Mayuri tue Szayelaporro (ch. 296-307)")
fight(0.44, "huecomundo", "ichigo", "ulquiorra", "D", note="Au sommet du dôme, échange égal (ch. 338-342)", flags="i")
fight(0.4405, "huecomundo", "ulquiorra", "ichigo", "A", 3, note="Segunda Etapa : Ulquiorra perce la poitrine d'Ichigo (ch. 343-348)")
fight(0.441, "huecomundo", "ulquiorra", "uryu", "A", 3, note="L'attaque d'Uryū échoue, Ulquiorra l'abat (ch. 347-348)")
fight(0.442, "huecomundo", "ichigo_hollow", "ulquiorra", "A", 3,
      note="Ichigo Hollow intégral arrache les membres d'Ulquiorra ; Ulquiorra meurt en ayant trouvé un cœur (ch. 348-353)")
fight(0.443, "huecomundo", ["rukia", "renji", "chad"], "rudbornn", "A", 2, note="Rukia achève Rudbornn grâce à Chad et Renji (ch. 316-355)", flags="e")
fight(0.444, "huecomundo", "yammy", ["rukia", "renji", "chad"], "A", 2, tb=["epuise"],
      note="Yammy domine le trio jusqu'à l'arrivée de Kenpachi et Byakuya (ch. 355-357)", flags="i")

# ============================================================== Faux Karakura : Espada contre capitaines
fight(0.46, "karakura", "yumichika", "charlotte", "A", 2, note="Vrai pouvoir de Ruri'iro Kujaku, dans une bulle de Charlotte (ch. 319-322)")
fight(0.4601, "karakura", "kira", "avirama", "A", 2, note="Wabisuke alourdit Avirama, Kira le tue (ch. 320-323)")
fight(0.4601, "karakura", "hisagi", "findor", "A", 2, note="Kazeshini libéré, Hisagi vainc Findor (ch. 321-324)")
fight(0.4602, "karakura", "poww", "ikkaku", "A", 2, note="Poww brise le Bankai d'Ikkaku et détruit un pilier (ch. 321-324)")
fight(0.4603, "karakura", "komamura", "poww", "A", 3, note="Bankai de Komamura, Poww écrasé d'un coup (ch. 324-325)")
fight(0.4604, "karakura", "soifon", "ggio", "A", 2, note="Suì-Fēng vainc Ggio Vega (ch. 327-332)")
fight(0.4604, "karakura", "omaeda", "nirgge", "A", 2, note="Ōmaeda assomme Nirgge (ch. 327-332)", flags="?")
fight(0.4605, "karakura", "tres_bestias", ["rangiku", "hinamori"], "D", note="Rangiku puis Hinamori contre les trois Fracciones de Harribel (ch. 333-335)", flags="i")
fight(0.4606, "karakura", "ayon", ["rangiku", "hinamori", "iba"], "A", 3, note="Ayon, invoqué par les trois Fracciones, écrase tout le monde (ch. 335-338)")
fight(0.461, "karakura", "yamamoto", "ayon", "A", 3, note="Yamamoto incinère Ayon (ch. 338-339)")
fight(0.4611, "karakura", "baraggan", "soifon", "A", 2, note="Respira de Baraggan : Suì-Fēng sacrifie son bras (ch. 351-357)")
fight(0.4612, "karakura", "harribel", "hitsugaya", "A", 1, note="Resurrección de Harribel, Hitsugaya en difficulté (ch. 335-358)", flags="i")
fight(0.4613, "karakura", "hitsugaya", "harribel", "A", 1, note="Hyōten Hyakkasō : Hitsugaya gèle Harribel, Wonderweiss la libère (ch. 358-361)", flags="i")
fight(0.4613, "karakura", ["soifon", "omaeda"], "baraggan", "A", 1, note="Bankai Jakuhō Raikōben sur Baraggan, qui survit (ch. 359-363)", flags="i")
fight(0.4614, "karakura", "stark", ["kyoraku", "ukitake"], "A", 1, ta=["surprise"],
      note="Los Lobos ; Ukitake poignardé par surprise par Wonderweiss, Kyōraku pris par un Cero (ch. 339-366)", flags="i")
fight(0.4615, "karakura", "stark", ["love", "rose"], "A", 2, note="Stark repousse Love et Rose (ch. 367-372)")
fight(0.4617, "karakura", ["hachi", "soifon"], "baraggan", "A", 2,
      note="Hachi renvoie le Respira dans le corps de Baraggan, Suì-Fēng l'achève (ch. 368-370)")
fight(0.4618, "karakura", "kyoraku", "stark", "A", 2, note="Katen Kyōkotsu, Kyōraku tue Stark quand il se met à combattre sérieusement (ch. 371-374)")
fight(0.4619, "karakura", "mashiro", "hooleer", "A", 3, note="Mashiro masquée détruit Hooleer d'un coup de pied (ch. 368-372)")
fight(0.462, "karakura", "wonderweiss", ["mashiro", "kensei"], "D", note="Kensei sauve Mashiro de Wonderweiss (ch. 371-372)", flags="i")
fight(0.4621, "karakura", "aizen", "harribel", "A", 3, ta=["surprise"], note="Aizen tranche Harribel, qu'il juge inutile (ch. 375-376)")
fight(0.4621, "karakura", "gin", "hiyori", "A", 3, ta=["surprise"], note="Gin coupe Hiyori en deux (ch. 376)")
fight(0.4622, "karakura", "aizen", "shinji", "A", 2, note="Shinji et Sakanade contre Kyōka Suigetsu, Aizen domine (ch. 377-379)")
fight(0.4623, "karakura", "tosen", ["komamura", "hisagi"], "A", 2, note="Tōsen hollowifié puis libéré domine Komamura (ch. 379-383)")
fight(0.4624, "karakura", "hisagi", "tosen", "A", 1, ta=["surprise"], note="Hisagi tranche la gorge de Tōsen avec Kazeshini (ch. 383-385)")
fight(0.4628, "karakura", ["kenpachi", "byakuya"], "yammy", "A", 2,
      note="Yammy libéré (Espada 0) contre Kenpachi et Byakuya, qui se disputent le combat ; vaincu hors champ (ch. 384-386, ch. 422)", flags="?")
fight(0.463, "karakura", "aizen", ["hitsugaya", "shinji", "lisa", "hiyori", "love", "rose", "kensei", "hachi"], "A", 3,
      note="Kyōka Suigetsu : Hitsugaya poignarde Hinamori, Aizen défait les Visored et Hitsugaya (ch. 389-392)")
fight(0.4631, "karakura", "aizen", "ichigo", "A", 3, note="Le premier coup d'Ichigo est paré à mains nues (ch. 389-390)")
fight(0.4633, "karakura", "yamamoto", "wonderweiss", "A", 3, note="Wonderweiss étouffe les flammes, Yamamoto le pulvérise à mains nues (ch. 392-394)")
fight(0.4634, "karakura", "aizen", "yamamoto", "A", 1, tb=["epuise"],
      note="Ittō Kasō : Yamamoto perd son bras, Aizen survit grâce au Hōgyoku (ch. 392-395)", flags="i")
fight(0.4636, "karakura", "aizen", "ichigo", "A", 2, note="Ichigo blesse Aizen, le Hōgyoku le régénère (ch. 395-397)")

# ============================================================== Faux Karakura : chrysalide
fight(0.464, "chrysalide", "aizen", ["isshin", "urahara", "yoruichi"], "A", 2,
      note="Première transformation ; Isshin, Urahara et Yoruichi n'en viennent pas à bout (ch. 397-403)")
fight(0.4642, "chrysalide", "gin", "ichigo", "A", 2, ta=["retenue"], note="Kamishini no Yari, Gin joue avec Ichigo (ch. 401-404)", flags="i")
fight(0.4656, "chrysalide", "aizen", ["isshin", "urahara", "yoruichi"], "A", 3, note="Chrysalide achevée, Aizen défait ses adversaires et part pour Karakura (ch. 405-406)")
fight(0.466, "chrysalide", "aizen", "gin", "A", 2, tb=["surprise"],
      note="Gin trahit, le poison de Kamishini no Yari et le vol du Hōgyoku échouent ; Aizen le tranche (ch. 412-415)")

# ============================================================== Getsuga Tenshō final
fight(0.471, "getsuga", "ichigo", "aizen", "A", 2, note="Ichigo revenu du Dangai, Aizen ne perçoit plus sa force (ch. 416-417)")
fight(0.4716, "getsuga", "ichigo", "aizen", "A", 3,
      note="Getsuga Tenshō final, Mugetsu : Aizen tranché, le Hōgyoku ne peut plus le régénérer (ch. 418-420)")
fight(0.4725, "getsuga", "urahara", "aizen", "A", 3, ta=["prepa"], tb=["epuise"],
      note="Kidō de scellement implanté par Urahara pendant le combat, le Hōgyoku rejette Aizen (ch. 420-421)")

# ============================================================== Fullbring
fight(1.85, "fullbring", "ichigo", "moe", "A", 1, note="Ichigo, sans pouvoirs, défend Keigo et Mizuiro contre Shishigawara (ch. 424-426)", flags="?")
fight(1.925, "fullbring", "ichigo", "jackie", "A", 1, note="Bringer Light : Ichigo renverse Jackie puis perd le contrôle (ch. 442-447)", flags="i")
fight(1.93, "fullbring", "tsukishima", "ichigo", "A", 2, note="Tsukishima domine Ichigo, Ginjō le retient (ch. 448-450)", flags="i")
fight(1.946, "fullbring", "ginjo", "ichigo", "D", ta=["retenue"], note="Fullbring complet en combat d'entraînement, Ginjō arrête le duel (ch. 451-455)", flags="i")
fight(1.95, "fullbring", "ginjo", "ichigo", "A", 3, ta=["surprise"], note="Trahison : Ginjō abat Ichigo et lui prend son Fullbring (ch. 456-458)")

# ============================================================== Fullbring : pouvoirs restaurés
fight(1.958, "restauration", ["urahara", "isshin"], ["chad", "orihime"], "A", 3, ta=["retenue"],
      note="Urahara et Isshin assomment Chad et Orihime pour les protéger (ch. 461-462)", flags="?")
fight(1.959, "restauration", "ikkaku", "moe", "A", 3, note="Un coup de tête d'Ikkaku (ch. 465-466)")
fight(1.96, "restauration", "kenpachi", "giriko", "A", 3, note="Kenpachi tue Giriko d'un coup (ch. 466-467)")
fight(1.961, "restauration", "renji", "jackie", "A", 2, note="Renji vainc Jackie (ch. 467-468)")
fight(1.962, "restauration", "hitsugaya", "yukio", "A", 2, note="Hitsugaya déjoue le jeu de Yukio (ch. 469-471)")
fight(1.963, "restauration", "rukia", "riruka", "D", note="Riruka enferme Rukia dans une poupée, puis cède (ch. 469-473)", flags="i")
fight(1.964, "restauration", "byakuya", "tsukishima", "A", 1, note="Tsukishima blesse gravement Byakuya, qui le blesse mortellement (ch. 469-474)")
fight(1.97, "restauration", "ichigo", "ginjo", "A", 2, note="Ichigo restauré bat Ginjō en Bankai-Fullbring et le tue (ch. 460-477)")
