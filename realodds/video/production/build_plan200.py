"""Calcule le verdict du modèle et les preuves canon de chacune des 200 vidéos, puis écrit plan_200_videos.xlsx
(et plan200_verdicts.json, utilisé pour vérifier que l'avis final ne contredit pas le calcul)."""
import json, math, os, sys, collections
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from plan200 import PLAN
PATH = {"naruto": "model_out.json"}
MO = {}
def mo(v):
    if v not in MO: MO[v] = json.load(open(os.path.join(ROOT, PATH.get(v, f"verses/{v}/model_out.json"))))
    return MO[v]
LABEL = {"naruto": "Naruto", "onepiece": "One Piece", "dragonball": "Dragon Ball", "jujutsukaisen": "Jujutsu Kaisen", "bleach": "Bleach",
         "hunterxhunter": "Hunter x Hunter", "demonslayer": "Demon Slayer", "mha": "My Hero Academia", "aot": "L'Attaque des Titans", "chainsawman": "Chainsaw Man"}

def parse(spec):
    v, rest = spec.split(":"); c, arc = (rest.split("@") + [None])[:2]
    d = mo(v); ch = d["chars"].get(c)
    if ch is None: raise KeyError(f"{v}:{c} inconnu")
    ser = ch["series"]
    if arc is None: s = max(ser, key=lambda x: x["mean"])
    else:
        m = [x for x in ser if x["arc"] == arc]
        if not m: raise KeyError(f"{v}:{c} n'a pas d'arc {arc} (arcs : {[x['arc'] for x in ser]})")
        s = m[0]
    aname = {a["id"]: a["name"] for a in d["arcs"]}[s["arc"]]
    return dict(v=v, c=c, arc=s["arc"], arcname=aname, name=ch["name"], m=s["mean"], sd=s["sd"])

rng = np.random.default_rng(1)
def probs(d_logit, c1):
    pa = 1 - 1 / (1 + np.exp(-(c1 - d_logit))); pb = 1 / (1 + np.exp(c1 + d_logit)); return pa.mean(), pb.mean()
def duel1(A, B, n=40000):
    d = mo(A["v"]); K = d["meta"]["tier"]; c1 = d["cuts"][3]
    z = rng.normal(A["m"] - B["m"], math.hypot(A["sd"], B["sd"]), n) * K; return probs(z, c1)
def team(As, Bs, n=20000, copies=1):
    d = mo(As[0]["v"]); K = d["meta"]["tier"]; c1 = d["cuts"][3]; eta0 = d["meta"]["eta"]; lsd = d["meta"]["eta_log_sd"]
    eta = eta0 * np.exp(lsd * rng.standard_normal(n))
    def T(X):
        S = np.stack([(x["m"] + x["sd"] * rng.standard_normal(n)) * K for x in X])
        return eta * np.log(np.exp((S - S.max(0)) / eta).sum(0)) + S.max(0)
    return probs(T(As) + eta * math.log(copies) - T(Bs), c1)

sys.argv = [sys.argv[0]]
import importlib.util
sp = importlib.util.spec_from_file_location("cross", os.path.join(ROOT, "interoeuvres", "cross.py")); cross = importlib.util.module_from_spec(sp)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()): sp.loader.exec_module(cross)
XF = json.load(open(os.path.join(ROOT, "interoeuvres", "cross_out.json")))["feats"]

def evidence(A, B):
    """Preuves canon : combats directs, puis adversaires communs (A a battu X ; X a affronté B)."""
    if A["v"] != B["v"]: return ""
    F = mo(A["v"])["fights"]; names = {k: v["name"] for k, v in mo(A["v"])["chars"].items()}
    out = []
    for f in F:
        if (A["c"] in f["a"] and B["c"] in f["b"]) or (B["c"] in f["a"] and A["c"] in f["b"]):
            w = "nul" if f["res"] == "D" else names.get(f["a"][0], f["a"][0]) + " gagne"
            out.append(f"Combat direct : {w} — {f['note'] or f['arc']}")
    def beats(c):
        r = {}
        for f in F:
            if f["res"] == "A" and c in f["a"]:
                for o in f["b"]: r.setdefault(o, f)
            if f["res"] == "A" and c in f["b"]:
                for o in f["a"]: r.setdefault(("lost", o), f)
        return r
    ra, rb = beats(A["c"]), beats(B["c"])
    com = [o for o in ra if not isinstance(o, tuple) and (o in rb or ("lost", o) in rb) and not mo(A["v"])["chars"].get(o, {}).get("generic")]
    for o in com[:3]:
        rel = "a battu" if o in rb else "a perdu contre"
        out.append(f"{A['name']} a battu {names.get(o, o)} ; {B['name']} {rel} {names.get(o, o)}")
    return "\n".join(out[:5])

def cross_team(As, Bs, n=6000):
    """Équipes de plusieurs œuvres : chacun est placé sur l'échelle commune, puis projeté dans les règles de chaque œuvre
    présente (son poids des alliés, ses seuils) ; la cote est la moyenne sur ces œuvres."""
    ids = [v["id"] for v in cross.V]; NV = cross.NV
    TT = rng.multivariate_normal(cross.th, cross.cov, n); a = TT[:, :NV]; b = np.exp(TT[:, NV:2 * NV])
    def U(X):
        i = ids.index(X["v"]); return a[:, i] + b[:, i] * (X["m"] + X["sd"] * rng.standard_normal(n))
    UA, UB = [U(x) for x in As], [U(x) for x in Bs]; out = []
    for w in sorted(set(x["v"] for x in As + Bs)):
        i = ids.index(w); K = mo(w)["meta"]["tier"]; c1 = mo(w)["cuts"][3]
        eta = mo(w)["meta"]["eta"] * np.exp(mo(w)["meta"]["eta_log_sd"] * rng.standard_normal(n))
        def T(UU):
            S = np.stack([(uu - a[:, i]) / b[:, i] * K for uu in UU]); m = S.max(0)
            return m + eta * np.log(np.exp((S - m) / eta).sum(0))
        out.append(probs(T(UA) - T(UB), c1))
    return float(np.mean([o[0] for o in out])), float(np.mean([o[1] for o in out])), [float(np.mean(x)) for x in UA + UB]

def featline(X):
    fs = [f for f in XF if f["verse"] == X["v"] and f["c"] == X["c"]]
    return " ; ".join(f"{f['label']} ({f['ref']})" for f in fs[:2])

rows, verd, chars_used = [], [], collections.Counter()
for k, (fmt, sa, sb, title, hook, take) in enumerate(PLAN, 1):
    if fmt in ("1v1", "inter", "clones"):
        A, B = parse(sa), parse(sb); chars_used[(A["v"], A["c"])] += 1; chars_used[(B["v"], B["c"])] += 1
        if fmt == "1v1": pa, pb = duel1(A, B); ev = evidence(A, B)
        elif fmt == "inter":
            r = cross.duel(A["v"], A["c"], A["arc"], B["v"], B["c"], B["arc"], n=6000); pa, pb = r["pa"], r["pb"]
            ev = "\n".join(x for x in [f"{A['name']} : environ 10^{r['ua'][0]:.0f} × un humain" + (f" — {featline(A)}" if featline(A) else ""),
                                       f"{B['name']} : environ 10^{r['ub'][0]:.0f} × un humain" + (f" — {featline(B)}" if featline(B) else "")] if x)
        else:
            nmax = max(10, mo(A["v"])["meta"]["max_team"]); first = None
            for nn in range(1, 31):
                pa_, pb_ = team([A], [B], 8000, copies=nn)
                if pa_ >= pb_: first = nn; break
            pa, pb = team([A], [B], 8000, copies=first or 30)
            ev = f"Il faut {first} {A['name']} pour passer devant" if first else f"Même 30 {A['name']} ne suffisent pas"
            if first and first > mo(A['v'])['meta']['max_team']: ev += f" (au-delà des groupes vus dans l'œuvre : extrapolation)"
        lab_a, lab_b = f"{A['name']} ({A['arcname']})", f"{B['name']} ({B['arcname']})"
    else:
        As = [parse(x) for x in sa.split("+")]; Bs = [parse(x) for x in sb.split("+")]
        for X in As + Bs: chars_used[(X["v"], X["c"])] += 1
        A, B = As[0], Bs[0]
        lab_a, lab_b = " + ".join(x["name"] for x in As), " + ".join(x["name"] for x in Bs)
        if fmt == "equipe":
            pa, pb = team(As, Bs)
            ev = f"Poids des alliés appris dans l'œuvre : η = {mo(A['v'])['meta']['eta']:.2f}"
        else:
            pa, pb, us = cross_team(As, Bs)
            ev = " ; ".join(f"{x['name']} ≈ 10^{u:.0f} × humain" for x, u in zip(As + Bs, us))
    pd_ = 1 - pa - pb; win = "A" if pa > pb + .03 else "B" if pb > pa + .03 else "="
    oeuvre = LABEL[A["v"]] if fmt not in ("inter", "inter_equipe") else " × ".join(dict.fromkeys(LABEL[x["v"]] for x in (As + Bs if fmt == "inter_equipe" else [A, B])))
    rows.append([k, {"1v1": "1 contre 1", "equipe": "Combat de groupe", "clones": "Combien il en faut ?", "inter": "Inter-œuvres", "inter_equipe": "Groupes inter-œuvres"}[fmt], oeuvre, title,
                 lab_a, lab_b, round(pa, 3), round(pd_, 3), round(pb, 3), hook, take, ev])
    verd.append(dict(k=k, title=title, win=win, pa=round(pa, 3), pb=round(pb, 3), take=take))
json.dump(verd, open(os.path.join(HERE, "plan200_verdicts.json"), "w"), ensure_ascii=False, indent=0)

# ---------------- classeur
F = "Arial"; hdr = Font(name=F, bold=True, color="FFFFFF"); body = Font(name=F, size=10)
HF = PatternFill("solid", fgColor="18140F"); thin = Side(style="thin", color="BFBFBF"); BRD = Border(left=thin, right=thin, top=thin, bottom=thin)
def table(ws, H, R, W, pct_cols=(), status_col=None, statuses='"À chercher,Trouvé,Reçu,Introuvable"'):
    ws.append(H)
    for c in range(1, len(H) + 1):
        x = ws.cell(1, c); x.font = hdr; x.fill = HF; x.alignment = Alignment(wrap_text=True, vertical="center"); x.border = BRD
    for r in R: ws.append(r)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for x in row: x.font = body; x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = BRD
        for c in pct_cols: row[c - 1].number_format = "0%"
    for i, w in enumerate(W, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "E2"; ws.auto_filter.ref = ws.dimensions
    if status_col:
        dv = DataValidation(type="list", formula1=statuses, allow_blank=True); ws.add_data_validation(dv)
        dv.add(f"{get_column_letter(status_col)}2:{get_column_letter(status_col)}{ws.max_row + 50}")

wb = Workbook(); ws = wb.active; ws.title = "Mode d'emploi"
lines = [("LE VERDICT — les 200 vidéos et tout ce qu'il faut pour les animer", True), ("", False),
 ("Onglet « 200 vidéos »", True),
 ("Chaque ligne est une vidéo : le duel, le moment de l'histoire de chaque perso, la cote du modèle (A / nul / B), l'accroche, l'avis final controversé et les preuves canon tirées des données (combats directs, adversaires communs, exploits chiffrés).", False),
 ("Les cotes sont calculées par le modèle à la date de ce classeur ; elles peuvent bouger quand le modèle est affiné. La colonne « État » est à remplir (Idée / Texte écrit / Voix enregistrée / Montée / Publiée).", False),
 ("Ordre conseillé : alterner Naruto et One Piece d'abord (les plus débattus), puis une vidéo d'une autre œuvre tous les 3-4, un combat de groupe par semaine, une vidéo inter-œuvres toutes les 2 semaines.", False), ("", False),
 ("Onglet « Médias par perso »", True),
 ("Pour chaque perso qui apparaît dans les 200 vidéos : un court extrait de sa technique signature, un extrait de sa victoire la plus célèbre, et un GIF de pose ou d'aura. Les persos sont classés par nombre de vidéos où ils apparaissent : commence par le haut.", False),
 ("Onglet « Effets et archives »", True),
 ("Les animations de comparaison (explosions nucléaires d'archive, météorites, Lune, Terre, tsunamis, éclairs…) pour les vidéos inter-œuvres et « tant de fois un humain ».", False), ("", False),
 ("Formats des médias", True),
 ("Extraits vidéo : MP4, 3 à 8 secondes, la meilleure qualité possible, sans sous-titres incrustés ni logo de chaîne si possible. GIF : accepté, mais un MP4 court est toujours mieux. Nom du fichier = colonne « Fichier ».", False),
 ("Attention aux droits", True),
 ("Les extraits d'anime (Toei pour One Piece et Dragon Ball notamment) déclenchent souvent des réclamations Content ID qui coupent la monétisation. Règles prudentes : extraits très courts (moins de 5 s), jamais plusieurs à la suite, toujours transformés (recadrage, trame manga, ralenti, texte par-dessus) et commentés. Les cases de manga redessinées par l'animation de la chaîne restent la base. Les archives d'explosions nucléaires du gouvernement américain et les images de la NASA sont dans le domaine public. Ce n'est pas un avis juridique.", False)]
for i, (s, b) in enumerate(lines, 1):
    c = ws.cell(i, 1, s); c.font = Font(name=F, bold=b, size=14 if i == 1 else 10); c.alignment = Alignment(wrap_text=True, vertical="top")
ws.column_dimensions["A"].width = 130

ws = wb.create_sheet("200 vidéos")
table(ws, ["N°", "Format", "Œuvre", "Titre", "Combattant A (moment)", "Combattant B (moment)", "A gagne", "Nul", "B gagne", "Accroche", "Avis final (controversé)", "Preuves canon (tirées du modèle)", "État"],
      [r + ["Idée"] for r in rows], [5, 14, 16, 30, 26, 26, 8, 7, 8, 34, 44, 60, 12], pct_cols=(7, 8, 9), status_col=13,
      statuses='"Idée,Texte écrit,Voix enregistrée,Montée,Publiée"')

ws = wb.create_sheet("Médias par perso")
media = []
for (v, c), cnt in chars_used.most_common():
    name = mo(v)["chars"][c]["name"]; pr = 1 if cnt >= 3 else 2 if cnt == 2 else 3
    media += [[f"{v}_{c}_signature.mp4", LABEL[v], name, cnt, "Extrait vidéo (3-8 s)", "Sa technique signature, au moment le plus spectaculaire", pr, "À chercher", ""],
              [f"{v}_{c}_victoire.mp4", LABEL[v], name, cnt, "Extrait vidéo (3-8 s)", "Le coup final de sa victoire la plus célèbre", pr, "À chercher", ""],
              [f"{v}_{c}_aura.gif", LABEL[v], name, cnt, "GIF ou MP4 en boucle", "Pose ou aura en boucle (transformation, regard, mise en garde)", min(3, pr + 1), "À chercher", ""]]
table(ws, ["Fichier", "Œuvre", "Personnage", "Nb de vidéos", "Type", "Quoi", "Priorité", "Statut", "Remarque"], media, [34, 16, 26, 10, 18, 52, 9, 13, 30], status_col=8)

ws = wb.create_sheet("Effets et archives")
FX = [("arch_nucleaire_trinity.mp4", "Explosion nucléaire d'archive (essai Trinity ou Castle Bravo)", "Domaine public (archives du gouvernement américain)", 1),
      ("arch_tsar_bomba.mp4", "Champignon de la Tsar Bomba (la plus grosse bombe de l'histoire)", "Archive, vérifier la licence", 1),
      ("arch_hiroshima_echelle.png", "Schéma ou photo d'échelle de Hiroshima (unité « bombe d'Hiroshima »)", "Domaine public", 1),
      ("nasa_lune.mp4", "La Lune qui tourne (NASA)", "Domaine public NASA", 1), ("nasa_terre.mp4", "La Terre vue de l'espace (NASA)", "Domaine public NASA", 1),
      ("nasa_meteorite.mp4", "Météore ou bolide filmé (ou animation NASA d'impact)", "Domaine public NASA", 1),
      ("reel_tsunami.mp4", "Vague géante réelle (sans victimes visibles)", "Libre de droits (Pexels, Wikimedia)", 2),
      ("reel_eclair.mp4", "Éclair au ralenti", "Libre de droits", 1), ("reel_volcan.mp4", "Éruption volcanique, coulée de lave", "Libre de droits", 2),
      ("reel_seisme.mp4", "Sol qui se fend, effondrement (démolition contrôlée)", "Libre de droits", 2),
      ("reel_ville_vue_ciel.mp4", "Ville vue du ciel (drone)", "Libre de droits", 2), ("reel_montagne.mp4", "Montagne vue de loin", "Libre de droits", 2),
      ("reel_sprinter.mp4", "Sprinter ou boxeur (l'humain normal de référence)", "Libre de droits", 1),
      ("reel_ours.mp4", "Ours ou gorille qui charge (repère animal)", "Libre de droits", 3),
      ("fx_encre_eclaboussure.mp4", "Éclaboussure d'encre noire sur fond blanc", "Libre de droits ou je la génère", 2),
      ("fx_papier_dechire.mp4", "Papier qui se déchire (transition)", "Libre de droits", 3),
      ("fx_glitch_vhs.mp4", "Glitch / distorsion (pour les « hax »)", "Libre de droits", 3),
      ("fx_etincelles.mp4", "Étincelles ou braises sur fond noir", "Libre de droits", 3)]
table(ws, ["Fichier", "Quoi", "Source conseillée", "Priorité", "Statut", "Remarque"], [[a, b, c, p, "À chercher", ""] for a, b, c, p in FX], [30, 56, 40, 9, 13, 30], status_col=5)
wb.save(os.path.join(HERE, "plan_200_videos.xlsx"))
print(len(rows), "vidéos ;", len(media), "médias perso ;", len(FX), "effets")
