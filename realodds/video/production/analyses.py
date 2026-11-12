"""Analyses « gaulerie mais sérieuses » tirées du modèle, pour les vidéos d'idées :
1. Les persos disent-ils vrai ? Chaque déclaration de hiérarchie (« X est plus fort que Y ») est confrontée à ce que
   disent les COMBATS SEULS (modèle réajusté sans aucune déclaration, NO_ORDER=1).
2. Les pires incohérences : les résultats canon que le modèle trouve les moins plausibles.
3. Plot armor : qui gagne le plus de combats qu'il « aurait dû » perdre.
4. Quelle œuvre est la plus cohérente : surprise moyenne par combat.
Écrit analyses.json."""
import json, math, os, glob, importlib.util
import numpy as np
from scipy.stats import norm
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SP = "/tmp/claude-0/-home-claude-tinylaws-media/6e4e3678-2eb0-528e-b94c-502dffb30ed4/scratchpad/groups"
DIRS = {"naruto": ".", **{v: f"verses/{v}" for v in ["onepiece", "dragonball", "hunterxhunter", "jujutsukaisen", "demonslayer", "bleach", "mha", "aot", "chainsawman"]}}
LABEL = {"naruto": "Naruto", "onepiece": "One Piece", "dragonball": "Dragon Ball", "jujutsukaisen": "Jujutsu Kaisen", "bleach": "Bleach",
         "hunterxhunter": "Hunter x Hunter", "demonslayer": "Demon Slayer", "mha": "My Hero Academia", "aot": "L'Attaque des Titans", "chainsawman": "Chainsaw Man"}

def load(path, name):
    p = os.path.join(ROOT, path, name)
    sp = importlib.util.spec_from_file_location(name + path.replace("/", "_"), p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m

def node(mo, c, t):
    ch = mo["chars"].get(c)
    if not ch or not ch["series"]: return None
    at = {a["id"]: a["t"] for a in mo["arcs"]}
    ok = [s for s in ch["series"] if at[s["arc"]] <= t + 1e-6]
    return (ok[-1] if ok else ch["series"][0])

out = dict(statements=[], surprises=[], armor=[], coherence=[])
for v, d in DIRS.items():
    prod = json.load(open(os.path.join(ROOT, d, "model_out.json")))
    p_no = os.path.join(SP, f"noorder_{v}.json")
    if os.path.exists(p_no):
        no = json.load(open(p_no)); st = load(d, "status.py")
        for (a, ta, b, tb, gap, sd, lab) in getattr(st, "ORDER", []):
            A, B = node(no, a, ta), node(no, b, tb)
            if not A or not B: continue
            mu, s = A["mean"] - B["mean"], math.hypot(A["sd"], B["sd"])
            if gap <= 0:   # égalité annoncée
                p = norm.cdf((0.5 - mu) / s) - norm.cdf((-0.5 - mu) / s); kind = "égalité"
            else:
                p = 1 - norm.cdf((0 - mu) / s); kind = "plus fort"
            out["statements"].append(dict(verse=v, a=prod["chars"].get(a, {}).get("name", a), b=prod["chars"].get(b, {}).get("name", b),
                                          kind=kind, p=round(float(p), 3), gap_combats=round(mu, 2), label=lab))
    names = {k: c["name"] for k, c in prod["chars"].items()}
    F = [f for f in prod["fights"] if f["res"] != "D"]
    for f in sorted([f for f in F if "i" not in f["flags"]], key=lambda f: f["p_a"])[:12]:
        out["surprises"].append(dict(verse=v, winner=" + ".join(names.get(x, x) for x in f["a"]), loser=" + ".join(names.get(x, x) for x in f["b"]),
                                     p=round(f["p_a"], 3), note=f["note"], flags=f["flags"]))
    arm = {}
    for f in F:
        for c in f["a"]:
            if prod["chars"].get(c, {}).get("generic"): continue
            r = arm.setdefault(c, [0.0, 0, 0]); r[0] += max(0.0, 0.5 - f["p_a"]); r[1] += 1; r[2] += f["p_a"] < 0.35
    for c, (sc, n, k) in sorted(arm.items(), key=lambda x: -x[1][0])[:8]:
        out["armor"].append(dict(verse=v, c=names[c], score=round(sc, 2), wins=n, unlikely=int(k)))
    allf = prod["fights"]; sur = [f["surprise"] for f in allf]
    out["coherence"].append(dict(verse=v, label=LABEL[v], mean_surprise=round(float(np.mean(sur)), 3), n=len(allf),
                                 shock=int(sum(1 for f in F if f["p_a"] < 0.25)), eta=prod["meta"].get("eta")))
json.dump(out, open(os.path.join(os.path.dirname(__file__), "analyses.json"), "w"), ensure_ascii=False, indent=0)
print(len(out["statements"]), "déclarations ;", len(out["surprises"]), "surprises")
for c in sorted(out["coherence"], key=lambda x: x["mean_surprise"]): print(c["label"], c["mean_surprise"], c["shock"], "/", c["n"])
