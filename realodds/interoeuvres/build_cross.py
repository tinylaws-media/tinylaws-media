"""Construit la page « Inter-œuvres » (interoeuvres/real-odds-interoeuvres.html) à partir de cross_out.json et des modèles."""
import json, os, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
X = json.load(open(os.path.join(HERE, "cross_out.json")))
PATHS = {"naruto": ".", "onepiece": "verses/onepiece", "dragonball": "verses/dragonball", "jujutsukaisen": "verses/jujutsukaisen"}
cov = np.array(X["cov"]); L = np.linalg.cholesky(cov + 1e-12 * np.eye(len(cov)))
data = dict(theta=X["theta"], L=L.round(6).tolist(), sigma=X["sigma"], humain=X["humain"], feats=X["feats"], verses=[])
for v in X["verses"]:
    mo = json.load(open(os.path.join(ROOT, PATHS[v["id"]], "model_out.json")))
    chars = {c: dict(n=ch["name"], g=ch["generic"], s=[[s["arc"], round(s["mean"], 3), round(s["sd"], 3)] for s in ch["series"]])
             for c, ch in mo["chars"].items() if ch["series"]}
    fights = [[f["arc"], f["a"], f["b"], f["res"]] for f in mo["fights"]]
    data["verses"].append(dict(id=v["id"], label=v["label"], tier=v["tier"], c1=v["cuts"][3], arcs=[[a["id"], a["name"]] for a in mo["arcs"]],
                               chars=chars, fights=fights))
T = open(os.path.join(ROOT, "template.html")).read()
head = T[:T.index("</style>")] + """
.ladder svg{min-width:640px}
.ladder .dot{cursor:pointer}
.ladder text{font:11px var(--f-body);fill:var(--ink2)}
.ladder .hl text{fill:var(--ink);font-weight:600}
.feat{display:grid;grid-template-columns:1fr auto;gap:2px 10px;padding:8px 0;border-bottom:1px solid var(--rule);font-size:14px}
.feat .q{font:600 13px var(--f-mono);white-space:nowrap}
.feat .c{grid-column:1/-1;color:var(--ink3);font-size:12.5px}
.warn{color:var(--a);font-weight:600}
</style>"""
head = head.replace("<title>Naruto : The Real Odds</title>", "<title>Inter-œuvres : The Real Odds</title>")
body = open(os.path.join(HERE, "body_cross.html")).read()
page = head + "\n" + body.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
open(os.path.join(HERE, "real-odds-interoeuvres.html"), "w").write(page)
print("ok", len(page) // 1024, "Ko")
