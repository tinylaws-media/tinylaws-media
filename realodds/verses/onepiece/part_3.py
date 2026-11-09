# Partie 3 : après Wano (suites de la Rêverie, Hachinosu), Egghead, Elbaf jusqu'au ch. 1198 (8 nov. 2026),
# plus les flash-backs révélés dans ces chapitres qui ne sont pas déjà dans part_1 (God Valley y est déjà codé).
# Manga uniquement. Temps : post-Wano 2.45-2.49, Egghead/Hachinosu 2.50-2.549 (Saturn meurt à 2.55, ch. 1125), Elbaf 2.60-2.70.
# Flash-backs : ère de Rocks vers -40, God Valley -38, mort de Harald -14 (« il y a 14 ans », ch. 1137/1168).
# Rem. : on suit l'id "koby" déjà utilisé dans part_1 (et non "coby").
# fight() est injectée par data.py.

CHARS_PART = {
    # ---- Chapeau de paille et alliés
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
    "bonney": ("Jewelry Bonney", "Pirates de Bonney", 4.0, None, None),
    "law": ("Trafalgar Law", "Pirates du Heart", 4.0, None, None),
    "kid": ("Eustass Kid", "Pirates de Kid", 4.0, None, None),
    "killer": ("Killer", "Pirates de Kid", 3.5, None, None),
    "bartolomeo": ("Bartolomeo", "Pirates du Barto Club", 4.5, None, None),
    # ---- Géants d'Elbaf
    "dorry": ("Dorry", "Pirates guerriers géants", 5.0, None, None),
    "brogy": ("Brogy", "Pirates guerriers géants", 5.0, None, None),
    "oimo": ("Oimo", "Pirates guerriers géants", 4.0, None, None),
    "kashii": ("Kashii", "Pirates guerriers géants", 4.0, None, None),
    "hajrudin": ("Hajrudin", "Pirates des Géants", 4.0, None, None),
    "saul": ("Jaguar D. Saul", "Elbaf", 4.5, None, None),
    "jarul": ("Jarul", "Elbaf", 5.0, None, None),
    "loki": ("Loki (prince d'Elbaf)", "Elbaf", 3.5, None, None),
    "harald": ("Harald (roi d'Elbaf)", "Elbaf / Chevaliers divins", 7.0, -13.999, None),
    "gaban": ("Scopper Gaban", "Pirates de Roger", 6.5, None, None),
    # ---- Gouvernement, Marine, Chevaliers divins
    "imu": ("Imu", "Gouvernement mondial", 8.5, None, None),
    "saturn": ("Saint Jaygarcia Saturn", "Doyens (Gorosei)", 7.0, 2.55, None),
    "mars": ("Saint Marcus Mars", "Doyens (Gorosei)", 7.0, None, None),
    "warcury": ("Saint Topman Warcury", "Doyens (Gorosei)", 7.0, None, None),
    "nusjuro": ("Saint Ethanbaron V. Nusjuro", "Doyens (Gorosei)", 7.0, None, None),
    "ju_peter": ("Saint Shepherd Ju Peter", "Doyens (Gorosei)", 7.0, None, None),
    "gunko": ("Sainte Gunko", "Chevaliers divins", 6.0, None, None),
    "shamrock": ("Saint Figarland Shamrock", "Chevaliers divins", 6.5, None, None),
    "sommers": ("Saint Shepherd Sommers", "Chevaliers divins", 5.0, None, None),
    "killingham": ("Saint Killingham", "Chevaliers divins", 5.5, None, None),
    "kizaru": ("Borsalino (Kizaru)", "Marine", 6.0, None, None),
    "akainu": ("Sakazuki (Akainu)", "Marine", 6.0, None, None),
    "garp": ("Monkey D. Garp", "Marine", 7.5, None, None),
    "koby": ("Koby", "Marine", 2.0, None, None),
    "hibari": ("Hibari", "Marine (SWORD)", 2.5, None, None),
    "sentomaru": ("Sentomaru", "Marine", 4.0, None, None),
    "doll": ("Doll (vice-amirale)", "Marine", 4.0, None, None),
    "bluegrass": ("Bluegrass (vice-amiral)", "Marine", 4.0, None, None),
    "lucci": ("Rob Lucci", "CP0", 3.0, None, None),
    "kaku": ("Kaku", "CP0", 3.0, None, None),
    "stussy": ("Stussy", "CP0 / MADS", 4.0, None, None),
    "atlas": ("Vegapunk Atlas", "Vegapunk", 2.5, 2.549, None),
    "emet": ("Emet (Géant de fer)", "Joy Boy (robot ancien)", 7.0, None, None),
    # ---- Pirates
    "blackbeard": ("Marshall D. Teach (Barbe Noire)", "Pirates de Barbe Noire", 4.5, None, None),
    "aokiji": ("Kuzan (Aokiji)", "Marine puis Pirates de Barbe Noire", 6.0, None, None),
    "pizarro": ("Avalo Pizarro", "Pirates de Barbe Noire", 5.5, None, None),
    "sanjuan_wolf": ("Sanjuan Wolf", "Pirates de Barbe Noire", 5.0, None, None),
    "hancock": ("Boa Hancock", "Pirates Kuja", 4.0, None, None),
    "shanks": ("Shanks le Roux", "Pirates du Roux", 7.0, None, None),
    "yasopp": ("Yasopp", "Pirates du Roux", 5.5, None, None),
    "crocodile": ("Sir Crocodile", "Cross Guild", 4.0, None, None),
    "mihawk": ("Dracule Mihawk", "Cross Guild", 6.5, None, None),
    "buggy": ("Baggy le Clown", "Cross Guild", 1.5, None, None),
    "sabo": ("Sabo", "Armée révolutionnaire", 1.0, None, None),
    "kuma": ("Bartholomew Kuma", "Armée révolutionnaire", 2.5, None, None),
    # ---- Ère de Rocks / God Valley
    "rocks": ("Rocks D. Xebec", "Pirates de Rocks", 8.0, -37.987, None),
    "kaido": ("Kaido", "Pirates de Rocks puis aux Cent Bêtes", 4.5, None, None),
    "ganzui": ("Ganzui", "Pirates de Rocks", 5.5, None, None),
    "john": ("Capitaine John", "Pirates de Rocks", 5.0, None, None),
}
GENERIC_PART = set()

JUMPS_PART = [
    ("lucci", 2.499, 0.5, 0.5, "Éveil du fruit Neko Neko (Léopard) révélé à Egghead"),
    ("bonney", 2.531, 1.0, 0.8, "Distorsion du futur : forme Nika"),
    ("zoro", 2.68, 0.3, 0.4, "Haki des rois enfin maîtrisé contre Sommers (ch. 1194)"),
    ("sanji", 2.69, 0.5, 0.5, "Éveil du Haki des rois contre Killingham (ch. 1197)"),
    ("loki", -20.0, 2.0, 1.0, "Loki enfant devenu adulte (géant)"),
    ("loki", -14.01, 1.0, 0.8, "Mange le fruit gardé par Ragnir (Zoan Nidhöggr)"),
    ("garp", 2.514, -0.3, 0.4, "Âge et blessures (Hachinosu, il dit avoir perdu en puissance)"),
]

# ================================================================ flash-backs : ère de Rocks
fight(-40.0, "godvalley", "rocks", "harald", "D", ta=[], tb=[],
      note="Choc de Haki des rois en Terre sainte, tout est rasé sur 5 km, sans vainqueur ; Rocks quitte la Red Line (ch. 1155)")
fight(-39.8, "godvalley", "rocks", "kaido", "A", 3, note="Kaido jeune propose de battre le roi, Rocks le frappe (ch. 1156)")
fight(-39.79, "godvalley", "roger", "garp", "D", note="Roger lâche tout pour échanger des coups avec Garp, sans issue montrée (ch. 1156)", flags="i")
fight(-39.5, "godvalley", "rocks", "harald", "D", ta=[], tb=[],
      note="Duel Rocks contre Harald, impasse, fin de leur amitié (ch. 1158)")
fight(-39.0, "godvalley", "rocks", "loki", "A", 3,
      note="Loki enfant se jette sur Rocks à Elbaf et est écarté sans effort (ch. 1155)")
fight(-38.1, "godvalley", "harald", "rocks", "D", note="Bref choc, Rocks s'échappe ; Harald refuse de l'aider (ch. 1159)", flags="i")
# ================================================================ flash-backs : God Valley (compléments à part_1)
fight(-37.9965, "godvalley", "whitebeard", "maffey", "A", 3,
      note="Un coup perdu de Newgate tranche Maffey en deux et sauve Dragon ; elle se régénère et repart avec Shamrock (ch. 1161)")
fight(-37.991, "godvalley", "john", "dragon", "A", 3, note="John attire métal et hommes armés à lui et assomme Dragon qui portait Shanks (ch. 1163)")
fight(-37.9905, "godvalley", "ganzui", "john", "A", 2, ta=["surprise"],
      note="John trahit l'équipage, Ganzui l'assomme avec le Bomu Bomu (ch. 1163)")
fight(-37.9895, "godvalley", "rocks", "whitebeard", "D", ta=["boost"],
      note="Rocks démonisé par Imu et Newgate échangent à égalité, le pic nord-est s'effondre (ch. 1164)", flags="i")
# ================================================================ flash-back : mort de Harald (il y a 14 ans)
fight(-14.02, "oden", "harald", "jarul", "A", 2, ta=["boost"],
      note="Harald, corrompu par Imu, massacre les gardes et plante une épée dans le casque de Jarul (ch. 1169)")
fight(-14.015, "oden", ["shanks", "gaban"], "harald", "D", tb=["boost"],
      note="Shanks et Gaban affaiblissent Harald immortel sans l'achever (ch. 1169-1170)", flags="i")
fight(-14.0, "oden", "loki", "harald", "A", 2, ta=["boost"], tb=["boost"],
      note="Loki, transformé par le fruit, brise Harald d'un éclair chargé de Haki des rois (ch. 1170)")

# ================================================================ après Wano : Rêverie, Cross Guild, Barbe Noire
fight(2.45, "wano", "imu", "sabo", "A", 2,
      note="Rêverie : Imu et les Doyens attaquent Sabo, Imu absorbe son feu, Cobra meurt, Sabo fuit (ch. 1085-1086)")
fight(2.451, "wano", "akainu", "kuma", "A", 1, tb=["epuise"],
      note="Kuma (cyborg) saccage Marie-Joie ; Akainu lui arrache une jambe, Kuma s'échappe gravement blessé (ch. 1092)")
fight(2.46, "wano", "blackbeard", "hancock", "A", 2,
      note="Amazon Lily : Teach la saisit à la gorge et annule son pouvoir ; Rayleigh s'interpose (ch. 1059)", flags="i")
fight(2.465, "wano", "blackbeard", "law", "A", 2, ta=["prepa"],
      note="Île Winner : Law tranche le Stronger et blesse Teach de l'intérieur, mais Teach gagne, Bepo emporte Law (ch. 1063-1064, 1081)")

# ================================================================ Egghead (1re partie) et Hachinosu
fight(2.5000, "egghead", "lucci", "atlas", "A", 3, note="Rokuogan en forme hybride éveillée, Atlas inconsciente (ch. 1068-1069)")
fight(2.5008, "egghead", "lucci", "sentomaru", "A", 2, note="Lucci empale Sentomaru (ch. 1069-1070)")
fight(2.5016, "egghead", "luffy", "lucci", "A", 2, ta=[],
      note="Gear 5 contre Zoan éveillé : Dawn Whip puis Dawn Rocket (ch. 1069-1070)")
fight(2.5080, "egghead", "stussy", ["kaku", "lucci"], "A", 2, ta=["surprise"],
      note="Stussy (MADS) vide Kaku de son sang et entrave Lucci au granit marin (ch. 1073)")
fight(2.5120, "egghead", "shanks", ["kid", "killer"], "A", 3, ta=[],
      note="Près d'Elbaf : Kamusari d'un seul coup, Dorry et Brogy coulent le Victoria Punk (ch. 1079)")
fight(2.5144, "egghead", "aokiji", "hibari", "A", 3, note="Hachinosu : Kuzan gèle Hibari (ch. 1081)")
fight(2.5160, "egghead", "garp", "sanjuan_wolf", "A", 3, ta=[], note="Hachinosu : Garp jette Wolf à la mer (ch. 1087)")
fight(2.5168, "egghead", "garp", "pizarro", "A", 2, ta=[],
      note="Galaxy Divide fend le crâne de pierre et blesse le vrai corps de Pizarro (ch. 1088)")
fight(2.5176, "egghead", "koby", "pizarro", "D", note="Honesty Impact tranche la main de pierre géante, sans toucher Pizarro lui-même (ch. 1088)", flags="i")
fight(2.5184, "egghead", "aokiji", "garp", "A", 1, tb=["protege"],
      note="Garp domine d'abord (Blue Hole, ch. 1081), poignardé par Shiryu en protégeant Koby, puis empalé et gelé par Kuzan et capturé (ch. 1081-1088)")

# ================================================================ Egghead (Kizaru, Saturn, Kuma)
fight(2.5240, "egghead", "kizaru", "sentomaru", "A", 2, note="Rayon laser, Sentomaru inconscient (ch. 1090-1091)")
fight(2.5248, "egghead", "kizaru", "luffy", "A", 2, note="Luffy en Gear 4 : Kizaru bloque tout et l'envoie dans la barrière (ch. 1092)")
fight(2.5250, "egghead", "kizaru", "bonney", "A", 3, ta=["retenue"], note="Kizaru esquive Toshi Tsuki et l'envoie dans la barrière (ch. 1092)")
fight(2.5256, "egghead", "luffy", "kizaru", "A", 1, ta=[], tb=["retenue"],
      note="Gear 5 : coup critique à la tête, Kizaru hors de combat un moment ; Luffy épuisé ensuite (ch. 1092-1094)")
fight(2.5264, "egghead", "saturn", "bonney", "A", 3, note="Bonney le poignarde, il se régénère et l'écrase (ch. 1094-1095, 1103)")
fight(2.5266, "egghead", "saturn", "sanji", "A", 2, note="Saturn met Sanji au tapis (ch. 1094-1095)")
fight(2.5320, "egghead", "kuma", "saturn", "A", 1, tb=["surprise"],
      note="Kuma encaisse pour Bonney et projette Saturn à travers plusieurs bâtiments ; Saturn se régénère (ch. 1103-1104)", flags="i")
fight(2.5360, "egghead", "luffy", "saturn", "A", 2, ta=[], note="Dawn Gatling, Saturn projeté au loin (ch. 1106-1107)")
fight(2.5368, "egghead", "kizaru", "sanji", "A", 2, note="Kizaru écarte Sanji puis transperce Vegapunk (ch. 1107-1108)")
fight(2.5376, "egghead", "luffy", ["kizaru", "saturn"], "A", 2, ta=[], tb=["retenue"],
      note="Luffy géant aplatit Kizaru et Saturn en disques et les projette (ch. 1108-1109)")
fight(2.5400, "egghead", "zoro", "lucci", "A", 2,
      note="Long duel conclu par Kokoba Madara Gari, Lucci tombe (ch. 1091-1110)")
# ================================================================ Egghead (les Doyens)
fight(2.5408, "egghead", ["dorry", "brogy"], "ju_peter", "A", 1,
      note="Ju Peter (ver des sables) avale Luffy, les deux géants le décapitent ; il se régénère (ch. 1110)", flags="i")
fight(2.5416, "egghead", ["dorry", "brogy"], "warcury", "A", 1,
      note="Svalinn Sun-Shield puis Skilja Split repoussent Warcury (ch. 1111)", flags="i")
fight(2.5424, "egghead", "warcury", "luffy", "A", 1, ta=[], tb=[],
      note="Le rugissement de Warcury défait l'aspect caoutchouc ; Red Roc se brise sur son crâne (ch. 1111-1112)", flags="i")
fight(2.5432, "egghead", "sanji", "nusjuro", "D",
      note="Sanji fait saigner Nusjuro, qui le saisit ; Oimo et Kashii le plaquent (ch. 1113)", flags="i")
fight(2.5440, "egghead", "saturn", ["nami", "chopper", "usopp", "brook"], "A", 2,
      note="Saturn traverse le groupe pour atteindre la salle de la Mother Flame (ch. 1113-1114)")
fight(2.5448, "egghead", ["zoro", "jinbe"], "nusjuro", "D",
      note="Rashomon de Zoro lancé par Jinbe contre la taille de Nusjuro, les deux reculent (ch. 1117)", flags="i")
fight(2.5456, "egghead", "doll", "kashii", "A", 2, note="Rock 'n' Roll Blaster (ch. 1117)")
fight(2.5464, "egghead", "bonney", ["doll", "bluegrass"], "A", 2, ta=["boost"],
      note="Bonney rajeunit les deux vice-amiraux en enfants (ch. 1118)")
fight(2.5480, "egghead", "warcury", "emet", "A", 2,
      note="Emet retient les Doyens, Ju Peter lui arrache un bras, Warcury l'écrase et broie l'escargophone (ch. 1120-1122)")
fight(2.5488, "egghead", "emet", ["mars", "warcury", "nusjuro", "ju_peter"], "A", 2, ta=[],
      note="Vague de Haki des rois scellée par Joy Boy : Doyens privés de leurs formes, trois projetés à Marie-Joie ; les Chapeaux de paille s'échappent (ch. 1122)")

# ================================================================ Elbaf
fight(2.60, "elbaf", "yasopp", "bartolomeo", "A", 3,
      note="L'équipage du Roux soumet le Barto Club à Gartel, Yasopp pulvérise le navire d'un tir (ch. 1126)")
fight(2.62, "elbaf", "gaban", "luffy", "A", 1, ta=["retenue"],
      note="Gaban domine (Yasotakeru) puis cède la clé quand Luffy passe en Gear 5 (ch. 1140, 1151)", flags="i")
fight(2.625, "elbaf", ["gunko", "shamrock"], "loki", "A", 2, tb=["epuise"],
      note="Loki, à peine libéré de ses chaînes et blessé, s'effondre sous leurs coups (ch. 1137, 1143)")
fight(2.626, "elbaf", "luffy", "loki", "A", 1, tb=["epuise"],
      note="Luffy abat Loki affaibli d'un coup mou ; Zoro le soupçonne de bluffer (ch. 1143)")
fight(2.63, "elbaf", "sommers", "saul", "A", 2, note="Épines invisibles puis Saul inconscient (ch. 1143, 1146)")
fight(2.631, "elbaf", "gunko", ["nami", "jinbe", "brook", "usopp"], "A", 2,
      note="Gunko renvoie Zeus, monte Jinbe contre Brook (Aloe), capture Colon ; Usopp la coupe en deux, elle se régénère (ch. 1146-1147)")
fight(2.633, "elbaf", "sommers", "robin", "A", 2, note="Craspedia lui brise le dos, il se remet et la cloue (ch. 1148)")
fight(2.634, "elbaf", "gaban", "sommers", "A", 2, ta=[],
      note="Gaban lui coupe un bras (qui ne repousse pas) puis le fend en deux (ch. 1148-1149)")
fight(2.635, "elbaf", "gunko", "gaban", "A", 1, tb=["protege"],
      note="Otage (Colon) : Gaban lâche ses haches, criblé de flèches et jeté de la branche (ch. 1149)")
fight(2.636, "elbaf", "gunko", ["dorry", "brogy"], "A", 3, ta=["boost"],
      note="Imu à travers le corps de Gunko (Domi Reversi) arrache la main de Brogy et démonise les deux capitaines (ch. 1149-1150)")
fight(2.65, "elbaf", "sanji", "killingham", "A", 2,
      note="Ifrit Jambe Concassé brise le casque de Killingham (ch. 1176) ; il finit ligoté à un arbre (ch. 1179)")
fight(2.651, "elbaf", "gunko", "usopp", "A", 3, ta=["boost"], tb=["protege"],
      note="Imu dans le corps de Gunko massacre Usopp qui protège Brook (ch. 1177)")
fight(2.652, "elbaf", ["luffy", "loki"], "gunko", "A", 2, ta=[], tb=["boost"],
      note="Domi Reversi échoue, Luffy la martèle et Loki gèle Imu-Gunko avec Niflheim (ch. 1178)")
fight(2.66, "elbaf", "imu", "zoro", "A", 3, note="Imu pare Rengoku Oni Giri avec sa queue, Zoro à terre d'un Omen (ch. 1180)")
fight(2.6602, "elbaf", "imu", "hajrudin", "A", 3, note="Un Omen met Hajrudin au tapis (ch. 1180)")
fight(2.6604, "elbaf", "imu", "sanji", "A", 2, note="Imu bloque et repousse Sanji d'un coup de pied (ch. 1180)")
fight(2.665, "elbaf", "imu", "loki", "A", 1,
      note="Loki (Nidhöggr) le frappe avec Ragnir, mais Imu l'empale (Nemesis) et le brûle (Stigma) (ch. 1181-1187)", flags="i")
fight(2.67, "elbaf", "imu", "luffy", "A", 2, ta=[], tb=[],
      note="Luffy le frappe au Haki (ch. 1186-1187) ; Gear 5 à bout, Imu l'embroche avec Void (ch. 1188) puis le cloue à un arbre avec une seconde épée (ch. 1189)")
fight(2.672, "elbaf", "imu", "gaban", "A", 2, tb=["protege"],
      note="Gaban interrompt le coup de grâce (ch. 1189), tient longtemps puis perd un bras au coude (ch. 1190)")
fight(2.675, "elbaf", ["luffy", "loki", "hajrudin"], "imu", "D", ta=["epuise"],
      note="Gokoku Sovereignty (ch. 1191) ; Imu encaisse et continue (ch. 1192) ; Dawn Thor Bullet perce sa barrière, puis le Gear 5 de Luffy s'épuise (ch. 1193)", flags="i")
fight(2.68, "elbaf", "zoro", "sommers", "A", 3, ta=["haki_roi"],
      note="Zoro le transperce en manquant le cœur (ch. 1193), s'exerce au Haki des rois sur lui (ch. 1194) ; Sommers fuit en pleurant, Zoro le rattrape (ch. 1195)")
fight(2.69, "elbaf", "sanji", "killingham", "A", 2, ta=["haki_roi"], tb=["boost"],
      note="Killingham relancé par Imu et armé de Longinus (ch. 1187-1189) ; Sanji éveille le Haki des rois (ch. 1197), brise son armure d'Omen, Killingham fuit terrifié (ch. 1198)")
fight(2.695, "elbaf", "imu", "loki", "A", 3, note="Loki en forme hybride complète tient d'abord, puis Imu dans une nouvelle forme le terrasse d'un seul coup, en grande partie hors champ (ch. 1198)")

# ajouts : Shanks face aux autres sommets
fight(-0.05, "avant", "shanks", "kaido", "D", note="Shanks retient Kaido pour l'empêcher de rejoindre Marineford (ch. 434, 556)", flags="i?")
fight(2.4499, "wano", "shanks", "ryokugyu", "A", 2, note="Le Haki des rois de Shanks fait reculer Ryokugyu à distance (ch. 1055)")
