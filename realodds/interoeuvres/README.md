# Inter-œuvres (expérimental)

- `../feats.py`, `../verses/<œuvre>/feats.py` : exploits canon chiffrés (log10 SI) et ancres (humains armés, êtres réels).
- `cross.py` : relie l'échelle de chaque œuvre à l'échelle commune u = log10(« × humain normal ») ; MAP + Laplace ;
  vraisemblance de Student pour les exploits ; pentes des exploits non énergétiques estimées. Écrit `cross_out.json`.
- `build_cross.py` + `body_cross.html` : page publiée « Inter-œuvres ».
- Ajouter une œuvre : écrire son `feats.py` (même format), l'ajouter à `VERSES` dans `cross.py` et à `PATHS` dans `build_cross.py`.
