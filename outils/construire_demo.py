#!/usr/bin/env python3
"""Construit la démonstration autonome de Manag'Hérault 2027/28, à partir des
fichiers de production, sans les modifier.

Usage : python3 construire_demo.py index.html offre.csv [sortie.html] [étiquette]
Défaut : demo-managherault.html dans le dossier courant.

La démonstration est un fichier unique, ouvrable par double-clic, qui diffère de
la production par deux points et deux seulement :
  1. le catalogue est embarqué dans la page, à la place de l'appel réseau ;
  2. le filtrage d'accès est neutralisé, sinon la page se refuse à elle-même.
Elle n'est JAMAIS déposée dans le dépôt : elle n'a pas de filtrage et son
catalogue est figé à la date de génération.

Code retour 1 si une ancre est introuvable : rien n'est écrit."""
import re, sys, datetime, pathlib

def erreur(msg, remede):
    print(f"ERREUR — {msg}\n  Remède : {remede}", file=sys.stderr); sys.exit(1)

def une_fois(motif, texte, quoi, remede):
    trouve = list(re.finditer(motif, texte, re.MULTILINE | re.DOTALL))
    if len(trouve) != 1:
        erreur(f"{quoi} : {len(trouve)} correspondance(s) dans index.html, 1 attendue.", remede)
    return trouve[0]

def main():
    if len(sys.argv) < 3:
        erreur("arguments manquants.", "python3 construire_demo.py index.html offre.csv [sortie.html] [étiquette]")
    p_html, p_csv = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    p_out = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else "demo-managherault.html")
    src = p_html.read_text(encoding="utf-8")
    csv = p_csv.read_text(encoding="utf-8-sig")
    jour = datetime.date.today().strftime("%d/%m/%Y")
    etiquette = sys.argv[4] if len(sys.argv) > 4 else f"catalogue figé au {jour}, intégré à la page"
    if "</script" in csv.lower():
        erreur("offre.csv contient la chaîne « </script » : il ne peut pas être embarqué tel quel.",
               "retirer cette chaîne du classeur, puis extraire à nouveau.")

    m = une_fois(r"^[ \t]*var ok = autorise\(\);[ \t]*$", src,
                 "ancre du filtrage d'accès (« var ok = autorise(); »)",
                 "le bloc de filtrage d'index.html a été réécrit : mettre à jour cette ancre, sans modifier index.html.")
    src = (src[:m.start()] + "  /* DÉMO : filtrage d'accès neutralisé, la page s'ouvre en file:// */\n"
           "  var ok = true; void autorise;" + src[m.end():])

    p_par = p_html.parent / "parametres.csv"
    par = p_par.read_text(encoding="utf-8-sig") if p_par.exists() else ""
    if "</script" in par.lower(): erreur("parametres.csv contient « </script ».", "corriger parametres.csv.")
    m = une_fois(r'fetch\("parametres\.csv".*?\.catch\([^;]*\);', src,
                 "ancre du chargement des paramètres (« fetch(\"parametres.csv\" … .catch(…); »)",
                 "la page ne charge plus parametres.csv de cette manière : mettre à jour cette ancre.")
    src = (src[:m.start()] + "{ /* DÉMO : paramètres embarqués. */ parametres(document.getElementById(\"parametres-embarques\").textContent); }"
           + src[m.end():])
    m = une_fois(r'fetch\("offre\.csv".*?\.catch\([^;]*\);', src,
                 "ancre du chargement du CSV (« fetch(\"offre.csv\" … .catch(…); »)",
                 "la page ne charge plus le CSV de cette manière : mettre à jour cette ancre.")
    src = (src[:m.start()] + "{ /* DÉMO : catalogue embarqué dans la page, aucun appel réseau. */\n"
           "try{\n  boot(parseCSV(document.getElementById(\"offre-embarquee\").textContent));\n"
           "}catch(e){ fail(String(e.message || e)); } }" + src[m.end():])

    # Police : les fichiers fonts/*.woff2 sont embarqués, sinon la démonstration
    # ouverte hors du site retomberait sur une police système.
    import base64
    def embarquer(m):
        f = p_html.parent / m.group(1)
        if not f.exists():
            erreur(f"police {m.group(1)} introuvable à côté d'index.html.", "lancer le script depuis une copie complète du dépôt.")
        return "url(data:font/woff2;base64," + base64.b64encode(f.read_bytes()).decode("ascii") + ")"
    src = re.sub(r"url\((fonts/[a-z0-9-]+\.woff2)\)", embarquer, src)

    bandeau = (f"<!-- DÉMO générée le {jour} — NE PAS DÉPOSER DANS LE DÉPÔT -->\n"
        '<div style="background:#231f20;color:#fff;font:500 12px/1.4 Montserrat,system-ui,sans-serif;'
        'padding:7px 24px;text-align:center;letter-spacing:.02em">'
        f"Version de <strong>démonstration</strong> &mdash; {etiquette}. "
        'La version en service lit <code style="font-size:11px">offre.csv</code>.</div>\n'
        '<script type="text/plain" id="offre-embarquee">' + csv + "</script>\n"
        '<script type="text/plain" id="parametres-embarques">' + par + "</script>\n")
    m = une_fois(r"<body>", src, "balise <body>", "index.html n'a plus de balise <body> littérale : adapter l'ancre.")
    src = src[:m.end()] + "\n" + bandeau + src[m.end():]

    for quoi, present in (("le catalogue embarqué", 'id="offre-embarquee"' in src),
                          ("le bandeau de démonstration", "démonstration</strong>" in src),
                          ("la neutralisation du filtrage", "var ok = true;" in src)):
        if not present: erreur(f"{quoi} est absent du fichier produit.", "ne pas livrer ; reprendre le script.")
    if 'fetch("offre.csv"' in src or 'fetch("parametres.csv"' in src:
        erreur("un appel réseau vers offre.csv subsiste : la démonstration échouerait en file://.",
               "vérifier qu'index.html ne charge le CSV qu'en un seul endroit.")
    p_out.write_text(src, encoding="utf-8")
    lignes = len([l for l in csv.splitlines() if l.strip()]) - 1
    print(f"{p_out} écrit — {len(src.encode('utf-8'))} octets, figé au {jour}.")

if __name__ == "__main__": main()
