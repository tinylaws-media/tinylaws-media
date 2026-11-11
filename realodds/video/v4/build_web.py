"""Spider web of every Naruto fight (character level) for the v4 video: layout + BFS hops from Itachi and Minato."""
import json, random, collections, networkx as nx
d = json.load(open('../../model_out.json'))
ch = d['chars']
G = nx.Graph()
for f in d['fights']:
    for a in f['a']:
        for b in f['b']:
            if a == b: continue
            if G.has_edge(a, b): G[a][b]['n'] += 1
            else: G.add_edge(a, b, n=1)
G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
fix = {'itachi': (-0.55, 0.05), 'minato': (0.55, 0.05)}
pos = nx.spring_layout(G, seed=7, k=0.32, iterations=400, pos={**{n: (random.Random(n).uniform(-1, 1), random.Random(n + 'y').uniform(-1, 1)) for n in G}, **fix}, fixed=list(fix))
import math
cx = sum(p[0] for p in pos.values()) / len(pos); cy = sum(p[1] for p in pos.values()) / len(pos)
order = sorted(pos, key=lambda n: math.hypot(pos[n][0] - cx, pos[n][1] - cy))
rk = {n: i for i, n in enumerate(order)}
P = {}
for n in pos:
    if n in fix: P[n] = (540 + fix[n][0] * 420, 930); continue
    an = math.atan2(pos[n][1] - cy, pos[n][0] - cx); r = 0.28 + 0.72 * math.sqrt((rk[n] + 1) / len(pos))
    P[n] = (540 + r * 470 * math.cos(an), 930 + r * 560 * math.sin(an))
def sx(n): return round(P[n][0])
def sy(n): return round(P[n][1])
hi = nx.single_source_shortest_path_length(G, 'itachi'); hm = nx.single_source_shortest_path_length(G, 'minato')
nodes = {n: [sx(n), sy(n), ch[n]['name'].split(' ')[0], hi.get(n, 9), hm.get(n, 9)] for n in G}
edges = [[u, v, e['n']] for u, v, e in G.edges(data=True)]
both = sum(1 for n in G if n in hi and n in hm)
print(len(nodes), 'nodes', len(edges), 'edges', 'max hops', max(hi.values()), max(hm.values()), 'both', both)
print('hop counts I', collections.Counter(hi.values()), 'M', collections.Counter(hm.values()))
json.dump(dict(nodes=nodes, edges=edges), open('web.json', 'w'), ensure_ascii=False)
