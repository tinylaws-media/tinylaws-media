"""Real Odds — animaux : rencontres documentées, cluster NORD (AMÉRIQUES / EURASIE / ARCTIQUE).

Convention : `a` = vainqueur quand res="A" ; res="D" = issue nulle / désengagement après contact réel.
na/nb = individus réellement engagés. m : 1 serré / déplacement, 2 net, 3 mort/tué.
Remarques générales :
- Beaucoup de lignes loup-ours / ours-ours / ours-puma sont des DÉPLACEMENTS SUR CARCASSE (tag "carcasse"),
  souvent sans contact physique lourd : ce sont des tests de dominance plus que des combats à mort.
- Quand une synthèse ne donne que des pourcentages, les counts sont arrondis (indiqué dans la note).
- Quand la taille de meute n'est pas donnée par rencontre, na des loups est une estimation (« effectif estimé »).
- « ours_noir » sert aussi pour l'ours noir d'Asie (U. thibetanus) dans les lignes tigre (masse comparable) ;
  « caiman » sert aussi pour le caïman à lunettes (C. crocodilus) au Venezuela ; « anaconda » (vert) sert de proxy
  pour l'anaconda jaune (E. notaeus) du Pantanal (lignes marquées).
- Les registres d'attaques mortelles (ours noir > humain) n'ont pas de dénominateur : biais en faveur de l'animal.
2e passage (vérification ligne par ligne, 11/2026) : chaque ligne porte # vérifié / # corrigé / # supprimé / # ajouté.
"""

ENC = []


def E(a, na, b, nb, res, m=2, ta=(), tb=(), count=1, qual="B", src="", note="", lieu="", annee=None):
    ENC.append(dict(a=a, na=na, b=b, nb=nb, res=res, m=m, ta=list(ta), tb=list(tb), count=count, qual=qual,
                    src=src, note=note, lieu=lieu, annee=annee))


_REG = " (registre : seuls les décès sont recensés)"
BALLARD = "Ballard, Carbyn & Smith 2003, 'Wolf interactions with non-prey', in Mech & Boitani (eds) Wolves, ch.10 — https://core.ac.uk/download/188128267.pdf"

# ---------------------------------------------------------------------------
# LOUP vs OURS BRUN (grizzli)
# ---------------------------------------------------------------------------
# Table 10.1 (COMPTES, pas des %) : 108 interactions hors Yellowstone. Issue : ours 38 (35 %), loups 19 (18 %),
# aucun 43 (40 %), les deux 3, inconnu 5. Seulement 26 (24 %) sont des combats/poursuites ; 62 aux sites
# d'alimentation (ours vainqueurs 22/22), 15 aux tanières. Loups plus nombreux 58, égalité 25, ours plus nombreux 21.
E("ours_brun", 1, "loup", 3, "A", 1, tb=["carcasse"], count=36, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique hors Yellowstone (Table 10.1) : l'ours l'emporte dans 38 des 108 interactions (36 non mortelles ici) ; aux sites d'alimentation l'ours gagne 22/22 ; surtout défense/vol de carcasse, contact rarement décrit (effectif estimé)", lieu="Amérique du Nord (Alaska, Canada)")  # vérifié (comptes du tableau ; effectif estimé)
E("ours_brun", 1, "loup", 3, "A", 3, count=2, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique : 2 loups tués par des grizzlis sur 108 interactions, surtout sur sites d'alimentation (effectif estimé)", lieu="Amérique du Nord")  # vérifié
E("loup", 3, "ours_brun", 1, "A", 1, count=16, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique : les loups l'emportent dans 19 des 108 (16 non mortelles ici), surtout près de leur tanière (ours chassé, souvent sans contact décrit) (effectif estimé)", lieu="Amérique du Nord")  # vérifié (note précisée)
E("loup", 3, "ours_brun", 1, "A", 3, count=3, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique : 3 ours tués par des loups sur 108 interactions (effectif estimé)", lieu="Amérique du Nord")  # vérifié
# supprimé : loup vs ours_brun "D" count=46 (43 « aucun vainqueur » + 3 « les deux ») — surtout co-présence sans contact ;
#   seuls 26/108 sont des combats/poursuites, déjà répartis dans les issues ours/loups ci-dessus.
# Yellowstone 1996-2001 (Table 10.2, D.W. Smith non publ.) : 58 interactions ; « même zone » 20 (34 %), ours défend
# une proie 11, ours vole une proie 11, loup traque l'ours 7 ; ours vainqueurs 40 %, indéterminé 40 %, loups ~20 %.
E("ours_brun", 1, "loup", 5, "A", 1, tb=["carcasse"], count=22, qual="A", src=BALLARD,
  note="Yellowstone 1996-2001 (Table 10.2) : l'ours gagne 23 des 58 interactions (40 %), en défendant (11) ou volant (11) une proie ; 1 retiré (cas Gunther & Smith ci-dessous) ; loups plus nombreux dans 76 % (effectif estimé)", lieu="Yellowstone", annee=2001)  # corrigé : 23→22 (doublon avec la ligne Druid Peak 17/06/2001)
E("loup", 5, "ours_brun", 1, "A", 1, count=10, qual="A", src=BALLARD,
  note="Yellowstone 1996-2001 : loups vainqueurs dans ~20 % des 58 (count arrondi, reste après 40 % ours + 40 % indéterminé ; hors 2 oursons tués) ; défense de tanière/proie, contact rarement décrit (effectif estimé)", lieu="Yellowstone", annee=2001)  # vérifié (arithmétique : 58 − 23 − 23 ≈ 12, dont 2 oursons)
E("loup", 5, "ours_brun", 1, "A", 3, tb=["jeune"], count=2, qual="A",
  src="https://webarchive.library.unt.edu/eot2008/20080916031905/http://nrmsc.usgs.gov/files/norock/products/Ursus-15-02-Gunther_Smith.pdf",
  note="Gunther & Smith 2004 (Ursus 15) : 2 oursons grizzlis PROBABLEMENT tués par des loups (Hayden, mâle, juillet ; Lamar, femelle, août 2001, 10 loups Druid Peak vus près d'une carcasse de bison) ; mort non observée, puma/ours noir non exclus (effectif estimé)", lieu="Yellowstone", annee=2001)  # corrigé : « probablement », détails
E("ours_brun", 1, "loup", 6, "A", 1, ta=["defense_petits"], tb=["carcasse"], qual="A",
  src="https://webarchive.library.unt.edu/eot2008/20080916031905/http://nrmsc.usgs.gov/files/norock/products/Ursus-15-02-Gunther_Smith.pdf",
  note="17/06/2001 : femelle grizzli avec 2 oursons prend une carcasse de wapiti à 6 loups Druid Peak (4 adultes, 2 d'un an) qui l'encerclent et la mordillent ~20 min ; aucun blessé (retirée de l'agrégat Table 10.2)",
  lieu="Lamar Valley, Yellowstone", annee=2001)  # corrigé : contact (morsures) précisé ; agrégat réduit de 1 pour éviter le doublon
# supprimé : grizzli mange la proie de 3 loups qui attendent à 50 m (YELL709) — les loups avaient fini de manger et cèdent sans aucune contestation ; probablement aussi dans la Table 10.2.
# supprimé : femelle + 2 grizzlis de 2 ans « repoussent » 5 loups (YELL709) — pas de carcasse, aucun contact, jugé ludique par des observateurs ; probablement aussi dans la Table 10.2.
E("loup", 6, "ours_brun", 1, "A", 1, tb=["carcasse"], qual="A",
  src="https://www.nps.gov/yell/learn/nature/upload/2022-Web-Wolf-Report.pdf",
  note="Rescue Creek (meute de 12 en fin d'année) : les loups défient un grizzli qui a pris leur wapiti ; l'ours se défend à coups de patte et est repoussé de la carcasse (légende photo) (effectif estimé)", lieu="Yellowstone", annee=2022)  # corrigé : effectif estimé (meute de 12, engagés non comptés)
E("ours_brun", 1, "loup", 1, "A", 3, qual="B",
  src="https://www.nps.gov/yell/learn/nature/upload/2022-Web-Wolf-Report.pdf",
  note="Loup adulte non collier de Wapiti Lake mort le 13/09/2022, cause « interspécifique (ours) » ; espèce d'ours non précisée (grizzli probable), circonstances inconnues", lieu="Yellowstone", annee=2022)  # corrigé : espèce d'ours non identifiée → qual A→B
E("ours_brun", 1, "loup", 1, "A", 3, tb=["jeune"], qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/550/556/2218",
  note="Jimenez et al. 2008 : louveteau femelle (20-22 kg ; meute de 4 adultes + 4 jeunes) tué par un grizzli près d'une carcasse d'orignal d'un an (traces fraîches de grizzli) ; 1er cas documenté dans l'Ouest des É.-U.", lieu="Jackson, Wyoming", annee=2005)  # corrigé : composition de meute, carcasse
E("ours_brun", 2, "loup", 5, "A", 1, tb=["carcasse"], qual="B",
  src="https://www.pulse.bot/science/news/a-yellowstone-grizzly-had-a-fierce-standoff-with-a-wolf-pack-it-was-caught-on-video-84d48a71-2b08-42dd-9361-db159f9b86bf/",
  note="Vidéo (relayée d'Outside) : grand mâle grizzli (+ un subadulte) fait reculer une meute sur une carcasse de bison noyé, 7/05/2026 ; contact non décrit (effectif estimé)", lieu="Yellowstone", annee=2026)  # corrigé : effectif estimé, contact non décrit

# ---------------------------------------------------------------------------
# LOUP vs OURS NOIR
# ---------------------------------------------------------------------------
# Table 10.3 : 26 interactions, loups plus nombreux dans 21 (81 %) ; loups gagnent 18 (69 %), ours 4 (15 %) ;
# 9 ours tués (surtout à leur tanière), 1 loup tué ; jeunes ours impliqués dans 9 (35 %).
E("loup", 3, "ours_noir", 1, "A", 3, count=9, qual="A", src=BALLARD,
  note="9 ours noirs tués par des loups sur 26 interactions, la plupart cherchés dans leur tanière (ours en hibernation, souvent jeunes) (effectif estimé)", lieu="Amérique du Nord (Minnesota, Alberta, Manitoba)")  # corrigé : « 6 en tanière » non vérifiable → « la plupart » ; effectif estimé
E("loup", 3, "ours_noir", 1, "A", 2, count=9, qual="A", src=BALLARD,
  note="Loups vainqueurs non mortels (18 victoires sur 26 − 9 mortelles) (effectif estimé)", lieu="Amérique du Nord")  # vérifié
E("ours_noir", 1, "loup", 1, "A", 3, qual="A", src=BALLARD,
  note="1 loup tué par un ours noir près d'une tanière de loups (Rogers & Mech 1981)", lieu="NE Minnesota")  # vérifié
E("ours_noir", 1, "loup", 1, "A", 1, count=3, qual="A", src=BALLARD,
  note="Ours noirs vainqueurs non mortels (4 victoires sur 26 − 1 mortelle) (effectif estimé)", lieu="Amérique du Nord")  # vérifié
E("loup", 3, "ours_noir", 1, "D", 1, count=4, qual="A", src=BALLARD,
  note="Interactions sans vainqueur net (26 − 18 − 4) ; contact non garanti (effectif estimé)", lieu="Amérique du Nord")  # vérifié (arithmétique)
E("ours_noir", 1, "loup", 1, "A", 1, tb=["carcasse"], qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/977/982/3907",
  note="Fremmerlid & Latham 2009 : ours noir adulte, sur la proie (caribou) d'un loup solitaire, le charge et le chasse (< 1 m entre eux), aucun blessé", lieu="Wabasca, NE Alberta", annee=2002)  # vérifié

# ---------------------------------------------------------------------------
# LOUP vs PUMA
# ---------------------------------------------------------------------------
E("loup", 5, "puma", 1, "A", 3, count=3, qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/2461/2339/0",
  note="Ruth, Buotte & Hornocker 2019 (Yellowstone Cougars ; compte rendu de J. Way, CFN 133) : au moins 3 pumas adultes tués par des loups (1998-2005) (effectif estimé)", lieu="Northern Range, Yellowstone", annee=2005)  # vérifié
E("loup", 5, "puma", 1, "A", 3, tb=["jeune"], count=5, qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/2461/2339/0",
  note="Ruth et al. 2019 : 5 chatons de puma tués par des loups (effectif estimé)", lieu="Yellowstone", annee=2005)  # vérifié
E("loup", 5, "puma", 1, "A", 3, count=2, qual="A",
  src="https://www.eurekalert.org/news-releases/1113729",
  note="Binder et al. 2026 PNAS : 2 des 12 morts de pumas adultes (2016-2024) dues aux loups, sans terrain d'échappement ; les loups mangent le wapiti du puma ; aucun des 90 loups morts tué par un puma (effectif estimé)", lieu="Yellowstone", annee=2024)  # vérifié
E("loup", 8, "puma", 1, "A", 1, tb=["carcasse"], count=2, qual="A",
  src="https://objects.lib.uidaho.edu/twrs/AKENSON__J_J__H_A_2005_Effects_Wolf_Cougars.pdf",
  note="Akenson et al. 2005 : 2 pumas mis dans un arbre par la meute Chamberlain (7-10 loups en hiver), qui prend leurs proies (cerf mulet, mouflon) ; sans contact (effectif estimé)", lieu="Big Creek, Idaho", annee=2002)  # corrigé : sans contact, effectif estimé
E("puma", 1, "loup", 1, "A", 3, count=3, qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/550/556/2218",
  note="Jimenez et al. 2008 : 3 loups tués par des pumas (perforation/fracture du crâne) — femelle adulte seule (Drummond MT 1996), femelle de Mill Creek (Paradise Valley MT 2003, 2 loups voyageaient ensemble ; puma suitée), jeune mâle sain (Turner Valley AB 2006)", lieu="Montana / Alberta", annee=2006)  # corrigé : tag embuscade retiré (non documenté), détails des 3 cas
E("puma", 1, "loup", 1, "A", 3, count=6, qual="B",
  src="https://www.kuow.org/stories/in-a-battle-of-apex-predators-cougars-are-killing-wolves-at-a-surprising-rate",
  note="6 loups (à collier) tués par des pumas en ~10 ans dans l'État de Washington (perforations du crâne) ; circonstances non publiées, loups isolés supposés (effectif estimé)", lieu="Washington", annee=2022)  # corrigé : tag embuscade retiré (hypothèse de l'article), effectif estimé

# ---------------------------------------------------------------------------
# LOUP vs COYOTE (Merkle, Stahler & Smith 2009, Can. J. Zool. 87:56-63 ; aussi Intermountain J. Sci. 14:4, 2008)
# 337 interactions 1995-2007 ; 75 % aux carcasses ; loups dominent 91 % (≈307) ; 79 % (≈266, dénominateur 337)
# poursuites sans contact ; 25 coyotes tués ; loups plus nombreux dans 39 % seulement (80 % des cas mortels) ;
# 18 cas où les coyotes, non en infériorité, chassent/attaquent/harcèlent les loups.
# ---------------------------------------------------------------------------
MERKLE = "Merkle, Stahler & Smith 2009, Can. J. Zool. 87:56 — https://next.sciencegate.app/document/10.1139/z08-136 ; https://arc.lib.montana.edu/ojs/index.php/IJS/article/view/2162/1816"
E("loup", 2, "coyote", 1, "A", 3, count=25, qual="A", src=MERKLE,
  note="25 coyotes tués par des loups sur 337 interactions ; loups plus nombreux dans 80 % de ces cas mortels (effectif estimé)", lieu="Yellowstone", annee=2007)  # vérifié
E("loup", 1, "coyote", 1, "A", 1, count=16, qual="A", src=MERKLE,
  note="Loups dominants avec contact, coyote survivant (count dérivé : 307 dominés − 266 poursuites sans contact − 25 mortels) ; blessures non détaillées (effectif estimé)", lieu="Yellowstone", annee=2007)  # corrigé : 46→16 (79 % porte sur les 337), m 2→1
E("loup", 1, "coyote", 2, "A", 1, tb=["carcasse"], count=200, qual="A", src=MERKLE,
  note="Loup chasse le(s) coyote(s) SANS contact sur une carcasse (count dérivé : 266 poursuites sans contact × 75 % aux carcasses) ; loups en infériorité ou égalité dans 61 % des interactions (effectif estimé)", lieu="Yellowstone", annee=2007)  # corrigé : 236→200 ; ~66 poursuites sans contact hors carcasse supprimées (simple fuite)
E("coyote", 2, "loup", 1, "A", 1, tb=["carcasse"], count=18, qual="A", src=MERKLE,
  note="18 interactions où des coyotes, non en infériorité numérique, chassent ou attaquent/harcèlent des loups ; issue et contact non détaillés (effectif estimé)", lieu="Yellowstone", annee=2007)  # corrigé : 30→18 (les 9 % non dominés par les loups ne sont pas des victoires de coyotes)
E("loup", 1, "coyote", 3, "A", 1, ta=["blesse"], tb=["carcasse"], qual="B",
  src="https://kmhk.com/watch-lone-wolf-fends-off-coyotes-for-dead-bison-in-yellowstone-national-park/",
  note="Loup solitaire blessé à une patte s'approche de coyotes sur une carcasse de bison ; brève bagarre, les coyotes lui laissent la carcasse (effectif estimé : « une bande » de coyotes)", lieu="NE d'Elk Creek, Yellowstone", annee=2021)  # corrigé : source lisible (Yahoo bloqué), année, effectif estimé

# ---------------------------------------------------------------------------
# LOUP vs ORIGNAL (Isle Royale)
# ---------------------------------------------------------------------------
MECH = "Mech 1966, The Wolves of Isle Royale (Fauna Series 7) — https://npshistory.com/series/fauna/7/summary.htm"
E("loup", 15, "orignal", 1, "D", 1, count=36, qual="A", src=MECH,
  note="Sur 77 orignaux « testés » par la meute de 15-16 loups, 36 tiennent tête aux abois jusqu'à ce que les loups abandonnent ; aucun tué ; morsures non décrites dans le résumé (effectif estimé)", lieu="Isle Royale, Michigan", annee=1961)  # corrigé : orignal vainqueur → nul (res D, la meute renonce) ; la règle « orignaux aux abois » de corrections.py ne s'applique plus (même effet)
E("loup", 15, "orignal", 1, "A", 3, count=6, qual="A", src=MECH,
  note="6 orignaux tués sur 77 testés (efficacité 7,8 %), tous parmi les fuyards (le résumé n'en détaille que 5) ; 36 fuyards non tués exclus (pas de combat) (effectif estimé)", lieu="Isle Royale", annee=1961)  # vérifié (écart 5/6 interne à la source signalé)
E("loup", 3, "orignal", 1, "A", 3, tb=["vieux", "blesse"], qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/1030/1034/4117",
  note="Jordan, Peterson & LeDoux 2010 : 3 loups adultes poursuivent à la nage une femelle seule, deux lui montent sur le dos et la mordent au cou, elle les secoue ; retrouvée tuée sur la rive une semaine plus tard (~14 ans, arthrite) ; mise à mort non observée", lieu="Isle Royale", annee=2008)  # vérifié

# ---------------------------------------------------------------------------
# LOUP vs BISON (Yellowstone)
# ---------------------------------------------------------------------------
E("loup", 8, "bison", 1, "A", 3, ta=["jeune"], tb=["jeune", "blesse"], qual="A",
  src="https://webarchive.library.unt.edu/eot2008/20081105200338/http://www.npwrc.usgs.gov/resource/mammals/wlfbison/index.htm",
  note="Smith et al. 2000 (J. Mammal. 81:1128) : veau seul émacié tué par 8 loups d'un an, 21 jours après lâcher", lieu="Yellowstone", annee=1995)  # corrigé : tag jeune côté loups (loups d'un an)
E("loup", 8, "bison", 1, "A", 3, tb=["blesse"], count=13, qual="A",
  src="https://webarchive.library.unt.edu/eot2008/20081105200338/http://www.npwrc.usgs.gov/resource/mammals/wlfbison/index.htm",
  note="Smith et al. 2000 : 13 autres bisons tués 1995-1999 (14 en tout), tous en fin d'hiver, bêtes en mauvais état, blessées ou jeunes (mélange) (effectif estimé)", lieu="Yellowstone", annee=1999)  # vérifié (effectif estimé)
# supprimé : bison vs 11 loups (MacNulty et al. 2014) — ligne « indicative » sans compte publié, aucune rencontre précise.
E("loup", 14, "bison", 1, "D", 1, tb=["defense_petits"], qual="A",
  src="https://www.nps.gov/yell/learn/nature/upload/2014-wolf-report.pdf",
  note="Une vache bison protège avec succès son veau tardif (novembre) contre la meute Prospect Peak (14 loups) ; la meute renonce (effectif estimé : taille de meute)", lieu="Yellowstone", annee=2014)  # corrigé : bison vainqueur → nul (attaquant qui renonce), effectif estimé
E("loup", 5, "bison", 6, "D", 1, tb=["blesse"], qual="B",
  src="https://cowboystatedaily.com/2023/09/15/video-shows-yellowstone-wolf-pack-fail-in-rare-attempt-to-take-down-bison",
  note="Meute Junction Butte : quelques loups mordillent les pattes arrière d'un bison isolé (peut-être boiteux) ; il rejoint le troupeau qui forme un mur de cornes ; les loups renoncent (effectif estimé)", lieu="Lamar Valley, Yellowstone", annee=2023)  # corrigé : bison vainqueur → nul, effectif estimé
E("loup", 10, "bison", 1, "A", 3, tb=["blesse"], qual="B",
  src="https://cowboystatedaily.com/2024/01/22/wolf-pack-takes-down-bison-on-firehole-river-in-yellowstone-standoff",
  note="Meute Wapiti Lake encercle un bison isolé, saignant (blessé ou malade avant ?), dans la Firehole ; les loups finissent par le tuer (récits de photographes) (effectif estimé)", lieu="Firehole River, Yellowstone", annee=2024)  # corrigé : tag blesse (bison apparemment blessé), effectif estimé

# ---------------------------------------------------------------------------
# COYOTE vs BISON
# ---------------------------------------------------------------------------
E("coyote", 1, "bison", 1, "A", 3, tb=["jeune"], qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/974/979/3895",
  note="Sheldon et al. 2009 : le mâle alpha M361 (6 ans) tue en ~3,5 h un veau nouveau-né (≈2× son poids) laissé par le troupeau ; le veau rue et le frappe à la tête", lieu="Lamar River, Yellowstone", annee=2009)  # vérifié

# ---------------------------------------------------------------------------
# OURS BRUN vs BISON
# ---------------------------------------------------------------------------
E("ours_brun", 1, "bison", 1, "A", 3, ta=["jeune"], tb=["jeune"], qual="B",
  src="https://www.fieldandstream.com/conservation/grizzly-bear-attacks-bison-yellowstone-video/",
  note="Grizzli subadulte (2-4 ans, 90-110 kg) maîtrise en ~17 min une femelle bison d'un an (~230 kg) isolée", lieu="Grand Prismatic, Yellowstone", annee=2020)  # vérifié
E("bison", 1, "ours_brun", 1, "A", 1, ta=["defense_petits"], qual="B",
  src="https://www.foxweather.com/earth-space/yellowstone-bear-mother-bison",
  note="Une mère bison charge un grizzli (6-7 ans) qui traquait les jeunes et le chasse ; contact non décrit", lieu="Lamar Valley, Yellowstone", annee=2023)  # vérifié

# ---------------------------------------------------------------------------
# TIGRE vs OURS (Extrême-Orient russe)
# ---------------------------------------------------------------------------
SERYODKIN = ("Seryodkin, Miquelle, Goodrich, Kostyria & Petrunenko 2018, Biology Bulletin 45:853 — "
             "https://journals.rcsi.science/1062-3590/article/view/182870 (résumé : ours = 2,2 % des 763 proies ≈ 17 ; "
             "ventilation par espèce et comptes de vols via le forum https://wildfact.com/forum/showthread.php?pid=65104, non vérifiés dans l'article)")
E("tigre", 1, "ours_brun", 1, "A", 3, count=5, qual="B", src=SERYODKIN,
  note="Sikhote-Aline 1992-2013 : ~15 ours tués par des tigres (résumé de l'article : ~17 ours parmi 763 proies) ; selon le résumé de forum, 7 ours bruns dont 5 femelles adultes (souvent par des tigres mâles adultes) ; ventilation non vérifiée (7 ou 9 selon les messages)", lieu="Sikhote-Aline, Russie", annee=2013)  # corrigé : qual A→B (ventilation par espèce d'un forum), scindé adultes / immatures
E("tigre", 1, "ours_brun", 1, "A", 3, tb=["jeune"], count=2, qual="B", src=SERYODKIN,
  note="Idem : 2 ours bruns immatures (~1-4 ans) tués par des tigres (forum)", lieu="Sikhote-Aline, Russie", annee=2013)  # corrigé : partie de l'ancien count=7, tag jeune
E("tigre", 1, "ours_noir", 1, "A", 3, count=8, qual="B", src=SERYODKIN,
  note="Idem : ~8 ours noirs d'Asie (U. thibetanus, proxy ours_noir) tués par des tigres, dont 2 jeunes adultes (forum ; 8 ou 9 selon les messages)", lieu="Sikhote-Aline, Russie", annee=2013)  # corrigé : qual A→B (forum)
E("ours_brun", 1, "tigre", 1, "A", 1, tb=["carcasse"], count=11, qual="B", src=SERYODKIN,
  note="Idem : des ours prennent aux tigres 11 de leurs 378 proies (saison active), surtout à des tigresses ; l'article confirme le vol de proies sans le chiffrer ; espèce d'ours non ventilée (attribuée à ours_brun) ; contact non décrit", lieu="Sikhote-Aline", annee=2013)  # corrigé : qual A→B (chiffre du forum)
# supprimé : ours_brun vs tigre "D" count=7 (proies « partagées ») — l'article précise un partage « à tour de rôle », sans confrontation.
E("ours_brun", 1, "tigre", 1, "A", 3, count=12, qual="C",
  src="https://en.wikipedia.org/wiki/Ussuri_brown_bear",
  note="Rapport soviétique de 1973 : 12 cas connus d'ours bruns tuant des tigres, y compris des mâles adultes, tous ensuite mangés ; compilation historique non vérifiable (via International Wildlife 2009)", lieu="Extrême-Orient russe", annee=1973)  # corrigé : « surtout tigresses/jeunes » absent de la source → retiré ; qual C conservée
E("tigre", 1, "ours_brun", 1, "A", 3, tb=["jeune"], qual="B",
  src="https://m.washingtontimes.com/news/2015/jul/15/putins-tiger-boris-kills-and-eats-bear-russias-far/",
  note="Le tigre réintroduit « Boris » (jeune adulte) tue et mange un jeune ours brun (restes trouvés par la réserve, Interfax)", lieu="Réserve, région de l'Amour", annee=2015)  # vérifié

# ---------------------------------------------------------------------------
# OURS BRUN vs OURS POLAIRE
# ---------------------------------------------------------------------------
E("ours_brun", 1, "ours_polaire", 1, "A", 1, tb=["carcasse"], count=68, qual="A",
  src="https://www.rcinet.ca/eye-on-the-arctic/2015/12/04/small-grizzlies-dominate-bigger-polar-bears-study",
  note="Miller et al. 2015 (J. Mammal.) : 137 rencontres grizzli-ours polaire sur le tas d'os de baleine (2005-2007) ; les grizzlis déplacent complètement les ours polaires dans ~la moitié (count arrondi), SANS agression ouverte ni contact ; polaires soumis/évitants", lieu="Kaktovik, Alaska", annee=2007)  # vérifié (déplacement sans contact : tag carcasse, m=1)

# ---------------------------------------------------------------------------
# OURS NOIR vs PUMA (kleptoparasitisme)
# ---------------------------------------------------------------------------
ELBROCH = "Elbroch et al. 2015, Pumas, black bears and competition refuges — https://www.originalwisdom.com/wp-content/uploads/bsk-pdf-manager/2019/03/Elbroch-et-al_2015_Pumas-black-bears-and-competition-refuges_CT.pdf"
E("ours_noir", 1, "puma", 1, "A", 1, tb=["carcasse"], count=58, qual="A", src=ELBROCH,
  note="Caméras : des ours noirs chassent des pumas de 58 proies (29 Colorado + 29 Californie) ; contact non décrit", lieu="Colorado / Californie", annee=2014)  # corrigé : 47→58 (tous les déplacements sont des victoires de l'ours ; le retour ultérieur du puma n'annule pas le déplacement)
# supprimé : puma vs ours_noir count=10 « le puma revient sur sa proie » — revenir après le départ de l'ours n'est pas une victoire (pas de confrontation).
E("puma", 1, "ours_noir", 1, "A", 3, tb=["jeune"], qual="A", src=ELBROCH,
  note="Femelle puma adulte revient et tue une ourse de 3 ans (subadulte) qui l'avait chassée de sa proie", lieu="Mendocino NF, Californie", annee=2014)  # vérifié

# ---------------------------------------------------------------------------
# PUMA / OURS vs ALLIGATOR
# ---------------------------------------------------------------------------
E("puma", 1, "alligator", 1, "A", 3, qual="A",
  src="https://eaglehill.us/SENAonline/articles/SENA-9-4/30-McBride.shtml",
  note="McBride & McBride 2010 : un mâle adulte de panthère de Floride tue un alligator de 2,69 m (plus grand connu ; autres proies 0,46-1,52 m) ; kill trouvé, combat non observé", lieu="Big Cypress, Floride", annee=2008)  # vérifié
E("ours_noir", 1, "alligator", 2, "D", 1, tb=["eau"], qual="B",
  src="https://www.fieldandstream.com/stories/bear-vs-alligator-florida",
  note="Ours noir traversant le St. Johns à la nage : deux alligators se jettent sur lui, il donne un coup de patte et continue, sort indemne ; état des alligators inconnu", lieu="St. Johns River, Floride")  # corrigé : ours vainqueur → nul (les attaquants renoncent, pas de victoire nette)

# ---------------------------------------------------------------------------
# JAGUAR vs CAÏMAN / ANACONDA / PUMA
# ---------------------------------------------------------------------------
E("jaguar", 1, "caiman", 1, "A", 3, ta=["embuscade"], count=71, qual="A",
  src="https://bv.fapesp.br/en/publicacao/52743/predator-prey-interactions-jaguar-predation-on-caiman-in-a",
  note="Azevedo & Verdade 2012 (J. Zool. 286:200) : 71 des 114 caïmans yacare morts (62 %) attribués à la prédation (jaguar, toutes tailles y compris petits) ; morsure crânienne ; résistance non observée", lieu="Pantanal sud, Brésil")  # corrigé : note (prédation attribuée, toutes tailles)
E("jaguar", 1, "anaconda", 1, "A", 2, qual="B",
  src="https://www.futura-sciences.com/planete/breves/animaux-jaguar-filme-train-attaquer-anaconda-geant-amerique-sud-5992/",
  note="Jaguar filmé par des touristes attaquant un anaconda (au Pantanal : anaconda jaune, proxy) ; issue mortelle suggérée mais non confirmée", lieu="Pantanal", annee=2022)  # corrigé : m 3→2 (mort non confirmée), proxy anaconda jaune
E("jaguar", 1, "anaconda", 1, "A", 2, qual="B",
  src="https://www.bluradio.com/sociedad/increible-foto-muestra-el-feroz-duelo-entre-una-anaconda-y-un-jaguar-en-el-pantanal-rs15",
  note="Femelle jaguar « Ámbar » : l'anaconda (jaune au Pantanal, proxy) s'enroule sur son museau ; après quelques minutes elle se libère et le maîtrise (récit de F. Oliveira)", lieu="Pantanal, Brésil", annee=2025)  # corrigé : enroulé sur le museau (pas le corps), proxy anaconda jaune
# supprimé : jaguar vs puma (Cuiabá, 2026) — simple poursuite, le puma fuit, aucun contact décrit.

# ---------------------------------------------------------------------------
# CAÏMAN vs ANACONDA (Venezuela, caïman à lunettes = proxy caiman)
# ---------------------------------------------------------------------------
E("caiman", 1, "anaconda", 1, "A", 3, count=7, qual="A",
  src="https://anacondas.org/anacondas.org/fight.htm",
  note="Rivas et al. 1999 (Herp. Rev. 30:101) : 8 attaques de caïmans à lunettes (proxy) attribuées (6 mâles, 2 femelles) ; 7 anacondas morts (mâles ~2,7 m en moyenne ; femelle de 4,9 m/29 kg déjà blessée, morte d'infection 2 mois après) ; combats jusqu'à 5 h", lieu="Llanos, Venezuela", annee=1997)  # corrigé : 8→7 morts (1 survivante, ligne suivante)
E("caiman", 1, "anaconda", 1, "A", 2, tb=["jeune"], qual="A",
  src="https://anacondas.org/anacondas.org/fight.htm",
  note="Rivas et al. 1999 : petite femelle anaconda (1,52 m, 1,7 kg) tenue par un caïman (>90 cm SVL), lâchée à l'approche des chercheurs, gravement blessée mais survivante", lieu="Llanos, Venezuela", annee=1997)  # ajouté (scindé de la ligne précédente)
E("anaconda", 1, "caiman", 1, "A", 2, qual="A",
  src="https://anacondas.org/anacondas.org/subduing.htm",
  note="Rivas 2004 (Herp. Rev. 35:66) : femelle anaconda (~4,5 m) serre un grand caïman à lunettes (1,8 m) ; colonne apparemment brisée/disloquée ; issue finale non rapportée", lieu="Llanos, Venezuela", annee=1999)  # corrigé : m 3→2 (mort non rapportée)

# ---------------------------------------------------------------------------
# OURS POLAIRE vs MORSE
# ---------------------------------------------------------------------------
OVS = "Ovsyanikov 1995, Polar bear predation of walruses on Wrangel Island — https://www.arlis.org/docs/vol1/E/Walrus/Russian/Ovsyanikov.1995.PolarBearPredationWalrusWrangellIsland.BullM.pdf"
E("morse", 3, "ours_polaire", 1, "A", 1, count=3, qual="A", src=OVS,
  note="25 chasses observées ; 11 attaques avec contact sur morses adultes, toutes échouent ; dans 3 l'ours est blessé (défenses au museau/cou avec sang, au cou, à la patte) (effectif estimé : troupeau)", lieu="Cap Blossom, île Wrangel", annee=1990)  # corrigé : m 2→1 (blessures modérées)
E("ours_polaire", 1, "morse", 3, "D", 1, count=8, qual="A", src=OVS,
  note="Autres attaques avec contact sur adultes (8 des 11), l'ours renonce sans blessure notée (5 ours de Cap Blossom portaient des plaies de défenses) (effectif estimé)", lieu="Cap Blossom, île Wrangel", annee=1990)  # corrigé : morse vainqueur → nul (l'attaquant renonce) ; « 16 plaies » non trouvé dans la source → retiré
E("ours_polaire", 1, "morse", 1, "A", 3, tb=["jeune"], count=2, qual="A", src=OVS,
  note="Seuls succès sur 25 chasses : 2 veaux de l'année pris par la même femelle adulte solitaire ; l'auteur juge qu'un ours ne peut tuer un morse adulte à terre", lieu="Cap Blossom, île Wrangel", annee=1990)  # vérifié
E("ours_polaire", 1, "morse", 1, "A", 3, count=7, qual="A",
  src="https://www.bearbiology.org/download/interactions-between-polar-bears-and-overwintering-walruses-in-the-central-canadian-high-arctic/",
  note="Calvert & Stirling 1990 : 3 morses tués + 4 probablement tués par des ours en hiver aux polynies (1981-1989) ; âge/sexe non rapportés", lieu="Haut-Arctique canadien", annee=1989)  # vérifié
E("ours_polaire", 1, "morse", 1, "D", 1, tb=["eau"], count=3, qual="A",
  src="https://www.bearbiology.org/download/interactions-between-polar-bears-and-overwintering-walruses-in-the-central-canadian-high-arctic/",
  note="Calvert & Stirling 1990 : 3 morses blessés mais non tués (attaques non mortelles ; riposte non décrite)", lieu="Haut-Arctique canadien", annee=1989)  # corrigé : morse vainqueur → nul (survie ≠ victoire)

# ---------------------------------------------------------------------------
# CHIEN vs LOUP / OURS
# ---------------------------------------------------------------------------
E("loup", 2, "chien", 1, "A", 3, count=35, qual="A",
  src="https://largecarnivores.fi/large-carnivores-and-us/damages/damages-to-dogs.html",
  note="Kojola & Kuittinen : 43 attaques confirmées de loups sur chiens 1996-1999 (65 signalées − 22 non confirmées), 82 % des chiens tués ; surtout chiens courants/élan et spitz finlandais (souvent sous le gabarit du proxy) ; chiens de chasse souvent attaqués par ≥2 loups (effectif estimé)", lieu="Finlande", annee=1999)  # vérifié (43 × 82 % = 35)
E("loup", 2, "chien", 1, "D", 1, count=8, qual="A",
  src="https://largecarnivores.fi/large-carnivores-and-us/damages/damages-to-dogs.html",
  note="Idem : 18 % des chiens attaqués survivent ; issue non détaillée (effectif estimé)", lieu="Finlande", annee=1999)  # corrigé : loup vainqueur m=2 → nul (survie, issue inconnue)
E("chien", 1, "ours_brun", 1, "A", 1, count=19, qual="B",
  src="https://library.kab.ac.ug/Record/doaj-art-4a5c732b47bb4f2095a2d0cf5c495b48/Description",
  note="Smith & Herrero 2018 (Alaska 1880-2015) : quand des chiens interviennent, ils mettent fin à l'attaque d'ours dans 47,5 % des cas (count déduit en supposant n=40 ; ensemble des conflits : 88 % grizzlis, 11 % ours noirs) ; armes humaines non exclues", lieu="Alaska", annee=2015)  # corrigé : n=40 = hypothèse, la part 88 % porte sur tous les conflits
# supprimé : ours_brun vs chien count=21 — « le chien n'arrête pas l'attaque » sur l'humain n'est pas une défaite du chien face à l'ours (issue chien-ours inconnue).

# ---------------------------------------------------------------------------
# HUMAIN vs PUMA (sans arme à feu)
# ---------------------------------------------------------------------------
CA_LIONS = "https://tchester.org/sgm/lists/lion_attacks_ca.html"
E("humain", 1, "puma", 1, "A", 3, ta=["outil"], tb=["jeune"], qual="B",
  src="https://www.cbsnews.com/amp/colorado/news/travis-kauffman-mountain-lion-attacked-killed-colorado-fort-collins",
  note="T. Kauffman, coureur seul, mordu au poignet : bloque avec les mains, bâtons inefficaces, 2 coups de pierre, puis étouffe le jeune puma avec le pied ; ~20 points de suture au visage", lieu="Horsetooth Mountain, Colorado", annee=2019)  # vérifié
E("humain", 2, "puma", 1, "A", 1, ta=["outil"], qual="B",
  src="https://www.nbcnews.com/id/wbna16817149",
  note="Jim Hamm (70 ans) saisi par un puma ; sa femme Nell (65) frappe l'animal avec une bûche (stylo plié) jusqu'à ce qu'il lâche ; Jim grièvement blessé ; femelle abattue ensuite", lieu="Prairie Creek Redwoods, Californie", annee=2007)  # vérifié
E("humain", 4, "puma", 1, "A", 1, ta=["outil"], qual="B", src=CA_LIONS,
  note="A. Hjelle saisie à la tête ; D. Nicholls la tient par les jambes, N. Magnuson et M. Castellano jettent des pierres ; le puma lâche (abattu ensuite)", lieu="Whiting Ranch, Californie", annee=2004)  # corrigé : na 3→4 (victime incluse, comme les autres lignes)
E("humain", 4, "puma", 1, "A", 1, ta=["arme_blanche", "outil"], qual="B", src=CA_LIONS,
  note="Femme de 27 ans attaquée, 3 compagnons ; 2 coups de couteau à l'épaule peu efficaces puis pierres à la tête ; le puma lâche, victime perd un œil (effectif estimé)", lieu="Johnsondale, Californie", annee=2004)  # vérifié
E("humain", 3, "puma", 1, "A", 1, ta=["arme_blanche", "outil"], tb=["blesse"], qual="B", src=CA_LIONS,
  note="Puma enragé : plusieurs personnes lui sautent dessus, coups de couteau à pain ; T. Winslow perd un pouce en le saisissant près de la gueule (effectif estimé)", lieu="Dos Rios, Californie", annee=1994)  # corrigé : effectif estimé (« d'autres »)
E("humain", 1, "puma", 1, "A", 1, ta=["outil"], qual="B", src=CA_LIONS,
  note="Cycliste seul (S. Fike, 27 ans) repousse le puma à coups de pierres ; puma abattu ensuite", lieu="Mount Lowe, Californie", annee=1995)  # vérifié
E("humain", 1, "puma", 1, "A", 1, ta=["outil"], qual="B", src=CA_LIONS,
  note="Un père atteint d'une pierre entre les yeux le puma qui emportait son fils de 9 ans ; le puma lâche l'enfant", lieu="Gaviota SP, Californie", annee=1992)  # vérifié
E("puma", 1, "humain", 1, "A", 3, qual="B", src=CA_LIONS,
  note="Barbara Schoener (40 ans), seule, se défend avec les bras, tuée (retirée de l'agrégat Mattson)", lieu="Auburn SRA, Californie", annee=1994)  # vérifié
# supprimé : Iris Kenna (56 ans), Cuyamaca 1994 — aucune résistance décrite (randonneuse seule) ; déjà dans l'agrégat Mattson.
E("puma", 1, "humain", 1, "A", 3, count=10, qual="A",
  src="https://core.ac.uk/download/77526645.pdf",
  note="Mattson et al. 2011 (1890-2008) : 200 attaques avec contact (29 mortelles) ; adultes = 51 % des victimes (≈102), létalité 10,9 % (≈11) ; aucun adulte en groupe d'adultes tué ; armes à feu non exclues ; 1 retiré (Schoener, ligne individuelle) ; count déduit de pourcentages", lieu="Amérique du Nord", annee=2008)  # corrigé : 11→10 (doublon Schoener ; Kenna laissée dans l'agrégat), année 2010→2008
E("humain", 1, "puma", 1, "A", 1, count=86, qual="B",
  src="https://core.ac.uk/download/77526645.pdf",
  note="Idem : adultes attaqués survivants (≈91 déduits − 5 cas individuels ci-dessus : Hamm, Hjelle, Johnsondale, Dos Rios, Fike) — attaque interrompue par la victime, des compagnons ou parfois une arme à feu ; à pondérer fortement", lieu="Amérique du Nord", annee=2008)  # corrigé : 91→86 (doublons), année

# ---------------------------------------------------------------------------
# HUMAIN vs OURS (sans arme à feu ni spray)
# ---------------------------------------------------------------------------
E("humain", 1, "ours_brun", 1, "A", 3, ta=["arme_blanche"], qual="B",
  src="https://www.themeateater.com/conservation/wildlife-management/a-knife-fight-with-a-brown-bear-the-story-of-gene-moe",
  note="Gene Moe, chasseur, fusil hors de portée, combat un ours brun ~270 kg au couteau de 10 cm jusqu'à ce que l'ours s'effondre, puis l'achève au fusil ; bras et cuisse déchiquetés, ~500-1000 points", lieu="Raspberry Island, Alaska", annee=1999)  # vérifié (achèvement au fusil déjà signalé)
E("humain", 1, "ours_brun", 1, "A", 1, ta=["arme_blanche", "outil"], qual="B",
  src="https://www.outsideonline.com/outdoor-adventure/exploration-survival/bear-attack-pocket-knife-canada-colin-dowler?scope=anon",
  note="Colin Dowler, attaque prédatrice d'un grizzli sain de 4-5 ans : bâton de marche, œil, puis canif de 7 cm au thorax et au cou ; l'ours lâche et s'éloigne en saignant ; graves blessures à la cuisse", lieu="Côte de C.-B., Canada", annee=2019)  # corrigé : tag outil (bâton de marche)
E("humain", 1, "ours_brun", 1, "A", 1, qual="B",
  src="https://930kmpt.com/montana-man-fights-off-griz-by-shoving-hand-down-bears-throat/",
  note="Chase Dellwo (30 ans), chasseur à l'arc (arc en bouclier, spray inutilisable par le vent), enfonce son poing dans la gorge d'un grizzli de ~180 kg (attaque défensive) ; l'ours s'enfuit ; lacérations tête et jambe", lieu="Rocky Mountain Front, Montana", annee=2015)  # vérifié
E("ours_brun", 1, "humain", 1, "A", 3, qual="B",
  src="https://en.wikipedia.org/wiki/List_of_fatal_bear_attacks_in_North_America",
  note="Randonneur seul (L. Crosby) tué par une femelle grizzli suitée (Yellowstone, août 2015)", lieu="Yellowstone", annee=2015)  # corrigé : statistique « 19 attaques mortelles 2000-2024 » non vérifiée → retirée
E("humain", 1, "ours_noir", 1, "A", 1, tb=["defense_petits"], qual="B",
  src="https://www.npr.org/2022/10/24/1130857186/a-washington-state-woman-fended-off-a-black-bear-attack",
  note="Femme frappe « en plein sur le nez » une ourse noire suitée de 2 oursons ; l'ourse s'enfuit ; blessures légères", lieu="Chelan County, Washington", annee=2022)  # vérifié
E("ours_noir", 1, "humain", 1, "A", 3, count=58, qual="A",
  src="https://www.sciencedaily.com/releases/2011/05/110511074807.htm?hl=en-CA",
  note="Herrero et al. 2011 : 63 personnes tuées en 59 incidents 1900-2009, toujours un seul ours, 88 % prédateurs (92 % mâles) ; armes non exclues ; 1 incident retiré (Liard River 1997, détaillé dans data_complements)" + _REG, lieu="Amérique du Nord", annee=2009)  # corrigé : 59→58 (doublon data_complements), mention registre
E("humain", 1, "ours_noir", 1, "A", 1, qual="B",
  src="https://www.startribune.com/bear-attacks-3-men-in-northern-minnesota-animal-located-shot-dead/465432873/",
  note="Bill Vagts (68 ans), à mains nues, saisit au cou un ours noir mâle adulte (~68 kg) qui attaquait son corgi et l'en arrache ; l'ours le mord au ventre et s'enfuit (abattu plus tard après 2 autres attaques)", lieu="Isabella, Minnesota", annee=2017)  # ajouté (humain à mains nues)

# ---------------------------------------------------------------------------
# HUMAIN vs LOUP
# ---------------------------------------------------------------------------
E("humain", 2, "loup", 1, "A", 1, tb=["vieux", "blesse"], ta=["outil"], qual="B",
  src="https://www.theweathernetwork.com/en/news/nature/animals/banff-national-park-wolf-attack-survivors-share-details-of-terrifying-ordeal",
  note="Loup attaque une tente ; le voisin R. Fee lui donne un coup de pied, M. Rispoli le plaque et lui tient la gueule à mains nues, puis pierres ; le loup lâche (vieux, en mauvais état, abattu ensuite)", lieu="Rampart Creek, Banff", annee=2019)  # vérifié
E("humain", 3, "loup", 1, "A", 1, qual="B",
  src="https://en.wikipedia.org/wiki/Wolf_attacks_in_North_America",
  note="S. Langevin attaqué dans son sac de couchage, se bat à mains nues ; un groupe d'autres campeurs chasse le loup (non enragé) (effectif estimé)", lieu="Vargas Island, C.-B.", annee=2000)  # corrigé : na 2→3, effectif estimé (« un groupe »)
E("loup", 2, "humain", 1, "A", 3, qual="B",
  src="https://en.wikipedia.org/wiki/Wolf_attacks_in_North_America",
  note="Kenton Carnegie, étudiant seul, tué par des loups habitués à une décharge ; résistance non documentée (effectif estimé)", lieu="Points North, Saskatchewan", annee=2005)  # corrigé : effectif estimé, résistance inconnue
E("loup", 2, "humain", 1, "A", 3, qual="B",
  src="https://en.wikipedia.org/wiki/Wolf_attacks_in_North_America",
  note="Candice Berner, joggeuse seule, tuée (attaque prédatrice, loups non enragés) ; résistance non documentée (effectif estimé)", lieu="Chignik Lake, Alaska", annee=2010)  # corrigé : effectif estimé, résistance inconnue
E("humain", 1, "loup", 2, "A", 1, ta=["outil"], qual="B",
  src="https://www.cbsnews.com/amp/minnesota/news/man-beats-back-wolves-to-save-dog-in-woods-near-duluth",
  note="Paul Moore frappe un des 2 loups qui attaquaient son labrador avec le manche de sa hache, se couche sur le chien et leur donne des coups de pied jusqu'à leur retraite ; chien mordu (5 plaies), homme indemne", lieu="Duluth, Minnesota", annee=2019)  # ajouté (1 humain vs 2 loups)
