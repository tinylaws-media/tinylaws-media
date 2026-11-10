"""Real Odds — animaux : rencontres documentées, cluster NORD (AMÉRIQUES / EURASIE / ARCTIQUE).

Convention : `a` = vainqueur quand res="A" ; res="D" = issue nulle / désengagement après contact réel.
na/nb = individus réellement engagés. m : 1 serré / déplacement, 2 net, 3 mort/tué.
Remarques générales :
- Beaucoup de lignes loup-ours / ours-ours / ours-puma sont des DÉPLACEMENTS SUR CARCASSE (tag "carcasse"),
  souvent sans contact physique lourd : ce sont des tests de dominance plus que des combats à mort.
- Quand une synthèse ne donne que des pourcentages, les counts sont arrondis (indiqué dans la note).
- Quand la taille de meute n'est pas donnée par rencontre, na des loups est une approximation (indiqué « ~ »).
- « ours_noir » sert aussi pour l'ours noir d'Asie (U. thibetanus) dans les lignes tigre (masse comparable) ;
  « caiman » sert aussi pour le caïman à lunettes (C. crocodilus) au Venezuela (lignes marquées).
- Les registres d'attaques mortelles (ours noir > humain) n'ont pas de dénominateur : biais en faveur de l'animal.
"""

ENC = []


def E(a, na, b, nb, res, m=2, ta=(), tb=(), count=1, qual="B", src="", note="", lieu="", annee=None):
    ENC.append(dict(a=a, na=na, b=b, nb=nb, res=res, m=m, ta=list(ta), tb=list(tb), count=count, qual=qual,
                    src=src, note=note, lieu=lieu, annee=annee))


BALLARD = "Ballard, Carbyn & Smith 2003, 'Wolf interactions with non-prey', in Mech & Boitani (eds) Wolves, ch.10 — https://core.ac.uk/download/188128267.pdf"

# ---------------------------------------------------------------------------
# LOUP vs OURS BRUN (grizzli)
# ---------------------------------------------------------------------------
# Amérique du Nord hors Yellowstone : 108 interactions (Table 10.1). Loups plus nombreux dans 54 %, égalité 23 %,
# ours plus nombreux 19 % -> na loups ~3 en moyenne. Ours gagnent 38, loups 19, aucun 43, les deux 3, inconnu 5.
E("ours_brun", 1, "loup", 3, "A", 1, tb=["carcasse"], count=36, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique hors Yellowstone : l'ours l'emporte (36 sur 108, hors 2 mortels) ; aux carcasses l'ours gagne 22/22 ; ~3 loups en moyenne", lieu="Amérique du Nord (Alaska, Canada)")
E("ours_brun", 1, "loup", 3, "A", 3, count=2, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique : 2 loups tués par des grizzlis sur 108 interactions, surtout sur sites d'alimentation", lieu="Amérique du Nord")
E("loup", 3, "ours_brun", 1, "A", 1, count=16, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique : les loups l'emportent (16 non mortels sur 19) ; gagnent surtout près de leur tanière", lieu="Amérique du Nord")
E("loup", 3, "ours_brun", 1, "A", 3, count=3, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique : 3 ours tués par des loups sur 108 interactions", lieu="Amérique du Nord")
E("loup", 3, "ours_brun", 1, "D", 1, count=46, qual="A", src=BALLARD,
  note="Synthèse N.-Amérique : 43 sans vainqueur + 3 « les deux gagnent » (combats/poursuites dans 24 % des cas)", lieu="Amérique du Nord")
# Yellowstone 1996-2001 (Table 10.2, D.W. Smith non publ.) : 58 interactions, loups plus nombreux dans 76 %.
E("ours_brun", 1, "loup", 5, "A", 1, tb=["carcasse"], count=23, qual="A", src=BALLARD,
  note="Yellowstone 1996-2001 : l'ours gagne ~40 % de 58 interactions (count arrondi), le plus souvent en défendant ou volant une carcasse ; meutes ~5", lieu="Yellowstone", annee=2001)
E("loup", 5, "ours_brun", 1, "A", 1, count=10, qual="A", src=BALLARD,
  note="Yellowstone 1996-2001 : loups vainqueurs dans ~20 % (count arrondi, hors 2 oursons tués)", lieu="Yellowstone", annee=2001)
E("loup", 5, "ours_brun", 1, "A", 3, tb=["jeune"], count=2, qual="A",
  src="https://webarchive.library.unt.edu/eot2008/20080916031905/http://nrmsc.usgs.gov/files/norock/products/Ursus-15-02-Gunther_Smith.pdf",
  note="Gunther & Smith 2004 (Ursus 15) : 2 oursons grizzlis probablement tués par des loups (Hayden et Lamar, 2001), près de carcasses", lieu="Yellowstone", annee=2001)
E("ours_brun", 1, "loup", 6, "A", 1, ta=["defense_petits"], tb=["carcasse"], qual="A",
  src="https://webarchive.library.unt.edu/eot2008/20080916031905/http://nrmsc.usgs.gov/files/norock/products/Ursus-15-02-Gunther_Smith.pdf",
  note="Femelle grizzli avec 2 oursons prend une carcasse de wapiti à 6 loups Druid Peak (4 adultes, 2 d'un an), sans blessé (déjà inclus dans la synthèse ; ligne pour la taille de groupe)",
  lieu="Lamar Valley, Yellowstone", annee=2001)
E("ours_brun", 1, "loup", 3, "A", 1, tb=["carcasse"], qual="A",
  src="https://webarchive.library.unt.edu/web/20120927065533/http://www.nps.gov/yell/forkids/upload/YELL709.pdf",
  note="Un grizzli mange la proie de 3 loups (2 adultes, 1 d'un an) qui attendent à 50 m", lieu="Yellowstone")
E("ours_brun", 3, "loup", 5, "A", 1, qual="A",
  src="https://webarchive.library.unt.edu/web/20120927065533/http://www.nps.gov/yell/forkids/upload/YELL709.pdf",
  note="Une femelle et 2 grizzlis de 2 ans repoussent progressivement 5 loups à ~250 m de leurs couches, sans blessé", lieu="Yellowstone")
E("loup", 6, "ours_brun", 1, "A", 1, tb=["carcasse"], qual="A",
  src="https://www.nps.gov/yell/learn/nature/upload/2022-Web-Wolf-Report.pdf",
  note="Rescue Creek : les loups défient un grizzli qui a pris leur wapiti et le chassent de la carcasse (il se défend à coups de patte) ; taille de meute ~", lieu="Yellowstone", annee=2022)
E("ours_brun", 1, "loup", 1, "A", 3, qual="A",
  src="https://www.nps.gov/yell/learn/nature/upload/2022-Web-Wolf-Report.pdf",
  note="Loup adulte non collier de Wapiti Lake tué par un grizzli (mortalité interspécifique, 13/09/2022)", lieu="Yellowstone", annee=2022)
E("ours_brun", 1, "loup", 1, "A", 3, tb=["jeune"], qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/550/556/2218",
  note="Jimenez et al. 2008 : louveteau femelle (20-22 kg, meute de 8) tué par un grizzli près d'un orignal tué par les loups ; 1er cas documenté dans l'Ouest des É.-U.", lieu="Jackson, Wyoming", annee=2005)
E("ours_brun", 2, "loup", 5, "A", 1, tb=["carcasse"], qual="B",
  src="https://www.pulse.bot/science/news/a-yellowstone-grizzly-had-a-fierce-standoff-with-a-wolf-pack-it-was-caught-on-video-84d48a71-2b08-42dd-9361-db159f9b86bf/",
  note="Vidéo : grand mâle grizzli (+ un subadulte) fait reculer une meute sur une carcasse de bison noyé ; taille de meute ~", lieu="Yellowstone", annee=2026)

# ---------------------------------------------------------------------------
# LOUP vs OURS NOIR
# ---------------------------------------------------------------------------
# Table 10.3 : 26 interactions, loups plus nombreux dans 81 % ; loups gagnent 69 %, ours 15 %.
E("loup", 3, "ours_noir", 1, "A", 3, count=9, qual="A", src=BALLARD,
  note="9 ours noirs tués par des loups sur 26 interactions, dont 6 cherchés dans leur tanière (ours léthargique)", lieu="Amérique du Nord (Minnesota, Alberta, Manitoba)")
E("loup", 3, "ours_noir", 1, "A", 2, count=9, qual="A", src=BALLARD,
  note="Loups vainqueurs non mortels (total loups 69 % de 26, count arrondi)", lieu="Amérique du Nord")
E("ours_noir", 1, "loup", 1, "A", 3, qual="A", src=BALLARD,
  note="1 loup solitaire tué par un ours noir près d'une tanière de loups (Rogers & Mech 1981)", lieu="NE Minnesota")
E("ours_noir", 1, "loup", 1, "A", 1, count=3, qual="A", src=BALLARD,
  note="Ours noirs vainqueurs (15 % de 26) ; ours adultes chassant des loups solitaires", lieu="Amérique du Nord")
E("loup", 3, "ours_noir", 1, "D", 1, count=4, qual="A", src=BALLARD,
  note="Interactions sans vainqueur net (reste des 26)", lieu="Amérique du Nord")
E("ours_noir", 1, "loup", 1, "A", 1, tb=["carcasse"], qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/977/982/3907",
  note="Fremmerlid & Latham 2009 : ours noir adulte chasse un loup solitaire de sa proie (caribou femelle) le lendemain du kill", lieu="Wabasca, NE Alberta", annee=2002)

# ---------------------------------------------------------------------------
# LOUP vs PUMA
# ---------------------------------------------------------------------------
E("loup", 5, "puma", 1, "A", 3, count=3, qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/2461/2339/0",
  note="Ruth, Buotte & Hornocker 2019 (Yellowstone Cougars) : au moins 3 pumas adultes tués par des loups (1998-2005) ; taille de meute ~", lieu="Northern Range, Yellowstone", annee=2005)
E("loup", 5, "puma", 1, "A", 3, tb=["jeune"], count=5, qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/2461/2339/0",
  note="Ruth et al. 2019 : 5 chatons de puma tués par des loups", lieu="Yellowstone", annee=2005)
E("loup", 5, "puma", 1, "A", 3, count=2, qual="A",
  src="https://www.eurekalert.org/news-releases/1113729",
  note="Binder et al. 2026 PNAS : 2 des 12 morts de pumas adultes (2016-2024) dues aux loups, sans terrain d'échappement ; aucun des 90 loups morts tué par un puma ; taille de meute ~", lieu="Yellowstone", annee=2024)
E("loup", 8, "puma", 1, "A", 1, tb=["carcasse"], count=2, qual="A",
  src="https://objects.lib.uidaho.edu/twrs/AKENSON__J_J__H_A_2005_Effects_Wolf_Cougars.pdf",
  note="Akenson et al. 2005 : 2 pumas mis dans un arbre par des meutes (7-10 loups en hiver), qui prennent leurs proies (cerf, mouflon)", lieu="Big Creek, Idaho", annee=2002)
E("puma", 1, "loup", 1, "A", 3, ta=["embuscade"], count=3, qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/550/556/2218",
  note="Jimenez et al. 2008 : 3 loups seuls tués par des pumas (perforation du crâne) — Drummond MT 1996, Paradise Valley MT 2003, Turner Valley AB 2006", lieu="Montana / Alberta", annee=2006)
E("puma", 1, "loup", 1, "A", 3, ta=["embuscade"], count=6, qual="B",
  src="https://www.kuow.org/stories/in-a-battle-of-apex-predators-cougars-are-killing-wolves-at-a-surprising-rate",
  note="6 loups (à collier) tués par des pumas en ~10 ans dans l'État de Washington ; probablement loups isolés en terrain accidenté", lieu="Washington", annee=2022)

# ---------------------------------------------------------------------------
# LOUP vs COYOTE (Merkle, Stahler & Smith 2009, Can. J. Zool. 87:56-63)
# 337 interactions 1995-2007 ; loups dominent 91 % ; 79 % poursuites sans contact ; 25 coyotes tués ;
# loups plus nombreux dans 39 % seulement (80 % des cas mortels) ; 18 cas où les coyotes, non en infériorité, chassent/attaquent les loups.
# ---------------------------------------------------------------------------
MERKLE = "Merkle, Stahler & Smith 2009, Can. J. Zool. 87:56 — https://next.sciencegate.app/document/10.1139/z08-136"
E("loup", 2, "coyote", 1, "A", 3, count=25, qual="A", src=MERKLE,
  note="25 coyotes tués par des loups sur 337 interactions ; loups plus nombreux dans 80 % de ces cas mortels", lieu="Yellowstone", annee=2007)
E("loup", 1, "coyote", 1, "A", 2, count=46, qual="A", src=MERKLE,
  note="Interactions avec contact physique, coyote blessé/chassé mais survivant (count dérivé : 21 % avec contact − mortels)", lieu="Yellowstone", annee=2007)
E("loup", 1, "coyote", 2, "A", 1, tb=["carcasse"], count=236, qual="A", src=MERKLE,
  note="Loup chasse le(s) coyote(s) SANS contact, surtout aux carcasses (count dérivé de 91 % dominés) ; loups en infériorité ou égalité dans 61 % des interactions", lieu="Yellowstone", annee=2007)
E("coyote", 2, "loup", 1, "A", 1, tb=["carcasse"], count=30, qual="A", src=MERKLE,
  note="Coyotes dominants (~9 % des 337), dont 18 cas où ils chassent ou attaquent des loups sans être en infériorité numérique", lieu="Yellowstone", annee=2007)
E("loup", 1, "coyote", 3, "A", 1, ta=["blesse"], tb=["carcasse"], qual="B",
  src="https://www.yahoo.com/entertainment/yellowstone-wolf-alone-injured-shows-113018510.html",
  note="Loup solitaire boiteux attaqué plusieurs fois par 3 coyotes sur une carcasse de bison ; il les repousse, mange 15 min et repart indemne", lieu="Elk Creek, Yellowstone")

# ---------------------------------------------------------------------------
# LOUP vs ORIGNAL (Isle Royale)
# ---------------------------------------------------------------------------
MECH = "Mech 1966, The Wolves of Isle Royale (Fauna Series 7) — https://npshistory.com/series/fauna/7/summary.htm"
E("orignal", 1, "loup", 15, "A", 1, count=36, qual="A", src=MECH,
  note="Sur 77 orignaux « testés » par la meute de 15-16 loups, 36 tiennent tête (aux abois) jusqu'à ce que les loups abandonnent ; aucun tué", lieu="Isle Royale, Michigan", annee=1961)
E("loup", 15, "orignal", 1, "A", 3, count=6, qual="A", src=MECH,
  note="6 orignaux tués sur 77 testés (efficacité 7,8 %), surtout parmi ceux qui fuient ; 36 fuyards non tués exclus (pas de combat)", lieu="Isle Royale", annee=1961)
E("loup", 3, "orignal", 1, "A", 3, tb=["vieux", "blesse"], qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/1030/1034/4117",
  note="Jordan, Peterson & LeDoux 2010 : ≥3 loups attaquent à la nage une vieille femelle (~14 ans, arthrite), retrouvée tuée sur la rive", lieu="Isle Royale", annee=2008)

# ---------------------------------------------------------------------------
# LOUP vs BISON (Yellowstone)
# ---------------------------------------------------------------------------
E("loup", 8, "bison", 1, "A", 3, tb=["jeune", "blesse"], qual="A",
  src="https://webarchive.library.unt.edu/eot2008/20081105200338/http://www.npwrc.usgs.gov/resource/mammals/wlfbison/index.htm",
  note="Smith et al. 2000 (J. Mammal. 81:1128) : veau émacié tué par 8 loups d'un an, 21 jours après lâcher", lieu="Yellowstone", annee=1995)
E("loup", 8, "bison", 1, "A", 3, tb=["blesse"], count=13, qual="A",
  src="https://webarchive.library.unt.edu/eot2008/20081105200338/http://www.npwrc.usgs.gov/resource/mammals/wlfbison/index.htm",
  note="Smith et al. 2000 : 13 autres bisons tués 1995-1999, tous en fin d'hiver, bêtes affaiblies/blessées/jeunes ; meutes ~", lieu="Yellowstone", annee=1999)
E("bison", 1, "loup", 11, "A", 1, qual="A",
  src="https://pmc.ncbi.nlm.nih.gov/articles/PMC4229308",
  note="MacNulty et al. 2014 (239 rencontres) : prob. de capture d'un bison par un loup seul ~1 %, croît jusqu'à ~11 loups ; bison mordus et retenus s'échappent souvent ; ligne indicative (pas de comptes publiés)", lieu="Pelican Valley, Yellowstone", annee=2009)
E("bison", 1, "loup", 14, "A", 1, ta=["defense_petits"], qual="A",
  src="https://www.nps.gov/yell/learn/nature/upload/2014-wolf-report.pdf",
  note="Une vache bison protège avec succès son veau tardif contre la meute Prospect Peak (14 loups)", lieu="Yellowstone", annee=2014)
E("bison", 6, "loup", 5, "A", 1, qual="B",
  src="https://cowboystatedaily.com/2023/09/15/video-shows-yellowstone-wolf-pack-fail-in-rare-attempt-to-take-down-bison",
  note="Meute Junction Butte attaque un bison isolé (peut-être blessé) ; il rejoint le troupeau qui forme un mur de cornes ; échec ; effectifs ~", lieu="Lamar Valley, Yellowstone", annee=2023)
E("loup", 10, "bison", 1, "A", 3, qual="B",
  src="https://cowboystatedaily.com/2024/01/22/wolf-pack-takes-down-bison-on-firehole-river-in-yellowstone-standoff",
  note="Meute Wapiti Lake tue un bison isolé après un long face-à-face dans la Firehole ; effectif de meute ~", lieu="Firehole River, Yellowstone", annee=2024)

# ---------------------------------------------------------------------------
# COYOTE vs BISON
# ---------------------------------------------------------------------------
E("coyote", 1, "bison", 1, "A", 3, tb=["jeune"], qual="A",
  src="https://canadianfieldnaturalist.ca/index.php/cfn/article/download/974/979/3895",
  note="Sheldon et al. 2009 : un mâle coyote seul tue en ~3,5 h un veau de bison isolé de son troupeau de l'autre côté de la rivière", lieu="Lamar River, Yellowstone", annee=2009)

# ---------------------------------------------------------------------------
# OURS BRUN vs BISON
# ---------------------------------------------------------------------------
E("ours_brun", 1, "bison", 1, "A", 3, ta=["jeune"], tb=["jeune"], qual="B",
  src="https://www.fieldandstream.com/conservation/grizzly-bear-attacks-bison-yellowstone-video/",
  note="Grizzli subadulte (90-110 kg) maîtrise en ~17 min une femelle bison d'un an (~230 kg) isolée", lieu="Grand Prismatic, Yellowstone", annee=2020)
E("bison", 1, "ours_brun", 1, "A", 1, ta=["defense_petits"], qual="B",
  src="https://www.foxweather.com/earth-space/yellowstone-bear-mother-bison",
  note="Une mère bison charge un grizzli qui rôde près d'une nurserie et le chasse", lieu="Lamar Valley, Yellowstone", annee=2023)

# ---------------------------------------------------------------------------
# TIGRE vs OURS (Extrême-Orient russe)
# ---------------------------------------------------------------------------
SERYODKIN = ("Seryodkin, Miquelle, Goodrich, Kostyria & Petrunenko 2018, Biology Bulletin 45:853 — "
             "https://journals.rcsi.science/1062-3590/article/view/182870 (détails chiffrés via https://wildfact.com/forum/showthread.php?pid=65104)")
E("tigre", 1, "ours_brun", 1, "A", 3, count=7, qual="A", src=SERYODKIN,
  note="Sikhote-Aline 1992-2013 : sur 763 proies de tigres, ~15 ours tués par des tigres dont ~7 ours bruns (souvent jeunes/subadultes ou femelles ; surtout par des mâles adultes)", lieu="Sikhote-Aline, Russie", annee=2013)
E("tigre", 1, "ours_noir", 1, "A", 3, count=8, qual="A", src=SERYODKIN,
  note="Idem : ~8 ours noirs d'Asie (U. thibetanus) tués par des tigres (proxy ours_noir)", lieu="Sikhote-Aline, Russie", annee=2013)
E("ours_brun", 1, "tigre", 1, "A", 1, tb=["carcasse"], count=11, qual="A", src=SERYODKIN,
  note="Idem : des ours chassent des tigres de 11 de leurs 378 proies (saison active), surtout des tigresses ; espèce d'ours non ventilée (attribuée à ours_brun)", lieu="Sikhote-Aline", annee=2013)
E("ours_brun", 1, "tigre", 1, "D", 1, tb=["carcasse"], count=7, qual="A", src=SERYODKIN,
  note="Idem : 7 proies partagées ours/tigre (dont un tigre mâle adulte contraint de partager) ; aucun tigre tué par un ours en 1992-2013", lieu="Sikhote-Aline", annee=2013)
E("ours_brun", 1, "tigre", 1, "A", 3, count=12, qual="C",
  src="https://en.wikipedia.org/wiki/Ussuri_brown_bear",
  note="Rapport soviétique de 1973 : 12 cas connus d'ours bruns tuant des tigres (surtout tigresses/jeunes, dont mâles adultes), ensuite mangés ; compilation historique", lieu="Extrême-Orient russe", annee=1973)
E("tigre", 1, "ours_brun", 1, "A", 3, tb=["jeune"], qual="B",
  src="https://m.washingtontimes.com/news/2015/jul/15/putins-tiger-boris-kills-and-eats-bear-russias-far/",
  note="Le tigre réintroduit « Boris » tue et mange un jeune ours brun", lieu="Réserve, région de l'Amour", annee=2015)

# ---------------------------------------------------------------------------
# OURS BRUN vs OURS POLAIRE
# ---------------------------------------------------------------------------
E("ours_brun", 1, "ours_polaire", 1, "A", 1, tb=["carcasse"], count=68, qual="A",
  src="https://www.rcinet.ca/eye-on-the-arctic/2015/12/04/small-grizzlies-dominate-bigger-polar-bears-study",
  note="Miller et al. 2015 (J. Mammal.) : 137 rencontres grizzli-ours polaire sur os de baleine ; les grizzlis (≈ moitié plus petits) déplacent complètement les ours polaires dans ~la moitié (count arrondi), polaires surtout soumis", lieu="Kaktovik, Alaska", annee=2007)

# ---------------------------------------------------------------------------
# OURS NOIR vs PUMA (kleptoparasitisme)
# ---------------------------------------------------------------------------
ELBROCH = "Elbroch et al. 2015, Pumas, black bears and competition refuges — https://www.originalwisdom.com/wp-content/uploads/bsk-pdf-manager/2019/03/Elbroch-et-al_2015_Pumas-black-bears-and-competition-refuges_CT.pdf"
E("ours_noir", 1, "puma", 1, "A", 1, tb=["carcasse"], count=47, qual="A", src=ELBROCH,
  note="Caméras : des ours noirs chassent des pumas de 58 proies (29 Colorado + 29 Californie) ; puma ne revient pas dans 47 cas", lieu="Colorado / Californie", annee=2014)
E("puma", 1, "ours_noir", 1, "A", 1, tb=["carcasse"], count=10, qual="A", src=ELBROCH,
  note="Le puma revient sur sa proie après déplacement (11 cas dont 1 mortel ci-dessous)", lieu="Colorado / Californie", annee=2014)
E("puma", 1, "ours_noir", 1, "A", 3, tb=["jeune"], qual="A", src=ELBROCH,
  note="Femelle puma adulte revient et tue une ourse de 3 ans qui l'avait chassée de sa proie", lieu="Mendocino NF, Californie", annee=2014)

# ---------------------------------------------------------------------------
# PUMA / OURS vs ALLIGATOR
# ---------------------------------------------------------------------------
E("puma", 1, "alligator", 1, "A", 3, qual="A",
  src="https://eaglehill.us/SENAonline/articles/SENA-9-4/30-McBride.shtml",
  note="McBride & McBride 2010 : un mâle adulte de panthère de Floride tue un alligator de 2,69 m (plus grand connu ; autres proies 0,5-1,5 m)", lieu="Big Cypress, Floride", annee=2008)
E("ours_noir", 1, "alligator", 2, "A", 1, tb=["eau"], qual="B",
  src="https://www.fieldandstream.com/stories/bear-vs-alligator-florida",
  note="Ours noir traversant le St. Johns à la nage chargé par un grand alligator puis attaqué par un second ; il les repousse et sort indemne", lieu="St. Johns River, Floride")

# ---------------------------------------------------------------------------
# JAGUAR vs CAÏMAN / ANACONDA / PUMA
# ---------------------------------------------------------------------------
E("jaguar", 1, "caiman", 1, "A", 3, ta=["embuscade"], count=71, qual="A",
  src="https://bv.fapesp.br/en/publicacao/52743/predator-prey-interactions-jaguar-predation-on-caiman-in-a",
  note="Azevedo & Verdade 2012 (J. Zool. 286:200) : 71 des 114 caïmans yacare morts (62 %) tués par des jaguars, toutes tailles ; morsure crânienne", lieu="Pantanal sud, Brésil")
E("jaguar", 1, "anaconda", 1, "A", 3, qual="B",
  src="https://www.futura-sciences.com/planete/breves/animaux-jaguar-filme-train-attaquer-anaconda-geant-amerique-sud-5992/",
  note="Jaguar filmé par des touristes attaquant un grand anaconda ; le serpent ne s'en sort pas", lieu="Pantanal", annee=2022)
E("jaguar", 1, "anaconda", 1, "A", 2, qual="B",
  src="https://www.bluradio.com/sociedad/increible-foto-muestra-el-feroz-duelo-entre-una-anaconda-y-un-jaguar-en-el-pantanal-rs15",
  note="Femelle jaguar « Ámbar » enserrée par un anaconda se libère après plusieurs minutes et le maîtrise (photos F. Oliveira)", lieu="Pantanal", annee=2025)
E("jaguar", 1, "puma", 1, "A", 1, qual="B",
  src="https://www.discoverwildlife.com/animal-facts/jaguar-fighting-puma-pantanal",
  note="Des touristes voient un jaguar chasser un puma qui fuit, berges du Cuiabá", lieu="Pantanal", annee=2026)

# ---------------------------------------------------------------------------
# CAÏMAN vs ANACONDA (Venezuela, caïman à lunettes = proxy caiman)
# ---------------------------------------------------------------------------
E("caiman", 1, "anaconda", 1, "A", 3, count=8, qual="A",
  src="https://anacondas.org/anacondas.org/fight.htm",
  note="Rivas et al. 1999 (Herp. Rev. 30:101) : 8 anacondas (6 mâles, 2 femelles ; mâles ~2,7 m, 5-10 kg, une femelle 4,9 m/29 kg) tués par des caïmans à lunettes ; combats jusqu'à 5 h", lieu="Llanos, Venezuela", annee=1997)
E("anaconda", 1, "caiman", 1, "A", 3, qual="A",
  src="https://anacondas.org/anacondas.org/subduing.htm",
  note="Rivas 2004 (Herp. Rev. 35:66) : femelle anaconda de 4,5 m serre un grand caïman à lunettes (1,8 m) et lui disloque la colonne", lieu="Llanos, Venezuela", annee=1999)

# ---------------------------------------------------------------------------
# OURS POLAIRE vs MORSE
# ---------------------------------------------------------------------------
OVS = "Ovsyanikov 1995, Polar bear predation of walruses on Wrangel Island — https://www.arlis.org/docs/vol1/E/Walrus/Russian/Ovsyanikov.1995.PolarBearPredationWalrusWrangellIsland.BullM.pdf"
E("morse", 3, "ours_polaire", 1, "A", 2, count=3, qual="A", src=OVS,
  note="Attaques avec contact sur morses adultes : toutes échouent (11/11) ; dans 3 l'ours est blessé (coups de défenses) ; nb morses ~ (troupeau)", lieu="Cap Blossom, île Wrangel", annee=1990)
E("morse", 3, "ours_polaire", 1, "A", 1, count=8, qual="A", src=OVS,
  note="Autres attaques avec contact sur adultes, échec sans blessure notée de l'ours (5 ours portaient 16 plaies de défenses)", lieu="Cap Blossom, île Wrangel", annee=1990)
E("ours_polaire", 1, "morse", 1, "A", 3, tb=["jeune"], count=2, qual="A", src=OVS,
  note="Seuls succès sur 25 chasses : 2 veaux de l'année arrachés au troupeau par la même femelle ; l'auteur juge qu'un ours ne peut tuer un morse adulte à terre", lieu="Cap Blossom, île Wrangel", annee=1990)
E("ours_polaire", 1, "morse", 1, "A", 3, count=7, qual="A",
  src="https://www.bearbiology.org/download/interactions-between-polar-bears-and-overwintering-walruses-in-the-central-canadian-high-arctic/",
  note="Calvert & Stirling 1990 : 3 morses tués + 4 probablement tués par des ours en hiver aux polynies (dont un morse bloqué hors de son trou)", lieu="Haut-Arctique canadien", annee=1989)
E("morse", 1, "ours_polaire", 1, "A", 1, ta=["eau"], count=3, qual="A",
  src="https://www.bearbiology.org/download/interactions-between-polar-bears-and-overwintering-walruses-in-the-central-canadian-high-arctic/",
  note="Calvert & Stirling 1990 : 3 morses blessés mais non tués (attaques non mortelles)", lieu="Haut-Arctique canadien", annee=1989)

# ---------------------------------------------------------------------------
# CHIEN vs LOUP / OURS
# ---------------------------------------------------------------------------
E("loup", 2, "chien", 1, "A", 3, count=35, qual="A",
  src="https://largecarnivores.fi/large-carnivores-and-us/damages/damages-to-dogs.html",
  note="Kojola & Kuittinen : 43 attaques confirmées de loups sur chiens 1996-1999, 82 % des chiens tués ; chiens de chasse souvent attaqués par ≥2 loups", lieu="Finlande", annee=1999)
E("loup", 2, "chien", 1, "A", 2, count=8, qual="A",
  src="https://largecarnivores.fi/large-carnivores-and-us/damages/damages-to-dogs.html",
  note="Idem : 18 % des chiens attaqués survivent (blessés/échappés)", lieu="Finlande", annee=1999)
E("chien", 1, "ours_brun", 1, "A", 1, count=19, qual="B",
  src="https://library.kab.ac.ug/Record/doaj-art-4a5c732b47bb4f2095a2d0cf5c495b48/Description",
  note="Smith & Herrero 2018 : les chiens ont mis fin à l'attaque d'ours dans 47,5 % des cas (count déduit, n≈40 ; 88 % grizzlis) ; armes humaines non exclues", lieu="Alaska", annee=2015)
E("ours_brun", 1, "chien", 1, "A", 1, count=21, qual="B",
  src="https://library.kab.ac.ug/Record/doaj-art-4a5c732b47bb4f2095a2d0cf5c495b48/Description",
  note="Idem, chien présent mais n'arrête pas l'attaque (count déduit) ; issue chien-ours non détaillée", lieu="Alaska", annee=2015)

# ---------------------------------------------------------------------------
# HUMAIN vs PUMA (sans arme à feu)
# ---------------------------------------------------------------------------
CA_LIONS = "https://tchester.org/sgm/lists/lion_attacks_ca.html"
E("humain", 1, "puma", 1, "A", 3, ta=["outil"], tb=["jeune"], qual="B",
  src="https://www.cbsnews.com/amp/colorado/news/travis-kauffman-mountain-lion-attacked-killed-colorado-fort-collins",
  note="T. Kauffman, coureur, mordu au poignet : bâtons inefficaces, 2 coups de pierre, puis étouffe le jeune puma avec le pied ; ~20 points de suture", lieu="Horsetooth Mountain, Colorado", annee=2019)
E("humain", 2, "puma", 1, "A", 1, ta=["outil"], qual="B",
  src="https://www.nbcnews.com/id/wbna16817149",
  note="Jim Hamm (70 ans) saisi par un puma ; sa femme Nell (65) frappe l'animal avec une bûche (stylo plié) jusqu'à ce qu'il lâche ; Jim grièvement blessé", lieu="Prairie Creek Redwoods, Californie", annee=2007)
E("humain", 3, "puma", 1, "A", 1, ta=["outil"], qual="B", src=CA_LIONS,
  note="A. Hjelle saisie à la tête ; D. Nicholls la tient par les jambes, 2 hommes jettent des pierres ; le puma lâche (abattu ensuite)", lieu="Whiting Ranch, Californie", annee=2004)
E("humain", 4, "puma", 1, "A", 1, ta=["arme_blanche", "outil"], qual="B", src=CA_LIONS,
  note="Femme de 27 ans attaquée, 3 compagnons ; coups de couteau peu efficaces puis pierres ; puma repoussé, victime perd un œil", lieu="Johnsondale, Californie", annee=2004)
E("humain", 3, "puma", 1, "A", 1, ta=["arme_blanche", "outil"], tb=["blesse"], qual="B", src=CA_LIONS,
  note="Puma enragé repoussé par 3 personnes avec pierres et couteau à pain (un homme perd un pouce)", lieu="Dos Rios, Californie", annee=1994)
E("humain", 1, "puma", 1, "A", 1, ta=["outil"], qual="B", src=CA_LIONS,
  note="Cycliste seul (27 ans) repousse le puma à coups de pierres ; puma abattu ensuite", lieu="Mount Lowe, Californie", annee=1995)
E("humain", 1, "puma", 1, "A", 1, ta=["outil"], qual="B", src=CA_LIONS,
  note="Un père atteint d'une pierre le puma qui emportait son fils de 9 ans ; le puma lâche l'enfant", lieu="Gaviota SP, Californie", annee=1992)
E("puma", 1, "humain", 1, "A", 3, qual="B", src=CA_LIONS,
  note="Femme de 40 ans seule, se défend avec les bras, tuée", lieu="Auburn SRA, Californie", annee=1994)
E("puma", 1, "humain", 1, "A", 3, qual="B", src=CA_LIONS,
  note="Femme de 56 ans seule, tuée", lieu="Cuyamaca Peak, Californie", annee=1994)
E("puma", 1, "humain", 1, "A", 3, count=11, qual="A",
  src="https://core.ac.uk/download/77526645.pdf",
  note="Mattson et al. 2011 : 200 attaques avec contact (29 mortelles) ; adultes = 51 % des victimes, létalité 10,9 % (count déduit ≈11) ; aucun adulte en groupe d'adultes tué ; armes à feu non exclues", lieu="Amérique du Nord", annee=2010)
E("humain", 1, "puma", 1, "A", 1, count=91, qual="B",
  src="https://core.ac.uk/download/77526645.pdf",
  note="Idem : adultes attaqués survivants (count déduit ≈91) — attaque interrompue par la victime, des compagnons ou parfois une arme à feu ; à pondérer fortement", lieu="Amérique du Nord", annee=2010)

# ---------------------------------------------------------------------------
# HUMAIN vs OURS (sans arme à feu ni spray)
# ---------------------------------------------------------------------------
E("humain", 1, "ours_brun", 1, "A", 3, ta=["arme_blanche"], qual="B",
  src="https://www.themeateater.com/conservation/wildlife-management/a-knife-fight-with-a-brown-bear-the-story-of-gene-moe",
  note="Gene Moe, chasseur, fusil hors de portée, tue un ours brun ~270 kg au couteau de 10 cm ; bras et cuisse déchiquetés (fusil seulement après que l'ours soit à terre)", lieu="Raspberry Island, Alaska", annee=1999)
E("humain", 1, "ours_brun", 1, "A", 1, ta=["arme_blanche"], qual="B",
  src="https://www.outsideonline.com/outdoor-adventure/exploration-survival/bear-attack-pocket-knife-canada-colin-dowler?scope=anon",
  note="Colin Dowler, attaque prédatrice d'un grizzli sain de 4-5 ans ; le poignarde au cou avec un canif de 7 cm, l'ours part ; graves blessures abdominales", lieu="Côte de C.-B., Canada", annee=2019)
E("humain", 1, "ours_brun", 1, "A", 1, qual="B",
  src="https://930kmpt.com/montana-man-fights-off-griz-by-shoving-hand-down-bears-throat/",
  note="Chase Dellwo, chasseur à l'arc, enfonce son poing dans la gorge d'un grizzli de ~180 kg (attaque défensive) ; l'ours s'enfuit ; lacérations tête et jambe", lieu="Rocky Mountain Front, Montana", annee=2015)
E("ours_brun", 1, "humain", 1, "A", 3, qual="B",
  src="https://en.wikipedia.org/wiki/List_of_fatal_bear_attacks_in_North_America",
  note="Ex. : randonneur seul tué par une femelle grizzli (Yellowstone 2015) ; registre 2000-2024 : 19 attaques mortelles de grizzlis en Amérique du Nord (sans dénominateur)", lieu="Yellowstone", annee=2015)
E("humain", 1, "ours_noir", 1, "A", 1, tb=["defense_petits"], qual="B",
  src="https://www.npr.org/2022/10/24/1130857186/a-washington-state-woman-fended-off-a-black-bear-attack",
  note="Femme frappe « en plein sur le nez » une ourse noire suitée de 2 oursons ; l'ourse s'enfuit ; blessures légères", lieu="Chelan County, Washington", annee=2022)
E("ours_noir", 1, "humain", 1, "A", 3, count=59, qual="A",
  src="https://www.sciencedaily.com/releases/2011/05/110511074807.htm?hl=en-CA",
  note="Herrero et al. 2011 : 63 personnes tuées en 59 incidents 1900-2009, toujours un seul ours, 88 % prédateurs (92 % mâles) ; REGISTRE DE VICTIMES sans dénominateur, armes non exclues", lieu="Amérique du Nord", annee=2009)

# ---------------------------------------------------------------------------
# HUMAIN vs LOUP
# ---------------------------------------------------------------------------
E("humain", 2, "loup", 1, "A", 1, tb=["vieux", "blesse"], ta=["outil"], qual="B",
  src="https://www.theweathernetwork.com/en/news/nature/animals/banff-national-park-wolf-attack-survivors-share-details-of-terrifying-ordeal",
  note="Loup attaque une tente ; M. Rispoli le plaque et lui tient la gueule à mains nues, un voisin lui donne des coups de pied, pierres ; le loup lâche (vieux, en mauvais état, abattu ensuite)", lieu="Rampart Creek, Banff", annee=2019)
E("humain", 2, "loup", 1, "A", 1, qual="B",
  src="https://en.wikipedia.org/wiki/Wolf_attacks_in_North_America",
  note="S. Langevin attaqué dans son sac de couchage, se bat à mains nues ; d'autres campeurs chassent le loup (non enragé)", lieu="Vargas Island, C.-B.", annee=2000)
E("loup", 2, "humain", 1, "A", 3, qual="B",
  src="https://en.wikipedia.org/wiki/Wolf_attacks_in_North_America",
  note="Kenton Carnegie, étudiant seul, tué par des loups habitués à une décharge (plusieurs loups ; nombre exact incertain)", lieu="Points North, Saskatchewan", annee=2005)
E("loup", 2, "humain", 1, "A", 3, qual="B",
  src="https://en.wikipedia.org/wiki/Wolf_attacks_in_North_America",
  note="Candice Berner, joggeuse seule, tuée (attaque prédatrice, loups non enragés ; ≥2 loups, nombre exact incertain)", lieu="Chignik Lake, Alaska", annee=2010)
