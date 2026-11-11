"""Comparaison inter-œuvres : relier l'échelle de force de chaque œuvre à une échelle physique commune.

Échelle commune u = log10 de « combien de fois un humain adulte normal » (u = 0 : humain ; u = 3 : mille fois un humain).
Pour chaque œuvre v, la force latente s (en échelons, sortie de model.py) est reliée à u par une droite :
        u = a_v + b_v · s
a_v et b_v sont estimés à partir de trois sortes de preuves, toutes canon :
  1. les exploits chiffrés (feats.py) : log10(grandeur) = c_k + β_k · u + bruit (Student t, ν = 4, robuste aux exploits isolés),
     avec c_k et β_k fixés par la physique et un humain de référence (voir HUMAIN) ;
  2. les combattants du modèle qui sont de simples humains armés (ANCHOR_ENTITIES) : leur u est connu à peu près ;
  3. les rencontres canon avec des êtres réels (ANCHORS) : la probabilité du résultat suit le modèle de l'œuvre lui-même.
Le bruit d'exploit σ (en décades) est commun à toutes les œuvres. MAP + approximation de Laplace.
L'énergie destructrice définit l'échelle (β = 1). Pour la force de levage, la vitesse et la résistance, la pente β_k est
estimée (a priori centré sur la valeur physique) : dans la fiction, soulever ou courir ne grandit pas forcément aussi vite
que la puissance des attaques, et un β fixé à la main faisait apparaître de faux exploits « hors norme ».

Cote d'un duel A (œuvre v) contre B (œuvre w) : on projette B dans l'échelle de v (s_B→v = (u_B − a_v)/b_v) et on applique
le modèle ordinal de v ; on fait de même dans l'échelle de w ; la cote finale est la moyenne des deux. Quand v = w, on retrouve
exactement le modèle de l'œuvre. L'écart entre les deux projections mesure le désaccord entre les « physiques » des deux œuvres.
"""
import importlib.util, json, math, os, sys
import numpy as np
import jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update("jax_enable_x64", True)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VERSES = [("naruto", "Naruto", "."), ("onepiece", "One Piece", "verses/onepiece"),
          ("dragonball", "Dragon Ball", "verses/dragonball"), ("jujutsukaisen", "Jujutsu Kaisen", "verses/jujutsukaisen")]
# humain adulte de référence (u = 0) : log10 de la grandeur SI, et pente physique β (décades de grandeur par décade de u)
HUMAIN = {"energie": (2.1, 1.0),      # coup de poing ~125 J
          "resistance": (2.3, 1.0),   # encaisse ~200 J sans être mis hors combat
          "force": (1.9, 1.0),        # soulève ~80 kg
          "vitesse": (0.85, 0.5)}     # sprint ~7 m/s ; l'énergie varie comme v², d'où β = 0,5
# êtres réels (u, incertitude)
REEL = {"humain": (0.0, 0.3), "soldat_arme": (1.1, 0.4)}   # fusil d'assaut : ~1,5-3 kJ par balle
NU = 4.0


def load(path, name):
    p = os.path.join(ROOT, path, name)
    if not os.path.exists(p):
        return None
    sp = importlib.util.spec_from_file_location(name.replace(".", "_") + path.replace("/", "_"), p)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


def species_u():
    sp = load("animaux", "species.py")
    if sp is None:
        return {}
    out = {}
    for k, v in sp.SPECIES.items():
        mass = v[1] if isinstance(v, (tuple, list)) else v.get("mass")
        if isinstance(mass, (int, float)):
            out[k] = (math.log10(mass / 78.0), 0.5)
    return out


REEL.update({k: v for k, v in species_u().items() if k not in REEL})

V = []
for vid, label, path in VERSES:
    mo = json.load(open(os.path.join(ROOT, path, "model_out.json")))
    fe = load(path, "feats.py")
    V.append(dict(id=vid, label=label, mo=mo, feats=getattr(fe, "FEATS", []), anchors=getattr(fe, "ANCHORS", []),
                  ents=getattr(fe, "ANCHOR_ENTITIES", {}), tier=mo["meta"]["tier"], eta=mo["meta"].get("eta", 1.0),
                  c1=mo["cuts"][3]))


def node(v, c, arc):
    s = [x for x in v["mo"]["chars"][c]["series"] if x["arc"] == arc][0]
    return s["mean"], s["sd"]


# ---- observations, mises à plat
KINDS = ["force", "vitesse", "resistance"]           # types dont la pente est estimée
F = []   # feats : (verse, y, c, beta, fsd, m, sd, kind index ou -1 pour énergie)
for i, v in enumerate(V):
    for (c, arc, kind, y, fsd, *_rest) in v["feats"]:
        m, sd = node(v, c, arc); c0, be = HUMAIN[kind]; F.append((i, y, c0, be, fsd, m, sd, KINDS.index(kind) if kind in KINDS else -1))
E = []   # entités-ancres : (verse, u, usd, m, sd)
for i, v in enumerate(V):
    for e, (u, usd) in v["ents"].items():
        ser = v["mo"]["chars"][e]["series"]; m = float(np.mean([x["mean"] for x in ser])); sd = float(np.mean([x["sd"] for x in ser]))
        E.append((i, u, usd, m, sd))
A = []   # rencontres réelles : (verse, u_e, usd_e, n, m, sd, gagne(1)/perd(0)/nul(.5))
for i, v in enumerate(V):
    for (c, arc, ent, res, *_r) in v["anchors"]:
        name, n = (ent.split("*") + ["1"])[:2]; u, usd = REEL[name]; m, sd = node(v, c, arc)
        A.append((i, u, usd, int(n), m, sd, {"A": 1.0, "B": 0.0, "D": 0.5}[res]))
NV = len(V)
Fa = {k: jnp.array([f[j] for f in F]) for j, k in enumerate(["v", "y", "c", "be", "fsd", "m", "sd", "k"])}
Fa["v"] = Fa["v"].astype(int); Fa["k"] = Fa["k"].astype(int)
NK = len(KINDS); BE0 = jnp.array([HUMAIN[k][1] for k in KINDS])
TIER = jnp.array([v["tier"] for v in V]); ETA = jnp.array([v["eta"] for v in V]); C1 = jnp.array([v["c1"] for v in V])


def unpack(th):
    return th[:NV], jnp.exp(th[NV:2 * NV]), jnp.exp(th[2 * NV])


def betas(th):
    bk = BE0 * jnp.exp(th[2 * NV + 1:2 * NV + 1 + NK])
    return jnp.where(Fa["k"] >= 0, bk[jnp.maximum(Fa["k"], 0)], 1.0)


def tlog(z, scale):
    return jax.scipy.special.gammaln((NU + 1) / 2) - jax.scipy.special.gammaln(NU / 2) - 0.5 * jnp.log(NU * math.pi) - jnp.log(scale) \
        - (NU + 1) / 2 * jnp.log1p((z / scale) ** 2 / NU)


def neg_logpost(th):
    a, b, sig = unpack(th)
    lp = -0.5 * jnp.sum((a / 1.5) ** 2) - 0.5 * jnp.sum(((jnp.log(b) - math.log(2.0)) / 1.0) ** 2) - 0.5 * ((jnp.log(sig) - math.log(0.8)) / 0.5) ** 2
    if F:
        v = Fa["v"]; be = betas(th); u = a[v] + b[v] * Fa["m"]; mu = Fa["c"] + be * u
        scale = jnp.sqrt(sig ** 2 + Fa["fsd"] ** 2 + (be * b[v] * Fa["sd"]) ** 2)
        lp += -0.5 * jnp.sum((th[2 * NV + 1:2 * NV + 1 + NK] / 0.7) ** 2)
        lp += jnp.sum(tlog(Fa["y"] - mu, scale))
    for (i, u, usd, m, sd) in E:
        lp += -0.5 * ((u - (a[i] + b[i] * m)) ** 2 / (usd ** 2 + (b[i] * sd) ** 2))
    for (i, u, usd, n, m, sd, r) in A:
        se = (u - a[i]) / b[i] + ETA[i] / TIER[i] * math.log(n)            # entité (et son groupe) dans l'échelle de l'œuvre
        var = sd ** 2 + (usd / b[i]) ** 2
        d = TIER[i] * (m - se) / jnp.sqrt(1 + math.pi * TIER[i] ** 2 * var / 8)
        pa = 1 - jax.nn.sigmoid(C1[i] - d); pb = jax.nn.sigmoid(-C1[i] - d); pd = 1 - pa - pb
        lp += jnp.log(jnp.clip(pa if r == 1 else pb if r == 0 else pd, 1e-9, 1))
    return -lp


P = 2 * NV + 1 + NK
x0 = np.concatenate([np.zeros(NV), np.full(NV, math.log(2.0)), [math.log(0.8)], np.zeros(NK)])
f = jax.jit(neg_logpost); g = jax.jit(jax.grad(neg_logpost))
res = minimize(lambda x: float(f(x)), x0, jac=lambda x: np.asarray(g(x)), method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-9))
H = np.asarray(jax.hessian(neg_logpost)(res.x)); H = 0.5 * (H + H.T) + 1e-9 * np.eye(P)
cov = np.linalg.inv(H); th = res.x
a, b, sig = [np.asarray(x) for x in unpack(jnp.array(th))]
BK = np.asarray(BE0 * np.exp(th[2 * NV + 1:]))
print("MAP", round(res.fun, 3), "converge", res.success, "σ exploits (décades)", round(float(sig), 2), "pentes", dict(zip(KINDS, np.round(BK, 2))))
for i, v in enumerate(V):
    print(f"  {v['label']:15s} a = {a[i]:+.2f} ± {math.sqrt(cov[i, i]):.2f}   b = {b[i]:.2f} décades/échelon (×/÷ {math.exp(math.sqrt(cov[NV + i, NV + i])):.2f})"
          f"   exploits {sum(1 for x in F if x[0] == i)}, ancres {sum(1 for x in E if x[0] == i) + sum(1 for x in A if x[0] == i)}")

# résidus standardisés des exploits
resid = []
for (i, y, c0, be, fsd, m, sd, k), raw in zip(F, [x for v in V for x in v["feats"]]):
    be = BK[k] if k >= 0 else 1.0
    mu = c0 + be * (a[i] + b[i] * m); sc = math.sqrt(sig ** 2 + fsd ** 2 + (be * b[i] * sd) ** 2)
    resid.append(dict(verse=V[i]["id"], c=raw[0], arc=raw[1], kind=raw[2], y=y, pred=round(mu, 2), z=round((y - mu) / sc, 2), label=raw[5], ref=raw[6], calc=raw[7]))
print("exploits hors norme (|z| > 2) :", [(r["verse"], r["c"], r["z"]) for r in resid if abs(r["z"]) > 2])

out = dict(verses=[dict(id=v["id"], label=v["label"], tier=v["tier"], eta=v["eta"], cuts=v["mo"]["cuts"]) for v in V],
           theta=[float(x) for x in th], cov=cov.tolist(), sigma=float(sig), humain=HUMAIN, pentes=dict(zip(KINDS, [float(x) for x in BK])), feats=resid,
           anchors=[dict(verse=V[i]["id"], u=u, n=n, res=r) for (i, u, usd, n, m, sd, r) in A],
           entities=[dict(verse=V[i]["id"], u=u) for (i, u, usd, m, sd) in E])
json.dump(out, open(os.path.join(os.path.dirname(__file__), "cross_out.json"), "w"), ensure_ascii=False)


def duel(va, ca, ka, vb, cb, kb, n=20000, seed=0):
    """Cote A (œuvre va) contre B (œuvre vb), moyenne des deux projections."""
    rng = np.random.default_rng(seed); ia = [v["id"] for v in V].index(va); ib = [v["id"] for v in V].index(vb)
    T = rng.multivariate_normal(th, cov, n); aa, bb = T[:, :NV], np.exp(T[:, NV:2 * NV])
    ma, sa = node(V[ia], ca, ka); mb, sb = node(V[ib], cb, kb)
    xa = ma + sa * rng.standard_normal(n); xb = mb + sb * rng.standard_normal(n)
    ua = aa[:, ia] + bb[:, ia] * xa; ub = aa[:, ib] + bb[:, ib] * xb
    outp = []
    for i in (ia, ib):
        d = V[i]["tier"] * ((ua - aa[:, i]) / bb[:, i] - (ub - aa[:, i]) / bb[:, i]); c1 = V[i]["c1"]
        pa = 1 - 1 / (1 + np.exp(-(c1 - d))); pb = 1 / (1 + np.exp(c1 + d)); outp.append((pa.mean(), pb.mean()))
    pa = (outp[0][0] + outp[1][0]) / 2; pb = (outp[0][1] + outp[1][1]) / 2
    return dict(pa=round(pa, 3), pb=round(pb, 3), pd=round(1 - pa - pb, 3), ua=(round(ua.mean(), 2), round(ua.std(), 2)),
                ub=(round(ub.mean(), 2), round(ub.std(), 2)), proj=[tuple(round(x, 3) for x in o) for o in outp])


if __name__ == "__main__":
    for q in [("jujutsukaisen", "sukuna", "shinjuku2", "onepiece", "luffy", "wano5"), ("naruto", "naruto", "final", "onepiece", "luffy", "wano5"),
              ("naruto", "minato", "kyubi", "naruto", "itachi", "invasion"), ("dragonball", "goku", "superbuu", "naruto", "naruto", "final"),
              ("jujutsukaisen", "gojo", "shinjuku", "naruto", "itachi", "invasion"), ("onepiece", "zoro", "wano", "jujutsukaisen", "sukuna", "shibuya")]:
        print(q, duel(*q))
