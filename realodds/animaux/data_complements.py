"""Real Odds — animaux : compléments (gorille, groupes d'humains contre un animal, chimpanzé contre humain adulte).

Convention : `a` = vainqueur quand res="A" ; res="D" = issue nulle après contact réel.
na/nb = individus réellement engagés. m : 1 serré, 2 net, 3 mort/tué.
Remarques :
- « gorille » sert aussi de proxy pour le gorille de montagne (G. beringei) : lignes marquées « montagne ».
- « ours_noir » sert de proxy pour l'ours noir d'Asie (Cachemire) et, faute de mieux, pour un ours indien
  d'espèce non confirmée (probablement ours lippu) : indiqué dans la note.
- « loup » sert de proxy pour le loup indien (Bahraich), plus petit (~25 kg).
- Aucune ligne avec arme à feu, spray ou véhicule (exclus) ; les incidents de zoo sont tagués captivite.
"""

ENC = []


def E(a, na, b, nb, res, m=2, ta=(), tb=(), count=1, qual="B", src="", note="", lieu="", annee=None):
    ENC.append(dict(a=a, na=na, b=b, nb=nb, res=res, m=m, ta=list(ta), tb=list(tb), count=count, qual=qual,
                    src=src, note=note, lieu=lieu, annee=annee))


# ---------------------------------------------------------------------------
# GORILLE vs HUMAIN — captivité (évasions, soigneurs)
# ---------------------------------------------------------------------------
E("gorille", 1, "humain", 1, "A", 2, ta=["captivite"], qual="B",
  src="https://en.wikipedia.org/wiki/Bokito_(gorilla) ; https://www.inquirer.com/philly/news/nation_world/20070519_At_zoo__a_gorilla_in_their_midst.html",
  note="Bokito (mâle dos argenté, 11 ans, ~180 kg) franchit le fossé, saisit une visiteuse, la traîne sur des dizaines de mètres : fractures, >100 morsures ; personne ne s'interpose (clients du restaurant fuient), endormi au fusil hypodermique",
  lieu="Zoo Blijdorp, Rotterdam", annee=2007)
E("gorille", 1, "humain", 1, "A", 2, ta=["captivite", "jeune"], qual="B",
  src="https://www.bornfreeusa.org/?p=3674 ; https://www.semissourian.com/news/gorilla-exits-boston-zoo-injuring-toddler-and-teenager-121007",
  note="Little Joe (mâle adolescent ~10 ans, ~136 kg, dos noir) évadé : projette, piétine, traîne et mord au dos une femme de 18 ans ; lui arrache la fillette de 2 ans qu'elle portait (blessée)",
  lieu="Franklin Park Zoo, Boston", annee=2003)
E("gorille", 1, "humain", 3, "A", 1, ta=["captivite"], qual="B",
  src="https://dallasnews.com/news/2004/03/19/2004-charging-gorilla-killed-by-police-after-hurting-3-at-dallas-zoo",
  note="Jabari (mâle 13 ans, ~136 kg) évadé : projette un bambin contre un mur et le mord, morsures légères à la mère et à un autre adulte ; abattu par la police (blessures « mineures »)",
  lieu="Dallas Zoo, Texas", annee=2004)
E("gorille", 1, "humain", 1, "A", 1, ta=["captivite"], qual="B",
  src="https://www.gulf-times.com/story/57976/gorilla-escapes-bites-zookeeper",
  note="Koga (dos argenté 24 ans, ~180 kg) sorti de sa loge mord une soigneuse à la main et au mollet (blessures non graves) ; endormi à la sarbacane",
  lieu="Buffalo Zoo, New York", annee=2012)
E("gorille", 1, "humain", 1, "A", 2, ta=["captivite"], qual="B",
  src="https://www.deseret.com/1997/8/8/19354906/hogle-zoo-gorilla-attacks-bites-keeper",
  note="Tino (mâle adulte ~200 kg) renverse et mord le chef soigneur R. Pratt (5 plaies perforantes bras/torse) ; le soigneur s'enfuit à l'étage",
  lieu="Hogle Zoo, Salt Lake City", annee=1997)
E("gorille", 1, "humain", 1, "A", 2, ta=["captivite"], qual="B",
  src="https://www.ibtimes.co.uk/gorilla-breaks-through-three-doors-before-attacking-zookeeper-who-raised-him-1683858",
  note="Malabo (dos argenté 29 ans, ~200 kg) attaque une soigneuse de 46 ans : trauma crânien et thoracique, deux bras cassés, fractures multiples ; collègues le repoussent aux extincteurs (non codé : assimilé à un spray)",
  lieu="Zoo Aquarium de Madrid", annee=2020)
E("gorille", 1, "humain", 1, "A", 2, ta=["captivite"], qual="A",
  src="https://doaj.org/article/db9cb3b5be784d6e9d521b6501f229bc",
  note="Trauma Case Reports 2023 : gorille des plaines >170 kg (sexe non précisé, probablement mâle) mord et malmène un soigneur : fracture ouverte de l'avant-bras, morsures multiples (lieu non précisé ; doublon possible avec Madrid 2020 non exclu)",
  lieu="Zoo (non précisé)", annee=2023)

# ---------------------------------------------------------------------------
# GORILLE vs HUMAIN / CHIEN — sauvages
# ---------------------------------------------------------------------------
E("humain", 6, "gorille", 1, "A", 3, ta=["arme_blanche"], tb=["defense_petits"], qual="B",
  src="https://www.nationalgeographic.com/magazine/article/mountain-gorillas-virunga-peril-dian-fossey",
  note="Digit (jeune dos argenté, montagne) retient 6 braconniers armés de lances et leurs chiens pendant que son groupe fuit ; tué de 5 coups de lance (Fossey, NatGeo 1981)",
  lieu="Karisoke, Volcans, Rwanda", annee=1977)
E("gorille", 1, "chien", 1, "A", 3, tb=["defense_petits"], qual="B",
  src="https://www.nationalgeographic.com/magazine/article/mountain-gorillas-virunga-peril-dian-fossey",
  note="Même combat que la ligne précédente : Digit tue un des chiens des braconniers avant de mourir (montagne)",
  lieu="Karisoke, Volcans, Rwanda", annee=1977)
E("gorille", 1, "humain", 3, "A", 2, ta=["defense_petits"], qual="B",
  src="https://gorillafund.org/we-try-to-free-infant-imfura-from-a-snare/",
  note="Dos argenté Gicurasi (montagne) charge l'équipe qui tente de libérer un petit d'un collet et mord profondément un pisteur à l'épaule et au bras (hospitalisé) ; intervention abandonnée (effectif estimé)",
  lieu="Parc des Volcans, Rwanda", annee=2011)

# ---------------------------------------------------------------------------
# LÉOPARD vs GORILLE
# ---------------------------------------------------------------------------
E("leopard", 1, "gorille", 1, "A", 3, count=2, qual="B",
  src="https://storre.stir.ac.uk/bitstream/1893/3015/1/MK%20Thesis.pdf",
  note="Schaller 1963 (cité par Klailova 2011, §1.5) : morts confirmées de 2-3 mâles adultes (montagne) tués par des léopards (2 retenues)",
  lieu="Virunga", annee=1960)
E("leopard", 1, "gorille", 1, "A", 3, qual="C",
  src="https://storre.stir.ac.uk/bitstream/1893/3015/1/MK%20Thesis.pdf",
  note="Robbins et al. 2004 (cité par Klailova) : prédation par léopard « fortement soupçonnée » dans la mort d'un dos argenté (non confirmée)",
  lieu="Mbeli Bai, Congo", annee=2004)
E("leopard", 1, "gorille", 1, "A", 3, tb=["jeune"], qual="C",
  src="https://storre.stir.ac.uk/bitstream/1893/3015/1/MK%20Thesis.pdf",
  note="Robbins et al. 2004 (cité par Klailova) : mort d'un dos noir (mâle ~8-12 ans, subadulte) soupçonnée due à un léopard",
  lieu="Lossi, Congo", annee=2004)

# ---------------------------------------------------------------------------
# GORILLE vs GORILLE
# ---------------------------------------------------------------------------
E("gorille", 1, "gorille", 1, "A", 3, count=8, qual="A",
  src="https://pmc.ncbi.nlm.nih.gov/articles/PMC7673674",
  note="Caillaud et al. 2020 Sci. Adv. : 8 mâles matures morts de blessures reçues lors de rencontres entre unités (1 en 2000-06, 7 en 2007-17), montagne ; sur 625 rencontres observées, agression entre mâles dans 22 % (surtout parades) ; parfois coalitions (effectif ~1 contre 1)",
  lieu="Volcans, Rwanda", annee=2017)

# ---------------------------------------------------------------------------
# CHIMPANZÉ vs HUMAIN ADULTE
# ---------------------------------------------------------------------------
E("chimpanze", 1, "humain", 1, "A", 1, qual="A",
  src="https://www.greencorridor.info/data/Attacks_on_local_persons_by_chimpanzees_in_Bossou,_Republic_of_Guinea__long-term_perspectives.pdf",
  note="Hockings et al. 2010 : seule victime adulte sur 11 attaques 1995-2009 (les 10 autres = enfants) : femme de 30 ans, coupures aux jambes",
  lieu="Bossou, Guinée", annee=2006)
E("chimpanze", 3, "humain", 1, "A", 2, qual="B",
  src="https://fr.journalducameroun.com/cameroun-trois-chimpanzes-attaquent-un-homme-a-ndom/",
  note="Trois chimpanzés sauvages attaquent un cultivateur adulte sur le chemin de son champ : plaies au crâne et au visage, grièvement blessé, survit",
  lieu="Logmang, Ndom, Cameroun", annee=2025)
E("chimpanze", 1, "humain", 1, "A", 1, count=2, qual="B",
  src="https://archive.spectator.co.uk/article/29th-june-2002/22/me-frodo-you-jane ; https://www.greenmatters.com/environmental-leaders/was-jane-goodall-ever-attacked-by-chimps",
  note="Frodo (mâle alpha sauvage habitué) frappe Jane Goodall (1989, nuque presque brisée) et rosse le dessinateur Gary Larson ; pas de blessure durable",
  lieu="Gombe, Tanzanie", annee=1989)

# ---------------------------------------------------------------------------
# PLUSIEURS HUMAINS vs UN FÉLIN (bâtons, outils agricoles)
# ---------------------------------------------------------------------------
E("humain", 15, "leopard", 1, "A", 3, ta=["arme_blanche"], qual="B",
  src="https://www.outlookindia.com/national/leopard-attack-in-mandi-leaves-one-dead-nine-injured-before-animal-is-killed",
  note="Léopard : 1 mort et 9 blessés (5 graves) dans 3 villages ; encerclé et tué à coups de bâtons et d'outils tranchants, quelques blessés légers quand il riposte (effectif estimé)",
  lieu="Balh, Mandi, Himachal Pradesh")
E("humain", 10, "leopard", 1, "A", 3, ta=["outil"], qual="B",
  src="https://theprint.in/india/leopard-beaten-to-death-by-villagers-after-attack-on-man-in-udaipur/2307255",
  note="Léopard attaque le bétail puis un homme de 55 ans (blessé) ; villageois accourus le tuent à coups de bâtons (effectif estimé)",
  lieu="Sayra, Udaipur, Rajasthan", annee=2024)
E("humain", 10, "leopard", 1, "A", 3, ta=["outil"], qual="B",
  src="https://theprint.in/india/mp-leopard-beaten-to-death-by-villagers-after-it-attacks-injures-man-in-khargone-district/1595737/",
  note="Léopard (3-4 ans) blesse un homme à la main ; villageois l'acculent et le tuent avec bâtons et pierres (effectif estimé)",
  lieu="Chainpur, Khargone, Madhya Pradesh", annee=2023)
E("humain", 10, "leopard", 1, "A", 3, ta=["arme_blanche"], qual="B",
  src="https://ianslive.in/leopardess-beaten-to-death-by-villagers--20240510062706",
  note="Femelle léopard de 3 ans blesse 3 ouvriers agricoles ; tuée à coups de bâtons et d'outils agricoles tranchants (effectif estimé)",
  lieu="Rampur, Pilibhit, Uttar Pradesh", annee=2024)
E("humain", 2, "tigre", 1, "A", 1, ta=["outil"], qual="B",
  src="https://www.freepressjournal.in/bhopal/tribal-man-survives-tiger-attack-in-pench-reserve-fends-off-big-cat-with-lathi",
  note="Bouvier de 50 ans attaqué (tête, mains), repousse le tigre au lathi ; un second bouvier accourt, le tigre fuit",
  lieu="Pench, Madhya Pradesh", annee=2025)
E("humain", 4, "tigre", 1, "A", 1, ta=["outil"], qual="B",
  src="https://www.inkl.com/news/fisherman-saved-after-20-minute-fight-with-tiger-in-sunderbans-tiger-reserve-area",
  note="Tigre saute sur un bateau et saisit un pêcheur (cou, dos, cuisse, état critique) ; 3 compagnons le frappent au bâton ~20 min, le tigre se retire",
  lieu="Rivière Kapura, Sundarbans, Inde")
E("humain", 6, "tigre", 1, "A", 1, ta=["outil"], qual="B",
  src="https://en.prothomalo.com/bangladesh/Man-survives-fight-against-tiger",
  note="Tigre saisit le bras d'un pêcheur et le traîne ; son frère le frappe au bâton avec 4 pêcheurs, le tigre lâche et fuit",
  lieu="Rivière Shela, Sundarbans, Bangladesh", annee=2019)
E("humain", 2, "tigre", 1, "A", 1, ta=["outil"], qual="B",
  src="https://theprint.in/india/galat-jagah-pakad-liya-forest-guards-split-second-courage-saves-colleague-from-tiger/3078395/",
  note="Tigre mord un garde forestier au cou ; un collègue le frappe 3 fois au bâton, le tigre lâche et se retire (patrouille de 4, 1 seul intervient)",
  lieu="Corbett, Uttarakhand", annee=2026)
E("humain", 30, "tigre", 1, "A", 3, ta=["arme_blanche"], qual="B",
  src="https://nzherald.co.nz/world/tiger-beaten-to-death-on-video-outraging-india/IGLKOS6SPAEPP5ZPVIF3YWLLTI",
  note="Tigresse (5-6 ans) blesse un pêcheur puis 8 autres personnes dans la mêlée (1 meurt ensuite) ; plusieurs dizaines d'hommes (lance, bâtons, machettes) la tuent",
  lieu="Pilibhit, Uttar Pradesh", annee=2019)
E("humain", 8, "tigre", 1, "A", 3, ta=["outil"], qual="B",
  src="https://dunyanews.tv/en/WeirdNews/141719--Villagers-beat-Bengal-tiger-to-death",
  note="Tigre mord un pêcheur à la main en tentant de l'emporter ; villageois le tuent à coups de bâtons et de rames (effectif estimé)",
  lieu="Naodag, Sundarbans, Bangladesh", annee=2012)
E("humain", 10, "tigre", 1, "A", 1, ta=["outil"], qual="B",
  src="https://gulfnews.com/world/asia/india/men-attack-tiger-big-cat-fights-back-1.1579968575698",
  note="Foule armée de bâtons et barres poursuit un tigre, qui se retourne et renverse un homme puis s'enfuit quand les hommes approchent (vidéo ; effectif estimé)",
  lieu="Maharashtra", annee=2020)

# ---------------------------------------------------------------------------
# PLUSIEURS HUMAINS vs UN OURS
# ---------------------------------------------------------------------------
E("ours_noir", 1, "humain", 3, "A", 3, tb=["outil"], qual="A",
  src="https://www.carnegiehero.org/hero-search/frank-s-hedingham/ ; https://carnegiehero.org/hero-search/kelly-mcconnell",
  note="Ours noir mâle de 99 kg (prédateur) : tue Patti McConnell et Raymond Kitchen (bâton), grièvement blessé son fils Kelly, 13 ans (branche, coups de pied) ; aussi compté dans l'agrégat Herrero (1v1) de data_nord",
  lieu="Liard River Hot Springs, C.-B.", annee=1997)
E("humain", 3, "ours_noir", 1, "A", 1, qual="A",
  src="https://carnegiehero.org/hero-search/gary-richmond",
  note="Même attaque : G. Richmond et d'autres visiteurs chassent l'ours de la passerelle ; il attaque ensuite une 4e personne et est abattu (effectif estimé)",
  lieu="Liard River Hot Springs, C.-B.", annee=1997)
E("humain", 10, "ours_noir", 1, "A", 3, ta=["outil"], qual="B",
  src="https://www.oneindia.com/2008/10/07/3-injured-in-bear-attack-villagers-kills-bear-in-kashmir-1223377558.html",
  note="Ours noir d'Asie (proxy) blesse 3 personnes dont une fille dans un état critique ; villageois le tuent à coups de pierres et de bâtons (effectif estimé)",
  lieu="Dangipora, Kokernag, Cachemire", annee=2008)
E("humain", 10, "ours_noir", 1, "A", 3, ta=["outil"], qual="B",
  src="https://www.oneindia.com/2007/11/05/bear-killed-by-villagers-after-injuring-two-in-kashmir-1194254070.html",
  note="Ours noir d'Asie (proxy) blesse 2 hommes ; villageois les secourent et le tuent au lathi (effectif estimé)",
  lieu="Mattan, Anantnag, Cachemire", annee=2007)
E("ours_noir", 1, "humain", 4, "A", 3, qual="B",
  src="https://www.fieldandstream.com/survival/bear-kills-three-people-india/?amp",
  note="Ours d'espèce non confirmée (probablement ours lippu, proxy) : après avoir tué un ramasseur de bois, tue 2 des 4 hommes partis le chercher et blesse les 2 autres",
  lieu="Odisha, Inde")
E("humain", 10, "ours_noir", 1, "A", 3, qual="B",
  src="https://www.fieldandstream.com/survival/bear-kills-three-people-india/?amp",
  note="Même ours : les villageois le traquent et le tuent à coups (armes non précisées, effectif estimé)",
  lieu="Odisha, Inde")

# ---------------------------------------------------------------------------
# HUMAIN vs CANIDÉS SAUVAGES
# ---------------------------------------------------------------------------
E("humain", 1, "loup", 1, "A", 3, qual="B",
  src="https://www.themoscowtimes.com/2013/09/05/kazakh-man-kills-wolf-with-bare-hands-a27404",
  note="Ex-policier attaqué par surprise par un loup (morsures dos et membres) l'étrangle à mains nues ; confirmé par la police",
  lieu="Zhetybai, Kazakhstan", annee=2013)
E("loup", 1, "humain", 1, "A", 2, ta=["embuscade"], qual="B",
  src="https://www.deccanherald.com/india/uttar-pradesh/up-woman-injured-in-fresh-wolf-attack-at-home-in-bahraich-3187641",
  note="Loup indien (proxy) entre dans la maison et blesse grièvement une femme de 50 ans endormie ; fuit à l'arrivée de la famille et des voisins",
  lieu="Kowinpura, Bahraich, Uttar Pradesh")
E("humain", 1, "coyote", 1, "A", 3, qual="B",
  src="https://www.eastidahonews.com/?p=418751",
  note="Coyote saisit un enfant de 2 ans ; le père le repousse du pied puis l'étouffe ~10 min en lui tenant la gueule (mordu 2 fois)",
  lieu="New Hampshire", annee=2020)
