#!/usr/bin/env python3
"""Contrôle d'un offre.csv de Manag'Hérault 2027/28, avant mise en ligne.

Usage : python3 controle_csv.py nouveau.csv [ancien.csv]
Sortie : rapport en Markdown ; code retour 1 s'il reste une ERREUR bloquante.

Schéma à dix colonnes, arrêté le 11 novembre 2026 :
  id;titre;modalite;date;axe;thematiques;lien;type_lien;nouveau;presentation
Le CSV est extrait du classeur de pilotage (outils/extraire_catalogue.py ou
feuille d'export) : une erreur se corrige DANS LE CLASSEUR, jamais dans le CSV."""
import csv, datetime, io, re, sys, unicodedata
from collections import Counter

COLS = ["id", "titre", "modalite", "date", "axe", "thematiques", "lien", "type_lien", "nouveau", "presentation"]
MOD = ["Formation", "Formation e-learning", "Parcours Hérault Managers", "Atelier d'échange de pratiques",
       "Guide / fiche boussole", "Lundi RH", "Lundi RH Replay", "Outil'thèque", "Ressources", "#Managers", "Webinaire", "Autres"]
# Appellations antérieures, encore lues par la page : signalées, non bloquantes.
MOD_ANCIENNES = {"Atelier de co-construction de solutions": "Atelier d'échange de pratiques", "Atelier d'échange de pratique": "Atelier d'échange de pratiques"}
AXE = ["1", "2", "3", "1 et 2", "1 et 3", "2 et 3", "Transverse"]
ACC = ["direct", "inscription", "inscription Neeva", "generique", "plateforme", ""]
THEMES = ["Accompagner le changement et les transitions", "Accompagner les moments clés de la vie d'une équipe",
  "Adapter ses pratiques aux nouvelles organisations du travail", "Affirmer sa posture de manager",
  "Animer des réunions et des collectifs de travail", "Communiquer et donner du feedback",
  "Développer les compétences et accompagner les parcours", "Développer un management humain et responsable",
  "Être manager, acteur RH", "Exercer ses responsabilités et sécuriser ses pratiques",
  "Mobiliser et faire vivre les collectifs", "Organiser son temps, déléguer et responsabiliser",
  "Piloter l'activité et les projets", "Piloter les compétences avec les outils RH",
  "Prévenir et gérer les tensions et les conflits", "Prévenir les violences, discriminations et harcèlements",
  "Recruter et intégrer", "Ressources et accompagnements permanents"]
# Thématiques appelées par cinq boutons « situation » d'index.html : un renommage les casse.
SITUATIONS = {
  "Je reprends une équipe": ["Développer un management humain et responsable",
      "Accompagner les moments clés de la vie d'une équipe", "Affirmer sa posture de manager"],
  "J'ai un conflit dans mon équipe": ["Prévenir et gérer les tensions et les conflits",
      "Prévenir les violences, discriminations et harcèlements"],
  "Je recrute et j'intègre": ["Recruter et intégrer", "Accompagner les moments clés de la vie d'une équipe"],
  "Je conduis un changement": ["Accompagner le changement et les transitions", "Mobiliser et faire vivre les collectifs"],
  "Je mène mes entretiens": ["Être manager, acteur RH"]}
PRES_MAX = 300

def lire(path):
    raw = open(path, "rb").read()
    try: txt = raw.decode("utf-8-sig"); enc = "UTF-8"
    except UnicodeDecodeError: txt = raw.decode("cp1252"); enc = "Windows-1252 (export Excel non UTF-8)"
    l0 = txt.splitlines()[0]
    sep = ";" if l0.count(";") > l0.count(",") else ","
    rows = [r for r in csv.reader(io.StringIO(txt), delimiter=sep) if any(c.strip() for c in r)]
    head = [h.strip().lower() for h in rows[0]]
    data = [{h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(head)} for r in rows[1:]]
    return enc, sep, head, data

def dates(brut):
    """(liste de dates, mention « à venir », écritures illisibles)"""
    ok, avenir, ko = [], False, []
    for v in [x.strip() for x in brut.split("|") if x.strip()]:
        if v.lower() == "à venir": avenir = True; continue
        m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", v)
        m2 = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", v)
        try:
            if m: ok.append(datetime.date(int(m[1]), int(m[2]), int(m[3])))
            elif m2: ok.append(datetime.date(int(m2[3]), int(m2[2]), int(m2[1])))
            else: ko.append(v)
        except ValueError: ko.append(v)
    return ok, avenir, ko

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    enc, sep, head, data = lire(sys.argv[1])
    E, A = [], []
    if not enc.startswith("UTF-8"): E.append(f"Encodage {enc} : réenregistrer en « CSV UTF-8 » (sinon accents cassés).")
    manq = [c for c in COLS if c not in head]
    if manq: E.append("Colonnes manquantes : " + ", ".join(manq))
    trop = [c for c in head if c not in COLS]
    if trop: E.append("Colonnes hors schéma : " + ", ".join(trop) + ". Le dépôt est public : seules les dix colonnes "
                      "publiables sortent du classeur (ni intervenant, ni référent, ni remarque, ni salle, ni effectif).")
    ids = Counter(d.get("id", "") for d in data); tits = Counter(d.get("titre", "").lower() for d in data)
    themes, auj, passees, datees, avenirs = Counter(), datetime.date.today(), 0, 0, 0
    for n, d in enumerate(data, start=2):
        L = f"L{n} « {d.get('titre') or '(sans titre)'} »"
        if not d.get("titre"): E.append(f"{L} : titre vide, la ligne sera ignorée.")
        if not re.fullmatch(r"[a-z0-9-]+", d.get("id", "")): E.append(f"{L} : id « {d.get('id')} » non conforme (minuscules, chiffres, tirets).")
        if ids[d.get("id", "")] > 1: E.append(f"{L} : id en double (les liens directs #r-id se confondent).")
        if tits[d.get("titre", "").lower()] > 1: A.append(f"{L} : titre en double.")
        if d.get("modalite") in MOD_ANCIENNES:
            A.append(f"{L} : modalité « {d['modalite']} », renommée « {MOD_ANCIENNES[d['modalite']]} » dans la liste du classeur. "
                     "La page la range sous la nouvelle rubrique ; corriger la cellule E du classeur.")
        for col, ok in (("modalite", MOD + list(MOD_ANCIENNES)), ("axe", AXE), ("type_lien", ACC)):
            if d.get(col, "") not in ok:
                E.append(f"{L} : {col} = « {d.get(col)} » inconnu (valeurs admises : {' · '.join(v for v in ok if v)}).")
        if d.get("modalite") in ("#Managers", "Webinaire", "Autres"):
            A.append(f"{L} : modalité « {d['modalite']} » — elle devient une rubrique visible du catalogue. Confirmer ou requalifier.")
        if d.get("nouveau", "") not in ("", "oui"): E.append(f"{L} : nouveau = « {d['nouveau']} » (attendu : oui ou vide).")
        p = d.get("presentation", "")
        if len(p) > PRES_MAX: A.append(f"{L} : présentation de {len(p)} caractères ({PRES_MAX} au plus).")
        if "\n" in p: A.append(f"{L} : retour à la ligne dans la présentation.")
        u, k = d.get("lien", ""), d.get("type_lien", "")
        if u and not u.startswith("https://"): E.append(f"{L} : lien non https ou mal formé : {u}")
        if u and not k: A.append(f"{L} : lien présent mais type_lien vide (affiché « Consulter »).")
        if k and not u: A.append(f"{L} : type_lien « {k} » sans lien (affiché « Lien à renseigner »).")
        if k == "direct" and u.rstrip("/").endswith(("360learning.com", "hi_2589236/outils")):
            A.append(f"{L} : lien générique marqué « direct ».")
        ok, avenir, ko = dates(d.get("date", ""))
        for v in ko: E.append(f"{L} : date « {v} » illisible (attendu AAAA-MM-JJ, JJ/MM/AAAA, « à venir » ou vide).")
        if ok: datees += 1
        elif avenir: avenirs += 1
        passees += sum(1 for x in ok if x < auj)
        th = [x.strip() for x in d.get("thematiques", "").split("|") if x.strip()]
        if not th: A.append(f"{L} : aucune thématique (la fiche n'apparaîtra dans aucun filtre thématique).")
        if len(th) > 1: A.append(f"{L} : {len(th)} thématiques — une seule par action depuis le 11 novembre 2026.")
        for t in th:
            if t not in THEMES: A.append(f"{L} : thématique « {t} » absente de la liste de référence (nouvelle, ou faute de frappe ?).")
        themes.update(th)
    for sit, ths in SITUATIONS.items():
        if not any(t in themes for t in ths):
            E.append(f"Bouton « {sit} » : aucune de ses thématiques n'est portée par une fiche — il ne renverrait rien.")
        for t in ths:
            if t not in themes: A.append(f"Bouton « {sit} » : la thématique « {t} » n'est portée par aucune fiche.")
    cle = lambda s: re.sub(r"\W", "", unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower())
    vus = {}
    for t in themes:
        if cle(t) in vus: E.append(f"Thématiques quasi identiques : « {vus[cle(t)]} » et « {t} » : deux filtres au lieu d'un.")
        else: vus[cle(t)] = t

    k = Counter(d.get("type_lien") or ("direct" if d.get("lien") else "à renseigner") for d in data)
    print(f"# Contrôle de offre.csv\n\n- Encodage : {enc} · séparateur « {sep} » · **{len(data)} fiches**")
    print(f"- Liens : {sum(1 for d in data if d.get('lien'))} renseignés, {sum(1 for d in data if not d.get('lien'))} à renseigner ("
          + ", ".join(f"{a} {b}" for a, b in k.most_common()) + ")")
    print("- Par modalité : " + ", ".join(f"{m} {c}" for m, c in Counter(d.get('modalite') for d in data).most_common()))
    print("- Par axe : " + ", ".join(f"{m} {c}" for m, c in sorted(Counter(d.get('axe') for d in data).items())))
    print(f"- Calendrier : {datees} fiches datées (dont {passees} date(s) passée(s)), {avenirs} « à venir », {len(data)-datees-avenirs} en accès permanent")
    print(f"- Nouveautés : {sum(1 for d in data if d.get('nouveau') == 'oui')} · présentations : {sum(1 for d in data if d.get('presentation'))} sur {len(data)}")
    print(f"- Thématiques : {len(themes)}")
    print(f"\n## Erreurs bloquantes ({len(E)})"); print("\n".join("- " + x for x in E) or "Aucune.")
    print(f"\n## Avertissements ({len(A)})"); print("\n".join("- " + x for x in A) or "Aucun.")

    if len(sys.argv) > 2:
        _, _, h_old, old = lire(sys.argv[2])
        o = {d["id"]: d for d in old}; n = {d["id"]: d for d in data}
        communs = [c for c in COLS if c in h_old and c != "id"]
        print("\n## Changements depuis la version précédente")
        if set(h_old) != set(head):
            print(f"- **Changement de schéma** : colonnes retirées {sorted(set(h_old)-set(head)) or '∅'}, ajoutées {sorted(set(head)-set(h_old)) or '∅'}.")
        add = [n[i]["titre"] for i in n if i not in o]; rem = [o[i]["titre"] for i in o if i not in n]
        mod = [(n[i]["titre"], c, o[i].get(c, ""), n[i].get(c, "")) for i in n if i in o for c in communs if o[i].get(c, "") != n[i].get(c, "")]
        print(f"- Ajoutées ({len(add)}) : " + ("; ".join(add) or "aucune"))
        print(f"- Retirées ({len(rem)}) : " + ("; ".join(rem) or "aucune"))
        par = Counter(c for _, c, _, _ in mod)
        print(f"- Champs modifiés ({len(mod)}) : " + ", ".join(f"{c} {k}" for c, k in par.most_common()))
        for t, c, a, b in mod:
            if c in ("titre", "date", "lien", "type_lien"): print(f"  - « {t} » · {c} : « {a or '∅'} » → « {b or '∅'} »")
    sys.exit(1 if E else 0)

if __name__ == "__main__": main()
