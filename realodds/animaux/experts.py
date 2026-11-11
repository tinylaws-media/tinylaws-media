"""Avis d'experts sourcés sur l'issue de combats (1 contre 1 ou n contre 1), utilisés comme contraintes souples
(poids modeste) à côté des rencontres documentées.

X(a, b, gap, sd, na, nb, ...) : selon l'expert, `na` adultes de a l'emportent sur `nb` adultes de b avec un écart
d'environ `gap` sur l'échelle logit de la probabilité de victoire en combat neutre (0 = égal ; 1,1 ≈ 75 % ;
2,2 ≈ 90 % ; 3 ≈ 95 % ; 4,6 ≈ 99 %), incertitude `sd`.
Conversion (prudente) : « aucune chance » → 3-4,6 / sd 1 ; « gagnerait presque sûrement » → 2,2-3 / sd 0,9 ;
« probablement » → 1,1 / sd 0,9 ; « ça peut aller dans les deux sens » → 0 / sd 0,7. Les sd sont relevées
quand l'énoncé porte sur la dominance (carcasses, fuite) plutôt que sur un combat, ou quand il est vague.
Citations dans la langue d'origine, telles que publiées."""

EXPERTS = []


def X(a, b, gap, sd, na=1, nb=1, src="", quote="", qui="", note=""):
    EXPERTS.append(dict(a=a, b=b, gap=gap, sd=sd, na=na, nb=nb, src=src, quote=quote, qui=qui, note=note))


# ---------------------------------------------------------------- Humain contre gorille
X("gorille", "humain", 3.5, 1.0,
  src="https://www.axios.com/local/columbus/2025/05/09/gorilla-vs-100-men-debate-columbus-zoo",
  quote="Pure strength? One-on-one, the gorilla is going to win, hands down.",
  qui="Jan Ramer, vice-présidente soins animaliers et conservation, Columbus Zoo and Aquarium (Axios, mai 2025)")
X("gorille", "humain", 3.5, 1.0,
  src="https://leakeyfoundation.org/who-would-win-in-a-fight-between-100-men-and-1-gorilla-an-evolutionary-expert-weighs-in/",
  quote='In a one-on-one brawl, the gorilla can make "human-mash" with one hand.',
  qui="Renaud Joannes-Boyau, professeur, Southern Cross University (texte republié par la Leakey Foundation, 2025)")
X("humain", "gorille", 1.1, 1.1, na=100,
  src="https://leakeyfoundation.org/who-would-win-in-a-fight-between-100-men-and-1-gorilla-an-evolutionary-expert-weighs-in/",
  quote="A fight between 100 men and one gorilla might lead to a lot of dead men. [...] humans would likely lose many battles but ultimately win the fight.",
  qui="Renaud Joannes-Boyau, Southern Cross University",
  note="Son argument s'appuie en partie sur la stratégie et la coopération ; « likely » → 1,1.")
X("humain", "gorille", 1.1, 1.0, na=100,
  src="https://www.yahoo.com/news/100-men-vs-1-gorilla-who-would-win-a-primatology-expert-addresses-the-viral-debate-201209014.html",
  quote="I think, though, that in this case, it's a numbers game. [...] They can coordinate their behavior; they can take turns.",
  qui="Tara Stoinski, présidente et directrice scientifique, Dian Fossey Gorilla Fund",
  note="Elle ajoute qu'un gorille « would probably take out a number of humans in the fight ».")
X("humain", "gorille", 1.1, 1.1, na=100,
  src="https://futurism.com/ape-researchers-humans-vs-gorilla",
  quote="It could be a kamikaze mission for the men closest to the gorilla.",
  qui="Ron Magill, directeur de la communication, Zoo Miami (cité par Rolling Stone, repris par Futurism)",
  note="Pense que ~100 hommes jeunes et en forme l'emporteraient (« human straightjacket »), avec de lourdes pertes.")
X("gorille", "humain", 3.0, 1.1, nb=100,
  src="https://futurism.com/ape-researchers-humans-vs-gorilla",
  quote="Honestly, 100 guys wouldn't stand a chance. [...] a single one of his punches would floor them.",
  qui="Cat Hobaiter, primatologue, University of St Andrews (citée par Rolling Stone, reprise par Futurism)",
  note="Avis contraire aux trois précédents sur 100 contre 1 ; sd élevée car hypothèse « gorille de montagne chez lui ».")

# ---------------------------------------------------------------- Humain contre chimpanzé
X("chimpanze", "humain", 2.2, 1.0,
  src="https://www.scientificamerican.com/article/why-would-a-chimpanzee-at/",
  quote="Chimpanzee males have been measured as having five times the arm strength as a human male. [...] But a pro wrestler would not be able to hold a chimpanzee still if they wanted to. [...] So you have a very dangerous creature in front of you that is impossible to control.",
  qui="Frans de Waal, Yerkes National Primate Research Center / Emory University (Scientific American, 2009)",
  note="Le facteur 5 de force est contesté (O'Neill et al. 2017 : ~1,35×) ; énoncé indirect → sd 1.")

# ---------------------------------------------------------------- Humain contre ours, puma, loup
X("ours_brun", "humain", 3.5, 1.0,
  src="https://www.insidehook.com/article/news-opinion/men-wild-animals-imaginary-fights",
  quote="The physical strength of bears is awesome – greater pound for pound than we can appreciate [...] capable of quickly inflicting serious incapacitating damage to a creature as fragile as a human if they choose.",
  qui="John Hechtel, spécialiste des ours, ancien membre du conseil de l'International Association for Bear Research and Management")
X("ours_noir", "humain", 1.1, 1.3,
  src="https://www.sciencedaily.com/releases/2011/05/110511074807.htm",
  quote="With training, people can learn to recognize the behaviour of a bear that is considering them as prey [...] deter an attack by taking aggressive action such as fighting back.",
  qui="Stephen Herrero, University of Calgary (étude des attaques mortelles d'ours noirs, J. Wildlife Management 2011)",
  note="Conseil de riposte, pas un pronostic : l'humain n'est pas sans chance face à un ours noir prédateur. Conversion très incertaine.")
X("puma", "humain", 0.5, 1.2,
  src="https://www.nationalgeographic.com/animals/article/fatal-cougar-attack-washington-sj-brooks-isaac-sederbaum-animals",
  quote="they have successfully done so—they’ve scared off or even killed the puma.",
  qui="Mark Elbroch, responsable du programme puma, Panthera (National Geographic, 2018)",
  note="À propos des victimes récentes qui se sont défendues ; suggère un combat assez ouvert, puma légèrement favori.")
X("loup", "humain", 1.5, 1.2,
  src="https://wolf.org/wolf-info/basic-wolf-info/wolves-and-humans/whos-afraid-of-the-big-bad-wolf/",
  quote="It is clear that wolves could easily kill a human if they so desired.",
  qui="L. David Mech, International Wolf Center / USGS",
  note="Pluriel (« wolves ») ambigu entre un loup et une meute → écart modéré, sd élevée.")

# ---------------------------------------------------------------- Lion contre tigre
X("tigre", "lion", 0.6, 0.9,
  src="https://www.livescience.com/21619-lion-tiger-fight.html",
  quote="the outcome of a given fight completely depends on the individuals [...] But if I had to put my money on it I would give the advantage to the tiger [...] What I've seen from tigers, they seem to be more aggressive; they go for the throat, go for the kill",
  qui="Craig Saffoe, biologiste, conservateur des grands félins, Smithsonian's National Zoo (Live Science, 2012)")
X("tigre", "lion", 0.6, 1.0,
  src="https://www.smithsonianmag.com/smart-news/tiger-vs-lionwho-would-win-83275452/",
  quote="back in the day of the Roman Coliseum, the smart money usually backed the tiger.",
  qui="William Bridges, conservateur des publications, Bronx Zoo (Spokesman-Review, 1959, cité par Smithsonian Magazine)",
  note="Argument historique de seconde main.")
X("tigre", "lion", 0.6, 1.0,
  src="https://bigcatrescue.org/if-a-lion-and-tiger-got-into-a-fight-who-would-win",
  quote="tigers tend to have the upper paw",
  qui="Carole Baskin, fondatrice et directrice de Big Cat Rescue (sanctuaire de grands félins)",
  note="Gestionnaire de sanctuaire, pas chercheuse → poids faible (sd 1).")

# ---------------------------------------------------------------- Ours polaire contre grizzli
X("ours_brun", "ours_polaire", 1.1, 1.1,
  src="https://www.rcinet.ca/eye-on-the-arctic/2015/12/04/small-grizzlies-dominate-bigger-polar-bears-study",
  quote="Brown bears just showed up and polar bears left [...] look like they're half the size of the polar bears",
  qui="Susanne Miller, U.S. Fish and Wildlife Service, autrice principale de Miller et al. 2015 (J. Mammalogy 96:1317)",
  note="Dominance aux carcasses de baleine de Kaktovik (les grizzlis font fuir des ours polaires plus gros), pas des combats → sd élevée.")
X("ours_brun", "ours_polaire", 1.1, 1.2,
  src="https://www.rcinet.ca/eye-on-the-arctic/2015/12/04/small-grizzlies-dominate-bigger-polar-bears-study",
  quote="He just wandered in from behind the bone pile and all but one of the big polar bears ran away [...] I think it's attitude. [...] They're more aggressive in terms of bear-bear interaction",
  qui="Ryan Wilson (USFWS, coauteur) et Richard Shideler (Alaska Department of Fish and Game)",
  note="Même étude que l'entrée précédente : ne pas compter double si l'on veut être strict.")

# ---------------------------------------------------------------- Tigre contre ours brun
X("tigre", "ours_brun", 0.5, 1.3,
  src="https://journals.rcsi.science/1062-3590/article/view/182870",
  quote="Bears are an important part of the tigers’ diet, representing 2.2% of all kills found. [...] Bears exploited tiger kills after a tiger had left, by usurping a kill, or by “sharing” a kill at alternate times.",
  qui="Seryodkin, Miquelle, Goodrich, Kostyria, Petrunenko 2018, Biology Bulletin 45:853 (Amur tiger vs ours bruns et noirs d'Asie)",
  note="Le tigre prédate des ours (surtout jeunes / ours à collier) mais les ours bruns lui volent aussi des proies : léger avantage au tigre, très incertain.")

# ---------------------------------------------------------------- Hyènes contre lion
X("hyene", "lion", 0.5, 1.0, na=4,
  src="https://www.hyaenidae.org/the-hyaenidae/spotted-hyena-crocuta-crocuta/crocuta-association-with-other-species/",
  quote="if hyaena group size is large and the ratio of the number of spotted hyaenas to the number of female and subadult lions exceeds four, hyaenas are often able to displace lions from kills unless a male lion is present (Cooper 1991).",
  qui="S. M. Cooper 1991, African Journal of Ecology 29:130 (cité par le site du IUCN Hyaena Specialist Group)",
  note="Seuil pour des lionnes/subadultes ; déplacement de carcasse plutôt que combat.")
X("lion", "hyene", 1.5, 1.2, nb=4,
  src="https://www.hyaenidae.org/the-hyaenidae/spotted-hyena-crocuta-crocuta/crocuta-association-with-other-species/",
  quote="hyaenas are often able to displace lions from kills unless a male lion is present (Cooper 1991).",
  qui="S. M. Cooper 1991 (via IUCN Hyaena Specialist Group)",
  note="Lion mâle : 4 hyènes ne suffisent pas ; le lion du modèle mélange les sexes, d'où sd élevée.")
X("lion", "hyene", 2.5, 1.1,
  src="https://www.smithsonianmag.com/science-nature/whos-laughing-now-38529396/",
  quote="Holekamp traces 60 percent of the mortalities among her hyenas to lions. [...] “Most hyenas die violently, from lions or people,”",
  qui="Kay Holekamp, Michigan State University (Smithsonian Magazine)",
  note="Énoncé de mortalité, pas de combat : en tête-à-tête le lion domine largement.")

# ---------------------------------------------------------------- Loups contre grizzli
X("ours_brun", "loup", 0.5, 1.2, nb=10,
  src="https://cowboystatedaily.com/2023/01/31/bears-are-still-king-even-though-a-grizzly-lost-a-fight-to-a-pack-of-wolves-in-yellowstone",
  quote="The dominance hierarchy works itself out pretty well in nature with grizzly bears coming out on top",
  qui="Dan Thompson, spécialiste des grands carnivores, Wyoming Game and Fish Department (2023)",
  note="Il juge exceptionnel l'épisode où une meute de 10 loups a chassé un grand grizzli ; écart faible car 10 loups l'ont fait.")
X("ours_brun", "loup", 1.1, 1.2, nb=6,
  src="https://dailymontanan.com/?p=9782",
  quote="It's kind of like Groundhog Day in that scenario",
  qui="Matthew Metz, Yellowstone Wolf Project (avec Aimee Tallian, NINA ; Daily Montanan 2022)",
  note="Décrit les ours qui prennent régulièrement les proies des meutes de Yellowstone (taille de meute typique ~6-10) ; dominance de carcasse.")

# ---------------------------------------------------------------- Orque contre grand requin blanc
X("orque", "requin_blanc", 3.5, 1.0,
  src="https://news.mongabay.com/2019/04/killer-whale-vs-great-white-no-contest-the-shark-always-flees/",
  quote="When confronted by orcas, white sharks will immediately vacate their preferred hunting ground",
  qui="Salvador Jorgensen, Monterey Bay Aquarium (Jorgensen et al. 2019, Scientific Reports 9:6153)",
  note="Fuite systématique aux Farallon ; les orques tuent des requins blancs (Afrique du Sud, Towner et al. 2022).")
X("orque", "requin_blanc", 3.0, 1.1,
  src="https://nhm.ac.uk/discover/news/2022/july/killer-whales-attack-great-white-sharks-changing-marine-ecosystem.html",
  quote="Following an initial orca attack in Gansbaai, individual great white sharks did not appear for weeks or months. [...] What we seem to be witnessing though is a large-scale avoidance strategy.",
  qui="Alison Towner, Dyer Island Conservation Trust (Towner et al. 2022, African Journal of Marine Science)",
  note="Orques en paire (Port et Starboard) contre requins isolés ; individus orques souvent 2 → gap légèrement réduit.")

# ---------------------------------------------------------------- Éléphant contre rhinocéros
X("elephant", "rhinoceros", 2.2, 1.0,
  src="https://pachydermjournal.org/index.php/pachyderm/article/view/1058",
  quote="Between 1991 and 2001 elephants killed 58 white and 5 black rhinos in Hluhluwe-Umfolozi.",
  qui="Slotow, Balfour & Howison 2001, Pachyderm 31:14",
  note="Surtout de jeunes mâles en musth précoce, la plupart des rhinos tués étaient adultes ; aucun cas inverse rapporté.")
X("elephant", "rhinoceros", 2.2, 1.0,
  src="https://www.sciencenews.org/article/really-big-guys-restrain-youth-violence",
  quote="in 5 years, they had killed more than 40 white rhinos.",
  qui="Rob Slotow (University of Natal), Gus van Dyk (écologue du parc), Joyce Poole — Slotow et al. 2000, Nature 408:425 (Pilanesberg)",
  note="Jeunes mâles orphelins, pas des mâles adultes au sommet de leur masse.")
