# L'Attaque des Titans, partie 1 : tout le manga d'Isayama (ch. 1-139), flash-back compris.
# Manga uniquement : pas de scènes propres à l'anime, pas d'OAD ni de « No Regrets ». "fight" est injecté par data.py.
# Numéros et titres de chapitres vérifiés sur la liste des chapitres (Wikipedia) et les résumés d'arc du wiki
# (fandom) ; "ch. ~N" = à un ou deux chapitres près.
# Repères de temps (t = années depuis la chute du mur Maria, an 845 = 0) : Marcel dévoré -0,02, chute -0,01,
# Grisha contre Frieda 0,001 (même jour), entraînement de la 104e 2-5, Trost 5,00-5,02, 57e expédition 5,10-5,11,
# Stohess 5,15, Utgard 5,20, Clash des Titans 5,21, insurrection 5,40-5,45, reconquête du mur Maria 5,80-5,81,
# ellipse de quatre ans, fort Slava 8,9, Liberio 9,00-9,01, guerre pour Paradis 9,10-9,105, Originel 9,12,
# Grondement 9,2-9,25, bataille du Ciel et de la Terre 9,30-9,31.
# Flash-back : Kenny massacre la Brigade spéciale -25 et tente de tuer Uri -24 (estimations : Kenny a la
# cinquantaine en 850), Kruger sur le mur de Paradis -12 (Grisha arrive sur l'île vers 832-833), enlèvement de
# Mikasa -1 (Eren et Mikasa ont 9 ans). Ces dates de flash-back sont des estimations, pas des dates du manga.

CHARS_PART = {
    # ---------------------------------------------------------------- 104e brigade et Bataillon d'exploration
    "eren": ("Eren Jäger", "Bataillon d'exploration", 0.3, 9.3101, None),
    "mikasa": ("Mikasa Ackerman", "Bataillon d'exploration", 1.6, None, None),
    "armin": ("Armin Arlelt", "Bataillon d'exploration", 0.8, None, None),
    "jean": ("Jean Kirschtein", "Bataillon d'exploration", 1.3, None, None),
    "connie": ("Connie Springer", "Bataillon d'exploration", 1.1, None, None),
    "sasha": ("Sasha Braus", "Bataillon d'exploration", 1.1, 9.0101, None),
    "historia": ("Historia Reiss (Christa Lenz)", "Bataillon d'exploration", 0.8, None, None),
    "marco": ("Marco Bodt", "104e brigade", 1.2, 5.0006, None),
    "levi": ("Livaï Ackerman", "Bataillon d'exploration", 6.0, None, None),
    "erwin": ("Erwin Smith", "Bataillon d'exploration", 2.5, 5.8055, None),
    "hange": ("Hansi Zoë", "Bataillon d'exploration", 2.5, 9.2501, None),
    "mike": ("Mike Zacharias", "Bataillon d'exploration", 3.5, 5.2002, None),
    "petra": ("Petra Ral", "Escouade Livaï", 2.8, 5.1061, None),
    "oruo": ("Oruo Bozado", "Escouade Livaï", 2.8, 5.1061, None),
    "eld": ("Eld Jinn", "Escouade Livaï", 2.8, 5.1061, None),
    "gunther": ("Gunther Schultz", "Escouade Livaï", 2.7, 5.1041, None),
    "hannes": ("Hannes", "Garnison", 1.0, 5.2141, None),
    "floch": ("Floch Forster", "Yeageristes", 1.5, 9.2401, None),
    # ---------------------------------------------------------------- guerriers de Mahr et Titans de l'ennemi
    "reiner": ("Reiner Braun (Titan Cuirassé)", "Guerriers de Mahr", 4.3, None, None),
    "bertholdt": ("Bertolt Hoover (Titan Colossal)", "Guerriers de Mahr", 5.0, 5.81, None),
    "annie": ("Annie Leonhart (Titan Féminin)", "Guerriers de Mahr", 4.8, None, None),
    "zeke": ("Zeke Jäger (Titan Bestial)", "Guerriers de Mahr", 5.5, 9.3051, None),
    "pieck": ("Pieck Finger (Titan Charrette)", "Guerriers de Mahr", 3.8, None, None),
    "porco": ("Porco Galliard (Titan Mâchoire)", "Guerriers de Mahr", 4.3, 9.103, None),
    "marcel": ("Marcel Galliard (Titan Mâchoire)", "Guerriers de Mahr", 3.5, -0.0199, None),
    "gabi": ("Gabi Braun", "Guerriers de Mahr", 1.2, None, None),
    "falco": ("Falco Grice", "Guerriers de Mahr", 0.8, None, None),
    "lara": ("Lara Tybur (Titan Marteau d'armes)", "Famille Tybur", 5.0, 9.0041, None),
    "magath": ("Theo Magath", "Armée de Mahr", 2.0, 9.215, None),
    "ymir": ("Ymir (Titan Mâchoire)", "Bataillon d'exploration", 1.5, 6.0, None),
    "dina": ("Dina Fritz (Titan souriant)", "Titans purs", 1.8, 5.2151, None),
    # ---------------------------------------------------------------- famille royale, Ackerman, Grisha
    "kenny": ("Kenny Ackerman (l'Éventreur)", "Brigade spéciale", 5.0, 5.46, None),
    "traute": ("Traute Carven", "Brigade spéciale", 3.0, 5.445, None),
    "uri": ("Uri Reiss (Titan Originel)", "Famille Reiss", 6.0, -10.0, None),
    "frieda": ("Frieda Reiss (Titan Originel)", "Famille Reiss", 4.5, 0.0011, None),
    "rod": ("Rod Reiss (Titan pur géant)", "Famille Reiss", 2.0, 5.4501, None),
    "grisha": ("Grisha Jäger (Titan Assaillant)", "Restaurationnistes eldiens", 3.0, 0.01, None),
    "kruger": ("Eren Kruger, le Hibou (Titan Assaillant)", "Restaurationnistes eldiens", 4.0, -11.9, None),
    # ---------------------------------------------------------------- groupes
    "titans_purs": ("Titans purs (groupe)", "Titans purs", 1.3, None, None),
    "titans_colossaux": ("Titans colossaux des murs (groupe)", "Titans purs", 4.0, None, None),
    "titans_du_passe": ("Titans des anciens détenteurs, invoqués par l'Originel (groupe)", "Titans purs", 5.0, None, None),
    "bataillon": ("Soldats du Bataillon d'exploration (groupe)", "Bataillon d'exploration", 1.8, None, None),
    "garnison": ("Soldats de la Garnison (groupe)", "Garnison", 1.0, None, None),
    "brigade_speciale": ("Brigade spéciale (groupe)", "Brigade spéciale", 1.0, None, None),
    "escouade_kenny": ("Escouade anti-personnel de Kenny (groupe)", "Brigade spéciale", 3.0, None, None),
    "voyous": ("Ravisseurs et hommes de main (groupe)", "Civils", 0.4, None, None),
    "armee_mahr": ("Armée de Mahr (groupe)", "Armée de Mahr", 1.5, None, None),
    "flotte_mahr": ("Flotte de Mahr (groupe)", "Armée de Mahr", 2.0, None, None),
    "armee_moyen_orient": ("Alliance du Moyen-Orient, armée (groupe)", "Alliance du Moyen-Orient", 1.5, None, None),
    "flotte_moyen_orient": ("Alliance du Moyen-Orient, flotte (groupe)", "Alliance du Moyen-Orient", 2.0, None, None),
    "yeageristes": ("Yeageristes (groupe)", "Yeageristes", 1.5, None, None),
}

GENERIC_PART = {"titans_purs", "titans_colossaux", "titans_du_passe", "bataillon", "garnison", "brigade_speciale",
                "escouade_kenny", "voyous", "armee_mahr", "flotte_mahr", "armee_moyen_orient", "flotte_moyen_orient",
                "yeageristes"}

# gains et pertes permanents : (perso, temps, changement moyen en échelons, écart-type, libellé)
JUMPS_PART = [
    ("eren", 3.0, 0.8, 0.4, "Entraînement de la 104e brigade, 5e de la promotion (ch. 3-4, 17-18)"),
    ("eren", 5.0025, 2.2, 0.6, "Première transformation en Titan Assaillant, dans le ventre d'un Titan (ch. 9-10)"),
    ("eren", 5.445, 0.7, 0.4, "Durcissement acquis en buvant le sérum « Armure » de Rod Reiss (ch. 66-67)"),
    ("eren", 5.6, 0.3, 0.3, "Maîtrise du durcissement : lames et poings durcis (ch. 70-71)"),
    ("eren", 7.5, 0.6, 0.4, "Ellipse de quatre ans : souvenirs du Titan Assaillant, infiltration de Mahr (ch. 90-100)"),
    ("eren", 9.0042, 0.6, 0.4, "Titan Marteau d'armes : Eren dévore Lara Tybur (ch. 103-104)"),
    ("eren", 9.12, 3.5, 0.8, "Titan Originel : contact avec Zeke, Ymir se range du côté d'Eren dans les Chemins (ch. 120-122)"),
    ("mikasa", 3.0, 1.6, 0.5, "Entraînement : major de la 104e brigade (ch. 3-4, 17)"),
    ("mikasa", 7.5, 0.4, 0.3, "Ellipse de quatre ans, soldate d'élite du Bataillon (ch. 90-105)"),
    ("armin", 3.0, 0.3, 0.3, "Entraînement de la 104e brigade (ch. 3-4)"),
    ("armin", 5.81, 3.5, 0.8, "Titan Colossal : sérum d'Erwin, Armin dévore Bertolt (ch. 83-84)"),
    ("armin", 7.5, 0.3, 0.3, "Ellipse de quatre ans, maîtrise du Colossal (ch. 90-102)"),
    ("jean", 7.5, 0.5, 0.3, "Ellipse de quatre ans, vétéran et chef d'escouade de fait (ch. 90-105)"),
    ("connie", 7.5, 0.4, 0.3, "Ellipse de quatre ans (ch. 90-105)"),
    ("sasha", 7.5, 0.4, 0.3, "Ellipse de quatre ans (ch. 90-105)"),
    ("reiner", 3.0, 0.4, 0.3, "Entraînement de la 104e brigade, 2e de la promotion (ch. 3-4)"),
    ("ymir", -0.005, 2.0, 0.6, "Ymir dévore Marcel : redevenue humaine avec le Titan Mâchoire (ch. 95, ch. 89)"),
    ("falco", 9.1035, 3.2, 0.8, "Titan Mâchoire : Falco, changé en Titan pur, dévore Porco (ch. 118-119)"),
    ("falco", 9.29, 0.3, 0.3, "Titan Mâchoire ailé, effet de la moelle de Zeke (ch. 133-134)"),
    ("levi", 9.1015, -0.6, 0.4, "Blessures de la lance foudroyante de Zeke : visage balafré, doigts perdus (ch. 115-116)"),
]

# ============================================================== Jeunesse de Kenny (flash-back)
fight(-25.0, "kenny", "kenny", "brigade_speciale", "A", 3,
      note="Kenny l'Éventreur égorge plus de cent membres de la Brigade spéciale de la capitale (ch. 57, ch. 69)")
fight(-24.0, "kenny", "uri", "kenny", "A", 3,
      note="Kenny tente d'assassiner Uri Reiss ; Uri, en Titan, le saisit puis l'épargne (ch. 69)")

# ============================================================== Grisha et le Hibou (flash-back)
fight(-12.0, "hibou", "kruger", "armee_mahr", "A", 3, ta=["surprise"],
      note="Eren Kruger, le Hibou, se transforme sur le mur de Paradis et dévore les officiers de Mahr (ch. 88)")

# ============================================================== Enfance à Shiganshina
fight(-1.001, "avant", "eren", "voyous", "A", 2, ta=["surprise"],
      note="Eren, 9 ans, poignarde deux des ravisseurs de Mikasa (ch. 6)")
fight(-1.0, "avant", "mikasa", "voyous", "A", 2,
      note="Éveil Ackerman de Mikasa : elle tue le troisième ravisseur d'un coup de couteau (ch. 6)")

# ============================================================== Chute du mur Maria (845)
fight(-0.02, "chute", "ymir", "marcel", "A", 3, ta=["surprise"],
      note="Ymir, Titan pur errant depuis 60 ans, dévore Marcel Galliard par surprise (ch. 95)")
fight(-0.01, "chute", "bertholdt", "garnison", "A", 3, ta=["surprise"],
      note="Le Titan Colossal enfonce la porte de Shiganshina (ch. 1-2)")
fight(-0.009, "chute", "dina", "hannes", "A", 1,
      note="Hannes renonce à affronter le Titan souriant et fuit avec Eren et Mikasa ; Carla est dévorée (ch. 2)", flags="?")
fight(-0.008, "chute", "reiner", "garnison", "A", 3,
      note="Le Titan Cuirassé enfonce la porte intérieure du mur Maria (ch. 2-3)")
fight(0.001, "chute", "grisha", "frieda", "A", 1,
      note="Grisha, Titan Assaillant, contre le Titan Originel de Frieda Reiss, inexpérimentée : d'abord dominé, "
           "il l'arrache de sa nuque et la dévore (ch. 121)")

# ============================================================== 104e brigade d'entraînement
fight(3.9, "entrainement", "annie", "eren", "A", 2,
      note="Corps-à-corps : Annie projette Eren et lui montre sa technique (ch. 17)", flags="?")
fight(3.901, "entrainement", "annie", "reiner", "A", 2, tb=["retenue"],
      note="Annie soulève et projette Reiner, qui cache sa force (ch. 17)", flags="?")
fight(3.95, "entrainement", "eren", "jean", "A", 1,
      note="Eren met Jean au sol avec la technique d'Annie (ch. ~18) ; exercice, pas un vrai combat", flags="?")

# ============================================================== Bataille de Trost
fight(5.0, "trost", "bertholdt", "eren", "D",
      note="Eren attaque le Titan Colossal sur le mur ; il s'évapore (ch. 4-5)", flags="i")
fight(5.0005, "trost", ["reiner", "annie", "bertholdt"], "marco", "A", 3, ta=["surprise"],
      note="Les trois guerriers retirent l'équipement tridimensionnel de Marco et le livrent à un Titan (souvenir, ch. 77)")
fight(5.001, "trost", "titans_purs", "eren", "A", 3,
      note="Escouade 34 décimée ; Eren perd une jambe et est avalé en sauvant Armin (ch. 4-5)")
fight(5.0015, "trost", "mikasa", "titans_purs", "A", 3, note="Mikasa tranche une série de Titans dans Trost (ch. 6-8)")
fight(5.002, "trost", "titans_purs", "mikasa", "A", 1, tb=["epuise"],
      note="À court de gaz, Mikasa tombe face à un Titan ; le Titan d'Eren la sauve (ch. 8-9)", flags="i")
fight(5.003, "trost", "eren", "titans_purs", "A", 3,
      note="Première transformation : le Titan d'Eren massacre les Titans à mains nues (ch. 9-10)")
fight(5.004, "trost", ["mikasa", "reiner", "annie", "bertholdt", "jean", "connie", "sasha"], "titans_purs", "A", 2,
      ta=["prepa"], note="Plan d'Armin au QG de ravitaillement : sept Titans tués d'un même assaut (ch. 9-10)")
fight(5.01, "trost", ["eren", "mikasa", "armin", "garnison"], "titans_purs", "A", 2,
      note="Opération du rocher : Armin réveille Eren, qui bouche la brèche sous la garde des escouades d'élite (ch. 14-19)")
fight(5.012, "trost", "levi", "titans_purs", "A", 3, note="Arrivée de Livaï, il tranche les Titans autour d'Eren (ch. 19)")

# ============================================================== 57e expédition et Titan Féminin
fight(5.1, "feminin", "annie", "bataillon", "A", 3, note="Le Titan Féminin écrase l'aile droite de la formation (ch. 22-23)")
fight(5.1005, "feminin", "annie", "armin", "A", 3, note="Annie soulève la capuche d'Armin et l'épargne (ch. 23)")
fight(5.101, "feminin", "annie", ["jean", "armin"], "A", 2,
      note="Jean et Armin tentent de la retarder avec Reiner ; elle les écarte (ch. 23-24)", flags="i")
fight(5.102, "feminin", "annie", "bataillon", "A", 3,
      note="Arrière-garde massacrée à l'entrée de la forêt des Titans géants (ch. 24-25)")
fight(5.103, "feminin", ["levi", "mike", "bataillon"], "annie", "D", ta=["prepa"],
      note="Piège d'Erwin : le Titan Féminin immobilisé par les harpons ; elle durcit sa nuque contre Livaï et Mike "
           "et appelle les Titans qui dévorent son corps (ch. 26-27)", flags="i")
fight(5.104, "feminin", "annie", "gunther", "A", 3, ta=["surprise"],
      note="Annie, en tridimensionnel et encapuchonnée, tranche la nuque de Gunther (ch. 28)")
fight(5.105, "feminin", ["eld", "petra", "oruo"], "annie", "A", 1,
      note="Eld, Petra et Oruo aveuglent le Titan Féminin et lui tranchent les bras (ch. 28)", flags="i")
fight(5.106, "feminin", "annie", ["eld", "petra", "oruo"], "A", 3,
      note="Un œil régénéré à temps, elle tue Eld, Petra puis Oruo (ch. 28-29)")
fight(5.107, "feminin", "annie", "eren", "A", 3,
      note="Eren contre le Titan Féminin : poing durci d'Annie, Eren décapité et avalé (ch. 29-30)")
fight(5.108, "feminin", ["levi", "mikasa"], "annie", "A", 2,
      note="Livaï déchiquette le Titan Féminin et libère Eren ; il se blesse à la jambe en protégeant Mikasa (ch. 30-31)")

# ============================================================== District de Stohess
fight(5.15, "stohess", "annie", ["mikasa", "eren", "armin"], "A", 1,
      note="Dans le passage souterrain, Annie se transforme malgré Mikasa ; Eren ne parvient pas à se transformer (ch. 32)",
      flags="i")
fight(5.151, "stohess", "annie", "bataillon", "A", 2, note="Le Titan Féminin traverse les pièges de Hansi dans Stohess (ch. 32-33)")
fight(5.152, "stohess", ["eren", "mikasa"], "annie", "A", 2,
      note="Eren domine le Titan Féminin ; Mikasa tranche ses doigts sur le mur, Annie se cristallise (ch. 33-34)")

# ============================================================== Mur Rose et Utgard
fight(5.2, "utgard", "mike", "titans_purs", "A", 3, note="Mike tue cinq Titans pour couvrir la retraite (ch. 35)")
fight(5.2001, "utgard", "zeke", "mike", "A", 3, tb=["epuise"],
      note="Le Titan Bestial arrache le cheval de Mike et le livre à ses Titans (ch. 35-36)")
fight(5.202, "utgard", "sasha", "titans_purs", "D",
      note="Sasha aveugle un Titan à l'arc pour sauver une fillette de son village (ch. ~37)", flags="i")
fight(5.204, "utgard", ["reiner", "connie"], "titans_purs", "A", 1,
      note="Reiner, mordu au bras, jette un Titan par la fenêtre de la tour d'Utgard (ch. 39)")
fight(5.205, "utgard", "titans_purs", "bataillon", "A", 2,
      note="Titans actifs la nuit : Nanaba, Gelgar et les vétérans tombent à Utgard (ch. 39-40)")
fight(5.206, "utgard", "ymir", "titans_purs", "D",
      note="Ymir se transforme et tue de nombreux Titans avant d'être submergée (ch. 40-41)", flags="i")
fight(5.207, "utgard", ["mikasa", "hange", "eren", "bataillon"], "titans_purs", "A", 3,
      note="Renforts : Mikasa et le Bataillon nettoient les Titans d'Utgard (ch. 41)")

# ============================================================== Clash des Titans
fight(5.21, "rose", "mikasa", ["reiner", "bertholdt"], "A", 1, ta=["surprise"],
      note="Après l'aveu de Reiner, Mikasa les tranche avant qu'ils ne se transforment (ch. 42)", flags="i")
fight(5.2101, "rose", "reiner", "mikasa", "A", 2, note="Les lames de Mikasa se brisent sur l'armure du Cuirassé (ch. 43)")
fight(5.2102, "rose", "eren", "reiner", "A", 1,
      note="Clé de bras apprise d'Annie : Eren arrache le bras du Cuirassé (ch. 44)", flags="i")
fight(5.2103, "rose", ["reiner", "bertholdt"], "eren", "A", 2,
      note="Le Colossal s'abat sur Eren ; Reiner l'arrache de sa nuque et l'emporte (ch. 45-46)")
fight(5.212, "rose", ["erwin", "mikasa", "bataillon"], ["reiner", "bertholdt", "ymir"], "A", 1, ta=["prepa"],
      note="Charge d'Erwin avec une horde de Titans pure attirée sur le Cuirassé ; Eren repris, Erwin perd un bras (ch. 48-50)")
fight(5.214, "rose", "dina", "hannes", "A", 3, note="Le Titan souriant dévore Hannes (ch. 50)")
fight(5.215, "rose", "eren", "dina", "A", 3, ta=["aide"],
      note="Cri de la Coordonnée (contact avec le sang royal de Dina) : les Titans dévorent le Titan souriant (ch. 50)")
fight(5.216, "rose", "eren", ["reiner", "bertholdt"], "A", 1, ta=["aide"],
      note="Les Titans se jettent sur le Cuirassé, qui fuit en abandonnant Eren (ch. 50)")

# ============================================================== Insurrection
fight(5.4, "insurrection", ["levi", "mikasa"], "voyous", "A", 3,
      note="L'escouade Livaï prend en embuscade les hommes de la compagnie Reeves (ch. 54)")
fight(5.41, "insurrection", "levi", "kenny", "A", 1,
      note="Embuscade de Kenny dans un bar : Livaï lui tire dessus avec le fusil du patron et s'échappe (ch. 57-58)", flags="i")
fight(5.411, "insurrection", "levi", "escouade_kenny", "A", 2,
      note="Poursuite sur les toits : Livaï tue de nombreux membres de l'escouade anti-personnel (ch. 58)")
fight(5.412, "insurrection", "escouade_kenny", ["mikasa", "jean", "armin", "sasha", "connie"], "D",
      note="Livaï et Mikasa repoussent l'escouade, mais Eren et Historia sont emmenés (ch. 58)", flags="i")
fight(5.413, "insurrection", "armin", "escouade_kenny", "A", 1, ta=["surprise"],
      note="Armin abat la soldate qui allait tuer Jean (ch. 58-59)", flags="?")
fight(5.42, "insurrection", "hange", "brigade_speciale", "A", 2,
      note="Hansi et Moblit éliminent des membres de la Brigade spéciale à Trost (ch. 60)")
fight(5.44, "insurrection", ["levi", "mikasa", "hange", "jean", "armin", "connie", "sasha"],
      ["kenny", "traute", "escouade_kenny"], "D",
      note="Chapelle souterraine des Reiss : fumée, barils et fusées contre l'escouade de Kenny (ch. 63-65)", flags="i")
fight(5.441, "insurrection", "traute", "hange", "A", 1, note="Hansi grièvement blessée par la seconde de Kenny (ch. 64)")
fight(5.45, "insurrection", ["eren", "historia", "levi", "mikasa", "bataillon"], "rod", "A", 3, ta=["prepa"],
      note="Orvud : barils de poudre, Eren durci les fait exploser dans la bouche de Rod, Historia tranche la nuque "
           "(ch. 67-68)")

# ============================================================== Reconquête du mur Maria
fight(5.8, "shiganshina", "levi", "reiner", "A", 1, ta=["surprise"],
      note="Livaï débusque Reiner caché dans le mur et le poignarde ; il se transforme (ch. 73)", flags="i")
fight(5.801, "shiganshina", "reiner", "eren", "A", 1, note="Le Cuirassé domine Eren au corps-à-corps (ch. 74-75)", flags="i")
fight(5.802, "shiganshina", ["hange", "mikasa", "eren"], "reiner", "A", 1, ta=["lances"],
      note="Les lances foudroyantes fendent l'armure de la nuque, Reiner appelle à l'aide (ch. 75-76)", flags="i")
fight(5.803, "shiganshina", "zeke", "bataillon", "A", 3,
      note="Bombardement de pierres du Titan Bestial sur l'arrière-garde et les chevaux (ch. 76-78)")
fight(5.8035, "shiganshina", "bertholdt", ["hange", "bataillon"], "A", 3,
      note="Explosion du Colossal : l'escouade Hansi soufflée, Shiganshina rasée (ch. 77-78)")
fight(5.804, "shiganshina", "bertholdt", "eren", "A", 2, note="La vapeur du Colossal repousse Eren (ch. 78-79)")
fight(5.8045, "shiganshina", ["mikasa", "jean", "connie", "sasha"], "reiner", "A", 2, ta=["lances"],
      note="Lances foudroyantes dans la bouche du Cuirassé (Mikasa), Reiner laissé pour mort (ch. 79-80)")
fight(5.805, "shiganshina", "zeke", ["erwin", "bataillon"], "A", 2,
      note="Charge suicide d'Erwin et des recrues sous les pierres du Bestial (ch. 80)")
fight(5.806, "shiganshina", "levi", "titans_purs", "A", 3, note="Livaï tranche les Titans de Zeke (ch. 81)")
fight(5.8065, "shiganshina", "levi", "zeke", "A", 3, ta=["prepa"],
      note="Grâce à la charge d'Erwin, Livaï découpe le Titan Bestial et arrache Zeke de sa nuque ; "
           "le Titan Charrette l'emporte (ch. 81-82)")
fight(5.807, "shiganshina", ["eren", "armin"], "bertholdt", "A", 2,
      note="Armin s'accroche à la nuque brûlante en appât ; Eren, caché, arrache Bertolt (ch. 81-83)")

# ============================================================== Guerre de Mahr (fort Slava)
fight(8.9, "mahr", "gabi", "armee_moyen_orient", "A", 2, ta=["surprise"],
      note="Gabi fait sauter les rails sous le train blindé du fort Slava (ch. 91)")
fight(8.901, "mahr", ["zeke", "reiner", "porco", "pieck"], "armee_moyen_orient", "A", 2,
      note="Assaut des guerriers sur le fort Slava malgré l'artillerie anti-Titan (ch. 91-92)")
fight(8.902, "mahr", "zeke", "flotte_moyen_orient", "A", 3,
      note="Le Bestial bombarde et coule la flotte de l'Alliance du Moyen-Orient (ch. 92)")

# ============================================================== Raid sur Liberio
fight(9.0, "liberio", "eren", "armee_mahr", "A", 3, ta=["surprise"],
      note="Eren se transforme sous l'estrade, dévore Willy Tybur et massacre l'état-major (ch. 100-101)")
fight(9.001, "liberio", "lara", "eren", "A", 2,
      note="Le Marteau d'armes empale Eren et le domine avant l'intervention du Bataillon (ch. 101-102)", flags="i")
fight(9.0015, "liberio", "armin", "flotte_mahr", "A", 3,
      note="Armin se transforme en Colossal et rase le port et la flotte de Mahr (ch. 102)")
fight(9.002, "liberio", ["jean", "connie", "sasha", "bataillon"], "pieck", "A", 1, ta=["lances"],
      note="Les lances foudroyantes abattent le Titan Charrette et son armement (ch. 102-103)")
fight(9.003, "liberio", ["eren", "mikasa"], "porco", "A", 2,
      note="Mikasa et Eren mettent le Titan Mâchoire hors combat (ch. 103)")
fight(9.004, "liberio", ["eren", "mikasa"], "lara", "A", 2, ta=["lances"],
      note="Lances de Mikasa sur le Marteau d'armes ; Eren brise le cristal avec les mâchoires de Porco et dévore Lara (ch. 103-104)")
fight(9.0045, "liberio", "levi", "zeke", "A", 3, tb=["retenue"],
      note="Livaï abat le Titan Bestial ; Zeke, en secret allié d'Eren, se laisse emmener (ch. 103-104)", flags="?")
fight(9.005, "liberio", "reiner", "eren", "D",
      note="Reiner se transforme et engage Eren, qui s'échappe par le dirigeable (ch. 104)", flags="i")
fight(9.01, "liberio", "gabi", "sasha", "A", 1, ta=["surprise"],
      note="Gabi, cachée dans le dirigeable, abat Sasha (ch. 105) ; tir d'une enfant cachée, pas un vrai duel", flags="?")

# ============================================================== Guerre pour Paradis
fight(9.1, "paradis", "levi", "titans_purs", "A", 3,
      note="Le cri de Zeke change l'escouade de Livaï en Titans ; Livaï tue ses trente hommes (ch. 112-113)")
fight(9.1005, "paradis", "levi", "zeke", "A", 3, ta=["surprise"],
      note="Zeke, qui croyait Livaï dévoré par ses hommes changés en Titans, est rattrapé sous forme humaine avant de "
           "pouvoir se transformer ; Livaï le mutile et l'attache à une lance foudroyante (ch. 112-113)", flags="?")
fight(9.101, "paradis", "zeke", "levi", "D",
      note="Zeke déclenche la lance : tous deux gravement blessés, Hansi emporte Livaï (ch. 114-116)")
fight(9.1015, "paradis", ["reiner", "pieck", "porco", "armee_mahr"], "yeageristes", "A", 1, ta=["surprise"],
      note="Attaque surprise de Mahr sur Shiganshina par dirigeable (ch. 116-117)", flags="?")
fight(9.102, "paradis", "eren", ["reiner", "porco"], "D",
      note="Eren, avec le Marteau d'armes, tient tête au Cuirassé et au Mâchoire (ch. 117-118)", flags="i")
fight(9.1025, "paradis", "zeke", "armee_mahr", "A", 2,
      note="Zeke, régénéré dans un Titan, bombarde les forces de Mahr dans Shiganshina (ch. 116-119)", flags="?")
fight(9.104, "paradis", "gabi", "eren", "A", 1, ta=["surprise"],
      note="Tir de Gabi avec le fusil de Colt : Eren décapité alors qu'il court vers Zeke (ch. 119-120) ; "
           "un tir surprise, pas un duel", flags="?")

# ============================================================== Le Grondement
fight(9.2, "grondement", "eren", "armee_mahr", "A", 3,
      note="Le Grondement : les Titans colossaux des murs écrasent Mahr et ses alliés (ch. 123-131)")
fight(9.21, "grondement", ["mikasa", "jean", "connie", "armin", "annie", "reiner", "pieck", "hange", "magath"],
      "yeageristes", "A", 2,
      note="Forêt puis port d'Odiha : l'Alliance repousse les Yeageristes ; Magath et Shadis se sacrifient (ch. 127-130)")
fight(9.24, "grondement", "mikasa", "floch", "A", 3, note="Floch troue la coque de l'hydravion ; Mikasa l'abat (ch. 131)")
fight(9.25, "grondement", "titans_colossaux", "hange", "A", 2,
      note="Hansi tranche plusieurs Titans colossaux pour couvrir le décollage, puis brûle (ch. 132)")

# ============================================================== Bataille du Ciel et de la Terre
fight(9.3, "ciel_terre", "eren", ["reiner", "annie", "pieck", "falco", "mikasa", "levi", "armin", "jean", "connie", "gabi"],
      "A", 2, note="Fort Salta : les Titans du passé repoussent l'Alliance, Eren capture Armin (ch. 133-135)")
fight(9.301, "ciel_terre", "titans_du_passe", ["reiner", "annie", "pieck"], "A", 1,
      note="Le Cuirassé, le Féminin et le Charrette submergés par les Titans de l'Originel (ch. 134-135)", flags="i")
fight(9.302, "ciel_terre", ["mikasa", "levi", "jean", "connie"], "titans_du_passe", "A", 1,
      note="Mikasa et Livaï se frayent un chemin sur le dos de l'Originel (ch. 134-136)", flags="i")
fight(9.305, "ciel_terre", "levi", "zeke", "A", 3, tb=["retenue"],
      note="Zeke sort de lui-même de l'Originel ; Livaï le décapite, le Grondement s'arrête (ch. 136-137)", flags="?")
fight(9.306, "ciel_terre", ["armin", "titans_du_passe"], "eren", "A", 2, tb=["retenue"],
      note="Aidé par les anciens détenteurs libérés, Armin détruit le corps de l'Originel par l'explosion du Colossal (ch. 137)",
      flags="?")
fight(9.31, "ciel_terre", ["mikasa", "levi", "reiner", "annie", "armin", "jean", "connie", "pieck", "falco", "gabi"], "eren",
      "A", 1, ta=["aide"], tb=["retenue"],
      note="Reiner retient le Titan d'Eren, Livaï lui ouvre la bouche à la lance foudroyante, Mikasa le décapite ; "
           "Eren voulait être arrêté par ses amis (ch. 138-139)", flags="?")
