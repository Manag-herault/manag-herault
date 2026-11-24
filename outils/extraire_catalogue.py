#!/usr/bin/env python3
"""Extrait offre.csv du classeur de pilotage Manag'Hérault 2027/28.

Usage : python3 extraire_catalogue.py classeur.xlsx [offre.csv]

Le classeur est le fichier maître ; offre.csv n'est jamais modifié à la main.
Seules douze colonnes publiables sortent : aucun intervenant, référent, remarque,
salle ni effectif. Les colonnes sont repérées par leur EN-TÊTE, pas par leur
lettre : déplacer une colonne dans le classeur ne casse pas l'extraction.

Règles (voir claude/methode-pilotage-catalogue.md) :
  - une ligne du classeur = une session ; les lignes de même identifiant sont
    regroupées en une fiche, leurs dates réunies et séparées par « | » ;
  - seules sortent les fiches dont « Publier au catalogue » vaut Oui ;
  - colonne date : les dates saisies (du début à la fin si une date de fin est
    donnée), hors sessions « Suspendu » ou « Annulé » ; à défaut, vide si toutes
    les lignes sont « Déployé » (accès permanent), sinon « à venir » ;
  - nouveau = oui si « Type projet » vaut « Nouveaux projets » ;
  - code_neeva : « Code Neeva » de la première ligne qui en porte un ;
  - duree : « Durée » (texte libre, pour une durée en heures) si elle est remplie,
    sinon « Nombre de jours par session » mis en forme (« ½ journée », « 2 jours »).

Code retour 1 en cas d'anomalie bloquante : le CSV n'est alors pas écrit."""
import csv, datetime, json, re, sys, unicodedata

SORTIE = ["id", "titre", "modalite", "date", "axe", "thematiques",
          "lien", "type_lien", "nouveau", "presentation", "code_neeva", "duree"]
# synonymes admis dans la colonne « Type de lien » du classeur -> valeur écrite dans offre.csv
# Synonymes de « Type de lien ». Une valeur absente de cette table passe telle quelle :
# la page lui donne alors un bouton « Consulter » à son nom (rien ne bloque).
TLIEN = {"directe": "direct", "inscription directe": "inscription", "inscription neeva": "inscription Neeva", "intra34": "intra34", "plateforme e-learning": "plateforme", "plateforme": "plateforme", "plateforme externe": "externe", "externe": "externe"}
# Valeurs qui changent le sens d'une ligne : une valeur inconnue est signalée, jamais bloquante.
ETATS = ("a faire", "en cours", "communication", "realise", "suspendu", "annule", "deploye")
# en-tête du classeur (début, sans accent ni casse) -> nom interne
ENTETES = {"identifiant": "id", "intitule de l'action": "titre", "axe": "axe",
           "thematique": "th", "modalite de mise en oeuvre": "mod",
           "type projet": "type", "presentation courte": "pres",
           "date de debut": "debut", "date (1re session)": "debut",
           "date de fin": "fin", "etat d'avancement": "etat",
           "publier au catalogue": "pub", "lien": "lien", "type de lien": "tlien",
           "code neeva": "code", "duree": "duree", "nombre de jours par session": "jours"}

def jours_en_texte(v):
    """Nombre de jours par session -> libellé affiché ; vide si illisible ou nul."""
    try: x = float(str(v).replace(",", ".").strip())
    except ValueError: return ""
    if x <= 0: return ""
    if x == 0.5: return "½ journée"
    n = ("%g" % x).replace(".", ",")
    return n + (" jour" if x < 2 else " jours")

def cle(s):
    s = str(s or "").replace("œ", "oe").replace("Œ", "OE").replace("’", "'")
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()

def lire(chemin):
    """Retourne la feuille Actions sous forme de liste de listes."""
    if chemin.endswith(".json"):                 # relevé texte du classeur
        return json.load(open(chemin, encoding="utf-8")), "MJA"
    import openpyxl
    wb = openpyxl.load_workbook(chemin, data_only=True, read_only=True)
    if "Actions" not in wb.sheetnames:
        sys.exit("ERREUR — feuille « Actions » introuvable dans le classeur.")
    return [list(r) for r in wb["Actions"].iter_rows(values_only=True)], "JMA"

def en_date(v, ordre):
    """Date ISO, ou None. `ordre` lève l'ambiguïté des dates écrites en texte."""
    if v in (None, ""): return None
    if isinstance(v, datetime.datetime): return v.date()
    if isinstance(v, datetime.date): return v
    s = str(v).strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m: return datetime.date(*map(int, m.groups()))
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        a, b, an = map(int, m.groups())
        j, mo = (b, a) if ordre == "MJA" else (a, b)
        return datetime.date(an, mo, j)
    raise ValueError(s)

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    lignes, ordre = lire(sys.argv[1])
    sortie = sys.argv[2] if len(sys.argv) > 2 else "offre.csv"
    tete = [cle(h) for h in lignes[0]]
    col = {}
    for i, h in enumerate(tete):
        for debut, nom in ENTETES.items():
            if h == debut or (debut in ("presentation courte", "duree", "code neeva") and h.startswith(debut)):
                col.setdefault(nom, i)
    manq = [n for n in ("id", "titre", "axe", "th", "mod", "type", "pres", "debut",
                        "etat", "pub", "lien", "tlien") if n not in col]
    if manq: sys.exit("ERREUR — colonnes introuvables dans la feuille Actions : " + ", ".join(manq))
    val = lambda r, n: ("" if n not in col or col[n] >= len(r) or r[col[n]] is None else r[col[n]])
    txt = lambda r, n: re.sub(r"\s+", " ", str(val(r, n))).strip()

    fiches, ordre_ids, E, A = {}, [], [], []
    for n, r in enumerate(lignes[1:], start=2):
        if not txt(r, "titre") and not txt(r, "id"): continue
        i = txt(r, "id")
        if not i: E.append(f"L{n} « {txt(r,'titre')} » : identifiant vide."); continue
        f = fiches.get(i)
        if f is None:
            f = fiches[i] = {"id": i, "titre": txt(r, "titre"), "mod": txt(r, "mod"),
                             "axe": txt(r, "axe"), "th": txt(r, "th"), "lien": txt(r, "lien"),
                             "tlien": txt(r, "tlien"), "type": txt(r, "type"),
                             "pres": txt(r, "pres"), "pub": cle(txt(r, "pub")) == "oui",
                             "code": txt(r, "code"), "duree": txt(r, "duree"), "jours": txt(r, "jours"),
                             "dates": set(), "etats": [], "ligne": n}
            ordre_ids.append(i)
        else:
            if txt(r, "titre") != f["titre"]:
                E.append(f"L{n} : l'identifiant « {i} » porte deux intitulés (« {f['titre']} », ligne {f['ligne']}, et « {txt(r,'titre')} »).")
            for k, lib in (("mod", "modalité"), ("axe", "axe"), ("th", "thématique")):
                if txt(r, k) != f[k]:
                    A.append(f"L{n} « {f['titre']} » : {lib} différente de la ligne {f['ligne']} ; celle de la ligne {f['ligne']} est retenue.")
            if not f["lien"] and txt(r, "lien"): f["lien"], f["tlien"] = txt(r, "lien"), txt(r, "tlien")
            if not f["pres"] and txt(r, "pres"): f["pres"] = txt(r, "pres")
            if txt(r, "code") and f["code"] and txt(r, "code") != f["code"]:
                A.append(f"L{n} « {f['titre']} » : code Neeva « {txt(r, 'code')} » différent de la ligne {f['ligne']} ; celui de la ligne {f['ligne']} est retenu.")
            for k in ("code", "duree", "jours"):
                if not f[k] and txt(r, k): f[k] = txt(r, k)
            f["pub"] = f["pub"] or cle(txt(r, "pub")) == "oui"
        etat = txt(r, "etat"); f["etats"].append(etat)
        if etat and cle(etat) not in ETATS:
            A.append(f"L{n} « {f['titre']} » : état « {etat} » non reconnu — traité comme « En cours » "
                     "(seuls « Suspendu », « Annulé » et « Déployé » changent le calendrier).")
        if txt(r, "pub") and cle(txt(r, "pub")) not in ("oui", "non"):
            A.append(f"L{n} « {f['titre']} » : « Publier au catalogue » = « {txt(r, 'pub')} » — seul « Oui » publie.")
        try:
            d, fin = en_date(val(r, "debut"), ordre), en_date(val(r, "fin"), ordre)
        except ValueError as e:
            E.append(f"L{n} « {f['titre']} » : date illisible « {e} »."); continue
        if d and cle(etat) not in ("suspendu", "annule"):
            fin = fin if fin and d <= fin <= d + datetime.timedelta(days=14) else d
            while d <= fin:
                f["dates"].add(d.isoformat()); d += datetime.timedelta(days=1)

    rangs = []
    for i in ordre_ids:
        f = fiches[i]
        if not f["pub"]: continue
        if f["dates"]: date = " | ".join(sorted(f["dates"]))
        elif f["etats"] and all(cle(e) == "deploye" for e in f["etats"]): date = ""
        else: date = "à venir"
        if len(f["pres"]) > 300:
            A.append(f"L{f['ligne']} « {f['titre']} » : présentation de {len(f['pres'])} caractères (300 au plus).")
        rangs.append([i, f["titre"], f["mod"], date, f["axe"], f["th"], f["lien"], TLIEN.get(cle(f["tlien"]), f["tlien"]),
                      "oui" if cle(f["type"]).startswith("nouveau") else "", f["pres"],
                      f["code"], f["duree"] or jours_en_texte(f["jours"])])

    for x in A: print("Avertissement — " + x)
    if E:
        for x in E: print("ERREUR — " + x)
        sys.exit(1)
    with open(sortie, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter=";", lineterminator="\r\n")
        w.writerow(SORTIE); w.writerows(rangs)
    print(f"{sortie} écrit — {len(rangs)} fiches publiées sur {len(fiches)} actions ({len(lignes)-1} lignes lues).")

if __name__ == "__main__": main()
