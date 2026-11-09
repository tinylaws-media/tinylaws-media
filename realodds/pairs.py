import json, math, sys, numpy as np
d = json.load(open(sys.argv[1])); c1 = d['cuts'][3]
def g(c, a):
    s = [x for x in d['chars'][c]['series'] if x['arc'] == a]
    return s[0] if s else None
for q in sys.argv[2:]:
    a, ka, b, kb = q.split(':')
    A, B = g(a, ka), g(b, kb)
    if not A or not B: print(q, 'missing'); continue
    z = np.random.default_rng(0).normal(A['mean'] - B['mean'], math.hypot(A['sd'], B['sd']), 100000)
    pa = (1 - 1 / (1 + np.exp(-(c1 - z)))).mean(); pb = (1 / (1 + np.exp(c1 + z))).mean()
    print(f"{a}({ka}) {A['mean']:.1f} vs {b}({kb}) {B['mean']:.1f}: {pa:.0%} / nul {1-pa-pb:.0%} / {pb:.0%}")
