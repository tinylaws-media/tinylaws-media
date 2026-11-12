# Partie 2 : après l'ellipse, du retour à Sabaody jusqu'à la fin de Wano (t de 2.0 à 2.45).
# Manga uniquement. Chapitres vérifiés (One Piece Wiki / résumés de chapitres) ; "?" = source introuvable ou contradictoire.
# fight() est injectée par data.py.

CHARS_PART = {
    # ---- Équipage du Chapeau de paille (tier = statut au tout premier combat de l'histoire)
    "luffy": ("Monkey D. Luffy", "Chapeau de paille", 1.5, None, None),
    "zoro": ("Roronoa Zoro", "Chapeau de paille", 1.5, None, None),
    "nami": ("Nami", "Chapeau de paille", 0.8, None, None),
    "usopp": ("Usopp", "Chapeau de paille", 0.8, None, None),
    "sanji": ("Sanji", "Chapeau de paille", 1.5, None, None),
    "chopper": ("Tony Tony Chopper", "Chapeau de paille", 1.0, None, None),
    "robin": ("Nico Robin", "Chapeau de paille", 2.5, None, None),
    "franky": ("Franky", "Chapeau de paille", 2.5, None, None),
    "brook": ("Brook", "Chapeau de paille", 3.0, None, None),
    "jinbe": ("Jinbe", "Chapeau de paille", 4.0, None, None),
    # ---- Retour à Sabaody
    "pacifista": ("Pacifista (unité)", "Marine", 4.0, None, None),
    "sentomaru": ("Sentomaru", "Marine", 4.0, None, None),
    "demaro_black": ("Demaro Black (faux Luffy)", "Faux Chapeaux de paille", 1.0, None, None),
    "caribou": ("Caribou", "Pirates de Caribou", 3.0, None, None),
    # ---- Île des Hommes-Poissons
    "kraken": ("Surume (Kraken)", "Créature marine", 3.5, None, None),
    "hammond": ("Hammond", "Nouveaux Hommes-Poissons", 2.5, None, None),
    "wadatsumi": ("Wadatsumi", "Nouveaux Hommes-Poissons", 3.0, None, None),
    "neptune": ("Roi Neptune", "Royaume Ryugu", 4.0, None, None),
    "hody": ("Hody Jones", "Nouveaux Hommes-Poissons", 3.5, None, None),
    "vander_decken": ("Vander Decken IX", "Pirates du Hollandais volant", 3.0, None, None),
    "fukaboshi": ("Fukaboshi", "Royaume Ryugu", 3.5, None, None),
    "dosun": ("Dosun", "Nouveaux Hommes-Poissons", 3.0, None, None),
    "zeo": ("Zeo", "Nouveaux Hommes-Poissons", 3.0, None, None),
    "daruma": ("Daruma", "Nouveaux Hommes-Poissons", 3.0, None, None),
    "ikaros_much": ("Ikaros Much", "Nouveaux Hommes-Poissons", 3.0, None, None),
    "hyozo": ("Hyozo", "Nouveaux Hommes-Poissons", 3.0, None, None),
    # ---- Punk Hazard
    "punk_dragon": ("Dragon de Punk Hazard", "Créature", 3.0, None, None),
    "brownbeard": ("Barbe Brune", "Centaures de Caesar", 2.5, None, None),
    "law": ("Trafalgar Law", "Pirates du Heart", 4.0, None, None),
    "smoker": ("Smoker", "Marine", 3.0, None, None),
    "tashigi": ("Tashigi", "Marine", 2.0, None, None),
    "rock": ("Rock (frères Yéti Cool)", "Mercenaires", 3.5, None, None),
    "scotch": ("Scotch (frères Yéti Cool)", "Mercenaires", 3.5, None, None),
    "caesar": ("Caesar Clown", "Donquixote (allié)", 4.5, None, None),
    "monet": ("Monet", "Famille Donquixote", 4.0, 2.215, None),
    "vergo": ("Vergo", "Famille Donquixote", 5.0, None, None),
    "baby_5": ("Baby 5", "Famille Donquixote", 3.5, None, None),
    "buffalo": ("Buffalo", "Famille Donquixote", 3.5, None, None),
    "doflamingo": ("Donquixote Doflamingo", "Famille Donquixote", 4.5, None, None),
    "aokiji": ("Kuzan (Aokiji)", "Marine", 6.0, None, None),
    # ---- Dressrosa
    "fujitora": ("Issho (Fujitora)", "Marine", 6.0, None, None),
    "bartolomeo": ("Bartolomeo", "Pirates du Barto Club", 4.5, None, None),
    "elizabello": ("Elizabello II", "Royaume de Prodence", 4.5, None, None),
    "hajrudin": ("Hajrudin", "Pirates des Géants", 4.0, None, None),
    "chinjao": ("Don Chinjao", "Famille Chinjao", 4.5, None, None),
    "burgess": ("Jesus Burgess", "Pirates de Barbe Noire", 4.0, None, None),
    "cavendish": ("Cavendish (Hakuba)", "Pirates du Beautiful", 4.0, None, None),   # rookie à 280 M, niveau Supernova, pas un commandant d'Empereur
    "rebecca": ("Rebecca", "Royaume de Dressrosa", 3.0, None, None),
    "suleiman": ("Suleiman", "Gladiateur", 4.0, None, None),
    "sabo": ("Sabo", "Armée révolutionnaire", 1.0, None, None),
    "diamante": ("Diamante", "Famille Donquixote", 5.0, None, None),
    "sugar": ("Sugar", "Famille Donquixote", 3.0, None, None),
    "trebol": ("Trebol", "Famille Donquixote", 5.0, None, None),
    "kyros": ("Kyros", "Royaume de Dressrosa", 5.0, None, None),
    "bellamy": ("Bellamy", "Pirates de Bellamy", 3.0, None, None),
    "dellinger": ("Dellinger", "Famille Donquixote", 4.0, None, None),
    "viola": ("Viola", "Royaume de Dressrosa", 2.5, None, None),
    "senor_pink": ("Señor Pink", "Famille Donquixote", 4.5, None, None),
    "pica": ("Pica", "Famille Donquixote", 5.0, None, None),
    "gladius": ("Gladius", "Famille Donquixote", 4.0, None, None),
    "lao_g": ("Lao G", "Famille Donquixote", 4.5, None, None),
    "sai": ("Sai", "Flotte de Happo", 4.5, None, None),
    "machvise": ("Machvise", "Famille Donquixote", 4.0, None, None),
    "leo": ("Leo", "Tontatta", 2.5, None, None),
    "giolla": ("Giolla", "Famille Donquixote", 3.5, None, None),
    # ---- Zou
    "jack": ("Jack", "Pirates aux Cent Bêtes", 5.5, None, None),
    "inuarashi": ("Inuarashi", "Minks / Fourreaux rouges", 3.0, None, None),   # 1er nœud = mousse adolescent de Roger (t = -24, ch. 967)
    "nekomamushi": ("Nekomamushi", "Minks / Fourreaux rouges", 3.0, None, None),   # 1er nœud = mousse adolescent de Roger (t = -24, ch. 967)
    "zunesha": ("Zunesha", "Éléphant géant", 6.5, None, None),
    # ---- Whole Cake Island
    "urouge": ("Urouge", "Pirates du Moine fou", 4.0, None, None),
    "snack": ("Charlotte Snack", "Pirates de Big Mom", 5.0, None, None),
    "cracker": ("Charlotte Cracker", "Pirates de Big Mom", 5.5, None, None),
    "niji": ("Vinsmoke Niji", "Germa 66", 4.0, None, None),
    "ichiji": ("Vinsmoke Ichiji", "Germa 66", 4.5, None, None),
    "yonji": ("Vinsmoke Yonji", "Germa 66", 4.0, None, None),
    "judge": ("Vinsmoke Judge", "Germa 66", 4.5, None, None),
    "big_mom": ("Charlotte Linlin (Big Mom)", "Pirates de Big Mom", 7.0, None, None),
    "pedro": ("Pedro", "Minks / Pirates du Nox", 4.5, 2.36, None),   # prime 382 M, battu par Perospero (ch. 877-878)
    "tamago": ("Baron Tamago", "Pirates de Big Mom", 4.5, None, None),
    "perospero": ("Charlotte Perospero", "Pirates de Big Mom", 5.0, None, None),
    "bege": ("Capone Bege", "Pirates de Fire Tank", 5.0, None, None),
    "katakuri": ("Charlotte Katakuri", "Pirates de Big Mom", 6.0, None, None),
    "carrot": ("Carrot", "Minks", 3.0, None, None),
    "brulee": ("Charlotte Brûlée", "Pirates de Big Mom", 3.5, None, None),
    "wanda": ("Wanda", "Minks", 3.5, None, None),
    "zeus": ("Zeus (nuage homie)", "Homie", 4.0, None, None),
    # ---- Rêverie
    "ryokugyu": ("Aramaki (Ryokugyu)", "Marine", 6.0, None, None),
    # ---- Wano
    "hawkins": ("Basil Hawkins", "Pirates de Hawkins", 4.0, None, None),
    "urashima": ("Urashima", "Wano (sumo)", 3.0, None, None),
    "holdem": ("Holdem", "Pirates aux Cent Bêtes", 4.5, None, None),
    "kaido": ("Kaido", "Pirates aux Cent Bêtes", 7.0, None, None),
    "kid": ("Eustass Kid", "Pirates de Kid", 4.0, None, None),
    "killer": ("Killer", "Pirates de Kid", 4.0, None, None),
    "page_one": ("Page One", "Pirates aux Cent Bêtes", 4.5, None, None),
    "babanuki": ("Babanuki", "Pirates aux Cent Bêtes", 4.5, None, None),
    "queen": ("Queen", "Pirates aux Cent Bêtes", 6.0, None, None),
    "hyogoro": ("Hyogoro", "Wano", 4.5, None, None),
    "gyukimaru": ("Gyukimaru", "Wano (bandit)", 4.0, None, None),
    "ashura_doji": ("Ashura Doji", "Fourreaux rouges", 5.0, 2.4445, None),
    "ulti": ("Ulti", "Pirates aux Cent Bêtes", 5.0, None, None),
    "yamato": ("Yamato", "Pirates aux Cent Bêtes", 5.5, None, None),   # fille de Kaido, sans titre officiel ; ne fait que retarder Kaido (ch. 1018-1026)
    "kinemon": ("Kin'emon", "Fourreaux rouges", 4.0, None, None),
    "kiku": ("Kikunojo", "Fourreaux rouges", 5.0, None, None),
    "kawamatsu": ("Kawamatsu", "Fourreaux rouges", 5.0, None, None),
    "denjiro": ("Denjiro", "Fourreaux rouges", 5.0, None, None),
    "raizo": ("Raizo", "Fourreaux rouges", 5.0, None, None),
    "kanjuro": ("Kanjuro", "Fourreaux rouges (traître)", 4.5, 2.4406, None),
    "marco": ("Marco", "Pirates de Barbe Blanche", 5.0, None, None),
    "king": ("King", "Pirates aux Cent Bêtes", 6.0, None, None),
    "black_maria": ("Black Maria", "Pirates aux Cent Bêtes", 5.0, None, None),
    "sasaki": ("Sasaki", "Pirates aux Cent Bêtes", 5.0, None, None),
    "who_s_who": ("Who's-Who", "Pirates aux Cent Bêtes", 5.0, None, None),
    "fukurokuju": ("Fukurokuju", "Oniwabanshu", 4.5, None, None),
    "izo": ("Izo", "Pirates de Barbe Blanche", 5.0, 2.4472, None),
    "maha": ("Maha", "CP0", 5.0, None, None),
    "guernica": ("Guernica", "CP0", 5.0, None, None),
    "orochi": ("Kurozumi Orochi", "Shogunat de Wano", 3.0, 2.4498, None),
}

GENERIC_PART = {"pacifista"}

JUMPS_PART = [
    # entraînement de l'ellipse (deux ans), placé à t = 1.5
    ("luffy", 1.5, 1.5, 0.8, "Ellipse : Haki avec Rayleigh (Rusukaina)"),
    ("zoro", 1.5, 1.5, 0.8, "Ellipse : entraînement avec Mihawk"),
    ("sanji", 1.5, 1.2, 0.8, "Ellipse : Kamabakka, Haki, Sky Walk"),
    ("nami", 1.5, 0.8, 0.6, "Ellipse : Weatheria, Sorcery Clima-Tact"),
    ("usopp", 1.5, 1.0, 0.6, "Ellipse : Boin, Pop Greens"),
    ("chopper", 1.5, 1.0, 0.6, "Ellipse : Torino, contrôle du Monster Point"),
    ("robin", 1.5, 0.8, 0.6, "Ellipse : Tequila Wolf / Armée révolutionnaire"),
    ("koby", 1.5, 1.0, 0.6, "Ellipse : entraînement avec Garp, promu capitaine, « Héros Koby » (ch. 905, 1080)"),
    ("franky", 1.5, 1.0, 0.6, "Ellipse : Baldimore, nouveau corps"),
    ("brook", 1.5, 1.0, 0.6, "Ellipse : maîtrise de l'âme (Yomi Yomi)"),
    # Dressrosa
    ("sabo", 2.255, 1.0, 0.7, "Mange le Mera Mera no Mi (ch. 744)"),
    ("usopp", 2.2741, 0.4, 0.4, "Éveil du Haki de l'observation (ch. 777)"),
    ("luffy", 2.2785, 1.0, 0.7, "Gear 4 (ch. 784)"),
    # Whole Cake Island
    ("luffy", 2.364, 0.4, 0.4, "Observation du futur apprise contre Katakuri (ch. 893-896)"),
    ("nami", 2.36455, 0.5, 0.4, "Zeus asservi au Clima-Tact (ch. 890), partenaire de Nami à Onigashima (ch. 1018)"),
    # Wano
    ("luffy", 2.4165, 0.5, 0.5, "Ryuo / Haki émis appris à Udon (ch. 939-948)"),
    ("zoro", 2.42, 0.3, 0.4, "Obtient Enma (ch. 955)"),
    ("luffy", 2.4399, 0.5, 0.5, "Haki des rois imprégné, découvert pendant le duel du toit contre Kaido (ch. 1010-1015) ; daté 2.4435 avant l'audit vidéo, le combat portait un tag haki_roi à la place"),
    ("robin", 2.4439, 0.4, 0.4, "Demonio Fleur (ch. 1021-1022)"),
    ("sanji", 2.4459, 0.8, 0.6, "Éveil du corps modifié Germa (ch. 1031-1034)"),
    ("zoro", 2.4461, 0.8, 0.6, "Haki des rois éveillé et imprégné (ch. 1033-1035)"),
    ("law", 2.4471, 0.8, 0.6, "Éveil de l'Ope Ope no Mi (ch. 1039-1042)"),
    ("kid", 2.4471, 0.8, 0.6, "Éveil du Jiki Jiki no Mi (ch. 1039-1042)"),
    ("luffy", 2.4495, 1.0, 0.8, "Gear 5 / éveil du Gomu Gomu (Hito Hito modèle Nika) acquis (ch. 1044)"),
]

# ============================================================== retour à Sabaody (ch. 598-603)
fight(2.0, "fishman", "sentomaru", "demaro_black", "A", 3, note="Sentomaru écrase le faux Luffy du plat de sa hache (ch. 601)")
fight(2.001, "fishman", "luffy", "pacifista", "A", 3, note="Luffy détruit le PX-5 d'un seul Jet Pistol imprégné de Haki (ch. 601)")
fight(2.002, "fishman", ["zoro", "sanji"], "pacifista", "A", 3, note="Zoro et Sanji détruisent ensemble un autre Pacifista (ch. 601)")
fight(2.01, "fishman", ["franky", "sanji"], "caribou", "A", 3, tb=["retenue"],
      note="Caribou, monté à bord, se laisse frapper par Franky et Sanji pour cacher son Logia, ligoté (ch. 604) puis scellé dans un tonneau par Franky (ch. 606)")

# ============================================================== Île des Hommes-Poissons (ch. 603-653)
fight(2.1, "fishman", ["luffy", "zoro", "sanji"], "kraken", "A", 3,
      note="Le Kraken assommé par l'Elephant Gun imprégné de Luffy, puis apprivoisé (ch. 605)")
fight(2.1005, "fishman", "kraken", "wadatsumi", "A", 3, note="Surume, désormais à Luffy, assomme Wadatsumi (ch. 606)")
fight(2.105, "fishman", "luffy", "hammond", "A", 3, note="Luffy balaie le filet et met Hammond et ses hommes K.O. au Jet Pistol (ch. 609)")
fight(2.11, "fishman", ["zoro", "nami", "usopp", "brook"], "neptune", "A", 2, tb=["malade"],
      note="Zoro bloque le trident de Neptune (ch. 613) ; le roi et sa garde ligotés (ch. 614) ; Neptune souffre du dos")
fight(2.1105, "fishman", "luffy", "vander_decken", "A", 2, note="Luffy fait chuter Decken puis Jet Hammer, tête dans le sol (ch. 618)")
fight(2.111, "fishman", "zoro", "hody", "A", 2, note="Zoro tranche Hody sous l'eau d'un seul coup (ch. 618-619)")
fight(2.112, "fishman", "hody", "neptune", "A", 2, ta=["boost"], tb=["malade", "protege"],
      note="Hody, ranimé par une pilule d'Énergie Stéroïde, rattrape Neptune (dos bloqué après Ultramarine, protège ses gardes) ; Zoro, à court d'air, Usopp et Brook capturés (ch. 617-619)")
fight(2.118, "fishman", "luffy", "jinbe", "D", note="Dispute au Sea Forest, Robin s'interpose (ch. 628-629)", flags="i")
fight(2.129, "fishman", "fukaboshi", "dosun", "A", 2, note="Fukaboshi frappe Dosun (ch. 620) et l'enchaîne ; Dosun se libère ensuite au stéroïde (ch. 630)")
fight(2.13, "fishman", ["dosun", "zeo", "daruma", "ikaros_much", "hyozo"], "fukaboshi", "A", 2, ta=["boost"],
      note="Les trois princes, après avoir battu les monstres marins, défaits par les officiers dopés (ch. 631-632)")
fight(2.14, "fishman", "hody", "vander_decken", "A", 3, ta=["surprise"], note="Hody transperce son allié Decken de son trident à bord de l'Arche (ch. 638)")
fight(2.1405, "fishman", "robin", "hammond", "A", 3, note="Hammond tente de la prendre au filet, Robin lui brise le dos (ch. 643)")
fight(2.141, "fishman", "luffy", "hody", "A", 3, tb=["boost"], note="Red Hawk puis Elephant Gatling ; Hody avale des pilules d'Énergie Stéroïde (ch. 645)")
fight(2.142, "fishman", "chopper", "dosun", "A", 2, tb=["boost"], note="Monster Point contrôlé, Kokutei Palme (ch. 646)")
fight(2.1421, "fishman", "usopp", "daruma", "A", 2, tb=["boost"], note="Impact Wolf (ch. 646)")
fight(2.1422, "fishman", "franky", "ikaros_much", "A", 2, tb=["boost"], note="Radical Beam (ch. 646)")
fight(2.1423, "fishman", "brook", "zeo", "A", 2, tb=["boost"], note="Chant du blizzard (ch. 646)")
fight(2.1424, "fishman", ["jinbe", "sanji"], "wadatsumi", "A", 2, note="Buraikan puis Hell Memories (ch. 646)")
fight(2.1425, "fishman", "zoro", "hyozo", "A", 3, tb=["boost"], note="Rengoku Oni Giri (ch. 646)")

# ============================================================== Punk Hazard (ch. 654-699)
fight(2.2, "punkhazard", ["luffy", "zoro", "usopp", "robin"], "punk_dragon", "A", 3, note="Zoro tue le dragon d'un seul coup (ch. 656)")
fight(2.201, "punkhazard", ["luffy", "zoro", "usopp", "robin", "brook"], "brownbeard", "A", 3,
      note="Brook retourne les bazookas gelés ; centaures battus, Barbe Brune contraint de les porter (ch. 661-662)")
fight(2.203, "punkhazard", "law", "smoker", "A", 2, note="Law arrache le cœur de Smoker avec Mes (ch. 661-662), puis échange les corps (ch. 663)")
fight(2.204, "punkhazard", "law", "tashigi", "A", 3, note="Law coupe Tashigi et son sabre en deux sans la tuer (ch. 661)")
fight(2.206, "punkhazard", ["scotch", "rock"], ["zoro", "sanji", "brook"], "A", 2, ta=["surprise"],
      note="Les frères Yéti Cool les abattent aux balles de gaz KYP (ch. 665, montré en flash-back ch. 669) ; Sanji dans le corps de Nami")
fight(2.207, "punkhazard", ["luffy", "franky"], "rock", "A", 3,
      note="Luffy renvoie les balles, Franky (dans le corps de Chopper) lui jette un bloc de montagne, Elephant Gun (ch. 667)")
fight(2.2071, "punkhazard", "law", "scotch", "A", 3, note="Law le tranche en deux puis Counter Shock (ch. 667)")
fight(2.208, "punkhazard", "caesar", ["franky", "robin", "smoker", "tashigi"], "A", 2, ta=["prepa"],
      note="Caesar les met à terre sans contact puis les fait enchaîner au granit marin (ch. 672)")
fight(2.209, "punkhazard", "caesar", "luffy", "A", 2, ta=["prepa"],
      note="Luffy le touche au Haki mais s'effondre, privé d'oxygène ; capturé (ch. 670-672)")
fight(2.21, "punkhazard", "vergo", "law", "A", 3, tb=["malade"],
      note="Vergo assomme Law en quelques secondes au bambou imprégné ; Law a échangé son cœur (ch. 672)")
fight(2.2105, "punkhazard", "vergo", "tashigi", "A", 3, note="Vergo bloque son sabre et l'écrase au sol (ch. 680)")
fight(2.2106, "punkhazard", "vergo", "sanji", "D", tb=["retenue"],
      note="Vergo fêle la jambe de Sanji puis abandonne le combat (ch. 680-682)", flags="i")
fight(2.2108, "punkhazard", "vergo", "law", "A", 2, tb=["malade"], note="Vergo serre le cœur de Law et le roue de coups (ch. 683)")
fight(2.212, "punkhazard", ["zoro", "nami", "robin", "tashigi"], "monet", "A", 1,
      note="Heat Ball, Quatro Mano, puis Tashigi blesse au Haki l'aile de Monet, qui se replie (ch. 685-686)", flags="i")
fight(2.213, "punkhazard", ["zoro", "tashigi"], "monet", "A", 3, note="Zoro la tranche en deux, Tashigi l'arrête quand elle revient (ch. 687)")
fight(2.2141, "punkhazard", "vergo", "smoker", "A", 2, tb=["retenue"],
      note="Smoker gagne du temps pour que Law récupère son cœur ; Vergo brise son jitte (ch. 683-690)")
fight(2.2145, "punkhazard", "law", "vergo", "A", 3, note="Law tranche Vergo, le laboratoire et la montagne (ch. 690-691)")
fight(2.215, "punkhazard", "luffy", "caesar", "A", 3, note="Poings au visage puis Gomu Gomu no Grizzly Magnum (ch. 689-692)")
fight(2.218, "punkhazard", "franky", ["baby_5", "buffalo"], "D", note="Ils percent l'armure du General Franky, General Cannon sans effet décisif (ch. 694-695)", flags="i")
fight(2.2181, "punkhazard", ["nami", "usopp"], ["baby_5", "buffalo"], "A", 2,
      note="Thunder Breed Tempo de Nami puis Hissatsu Ryusei-gun d'Usopp, menottes en granit marin sur Caesar (ch. 695)")
fight(2.2182, "punkhazard", "law", ["baby_5", "buffalo"], "A", 3, tb=["epuise"],
      note="Hors champ : Law leur a séparé la tête du corps, retrouvés sur un canot (ch. 697)")
fight(2.2185, "punkhazard", "doflamingo", "smoker", "A", 3, tb=["epuise"], note="Doflamingo blesse gravement Smoker, Kuzan l'arrête (ch. 698)")
fight(2.219, "punkhazard", "aokiji", "doflamingo", "D", ta=["retenue"], tb=["retenue"],
      note="Kuzan gèle Doflamingo, qui se libère et se retire (ch. 698-699)", flags="i")

# ============================================================== Dressrosa (ch. 700-801)
fight(2.232, "punkhazard", "bartolomeo", "elizabello", "A", 2, note="Bloc B : la barrière résiste au King Punch, Bartolomeo met le roi K.O. (ch. 709)")
fight(2.233, "punkhazard", "luffy", "hajrudin", "A", 3, note="Bloc C, un seul coup de poing au visage (ch. 714)")
fight(2.234, "punkhazard", "luffy", "chinjao", "A", 3, note="Bloc C, Thor Elephant Gun (ch. 718-719)")
fight(2.237, "punkhazard", "doflamingo", "law", "A", 2, note="Green Bit puis le pont : Law capturé et blessé par balles (ch. 722-730)")
fight(2.2368, "punkhazard", "fujitora", "law", "A", 2,
      note="Green Bit : Fujitora plaque Law au sol par la gravité, Law s'échappe avec Caesar avant l'arrivée de Doflamingo (ch. 722-723) ; ajouté à l'audit vidéo", flags="i")
fight(2.2378, "punkhazard", "fujitora", "zoro", "A", 2,
      note="Zoro vise Doflamingo, Fujitora s'interpose, l'enfonce dans le sol et repousse son tranchant volant (ch. 729-730) ; ajouté à l'audit vidéo", flags="i")
fight(2.2375, "punkhazard", "doflamingo", "sanji", "A", 2, note="Sanji immobilisé, Law le téléporte (ch. 723-724)", flags="i")
fight(2.24, "punkhazard", "cavendish", "suleiman", "A", 3, ta=["surprise"],
      note="Bloc D : Hakuba, réveillé, fauche tous les combattants sauf Rebecca (ch. 734)")
fight(2.2401, "punkhazard", "rebecca", "suleiman", "D", note="Bloc D, interrompu par Hakuba ; Rebecca, seule à esquiver, gagne le bloc (ch. 734)", flags="i")
fight(2.245, "punkhazard", "trebol", "usopp", "A", 2, note="Usopp coupe Trebol en deux (Platanus Shuriken) mais Trebol le prend dans sa glu (ch. 741-742)")
fight(2.246, "punkhazard", "usopp", "sugar", "A", 3, ta=["surprise"], note="Sugar s'évanouit de peur (Tatababasco) (ch. 742)")
fight(2.2465, "punkhazard", "sabo", ["diamante", "burgess", "bartolomeo", "rebecca"], "D",
      note="Finale de la Corrida : Sabo tient Burgess, détruit l'arène et prend le Mera Mera (ch. 741-744)", flags="i")
fight(2.247, "punkhazard", "diamante", "rebecca", "A", 2, note="Coup de masse en finale, Bartolomeo la protège (ch. 742)", flags="i")
fight(2.2585, "punkhazard", "sabo", "fujitora", "D",
      note="Sabo bloque les Marines (ch. 750) ; duel acharné, Fujitora finit par partir parier sur Luffy (ch. 751-760)", flags="i")
fight(2.259, "punkhazard", "usopp", "sugar", "A", 3, ta=["surprise"], note="Tir depuis le plateau portant le dessin de son visage terrifiant (ch. 758)")
fight(2.262, "punkhazard", "doflamingo", "viola", "A", 3, note="Viola immobilisée (chapitre non retrouvé)", flags="?")
fight(2.2621, "punkhazard", "doflamingo", "bellamy", "A", 3, tb=["epuise"],
      note="Bellamy affronte Doflamingo sur le toit (ch. 753), retrouvé à terre (ch. 758), servi de bouclier puis de pantin (ch. 759-761)")
fight(2.263, "punkhazard", "doflamingo", ["luffy", "law"], "D", tb=["protege"],
      note="Combat au palais, Law perd un bras (ch. 769) ; Luffy place un Red Hawk (ch. 759-769)", flags="i")
fight(2.2695, "punkhazard", "hajrudin", "machvise", "A", 2, tb=[], note="Hajrudin, blessé, l'envoie dans la Cage puis s'effondre (ch. 770)")
fight(2.27, "punkhazard", "lao_g", "chinjao", "A", 2, ta=["surprise"], note="Lao G frappe Chinjao, tête déjà pliée par Sai (ch. 771)")
fight(2.2701, "punkhazard", "sai", "lao_g", "A", 2, note="Kiryu Kirikugi imprégné de Haki (ch. 771)")
fight(2.2705, "punkhazard", "cavendish", "dellinger", "A", 3, ta=["surprise"], tb=["epuise"], note="Hakuba fauche Dellinger et les gardes du 3e niveau (ch. 773) ; Ideo l'avait touché (ch. 770)")
fight(2.2708, "punkhazard", "leo", "giolla", "A", 2, note="Haute Couture: Patchwork, Mansherry libérée (ch. 774)")
fight(2.2715, "punkhazard", "franky", "senor_pink", "A", 1, note="Usine SMILE, commencé ch. 732, Franky Iron Boxing (ch. 775)")
fight(2.272, "punkhazard", "kyros", "diamante", "A", 2, note="Champ de fleurs, sur la tombe de Scarlett (ch. 776)")
fight(2.274, "punkhazard", "zoro", "pica", "A", 2, note="Sanzen Sekai (ch. 777)")
fight(2.2741, "punkhazard", "bartolomeo", "gladius", "A", 2, note="Poing de barrière (ch. 777)")
fight(2.2742, "punkhazard", "usopp", "sugar", "A", 3, ta=["surprise"], note="Tir à 4 km, Haki de l'observation (ch. 777)")
fight(2.2765, "punkhazard", "luffy", "bellamy", "A", 2, tb=["epuise"],
      note="Libéré des fils, Bellamy choisit un dernier combat ; Gear 2 imprégné (ch. 769-779)")
fight(2.277, "punkhazard", "law", "trebol", "A", 2, ta=["epuise"], note="Sterben ; Trebol tente de l'emporter dans une explosion (ch. 782)")
fight(2.278, "punkhazard", "doflamingo", "law", "A", 2, tb=["epuise"], note="Gamma Knife ne suffit pas, Doflamingo se soigne (ch. 781-782)")
fight(2.279, "gear4", "luffy", "doflamingo", "A", 1, tb=["epuise"],
      note="Gear 4 ; Luffy à court de temps, puis King Kong Gun (ch. 783-790)")
fight(2.286, "gear4", "sabo", "burgess", "A", 2, note="Griffe du roi dragon (ch. 787), puis Burgess, qui le provoque au sujet d'Ace, brûlé à bout portant (ch. 792)")
fight(2.287, "gear4", "luffy", "fujitora", "D", tb=["retenue"],
      note="Au port, Luffy annonce ses coups ; Fujitora le projette par la gravité puis laisse filer la flotte (ch. 799)", flags="i")

# ============================================================== Zou (ch. 802-824)
fight(2.29, "wci", "jack", ["inuarashi", "nekomamushi"], "A", 1, ta=["prepa"],
      note="Invasion de Zou : cinq jours de combat jour/nuit, Jack l'emporte avec le gaz Koro de Caesar (ch. 808-810, récit)")
fight(2.31, "wci", "zunesha", "jack", "A", 3, note="Sur l'ordre de Momonosuke, un coup de trompe coule la flotte de Jack (ch. 821)")

# ============================================================== Whole Cake Island (ch. 825-902)
fight(2.311, "wci", "urouge", "snack", "A", 2, note="Avant l'histoire : Urouge bat un Sweet Commander (Snack), récit de Brûlée (ch. 837)")
fight(2.3112, "wci", "cracker", "urouge", "A", 2, note="Avant l'histoire : Cracker bat ensuite Urouge, qui s'enfuit (ch. 837, récit)")
fight(2.315, "wci", "sanji", "yonji", "A", 2, note="Hors champ, Sanji enfonce le visage de Yonji (ch. 832-833, récit)")
fight(2.322, "wci", "judge", "sanji", "A", 2, ta=["prepa"], tb=["protege"],
      note="Judge sacrifie un soldat, lance électrique ; Sanji porte les bracelets explosifs (ch. 832-833)")
fight(2.33, "wci", "luffy", "cracker", "A", 2, ta=["epuise"], tb=["epuise"],
      note="Onze heures de combat, Gear 4 puis Tankman (ch. 835-843)")
fight(2.3305, "wci", "nami", "brulee", "A", 2, note="Pound la fait lâcher, Thunderbolt Tempo ; Brûlée fuit dans le Mirro-World (ch. 837)")
fight(2.3315, "wci", "niji", "sanji", "A", 2, tb=["protege"],
      note="Sanji frappe Niji pour Cosette, Ichiji menace Zeff ; Niji le roue d'attaques électriques (ch. 840)")
fight(2.332, "wci", ["carrot", "chopper"], "brulee", "A", 2, ta=["surprise"],
      note="Carrot renverse la marmite bouillante sur Brûlée, Chopper se libère ; Brûlée capturée (ch. 849)")
fight(2.335, "wci", "big_mom", "brook", "A", 3, note="Brook, surpris dans la salle des ponéglyphes, vaincu par Big Mom qui ne peut pourtant pas prendre son âme (ch. 849-850)")
fight(2.336, "wci", "pedro", "tamago", "A", 2, note="Pedro coupe Tamago puis Hiyoko et se fait sauter, sauvé par le Mirro-World (ch. 850-853)")
fight(2.34, "wci", "sanji", "luffy", "A", 3, tb=["retenue", "epuise"], note="Luffy refuse de riposter (ch. 856)")
fight(2.35, "wci", "big_mom", "bege", "A", 2, tb=["prepa"], note="Le cri de Big Mom ruine l'assassinat et les KX Launchers (ch. 865-868)")
fight(2.351, "wci", "katakuri", "ichiji", "A", 3, note="Katakuri domine Ichiji, arrêté par l'effondrement du château (ch. 871)", flags="i")
fight(2.36, "wci", "perospero", "pedro", "A", 1, tb=["protege"],
      note="Pedro maîtrisé par Perospero se fait exploser pour libérer le Sunny ; Perospero survit, perd un bras (ch. 877-878)")
fight(2.3645, "wci", "luffy", "katakuri", "A", 1, ta=["epuise"], tb=["epuise"],
      note="Monde des miroirs, Luffy apprend l'observation du futur (ch. 882-896)")
fight(2.3646, "wci", ["jinbe", "nami", "brook", "zeus"], "big_mom", "D", tb=["malade"],
      note="Big Mom, folle de faim, sur le Sunny : Jinbe la fait tomber et l'arrose, Brook coupe Zeus, Nami l'électrocute (ch. 890)", flags="i")

# ============================================================== Rêverie (ch. 903-908, conséquences ch. 956)
# retiré : « Sabo contre Fujitora et Ryokugyu à la Rêverie » : ce sont les commandants révolutionnaires qui affrontent
# les deux amiraux (ch. 956), Sabo n'y est pas montré au combat.

# ============================================================== Wano acte 1 (ch. 909-924)
fight(2.4, "wano", "hawkins", ["luffy", "zoro"], "D", ta=["prepa"], note="Les coups renvoyés sur ses hommes ; Komachiyo emporte Luffy et Zoro (ch. 912-913)", flags="i")
fight(2.401, "wano", "luffy", "urashima", "A", 3, note="Gear 3 Harite (ch. 916)")
fight(2.402, "wano", "kiku", "urashima", "A", 3, note="Kiku lui tranche le chignon (ch. 916)")
fight(2.403, "wano", "luffy", "holdem", "A", 2, note="Red Hawk à Bakura (ch. 917)")
fight(2.404, "wano", "law", "hawkins", "D", note="Bref heurt à Bakura, Hawkins démasque Law, blessures renvoyées sur ses hommes (ch. 918)", flags="i")
fight(2.405, "wano", "kaido", "luffy", "A", 3, note="Ruines du château d'Oden, Raimei Hakke (ch. 923-924)")
fight(2.406, "wano", "kaido", "kid", "A", 3, ta=["prepa"], note="Kid battu par Kaido avant l'histoire et envoyé à Udon (récit ; Kid aux mines ch. 926)", flags="?")

# ============================================================== Wano acte 2 (ch. 925-957)
fight(2.41, "wano", "sanji", "page_one", "D", note="Raid Suit invisible : coup de pied, Page One le projette à travers des maisons, Sanji revient d'en haut ; issue non montrée (ch. 931)", flags="i")
fight(2.412, "wano", "zoro", "gyukimaru", "D", note="Premier duel sur le pont Oihagi (ch. 937-938)", flags="i")
fight(2.413, "wano", "zoro", "killer", "A", 1, tb=["malade"], note="Zoro abat Kamazo (Killer sous SMILE) avec sa propre faux (ch. 937-938)")
fight(2.416, "wano", "big_mom", "queen", "A", 2, note="Udon, Big Mom amnésique écrase Queen (ch. 945-946)")
fight(2.4161, "wano", "big_mom", ["luffy", "hyogoro"], "A", 2, note="Sumo Inferno, Luffy arrache les colliers (ch. 946-947)", flags="i")
fight(2.417, "wano", "luffy", "babanuki", "A", 2, note="Luffy noue la trompe, l'Excite Shell explose dans Babanuki (ch. 949)")
fight(2.4199, "wano", "hawkins", "law", "A", 2, tb=["protege"],
      note="Hawkins lie Bepo, Shachi et Penguin à sa paille ; Law se rend (ch. 945-951)")
fight(2.4195, "wano", "big_mom", "kaido", "D",
      note="Onigashima : à peine démenottée, Big Mom attaque Kaido, Napoleon contre Hassaikai, le ciel se fend ; pas de vainqueur montré, puis alliance (ch. 951-954) ; ajouté à l'audit vidéo", flags="i")
fight(2.42, "wano", "zoro", "gyukimaru", "D", note="Second duel, Kawamatsu intervient (ch. 951-952)", flags="i")
fight(2.421, "wano", "inuarashi", "ashura_doji", "D", note="Combat à égalité, Kin'emon arrête (chapitre non retrouvé)", flags="i?")

# ============================================================== Wano acte 3 et Onigashima (ch. 958-1057)
fight(2.43, "wano", "luffy", ["ulti", "page_one"], "D", note="Toits d'Onigashima, interrompu par Yamato (ch. 981-983)", flags="i")
fight(2.4301, "wano", "yamato", "ulti", "A", 3, ta=["surprise"], note="Yamato assomme Ulti d'un coup de kanabo, Raimei Hakke (ch. 983)")
fight(2.433, "wano", "kaido", "orochi", "A", 3, ta=["surprise"], note="Kaido décapite Orochi avec le sabre de King au banquet (ch. 985) ; Orochi survit")
fight(2.435, "wano", "kaido", ["kinemon", "kiku", "kawamatsu", "denjiro", "raizo", "ashura_doji", "inuarashi", "nekomamushi", "kanjuro"], "A", 2,
      ta=[], tb=["prepa"], note="Fourreaux rouges sur le toit : Kaido entaillé mais vainqueur (ch. 990-993)")
fight(2.4365, "wano", ["ulti", "page_one"], ["usopp", "nami"], "A", 3, note="Ulti les roue de coups de tête, Tama les sauve sur un komainu (ch. 995-996)")
fight(2.438, "wano", ["kaido", "big_mom"], ["luffy", "zoro", "law", "kid", "killer"], "D",
      note="Les cinq Supernovas contre les deux Empereurs ; Zoro entaille Kaido (ch. 1000-1009)", flags="ei")
fight(2.439, "wano", "marco", ["king", "queen"], "D", note="Marco retient King et Queen, Hoo-in, Bluebird (ch. 1001-1007)", flags="i")
fight(2.4392, "wano", "black_maria", "sanji", "A", 2, ta=["prepa"], tb=["retenue"],
      note="Sanji refuse de frapper une femme, roué dans la toile ; Robin la renverse, Sanji s'échappe (ch. 1004-1005)", flags="i")
fight(2.4393, "wano", "perospero", ["carrot", "wanda"], "A", 2, tb=["epuise"],
      note="Blessé par leurs Sulong (ch. 995), Perospero les bat une fois la lune cachée (ch. 1006)")
fight(2.4395, "wano", "chopper", "queen", "A", 1, ta=["surprise"],
      note="Le Chopperphage guérit l'Ice Oni, les Pleasures se retournent contre Queen ; Marco le saisit au cou et Chopper, en Monster Point, "
           "le gifle en sang (ch. 1007)", flags="i")
fight(2.44, "wano", "kaido", "luffy", "A", 2, note="Luffy découvre le Haki des rois imprégné mais tombe (ch. 1010-1015)")
fight(2.4401, "wano", "big_mom", "ulti", "A", 3, note="Napoleon, Prometheus et Hera combinés ; Ulti assommée en voulant tuer Nami (ch. 1013)")
fight(2.4405, "wano", "kinemon", "kanjuro", "A", 2, tb=["surprise"],
      note="Kanjuro, déguisé en Oden, transperce Kiku ; Kin'emon lui porte le coup fatal (ch. 1014)")
fight(2.4415, "wano", ["nami", "zeus", "usopp"], "ulti", "A", 2, tb=["epuise"],
      note="Zeus, logé dans le Clima-Tact, foudroie Ulti ; Usopp la ligote (Midori Boshi: Devil) (ch. 1016)")
fight(2.4417, "wano", "jinbe", "who_s_who", "A", 2, note="Ancien CP9 ; doigts brisés sur le Haki, Onigawara Seiken (ch. 1017-1018)")
fight(2.4418, "wano", "franky", "sasaki", "A", 2, note="General Franky détruit, Franky éjecté le met K.O. au Radical Beam (ch. 1016-1019)")
fight(2.442, "wano", "kaido", "yamato", "A", 2,
      note="Yamato retarde Kaido jusqu'au retour de Luffy mais est dominée et à bout quand Luffy revient (ch. 1018-1026)", flags="i")
fight(2.444, "wano", "robin", "black_maria", "A", 2, note="Demonio Fleur (ch. 1021-1022)")
fight(2.4446, "wano", "inuarashi", "jack", "A", 2, ta=["boost"], note="Sulong ; Oden Ittoryu: Inu Spire (ch. 1023-1026)")
fight(2.4447, "wano", "nekomamushi", "perospero", "A", 2, ta=["boost"],
      note="Sulong, d'abord dominé quand la lune se cache, puis Oden Ittoryu: Neko Niko Ban (ch. 1023-1026)")
fight(2.4455, "wano", "killer", "hawkins", "A", 2,
      note="Blessures d'abord renvoyées sur la poupée de Kid (ch. 1022) ; Killer lui coupe le bras et décapite l'homme de paille (ch. 1029)")
fight(2.446, "wano", "sanji", "queen", "A", 2, note="Sanji éveille son corps modifié (ch. 1031-1034) ; tag « boost » retiré (audit vidéo) : déjà le saut daté 2.4459")
fight(2.4462, "wano", "zoro", "king", "A", 1, note="Haki des rois imprégné et Enma, Kokujo O Tatsumaki ; King chute (ch. 1033-1035) ; tag « haki_roi » retiré (audit vidéo) : déjà le saut daté 2.4461")
fight(2.447, "wano", "izo", "maha", "D", 1, note="Izo et Maha (CP0) s'entretuent (ch. 1038-1041)")
fight(2.4472, "wano", ["law", "kid"], "big_mom", "A", 1, tb=["epuise"],   # tag « eveil » retiré (audit vidéo) : éveils déjà dans les sauts datés 2.4471
      note="Éveils de Law et Kid, Big Mom jetée par la cheminée jusqu'au dépôt d'armes (ch. 1039-1040)", flags="e")
fight(2.4474, "wano", "raizo", "fukurokuju", "A", 1, note="Impasse de paralysie, puis Raizo tient plus longtemps dans la pièce en feu (ch. 1040-1046)")
fight(2.4485, "wano", "kaido", "luffy", "A", 1, ta=["surprise"], tb=["epuise"],   # tag « haki_roi » retiré (audit vidéo) : déjà le saut daté 2.4399
      note="Le CP0 immobilise Luffy et Kaido le frappe (ch. 1042-1043)")
fight(2.4486, "wano", "kaido", "guernica", "A", 3, note="Kaido punit le CP0 qui s'est mêlé du duel (ch. 1043)")
fight(2.4497, "wano5", "luffy", "kaido", "A", 2,
      note="Gear 5, Bajrang Gun ; Kaido tombe dans le magma (ch. 1044-1049)")
fight(2.4498, "wano5", "denjiro", "orochi", "A", 3, note="Orochi piégé dans le feu puis décapité (ch. 1049-1050)")
