"""Real Odds — animaux. Modèle bayésien des rencontres documentées entre espèces.

Chaque espèce a une force latente s (échelle logit). A priori : s ~ N(a0 + b·ln(masse/78 kg) + Σ bonus des armes, TAU).
Un groupe de n individus vaut s + γ_social · ln(n_eff), avec n_eff = ln(1 + n/C) / ln(1 + 1/C) : au-delà de C attaquants,
ils se gênent et chaque attaquant de plus rapporte moins (C grandit quand la cible est plus grosse qu'eux : C = 1 + κ·√(masse cible / masse attaquant)).
Chaque rencontre ajoute la variabilité individuelle (σ = b·écart-type du log de la masse + résiduel, divisée par n pour un
groupe) et le hasard du combat (logit ordinal : à l'arraché / net / mise à mort, ou nul). Une part EPS de chaque résultat
peut être un coup de chance. Les circonstances (embuscade, petits à défendre, eau, arme blanche, jeune, blessé…) sont des
effets estimés, qu'on retire pour le combat neutre. MAP + Laplace (JAX) ; sortie animaux_out.json.
Usage : python3 model_animaux.py
"""
import importlib.util, json, math, os
import numpy as np
import jax, jax.numpy as jnp
from scipy.optimize import minimize
jax.config.update("jax_enable_x64", True)

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


SPECIES = load("species").SPECIES
PLURAL = {'lion': 'lions', 'tigre': 'tigres', 'jaguar': 'jaguars', 'leopard': 'léopards', 'guepard': 'guépards', 'puma': 'pumas', 'ours_brun': 'ours bruns', 'ours_noir': 'ours noirs', 'ours_polaire': 'ours polaires', 'loup': 'loups', 'coyote': 'coyotes', 'lycaon': 'lycaons', 'chien': 'gros chiens', 'hyene': 'hyènes', 'crocodile_nil': 'crocodiles du Nil', 'alligator': 'alligators', 'caiman': 'caïmans', 'anaconda': 'anacondas', 'orque': 'orques', 'requin_blanc': 'grands requins blancs', 'morse': 'morses', 'elephant': 'éléphants', 'hippopotame': 'hippopotames', 'rhinoceros': 'rhinocéros', 'buffle': 'buffles', 'bison': 'bisons', 'orignal': 'orignaux', 'gorille': 'gorilles', 'chimpanze': 'chimpanzés', 'babouin': 'babouins', 'humain': 'humains', 'ratel': 'ratels', 'kangourou': 'kangourous'}
ENC = []
for f in ("data_afrique", "data_nord", "data_transverse"):
    ENC += load(f).ENC
ENC, CORR_LOG = load("corrections").apply(ENC)
SP = list(SPECIES); IX = {s: i for i, s in enumerate(SP)}; NSP = len(SP)
WEAP = ["griffes", "crocs", "morsure", "cornes", "defenses", "coups", "constriction", "mains", "predateur"]
PRED = {"lion", "tigre", "jaguar", "leopard", "guepard", "puma", "ours_brun", "ours_polaire", "loup", "coyote", "lycaon", "hyene", "crocodile_nil", "alligator", "caiman", "anaconda", "orque", "requin_blanc"}
SOC = ["meute", "groupe", "solitaire"]
TAGS = ["embuscade", "defense_petits", "carcasse", "jeune", "vieux", "blesse", "eau", "arme_blanche", "outil", "captivite"]
TAG_PRIOR = {"embuscade": (1.0, .7), "defense_petits": (.5, .5), "carcasse": (0., .01), "jeune": (-1.5, .6), "vieux": (-.7, .5),
             "blesse": (-1.0, .5), "eau": (1.0, .7), "arme_blanche": (1.2, .6), "outil": (.5, .4), "captivite": (0., .5)}
QUALW = {"A": 1.0, "B": 0.7, "C": 0.35}
COUNT_CAP = 5          # un compte agrégé pèse au plus comme 5 rencontres (biais de signalement)
EPS = 0.05              # part « coup de chance » de chaque résultat
TAU = 0.6               # écart permis entre une espèce et ce que prédisent sa masse et ses armes
RESID = 0.35            # variabilité individuelle non expliquée par la masse (logit)

lnm = np.array([math.log(SPECIES[s][2] / 78.0) for s in SP])
sdlnm = np.array([(math.log(SPECIES[s][4]) - math.log(SPECIES[s][3])) / 3.29 for s in SP])
Wm = np.array([[1.0 if (w in SPECIES[s][5] or (w == "predateur" and s in PRED)) else 0.0 for w in WEAP] for s in SP])
socx = np.array([SOC.index(SPECIES[s][6]) for s in SP])
mass = np.array([SPECIES[s][2] for s in SP], float)

# ---- rencontres
ia, ib, na, nb, y, w, ta, tb = [], [], [], [], [], [], [], []
for r in ENC:
    if r["a"] not in IX or r["b"] not in IX:
        continue
    ia.append(IX[r["a"]]); ib.append(IX[r["b"]]); na.append(max(1, r["na"])); nb.append(max(1, r["nb"]))
    y.append(3 if r["res"] == "D" else 3 + r["m"])            # catégories 0..6 ; le vainqueur est toujours A
    wt = QUALW.get(r["qual"], .5) * min(r["count"], COUNT_CAP) * r["poids"]
    if "carcasse" in r["ta"] + r["tb"]:
        wt *= 0.5                                                   # simple déplacement autour d'une carcasse
    w.append(wt)
    ta.append([1.0 if t in r["ta"] else 0.0 for t in TAGS]); tb.append([1.0 if t in r["tb"] else 0.0 for t in TAGS])
ia, ib = jnp.array(ia), jnp.array(ib); na, nb = jnp.array(na, float), jnp.array(nb, float)
y = jnp.array(y); w = jnp.array(w); ta = jnp.array(ta); tb = jnp.array(tb)
NE = len(y); NT = len(TAGS); NW = len(WEAP)
lnm_j, sdlnm_j, Wm_j, mass_j, soc_j = jnp.array(lnm), jnp.array(sdlnm), jnp.array(Wm), jnp.array(mass), jnp.array(socx)

# paramètres : s (NSP), γ (3), lnκ, a0, b, bonus armes (NW), β tags (NT), 3 seuils
o_g = NSP; o_k = o_g + 3; o_a0 = o_k + 1; o_b = o_a0 + 1; o_w = o_b + 1; o_t = o_w + NW; o_c = o_t + NT; P = o_c + 3


def unpack(th):
    a = th[o_c:o_c + 3]; c1 = jnp.exp(a[0]); c2 = c1 + jnp.exp(a[1]); c3 = c2 + jnp.exp(a[2])
    return (th[:NSP], th[o_g:o_g + 3], th[o_k], th[o_a0], th[o_b], th[o_w:o_w + NW], th[o_t:o_t + NT],
            jnp.array([-c3, -c2, -c1, c1, c2, c3]))


def team(s, g, lk, i, n, j):
    C = 1.0 + jnp.exp(lk) * jnp.sqrt(mass_j[j] / mass_j[i])
    neff = jnp.log1p(n / C) / jnp.log1p(1.0 / C)   # ≈ n tant que n ≪ C, puis croît en log : rendement décroissant
    return s[i] + g[soc_j[i]] * jnp.log(neff)


def ord_logp(d, sc, cuts):
    cdf = jax.nn.sigmoid((cuts[None, :] - d[:, None]) / sc[:, None])
    cdf = jnp.concatenate([jnp.zeros((d.shape[0], 1)), cdf, jnp.ones((d.shape[0], 1))], axis=1)
    lp = jnp.log(jnp.clip(cdf[:, 1:] - cdf[:, :-1], 1e-12, 1.0))
    return jnp.logaddexp(jnp.log1p(-EPS) + lp, math.log(EPS / 7.0))


def enc_terms(th):
    s, g, lk, a0, b, bw, bt, cuts = unpack(th)
    d = team(s, g, lk, ia, na, ib) - team(s, g, lk, ib, nb, ia) + ta @ bt - tb @ bt
    sig2 = lambda i, n: ((b * sdlnm_j[i]) ** 2 + RESID ** 2) / n
    sc = jnp.sqrt(1.0 + math.pi * (sig2(ia, na) + sig2(ib, nb)) / 8.0)   # variabilité individuelle intégrée
    return d, sc, cuts


def enc_ll(th):
    d, sc, cuts = enc_terms(th)
    return w * jnp.take_along_axis(ord_logp(d, sc, cuts), y[:, None], axis=1)[:, 0]


def neg_logpost(th):
    s, g, lk, a0, b, bw, bt, cuts = unpack(th)
    mu = a0 + b * lnm_j + Wm_j @ bw
    lp = -0.5 * jnp.sum(((s - mu) / TAU) ** 2)
    lp += -0.5 * jnp.sum(((g - 1.0) / 0.25) ** 2) - 0.5 * ((lk - math.log(2.0)) / 0.5) ** 2
    lp += -0.5 * (a0 / 1.5) ** 2 - 0.5 * ((b - 1.5) / 0.25) ** 2
    lp += -0.5 * jnp.sum(((bw - jnp.array([0. if x in ("mains", "predateur") else .5 for x in WEAP])) / 0.7) ** 2)
    lp += -0.5 * jnp.sum(((bt - jnp.array([TAG_PRIOR[t][0] for t in TAGS])) / jnp.array([TAG_PRIOR[t][1] for t in TAGS])) ** 2)
    a = th[o_c:o_c + 3]
    lp += -0.5 * jnp.sum(((a - jnp.array([math.log(.4), 0., math.log(1.2)])) / .5) ** 2)
    return -(lp + jnp.sum(enc_ll(th)))


f_val = jax.jit(neg_logpost); f_grad = jax.jit(jax.grad(neg_logpost))
x0 = np.zeros(P); x0[o_g:o_g + 3] = 1.0; x0[o_k] = math.log(2.); x0[o_b] = 1.5
x0[:NSP] = 1.5 * lnm; x0[o_t:o_t + NT] = [TAG_PRIOR[t][0] for t in TAGS]; x0[o_c:o_c + 3] = [math.log(.4), 0., math.log(1.2)]
opt = dict(maxiter=50000, maxfun=100000, ftol=1e-14, gtol=1e-8)
res = minimize(lambda v: float(f_val(v)), x0, jac=lambda v: np.asarray(f_grad(v)), method="L-BFGS-B", options=opt)
for _ in range(4):
    if float(np.abs(np.asarray(f_grad(res.x))).max()) < 1e-4:
        break
    res = minimize(lambda v: float(f_val(v)), res.x, jac=lambda v: np.asarray(f_grad(v)), method="L-BFGS-B", options=opt)
th = res.x; gmax = float(np.abs(np.asarray(f_grad(th))).max())
H = np.asarray(jax.jit(jax.hessian(neg_logpost))(th)); H = .5 * (H + H.T) + 1e-8 * np.eye(P)
cov = np.linalg.inv(H); sd = np.sqrt(np.diag(cov))
s_, g_, lk_, a0_, b_, bw_, bt_, cuts_ = [np.asarray(v) for v in unpack(jnp.array(th))]
print("MAP", round(res.fun, 2), "max|grad|", gmax, "rencontres", NE, "γ", np.round(g_, 2), "κ", round(math.exp(lk_), 2), "b", round(float(b_), 2))

# ---- explications : influence de chaque rencontre sur chaque espèce (un pas de Newton)
G = np.asarray(jax.jacrev(enc_ll)(jnp.array(th)))   # NE x P
EF = G @ cov[:, :NSP]
d_, sc_, _ = enc_terms(jnp.array(th)); probs = np.exp(np.asarray(ord_logp(d_, sc_, jnp.array(cuts_))))

# ---- sortie : moyenne et facteur de Cholesky des paramètres utiles à la simulation dans la page
keep = list(range(NSP)) + [o_g, o_g + 1, o_g + 2, o_k, o_b]
Ck = cov[np.ix_(keep, keep)]; L = np.linalg.cholesky(Ck + 1e-10 * np.eye(len(keep)))
rows = [r for r in ENC if r["a"] in IX and r["b"] in IX]
out = dict(
    rel_h=[(float(s_[i] - s_[IX['humain']]), float(math.sqrt(max(cov[i, i] + cov[IX['humain'], IX['humain']] - 2 * cov[i, IX['humain']], 1e-9)))) for i in range(NSP)],
    species=[dict(id=s, name=SPECIES[s][0], pl=PLURAL.get(s, SPECIES[s][0]), sg=SPECIES[s][0].split(' (')[0].lower().replace('du nil', 'du Nil').replace("d'amérique", "d'Amérique").replace("d'afrique", "d'Afrique"), fam=SPECIES[s][1], mass=SPECIES[s][2], m5=SPECIES[s][3], m95=SPECIES[s][4],
                  weapons=SPECIES[s][5], social=SPECIES[s][6], s=round(float(s_[i]), 4), sd=round(float(sd[i]), 4),
                  prior=round(float(a0_ + b_ * lnm[i] + Wm[i] @ bw_), 3), rel=round(float(s_[i] - s_[IX['humain']]), 3), rel_sd=round(float(math.sqrt(max(cov[i, i] + cov[IX['humain'], IX['humain']] - 2 * cov[i, IX['humain']], 1e-9))), 3), sdlnm=round(float(sdlnm[i]), 4),
                  n_enc=int(sum(1 for r in rows if s in (r["a"], r["b"]))), n_tot=int(sum(r["count"] for r in rows if s in (r["a"], r["b"]))),
                  why=[dict(e=int(j), v=round(float(EF[j, i]), 3)) for j in np.argsort(-np.abs(EF[:, i]))[:8] if abs(EF[j, i]) >= .02])
             for i, s in enumerate(SP)],
    encounters=[dict(a=r["a"], na=r["na"], b=r["b"], nb=r["nb"], res=r["res"], m=r["m"], ta=r["ta"], tb=r["tb"], count=r["count"], poids=r["poids"],
                     qual=r["qual"], src=r["src"], note=r["note"], lieu=r.get("lieu", ""), annee=r.get("annee"),
                     p_a=round(float(probs[j, 4:].sum()), 3), surprise=round(float(-math.log(probs[j, int(y[j])])), 3))
                for j, r in enumerate(rows)],
    social=SOC, gamma=[round(float(v), 4) for v in g_], kappa=round(math.exp(float(lk_)), 4), b=round(float(b_), 4), resid=RESID,
    cuts=[round(float(v), 4) for v in cuts_], weapons=dict(zip(WEAP, [round(float(v), 3) for v in bw_])),
    tags={t: dict(beta=round(float(bt_[i]), 3), sd=round(float(sd[o_t + i]), 3)) for i, t in enumerate(TAGS)},
    mean=[round(float(th[k]), 5) for k in keep], chol=[[round(float(v), 6) for v in row] for row in L],
    corrections=[dict(rule=k, n=v) for k, v in CORR_LOG.items()],
    meta=dict(n_rows=len(rows), n_enc=int(sum(r["count"] for r in rows)), eps=EPS, count_cap=COUNT_CAP, converged=gmax < 1e-2),
)
json.dump(out, open(os.path.join(HERE, "animaux_out.json"), "w"), ensure_ascii=False)


def p1v1(a, b, n_a=1, n_b=1, draws=20000):
    """Probabilité de victoire de n_a individus de a contre n_b de b, combat neutre (paramètres + individus + hasard)."""
    rng = np.random.default_rng(0); z = rng.standard_normal((draws, len(keep))) @ L.T + np.array(out["mean"])
    sA, sB = z[:, IX[a]], z[:, IX[b]]; gg = z[:, NSP:NSP + 3]; kk = np.exp(z[:, NSP + 3]); bb = z[:, NSP + 4]
    def T(sx, i, n, j, gcol):
        C = 1 + kk * math.sqrt(mass[j] / mass[i]); ne = np.log1p(n / C) / np.log1p(1 / C); return sx + gcol * math.log(1) + gg[:, socx[i]] * np.log(ne)
    d = T(sA, IX[a], n_a, IX[b], 0) - T(sB, IX[b], n_b, IX[a], 0)
    d += rng.standard_normal(draws) * np.sqrt(((bb * sdlnm[IX[a]]) ** 2 + RESID ** 2) / n_a + ((bb * sdlnm[IX[b]]) ** 2 + RESID ** 2) / n_b)
    pa = 1 / (1 + np.exp(-(d - cuts_[3]))); pb = 1 / (1 + np.exp(d + cuts_[3]))
    return round(float(pa.mean()), 3), round(float(1 - pa.mean() - pb.mean()), 3), round(float(pb.mean()), 3)


if __name__ == "__main__":
    for s in sorted(SP, key=lambda s: -s_[IX[s]]):
        print(f"{SPECIES[s][0]:32s} s={s_[IX[s]]:6.2f} ±{sd[IX[s]]:.2f}  a priori {a0_ + b_ * lnm[IX[s]] + Wm[IX[s]] @ bw_:6.2f}  rencontres {sum(1 for r in rows if s in (r['a'], r['b']))}")
    print("tags", {t: round(float(bt_[i]), 2) for i, t in enumerate(TAGS)}, "armes", out["weapons"])
    for q in [("lion", "tigre"), ("ours_brun", "tigre"), ("ours_brun", "lion"), ("gorille", "humain"), ("chimpanze", "humain"),
              ("loup", "humain"), ("ours_brun", "humain"), ("orque", "requin_blanc"), ("hyene", "lion"), ("jaguar", "leopard")]:
        print(q, p1v1(*q))
