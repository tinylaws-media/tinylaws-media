# One Piece, partie 1 : flashbacks (Rocks / God Valley, Roger, Oden, enfance de Luffy, Ace et Sabo, Fisher Tiger,
# Kuma, Ohara, Doflamingo et Corazon...) puis tout l'avant-ellipse (East Blue -> Marineford et l'après-guerre).
# Manga uniquement (+ infos Oda/Vivre Card quand elles donnent un résultat). "fight" est injecté par data.py.
# Repères de temps : East Blue 0.01-0.38, Alabasta 0.40-0.53, Jaya/Skypiea 0.55-0.68, Long Ring/Water 7/Enies Lobby
# 0.70-0.78, Thriller Bark 0.80-0.85, Sabaody 0.90-0.91, Amazon Lily 0.915, Impel Down 0.92-0.935,
# Marineford 0.94-0.952 (mort d'Ace 0.9495, de Barbe Blanche 0.952), après-guerre 0.96-1.5.
# "ch. ~N" = numéro de chapitre approximatif (à un ou deux chapitres près).

CHARS_PART = {
    # ---------------------------------------------------------------- légendes, God Valley
    "rocks": ("Rocks D. Xebec", "Pirates de Rocks", 8.0, -37.98, None),
    "roger": ("Gol D. Roger", "Pirates de Roger", 8.0, -22.0, None),
    "garp": ("Monkey D. Garp", "Marine", 8.0, None, None),
    "whitebeard": ("Edward Newgate (Barbe Blanche)", "Pirates de Barbe Blanche", 7.5, 0.952, None),
    "kaido": ("Kaido", "Pirates aux Cent Bêtes", 5.0, None, None),
    "big_mom": ("Charlotte Linlin (Big Mom)", "Pirates de Big Mom", 5.5, None, None),
    "rayleigh": ("Silvers Rayleigh", "Pirates de Roger", 7.0, None, None),
    "shakky": ("Shakuyaku (Shakky)", "Pirates de Rocks", 4.5, None, None),
    "imu": ("Imu", "Gouvernement mondial", 8.5, None, None),
    "saturn": ("Saint Jaygarcia Saturn", "Cinq Doyens", 6.5, 2.55, None),
    "garling": ("Saint Figarland Garling", "Chevaliers divins", 5.5, None, None),
    "maffey": ("Saint Satchels Maffey", "Chevaliers divins", 5.0, None, None),
    "sommers": ("Saint Shepherd Sommers", "Chevaliers divins", 5.0, None, None),
    "chevaliers_divins": ("Chevaliers divins (groupe)", "Chevaliers divins", 4.5, None, None),
    "dragon": ("Monkey D. Dragon", "Armée révolutionnaire", 4.0, None, None),
    "ivankov": ("Emporio Ivankov", "Armée révolutionnaire", 1.5, None, None),
    "kuma": ("Bartholomew Kuma", "Armée révolutionnaire / Shichibukai", 4.0, None, None),   # 1er nœud = prime de 296 M (t = -10), adulte ; 0,5 (enfant à God Valley) ne valait pas à cette date
    "pirates_ordinaires": ("Pirates ordinaires (groupe)", "Pirates", 1.0, None, None),
    "marines_ordinaires": ("Marines ordinaires (groupe)", "Marine", 1.0, None, None),
    # ---------------------------------------------------------------- Roger, Oden, Wano
    "oden": ("Kozuki Oden", "Wano / Pirates de Roger", 4.5, -20.0, None),
    "ashura_doji": ("Ashura Doji", "Fourreaux rouges", 3.5, 2.45, None),
    "akazaya": ("Fourreaux rouges (groupe)", "Wano", 3.5, None, None),
    "pirates_aux_cent_betes": ("Pirates aux Cent Bêtes (troupe)", "Pirates aux Cent Bêtes", 2.0, None, None),
    "saul": ("Jaguar D. Saul", "Marine (déserteur)", 4.0, None, None),
    "aokiji": ("Kuzan (Aokiji)", "Marine", 5.0, None, None),
    "kizaru": ("Borsalino (Kizaru)", "Marine", 5.5, None, None),
    "fisher_tiger": ("Fisher Tiger", "Pirates du Soleil", 4.0, -10.0, None),   # mort à -12, fixée à l'ancre de l'arc « avant » pour qu'il y figure
    "strawberry": ("Strawberry", "Marine", 3.5, None, None),
    "arlong": ("Arlong", "Pirates d'Arlong", 2.5, None, None),
    "bellemere": ("Bell-mère", "Village de Cocoyashi", 1.0, -8.0, None),
    "genzo": ("Genzo", "Village de Cocoyashi", 0.5, None, None),
    "doflamingo": ("Donquixote Doflamingo", "Famille Donquixote", 4.0, None, None),
    "vergo": ("Vergo", "Famille Donquixote", 4.0, None, None),
    "rosinante": ("Donquixote Rosinante (Corazon)", "Marine", 3.5, -10.0, None),   # mort à -11, fixée à l'ancre de l'arc « avant »
    "crocodile": ("Sir Crocodile", "Baroque Works", 3.5, None, None),   # 1er nœud = sa défaite de jeunesse contre Barbe Blanche (t = -24), pas encore Shichibukai
    "shanks": ("Shanks le Roux", "Pirates du Roux", 2.0, None, None),   # 1er nœud = mousse de Roger (t = -24, ch. 966) ; la montée vient du saut daté ci-dessous
    "mihawk": ("Dracule Mihawk", "Shichibukai", 6.0, None, None),   # 1er nœud = jeunes duels avec Shanks (t = -15, ch. 434)
    "benn_beckman": ("Benn Beckman", "Pirates du Roux", 5.5, None, None),
    "higuma": ("Higuma", "Bandits", 1.0, -10.0, None),
    "seigneur_cote": ("Seigneur de la côte (monstre marin)", "Animaux", 2.0, None, None),
    # ---------------------------------------------------------------- enfances
    "luffy": ("Monkey D. Luffy", "Équipage du Chapeau de paille", 0.3, None, None),
    "ace": ("Portgas D. Ace", "Pirates de Barbe Blanche", 0.8, 0.9495, None),
    "sabo": ("Sabo", "Armée révolutionnaire", 0.8, None, None),
    "porchemy": ("Porchemy", "Pirates de Bluejam", 1.0, None, None),
    "bluejam": ("Bluejam", "Pirates de Bluejam", 1.5, None, None),
    "dadan": ("Curly Dadan", "Bandits de Dadan", 1.0, None, None),
    "zoro": ("Roronoa Zoro", "Équipage du Chapeau de paille", 0.5, None, None),
    "kuina": ("Kuina", "Dojo Isshin", 1.0, -10.0, None),   # morte peu après ses duels (-10,4), fixée à l'ancre de l'arc « avant »
    "jinbe": ("Jinbe", "Pirates du Soleil / Shichibukai", 4.5, None, None),
    # ---------------------------------------------------------------- East Blue
    "alvida": ("Alvida", "Pirates d'Alvida", 1.0, None, None),
    "morgan": ("Morgan", "Marine", 1.5, None, None),
    "mohji": ("Mohji", "Pirates de Buggy", 1.0, None, None),
    "cabaji": ("Cabaji", "Pirates de Buggy", 1.5, None, None),
    "buggy": ("Baggy le Clown", "Pirates de Buggy", 1.0, None, None),   # 1er nœud = apprenti de Roger (t = -24, ch. 966)
    "kuro": ("Kuro", "Pirates du Chat noir", 2.0, None, None),
    "jango": ("Jango", "Pirates du Chat noir", 1.5, None, None),
    "nyaban_brothers": ("Frères Nyaban (Sham et Buchi)", "Pirates du Chat noir", 1.3, None, None),
    "usopp": ("Usopp", "Équipage du Chapeau de paille", 1.0, None, None),
    "sanji": ("Sanji", "Équipage du Chapeau de paille", 2.0, None, None),
    "fullbody": ("Fullbody", "Marine", 1.0, None, None),
    "gin": ("Gin", "Pirates de Don Krieg", 2.0, None, None),
    "pearl": ("Pearl", "Pirates de Don Krieg", 1.5, None, None),
    "don_krieg": ("Don Krieg", "Pirates de Don Krieg", 2.0, None, None),
    "pirates_de_krieg": ("Flotte de Don Krieg (groupe)", "Pirates de Don Krieg", 1.0, None, None),
    "hachi": ("Hatchan (Hachi)", "Pirates d'Arlong", 2.0, None, None),
    "chew": ("Chew", "Pirates d'Arlong", 1.5, None, None),
    "kuroobi": ("Kuroobi", "Pirates d'Arlong", 2.0, None, None),
    "smoker": ("Smoker", "Marine", 3.5, None, None),
    "tashigi": ("Tashigi", "Marine", 2.0, None, None),
    # ---------------------------------------------------------------- Alabasta
    "nami": ("Nami", "Équipage du Chapeau de paille", 1.0, None, None),
    "vivi": ("Nefertari Vivi", "Alabasta", 1.0, None, None),
    "chopper": ("Tony Tony Chopper", "Équipage du Chapeau de paille", 1.5, None, None),
    "robin": ("Nico Robin", "Équipage du Chapeau de paille", 3.0, None, None),
    "baroque_works_agents": ("Agents de Baroque Works (groupe)", "Baroque Works", 1.0, None, None),
    "mr_5": ("Mr. 5", "Baroque Works", 2.0, None, None),
    "miss_valentine": ("Miss Valentine", "Baroque Works", 1.5, None, None),
    "mr_3": ("Mr. 3 (Galdino)", "Baroque Works", 2.0, None, None),
    "miss_goldenweek": ("Miss Goldenweek", "Baroque Works", 1.5, None, None),
    "dorry": ("Dorry", "Géants d'Elbaf", 3.0, None, None),
    "brogy": ("Brogy", "Géants d'Elbaf", 3.0, None, None),
    "wapol": ("Wapol", "Royaume de Drum", 1.5, None, None),
    "chess": ("Chess", "Royaume de Drum", 1.0, None, None),
    "kuromarimo": ("Kuromarimo", "Royaume de Drum", 1.0, None, None),
    "mr_1": ("Mr. 1 (Daz Bonez)", "Baroque Works", 3.0, None, None),
    "miss_doublefinger": ("Miss Doublefinger", "Baroque Works", 2.5, None, None),
    "mr_4": ("Mr. 4", "Baroque Works", 2.0, None, None),
    "miss_merry_christmas": ("Miss Merry Christmas", "Baroque Works", 2.0, None, None),
    "bon_clay": ("Bon Clay (Mr. 2)", "Baroque Works", 2.5, None, None),
    # ---------------------------------------------------------------- Jaya, Skypiea
    "bellamy": ("Bellamy", "Pirates de Bellamy", 2.0, None, None),
    "satori": ("Satori", "Prêtres d'Enel", 2.0, None, None),
    "gedatsu": ("Gedatsu", "Prêtres d'Enel", 2.0, None, None),
    "yama": ("Yama (chef des Soldats divins)", "Soldats divins d'Enel", 2.0, None, None),
    "shura": ("Shura", "Prêtres d'Enel", 2.5, None, None),
    "ohm": ("Ohm", "Prêtres d'Enel", 3.0, None, None),
    "gan_fall": ("Gan Fall", "Skypiea", 2.5, None, None),
    "wyper": ("Wyper", "Shandia", 3.0, None, None),
    "enel": ("Enel", "Skypiea", 4.0, None, None),
    # ---------------------------------------------------------------- Long Ring Long Land, Water 7, Enies Lobby
    "foxy": ("Foxy", "Pirates de Foxy", 1.5, None, None),
    "groggy_monsters": ("Groggy Monsters (groupe)", "Pirates de Foxy", 1.5, None, None),
    "franky_family": ("Franky Family (groupe)", "Franky Family", 1.0, None, None),
    "lucci": ("Rob Lucci", "CP9", 4.0, None, None),
    "kaku": ("Kaku", "CP9", 3.5, None, None),
    "kalifa": ("Kalifa", "CP9", 3.0, None, None),
    "jabra": ("Jabra", "CP9", 3.5, None, None),
    "blueno": ("Blueno", "CP9", 3.0, None, None),
    "kumadori": ("Kumadori", "CP9", 3.0, None, None),
    "fukurou": ("Fukurou", "CP9", 2.5, None, None),
    "nero": ("Nero", "CP9", 2.0, None, None),
    "wanze": ("Wanze", "CP7", 2.0, None, None),
    "t_bone": ("T-Bone", "Marine", 2.5, None, None),
    "spandam": ("Spandam", "CP9", 0.5, None, None),
    "franky": ("Franky", "Équipage du Chapeau de paille", 3.0, None, None),
    "blackbeard": ("Marshall D. Teach (Barbe Noire)", "Pirates de Barbe Noire", 4.5, None, None),
    # ---------------------------------------------------------------- Thriller Bark
    "moria": ("Gecko Moria", "Shichibukai", 4.0, None, None),
    "absalom": ("Absalom", "Pirates de Thriller Bark", 2.5, None, None),
    "perona": ("Perona", "Pirates de Thriller Bark", 2.5, None, None),
    "hogback": ("Hogback", "Pirates de Thriller Bark", 1.0, None, None),
    "ryuma_zombie": ("Ryuma (zombie à l'ombre de Brook)", "Pirates de Thriller Bark", 3.5, None, None),
    "oars_zombie": ("Oars (zombie à l'ombre de Luffy)", "Pirates de Thriller Bark", 3.5, None, None),
    "brook": ("Brook", "Équipage du Chapeau de paille", 3.0, None, None),
    # ---------------------------------------------------------------- Sabaody, Amazon Lily, Impel Down
    "duval": ("Duval", "Rosy Life Riders", 1.5, None, None),
    "charloss": ("Saint Charlos", "Dragons célestes", 0.0, None, None),
    "kid": ("Eustass Kid", "Pirates de Kid", 4.0, None, None),
    "law": ("Trafalgar Law", "Pirates du Heart", 4.0, None, None),
    "urouge": ("Urouge", "Pirates du Moine fou", 4.0, None, None),
    "hawkins": ("Basil Hawkins", "Pirates de Hawkins", 4.0, None, None),
    "drake": ("X Drake", "Pirates de Drake", 4.0, None, None),
    "apoo": ("Scratchmen Apoo", "Pirates de On Air", 4.0, None, None),
    "pacifista": ("Pacifista (un exemplaire)", "Marine", 4.0, None, None),
    "sentomaru": ("Sentomaru", "Marine", 4.0, None, None),
    "sandersonia": ("Boa Sandersonia", "Pirates Kuja", 3.0, None, None),
    "marigold": ("Boa Marigold", "Pirates Kuja", 3.0, None, None),
    "hancock": ("Boa Hancock", "Pirates Kuja / Shichibukai", 4.5, None, None),
    "minotaurus": ("Minotaurus (bête geôlière)", "Impel Down", 3.0, None, None),
    "magellan": ("Magellan", "Impel Down", 5.0, None, None),
    "hannyabal": ("Hannyabal", "Impel Down", 3.0, None, None),
    "sadi": ("Sadi-chan", "Impel Down", 3.0, None, None),
    "gardes_impel_down": ("Gardes d'Impel Down (groupe)", "Impel Down", 1.5, None, None),
    "blackbeard_pirates": ("Pirates de Barbe Noire (équipage)", "Pirates de Barbe Noire", 4.0, None, None),
    # ---------------------------------------------------------------- Marineford
    "marco": ("Marco", "Pirates de Barbe Blanche", 5.0, None, None),
    "jozu": ("Joz (Jozu)", "Pirates de Barbe Blanche", 5.0, None, None),
    "vista": ("Vista", "Pirates de Barbe Blanche", 5.0, None, None),
    "squard": ("Squard", "Alliés de Barbe Blanche", 3.0, None, None),
    "oars_jr": ("Little Oars Jr.", "Alliés de Barbe Blanche", 4.0, None, None),
    "akainu": ("Sakazuki (Akainu)", "Marine", 6.5, None, None),
    "sengoku": ("Sengoku", "Marine", 6.5, None, None),
    "onigumo": ("Onigumo", "Marine", 4.0, None, None),
    "koby": ("Koby", "Marine", 2.0, None, None),
}

GENERIC_PART = {"chevaliers_divins", "pirates_ordinaires", "marines_ordinaires", "akazaya", "pirates_aux_cent_betes",
                "pirates_de_krieg", "baroque_works_agents", "groggy_monsters", "franky_family", "pacifista",
                "gardes_impel_down", "blackbeard_pirates"}

# (perso, t, gain moyen en échelons, écart-type, label) : progrès ou déclins permanents dans ma portée
JUMPS_PART = [
    ("kaido", -30.0, 2.0, 0.8, "Maturité, maîtrise de l'Uo Uo no Mi (après God Valley)"),
    ("big_mom", -30.0, 1.5, 0.8, "Maturité (après God Valley)"),
    ("ivankov", -25.0, 3.0, 1.0, "Adulte, cadre révolutionnaire (enfant à God Valley)"),
    ("dragon", -25.0, 3.0, 1.0, "Fondateur et chef de l'Armée révolutionnaire"),
    ("kuma", -27.0, 3.5, 1.0, "Adulte, maîtrise du Nikyu Nikyu no Mi (enfant à God Valley)"),
    ("kuma", -5.0, 1.0, 0.6, "Transformation en cyborg par Vegapunk"),
    ("oden", -26.0, 1.0, 0.6, "Voyages avec Barbe Blanche"),
    ("rayleigh", -10.0, -0.8, 0.3, "Âge (retraite), même génération que Gaban"),
    ("gaban", -10.0, -0.8, 0.3, "Âge, même génération que Rayleigh"),
    ("garp", -15.0, -0.8, 0.5, "Âge (fin de son apogée)"),
    ("whitebeard", -2.0, -1.0, 0.5, "Âge et maladie"),
    ("aokiji", -10.0, 1.2, 0.6, "Promu amiral"),
    ("kizaru", -10.0, 0.7, 0.5, "Promu amiral"),
    ("doflamingo", -5.0, 1.0, 0.6, "Maturité, Shichibukai"),
    ("ace", -3.5, 3.0, 1.0, "Départ en mer, Mera Mera no Mi"),
    ("sabo", -1.0, 3.5, 1.2, "Formation dans l'Armée révolutionnaire (hors champ, sans le Mera Mera)"),
    ("zoro", -0.5, 2.0, 0.7, "Entraînement, chasseur de primes"),
    ("zoro", 0.4929, 0.4, 0.4, "Apprend à trancher l'acier (« souffle de toute chose ») contre Mr. 1 (ch. 195)"),
    ("zoro", 0.7365, 0.4, 0.4, "Asura / Kyutoryu à Enies Lobby (ch. 417)"),
    ("shanks", -20.0, 3.5, 1.0, "Après l'exécution de Roger : capitaine, duels avec Mihawk « qui ébranlaient Grand Line » (ch. 434)"),
    ("luffy", -0.02, 1.7, 0.6, "Dix ans d'entraînement (enfant -> départ en mer)"),
    ("sanji", 0.745, 0.4, 0.4, "Diable Jambe"),
    ("luffy", 0.7299, 0.6, 0.4, "Gear 2 et Gear 3 (Gear 2 dès Blueno, ch. 387-388)"),   # placé avant le combat où il apparaît
    ("blackbeard", 0.9523, 1.5, 0.8, "Vole le Gura Gura no Mi de Barbe Blanche"),
]

# ================================================================ God Valley (ch. 1096, 1158-1166)
fight(-38.0, "godvalley", "big_mom", "ivankov", "A", 3, note="Linlin écarte Ivankov enfant et lui prend le fruit Seiryu (ch. 1096, revu ch. 1162)")
fight(-37.999, "godvalley", "maffey", "dragon", "A", 1, note="Maffey blesse gravement Dragon, interrompu par Newgate ; Dragon fuit avec Shanks (ch. 1161)", flags="i")
fight(-37.998, "godvalley", "garp", ["whitebeard", "kaido", "big_mom"], "A", 1,
      note="Garp les charge (avec Shiki) ; les Homies et le Heavenly Fire de Linlin sont sans effet, les quatre fuient (ch. 1161)")
fight(-37.997, "godvalley", ["whitebeard", "kaido", "big_mom"], "pirates_ordinaires", "A", 3,
      note="Embuscade de petits équipages balayée (avec Shiki) (ch. 1161)")
fight(-37.996, "godvalley", "shakky", "marines_ordinaires", "A", 3, note="Shakuyaku, enchaînée, bat les Marines (ch. 1161)")
fight(-37.995, "godvalley", "rayleigh", "sommers", "A", 2, note="Rayleigh abat Sommers pour sauver Shakuyaku (ch. 1161)")
fight(-37.993, "godvalley", "rocks", ["garling", "chevaliers_divins"], "D", ta=["protege"],
      note="Rocks échange avec Garling et un chevalier en portant Ellis et Teach, puis fuit (ch. 1162)", flags="i")
fight(-37.992, "godvalley", "rocks", ["garling", "chevaliers_divins"], "A", 2,
      note="Sa famille à l'abri, Rocks se retourne et bat hors champ Garling et les chevaliers malgré leur régénération (ch. 1162)")
fight(-37.991, "godvalley", "kaido", "big_mom", "A", 1, ta=["surprise"],
      note="Kaido prend à Linlin le fruit Seiryu par surprise et le mange (ch. 1162)")
fight(-37.99, "godvalley", "imu", ["roger", "garp", "rocks", "whitebeard", "kaido", "big_mom"], "D",
      note="Leur attaque combinée détruit le corps d'Imu (dans celui de Saturn), qui se régénère aussitôt et riposte au Haki des rois (ch. 1163)", flags="i")
fight(-37.989, "godvalley", "rocks", ["kaido", "big_mom"], "A", 3, ta=["possede"],
      note="Rocks démonisé (Domi Reversi d'Imu, ch. 1163) projette Kaido dans la montagne et expédie Linlin ; Newgate lui tient tête (ch. 1164)")
fight(-37.988, "godvalley", ["roger", "garp"], "rocks", "A", 1, ta=[], tb=["possede"],
      note="Attaque combinée de Roger et Garp, Rocks (Domi Reversi) vaincu, les trois s'effondrent d'épuisement (ch. 1165-1166) ; "
           "victoire à deux partenaires égaux (aucun des deux n'aurait suffi seul, ch. 957)", flags="e")
# retiré : « Garling achève Rocks déjà à terre d'un coup d'épée (ch. 1166) » : coup de grâce sur un homme à terre,
# pas un combat ; il faisait passer Garling (5,0 à God Valley) pour un égal de Rocks et tirait Rocks vers le bas.

# ================================================================ Ère de Roger, Oden (ch. 960-972)
fight(-33.5, "oden", "oden", "ashura_doji", "A", 2, note="Oden bat Ashura Doji, qui devient son vassal (ch. 961)")
fight(-24.5, "roger", "roger", "whitebeard", "D", ta=[], tb=[],
      note="Rencontre des deux équipages, trois jours de combat sans vainqueur (ch. 966)")
fight(-24.499, "roger", "roger", "oden", "D", note="Échange Roger/Oden pendant le même affrontement (ch. 966)", flags="i")
fight(-24.0, "roger", "whitebeard", "crocodile", "A", 3,
      note="Crocodile a perdu jadis contre Barbe Blanche (évoqué à Marineford ; date et chapitre exacts non confirmés)", flags="?")
fight(-20.2, "oden", ["oden", "akazaya"], "pirates_aux_cent_betes", "A", 2, note="Raid d'Oden et des Fourreaux rouges (ch. 970)")
fight(-20.15, "oden", "kaido", "oden", "A", 1, ta=["surprise"],
      note="Oden blesse Kaido (cicatrice) mais est distrait par Higurashi déguisée en Momonosuke (ch. 970)")
fight(-20.0, "oden", "aokiji", "saul", "A", 2, note="Ohara : Kuzan gèle Saul (ch. 397)")
fight(-15.0, "avant", "shanks", "mihawk", "D", note="Rivalité et duels de jeunesse évoqués, sans vainqueur connu (ch. 434)")
fight(-12.0, "avant", "kizaru", "arlong", "A", 3, note="Borsalino bat Arlong et l'emprisonne (ch. 623)")
fight(-12.0, "avant", ["strawberry", "marines_ordinaires"], "fisher_tiger", "A", 2, ta=["surprise"],
      note="Embuscade de Foolshout, Tiger mortellement blessé (ch. 623)")
fight(-11.0, "avant", "vergo", "rosinante", "A", 3, tb=["epuise"], note="Vergo passe Corazon à tabac sur Minion ; Corazon, déjà criblé de balles par une patrouille pirate, ne riposte pas (ch. 766)")
fight(-11.0, "avant", "doflamingo", "rosinante", "A", 3, tb=["epuise"], note="Doflamingo abat son frère (ch. 767)")
fight(-10.4, "avant", "kuina", "zoro", "A", 3, note="Zoro enfant perd ses 2001 duels contre Kuina (ch. 5)")
fight(-10.0, "avant", "higuma", "luffy", "A", 3, note="Luffy enfant enlevé par Higuma (ch. 1)")
fight(-10.0, "avant", "benn_beckman", "higuma", "A", 3, note="L'équipage du Roux, Beckman en tête, écrase les bandits (ch. 1)")
fight(-10.0, "avant", "shanks", "seigneur_cote", "A", 3, ta=["protege"],
      note="Shanks fait fuir le Seigneur de la côte en sauvant Luffy, perd un bras (ch. 1)")
fight(-9.9, "avant", "ace", "luffy", "A", 3, note="Ace bat Luffy à chaque duel, enfants (ch. 584-588)")
fight(-9.89, "avant", "porchemy", "luffy", "A", 3, note="Porchemy capture et torture Luffy (ch. 584)")
fight(-9.88, "avant", ["ace", "sabo"], "porchemy", "A", 2, note="Ace et Sabo sauvent Luffy (ch. 584-585)")
fight(-9.0, "cocoyashi", ["ace", "dadan"], "bluejam", "A", 1,
      note="Incendie du Grey Terminal : Ace éveille le Haki des rois et tient tête, Dadan abat Bluejam d'un coup de hache (ch. 587)")
fight(-8.0, "cocoyashi", "arlong", "bellemere", "A", 3, note="Arlong abat Bell-mère (ch. 77-78)")
fight(-8.0, "cocoyashi", "arlong", "genzo", "A", 3, note="Genzo lacéré (ch. 78-79)")
fight(-2.5, "ace_wb", "ace", "jinbe", "D", note="Cinq jours de combat, arrêtés par Barbe Blanche (ch. 552)")
fight(-2.49, "ace_wb", "whitebeard", "ace", "A", 3, ta=["retenue"], note="Ace écrasé puis cent tentatives d'assassinat ratées (ch. 552)")

# ================================================================ East Blue
fight(0.01, "eastblue", "luffy", "alvida", "A", 3, note="Gomu Gomu no Pistol (ch. 2)")
fight(0.03, "eastblue", ["luffy", "zoro"], "morgan", "A", 3, note="Shells Town (ch. 6-7)")
fight(0.05, "eastblue", "luffy", "mohji", "A", 3, note="Orange Town, Mohji et Richie (ch. 13)")
fight(0.051, "eastblue", "zoro", "cabaji", "A", 1, ta=["epuise"], note="Zoro blessé par Buggy (ch. 16-17)")
fight(0.052, "eastblue", "luffy", "buggy", "A", 2, note="Orange Town (ch. 19-20)")
fight(0.08, "eastblue", "zoro", "nyaban_brothers", "A", 2, note="Syrup, Buchi puis Sham (ch. 35-36)")
fight(0.081, "eastblue", "usopp", "jango", "A", 1, note="Syrup, Jango tombe à la fin (ch. 39-40)")
fight(0.082, "eastblue", "luffy", "kuro", "A", 2, note="Syrup (ch. 38-40)")
fight(0.12, "eastblue", "sanji", "fullbody", "A", 3, note="Baratie (ch. 44)")
fight(0.121, "eastblue", "sanji", "gin", "A", 3, tb=["epuise"], note="Gin affamé (ch. 45)")
fight(0.125, "eastblue", "mihawk", "pirates_de_krieg", "A", 3, note="Mihawk coule la flotte de Krieg (ch. 50)")
fight(0.126, "eastblue", "mihawk", "zoro", "A", 3, ta=["retenue"], note="Mihawk n'utilise d'abord qu'un couteau (ch. 51-52)")
fight(0.13, "eastblue", "gin", "pearl", "A", 3, note="Gin assomme Pearl d'un seul coup (Luffy n'a pas combattu Pearl) (ch. 59)")
fight(0.131, "eastblue", "gin", "sanji", "A", 2, tb=["protege"], note="Sanji protège Zeff (ch. 61-62)")
fight(0.132, "eastblue", "luffy", "gin", "A", 2, note="Baratie (ch. 63)")
fight(0.133, "eastblue", "luffy", "don_krieg", "A", 2, note="Baratie (ch. 64-67)")
fight(0.2, "eastblue", "usopp", "chew", "A", 1, note="Arlong Park (ch. 84-86)")
fight(0.201, "eastblue", "zoro", "hachi", "A", 2, ta=["epuise"], note="Zoro encore blessé par Mihawk (ch. 84-86)")
fight(0.202, "eastblue", "sanji", "kuroobi", "A", 2, note="Arlong Park (ch. 87-88)")
fight(0.203, "eastblue", "luffy", "arlong", "A", 2, note="Arlong Park (ch. 89-93)")
fight(0.35, "eastblue", "zoro", "tashigi", "A", 2, ta=["retenue"], note="Loguetown, Zoro la maîtrise, lame sous la gorge, et l'épargne (ch. 100)")
fight(0.351, "eastblue", "smoker", "luffy", "A", 3, note="Loguetown, Dragon intervient (ch. 100)", flags="i")

# ================================================================ Alabasta saga
fight(0.41, "alabasta", "zoro", "baroque_works_agents", "A", 3, note="Whisky Peak, cent chasseurs de primes (ch. 108)")
fight(0.411, "alabasta", "luffy", "zoro", "D", note="Whisky Peak, Nami les arrête (ch. 110)", flags="i")
fight(0.412, "alabasta", "luffy", ["mr_5", "miss_valentine"], "A", 3, note="Whisky Peak (ch. 112)")
fight(0.42, "alabasta", "dorry", "brogy", "D", note="Little Garden, duel centenaire sans vainqueur (ch. 116)")
fight(0.4205, "alabasta", "mr_3", "brogy", "A", 2, ta=["surprise"], note="Little Garden, Mr. 3 révèle son rôle et fige les pieds de Brogy dans la cire (ch. 120)")
fight(0.421, "alabasta", ["mr_3", "miss_goldenweek"], ["zoro", "nami", "vivi"], "A", 2, ta=["prepa"],
      note="Little Garden, gâteau de cire (ch. 123-125)")
fight(0.4215, "alabasta", ["nami", "vivi"], "miss_valentine", "A", 2, note="Little Garden, elles surgissent des flammes et l'abattent (ch. 126)")
fight(0.4216, "alabasta", ["usopp", "zoro"], "mr_5", "A", 2, note="Little Garden, Mr. 5 avale l'Étoile tabasco d'Usopp, Zoro l'abat (ch. 126)")
fight(0.422, "alabasta", "luffy", "mr_3", "A", 2, note="Little Garden, Candle Champion brûlé puis coup de pied au visage (ch. 125-126)")
fight(0.44, "alabasta", "chopper", ["chess", "kuromarimo"], "A", 2, note="Drum, Chessmarimo assommé (Brain Point) (ch. 148-149)")
fight(0.441, "alabasta", "luffy", "wapol", "A", 3, note="Drum (ch. 149-151)")
fight(0.46, "alabasta", "ace", "smoker", "D", note="Nanohana, Ace retient Smoker (ch. 158)", flags="i")
fight(0.461, "alabasta", "ace", "baroque_works_agents", "A", 3, note="Hiken, cinq navires des Billions (ch. 159)")
fight(0.48, "alabasta", "crocodile", "luffy", "A", 3, note="Premier duel, Luffy desséché (ch. 177-178)")
fight(0.49, "alabasta", ["usopp", "chopper"], ["mr_4", "miss_merry_christmas"], "A", 1, note="Alubarna (ch. 182-185)")
fight(0.491, "alabasta", "sanji", "bon_clay", "A", 2, note="Alubarna (ch. 186-188)")
fight(0.492, "alabasta", "nami", "miss_doublefinger", "A", 1, note="Clima-Tact (ch. 190-191)")
fight(0.493, "alabasta", "zoro", "mr_1", "A", 1, note="Zoro tranche l'acier (ch. 193-195)")
fight(0.5, "alabasta", "crocodile", "luffy", "A", 2, tb=["prepa"], note="Deuxième duel, Luffy utilise l'eau (ch. 199-200)")
fight(0.51, "alabasta", "luffy", "crocodile", "A", 1, ta=["prepa"], note="Troisième duel, dans le tombeau (ch. 207-211)")

# ================================================================ Jaya, Skypiea
fight(0.55, "skypiea", "luffy", "bellamy", "A", 3, note="Mock Town, un seul coup (ch. 233)")
fight(0.58, "skypiea", ["luffy", "usopp", "sanji"], "satori", "A", 2, note="Épreuve des boules ; Sanji l'achève (Concassé) (ch. 246-248)")
fight(0.59, "skypiea", "shura", "gan_fall", "A", 2, note="Shura attaque le Merry gardé par Chopper ; Gan Fall arrive et tombe sous la lance (ch. 247-249)")
fight(0.61, "skypiea", "wyper", "shura", "A", 2, note="Jeu de survie, Reject dial, premier éliminé (ch. 256)")
fight(0.612, "skypiea", "chopper", "gedatsu", "A", 2, note="Chopper arrache un dial de sa chaussure, Gedatsu tombe dans son propre marais (ch. 262)")
fight(0.613, "skypiea", "robin", "yama", "A", 3, note="Cien Fleur Delphinium puis Clutch (ch. 265)")
fight(0.614, "skypiea", "ohm", "chopper", "A", 3, note="Ohm abat Chopper à distance (ch. 266)")
fight(0.62, "skypiea", "zoro", "ohm", "A", 1, note="Épreuve de fer, Hyakuhachi Pound Ho (ch. 268-271)")
fight(0.63, "skypiea", "enel", "wyper", "A", 2, note="Reject dial, Enel relance son cœur puis transperce Wyper (ch. 275-276)")
fight(0.631, "skypiea", "enel", ["zoro", "robin", "gan_fall"], "A", 3, note="Enel foudroie Gan Fall, Robin et Zoro (ch. 274-276)")
fight(0.65, "skypiea", "enel", "sanji", "A", 3, tb=["protege"], note="Arche Maxim, Sanji encaisse un El Thor pour couvrir Nami et Usopp (ch. 284)")
fight(0.64, "skypiea", "enel", "luffy", "A", 1, tb=["contre"],
      note="Caoutchouc contre foudre, mais Enel jette Luffy hors de l'arche avec une boule d'or (ch. 279-282)")
fight(0.66, "skypiea", "luffy", "enel", "A", 2, ta=["contre"], note="Gold Rifle (ch. 297-300)")

# ================================================================ Long Ring Long Land, Water 7, Enies Lobby
fight(0.7, "water7", ["zoro", "sanji"], "groggy_monsters", "A", 2, note="Davy Back Fight, Groggy Ring (ch. 310-312)")
fight(0.701, "water7", "luffy", "foxy", "A", 2, note="Davy Back Fight, combat final (ch. 316-318)")
fight(0.702, "water7", "aokiji", ["luffy", "zoro", "sanji"], "A", 3, note="Long Ring Long Land (ch. 320-321)")
fight(0.703, "water7", "aokiji", "luffy", "A", 3, note="Duel, Luffy gelé (ch. 321)")
fight(0.71, "water7", "franky_family", "usopp", "A", 3, note="Usopp tabassé hors champ, argent volé (ch. 328)")
fight(0.711, "water7", ["luffy", "zoro"], "franky_family", "A", 3, note="Assaut de la Franky House (ch. 330-332)")
fight(0.712, "water7", "luffy", "usopp", "A", 3, note="Duel pour le Vogue Merry (ch. 334)")
fight(0.716, "water7", "lucci", ["luffy", "zoro"], "A", 3, note="Galley-La, Tekkai et Shigan, Luffy et Zoro projetés dans la ville (ch. 347-349)")
fight(0.72, "water7", "sanji", "wanze", "A", 2, note="Sea Train (ch. 368-369)")
fight(0.721, "water7", "franky", "nero", "A", 3, note="Sea Train, Nero projeté à travers un wagon (ch. 370-373)")
fight(0.722, "water7", "zoro", "t_bone", "A", 3, note="Rocket Man, T-Bone abattu d'un coup (Gyuki Yuzume) (ch. 371)")
fight(0.73, "water7", "luffy", "blueno", "A", 2, ta=["eveil"], note="Première utilisation du Gear 2 (ch. 387-388)")
fight(0.731, "water7", "kalifa", "sanji", "A", 2, tb=["retenue"], note="Sanji refuse de frapper une femme (ch. 402-403)")
fight(0.732, "water7", "kumadori", "chopper", "A", 2, note="Rumble Ball prématurée, Chopper d'abord battu (ch. 406-407)")
fight(0.733, "water7", "franky", "fukurou", "A", 2, note="Coup de Vent (ch. 404-406)")
fight(0.734, "water7", "chopper", "kumadori", "A", 2, ta=["eveil"], note="Monster Point, trois Rumble Balls (ch. 407-408)")
fight(0.735, "water7", "nami", "kalifa", "A", 1, note="Thunder Lance Tempo (ch. 411)")
fight(0.736, "water7", "sanji", "jabra", "A", 2, note="Première Diable Jambe (ch. 413-415)")
fight(0.737, "water7", "zoro", "kaku", "A", 2, note="Asura Ichibugin (ch. 416-417)")
fight(0.74, "water7", "luffy", "lucci", "A", 1, ta=["eveil"], note="Gear 2 et Gear 3, Jet Gatling final (ch. 419-427)")
fight(0.741, "water7", "robin", "spandam", "A", 3, note="Robin se venge de Spandam (ch. 428-429)")
fight(0.775, "water7", "shanks", "whitebeard", "D", ta=[], tb=[],
      note="Shanks rend visite à Barbe Blanche, choc de Haki (ch. 434)", flags="i")
fight(0.78, "water7", "blackbeard", "ace", "A", 1, note="Banaro (ch. 440-441)")

# ================================================================ Thriller Bark
fight(0.812, "thriller", "ryuma_zombie", "brook", "A", 2, note="Revanche de Brook contre le zombie porteur de son ombre, transpercé deux fois (ch. 458-459)")
fight(0.81, "thriller", "moria", ["luffy", "zoro", "sanji"], "A", 2, ta=["surprise"], note="Moria vole leurs ombres (ch. 459-461)")
fight(0.82, "thriller", "usopp", "perona", "A", 2, ta=["contre"], note="Usopp immunisé contre les fantômes négatifs (ch. 465-466)")
fight(0.821, "thriller", "zoro", "ryuma_zombie", "A", 2, note="Duel des sabreurs (ch. 466-468)")
fight(0.815, "thriller", "sanji", "absalom", "A", 2, note="Cathédrale, Extra Hachis malgré l'invisibilité (ch. 463-464)")
fight(0.823, "thriller", ["robin", "chopper"], "hogback", "A", 3, note="Hogback (ch. 468-469)")
fight(0.83, "thriller", ["luffy", "zoro", "sanji", "usopp", "chopper", "franky", "robin", "nami", "brook"], "oars_zombie", "A", 2,
      note="Le géant zombie à l'ombre de Luffy (ch. 473-476)")
fight(0.84, "thriller", "luffy", "moria", "A", 1, ta=["boost"], note="Nightmare Luffy, cent ombres (ch. 478-482)")
fight(0.85, "thriller", "kuma", ["luffy", "zoro", "sanji", "usopp", "chopper", "franky", "robin", "nami", "brook"], "A", 3,
      ta=["retenue"], tb=["epuise"], note="Ursus Shock, Zoro prend la douleur de Luffy (ch. 484-485)")

# ================================================================ Sabaody
fight(0.9, "marineford", "sanji", "duval", "A", 3, note="Rosy Life Riders, coup de pied qui refait le visage de Duval (ch. 494)")
fight(0.901, "marineford", "luffy", "charloss", "A", 3, note="Hôtel des ventes (ch. 502)")
fight(0.902, "marineford", "rayleigh", "marines_ordinaires", "A", 3, note="Haki des rois, gardes assommés (ch. 503)")
fight(0.903, "marineford", ["luffy", "law", "kid"], "marines_ordinaires", "A", 3, note="Sortie de l'hôtel des ventes (ch. 504)")
fight(0.904, "marineford", "kizaru", "urouge", "A", 3, note="Coup de pied à la vitesse de la lumière (ch. 509-510)")
fight(0.9041, "marineford", "kizaru", "hawkins", "A", 3, note="Aveuglé par la lumière (ch. 509-510)")
fight(0.9042, "marineford", "kizaru", "drake", "A", 3, note="Allosaure blessé, abattu ensuite (ch. 509-510)")
fight(0.9043, "marineford", "kizaru", "apoo", "A", 3, note="Apoo coupe le bras de Kizaru et le fait tomber, puis est abattu (ch. 509-510)")
fight(0.9035, "marineford", "drake", "pacifista", "D", note="Hache puis morsure d'allosaure sur un Pacifista, le laser lui perce l'épaule (ch. 508-509)", flags="i")
fight(0.905, "marineford", ["luffy", "zoro", "sanji", "usopp", "chopper", "franky", "robin", "nami", "brook"], "pacifista", "A", 1,
      tb=["contre"], note="Pacifista abattu de justesse, Gigant Rifle final (ch. 508-510)")
fight(0.906, "marineford", "sentomaru", "luffy", "A", 2, ta=["contre"], tb=["epuise"], note="Haki, Luffy projeté (ch. 508-509)")
fight(0.907, "marineford", "kizaru", "zoro", "A", 3, tb=["epuise"], note="Rayleigh sauve Zoro (ch. 509)")
fight(0.908, "marineford", "rayleigh", "kizaru", "D", note="Duel au sabre, interrompu par la fuite des Chapeaux de paille (ch. 510-511)", flags="i")
fight(0.909, "marineford", "kuma", ["luffy", "zoro", "sanji", "usopp", "chopper", "franky", "robin", "nami", "brook"], "A", 3,
      ta=["retenue"], tb=["epuise"], note="Kuma disperse l'équipage (ch. 511-513)")

# ================================================================ Amazon Lily
fight(0.915, "marineford", "luffy", ["sandersonia", "marigold"], "A", 2, note="Arène de Kuja (ch. 519-520)")

# ================================================================ Impel Down
fight(0.92, "marineford", "hancock", "gardes_impel_down", "A", 3, note="Hancock pétrifie Domino et les gardes (ch. 525)")
fight(0.921, "marineford", "luffy", "minotaurus", "A", 2, note="Avec Bon Clay, niveau 3 (ch. 531-532)")
fight(0.922, "marineford", "hannyabal", ["buggy", "mr_3"], "A", 3, note="Niveau 3, combat hors champ, Hannyabal debout sur eux (ch. 534-535)")
fight(0.923, "marineford", "magellan", "luffy", "A", 3, ta=["contre"], note="Poison, Luffy à l'agonie (ch. 533-535)")
fight(0.928, "marineford", ["luffy", "jinbe", "crocodile"], "gardes_impel_down", "A", 3, note="Remontée du niveau 4 (ch. 541-542)")
fight(0.9281, "marineford", "ivankov", "sadi", "A", 2, note="Niveau 4, Ivankov saisit son fouet et la laisse ligotée (ch. 543)")
fight(0.9282, "marineford", "luffy", "hannyabal", "A", 1, note="Jet Gatling, Hannyabal se relève, Barbe Noire arrive (ch. 543)", flags="i")
fight(0.9283, "marineford", "blackbeard", "hannyabal", "A", 3, note="Barbe Noire écrase Hannyabal (ch. 543)")
fight(0.9284, "marineford", "luffy", "blackbeard", "D", note="Gear 2 contre Yami Yami, Jinbe arrête Luffy (ch. 544)", flags="i")
fight(0.9285, "marineford", "magellan", "blackbeard_pirates", "A", 2, note="Hydra empoisonne Barbe Noire et son équipage (ch. 544)")
fight(0.929, "marineford", ["luffy", "mr_3"], "magellan", "A", 1, note="Mur de cire et Gigant Stamp, fuite (ch. 546-547)", flags="i")

# ================================================================ Marineford (ch. 550-580)
fight(0.94, "marineford", "whitebeard", "aokiji", "A", 2, note="Ice Age arrêté par un séisme, Kuzan empalé (ch. 553-554)", flags="i")
fight(0.9401, "marineford", "marco", "kizaru", "D", note="Duel aérien (ch. 554-555)", flags="i")
fight(0.9402, "marineford", ["kuma", "doflamingo", "moria"], "oars_jr", "A", 2,
      note="Oars jr. abattu (Ursus Shock, jambe coupée, lance d'ombre) (ch. 555)")
fight(0.9403, "marineford", "jinbe", "moria", "A", 2, note="Samegawara Seiken, Moria au tapis (ch. 559)")
fight(0.9404, "marineford", "smoker", "luffy", "A", 1, note="Smoker plaque Luffy au jitte, Hancock intervient (ch. 559)", flags="i")
fight(0.9405, "marineford", "hancock", "smoker", "A", 2, note="Hancock repousse Smoker et brise son jitte (ch. 559-560)", flags="i")
fight(0.9406, "marineford", "jozu", "crocodile", "A", 1, note="Coup de poing qui envoie Crocodile au loin, Doflamingo bloque la suite (ch. 560)", flags="i")
fight(0.9407, "marineford", "ivankov", "kuma", "D", note="Face Spectrum et Galaxy Wink contre Kuma, sans issue montrée (ch. 560)", flags="i")
fight(0.9408, "marineford", "mihawk", "luffy", "A", 1, ta=["retenue"], note="Luffy fuit plutôt que perdre un bras, Baggy en bouclier (ch. 561)", flags="i")
fight(0.9409, "marineford", "vista", "mihawk", "D", tb=["retenue"], note="Vista intercepte Mihawk (ch. 561-562)", flags="i")
fight(0.941, "marineford", "squard", "whitebeard", "A", 1, ta=["surprise"],
      note="Squard poignarde Barbe Blanche, qui le pardonne (ch. 562-563)")
fight(0.9411, "marineford", "crocodile", "doflamingo", "D", note="Doflamingo décapite Crocodile, qui se reforme et contre-attaque (ch. 566)", flags="i")
fight(0.9412, "marineford", "aokiji", "luffy", "A", 2, note="Sabre de glace (ch. 566)", flags="i")
fight(0.9413, "marineford", "kizaru", "luffy", "A", 3, tb=["epuise"], note="Kizaru écarte Luffy d'un coup de pied, deux fois ; Luffy s'effondre (ch. 566-567)")
fight(0.942, "marineford", "garp", "marco", "A", 2, note="Garp abat Marco en forme de phénix (ch. 567)")
fight(0.9421, "marineford", ["kizaru", "onigumo"], "marco", "A", 2, ta=["surprise"],
      note="Kizaru transperce Marco qui protège Barbe Blanche, puis menottes en granit marin d'Onigumo (ch. 568-569)")
fight(0.9422, "marineford", "aokiji", "jozu", "A", 2, note="Bras gelé, puis Jozu gelé en entier (ch. 567-569)")
fight(0.9423, "marineford", "luffy", "koby", "A", 3, note="Luffy lit son Soru et l'abat d'un coup (ch. 569)")
fight(0.9424, "marineford", "luffy", "marines_ordinaires", "A", 3, note="Éveil du Haki des rois de Luffy, bourreaux assommés (ch. 569)")
fight(0.9425, "marineford", "mihawk", "mr_1", "A", 3, note="Mr. 1 bloque Mihawk pour Luffy et tombe (ch. 570)")
fight(0.9431, "marineford", "luffy", "garp", "A", 1, tb=["retenue"], note="Garp se laisse frapper (ch. 571)")
fight(0.9432, "marineford", ["luffy", "mr_3"], "sengoku", "D", note="Gigant Fusen et mur de cire retiennent le poing de Bouddha, l'échafaud s'effondre (ch. 571)", flags="i")
fight(0.9433, "marineford", "ace", "aokiji", "D", note="Mur de flammes contre glace (ch. 572)", flags="i")
fight(0.9494, "marineford", "akainu", "ace", "A", 3, ta=["contre"], note="Le magma consume le feu (ch. 574)")
fight(0.9495, "marineford", "akainu", ["ace", "luffy"], "A", 3, tb=["protege"], note="Ace meurt en protégeant Luffy (ch. 574)")
fight(0.9496, "marineford", "whitebeard", "akainu", "A", 1, tb=["epuise"],
      note="Barbe Blanche perd la moitié du visage mais fend l'île et projette Akainu dans la faille (ch. 575)")
fight(0.952, "marineford", "blackbeard_pirates", "whitebeard", "A", 1, tb=["epuise"],
      note="Barbe Blanche étrangle Teach, puis meurt sous les balles de son équipage (ch. 576)")
fight(0.9521, "marineford", "akainu", ["jinbe", "luffy"], "A", 3, tb=["epuise"], note="Poing de magma à travers Jinbe (ch. 577-578)")
fight(0.9522, "marineford", "akainu", ["marco", "vista"], "D", note="Marco et Vista s'interposent entre Akainu et Luffy (ch. 578)", flags="i")
fight(0.9523, "marineford", "crocodile", "akainu", "D", note="Vague de sable, Akainu coupé en deux (ch. 578)", flags="i")
fight(0.9524, "marineford", "sengoku", "blackbeard", "D", note="Bouddha écrase deux fois les séismes de Teach et disperse son équipage (ch. 578)", flags="i")
fight(0.9525, "marineford", "shanks", "akainu", "D", note="Shanks bloque le poing d'Akainu visant Koby, fin de la guerre (ch. 579)", flags="i")

# ================================================================ après-guerre
fight(0.96, "marineford", "blackbeard_pirates", "magellan", "A", 2,
      note="Pendant l'évasion du niveau 6, Magellan battu à mort par l'équipage de Teach, puis rétrogradé (hors champ ; arrivée de Teach avec ses recrues ch. 575, chapitre de la révélation non trouvé)", flags="?")
fight(1.5, "marineford", "akainu", "aokiji", "A", 1,
      note="Dix jours de combat à Punk Hazard pour le poste d'amiral en chef (ellipse, révélé par Jinbe ch. 650)")
