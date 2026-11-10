"""Real Odds — animaux : rencontres documentées, cluster MER / HUMAINS / CHIENS / KANGOUROUS.

Convention : `a` = vainqueur quand res="A" ; res="D" = issue nulle après contact réel.
na/nb = individus réellement engagés. m : 1 serré, 2 net, 3 mort/tué.
Remarques générales :
- « chien » sert aussi de proxy pour le dingo (lignes marquées « dingo » dans la note).
- Les attaques de kangourous sur des humains concernent surtout le kangourou gris (M. giganteus), pas le roux.
- Les statistiques chien>humain et loup>chien sont des registres de victimes (pas de dénominateur des
  rencontres où l'humain/le chien l'a emporté) : biais fort en faveur de l'attaquant, à pondérer.
"""

ENC = []


def E(a, na, b, nb, res, m=2, ta=(), tb=(), count=1, qual="B", src="", note="", lieu="", annee=None):
    ENC.append(dict(a=a, na=na, b=b, nb=nb, res=res, m=m, ta=list(ta), tb=list(tb), count=count, qual=qual,
                    src=src, note=note, lieu=lieu, annee=annee))


# ---------------------------------------------------------------------------
# ORQUE vs REQUIN BLANC
# ---------------------------------------------------------------------------
E("orque", 2, "requin_blanc", 1, "A", 3, tb=["jeune"], qual="A",
  src="https://www.nwf.org/en/Magazines/National-Wildlife/2004/Showdown-at-Sea",
  note="Deux orques (CA2 et CA6, pod L.A.) tuent un requin blanc subadulte de ~3 m et mangent le foie ; les requins désertent les Farallon ensuite (obs. P. Pyle)",
  lieu="Îles Farallon, Californie", annee=1997)
E("orque", 2, "requin_blanc", 1, "A", 3, count=8, qual="A",
  src="https://www.tandfonline.com/doi/abs/10.2989/1814232X.2022.2066723",
  note="Port et Starboard (2 mâles) liés à 8 carcasses de requins blancs éviscérés (foie retiré) échouées depuis 2017 (Towner et al. 2022, Afr. J. Mar. Sci.)",
  lieu="Gansbaai, Afrique du Sud", annee=2017)
E("orque", 5, "requin_blanc", 1, "A", 3, count=1, qual="A",
  src="https://phys.org/news/2022-10-proof-orcas-white-sharks.amp",
  note="Groupe de 5 orques filmé (hélico/drone) tuant un requin blanc ; Towner et al. 2022 Ecology doi:10.1002/ecy.3875",
  lieu="Mossel Bay, Afrique du Sud", annee=2022)
E("orque", 5, "requin_blanc", 1, "A", 3, count=3, qual="B",
  src="https://phys.org/news/2022-10-proof-orcas-white-sharks.amp",
  note="Même chasse d'une heure : 3 autres requins blancs probablement tués (non filmés en entier)",
  lieu="Mossel Bay, Afrique du Sud", annee=2022)
E("orque", 1, "requin_blanc", 1, "A", 3, tb=["jeune"], qual="A",
  src="https://www.scientificamerican.com/article/lone-orca-killed-great-white-shark-in-first-documented-case/",
  note="Starboard seul tue un requin blanc juvénile de 2,5 m en moins de 2 min et mange son foie (1er cas 1 contre 1 documenté)",
  lieu="Mossel Bay, Afrique du Sud", annee=2023)
E("orque", 1, "requin_blanc", 1, "A", 3, qual="B",
  src="https://www.scientificamerican.com/article/lone-orca-killed-great-white-shark-in-first-documented-case/",
  note="Requin blanc de 3,55 m échoué le lendemain sans foie, attribué probablement à une attaque antérieure non observée (nb d'orques inconnu, 1-2)",
  lieu="Mossel Bay, Afrique du Sud", annee=2023)
E("orque", 5, "requin_blanc", 1, "A", 3, tb=["jeune"], count=2, qual="A",
  src="https://www.frontiersin.org/news/2025/11/03/orcas-killing-young-great-white-sharks-by-flipping-upside-down-frontiers-marine-science",
  note="Pod de Moctezuma (5 orques) retourne et tue 2 requins blancs juvéniles, foie consommé (Higuera Rivas et al. 2025, Front. Mar. Sci.)",
  lieu="Golfe de Californie, Mexique", annee=2020)
E("orque", 5, "requin_blanc", 1, "A", 3, tb=["jeune"], count=1, qual="A",
  src="https://www.frontiersin.org/news/2025/11/03/orcas-killing-young-great-white-sharks-by-flipping-upside-down-frontiers-marine-science",
  note="Même pod (5 orques) tue un 3e requin blanc juvénile",
  lieu="Golfe de Californie, Mexique", annee=2022)
E("orque", 7, "requin_blanc", 1, "A", 3, qual="B",
  src="https://www.livescience.com/animals/sharks/great-white-shark-ripped-in-2-was-loaded-with-orca-dna-scientists-say",
  note="Requin blanc de ~4,9 m retrouvé coupé en deux, ADN d'orque sur les plaies ; ~7 orques vues à proximité quelques jours avant",
  lieu="Portland, Victoria, Australie", annee=2023)

# ---------------------------------------------------------------------------
# ORQUE vs MORSE (très peu documenté)
# ---------------------------------------------------------------------------
E("orque", 6, "morse", 1, "A", 3, qual="A",
  src="https://repository.library.noaa.gov/view/noaa/27306/noaa_27306_DS1.pdf",
  note="Kryukova et al. 2012 (Biology Bulletin 39:768) : 9 orques (6 adultes actifs + 2 petits) attaquent un groupe de morses près d'une échouerie, isolent un individu, 55 attaques en 17 min ; les orques repartent avec le morse (issue tirée du résumé)",
  lieu="Flèche de Retkyn, Tchoukotka", annee=2008)

# ---------------------------------------------------------------------------
# REQUIN BLANC vs HUMAIN
# ---------------------------------------------------------------------------
E("requin_blanc", 1, "humain", 1, "A", 3, ta=["embuscade"], count=59, qual="A",
  src="https://www.floridamuseum.ufl.edu/shark-attacks/factors/species-implicated/",
  note="ISAF (1580-2022) : 59 attaques non provoquées mortelles attribuées au requin blanc",
  lieu="Monde")
E("requin_blanc", 1, "humain", 1, "D", 1, count=292, qual="A",
  src="https://www.floridamuseum.ufl.edu/shark-attacks/factors/species-implicated/",
  note="ISAF : 292 attaques non mortelles ; le requin lâche souvent après une morsure (morsure exploratoire / riposte) ; issue ambiguë, à sous-pondérer",
  lieu="Monde")
E("humain", 2, "requin_blanc", 1, "A", 1, qual="B",
  src="https://www.foxnews.com/world/australian-man-punches-10-foot-shark-after-wife-attacked-while-surfing",
  note="Chantelle Doyle mordue à la jambe par un requin blanc de ~3 m ; son mari arrive en planche et le frappe à coups de poing jusqu'à ce qu'il lâche ; blessures graves mais survit",
  lieu="Shelly Beach, Port Macquarie, Australie", annee=2020)
E("humain", 1, "requin_blanc", 1, "A", 1, qual="B",
  src="https://au.sports.yahoo.com/shark-attack-new-zealand-surfer-nick-minogue-punches-great-white-survives-incident-000825715.html",
  note="Nick Minogue (60 ans) mordu au bras ; frappe le requin blanc dans l'œil, celui-ci lâche ; blessure légère",
  lieu="Pauanui, Nouvelle-Zélande")
E("humain", 1, "requin_blanc", 1, "A", 1, qual="B",
  src="https://www.washingtontimes.com/news/2008/may/13/poke-in-shark-eye-saves-swimmer-in-australia/",
  note="Jason Cull saisi à la jambe par un requin (prob. blanc, ~5 m) ; coups de poing puis doigt dans l'œil, le requin lâche ; mollet en grande partie arraché",
  lieu="Middleton Beach, Albany, Australie", annee=2008)
E("humain", 1, "requin_blanc", 1, "A", 1, ta=["outil"], qual="B",
  src="https://gulfnews.com/world/oceania/diver-saved-his-life-by-poking-shark-in-the-eye-1.156535",
  note="Eric Nerhus, plongeur, tête et épaules dans la gueule d'un requin de ~3 m ; doigts dans l'orbite puis coup de burin à ormeaux dans l'œil, s'échappe (gilet plombé l'a protégé)",
  lieu="Cape Howe, Eden, Australie", annee=2007)
E("humain", 1, "requin_blanc", 1, "A", 1, qual="B",
  src="https://www.illawarramercury.com.au/story/8996843/how-shark-cage-diving-pioneer-rodney-fox-survived-a-shark-attack/",
  note="Rodney Fox, chasseur sous-marin : yeux arrachés au requin, étreinte ; le requin part sur le flotteur ; 462 points de suture, survit de justesse",
  lieu="Aldinga Beach, Australie du Sud", annee=1963)
E("humain", 1, "requin_blanc", 1, "D", 1, qual="B",
  src="https://newsinfo.inquirer.net/?p=706629",
  note="Mick Fanning renversé par un requin (prob. blanc, non confirmé), le frappe ; leash coupé, indemne ; l'expert parle d'investigation plutôt que de prédation",
  lieu="Jeffreys Bay, Afrique du Sud", annee=2015)

# ---------------------------------------------------------------------------
# ORQUE / GORILLE vs HUMAIN (sauvages — quasi inexistant)
# ---------------------------------------------------------------------------
E("orque", 1, "humain", 1, "A", 2, qual="C",
  src="https://en.wikipedia.org/wiki/Orca_attacks",
  note="Seule morsure d'orque sauvage bien rapportée : surfeur Hans Kretschmer mordu (100 points), probable confusion avec un otarie ; l'orque repart",
  lieu="Point Sur, Californie", annee=1972)
E("gorille", 1, "humain", 4, "A", 3, tb=["jeune"], qual="C",
  src="https://www.camer.be/64351/11:1/cameroun-un-gorille-bastonne-un-enfant-a-mort-cameroon.html",
  note="Un gorille sort de la brousse, frappe mortellement un garçon de 14 ans puis malmène le père, le frère de 9 ans et la mère avant de repartir (presse locale)",
  lieu="Nguen, Haute-Sanaga, Cameroun", annee=2017)
E("gorille", 1, "humain", 1, "A", 3, qual="C",
  src="https://www.camer.be/actualites/societe/cameroun-tuac-par-un-gorille-cameroon.html",
  note="Homme d'une trentaine d'années traîné en forêt et tué par un gorille (témoin unique) ; même village : attaques mortelles signalées en 2012 et 2015",
  lieu="Birpondo, près de Bertoua, Cameroun", annee=2018)

# ---------------------------------------------------------------------------
# CHIMPANZÉ vs HUMAIN
# ---------------------------------------------------------------------------
E("chimpanze", 1, "humain", 2, "A", 2, ta=["captivite"], tb=["arme_blanche"], qual="A",
  src="https://en.wikipedia.org/wiki/Travis_(chimpanzee)",
  note="Travis (~90 kg, animal de compagnie) défigure Charla Nash ; la propriétaire le frappe à la pelle et le poignarde sans l'arrêter ; la police l'abat",
  lieu="Stamford, Connecticut", annee=2009)
E("chimpanze", 2, "humain", 2, "A", 2, ta=["captivite"], qual="A",
  src="https://en.wikipedia.org/wiki/St._James_Davis_chimpanzee_attack",
  note="Deux mâles évadés (Buddy, Ollie) mutilent St. James Davis (doigts, nez, pied, etc.) et blessent sa femme ; abattus par balle",
  lieu="Animal Haven Ranch, Californie", annee=2005)
E("chimpanze", 2, "humain", 1, "A", 2, ta=["captivite"], qual="B",
  src="https://www.bangordailynews.com/2012/06/29/news/chimps-attack-american-at-south-africa-sanctuary/",
  note="Andrew Oberle traîné sous la clôture et mutilé par deux chimpanzés mâles du sanctuaire ; survit",
  lieu="Chimp Eden, Mpumalanga, Afrique du Sud", annee=2012)
E("chimpanze", 2, "humain", 2, "A", 2, ta=["captivite"], qual="B",
  src="https://www.animallaw.info/article/incidents-attacks-involving-captive-chimpanzees",
  note="Deux chimpanzés attaquent deux soigneurs, l'un grièvement blessé ; abattus",
  lieu="Hogle Zoo, Salt Lake City", annee=1999)
E("chimpanze", 3, "humain", 4, "A", 3, ta=["captivite"], qual="B",
  src="https://newspaper.animalpeopleforum.org/2006/05/01/1st-chimp-at-tacugama-kills-man-leads-escape/",
  note="Évasion de 31 chimpanzés menée par Bruno ; le chauffeur Issa Kanu tué, 3 passagers blessés (nb exact d'attaquants inconnu, ~3 estimé)",
  lieu="Tacugama, Sierra Leone", annee=2006)
E("chimpanze", 1, "humain", 1, "A", 2, tb=["jeune"], count=2, qual="A",
  src="https://radar.brookes.ac.uk/radar/file/22474f93-1df8-a60c-8d8f-a4cb4548bff9/1/mclennan2012troublesome.pdf",
  note="Chimpanzés sauvages : 2 attaques graves sur des enfants en 2007 (McLennan & Hill 2012, J. Nat. Conserv.)",
  lieu="Bulindi, Hoima, Ouganda", annee=2007)
E("chimpanze", 1, "humain", 1, "A", 3, tb=["jeune"], count=3, qual="B",
  src="https://www.fox35orlando.com/news/chimps-are-killing-people-in-uganda-it-broke-off-the-arm-opened-the-stomach-and-removed-the-kidneys",
  note="Chimpanzés sauvages : 3 enfants tués (et ~6 blessés) depuis 2014 dans une zone de forêt fragmentée",
  lieu="Muhororo, ouest de l'Ouganda", annee=2014)

# ---------------------------------------------------------------------------
# CHIEN vs HUMAIN
# ---------------------------------------------------------------------------
_NCRC = "https://nationalcanineresearchcouncil.com/wp-content/uploads/2015/09/Update-Dog-Bite-Related-Fatalities-In-The-United-States-2000-2015_0.pdf"
_n = "NCRC, décès par morsure de chien aux USA 2000-2015 (466 cas, 86,9 % sans adulte valide pour intervenir) ; victimes 16-69 ans (n=131) réparties selon la distribution globale du nombre de chiens (approximation)"
E("chien", 1, "humain", 1, "A", 3, count=74, qual="A", src=_NCRC, note=_n + " : 1 chien", lieu="États-Unis", annee=2008)
E("chien", 2, "humain", 1, "A", 3, count=28, qual="A", src=_NCRC, note=_n + " : 2 chiens", lieu="États-Unis", annee=2008)
E("chien", 3, "humain", 1, "A", 3, count=8, qual="A", src=_NCRC, note=_n + " : 3 chiens", lieu="États-Unis", annee=2008)
E("chien", 5, "humain", 1, "A", 3, count=14, qual="A", src=_NCRC, note=_n + " : 4 chiens ou plus", lieu="États-Unis", annee=2008)
_n2 = "NCRC 2000-2015 : victimes de 70 ans et plus (n=71), réparties selon la distribution globale du nombre de chiens"
E("chien", 1, "humain", 1, "A", 3, tb=["vieux"], count=40, qual="A", src=_NCRC, note=_n2 + " : 1 chien", lieu="États-Unis", annee=2008)
E("chien", 2, "humain", 1, "A", 3, tb=["vieux"], count=15, qual="A", src=_NCRC, note=_n2 + " : 2 chiens", lieu="États-Unis", annee=2008)
E("chien", 3, "humain", 1, "A", 3, tb=["vieux"], count=4, qual="A", src=_NCRC, note=_n2 + " : 3 chiens", lieu="États-Unis", annee=2008)
E("chien", 5, "humain", 1, "A", 3, tb=["vieux"], count=8, qual="A", src=_NCRC, note=_n2 + " : 4+ chiens", lieu="États-Unis", annee=2008)
E("chien", 6, "humain", 1, "A", 3, qual="B",
  src="https://www.kbtx.com/2023/07/31/man-mauled-death-by-pack-dogs-sheriff-says/",
  note="Homme de 27 ans tué par une meute (5-6 chiens visibles sur vidéo, 2-3 de plus au début)",
  lieu="Skipperville, Alabama", annee=2023)
E("chien", 5, "humain", 1, "A", 3, qual="B",
  src="https://abc7chicago.com/dog-attack-postal-worker-killed-pamela-jane-rock/12162017/",
  note="Factrice de 61 ans tuée par 5 chiens après une panne de véhicule",
  lieu="Putnam County, Floride", annee=2022)
E("chien", 6, "humain", 1, "A", 3, tb=["jeune"], count=12, qual="B",
  src="https://www.cbsnews.com/news/india-feral-dogs-kill-children-in-attacks-around-sitapur",
  note="Meutes de chiens errants : 12 enfants de 5-12 ans tués en 6 mois (meute ~6 chiens)",
  lieu="Sitapur, Uttar Pradesh, Inde", annee=2018)
E("humain", 1, "chien", 1, "A", 3, qual="B",
  src="https://worldwiderunning.com/truestories_runnerkillsdog.php",
  note="Joggeur (Joshua Harris) attaqué par un croisé labrador/chow ; le saisit au cou et l'immobilise jusqu'à la mort ; quelques morsures",
  lieu="St. Lucie, Floride")
E("humain", 1, "chien", 1, "A", 3, qual="B",
  src="https://www.local10.com/news/local/2025/09/09/i-didnt-want-to-do-it-hollywood-man-explains-why-he-strangled-neighbors-pit-bull",
  note="Homme étrangle à mains nues le pit-bull du voisin qui attaquait son chien",
  lieu="Hollywood, Floride", annee=2025)
E("humain", 1, "chien", 1, "A", 1, qual="B",
  src="https://abc7chicago.com/dog-attack-pit-bull-rescue-bites-boy/992818",
  note="Ex-boxeur olympique (Danell Nicholson) arrache un pit-bull à un enfant, est mordu aux bras et jambes mais maîtrise le chien",
  lieu="Chicago", annee=2015)
E("humain", 1, "chien", 2, "A", 1, ta=["outil"], qual="B",
  src="https://www.boston25news.com/news/local/caught-camera-stick-wielding-man-fights-off-dogs-after-boy-woman-attacked-north-shore-park/VCLPBPHTXRCJZPKNOVCQSMOZEU",
  note="Deux pit-bulls errants blessent un enfant et une femme ; un homme les repousse avec un bâton",
  lieu="Lynn, Massachusetts", annee=2025)
E("humain", 2, "chien", 2, "D", 1, ta=["outil"], qual="B",
  src="https://saskatoon.ctvnews.ca/screaming-for-help-saskatoon-man-injured-saving-family-from-dog-attack-1.6670648",
  note="Deux pit-bulls : le père (renversé, mordu) et un voisin armé d'un balai (mordu) protègent les enfants ; les chiens finissent par partir",
  lieu="Saskatoon, Canada", annee=2022)

# ---------------------------------------------------------------------------
# CHIEN vs LOUP (registres de chiens tués : biais, les victoires des chiens ne sont pas recensées)
# ---------------------------------------------------------------------------
E("loup", 3, "chien", 1, "A", 3, count=41, qual="A",
  src="https://www.wpr.org/animals/record-number-hunting-dogs-killed-wolves-2016",
  note="WDNR : 41 chiens de chasse (chiens courants à ours/coyote) tués par des loups en 2016 (record) ; taille de meute estimée",
  lieu="Wisconsin", annee=2016)
E("loup", 3, "chien", 1, "A", 3, count=14, qual="A",
  src="https://dnr.wisconsin.gov/topic/WildlifeHabitat/wolf/dogdeps.html",
  note="WDNR tableau 2026 : 12 incidents, 14 chiens courants tués",
  lieu="Wisconsin", annee=2026)
E("loup", 3, "chien", 1, "A", 2, count=2, qual="A",
  src="https://dnr.wisconsin.gov/topic/WildlifeHabitat/wolf/dogdeps.html",
  note="WDNR tableau 2026 : 2 chiens courants blessés",
  lieu="Wisconsin", annee=2026)
E("loup", 3, "chien", 1, "A", 3, count=83, qual="A",
  src="https://escholarship.org/content/qt4vg5p9hs/qt4vg5p9hs.pdf?t=plu10i",
  note="Bangs et al. 2006 : 83 chiens (surtout chiens de berger/protection et chiens courants) tués par les loups 1987-2005 ; « les meutes recherchent et tuent les chiens de protection »",
  lieu="Nord des Rocheuses, USA", annee=1996)
E("loup", 3, "chien", 1, "A", 3, count=157, qual="A",
  src="https://predator-friendly-ranching.blogspot.com/2014/11/",
  note="Mertens & Schneider 2005 (CDPNews) : 157 chiens de protection adultes tués par les loups en 22 mois (48 % attachés, 91 % la nuit) ; loups préfèrent les fermes avec peu de chiens",
  lieu="Carpates, Roumanie", annee=2002)
E("loup", 2, "chien", 1, "A", 3, count=276, qual="A",
  src="https://openpolar.no/Record/crwiley:10.1002%2Fwlb3.01038/Description",
  note="Wildlife Biology (~20 ans de données) : 276 chiens tués par des loups en Finlande orientale, surtout pendant la chasse",
  lieu="Finlande orientale", annee=2010)
E("loup", 2, "chien", 1, "A", 3, ta=["jeune"], count=168, qual="A",
  src="https://openpolar.no/Record/crwiley:10.1002%2Fwlb3.01038/Description",
  note="Même étude : 168 chiens tués en Estonie, 90 % dans la cour des propriétaires, surtout par des loups subadultes erratiques ou des paires",
  lieu="Estonie", annee=2010)
E("loup", 4, "chien", 1, "A", 3, count=5, qual="A",
  src="https://cowboystatedaily.com/2023/01/01/cat-urbigkit-what-leads-to-wolf-attacks-on-dogs/",
  note="Meute de Dog Creek : 5 chiens de protection tués ou blessés (rapport annuel WGFD)",
  lieu="Ouest du Wyoming", annee=2021)

# ---------------------------------------------------------------------------
# CHIEN vs COYOTE
# ---------------------------------------------------------------------------
E("chien", 1, "coyote", 1, "A", 1, count=84, qual="A",
  src="https://sanangelo.tamu.edu/files/2022/05/How-Komondor-Dogs-Reduce-Sheep-Losses-to-Coyotes.pdf",
  note="McGrew & Blakesley 1982 (J. Range Manage.) : 9 komondors vs coyotes en enclos de 65 ha ; 141 interactions dont 84 attaques de coyote interrompues par le chien (coyote repoussé)",
  lieu="Utah, USA", annee=1981)
E("chien", 1, "coyote", 3, "A", 1, qual="B",
  src="https://www.cbsnews.com/boston/news/video-cohasset-dog-coyotes",
  note="Le chien Tuukka repousse 3 coyotes devant la maison (vidéo)",
  lieu="Cohasset, Massachusetts", annee=2024)
E("chien", 1, "coyote", 8, "A", 3, count=1, qual="C",
  src="https://news.yahoo.com/georgia-sheepdog-fights-kills-8-214125657.html",
  note="Chien de berger Casper aurait tué 8 coyotes d'une meute en défendant les moutons, revient gravement blessé (récit du propriétaire seulement)",
  lieu="Géorgie, USA")

# ---------------------------------------------------------------------------
# CHIEN vs GRANDS PRÉDATEURS (léopard, puma, ours, guépard)
# ---------------------------------------------------------------------------
E("chien", 3, "leopard", 1, "A", 2, qual="B",
  src="https://dnaindia.com/viral/report-watch-brave-dogs-defend-home-chase-away-leopard-in-nainital-cctv-footage-goes-viral-3100044/amp",
  note="Trois chiens chassent un léopard qui tentait d'entrer dans une maison (vidéosurveillance)",
  lieu="Nainital, Inde", annee=2024)
E("chien", 4, "leopard", 1, "A", 1, tb=["embuscade"], qual="B",
  src="https://www.freepressjournal.in/viral/uttarakhand-news-leopard-pounces-on-street-dog-in-haridwar-at-night-cctv-captures-how-pack-saves-it-from-deadly-attack",
  note="Léopard saisit au cou un chien errant endormi ; plusieurs chiens (≈4) le font fuir",
  lieu="Haridwar, Inde", annee=2025)
E("chien", 1, "leopard", 1, "A", 1, tb=["embuscade"], qual="B",
  src="https://www.freepressjournal.in/amp/pune/pune-dog-fights-off-leopard-in-khed-taluka-cctv-footage-goes-viral",
  note="Léopard bondit sur un chien couché dans une ruelle ; le chien se défend et le fait fuir (chien de rue, probablement < 30 kg)",
  lieu="Khed, Pune, Inde", annee=2025)
E("chien", 1, "puma", 1, "D", 1, qual="B",
  src="https://www.reddeeradvocate.com/national-news/family-dog-saves-b-c-boy-11-from-cougar-attack/",
  note="Chienne retriever (18 mois) s'interpose entre un puma et un garçon de 11 ans et se bat jusqu'à ce qu'un policier abatte le puma ; chienne blessée, survit",
  lieu="Boston Bar, Colombie-Britannique", annee=2010)
E("puma", 1, "chien", 1, "A", 3, qual="B",
  src="https://sanangelo.tamu.edu/files/2022/05/Effectiveness-of-LGDs-for-Ruducing-Predation-on-Domestic-Sheep-Andelt-1992.pdf",
  note="Andelt 1992 (Wildl. Soc. Bull.) : un chien de protection (<1 an) probablement tué par un puma (déclaration d'éleveur)",
  lieu="Ouest des USA", annee=1990)
E("ours_noir", 1, "chien", 1, "A", 3, qual="B",
  src="https://cottagelife.com/news/dog-dead-after-saving-owner-from-bear-attack",
  note="Ours noir adulte attaque un promeneur ; son schnauzer (petit chien) le détourne et meurt ; l'homme s'échappe",
  lieu="Sandbar Lake PP, Ontario", annee=2013)
E("chien", 1, "ours_noir", 1, "D", 1, tb=["defense_petits"], qual="B",
  src="https://abc7ny.com/post/hero-dog-saves-man-from-bear-attack/281404/",
  note="Ourse (~110 kg) avec oursons mord un randonneur ; son croisé labrador l'attaque et l'homme la frappe avec une pierre ; l'ourse cesse",
  lieu="Virginie-Occidentale", annee=2014)
E("chien", 1, "guepard", 1, "A", 3, qual="A",
  src="https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/607619E840644481488447558D32279B/S0030605315000113a.pdf/more-bark-than-bite-the-role-of-livestock-guarding-dogs-in-predator-control-on-namibian-farmlands.pdf",
  note="Potgieter et al. 2016 (Oryx) : sur 83 chiens de protection (bergers anatoliens), 1 a tué un guépard entré dans un enclos de nuit ; 0 léopard tué",
  lieu="Namibie", annee=2012)

# ---------------------------------------------------------------------------
# KANGOUROU vs HUMAIN
# ---------------------------------------------------------------------------
E("kangourou", 1, "humain", 1, "A", 3, ta=["captivite"], tb=["vieux"], qual="B",
  src="https://www.cbsnews.com/news/kangaroo-kills-man-rare-fatal-attack-australia/?ftag=CNM-00-10aab4i",
  note="Peter Eades (77 ans) tué par un kangourou mâle adulte qu'il gardait comme animal de compagnie ; l'animal bloque les secours, abattu",
  lieu="Redmond, Australie-Occidentale", annee=2022)
E("kangourou", 1, "humain", 1, "A", 3, qual="B",
  src="https://www.cbsnews.com/news/kangaroo-kills-man-rare-fatal-attack-australia/?ftag=CNM-00-10aab4i",
  note="William Cruickshank (38 ans) attaqué par un grand kangourou en voulant sauver ses deux chiens ; mâchoire brisée, meurt des mois plus tard",
  lieu="Hillston, Nouvelle-Galles du Sud", annee=1936)
E("humain", 3, "kangourou", 1, "A", 1, ta=["outil"], qual="B",
  src="https://www.omanobserver.om/ampArticle/45866",
  note="Grand mâle (≥1,80 m) attaque un homme qui le nourrissait ; sa femme l'arrache (poumon perforé, côtes cassées) et le fils le frappe à la pelle ; le kangourou s'enfuit",
  lieu="Darling Downs, Queensland", annee=2018)
E("kangourou", 1, "humain", 2, "A", 1, qual="A",
  src="https://www.mja.com.au/journal/2001/175/11/kangaroo-capers",
  note="Med J Aust 2001 : un kangourou gris blesse deux hommes (abrasions profondes, morsure ; l'autre projeté au sol en le tirant par la queue) et repart indemne",
  lieu="Australie", annee=2001)
E("humain", 2, "kangourou", 1, "A", 1, ta=["outil"], qual="B",
  src="https://www.yahoo.com/news/articles/retired-farmer-lucky-alive-being-112607433.html",
  note="Retraité « Col » frappé, griffé (plaies abdominales de 7 cm) ; un ami frappe le kangourou à la pelle, il lâche et retourne dans le barrage",
  lieu="Victoria, Australie", annee=2026)
E("kangourou", 1, "humain", 1, "A", 2, ta=["defense_petits"], qual="B",
  src="https://abcnews4.com/news/nation-world/kangaroo-breaks-womans-leg-others-attacked-macroom-australia-attacks-injured-department-of-environment-and-science-wallabies-marsupials",
  note="Femelle avec petit fracture le fémur d'une femme ; 7 attaques signalées en un an dans le village, toutes par des femelles suitées",
  lieu="Queensland", annee=2022)
E("humain", 1, "kangourou", 1, "A", 1, qual="B",
  src="https://www.nationalgeographic.com/animals/article/man-punches-kangaroo-saves-dog-australia",
  note="Greig Tonkins frappe au visage un grand mâle (~1,80 m, ~77 kg) qui tenait son chien en clé ; le kangourou recule et part",
  lieu="Nouvelle-Galles du Sud", annee=2016)
E("humain", 1, "kangourou", 1, "A", 1, qual="B",
  src="https://www.heraldnet.com/news/kangaroo-tries-to-drown-dog-attacks-owner",
  note="Chris Rickard (49 ans) libère son chien ; le kangourou lui lacère ventre et visage ; il le fait reculer d'un coup de coude à la gorge",
  lieu="Arthurs Creek, Victoria", annee=2009)
E("humain", 1, "kangourou", 1, "D", 1, qual="B",
  src="https://www.livescience.com/animals/land-mammals/kangaroos-might-try-to-drown-your-dog-heres-why",
  note="Mick Moloney entre dans la rivière, frappe le kangourou qui tient son chien ; le kangourou riposte ; homme et chien regagnent la rive",
  lieu="Murray River, Victoria", annee=2023)

# ---------------------------------------------------------------------------
# KANGOUROU vs CHIEN / DINGO
# ---------------------------------------------------------------------------
E("kangourou", 1, "chien", 1, "A", 2, ta=["eau"], qual="B",
  src="https://www.heraldnet.com/news/kangaroo-tries-to-drown-dog-attacks-owner",
  note="Mâle agressif maintient sous l'eau un bouvier australien qui l'avait poursuivi dans une mare ; chien à moitié noyé",
  lieu="Arthurs Creek, Victoria", annee=2009)
E("kangourou", 1, "chien", 1, "A", 1, ta=["eau"], qual="B",
  src="https://www.livescience.com/animals/land-mammals/kangaroos-might-try-to-drown-your-dog-heres-why",
  note="Kangourou dans l'eau à la taille immobilise le chien Hutchy jusqu'à l'intervention du maître",
  lieu="Murray River, Victoria", annee=2023)
E("kangourou", 1, "chien", 1, "A", 1, qual="B",
  src="https://www.nationalgeographic.com/animals/article/man-punches-kangaroo-saves-dog-australia",
  note="Grand mâle tient le chien de chasse en clé de bras avant l'intervention du maître",
  lieu="Nouvelle-Galles du Sud", annee=2016)
E("chien", 2, "kangourou", 1, "A", 3, qual="B",
  src="https://www.goulburnpost.com.au/story/5490344/dogs-attacking-kangaroo-a-warning-to-dog-ownerslandholders-video-pictures/",
  note="Deux chiens attaquent un kangourou près d'un barrage ; il est retrouvé mort de ses blessures le lendemain",
  lieu="Gundary, près de Goulburn, NSW", annee=2018)
E("kangourou", 1, "chien", 1, "A", 1, qual="A",
  src="https://www.publish.csiro.au/wr/WR9930845",
  note="Wright 1993 (Wildl. Res.) : un mâle de kangourou gris tient tête à un dingo pendant >60 min (6 phases de combat, coups de pied et de queue) ; le dingo abandonne (dingo)",
  lieu="Wallaby Creek, NSW", annee=1990)
E("chien", 5, "kangourou", 1, "A", 3, count=3, qual="A",
  src="https://publish.csiro.au/WR/WR9810255",
  note="Shepherd 1981 (Aust. Wildl. Res.) : une meute de 5 dingos tue 83 kangourous roux en 7 semaines près d'un point d'eau, dont seulement 3 adultes (les 80 juvéniles exclus : proies qui fuient) (dingo)",
  lieu="Nord-ouest de la Nouvelle-Galles du Sud", annee=1980)
