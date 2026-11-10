# Chainsaw Man, partie 1 (Public Safety, ch. 1-97). Manga de Fujimoto uniquement ; "fight" est injecté par data.py.
# Sources : Chainsaw Man Wiki (fandom, pages de chapitres 69, 70, 84, 87, 88, 94…), liste des chapitres de Wikipedia
# (résumés des volumes), relectures du manga. "ch. ~N" = à un ou deux chapitres près.
# Repères de temps (t = années depuis l'entrée de Denji à la Sécurité publique) : débuts 0.00-0.08, hôtel de l'Éternité
# 0.10-0.13, Katana Man et entraînement de Kishibe 0.20-0.30, Reze 0.40-0.46, assassins 0.60-0.67 (hiver),
# Démon du Fusil 0.75-0.78, Démon du Contrôle 0.80-0.85.
# Pochita aux commandes du corps de Denji (vrai Chainsaw Man, ch. 83-89) est le personnage "pochita".
# L'immortalité de Makima (ses blessures passent sur des citoyens japonais, contrat avec le Premier ministre, ch. 76-89)
# est un pouvoir prêté : étiquette "aide" dans les combats qu'elle décide.

CHARS_PART = {
    # ---------------------------------------------------------------- Sécurité publique
    "denji": ("Denji (Chainsaw Man)", "Sécurité publique", 2.4, None, None),
    "power": ("Power (Démone du Sang)", "Sécurité publique", 2.2, 0.8455, None),
    "aki": ("Aki Hayakawa", "Sécurité publique", 2.4, 0.755, None),
    "himeno": ("Himeno (Démon Fantôme)", "Sécurité publique", 2.6, 0.2015, None),
    "kobeni": ("Kobeni Higashiyama", "Sécurité publique", 2.0, None, None),
    "beam": ("Beam (Démon Requin)", "Sécurité publique", 2.3, None, None),
    "angel": ("Démon de l'Ange", "Sécurité publique", 2.8, None, None),
    "kishibe": ("Kishibe", "Sécurité publique", 4.3, None, None),
    "makima": ("Makima (Démon du Contrôle)", "Cavaliers", 6.5, 0.846, None),
    "agents_sp": ("Agents et chasseurs de la Sécurité publique (groupe)", "Sécurité publique", 1.2, None, None),
    "cosmo": ("Cosmo (Démone du Cosmos)", "Assassins", 2.5, None, None),
    # ---------------------------------------------------------------- démons et ennemis
    "zombie": ("Démon Zombie", "Démons", 2.0, 0.0005, None),
    "chauve_souris": ("Démon de la Chauve-souris", "Démons", 2.6, 0.031, None),
    "sangsue": ("Démon de la Sangsue", "Démons", 2.2, 0.041, None),
    "eternite": ("Démon de l'Éternité", "Démons", 3.5, 0.131, None),
    "katana_man": ("Katana Man (hybride du Sabre)", "Hybrides", 3.0, None, None),
    "akane": ("Akane Sawatari (Démon Serpent)", "Yakuzas du Fusil", 3.0, 0.29, None),
    "yakuzas": ("Yakuzas et tireurs du Démon du Fusil (groupe)", "Yakuzas du Fusil", 0.6, None, None),
    "reze": ("Reze (hybride de la Bombe)", "Hybrides", 4.0, None, None),
    "typhon": ("Démon du Typhon", "Démons", 3.2, 0.43, None),
    "quanxi": ("Quanxi (hybride de l'Arbalète)", "Hybrides", 4.6, None, None),
    "santa": ("Santa Claus (Démon de la Poupée)", "Assassins", 3.8, 0.6605, None),
    "poupees": ("Poupées de Santa Claus (groupe)", "Assassins", 1.5, None, None),
    "tenebres": ("Démon des Ténèbres", "Démons primordiaux", 6.3, None, None),
    "demon_fusil": ("Démon du Fusil", "Démons", 5.8, 0.7601, None),
    "fiend_fusil": ("Démon du Fusil dans le corps d'Aki (Gun Fiend)", "Démons", 4.6, 0.7801, None),
    "demons_enfer": ("Démons de l'Enfer et Démon de l'Enfer ranimé (groupe)", "Démons", 3.5, None, None),
    "hybrides_makima": ("Hybrides d'armes de Makima (Miri Sugo, Fouet, Lance, groupe)", "Hybrides", 3.2, None, None),
    "barem": ("Barem Bridge (hybride du Lance-flammes)", "Hybrides", 3.3, None, None),
    "pochita": ("Pochita (vrai Chainsaw Man)", "Démons", 6.4, 1.845, None),
}

GENERIC_PART = {"agents_sp", "yakuzas", "poupees", "demons_enfer", "hybrides_makima"}

REVIVE_PART = {"power": 2.4}   # Power revient dans le monde réécrit de l'épilogue (ch. 232)

# gains et pertes permanents : (perso, temps, changement moyen en échelons, écart-type, libellé)
JUMPS_PART = [
    ("denji", 0.035, 0.2, 0.3, "Premiers combats, apprend à se battre en buvant du sang (ch. 5-12)"),
    ("denji", 0.245, 0.5, 0.3, "Entraînement de Kishibe : apprendre à penser en combat (ch. 30-34)"),
    ("power", 0.245, 0.3, 0.3, "Entraînement de Kishibe (ch. 30-34)"),
    ("aki", 0.205, 0.4, 0.4, "Contrat avec le Démon du Futur, œil droit (ch. 29-30), en plus du Renard et de la Malédiction"),
    ("denji", 0.62, 0.2, 0.3, "Chaînes et combat en feu développés contre Santa Claus (ch. 67-69)"),
    ("santa", 0.636, 1.4, 0.6, "Contrat avec le Démon des Ténèbres en Enfer : pouvoir des Ténèbres (ch. 64-66)"),
    ("power", 0.835, -0.3, 0.4, "Ramenée comme simple Démone du Sang affaiblie, cachée dans Denji (ch. ~92-93)"),
]

# ============================================================== Débuts (ch. 1-12)
fight(0.0, "debut", "denji", "zombie", "A", 3,
      note="Fusion avec Pochita : Denji devient Chainsaw Man et massacre le Démon Zombie et ses zombies (ch. 1)")
fight(0.01, "debut", "aki", "denji", "A", 1,
      note="Aki rosse Denji dans une ruelle pour qu'il quitte la Sécurité publique ; Denji lui rend un coup bas (ch. 3)", flags="?")
fight(0.03, "debut", "chauve_souris", "denji", "A", 2, ta=["prepa"],
      note="Power livre Denji au Démon de la Chauve-souris, qui l'écrase avant qu'il ne boive son sang (ch. 6-7)", flags="i")
fight(0.031, "debut", "denji", "chauve_souris", "A", 3,
      note="Ranimé par le sang de Power, Denji tranche le Démon de la Chauve-souris en vol (ch. 7)")
fight(0.04, "debut", "denji", "sangsue", "A", 2,
      note="Denji, déjà blessé, achève la Sangsue venue venger la Chauve-souris ; Aki et Himeno arrivent après (ch. 8-9)", flags="?")

# ============================================================== Hôtel du Démon de l'Éternité (ch. 13-21)
fight(0.12, "eternite", "kobeni", "denji", "A", 1, ta=["surprise"],
      note="Kobeni, paniquée, poignarde Denji pour le livrer à l'Éternité ; Aki l'arrête (ch. 17)", flags="?")
fight(0.13, "eternite", "denji", "eternite", "A", 3,
      note="Trois jours à tronçonner le Démon de l'Éternité qui finit par implorer la mort (ch. 18-20)")

# ============================================================== Katana Man, yakuzas, entraînement (ch. 22-38)
fight(0.2, "katana", "katana_man", "denji", "A", 2, ta=["surprise"],
      note="Katana Man tranche Denji, privé de sang, lors de l'embuscade (ch. 22)")
fight(0.2005, "katana", "katana_man", "aki", "A", 3, ta=["surprise"],
      note="Aki, distrait par l'attaque, est tranché par Katana Man (ch. 22-23)")
fight(0.201, "katana", ["akane", "katana_man"], "himeno", "A", 3,
      note="Himeno donne tout son corps au Démon Fantôme, qui retient Katana Man ; le Serpent d'Akane dévore le Fantôme (ch. 23-25)")
fight(0.2012, "katana", "kobeni", "yakuzas", "A", 3,
      note="Kobeni abat les tireurs yakuzas d'un enchaînement éclair au couteau (ch. 23-24)")
fight(0.215, "katana", "makima", "yakuzas", "A", 3, ta=["aide"],
      note="Abattue dans le train, Makima se relève et tue à distance les tueurs et leurs familles grâce à des prisonniers sacrifiés (ch. 26-27)")
fight(0.24, "katana", "kishibe", "denji", "A", 3,
      note="Kishibe tue et ranime Denji encore et encore à l'entraînement, sans jamais être touché (ch. 30-34)")
fight(0.2401, "katana", "kishibe", "power", "A", 3,
      note="Kishibe tue Power à répétition à l'entraînement (ch. 30-34)")
fight(0.28, "katana", "aki", "akane", "A", 2,
      note="Aki, avec le Démon du Futur, résiste au Fantôme et au Serpent d'Akane, qui se fait dévorer par son Serpent (ch. 36-38)", flags="?")
fight(0.29, "katana", ["denji", "aki"], "katana_man", "A", 2,
      note="Revanche sur le toit du train : Denji vainc Katana Man, Aki l'aide ; coup de pied vengeur pour Himeno (ch. 37-39)")

# ============================================================== Reze (ch. 39-52)
fight(0.4, "reze", "reze", "denji", "A", 3, ta=["surprise"],
      note="Reze se dévoile : lui mord la langue, l'arrose d'explosions et le tranche à la piscine (ch. 41-42)")
fight(0.41, "reze", "reze", "agents_sp", "A", 3,
      note="Reze extermine l'escorte de la Sécurité publique et les yakuzas (ch. 42-44)")
fight(0.43, "reze", ["denji", "beam"], ["reze", "typhon"], "A", 2,
      note="Denji chevauche Beam contre Reze et le Démon du Typhon ; Reze est entravée et noyée dans la mer (ch. 45-50)")
fight(0.45, "reze", ["makima", "angel"], "reze", "A", 3, ta=["surprise"],
      note="Makima et l'Ange coincent Reze dans la ruelle avant son rendez-vous avec Denji (ch. 52)")

# ============================================================== Assassins internationaux (ch. 53-70)
fight(0.62, "assassins", "quanxi", ["agents_sp", "poupees"], "A", 3,
      note="Quanxi massacre 49 personnes, chasseurs et poupées, et cinq chasseurs avant qu'ils ne réagissent (ch. 60)")
fight(0.625, "assassins", "quanxi", ["denji", "agents_sp"], "A", 3,
      note="Quanxi met Denji, Tamaoki et Kusakabe hors d'état en quelques coups de pied (ch. 61)")
fight(0.635, "assassins", "tenebres", ["quanxi", "aki", "power", "denji", "kobeni", "angel"], "A", 3,
      note="En Enfer, le Démon des Ténèbres arrache les bras de tous : Quanxi perd un bras, ses démones meurent (ch. 64-65)")
fight(0.65, "assassins", "denji", "santa", "A", 2,
      note="Denji en flammes déchire Santa Claus, armée du pouvoir des Ténèbres et de ses poupées (ch. 67-69)")
fight(0.66, "assassins", "quanxi", "denji", "A", 2, ta=["surprise"],
      note="Quanxi décapite Denji sitôt Santa vaincue (ch. 70)")
fight(0.6601, "assassins", "cosmo", "santa", "A", 3, ta=["contre"], tb=["epuise"],
      note="Le pouvoir de Cosmo (« Halloween ») noie l'esprit de Santa Claus déjà réduite par Denji (ch. 70)")
fight(0.661, "assassins", "makima", "quanxi", "A", 3,
      note="Makima décapite les démones de Quanxi ; Quanxi se rend sans combattre (ch. 70)", flags="?")

# ============================================================== Démon du Fusil (ch. 71-79)
fight(0.76, "fusil", "makima", "demon_fusil", "A", 3, ta=["aide"],
      note="Makima abat le Démon du Fusil (avec presque toute sa chair) ; les balles reçues passent sur des citoyens japonais (ch. 75-77)")
fight(0.78, "fusil", "denji", "fiend_fusil", "A", 2,
      note="Denji doit tuer Aki devenu le Démon du Fusil ; le fiend croit jouer aux boules de neige (ch. 77-79)")

# ============================================================== Démon du Contrôle (ch. 80-97)
fight(0.8, "controle", "makima", "power", "A", 3, ta=["surprise"],
      note="Makima fait exploser Power d'un « bang » sous les yeux de Denji (ch. 80)")
fight(0.81, "controle", "makima", ["kishibe", "agents_sp"], "A", 3, ta=["aide"],
      note="L'assaut de Kishibe et de ses tireurs échoue : Makima, criblée de balles, se relève (ch. ~83-85)", flags="?")
fight(0.815, "controle", "pochita", "demons_enfer", "A", 3,
      note="Envoyé en Enfer par le Démon de l'Enfer ranimé, le vrai Chainsaw Man éventre tous les démons qu'il croise (ch. 84)")
fight(0.82, "controle", "pochita", ["quanxi", "katana_man", "hybrides_makima"], "A", 3,
      note="Le vrai Chainsaw Man décapite Quanxi, Miri Sugo et Katana Man sans recevoir de blessure (ch. 87)")
fight(0.821, "controle", "pochita", ["makima", "reze", "barem", "hybrides_makima"], "A", 2, tb=["aide"],
      note="Projeté dans l'espace par les « bang » de Makima, il revient et déchiquette Makima, Barem, Reze et les hybrides ; "
           "Makima, immortelle par contrat, se relève (ch. 88)", flags="i")
fight(0.822, "controle", "makima", "pochita", "A", 2, tb=["protege"],
      note="Tuée 26 fois, Makima gagne : sa lance transperce Pochita qui protégeait Kobeni (ch. 89)")
fight(0.84, "controle", "denji", ["quanxi", "katana_man", "reze", "barem", "hybrides_makima"], "A", 1, ta=["prepa"],
      note="Au cimetière, Denji tranche Katana Man, Miri, Reze, les hybrides et Barem, décapite Quanxi, puis s'effondre (ch. ~93-94)")
fight(0.843, "controle", "makima", "power", "A", 3,
      note="Power, revenue en Démone du Sang, est de nouveau tuée par Makima (ch. ~94-95)", flags="?")
fight(0.845, "controle", "denji", "makima", "A", 2, ta=["prepa"],
      note="Makima ne perçoit que Chainsaw Man : Denji l'attaque en tant que Denji, avec la tronçonneuse de sang de Power, "
           "et la tranche ; il la mange pour qu'elle ne revienne pas (ch. 95-96)")
