"""Exploits mesurables (canon) de Naruto pour la comparaison inter-œuvres. Valeurs en log10 de l'unité SI.
Chaque calcul est un ordre de grandeur : les hypothèses sont écrites, l'incertitude (log10_sd) est large exprès.
Ne garder que des exploits à pleine puissance ou à enjeu (un exploit « décontracté » sous-estime la force)."""
FEATS = [
    # (perso, arc, type, log10_valeur, log10_sd, exploit, réf. canon, calcul et hypothèses, source)
    ("sasuke", "itachi", "energie", 9.5, 0.4, "Kirin : il fait tomber un vrai éclair sur Itachi", "ch. 391-392",
     "un éclair naturel libère 1 à 5 GJ", ""),
    ("deidara", "itachi", "energie", 16.0, 0.7, "C0 : autodestruction annoncée sur 10 km de rayon", "ch. 361-362",
     "rayon de destruction ~10 km ; loi en cube depuis Hiroshima (6e13 J, ~1,6 km) : (10/1,6)^3 × 6e13 ≈ 1e16 J", ""),
    ("nagato", "pain", "energie", 15.0, 0.8, "Shinra Tensei : Konoha rasée, cratère d'environ 1 km", "ch. 422",
     "cratère ~1 km de diamètre, ~50 m de profondeur : ~4e7 m³ déplacés et fracturés à ~2e7 J/m³ ≈ 1e15 J", ""),
    ("nagato", "pain", "energie", 16.0, 1.0, "Chibaku Tensei : une sphère de roche de plusieurs centaines de mètres soulevée dans le ciel", "ch. 449",
     "sphère ~600 m (3e11 kg) montée à ~1-3 km : m·g·h ≈ 3e15 à 1e16 J", ""),
    ("madara", "guerre4a", "energie", 16.0, 1.0, "Tengai Shinsei : deux météorites tombent sur l'Alliance", "ch. 575-576",
     "roche ~300 m (4e10 kg) à ~700 m/s à l'impact : ½mv² ≈ 1e16 J", ""),
    ("hagoromo", "kaguya", "energie", 29.0, 1.5, "Il crée la Lune (Chibaku Tensei sur l'enveloppe de Jûbi)", "ch. 670",
     "énergie de liaison gravitationnelle de la Lune ≈ 1,2e29 J ; exploit mythique et isolé, incertitude maximale", ""),
    ("tsunade", "tsunade", "energie", 9.0, 0.8, "Un coup de poing qui fend le sol sur des dizaines de mètres", "ch. ~166-170",
     "fissure ~30 m × 5 m × 3 m de roche fracturée (~5e2 m³) à 2e6-2e7 J/m³ ≈ 1e9 J", ""),
    ("killer_b", "hachibi", "energie", 14.0, 1.0, "Bijû Dama de Hachibi contre Taka", "ch. ~413-415",
     "explosion de plusieurs centaines de mètres ; équivalent ~25 kt de TNT ≈ 1e14 J", ""),
    ("naruto", "final", "energie", 15.0, 1.0, "Dernier choc contre Sasuke : la Vallée de la Fin et ses statues pulvérisées", "ch. 695-698",
     "cratère et falaises détruits sur ~1 km : ~1e7-1e8 m³ fracturés ≈ 1e15 J", ""),
    ("naruto", "pain", "force", 5.0, 0.7, "En mode Ermite, il soulève la statue géante de crapaud du mont Myôboku", "ch. ~412",
     "statue de pierre ~15 m de haut ≈ 1e5 kg", ""),
]
ANCHORS = [
    # rencontres canon avec des êtres réels : (perso, arc, entité, résultat, exploit, réf.)
    ("zabuza", "vague", "soldat_arme*30", "A", "Zabuza, désarmé et mourant, massacre les mercenaires de Gatô", "ch. 32"),
    ("naruto", "vague", "soldat_arme*2", "A", "Naruto (clones) bat les deux hommes de main de Gatô chez Tazuna", "ch. ~30"),
]
