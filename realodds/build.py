"""Build the explorer page of each verse from template.html + model_out.json."""
import re
import sys

T = open("template.html").read()
COMMON_NON_NARUTO = [
    (" Un corps d'Edo Tensei garde la force de la personne à sa mort.", ""),
    ("<p class=\"note\">Point creux : corps d\\'Edo Tensei (force figée à la mort).</p>", ""),
    ("de l'information vient des combats et du databook", "de l'information vient des combats"),
]
V = {
    "naruto": dict(out="real-odds-naruto.html", data="model_out.json", rep=[]),
    "onepiece": dict(out="verses/onepiece/real-odds-onepiece.html", data="verses/onepiece/model_out.json", rep=COMMON_NON_NARUTO + [
        ("<title>Naruto : The Real Odds</title>", "<title>One Piece : The Real Odds</title>"),
        ("The Real Odds · Naruto · modèle v3", "The Real Odds · One Piece · modèle v2"),
        ("Chaque combat du manga, de l'ère de Kaguya à Two Blue Vortex,", "Chaque combat du manga, de God Valley à Elbaf (ch. 1198),"),
        ("fillChars(ca,'itachi');fillChars(cb,'minato');fillArcs(aa,'itachi','itachi');fillArcs(ab,'minato','kyubi');",
         "fillChars(ca,'shanks');fillChars(cb,'kaido');fillArcs(aa,'shanks','egghead');fillArcs(ab,'kaido','wano');"),
        ("let picked=['naruto','sasuke','kakashi','itachi'];", "let picked=['luffy','zoro','sanji','law'];"),
        ("rarc.value='guerre4b';", "rarc.value='wano';"),
        ("['huit_portes','8e porte (Gai)','huit_portes'],", "['eveil','Éveil / Gear 5','eveil'],['haki_roi','Haki des rois imprégné (découverte)','haki_roi'],"),
        ("Mode Ermite, Kyūbi, Six Chemins", "Gear 2, Gear 4, Gear 5, l'entraînement de l'ellipse"),
        ("boost temporaire (portes, marque maudite, pilules)", "boost temporaire, éveil, Haki des rois imprégné quand il est découvert"),
        ("genin, jounin, kage, légende…", "pirate ordinaire, Shichibukai, amiral, Empereur…"),
        ("Préparé, transformation temporaire, 8e porte, épuisé, malade", "Préparé, transformation temporaire, éveil, Haki des rois, épuisé, malade"),
    ]),
    "dragonball": dict(out="verses/dragonball/real-odds-dragonball.html", data="verses/dragonball/model_out.json", rep=COMMON_NON_NARUTO + [
        ("<title>Naruto : The Real Odds</title>", "<title>Dragon Ball : The Real Odds</title>"),
        ("The Real Odds · Naruto · modèle v3", "The Real Odds · Dragon Ball · modèle v1"),
        ("Chaque combat du manga, de l'ère de Kaguya à Two Blue Vortex,", "Chaque combat du manga de Toriyama et du manga Dragon Ball Super, de Pilaf à Super Hero,"),
        ("fillChars(ca,'itachi');fillChars(cb,'minato');fillArcs(aa,'itachi','itachi');fillArcs(ab,'minato','kyubi');",
         "fillChars(ca,'goku');fillChars(cb,'vegeta');fillArcs(aa,'goku','granolah');fillArcs(ab,'vegeta','granolah');"),
        ("let picked=['naruto','sasuke','kakashi','itachi'];", "let picked=['goku','vegeta','gohan','freeza'];"),
        ("rarc.value='guerre4b';", "rarc.value='tdp';"),
        ("['huit_portes','8e porte (Gai)','huit_portes'],", "['ultra','Ultra Instinct / Ultra Ego / Bête','ultra'],"),
        ("Mode Ermite, Kyūbi, Six Chemins", "Super Saiyan, SSJ2, SSJ3, God, Blue, Ultra Instinct"),
        ("boost temporaire (portes, marque maudite, pilules)", "boost temporaire (Kaiōken, transformation)"),
        ("genin, jounin, kage, légende…", "artiste martial, Saiyan, Freezer, dieu de la destruction…"),
        ("Préparé, transformation temporaire, 8e porte, épuisé, malade", "Préparé, Kaiōken, Ultra Instinct, épuisé, malade"),
        ("Le statut ne sert qu'à combler les trous.", "Le statut ne sert qu'à combler les trous."),
    ]),
}
for name in (sys.argv[1:] or V):
    cfg = V[name]
    o = T
    for a, b in cfg["rep"]:
        assert a in o, (name, a)
        o = o.replace(a, b)
    if name != "naruto":
        o = re.sub(r"<p><b>Les databooks officiels comptent aussi\.</b>.*?</p>\n    ", "", o, flags=re.S)
    o = o.replace("__DATA__", open(cfg["data"]).read().replace("</", "<\\/"))
    open(cfg["out"], "w").write(o)
    print("built", cfg["out"])
