# Bleach, partie 2 : la Guerre de Mille Ans (ch. 480-686). Manga de Kubo uniquement : pas d'ajouts de l'anime
# Thousand-Year Blood War, pas de romans (Can't Fear Your Own World...). "fight" est injecté par data.py.
# Repères (t = années depuis le ch. 1) : première invasion 2.000-2.011, Division zéro / entraînement 2.10-2.16,
# seconde invasion 2.20-2.24, palais du Roi des âmes 2.24-2.26, bataille finale 2.27-2.33.
# Un Bankai volé par un médaillon et retourné contre son propriétaire est un pouvoir externe : étiquette « aide ».
# Vollständig, The Almighty, l'Auswählen et l'absorption du Roi des âmes sont des sauts datés.

CHARS_PART = {
    # ---------------------------------------------------------------- Wandenreich
    "yhwach": ("Yhwach (roi des Quincy)", "Wandenreich", 7.0, 2.33, None),
    "haschwalth": ("Jugram Haschwalth (« B », grand maître)", "Wandenreich", 5.4, 2.32, None),
    "gerard": ("Gerard Valkyrie (« M », Schutzstaffel)", "Wandenreich", 5.6, 2.318, None),
    "lille": ("Lille Barro (« X », Schutzstaffel)", "Wandenreich", 5.5, 2.318, None),
    "pernida": ("Pernida Parnkgjas (« C », Schutzstaffel)", "Wandenreich", 5.4, 2.2905, None),
    "askin": ("Askin Nakk Le Vaar (« D », Schutzstaffel)", "Wandenreich", 5.1, 2.3065, None),
    "bazzb": ("Bazz-B (« H »)", "Wandenreich", 4.8, 2.2745, None),
    "as_nodt": ("Äs Nödt (« F »)", "Wandenreich", 4.4, 2.2105, None),
    "bambietta": ("Bambietta Basterbine (« E »)", "Wandenreich", 4.4, 2.2045, None),
    "cang_du": ("Cang Du (« I »)", "Wandenreich", 4.3, 2.2065, None),
    "bg9": ("BG9 (« K »)", "Wandenreich", 4.3, 2.2065, None),
    "mask": ("Mask De Masculine (« S »)", "Wandenreich", 4.6, None, None),
    "gremmy": ("Gremmy Thoumeaux (« V »)", "Wandenreich", 5.2, 2.2145, None),
    "quilge": ("Quilge Opie (« J »)", "Wandenreich", 4.4, 2.0082, None),
    "driscoll": ("Driscoll Berci (« O »)", "Wandenreich", 4.1, 2.0051, None),
    "royd": ("Royd Lloyd (« Y », sosie de Yhwach)", "Wandenreich", 4.0, 2.0091, None),
    "candice": ("Candice Catnipp (« T »)", "Wandenreich", 4.2, None, None),
    "liltotto": ("Liltotto Lamperd (« G »)", "Wandenreich", 4.2, None, None),
    "meninas": ("Meninas McAllon (« P »)", "Wandenreich", 4.1, None, None),
    "giselle": ("Giselle Gewelle (« Z »)", "Wandenreich", 4.2, None, None),
    "nanana": ("NaNaNa Najahkoop (« U »)", "Wandenreich", 4.1, 2.2705, None),
    "nianzol": ("Nianzol Weizol (« W »)", "Wandenreich", 4.0, 2.2405, None),
    "pepe": ("Pepe Waccabrada (« L »)", "Wandenreich", 4.0, 2.2305, None),
    "sternritter": ("Sternritter de second rang (groupe)", "Wandenreich", 3.8, None, None),
    "ebern": ("Ebern Asguiaro (arrancar du Wandenreich)", "Wandenreich", 2.5, 2.0011, None),
    # ---------------------------------------------------------------- Division zéro
    "ichibe": ("Ichibē Hyōsube (Division zéro)", "Division zéro", 6.7, None, None),
    "oetsu": ("Ōetsu Nimaiya (Division zéro)", "Division zéro", 5.8, None, None),
    "kirinji": ("Tenjirō Kirinji (Division zéro)", "Division zéro", 5.6, None, None),
    "hikifune": ("Kirio Hikifune (Division zéro)", "Division zéro", 5.5, None, None),
    "tenjiro": ("Senjumaru Shutara (Division zéro)", "Division zéro", 5.5, None, None),
    "yushiro": ("Yūshirō Shihōin", "Gotei 13", 4.0, None, None),
    "monstres_noirs": ("Monstres noirs de Yhwach (groupe)", "Wandenreich", 3.5, None, None),
}

GENERIC_PART = {"sternritter", "monstres_noirs"}

JUMPS_PART = [
    # Yhwach
    ("yhwach", -999.0, -3.0, 0.8, "Scellé après sa défaite : il ne retrouve son cœur qu'au bout de 900 ans, son intelligence 90 ans plus tard (ch. 537)"),
    ("yhwach", -9.0, 3.0, 0.8, "Retrouve sa puissance neuf ans avant l'invasion, Auswählen (ch. 536-537)"),
    ("yhwach", 2.245, 0.4, 0.4, "Auswählen au palais : prend la force des Sternritter tombés (ch. 543, ch. 603)"),
    ("yhwach", 2.26, 1.5, 0.6, "Absorbe le Roi des âmes et Mimihagi (ch. 614-617)"),
    ("yhwach", 2.321, 0.3, 0.3, "Auswählen sur Haschwalth et les Schutzstaffel (ch. 676-678)"),
    # Ichigo
    ("ichigo", 2.012, -1.2, 0.5, "Bankai brisé par Yhwach (ch. 513-514)"),
    ("ichigo", 2.15, 2.6, 0.7, "Vrai Zanpakutō forgé par Nimaiya, vrai Shikai double (ch. 538-542)"),
    # Shinigami
    ("kenpachi", 2.1702, 1.6, 0.5, "Entend la voix de Nozarashi et cesse de brider sa force (ch. 527-528)"),
    ("kenpachi", 2.2105, 0.3, 0.3, "Shikai Nozarashi libéré contre Gremmy (ch. 576-577)"),
    ("kenpachi", 2.3, 0.6, 0.4, "Bankai débloqué contre Gerard (ch. 668-670)"),
    ("renji", 2.15, 0.9, 0.5, "Vrai Bankai Sōō Zabimaru, entraîné par Ichibē (ch. 522-523, ch. 562-564)"),
    ("rukia", 2.15, 1.6, 0.6, "Bankai Hakka no Togame, entraînée par Byakuya (ch. 566-569)"),
    ("byakuya", 2.15, 0.2, 0.3, "Guéri et réentraîné au palais (ch. 541-546)"),
    ("komamura", 2.2042, 1.0, 0.5, "Technique d'humanisation : Bankai renforcé, au prix de sa forme humaine (ch. 556-558)"),
    ("komamura", 2.206, -3.0, 0.8, "Redevenu loup (ch. 559)"),
    ("hitsugaya", 2.3005, 0.8, 0.4, "Guéri de la zombification, Bankai complet en forme adulte (ch. 668-669)"),
    ("uryu", 2.15, 1.5, 0.6, "Sternritter « A », The Antithesis (ch. 540-547, ch. 662)"),
    ("grimmjow", 2.27, 0.3, 0.4, "Rétabli, rejoint Ichigo (ch. 625)"),
    ("ichigo", 2.326, 1.2, 0.5, "Zangetsu brisé se reforme sous une forme nouvelle, il tranche Yhwach en deux (ch. 679-682)"),
    ("aizen", 2.25, 0.8, 0.5, "Libéré de Muken par Kyōraku, sceaux partiellement levés (ch. 619-621)"),
]

# ============================================================== Première invasion
fight(2.0, "invasion1", "ichigo", "ebern", "A", 2, note="Ebern tente de voler le Bankai d'Ichigo et s'enfuit (ch. 480-482)", flags="i")
fight(2.002, "invasion1", "driscoll", "sasakibe", "A", 3, note="Driscoll tue Sasakibe et vole son Bankai (ch. 483-486)")
fight(2.004, "invasion1", "quilge", "tres_bestias", "A", 3, note="Quilge abat les trois Fracciones de Harribel (ch. 486-488)")
fight(2.005, "invasion1", "yamamoto", "driscoll", "A", 3, note="Yamamoto incinère Driscoll, qui utilisait le Bankai de Sasakibe (ch. 505)")
fight(2.006, "invasion1", "ichigo", "quilge", "A", 1, note="Ichigo prend d'abord l'avantage sur Quilge (ch. 489-491)")
fight(2.0062, "invasion1", "quilge", "ichigo", "A", 2, note="Vollständig de Quilge, Ichigo emprisonné dans son Jail (ch. 491-500)", flags="i")
fight(2.0064, "invasion1", "as_nodt", "byakuya", "A", 3, ta=["aide"], note="Bankai de Byakuya volé, Äs Nödt le laisse pour mort (ch. 494-502)")
fight(2.0064, "invasion1", "cang_du", "hitsugaya", "A", 2, ta=["aide"], note="Bankai de Hitsugaya volé (ch. 494-499)")
fight(2.0064, "invasion1", "bg9", "soifon", "A", 2, ta=["aide"], note="Bankai de Suì-Fēng volé (ch. 494-499)")
fight(2.0064, "invasion1", "bambietta", "komamura", "A", 2, ta=["aide"], note="Bankai de Komamura volé (ch. 494-499)")
fight(2.0066, "invasion1", "kenpachi", "sternritter", "A", 3, note="Kenpachi massacre trois Sternritter (ch. 500-504)")
fight(2.007, "invasion1", "yamamoto", "royd", "A", 3,
      note="Bankai Zanka no Tachi : Yamamoto anéantit celui qu'il croit être Yhwach, en fait son sosie Royd Lloyd (ch. 506-510)")
fight(2.009, "invasion1", "yhwach", "yamamoto", "A", 3, ta=["aide"], tb=["epuise"],
      note="Le vrai Yhwach vole le Bankai de Yamamoto et le coupe en deux (ch. 510-511)")
fight(2.0095, "invasion1", "yhwach", "kenpachi", "A", 2, note="Kenpachi charge Yhwach et est abattu (ch. 511-512)", flags="?")
fight(2.0105, "invasion1", "yhwach", "ichigo", "A", 3, note="Yhwach brise le Bankai d'Ichigo d'un coup (ch. 512-514)")

# ============================================================== Division zéro : entraînement
fight(2.165, "zeroeme", "unohana", "kenpachi", "A", 2,
      note="Dans Muken, Unohana tue et ressuscite Kenpachi encore et encore (ch. 524-527)", flags="i")
fight(2.1704, "zeroeme", "kenpachi", "unohana", "A", 1,
      note="Kenpachi entend Nozarashi, cesse de se retenir et tue Unohana (ch. 527-528)")

# ============================================================== Seconde invasion
fight(2.2, "seireitei", "haschwalth", ["kyoraku", "nanao"], "D", note="Le bouclier de Nanao retient Haschwalth (ch. 544-551)", flags="i")
fight(2.2005, "seireitei", "mayuri", "askin", "D", note="Mayuri et Askin, duel de poisons, la retraite l'interrompt (ch. 545-552)", flags="i?")
fight(2.201, "seireitei", "bazzb", ["hitsugaya", "rangiku"], "D", note="Bazz-B contre Hitsugaya et Rangiku (ch. 546-550)", flags="i")
fight(2.202, "seireitei", "hitsugaya", "cang_du", "A", 2, note="Bankai récupéré grâce au Shin'eiyaku, Hitsugaya vainc Cang Du (ch. 551-554)")
fight(2.2021, "seireitei", ["soifon", "omaeda"], "bg9", "D", note="Suì-Fēng et Ōmaeda contre BG9 (ch. 549-555)", flags="i?")
fight(2.2045, "seireitei", "komamura", "bambietta", "A", 3, note="Komamura humanisé, Bankai Kokujō Tengen Myō'ō : Bambietta vaincue (ch. 556-559)")
fight(2.205, "seireitei", "mask", ["kensei", "rose"], "A", 2, note="Mask domine Kensei et Rose (ch. 560-562)")
fight(2.206, "seireitei", "renji", "mask", "A", 2, note="Sōō Zabimaru, Renji vainc Mask (ch. 562-565)")
fight(2.21, "seireitei", "rukia", "as_nodt", "A", 1, note="Hakka no Togame : Rukia gèle Äs Nödt, avec l'aide de Byakuya à la fin (ch. 566-570)")
fight(2.2101, "seireitei", "gremmy", ["kensei", "rose"], "A", 3, ta=["surprise"], note="Gremmy tue Kensei et Rose par une diversion (ch. 571-572)")
fight(2.2102, "seireitei", "gremmy", "yachiru", "A", 2, note="Gremmy domine Yachiru (ch. 573-574)")
fight(2.2144, "seireitei", "kenpachi", "gremmy", "A", 2,
      note="Kenpachi tranche la météorite avec son Shikai ; Gremmy se détruit à vouloir l'égaler (ch. 574-580)")
fight(2.215, "seireitei", ["candice", "liltotto", "meninas", "giselle"], "kenpachi", "A", 2, tb=["epuise"],
      note="Les quatre Sternritter tombent sur Kenpachi épuisé (ch. 580-581)")
fight(2.2155, "seireitei", "ichigo", ["candice", "liltotto", "meninas", "giselle"], "A", 2,
      note="Ichigo et son vrai Zanpakutō sauvent Kenpachi (ch. 581-583)", flags="i")
fight(2.216, "seireitei", ["bazzb", "candice", "liltotto", "meninas"], "ichigo", "D", note="Ichigo face à Bazz-B et trois autres, ses amis prennent le relais (ch. 583-587)", flags="i")
fight(2.22, "seireitei", "giselle", ["ikkaku", "yumichika"], "A", 2, ta=["aide"],
      note="Bambietta et Hitsugaya zombifiés défont Ikkaku et Yumichika (ch. 588-594)")
fight(2.225, "seireitei", "pepe", "byakuya", "A", 2, tb=["epuise"], note="Love-love de Pepe sur Byakuya encore blessé, Mayuri le sauve (ch. 594-597)")
fight(2.23, "seireitei", "kensei", "pepe", "A", 2, note="Kensei, zombie libéré par Mayuri, vainc Pepe (ch. 597-598)")

# ============================================================== Palais du Roi des âmes
fight(2.24, "palais", "kirinji", "nianzol", "A", 3, note="Nianzol meurt en s'en prenant à Kirinji (ch. 596-597)", flags="?")
fight(2.241, "palais", "oetsu", ["gerard", "lille", "pernida"], "A", 3, note="Ōetsu tue les gardes du corps de Yhwach (ch. 599-601)", flags="?")
fight(2.242, "palais", "oetsu", "askin", "A", 2, note="Ōetsu annule le poison d'Askin et le tue (ch. 601-602)")
fight(2.246, "palais", ["gerard", "lille", "pernida", "askin"], ["oetsu", "kirinji", "hikifune", "tenjiro"], "A", 2,
      note="Ressuscités par l'Auswählen, les Schutzstaffel terrassent la Division zéro (ch. 603-606)", flags="?")
fight(2.25, "palais", "ichibe", "yhwach", "A", 2, note="Shinuchi Shirafude Ichimonji : Ichibē efface le nom et la force de Yhwach (ch. 606-609)", flags="i")
fight(2.251, "palais", "yhwach", "ichibe", "A", 3, note="The Almighty : Yhwach tue Ichibē (ch. 609-611)")

# ============================================================== Bataille finale
fight(2.27, "final", "aizen", "monstres_noirs", "A", 3, note="Aizen, enchaîné, détruit les monstres noirs (ch. 621-622)")
fight(2.2705, "final", "bazzb", "nanana", "A", 3, ta=["surprise"], note="Bazz-B tue NaNaNa qui s'en prenait à Aizen (ch. 623)")
fight(2.272, "final", "askin", "grimmjow", "A", 2, note="Askin et son Gift Ball laissent Grimmjow pour mort (ch. 628-632)")
fight(2.274, "final", "haschwalth", "bazzb", "A", 3, note="The Balance : Haschwalth tue Bazz-B (ch. 630-634)")
fight(2.276, "final", "yhwach", ["giselle", "liltotto"], "A", 3, note="Yhwach abat Giselle et Liltotto (ch. 635-636)", flags="?")
fight(2.28, "final", "pernida", "kenpachi", "A", 2, note="Pernida, bras gauche du Roi des âmes, mutile Kenpachi (ch. 636-639)")
fight(2.289, "final", "pernida", "nemu", "A", 3, note="Nemu s'interpose contre Pernida et en meurt (ch. 642-644)")
fight(2.29, "final", "mayuri", "pernida", "A", 1, ta=["prepa"],
      note="Mayuri sauve Kenpachi ; le corps empoisonné de Nemu fait exploser Pernida (ch. 640-645)")
fight(2.292, "final", "lille", "kyoraku", "A", 2, note="Vollständig de Lille, Kyōraku dominé (ch. 646-649)")
fight(2.293, "final", "kyoraku", "lille", "A", 1, note="Bankai Katen Kyōkotsu Karamatsu Shinjū semble abattre Lille (ch. 649-651)", flags="i")
fight(2.294, "final", "lille", "kyoraku", "A", 2, note="Lille se transforme encore et manque de tuer Kyōraku (ch. 651-652)", flags="i")
fight(2.295, "final", ["nanao", "kyoraku"], "lille", "A", 1, note="Shinken Hakkyōken de Nanao renvoie le coup de Lille, Kira l'attaque (ch. 653-654)", flags="e")
fight(2.296, "final", "gerard", ["byakuya", "rukia", "renji", "hisagi"], "A", 3, note="The Miracle, Gerard géant écrase les shinigami (ch. 655-658)", flags="?")
fight(2.297, "final", ["shinji", "love", "rose", "lisa", "hiyori", "hitsugaya"], "gerard", "D",
      note="Les Visored et Hitsugaya gèlent en partie le géant (ch. 659-661)", flags="i")
fight(2.298, "final", "askin", ["ichigo", "orihime", "chad"], "A", 2, ta=["prepa"], note="Gift Ball d'Askin, Ichigo et ses amis empoisonnés (ch. 656-659)")
fight(2.299, "final", "askin", ["yoruichi", "yushiro"], "A", 1, note="Shunkō Raijin de Yoruichi, Yūshirō la rejoint, ils perdent pied (ch. 659-663)", flags="i")
fight(2.3, "final", "gerard", "kenpachi", "A", 1, note="Gerard renvoie les coups de Kenpachi, dont le Bankai s'éveille (ch. 666-669)", flags="i")
fight(2.306, "final", ["urahara", "grimmjow"], "askin", "A", 1,
      note="Bankai d'Urahara Kannonbiraki Benihime Aratame et Grimmjow blessent mortellement Askin ; Nel protège les autres (ch. 663-668)", flags="e")
fight(2.307, "final", ["hitsugaya", "kenpachi", "byakuya"], "gerard", "A", 1,
      note="Bankai complet de Hitsugaya, Byakuya et Kenpachi semblent tuer Gerard, qui se régénère (ch. 668-671)", flags="i")
fight(2.31, "final", "haschwalth", "uryu", "A", 2, note="The Balance l'emporte sur The Antithesis (ch. 662-675)")
fight(2.312, "final", "yhwach", "ichigo", "A", 3, note="Yhwach brise le sabre d'Ichigo et lui prend ses pouvoirs (ch. 671-677)")
fight(2.325, "final", "aizen", "yhwach", "D",
      note="Kyōka Suigetsu trompe Yhwach assez longtemps pour qu'Ichigo et Renji frappent ; The Almighty reprend le dessus (ch. 678-682)", flags="i")
fight(2.329, "final", "ichigo", "yhwach", "A", 1, ta=["prepa", "aide"],
      note="Ichigo tranche Yhwach en deux, la pointe d'argent immobile de Ryūken tirée par Uryū suspend The Almighty, Ichigo porte le coup final ; crédit à Ichigo, les aides d'Uryū et d'Aizen en étiquettes (ch. 682-685)")
