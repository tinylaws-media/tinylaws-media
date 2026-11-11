"""Corrections de lecture appliquées aux rencontres (biais de sélection connus).
Chaque règle : (description, test sur la ligne, action). Actions : poids ×k, retrait d'un tag mal posé.
Le codage fin (nul quand l'attaquant lâche prise, contact réel ou non, âges) est fait ligne par ligne dans les fichiers de données,
vérifiés à la source ; ces règles ne traitent que les biais de sélection qu'aucun codage ne peut corriger."""

PRED = {"lion", "tigre", "jaguar", "leopard", "guepard", "puma", "ours_brun", "ours_polaire", "loup", "coyote", "lycaon", "hyene",
        "crocodile_nil", "alligator", "caiman", "anaconda", "orque", "requin_blanc"}
HERB = {"elephant", "hippopotame", "rhinoceros", "buffle", "bison", "orignal", "kangourou", "morse", "babouin", "gorille", "chimpanze", "humain"}


def has(r, a, b):
    return {r["a"], r["b"]} == {a, b}


RULES = [
    ("Registres qui ne recensent que les morts (morsures de chien mortelles, ours noirs, requins, lions tués à la lance) : sans dénominateur, ils surestiment le vainqueur",
     lambda r: r["res"] == "A" and r["m"] == 3 and r["count"] >= 8 and "registre" in r["note"].lower(), ("poids", 0.3)),
    ("Registres de chiens tués par des loups : les victoires des chiens ne sont jamais recensées",
     lambda r: has(r, "loup", "chien") and r["a"] == "loup" and r["count"] >= 8, ("poids", 0.3)),
    ("Meurtres entre chimpanzés : ils n'attaquent que lorsqu'ils sont très nombreux (sélection des occasions)",
     lambda r: r["a"] == r["b"] == "chimpanze", ("poids", 0.3)),
    ("Chiens qui interrompent une attaque d'ours sur une personne : diversion plus que victoire",
     lambda r: has(r, "chien", "ours_brun") and r["count"] >= 15, ("poids", 0.3)),
    ("Prédation : le prédateur choisit sa proie (isolée, affaiblie) ; victoire moins informative sur un duel neutre",
     lambda r: r["res"] == "A" and r["a"] in PRED and r["b"] in HERB, ("poids", 0.5)),
    ("Foules qui tuent un animal (représailles en Inde, villageois) : animal acculé, souvent épuisé ou déjà blessé",
     lambda r: r["a"] == "humain" and r["na"] >= 5 and r["res"] == "A", ("poids", 0.5)),
    ("Éléphants tueurs de rhinocéros : jeunes mâles adultes en musth, pas des juvéniles",
     lambda r: r["a"] == "elephant" and r["b"] == "rhinoceros" and "jeune" in r["ta"], ("retirer_tag_a", "jeune")),
]


def apply(rows):
    out, log = [], {d: 0 for d, _, _ in RULES}
    for r in rows:
        r = dict(r, ta=list(r["ta"]), tb=list(r["tb"]), poids=1.0)
        for d, test, act in RULES:
            if not test(r):
                continue
            log[d] += 1
            if act[0] == "poids":
                r["poids"] *= act[1]
            elif act[0] == "retirer_tag_a":
                r["ta"] = [t for t in r["ta"] if t != act[1]]
        out.append(r)
    return out, log
