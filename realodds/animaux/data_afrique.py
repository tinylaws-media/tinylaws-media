"""Real Odds — animaux : rencontres documentées, cluster AFRIQUE.

Convention : a = vainqueur quand res="A" ; res="D" = match nul / désengagement après contact réel.
m : 1 = étroit, 2 = net, 3 = mort/consommé. Tags : voir guide.
Remarque : pour quelques études ne donnant qu'une proportion, les `count` sont reconstruits
à partir de la proportion publiée (indiqué dans la note par « compte reconstruit »).
"""

ENC = []


def E(a, na, b, nb, res, m=2, ta=(), tb=(), count=1, qual="B", src="", note="", lieu="", annee=None):
    ENC.append(dict(a=a, na=na, b=b, nb=nb, res=res, m=m, ta=list(ta), tb=list(tb), count=count,
                    qual=qual, src=src, note=note, lieu=lieu, annee=annee))


# ---------------------------------------------------------------------------
# LION vs HYÈNE (kleptoparasitisme, effectifs)
# ---------------------------------------------------------------------------
_LEHMANN = "https://par.nsf.gov/servlets/purl/10132938"  # Lehmann et al. 2017, Current Zoology 63:313-322
E("lion", 4, "hyene", 15, "A", 1, ta=["carcasse"], tb=["carcasse"], count=67, qual="A", src=_LEHMANN,
  note="Sessions alimentaires avec mâle(s) lion présent(s) : les lions gardent/prennent la nourriture dans 67 cas sur 93 (effectifs médians : 3-4 lions, 14 hyènes)",
  lieu="Masai Mara (Talek), Kenya", annee=2017)
E("hyene", 15, "lion", 4, "A", 1, ta=["carcasse"], tb=["carcasse"], count=26, qual="A", src=_LEHMANN,
  note="Même étude : les hyènes obtiennent ou gardent la nourriture malgré la présence de mâles lions dans 26 cas sur 93 (mobbing, médiane 4 hyènes par mob)",
  lieu="Masai Mara (Talek), Kenya", annee=2017)

_COOPER = "https://bestgamerst.netlify.app/host-https-ui.adsabs.harvard.edu/abs/1991AfJEc..29..130C"  # Cooper 1991 Afr J Ecol 29:130
E("hyene", 12, "lion", 3, "A", 1, ta=["carcasse"], tb=["carcasse"], count=2, qual="A", src=_COOPER,
  note="Sans mâle adulte, les hyènes chassent lionnes/subadultes des proies au-delà d'un rapport ~4:1 ; ces groupes perdent ~20 % de leur nourriture (compte reconstruit 2/10)",
  lieu="Savuti, Chobe, Botswana", annee=1991)
E("lion", 3, "hyene", 8, "A", 1, ta=["carcasse"], tb=["carcasse"], count=8, qual="A", src=_COOPER,
  note="Même étude : lionnes/subadultes conservent ~80 % des proies face aux hyènes (compte reconstruit 8/10)",
  lieu="Savuti, Chobe, Botswana", annee=1991)

_HYPROJ = "https://hyena-project.com/research-topics/conflict-with-lions/"
E("lion", 1, "hyene", 20, "A", 2, ta=["carcasse"], tb=["carcasse"], count=1, qual="A", src=_HYPROJ,
  note="Ngorongoro : un lion mâle adulte domine ou prend toujours la carcasse quel que soit le nombre de hyènes (synthèse du projet, Höner et al.)",
  lieu="Cratère du Ngorongoro, Tanzanie", annee=2002)
E("hyene", 12, "lion", 2, "A", 1, ta=["carcasse"], tb=["carcasse"], count=1, qual="A", src=_HYPROJ,
  note="Ngorongoro : les hyènes gardent/prennent la proie face à des lionnes ou jeunes mâles si elles sont au moins 6 fois plus nombreuses",
  lieu="Cratère du Ngorongoro, Tanzanie", annee=2002)
E("hyene", 9, "lion", 3, "A", 1, ta=["carcasse"], tb=["carcasse"], count=1, qual="A",
  src="https://www.timeshighereducation.com/node/38511",
  note="Hyènes à 3 contre 1 ou plus face à des lionnes : elles gardent la carcasse, sinon les lions mangent (étude de terrain, Kenya)",
  lieu="Masai Mara, Kenya")
E("lion", 1, "hyene", 1, "A", 3, count=1, qual="A",
  src="https://www.frontiersin.org/journals/ethology/articles/10.3389/fetho.2026.1901233/full",
  note="Trinkel & Kastberger 2005 (cité) : les lions mâles adultes causent l'essentiel de la mortalité des hyènes liée aux lions et empêchent le kleptoparasitisme",
  lieu="Etosha, Namibie", annee=2005)
E("lion", 4, "hyene", 20, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/twenty-hyenas-take-on-four-lions",
  note="1 jeune mâle + 3 lionnes gardent la proie face à un grand clan (~20) ; pas de blessé", lieu="Crocodile River, Kruger", annee=2026)
E("lion", 22, "hyene", 22, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/22-lions-chase-22-hyenas-from-a-hippo",
  note="Grande troupe (surtout lionnes) chasse 22 hyènes d'une carcasse d'hippopotame", lieu="Ngala, Grand Kruger", annee=2026)
E("lion", 1, "hyene", 15, "D", 1, ta=["carcasse", "defense_petits"], tb=["carcasse"], qual="B",
  src="https://blog.londolozi.com/2020/03/07/lioness-takes-on-15-hyenas/",
  note="Lionne Tsalala avec petit : chassée de son gnou puis revient deux fois disperser ~15 hyènes ; partage final de la carcasse",
  lieu="Londolozi, Afrique du Sud", annee=2020)
E("hyene", 8, "lion", 1, "A", 2, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/hyenas-mob-and-bite-lone-lioness-serondella",
  note="Lionne seule mordue de toutes parts par un clan, blessée, abandonne sa proie", lieu="Serondella, Chobe, Botswana", annee=2024)
E("hyene", 20, "lion", 1, "A", 1, tb=["jeune"], qual="B",
  src="https://whyevolutionistrue.com/2018/11/30/lion-attacked-by-hyenas-saved-by-pal/",
  note="Jeune mâle encerclé par plus de 20 hyènes, en difficulté (BBC Earth)", annee=2018)
E("lion", 2, "hyene", 20, "A", 1, ta=["jeune"], qual="B",
  src="https://whyevolutionistrue.com/2018/11/30/lion-attacked-by-hyenas-saved-by-pal/",
  note="L'arrivée du second mâle (Tatu) disperse les hyènes", annee=2018)
E("lion", 1, "hyene", 6, "D", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://www.upi.com/Odd_News/2023/08/29/africa-hyena-lion-attack/1811693324787/",
  note="Gros mâle charge un clan sur une carcasse et saisit une hyène ; le clan accourt, issue incertaine", lieu="Arathusa, Sabi Sand", annee=2023)

# ---------------------------------------------------------------------------
# LION vs BUFFLE
# ---------------------------------------------------------------------------
E("buffle", 6, "lion", 2, "A", 3, qual="B",
  src="https://latestsightings.com/single-post/stampeding-buffaloes-trample-lion-in-wild-chase",
  note="Un troupeau projette et piétine une lionne à mort, la seconde est chassée", lieu="Mestel Dam, Kruger", annee=2025)
E("buffle", 6, "lion", 1, "A", 3, qual="B",
  src="https://www.lafm.com.co/medio-ambiente/impactante-muerte-de-leona-que-fue-corneada-por-manada-de-bufalos",
  note="Lionne encornée et piétinée à mort par un troupeau", lieu="Kruger", annee=2020)
E("lion", 2, "buffle", 1, "A", 3, tb=["blesse"], qual="B",
  src="https://latestsightings.com/single-post/watch-male-lions-capture-buffalo-mother-and-calf",
  note="Deux mâles tuent une bufflonne blessée (qui en encorne un) puis son veau", lieu="S41, Kruger", annee=2025)
E("buffle", 4, "lion", 4, "A", 1, qual="B",
  src="https://latestsightings.com/single-post/watch-lions-attack-buffaloes-in-intense-kruger-battle",
  note="1 jeune mâle + 3 lionnes attaquent une vache ; elle se relève et 4 mâles buffles repoussent les lions", lieu="Lower Sabie, Kruger", annee=2025)
E("buffle", 8, "lion", 3, "D", 1, qual="B",
  src="https://latestsightings.com/single-post/brave-buffalos-stand-off-against-3-male-lions",
  note="Trois mâles face à un petit troupeau : une charge, le lion recule ; impasse", lieu="Napi Road, Kruger", annee=2026)
E("lion", 7, "buffle", 1, "A", 3, tb=["jeune"], qual="B",
  src="https://blog.londolozi.com/2017/09/14/an-epic-standoff-between-lions-and-buffalo/",
  note="6 lionnes + 1 mâle acculent une jeune vache au bord de l'eau, le mâle l'étouffe", lieu="Londolozi", annee=2017)
E("lion", 2, "buffle", 80, "D", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://blog.londolozi.com/2017/09/14/an-epic-standoff-between-lions-and-buffalo/",
  note="Un troupeau de ~80 buffles confronte un mâle et une lionne sur la carcasse pendant 1 h ; les lions gardent la carcasse", lieu="Londolozi", annee=2017)

# ---------------------------------------------------------------------------
# LION vs ÉLÉPHANT / HIPPO / RHINO / CROCODILE
# ---------------------------------------------------------------------------
_LOVERIDGE = "https://www.originalwisdom.com/wp-content/uploads/bsk-pdf-manager/2019/04/Loveridge-et-al_2006_Influence-of-drought-on-predation-of-elephant-calves-by-lions-savannah.pdf"
E("lion", 7, "elephant", 1, "A", 3, tb=["jeune"], count=41, qual="A", src=_LOVERIDGE,
  note="Loveridge et al. 2006 : 44 éléphants tués par des lions, âge moyen 2,4 ans (88 % < 4 ans), groupes de ~7 lionnes ; surtout veaux isolés en sécheresse",
  lieu="Hwange, Zimbabwe", annee=2003)
E("lion", 1, "elephant", 1, "A", 3, tb=["jeune"], count=3, qual="A", src=_LOVERIDGE,
  note="Même étude : un mâle seul tue un éléphanteau à 3 reprises (le plus âgé : 3 ans)", lieu="Hwange, Zimbabwe", annee=2003)
E("elephant", 2, "lion", 1, "A", 1, ta=["defense_petits"], count=1, qual="A", src=_LOVERIDGE,
  note="Deux femelles adultes défendent un jeune de 5-6 ans contre une lionne", lieu="Hwange, Zimbabwe", annee=2003)
E("elephant", 1, "lion", 1, "A", 1, ta=["jeune"], count=1, qual="A", src=_LOVERIDGE,
  note="Un jeune éléphant traîne un lion mâle sur ~10 m et s'échappe", lieu="Hwange, Zimbabwe", annee=2003)

E("lion", 9, "hippopotame", 1, "A", 3, ta=["jeune"], count=6, qual="B",
  src="https://www.zambiatourism.com/south-luangwa-lions-developing-a-taste-for-hippo/",
  note="Troupe de 9 (1 femelle adulte + 8 subadultes) tue 6 hippos en quelques mois (souvent jeunes en distrayant la mère)",
  lieu="South Luangwa, Zambie", annee=2015)
E("hippopotame", 1, "lion", 9, "A", 1, tb=["jeune"], count=1, qual="B",
  src="https://www.zambiatourism.com/south-luangwa-lions-developing-a-taste-for-hippo/",
  note="Même troupe : « beaucoup d'autres tentatives » échouées (nombre non précisé, compté 1)", lieu="South Luangwa, Zambie", annee=2015)
E("hippopotame", 1, "lion", 1, "A", 3, ta=["defense_petits"], qual="B",
  src="https://peopledaily.digital/news/kws-confirms-death-of-lion-after-attack-by-mother-hippo-in-maasai-mara",
  note="Le mâle Kiminati (11 ans) attaque un bébé hippo ; la mère contre-attaque, blessures mortelles (confirmé KWS)", lieu="Masai Mara, Kenya", annee=2026)
E("hippopotame", 1, "lion", 3, "A", 1, ta=["eau"], qual="B",
  src="https://latestsightings.com/single-post/watch-hippo-attack-3-lions-crossing-the-river",
  note="Hippo charge trois lions traversant un chenal, troupe dispersée, pas de blessé", lieu="Selinda, Botswana", annee=2025)
E("lion", 2, "hippopotame", 1, "A", 3, qual="B",
  src="https://latestsightings.com/single-post/hippos-desperate-attempt-to-save-friend-from-lions-zambia",
  note="Deux mâles éventrent un hippo à terre ; un second hippo s'approche, les lions partent, la victime meurt le lendemain", lieu="Ila Safari Lodge, Zambie", annee=2024)

_BRAIN = "https://rhinoresourcecenter.com/wp-content/uploads/2006/12/1175858056.pdf"
E("lion", 3, "rhinoceros", 1, "A", 3, tb=["jeune"], count=3, qual="A", src=_BRAIN,
  note="Brain et al. 1999 : trois mâles (~6 ans) tuent 3 rhinocéros noirs subadultes (3-4 ans) aux points d'eau en 1995 (rhino noir, pas blanc)",
  lieu="Etosha, Namibie", annee=1995)
E("rhinoceros", 1, "lion", 1, "A", 3, ta=["defense_petits"], count=1, qual="A", src=_BRAIN,
  note="Goddard 1966 (cité) : une femelle rhino noir tue un lion menaçant son petit", lieu="Tanzanie", annee=1966)
E("rhinoceros", 1, "lion", 3, "A", 2, tb=["jeune"], qual="B",
  src="https://latestsightings.com/single-post/lions-attack-black-rhino-trapped-in-mud",
  note="Trois jeunes mâles attaquent un rhino noir dans la boue ; il en éjecte un de son dos, charge, les lions abandonnent", lieu="Etosha, Namibie", annee=2025)
E("lion", 5, "rhinoceros", 1, "A", 3, tb=["blesse"], qual="B",
  src="https://latestsightings.com/single-post/watch-elephants-try-saving-stuck-rhino-from-hungry-lions",
  note="Rhino noir embourbé : la troupe le renverse, il se noie", lieu="Aus, Etosha", annee=2024)
E("elephant", 5, "lion", 5, "A", 1, qual="B",
  src="https://latestsightings.com/single-post/watch-elephants-try-saving-stuck-rhino-from-hungry-lions",
  note="Un troupeau d'éléphants charge et écarte temporairement les lions du rhino embourbé", lieu="Aus, Etosha", annee=2024)

E("lion", 5, "crocodile_nil", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/cornered-crocodile-forced-to-fight-off-five-lions",
  note="Crocodile sorti voler une proie, 5 lionnes prennent le dessus mais il regagne l'eau", lieu="Sabi Sand", annee=2025)
E("lion", 2, "crocodile_nil", 1, "A", 3, count=1, qual="B",
  src="https://panthera.org/blog-post/when-lions-hunt-elephants-and-crocs",
  note="Everatt (Panthera) : lions de Matusadona chassent « couramment » des crocodiles jusqu'à ~3,6 m hors de l'eau (pas de compte)",
  lieu="Matusadona, Zimbabwe", annee=2024)
E("lion", 1, "crocodile_nil", 1, "D", 1, tb=["eau"], qual="B",
  src="https://latestsightings.com/single-post/crocodile-attacks-male-lion-in-riverside-showdown",
  note="Crocodile happe un lion dans la rivière, tous deux sous l'eau ; le lion ressort et s'échappe", lieu="Sabie, Kruger", annee=2025)
E("crocodile_nil", 1, "lion", 1, "A", 3, ta=["eau", "embuscade"], tb=["jeune"], qual="B",
  src="https://risingsunnewspapers.co.za/video_of_the_day/watch-crocodile-snatches-lion-cub-during-dramatic-river-crossing/",
  note="Crocodile happe un lionceau lors d'une traversée")

# ---------------------------------------------------------------------------
# LION vs LÉOPARD / GUÉPARD / LYCAON / RATEL
# ---------------------------------------------------------------------------
E("lion", 2, "leopard", 1, "A", 3, qual="B",
  src="https://latestsightings.com/single-post/world-famous-three-rivers-leopard-found-dead-after-evidence-of-a-lion-attack",
  note="Femelle Three Rivers retrouvée mutilée près de deux lionnes (attribution aux lions probable, non vue)", lieu="Sabi Sand", annee=2026)
_HUNTER = "https://ora.ox.ac.uk/objects/uuid:f8d14a94-3c96-4127-bc17-7d4cfdc8677e/files/m41b799fd5f7329089f7fc5ae5c7386fa"
E("hyene", 1, "guepard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], count=64, qual="A", src=_HUNTER,
  note="Hunter et al. 2007 (cité par Broekhuis & Irungu 2016) : guépards perdent jusqu'à 12,9 % des proies, 78 % aux hyènes ; sur 639 proies → ~64 (compte reconstruit)",
  lieu="Serengeti, Tanzanie", annee=2007)
E("lion", 1, "guepard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], count=12, qual="A", src=_HUNTER,
  note="Même source : 15 % des pertes vont aux lions → ~12 proies sur 639 (compte reconstruit)", lieu="Serengeti, Tanzanie", annee=2007)
E("guepard", 4, "hyene", 1, "A", 1, ta=["carcasse", "jeune"], tb=["carcasse"], qual="A", src=_HUNTER,
  note="Inversion rare : une femelle guépard et ses 3 jeunes chassent une hyène de sa proie", lieu="Masai Mara, Kenya", annee=2015)
E("hyene", 1, "guepard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://blog.londolozi.com/2013/09/25/cheetah-on-the-backfoot/",
  note="Mâle guépard feule mais cède son impala à une hyène seule", lieu="Londolozi", annee=2013)

E("lion", 3, "lycaon", 10, "A", 3, qual="B",
  src="https://latestsightings.com/single-post/male-lion-ends-alpha-wild-dogs-reign-sabi-sands",
  note="Mâle + lionnes : le mâle tue la femelle alpha, une lionne tue un jeune chien (2 morts, ~20 % de la meute)", lieu="Sabi Sand", annee=2022)

E("lion", 1, "ratel", 1, "A", 3, qual="B", src="https://www.sundestinations.co.za/blog/?p=7115",
  note="Une lionne Ross tue un ratel après ~20 min de résistance acharnée", lieu="Afrique du Sud (Africa on Foot)", annee=2015)
E("lion", 1, "ratel", 1, "A", 3, tb=["jeune"], qual="B",
  src="https://latestsightings.com/single-post/mom-honey-badger-leaves-her-baby-to-the-lions-kruger-national-park",
  note="Trois mâles ; l'un emporte le petit ratel, la mère s'enfuit (sort incertain)", lieu="H9, Kruger", annee=2024)

# ---------------------------------------------------------------------------
# HYÈNE vs LYCAON / LÉOPARD
# ---------------------------------------------------------------------------
E("lycaon", 10, "hyene", 2, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/watch-wild-dogs-defend-kill-against-hungry-hyenas",
  note="Plus de 10 lycaons encerclent et harcèlent 2 hyènes qui abandonnent", lieu="Grand Kruger", annee=2015)
E("hyene", 6, "lycaon", 8, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/hyenas-steal-wild-dog-kill-twice-in-epic-battle",
  note="Un clan tue un lechwe puis surpasse la meute et lui prend sa proie", lieu="Okavango, Botswana", annee=2025)
E("hyene", 2, "lycaon", 5, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/lone-hyena-surrounded-by-a-pack-of-wild-dogs",
  note="Deux puis une seule hyène gardent l'essentiel de la carcasse malgré les attaques de quelques lycaons", annee=2026)
E("lycaon", 4, "hyene", 5, "D", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://blog.londolozi.com/2020/07/11/wild-dogs-vs-hyena-vs-leopard/",
  note="4 lycaons mangent malgré 5-6 hyènes, confrontation puis partage (les hyènes finissent les restes)", lieu="Londolozi", annee=2020)
E("lycaon", 4, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://blog.londolozi.com/2020/07/11/wild-dogs-vs-hyena-vs-leopard/",
  note="Le léopard abandonne sa proie et grimpe à l'arbre à l'arrivée de 4 lycaons", lieu="Londolozi", annee=2020)
E("leopard", 1, "lycaon", 1, "A", 3, tb=["jeune"], qual="B",
  src="https://latestsightings.com/single-post/wild-dogs-get-revenge-on-leopard-that-caught-a-puppy-chobe-national-park",
  note="Un léopard attrape un louveteau de lycaon", lieu="Savuti, Chobe", annee=2023)
E("lycaon", 8, "leopard", 1, "A", 1, qual="B",
  src="https://latestsightings.com/single-post/wild-dogs-get-revenge-on-leopard-that-caught-a-puppy-chobe-national-park",
  note="La meute attaque le léopard qui se réfugie dans un fourré, « relativement indemne »", lieu="Savuti, Chobe", annee=2023)

_BALME = "https://datadryad.org/dataset/doi:10.5061/dryad.gb794"
E("hyene", 1, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], count=340, qual="A", src=_BALME,
  note="Balme et al. 2017 : ≥21 % de 2032 proies de 104 léopards perdues, surtout aux hyènes ; ~80 % de ces pertes attribuées aux hyènes (compte reconstruit, souvent sans combat)",
  lieu="Sabi Sand, Afrique du Sud", annee=2015)
E("hyene", 2, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/hyenas-dominate-leopard-and-steal-its-kill",
  note="Deux hyènes surpassent le léopard (qui mord quelques fois) et prennent l'impala", lieu="Grand Kruger", annee=2025)
E("hyene", 1, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/leopard-fights-off-hyena-to-keep-her-kill",
  note="Une hyène seule finit par prendre la proie, le léopard repart blessé à une patte arrière", lieu="Sabi Sand", annee=2025)

# ---------------------------------------------------------------------------
# LÉOPARD vs BABOUIN / CROCODILE / RATEL
# ---------------------------------------------------------------------------
_BUSSE = "https://curtbusse.com/wp-content/uploads/2026/02/Busse1980.pdf"
E("leopard", 1, "babouin", 1, "A", 3, ta=["embuscade"], count=3, qual="A", src=_BUSSE,
  note="Busse 1980 : 6 attaques de léopard aux dortoirs, 3 adultes tués (2 femelles, 1 mâle)", lieu="Moremi, Botswana", annee=1979)
E("babouin", 20, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], count=1, qual="A", src=_BUSSE,
  note="Même étude : un léopard abandonne sa proie face à ~20 babouins menaçants (pas de blessure)", lieu="Moremi, Botswana", annee=1979)
E("leopard", 1, "babouin", 30, "A", 1, ta=["carcasse"], qual="B",
  src="https://wildernessdestinations.com/journal/your-guide-to-africa/leopard-left-for-dead-by-baboon-troop",
  note="Léoparde tue un jeune babouin, est assaillie par la troupe (~30) et reste immobile 2 h 30, puis chasse un gros mâle et emporte sa proie",
  lieu="Linyanti, Botswana", annee=2006)
E("babouin", 10, "leopard", 1, "A", 2, tb=["jeune"], qual="B",
  src="https://latestsightings.com/single-post/watch-leopard-outnumbered-by-50-baboons",
  note="Jeune mâle léopard saisit un babouin, la troupe (~50) l'attaque, il lâche sa prise et est chassé", lieu="route de Satara, Kruger", annee=2023)
E("leopard", 1, "babouin", 1, "A", 3, ta=["embuscade"], qual="B",
  src="https://latestsightings.com/single-post/watch-baboons-fight-back-after-leopard-ambush",
  note="Léopard tue un babouin en embuscade", lieu="Singita Lebombo, Kruger", annee=2024)
E("babouin", 10, "leopard", 1, "A", 1, ta=["carcasse"], tb=["carcasse"], qual="B",
  src="https://latestsightings.com/single-post/watch-baboons-fight-back-after-leopard-ambush",
  note="La troupe chasse ensuite le léopard qui fuit sans sa proie", lieu="Singita Lebombo, Kruger", annee=2024)

E("leopard", 1, "crocodile_nil", 1, "A", 3, ta=["embuscade"], qual="B",
  src="https://www.discovermagazine.com/in-battle-of-african-titans-leopard-vanquishes-crocodile-28158",
  note="Léopard tue un crocodile en le mordant à la nuque (photos, point d'eau)", lieu="Afrique du Sud", annee=2008)
E("crocodile_nil", 1, "leopard", 1, "A", 3, ta=["eau"], tb=["blesse"], qual="B",
  src="https://jacarandafm.com/shows/sunday-breakfast-boost/leopard-meets-cruel-fate-jaws-crocodile",
  note="Crocodile saisit un léopard affaibli et l'entraîne vers la rivière", lieu="Lower Sabie, Kruger")

E("ratel", 2, "leopard", 1, "A", 1, qual="B",
  src="https://latestsightings.com/single-post/leopard-humbled-after-picking-fight-with-2-honey-badgers",
  note="Deux ratels chargent un léopard qui recule puis se retire après un long face-à-face", lieu="S30, Kruger", annee=2026)
E("ratel", 1, "leopard", 1, "A", 1, ta=["defense_petits"], qual="B", src="https://getaway.co.za/?p=15472287",
  note="Mère ratel contre-attaque un léopard qui s'en prenait à son petit (« sauvetage » selon le titre)", lieu="Kruger", annee=2021)

# ---------------------------------------------------------------------------
# CROCODILE vs HIPPO / ÉLÉPHANT
# ---------------------------------------------------------------------------
E("hippopotame", 10, "crocodile_nil", 1, "A", 1, ta=["eau"], qual="B",
  src="https://latestsightings.com/single-post/30-hippos-attack-one-crocodile",
  note="Groupe de 30+ hippos (une dizaine au contact) secoue et mord un crocodile qui s'échappe", lieu="Hippo Pool, Serengeti", annee=2022)
E("hippopotame", 2, "crocodile_nil", 1, "A", 3, ta=["defense_petits", "eau"], qual="B",
  src="https://www.nzherald.co.nz/world/hippos-kill-crocodile/IQRJU7XMBG62JLHBK73OPZO5BI",
  note="Crocodile approche une mère hippo ; les hippos le tuent", lieu="Nil")
E("elephant", 1, "crocodile_nil", 1, "A", 3, ta=["defense_petits"], qual="B",
  src="https://latestsightings.com/single-post/elephant-kills-crocodile-south-luangwa",
  note="Femelle sans défenses piétine et projette à mort un crocodile qui menaçait son petit", lieu="South Luangwa, Zambie", annee=2021)
_TETZOO = "https://tetzoo.com/blog/2025/8/7/crocodiles-attack-elephants-still"
E("elephant", 1, "crocodile_nil", 1, "A", 1, tb=["eau"], qual="B", src=_TETZOO,
  note="Crocodile mord la trompe d'une femelle adulte, elle le tire hors de l'eau et il lâche", lieu="Luangwa, Zambie", annee=2010)
E("elephant", 4, "crocodile_nil", 1, "A", 1, ta=["defense_petits"], tb=["eau"], qual="B", src=_TETZOO,
  note="Crocodile saisit un jeune, les autres éléphants interviennent, le crocodile lâche", lieu="Kruger", annee=2010)
E("elephant", 1, "crocodile_nil", 1, "A", 1, tb=["eau"], qual="C", src=_TETZOO,
  note="Crocodile saisit le bout de la trompe puis lâche (vidéo)", lieu="Chobe, Botswana", annee=2012)

# ---------------------------------------------------------------------------
# ÉLÉPHANT vs RHINOCÉROS
# ---------------------------------------------------------------------------
E("elephant", 1, "rhinoceros", 1, "A", 3, ta=["jeune"], count=63, qual="A",
  src="https://pachydermjournal.org/index.php/pachyderm/article/view/1058",
  note="1991-2001 : jeunes mâles (17-25 ans, musth précoce) tuent 58 rhinos blancs et 5 noirs", lieu="Hluhluwe-iMfolozi, Afrique du Sud", annee=2001)
E("elephant", 1, "rhinoceros", 1, "A", 3, ta=["jeune"], count=49, qual="A",
  src="https://koedoe.co.za/index.php/koedoe/article/view/188",
  note="Slotow & van Dyk 2001 : jusqu'à 49 rhinos blancs tués par de jeunes mâles en musth précoce", lieu="Pilanesberg, Afrique du Sud", annee=1996)
E("elephant", 1, "rhinoceros", 2, "A", 1, tb=["defense_petits"], qual="B",
  src="https://latestsightings.com/single-post/elephant-tramples-rhino-and-baby-in-shocking-encounter",
  note="Éléphant renverse une mère rhino blanc sur son petit, tente de l'encorner, poursuite de 100 m ; pas de blessure grave", lieu="Shishangeni, Kruger", annee=2025)

# ---------------------------------------------------------------------------
# GRANDS SINGES (chimpanzé, gorille)
# ---------------------------------------------------------------------------
_BOESCH = "https://www.eva.mpg.de/fileadmin/content_files/staff/boesch/pdf/behav_leopard_predation.pdf"
E("chimpanze", 6, "leopard", 1, "A", 1, count=9, qual="A", src=_BOESCH,
  note="Boesch 1991 : 9 cas où des chimpanzés chassent un léopard (ex. 7-8 individus l'assiègent 2 h dans un trou, coups de bâton)", lieu="Taï, Côte d'Ivoire", annee=1990)
E("leopard", 1, "chimpanze", 1, "A", 3, ta=["embuscade"], count=4, qual="A", src=_BOESCH,
  note="Même étude : 4 chimpanzés tués lors d'attaques de léopard (morsure gorge/thorax)", lieu="Taï, Côte d'Ivoire", annee=1990)
E("chimpanze", 5, "leopard", 1, "A", 1, tb=[], count=5, qual="A", src=_BOESCH,
  note="Attaques où la victime survit blessée (5-19 plaies) ; le groupe accourt et le léopard part (compte = 9 attaques - 4 morts)", lieu="Taï, Côte d'Ivoire", annee=1990)
E("chimpanze", 6, "leopard", 1, "A", 3, tb=["jeune"], count=1, qual="A", src=_BOESCH,
  note="Hiraiwa-Hasegawa (cité) : les chimpanzés de Mahale tuent un léopardeau", lieu="Mahale, Tanzanie")
E("leopard", 1, "gorille", 1, "A", 3, count=1, qual="A",
  src="https://rcastoragev2.blob.core.windows.net/21883131bae2b7b154ba43c8acfb9061/main.PMC10960106.pdf",
  note="Fay et al. 1995 (cité par Potel 2024) : attaque et consommation de gorille(s) par un léopard ; aucune attaque observée en 26 ans de suivi à Dzanga",
  lieu="République centrafricaine", annee=1995)
E("chimpanze", 18, "gorille", 5, "A", 2, qual="A", src="https://africageographic.com/stories/chimps-kill-baby-gorillas",
  note="Southern et al. 2021 : ~9 mâles chimpanzés encerclent et chassent le dos argenté, un petit gorille tué", lieu="Loango, Gabon", annee=2019)
E("chimpanze", 27, "gorille", 5, "A", 2, qual="A", src="https://africageographic.com/stories/chimps-kill-baby-gorillas",
  note="Second cas : le dos argenté fuit, la mère encerclée par 8 mâles perd son petit, mangé", lieu="Loango, Gabon", annee=2019)
E("chimpanze", 8, "chimpanze", 1, "A", 3, count=99, qual="A",
  src="https://dienekes.blogspot.com/2014/09/murderous-chimps.html",
  note="Wilson et al. 2014 Nature : 152 meurtres (58 observés + 41 déduits comptés), rapport médian attaquants:victime 8:1, 66 % intercommunautaires",
  lieu="18 communautés, Afrique", annee=2014)
E("gorille", 1, "gorille", 1, "A", 3, count=3, qual="A", src="https://doaj.org/article/fddf0e59dcf74059bc7e6bdc0523cbec",
  note="Potel et al. 2024 : morts de 3 dos argentés et 1 femelle avec blessures attribuées à des combats entre gorilles (3 retenues)", lieu="RCA (gorilles de l'Ouest)", annee=2024)

# ---------------------------------------------------------------------------
# HUMAINS (mains nues, bâton, lance/machette ; armes à feu exclues)
# ---------------------------------------------------------------------------
_MAASAI = "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5872D7AE49E17FB99A13BDC9D9657A8D/S0030605312000907a.pdf/div-class-title-beyond-ritual-and-economics-maasai-lion-hunting-and-conservation-politics-div.pdf"
E("humain", 15, "lion", 1, "A", 3, ta=["arme_blanche"], count=19, qual="A", src=_MAASAI,
  note="Goldman et al. 2013 : chasses olamayio à la lance (les guerriers encerclent le lion) ; 2+6+5+6 lions tués 2005-2008 ; effectif ~10-30 guerriers",
  lieu="Manyara Ranch, Tanzanie", annee=2008)
E("humain", 1, "lion", 1, "A", 3, ta=["arme_blanche"], qual="B", src="https://standardmedia.co.ke/counties/article/2001274641",
  note="Éleveur de 45 ans tue à la lance une lionne entrée dans son enclos (2 lions)", lieu="Olare Motorogi, Mara", annee=2018)
E("humain", 1, "lion", 1, "A", 1, tb=["blesse"], qual="B", src="https://www.thezimbabwean.co/2015/09/man-fights-lion-with-bare-hands/",
  note="Homme à mains nues lutte ~30 min en tenant la gorge d'un lion affamé et blessé, le lion s'enfuit ; homme grièvement blessé",
  lieu="Chiredzi, Zimbabwe", annee=2015)
E("humain", 2, "lion", 1, "A", 1, ta=["outil"], tb=["defense_petits"], qual="B", src="https://www.adomonline.com/?p=2201566",
  note="Lionne suitée attaque un adolescent ; son camarade crie et secoue des branches, elle fuit ; blessé aux jambes", lieu="Victoria Falls, Zimbabwe")
E("humain", 1, "lion", 1, "D", 1, qual="C",
  src="https://www.sciencetimes.com/articles/37101/20220411/man-uganda-wrestled-ferocious-lion-leaving-severely-injured-killing-beast.htm",
  note="Homme désarmé lutte avec un lion errant, grièvement blessé ; le lion a ensuite été abattu par l'armée (récits contradictoires)", lieu="Kagadi, Ouganda", annee=2022)

E("humain", 1, "leopard", 1, "A", 3, qual="B", src="https://www.spacedaily.com/reports/Ageing_Farmer_Kills_Leopard_With_Bare_Hands_In_Kenya.html",
  note="Fermier de 73 ans lâche sa machette, enfonce la main dans la gueule et arrache la langue ; le léopard meurt (peut-être déjà blessé selon KWS)",
  lieu="Mont Kenya, Kenya", annee=2005)
E("humain", 1, "leopard", 1, "A", 3, qual="C", src="https://www.mentalfloss.com/article/80239/time-carl-akeley-killed-leopard-his-bare-hands",
  note="Carl Akeley étouffe à mains nues un léopard qui l'attaquait", lieu="Somalie", annee=1896)
E("humain", 10, "leopard", 1, "A", 3, ta=["outil"], qual="B",
  src="https://nation.africa/kenya/counties/kwale/stray-leopard-injures-two-in-kwale-before-villagers-put-it-down-3994834",
  note="Léopard blesse 2 personnes ; de nombreux villageois armés (armes non précisées, pas d'arme à feu mentionnée) le tuent", lieu="Kwale, Kenya")

E("humain", 5, "hyene", 1, "A", 3, ta=["outil"], qual="B",
  src="https://nation.africa/kenya/news/mother-wins-battle-after-hyena-attacks-home-in-laikipia-1009978",
  note="Hyène attaque une maison la nuit ; la mère la frappe avec une bûche, villageois la tuent ; plusieurs blessés", lieu="Laikipia, Kenya")
E("hyene", 1, "humain", 4, "A", 2, tb=["outil"], qual="B",
  src="https://nation.africa/kenya/counties/tana-river/four-injured-in-attack-by-a-hyena-in-a-tana-river-village-174238",
  note="Quatre hommes traquent une hyène : armes trop faibles, tous gravement blessés, ils fuient (la police l'abat ensuite)", lieu="Tana River, Kenya")

E("chimpanze", 1, "humain", 1, "A", 3, tb=["jeune"], count=10, qual="B",
  src="https://www.nationalgeographic.com/animals/article/chimps-and-people-are-clashing-in-rural-uganda-feature",
  note="Enfants enlevés et tués par des chimpanzés (≥ ~14 morts recensés, 10 retenus pour éviter les doublons)", lieu="Ouest de l'Ouganda", annee=2018)
E("humain", 3, "chimpanze", 1, "A", 1, count=4, qual="B",
  src="https://www.nationalgeographic.com/animals/article/chimps-and-people-are-clashing-in-rural-uganda-feature",
  note="Parents/villageois poursuivent les chimpanzés qui lâchent l'enfant (survivant)", lieu="Ouest de l'Ouganda", annee=2018)
E("humain", 5, "chimpanze", 1, "A", 3, ta=["outil"], qual="B", src="https://www.newvision.co.ug/news/1303425/chimpanzee-kidnaps-kills-boy",
  note="Mabale : le père récupère l'enfant, les habitants tuent le chimpanzé ravisseur", lieu="Bwikara, Ouganda", annee=2013)

E("hippopotame", 1, "humain", 2, "A", 3, ta=["eau"], qual="B",
  src="https://archive.seattletimes.com/archive/19960524/2330965/guide-survives-harrowing-attack-by-persistent-hippo----4000--pounder-struck-3-times",
  note="Hippo renverse un canoë : guide Templer (n'a pas pu dégainer, se débat à mains nues) perd un bras, un pagayeur meurt", lieu="Zambèze, Zimbabwe", annee=1996)
E("humain", 1, "crocodile_nil", 1, "A", 1, ta=["outil", "defense_petits"], tb=["eau"], qual="B",
  src="https://www.cbsnews.com/news/zimbabwe-man-fistfights-crocodile-to-save-child",
  note="Père saute sur le crocodile, frappe la tête et pique les yeux avec des roseaux ; il lâche l'enfant (amputé d'une jambe)", lieu="Mutoko, Zimbabwe", annee=2013)
