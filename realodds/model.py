"""Dynamic Bayesian Bradley-Terry with ordinal margins. MAP + Laplace (JAX), exports JSON for the explorer."""
import json
import math
import sys

import jax
import jax.numpy as jnp
import numpy as np
from scipy.optimize import minimize

jax.config.update("jax_enable_x64", True)
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from data import ARCS, CHARS, F, GENERIC, JUMPS  # noqa: E402

TIER = 1.0       # one tier = 1 logit
PRIOR_SD = 1.5   # sd of the status prior at a character's first node
Q = 0.5        # random-walk sd per sqrt(year)
DT_CAP = 12.0
TAG_PRIOR = {"malade": -1.0, "epuise": -0.8, "retenue": -1.0, "protege": -0.7, "surprise": 0.7, "prepa": 0.7,
             "boost": 1.0, "edo": 0.4, "edo_ctrl": -0.5, "contre": 0.7, "age": -0.7}
TAGS = list(TAG_PRIOR)

for f in F:
    for c in f["a"] + f["b"]:
        assert c in CHARS, c


def eff_time(c, t):
    """Edo Tensei bodies keep the strength of their edo_ref time."""
    name, team, tier, death, edo = CHARS[c]
    if death is not None and t > death + 1e-9 and edo is not None:
        return edo
    return t


def arc_t(a):
    return dict((k, t) for k, _, t in ARCS)[a]


# ---- nodes: per character, sorted distinct times (fight times + arc query times inside the alive span)
first_t = {}
last_t = {}
edo_arcs = {}
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
query = {}  # (c, arc) -> time used
for c in CHARS:
    if c not in first_t:
        continue
    death = CHARS[c][3]
    end = death if death is not None else max(last_t[c], 40)
    for k, _, t in ARCS:
        if first_t[c] - 0.3 <= t <= end + 1e-9 or (k in edo_arcs.get(c, ())):
            tt = round(eff_time(c, t), 4)
            if tt < first_t[c] - 0.3:
                continue
            query[(c, k)] = tt
            node_times[c].add(tt)

index = {}
nodes = []
for c in CHARS:
    for t in sorted(node_times[c]):
        index[(c, t)] = len(nodes)
        nodes.append((c, t))
N = len(nodes)

# prior structure: first node ~ N(tier, PRIOR_SD); increments ~ N(sum jumps, Q^2 dt + sum jump sd^2)
prior_first = []
incr = []  # (i_prev, i_next, mean, sd)
for c in CHARS:
    ts = sorted(node_times[c])
    if not ts:
        continue
    prior_first.append((index[(c, ts[0])], CHARS[c][2] * TIER))
    for t0, t1 in zip(ts, ts[1:]):
        mu, var = 0.0, Q * Q * min(t1 - t0, DT_CAP)
        for jc, jt, jm, js, _ in JUMPS:
            if jc == c and t0 < jt <= t1:
                mu += jm * TIER
                var += (1.5 * js) ** 2
        incr.append((index[(c, t0)], index[(c, t1)], mu, math.sqrt(var)))
pf_i = np.array([i for i, _ in prior_first])
pf_m = np.array([m for _, m in prior_first])
in_a = np.array([a for a, _, _, _ in incr])
in_b = np.array([b for _, b, _, _ in incr])
in_m = np.array([m for _, _, m, _ in incr])
in_s = np.array([s for _, _, _, s in incr])

# fights
MAXT = 7
fa_idx, fa_mask, fb_idx, fb_mask, ya, wts, tga, tgb = [], [], [], [], [], [], [], []
for f in F:
    ia = [index[(c, round(eff_time(c, f["t"]), 4))] for c in f["a"]]
    ib = [index[(c, round(eff_time(c, f["t"]), 4))] for c in f["b"]]
    fa_idx.append(ia + [0] * (MAXT - len(ia)))
    fa_mask.append([1] * len(ia) + [0] * (MAXT - len(ia)))
    fb_idx.append(ib + [0] * (MAXT - len(ib)))
    fb_mask.append([1] * len(ib) + [0] * (MAXT - len(ib)))
    y = 3 if f["res"] == "D" else 3 + f["m"]          # categories 0..6, 3 = draw, 4..6 = A wins
    ya.append(y)
    w = 1.0
    if "i" in f["flags"]:
        w *= 0.5
    if "?" in f["flags"]:
        w *= 0.5
    if len(f["a"]) > 1 or len(f["b"]) > 1:
        w *= 0.75   # team fights: shared credit, counted less
    wts.append(w)
    tga.append([1.0 if t in f["ta"] else 0.0 for t in TAGS])
    tgb.append([1.0 if t in f["tb"] else 0.0 for t in TAGS])
fa_idx, fb_idx = jnp.array(fa_idx), jnp.array(fb_idx)
fa_mask, fb_mask = jnp.array(fa_mask, float), jnp.array(fb_mask, float)
ya, wts = jnp.array(ya), jnp.array(wts)
tga, tgb = jnp.array(tga), jnp.array(tgb)
tag_mu = jnp.array([TAG_PRIOR[t] for t in TAGS])
NT = len(TAGS)
P = N + NT + 3


def unpack(th):
    s = th[:N]
    beta = th[N:N + NT]
    a = th[N + NT:]
    c1 = jnp.exp(a[0])
    c2 = c1 + jnp.exp(a[1])
    c3 = c2 + jnp.exp(a[2])
    return s, beta, jnp.array([-c3, -c2, -c1, c1, c2, c3])


def team(s, idx, mask):
    v = jnp.where(mask > 0, s[idx], -1e9)
    return jax.scipy.special.logsumexp(v, axis=1)


def diff(s, beta):
    return team(s, fa_idx, fa_mask) - team(s, fb_idx, fb_mask) + tga @ beta - tgb @ beta


def cat_logp(d, cuts):
    cdf = jax.nn.sigmoid(cuts[None, :] - d[:, None])            # P(y <= j), j = 0..5
    cdf = jnp.concatenate([jnp.zeros((d.shape[0], 1)), cdf, jnp.ones((d.shape[0], 1))], axis=1)
    p = jnp.clip(cdf[:, 1:] - cdf[:, :-1], 1e-12, 1.0)        # 7 categories
    return jnp.log(p)


def neg_logpost(th):
    s, beta, cuts = unpack(th)
    lp = -0.5 * jnp.sum(((s[pf_i] - pf_m) / PRIOR_SD) ** 2)
    lp += -0.5 * jnp.sum(((s[in_b] - s[in_a] - in_m) / in_s) ** 2)
    lp += -0.5 * jnp.sum(((beta - tag_mu) / 0.7) ** 2)
    a = th[N + NT:]
    lp += -0.5 * jnp.sum(((a - jnp.array([math.log(0.4), math.log(1.0), math.log(1.2)])) / 0.5) ** 2)
    d = diff(s, beta)
    lp += jnp.sum(wts * jnp.take_along_axis(cat_logp(d, cuts), ya[:, None], axis=1)[:, 0])
    return -lp


f_val = jax.jit(neg_logpost)
f_grad = jax.jit(jax.grad(neg_logpost))
x0 = np.zeros(P)
for i, m in prior_first:
    pass
# initialise each character's nodes at its tier
tier_of = {c: CHARS[c][2] for c in CHARS}
for k, (c, t) in enumerate(nodes):
    x0[k] = tier_of[c] * TIER
x0[N + NT:] = [math.log(0.4), 0.0, math.log(1.2)]
x0[N:N + NT] = [TAG_PRIOR[t] for t in TAGS]
res = minimize(lambda x: float(f_val(x)), x0, jac=lambda x: np.asarray(f_grad(x)), method="L-BFGS-B",
               options=dict(maxiter=50000, maxfun=100000, ftol=1e-12, gtol=1e-6))
for _ in range(3):
    gnorm = float(np.abs(np.asarray(f_grad(res.x))).max())
    if gnorm < 1e-3: break
    res = minimize(lambda x: float(f_val(x)), res.x, jac=lambda x: np.asarray(f_grad(x)), method="L-BFGS-B", options=dict(maxiter=50000, maxfun=100000, ftol=1e-14, gtol=1e-7))
print("max |grad|", float(np.abs(np.asarray(f_grad(res.x))).max()), res.message)
print("MAP", res.success, res.fun, "params", P, "fights", len(F))
th = res.x
H = np.asarray(jax.jit(jax.hessian(neg_logpost))(th))
H = 0.5 * (H + H.T) + 1e-6 * np.eye(P)
cov = np.linalg.inv(H)
sd = np.sqrt(np.clip(np.diag(cov), 1e-12, None))
s_map, beta_map, cuts_map = unpack(jnp.array(th))
s_map, beta_map, cuts_map = np.asarray(s_map), np.asarray(beta_map), np.asarray(cuts_map)

# prior variance at each node (for "share of info from fights")
prior_var = np.zeros(N)
for c in CHARS:
    ts = sorted(node_times[c])
    v = PRIOR_SD ** 2
    for i, t in enumerate(ts):
        if i > 0:
            t0 = ts[i - 1]
            v += Q * Q * min(t - t0, DT_CAP) + sum((1.5 * js) ** 2 for jc, jt, jm, js, _ in JUMPS if jc == c and t0 < jt <= t)
        prior_var[index[(c, t)]] = v

# per-fight surprise under MAP
d_map = np.asarray(diff(jnp.array(s_map), jnp.array(beta_map)))
lp = np.asarray(cat_logp(jnp.array(d_map), jnp.array(cuts_map)))
probs = np.exp(lp)

out_chars = {}
for c, (name, team_, tier, death, edo) in CHARS.items():
    if c not in first_t:
        continue
    series = []
    for k, label, t in ARCS:
        if (c, k) in query:
            i = index[(c, query[(c, k)])]
            series.append(dict(arc=k, mean=round(float(s_map[i]), 3), sd=round(float(sd[i]), 3),
                               info=round(float(max(0.0, 1 - sd[i] ** 2 / prior_var[i])), 3),
                               edo=bool(k in edo_arcs.get(c, ()))))
    nf = sum(1 for f in F if c in f["a"] + f["b"])
    out_chars[c] = dict(name=name, team=team_, generic=c in GENERIC, fights=nf, series=series)

out_fights = []
for j, f in enumerate(F):
    y = int(ya[j])
    pa = float(probs[j, 4:].sum())
    pd = float(probs[j, 3])
    out_fights.append(dict(t=f["t"], arc=f["arc"], a=f["a"], b=f["b"], res=f["res"], m=f["m"], ta=f["ta"], tb=f["tb"],
                           note=f["note"], flags=f["flags"], p_obs=round(float(probs[j, y]), 4),
                           p_a=round(pa, 3), p_d=round(pd, 3), surprise=round(float(-math.log(probs[j, y])), 3)))

out = dict(
    arcs=[dict(id=k, name=n, t=t) for k, n, t in ARCS],
    chars=out_chars,
    fights=out_fights,
    tags={t: dict(beta=round(float(beta_map[i]), 3), sd=round(float(sd[N + i]), 3)) for i, t in enumerate(TAGS)},
    cuts=[round(float(x), 3) for x in cuts_map],
    jumps=[dict(c=c, t=t, label=l) for c, t, m, s, l in JUMPS],
    meta=dict(n_fights=len(F), n_chars=len([c for c in out_chars if not out_chars[c]["generic"]]), q=Q, prior_sd=PRIOR_SD),
)
json.dump(out, open(__file__.rsplit("/", 1)[0] + "/model_out.json", "w"), ensure_ascii=False)

# ---- checks
def P_win(a, ka, b, kb):
    ia = index[(a, query[(a, ka)])]
    ib = index[(b, query[(b, kb)])]
    mu = s_map[ia] - s_map[ib]
    v = cov[ia, ia] + cov[ib, ib] - 2 * cov[ia, ib]
    z = np.random.default_rng(0).normal(mu, math.sqrt(v), 20000)
    cdf_draw_hi = 1 / (1 + np.exp(-(cuts_map[3] - z)))
    return float(np.mean(1 - cdf_draw_hi))


print("tags", {t: round(float(beta_map[i]), 2) for i, t in enumerate(TAGS)}, "cuts", np.round(cuts_map, 2))
for q in [("itachi", "itachi", "minato", "kyubi"), ("naruto", "final", "sasuke", "final"), ("madara", "guerre4b", "hashirama", "fondation"),
          ("gaara", "kazekage", "deidara", "kazekage"), ("kakashi", "pain", "itachi", "itachi"), ("naruto", "pain", "jiraiya", "itachi")]:
    print(q, round(P_win(*q), 3))
top = sorted(out_fights, key=lambda x: -x["surprise"])[:8]
for f in top:
    print("surprise", f["surprise"], f["a"], f["b"], f["res"], f["arc"])
