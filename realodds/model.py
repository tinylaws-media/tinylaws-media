"""The Real Odds model (v3): dynamic Bayesian Bradley-Terry with ordinal margins, databook observations,
Edo Tensei / revival handling, and per-estimate explanations. MAP + Laplace (JAX).

Usage: python3 model.py [verse_dir]   (default: this folder, i.e. Naruto)
The verse folder holds data.py (ARCS, CHARS, F, GENERIC, JUMPS, optional REVIVE, EXTRA_TAGS, BOOK_TIMES)
and optionally databook.py (DATABOOK). Output: <verse_dir>/model_out.json
"""
import importlib.util
import json
import math
import os
import sys

import jax
import jax.numpy as jnp
import numpy as np
from scipy.optimize import minimize

jax.config.update("jax_enable_x64", True)
HERE = os.path.dirname(os.path.abspath(__file__))
VDIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]) else HERE


def load(name):
    p = os.path.join(VDIR, name + ".py")
    if not os.path.exists(p):
        return None
    spec = importlib.util.spec_from_file_location(name + "_" + str(abs(hash(VDIR))), p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


D = load("data")
ARCS, CHARS, F, GENERIC, JUMPS = D.ARCS, D.CHARS, D.F, D.GENERIC, D.JUMPS
REVIVE = getattr(D, "REVIVE", {})
DBM = load("databook")
DATABOOK = DBM.DATABOOK if DBM else {}
BOOK_TIMES = getattr(D, "BOOK_TIMES", {1: 12.3, 2: 12.9, 3: 16.5})
DB_TIME_OVERRIDE = getattr(D, "DB_TIME_OVERRIDE", {})

TIER = 1.0       # one tier = 1 logit
PRIOR_SD = 1.5   # sd of the status prior at a character's first node
Q = 0.5          # random-walk sd per sqrt(year)
DT_CAP = 12.0
DB_SD = 1.2      # how far one databook rating may sit from the true strength
TAG_PRIOR = {"malade": (-1.0, .7), "epuise": (-0.8, .7), "retenue": (-1.0, .7), "protege": (-0.7, .7),
             "surprise": (0.7, .7), "prepa": (0.7, .7), "boost": (1.0, .7), "edo": (0.4, .7), "edo_ctrl": (-0.5, .7),
             "contre": (0.7, .7), "age": (-0.7, .7)}
TAG_PRIOR.update(getattr(D, "EXTRA_TAGS", {}))
TAGS = list(TAG_PRIOR)

for f in F:
    for c in f["a"] + f["b"]:
        assert c in CHARS, c
    for t in f["ta"] + f["tb"]:
        assert t in TAG_PRIOR, t


def eff_time(c, t):
    """After death, an Edo Tensei body keeps the strength of edo_ref; after a revival, time runs again."""
    death, edo = CHARS[c][3], CHARS[c][4]
    rv = REVIVE.get(c)
    if death is not None and t > death + 1e-9:
        if rv is not None and t >= rv - 1e-9:
            return t
        if edo is not None:
            return edo
    return t


# ---- nodes
first_t, last_t, edo_arcs = {}, {}, {}
for f in F:
    for c in f["a"] + f["b"]:
        et = eff_time(c, f["t"])
        if et != f["t"]:
            edo_arcs.setdefault(c, set()).add(f["arc"])
        else:
            first_t[c] = min(first_t.get(c, 1e9), f["t"])
            last_t[c] = max(last_t.get(c, -1e9), f["t"])

node_times = {c: set() for c in CHARS}
for f in F:
    for c in f["a"] + f["b"]:
        node_times[c].add(round(eff_time(c, f["t"]), 4))

db_obs = []  # (char, time, book, total)
for c, rows in DATABOOK.items():
    if c not in CHARS or c not in first_t:
        continue
    for book, total, _ in rows:
        t = DB_TIME_OVERRIDE.get((c, book), BOOK_TIMES[book])
        death = CHARS[c][3]
        if death is not None and t > death and REVIVE.get(c) is None:
            t = death
        t = round(t, 4)
        node_times[c].add(t)
        db_obs.append((c, t, book, total))

query = {}
for c in CHARS:
    if c not in first_t:
        continue
    death = CHARS[c][3]
    rv = REVIVE.get(c)
    end = death if death is not None else max(last_t[c], 40)
    for k, _, t in ARCS:
        alive = first_t[c] - 0.3 <= t <= end + 1e-9
        revived = rv is not None and rv - 0.05 <= t <= last_t[c] + 0.3
        if alive or revived or k in edo_arcs.get(c, ()):
            tt = round(eff_time(c, t), 4)
            if tt < first_t[c] - 0.3:
                continue
            query[(c, k)] = tt
            node_times[c].add(tt)

index, nodes = {}, []
for c in CHARS:
    for t in sorted(node_times[c]):
        index[(c, t)] = len(nodes)
        nodes.append((c, t))
N = len(nodes)


def jump_terms(c, t0, t1):
    mu, var = 0.0, 0.0
    for jc, jt, jm, js, _ in JUMPS:
        if jc == c and t0 < jt <= t1:
            mu += jm * TIER
            var += (1.5 * js) ** 2
    return mu, var


prior_first, incr = [], []
for c in CHARS:
    ts = sorted(node_times[c])
    if not ts:
        continue
    prior_first.append((index[(c, ts[0])], CHARS[c][2] * TIER))
    for t0, t1 in zip(ts, ts[1:]):
        jm, jv = jump_terms(c, t0, t1)
        incr.append((index[(c, t0)], index[(c, t1)], jm, math.sqrt(Q * Q * min(t1 - t0, DT_CAP) + jv)))
pf_i = np.array([i for i, _ in prior_first]); pf_m = np.array([m for _, m in prior_first])
in_a = np.array([a for a, _, _, _ in incr]); in_b = np.array([b for _, b, _, _ in incr])
in_m = np.array([m for _, _, m, _ in incr]); in_s = np.array([s for _, _, _, s in incr])
db_i = np.array([index[(c, t)] for c, t, _, _ in db_obs], dtype=int)
db_x = np.array([(tot - 30.0) / 5.0 for _, _, _, tot in db_obs])   # databook total, centred at 30, per 5 points

# ---- fights
MAXT = max(len(f["a"]) for f in F + [dict(a=[1], b=[1])])
MAXT = max(MAXT, max(len(f["b"]) for f in F))
fa_idx, fa_mask, fb_idx, fb_mask, ya, wts, tga, tgb = [], [], [], [], [], [], [], []
for f in F:
    ia = [index[(c, round(eff_time(c, f["t"]), 4))] for c in f["a"]]
    ib = [index[(c, round(eff_time(c, f["t"]), 4))] for c in f["b"]]
    fa_idx.append(ia + [0] * (MAXT - len(ia))); fa_mask.append([1] * len(ia) + [0] * (MAXT - len(ia)))
    fb_idx.append(ib + [0] * (MAXT - len(ib))); fb_mask.append([1] * len(ib) + [0] * (MAXT - len(ib)))
    ya.append(3 if f["res"] == "D" else 3 + f["m"])
    w = 1.0
    if "i" in f["flags"]:
        w *= 0.5
    if "?" in f["flags"]:
        w *= 0.5
    if len(f["a"]) > 1 or len(f["b"]) > 1:
        w *= 0.75
    wts.append(w)
    tga.append([1.0 if t in f["ta"] else 0.0 for t in TAGS])
    tgb.append([1.0 if t in f["tb"] else 0.0 for t in TAGS])
fa_idx, fb_idx = jnp.array(fa_idx), jnp.array(fb_idx)
fa_mask, fb_mask = jnp.array(fa_mask, float), jnp.array(fb_mask, float)
ya, wts = jnp.array(ya), jnp.array(wts)
tga, tgb = jnp.array(tga), jnp.array(tgb)
tag_mu = jnp.array([TAG_PRIOR[t][0] for t in TAGS]); tag_sd = jnp.array([TAG_PRIOR[t][1] for t in TAGS])
NT = len(TAGS)
P = N + NT + 3 + 3   # strengths, tag effects, 3 cutpoints, databook intercept + slope + curvature


def unpack(th):
    s = th[:N]; beta = th[N:N + NT]; a = th[N + NT:N + NT + 3]; db = th[N + NT + 3:]
    c1 = jnp.exp(a[0]); c2 = c1 + jnp.exp(a[1]); c3 = c2 + jnp.exp(a[2])
    return s, beta, jnp.array([-c3, -c2, -c1, c1, c2, c3]), db


def team(s, idx, mask):
    return jax.scipy.special.logsumexp(jnp.where(mask > 0, s[idx], -1e9), axis=1)


def diff(s, beta):
    return team(s, fa_idx, fa_mask) - team(s, fb_idx, fb_mask) + tga @ beta - tgb @ beta


def cat_logp(d, cuts):
    cdf = jax.nn.sigmoid(cuts[None, :] - d[:, None])
    cdf = jnp.concatenate([jnp.zeros((d.shape[0], 1)), cdf, jnp.ones((d.shape[0], 1))], axis=1)
    return jnp.log(jnp.clip(cdf[:, 1:] - cdf[:, :-1], 1e-12, 1.0))


def fight_ll(th):
    s, beta, cuts, _ = unpack(th)
    return wts * jnp.take_along_axis(cat_logp(diff(s, beta), cuts), ya[:, None], axis=1)[:, 0]


def db_ll(th):
    s, _, _, db = unpack(th)
    return -0.5 * ((s[db_i] - (db[0] + db[1] * db_x + db[2] * jnp.maximum(db_x, 0.0) ** 2)) / DB_SD) ** 2


def neg_logpost(th):
    s, beta, cuts, db = unpack(th)
    lp = -0.5 * jnp.sum(((s[pf_i] - pf_m) / PRIOR_SD) ** 2)
    lp += -0.5 * jnp.sum(((s[in_b] - s[in_a] - in_m) / in_s) ** 2)
    lp += -0.5 * jnp.sum(((beta - tag_mu) / tag_sd) ** 2)
    a = th[N + NT:N + NT + 3]
    lp += -0.5 * jnp.sum(((a - jnp.array([math.log(0.4), math.log(1.0), math.log(1.2)])) / 0.5) ** 2)
    lp += -0.5 * (((db[0] - 5.0) / 2.0) ** 2 + ((db[1] - 1.0) / 0.7) ** 2 + ((db[2] - 0.5) / 0.5) ** 2)
    lp += jnp.sum(fight_ll(th)) + jnp.sum(db_ll(th))
    return -lp


f_val = jax.jit(neg_logpost); f_grad = jax.jit(jax.grad(neg_logpost))
x0 = np.zeros(P)
for k, (c, t) in enumerate(nodes):
    x0[k] = CHARS[c][2] * TIER
x0[N:N + NT] = [TAG_PRIOR[t][0] for t in TAGS]
x0[N + NT:N + NT + 3] = [math.log(0.4), 0.0, math.log(1.2)]
x0[N + NT + 3:] = [5.0, 1.0, 0.5]
opt = dict(maxiter=50000, maxfun=100000, ftol=1e-13, gtol=1e-7)
res = minimize(lambda x: float(f_val(x)), x0, jac=lambda x: np.asarray(f_grad(x)), method="L-BFGS-B", options=opt)
for _ in range(4):
    if float(np.abs(np.asarray(f_grad(res.x))).max()) < 1e-3:
        break
    res = minimize(lambda x: float(f_val(x)), res.x, jac=lambda x: np.asarray(f_grad(x)), method="L-BFGS-B", options=opt)
gmax = float(np.abs(np.asarray(f_grad(res.x))).max())
print("MAP", res.fun, "max|grad|", gmax, "params", P, "fights", len(F), "databook obs", len(db_obs))
th = res.x
H = np.asarray(jax.jit(jax.hessian(neg_logpost))(th))
H = 0.5 * (H + H.T) + 1e-6 * np.eye(P)
cov = np.linalg.inv(H)
sd = np.sqrt(np.clip(np.diag(cov), 1e-12, None))
s_map, beta_map, cuts_map, db_map = [np.asarray(x) for x in unpack(jnp.array(th))]

prior_var = np.zeros(N)
for c in CHARS:
    ts = sorted(node_times[c]); v = PRIOR_SD ** 2
    for i, t in enumerate(ts):
        if i > 0:
            jm, jv = jump_terms(c, ts[i - 1], t)
            v += Q * Q * min(t - ts[i - 1], DT_CAP) + jv
        prior_var[index[(c, t)]] = v

# ---- explanations: effect of each piece of evidence on each query node (one Newton step: Cov @ grad)
Gf = np.asarray(jax.jacrev(fight_ll)(jnp.array(th)))          # fights x P
Gd = np.asarray(jax.jacrev(db_ll)(jnp.array(th))) if len(db_obs) else np.zeros((0, P))
qnodes = sorted(set(index[(c, t)] for (c, k), t in query.items()))
Cq = cov[:, qnodes]
Ef = Gf @ Cq; Ed = Gd @ Cq                                       # effect on s(node)
qpos = {n: i for i, n in enumerate(qnodes)}

d_map = np.asarray(diff(jnp.array(s_map), jnp.array(beta_map)))
probs = np.exp(np.asarray(cat_logp(jnp.array(d_map), jnp.array(cuts_map))))

out_chars = {}
for c, (name, team_, tier, death, edo) in CHARS.items():
    if c not in first_t:
        continue
    series = []
    for k, label, t in ARCS:
        if (c, k) not in query:
            continue
        i = index[(c, query[(c, k)])]; q = qpos[i]
        why = [dict(f=int(j), v=round(float(Ef[j, q]), 3)) for j in np.argsort(-np.abs(Ef[:, q]))[:8] if abs(Ef[j, q]) >= 0.03]
        dbw = [dict(book=db_obs[j][2], total=db_obs[j][3], who=db_obs[j][0], v=round(float(Ed[j, q]), 3))
               for j in np.argsort(-np.abs(Ed[:, q]))[:3] if abs(Ed[j, q]) >= 0.03] if len(db_obs) else []
        series.append(dict(arc=k, mean=round(float(s_map[i]), 3), sd=round(float(sd[i]), 3),
                           info=round(float(max(0.0, 1 - sd[i] ** 2 / prior_var[i])), 3),
                           edo=bool(k in edo_arcs.get(c, ())) and query[(c, k)] != t, why=why, db=dbw))
    nf = sum(1 for f in F if c in f["a"] + f["b"])
    out_chars[c] = dict(name=name, team=team_, generic=c in GENERIC, fights=nf, tier=tier,
                        databook=[dict(book=b, total=tot) for b, tot, _ in DATABOOK.get(c, [])], series=series)

out_fights = []
for j, f in enumerate(F):
    y = int(ya[j])
    out_fights.append(dict(t=f["t"], arc=f["arc"], a=f["a"], b=f["b"], res=f["res"], m=f["m"], ta=f["ta"], tb=f["tb"],
                           note=f["note"], flags=f["flags"], w=round(float(wts[j]), 3), p_a=round(float(probs[j, 4:].sum()), 3),
                           p_d=round(float(probs[j, 3]), 3), surprise=round(float(-math.log(probs[j, y])), 3)))

out = dict(
    arcs=[dict(id=k, name=n, t=t) for k, n, t in ARCS], chars=out_chars, fights=out_fights,
    tags={t: dict(beta=round(float(beta_map[i]), 3), sd=round(float(sd[N + i]), 3)) for i, t in enumerate(TAGS)},
    cuts=[round(float(x), 3) for x in cuts_map],
    databook=dict(intercept=round(float(db_map[0]), 3), slope_per5=round(float(db_map[1]), 3), curve=round(float(db_map[2]), 3), n=len(db_obs)),
    jumps=[dict(c=c, t=t, label=l) for c, t, m, s, l in JUMPS],
    meta=dict(n_fights=len(F), n_chars=len([c for c in out_chars if not out_chars[c]["generic"]]), q=Q, prior_sd=PRIOR_SD,
              converged=gmax < 1e-2),
)
json.dump(out, open(os.path.join(VDIR, "model_out.json"), "w"), ensure_ascii=False)


def P_win(a, ka, b, kb):
    ia, ib = index[(a, query[(a, ka)])], index[(b, query[(b, kb)])]
    z = np.random.default_rng(0).normal(s_map[ia] - s_map[ib], math.sqrt(cov[ia, ia] + cov[ib, ib] - 2 * cov[ia, ib]), 50000)
    return round(float(np.mean(1 - 1 / (1 + np.exp(-(cuts_map[3] - z))))), 3)


print("tags", {t: round(float(beta_map[i]), 2) for i, t in enumerate(TAGS)}, "cuts", np.round(cuts_map, 2),
      "databook", np.round(db_map, 2))
for q in getattr(D, "CHECKS", []):
    try:
        print(q, P_win(*q))
    except KeyError as e:
        print(q, "missing", e)
