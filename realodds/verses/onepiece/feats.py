"""Exploits mesurables (canon) de One Piece pour la comparaison inter-œuvres. Valeurs en log10 de l'unité SI."""
FEATS = [
    ("luffy", "eastblue", "energie", 10.0, 0.8, "Luffy fait s'effondrer Arlong Park", "ch. ~92-93",
     "tour de pierre de plusieurs étages (~2e3 m³ de maçonnerie) fracturée à 2e6-2e7 J/m³ ≈ 1e10 J", ""),
    ("ace", "alabasta", "energie", 11.5, 0.8, "Hiken : cinq navires de Baroque Works détruits d'un coup", "ch. ~158-159",
     "5 navires en bois ~200 t chacun, structure brisée et en feu ≈ 3e11 J", ""),
    ("whitebeard", "marineford", "energie", 17.5, 1.0, "Il lève deux tsunamis géants de chaque côté de Marineford", "ch. 553",
     "vagues de ~100 m sur des kilomètres : énergie potentielle et cinétique ~1e17-1e18 J", ""),
    ("aokiji", "marineford", "energie", 16.0, 0.8, "Il gèle les deux tsunamis et la baie d'un coup", "ch. 553",
     "~3e7 m³ d'eau gelée × 3,3e8 J/m³ (fusion + refroidissement) ≈ 1e16 J", ""),
    ("akainu", "marineford", "energie", 14.0, 1.0, "Ryûsei Kazan : une pluie de poings de magma sur la baie", "ch. ~570",
     "dizaines de blocs de ~10 m (~3e6 kg) portés à la fusion (~1,5e6 J/kg) ≈ 1e14 J", ""),
    ("fujitora", "gear4", "energie", 14.5, 1.2, "Il fait tomber une météorite sur Dressrosa", "ch. ~709",
     "météorite ~50 m (~2e8 kg) arrivant à ~5 km/s ≈ 3e15 J, partiellement retenue : ~3e14 J", ""),
    ("luffy", "wano5", "force", 6.5, 1.0, "Gear 5 : il attrape Kaido en dragon et le fait tournoyer", "ch. ~1044-1046",
     "dragon de plusieurs centaines de mètres : ~1e6-1e7 kg", ""),
]
ANCHORS = []
ANCHOR_ENTITIES = {
    "marines_ordinaires": (1.6, 0.7),   # Marines armés de fusils, en groupe
    "higuma": (1.1, 0.4),               # bandit armé, humain sans pouvoir (bat Luffy enfant)
}
