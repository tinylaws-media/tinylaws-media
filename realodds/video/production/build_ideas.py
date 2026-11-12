"""Ajoute au classeur plan_200_videos.xlsx : vidéos longues, idées d'analyses, et les résultats calculés (analyses.json)."""
import json, os
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, "analyses.json")))
LABEL = {"naruto": "Naruto", "onepiece": "One Piece", "dragonball": "Dragon Ball", "jujutsukaisen": "Jujutsu Kaisen", "bleach": "Bleach",
         "hunterxhunter": "Hunter x Hunter", "demonslayer": "Demon Slayer", "mha": "My Hero Academia", "aot": "L'Attaque des Titans", "chainsawman": "Chainsaw Man"}

LONGUES = [
 ("Le classement définitif de Naruto : tous les persos, arc par arc", "20-30 min", "Classement par arc + toile de tous les combats + 10 duels les plus disputés", "Prêt"),
 ("Le classement définitif de One Piece, de God Valley à Elbaf", "25-35 min", "Idem One Piece, avec les Empereurs à chaque époque", "Prêt"),
 ("Le tournoi ultime : 64 persos de 4 œuvres, simulé 10 000 fois", "30 min", "Tableau à élimination, chaque duel simulé par le modèle inter-œuvres ; hax commentés à part", "Prêt (4 œuvres)"),
 ("Quel mangaka est le plus cohérent ? Les 10 œuvres passées au modèle", "20 min", "Taux de combats « impossibles », exploits hors norme, persos instables", "Prêt"),
 ("Les persos mentent-ils ? Toutes les déclarations « X est plus fort que Y » vérifiées", "20-25 min", "Chaque déclaration confrontée aux combats seuls (modèle sans déclarations)", "Prêt"),
 ("Le plot armor en chiffres : qui gagne alors qu'il devrait perdre ?", "15-20 min", "Indice de plot armor par perso et par œuvre", "Prêt"),
 ("Combien d'humains pour battre… : de l'ours à Kaido", "20 min", "Modèle animaux + échelle commune « × humain »", "Prêt"),
 ("Comment j'ai construit le modèle (making-of nerd)", "25 min", "Bayésien, combats datés, incertitudes ; pour la communauté qui veut comprendre", "Prêt"),
 ("Dans One Piece, le nombre ne sert à rien (et c'est voulu)", "15 min", "Le poids des alliés par œuvre : One Piece et Dragon Ball où le plus fort porte tout, Demon Slayer où l'équipe compte", "Prêt"),
 ("L'évolution de Luffy (ou Naruto, Goku) en une courbe", "15 min", "Évolution de la force arc par arc, avec chaque power-up daté", "Prêt"),
 ("Les Hokage classés, du premier au septième", "15-20 min", "Chaque Hokage à son apogée + duels croisés", "Prêt"),
 ("Les Yonko classés à chaque époque", "15-20 min", "Empereurs de l'ère Rocks à Elbaf", "Prêt"),
 ("Les 50 combats les plus injustes de l'anime", "30 min", "Top surprises de toutes les œuvres, avec contexte", "Prêt"),
 ("Les éléments de Naruto : le feu bat-il vraiment le vent ?", "15 min", "Il faut d'abord ajouter l'élément de chaque technique dans les combats", "Données à ajouter"),
 ("Les primes de One Piece sont-elles justes ?", "15 min", "Prime officielle comparée à la force estimée par les combats", "Prêt"),
 ("Les niveaux de puissance de Dragon Ball veulent-ils dire quelque chose ?", "15 min", "Niveaux officiels contre combats", "Prêt"),
]

IDEES = [
 # (thème, idée, ce que le modèle calcule, statut)
 ("Mensonges", "Itachi mentait-il sur Jiraiya ?", "Probabilité que « à deux on y resterait » soit vraie selon les combats seuls", "Prêt"),
 ("Mensonges", "Tobirama a-t-il raison de dire que Minato le dépasse ?", "Déclaration confrontée aux combats", "Prêt"),
 ("Mensonges", "Gaban, vraiment n°2 de l'équipage de Roger ?", "Déclaration intéressée confrontée aux combats", "Prêt"),
 ("Mensonges", "Le Raikage est-il vraiment le plus rapide après Minato ?", "Déclaration confrontée aux combats", "Prêt"),
 ("Mensonges", "Toutes les déclarations d'une œuvre : le top des mensonges et des vérités", "Tableau « Les persos disent-ils vrai ? »", "Prêt"),
 ("Mensonges", "Les databooks de Kishimoto mentent-ils ?", "Notes officielles contre forces estimées par les combats", "Prêt"),
 ("Mensonges", "Les primes mentent-elles ? Les plus sur-cotés et sous-cotés de One Piece", "Prime contre force", "Prêt"),
 ("Mensonges", "Les niveaux de puissance de Dragon Ball : utiles ou décoratifs ?", "Niveaux officiels contre combats", "Prêt"),
 ("Mensonges", "Barbe Blanche était-il vraiment « l'homme le plus fort du monde » ?", "Statut contre combats à chaque époque", "Prêt"),
 ("Mensonges", "Gojo, vraiment « le plus fort » ? Ce que disent ses combats", "Statut contre combats", "Prêt"),
 ("Incohérences", "Les 10 pires incohérences de Naruto", "Les victoires les moins plausibles selon le modèle", "Prêt"),
 ("Incohérences", "Les 10 pires incohérences de One Piece", "Idem", "Prêt"),
 ("Incohérences", "Les 10 pires incohérences de Dragon Ball", "Idem, plus les Lunes détruites trop tôt (exploits hors norme)", "Prêt"),
 ("Incohérences", "Le perso le plus instable de chaque œuvre", "Persos dont les combats se contredisent le plus (fourchette élargie)", "Prêt"),
 ("Incohérences", "Quel mangaka respecte le plus ses propres règles ?", "Surprise moyenne par combat, œuvre par œuvre", "Prêt"),
 ("Incohérences", "Roshi qui détruit la Lune : l'exploit le plus absurde de l'anime ?", "Écart de l'exploit à la tendance de l'œuvre", "Prêt"),
 ("Incohérences", "Le power-down le plus violent de l'histoire", "Persos qui perdent le plus de force d'un arc à l'autre", "Prêt"),
 ("Plot armor", "Le plot armor en chiffres : top 10 toutes œuvres", "Somme des victoires improbables", "Prêt"),
 ("Plot armor", "Luffy a-t-il plus de plot armor que Naruto ?", "Indice comparé", "Prêt"),
 ("Plot armor", "Les persos qui perdent alors qu'ils devraient gagner (anti plot armor)", "Défaites improbables", "Prêt"),
 ("Plot armor", "Le héros qui gagne toujours au dernier moment : est-ce statistique ?", "Marge des victoires du héros contre celles des autres", "Prêt"),
 ("Règles de l'œuvre", "Les éléments de Naruto : la règle feu > vent > foudre… se voit-elle dans les combats ?", "Effet de l'avantage élémentaire estimé (il faut coder l'élément de chaque combat)", "Données à ajouter"),
 ("Règles de l'œuvre", "Le Haki bat-il vraiment les fruits du démon ?", "Effet estimé du Haki dans les combats contre des logias", "Données à ajouter"),
 ("Règles de l'œuvre", "Le Sharingan est-il surcoté ? Uchiha contre non-Uchiha à force égale", "Effet estimé du clan", "Données à ajouter"),
 ("Règles de l'œuvre", "Les logias sont-ils les fruits les plus forts ?", "Force moyenne par type de fruit", "Données à ajouter"),
 ("Règles de l'œuvre", "Le Bankai, vraiment 5 à 10 fois plus fort que le Shikai ?", "Saut de force estimé au Bankai", "Prêt"),
 ("Règles de l'œuvre", "Les 8 portes valent-elles vraiment la mort ?", "Effet estimé des portes", "Prêt"),
 ("Règles de l'œuvre", "Le mode Ermite : combien d'échelons gagnés ?", "Saut daté estimé", "Prêt"),
 ("Règles de l'œuvre", "Le Gear 5 est-il le plus gros power-up de One Piece ?", "Sauts datés comparés", "Prêt"),
 ("Règles de l'œuvre", "Le domaine bat-il toujours la technique ? (Jujutsu Kaisen)", "Combats avec domaine contre sans", "Données à ajouter"),
 ("Nombre", "Dans One Piece, le nombre ne sert à rien", "Poids des alliés par œuvre", "Prêt"),
 ("Nombre", "Combien de Supernovas pour battre un Empereur ?", "« Combien il en faut ? »", "Prêt"),
 ("Nombre", "Combien de genin pour battre un Kage ?", "Idem", "Prêt"),
 ("Nombre", "L'Alliance ninja servait-elle à quelque chose ?", "Poids des alliés et force des armées", "Prêt"),
 ("Nombre", "Combien d'humains normaux pour battre Luffy ? Gojo ? Goku ?", "Échelle commune « × humain »", "Prêt"),
 ("Réel", "Le gorille et les 100 hommes : la version sérieuse", "Modèle animaux", "Prêt"),
 ("Réel", "Quel perso de manga battrait un ours ? Un éléphant ?", "Échelle commune + modèle animaux", "Prêt"),
 ("Réel", "Yuji Itadori : à quel point il dépasse les records du monde ?", "Exploits chiffrés (lancer de poids, 50 m)", "Prêt"),
 ("Réel", "Tous les persos de Naruto en bombes d'Hiroshima", "Échelle commune, unité « bombe d'Hiroshima »", "Prêt"),
 ("Réel", "La Lune détruite combien de fois ? Les exploits planétaires classés", "Exploits chiffrés", "Prêt"),
 ("Évolution", "La courbe de Luffy du ch. 1 au ch. 1198", "Évolution par arc", "Prêt"),
 ("Évolution", "Naruto a-t-il régressé dans Boruto ?", "Force par arc", "Prêt"),
 ("Évolution", "Qui a la plus grosse progression de toute l'histoire ?", "Écart entre premier et meilleur arc", "Prêt"),
 ("Évolution", "Le vieillissement des légendes : Garp, Hiruzen, Yamamoto", "Déclin daté", "Prêt"),
 ("Hiérarchie", "Les Hokage classés", "Classement par arc", "Prêt"),
 ("Hiérarchie", "Les amiraux classés, de Sengoku à Ryokugyu", "Classement", "Prêt"),
 ("Hiérarchie", "Les Espada classés : le numéro veut-il dire quelque chose ?", "Numéro officiel contre force", "Prêt"),
 ("Hiérarchie", "Les Lunes supérieures : le rang est-il juste ?", "Rang officiel contre force", "Prêt"),
 ("Hiérarchie", "Les Hashira classés", "Classement", "Prêt"),
 ("Hiérarchie", "Les Fourreaux rouges classés", "Classement", "Prêt"),
 ("Hiérarchie", "Le top 10 des héros de My Hero Academia : le classement officiel tient-il ?", "Rang officiel contre force", "Prêt"),
 ("Méta", "Le duel le plus serré de chaque œuvre (le vrai 50/50)", "Recherche automatique des duels les plus équilibrés", "Prêt"),
 ("Méta", "Le perso le plus sous-coté de chaque œuvre", "Écart entre statut officiel et force par les combats", "Prêt"),
 ("Méta", "Le perso le plus surcoté de chaque œuvre", "Idem, dans l'autre sens", "Prêt"),
 ("Méta", "Vos commentaires ont changé le modèle : les 10 arguments qui ont fait bouger un verdict", "Historique des corrections venues des commentaires", "Au fil des vidéos"),
 ("Hax", "En puissance brute contre avec les pouvoirs : les 10 duels où les hax changent tout", "Cote brute + liste des pouvoirs décisifs", "Prêt"),
 ("Hax", "L'Infini de Gojo bat-il tout l'univers Naruto ?", "Cote brute, puis débat sur l'Infini", "Prêt"),
]

F = "Arial"; hdr = Font(name=F, bold=True, color="FFFFFF"); body = Font(name=F, size=10)
HF = PatternFill("solid", fgColor="18140F"); thin = Side(style="thin", color="BFBFBF"); BRD = Border(left=thin, right=thin, top=thin, bottom=thin)
def table(ws, H, R, W, pct=()):
    ws.append(H)
    for c in range(1, len(H) + 1):
        x = ws.cell(1, c); x.font = hdr; x.fill = HF; x.alignment = Alignment(wrap_text=True, vertical="center"); x.border = BRD
    for r in R: ws.append(r)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for x in row: x.font = body; x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = BRD
        for c in pct: row[c - 1].number_format = "0%"
    for i, w in enumerate(W, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "B2"; ws.auto_filter.ref = ws.dimensions

p = os.path.join(HERE, "plan_200_videos.xlsx"); wb = load_workbook(p)
table(wb.create_sheet("Vidéos longues"), ["Titre", "Durée", "Contenu", "Statut"], [list(x) for x in LONGUES], [60, 10, 70, 16])
table(wb.create_sheet("Idées d'analyses"), ["Thème", "Idée de vidéo", "Ce que le modèle calcule", "Statut"], [list(x) for x in IDEES], [16, 60, 60, 16])
st = sorted(A["statements"], key=lambda s: s["p"])
table(wb.create_sheet("Les persos disent-ils vrai"), ["Œuvre", "Déclaration (canon)", "A", "B", "Type", "Probabilité que ce soit vrai (combats seuls)", "Verdict"],
      [[LABEL[s["verse"]], s["label"], s["a"], s["b"], s["kind"], s["p"], "Probablement faux" if s["p"] < .35 else "Probablement vrai" if s["p"] > .65 else "Incertain"] for s in st],
      [14, 70, 22, 22, 11, 16, 18], pct=(6,))
table(wb.create_sheet("Pires incohérences"), ["Œuvre", "Vainqueur (canon)", "Perdant", "Chance que le modèle lui donnait", "Contexte"],
      [[LABEL[s["verse"]], s["winner"], s["loser"], s["p"], s["note"]] for s in A["surprises"]], [14, 30, 30, 14, 70], pct=(4,))
table(wb.create_sheet("Plot armor"), ["Œuvre", "Perso", "Indice de plot armor", "Victoires", "Victoires improbables (< 35 %)"],
      [[LABEL[s["verse"]], s["c"], s["score"], s["wins"], s["unlikely"]] for s in A["armor"]], [14, 30, 14, 10, 18])
table(wb.create_sheet("Cohérence des œuvres"), ["Œuvre", "Surprise moyenne par combat (plus bas = plus cohérent)", "Combats « choquants » (vainqueur à moins de 25 %)", "Combats", "Poids des alliés η"],
      [[c["label"], c["mean_surprise"], c["shock"], c["n"], c["eta"]] for c in sorted(A["coherence"], key=lambda c: c["mean_surprise"])], [22, 26, 22, 10, 14])
wb.save(p); print("ok")
