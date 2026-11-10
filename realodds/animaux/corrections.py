"""Corrections de lecture appliquées aux rencontres brutes (biais de sélection, codage).
Chaque règle : (description, test sur la ligne, action). Actions : poids ×k, recodage, suppression."""

PRED = {"lion", "tigre", "jaguar", "leopard", "guepard", "puma", "ours_brun", "ours_polaire", "loup", "coyote", "lycaon", "hyene",
        "crocodile_nil", "alligator", "caiman", "anaconda", "orque", "requin_blanc"}
HERB = {"elephant", "hippopotame", "rhinoceros", "buffle", "bison", "orignal", "kangourou", "morse", "babouin", "gorille", "chimpanze", "humain"}


def has(r, a, b):
    return {r["a"], r["b"]} == {a, b}

RULES = [
    ("Décès par morsure de chien aux USA (NCRC) : 87 % sans adulte valide présent, aucun dénominateur → quasi ignorés",
     lambda r: r["a"] == "chien" and r["b"] == "humain" and "NCRC" in r["note"], ("poids", 0.33)),
    # registres qui ne comptent que les morts (pas de dénominateur) : ils surestiment le gagnant
    ("Registres de décès humains (chiens, ours noirs, requins, enfants) : biais de sélection",
     lambda r: r["b"] == "humain" and r["res"] == "A" and r["m"] == 3 and r["count"] >= 8, ("poids", 0.3)),
    ("Registres de chiens tués par des loups : les victoires des chiens ne sont jamais recensées",
     lambda r: has(r, "loup", "chien") and r["a"] == "loup" and r["count"] >= 8, ("poids", 0.3)),
    ("Meurtres entre chimpanzés : ils n'attaquent que quand ils sont très nombreux (sélection des occasions)",
     lambda r: r["a"] == r["b"] == "chimpanze", ("poids", 0.3)),
    ("Morsures de requin non mortelles : le requin lâche par erreur de proie, ce n'est pas un combat",
     lambda r: has(r, "requin_blanc", "humain") and r["res"] == "D" and r["count"] > 10, ("supprimer",)),
    ("Déplacements sans contact (coyotes, léopards, guépards chassés de leurs proies)",
     lambda r: "carcasse" in r["ta"] + r["tb"] and r["count"] >= 30, ("poids", 0.3)),
    ("Orignaux aux abois : la meute renonce sans vrai combat → nul",
     lambda r: r["a"] == "orignal" and r["b"] == "loup" and r["count"] >= 30, ("nul",)),
    ("Survivants d'attaques de puma : sauvés souvent par des compagnons ou une arme, pas par le combat seul",
     lambda r: has(r, "humain", "puma") and r["a"] == "humain" and r["count"] >= 30, ("poids", 0.3)),
    ("Chiens qui font cesser une attaque d'ours : diversion plus que victoire",
     lambda r: has(r, "chien", "ours_brun") and r["count"] >= 15, ("poids", 0.3)),
    ("Humain qui repousse une attaque (victoire « à l'arraché ») : l'animal renonce, ce n'est pas un combat gagné → nul",
     lambda r: r["a"] == "humain" and r["res"] == "A" and r["m"] == 1, ("nul",)),
    ("Prédation : le prédateur choisit sa proie (isolée, affaiblie) — victoire moins informative sur un duel neutre",
     lambda r: r["res"] == "A" and r["a"] in PRED and r["b"] in HERB, ("poids", 0.5)),
    ("Éléphants tueurs de rhinocéros : jeunes mâles adultes en musth, pas des juvéniles",
     lambda r: r["a"] == "elephant" and r["b"] == "rhinoceros" and "jeune" in r["ta"], ("retirer_tag_a", "jeune")),
]


def apply(rows):
    out, log = [], {d: 0 for d, _, _ in RULES}
    for r in rows:
        r = dict(r, ta=list(r["ta"]), tb=list(r["tb"]), poids=1.0); drop = False
        for d, test, act in RULES:
            if not test(r):
                continue
            log[d] += 1
            if act[0] == "poids":
                r["poids"] *= act[1]
            elif act[0] == "supprimer":
                drop = True
            elif act[0] == "nul":
                r["res"] = "D"; r["m"] = 1
            elif act[0] == "retirer_tag_a":
                r["ta"] = [t for t in r["ta"] if t != act[1]]
        if not drop:
            out.append(r)
    return out, log
