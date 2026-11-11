"""Real Odds — animaux : rencontres documentées, cluster MER / HUMAINS / CHIENS / KANGOUROUS.

Convention : `a` = vainqueur quand res="A" ; res="D" = issue nulle après contact réel.
na/nb = individus réellement engagés. m : 1 serré, 2 net, 3 mort/tué.
Remarques générales :
- « chien » sert aussi de proxy pour le dingo (lignes marquées « dingo » dans la note) : un dingo pèse ~15 kg,
  nettement moins que le « gros chien domestique » du modèle (32 kg). Les chiens errants indiens (~15-25 kg) et
  les petits chiens (schnauzer) sont également hors gabarit et signalés dans la note.
- L'id « kangourou » est le kangourou roux ; la plupart des attaques sur humains et chiens sont le fait du
  kangourou gris (de l'Est M. giganteus, de l'Ouest M. fuliginosus) : proxy signalé dans la note.
- Les statistiques chien>humain et loup>chien sont des registres de victimes (pas de dénominateur des
  rencontres où l'humain/le chien l'a emporté) : biais fort en faveur de l'attaquant, à pondérer.
- 2e passage : chaque ligne porte « # vérifié », « # corrigé : … » ou « # supprimé : … ».
"""

ENC = []


def E(a, na, b, nb, res, m=2, ta=(), tb=(), count=1, qual="B", src="", note="", lieu="", annee=None):
    ENC.append(dict(a=a, na=na, b=b, nb=nb, res=res, m=m, ta=list(ta), tb=list(tb), count=count, qual=qual,
                    src=src, note=note, lieu=lieu, annee=annee))


_REG = " (registre : seuls les décès sont recensés)"

# ---------------------------------------------------------------------------
# ORQUE vs REQUIN BLANC
# ---------------------------------------------------------------------------
E("orque", 2, "requin_blanc", 1, "A", 3, tb=["jeune"], qual="A",
  src="https://www.nwf.org/en/Magazines/National-Wildlife/2004/Showdown-at-Sea",
  note="Deux orques femelles adultes (CA2 et CA6, pod L.A.) tuent un requin blanc subadulte de ~3 m et mangent le foie ; départ des requins des Farallon ensuite (lien supposé) (obs. P. Pyle)",
  lieu="Îles Farallon, Californie", annee=1997)  # corrigé : orques = 2 femelles adultes (la « petite » était adulte) ; lien avec le départ des requins présenté comme spéculatif
E("orque", 2, "requin_blanc", 1, "A", 3, count=8, qual="A",
  src="https://www.livescience.com/killer-whale-great-white-shark-killing-spree",
  note="Towner et al. 2022 (Afr. J. Mar. Sci., doi:10.2989/1814232X.2022.2066723) : Port et Starboard (2 mâles adultes) liés à ≥8 carcasses de requins blancs éviscérées (foie retiré) depuis 2017 ; attribution indirecte (carcasses + présence des orques, mises à mort non observées), tailles des requins non précisées",
  lieu="Gansbaai, Afrique du Sud", annee=2017)  # corrigé : attribution indirecte précisée ; source lisible (tandfonline non accessible)
E("orque", 5, "requin_blanc", 1, "A", 3, count=1, qual="A",
  src="https://phys.org/news/2022-10-proof-orcas-white-sharks.amp",
  note="Groupe de 5 orques filmé (hélico/drone) tuant un requin blanc ; Towner et al. 2022 Ecology doi:10.1002/ecy.3875 ; taille du requin non précisée",
  lieu="Mossel Bay, Afrique du Sud", annee=2022)  # vérifié
E("orque", 5, "requin_blanc", 1, "A", 3, count=3, qual="B",
  src="https://phys.org/news/2022-10-proof-orcas-white-sharks.amp",
  note="Même chasse : 3 autres requins blancs probablement tués (suspectés, non filmés)",
  lieu="Mossel Bay, Afrique du Sud", annee=2022)  # vérifié
E("orque", 1, "requin_blanc", 1, "A", 3, tb=["jeune"], qual="A",
  src="https://www.scientificamerican.com/article/lone-orca-killed-great-white-shark-in-first-documented-case/",
  note="Starboard (mâle adulte) seul tue un requin blanc juvénile de 2,5 m en moins de 2 min et mange son foie (Port présent mais non impliqué)",
  lieu="Mossel Bay, Afrique du Sud", annee=2023)  # vérifié
E("orque", 2, "requin_blanc", 1, "A", 3, tb=["jeune"], qual="B",
  src="https://www.scientificamerican.com/article/lone-orca-killed-great-white-shark-in-first-documented-case/",
  note="Requin blanc de 3,55 m (subadulte probable) échoué le lendemain sans foie, attribué à une attaque antérieure non observée (effectif estimé : Port et Starboard seuls présents)",
  lieu="Mossel Bay, Afrique du Sud", annee=2023)  # corrigé : na 1→2 (effectif estimé), requin de 3,55 m tagué jeune (subadulte)
E("orque", 5, "requin_blanc", 1, "A", 3, tb=["jeune"], count=2, qual="A",
  src="https://www.frontiersin.org/news/2025/11/03/orcas-killing-young-great-white-sharks-by-flipping-upside-down-frontiers-marine-science",
  note="Pod de Moctezuma (5 orques) retourne et tue 2 requins blancs juvéniles, foie consommé (Higuera Rivas et al. 2025, Front. Mar. Sci.)",
  lieu="Golfe de Californie, Mexique", annee=2020)  # vérifié
E("orque", 5, "requin_blanc", 1, "A", 3, tb=["jeune"], count=1, qual="A",
  src="https://www.frontiersin.org/news/2025/11/03/orcas-killing-young-great-white-sharks-by-flipping-upside-down-frontiers-marine-science",
  note="Même pod (5 orques) tue un 3e requin blanc juvénile",
  lieu="Golfe de Californie, Mexique", annee=2022)  # vérifié
E("orque", 7, "requin_blanc", 1, "A", 3, qual="B",
  src="https://www.livescience.com/animals/sharks/great-white-shark-ripped-in-2-was-loaded-with-orca-dna-scientists-say",
  note="Requin blanc adulte de ~4,9 m retrouvé coupé en deux, ADN d'orque sur les plaies ; ~7 orques vues à proximité quelques jours avant (effectif estimé)",
  lieu="Portland, Victoria, Australie", annee=2023)  # vérifié (effectif estimé ajouté)

# ---------------------------------------------------------------------------
# ORQUE vs MORSE (très peu documenté)
# ---------------------------------------------------------------------------
E("orque", 6, "morse", 1, "A", 3, qual="A",
  src="https://repository.library.noaa.gov/view/noaa/27306/noaa_27306_DS1.pdf",
  note="Kryukova et al. 2012 (Biology Bulletin 39:768) : 9 orques (7 adultes dont 1 mâle non participant, + 2 petits), 55 attaques sur un morse isolé en 17,3 min ; les orques repartent avec le morse (mise à mort implicite, tirée du résumé)",
  lieu="Flèche de Retkyn, Tchoukotka", annee=2008)  # vérifié

# ---------------------------------------------------------------------------
# REQUIN BLANC vs HUMAIN
# ---------------------------------------------------------------------------
E("requin_blanc", 1, "humain", 1, "A", 3, ta=["embuscade"], count=59, qual="A",
  src="https://www.floridamuseum.ufl.edu/shark-attacks/factors/species-implicated/",
  note="ISAF (1580-aujourd'hui, page consultée en 2026) : 59 attaques non provoquées mortelles attribuées au requin blanc" + _REG,
  lieu="Monde")  # corrigé : période « 1580-présent » (pas 2022) ; mention registre
E("requin_blanc", 1, "humain", 1, "D", 1, count=292, qual="A",
  src="https://www.floridamuseum.ufl.edu/shark-attacks/factors/species-implicated/",
  note="ISAF (1580-aujourd'hui) : 292 attaques non provoquées non mortelles ; le requin lâche souvent après une morsure (morsure exploratoire / riposte) ; issue ambiguë (supprimée par corrections.py)",
  lieu="Monde")  # vérifié (chiffre exact ; ligne retirée automatiquement par corrections.py)
E("humain", 2, "requin_blanc", 1, "D", 1, qual="B",
  src="https://www.foxnews.com/world/australian-man-punches-10-foot-shark-after-wife-attacked-while-surfing",
  note="Chantelle Doyle mordue à la jambe par un requin blanc de ~3 m ; son mari saute de sa planche sur le requin et le frappe jusqu'à ce qu'il lâche ; lacérations graves, survit",
  lieu="Shelly Beach, Port Macquarie, Australie", annee=2020)  # corrigé : A→D (le requin lâche, pas vaincu)
E("humain", 1, "requin_blanc", 1, "D", 1, qual="B",
  src="https://au.sports.yahoo.com/shark-attack-new-zealand-surfer-nick-minogue-punches-great-white-survives-incident-000825715.html",
  note="Nick Minogue (60 ans) : le requin blanc (identifié par les morsures) mord sa planche et lui entaille le bras ; deux coups de poing dans l'œil, le requin lâche",
  lieu="Pauanui, Nouvelle-Zélande")  # corrigé : A→D ; morsure sur la planche + bras
E("humain", 1, "requin_blanc", 1, "D", 1, qual="B",
  src="https://www.washingtontimes.com/news/2008/may/13/poke-in-shark-eye-saves-swimmer-in-australia/",
  note="Jason Cull (37 ans) saisi à la jambe par un requin (prob. blanc, ~5 m) ; coups de poing puis doigt dans l'œil, le requin lâche ; mollet en grande partie arraché",
  lieu="Middleton Beach, Albany, Australie", annee=2008)  # corrigé : A→D
E("humain", 1, "requin_blanc", 1, "D", 1, ta=["outil"], qual="B",
  src="https://gulfnews.com/world/oceania/diver-saved-his-life-by-poking-shark-in-the-eye-1.156535",
  note="Eric Nerhus (41 ans), plongeur, tête et épaules dans la gueule d'un requin de ~3 m (espèce non précisée par la source, prob. blanc) ; doigts dans l'orbite puis coup de burin à ormeaux dans l'œil, s'échappe (gilet plombé l'a protégé)",
  lieu="Cape Howe, Eden, Australie", annee=2007)  # corrigé : A→D ; espèce non confirmée par la source
E("humain", 1, "requin_blanc", 1, "D", 1, qual="B",
  src="https://www.illawarramercury.com.au/story/8996843/how-shark-cage-diving-pioneer-rodney-fox-survived-a-shark-attack/",
  note="Rodney Fox, chasseur sous-marin : griffe les yeux du requin, main dans la gueule, l'étreint ; le requin mord le flotteur à poissons, la ligne casse et Fox s'échappe ; 462 points de suture",
  lieu="Aldinga Beach, Australie du Sud", annee=1963)  # corrigé : A→D ; « yeux arrachés » → griffés ; le requin part avec le flotteur
E("humain", 1, "requin_blanc", 1, "D", 1, qual="C",
  src="https://newsinfo.inquirer.net/?p=706629",
  note="Mick Fanning renversé par un requin (espèce non identifiée par la source, blanc supposé), le frappe ; leash coupé, indemne ; l'expert parle d'investigation plutôt que de prédation",
  lieu="Jeffreys Bay, Afrique du Sud", annee=2015)  # corrigé : qual B→C (espèce non identifiée)

# ---------------------------------------------------------------------------
# ORQUE / GORILLE vs HUMAIN (sauvages — quasi inexistant)
# ---------------------------------------------------------------------------
E("orque", 1, "humain", 1, "D", 1, qual="C",
  src="https://en.wikipedia.org/wiki/Orca_attacks",
  note="Seule morsure d'orque sauvage bien rapportée : surfeur Hans Kretschmer mordu à la jambe (100 points), probable confusion avec un pinnipède (non sourcé sur Wikipédia) ; morsure unique sans combat",
  lieu="Point Sur, Californie", annee=1972)  # corrigé : A m=2 → D m=1 (morsure unique par erreur de proie, comme les morsures de requin non mortelles)
E("gorille", 1, "humain", 1, "A", 3, tb=["jeune"], qual="C",
  src="https://www.camer.be/64351/11:1/cameroun-un-gorille-bastonne-un-enfant-a-mort-cameroon.html",
  note="Un gorille (espèce non vérifiée, presse locale sans source nommée) rattrape un garçon de 14 ans qui fuyait et le frappe (mort dans la nuit, hémorragie) ; il bat ensuite séparément le père, le frère de 9 ans et la mère, puis regagne la forêt",
  lieu="Nguen, Haute-Sanaga, Cameroun", annee=2017)  # corrigé : nb 4→1 (victimes frappées l'une après l'autre en fuyant, pas un combat à 4)
# supprimé : gorille vs humain, Birpondo/Bertoua 2018 (camer.be) — témoin unique qui voit seulement un « gorille » traîner
#   la victime, corps non formellement retrouvé ni identifié, espèce non vérifiée, comportement (traîner un homme en forêt)
#   très improbable pour un gorille : trop peu fiable même en qual C.

# ---------------------------------------------------------------------------
# CHIMPANZÉ vs HUMAIN
# ---------------------------------------------------------------------------
E("chimpanze", 1, "humain", 2, "A", 2, ta=["captivite"], tb=["arme_blanche", "outil"], qual="A",
  src="https://en.wikipedia.org/wiki/Travis_(chimpanzee)",
  note="Travis (mâle adulte de 13 ans, 91 kg, obèse, élevé comme animal de compagnie) mutile Charla Nash (55 ans) ; la propriétaire Sandra Herold (70 ans) le frappe à la pelle et le poignarde au couteau de boucher sans l'arrêter ; un policier l'abat",
  lieu="Stamford, Connecticut", annee=2009)  # corrigé : âge/sexe/masse (bien au-dessus du chimpanzé moyen), tag outil (pelle) ajouté, âges des humains
E("chimpanze", 2, "humain", 2, "A", 2, ta=["captivite"], qual="A",
  src="https://en.wikipedia.org/wiki/St._James_Davis_chimpanzee_attack",
  note="Deux mâles évadés de leurs cages (Buddy 16 ans, Ollie 13 ans) mutilent St. James Davis (62 ans : doigts, pied, visage…) qui protège sa femme (pouce arraché) ; abattus au revolver par le gendre du propriétaire",
  lieu="Animal Haven Ranch, Bakersfield, Californie", annee=2005)  # corrigé : sexe/âges ajoutés
E("chimpanze", 2, "humain", 1, "A", 2, ta=["captivite"], qual="B",
  src="https://www.bangordailynews.com/2012/06/29/news/chimps-attack-american-at-south-africa-sanctuary/",
  note="Andrew Oberle (26 ans) tiré sous la clôture et traîné par deux chimpanzés du sanctuaire (Amadeus, Nikki), morsures multiples graves ; le gérant tire en l'air pour les chasser ; survit",
  lieu="Chimp Eden, Mpumalanga, Afrique du Sud", annee=2012)  # corrigé : sexe non confirmé pour les deux, fin par tirs de sommation
E("chimpanze", 2, "humain", 2, "A", 2, ta=["captivite"], qual="B",
  src="https://www.animallaw.info/article/incidents-attacks-involving-captive-chimpanzees",
  note="Deux chimpanzés évadés attaquent deux employés du zoo, l'un grièvement blessé ; abattus par les employés puis euthanasiés",
  lieu="Hogle Zoo, Salt Lake City", annee=1999)  # vérifié
E("chimpanze", 1, "humain", 1, "A", 3, ta=["captivite"], qual="B",
  src="https://newspaper.animalpeopleforum.org/2006/05/01/1st-chimp-at-tacugama-kills-man-leads-escape/",
  note="Évasion de 32 chimpanzés (Bruno, 20 ans, et 31 autres) ; Bruno tue le chauffeur Issa Kanu ; 3 passagers blessés (origine des blessures non précisée) (effectif estimé : seul Bruno est décrit attaquant)",
  lieu="Tacugama, Sierra Leone", annee=2006)  # corrigé : na 3→1, nb 4→1 (seul Bruno décrit attaquant ; les passagers ne sont pas décrits comme combattant)
E("chimpanze", 1, "humain", 1, "A", 2, tb=["jeune"], count=2, qual="A",
  src="https://radar.brookes.ac.uk/radar/file/22474f93-1df8-a60c-8d8f-a4cb4548bff9/1/mclennan2012troublesome.pdf",
  note="Chimpanzés sauvages : 2 attaques sur des enfants en 2007, la 1re « grave, non mortelle », gravité de la 2e non décrite (McLennan & Hill 2012, J. Nat. Conserv.)",
  lieu="Bulindi, Hoima, Ouganda", annee=2007)  # corrigé : seule la 1re attaque est dite grave
# supprimé : 3 enfants tués par des chimpanzés dans l'ouest de l'Ouganda depuis 2014 (fox35orlando) — doublon avec
#   data_afrique.py (NatGeo 2018, ≥14 enfants tués dans l'ouest de l'Ouganda, 10 retenus) qui couvre la même période et zone.

# ---------------------------------------------------------------------------
# CHIEN vs HUMAIN
# ---------------------------------------------------------------------------
_NCRC = "https://nationalcanineresearchcouncil.com/wp-content/uploads/2015/09/Update-Dog-Bite-Related-Fatalities-In-The-United-States-2000-2015_0.pdf"
_n = ("NCRC, décès par morsure de chien aux USA 2000-2015 (466 cas ; 86,9 % sans adulte valide pour intervenir). "
      "Nombre de chiens non ventilé par âge ; tous âges : 1 chien 56,7 %, 2 : 21,2 %, 3 : 5,8 %, 4+ : 10,9 %, inconnu 5,4 % "
      "(moyenne ≈ 1,8 → effectif estimé 2)")
E("chien", 2, "humain", 1, "A", 3, count=131, qual="A", src=_NCRC,
  note=_n + " : victimes de 16-69 ans (n=131)" + _REG, lieu="États-Unis", annee=2008)
# corrigé : les 4 lignes 16-69 ans (74/28/8/14 par nb de chiens) étaient une ré-allocation non publiée → 1 ligne count=131, na=2 estimé
E("chien", 2, "humain", 1, "A", 3, tb=["vieux"], count=71, qual="A", src=_NCRC,
  note=_n + " : victimes de 70 ans et plus (n=71)" + _REG, lieu="États-Unis", annee=2008)
# corrigé : idem pour les 70+ (40/15/4/8, somme 67 ≠ 71) → 1 ligne count=71, na=2 estimé
E("chien", 6, "humain", 1, "A", 3, qual="B",
  src="https://www.kbtx.com/2023/07/31/man-mauled-death-by-pack-dogs-sheriff-says/",
  note="Demarcus McKenzie (27 ans) tué par une meute ; 2-3 chiens se joignent en cours d'attaque, 5-6 visibles sur vidéo ; il tente de fuir",
  lieu="Skipperville, Alabama", annee=2023)  # corrigé : note (5-6 au total, pas 5-6 + 2-3)
E("chien", 5, "humain", 1, "A", 3, qual="B",
  src="https://abc7chicago.com/dog-attack-postal-worker-killed-pamela-jane-rock/12162017/",
  note="Factrice de 61 ans tuée par 5 chiens après une panne de véhicule ; voisins et propriétaires arrachent les chiens (un voisin tire en l'air), elle meurt le lendemain",
  lieu="Putnam County, Floride", annee=2022)  # corrigé : intervention des voisins/coup de feu signalée
E("chien", 6, "humain", 1, "A", 3, tb=["jeune"], count=12, qual="B",
  src="https://www.cbsnews.com/news/india-feral-dogs-kill-children-in-attacks-around-sitapur",
  note="Chiens errants (gabarit ~15-25 kg, sous le proxy) : 12 enfants de 5-12 ans tués de nov. 2017 à mai 2018 ; ~6 chiens sur un cas, une meute tue 3 enfants le 1er mai (effectif estimé)" + _REG,
  lieu="Sitapur, Uttar Pradesh, Inde", annee=2018)  # corrigé : effectif estimé, gabarit, registre
E("humain", 1, "chien", 1, "A", 3, qual="B",
  src="https://worldwiderunning.com/truestories_runnerkillsdog.php",
  note="Joggeur (Joshua Harris) attaqué avec son fils par un croisé labrador/chow ; le saisit au cou, l'immobilise au sol jusqu'à la mort ; morsures au bras, doigt, nez",
  lieu="St. Lucie, Floride")  # vérifié
E("humain", 1, "chien", 1, "A", 3, qual="C",
  src="https://www.local10.com/news/local/2025/09/09/i-didnt-want-to-do-it-hollywood-man-explains-why-he-strangled-neighbors-pit-bull",
  note="Homme étrangle le pit-bull du voisin qu'il dit avoir vu attaquer son chien (moyen non précisé par la source accessible ; récit de l'auteur)",
  lieu="Hollywood, Floride", annee=2025)  # corrigé : « à mains nues » non confirmé, qual B→C
E("humain", 1, "chien", 1, "D", 1, qual="B",
  src="https://abc7chicago.com/dog-attack-pit-bull-rescue-bites-boy/992818",
  note="Ex-boxeur olympique (Danell Nicholson) arrache un pit-bull à un enfant de 8 ans, est mordu aux bras et jambes et le repousse (sort du chien non précisé)",
  lieu="Chicago", annee=2015)  # corrigé : A→D (chien repoussé, pas vaincu)
E("humain", 1, "chien", 2, "A", 1, ta=["outil"], qual="B",
  src="https://www.boston25news.com/news/local/caught-camera-stick-wielding-man-fights-off-dogs-after-boy-woman-attacked-north-shore-park/VCLPBPHTXRCJZPKNOVCQSMOZEU",
  note="Deux pit-bulls errants mordent un garçon de 5 ans et une femme de 22 ans, puis acculent Kyle Emerson dans son allée ; son père les chasse au bâton",
  lieu="Lynn, Massachusetts", annee=2025)  # corrigé : note (qui a été acculé, qui a combattu) ; chiens chassés → A m=1 conservé
E("humain", 2, "chien", 2, "D", 1, ta=["outil"], qual="B",
  src="https://saskatoon.ctvnews.ca/screaming-for-help-saskatoon-man-injured-saving-family-from-dog-attack-1.6670648",
  note="Deux pit-bulls : le père (mordu jambe et avant-bras) et un voisin armé d'un balai (mordu, se réfugie sur une voiture puis chez lui) protègent les enfants ; les chiens partent et sont retrouvés à un pâté de maisons",
  lieu="Saskatoon, Canada")  # corrigé : année non indiquée par la source (2022 retiré)

# ---------------------------------------------------------------------------
# CHIEN vs LOUP (registres de chiens tués : biais, les victoires des chiens ne sont pas recensées)
# ---------------------------------------------------------------------------
E("loup", 3, "chien", 1, "A", 3, count=41, qual="A",
  src="https://www.wpr.org/animals/record-number-hunting-dogs-killed-wolves-2016",
  note="WDNR : 41 chiens courants (chasse à l'ours et au coyote) tués par des loups en 2016 (record ; 23 en 2014) ; nombre de loups non publié (effectif estimé)" + _REG,
  lieu="Wisconsin", annee=2016)  # corrigé : effectif estimé + registre
E("loup", 3, "chien", 1, "A", 3, count=14, qual="A",
  src="https://dnr.wisconsin.gov/topic/WildlifeHabitat/wolf/dogdeps.html",
  note="WDNR tableau 2026 : 12 incidents (dont 1 daté 08/05/2025, probable coquille), 14 chiens courants tués (Plott, Bluetick, Walker, Redbone, Black and Tan ; ~20-35 kg ; 3 chiens de moins d'un an) ; nombre de loups non publié (effectif estimé)" + _REG,
  lieu="Wisconsin", annee=2026)  # corrigé : races/âges, effectif estimé, registre (tableau en ligne au 11/2026 : chiffres conformes)
E("loup", 3, "chien", 1, "A", 2, count=2, qual="A",
  src="https://dnr.wisconsin.gov/topic/WildlifeHabitat/wolf/dogdeps.html",
  note="WDNR tableau 2026 : 2 chiens courants blessés (Redbone/Bluetick 9-10 ans ; Plott 4 ans / Plott-Walker 9 mois — le blessé de chaque paire non précisé) (effectif estimé)",
  lieu="Wisconsin", annee=2026)  # corrigé : effectif estimé
E("loup", 3, "chien", 1, "A", 3, count=83, qual="A",
  src="https://escholarship.org/content/qt4vg5p9hs/qt4vg5p9hs.pdf?t=plu10i",
  note="Bangs et al. 2006 : 83 chiens confirmés tués par les loups 1987-2005 (surtout chiens de conduite/protection et chiens courants) ; « les meutes recherchent, attaquent et tuent les chiens de protection » (effectif estimé)" + _REG,
  lieu="Nord des Rocheuses (MT, ID, WY), USA", annee=1996)  # corrigé : effectif estimé + registre
E("loup", 3, "chien", 1, "A", 3, count=157, qual="B",
  src="https://predator-friendly-ranching.blogspot.com/2014/11/",
  note="Mertens & Schneider 2005 (Carnivore Damage Prevention News, non arbitré ; chiffres via un blog) : 157 chiens de protection adultes tués par les loups (jan. 2001-oct. 2002 ; + 2 chiots et 27 petits chiens de conduite non retenus) ; 48 % attachés au moment de l'attaque, 91 % de nuit ; 39 % des fermes touchées n'avaient qu'un chien, 33 % deux (effectif estimé)" + _REG,
  lieu="Carpates, Roumanie", annee=2002)  # corrigé : qual A→B (bulletin cité par un blog) ; « les loups préfèrent les fermes avec peu de chiens » non supporté → remplacé par la répartition réelle
E("loup", 2, "chien", 1, "A", 3, count=241, qual="A",
  src="https://cowboystatedaily.com/2023/01/01/cat-urbigkit-what-leads-to-wolf-attacks-on-dogs/",
  note="Kojola et al. 2022 (Wildl. Biol., doi:10.1002/wlb3.01038 ; chiffres via Cowboy State Daily) : 276 chiens tués par des loups en ~20 ans dans la zone d'étude finlandaise (est), surtout en chasse (chiens d'élan/spitz ~20-25 kg) ; 35 retirés pour recouvrement avec data_nord.py (Kojola & Kuittinen 1996-1999) → 241 (effectif estimé)" + _REG,
  lieu="Finlande orientale", annee=2010)  # corrigé : 276→241 (doublon partiel avec data_nord), source lisible, registre
E("loup", 2, "chien", 1, "A", 3, count=168, qual="A",
  src="https://cowboystatedaily.com/2023/01/01/cat-urbigkit-what-leads-to-wolf-attacks-on-dogs/",
  note="Kojola et al. 2022 : 168 chiens tués par des loups en Estonie (~20 ans), 90 % dans la cour des propriétaires (chiens de ferme souvent attachés, gabarit variable), surtout par des loups subadultes erratiques ou des paires (effectif estimé)" + _REG,
  lieu="Estonie", annee=2010)  # corrigé : tag jeune retiré côté loups (subadultes OU paires d'adultes, mélange) ; registre
E("loup", 4, "chien", 1, "A", 2, count=5, qual="B",
  src="https://cowboystatedaily.com/2023/01/01/cat-urbigkit-what-leads-to-wolf-attacks-on-dogs/",
  note="Meute de Dog Creek : 5 chiens de protection tués OU blessés (non distingués) en 2021, d'après le rapport annuel WGFD cité dans une chronique (effectif estimé)",
  lieu="Ouest du Wyoming", annee=2021)  # corrigé : m 3→2 (tués et blessés confondus), qual A→B (chronique citant le rapport)

# ---------------------------------------------------------------------------
# CHIEN vs COYOTE
# ---------------------------------------------------------------------------
E("chien", 1, "coyote", 1, "A", 1, ta=["captivite"], tb=["carcasse", "captivite"], count=84, qual="A",
  src="https://sanangelo.tamu.edu/files/2022/05/How-Komondor-Dogs-Reduce-Sheep-Losses-to-Coyotes.pdf",
  note="McGrew & Blakesley 1982 (J. Range Manage.) : 9 komondors, 2 coyotes mâles adultes lâchés (1 par enclos de 65 ha, 21 j) ; 141 interactions dont 84 où le chien interrompt une attaque sur les moutons et chasse le coyote ; aucun contact physique ni blessure rapporté (déplacement de proie, pas un combat) ; 37 des 89 moutons tués malgré tout",
  lieu="Utah, USA", annee=1981)  # corrigé : coyotes = 2 mâles en enclos (captivite) ; sans contact → tag carcasse (déplacement), m=1 conservé
# supprimé : chien Tuukka vs 3 coyotes, Cohasset 2024 (CBS) — aboiements et fuite des coyotes, aucun contact rapporté.
E("chien", 1, "coyote", 8, "A", 3, count=1, qual="C",
  src="https://news.yahoo.com/georgia-sheepdog-fights-kills-8-214125657.html",
  note="Grand chien de berger blanc Casper aurait tué 8 coyotes en plus d'une demi-heure de combat en défendant les moutons, revient gravement blessé (récit du propriétaire seulement, sans confirmation)",
  lieu="Géorgie, USA")  # vérifié

# ---------------------------------------------------------------------------
# CHIEN vs GRANDS PRÉDATEURS (léopard, puma, ours, guépard, babouin)
# ---------------------------------------------------------------------------
E("chien", 3, "leopard", 1, "A", 1, qual="C",
  src="https://dnaindia.com/viral/report-watch-brave-dogs-defend-home-chase-away-leopard-in-nainital-cctv-footage-goes-viral-3100044/amp",
  note="Trois chiens (un, puis deux de plus) aboient et chassent un léopard ; le propriétaire dit que le léopard avait attaqué les chiens puis lui-même, la vidéo ne montre pas de contact clair",
  lieu="Nainital, Inde", annee=2024)  # corrigé : m 2→1, qual B→C (contact non établi par la vidéo)
E("chien", 4, "leopard", 1, "A", 1, tb=["embuscade"], qual="B",
  src="https://www.freepressjournal.in/viral/uttarakhand-news-leopard-pounces-on-street-dog-in-haridwar-at-night-cctv-captures-how-pack-saves-it-from-deadly-attack",
  note="Léopard saisit au cou un chien errant endormi ; « plusieurs » chiens errants (gabarit sous le proxy) l'attaquent et le chassent (effectif estimé)",
  lieu="Haridwar, Inde", annee=2025)  # corrigé : effectif estimé, gabarit
E("chien", 1, "leopard", 1, "A", 1, tb=["embuscade"], qual="B",
  src="https://www.freepressjournal.in/amp/pune/pune-dog-fights-off-leopard-in-khed-taluka-cctv-footage-goes-viral",
  note="Léopard bondit sur un chien de rue (probablement < 30 kg) dans une ruelle ; le chien se défend et le chasse",
  lieu="Khed, Pune, Inde", annee=2025)  # vérifié
E("chien", 1, "puma", 1, "D", 1, qual="B",
  src="https://www.reddeeradvocate.com/national-news/family-dog-saves-b-c-boy-11-from-cougar-attack/",
  note="Chienne retriever Angel (18 mois) s'interpose entre un puma et Austin Forman (11 ans) et se bat jusqu'à ce qu'un policier abatte le puma (combat interrompu par balle) ; chienne blessée, survit",
  lieu="Boston Bar, Colombie-Britannique", annee=2010)  # vérifié
E("puma", 1, "chien", 1, "A", 3, tb=["jeune"], qual="C",
  src="https://sanangelo.tamu.edu/files/2022/05/Effectiveness-of-LGDs-for-Ruducing-Predation-on-Domestic-Sheep-Andelt-1992.pdf",
  note="Andelt 1992 (Wildl. Soc. Bull.) : un chien de protection (<1 an) « que l'on pense » tué par un puma (déclaration téléphonique d'éleveur, non observé)",
  lieu="Ouest des USA", annee=1990)  # corrigé : chien de moins d'un an → jeune ; qual B→C (attribution non vérifiée)
E("ours_noir", 1, "chien", 1, "A", 3, qual="B",
  src="https://cottagelife.com/news/dog-dead-after-saving-owner-from-bear-attack",
  note="Ours noir adulte attaque Trevor Miller (42 ans) ; son schnauzer (petit chien, hors gabarit du proxy) le détourne et meurt ; l'homme s'échappe blessé",
  lieu="Sandbar Lake PP, Ontario", annee=2013)  # vérifié
E("chien", 1, "ours_noir", 1, "D", 1, tb=["defense_petits"], qual="B",
  src="https://abc7ny.com/post/hero-dog-saves-man-from-bear-attack/281404/",
  note="Ourse (~110 kg) avec 2 oursons renverse et mord Steve Kirchbaum ; son croisé labrador Henry l'attaque, l'homme la frappe à la tête avec une pierre ; l'ourse cesse (combat mixte chien + humain)",
  lieu="Virginie-Occidentale", annee=2014)  # vérifié (note : intervention humaine mixte)
E("chien", 1, "guepard", 1, "A", 3, qual="A",
  src="https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/607619E840644481488447558D32279B/S0030605315000113a.pdf/more-bark-than-bite-the-role-of-livestock-guarding-dogs-in-predator-control-on-namibian-farmlands.pdf",
  note="Potgieter et al. 2016 (Oryx) : sur 83 chiens de protection (surtout bergers anatoliens), 1 a tué un guépard entré de nuit dans l'enclos ; aucun léopard tué ; aucun chien tué par un prédateur rapporté" + " (registre : seuls les succès des chiens sont recensés)",
  lieu="Namibie", annee=2012)  # vérifié (mention registre ajoutée)
E("chien", 1, "babouin", 1, "A", 3, count=8, qual="A",
  src="https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/607619E840644481488447558D32279B/S0030605315000113a.pdf/more-bark-than-bite-the-role-of-livestock-guarding-dogs-in-predator-control-on-namibian-farmlands.pdf",
  note="Potgieter et al. 2016 (Oryx) : 8 des 83 chiens de protection (surtout bergers anatoliens) ont tué au moins un babouin chacma, de jour hors enclos (effectif estimé ; registre : seuls les succès des chiens sont recensés)",
  lieu="Namibie", annee=2012)  # ajouté

# ---------------------------------------------------------------------------
# KANGOUROU vs HUMAIN  (id kangourou = roux ; espèce réelle indiquée quand connue)
# ---------------------------------------------------------------------------
E("kangourou", 1, "humain", 1, "A", 3, ta=["captivite"], tb=["vieux"], qual="B",
  src="https://www.cbsnews.com/news/kangaroo-kills-man-rare-fatal-attack-australia/?ftag=CNM-00-10aab4i",
  note="Peter Eades (77 ans) tué par un kangourou sauvage qu'il gardait apparemment comme animal de compagnie (espèce non précisée, prob. kangourou gris de l'Ouest — proxy roux) ; l'animal bloque les secours, abattu",
  lieu="Redmond, Australie-Occidentale", annee=2022)  # corrigé : « mâle adulte » non dit par la source ; proxy d'espèce signalé
E("kangourou", 1, "humain", 1, "A", 3, qual="B",
  src="https://www.cbsnews.com/news/kangaroo-kills-man-rare-fatal-attack-australia/?ftag=CNM-00-10aab4i",
  note="William Cruickshank (38 ans) attaqué par un grand kangourou (espèce non précisée) en voulant sauver ses deux chiens ; blessures à la tête, mâchoire brisée, meurt à l'hôpital des mois plus tard",
  lieu="Hillston, Nouvelle-Galles du Sud", annee=1936)  # vérifié
E("humain", 3, "kangourou", 1, "D", 1, ta=["outil"], qual="B",
  src="https://www.omanobserver.om/ampArticle/45866",
  note="Grand mâle (≥1,80 m, espèce non précisée) attaque Jim Smith qui le nourrissait ; sa femme Linda (64 ans) intervient au balai puis au bâton (poumon perforé, côtes cassées), le fils (40 ans) le frappe à la pelle ; le kangourou repart dans le bush ; les trois blessés",
  lieu="Darling Downs, Queensland", annee=2018)  # corrigé : A→D (l'animal repart après avoir blessé les 3) ; déroulé (balai/bâton puis pelle)
E("kangourou", 1, "humain", 2, "A", 1, qual="A",
  src="https://www.mja.com.au/journal/2001/175/11/kangaroo-capers",
  note="Med J Aust 2001 (urgentiste, Canberra) : un kangourou gris (proxy roux) qui se battait avec un chien blesse un homme de 32 ans (abrasions profondes, morsure à l'avant-bras) puis un homme de 50 ans qui le tirait par la queue (projeté au sol) ; repart indemne",
  lieu="Région de Canberra (ACT), lieu exact non précisé", annee=2001)  # corrigé : âges, proxy d'espèce, lieu
E("humain", 2, "kangourou", 1, "D", 1, ta=["outil"], qual="B",
  src="https://www.yahoo.com/news/articles/retired-farmer-lucky-alive-being-112607433.html",
  note="Retraité « Col » frappe le kangourou au bâton, celui-ci revient de la mare et l'attaque (plaies abdominales de 7 cm, griffures, tête) ; un ami le frappe à la pelle, il lâche et retourne dans la mare (espèce non précisée)",
  lieu="Victoria, Australie", annee=2026)  # corrigé : A→D (l'animal lâche et se retire, pas vaincu)
E("kangourou", 1, "humain", 1, "A", 2, ta=["defense_petits"], qual="B",
  src="https://abcnews4.com/news/nation-world/kangaroo-breaks-womans-leg-others-attacked-macroom-australia-attacks-injured-department-of-environment-and-science-wallabies-marsupials",
  note="Femelle avec petit au pied fracture le fémur d'une femme (+ griffures, morsures) ; 7 attaques signalées en un an, toutes par des femelles suitées (espèce non précisée, prob. kangourou gris — proxy roux)",
  lieu="Macroom, Queensland", annee=2022)  # corrigé : proxy d'espèce ; « femelle » dans la note
E("humain", 1, "kangourou", 1, "D", 1, qual="B",
  src="https://www.nationalgeographic.com/animals/article/man-punches-kangaroo-saves-dog-australia",
  note="Greig Tonkins frappe au visage un grand mâle (~1,80 m, ~77 kg, 9-15 ans ; espèce non précisée) qui tenait son chien en clé ; le kangourou lâche, puis repart indemne dans le bush",
  lieu="Nouvelle-Galles du Sud", annee=2016)  # corrigé : A→D (animal indemne qui se retire)
E("humain", 1, "kangourou", 1, "D", 1, qual="B",
  src="https://www.heraldnet.com/news/kangaroo-tries-to-drown-dog-attacks-owner",
  note="Chris Rickard libère son chien ; le kangourou (~1,50 m, mâle d'après le récit, espèce non précisée) lui lacère ventre et visage ; un coup de coude à la gorge met fin à l'attaque",
  lieu="Arthurs Creek, Victoria", annee=2009)  # corrigé : A→D (l'attaque cesse, l'animal n'est pas vaincu) ; âge non donné par la source
E("humain", 1, "kangourou", 1, "D", 1, qual="B",
  src="https://www.livescience.com/animals/land-mammals/kangaroos-might-try-to-drown-your-dog-heres-why",
  note="Mick Moloney entre dans la rivière, frappe le kangourou gris de l'Est (proxy roux) qui tient son chien ; le kangourou riposte ; homme et chien regagnent la rive",
  lieu="Murray River, Victoria", annee=2023)  # corrigé : espèce (gris de l'Est) signalée

# ---------------------------------------------------------------------------
# KANGOUROU vs CHIEN / DINGO  (le dingo est codé « chien » : ~15 kg, sous le gabarit du proxy)
# ---------------------------------------------------------------------------
E("kangourou", 1, "chien", 1, "A", 2, qual="B",
  src="https://www.heraldnet.com/news/kangaroo-tries-to-drown-dog-attacks-owner",
  note="Kangourou (~1,50 m) poursuivi dans une mare maintient sous l'eau le bouvier australien Rocky ; chien « à moitié noyé », sauvé par son maître (dans l'eau, tactique défensive du kangourou)",
  lieu="Arthurs Creek, Victoria", annee=2009)  # corrigé : tag eau retiré (l'eau n'est pas le milieu du kangourou ; mentionné dans la note)
E("kangourou", 1, "chien", 1, "A", 1, qual="B",
  src="https://www.livescience.com/animals/land-mammals/kangaroos-might-try-to-drown-your-dog-heres-why",
  note="Kangourou gris de l'Est (proxy roux), dans l'eau à la taille, immobilise le chien Hutchy jusqu'à l'intervention du maître (tactique défensive dans l'eau)",
  lieu="Murray River, Victoria", annee=2023)  # corrigé : tag eau retiré, espèce signalée
E("kangourou", 1, "chien", 1, "A", 1, qual="B",
  src="https://www.nationalgeographic.com/animals/article/man-punches-kangaroo-saves-dog-australia",
  note="Grand mâle (~77 kg) tient le chien de chasse au cochon en clé avant l'intervention du maître",
  lieu="Nouvelle-Galles du Sud", annee=2016)  # vérifié
E("kangourou", 1, "chien", 1, "A", 1, qual="A",
  src="https://www.mja.com.au/journal/2001/175/11/kangaroo-capers",
  note="Med J Aust 2001 : un kangourou gris (proxy roux) se bat avec un chien qui s'échappe, avant de blesser deux hommes",
  lieu="Région de Canberra (ACT)", annee=2001)  # ajouté
E("chien", 2, "kangourou", 1, "A", 3, qual="B",
  src="https://www.goulburnpost.com.au/story/5490344/dogs-attacking-kangaroo-a-warning-to-dog-ownerslandholders-video-pictures/",
  note="Deux chiens attaquent un kangourou (espèce/sexe non précisés) près d'une mare ; le propriétaire chasse les chiens ; le kangourou, debout ensuite, est retrouvé mort de ses blessures le lendemain ; résistance non décrite",
  lieu="Gundary, près de Goulburn, NSW", annee=2018)  # corrigé : note (intervention humaine, résistance non décrite)
E("chien", 1, "kangourou", 1, "D", 1, qual="A",
  src="https://www.publish.csiro.au/wr/WR9930845",
  note="Wright 1993 (Wildl. Res.) : un grand mâle de kangourou gris de l'Est (proxy roux) tient tête à un dingo (codé chien) pendant >60 min (6 phases à <5 m, coups de pied, de queue, posture haute) ; le dingo finit par partir",
  lieu="Wallaby Creek, NSW")  # corrigé : A→D (l'attaquant renonce, le kangourou n'est pas vainqueur) ; année d'observation non donnée (1990 retiré) ; proxys signalés
E("chien", 5, "kangourou", 1, "A", 3, count=3, qual="A",
  src="https://publish.csiro.au/WR/WR9810255",
  note="Shepherd 1981 (Aust. Wildl. Res.) : une meute de 5 dingos (codés chien) tue 83 kangourous roux en 7 semaines près d'un point d'eau, dont seulement 3 non juvéniles (les 80 juvéniles exclus : proies qui fuient) ; résistance non décrite dans le résumé",
  lieu="Nord-ouest de la Nouvelle-Galles du Sud", annee=1980)  # vérifié (proxy dingo et absence de description de résistance signalés)
