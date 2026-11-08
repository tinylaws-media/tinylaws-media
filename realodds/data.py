"""Naruto fight database (manga canon + The Last + Boruto manga), coded by hand.

Time axis t = years since Naruto's birth (Kyubi attack = 0). Times inside an arc are offsets so fights stay in order.
Fight tuple: (t, arc, sideA, sideB, result, margin, tagsA, tagsB, note, flags)
  result: "A" = side A wins, "D" = draw / nobody wins
  margin (winner): 1 = serrée / à l'arraché, 2 = nette, 3 = écrasante (ignored for a draw)
  tags (per side): malade, epuise, retenue, protege, surprise, prepa, boost, edo, edo_ctrl, contre, age
  flags: "i" = interrompu (weight 0.5), "?" = codage à vérifier (weight 0.5)
Tier priors (statut au premier combat, en échelons) : 0 civil, 1 genin, 2 genin fort / chuunin, 3 jounin,
4 jounin d'élite, 5 kage, 6 kage d'élite / Akatsuki de pointe, 7 légende, 8 au-delà (Ōtsutsuki, Six Chemins).
These priors are the author's judgement of status, not databook numbers; the fights dominate wherever they exist.
"""

ARCS = [
    ("kaguya", "Ère de Kaguya et du Sage", -1000.0),
    ("clans", "Ère des clans", -70.0),
    ("fondation", "Fondation de Konoha", -56.0),
    ("guerre1", "1re Grande Guerre", -48.0),
    ("guerre2", "2e Grande Guerre", -32.0),
    ("guerre3", "3e Grande Guerre", -4.0),
    ("kyubi", "Attaque de Kyubi", 0.0),
    ("akatsuki", "Massacre des Uchiha, débuts d'Akatsuki", 8.0),
    ("vague", "Pays des Vagues", 12.0),
    ("chunin", "Examen chuunin", 12.3),
    ("invasion", "Invasion de Konoha", 12.5),
    ("tsunade", "Recherche de Tsunade", 12.65),
    ("sasuke", "Poursuite de Sasuke", 12.85),
    ("kazekage", "Sauvetage du Kazekage", 15.5),
    ("tenchi", "Pont du Tenchi", 15.6),
    ("hidan", "Hidan et Kakuzu", 15.8),
    ("itachi", "Poursuite d'Itachi", 16.1),
    ("pain", "Assaut de Pain", 16.4),
    ("sommet", "Sommet des Kage", 16.6),
    ("guerre4a", "4e Grande Guerre : Edo Tensei", 16.9),
    ("guerre4b", "4e Grande Guerre : Obito et Madara", 17.0),
    ("final", "4e Grande Guerre : Kaguya et Vallée de la Fin", 17.08),
    ("last", "The Last", 19.0),
    ("momoshiki", "Boruto : Momoshiki", 32.0),
    ("kara", "Boruto : Kara et Isshiki", 32.2),
    ("tbv", "Boruto : Two Blue Vortex", 36.0),
]

# id: (name, team / village, tier at first fight, death time or None, edo_ref time or None)
# edo_ref = the time whose strength an Edo Tensei body keeps (death time, or prime for Madara)
CHARS = {
    "kaguya": ("Kaguya Ōtsutsuki", "Ōtsutsuki", 8.5, -999.9, -1000.0),
    "hagoromo": ("Hagoromo (Sage des Six Chemins)", "Ōtsutsuki", 8.0, -950, None),
    "hamura": ("Hamura Ōtsutsuki", "Ōtsutsuki", 7.5, -950, None),
    "indra": ("Indra", "Ōtsutsuki", 7.0, -980, None),
    "asura": ("Asura", "Ōtsutsuki", 7.0, -980, None),
    "butsuma": ("Butsuma Senju", "Senju", 5.0, -68, None),
    "tajima": ("Tajima Uchiha", "Uchiha", 5.0, -68, None),
    "hashirama": ("Hashirama Senju", "Konoha", 6.0, -50, -50),
    "madara": ("Madara Uchiha", "Uchiha", 6.0, 17.06, -56),
    "tobirama": ("Tobirama Senju", "Konoha", 5.0, -48, -48),
    "izuna": ("Izuna Uchiha", "Uchiha", 5.0, -62, None),
    "kakuzu": ("Kakuzu", "Akatsuki", 4.0, 15.85, None),
    "kinkaku": ("Kinkaku", "Kumo", 4.5, -40, -40),
    "ginkaku": ("Ginkaku", "Kumo", 4.5, -40, -40),
    "hiruzen": ("Hiruzen Sarutobi", "Konoha", 6.0, 12.5, 12.5),
    "hanzo": ("Hanzō", "Ame", 6.0, 9.0, 9.0),
    "jiraiya": ("Jiraiya", "Konoha", 3.0, 16.2, None),
    "tsunade": ("Tsunade", "Konoha", 3.0, None, None),
    "orochimaru": ("Orochimaru", "Oto", 3.0, None, None),
    "sasori": ("Sasori", "Akatsuki", 4.0, 15.52, 15.52),
    "kazekage3": ("3e Kazekage", "Suna", 5.0, -22, None),
    "minato": ("Minato Namikaze", "Konoha", 5.5, 0.02, 0.02),
    "kushina": ("Kushina Uzumaki", "Konoha", 4.0, 0.02, 0.02),
    "a4": ("A (4e Raikage)", "Kumo", 5.0, None, None),
    "killer_b": ("Killer B", "Kumo", 5.0, None, None),
    "kakashi": ("Kakashi Hatake", "Konoha", 2.0, None, None),
    "obito": ("Obito Uchiha", "Akatsuki", 1.5, 17.06, None),
    "kakkou": ("Kakkō (Iwa)", "Iwa", 3.0, -4, None),
    "kiri_anbu": ("ANBU de Kiri (groupe)", "Kiri", 3.0, -3, None),
    "kurama": ("Kurama (Kyūbi)", "Bijū", 7.0, 33.12, None),
    "nagato": ("Nagato (Pain)", "Akatsuki", 5.0, 16.45, 16.45),
    "konan": ("Konan", "Akatsuki", 3.0, 16.75, None),
    "itachi": ("Itachi Uchiha", "Akatsuki", 5.5, 16.1, 16.1),
    "kisame": ("Kisame Hoshigaki", "Akatsuki", 5.0, 16.88, None),
    "gozu": ("Gōzu", "Kiri", 2.0, None, None),
    "meizu": ("Meizu", "Kiri", 2.0, None, None),
    "zabuza": ("Zabuza Momochi", "Kiri", 3.5, 12.06, 12.06),
    "haku": ("Haku", "Kiri", 2.5, 12.06, 12.06),
    "naruto": ("Naruto Uzumaki", "Konoha", 1.0, None, None),
    "sasuke": ("Sasuke Uchiha", "Konoha", 1.5, None, None),
    "sakura": ("Sakura Haruno", "Konoha", 0.8, None, None),
    "rock_lee": ("Rock Lee", "Konoha", 2.0, None, None),
    "gai": ("Might Gai", "Konoha", 4.5, None, None),
    "neji": ("Neji Hyūga", "Konoha", 2.0, 16.997, None),
    "hinata": ("Hinata Hyūga", "Konoha", 1.0, None, None),
    "tenten": ("Tenten", "Konoha", 1.2, None, None),
    "shikamaru": ("Shikamaru Nara", "Konoha", 1.3, None, None),
    "ino": ("Ino Yamanaka", "Konoha", 0.8, None, None),
    "choji": ("Chōji Akimichi", "Konoha", 1.2, None, None),
    "kiba": ("Kiba Inuzuka", "Konoha", 1.2, None, None),
    "shino": ("Shino Aburame", "Konoha", 1.4, None, None),
    "asuma": ("Asuma Sarutobi", "Konoha", 4.0, 15.8, 15.8),
    "kurenai": ("Kurenai Yūhi", "Konoha", 3.0, None, None),
    "izumo": ("Izumo", "Konoha", 2.0, None, None),
    "kotetsu": ("Kotetsu", "Konoha", 2.0, None, None),
    "gaara": ("Gaara", "Suna", 2.5, None, None),
    "kankuro": ("Kankurō", "Suna", 1.6, None, None),
    "temari": ("Temari", "Suna", 1.8, None, None),
    "chiyo": ("Chiyo", "Suna", 4.0, 15.53, None),
    "kabuto": ("Kabuto Yakushi", "Oto", 2.5, None, None),
    "yoroi": ("Yoroi Akadō", "Oto", 1.5, None, None),
    "misumi": ("Misumi Tsurugi", "Oto", 1.5, None, None),
    "dosu": ("Dosu Kinuta", "Oto", 1.5, 12.5, None),
    "zaku": ("Zaku Abumi", "Oto", 1.3, 12.5, None),
    "kin": ("Kin Tsuchi", "Oto", 1.0, 12.5, None),
    "ame_genin": ("Genin d'Ame (groupe)", "Ame", 1.0, 12.3, None),
    "jirobo": ("Jirōbō", "Oto", 2.5, 12.85, None),
    "kidomaru": ("Kidōmaru", "Oto", 2.5, 12.85, None),
    "sakon": ("Sakon et Ukon", "Oto", 2.5, 12.85, None),
    "tayuya": ("Tayuya", "Oto", 2.5, 12.85, None),
    "kimimaro": ("Kimimaro", "Oto", 3.5, 12.85, None),
    "deidara": ("Deidara", "Akatsuki", 4.5, 16.05, None),
    "hidan": ("Hidan", "Akatsuki", 4.5, None, None),
    "yamato": ("Yamato", "Konoha", 3.5, None, None),
    "sai": ("Sai", "Konoha", 2.5, None, None),
    "danzo": ("Danzō Shimura", "Konoha", 4.5, 16.62, None),
    "suigetsu": ("Suigetsu", "Taka", 3.0, None, None),
    "karin": ("Karin", "Taka", 1.5, None, None),
    "jugo": ("Jūgo", "Taka", 3.0, None, None),
    "mei": ("Mei Terumī (5e Mizukage)", "Kiri", 5.0, None, None),
    "ao": ("Ao", "Kiri", 3.5, None, None),
    "chojuro": ("Chōjūrō", "Kiri", 3.0, None, None),
    "onoki": ("Ōnoki (3e Tsuchikage)", "Iwa", 5.0, None, None),
    "mu": ("Mū (2e Tsuchikage)", "Iwa", 5.0, -30, -30),
    "darui": ("Darui", "Kumo", 4.0, None, None),
    "mifune": ("Mifune", "Pays du Fer", 4.5, None, None),
    "hinata_last": None,  # placeholder removed below
    "alliance": ("Armée de l'Alliance (groupe)", "Alliance", 4.0, None, None),
    "toneri": ("Toneri Ōtsutsuki", "Ōtsutsuki", 6.0, None, None),
    "boruto": ("Boruto Uzumaki", "Konoha", 3.0, None, None),
    "momoshiki": ("Momoshiki Ōtsutsuki", "Ōtsutsuki", 8.0, 32.05, None),
    "kinshiki": ("Kinshiki Ōtsutsuki", "Ōtsutsuki", 7.5, 32.04, None),
    "jigen": ("Jigen (Isshiki dans un corps)", "Kara", 7.5, 33.05, None),
    "isshiki": ("Isshiki Ōtsutsuki (vraie forme)", "Ōtsutsuki", 8.5, 33.1, None),
    "kashin_koji": ("Kashin Koji", "Kara", 6.0, None, None),
    "code": ("Code", "Kara", 6.5, None, None),
    "yugito": ("Yugito Nii (Nibi)", "Kumo", 5.0, 15.3, None),
    "baki": ("Baki", "Suna", 3.5, None, None),
    "hayate": ("Hayate Gekkō", "Konoha", 3.0, 12.33, None),
    "anko": ("Anko Mitarashi", "Konoha", 3.0, None, None),
    "raikage3": ("A (3e Raikage)", "Kumo", 5.5, -10, -10),
    "rasa": ("Rasa (4e Kazekage)", "Suna", 5.0, 12.4, 12.4),
    "shin": ("Shin Uchiha", "Akatsuki", 5.5, 31.5, None),
    "boro": ("Boro", "Kara", 6.0, 33.02, None),
    "kurotsuchi": ("Kurotsuchi (4e Tsuchikage)", "Iwa", 5.0, None, None),
    "jura": ("Jura", "Arbres-Dieux", 7.5, None, None),
    "hidari": ("Hidari", "Arbres-Dieux", 6.5, None, None),
    "matsuri": ("Matsuri", "Arbres-Dieux", 6.0, 36.3, None),
    "kawaki": ("Kawaki", "Konoha", 4.0, None, None),
    "sarada": ("Sarada Uchiha", "Konoha", 2.5, None, None),
    "taiseki": ("Taiseki (Iwa)", "Iwa", 3.0, -4.005, None),
    "yahiko": ("Yahiko", "Ame", 3.0, -2.9, None),
    "kumo_ninja": ("Ninjas de Kumo (groupe)", "Kumo", 2.0, -12.0, None),
    "hiashi": ("Hiashi Hyūga", "Konoha", 4.0, None, None),
    "kumo_chef": ("Chef ninja de Kumo (affaire Hyūga)", "Kumo", 3.0, 3.3, None),
    "shisui": ("Shisui Uchiha", "Konoha", 5.0, 7.985, None),
    "uchiha_police": ("Police Uchiha (groupe)", "Uchiha", 2.5, 8.01, None),
    "mizuki": ("Mizuki", "Konoha", 2.0, None, None),
    "konohamaru": ("Konohamaru Sarutobi", "Konoha", 1.5, None, None),
    "shizune": ("Shizune", "Konoha", 3.0, None, None),
    "fu_root": ("Fū Yamanaka (Racine)", "Konoha", 3.5, 16.615, None),
    "torune": ("Torune Aburame (Racine)", "Konoha", 3.5, 16.615, None),
    "gengetsu": ("Gengetsu Hōzuki (2e Mizukage)", "Kiri", 5.0, -30, -30),
    "mitsuki": ("Mitsuki", "Konoha", 3.0, None, None),
    "garo": ("Garō", "Kara", 4.5, 32.5, None),
    "delta": ("Delta", "Kara", 5.5, None, None),
    "daemon": ("Daemon", "Kara", 7.5, None, None),
    "ryu": ("Ryū (Arbre-Dieu, copie de Shinki)", "Arbres-Dieux", 6.5, 36.28, None),
    "mamushi": ("Mamushi (copie de Bug)", "Arbres-Dieux", 6.5, 36.45, None),
    "himawari": ("Himawari Uzumaki", "Konoha", 4.5, None, None),
}
del CHARS["hinata_last"]

GENERIC = {"alliance", "ame_genin", "kiri_anbu", "kumo_ninja", "uchiha_police"}

# permanent power-ups / losses: (char, time, mean change in tiers, sd)
JUMPS = [
    ("naruto", 16.35, 1.5, 1.0, "Mode Ermite"),
    ("naruto", 16.8, 1.5, 1.0, "Mode Chakra de Kyūbi"),
    ("naruto", 17.03, 2.0, 1.0, "Pouvoir des Six Chemins"),
    ("naruto", 33.08, 0.0, 1.0, "Mode Baryon (puis perte de Kurama)"),
    ("naruto", 33.12, -1.5, 1.0, "Mort de Kurama"),
    ("sasuke", 16.12, 1.0, 1.0, "Mangekyō Sharingan"),
    ("sasuke", 16.7, 1.0, 1.0, "Mangekyō éternel"),
    ("sasuke", 17.03, 2.0, 1.0, "Rinnegan, pouvoir des Six Chemins"),
    ("sasuke", 33.09, -1.0, 0.8, "Perte du Rinnegan"),
    ("kakashi", 15.0, 0.5, 0.6, "Mangekyō Sharingan"),
    ("kakashi", 17.04, 1.5, 0.8, "Double Mangekyō et Susanoo (chakra d'Obito)"),
    ("kakashi", 17.1, -2.0, 0.8, "Perte des deux Mangekyō"),
    ("konohamaru", 30.0, 2.5, 1.0, "Jōnin adulte"),
    ("kawaki", 35.0, 1.5, 1.0, "Ellipse de Two Blue Vortex"),
    ("sarada", 35.0, 1.5, 1.0, "Ellipse de Two Blue Vortex"),
    ("obito", 16.999, 2.5, 1.0, "Jinchūriki de Jūbi"),
    ("madara", 17.011, 1.0, 1.0, "Retour à la vie, Rinnegan"),
    ("madara", 17.02, 2.0, 1.0, "Jinchūriki de Jūbi"),
    ("gaara", 15.55, -0.5, 0.6, "Extraction de Shukaku"),
    ("kabuto", 16.8, 2.0, 1.0, "Mode Ermite et cellules"),
    ("boruto", 35.0, 1.5, 1.0, "Ellipse de Two Blue Vortex"),
]

F = []


def fight(t, arc, a, b, res, m=2, ta=(), tb=(), note="", flags=""):
    a = [a] if isinstance(a, str) else list(a)
    b = [b] if isinstance(b, str) else list(b)
    F.append(dict(t=t, arc=arc, a=a, b=b, res=res, m=m, ta=list(ta), tb=list(tb), note=note, flags=flags))


# ---------------------------------------------------------------- ère de Kaguya
fight(-1000.0, "kaguya", ["hagoromo", "hamura"], "kaguya", "A", 2, note="Les deux frères scellent leur mère")
fight(-990, "kaguya", "asura", "indra", "D", note="Indra défie Asura ; le manga ne montre pas l'issue", flags="?")
# ---------------------------------------------------------------- ère des clans
fight(-72, "clans", "butsuma", "tajima", "D", note="Chefs Senju et Uchiha, rivalité sans vainqueur", flags="?")
fight(-70, "clans", "hashirama", "madara", "D", note="Combats de jeunesse sans vainqueur")
fight(-66, "clans", "hashirama", "madara", "D", note="Combats répétés entre chefs de clan")
fight(-62.5, "clans", "tobirama", "izuna", "A", 2, note="Izuna mortellement blessé")
fight(-62, "clans", "hashirama", "madara", "A", 2, tb=["epuise"], note="Madara, après la mort d'Izuna, accepte la paix")
# ---------------------------------------------------------------- fondation
fight(-57, "fondation", "hashirama", "kakuzu", "A", 3, tb=["surprise"], note="Kakuzu échoue à assassiner Hashirama")
fight(-56, "fondation", "hashirama", ["madara", "kurama"], "A", 2, note="Vallée de la Fin ; Madara survit grâce à Izanagi")
# ---------------------------------------------------------------- 1re guerre
fight(-48, "guerre1", ["kinkaku", "ginkaku"], "tobirama", "A", 1, ta=["surprise"], tb=["protege"],
      note="Embuscade de la Force Kinkaku ; Tobirama se sacrifie pour couvrir l'équipe", flags="?")
# ---------------------------------------------------------------- 2e guerre
fight(-32, "guerre2", "hanzo", ["jiraiya", "tsunade", "orochimaru"], "A", 3, ta=["retenue"],
      note="Hanzō bat les trois futurs Sannin et leur donne leur surnom")
fight(-22, "guerre2", "sasori", "kazekage3", "A", 2, ta=["prepa"], note="Sasori fait du 3e Kazekage une marionnette", flags="?")
# ---------------------------------------------------------------- 3e guerre
fight(-5, "guerre3", "minato", ["a4", "killer_b"], "D", note="Choc de la 3e guerre, sans vainqueur", flags="i")
fight(-4.0, "guerre3", "kakkou", ["kakashi", "obito"], "A", 1, tb=["epuise"], note="Obito écrasé par le rocher")
fight(-3.99, "guerre3", "kakashi", "kakkou", "A", 2, ta=["boost"], note="Sharingan d'Obito, Chidori")
fight(-3, "guerre3", "obito", "kiri_anbu", "A", 3, ta=["boost"], note="Après la mort de Rin")
fight(1.5, "kyubi", "hiruzen", "orochimaru", "A", 1, ta=["retenue"], note="Hiruzen laisse fuir Orochimaru", flags="?")
# ---------------------------------------------------------------- Kyūbi
fight(0.0, "kyubi", "minato", "obito", "A", 2, note="Minato libère Kurama du contrôle d'Obito")
fight(0.01, "kyubi", ["minato", "kushina"], "kurama", "A", 2, ta=["epuise", "prepa"], note="Scellement de Kurama dans Naruto (un scellement plus qu'un duel)", flags="?")
# ---------------------------------------------------------------- Akatsuki
fight(9.0, "akatsuki", "nagato", "hanzo", "A", 3, note="Nagato tue Hanzō et prend Ame", flags="?")
fight(9.5, "akatsuki", "itachi", "orochimaru", "A", 3, note="Orochimaru tente de prendre le corps d'Itachi")
# ---------------------------------------------------------------- Pays des Vagues
fight(12.0, "vague", "kakashi", ["gozu", "meizu"], "A", 3, note="Les Frères Démons")
fight(12.02, "vague", "kakashi", "zabuza", "A", 2, ta=["epuise"], tb=["surprise"],
      note="Prison d'eau puis Kakashi l'emporte, Haku emporte Zabuza")
fight(12.05, "vague", "haku", "sasuke", "A", 2, ta=["prepa"], note="Miroirs de glace")
fight(12.051, "vague", "naruto", "haku", "A", 2, ta=["boost"], note="Première sortie du chakra de Kurama")
fight(12.055, "vague", "kakashi", "zabuza", "A", 2, ta=["prepa"], note="Chiens ninja, sur le pont")
# ---------------------------------------------------------------- examen chuunin
fight(12.25, "chunin", "rock_lee", "sasuke", "A", 3, note="Avant l'examen")
fight(12.28, "chunin", "orochimaru", ["sasuke", "naruto", "sakura"], "A", 3, ta=["retenue"], note="Forêt de la Mort")
fight(12.29, "chunin", "dosu", "rock_lee", "A", 2, note="Forêt de la Mort", flags="?")
fight(12.291, "chunin", "sasuke", ["zaku", "dosu", "kin"], "A", 3, ta=["boost"], note="Marque maudite niveau 1")
fight(12.292, "chunin", "gaara", "ame_genin", "A", 3, note="Forêt de la Mort")
fight(12.31, "chunin", "sasuke", "yoroi", "A", 2, ta=["epuise"], note="Éliminatoires")
fight(12.311, "chunin", "shino", "zaku", "A", 3, tb=["epuise"], note="Éliminatoires")
fight(12.312, "chunin", "kankuro", "misumi", "A", 3, note="Éliminatoires")
fight(12.313, "chunin", "sakura", "ino", "D", note="Éliminatoires, double KO")
fight(12.314, "chunin", "temari", "tenten", "A", 3, note="Éliminatoires")
fight(12.315, "chunin", "shikamaru", "kin", "A", 2, note="Éliminatoires")
fight(12.316, "chunin", "naruto", "kiba", "A", 1, note="Éliminatoires")
fight(12.317, "chunin", "neji", "hinata", "A", 3, note="Éliminatoires")
fight(12.318, "chunin", "gaara", "rock_lee", "A", 2, tb=["boost"], note="Éliminatoires, Lee ouvre cinq portes")
fight(12.319, "chunin", "dosu", "choji", "A", 2, note="Éliminatoires")
fight(12.45, "chunin", "naruto", "neji", "A", 1, ta=["boost"], note="Finale")
fight(12.451, "chunin", "temari", "shikamaru", "D", note="Shikamaru abandonne alors qu'il la tient")
fight(12.452, "chunin", "sasuke", "gaara", "A", 2, note="Finale interrompue par l'invasion", flags="i")
# ---------------------------------------------------------------- invasion
fight(12.5, "invasion", "orochimaru", "hiruzen", "A", 1, tb=["age"],
      note="Hiruzen meurt mais scelle les bras d'Orochimaru ; Edo Hashirama et Tobirama affaiblis")
fight(12.501, "invasion", "gaara", "sasuke", "A", 2, ta=["boost"], tb=["epuise"], note="Gaara à demi transformé")
fight(12.502, "invasion", "naruto", "gaara", "A", 2, ta=["boost"], tb=["boost"], note="Gamabunta contre Shukaku")
fight(12.503, "invasion", "shino", "kankuro", "D", flags="i")
fight(12.55, "invasion", "itachi", "kakashi", "A", 3, note="Tsukuyomi")
fight(12.551, "invasion", "itachi", "kurenai", "A", 2)
fight(12.552, "invasion", "asuma", "kisame", "D", flags="i")
fight(12.553, "invasion", "gai", "kisame", "D", flags="i")
fight(12.6, "invasion", "itachi", "sasuke", "A", 3, ta=["retenue"], note="À l'auberge")
fight(12.601, "invasion", "jiraiya", ["itachi", "kisame"], "D", 1, tb=["retenue"], note="Itachi et Kisame fuient", flags="i")
# ---------------------------------------------------------------- Tsunade
fight(12.65, "tsunade", "kabuto", "tsunade", "A", 1, tb=["malade"], note="Peur du sang de Tsunade")
fight(12.651, "tsunade", "naruto", "kabuto", "A", 1, ta=["epuise"], note="Premier Rasengan en combat")
fight(12.652, "tsunade", ["tsunade", "jiraiya"], ["orochimaru", "kabuto"], "A", 1, ta=["epuise"], tb=["epuise"],
      note="Jiraiya drogué, Orochimaru sans bras")
fight(12.75, "tsunade", "sasuke", "naruto", "D", note="Sur le toit de l'hôpital, arrêté par Kakashi", flags="i")
# ---------------------------------------------------------------- poursuite de Sasuke
fight(12.85, "sasuke", "choji", "jirobo", "A", 2, ta=["boost"], note="Pilules Akimichi")
fight(12.851, "sasuke", "neji", "kidomaru", "A", 1)
fight(12.852, "sasuke", "sakon", "kiba", "A", 2)
fight(12.853, "sasuke", "kankuro", "sakon", "A", 3)
fight(12.854, "sasuke", "tayuya", "shikamaru", "A", 1, flags="i")
fight(12.855, "sasuke", "temari", "tayuya", "A", 3)
fight(12.856, "sasuke", "kimimaro", "rock_lee", "A", 1, tb=["epuise"], note="Lee juste opéré", flags="i")
fight(12.857, "sasuke", "gaara", "kimimaro", "D", tb=["malade"], note="Kimimaro meurt de sa maladie en plein assaut")
fight(12.86, "sasuke", "sasuke", "naruto", "A", 1, ta=["boost", "retenue"], tb=["boost"], note="1re Vallée de la Fin")
# ---------------------------------------------------------------- Shippuden : Kazekage
fight(15.4, "kazekage", ["naruto", "sakura"], "kakashi", "A", 1, tb=["retenue"], note="Test des clochettes")
fight(15.5, "kazekage", "deidara", "gaara", "A", 2, tb=["protege"], note="Gaara protège le village")
fight(15.51, "kazekage", "sasori", "kankuro", "A", 3)
fight(15.52, "kazekage", ["sakura", "chiyo"], "sasori", "A", 1, ta=["prepa"], note="Chiyo connaît les marionnettes de Sasori")
fight(15.521, "kazekage", ["naruto", "kakashi"], "deidara", "A", 2)
# ---------------------------------------------------------------- Tenchi
fight(15.6, "tenchi", "naruto", "orochimaru", "D", ta=["boost"], note="Naruto à 4 queues hors de contrôle")
fight(15.62, "tenchi", "sasuke", ["naruto", "sakura", "sai", "yamato"], "A", 2, ta=["retenue"], note="Repaire d'Orochimaru", flags="i")
# ---------------------------------------------------------------- Hidan et Kakuzu
fight(15.8, "hidan", ["hidan", "kakuzu"], ["asuma", "shikamaru", "izumo", "kotetsu"], "A", 2, note="Mort d'Asuma")
fight(15.84, "hidan", "shikamaru", "hidan", "A", 2, ta=["prepa"], note="Piège dans la forêt Nara")
fight(15.841, "hidan", "kakuzu", ["kakashi", "ino", "choji"], "A", 1, flags="i")
fight(15.842, "hidan", ["naruto", "kakashi"], "kakuzu", "A", 3, ta=["surprise"], note="Rasenshuriken, Kakashi l'achève (ch. 343-344)")
# ---------------------------------------------------------------- poursuite d'Itachi
fight(15.9, "itachi", "sasuke", "orochimaru", "A", 3, tb=["malade"])
fight(16.05, "itachi", "sasuke", "deidara", "A", 1, ta=["contre"], note="Deidara s'autodétruit")
fight(16.1, "itachi", "sasuke", "itachi", "A", 1, tb=["malade", "retenue"], note="Itachi mourant, se retient")
fight(16.2, "itachi", "nagato", "jiraiya", "A", 2, note="Les six chemins de Pain")
fight(16.19, "itachi", "jiraiya", "konan", "A", 3)
fight(16.3, "itachi", "killer_b", ["sasuke", "karin", "suigetsu", "jugo"], "A", 1, note="B s'échappe avec un faux corps")
# ---------------------------------------------------------------- Pain
fight(16.4, "pain", "nagato", "kakashi", "A", 2, ta=["prepa"])
fight(16.42, "pain", "nagato", "hinata", "A", 3)
fight(16.43, "pain", "naruto", "nagato", "A", 2, note="Mode Ermite")
# ---------------------------------------------------------------- Sommet des Kage
fight(16.6, "sommet", "a4", "sasuke", "A", 2, flags="i")
fight(16.61, "sommet", "mei", "sasuke", "A", 2, tb=["epuise"], flags="i")
fight(16.62, "sommet", "sasuke", "danzo", "A", 1, tb=["epuise"])
fight(16.63, "sommet", "kakashi", "sasuke", "A", 1, tb=["epuise"], flags="i")
fight(16.65, "sommet", "naruto", "sasuke", "D", flags="i")
fight(16.75, "sommet", "obito", "konan", "A", 1, tb=["prepa"], note="Six cents milliards de parchemins, Izanagi")
# ---------------------------------------------------------------- 4e guerre : Edo Tensei
fight(16.8, "sommet", ["naruto", "kushina"], "kurama", "A", 2, note="Naruto prend le chakra de Kurama, dans sa tête", flags="?")
fight(16.612, "sommet", "kisame", "killer_b", "A", 1, note="B inconscient dans le dôme d'eau, Samehada trahit Kisame (ch. 470-472)", flags="i")
fight(16.613, "sommet", ["killer_b", "a4"], "kisame", "A", 2, tb=["epuise"], note="Double Lariat ; Kisame survit caché dans Samehada (ch. 473)", flags="?")
fight(16.87, "sommet", ["gai", "killer_b"], "kisame", "A", 2, ta=["boost"], note="Île-tortue : Kisame se tue pour ne rien révéler (ch. 505-507)")
fight(16.9, "guerre4a", "kakashi", ["zabuza", "haku"], "A", 2, tb=["edo"])
fight(16.91, "guerre4a", "darui", ["kinkaku", "ginkaku"], "A", 2, ta=["prepa"], tb=["edo"], note="Outils de scellement")
fight(16.92, "guerre4a", ["gaara", "onoki", "naruto"], "mu", "A", 2, tb=["edo"])
fight(16.93, "guerre4a", "kankuro", "sasori", "A", 2, tb=["edo", "retenue"])
fight(16.94, "guerre4a", ["shikamaru", "ino", "choji"], "asuma", "A", 2, tb=["edo", "edo_ctrl"])
fight(16.95, "guerre4a", "mifune", "hanzo", "A", 2, tb=["edo"])
fight(16.96, "guerre4a", ["naruto", "killer_b", "itachi"], "nagato", "A", 2, tb=["edo"])
fight(16.97, "guerre4a", ["itachi", "sasuke"], "kabuto", "A", 2, note="Izanami")
fight(16.98, "guerre4a", "madara", ["onoki", "a4", "gaara", "mei", "tsunade"], "A", 3, ta=["edo"], note="Madara contre les cinq Kage")
# ---------------------------------------------------------------- 4e guerre : Obito et Madara
fight(16.99, "guerre4b", "obito", ["naruto", "killer_b", "kakashi", "gai"], "D", ta=["prepa"], note="Les six chemins d'Obito détruits, il réveille Jūbi", flags="i")
fight(17.01, "guerre4b", ["naruto", "sasuke", "minato", "alliance"], "obito", "A", 2, note="Obito jinchūriki de Jūbi tombe")
fight(16.997, "guerre4b", "kakashi", "obito", "D", note="Dans la dimension de Kamui, chacun blesse l'autre")
fight(16.996, "guerre4b", ["naruto", "kakashi"], "obito", "A", 1, note="Rasengan et Kamui, masque d'Obito brisé")
fight(17.008, "guerre4b", "madara", "hashirama", "D", ta=["edo"], tb=["edo"], flags="i")
fight(17.005, "guerre4b", "obito", ["hashirama", "tobirama", "hiruzen", "minato"], "A", 2, tb=["edo"], note="Obito jinchūriki de Jūbi brise la Barrière rouge et transperce les Hokage (ch. 638-643)")
fight(17.03, "guerre4b", "madara", "gai", "A", 1, tb=["boost"], note="Gai ouvre la 8e porte")
fight(17.035, "guerre4b", ["naruto", "sasuke"], "madara", "A", 1, note="Pouvoir des Six Chemins ; Madara s'échappe et lance le Tsukuyomi infini (ch. 673-674)", flags="i")
# ---------------------------------------------------------------- Kaguya et Vallée de la Fin
fight(17.05, "final", ["naruto", "sasuke", "kakashi", "sakura", "obito"], "kaguya", "A", 2, note="Kaguya scellée")
fight(17.08, "final", "naruto", "sasuke", "A", 1, note="Dernière Vallée de la Fin : chacun perd un bras, Sasuke dit « j'ai perdu »")
# ---------------------------------------------------------------- The Last
fight(19.0, "last", "toneri", "naruto", "A", 2, ta=["prepa"], flags="?")
fight(19.02, "last", "naruto", "toneri", "A", 2, note="Naruto libère Hinata")
# ---------------------------------------------------------------- Boruto
fight(32.0, "momoshiki", ["momoshiki", "kinshiki"], ["naruto", "sasuke", "gaara", "kankuro", "chojuro", "darui", "kurotsuchi"], "A", 2,
      tb=["protege"], note="Attaque de la finale de l'examen ; Naruto capturé")
fight(32.03, "momoshiki", ["sasuke", "naruto", "gaara", "darui", "chojuro", "kurotsuchi"], "kinshiki", "A", 2, flags="?")
fight(32.05, "momoshiki", ["naruto", "sasuke", "boruto"], "momoshiki", "A", 2, ta=["surprise"], note="Rasengan de Boruto")
fight(33.0, "kara", "jigen", ["naruto", "sasuke"], "A", 2, note="Naruto scellé dans une autre dimension")
fight(33.05, "kara", "kashin_koji", "jigen", "A", 2, tb=["epuise"], note="Jigen, épuisé par Naruto et Sasuke, meurt dans les flammes de Koji")
fight(33.07, "kara", "isshiki", "kashin_koji", "A", 3, note="Koji s'échappe gravement blessé")
fight(33.08, "kara", "naruto", "isshiki", "A", 2, ta=["boost"], tb=["malade"], note="Mode Baryon ; le temps d'Isshiki est compté")
fight(36.0, "tbv", "boruto", "code", "A", 1, note="Code se retire grâce à l'intervention de Kawaki (ch. 2-3)", flags="i")

# ---------------------------------------------------------------- ajouts
fight(11.995, "vague", "kakashi", ["naruto", "sasuke", "sakura"], "A", 3, ta=["retenue"], note="Test des clochettes")
fight(12.29, "chunin", "orochimaru", "anko", "A", 2, note="Forêt de la Mort")
fight(12.33, "chunin", "baki", "hayate", "A", 2, ta=["surprise"], note="Baki tue Hayate")
fight(15.3, "kazekage", ["hidan", "kakuzu"], "yugito", "A", 2, note="Capture de Nibi")
fight(15.53, "kazekage", ["gai", "rock_lee", "neji", "tenten"], "kisame", "A", 2, tb=["retenue"], note="Copie de Kisame à 30 % du chakra")
fight(15.531, "kazekage", ["naruto", "kakashi", "sakura", "chiyo"], "itachi", "A", 2, tb=["retenue"], note="Copie d'Itachi")
fight(16.12, "itachi", ["naruto", "kakashi", "yamato", "hinata", "kiba", "shino"], "obito", "D", tb=["retenue"], note="Tobi joue avec eux", flags="i")
fight(16.61, "sommet", "gaara", "sasuke", "D", flags="i")
fight(16.905, "guerre4a", ["naruto", "alliance"], "raikage3", "A", 2, tb=["edo"], note="Naruto et l'équipe de scellement (ch. 554-555)")
fight(16.921, "guerre4a", "gaara", "rasa", "A", 2, tb=["edo", "retenue"], note="(ch. 546-547)")
fight(16.955, "guerre4a", ["naruto", "killer_b"], "itachi", "D", tb=["edo_ctrl"], note="Itachi se libère du contrôle", flags="i")
fight(31.5, "momoshiki", ["sasuke", "naruto"], "shin", "A", 3, note="Naruto Gaiden", flags="?")
fight(33.02, "kara", ["boruto", "sarada", "mitsuki", "kawaki"], "boro", "A", 2, ta=["boost"], note="Momoshiki prend le corps de Boruto pour l'achever (ch. 40-43)")
fight(33.06, "kara", "isshiki", ["naruto", "sasuke", "boruto", "kawaki"], "A", 2, note="Avant le mode Baryon")

fight(16.63, "sommet", "sasuke", "sakura", "A", 3, tb=["retenue"], note="Sakura n'ose pas frapper ; Kakashi intervient", flags="i")
fight(36.1, "tbv", "jura", "himawari", "A", 3, note="Himawari s'évanouit, Boruto la téléporte")
fight(36.12, "tbv", ["boruto", "sarada", "kawaki"], "hidari", "A", 2, note="Uzuhiko, puis Kawaki l'achève")
fight(36.05, "tbv", "jura", "kawaki", "A", 3, note="Un seul coup (ch. 8)")
fight(36.3, "tbv", "boruto", "matsuri", "A", 2, note="Boruto la tranche avec le sabre de Sasuke")
fight(36.31, "tbv", "jura", "boruto", "A", 3, note="Jura annule l'Uzuhiko")

# ---------------------------------------------------------------- recherche du 8 nov. (Narutopedia, chapitres)
fight(-12.0, "guerre2", "minato", "kumo_ninja", "A", 3, note="Minato libère Kushina enlevée par Kumo (ch. 498)", flags="?")
fight(-4.005, "guerre3", ["obito", "kakashi"], "taiseki", "A", 1, tb=["surprise"], note="Taiseki crève l'œil de Kakashi ; Obito éveille son Sharingan et le tue (ch. 242)")
fight(-2.9, "guerre3", "hanzo", ["yahiko", "nagato", "konan"], "A", 2, ta=["prepa"], note="Piège de Hanzō allié à Danzō, mort de Yahiko (ch. 446)", flags="?")
fight(-2.899, "guerre3", "nagato", "hanzo", "A", 1, ta=["boost"], note="Statue démoniaque ; Hanzō s'enfuit, Nagato a les jambes détruites (ch. 447)", flags="i")
fight(3.3, "kyubi", "hiashi", "kumo_chef", "A", 3, tb=["surprise"], note="Affaire Hyūga (ch. 102)")
fight(7.98, "akatsuki", "danzo", "shisui", "A", 1, ta=["surprise"], note="Danzō vole l'œil droit de Shisui (ch. 590)", flags="?")
fight(8.0, "akatsuki", "itachi", "uchiha_police", "A", 3, note="Yashiro, Inabi et Tekka (ch. 222)")
fight(11.0, "akatsuki", "itachi", "deidara", "A", 3, note="Recrutement de Deidara (ch. 359)", flags="?")
fight(11.99, "vague", "naruto", "mizuki", "A", 3, note="Multiclonage, Naruto protège Iruka (ch. 1)")
fight(12.4, "chunin", "gaara", "dosu", "A", 3, note="Gaara tue Dosu avant la finale (ch. 91)")
fight(12.649, "tsunade", "tsunade", "naruto", "A", 3, ta=["retenue"], note="Pari du collier (ch. 159)")
fight(12.8555, "sasuke", "kimimaro", "naruto", "A", 2, note="Jusqu'à l'arrivée de Lee (ch. 206-209)", flags="i")
fight(15.92, "itachi", ["sasuke", "suigetsu"], "jugo", "A", 2, ta=["retenue"], note="Recrutement de Jūgo (ch. 350-351)")
fight(16.402, "pain", "konohamaru", "nagato", "A", 1, ta=["surprise"], tb=["retenue"], note="Contre le seul chemin des Enfers (ch. 426-428)", flags="?")
fight(16.403, "pain", "nagato", "shizune", "A", 3, note="Le chemin des Humains (ch. 428-429)")
fight(16.41, "pain", "naruto", "nagato", "A", 2, ta=["prepa"], note="Mode Ermite : cinq chemins détruits (ch. 430-433)")
fight(16.415, "pain", "nagato", "naruto", "A", 2, tb=["epuise"], note="Hors du Mode Ermite, Tendō cloue Naruto (ch. 433-436)")
fight(16.425, "pain", "naruto", "nagato", "D", ta=["boost"], note="Naruto à six puis huit queues contre Tendō (ch. 438-440)", flags="i")
fight(16.598, "sommet", "a4", "jugo", "A", 3, tb=["boost"], note="(ch. 461-462)")
fight(16.599, "sommet", "darui", "suigetsu", "A", 2, note="(ch. 462-464 env.)", flags="?")
fight(16.615, "sommet", "obito", ["fu_root", "torune"], "A", 3, note="Kamui (ch. 474-475)")
fight(16.922, "guerre4a", ["gaara", "onoki"], "gengetsu", "A", 2, ta=["epuise"], tb=["edo"], note="(ch. 556-557)")
fight(16.975, "guerre4a", "madara", ["gaara", "onoki", "alliance"], "A", 2, ta=["edo"], note="Météores sur la 4e division (ch. 560-562)")
fight(17.012, "guerre4b", "madara", ["naruto", "gaara", "kurama"], "A", 2, note="Madara ressuscité scelle à nouveau les bijū (ch. 658-661)")
fight(17.013, "guerre4b", "madara", ["tobirama", "sasuke"], "A", 2, tb=["edo"], note="(ch. 661)")
fight(32.29, "kara", "ao", "konohamaru", "A", 2, note="(ch. 19-20)", flags="?")
fight(32.3, "kara", ["boruto", "sarada", "mitsuki", "konohamaru"], "ao", "A", 1, ta=["prepa"], note="(ch. 21-22)")
fight(32.32, "kara", "kashin_koji", ["konohamaru", "boruto", "sarada", "mitsuki"], "A", 2, note="(ch. 23)", flags="i")
fight(32.5, "kara", "kawaki", "garo", "A", 3, note="(ch. 25)")
fight(32.7, "kara", "naruto", "delta", "A", 2, ta=["retenue"], note="Naruto protège les enfants (ch. 30-33)")
fight(33.09, "kara", ["kawaki", "sasuke"], "boruto", "A", 1, tb=["boost"], note="Momoshiki possède Boruto et crève le Rinnegan de Sasuke (ch. 53-54)")
fight(33.2, "kara", "code", "kawaki", "A", 2, note="(ch. 62)")
fight(33.21, "kara", "code", "boruto", "A", 1, tb=["boost"], note="Code domine Boruto, puis se retire sur ordre d'Eida (ch. 63-65)", flags="i")
fight(33.23, "kara", "code", "kawaki", "A", 2, ta=["prepa"], note="Daemon par une griffe (ch. 67)")
fight(33.3, "kara", "daemon", "code", "A", 3, note="(ch. 71-72)")
fight(34.2, "kara", "code", ["sasuke", "boruto"], "A", 1, note="Sasuke se sacrifie pour que Boruto fuie (TBV ch. 5)")
fight(36.02, "tbv", ["hidari", "matsuri"], ["boruto", "code"], "A", 1, note="(ch. 4)", flags="i")
fight(36.04, "tbv", "boruto", "mitsuki", "A", 3, note="(ch. 7)")
fight(36.105, "tbv", "hidari", ["sarada", "konohamaru"], "A", 2, note="(ch. 10-11)", flags="i")
fight(36.15, "tbv", "matsuri", "gaara", "A", 2, note="(ch. 14-15)")
fight(36.16, "tbv", "ryu", "code", "A", 2, note="(ch. 15)", flags="i")
fight(36.28, "tbv", "sarada", "ryu", "A", 2, ta=["boost"], note="Mangekyō de Sarada (ch. 19-21)")
fight(36.29, "tbv", "matsuri", "konohamaru", "A", 2, note="(ch. 20-21)", flags="i")
fight(36.32, "tbv", "jura", ["boruto", "kawaki"], "A", 2, ta=["retenue"], note="(ch. 23-24)")
fight(36.4, "tbv", ["boruto", "kawaki", "sarada", "daemon", "delta"], "mamushi", "A", 2, note="(ch. 26-33)")
fight(36.45, "tbv", "boruto", "code", "A", 1, tb=["surprise"], note="(ch. 34)")
fight(36.5, "tbv", ["hidari", "code"], "sarada", "A", 1, note="(ch. 37-38, en cours)", flags="i")

# drop placeholder names kept by mistake
for f in F:
    f["b"] = [x for x in f["b"] if not x.endswith("_skip")]
    f["a"] = [x for x in f["a"] if not x.endswith("_skip")]
