# Partie 2 : après l'ellipse, du retour à Sabaody jusqu'à la fin de Wano (t de 2.0 à 2.45).
# Manga uniquement. Les numéros de chapitre précédés de "env." sont approximatifs.
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
    "cavendish": ("Cavendish (Hakuba)", "Pirates du Beautiful", 5.0, None, None),
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
    "ideo": ("Ideo", "Pirates XXX Gym", 4.0, None, None),
    "machvise": ("Machvise", "Famille Donquixote", 4.0, None, None),
    # ---- Zou
    "jack": ("Jack", "Pirates aux Cent Bêtes", 5.5, None, None),
    "inuarashi": ("Inuarashi", "Minks / Fourreaux rouges", 5.0, None, None),
    "nekomamushi": ("Nekomamushi", "Minks / Fourreaux rouges", 5.0, None, None),
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
    "pedro": ("Pedro", "Minks / Pirates du Nox", 5.0, 2.36, None),
    "tamago": ("Baron Tamago", "Pirates de Big Mom", 4.5, None, None),
    "perospero": ("Charlotte Perospero", "Pirates de Big Mom", 5.0, None, None),
    "bege": ("Capone Bege", "Pirates de Fire Tank", 5.0, None, None),
    "katakuri": ("Charlotte Katakuri", "Pirates de Big Mom", 6.0, None, None),
    "opera": ("Charlotte Opera", "Pirates de Big Mom", 4.5, None, None),
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
    "yamato": ("Yamato", "Pirates aux Cent Bêtes", 6.0, None, None),
    "kinemon": ("Kin'emon", "Fourreaux rouges", 4.0, None, None),
    "kiku": ("Kikunojo", "Fourreaux rouges", 5.0, None, None),
    "kawamatsu": ("Kawamatsu", "Fourreaux rouges", 5.0, None, None),
    "denjiro": ("Denjiro", "Fourreaux rouges", 5.0, None, None),
    "raizo": ("Raizo", "Fourreaux rouges", 5.0, None, None),
    "kanjuro": ("Kanjuro", "Fourreaux rouges (traître)", 4.5, 2.4475, None),
    "marco": ("Marco", "Pirates de Barbe Blanche", 5.0, None, None),
    "king": ("King", "Pirates aux Cent Bêtes", 6.0, None, None),
    "black_maria": ("Black Maria", "Pirates aux Cent Bêtes", 5.0, None, None),
    "sasaki": ("Sasaki", "Pirates aux Cent Bêtes", 5.0, None, None),
    "who_s_who": ("Who's-Who", "Pirates aux Cent Bêtes", 5.0, None, None),
    "fukurokuju": ("Fukurokuju", "Oniwabanshu", 4.5, None, None),
    "izo": ("Izo", "Pirates de Barbe Blanche", 5.0, 2.4472, None),
    "maha": ("Maha", "CP0", 5.0, None, None),
    "guernica": ("Guernica", "CP0", 5.0, None, None),
    "orochi": ("Kurozumi Orochi", "Shogunat de Wano", 3.0, 2.4495, None),
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
    ("franky", 1.5, 1.0, 0.6, "Ellipse : Baldimore, nouveau corps"),
    ("brook", 1.5, 1.0, 0.6, "Ellipse : maîtrise de l'âme (Yomi Yomi)"),
    # Dressrosa
    ("sabo", 2.255, 1.0, 0.7, "Mange le Mera Mera no Mi (ch. 744)"),
    ("usopp", 2.276, 0.4, 0.4, "Éveil du Haki de l'observation (ch. 777)"),
    ("luffy", 2.2785, 1.0, 0.7, "Gear 4 (ch. 784)"),
    # Whole Cake Island
    ("luffy", 2.364, 0.4, 0.4, "Observation du futur apprise contre Katakuri (ch. 893-896)"),
    ("nami", 2.37, 0.5, 0.4, "Zeus rejoint le Clima-Tact (ch. 899-902)"),
    # Wano
    ("luffy", 2.418, 0.5, 0.5, "Ryuo / Haki émis appris à Udon (ch. 939-948)"),
    ("zoro", 2.42, 0.3, 0.4, "Obtient Enma (ch. 955)"),
    ("luffy", 2.4435, 0.5, 0.5, "Haki des rois imprégné maîtrisé (ch. 1010-1043)"),
    ("robin", 2.4441, 0.4, 0.4, "Demonio Fleur (ch. 1021-1022)"),
    ("sanji", 2.4461, 0.8, 0.6, "Éveil du corps modifié Germa (ch. 1031-1034)"),
    ("zoro", 2.4466, 0.8, 0.6, "Haki des rois éveillé et imprégné (ch. 1033-1035)"),
    ("law", 2.4476, 0.8, 0.6, "Éveil de l'Ope Ope no Mi (ch. 1039-1042)"),
    ("kid", 2.4476, 0.8, 0.6, "Éveil du Jiki Jiki no Mi (ch. 1039-1042)"),
    ("luffy", 2.4492, 1.0, 0.8, "Gear 5 / éveil du Gomu Gomu (Hito Hito modèle Nika) acquis (ch. 1044)"),
]

# ============================================================== retour à Sabaody (ch. 598-603)
fight(2.0, "fishman", "sentomaru", "demaro_black", "A", 3, note="Sentomaru et les Pacifista écrasent le faux Luffy (ch. 601)")
fight(2.001, "fishman", "luffy", "pacifista", "A", 3, note="Luffy détruit le PX-5 d'un seul coup imprégné de Haki (ch. 601)")
fight(2.002, "fishman", ["zoro", "sanji"], "pacifista", "A", 3, note="Zoro et Sanji détruisent ensemble le PX-7 (ch. 601)")
fight(2.01, "fishman", "franky", "caribou", "A", 2, note="Franky maîtrise Caribou à bord du Sunny (env. ch. 603)", flags="?")

# ============================================================== Île des Hommes-Poissons (ch. 603-653)
fight(2.1, "fishman", ["luffy", "zoro", "sanji"], "kraken", "A", 3,
      note="Le Kraken assommé par l'Elephant Gun de Luffy, puis apprivoisé (ch. 605)")
fight(2.105, "fishman", "luffy", ["hammond", "wadatsumi"], "A", 3, note="Luffy bat Hammond et ses hommes, puis Wadatsumi (env. ch. 609-610)", flags="?")
fight(2.11, "fishman", "zoro", "neptune", "A", 2, tb=["retenue"], note="Zoro maîtrise le roi Neptune au palais Ryugu (env. ch. 614)", flags="?")
fight(2.111, "fishman", "zoro", "hody", "A", 2, note="Zoro tranche Hody au palais Ryugu (env. ch. 616)")
fight(2.112, "fishman", "hody", "neptune", "A", 2, ta=["surprise", "boost"],
      note="Hody, sous Énergie Stéroïde, capture Neptune avec Zoro, Usopp et Brook déjà pris (env. ch. 617-618)", flags="?")
fight(2.115, "fishman", "luffy", "vander_decken", "A", 2, note="Luffy repousse Decken à Coral Hill (env. ch. 618)", flags="?")
fight(2.118, "fishman", "luffy", "jinbe", "D", note="Dispute au Sea Forest, interrompue (env. ch. 621-622)", flags="i")
fight(2.13, "fishman", "hody", "fukaboshi", "A", 2, ta=["boost"], note="Hody, dopé, défait Fukaboshi et les princes (env. ch. 631-633)", flags="?")
fight(2.131, "fishman", "fukaboshi", "dosun", "A", 2, note="Fukaboshi bat Dosun avant que les officiers ne se dopent (env. ch. 630)", flags="?")
fight(2.135, "fishman", ["luffy", "zoro", "nami", "usopp", "sanji", "chopper", "robin", "franky", "brook"],
      "hody", "A", 3, note="Luffy met à terre la moitié des 100 000 hommes de Hody au Haki des rois (env. ch. 633-634) ; codé contre Hody comme chef", flags="?")
fight(2.14, "fishman", "hody", "vander_decken", "A", 3, ta=["surprise"], note="Hody poignarde Decken (env. ch. 642)")
fight(2.1405, "fishman", "robin", "hammond", "A", 2, note="Double Clutch (env. ch. 641-642)", flags="?")
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
      note="Les centaures battus, Barbe Brune contraint de les porter (env. ch. 659-661)", flags="?")
fight(2.203, "punkhazard", "law", "smoker", "A", 2, note="Law arrache le cœur de Smoker et échange les corps (ch. 663-664)")
fight(2.204, "punkhazard", "law", "tashigi", "A", 3, note="Law coupe Tashigi en deux sans la tuer (ch. 662)")
fight(2.206, "punkhazard", ["scotch", "rock"], ["zoro", "sanji", "brook"], "A", 2, ta=["surprise"],
      note="Les frères Yéti Cool les endorment au gaz KYP (env. ch. 668)", flags="?")
fight(2.207, "punkhazard", ["luffy", "franky"], "rock", "A", 2, note="Luffy le blesse, Franky l'achève avec un glacier (env. ch. 672-673)", flags="?")
fight(2.2071, "punkhazard", "law", "scotch", "A", 3, note="Law le tranche en deux (env. ch. 673)", flags="?")
fight(2.208, "punkhazard", "caesar", ["franky", "robin", "smoker", "tashigi"], "A", 2, ta=["prepa"],
      note="Gaz et Gastanet, Franky, Robin et les Marines capturés (env. ch. 674-676)", flags="?")
fight(2.209, "punkhazard", "caesar", "luffy", "A", 2, ta=["prepa"], note="Gastanet ; Luffy capturé (env. ch. 676)", flags="?")
fight(2.21, "punkhazard", "vergo", "law", "A", 2, ta=["prepa"], tb=["protege"],
      note="Vergo bat Law, dont Caesar tient le cœur (env. ch. 677-678)", flags="?")
fight(2.212, "punkhazard", ["zoro", "nami", "robin"], "monet", "A", 2, note="Monet repoussée en forme de monstre de neige (env. ch. 679)", flags="?")
fight(2.213, "punkhazard", ["zoro", "tashigi"], "monet", "A", 3, note="Zoro tranche Monet, Tashigi l'achève (ch. 680)")
fight(2.214, "punkhazard", "vergo", "sanji", "A", 2, note="Vergo fêle les os de Sanji (env. ch. 686)", flags="?")
fight(2.2141, "punkhazard", "vergo", "smoker", "A", 2, note="Smoker diversion ; Vergo le bat (env. ch. 689)", flags="?")
fight(2.2145, "punkhazard", "law", "vergo", "A", 3, note="Law récupère son cœur et tranche Vergo et le labo (ch. 689-690)")
fight(2.215, "punkhazard", "luffy", "caesar", "A", 3, note="Gomu Gomu no Grizzly Magnum (ch. 690)")
fight(2.218, "punkhazard", "franky", ["baby_5", "buffalo"], "A", 2, note="General Cannon (env. ch. 694-696)", flags="?")
fight(2.2181, "punkhazard", "law", ["baby_5", "buffalo"], "A", 3, note="Law les décapite (env. ch. 696)", flags="?")
fight(2.219, "punkhazard", "aokiji", "doflamingo", "D", ta=["retenue"], tb=["retenue"],
      note="Bref heurt, Doflamingo se retire (ch. 698-699)", flags="i?")

# ============================================================== Dressrosa (ch. 700-801)
fight(2.23, "punkhazard", "fujitora", "zoro", "D", ta=["retenue"], note="Premier heurt dans la ville (env. ch. 709)", flags="i?")
fight(2.232, "punkhazard", "bartolomeo", "elizabello", "A", 2, note="Finale du bloc B après le King Punch (ch. 707-708)")
fight(2.233, "punkhazard", "luffy", "hajrudin", "A", 3, note="Bloc C, un seul coup (env. ch. 717)", flags="?")
fight(2.234, "punkhazard", "luffy", "chinjao", "A", 3, note="Bloc C, Thor Elephant Gun (ch. 718-719)")
fight(2.235, "punkhazard", "burgess", "suleiman", "A", 2, note="Burgess gagne le bloc A (env. ch. 707-714) ; adversaire principal non précisé", flags="?")
fight(2.237, "punkhazard", "doflamingo", "law", "A", 2, note="Green Bit puis le pont : Law capturé et blessé par balles (ch. 722-730)")
fight(2.2375, "punkhazard", "doflamingo", "sanji", "A", 2, note="Sanji immobilisé, Law le téléporte (ch. 723-724)", flags="i")
fight(2.24, "punkhazard", "cavendish", ["rebecca", "suleiman"], "A", 3, tb=[],
      note="Hakuba balaie le bloc D, Rebecca seule à l'esquiver (ch. 734)", flags="?")
fight(2.2401, "punkhazard", "rebecca", "suleiman", "A", 1, note="Rebecca gagne le bloc D (ch. 734)")
fight(2.245, "punkhazard", "trebol", "usopp", "A", 2, note="Trebol bat Usopp au port (env. ch. 741)", flags="?")
fight(2.246, "punkhazard", "usopp", "sugar", "A", 3, ta=["surprise"], note="Sugar s'évanouit de peur (Tatababasco) (ch. 743)")
fight(2.2465, "punkhazard", "sabo", ["diamante", "burgess", "bartolomeo", "rebecca"], "D",
      note="Finale de la Corrida, Sabo détruit l'arène (ch. 742-743)", flags="i?")
fight(2.247, "punkhazard", "diamante", "rebecca", "A", 2, note="Coup de masse en finale, Bartolomeo la protège (ch. 742)", flags="i")
fight(2.25, "punkhazard", "luffy", "fujitora", "D", tb=["retenue"], note="Duel interrompu près du palais (env. ch. 746)", flags="i")
fight(2.26, "punkhazard", "dellinger", "bellamy", "A", 2, note="Bartolomeo l'arrête (env. ch. 758)", flags="?")
fight(2.261, "punkhazard", "luffy", "bellamy", "A", 2, tb=["epuise"], note="Bellamy refuse de tuer mais se bat ; Luffy l'emporte (ch. 759)")
fight(2.262, "punkhazard", "doflamingo", "viola", "A", 3, note="Viola immobilisée (env. ch. 761)", flags="?")
fight(2.2621, "punkhazard", "doflamingo", "bellamy", "A", 3, tb=["epuise"], note="Bellamy servi de bouclier (env. ch. 761-762)")
fight(2.263, "punkhazard", "doflamingo", ["luffy", "law"], "D", tb=["protege"],
      note="Combat au palais, Law sans un bras ; Luffy place un Red Hawk puis ils fuient (ch. 760-765)", flags="i")
fight(2.265, "punkhazard", "franky", "senor_pink", "A", 1, note="Usine SMILE (ch. 763-764)")
fight(2.27, "punkhazard", "lao_g", "chinjao", "A", 2, note="Escalier vers le palais (env. ch. 772-773)", flags="?")
fight(2.271, "punkhazard", "hajrudin", "machvise", "A", 2, note="Hajrudin l'envoie contre la Cage (env. ch. 774)", flags="?")
fight(2.272, "punkhazard", "kyros", "diamante", "A", 2, note="Champ de fleurs, sur la tombe de Scarlett (ch. 776)")
fight(2.2721, "punkhazard", "sai", "lao_g", "A", 2, note="Coup de pied Hasshoken (env. ch. 776)", flags="?")
fight(2.2722, "punkhazard", "ideo", "dellinger", "A", 2, note="env. ch. 776", flags="?")
fight(2.274, "punkhazard", "zoro", "pica", "A", 2, note="Sanzen Sekai (ch. 777)")
fight(2.2741, "punkhazard", "bartolomeo", "gladius", "A", 2, note="Poing de barrière (ch. 777)")
fight(2.2742, "punkhazard", "usopp", "sugar", "A", 3, ta=["surprise"], note="Tir à 4 km, Haki de l'observation (ch. 777)")
fight(2.277, "punkhazard", "law", "trebol", "A", 2, note="Law tranche Trebol (env. ch. 780-781)", flags="?")
fight(2.278, "punkhazard", "doflamingo", "law", "A", 2, tb=["epuise"], note="Gamma Knife ne suffit pas, Doflamingo se soigne (ch. 781-782)")
fight(2.279, "punkhazard", "luffy", "doflamingo", "A", 1, tb=["epuise"],
      note="Gear 4 ; Luffy à court de temps, puis King Kong Gun (ch. 783-790)")
fight(2.285, "punkhazard", "sabo", "fujitora", "D", note="Duel acharné, sans vainqueur (ch. 794)", flags="i")
fight(2.286, "punkhazard", "sabo", "burgess", "A", 2, note="Burgess le provoque au sujet d'Ace (env. ch. 795)", flags="?")

# ============================================================== Zou (ch. 802-824)
fight(2.29, "wci", "jack", ["inuarashi", "nekomamushi"], "A", 1, ta=["prepa"],
      note="Invasion de Zou : Jack l'emporte au bout de 5 jours avec le gaz Koro (ch. 808-809, récit)", flags="?")
fight(2.31, "wci", "zunesha", "jack", "A", 3, note="Zunesha écrase la flotte de Jack à la demande de Luffy (env. ch. 822)")

# ============================================================== Whole Cake Island (ch. 825-902)
fight(2.311, "wci", "urouge", "snack", "A", 2, note="Snack battu par Urouge, rapporté (env. ch. 829-830)", flags="?")
fight(2.32, "wci", ["ichiji", "niji", "yonji"], "sanji", "A", 2, tb=["protege"],
      note="Sanji frappe Niji puis est roué par les trois frères (ch. 832-833)", flags="?")
fight(2.322, "wci", "judge", "sanji", "A", 2, ta=["prepa"], tb=["protege"], note="Judge se sert de soldats et de la décharge électrique (env. ch. 839)", flags="?")
fight(2.33, "wci", "luffy", "cracker", "A", 2, ta=["epuise"], tb=["epuise"],
      note="Onze heures de combat, Gear 4 puis Tankman (ch. 835-843)")
fight(2.332, "wci", "carrot", "brulee", "A", 2, ta=["surprise"], note="Eau bouillante, Brûlée capturée avec Chopper (env. ch. 849-850)", flags="?")
fight(2.335, "wci", "big_mom", "brook", "A", 3, tb=["prepa"], note="Brook vaincu après avoir copié les ponéglyphes (ch. 849-850)")
fight(2.336, "wci", "pedro", "tamago", "A", 2, note="Pedro le tranche deux fois, Tamago se régénère (env. ch. 853)", flags="?")
fight(2.34, "wci", "sanji", "luffy", "A", 3, tb=["retenue", "epuise"], note="Luffy refuse de riposter (ch. 856)")
fight(2.35, "wci", "big_mom", "bege", "A", 2, tb=["prepa"], note="Le cri de Big Mom détruit les KX Launchers (env. ch. 868)")
fight(2.351, "wci", "katakuri", "ichiji", "A", 3, note="Mariage, la Germa défaite (env. ch. 863-866)", flags="?")
fight(2.352, "wci", "jinbe", "opera", "A", 2, note="Gosenmaigawara Seiken (env. ch. 866)", flags="?")
fight(2.36, "wci", "tamago", "pedro", "A", 1, tb=["protege"],
      note="Pedro se fait exploser pour libérer le Sunny ; Tamago survit (ch. 878)", flags="?")
fight(2.3645, "wci", "luffy", "katakuri", "A", 1, ta=["epuise"], tb=["epuise"],
      note="Monde des miroirs, Luffy apprend l'observation du futur (ch. 882-896)")
fight(2.37, "wci", "jinbe", "big_mom", "D", tb=["epuise"], note="Jinbe la fait tomber du Sunny (ch. 900-901)", flags="i?")
fight(2.371, "wci", ["nami", "zeus"], "big_mom", "A", 1, ta=["surprise"], note="Zeus foudroie Big Mom (ch. 899-900)", flags="?")

# ============================================================== Rêverie (ch. 903-908, conséquences ch. 956)
fight(2.38, "wci", "sabo", ["fujitora", "ryokugyu"], "D",
      note="Les commandants révolutionnaires affrontent deux amiraux à Marie-Joie, et s'échappent (ch. 956, récit)", flags="?")

# ============================================================== Wano acte 1 (ch. 909-924)
fight(2.4, "wano", "hawkins", ["luffy", "zoro"], "D", ta=["prepa"], note="Les coups renvoyés sur la poupée de paille, retraite (env. ch. 913)", flags="i")
fight(2.401, "wano", "luffy", "urashima", "A", 3, note="Gear 3 Harite (ch. 916)")
fight(2.402, "wano", "kiku", "urashima", "A", 3, note="Kiku lui tranche le chignon (ch. 916)")
fight(2.403, "wano", "luffy", "holdem", "A", 2, note="Red Hawk à Bakura (ch. 919)")
fight(2.404, "wano", "hawkins", "law", "A", 2, note="Hawkins démasque Law, puis clou en granit marin (env. ch. 920-924)", flags="?")
fight(2.405, "wano", "kaido", "luffy", "A", 3, note="Ruines du château d'Oden, Raimei Hakke (ch. 923-924)")
fight(2.406, "wano", "kaido", "kid", "A", 3, ta=["prepa"], note="Kid capturé après une défaite contre Kaido (récit, ch. 925 env.)", flags="?")

# ============================================================== Wano acte 2 (ch. 925-957)
fight(2.41, "wano", "sanji", "page_one", "A", 1, note="Raid Suit, Sanji contre-attaque d'en haut (env. ch. 931-932)", flags="?")
fight(2.411, "wano", "babanuki", "luffy", "A", 2, tb=["epuise"], note="Udon, Luffy affamé et sous granit marin (env. ch. 937)", flags="?")
fight(2.412, "wano", "zoro", "gyukimaru", "D", note="Premier duel sur le pont Oihagi (env. ch. 937-938)", flags="i")
fight(2.413, "wano", "zoro", "killer", "A", 1, tb=[], note="Zoro bat Kamazo (Killer sous SMILE) au Rengoku Oni Giri (env. ch. 937-939)", flags="?")
fight(2.414, "wano", "law", "hawkins", "A", 2, note="Prison de Rasetsu, Law le découpe (env. ch. 944)", flags="?")
fight(2.416, "wano", "big_mom", "queen", "A", 2, note="Udon, Big Mom amnésique écrase Queen (ch. 945-946)")
fight(2.4161, "wano", "big_mom", ["luffy", "hyogoro"], "A", 2, note="Sumo Inferno, Luffy arrache les colliers (ch. 946-947)", flags="i")
fight(2.417, "wano", "luffy", "babanuki", "A", 2, note="Révolte d'Udon, Babanuki pris dans sa propre explosion (env. ch. 948)", flags="?")
fight(2.42, "wano", "zoro", "gyukimaru", "D", note="Second duel, Kawamatsu intervient (env. ch. 951-952)", flags="i")
fight(2.421, "wano", "inuarashi", "ashura_doji", "D", note="Kin'emon arrête le combat (env. ch. 953)", flags="i?")

# ============================================================== Wano acte 3 et Onigashima (ch. 958-1057)
fight(2.43, "wano", "luffy", ["ulti", "page_one"], "D", note="Toits d'Onigashima (ch. 980-983)", flags="i")
fight(2.431, "wano", "yamato", "ulti", "A", 2, ta=["surprise"], note="Yamato met Ulti hors combat (env. ch. 984)", flags="?")
fight(2.433, "wano", "kaido", "orochi", "A", 3, ta=["surprise"], note="Kaido décapite Orochi au banquet (ch. 985) ; Orochi survit", flags="?")
fight(2.435, "wano", "kaido", ["kinemon", "kiku", "kawamatsu", "denjiro", "raizo", "ashura_doji", "inuarashi", "nekomamushi", "kanjuro"], "A", 2,
      ta=[], tb=["prepa"], note="Fourreaux rouges sur le toit : Kaido entaillé mais vainqueur (ch. 990-993)")
fight(2.438, "wano", ["kaido", "big_mom"], ["luffy", "zoro", "law", "kid", "killer"], "D",
      note="Les cinq Supernovas contre les deux Empereurs ; Zoro entaille Kaido (ch. 1000-1009)", flags="i")
fight(2.439, "wano", "marco", ["king", "queen"], "D", note="Marco retient King et Queen (env. ch. 1001-1007)", flags="i?")
fight(2.4392, "wano", "sanji", "black_maria", "D", tb=["prepa"], note="Sanji ne frappe pas une femme, s'échappe (env. ch. 1006-1007)", flags="i?")
fight(2.44, "wano", "kaido", "luffy", "A", 2, tb=["haki_roi"], note="Luffy découvre le Haki des rois imprégné mais tombe (ch. 1010-1015)")
fight(2.442, "wano", "kaido", "yamato", "D", note="Yamato tient Kaido jusqu'au retour de Luffy (ch. 1018-1026)", flags="i")
fight(2.4432, "wano", ["nami", "zeus"], "ulti", "A", 2, note="Ulti assommée par l'éclair de Zeus (env. ch. 1019)", flags="?")
fight(2.444, "wano", "robin", "black_maria", "A", 2, note="Demonio Fleur (ch. 1021-1022)")
fight(2.4442, "wano", "franky", "sasaki", "A", 2, note="Franky Shogun (env. ch. 1023)", flags="?")
fight(2.4444, "wano", "jinbe", "who_s_who", "A", 2, note="Ancien CP9 (env. ch. 1024)", flags="?")
fight(2.4445, "wano", "perospero", ["carrot", "wanda"], "A", 2, note="Onigashima (env. ch. 1017-1019)", flags="?")
fight(2.4455, "wano", "big_mom", "page_one", "A", 3, note="Un seul coup (env. ch. 1028)", flags="?")
fight(2.446, "wano", "sanji", "queen", "A", 2, ta=["boost"], note="Sanji éveille son corps modifié (ch. 1031-1034)")
fight(2.4462, "wano", "zoro", "king", "A", 1, ta=["haki_roi"], note="Haki des rois imprégné et Enma, Kokujo O Tatsumaki ; King chute (ch. 1033-1035)")
fight(2.4467, "wano", "killer", "hawkins", "A", 2, note="Killer venge Kid (env. ch. 1036)", flags="?")
fight(2.4468, "wano", ["inuarashi", "nekomamushi"], ["jack", "perospero"], "A", 2, ta=["boost"],
      note="Sulong sous la pleine lune (env. ch. 1036-1037)", flags="?")
fight(2.447, "wano", "izo", "maha", "A", 1, tb=["surprise"], note="Izo l'emporte au prix de sa vie (env. ch. 1040)", flags="?")
fight(2.4472, "wano", ["law", "kid"], "big_mom", "A", 1, ta=["eveil"], tb=["epuise"],
      note="Éveils de Law et Kid, Big Mom jetée dans la chambre magmatique (ch. 1039-1042)")
fight(2.4473, "wano", "kinemon", "kanjuro", "A", 2, note="Kanjuro meurt de ses blessures (env. ch. 1046)", flags="?")
fight(2.4474, "wano", "raizo", "fukurokuju", "A", 1, note="Raizo tient plus longtemps dans la pièce en feu (env. ch. 1047-1048)", flags="?")
fight(2.4485, "wano", "kaido", "luffy", "A", 1, ta=["surprise"], tb=["haki_roi", "epuise"],
      note="Guernica (CP0) immobilise Luffy et Kaido le frappe (ch. 1042-1043)", flags="?")
fight(2.4486, "wano", "kaido", "guernica", "A", 3, note="Kaido punit le CP0 qui s'est mêlé du duel (ch. 1043)")
fight(2.449, "wano", "luffy", "kaido", "A", 2, ta=["eveil", "haki_roi"], tb=["epuise"],
      note="Gear 5, Bajrang Gun ; Kaido tombe dans le magma (ch. 1044-1049)")
fight(2.4495, "wano", "denjiro", "orochi", "A", 3, note="Orochi piégé dans le feu puis décapité (ch. 1049-1050)")
