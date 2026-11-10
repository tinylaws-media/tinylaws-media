# Chainsaw Man, partie 2 (saga de l'Académie, ch. 98-232 ; le manga s'est achevé au ch. 232, 25 mars 2026).
# Manga de Fujimoto uniquement ; "fight" est injecté par data.py.
# Sources : liste des chapitres de Wikipedia (résumés des volumes 12-24), Chainsaw Man Wiki (fandom, chapitres 98,
# 150, 157-164, 169, 175, 180, 186), critiques chapitre par chapitre de Sportskeeda (ch. 209-210), Soapcentral
# (ch. 219, 223), Anime Explained (ch. 222, 227). "ch. ~N" = à un ou deux chapitres près.
# Repères de temps : Justice 1.50-1.53, aquarium et Chute 1.55-1.58, Église 1.60-1.645, évasion 1.65-1.68,
# monde du Vieillissement 1.70-1.73, Mort et Chute 1.75-1.77, guerre finale 1.80-1.845 (Pochita se mange lui-même
# au ch. 231), épilogue dans le monde réécrit 2.5.
# Yoru et Asa partagent un corps et le pouvoir du Démon de la Guerre : un seul personnage "yoru".
# Chainsaw Man noir (Pochita aux commandes, ch. 171-221) est le personnage "pochita" de la partie 1.

CHARS_PART = {
    "yoru": ("Yoru et Asa Mitaka (Démon de la Guerre)", "Cavaliers", 3.6, None, None),
    "delegue": ("Déléguée de classe (contrat avec la Justice)", "Humains", 1.2, 1.5001, None),
    "chauve_souris2": ("Démon de la Chauve-souris réincarné et Démon du Cafard", "Démons", 2.4, 1.5051, None),
    "yuko": ("Yuko (hybride de la Justice)", "Hybrides", 3.0, 1.5251, None),
    "fakesaw": ("Faux Chainsaw Man (Démon du Feu caché dans son cœur)", "Église de Chainsaw Man", 3.8, 1.7601, None),
    "eternite2": ("Démon de l'Éternité (aquarium)", "Démons", 3.3, 1.5501, None),
    "nayuta": ("Nayuta (Démon du Contrôle réincarné)", "Cavaliers", 4.3, None, None),
    "chute": ("Démon de la Chute", "Démons primordiaux", 6.0, 1.7701, None),
    "tueurs": ("Tueurs envoyés contre Denji (groupe)", "Humains", 1.0, None, None),
    "hybrides_p2": ("Hybrides d'armes de l'Église (Épée, Lance, Fouet, groupe)", "Hybrides", 3.2, None, None),
    "contractants_feu": ("Fidèles changés par le Démon du Feu (groupe)", "Église de Chainsaw Man", 1.5, None, None),
    "division_speciale": ("Divisions spéciales de la Sécurité publique (groupe)", "Sécurité publique", 3.0, None, None),
    "yoshida": ("Hirofumi Yoshida (Démon Pieuvre)", "Sécurité publique", 3.8, 1.8001, None),
    "clou": ("Démone du Clou (Nail Fiend)", "Sécurité publique", 2.6, None, None),
    "guillotine": ("Démon de la Guillotine (Guilly)", "Démons", 3.4, 1.8151, None),
    "fami": ("Fami (Démon de la Famine)", "Cavaliers", 4.3, 1.8151, None),
    "mort": ("Démon de la Mort (Li'l D)", "Cavaliers", 5.8, 1.8152, None),
    "division5": ("Division spéciale 5 et Démon de l'Oreille", "Sécurité publique", 3.0, 1.6721, None),
    "vieillissement": ("Démon du Vieillissement", "Démons primordiaux", 6.0, None, None),
    "humain_arbre": ("Humain-arbre évolué (monde du Vieillissement)", "Démons", 2.4, 1.7101, None),
    "fumiko": ("Fumiko Mifune", "Sécurité publique", 2.2, 1.7201, None),
    "lance_flammes": ("Démon du Lance-flammes", "Démons", 3.0, 1.8051, None),
    "sauterelle": ("Démon de la Sauterelle", "Démons", 5.0, 1.8351, None),
    "crabe": ("Démon crabe de l'épilogue", "Démons", 1.2, 2.5001, None),
}
# Barem meurt dévoré par Pochita (ch. 214) : sa mort est fixée ici car la partie 1 le déclare sans date.
CHARS_FIX = {"barem": ("Barem Bridge (hybride du Lance-flammes)", "Hybrides", 3.3, 1.8051, None)}

GENERIC_PART = {"tueurs", "hybrides_p2", "contractants_feu", "division_speciale"}

JUMPS_PART = [
    ("denji", 1.2, 0.3, 0.3, "Un an de Chainsaw Man en solitaire sous la garde de la Sécurité publique (ch. 98-103)"),
    ("yoru", 1.545, 0.3, 0.3, "Asa apprend à transformer ce qu'elle possède en armes : lance de l'aquarium (ch. 117-118)"),
    ("yoru", 1.6995, 1.0, 0.5, "Ses enfants Tank et Fusil (le Démon du Fusil réincarné) lui servent de bras (ch. 176-178)"),
    ("denji", 1.708, 0.4, 0.4, "Endurci dans le monde du Vieillissement, mange les entrailles de l'humain-arbre (ch. 181-185)"),
    ("yoru", 1.769, 1.5, 0.6, "Les armes nucléaires reviennent au monde : Yoru les reprend (ch. 209-210)"),
    ("yoru", 1.8, 0.5, 0.5, "Déclaration de guerre : la peur de la guerre la ramène à pleine puissance (ch. 215)"),
    ("denji", 1.825, 2.2, 0.8, "Denji et Pochita ne font plus qu'un : Denji Man, armure de têtes de démons (ch. 222-223)"),
    ("denji", 2.0, -2.5, 1.0, "Monde réécrit après que Pochita s'est mangé lui-même : plus de Chainsaw Man, contrat avec Power (ch. 231-232)"),
]

# ============================================================== Justice (ch. 98-112)
fight(1.5, "justice", "yoru", "delegue", "A", 3,
      note="Ressuscitée par Yoru, Asa forge l'épée « déléguée de classe » et le sabre « colonne vertébrale de Tanaka » (ch. 98)")
fight(1.505, "justice", "denji", "chauve_souris2", "A", 3,
      note="Chainsaw Man libère Asa et Yuko avalées par la Chauve-souris et tue le Démon du Cafard qui en sort (ch. 101-103)")
fight(1.51, "justice", "yuko", "yoru", "A", 2, note="Yoru ne parvient pas à arrêter Yuko devenue hybride de la Justice (ch. 108-109)")
fight(1.511, "justice", "yoru", "yuko", "A", 3, note="Asa reprend la main et découpe Yuko avec l'épée « uniforme scolaire » (ch. 109-110)")
fight(1.515, "justice", "denji", "yuko", "A", 2,
      note="Yuko ranimée par Fami : Chainsaw Man l'arrête (ch. 110-111)", flags="?")
fight(1.52, "justice", "yoru", "denji", "D",
      note="Yoru tente de tuer Chainsaw Man ; la Pieuvre de Yoshida emporte Denji (ch. 111)", flags="i")
fight(1.525, "justice", "fakesaw", "yuko", "A", 3, ta=["surprise"], note="Un faux Chainsaw Man tue Yuko la nuit (ch. 112)")

# ============================================================== Aquarium et Démon de la Chute (ch. 113-133)
fight(1.55, "chute", ["yoru", "denji"], "eternite2", "A", 3,
      note="Piégés par Fami dans l'aquarium ; Asa fait de l'aquarium une lance et tue le Démon de l'Éternité (ch. 114-118)")
fight(1.555, "chute", "nayuta", "yoru", "A", 2, ta=["surprise"],
      note="Yoru crache sur Denji : Nayuta lui donne l'esprit d'un chien (ch. 119-120)")
fight(1.57, "chute", "chute", ["yoru", "denji"], "A", 2,
      note="La Chute les fait tomber en Enfer sur une assiette géante en se servant de leurs traumatismes ; Fami la renvoie en Enfer (ch. 123-131)",
      flags="i")

# ============================================================== Église de Chainsaw Man (ch. 134-155)
fight(1.6, "eglise", "denji", "tueurs", "A", 3,
      note="Denji repousse une série d'agresseurs au karaoké pendant que Fumiko chante (ch. 136-137)")
fight(1.61, "eglise", "quanxi", "hybrides_p2", "A", 3,
      note="Quanxi démembre trois hybrides d'armes et en décapite trois autres avant qu'ils ne réagissent (ch. 143)")
fight(1.625, "eglise", "quanxi", "contractants_feu", "A", 3,
      note="Barem lance la foule changée par le Démon du Feu sur Nayuta ; Quanxi sauve Nayuta, Denji et Fumiko (ch. 146-147)")
fight(1.63, "eglise", "yoshida", "yoru", "A", 2,
      note="Yoshida tranche le bras droit d'Asa en l'arrêtant ; elle s'échappe (ch. ~149-150)", flags="i")
fight(1.635, "eglise", "hybrides_p2", "fumiko", "A", 3,
      note="L'hybride du Fouet met hors de combat Fumiko et son équipe (ch. ~150)")
fight(1.64, "eglise", "denji", "hybrides_p2", "A", 2, note="Chainsaw Man vainc les hybrides de l'Épée, de la Lance et du Fouet (ch. 152-153)")
fight(1.641, "eglise", "division_speciale", "denji", "A", 2, ta=["prepa"],
      note="Les hybrides restants piègent Chainsaw Man ; Denji est capturé et démembré (ch. 153-154)")

# ============================================================== Évasion, Chainsaw Man noir (ch. 156-175)
fight(1.65, "evasion", "guillotine", "agents_sp", "A", 3,
      note="Fami invoque la Guillotine au centre de détention : les gardes sont désarmés et se rendent (ch. 157-158)")
fight(1.655, "evasion", ["katana_man", "clou"], ["yoru", "fami"], "D",
      note="Katana Man et la Démone du Clou affrontent Asa et Fami, puis s'allient à elles (ch. 159-160)", flags="i")
fight(1.66, "evasion", "quanxi", ["katana_man", "clou"], "A", 3,
      note="Quanxi décapite Katana Man et éventre la Démone du Clou (ch. 162)")
fight(1.6601, "evasion", "quanxi", "yoru", "A", 1,
      note="Quanxi repousse Yoru armée d'un scalpel, puis se rend en voyant le visage de Denji (ch. 162)", flags="i")
fight(1.67, "evasion", "denji", "barem", "A", 2,
      note="Denji décapite Barem ; Pochita prend alors le contrôle, Chainsaw Man noir (ch. ~170-171)", flags="?")
fight(1.672, "evasion", "pochita", "division5", "A", 3,
      note="La Division spéciale 5 ne fait pas le poids : Pochita mange le Démon de l'Oreille (ch. 171-173)")
fight(1.675, "evasion", "pochita", ["vieillissement", "katana_man", "yoru"], "A", 2,
      note="Le Vieillissement perd ses mains, Katana Man ses bras et sa tête, Yoru son bras gauche (ch. 174-175)")

# ============================================================== Monde du Démon du Vieillissement (ch. 176-190)
fight(1.7, "vieillesse", "yoru", "pochita", "A", 2,
      note="Avec Tank et Fusil, des milliers d'index font voler Pochita en morceaux (ch. 176-178)", flags="i")
fight(1.705, "vieillesse", "vieillissement", "yoru", "A", 3,
      note="Le Vieillissement atteint Yoru d'un « bang » et l'envoie dans son monde, où ses pouvoirs ne marchent pas (ch. 179-180)")
fight(1.71, "vieillesse", "denji", "humain_arbre", "A", 2,
      note="Denji vainc un humain-arbre évolué et mange ses entrailles pour ranimer Pochita (ch. 182-183)")
fight(1.72, "vieillesse", "pochita", ["fumiko", "division_speciale"], "A", 3,
      note="Pochita blesse mortellement les agents de la Sécurité publique, Fumiko comprise (ch. 184-185)")
fight(1.725, "vieillesse", "pochita", "vieillissement", "D",
      note="Le Vieillissement sacrifie ongles, foie et yeux de ses contractants pour couper et décapiter Pochita, qui lui lance son cœur ; "
           "impasse (ch. 186-188)", flags="i")
fight(1.73, "vieillesse", ["yoshida", "yoru", "denji"], "vieillissement", "A", 1, ta=["prepa"],
      note="Yoshida piège le Vieillissement dans un contrat et renvoie chacun dans son monde (ch. 189-190)", flags="e")

# ============================================================== Démon de la Mort, retour de la Chute (ch. 191-210)
fight(1.75, "mort", "chute", "fakesaw", "A", 3,
      note="Le faux Chainsaw Man découpe la fausse « Mort », puis la Chute l'écrase (ch. 196-198)")
fight(1.755, "mort", "mort", ["fami", "fakesaw"], "A", 3,
      note="La vraie Mort, cachée sous les traits de Fami, asservit Famine et le faux Chainsaw Man (ch. 198-199)", flags="?")
fight(1.76, "mort", "denji", "fakesaw", "A", 2,
      note="Denji tranche le cœur du faux Chainsaw Man et révèle le Démon du Feu (ch. 202-205)")
fight(1.765, "mort", "chute", "denji", "A", 3, note="La Chute écrase Denji en renversant la gravité (ch. 200-207)")
fight(1.766, "mort", "chute", "yoru", "D",
      note="Yoru enfouit la Chute sous les lames et les lances ; elle s'en débarrasse sans mal (ch. 207-208)", flags="i")
fight(1.77, "mort", "yoru", "chute", "A", 3,
      note="Avec les armes nucléaires revenues, Yoru vainc la Chute et en fait un vêtement (ch. 209-210)")

# ============================================================== Guerre finale (ch. 211-231)
fight(1.8, "guerre", "barem", "yoshida", "A", 3, ta=["surprise"], note="Barem fait sauter l'école : Yoshida est tué (ch. 211-213)")
fight(1.805, "guerre", "pochita", ["barem", "lance_flammes"], "A", 3,
      note="Pochita dévore Barem et le Démon du Lance-flammes (ch. 213-214)")
fight(1.81, "guerre", "pochita", "yoru", "D",
      note="Yoru et Pochita s'affrontent sans vainqueur ; Asa fait sauter la tête de Yoru pour ouvrir une brèche à Denji (ch. 215-217)",
      flags="i")
fight(1.815, "guerre", "pochita", ["mort", "fami", "guillotine"], "A", 3,
      note="Pochita décapite Li'l D, Fami et Guilly, puis dévore la Mort tout entière (ch. 217-219)")
fight(1.82, "guerre", "yoru", "pochita", "A", 2,
      note="Coup de poing nucléaire de Yoru : explosion gigantesque, Chainsaw Man ne bouge plus (ch. 220-222)", flags="i")
fight(1.83, "guerre", "denji", "yoru", "D",
      note="Denji Man contre Yoru : drapeau de la Lune, moto tronçonneuse ; Denji efface ses jambes et ses dents, elle le fait exploser (ch. 222-225)",
      flags="i")
fight(1.835, "guerre", "sauterelle", ["yoru", "denji"], "A", 2,
      note="Le Démon de la Sauterelle, caché jusque-là, met en pièces Yoru et Denji (ch. 226)", flags="i")
fight(1.8351, "guerre", "denji", "sauterelle", "A", 2,
      note="Asa lui relance son bras : Denji tire la Sauterelle à lui par la chaîne et la mange (ch. 227)")
fight(1.84, "guerre", "yoru", "denji", "A", 2,
      note="Yoru tire à travers les immeubles et détruit bras et jambes de Denji ; elle renonce ensuite à l'écraser (ch. 227-229)", flags="i")

# ============================================================== Épilogue (ch. 232)
fight(2.5, "epilogue", ["denji", "power"], "crabe", "A", 3,
      note="Dans le monde réécrit, Denji et Power tuent un démon crabe à l'école ; Denji sauve Asa (ch. 232)")
