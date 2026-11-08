import runpy, math, numpy as np, jax, jax.numpy as jnp, json, sys
g = runpy.run_path("/home/claude/tinylaws-media/realodds/model.py")
a, ka, b, kb = sys.argv[1:5]
idx, query, cov, th, F = g["index"], g["query"], g["cov"], g["th"], g["F"]
ia, ib = idx[(a, query[(a, ka)])], idx[(b, query[(b, kb)])]
mu = th[ia] - th[ib]; v = cov[ia, ia] + cov[ib, ib] - 2 * cov[ia, ib]
c1 = float(np.asarray(g["unpack"](jnp.array(th))[2])[3])
z = np.random.default_rng(0).normal(mu, math.sqrt(v), 200000)
pa = 1 - 1 / (1 + np.exp(-(c1 - z))); pb = 1 / (1 + np.exp(-(-c1 - z)))
print(f"s_{a}={th[ia]:.2f}±{math.sqrt(cov[ia,ia]):.2f}  s_{b}={th[ib]:.2f}±{math.sqrt(cov[ib,ib]):.2f}  diff={mu:.2f}±{math.sqrt(v):.2f}")
print(f"P({a})={pa.mean():.3f} nul={1-pa.mean()-pb.mean():.3f} P({b})={pb.mean():.3f}  90%: {np.quantile(pa,.05):.2f}-{np.quantile(pa,.95):.2f}")
# influence of each fight on the difference: removing fight f moves theta by about -Cov @ grad_f
e = np.zeros(len(th)); e[ia] = 1; e[ib] = -1
ce = cov @ e
s, beta, cuts = g["unpack"](jnp.array(th))
def fight_ll(theta, j):
    s, beta, cuts = g["unpack"](theta)
    d = g["diff"](s, beta)
    return g["wts"][j] * g["cat_logp"](d, cuts)[j, g["ya"][j]]
gr = jax.jit(jax.grad(fight_ll), static_argnums=1)
infl = []
for j, f in enumerate(F):
    gj = np.asarray(gr(jnp.array(th), j))
    infl.append((float(ce @ gj), j))
infl.sort(key=lambda x: -abs(x[0]))
for val, j in infl[:14]:
    f = F[j]
    print(f"{val:+.2f}  {', '.join(f['a'])} vs {', '.join(f['b'])}  [{f['res']}{f['m'] if f['res']=='A' else ''}] {f['arc']} {f['note'][:60]}")
