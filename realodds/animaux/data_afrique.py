"""Real Odds — animaux : rencontres documentées, cluster AFRIQUE.

Convention : a = vainqueur quand res="A" ; res="D" = match nul / désengagement après contact réel.
m : 1 = étroit, 2 = net, 3 = mort/consommé. Tags : voir guide.
Remarque : pour quelques études ne donnant qu'une proportion, les `count` sont reconstruits
à partir de la proportion publiée (indiqué dans la note par « compte reconstruit »).
2e passage (vérification ligne par ligne) : chaque ligne porte « # vérifié », « # corrigé : … » ou « # supprimé : … ».
"""

ENC = []


def E(a, na, b, nb, res, m=2, ta=(), tb=(), count=1, qual="B", src="", note="", lieu="", annee=None):
    ENC.append(dict(a=a, na=na, b=b, nb=nb, res=res, m=m, ta=list(ta), tb=list(tb), count=count,
                    qual=qual, src=src, note=note, lieu=lieu, annee=annee))


# ---------------------------------------------------------------------------
# LION vs HYÈNE (kleptoparasitisme, effectifs)
# ---------------------------------------------------------------------------
_LEHMANN = "https://par.nsf.gov/servlets/purl/10132938"  # Lehmann et al. 2017, Current Zoology 63:313-322
E("lion", 3, "hyene", 14, "A", 1, ta=["carcasse"], tb=["carcasse"], count=67, qual="A", src=_LEHMANN,
  note="Sessions alimentaires avec mâle(s) lion présent(s) : les lions gardent/prennent la nourriture dans 67 cas sur 93 (93-26) ; effectifs = médianes de l'étude, 3 lions / 14 hyènes (effectif estimé) ; surtout sans contact physique",
  lieu="Masai Mara (Talek), Kenya", annee=2017)  # corrigé : effectifs ramenés aux médianes publiées (3 et 14)
E("hyene", 14, "lion", 3, "A", 1, ta=["carcasse"], tb=["carcasse"], count=26, qual="A", src=_LEHMANN,
  note="Même étude : les hyènes obtiennent la nourriture malgré la présence de mâles lions dans 26 cas sur 93 (mobbing, médiane 4 hyènes par mob ; effectif estimé)",
  lieu="Masai Mara (Talek), Kenya", annee=2017)  # corrigé : effectifs ramenés aux médianes publiées

_COOPER = "https://ui.adsabs.harvard.edu/abs/1991AfJEc..29..130C"  # Cooper 1991 Afr J Ecol 29:130-136
E("hyene", 12, "lion", 3, "A", 1, ta=["carcasse"], tb=["carcasse"], count=2, qual="A", src=_COOPER,
  note="Cooper 1991 : sans mâle adulte, les hyènes chassent lionnes/subadultes des proies si elles sont ≥ 4 fois plus nombreuses ; ces groupes perdent près de 20 % de leur NOURRITURE (proportion de biomasse, pas de rencontres : compte reconstruit 2/10, effectif estimé)",
  lieu="Savuti, Chobe, Botswana", annee=1991)  # corrigé : URL miroir douteuse remplacée par ADS ; précision « 20 % de la nourriture »
E("lion", 3, "hyene", 8, "A", 1, ta=["carcasse"], tb=["carcasse"], count=8, qual="A", src=_COOPER,
  note="Même étude : lionnes/subadultes conservent ~80 % de leur nourriture face aux hyènes (compte reconstruit 8/10, effectif estimé)",
  lieu="Savuti, Chobe, Botswana", annee=1991)  # corrigé : URL remplacée

_HYPROJ = "https://hyena-project.com/research-topics/conflict-with-lions/"
E("lion", 1, "hyene", 20, "A", 2, ta=["carcasse"], tb=["carcasse"], count=1, qual="A", src=_HYPROJ,
  note="Ngorongoro : un lion mâle adulte domine ou prend toujours la carcasse quel que soit le nombre de hyènes (synthèse du projet, Höner et al. 2002 ; effectif estimé)",
  lieu="Cratère du Ngorongoro, Tanzanie", annee=2002)  # vérifié
E("hyene", 12, "lion", 2, "A", 1, ta=["carcasse"], tb=["carcasse"], count=1, qual="A", src=_HYPROJ,
  note="Ngorongoro : les hyènes gardent/prennent la proie face à des lionnes ou jeunes mâles si elles sont au moins 6 fois plus nombreuses (Höner et al. ; 3:1 selon le compte rendu THE 2002 ; effectif estimé)",
  lieu="Cratère du Ngorongoro, Tanzanie", annee=2002)  # corrigé : note complétée (fusion avec la ligne THE)
# supprimé : ligne timeshighereducation.com/node/38511 — même étude Höner (Ngorongoro, pas Masai Mara), doublon de la ligne précédente
# supprimé : ligne « Trinkel & Kastberger 2005 » via Barker et al. 2026 — généralisation sans aucun compte ni rencontre décrite (count inventé)
E("lion", 4, "hyene", 20, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/twenty-hyenas-take-on-four-lions",
  note="1 jeune mâle + 3 lionnes chargent et dispersent à plusieurs reprises un grand clan (~20 d'après le titre, effectif estimé) ; pas de blessé, lions toujours sur la proie à la fin (issue finale non rapportée)",
  lieu="Crocodile River, bordure du Kruger", annee=2026)  # corrigé : effectif hyènes estimé, issue partielle
E("lion", 22, "hyene", 22, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/22-lions-chase-22-hyenas-from-a-hippo",
  note="Grande troupe (surtout lionnes) charge et chasse 22 hyènes d'une carcasse d'hippopotame, sans combat (déplacement)", lieu="Ngala, Grand Kruger", annee=2026)  # vérifié (déplacement sans contact, m=1)
E("lion", 1, "hyene", 15, "D", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://blog.londolozi.com/2020/03/07/lioness-takes-on-15-hyenas/",
  note="Lionne Tsalala (seule, avec un petit) : chassée de son gnou, revient deux fois disperser ~15 hyènes (effectif estimé), puis chassée le soir ; partage final ; pas de contact décrit",
  lieu="Londolozi, Afrique du Sud", annee=2020)  # corrigé : retiré defense_petits (conflit alimentaire, petit non menacé)
E("hyene", 8, "lion", 1, "A", 2, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/hyenas-mob-and-bite-lone-lioness-serondella",
  note="Lionne seule mordue de toutes parts par un clan (effectif estimé), abandonne sa proie", lieu="Serondella, Chobe, Botswana", annee=2024)  # corrigé : effectif estimé
# supprimé : ligne « hyène 20 vs jeune lion seul » (BBC Dynasties) — même événement que la ligne suivante, pas d'issue avant l'arrivée du second mâle
E("lion", 2, "hyene", 20, "A", 1, ta=["jeune"], qual="B",
  src="https://whyevolutionistrue.com/2018/11/30/lion-attacked-by-hyenas-saved-by-pal/",
  note="Jeune mâle encerclé par plus de 20 hyènes, sauvé par l'arrivée d'un second mâle (Tatu) qui disperse les hyènes (BBC Dynasties)", annee=2018)  # corrigé : fusion des deux lignes du même événement
E("lion", 1, "hyene", 6, "D", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://www.upi.com/Odd_News/2023/08/29/africa-hyena-lion-attack/1811693324787/",
  note="Gros mâle charge un clan sur une carcasse et saisit une hyène par la tête ; le clan accourt, issue inconnue (effectif estimé)", lieu="Arathusa, Sabi Sand", annee=2023)  # corrigé : effectif estimé

# ---------------------------------------------------------------------------
# LION vs BUFFLE
# ---------------------------------------------------------------------------
E("buffle", 10, "lion", 2, "A", 3, qual="B",
  src="https://www.getaway.co.za/?p=15455472",
  note="Troupeau de plus de 100 buffles : une lionne cachée dans les roseaux projetée, encornée et piétinée à mort, la seconde chassée (une dizaine au contact, effectif estimé)",
  lieu="Mestel Dam, Kruger", annee=2020)  # corrigé : événement de décembre 2020 (republié en 2025), source Getaway, effectif
# supprimé : ligne lafm.com.co — même événement que Mestel Dam (déc. 2020), doublon
E("lion", 2, "buffle", 1, "A", 3, tb=["blesse"], qual="B",
  src="https://latestsightings.com/single-post/watch-male-lions-capture-buffalo-mother-and-calf",
  note="Deux mâles tuent une bufflonne boiteuse (qui encorne et retourne l'un d'eux) puis son veau", lieu="S41, Kruger", annee=2025)  # vérifié
E("buffle", 5, "lion", 4, "A", 1, qual="B",
  src="https://latestsightings.com/single-post/watch-lions-attack-buffaloes-in-intense-kruger-battle",
  note="1 jeune mâle + 3 lionnes mettent à terre une vache ; 4 mâles buffles repoussent les lions, la vache blessée se relève et s'éloigne", lieu="Lower Sabie, Kruger", annee=2025)  # corrigé : na = vache + 4 mâles
# supprimé : ligne Napi Road (3 mâles vs troupeau) — aucun contact, simple face-à-face
E("lion", 7, "buffle", 1, "A", 3, qual="B",
  src="https://blog.londolozi.com/2017/09/14/an-epic-standoff-between-lions-and-buffalo/",
  note="6 lionnes Ntsevu + 1 mâle Majingilane acculent une jeune vache (âge non précisé, adulte probable) au bord de l'eau, le mâle l'étouffe", lieu="Londolozi", annee=2017)  # corrigé : retiré tag jeune (jeune vache ≠ subadulte avéré)
# supprimé : ligne « 80 buffles vs 2 lions sur la carcasse » — face-à-face sans contact, issue de la carcasse non rapportée

# ---------------------------------------------------------------------------
# LION vs ÉLÉPHANT / HIPPO / RHINO / CROCODILE
# ---------------------------------------------------------------------------
_LOVERIDGE = "https://www.originalwisdom.com/wp-content/uploads/bsk-pdf-manager/2019/04/Loveridge-et-al_2006_Influence-of-drought-on-predation-of-elephant-calves-by-lions-savannah.pdf"
E("lion", 7, "elephant", 1, "A", 3, tb=["jeune"], count=41, qual="A", src=_LOVERIDGE,
  note="Loveridge et al. 2006 : 44 éléphants tués par des lions (40 selon les tableaux), âge moyen 2,4 ans (88 % < 4 ans, max 7,5 ans), groupes de ~7 lionnes (effectif estimé) ; 7 des 8 mises à mort observées = veaux isolés de leur famille (résistance faible) ; 44 - 3 tués par un mâle seul",
  lieu="Hwange, Zimbabwe", annee=2003)  # corrigé : note (veaux isolés, total 40/44)
E("lion", 1, "elephant", 1, "A", 3, tb=["jeune"], count=3, qual="A", src=_LOVERIDGE,
  note="Même étude : des mâles seuls tuent un éléphanteau à 3 reprises (le plus âgé : 3 ans)", lieu="Hwange, Zimbabwe", annee=2003)  # vérifié
E("elephant", 2, "lion", 1, "A", 1, ta=["defense_petits"], count=1, qual="A", src=_LOVERIDGE,
  note="Deux femelles adultes reviennent défendre un jeune de 5-6 ans attaqué par une lionne, il s'échappe (contact non décrit)", lieu="Hwange, Zimbabwe", annee=2003)  # vérifié
E("elephant", 1, "lion", 1, "D", 1, ta=["jeune"], count=1, qual="A", src=_LOVERIDGE,
  note="Embuscade de 7 lions sur une petite famille (reconstitution par les traces) : un jeune éléphant traîne un lion mâle sur ~10 m et s'échappe (un veau < 1 mois tué, compté dans la 1re ligne)", lieu="Hwange, Zimbabwe", annee=2003)  # corrigé : res A→D (fuite de la victime, pas de victoire nette)

E("lion", 9, "hippopotame", 1, "A", 3, ta=["jeune"], tb=["jeune"], count=6, qual="B",
  src="https://www.zambiatourism.com/south-luangwa-lions-developing-a-taste-for-hippo/",
  note="Troupe de 9 (1 femelle adulte + 8 subadultes) tue 6 hippos en quelques mois, surtout des jeunes isolés en distrayant la mère",
  lieu="South Luangwa, Zambie", annee=2015)  # corrigé : tag jeune côté hippo (victimes juvéniles)
E("hippopotame", 1, "lion", 9, "D", 1, ta=["defense_petits"], tb=["jeune"], count=1, qual="B",
  src="https://www.zambiatourism.com/south-luangwa-lions-developing-a-taste-for-hippo/",
  note="Même troupe : « beaucoup d'autres tentatives » échouées (nombre et déroulé non précisés, compté 1)", lieu="South Luangwa, Zambie", annee=2015)  # corrigé : res A→D (échec du prédateur sans victoire décrite de l'hippo)
E("hippopotame", 1, "lion", 1, "A", 3, ta=["defense_petits"], qual="B",
  src="https://peopledaily.digital/news/kws-confirms-death-of-lion-after-attack-by-mother-hippo-in-maasai-mara",
  note="Le mâle Kiminati (11 ans, mâle adulte) s'attaque à un bébé hippo ; la mère contre-attaque, blessures mortelles (confirmé KWS)", lieu="Masai Mara, Kenya", annee=2026)  # vérifié
# supprimé : ligne Selinda (hippo charge 3 lions dans un chenal) — pas de contact rapporté, aucun blessé
E("lion", 2, "hippopotame", 1, "A", 3, qual="B",
  src="https://latestsightings.com/single-post/hippos-desperate-attempt-to-save-friend-from-lions-zambia",
  note="Deux mâles adultes attaquent l'hippo résident « Henry » au ventre ; un gros mâle hippo s'approche, les lions partent, la victime meurt le lendemain", lieu="Ila Safari Lodge, Zambie", annee=2024)  # vérifié

_BRAIN = "https://rhinoresourcecenter.com/wp-content/uploads/2006/12/1175858056.pdf"
E("lion", 3, "rhinoceros", 1, "A", 3, tb=["jeune"], count=3, qual="A", src=_BRAIN,
  note="Brain et al. 1999 : trois mâles (~6 ans) tuent 3 rhinocéros noirs subadultes (3-4 ans) aux points d'eau en 1995 (rhino noir → proxy rhinoceros)",
  lieu="Etosha, Namibie", annee=1995)  # vérifié
E("rhinoceros", 1, "lion", 1, "A", 3, ta=["defense_petits"], count=1, qual="B", src=_BRAIN,
  note="Goddard 1966 cité par Brain et al. : une femelle rhino noir (proxy) tue un lion menaçant son petit ; la référence citée porte sur l'accouplement, non vérifiée",
  lieu="Tsavo Est, Kenya", annee=1966)  # corrigé : lieu Tanzanie→Tsavo Est (Kenya), qual A→B (citation secondaire)
E("rhinoceros", 1, "lion", 3, "A", 1, tb=["jeune"], qual="B",
  src="https://latestsightings.com/single-post/lions-attack-black-rhino-trapped-in-mud",
  note="Trois jeunes mâles attaquent un rhino noir (proxy) épuisé dans un point d'eau ; il en éjecte un de son dos, charge à répétition, les lions abandonnent", lieu="Etosha, Namibie", annee=2025)  # corrigé : m 2→1 (repoussé sans blessure)
E("lion", 5, "rhinoceros", 1, "A", 3, tb=["blesse"], qual="B",
  src="https://latestsightings.com/single-post/watch-elephants-try-saving-stuck-rhino-from-hungry-lions",
  note="Rhino noir (proxy) embourbé : la troupe (effectif estimé) le renverse, il se noie", lieu="Aus, Etosha", annee=2024)  # corrigé : effectif estimé
# supprimé : ligne « éléphants chargent les lions » (Aus) — charge sans contact, les lions reviennent et gagnent

E("lion", 5, "crocodile_nil", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/cornered-crocodile-forced-to-fight-off-five-lions",
  note="Crocodile sorti voler le cobe tué par la troupe ; 5 lionnes l'acculent, il force le passage et regagne l'eau, les lions gardent la proie", lieu="Buffelshoek, Sabi Sand", annee=2025)  # vérifié
E("lion", 2, "crocodile_nil", 1, "A", 3, count=1, qual="B",
  src="https://panthera.org/blog-post/when-lions-hunt-elephants-and-crocs",
  note="Everatt (Panthera) : lions de Matusadona tuent « très couramment » des crocodiles jusqu'à ~3,6 m sortis de l'eau (pas de compte ; effectif estimé)",
  lieu="Matusadona, Zimbabwe", annee=2024)  # vérifié (généralisation, compté 1)
E("lion", 1, "crocodile_nil", 1, "D", 1, ta=["jeune"], tb=["eau", "embuscade"], qual="B",
  src="https://latestsightings.com/single-post/crocodile-attacks-male-lion-in-riverside-showdown",
  note="Crocodile happe à la tête un jeune mâle traversant la rivière, tous deux sous l'eau ; le lion ressort et s'échappe", lieu="Pont H10, Lower Sabie, Kruger", annee=2025)  # corrigé : tags jeune (lion) et embuscade (croc)
# supprimé : ligne « crocodile happe un lionceau » (risingsun) — issue non rapportée

# ---------------------------------------------------------------------------
# LION vs LÉOPARD / GUÉPARD / LYCAON / RATEL
# ---------------------------------------------------------------------------
E("lion", 2, "leopard", 1, "A", 3, qual="C",
  src="https://latestsightings.com/single-post/world-famous-three-rivers-leopard-found-dead-after-evidence-of-a-lion-attack",
  note="Femelle Three Rivers (~10 ans) retrouvée mutilée près de deux lionnes suitées (attribution aux lions probable, non vue)", lieu="Sabi Sand", annee=2026)  # corrigé : qual B→C (non observé)
_HUNTER = "https://ora.ox.ac.uk/objects/uuid:f8d14a94-3c96-4127-bc17-7d4cfdc8677e/files/m41b799fd5f7329089f7fc5ae5c7386fa"
E("hyene", 1, "guepard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], count=64, qual="A", src=_HUNTER,
  note="Hunter et al. 2007 (cité par Broekhuis & Irungu 2016) : guépards perdent jusqu'à 12,9 % des proies, 78 % aux hyènes ; sur 639 proies (1980-2002) → ~64 (compte reconstruit, souvent sans combat)",
  lieu="Serengeti, Tanzanie", annee=2007)  # vérifié (639 confirmé dans le résumé de Hunter et al. 2007)
E("lion", 1, "guepard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], count=12, qual="A", src=_HUNTER,
  note="Même source : 15 % des pertes vont aux lions → ~12 proies sur 639 (compte reconstruit)", lieu="Serengeti, Tanzanie", annee=2007)  # vérifié
E("guepard", 4, "hyene", 1, "A", 1, ta=["carcasse", "jeune"], tb=["carcasse"], qual="A", src=_HUNTER,
  note="Inversion rare : une femelle guépard et ses 3 jeunes (~15 mois) chassent une hyène de son topi", lieu="Masai Mara, Kenya", annee=2015)  # vérifié
E("hyene", 1, "guepard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://blog.londolozi.com/2013/09/25/cheetah-on-the-backfoot/",
  note="Mâle guépard feule mais cède son impala à une hyène seule, sans contact", lieu="Londolozi", annee=2013)  # vérifié

E("lion", 3, "lycaon", 10, "A", 3, qual="B",
  src="https://latestsightings.com/single-post/male-lion-ends-alpha-wild-dogs-reign-sabi-sands",
  note="Mâle + lionnes (effectif estimé) : le mâle tue la femelle alpha, une lionne tue un jeune chien (2 morts, « 20 % de la meute » → ~10 chiens)", lieu="Sabi Sand", annee=2022)  # corrigé : effectifs estimés

E("lion", 1, "ratel", 1, "A", 3, qual="B", src="https://www.sundestinations.co.za/blog/?p=7115",
  note="Une lionne Ross (3 présentes) tue un ratel après ~20 min de résistance acharnée", lieu="Grand Kruger (Africa on Foot)", annee=2015)  # vérifié
# supprimé : ligne « petit ratel emporté par un lion » (H9) — aucune résistance, mère non vue

# ---------------------------------------------------------------------------
# HYÈNE vs LYCAON / LÉOPARD
# ---------------------------------------------------------------------------
E("lycaon", 10, "hyene", 2, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/watch-wild-dogs-defend-kill-against-hungry-hyenas",
  note="Plus de 10 lycaons encerclent et harcèlent 2 hyènes qui abandonnent", lieu="Grand Kruger", annee=2015)  # vérifié
E("hyene", 6, "lycaon", 8, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/hyenas-steal-wild-dog-kill-twice-in-epic-battle",
  note="Un clan tue un lechwe puis un second groupe surpasse la meute et lui prend sa proie (effectifs estimés)", lieu="Okavango, Botswana", annee=2025)  # corrigé : effectifs estimés
E("hyene", 2, "lycaon", 5, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/lone-hyena-surrounded-by-a-pack-of-wild-dogs",
  note="Deux puis une seule hyène gardent l'essentiel de la proie volée aux lycaons malgré leurs morsures rapides (effectif estimé)", annee=2026)  # corrigé : effectif estimé
E("lycaon", 4, "hyene", 5, "D", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://blog.londolozi.com/2020/07/11/wild-dogs-vs-hyena-vs-leopard/",
  note="4 lycaons mangent malgré 5-6 hyènes, face-à-face puis les chiens partent et les hyènes finissent les restes", lieu="Londolozi", annee=2020)  # vérifié
E("lycaon", 4, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="C",
  src="https://blog.londolozi.com/2020/07/11/wild-dogs-vs-hyena-vs-leopard/",
  note="Léopard mâle perché près d'une proie mangée par 4 lycaons ; l'auteur suppose que la proie était la sienne (non observé, sans contact)", lieu="Londolozi", annee=2020)  # corrigé : qual B→C (attribution de la proie supposée)
# supprimé : ligne « léopard tue un louveteau » (Savuti) — hypothèse du photographe, non observé, pas de combat
E("lycaon", 8, "leopard", 1, "A", 1, qual="B",
  src="https://latestsightings.com/single-post/wild-dogs-get-revenge-on-leopard-that-caught-a-puppy-chobe-national-park",
  note="La meute (effectif estimé) encercle et mord le léopard sur le dos, qui se réfugie dans un fourré « relativement indemne »", lieu="Savuti, Chobe", annee=2023)  # corrigé : effectif estimé

_BALME = "https://datadryad.org/dataset/doi:10.5061/dryad.gb794"
E("hyene", 1, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], count=213, qual="A", src=_BALME,
  note="Balme et al. 2017 : ≥ 21 % de 2032 proies de 104 léopards (2013-2015) volées (~427), environ la moitié par des hyènes (Panthera) → ~213 (compte reconstruit, souvent sans combat)",
  lieu="Sabi Sand, Afrique du Sud", annee=2015)  # corrigé : 340→213 (part des hyènes ≈ 50 %, pas 80 %)
E("hyene", 2, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/hyenas-dominate-leopard-and-steal-its-kill",
  note="Deux hyènes surpassent le léopard (qui griffe) dans un tir à la corde et prennent l'impala", lieu="Grand Kruger", annee=2025)  # vérifié
E("hyene", 1, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/leopard-fights-off-hyena-to-keep-her-kill",
  note="Une hyène seule épuise une femelle léopard et prend la proie ; la léoparde repart blessée à une patte arrière", lieu="Sabi Sand", annee=2025)  # corrigé : sexe (femelle) ajouté

# ---------------------------------------------------------------------------
# LÉOPARD vs BABOUIN / CROCODILE / RATEL
# ---------------------------------------------------------------------------
_BUSSE = "https://curtbusse.com/wp-content/uploads/2026/02/Busse1980.pdf"
E("leopard", 1, "babouin", 1, "A", 3, ta=["embuscade"], count=3, qual="A", src=_BUSSE,
  note="Busse 1980 : 6 attaques de léopard aux dortoirs (nuit), 3 adultes tués (2 femelles, 1 mâle) ; résistance non décrite",
  lieu="Moremi, Botswana", annee=1979)  # vérifié
E("babouin", 20, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], count=1, qual="B", src=_BUSSE,
  note="Même étude (14/08/1978) : ~20 babouins menacent à < 10 m un léopard sur sa proie (femelle adulte) ; il l'abandonne à l'arrivée de l'observateur (sans contact)", lieu="Moremi, Botswana", annee=1978)  # corrigé : année, qual A→B (observateur a pu provoquer la fuite)
E("leopard", 1, "babouin", 30, "A", 1, ta=["carcasse"], qual="B",
  src="https://wildernessdestinations.com/journal/your-guide-to-africa/leopard-left-for-dead-by-baboon-troop",
  note="Léoparde allaitante tue un jeune babouin, est submergée par la troupe (~30, effectif estimé) et reste blessée immobile 2 h 30, puis chasse un gros mâle et emporte sa proie",
  lieu="Linyanti, Botswana", annee=2006)  # vérifié
E("babouin", 10, "leopard", 1, "A", 2, tb=["jeune"], qual="B",
  src="https://latestsightings.com/single-post/watch-leopard-outnumbered-by-50-baboons",
  note="Jeune mâle léopard saisit un babouin à la gorge, plusieurs mâles le plaquent et le mordent (effectif estimé), il lâche sa prise et est chassé", lieu="route de Satara, Kruger", annee=2023)  # corrigé : effectif estimé
E("leopard", 1, "babouin", 1, "A", 3, ta=["embuscade"], qual="B",
  src="https://latestsightings.com/single-post/watch-baboons-fight-back-after-leopard-ambush",
  note="Léopard tue un babouin en embuscade (âge/sexe non précisés)", lieu="Singita Lebombo, Kruger", annee=2024)  # vérifié
E("babouin", 10, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/watch-baboons-fight-back-after-leopard-ambush",
  note="La troupe (effectif estimé) poursuit et confronte ensuite le léopard qui fuit en laissant sa proie (coups non clairement décrits)", lieu="Singita Lebombo, Kruger", annee=2024)  # corrigé : effectif estimé

E("leopard", 1, "crocodile_nil", 1, "A", 2, ta=["embuscade"], qual="B",
  src="https://www.discovermagazine.com/in-battle-of-african-titans-leopard-vanquishes-crocodile-28158",
  note="Léopard attaque un crocodile à un point d'eau et le tient par la nuque jusqu'à la victoire (mort non confirmée explicitement)", lieu="Afrique du Sud", annee=2008)  # corrigé : m 3→2 (mort du croc non confirmée)
E("crocodile_nil", 1, "leopard", 1, "A", 2, ta=["eau"], tb=["blesse"], qual="B",
  src="https://jacarandafm.com/shows/sunday-breakfast-boost/leopard-meets-cruel-fate-jaws-crocodile",
  note="Crocodile saisit un léopard apparemment affaibli et l'entraîne vers la rivière (mort non confirmée)", lieu="Lower Sabie, Kruger")  # corrigé : m 3→2

# supprimé : ligne « deux ratels vs léopard » (S30) — le léopard recule sans contact
E("ratel", 1, "leopard", 1, "A", 1, ta=["defense_petits"], qual="C", src="https://getaway.co.za/?p=15472287",
  note="Mère ratel s'interpose face à un léopard qui s'en prenait à son petit (« sauvetage » selon le titre, déroulé non décrit)", lieu="Kruger", annee=2021)  # corrigé : qual B→C

# ---------------------------------------------------------------------------
# CROCODILE vs HIPPO / ÉLÉPHANT
# ---------------------------------------------------------------------------
E("hippopotame", 10, "crocodile_nil", 1, "A", 1, ta=["eau"], qual="B",
  src="https://latestsightings.com/single-post/30-hippos-attack-one-crocodile",
  note="Groupe de 30+ hippos (une dizaine au contact, effectif estimé) secoue et mord un crocodile qui s'échappe indemne", lieu="Hippo Pool, Serengeti", annee=2022)  # vérifié
E("hippopotame", 2, "crocodile_nil", 1, "A", 3, ta=["defense_petits", "eau"], qual="C",
  src="https://www.nzherald.co.nz/world/hippos-kill-crocodile/IQRJU7XMBG62JLHBK73OPZO5BI",
  note="Crocodile trop près d'une mère hippo ; des hippos le tuent (légende photo, effectif estimé)", lieu="Nil")  # corrigé : qual B→C (légende de photo seulement)
E("elephant", 1, "crocodile_nil", 1, "A", 3, ta=["defense_petits"], qual="B",
  src="https://latestsightings.com/single-post/elephant-kills-crocodile-south-luangwa",
  note="Femelle allaitante sans défenses piétine et projette à mort un crocodile proche de son petit", lieu="South Luangwa, Zambie", annee=2022)  # corrigé : année 2021→2022
_TETZOO = "https://tetzoo.com/blog/2025/8/7/crocodiles-attack-elephants-still"
E("elephant", 1, "crocodile_nil", 1, "D", 1, tb=["eau"], qual="B", src=_TETZOO,
  note="Crocodile mord la trompe d'une femelle adulte, elle le tire hors de l'eau et il lâche ; tous indemnes", lieu="Luangwa, Zambie", annee=2010)  # corrigé : res A→D (le croc lâche, pas de victoire nette)
E("elephant", 4, "crocodile_nil", 1, "D", 1, ta=["defense_petits"], tb=["eau"], qual="B", src=_TETZOO,
  note="Crocodile saisit la trompe d'un éléphanteau, les autres éléphants interviennent, le crocodile lâche (effectif estimé)", lieu="Kruger", annee=2010)  # corrigé : res A→D
E("elephant", 1, "crocodile_nil", 1, "D", 1, tb=["eau"], qual="C", src=_TETZOO,
  note="Crocodile saisit le bout de la trompe puis lâche (vidéo)", lieu="Chobe, Botswana", annee=2012)  # corrigé : res A→D

# ---------------------------------------------------------------------------
# ÉLÉPHANT vs RHINOCÉROS
# ---------------------------------------------------------------------------
E("elephant", 1, "rhinoceros", 1, "A", 3, ta=["jeune"], count=63, qual="A",
  src="https://pachydermjournal.org/index.php/pachyderm/article/view/1058",
  note="Slotow, Balfour & Howison 2001 : 1991-2001, jeunes mâles adultes (17-25 ans, musth précoce) tuent 58 rhinos blancs et 5 noirs", lieu="Hluhluwe-iMfolozi, Afrique du Sud", annee=2001)  # vérifié (tag jeune retiré par corrections.py)
E("elephant", 1, "rhinoceros", 1, "A", 3, ta=["jeune"], count=49, qual="A",
  src="https://koedoe.co.za/index.php/koedoe/article/view/188",
  note="Slotow & van Dyk 2001 : « jusqu'à » 49 rhinos tués (estimation haute) par de jeunes mâles en musth précoce (1992-1996)", lieu="Pilanesberg, Afrique du Sud", annee=1996)  # corrigé : note (estimation haute)
E("elephant", 1, "rhinoceros", 1, "A", 2, tb=["defense_petits"], qual="B",
  src="https://latestsightings.com/single-post/elephant-tramples-rhino-and-baby-in-shocking-encounter",
  note="Éléphant (mâle en musth probable) renverse une mère rhino blanc, roule son petit dans la boue, tente de l'encorner, poursuite de 100 m ; pas de blessure grave", lieu="Shishangeni, Kruger", annee=2025)  # corrigé : nb 2→1 (seule la mère engagée), m 1→2 (fuite nette)

# ---------------------------------------------------------------------------
# GRANDS SINGES (chimpanzé, gorille)
# ---------------------------------------------------------------------------
_BOESCH = "https://www.eva.mpg.de/fileadmin/content_files/staff/boesch/pdf/behav_leopard_predation.pdf"
E("chimpanze", 6, "leopard", 1, "A", 1, count=9, qual="A", src=_BOESCH,
  note="Boesch 1991 (1985-1990) : 9 poursuites de léopards par des chimpanzés (ex. ≥ 7 individus l'assiègent 2 h 22 dans un trou, 7 le frappent avec une branche) ; contact rare (effectif estimé)", lieu="Taï, Côte d'Ivoire", annee=1990)  # corrigé : note (contact rare, effectif estimé)
E("leopard", 1, "chimpanze", 1, "A", 3, ta=["embuscade"], count=4, qual="A", src=_BOESCH,
  note="Même étude : 4 chimpanzés tués lors d'attaques de léopard (1 juvénile femelle de 9 ans, 1 femelle adulte, 1 mâle adulte mort d'infection, 1 petit de 2 ans présumé)", lieu="Taï, Côte d'Ivoire", annee=1990)  # corrigé : détail des victimes
E("chimpanze", 3, "leopard", 1, "D", 1, count=6, qual="A", src=_BOESCH,
  note="Même étude : 6 chimpanzés blessés (5-19 plaies) survivent à l'attaque ; le léopard repart (effectif estimé)", lieu="Taï, Côte d'Ivoire", annee=1990)  # corrigé : count 5→6 (6 blessés survivants publiés), res A→D (le léopard se désengage)
E("chimpanze", 6, "leopard", 1, "A", 3, tb=["jeune"], count=1, qual="B", src=_BOESCH,
  note="Hiraiwa-Hasegawa cité par Boesch : les chimpanzés de Mahale tuent le petit d'une femelle léopard (effectif estimé)", lieu="Mahale, Tanzanie")  # corrigé : qual A→B (citation sans détails)
E("leopard", 1, "gorille", 1, "A", 3, count=1, qual="C",
  src="https://rcastoragev2.blob.core.windows.net/21883131bae2b7b154ba43c8acfb9061/main.PMC10960106.pdf",
  note="Fay et al. 1995 (J. Hum. Evol. 29:93-99, cité par Potel 2024) : attaque et consommation de gorille(s) par un léopard ; âge/sexe non vérifiés (gorille adulte selon une thèse citant Fay, sexe inconnu), preuves surtout indirectes (restes, fèces) ; aucune attaque observée en 26 ans à Dzanga",
  lieu="République centrafricaine", annee=1995)  # corrigé : qual A→C (source primaire non consultable, âge/sexe inconnus)
_SOUTHERN = "https://link.springer.com/10.1038/s41598-021-93829-x"  # Southern et al. 2021, Sci Rep 11:14673
E("chimpanze", 9, "gorille", 2, "A", 1, tb=["defense_petits"], qual="A", src=_SOUTHERN,
  note="Southern et al. 2021 (06/02/2019) : ~9 mâles chimpanzés sautent sur le dos argenté et le frappent ; il projette une adolescente (grièvement blessée), 2 mâles écorchés ; il recule de 30 m avec son groupe (5 gorilles), un NOURRISSON tué (non mangé) ; dos argenté non blessé",
  lieu="Loango, Gabon", annee=2019)  # corrigé : effectifs engagés (9 vs dos argenté + mère), m 2→1 (combat réel coûteux, victime = nourrisson), source primaire
E("chimpanze", 8, "gorille", 2, "A", 2, tb=["defense_petits"], qual="A", src=_SOUTHERN,
  note="Second cas (11/12/2019) : le dos argenté (mâle adulte) fuit SANS contact ; ≥ 8 mâles chimpanzés attaquent deux femelles dans un arbre, l'une garde son petit, l'autre perd son nourrisson (tué, mangé par une femelle chimpanzé)",
  lieu="Loango, Gabon", annee=2019)  # corrigé : adversaires = 2 femelles (pas le dos argenté), na 27→8, source primaire
E("chimpanze", 8, "chimpanze", 1, "A", 3, count=99, qual="A",
  src="https://dienekes.blogspot.com/2014/09/murderous-chimps.html",
  note="Wilson et al. 2014 Nature : 152 meurtres (58 observés + 41 déduits comptés, 53 suspectés exclus), rapport médian attaquants:victime 8:1, 66 % intercommunautaires ; victimes surtout mâles (73 %) et nourrissons (infanticides inclus)",
  lieu="15 communautés, Afrique", annee=2014)  # corrigé : 15 communautés (pas 18), mention des nourrissons
E("gorille", 1, "gorille", 1, "A", 3, count=2, qual="B", src="https://doaj.org/article/fddf0e59dcf74059bc7e6bdc0523cbec",
  note="Potel et al. 2024 : 2 dos argentés (mâles adultes, âgés) morts de blessures attribuées (par déduction) à des combats avec un dos argenté extérieur ; femelle blessée survivante, 3e dos argenté mort sans blessure (chute)", lieu="Dzanga-Sangha, RCA", annee=2024)  # corrigé : count 3→2 (seuls 2 décès attribués à des combats), qual A→B (cause déduite)

# ---------------------------------------------------------------------------
# HUMAINS (mains nues, bâton, lance/machette ; armes à feu exclues)
# ---------------------------------------------------------------------------
_MAASAI = "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5872D7AE49E17FB99A13BDC9D9657A8D/S0030605312000907a.pdf/div-class-title-beyond-ritual-and-economics-maasai-lion-hunting-and-conservation-politics-div.pdf"
E("humain", 15, "lion", 1, "A", 3, ta=["arme_blanche"], count=19, qual="A", src=_MAASAI,
  note="Goldman et al. 2013 : chasses olamayio à la lance ; 2 (2005) + 6 (déc. 2006, une seule chasse) + 5 (2007) + 6 (2008) lions tués ; effectif non publié (exemple : 30 ilmurran ; une chasse kényane de 11 a échoué ; effectif estimé) (registre : seuls les décès sont recensés)",
  lieu="Manyara Ranch, Tanzanie", annee=2008)  # corrigé : note (registre de décès, 6 lions en une chasse, effectif estimé)
E("humain", 1, "lion", 1, "A", 3, ta=["arme_blanche"], qual="B", src="https://standardmedia.co.ke/counties/article/2001274641",
  note="Éleveur de 45 ans tue à la lance une lionne entrée dans son enclos (2 lions ; aide éventuelle non précisée)", lieu="Olare Motorogi, Mara", annee=2018)  # vérifié
E("humain", 1, "lion", 1, "A", 1, tb=["blesse"], qual="B", src="https://www.thezimbabwean.co/2015/09/man-fights-lion-with-bare-hands/",
  note="Homme à mains nues lutte ~30 min contre un lion affamé et blessé, le lion s'enfuit ; homme dans un état critique",
  lieu="Chiredzi, Zimbabwe", annee=2015)  # vérifié
E("humain", 2, "lion", 1, "A", 1, ta=["outil"], tb=["defense_petits"], qual="B", src="https://www.adomonline.com/?p=2201566",
  note="Lionne suitée griffe un garçon de 16 ans à la jambe ; son camarade de 17 ans la charge en criant et en secouant des branches, elle fuit (pas de contact humain→lion)", lieu="Victoria Falls, Zimbabwe")  # vérifié
# supprimé : ligne « homme désarmé lutte avec un lion » (Kagadi, 2022) — démenti (Misbar) : l'homme était une victime, le lion a été abattu par des soldats (arme à feu)

E("humain", 1, "leopard", 1, "A", 3, tb=["blesse"], qual="B", src="https://www.spacedaily.com/reports/Ageing_Farmer_Kills_Leopard_With_Bare_Hands_In_Kenya.html",
  note="Daniel M'Mburugu (73 ans) lâche sa machette, enfonce la main dans la gueule et arrache la langue ; le léopard meurt (blessé auparavant selon KWS)",
  lieu="Mont Kenya, Kenya", annee=2005)  # corrigé : tag blesse côté léopard
E("humain", 1, "leopard", 1, "A", 3, ta=["arme_blanche"], tb=["blesse"], qual="C", src="https://www.mentalfloss.com/article/80239/time-carl-akeley-killed-leopard-his-bare-hands",
  note="Carl Akeley étouffe une léoparde (déjà blessée par balle) qui l'attaquait, l'achève au couteau", lieu="Ogaden", annee=1896)  # corrigé : tags blesse + arme_blanche, lieu Ogaden
E("humain", 10, "leopard", 1, "A", 3, ta=["outil"], qual="B",
  src="https://nation.africa/kenya/counties/kwale/stray-leopard-injures-two-in-kwale-before-villagers-put-it-down-3994834",
  note="Léopard blesse 2 personnes ; de nombreux villageois armés (armes non précisées, pas d'arme à feu mentionnée ; effectif estimé) le tuent", lieu="Batani, Kwale, Kenya")  # corrigé : effectif estimé

E("humain", 5, "hyene", 1, "A", 3, ta=["outil"], qual="B",
  src="https://nation.africa/kenya/news/mother-wins-battle-after-hyena-attacks-home-in-laikipia-1009978",
  note="Hyène attaque une maison la nuit ; la mère la combat seule > 30 min avec du bois de chauffage, les voisins aident à la chasser, les villageois la tuent ensuite ; 5 blessés (dont 2 enfants)", lieu="Laikipia Ouest, Kenya")  # corrigé : note (déroulé, 5 blessés)
E("hyene", 1, "humain", 4, "A", 2, tb=["outil"], qual="B",
  src="https://nation.africa/kenya/counties/tana-river/four-injured-in-attack-by-a-hyena-in-a-tana-river-village-174238",
  note="Quatre hommes traquent une hyène avec des armes de fortune : grièvement blessés, la hyène s'enfuit (la police l'abat ensuite)", lieu="Wayu, Tana River, Kenya")  # vérifié

E("chimpanze", 1, "humain", 1, "A", 3, tb=["jeune"], count=7, qual="B",
  src="https://www.nationalgeographic.com/animals/article/chimps-and-people-are-clashing-in-rural-uganda-feature",
  note="Jeunes enfants enlevés et tués par des chimpanzés (≥ ~14 morts recensés ; 7 retenus : 10 moins les 3 de Muhororo déjà dans data_transverse) (registre : seuls les décès sont recensés)", lieu="Ouest de l'Ouganda", annee=2018)  # corrigé : count 10→7 (doublon avec data_transverse), mention registre
E("humain", 2, "chimpanze", 1, "A", 1, count=4, qual="B",
  src="https://www.nationalgeographic.com/animals/article/chimps-and-people-are-clashing-in-rural-uganda-feature",
  note="Parents/villageois poursuivent ou défient les chimpanzés qui lâchent l'enfant vivant (4 cas 2017-2018, sans contact ; effectif estimé)", lieu="Ouest de l'Ouganda", annee=2018)  # corrigé : na 3→2 (souvent la mère seule), note sans contact
# supprimé : ligne New Vision (Kyamajaka 2014) — mal décrite (le chimpanzé n'a pas été tué) et déjà comptée parmi les enfants tués
E("humain", 5, "chimpanze", 1, "A", 3, ta=["arme_blanche"], qual="B",
  src="https://www.nationalgeographic.com/animals/article/chimps-and-people-are-clashing-in-rural-uganda-feature",
  note="Fin 2018 : un chimpanzé mâle adulte tué à la lance par des villageois (effectif estimé)", lieu="Ouest de l'Ouganda (Hoima)", annee=2018)  # ajouté
E("humain", 5, "chimpanze", 1, "A", 3, ta=["outil"], tb=["jeune"], qual="B",
  src="https://www.nationalgeographic.com/animals/article/chimps-and-people-are-clashing-in-rural-uganda-feature",
  note="Fin 2018 : une jeune femelle chimpanzé battue à mort avec bâtons et pierres par des villageois (effectif estimé)", lieu="Ouest de l'Ouganda (Hoima)", annee=2018)  # ajouté

E("hippopotame", 1, "humain", 2, "A", 3, ta=["eau"], qual="B",
  src="https://archive.seattletimes.com/archive/19960524/2330965/guide-survives-harrowing-attack-by-persistent-hippo----4000--pounder-struck-3-times",
  note="Mâle hippo renverse un canoë : le guide Templer (27 ans, revolver jamais dégainé) revient secourir le pagayeur, est attaqué 3 fois et perd un bras ; le pagayeur Nemasango meurt", lieu="Zambèze, Zimbabwe", annee=1996)  # vérifié
E("humain", 1, "crocodile_nil", 1, "A", 1, ta=["outil", "defense_petits"], tb=["eau"], qual="B",
  src="https://www.cbsnews.com/news/zimbabwe-man-fistfights-crocodile-to-save-child",
  note="Père saute sur le dos du crocodile, frappe la tête et pique les yeux avec des roseaux ; il lâche le garçon de 11 ans (amputé d'une jambe), père blessé au bras", lieu="Mutoko, Zimbabwe", annee=2013)  # vérifié
