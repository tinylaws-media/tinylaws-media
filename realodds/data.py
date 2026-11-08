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
    ("kara", "Boruto : Kara et Isshiki", 33.0),
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
    "minato": ("Minato Namikaze", "Konoha", 4.0, 0.02, 0.02),
    "kushina": ("Kushina Uzumaki", "Konoha", 4.0, 0.02, 0.02),
    "a4": ("A (4e Raikage)", "Kumo", 5.0, None, None),
    "killer_b": ("Killer B", "Kumo", 5.0, None, None),
    "kakashi": ("Kakashi Hatake", "Konoha", 2.0, None, None),
    "obito": ("Obito Uchiha", "Akatsuki", 1.5, 17.06, None),
    "kakkou": ("Kakkō (Iwa)", "Iwa", 3.0, -4, None),
    "kiri_anbu": ("ANBU de Kiri (groupe)", "Kiri", 3.0, -3, None),
    "kurama": ("Kurama (Kyūbi)", "Bijū", 7.0, 33.12, None),
    "nagato": ("Nagato (Pain)", "Akatsuki", 5.0, 16.45, 16.45),
    "konan": ("Konan", "Akatsuki", 4.0, 16.75, None),
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
    "boro": ("Boro", "Kara", 6.0, 32.6, None),
    "kurotsuchi": ("Kurotsuchi (4e Tsuchikage)", "Iwa", 5.0, None, None),
    "jura": ("Jura", "Arbres-Dieux", 7.5, None, None),
    "hidari": ("Hidari", "Arbres-Dieux", 6.5, None, None),
    "matsuri": ("Matsuri", "Arbres-Dieux", 6.0, 36.3, None),
    "kawaki": ("Kawaki", "Konoha", 5.5, None, None),
    "sarada": ("Sarada Uchiha", "Konoha", 4.5, None, None),
    "himawari": ("Himawari Uzumaki", "Konoha", 4.5, None, None),
}
del CHARS["hinata_last"]

GENERIC = {"alliance", "ame_genin", "kiri_anbu"}

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
    ("sasuke", 33.065, -1.0, 0.8, "Perte du Rinnegan"),
    ("kakashi", 15.0, 0.5, 0.6, "Mangekyō Sharingan"),
    ("kakashi", 17.1, -0.5, 0.6, "Perte du Sharingan"),
    ("obito", 16.999, 2.5, 1.0, "Jinchūriki de Jūbi"),
    ("madara", 17.0, 1.0, 1.0, "Retour à la vie, Rinnegan"),
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
fight(1.5, "akatsuki", "hiruzen", "orochimaru", "A", 1, ta=["retenue"], note="Hiruzen laisse fuir Orochimaru", flags="?")
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
fight(12.5, "invasion", "orochimaru", "hiruzen", "A", 1, ta=["prepa"], tb=["age"],
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
fight(12.652, "tsunade", ["tsunade", "jiraiya"], ["orochimaru", "kabuto"], "A", 2, ta=["epuise"], tb=["epuise"],
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
fight(15.842, "hidan", "naruto", "kakuzu", "A", 3, ta=["surprise"], note="Rasenshuriken")
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
fight(16.8, "guerre4a", ["naruto", "kushina"], "kurama", "A", 2, note="Naruto prend le chakra de Kurama, dans sa tête", flags="?")
fight(16.55, "sommet", "killer_b", "kisame", "A", 2, tb=["retenue"], note="Kisame se laisse « décapiter » et se cache dans Samehada")
fight(16.87, "guerre4a", "gai", "kisame", "A", 2, ta=["boost"])
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
fight(17.015, "guerre4b", "madara", "hashirama", "D", tb=["edo"], flags="i")
fight(17.02, "guerre4b", "madara", ["hashirama", "tobirama", "hiruzen", "minato"], "A", 2, tb=["edo"], flags="?")
fight(17.03, "guerre4b", "madara", "gai", "A", 1, tb=["boost"], note="Gai ouvre la 8e porte")
fight(17.035, "guerre4b", "madara", ["naruto", "sasuke"], "A", 2)
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
fight(36.0, "tbv", "boruto", "code", "A", 1, note="Code se retire", flags="?")

# ---------------------------------------------------------------- ajouts
fight(12.0, "vague", "kakashi", ["naruto", "sasuke", "sakura"], "A", 3, ta=["retenue"], note="Test des clochettes")
fight(12.29, "chunin", "orochimaru", "anko", "A", 2, note="Forêt de la Mort")
fight(12.33, "chunin", "baki", "hayate", "A", 2, ta=["surprise"], note="Baki tue Hayate")
fight(15.3, "kazekage", ["hidan", "kakuzu"], "yugito", "A", 2, note="Capture de Nibi")
fight(15.53, "kazekage", ["gai", "rock_lee", "neji", "tenten"], "kisame", "A", 2, tb=["retenue"], note="Copie de Kisame à 30 % du chakra")
fight(15.531, "kazekage", ["naruto", "kakashi", "sakura", "chiyo"], "itachi", "A", 2, tb=["retenue"], note="Copie d'Itachi")
fight(16.12, "itachi", ["naruto", "kakashi", "yamato", "hinata", "kiba", "shino"], "obito", "D", tb=["retenue"], note="Tobi joue avec eux", flags="i")
fight(16.61, "sommet", "gaara", "sasuke", "D", flags="i")
fight(16.905, "guerre4a", ["naruto", "darui"], "raikage3", "A", 2, tb=["edo"], flags="?")
fight(16.921, "guerre4a", "gaara", "rasa", "A", 2, tb=["edo", "retenue"], flags="?")
fight(16.955, "guerre4a", ["naruto", "killer_b"], "itachi", "D", tb=["edo_ctrl"], note="Itachi se libère du contrôle", flags="i")
fight(31.5, "momoshiki", ["sasuke", "naruto"], "shin", "A", 3, note="Naruto Gaiden", flags="?")
fight(32.6, "momoshiki", "boruto", "boro", "A", 2, ta=["boost"], note="Karma, Momoshiki prend le dessus", flags="?")
fight(33.06, "kara", "isshiki", ["naruto", "sasuke", "boruto", "kawaki"], "A", 2, note="Avant le mode Baryon ; Sasuke perd son Rinnegan")

fight(16.63, "sommet", "sasuke", "sakura", "A", 3, tb=["retenue"], note="Sakura n'ose pas frapper ; Kakashi intervient", flags="i")
fight(36.1, "tbv", "jura", "himawari", "A", 3, note="Himawari s'évanouit, Boruto la téléporte")
fight(36.12, "tbv", ["boruto", "sarada", "kawaki"], "hidari", "A", 2, note="Uzuhiko, puis Kawaki l'achève")
fight(36.13, "tbv", "jura", "kawaki", "A", 3, note="Un seul coup")
fight(36.3, "tbv", "boruto", "matsuri", "A", 2, note="Boruto la tranche avec le sabre de Sasuke")
fight(36.31, "tbv", "jura", "boruto", "A", 3, note="Jura annule l'Uzuhiko")

# drop placeholder names kept by mistake
for f in F:
    f["b"] = [x for x in f["b"] if not x.endswith("_skip")]
    f["a"] = [x for x in f["a"] if not x.endswith("_skip")]
