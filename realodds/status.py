"""Official canon evidence of power: ranks / titles over time (STATUS) and explicit canon
statements ranking characters (ORDER). Manga, The Last, Boruto manga (incl. Two Blue Vortex),
official databooks only; no anime filler.

STATUS: (id, t, tier, sd, label)   tier on the data.py scale (0 civil ... 8 au-delà)
ORDER:  (idA, tA, idB, tB, gap, sd, label)  A stronger than B by `gap` tiers (gap 0 = stated equal)
t = years since Naruto's birth (same axis as data.py).

Verified on English / French Narutopedia (WebFetch, 2026-11-09) where a page loaded:
Hashirama (ch. 619, 575, 620-626, 644), Hiruzen (ch. 94, 121, 126), Minato (ch. 240, 367,
541, 450; Databook 2 p. 266; "Naruto: Whorl within the Spiral" p. 31), Kakashi (jōnin at 12,
ANBU captain, 6th Hokage, Gai surpassed him), Might Guy (ch. 672 p. 11, 667, 669),
Troisième Kazekage (fr, ch. 266 p. 11 / 268 p. 9), Code (Boruto ch. 56 pp. 31-35, ch. 59 p. 9),
Isshiki (Boruto ch. 51 p. 11, ch. 38), Sasuke (power equal to Naruto, Naruto strongest in
history, "Sasaukage"), Jura (TBV ch. 4 p. 37, ch. 6 p. 9, ch. 11 p. 22, ch. 13 p. 27).
Other chapter numbers are from memory of the manga and are marked "(ch. ~N)" when approximate.
No Kishimoto interview ranking Minato vs Itachi could be verified (only fan articles), so none
is included.
"""

STATUS = [
    # ---- Ōtsutsuki / ère mythique
    ("kaguya", -1000.0, 8.5, 0.5, "Kaguya, déesse lapin, ancêtre du chakra, a dû être scellée par ses deux fils réunis (ch. 670-671)"),
    ("hagoromo", -950.0, 8.0, 0.5, "Hagoromo, Sage des Six Chemins, fondateur du ninshū (ch. 670)"),
    ("hamura", -950.0, 7.5, 0.6, "Hamura, co-scelleur de Kaguya avec Hagoromo (ch. 670)"),
    ("indra", -1000.0, 7.0, 0.7, "Indra, fils aîné du Sage, prodige ancêtre des Uchiha (ch. 670)"),
    ("asura", -1000.0, 7.0, 0.7, "Asura, successeur désigné du Sage, ancêtre des Senju (ch. 670)"),
    ("kaguya", 17.06, 8.5, 0.6, "Kaguya libérée par le Tsukuyomi infini ; il faut Naruto et Sasuke réunis pour la sceller (ch. 674-691)"),
    ("kurama", -56.0, 6.5, 0.8, "Kurama, le plus puissant des neuf bijū (ch. ~568 ; 4e databook)"),
    ("tobirama", -70.0, 4.5, 0.8, "Tobirama, frère de Hashirama, l'un des deux plus forts Senju de sa génération, rival d'Izuna (ch. 624)"),
    ("izuna", -70.0, 4.5, 0.8, "Izuna, frère de Madara, l'un des deux plus forts Uchiha de sa génération (ch. 624)"),
    ("yahiko", -4.0, 3.0, 0.8, "Yahiko, chef de l'Akatsuki d'origine, élève de Jiraiya (ch. 446)"),
    # ---- Konoha : Hokage et fondateurs
    ("hashirama", -56.0, 7.0, 0.5, "1er Hokage, « Dieu des Shinobi », shinobi le plus fort de son époque (ch. 619 p. 1)"),
    ("madara", -56.0, 7.0, 0.5, "Madara, chef du clan Uchiha, seul rival de Hashirama (ch. 620-626)"),
    ("tobirama", -50.0, 5.5, 0.6, "2e Hokage (ch. 620-627)"),
    ("hiruzen", -48.0, 5.0, 0.7, "Nommé 3e Hokage par Tobirama pendant la 1re Grande Guerre (ch. ~480)"),
    ("hiruzen", -25.0, 6.0, 0.6, "Hiruzen au sommet : « Dieu des Shinobi » (ch. 121 p. 3), « le Professeur », réputé Hokage le plus fort de l'histoire (ch. 94 p. 12)"),
    ("hiruzen", 12.5, 5.5, 0.6, "Hiruzen âgé, toujours Hokage, déclin reconnu (Orochimaru : dix ans plus jeune il m'aurait tué, ch. 126 p. 10)"),
    ("minato", -4.0, 5.5, 0.6, "« Éclair jaune de Konoha » ; ordre de fuite à vue donné aux shinobi ennemis (ch. 240 p. 11 ; Databook 2 p. 266)"),
    ("minato", -1.0, 6.0, 0.5, "4e Hokage, choisi plutôt qu'Orochimaru pour ses exploits de guerre (ch. 450 p. 15) ; shinobi le plus rapide de son temps (ch. 541 p. 8)"),
    ("tsunade", 12.7, 5.0, 0.6, "5e Hokage (ch. ~170-171)"),
    ("danzo", 16.6, 5.0, 0.8, "Danzō nommé Hokage par intérim / candidat 6e Hokage par le daimyō (ch. ~451)"),
    ("kakashi", 16.6, 4.5, 0.7, "Kakashi proposé comme 6e Hokage par le conseil de Konoha après l'attaque de Pain (ch. ~451)"),
    ("kakashi", 18.8, 5.0, 0.7, "Kakashi 6e Hokage après la guerre (ch. 700 ; The Last)"),
    ("naruto", 30.0, 7.5, 0.5, "Naruto 7e Hokage (ch. 700 ; Boruto ch. 1)"),
    ("naruto", 32.0, 7.5, 0.5, "Naruto reconnu comme le shinobi le plus fort de l'histoire (Boruto, cité par Narutopedia)"),
    ("naruto", 16.45, 6.0, 0.7, "Naruto acclamé héros de Konoha après avoir vaincu Pain (ch. 449-450)"),
    # ---- Sannin et Hanzō
    ("hanzo", -32.0, 6.0, 0.6, "Hanzō de la Salamandre, chef d'Ame, réputé demi-dieu, épargne et nomme les trois Sannin (ch. 372)"),
    ("jiraiya", -32.0, 4.0, 0.8, "Nommé Sannin par Hanzō pendant la 2e Grande Guerre (ch. 372)"),
    ("tsunade", -32.0, 4.0, 0.8, "Nommée Sannin par Hanzō pendant la 2e Grande Guerre (ch. 372)"),
    ("orochimaru", -32.0, 4.0, 0.8, "Nommé Sannin par Hanzō pendant la 2e Grande Guerre (ch. 372)"),
    ("jiraiya", 12.65, 5.0, 0.6, "Sannin légendaire, Hokage pressenti (refuse le poste, ch. ~146-147)"),
    ("orochimaru", 12.5, 5.0, 0.6, "Sannin légendaire, ancien candidat au poste de 4e Hokage (ch. 450)"),
    ("orochimaru", 4.0, 5.0, 0.8, "Orochimaru membre d'Akatsuki (partenaire de Sasori) avant sa défection (ch. ~263)"),
    # ---- Akatsuki
    ("nagato", 16.4, 6.0, 0.6, "Pain, chef d'Akatsuki, porteur du Rinnegan, « dieu » d'Ame (ch. 363-375)"),
    ("obito", 16.6, 6.5, 0.7, "Tobi / « Madara », véritable chef d'Akatsuki dans l'ombre (ch. 462-467)"),
    ("itachi", 12.65, 5.5, 0.6, "Itachi, criminel de rang S, membre d'Akatsuki (ch. 142-147)"),
    ("kisame", 12.65, 5.0, 0.6, "Kisame, ex-membre des Sept Épéistes de Kiri, membre d'Akatsuki, « bijū sans queue » (ch. 142-147)"),
    ("sasori", 15.5, 5.0, 0.6, "Sasori « Scorpion du Sable rouge », membre d'Akatsuki, a tué le 3e Kazekage (ch. 266-268)"),
    ("deidara", 15.5, 4.5, 0.6, "Deidara, ninja déserteur d'Iwa, membre d'Akatsuki (ch. 247-260)"),
    ("hidan", 15.8, 4.5, 0.7, "Hidan, membre d'Akatsuki (ch. 312-331)"),
    ("kakuzu", 15.8, 5.0, 0.6, "Kakuzu, membre d'Akatsuki, élite de Taki ayant affronté Hashirama (ch. 312-342)"),
    ("konan", 16.4, 4.5, 0.7, "Konan, ange d'Ame, membre fondateur d'Akatsuki (ch. ~363-510)"),
    ("sasuke", 16.5, 5.0, 0.8, "Sasuke et Taka rejoignent Akatsuki (ch. ~409)"),
    # ---- Itachi / Shisui / Kakashi / Gai
    ("itachi", 5.0, 2.8, 0.7, "Itachi chūnin à 10 ans (ch. ~221-224)"),
    ("itachi", 7.5, 4.0, 0.7, "Itachi capitaine ANBU à 13 ans (ch. ~142, 224)"),
    ("shisui", 7.9, 5.0, 0.7, "Shisui « de la Téléportation », renommé dans tous les pays (ch. ~550, 590)"),
    ("kakashi", -4.0, 3.0, 0.7, "Kakashi promu jōnin à 12 ans pendant la 3e Grande Guerre (Kakashi Gaiden, ch. 239-244)"),
    ("kakashi", 4.0, 3.5, 0.7, "Kakashi capitaine ANBU, chef de l'équipe Ro (ch. ~240, 4e databook)"),
    ("kakashi", 12.0, 4.0, 0.6, "« Kakashi le Ninja Copieur / Kakashi du Sharingan », connu dans les autres pays (ch. 9-10)"),
    ("gai", 12.3, 4.5, 0.6, "Gai, jōnin, « Fauve vert de Konoha », spécialiste du taijutsu (ch. ~89-143)"),
    ("gai", 17.03, 6.0, 0.8, "Gai à la 8e porte ; Madara : Gai inégalé en combat physique (ch. 672 p. 11)"),
    # ---- Suna
    ("kazekage3", -25.0, 5.5, 0.6, "3e Kazekage, considéré comme le Kage le plus puissant de l'histoire de Suna (ch. 266 p. 11, 268 p. 9)"),
    ("rasa", 12.0, 5.0, 0.7, "4e Kazekage (ch. ~95-140)"),
    ("gaara", 12.3, 3.0, 0.8, "Gaara, jinchūriki de Shukaku, genin (ch. ~66-95)"),
    ("gaara", 15.2, 4.5, 0.6, "Gaara 5e Kazekage à 15 ans (ch. 245-246)"),
    ("gaara", 16.9, 4.8, 0.6, "Gaara commandant de la 4e division et commandant de terrain de l'Alliance (ch. ~516)"),
    ("gaara", 32.0, 5.0, 0.7, "Gaara, 5e Kazekage toujours en poste (Boruto ch. ~8-10)"),
    ("chiyo", 15.5, 4.5, 0.7, "Chiyo, conseillère de Suna, marionnettiste légendaire (ch. 261-280)"),
    ("baki", 12.3, 3.5, 0.6, "Baki, jōnin de Suna (ch. ~38-95)"),
    ("kankuro", 15.5, 3.0, 0.7, "Kankurō jōnin dans la 2e partie"),
    ("temari", 15.5, 3.0, 0.7, "Temari jōnin dans la 2e partie"),
    # ---- Kumo
    ("raikage3", -10.0, 6.0, 0.6, "3e Raikage, a tenu trois jours et trois nuits face à 10 000 ninjas (ch. ~545, 557)"),
    ("a4", 16.6, 5.5, 0.5, "4e Raikage (ch. 455-470)"),
    ("killer_b", 16.5, 5.5, 0.6, "Killer B, jinchūriki parfait du Hachibi (ch. 412-420)"),
    ("yugito", 15.3, 5.0, 0.7, "Yugito Nii, jinchūriki maîtrisant le Nibi (ch. ~356)"),
    ("darui", 32.0, 5.0, 0.6, "Darui 5e Raikage (Boruto ch. ~1-10)"),
    # ---- Iwa
    ("mu", -35.0, 5.5, 0.7, "2e Tsuchikage (ch. ~522-526)"),
    ("onoki", 16.6, 5.5, 0.6, "Ōnoki, 3e Tsuchikage, a affronté Madara dans sa jeunesse (ch. 459-470, 561)"),
    ("kurotsuchi", 32.0, 5.0, 0.7, "Kurotsuchi 4e Tsuchikage (Boruto ch. ~1-10)"),
    # ---- Kiri
    ("gengetsu", -35.0, 5.0, 0.7, "2e Mizukage (ch. ~525-526)"),
    ("mei", 16.6, 5.0, 0.6, "Mei Terumī, 5e Mizukage (ch. 458-470)"),
    ("chojuro", 16.6, 3.5, 0.7, "Chōjūrō, membre des nouveaux Sept Épéistes de Kiri (ch. ~455)"),
    ("chojuro", 32.0, 5.0, 0.7, "Chōjūrō 6e Mizukage (Boruto ch. ~1-10)"),
    ("zabuza", 12.0, 4.0, 0.6, "Zabuza, « Démon du Brouillard », ex-membre des Sept Épéistes, déserteur de rang A (ch. 9-10)"),
    ("ao", 16.6, 3.5, 0.7, "Ao, ninja d'élite chasseur de Kiri (ch. 458-470)"),
    # ---- Autres
    ("mifune", 16.6, 4.5, 0.7, "Mifune, général des samouraïs du Pays du Fer (ch. 455-470)"),
    ("kushina", -4.0, 4.0, 0.9, "Kushina, jinchūriki de Kyūbi, « Piment rouge sanglant » (ch. 498-500)"),
    ("asuma", 6.0, 4.0, 0.7, "Asuma, ancien membre des Douze Ninjas Gardiens (ch. ~330)"),
    ("asuma", 12.3, 3.5, 0.6, "Asuma, jōnin (ch. ~322)"),
    ("kurenai", 12.3, 3.0, 0.6, "Kurenai, jōnin (ch. ~142)"),
    ("anko", 12.3, 3.0, 0.7, "Anko, jōnin spéciale (ch. ~45)"),
    ("hayate", 12.3, 3.0, 0.7, "Hayate, jōnin spécial (ch. ~65)"),
    ("yamato", 15.6, 3.5, 0.6, "Yamato, ANBU / jōnin (ch. 284)"),
    ("sai", 15.6, 3.0, 0.7, "Sai, membre de la Racine (ch. 284)"),
    ("kimimaro", 12.85, 3.5, 0.7, "Kimimaro, le plus fort des subordonnés d'Orochimaru (chef des Quatre d'Oto) (ch. ~210-218)"),
    ("shikamaru", 12.6, 2.0, 0.6, "Shikamaru promu chūnin, le seul après l'examen (ch. ~182)"),
    ("neji", 12.3, 2.0, 0.7, "Neji genin, génie du clan Hyūga (ch. ~38-104)"),
    ("neji", 15.5, 3.0, 0.6, "Neji jōnin dans la 2e partie (ch. ~246)"),
    ("rock_lee", 15.5, 2.0, 0.6, "Rock Lee chūnin dans la 2e partie"),
    ("tenten", 15.5, 2.0, 0.6, "Tenten chūnin dans la 2e partie"),
    ("sakura", 15.5, 2.0, 0.6, "Sakura chūnin dans la 2e partie"),
    ("naruto", 12.0, 1.0, 0.8, "Naruto genin, dernier de sa promotion (ch. 1-3)"),
    ("sasuke", 12.0, 1.5, 0.8, "Sasuke genin, premier de sa promotion (ch. 3)"),
    ("sakura", 12.0, 1.0, 0.8, "Sakura genin (ch. 3)"),
    ("hinata", 15.5, 2.0, 0.6, "Hinata chūnin dans la 2e partie"),
    ("ino", 15.5, 2.0, 0.6, "Ino chūnin dans la 2e partie"),
    ("choji", 15.5, 2.0, 0.6, "Chōji chūnin dans la 2e partie"),
    ("kiba", 15.5, 2.0, 0.6, "Kiba chūnin dans la 2e partie"),
    ("shino", 15.5, 2.0, 0.6, "Shino chūnin dans la 2e partie"),
    ("izumo", 12.3, 2.0, 0.6, "Izumo, chūnin (ch. ~40)"),
    ("kotetsu", 12.3, 2.0, 0.6, "Kotetsu, chūnin (ch. ~40)"),
    ("mizuki", 12.0, 2.0, 0.6, "Mizuki, chūnin instructeur (ch. 1)"),
    ("konohamaru", 16.4, 1.5, 0.7, "Konohamaru genin, élève d'Ebisu, maîtrise déjà le Rasengan (ch. 426-428)"),
    ("konohamaru", 32.0, 3.5, 0.6, "Konohamaru jōnin, chef de l'équipe 7 de Boruto (Boruto ch. ~3)"),
    ("boruto", 32.0, 2.0, 0.8, "Boruto genin (Boruto ch. ~3)"),
    # ---- Sasuke (Boruto)
    ("sasuke", 32.0, 7.5, 0.5, "Sasuke « Sasaukage » (Kage de soutien), puissance égale à celle de Naruto (Boruto ; Narutopedia)"),
    ("sasuke", 32.1, 7.0, 0.7, "Sasuke privé de son Rinnegan par Momoshiki, reste une menace (Boruto ch. ~10-13)"),
    # ---- Ōtsutsuki Boruto, Kara, Arbres-Dieux
    ("momoshiki", 32.0, 8.0, 0.6, "Momoshiki Ōtsutsuki (Boruto ch. 8-13)"),
    ("kinshiki", 32.0, 7.5, 0.7, "Kinshiki, serviteur de Momoshiki (Boruto ch. 8-10)"),
    ("isshiki", 33.1, 8.5, 0.5, "Isshiki, Ōtsutsuki de rang supérieur à Kaguya (Boruto ch. 51 p. 11)"),
    ("jigen", 32.5, 7.5, 0.6, "Jigen, chef de Kara, réceptacle d'Isshiki (Boruto ch. 38)"),
    ("isshiki", 32.45, 8.5, 0.6, "Isshiki, Ōtsutsuki de rang supérieur à Kaguya, caché dans Jigen, chef réel de Kara (Boruto ch. 38, 51)"),
    ("code", 32.45, 6.0, 0.8, "Code, Inner de Kara (Boruto ch. ~25-38)"),
    ("boro", 32.45, 5.5, 0.8, "Boro, Inner de Kara (Boruto ch. ~25, 40)"),
    ("delta", 32.45, 5.5, 0.8, "Delta, Inner de Kara (Boruto ch. ~25, 30)"),
    ("mamushi", 36.0, 6.0, 0.9, "Mamushi, Arbre-Dieu humanoïde de Code (TBV ch. ~26)"),
    ("jura", 36.0, 7.5, 0.6, "Jura, Arbre-Dieu le plus dangereux, puissance bien au-dessus de son créateur Code (TBV ch. 4 p. 37, ch. 6 p. 9)"),
]

NUMERIC = {}   # no official numeric ratings found beyond the 8-stat databook tables (databook.py)
NUMERIC_TRANSFORM = {}

ORDER = [
    # ---- Ère mythique
    ("kaguya", -1000.0, "hagoromo", -980.0, 0.5, 0.6, "Kaguya n'a pu être scellée que par Hagoromo ET Hamura réunis (ch. 670-671)"),
    ("kaguya", -1000.0, "hamura", -980.0, 0.8, 0.7, "Kaguya n'a pu être scellée que par Hagoromo ET Hamura réunis (ch. 670-671)"),
    ("kaguya", 17.08, "naruto", 17.08, 0.5, 0.8, "Hagoromo : seuls Naruto et Sasuke ensemble peuvent sceller Kaguya (ch. ~672-674)"),
    ("kaguya", 17.08, "sasuke", 17.08, 0.5, 0.8, "Hagoromo : seuls Naruto et Sasuke ensemble peuvent sceller Kaguya (ch. ~672-674)"),
    ("hagoromo", -950.0, "hashirama", -50.0, 0.5, 0.8, "Kabuto : la puissance de Hashirama était comparable à celle du Sage des Six Chemins (ch. 575 p. 4-5)"),
    # ---- Hashirama / Madara / Tobirama / Hiruzen
    ("hashirama", -56.0, "madara", -56.0, 0.3, 0.6, "Madara reconnaît toute sa vie la supériorité de Hashirama, même avec l'EMS et Kyūbi (ch. 620-626)"),
    ("hashirama", -50.0, "tobirama", -50.0, 0.8, 0.7, "Tobirama ne pouvait pas égaler Madara, seul Hashirama le pouvait (ch. 620-627)"),
    ("madara", -56.0, "tobirama", -50.0, 0.5, 0.7, "Seul Hashirama pouvait arrêter Madara ; Tobirama en était incapable (ch. 620-627)"),
    ("madara", -56.0, "onoki", 16.9, 1.2, 0.7, "Ōnoki : Madara, que seul Hashirama pouvait affronter (ch. ~560-562)"),
    ("madara", -56.0, "mei", 16.9, 1.3, 0.7, "Madara Edo face aux cinq Kage ; seul Hashirama l'égalait (ch. ~560-562)"),
    ("madara", -56.0, "hiruzen", -25.0, 0.8, 0.8, "Kabuto : depuis Hashirama, personne ne s'en est approché à part Madara (ch. 575 p. 4-5)"),
    ("hashirama", -50.0, "hiruzen", -25.0, 0.8, 0.8, "Kabuto : depuis Hashirama, personne ne s'en est approché à part Madara (ch. 575 p. 4-5)"),
    # retiré : Hashirama/Minato comparés par Kurama — source = roman (Naruto : le tourbillon dans la spirale), hors canon manga/databook
    ("hiruzen", 2.5, "orochimaru", 12.5, 0.5, 0.7, "Orochimaru : si Hiruzen avait eu dix ans de moins, il m'aurait tué (ch. 126 p. 10)"),
    ("hiruzen", -48.0, "danzo", -48.0, 0.5, 0.8, "Tobirama désigne Hiruzen plutôt que Danzō ; Danzō toujours un pas derrière son rival (ch. ~480)"),
    # ---- Minato
    ("minato", -1.0, "a4", 16.6, 0.3, 0.8, "A (4e Raikage) et Jiraiya : Minato inégalé, le plus rapide de son temps (ch. 367 p. 11, 541 p. 7-8)"),
    ("minato", -1.0, "tobirama", -50.0, 0.3, 0.9, "Tobirama reconnaît que Minato le surpasse au Hiraishin (ch. ~642)"),
    # ---- Sannin / Hanzō / Pain
    ("hanzo", -32.0, "jiraiya", -32.0, 1.0, 0.7, "Hanzō bat et épargne les trois futurs Sannin, puis les nomme (ch. 372)"),
    ("hanzo", -32.0, "tsunade", -32.0, 1.0, 0.7, "Hanzō bat et épargne les trois futurs Sannin, puis les nomme (ch. 372)"),
    ("hanzo", -32.0, "orochimaru", -32.0, 1.0, 0.7, "Hanzō bat et épargne les trois futurs Sannin, puis les nomme (ch. 372)"),
    ("nagato", 9.0, "hanzo", 9.0, 0.3, 0.8, "Pain renverse et tue Hanzō, le « demi-dieu » d'Ame (ch. ~372-375)"),
    ("jiraiya", 12.65, "kisame", 12.65, 0.3, 1.5, "Itachi : même à deux contre Jiraiya, nous y laisserions la vie (ch. ~147) ; propos peu fiable : Itachi, agent double, évite tout combat contre Konoha"),
    ("jiraiya", 12.65, "itachi", 12.65, 0.0, 1.5, "Itachi : même à deux contre Jiraiya, nous y laisserions la vie (ch. ~147) ; propos peu fiable : Itachi, agent double, évite tout combat contre Konoha, donc incertitude large"),
    # ---- Itachi / Kakashi / Gai
    # corrigé (audit des 25 duels) : la phrase du ch. 142 porte sur Kisame contre Kakashi, pas sur Itachi ; Itachi > Kakashi vient du combat lui-même
    ("kisame", 12.55, "kakashi", 12.55, -0.3, 0.8, "Itachi retient Kisame : contre Kakashi, forces trop proches, le combat coûterait temps et peine (ch. 142)"),
    ("kakashi", 12.55, "kisame", 12.55, -0.3, 0.8, "Itachi retient Kisame : contre Kakashi, forces trop proches, le combat coûterait temps et peine (ch. 142)"),
    ("itachi", 12.5, "orochimaru", 12.5, 0.3, 0.8, "Orochimaru reconnaît qu'Itachi est plus fort que lui (ch. 140 p. 5)"),
    ("shisui", 7.9, "itachi", 7.9, -0.3, 0.8, "La maîtrise du Sharingan de Shisui rivalisait avec celle d'Itachi (ch. 222 p. 7)"),
    ("itachi", 7.9, "shisui", 7.9, -0.3, 0.8, "La maîtrise du Sharingan de Shisui rivalisait avec celle d'Itachi (ch. 222 p. 7)"),
    ("gai", 17.03, "kakashi", 17.03, 0.5, 0.7, "Kakashi reconnaît que Gai l'a surpassé quand il ouvre la 8e porte (ch. 667-669)"),
    # ---- Suna
    ("kazekage3", -25.0, "rasa", 12.0, 0.5, 0.7, "3e Kazekage, Kage le plus puissant de l'histoire de Suna (ch. 266 p. 11, 268 p. 9)"),
    ("sasori", -4.0, "kazekage3", -25.0, 0.3, 0.8, "Sasori a enlevé et tué le 3e Kazekage pour en faire une marionnette (ch. 266-268)"),
    # ---- Naruto / Sasuke
    ("naruto", 17.1, "sasuke", 17.1, 0.0, 0.6, "Rivaux de puissance égale à la Vallée de la Fin (ch. 695-698 ; 4e databook)"),
    ("naruto", 32.0, "sasuke", 32.0, 0.0, 0.5, "Sasuke a une puissance égale à celle de Naruto ; même avec un bras il suit Naruto au combat (Boruto ; databook)"),
    # ---- Ōtsutsuki / Kara / Arbres-Dieux
    ("isshiki", 33.1, "momoshiki", 32.0, 0.7, 0.8, "Isshiki, de rang supérieur même à Kaguya (Boruto ch. 51 p. 11), au-dessus de Momoshiki"),
    ("momoshiki", 32.0, "kinshiki", 32.0, 0.5, 0.7, "Kinshiki, serviteur de Momoshiki, se laisse absorber par lui (Boruto ch. 8-10)"),
    ("jigen", 32.5, "naruto", 32.5, 0.3, 0.8, "Jigen tient tête à Naruto et Sasuke réunis (Boruto ch. 38)"),
    ("code", 34.0, "jigen", 32.5, 0.5, 0.5, "Amado : au sommet de ses capacités (limiteurs retirés), Code dépasse de loin Jigen (Boruto ch. 56 p. 31-34 ; Narutopedia)"),
    ("code", 33.3, "kashin_koji", 33.0, 0.3, 0.7, "Code, le plus fort des Inners après Isshiki ressuscité (Boruto ch. 56) ; statut absolu remplacé par cet ordre"),
    ("code", 33.3, "boro", 32.5, 0.5, 0.7, "Code, même bridé, jugé plus fort que Delta et Boro (Boruto ch. 56 p. 35)"),
    ("code", 33.3, "delta", 32.5, 0.5, 0.7, "Code, même bridé, jugé plus fort que Delta et Boro (Boruto ch. 56 p. 35)"),
    ("code", 33.3, "naruto", 33.3, 0.3, 0.8, "Code bridé pourrait battre le 7e Hokage (sans Kurama) en duel (Boruto ch. 59 p. 9)"),
    ("jura", 36.0, "code", 34.0, 0.8, 0.7, "Jura, puissance bien au-dessus de son créateur Code (TBV ch. 4 p. 37, ch. 6 p. 9)"),
    ("jura", 36.2, "himawari", 36.2, 1.5, 0.7, "Jura n'utilise qu'une infime part de sa puissance pour dominer Himawari, jinchūriki de Kurama (TBV ch. 11 p. 22)"),
    ("jura", 36.3, "kawaki", 36.3, 1.0, 0.7, "Jura met Kawaki hors combat d'une seule attaque (TBV ch. 13 p. 27)"),
]
