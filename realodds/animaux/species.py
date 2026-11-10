"""Espèces du modèle « animaux » : masse adulte (médiane, intervalle 5-95 % tous sexes confondus, kg),
armes naturelles, comportement social. La masse et les armes servent de point de départ (a priori) ;
les rencontres documentées déplacent ensuite chaque espèce."""

# id: (nom, famille, masse_médiane, masse_p5, masse_p95, armes, social)
# armes : griffes, crocs, morsure (morsure exceptionnelle), cornes, defenses, coups (sabots/pattes), constriction, mains
# social : meute (chasse coordonnée), groupe (se défend ou attaque à plusieurs), solitaire
SPECIES = {
    "lion": ("Lion", "Félins", 170, 110, 230, ["griffes", "crocs"], "meute"),
    "tigre": ("Tigre", "Félins", 170, 100, 260, ["griffes", "crocs"], "solitaire"),
    "jaguar": ("Jaguar", "Félins", 80, 50, 120, ["griffes", "crocs", "morsure"], "solitaire"),
    "leopard": ("Léopard", "Félins", 50, 30, 75, ["griffes", "crocs"], "solitaire"),
    "guepard": ("Guépard", "Félins", 45, 35, 60, ["griffes", "crocs"], "groupe"),
    "puma": ("Puma", "Félins", 55, 35, 80, ["griffes", "crocs"], "solitaire"),
    "ours_brun": ("Ours brun (grizzli)", "Ours", 220, 100, 450, ["griffes", "crocs"], "solitaire"),
    "ours_noir": ("Ours noir", "Ours", 100, 55, 200, ["griffes", "crocs"], "solitaire"),
    "ours_polaire": ("Ours polaire", "Ours", 350, 170, 600, ["griffes", "crocs"], "solitaire"),
    "loup": ("Loup gris", "Canidés", 40, 28, 55, ["crocs"], "meute"),
    "coyote": ("Coyote", "Canidés", 13, 9, 18, ["crocs"], "meute"),
    "lycaon": ("Lycaon", "Canidés", 25, 20, 32, ["crocs"], "meute"),
    "chien": ("Gros chien domestique", "Canidés", 32, 20, 50, ["crocs"], "groupe"),
    "hyene": ("Hyène tachetée", "Hyènes", 60, 45, 80, ["crocs", "morsure"], "meute"),
    "crocodile_nil": ("Crocodile du Nil", "Reptiles", 220, 70, 500, ["crocs", "morsure"], "solitaire"),
    "alligator": ("Alligator d'Amérique", "Reptiles", 180, 70, 360, ["crocs", "morsure"], "solitaire"),
    "caiman": ("Caïman yacare", "Reptiles", 45, 25, 60, ["crocs"], "solitaire"),
    "anaconda": ("Anaconda vert", "Reptiles", 55, 30, 100, ["constriction"], "solitaire"),
    "orque": ("Orque", "Mammifères marins", 4500, 3000, 6500, ["crocs"], "meute"),
    "requin_blanc": ("Grand requin blanc", "Poissons", 800, 400, 1500, ["crocs"], "solitaire"),
    "morse": ("Morse", "Mammifères marins", 1000, 600, 1500, ["defenses"], "groupe"),
    "elephant": ("Éléphant de savane", "Grands herbivores", 4500, 2500, 6500, ["defenses", "coups"], "groupe"),
    "hippopotame": ("Hippopotame", "Grands herbivores", 1500, 1000, 2500, ["crocs", "morsure"], "groupe"),
    "rhinoceros": ("Rhinocéros blanc", "Grands herbivores", 2000, 1500, 2500, ["cornes"], "solitaire"),
    "buffle": ("Buffle d'Afrique", "Grands herbivores", 650, 450, 900, ["cornes", "coups"], "groupe"),
    "bison": ("Bison d'Amérique", "Grands herbivores", 650, 400, 900, ["cornes", "coups"], "groupe"),
    "orignal": ("Orignal (élan)", "Grands herbivores", 450, 300, 650, ["coups"], "solitaire"),
    "gorille": ("Gorille des plaines", "Primates", 140, 75, 200, ["crocs", "mains"], "groupe"),
    "chimpanze": ("Chimpanzé", "Primates", 50, 35, 65, ["crocs", "mains"], "groupe"),
    "babouin": ("Babouin chacma", "Primates", 25, 15, 35, ["crocs", "mains"], "groupe"),
    "humain": ("Humain adulte (à mains nues)", "Primates", 78, 60, 105, ["mains"], "groupe"),
    "ratel": ("Ratel (blaireau du miel)", "Mustélidés", 10, 7, 14, ["griffes", "crocs"], "solitaire"),
    "kangourou": ("Kangourou roux", "Marsupiaux", 55, 25, 85, ["coups", "griffes"], "groupe"),
}
