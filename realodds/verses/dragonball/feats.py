"""Exploits mesurables (canon) de Dragon Ball pour la comparaison inter-œuvres. Valeurs en log10 de l'unité SI.
Canon : manga Dragon Ball (Toriyama) et manga Dragon Ball Super (Toyotarō). Les niveaux de puissance officiels ne sont pas
des exploits physiques et ne sont pas utilisés ici.
Révision (vérification) : chapitres contrôlés sur les résumés de Kanzenshuu ; dimensions non chiffrées dans le manga,
donc estimées à partir des cases, avec un sd en conséquence.
Les menaces non réalisées sont exclues : Cell qui menace de faire sauter le système solaire, Vegeta qui menace la Terre
avec le Galick Gun, le choc Goku-Beerus « qui ébranle l'univers ». Les pouvoirs spéciaux sont aussi exclus : Hakai,
aspiration d'énergie vitale de Moro, saut temporel de Hit.
Aucun exploit de Jiren, Moro, Gas ou Super Buu n'a été retenu : le canon ne donne aucun exploit réalisé et chiffrable pour eux."""
U1 = "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_1"
FEATS = [
    # ---------------------------------------------------------------- bas de l'échelle
    # corrigé : la voiture est soulevée puis lancée (pas « jetée » au sens vague) ; masse revue, URL ajoutée
    ("goku", "pilaf", "force", 3.0, 0.3, "Goku enfant soulève la voiture de Bulma et la lance (elle retombe sur le flanc)", "ch. 1",
     "petite voiture citadine 700-1 300 kg ⇒ ~1 000 kg", U1),
    ("goku", "pilaf", "resistance", 2.7, 0.4, "Goku enfant encaisse plusieurs balles de pistolet de Bulma : il a mal, mais il n'est pas blessé", "ch. 1",
     "balle de pistolet ½mv² ≈ 300-700 J (9 mm : 8 g à 360 m/s ≈ 520 J) ; énergie d'un seul tir", U1),
    ("goku", "pilaf", "vitesse", 1.07, 0.3, "100 m en 8,5 s (11 s avec des chaussures abîmées), test de Tortue Géniale", "ch. 28",
     "100 m / 8,5 s = 11,8 m/s ; avant l'entraînement de Roshi, donc état de l'arc Pilaf",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_28"),
    ("roshi", "tournoi21", "vitesse", 1.25, 0.3, "Tortue Géniale court le 100 m en 5,6 s pour montrer l'exemple", "ch. 28",
     "100 m / 5,6 s = 17,9 m/s (démonstration, peut-être sans tout donner)",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_28"),
    # ---------------------------------------------------------------- milieu
    # corrigé : ch. ~14 → ch. 14 ; le château est sur la montagne ; volume borné ; URL ajoutée
    ("roshi", "tournoi21", "energie", 14.5, 1.0,
     "Kamehameha (Roshi gonflé de muscles) : le feu du mont Fry-pan s'éteint, mais la montagne et le château disparaissent", "ch. 14",
     "montagne : cône de rayon 200-500 m et de haut 200-500 m ⇒ 1e7-1e8 m³ ; dispersée à 5e6-2e7 J/m³ ⇒ 4e13-3e15 J ≈ 3e14 J "
     "(exploit d'avant le 21e Championnat ; Roshi est stable : SLOW)",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_14"),
    ("tien", "tournoi22", "energie", 11.0, 1.2,
     "Kikōhō contre Goku : l'arène est « complètement désintégrée », il reste un grand trou à sa place", "ch. 133",
     "arène ~20-30 m de côté, trou ~3-5 m de profondeur ⇒ ~1e3-4e3 m³ de dallage et de sol pulvérisés à 2e7-1e8 J/m³ ⇒ 2e10-4e11 J "
     "(dimensions lues sur les cases)",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_133"),
    ("piccolo", "tournoi23", "energie", 14.7, 1.0,
     "Chō-bakuretsu-maha : l'île du tournoi devient un désert, toutes les dalles de l'arène ont disparu", "ch. 190",
     "zone détruite d'un rayon de 1-5 km ; souffle de 5 psi : Y ≈ (r/4,6 km)³ Mt ⇒ 0,01-1,3 Mt ≈ 4e13-5e15 J. "
     "Un calcul de fan (186 Mt) prend l'horizon pour rayon ; je ne le retiens pas",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_190"),
    # corrigé : ch. ~211 → ch. 213 ; le manga montre la main levée ; sd élargi (exploit décontracté, donc borne basse)
    ("nappa", "saiyan", "energie", 15.0, 0.9, "Nappa lève la main et toute la ville (East City) explose autour des capsules", "ch. 213",
     "ville rasée sur un rayon de 2-5 km ; souffle de 5 psi : (r/4,6 km)³ Mt ⇒ 0,1-1,3 Mt ≈ 4e14-5e15 J. "
     "Geste désinvolte, donc peut-être une sous-estimation",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_213"),
    ("goku", "namek", "force", 3.8, 0.4,
     "Goku s'entraîne à 100 G dans son vaisseau : il porte 100 fois ses ~60 kg (6 t selon le Dr Brief)", "ch. 251 (6 t), ch. 270 (100 G)",
     "60 kg × 100 = 6 000 kg porté en permanence (pompes, déplacements) ; c'est avant les combats de Namek, au niveau du combat contre Ginyu ; entraînement, pas un effort maximal : borne basse",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_270"),
    ("cell", "cyborgs", "resistance", 7.5, 0.8,
     "Cell parfait ne subit « aucune égratignure » des obus de chars et des missiles de l'armée", "ch. 392",
     "obus de char ~1e7 J (cinétique ou explosif), missile à ~10 kg d'explosif ≈ 4e7 J ⇒ ~3e7 J par coup. "
     "Indemne, donc borne basse très large de sa résistance",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_392"),
    # ---------------------------------------------------------------- haut (aberrants ou planétaires)
    # corrigé : ch. ~46 → ch. 52 ; sd 1,2 → 1,5 (aberrant ~14 décades au-dessus du mont Fry-pan pour le même Roshi)
    ("roshi", "tournoi21", "energie", 28.5, 1.5,
     "Kamehameha MAX de Jackie Chun qui détruit la Lune pour ramener Goku de sa forme Oozaru (toute son énergie y passe)", "ch. 52",
     "énergie de liaison de la Lune 3GM²/5R = 1,2e29 J ; la Lune disparaît, mais on ne voit pas de dispersion complète ⇒ 1e28-1e29 J. "
     "Aberrant (incohérent avec le reste de l'œuvre) : gardé, mais avec un sd large",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_52"),
    # corrigé : ch. ~204 → ch. 208 ; arc saiyan → raditz (début de l'entraînement de Gohan, avant l'année de progrès de Piccolo) ; sd 1,5
    ("piccolo", "raditz", "energie", 28.5, 1.5,
     "Piccolo détruit la Lune pendant la première transformation de Gohan en Oozaru", "ch. 208",
     "même calcul que la Lune de Roshi. Aberrant ; le Kanzenshuu dit seulement qu'il « décide de supprimer la Lune », "
     "et la Lune n'est plus revue avant d'être recréée",
     "https://dragonballupdates.fandom.com/wiki/Moon"),
    # corrigé : ch. ~319-328 → ch. 320 (tir), explosion ch. ~328 ; valeur 31,5 → 31,0 ; sd 1,0 → 1,5
    ("freeza", "freezer", "energie", 31.0, 1.5,
     "Freezer tire dans le noyau de Namek, qui explose environ cinq minutes plus tard ; il n'a pas tiré à pleine puissance", "ch. 320 (tir), ch. ~328 (explosion)",
     "Namek supposée de la taille de la Terre (le manga ne la chiffre pas) ; énergie de liaison 2,2e32 J comme borne haute ; "
     "explosion différée : le noyau fournit sans doute une partie de l'énergie ⇒ ~1e31 J, incertitude large",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_320"),
    # corrigé : ch. ~502 → ch. 508 ; arc buu → superbuu (Buu originel n'apparaît qu'à la fin de l'arc ; estimation identique)
    ("kid_buu", "superbuu", "energie", 32.3, 0.5, "Buu originel fait exploser la Terre avec une grosse boule d'énergie", "ch. 508",
     "énergie de liaison de la Terre 3GM²/5R = 2,24e32 J (la planète est détruite d'un coup)",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Chapter_508"),
    ("beerus", "dieux", "energie", 31.0, 1.5, "Beerus réduit en miettes une planète habitée qui avait tenté de l'empoisonner", "DBS ch. 1",
     "taille de la planète inconnue (1e29 J pour un corps lunaire, 2e32 J pour une Terre) ⇒ ~1e31 J ; geste désinvolte, donc borne basse",
     "https://www.kanzenshuu.com/wiki/Dragon_Ball_Super_Chapter_1"),
]
ANCHORS = [
    # rencontres canon avec des êtres RÉELS. Le manga ne contient presque pas d'animaux réels qui combattent :
    # tigre à dents de sabre, ptéranodon, dinosaures, poisson et pieuvre géants (fantastiques ou disparus) ; le requin du lac
    # au ch. 31 poursuit seulement Goku et Krillin, sans combat. Ils sont donc exclus.
    # Les soldats du Ruban rouge, les criminels et l'armée sont des combattants du modèle (voir ANCHOR_ENTITIES).
    ("mr_satan", "buu", "soldat_arme*2", "A",
     "Mr Satan assomme le complice du tireur, puis bat le tireur lui-même (fusil, et un pistolet qui le blesse ensuite)", "ch. 484"),
]
ANCHOR_ENTITIES = {
    # entité du modèle -> (log10 « × humain » attendu, incertitude) : groupes d'humains armés sans pouvoir
    # vérifié : soldats du Ruban rouge = humains ordinaires avec fusils (ch. 57 : Goku bloque les balles avec le Nyoi-Bō),
    # snipers et petits chars volants au QG (ch. 94)
    "soldats_ruban": (1.6, 0.7),
    # vérifié : braqueurs de banque armés qui tirent sur la police et sur Gohan (ch. 421), tireur et son complice (ch. 483-484)
    "criminels": (1.6, 0.7),
    # ajouté : l'armée (chars, missiles) qui attaque l'arène de Cell (ch. 392). Armes lourdes, mais toujours des humains sans pouvoir.
    # Un seul combat est connu, donc l'incertitude est grande
    "armee": (2.5, 1.0),
}
