# My Hero Academia, partie 2 : combats complémentaires du manga (ch. 1-430). "fight" est injecté par data.py.
# Sources : mémoire du manga, My Hero Academia Wiki (pages d'arc), Sportskeeda (sort des vilains, ch. 385, 430) ;
# "ch. ~N" = à quelques chapitres près.

CHARS_PART = {}
GENERIC_PART = set()
# progression générale de la classe 1-A (entraînements datés, en plus des sauts individuels de part_1)
_classe = ["deku", "bakugo", "todoroki", "iida", "uraraka", "kirishima", "tokoyami", "yaoyorozu", "tsuyu", "kaminari",
           "jiro", "mina", "sero", "shoji", "ojiro", "sato", "koda", "aoyama", "hagakure", "mineta"]
JUMPS_PART = [(c, 1.39, 0.3, 0.3, "Camp de la licence : super-coups spéciaux, licence provisoire (ch. 98-111)") for c in _classe] + \
             [(c, 2.29, 0.4, 0.3, "Six mois de guerre puis entraînement de la guerre finale, Yuei forteresse (ch. ~322-342)")
              for c in _classe + ["shinso"]]

# ============================================================== Rentrée
fight(0.9505, "usj", "aizawa", "bakugo", "A", 2,
      note="Test d'aptitude : Bakugo fonce sur Deku, Aizawa l'entrave et efface son Alter d'un regard (ch. 6-7)")

# ============================================================== USJ
fight(0.97055, "usj", ["iida", "uraraka", "shoji", "sato"], "kurogiri", "A", 1,
      note="Uraraka fait flotter l'armure de Kurogiri, Iida s'échappe pour prévenir les professeurs (ch. 17-19)", flags="ie")
fight(0.97085, "usj", ["todoroki", "bakugo", "kirishima"], "nomu_usj", "D",
      note="Todoroki gèle la moitié du Nomu pour libérer Deku, le Nomu se régénère aussitôt (ch. 18-19)", flags="i")

# ============================================================== Festival sportif : bataille de cavaliers
fight(1.00004, "festival", ["bakugo", "sero", "mina", "kirishima"], ["monoma", "classe_1b"], "A", 2,
      note="Bataille de cavaliers : Bakugo reprend tous les bandeaux de l'équipe de Monoma (ch. 30-31)")
fight(1.00006, "festival", ["todoroki", "iida", "yaoyorozu", "kaminari"], ["deku", "uraraka", "tokoyami", "hatsume"], "A", 1,
      note="Bataille de cavaliers : Iida reprend à Deku le bandeau à 10 millions ; l'équipe de Deku finit 4e (ch. 28-31)", flags="e")

# ============================================================== Hosu
fight(1.0499, "stain", "gran_torino", "nomus_hosu", "A", 2,
      note="Un Nomu percute le train, Gran Torino le repousse d'un coup de pied (ch. 50)")

# ============================================================== Licence provisoire
fight(1.4002, "licence", ["deku", "uraraka", "sero"], "candidats", "A", 2,
      note="Première épreuve : Deku et son groupe repoussent les candidats de Ketsubutsu (ch. 104-107)", flags="e?")
fight(1.4004, "licence", "todoroki", "inasa", "D",
      note="Todoroki et Inasa se disputent et se gênent : tous deux échouent l'examen (ch. 109-111)", flags="i")

# ============================================================== Guerre de libération du Paranormal
fight(1.9004, "guerre", "edgeshot", "re_destro", "A", 1,
      note="Raid de la villa de Gunga : Edgeshot neutralise Re-Destro (ch. ~262-266)", flags="?")
fight(1.90055, "guerre", ["uraraka", "tsuyu"], "toga", "D",
      note="Uraraka et Asui retiennent Toga après la mort de Twice (ch. ~285-288)", flags="i")
fight(1.90058, "guerre", "mirio", "compress", "A", 2,
      note="Mirio, sans Alter, met Mr. Compress hors de combat à Jaku (ch. ~291-293)", flags="?")

# ============================================================== Deku héros sombre
fight(2.02, "sombre", "deku", "muscular", "A", 3,
      note="Deku, Danger Sense et Blackwhip, écrase Muscular évadé de Tartarus (ch. ~307-308)")
