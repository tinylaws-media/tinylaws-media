"""Construit la page de l'explorateur animaux : styles communs de template.html + body_animaux.html + animaux_out.json."""
import os
H = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(H, "..", "template.html")).read()
head = T[:T.index("</style>") + len("</style>")].replace("<title>Naruto : The Real Odds</title>", "<title>Animaux : The Real Odds</title>")
body = open(os.path.join(H, "body_animaux.html")).read().replace("__DATA__", open(os.path.join(H, "animaux_out.json")).read().replace("</", "<\\/"))
open(os.path.join(H, "real-odds-animaux.html"), "w").write(head + "\n" + body)
print("built real-odds-animaux.html")
