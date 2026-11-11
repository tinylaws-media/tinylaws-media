"""Exploits mesurables (canon) de Dragon Ball pour la comparaison inter-œuvres. Valeurs en log10 de l'unité SI.
Les niveaux de puissance officiels ne sont pas des exploits physiques et ne sont pas utilisés ici."""
FEATS = [
    ("goku", "pilaf", "force", 3.0, 0.3, "Goku enfant soulève et jette la voiture de Bulma", "ch. 1",
     "voiture ~1 000 kg", ""),
    ("roshi", "tournoi21", "energie", 14.3, 1.0, "Kamehameha à pleine puissance : le mont Fry-pan et le château soufflés", "ch. ~14",
     "petite montagne ~1e7 m³ pulvérisée à ~2e7 J/m³ ≈ 2e14 J (exploit d'avant le 21e tournoi, même Roshi)", ""),
    ("roshi", "tournoi21", "energie", 28.5, 1.2, "Kamehameha qui détruit la Lune", "ch. ~46",
     "liaison gravitationnelle de la Lune 1,2e29 J ; « détruite » sans dispersion complète : 1e28-1e29 J ; exploit célèbre pour son incohérence", ""),
    ("piccolo", "saiyan", "energie", 28.5, 1.2, "Piccolo détruit la Lune pour que Gohan ne se transforme plus", "ch. ~204",
     "même calcul que Roshi", ""),
    ("nappa", "saiyan", "energie", 15.0, 0.8, "Un geste de deux doigts : une ville entière rasée", "ch. ~211",
     "explosion de plusieurs km de rayon ≈ 0,2-1 Mt de TNT ≈ 1e15 J", ""),
    ("freeza", "freezer", "energie", 31.5, 1.0, "Il fait exploser Namek (la planète met quelques minutes à mourir)", "ch. ~319-328",
     "Namek supposée proche de la Terre en taille ; liaison gravitationnelle de la Terre 2,2e32 J ; destruction lente, donc partielle : ~3e31 J", ""),
    ("kid_buu", "buu", "energie", 32.3, 0.5, "Buu détruit la Terre d'un coup", "ch. ~502",
     "liaison gravitationnelle de la Terre 2,2e32 J", ""),
]
ANCHORS = [
    # les soldats du Ruban rouge et les criminels sont déjà des combattants du modèle : ils servent d'ancres (voir ANCHOR_ENTITIES)
]
ANCHOR_ENTITIES = {
    # entité du modèle -> (log10 « × humain » attendu, incertitude) : humains armés en groupe
    "soldats_ruban": (1.6, 0.7),
    "criminels": (1.6, 0.7),
}
