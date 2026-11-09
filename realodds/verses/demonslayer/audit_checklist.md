# Audit Demon Slayer : contrôle de chaque personnage

Une ligne par personnage ayant au moins 2 combats ou un statut officiel (40 personnages, groupes génériques exclus). Valeurs : arcs où il combat, avant → après correction (échelons). Canon : manga de Gotōge (ch. 1-205) et fanbooks officiels. Seuil : écart ≥ ~0,4 échelon.

## Corrections transversales

- Marque, Monde transparent, lames rouges, danse du dieu du feu, éveil de Nezuko : retirés des étiquettes de combat (`marque`, `boost`, que le modèle ignorait de toute façon) et codés en sauts datés, placés **avant** le combat où la technique apparaît (plusieurs sauts tombaient juste après : Hinokami 2,2085 après Rui 2,208, Marque de Tanjiro 2,5031 après Daki 2,502, Marques de Giyu, Sanemi, Gyomei, Mitsuri, Iguro après leur combat).
- Âge de Yoriichi : étiquette `age` remplacée par un saut daté (-0,5 à -345) et `SLOW` pour Yoriichi, Urokodaki, Shinjuro ; le duel contre Kokushibo passe dans un arc à part (« vieillesse », -340) pour que l'arc Sengoku montre Yoriichi à son apogée.
- Poison de Shinobu contre Doma : circonstance extérieure portée par Doma (`malade`) au lieu d'un `prepa` crédité à Kanao et Inosuke.
- Arc « avant » placé à t = -2 (au lieu de -5) : Kanae, morte à -1,8, n'apparaissait dans aucun arc.
- Rééducation (jeux de Kanao, ch. 49-50) : jeux de réflexes, pas des combats → marqués « ? » ; la victoire de Tanjiro (après la concentration totale) passe à l'arc du train, pour que « Tanjiro à Natagumo » soit celui qui affronte Rui.

## Personnages

- **yoriichi** (Yoriichi Tsugikuni, 2 combats) — sengoku 8,0→8,6, vieillesse —→8,1 — trop proche de Muzan (62 % seulement) et l'arc Sengoku montrait le vieillard de -340 → CORRIGÉ (statut 8,5, écart 1,5 sur Muzan, Muzan à la fin toujours sous Yoriichi, saut de vieillesse daté ; ch. 174-178, 186-187)
- **muzan** (Muzan Kibutsuji, 9 combats) — sengoku 6,9→7,1, avant 7,0→7,3, mugen 7,2→7,4, chateau 7,1→7,4, aube 7,1→7,4 — trop proche de Kokushibo (61 %) → CORRIGÉ (écart 1,5 : il tient seul, empoisonné, les Piliers que Kokushibo n'a affrontés qu'à quatre ; ch. 98, 139, 184-191) ; drogue de Tamayo bien en `malade` dans tous les combats de l'aube
- **kokushibo** (Kokushibo, Lune supérieure 1, 6 combats) — vieillesse —→6,5, chateau 6,3→6,3 — ok (Lune 1 au-dessus de Doma, battu à quatre ; ch. 164-177)
- **tanjiro_oni** (Tanjiro roi des démons, 1 combat) — aube 6,3→6,4 — ok (ch. 201-204) ; NON RÉSOLU : la fenêtre d'affichage du modèle (premier nœud - 0,3 an) le montre dès le village des forgerons, effet de model.py
- **gyomei** (Gyomei Himejima, 6 combats) — avant 2,8→2,9, chateau 5,0→5,7, aube 5,0→5,9 — plus fort des Piliers mais dépassé par Muichiro au village et à l'entraînement (4,9 contre 4,7) → CORRIGÉ (statuts 4,8 et 5,0, ordre Gyomei > Muichiro et > Mitsuri, Marque et Monde transparent datés ; ch. 134-135, 168-172)
- **doma** (Doma, Lune supérieure 2, 4 combats) — avant —→5,8, chateau 5,9→5,9 — ok (poison de Shinobu désormais en `malade`, ch. 141-163)
- **akaza** (Akaza, Lune supérieure 3, 2 combats) — mugen 5,8→5,8, chateau 5,8→5,8 — ok (Rengoku 14 %, Giyu seul 23 % ; ch. 63-66, 147-156)
- **sanemi** (Sanemi Shinazugawa, 9 combats) — avant 1,6→1,6, entrainement 4,6→4,6, chateau 4,9→4,9, aube 4,9→5,1 — ok (Marque datée avant son duel avec Kokushibo, lame rouge ch. 187-189)
- **hantengu** (Hantengu, Lune supérieure 4, 3 combats) — forgerons 5,1→5,1 — ok
- **giyu** (Giyu Tomioka, 11 combats) — natagumo 4,4→4,4, chateau 4,8→4,9, aube 4,8→5,1 — ok (Marque datée avant Akaza, ch. 151)
- **muichiro** (Muichiro Tokito, 7 combats) — forgerons 5,0→4,9, entrainement 4,9→4,8, chateau 4,9→5,0 — au-dessus de Gyomei → CORRIGÉ par l'ordre sur Gyomei ; saut Mémoire + Marque porté à 0,8 pour sa victoire écrasante sur Gyokko (ch. 118-122), lame rouge datée (ch. 173). Duel Muichiro/Gyokko encore à 45/39, voir non résolus
- **tanjiro** (Tanjiro Kamado, 31 combats) — selection 2,1→2,1, asakusa 2,2→2,2, natagumo 3,3→2,7, mugen 3,4→3,3, yuukaku 3,8→3,7, forgerons 3,8→3,7, entrainement 4,2→4,1, chateau 4,2→4,6, aube 4,2→4,9 — trop haut à Natagumo (au-dessus de Rui, qu'il ne bat pas) et aucun progrès entre l'entraînement et la fin → CORRIGÉ (jeux de rééducation reclassés, Monde transparent ch. 148-151, treize mouvements ch. 192-194) ; progression désormais monotone
- **gyokko** (Gyokko, Lune supérieure 5, 2 combats) — forgerons 4,8→4,8 — ok
- **gyutaro** (Gyutaro, Lune supérieure 6, 1 combat) — yuukaku 4,7→4,7 — ok
- **mitsuri** (Mitsuri Kanroji, 7 combats) — forgerons 4,5→4,5, chateau 4,5→4,5, aube 4,5→4,7 — ok (Marque datée avant Zohakuten, ch. 123)
- **iguro** (Obanai Iguro, 7 combats) — entrainement 3,9→3,9, chateau 4,0→3,9, aube 4,2→4,5 — ok, un peu bas parmi les Piliers (épreuve d'entraînement perdue contre Tanjiro, `retenue`) ; Monde transparent et lame rouge datés (ch. 188-189)
- **nakime** (Nakime, 2 combats) — chateau 4,4→4,3 — ok (non combattante, statut large)
- **tengen** (Tengen Uzui, 2 combats) — yuukaku 4,3→4,3 — ok (retraite datée, ch. 97)
- **rengoku** (Kyojuro Rengoku, 1 combat) — mugen 4,3→4,3 — ok
- **shinobu** (Shinobu Kocho, 3 combats) — natagumo 4,1→4,1, chateau 4,1→4,1 — ok (seule Pilier incapable de décapiter, sous Giyu)
- **kanae** (Kanae Kocho, 1 combat) — avant —→4,1 — n'apparaissait dans aucun arc → CORRIGÉ (arc « avant » à t = -2)
- **kaigaku** (Kaigaku, 1 combat) — chateau 4,2→4,0 — statut 4,8 trop haut pour une Lune 6 promue depuis peu, battue d'un coup par Zenitsu → CORRIGÉ (statut 4,4, ch. 144-145)
- **kanao** (Kanao Tsuyuri, 7 combats) — natagumo 3,4→3,4, mugen 3,4→3,4, chateau 3,7→4,0, aube 3,7→4,0 — ok (Œil du jardin d'équinoxe daté puis œil abîmé, ch. 162-163)
- **shinjuro** (Shinjuro Rengoku, 1 combat) — mugen 3,7→3,9 — ok (ivre, `malade`)
- **urokodaki** (Sakonji Urokodaki, 1 combat) — avant 3,8→3,9 — ok
- **nezuko** (Nezuko Kamado, 9 combats) — selection 2,5→2,4, asakusa 2,6→2,4, natagumo 3,0→2,9, yuukaku 3,1→3,6, forgerons 3,4→3,4, aube 1,4→0,4 — sous Daki alors qu'elle la domine (forme éveillée seulement en `boost`, ignoré), et trop forte une fois humaine → CORRIGÉ (forme éveillée datée puis retour à la normale, ch. 83-86 ; retour à l'humain -3,0, ch. 196-197) ; immunité au soleil datée (ch. 126-127), simple petit saut
- **zenitsu** (Zenitsu Agatsuma, 9 combats) — asakusa 1,5→1,4, natagumo 1,6→1,5, yuukaku 2,1→2,0, chateau 3,3→3,6, aube 3,3→3,6 — sous Kaigaku qu'il bat → CORRIGÉ en partie (septième mouvement +0,8, ch. 145) ; voir non résolus
- **daki** (Daki, 4 combats) — yuukaku 3,3→3,4 — ok (la plus faible du duo)
- **enmu** (Enmu, Lune inférieure 1, 1 combat) — mugen 3,0→3,1 — ok
- **rui** (Rui, Lune inférieure 5, 2 combats) — natagumo 2,8→2,8 — ok (Tanjiro 39 % / Rui 45 % désormais)
- **inosuke** (Inosuke Hashibira, 12 combats) — asakusa 1,6→1,6, natagumo 1,6→1,6, mugen 2,1→2,1, yuukaku 2,1→2,1, chateau 2,5→2,5, aube 2,5→2,5 — un peu bas face à Zenitsu en fin d'histoire (2,5 contre 3,6) ; aucune victoire individuelle canon à ajouter, NON RÉSOLU
- **tamayo** (Tamayo, 2 combats) — asakusa 2,4→2,5, chateau 2,4→2,5 — ok
- **sabito** (Sabito, 4 combats) — avant 2,5→2,5 — ok
- **spider_father** (Père araignée, 3 combats) — natagumo 2,4→2,4 — ok
- **hand_demon** (Démon aux mains, 4 combats) — avant 2,2→2,2, selection 1,2→1,1 — ok
- **genya** (Genya Shinazugawa, 5 combats) — selection 0,9→0,9, forgerons 1,9→1,9, chateau 2,2→2,2 — ok
- **yushiro** (Yushiro, 3 combats) — asakusa 2,1→2,1, chateau 2,1→2,1, aube 2,1→2,1 — ok
- **kyogai** (Kyogai, 1 combat) — asakusa 2,1→2,1 — ok
- **hakuji** (Hakuji, 4 combats) — avant 1,8→1,8 — ok
- **spider_mother** (Mère araignée, 2 combats) — natagumo 1,3→1,3 — ok

## Rangs des pourfendeurs

Rangs (Mizunoto … Kinoe) : seul le rang Mizunoto de la Sélection finale est encodé. Les rangs suivants de Tanjiro (Kanoe puis au-delà) ne sont pas datés précisément dans le manga et récompensent le nombre de démons tués plus que la force ; non ajoutés.
