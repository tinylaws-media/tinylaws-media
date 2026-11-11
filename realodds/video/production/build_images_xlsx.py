"""Construit « images_le_verdict.xlsx » : la liste complète des images à fournir pour les 50 premières vidéos."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

P = "Pied détouré"; B = "Buste détouré"; R = "Visage détouré (PNG)"; D = "Décor (capture)"; O = "Objet détouré"
# (fichier, personnage, version / époque, catégorie, pose, orientation, tenue / détails, priorité, statut, fichier reçu)
NAR = [
 ("itachi_combat.png","Itachi","Akatsuki, adulte (Partie 2)",P,"Pose de combat, bras tendu","Face",'Manteau Akatsuki ouvert, corbeaux bienvenus',1,"Reçu","itachi facing front fight mode.png"),
 ("itachi_face.png","Itachi","Akatsuki, adulte",P,"Debout, calme","Face","Manteau Akatsuki, bandeau barré",1,"Reçu","itachi facing front.png"),
 ("itachi_gauche.png","Itachi","Akatsuki, adulte",P,"Debout, bras tendu","Vers la gauche","Manteau Akatsuki",1,"Reçu","itachi facing left.png"),
 ("minato_combat.png","Minato","4e Hokage",P,"Pose de combat, kunai + Rasengan","Vers la droite","Manteau de Hokage à flammes",1,"Reçu","minato facing front fight mode.png"),
 ("minato_droite.png","Minato","4e Hokage",P,"Debout, calme","Vers la droite","Manteau de Hokage à flammes",1,"Reçu","minato facing right.png"),
 ("obito_masque_assis.png","Obito","Tobi masqué (Akatsuki)",P,"Assis","Face","Masque spirale orange, manteau Akatsuki",2,"Reçu","sitting obito.png"),
 ("obito_masque_debout.png","Obito","Masque de guerre (4e guerre) ou Tobi",P,"Debout, pose de combat","Vers la gauche","Masque, manteau, éventail Gunbai si possible",1,"À chercher",""),
 ("kakashi_assis.png","Kakashi","Partie 2",P,"Assis","Face","Gilet de Konoha",2,"Reçu","sitting kakashi.png"),
 ("kakashi_guerre.png","Kakashi","4e Grande Guerre",P,"Debout, pose de combat, Sharingan visible","Vers la droite","Gilet de l'Alliance (bandeau « shinobi »)",1,"À chercher",""),
 ("kakashi_double_ms.png","Kakashi","Fin de la guerre (double Mangekyō)",B,"Buste, deux yeux Sharingan, Susanoo bienvenu","Face","Gilet de l'Alliance",2,"À chercher",""),
 ("raikage.png","A (4e Raikage)","Sommet des Kage",P,"Pose de combat","Face","Manteau de Kage blanc, torse nu",1,"Reçu","A raikage.png"),
 ("killer_b.png","Killer B","Partie 2",P,"Pose de combat, sabres dans le dos","Face","Tenue blanche, lunettes",1,"Reçu","killer b.png"),
 ("kunai_hiraishin.png","Kunai du Hiraishin","",O,"Objet seul","Diagonale","Kunai à trois lames avec inscriptions",1,"Reçu","kunai hiraishin.png"),
 ("madara_edo.png","Madara","Ressuscité (4e guerre)",P,"Debout, éventail Gunbai et faux","Vers la droite","Armure rouge, cheveux longs, Rinnegan",1,"À chercher",""),
 ("madara_jubi.png","Madara","Réceptacle de Jûbi (6 Chemins)",P,"Lévitation, bâton noir","Face","Peau et cheveux blancs, orbes noires dans le dos",1,"À chercher",""),
 ("hashirama.png","Hashirama","1er Hokage / Edo Tensei",P,"Debout, mains jointes ou combat","Vers la gauche","Armure rouge, cheveux longs",1,"À chercher",""),
 ("nagato_pain.png","Nagato / Pain","Tendô (Assaut de Pain)",P,"Debout, main levée (Shinra Tensei)","Vers la gauche","Manteau Akatsuki, piercings, cheveux orange",1,"À chercher",""),
 ("jiraiya.png","Jiraiya","Partie 2, idéalement mode ermite",P,"Pose de combat","Vers la droite","Gilet rouge, cheveux blancs ; verrues de crapaud si mode ermite",1,"À chercher",""),
 ("orochimaru.png","Orochimaru","Partie 1 ou Partie 2",P,"Debout, sourire, langue ou sabre Kusanagi","Vers la gauche","Tenue claire, corde violette",1,"À chercher",""),
 ("tsunade.png","Tsunade","5e Hokage",P,"Pose de combat, poing","Face","Haut vert, manteau « jeu »",2,"À chercher",""),
 ("gai_8portes.png","Might Gai","8e Porte (4e guerre)",P,"Pose de combat, aura","Vers la droite","Peau rouge, vapeur, cheveux dressés",1,"À chercher",""),
 ("gai_normal.png","Might Gai","Partie 2",P,"Pose « Nice Guy » ou garde","Vers la droite","Combinaison verte, gilet",2,"À chercher",""),
 ("naruto_6chemins.png","Naruto","Mode Six Chemins (fin de guerre)",P,"Pose de combat, orbes","Vers la droite","Manteau orange à flammes noires, orbes noires",1,"À chercher",""),
 ("naruto_ermite.png","Naruto","Mode ermite (Assaut de Pain)",P,"Pose de combat","Vers la droite","Manteau rouge à flammes noires, yeux de crapaud",1,"À chercher",""),
 ("naruto_baryon.png","Naruto","Mode Baryon (Boruto)",P,"Pose de combat","Vers la droite","Tenue de Hokage, aura orange",2,"À chercher",""),
 ("sasuke_6chemins.png","Sasuke","Rinnegan (fin de guerre)",P,"Pose de combat, sabre","Vers la gauche","Cape grise, Rinnegan + Mangekyō",1,"À chercher",""),
 ("sasuke_hebi.png","Sasuke","Hebi / Taka (combat contre Itachi)",P,"Pose de combat, sabre Kusanagi","Vers la droite","Haut blanc ouvert, corde violette",1,"À chercher",""),
 ("tobirama.png","Tobirama","2e Hokage",P,"Debout, pose de combat","Vers la gauche","Armure bleue, col de fourrure",2,"À chercher",""),
 ("hiruzen_jeune.png","Hiruzen","À son apogée (3e Hokage jeune)",P,"Pose de combat, bâton Enma","Vers la gauche","Armure, casque",2,"À chercher",""),
 ("hiruzen_vieux.png","Hiruzen","Invasion de Konoha",P,"Pose de combat","Vers la gauche","Tenue de combat noire, casque",2,"À chercher",""),
 ("shisui.png","Shisui","Jeune Uchiha",P,"Debout, pose de combat","Vers la droite","Gilet ANBU ou tenue Uchiha",2,"À chercher",""),
 ("danzo.png","Danzō","Sommet des Kage",P,"Debout, bras bandé dévoilé","Vers la droite","Bandages, bras couvert de Sharingan",2,"À chercher",""),
 ("kisame.png","Kisame","Akatsuki",P,"Pose de combat avec Samehada","Vers la droite","Manteau Akatsuki, peau bleue",1,"À chercher",""),
 ("rock_lee.png","Rock Lee","Examen chûnin (Partie 1)",P,"Garde de taijutsu","Vers la droite","Combinaison verte, poids aux jambes",2,"À chercher",""),
 ("gaara.png","Gaara","Examen chûnin (Partie 1)",P,"Bras croisés, sable","Vers la gauche","Gourde dans le dos",2,"À chercher",""),
 ("deidara.png","Deidara","Akatsuki",P,"Pose de combat, argile","Vers la droite","Manteau Akatsuki, mèche blonde",2,"À chercher",""),
 ("sasori.png","Sasori","Forme humaine (marionnette)",P,"Debout avec marionnettes","Vers la gauche","Manteau Akatsuki ou corps marionnette",2,"À chercher",""),
 ("kaguya.png","Kaguya","Fin de la guerre",P,"Lévitation","Face","Robe blanche, cornes, Byakugan + Rinne Sharingan",2,"À chercher",""),
 ("isshiki.png","Isshiki","Vraie forme (Boruto)",P,"Debout","Vers la gauche","Robe, cornes",2,"À chercher",""),
 ("boruto_tbv.png","Boruto","Two Blue Vortex",P,"Pose de combat, sabre","Vers la droite","Cape, cheveux longs",2,"À chercher",""),
 ("kawaki.png","Kawaki","Two Blue Vortex",P,"Pose de combat","Vers la gauche","Marques Karma",2,"À chercher",""),
]
OP = [
 ("mihawk.png","Mihawk","Après l'ellipse",P,"Debout, épée Yoru","Vers la droite","Chapeau à plume, manteau",1),
 ("shanks.png","Shanks","Empereur (Egghead / Elbaf)",P,"Debout, sabre, cape au vent","Vers la gauche","Cape noire, cheveux rouges, un seul bras",1),
 ("akainu.png","Akainu","Amiral en chef",P,"Poing de magma","Vers la droite","Costume rouge, manteau de la Marine, casquette",1),
 ("aokiji.png","Aokiji","Amiral (Marineford) ou pirate",P,"Pose de combat, glace","Vers la gauche","Costume blanc, bandeau sur le front",1),
 ("kizaru.png","Kizaru","Amiral",P,"Pose de rayon lumineux","Vers la gauche","Costume jaune rayé, lunettes",1),
 ("garp_vieux.png","Garp","Egghead",P,"Poing levé","Vers la droite","Veste de vice-amiral, cicatrice",1),
 ("garp_jeune.png","Garp","God Valley (jeune)",P,"Poing levé","Vers la droite","Veste de la Marine, cheveux noirs",1),
 ("barbe_blanche_vieux.png","Barbe Blanche","Marineford",P,"Debout, bisento","Vers la gauche","Manteau, moustache blanche",1),
 ("barbe_blanche_jeune.png","Barbe Blanche","Ère de Roger (à son apogée)",P,"Pose de combat, bisento","Vers la gauche","Moustache, torse nu",1),
 ("kaido_humain.png","Kaido","Wano, forme humaine",P,"Massue Hassaikai sur l'épaule","Vers la gauche","Cornes, manteau",1),
 ("kaido_dragon.png","Kaido","Wano, forme dragon",P,"Dragon enroulé","Vers la gauche","Dragon bleu",3),
 ("luffy_gear5.png","Luffy","Gear 5",P,"Pose de combat, sourire","Vers la droite","Blanc, cheveux en flammes",1),
 ("luffy_base.png","Luffy","Après l'ellipse (Wano / Egghead)",P,"Pose de combat, poing","Vers la droite","Chapeau de paille, tenue Wano ou Egghead",1),
 ("zoro.png","Zoro","Wano ou après",P,"Pose trois sabres","Vers la droite","Kimono vert, cicatrice à l'œil",1),
 ("sanji.png","Sanji","Wano ou après",P,"Coup de pied","Vers la gauche","Costume noir, cigarette",1),
 ("roger.png","Roger","Capitaine (ère de Roger)",P,"Sabre levé","Vers la droite","Manteau rouge, moustache",1),
 ("rayleigh_jeune.png","Rayleigh","Ère de Roger",P,"Sabre, pose de combat","Vers la gauche","Lunettes, cheveux blonds",1),
 ("rayleigh_vieux.png","Rayleigh","Sabaody / Marineford",P,"Sabre","Vers la gauche","Cheveux blancs, lunettes",2),
 ("gaban.png","Scopper Gaban","Elbaf",P,"Haches, pose de combat","Vers la droite","Bras-droit de Roger",1),
 ("marco.png","Marco","Marineford",P,"Flammes de phénix","Vers la droite","Chemise ouverte, flammes bleues",1),
 ("big_mom.png","Big Mom","Whole Cake Island",P,"Debout, épée Napoléon","Vers la droite","Robe rose, chapeau Zeus",1),
 ("katakuri.png","Katakuri","Whole Cake Island",P,"Trident Mogura","Vers la gauche","Écharpe, bouche visible ou non",1),
 ("barbe_noire.png","Barbe Noire","Après l'ellipse",P,"Ténèbres et tremblements","Vers la droite","Manteau, chapeau",1),
 ("law.png","Law","Wano",P,"Sabre Kikoku, Room","Vers la droite","Chapeau tacheté, manteau",1),
 ("kid.png","Kid","Wano",P,"Bras métallique","Vers la gauche","Manteau à fourrure, cheveux rouges",1),
 ("sabo.png","Sabo","Dressrosa",P,"Tuyau en main","Vers la droite","Haut-de-forme, manteau",1),
 ("fujitora.png","Fujitora","Dressrosa",P,"Canne-sabre","Vers la gauche","Amiral, yeux fermés",1),
 ("yamato.png","Yamato","Wano",P,"Massue, pose de combat","Vers la gauche","Cheveux blancs et cornes",1),
 ("loki.png","Loki","Elbaf",P,"Pose de combat","Vers la gauche","Géant, prince d'Elbaf",1),
 ("rocks.png","Rocks D. Xebec","God Valley",P,"Debout, menaçant","Vers la gauche","Manteau de capitaine",1),
 ("king.png","King","Wano, forme hybride",P,"Ailes, sabre","Vers la gauche","Masque retiré, feu dans le dos",1),
 ("doflamingo.png","Doflamingo","Dressrosa",P,"Fils, sourire","Vers la droite","Manteau à plumes roses, lunettes",1),
 ("crocodile.png","Crocodile","Marineford",P,"Crochet doré","Vers la gauche","Manteau à fourrure, cicatrice",1),
 ("ace.png","Ace","Marineford",P,"Poing de feu","Vers la droite","Chapeau orange, torse nu",1),
]
DEC = [
 ("dec_vallee_fin.jpg","Naruto","Vallée de la Fin (statues de Hashirama et Madara)",2),
 ("dec_guerre4.jpg","Naruto","Champ de bataille de la 4e Grande Guerre",2),
 ("dec_konoha_detruit.jpg","Naruto","Konoha rasé (Assaut de Pain)",2),
 ("dec_sommet_kage.jpg","Naruto","Salle du Sommet des Kage",3),
 ("dec_uchiha.jpg","Naruto","Repaire Uchiha (Sasuke contre Itachi)",2),
 ("dec_examen_chunin.jpg","Naruto","Arène de l'examen chûnin",3),
 ("dec_marineford.jpg","One Piece","Marineford (place et tour)",2),
 ("dec_onigashima.jpg","One Piece","Toit d'Onigashima (Wano)",2),
 ("dec_punk_hazard.jpg","One Piece","Punk Hazard (moitié feu, moitié glace)",2),
 ("dec_god_valley.jpg","One Piece","God Valley",2),
 ("dec_egghead.jpg","One Piece","Egghead",2),
 ("dec_wci.jpg","One Piece","Whole Cake Island / monde du miroir",3),
 ("dec_dressrosa.jpg","One Piece","Dressrosa (Colisée ou cage d'oiseau)",3),
 ("dec_elbaf.jpg","One Piece","Elbaf",3),
]
PORT_N = ["hinata","kiba","yamato","kabuto","konan","jugo","kakuzu","hidan","neji","shikamaru","kurama","code","jigen","sakura","kankuro","temari","zabuza","haku","kimimaro","mifune","onoki","mei","hanzo","chiyo","sai"]
PORT_O = ["nami","usopp","chopper","robin","franky","brook","jinbe","vivi","enel","lucci","kuma","magellan","boa_hancock","smoker","coby","issho","jozu","vista","queen","jack","perospero","bartolomeo","cavendish","oden","kozuki_momonosuke"]

# portraits supplémentaires : tous les persos importants de la toile des combats (classés par nombre de combats)
PORT_N2 = ["gaara","boruto","kinshiki","kawaki","momoshiki","sarada","hidari","asuma","darui","kashin_koji","isshiki","jura","tobirama","sasori","deidara","ao","konohamaru","kaguya","rock_lee","choji","mu","boro","mitsuki","hiruzen","shino","ino","suigetsu","chojuro","kurotsuchi","raikage3","gengetsu","kinkaku","ginkaku","danzo","toneri","hagoromo","indra","asura","izuna","kushina"]
PORT_O2 = ["rocks","gunko","loki","saturn","mr_3","ulti","vergo","harald","tashigi","moria","hawkins","fukaboshi","caesar","monet","brogy","neptune","killer","warcury","arlong","sentomaru","hody","baby_5","inuarashi","page_one","bonney","nusjuro","ivankov","ashura_doji","bellamy","kaku","urouge","rebecca","sugar","diamante","nekomamushi","ju_peter","dorry","gin","hannyabal","buffalo"]
# effets, objets et symboles pour les plans « fancy » (fichier, œuvre, quoi, catégorie, détails, priorité)
FX = [
 ("fx_sharingan_itachi.png","Naruto","Mangekyō Sharingan d'Itachi (œil seul)",O,"Gros plan de l'œil, détouré ; sert aux transitions et aux tampons",1),
 ("fx_sharingan_3tomoe.png","Naruto","Sharingan 3 tomoe (œil seul)",O,"Gros plan de l'œil",2),
 ("fx_rinnegan.png","Naruto","Rinnegan (œil seul)",O,"Gros plan, violet à cercles",2),
 ("fx_susanoo_itachi.png","Naruto","Susanoo d'Itachi (rouge, bouclier Yata + épée Totsuka)",P,"En entier, détouré",1),
 ("fx_susanoo_madara.png","Naruto","Susanoo parfait de Madara (bleu)",P,"En entier, détouré",2),
 ("fx_kurama.png","Naruto","Kurama (Kyûbi) en entier",P,"Pose menaçante, détouré",1),
 ("fx_corbeaux.png","Naruto","Nuée de corbeaux d'Itachi",O,"Plusieurs corbeaux en vol, détourés",1),
 ("fx_amaterasu.png","Naruto","Flammes noires d'Amaterasu",O,"Flammes seules, détourées",2),
 ("fx_rasengan.png","Naruto","Rasengan",O,"Sphère seule, détourée",1),
 ("fx_chidori.png","Naruto","Chidori / Raikiri",O,"Éclair seul, détouré",2),
 ("fx_hiraishin_flash.png","Naruto","Éclair jaune / marque du Hiraishin",O,"Formule de sceau du Hiraishin ou traînée jaune",2),
 ("fx_chapeau_hokage.png","Naruto","Chapeau de Hokage",O,"Seul, détouré",2),
 ("fx_manteau_hokage.png","Naruto","Manteau de Hokage à flammes (dos, kanji « 4e Hokage »)",O,"Vu de dos, détouré",2),
 ("sym_akatsuki.png","Naruto","Nuage rouge d'Akatsuki",O,"Symbole seul, détouré",1),
 ("sym_konoha.png","Naruto","Symbole de Konoha (bandeau)",O,"Plaque de bandeau, détourée ; une version barrée aussi",1),
 ("fx_gamabunta.png","Naruto","Gamabunta (crapaud)",P,"En entier, détouré",3),
 ("fx_gunbai.png","Naruto","Éventail Gunbai de Madara",O,"Seul, détouré",3),
 ("op_chapeau_paille.png","One Piece","Chapeau de paille",O,"Seul, détouré",1),
 ("op_haki_rois.png","One Piece","Éclairs noirs du Haki des rois",O,"Éclairs seuls (fond noir accepté)",1),
 ("op_gear5_nuage.png","One Piece","Luffy Gear 5, nuage / rire",P,"En entier, détouré",1),
 ("op_kaido_dragon.png","One Piece","Kaido en dragon",P,"En entier, détouré",1),
 ("op_fruit_gomu.png","One Piece","Fruit du Gomu Gomu / Hito Hito modèle Nika",O,"Fruit seul, détouré",2),
 ("op_wanted_luffy.png","One Piece","Avis de recherche de Luffy (prime actuelle)",O,"Affiche entière, à plat ; idem pour chaque perso d'un duel si possible",1),
 ("op_wanted_vierge.png","One Piece","Avis de recherche vierge",O,"Affiche sans photo ni prime : je remplis moi-même",1),
 ("op_jolly_roger_mugiwara.png","One Piece","Pavillon de l'équipage du Chapeau de paille",O,"Drapeau seul",2),
 ("op_jolly_roger_empereurs.png","One Piece","Pavillons de Barbe Blanche, Kaido, Big Mom, Shanks, Barbe Noire",O,"Un fichier par pavillon (suffixe _kaido, _bigmom…)",2),
 ("op_sabres_zoro.png","One Piece","Sabres de Zoro (Wado, Enma, Sandai Kitetsu)",O,"Croisés ou séparés, détourés",2),
 ("op_manteau_justice.png","One Piece","Manteau de la Marine « Justice »",O,"Vu de dos, détouré",2),
 ("op_den_den_mushi.png","One Piece","Den Den Mushi",O,"Seul, détouré",3),
 ("op_log_pose.png","One Piece","Log Pose",O,"Seul, détouré",3),
]

# ---- vidéos de combats de groupe (fichier, œuvre, groupe, catégorie, pose / composition, priorité)
GRP = [
 ("grp_akatsuki.png","Naruto","Akatsuki au complet (10 membres)",P,"Groupe en ligne ou en V, manteaux, de face",1),
 ("grp_sannin.png","Naruto","Les trois Sannin (Jiraiya, Tsunade, Orochimaru)",P,"Trio de face, idéalement jeunes",1),
 ("grp_cinq_kage.png","Naruto","Les cinq Kage (sommet / guerre)",P,"Groupe de face, chapeaux ou tenues de Kage",1),
 ("grp_naruto_sasuke.png","Naruto","Naruto et Sasuke côte à côte (fin de guerre)",P,"Dos à dos ou côte à côte",1),
 ("grp_hokage_edo.png","Naruto","Les quatre premiers Hokage ressuscités",P,"En ligne, de face",2),
 ("grp_equipe7.png","Naruto","Équipe 7 (Naruto, Sasuke, Sakura, Kakashi)",P,"Pose d'équipe",2),
 ("grp_mugiwara.png","One Piece","Équipage du Chapeau de paille (après l'ellipse)",P,"Équipage complet de face",1),
 ("grp_amiraux.png","One Piece","Les trois amiraux (Aokiji, Kizaru, Akainu) à Marineford",P,"Trio assis ou debout",1),
 ("grp_gorosei.png","One Piece","Les cinq doyens (Gorosei), formes humaines",P,"Groupe",1),
 ("grp_supernovas.png","One Piece","Les Supernovas (pire génération)",P,"Groupe",2),
 ("grp_empereurs.png","One Piece","Les quatre Empereurs de l'ère Barbe Blanche",P,"Chacun détouré ou en groupe",2),
 ("grp_z_team.png","Dragon Ball","Les Z (Goku, Vegeta, Gohan, Piccolo, Krillin…)",P,"Groupe",2),
 ("grp_exorcistes.png","Jujutsu Kaisen","Élèves de Tokyo (Yuji, Megumi, Nobara, Maki, Yuta…)",P,"Groupe",2),
]
# ---- vidéos inter-œuvres (persos d'autres œuvres + objets d'échelle)
XV = [
 ("jjk_sukuna_heian.png","Jujutsu Kaisen","Sukuna, vraie forme (4 bras, Shinjuku)",P,"Pose de combat, face",1),
 ("jjk_sukuna_yuji.png","Jujutsu Kaisen","Sukuna dans le corps de Yuji (Shibuya)",P,"Pose menaçante",1),
 ("jjk_gojo.png","Jujutsu Kaisen","Gojo sans bandeau (yeux visibles)",P,"Pose de combat, main levée",1),
 ("jjk_yuji.png","Jujutsu Kaisen","Yuji Itadori (fin du manga)",P,"Pose de combat",2),
 ("jjk_toji.png","Jujutsu Kaisen","Toji Fushiguro",P,"Pose de combat, arme",2),
 ("db_goku_ui.png","Dragon Ball","Goku Ultra Instinct (Super)",P,"Pose de combat",1),
 ("db_goku_ssj.png","Dragon Ball","Goku Super Saiyan (Namek)",P,"Pose de combat",1),
 ("db_goku_enfant.png","Dragon Ball","Goku enfant avec le bâton magique",P,"Debout",2),
 ("db_vegeta.png","Dragon Ball","Vegeta (Super, Ultra Ego si possible)",P,"Pose de combat",2),
 ("db_freezer.png","Dragon Ball","Freezer forme finale",P,"Debout, doigt levé",1),
 ("db_kid_buu.png","Dragon Ball","Kid Buu",P,"Pose de combat",2),
 ("db_roshi.png","Dragon Ball","Tortue géniale en pleine puissance (MAX)",P,"Kamehameha",2),
 ("db_gohan_beast.png","Dragon Ball","Gohan Beast",P,"Pose de combat",2),
 ("echelle_humain.png","Réel","Silhouette d'humain adulte normal",O,"De face, sans visage reconnaissable, détourée",1),
 ("echelle_lune.png","Réel","La Lune",O,"Image de la NASA ou libre de droits, détourée",1),
 ("echelle_terre.png","Réel","La Terre vue de l'espace",O,"Libre de droits, détourée",1),
 ("echelle_champignon.png","Réel","Champignon d'explosion nucléaire (archive)",O,"Archive publique, fond conservé",1),
 ("echelle_ville.png","Réel","Ville vue du ciel",D,"Photo libre de droits",2),
 ("echelle_montagne.png","Réel","Montagne",D,"Photo libre de droits",2),
 ("echelle_meteorite.png","Réel","Météorite ou cratère (Meteor Crater, Arizona)",D,"Photo libre de droits",2),
 ("echelle_ours.png","Réel","Ours brun",O,"Debout, détouré, libre de droits",3),
 ("echelle_soldat.png","Réel","Soldat avec fusil (silhouette)",O,"Silhouette détourée",2),
]
# ---- edits sur la musique (à affiner ensemble)
ED = [
 ("edit_<perso>_case_01.png … _10.png","Toutes","10 cases de manga emblématiques par perso, en haute définition",R,"Scans nets, une case par fichier, sans texte de traduction si possible",2),
 ("edit_<perso>_regard.png","Toutes","Gros plan des yeux du perso (Sharingan, Six Yeux…)",R,"Recadré serré, haute définition",2),
 ("edit_<perso>_aura.png","Toutes","Perso avec aura ou transformation, détouré",P,"Aura incluse dans le détourage",2),
 ("edit_impact_*.png","Toutes","Cases d'impact (coup qui touche, onde de choc)",R,"Plein cadre, très contrasté",3),
 ("edit_onomatopees_*.png","Toutes","Onomatopées dessinées extraites des pages (ドン, ゴゴゴ…)",O,"Détourées, fond transparent",3),
]
VID = [
 (1,"Naruto","Itachi vs Minato",["itachi_combat.png","itachi_face.png","minato_combat.png","minato_droite.png"],"Faite (v3)"),
 (2,"Naruto","Itachi vs Madara",["itachi_combat.png","itachi_face.png","madara_edo.png","madara_jubi.png"],""),
 (3,"Naruto","Madara vs Hashirama",["madara_edo.png","hashirama.png","dec_vallee_fin.jpg"],""),
 (4,"Naruto","Itachi en bonne santé vs Nagato (Pain)",["itachi_combat.png","nagato_pain.png","dec_konoha_detruit.jpg"],""),
 (5,"Naruto","Jiraiya vs Itachi",["jiraiya.png","itachi_combat.png"],""),
 (6,"Naruto","Kakashi double Mangekyō vs Obito",["kakashi_guerre.png","kakashi_double_ms.png","obito_masque_debout.png"],""),
 (7,"Naruto","Gai 8e Porte vs Madara",["gai_8portes.png","madara_jubi.png","dec_guerre4.jpg"],""),
 (8,"Naruto","Naruto vs Sasuke (Vallée de la Fin)",["naruto_6chemins.png","sasuke_6chemins.png","dec_vallee_fin.jpg"],""),
 (9,"Naruto","Minato vs A (4e Raikage)",["minato_combat.png","raikage.png"],""),
 (10,"Naruto","Jiraiya vs Orochimaru",["jiraiya.png","orochimaru.png"],""),
 (11,"Naruto","Le plus fort des Sannin",["jiraiya.png","orochimaru.png","tsunade.png"],""),
 (12,"Naruto","Minato vs Tobirama",["minato_combat.png","tobirama.png","kunai_hiraishin.png"],""),
 (13,"Naruto","Sasuke vs Itachi (le vrai combat)",["sasuke_hebi.png","itachi_combat.png","dec_uchiha.jpg"],""),
 (14,"Naruto","Kisame vs Gai",["kisame.png","gai_normal.png"],""),
 (15,"Naruto","Shisui vs Itachi",["shisui.png","itachi_combat.png"],""),
 (16,"Naruto","Hiruzen à son apogée vs Itachi",["hiruzen_jeune.png","itachi_combat.png"],""),
 (17,"Naruto","Rock Lee vs Gaara",["rock_lee.png","gaara.png","dec_examen_chunin.jpg"],""),
 (18,"Naruto","Deidara vs Sasori",["deidara.png","sasori.png"],""),
 (19,"Naruto","Naruto mode ermite vs Pain",["naruto_ermite.png","nagato_pain.png","dec_konoha_detruit.jpg"],""),
 (20,"Naruto","Kakashi vs Itachi",["kakashi_guerre.png","itachi_combat.png"],""),
 (21,"Naruto","Danzō vs Itachi",["danzo.png","itachi_combat.png"],""),
 (22,"Naruto","Kaguya vs Madara réceptacle de Jûbi",["kaguya.png","madara_jubi.png"],""),
 (23,"Naruto","Isshiki vs Naruto mode Baryon",["isshiki.png","naruto_baryon.png"],""),
 (24,"Naruto","Boruto (TBV) vs Kawaki",["boruto_tbv.png","kawaki.png"],""),
 (25,"Naruto","Obito vs Minato (nuit de Kyûbi)",["obito_masque_debout.png","minato_combat.png"],""),
 (26,"One Piece","Mihawk vs Shanks",["mihawk.png","shanks.png"],""),
 (27,"One Piece","Akainu vs Aokiji",["akainu.png","aokiji.png","dec_punk_hazard.jpg"],""),
 (28,"One Piece","Garp vs Akainu",["garp_vieux.png","akainu.png"],""),
 (29,"One Piece","Barbe Blanche à son apogée vs Kaido",["barbe_blanche_jeune.png","kaido_humain.png"],""),
 (30,"One Piece","Luffy Gear 5 vs Kaido",["luffy_gear5.png","kaido_humain.png","dec_onigashima.jpg"],""),
 (31,"One Piece","Zoro vs Sanji",["zoro.png","sanji.png"],""),
 (32,"One Piece","Zoro vs Mihawk",["zoro.png","mihawk.png"],""),
 (33,"One Piece","Shanks vs Kaido",["shanks.png","kaido_humain.png"],""),
 (34,"One Piece","Roger vs Barbe Blanche",["roger.png","barbe_blanche_jeune.png"],""),
 (35,"One Piece","Rayleigh vs Gaban",["rayleigh_jeune.png","gaban.png"],""),
 (36,"One Piece","Kizaru vs Marco",["kizaru.png","marco.png","dec_marineford.jpg"],""),
 (37,"One Piece","Big Mom vs Kaido",["big_mom.png","kaido_humain.png"],""),
 (38,"One Piece","Luffy vs Katakuri",["luffy_base.png","katakuri.png","dec_wci.jpg"],""),
 (39,"One Piece","Barbe Noire vs Shanks",["barbe_noire.png","shanks.png"],""),
 (40,"One Piece","Law vs Kid",["law.png","kid.png"],""),
 (41,"One Piece","Sabo vs Fujitora",["sabo.png","fujitora.png","dec_dressrosa.jpg"],""),
 (42,"One Piece","Yamato vs Zoro",["yamato.png","zoro.png"],""),
 (43,"One Piece","Loki vs Luffy",["loki.png","luffy_gear5.png","dec_elbaf.jpg"],""),
 (44,"One Piece","Rocks vs Roger (God Valley)",["rocks.png","roger.png","dec_god_valley.jpg"],""),
 (45,"One Piece","Garp vs Aokiji (Egghead)",["garp_vieux.png","aokiji.png","dec_egghead.jpg"],""),
 (46,"One Piece","Kizaru vs Luffy Gear 5",["kizaru.png","luffy_gear5.png","dec_egghead.jpg"],""),
 (47,"One Piece","Doflamingo vs Crocodile",["doflamingo.png","crocodile.png"],""),
 (48,"One Piece","King vs Zoro",["king.png","zoro.png"],""),
 (49,"One Piece","Ace vs Sabo",["ace.png","sabo.png"],""),
 (50,"One Piece","Luffy vs Shanks",["luffy_gear5.png","shanks.png"],""),
]

wb = Workbook()
F = "Arial"; hdr = Font(name=F, bold=True, color="FFFFFF"); body = Font(name=F, size=10); bold = Font(name=F, bold=True, size=10)
HF = PatternFill("solid", fgColor="18140F"); RECU = PatternFill("solid", fgColor="E2EFDA"); TODO = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="BFBFBF"); BRD = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
STATUTS = '"À chercher,Trouvé,Reçu,Introuvable"'

def table(ws, headers, rows, widths, status_col=None):
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(1, c); cell.font = hdr; cell.fill = HF; cell.alignment = Alignment(wrap_text=True, vertical="center"); cell.border = BRD
    for r in rows:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for cell in row:
            cell.font = body; cell.alignment = wrap; cell.border = BRD
        if status_col:
            st = row[status_col - 1].value
            fill = RECU if st == "Reçu" else TODO if st == "À chercher" else None
            if fill: row[status_col - 1].fill = fill
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "B2"; ws.auto_filter.ref = ws.dimensions
    if status_col:
        dv = DataValidation(type="list", formula1=STATUTS, allow_blank=True); ws.add_data_validation(dv)
        dv.add(f"{get_column_letter(status_col)}2:{get_column_letter(status_col)}{ws.max_row + 40}")

# 1) Mode d'emploi
ws = wb.active; ws.title = "Mode d'emploi"
lines = [
 ("LE VERDICT — images à fournir pour les 50 premières vidéos", True),
 ("", False),
 ("Comment remplir", True),
 ("1. Cherche chaque image des onglets « Naruto », « One Piece », « Décors », « Portraits » et « Effets & objets ».", False),
 ("2. Enregistre-la sous le nom exact de la colonne « Fichier » (minuscules, sans espaces), dans le dossier indiqué ci-dessous.", False),
 ("3. Mets à jour la colonne « Statut » (liste déroulante : À chercher / Trouvé / Reçu / Introuvable). Seule cette colonne et « Remarque » sont à modifier.", False),
 ("Nouveaux onglets : « Combats de groupe », « Inter-œuvres » (persos de Dragon Ball et Jujutsu Kaisen + objets d'échelle réels) et « Edits » (cases et effets pour les montages sur la musique).", False),
 ("Avant : l'onglet « Portraits » couvre maintenant tous les persos importants de la toile des combats, et l'onglet « Effets & objets » liste les yeux, symboles, objets et avis de recherche pour les plans les plus stylés.", False),
 ("4. L'onglet « Vidéos » se met à jour tout seul : il indique, pour chaque vidéo, combien d'images sont reçues et si elle est prête.", False),
 ("", False),
 ("Rangement du dossier", True),
 ("le_verdict/naruto/  (images de l'onglet Naruto)   ·   le_verdict/one_piece/   ·   le_verdict/decors/   ·   le_verdict/portraits/", False),
 ("", False),
 ("Les catégories", True),
 ("Pied détouré : personnage entier de la tête aux pieds, fond transparent (PNG), au moins 1 000 px de haut, sans ombre portée ni décor ni texte.", False),
 ("Buste détouré : de la taille à la tête, fond transparent (PNG), au moins 800 px de haut. Utile quand le visage ou un détail (yeux, Sharingan) compte.", False),
 ("Visage détouré (PNG) : tête et haut des épaules, fond transparent, au moins 600 px. Remplit les cercles de la toile. Une capture avec fond reste acceptée, je la découpe en cercle.", False),
 ("Décor (capture) : image de lieu sans personnage au premier plan si possible, au moins 1 280 px de large, JPG. Je la passe en trame de manga, la qualité compte peu.", False),
 ("Objet détouré : objet seul (kunai, sabre…), fond transparent (PNG).", False),
 ("", False),
 ("Orientation", True),
 ("« Vers la droite » / « Vers la gauche » = le personnage regarde ou attaque dans cette direction. Pour un duel, l'un regarde à droite, l'autre à gauche. Si tu ne trouves que l'autre sens, mets-le quand même : je retourne l'image (sauf texte ou symbole asymétrique).", False),
 ("", False),
 ("Priorité", True),
 ("1 = indispensable pour la vidéo · 2 = rend la vidéo bien meilleure · 3 = bonus si tu tombes dessus.", False),
 ("", False),
 ("À éviter", True),
 ("Images avec filigrane ou logo, fan arts au style très différent de l'anime, images générées par IA, détourages baveux (contour gris ou blanc), images trop petites agrandies.", False),
 ("", False),
 ("Exemple de ligne déjà remplie : voir « itachi_combat.png » dans l'onglet Naruto (statut Reçu, fichier d'origine noté en remarque).", False),
]
for i, (s, b) in enumerate(lines, 1):
    c = ws.cell(i, 1, s); c.font = Font(name=F, bold=b, size=14 if i == 1 else 10); c.alignment = Alignment(wrap_text=True, vertical="top")
ws.column_dimensions["A"].width = 130

H = ["Fichier", "Personnage", "Version / époque", "Catégorie", "Pose", "Orientation", "Tenue et détails à vérifier", "Priorité", "Utilisée dans (vidéos n°)", "Statut", "Remarque"]
W = [26, 18, 30, 18, 34, 15, 44, 9, 18, 13, 34]
use = {}
for n, _, _, files, _ in VID:
    for f in files: use.setdefault(f, []).append(n)
used = lambda f: ", ".join(map(str, use.get(f, []))) or "réseau / plans courts"
ws = wb.create_sheet("Naruto")
table(ws, H, [(f, p, v, c, po, o, t, pr, used(f), st, ("fichier reçu : " + rec) if rec else "") for f, p, v, c, po, o, t, pr, st, rec in NAR], W, status_col=10)
ws = wb.create_sheet("One Piece")
table(ws, H, [(f, p, v, c, po, o, t, pr, used(f), "À chercher", "") for f, p, v, c, po, o, t, pr in OP], W, status_col=10)
ws = wb.create_sheet("Décors")
table(ws, ["Fichier", "Œuvre", "Lieu", "Catégorie", "Priorité", "Utilisé dans (vidéos n°)", "Statut", "Remarque"],
      [(f, o, l, D, pr, used(f), "À chercher", "") for f, o, l, pr in DEC] + [("bg_kyubi / bg_kamui / bg_tsukuyomi", "Naruto", "Nuit de Kyûbi, dimension de Kamui, ciel rouge du Tsukuyomi", D, 1, "1", "Reçu", "déjà fournis")],
      [26, 12, 52, 18, 9, 18, 13, 30], status_col=7)
ws = wb.create_sheet("Portraits")
rows = [(f"p_{n}.jpg", "Naruto", n.replace("_", " ").title(), R, 3, "À chercher", "visage centré, de face ou de trois quarts") for n in PORT_N]
rows += [(f"p_{n}.jpg", "One Piece", n.replace("_", " ").title(), R, 3, "À chercher", "visage centré, de face ou de trois quarts") for n in PORT_O]
rows += [(f"p_{n}.png", "Naruto", n.replace("_", " ").title(), R, 2 if i < 20 else 3, "À chercher", "toile des combats ; visage centré, de face ou de trois quarts") for i, n in enumerate(PORT_N2)]
rows += [(f"p_{n}.png", "One Piece", n.replace("_", " ").title(), R, 2 if i < 20 else 3, "À chercher", "toile des combats ; visage centré, de face ou de trois quarts") for i, n in enumerate(PORT_O2)]
rows += [(f"p_{n}.webp", "Naruto", n.title(), R, 3, "Reçu", "déjà fourni") for n in ["madara", "hashirama", "naruto", "sasuke", "jiraiya", "orochimaru", "nagato", "kisame", "gai", "tsunade"]]
table(ws, ["Fichier", "Œuvre", "Personnage", "Catégorie", "Priorité", "Statut", "Remarque"], rows, [22, 12, 24, 20, 9, 13, 40], status_col=6)
ws.cell(ws.max_row + 2, 1, "Ces visages remplissent les cercles de la toile des combats. Idéal : PNG détouré (tête + haut des épaules, fond transparent, 600 px mini). Une capture avec fond reste acceptée : je la découpe en cercle.").font = Font(name=F, italic=True, size=10)

for title, rows_, note in [("Combats de groupe", GRP, "Pour les vidéos 2 contre 1, 3 contre 1, équipe contre équipe : des groupes déjà composés font gagner beaucoup de temps."),
                           ("Inter-œuvres", XV, "Pour les vidéos inter-œuvres (2 min) : persos des autres œuvres, et objets d'échelle (humain, ville, montagne, Lune, Terre) pour montrer « tant de fois un humain ». Les photos réelles doivent être libres de droits (NASA, Wikimedia Commons)."),
                           ("Edits", ED, "Pour les edits sur la musique : liste de départ, à affiner ensemble. Remplace <perso> par l'identifiant du perso (itachi, luffy…).")]:
    ws = wb.create_sheet(title)
    table(ws, ["Fichier", "Œuvre", "Quoi", "Catégorie", "Pose / composition", "Priorité", "Statut", "Remarque"], [(f, o, q, c, d, pr, "À chercher", "") for f, o, q, c, d, pr in rows_], [30, 14, 46, 18, 44, 9, 13, 30], status_col=7)
    ws.cell(ws.max_row + 2, 1, note).font = Font(name=F, italic=True, size=10)
ws = wb.create_sheet("Effets & objets")
table(ws, ["Fichier", "Œuvre", "Quoi", "Catégorie", "Détails", "Priorité", "Statut", "Remarque"], [(f, o, q, c, d, pr, "À chercher", "") for f, o, q, c, d, pr in FX], [28, 12, 46, 18, 50, 9, 13, 30], status_col=7)
ws.cell(ws.max_row + 2, 1, "Ces éléments servent aux transitions, tampons et plans « fancy » (yeux en gros plan, symboles, avis de recherche…). Aucun n'est bloquant pour une vidéo.").font = Font(name=F, italic=True, size=10)

# 5) Vidéos, avec suivi automatique
ws = wb.create_sheet("Vidéos")
hv = ["N°", "Œuvre", "Duel", "Image 1", "Image 2", "Image 3", "Image 4", "Images nécessaires", "Images reçues", "Prête ?", "État"]
ws.append(hv)
for c in range(1, len(hv) + 1):
    cell = ws.cell(1, c); cell.font = hdr; cell.fill = HF; cell.alignment = Alignment(wrap_text=True, vertical="center"); cell.border = BRD
for i, (n, o, duel, files, etat) in enumerate(VID, start=2):
    f4 = (files + ["", "", "", ""])[:4]
    ws.append([n, o, duel] + f4 + [None, None, None, etat])
    ws.cell(i, 8, f'=COUNTA(D{i}:G{i})')
    rec = "+".join(f"SUMPRODUCT(COUNTIFS('{sh}'!$A$2:$A$200,D{i}:G{i},'{sh}'!${col}$2:${col}$200,\"Reçu\"))" for sh, col in [("Naruto", "J"), ("One Piece", "J"), ("Décors", "G")])
    ws.cell(i, 9, "=" + rec)
    ws.cell(i, 10, f'=IF(I{i}>=H{i},"OUI","NON")')
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    for cell in row:
        cell.font = body; cell.border = BRD; cell.alignment = Alignment(vertical="top", wrap_text=True)
for col, w in zip("ABCDEFGHIJK", [5, 11, 40, 24, 24, 22, 20, 11, 11, 9, 14]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "D2"
last = ws.max_row
ws.cell(last + 2, 3, "Vidéos prêtes").font = bold
ws.cell(last + 2, 4, f'=COUNTIF(J2:J{last},"OUI")')
ws.cell(last + 3, 3, "Images uniques encore à chercher").font = bold
ws.cell(last + 3, 4, "=COUNTIF('Naruto'!J2:J200,\"À chercher\")+COUNTIF('One Piece'!J2:J200,\"À chercher\")+COUNTIF('Décors'!G2:G200,\"À chercher\")")
ws.cell(last + 4, 3, "Les colonnes H à J se calculent seules à partir des statuts des autres onglets.").font = Font(name=F, italic=True, size=9)
wb.save("images_le_verdict.xlsx"); print("ok")
