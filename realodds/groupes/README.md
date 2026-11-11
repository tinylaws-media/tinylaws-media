# Combats de groupe : comment le poids des alliés (η) est estimé

1. Chaque œuvre est ajustée avec log η libre (a priori N(0 ; 0,5)) : `OUT=... python3 model.py <dossier>`.
2. `pool.py` retire l'a priori de chaque estimation (approximation de Laplace) et combine les dix œuvres
   par méta-analyse à effets aléatoires (DerSimonian–Laird) : η commun ≈ 0,66 (IC 95 % 0,40–1,08),
   hétérogénéité τ ≈ 0,50 sur log η (Demon Slayer à part : les équipes y comptent beaucoup plus).
3. Ajustement final de chaque œuvre avec l'a priori partiellement mis en commun : log η ~ N(−0,419 ; 0,559)
   (`ETA_MU=-0.419 ETA_SD=0.559 python3 model.py <dossier>`).
4. Vérification indépendante de l'approximation : évidence de Laplace à η fixé (0,15 ; 0,4 ; 0,66 ; 1 ; 1,8)
   pour Naruto, One Piece et Demon Slayer (`evidence_grille.json`). « Seul le plus fort compte » (η = 0,15)
   perd de 1 à 3,7 unités de log-évidence ; les maxima concordent avec l'estimation libre.
