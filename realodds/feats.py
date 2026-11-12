"""Exploits mesurables (canon) de Naruto pour la comparaison inter-œuvres. Valeurs en log10 de l'unité SI.
Chaque calcul est un ordre de grandeur : les hypothèses sont écrites, l'incertitude (log10_sd) est large exprès.
Ne garder que des exploits à pleine puissance ou à enjeu (un exploit « décontracté » sous-estime la force).
Vérification de la version écrite de mémoire (nov. 2026) : chaque ligne d'origine porte # vérifié / # corrigé / # supprimé.
Énergies de référence : Hiroshima ≈ 6,3e13 J (15 kt), rayon de destruction lourde (5 psi) ≈ 1,7 km, le rayon suit E^(1/3) ;
fragmentation du granite 2–8 MJ/m³, broyage/éjection violente 2e7 J/m³ ; roche 2 700 kg/m³ ; eau 1 000 kg/m³."""
FEATS = [
    # (perso, arc, type, log10_valeur, log10_sd, exploit, réf. canon, calcul et hypothèses, source)

    # ---- bas de l'échelle (genin / jônin, 1re partie et début de la 2e) ----
    # nouveau
    ("kakashi", "vague", "energie", 9.7, 1.0, "Suiton : Daibakufu (grande cascade) contre Zabuza, vague qui balaie la berge du lac",
     "ch. ~15 (premier combat contre Zabuza)",
     "masse d'eau soulevée ~1e4–1e5 m³ (vague à hauteur d'arbres, ~20 m) montée de ~15 m : m·g·h ≈ 1,5e9–1,5e10 J ; dimensions lues sur les cases",
     "https://naruto.fandom.com/wiki/Water_Release:_Great_Waterfall_Technique"),
    # nouveau
    ("sakura", "kazekage", "energie", 8.9, 0.8, "Elle pulvérise d'un coup de poing le rocher qui scelle le repaire d'Akatsuki",
     "ch. 262",
     "rocher de 5–10 m de diamètre (65–520 m³ de granite) brisé en blocs à 2–8 MJ/m³ ≈ 1e8–4e9 J",
     "https://daddyjim.com/naruto/episode/Charge-Tactic-Button-Hook-Entry"),
    # corrigé : le « coup de poing qui fend le sol » (ch. ~166-170) n'avait ni chapitre ni dimensions ; la seule fente de sol
    #   sourcée (ch. 159) est une pichenette décontractée contre Naruto. Remplacé par l'exploit chiffrable du même combat.
    # ("tsunade", "tsunade", "energie", 9.0, 0.8, "Un coup de poing qui fend le sol sur des dizaines de mètres", "ch. ~166-170", ...),
    ("tsunade", "tsunade", "force", 5.4, 0.8, "Elle soulève et lance le sabre de Gamabunta pour clouer Manda",
     "ch. 170, p. 15-16",
     "lame de 20–35 m × 2–4 m × 0,3–0,5 m d'acier (12–70 m³ × 7 800 kg/m³) ≈ 1e5–5e5 kg ; taille de Gamabunta non chiffrée dans le canon",
     "https://naruto.fandom.com/wiki/Tsunade"),
    # vérifié (chapitre précisé : ch. 390-391) ; l'énergie est celle d'un éclair naturel que Sasuke guide, donc une borne
    #   de ce qu'il canalise, pas de ce qu'il produit.
    ("sasuke", "itachi", "energie", 9.5, 0.5, "Kirin : il fait tomber un vrai éclair sur Itachi",
     "ch. 390-391",
     "un éclair naturel libère ~1 à 10 GJ ; Sasuke ne fait que le guider (nuages créés par ses Katon et l'Amaterasu d'Itachi)",
     "https://daddyjim.com/naruto/manga-chapter/Together-with-the-Thunder"),
    # nouveau
    ("itachi", "itachi", "resistance", 9.5, 0.6, "Le Susanoo d'Itachi encaisse Kirin de plein fouet",
     "ch. 391",
     "même énergie que Kirin (~1–10 GJ) ; Itachi reste debout grâce au Susanoo (bouclier de chakra, pas son corps)",
     "https://daddyjim.com/naruto/manga-chapter/Together-with-the-Thunder"),

    # ---- milieu (Akatsuki, Kage) ----
    # nouveau
    ("deidara", "kazekage", "energie", 12.8, 1.0, "C3 lâché sur Suna : bombe donnée comme capable de raser un village",
     "ch. ~248-249 ; databook 3 (Sha no Sho) p. 245",
     "village rasé = rayon de destruction lourde 0,5–1,5 km ; (r/1,7 km)^3 × 6,3e13 J ≈ 1,6e12–4e13 J",
     "https://naruto.fandom.com/wiki/C3"),
    # nouveau
    ("gaara", "kazekage", "resistance", 12.8, 1.2, "Gaara arrête le C3 au-dessus de Suna avec un bouclier de sable et protège le village",
     "ch. ~248-249",
     "il absorbe toute l'énergie du C3 (estimée ci-dessus) ; bouclier de sable, pas son corps ; sd élargi",
     "https://naruto.fandom.com/wiki/C3"),
    # corrigé : chapitre (ch. 362-363 au lieu de 361-362) ; rayon de 10 km confirmé (dit par Deidara, et databook 3 p. 262) ;
    #   calcul refait avec le rayon 5 psi d'Hiroshima (1,7 km) ; autodestruction = pleine puissance.
    # ("deidara", "itachi", "energie", 16.0, 0.7, "C0 : autodestruction annoncée sur 10 km de rayon", "ch. 361-362", ...),
    ("deidara", "itachi", "energie", 16.1, 0.7, "C0 : autodestruction sur 10 km de rayon contre Sasuke",
     "ch. 362-363 ; databook 3 (Sha no Sho) p. 262",
     "rayon de destruction 10 km (annoncé par Deidara, repris par le databook) ; (10/1,7)^3 × 6,3e13 J ≈ 1,3e16 J",
     "https://naruto.fandom.com/wiki/C0"),
    # corrigé : chapitre (ch. 429, et non 422) ; taille du cratère : aucune donnée canon, Konoha estimée à 2,4–3,5 km
    #   par des fans d'après le mont des Hokage ; profondeur devinée ; sd élargi.
    # ("nagato", "pain", "energie", 15.0, 0.8, "Shinra Tensei : Konoha rasée, cratère d'environ 1 km", "ch. 422", ...),
    ("nagato", "pain", "energie", 14.8, 0.9, "Shinra Tensei à grande échelle : Konoha réduite à un cratère profond",
     "ch. 429, p. 10-13",
     "cratère de 1,5–3 km de diamètre, 30–100 m de profondeur : V ≈ (π/8)·D²·h ≈ 3e7–3,5e8 m³ broyés et éjectés à 2e6–2e7 J/m³ ≈ 5e13–7e15 J",
     "https://naruto.fandom.com/wiki/Shinra_Tensei"),
    # corrigé : chapitre (ch. 438-439, et non 449) ; taille de la sphère non donnée par le canon, refaite sur 300–600 m
    #   et une altitude de 0,5–2 km ; valeur abaissée de 16,0 à 15,0.
    # ("nagato", "pain", "energie", 16.0, 1.0, "Chibaku Tensei : une sphère de roche ... soulevée dans le ciel", "ch. 449", ...),
    ("nagato", "pain", "energie", 15.0, 1.2, "Chibaku Tensei : un satellite de roche formé et soulevé dans le ciel autour de Kurama",
     "ch. 438-439",
     "sphère de 300–600 m (3,8e10–3e11 kg à 2 700 kg/m³) montée à 0,5–2 km : m·g·h ≈ 2e14–6e15 J ; dimensions devinées",
     "https://naruto.fandom.com/wiki/Chibaku_Tensei"),
    # nouveau (remplace le soulèvement de la statue, voir plus bas)
    ("naruto", "pain", "force", 5.4, 1.0, "En mode Ermite, il arrête net la charge du rhinocéros géant de la Voie animale et le projette en l'air",
     "ch. ~431",
     "rhinocéros de 5–15 m au garrot ; masse d'un rhinocéros blanc (1,8 m, 2 300 kg) × (h/1,8)^3 ≈ 5e4–1,3e6 kg ; dimensions devinées",
     "https://naruto.fandom.com/wiki/Giant_Rhino"),
    # supprimé : la statue de crapaud soulevée au mont Myôboku vient de l'épisode 155 de l'anime (« The First Challenge ») ;
    #   aucun résumé de chapitre du manga (ch. 409-418) ne la mentionne, et sa taille était inventée.
    # ("naruto", "pain", "force", 5.0, 0.7, "En mode Ermite, il soulève la statue géante de crapaud du mont Myôboku", "ch. ~412", ...),

    # ---- haut de l'échelle (4e Grande Guerre et au-delà) ----
    # corrigé : chapitre (ch. 560-561 ; Ônoki allège la 1re météorite, Gaara la retient, la 2e la percute) ;
    #   taille non chiffrée par le canon, prise à 300 m–1 km ; vitesse d'impact 100–340 m/s (onomatopées, sous la
    #   vitesse du son) au lieu de 700 m/s.
    # ("madara", "guerre4a", "energie", 16.0, 1.0, "Tengai Shinsei : deux météorites ...", "ch. 575-576", ...),
    ("madara", "guerre4a", "energie", 15.9, 1.0, "Tengai Shinsei : deux météorites s'abattent sur la 4e division de l'Alliance",
     "ch. 560-561",
     "roches de 300 m–1 km (3,8e10–1,4e12 kg) à 100–340 m/s : ½mv² ≈ 2e14–8e16 J chacune, ~4e15 J au centre, × 2",
     "https://daddyjim.com/naruto/manga-chapter/The-Power-of-That-Name"),
    # corrigé : chapitre (ch. 696-697 pour le choc Flèche d'Indra / Kurama aux Six Chemins qui détruit les statues ;
    #   ch. 698 = dernier Rasengan contre Chidori) ; l'énergie est celle d'un choc à deux, la part de Naruto est
    #   prise à la moitié ; dimensions de la vallée non chiffrées.
    # ("naruto", "final", "energie", 15.0, 1.0, "Dernier choc contre Sasuke : la Vallée de la Fin et ses statues pulvérisées", "ch. 695-698", ...),
    ("naruto", "final", "energie", 14.5, 1.2, "Choc final contre Sasuke : la Vallée de la Fin et ses statues pulvérisées",
     "ch. 696-698",
     "falaises et statues (~100 m) détruites : ~1e7–1e8 m³ broyés à 2e6–2e7 J/m³ ≈ 2e13–2e15 J, dont la moitié pour Naruto",
     "https://naruto.fandom.com/wiki/Naruto_and_Sasuke_5"),
    # supprimé : la Bijû Dama de Hachibi contre Taka (ch. 414, et non ~413-415 approximatif) n'a aucune dimension canon
    #   (« le paysage est rasé ») et Suigetsu l'absorbe avec son corps d'eau : chiffre de 25 kt invention, exploit douteux.
    # ("killer_b", "hachibi", "energie", 14.0, 1.0, "Bijû Dama de Hachibi contre Taka", "ch. ~413-415", ...),
    # supprimé : la Lune n'est pas un Chibaku Tensei de Hagoromo seul, c'est le « Rikudô Chibaku Tensei » de Hagoromo ET
    #   Hamura (ch. 681), un sceau, raconté en flashback et non montré ; l'énergie dépend d'hypothèses inconnues
    #   (rassembler la roche ≠ la monter hors du puits terrestre, 1e29 à 5e30 J) ; c'est un pouvoir de scellement, pas
    #   une mesure de puissance brute.
    # ("hagoromo", "kaguya", "energie", 29.0, 1.5, "Il crée la Lune (Chibaku Tensei sur l'enveloppe de Jûbi)", "ch. 670", ...),
]
ANCHORS = [
    # rencontres canon avec des êtres réels : (perso, arc, entité, résultat, exploit, réf.)
    # corrigé : chapitre (ch. 23 « Deux attaques », et non ~30) ; c'est bien Naruto (avec ses clones) qui bat Zôri et
    #   Waraji, deux sabreurs à gages de Gatô sans chakra, après avoir tiré Inari d'affaire.
    ("naruto", "vague", "soldat_arme*2", "A", "Naruto (clones) bat Zôri et Waraji, les deux sabreurs de Gatô, devant chez Tazuna", "ch. 23"),
    # corrigé : Zabuza, bras inutilisables, se fraie un chemin jusqu'à Gatô avec un kunai entre les dents, mais tombe sous
    #   les coups des hommes de main ; il ne « massacre » pas la troupe (le nombre exact n'est pas donné, ~30 sur les cases).
    #   Résultat 'A' → 'D'.
    # ("zabuza", "vague", "soldat_arme*30", "A", "Zabuza, désarmé et mourant, massacre les mercenaires de Gatô", "ch. 32"),
    ("zabuza", "vague", "soldat_arme*30", "D", "Zabuza, bras brisés, traverse la troupe de Gatô jusqu'à lui puis s'effondre sous leurs coups", "ch. 32"),
    # nouveau
    ("zabuza", "vague", "humain", "A", "Zabuza décapite Gatô (homme d'affaires sans entraînement)", "ch. 32"),
    # nouveau
    ("kakashi", "vague", "soldat_arme*30", "A", "Kakashi, Naruto et les villageois font fuir les hommes de main restants de Gatô", "ch. 33"),
]
