# Manag'Hérault 2027/28 — instructions de travail

Lu automatiquement par Claude Code au début de chaque session. Fait autorité sur ce dépôt. Le lire en entier avant toute modification.

**État au 11 novembre 2026 : refonte du schéma et de la page, en un seul versement.** L'objet ne s'appelle plus « la boussole » mais **Manag'Hérault 2027/28**. Les noms de contenus (« fiche boussole », « La boussole du manager », « La boussole des valeurs ») sont inchangés.

---

## 1. L'objet

La MTAM — Mission Transversale d'Accompagnement des Managers, DGA Ressources humaines, Conseil départemental de l'Hérault — porte Manag'Hérault, l'offre d'accompagnement des encadrants de la collectivité. Ce dépôt en publie le catalogue : une page unique, cherchable et filtrable, qui part du besoin du manager. Elle est liée depuis l'intranet et servie par GitHub Pages : `https://manag-herault.github.io/manag-herault/`.

**L'interlocuteur de la MTAM ne lit pas le code et ne travaille pas en ligne de commande.** Tout compte rendu lui est adressé en français professionnel, sans jargon non traduit.

**Ce dépôt est public et son `README.md` s'affiche sur la page de profil du compte.** N'y écrire aucun nom de personne.

## 2. Un maître, un extrait

- **Le classeur Excel de pilotage de la MTAM est le fichier maître.** Il n'est pas dans ce dépôt et n'y entre jamais : il contient des noms et des remarques internes.
- **`offre.csv` en est extrait et n'est jamais modifié à la main.** Une erreur se corrige dans le classeur, puis on extrait à nouveau.
- `index.html` ne contient aucune donnée.

| Fichier | Rôle |
|---|---|
| `offre.csv` | Le catalogue, quatorze colonnes, une ligne par fiche |
| `index.html` | La page |
| `parametres.csv` | `cle;valeur;usage` — adresse de Neeva (`neeva_ouvrir`, `https://neeva.herault.fr/main.php` depuis le 26/11/2026 : hors réseau, Neeva demande identifiant et mot de passe ; sert au bouton « Ouvrir Neeva » du bandeau, au lien « Neeva » de l'encadré « S'inscrire » et au bouton « Ouvrir Neeva » du calendrier) ; groupe 360learning des managers (`elearning_managers`, 26/11/2026, bouton « Formations e-learning managers » du bandeau) ; page Intra34 de prise en main de 360learning (`elearning_aide`, 26/11/2026 : lien « Première connexion à 360learning ? » du bandeau et « S'approprier la plateforme 360learning » au bas de chaque fiche e-learning) ; délai de clôture des inscriptions en jours (`neeva_cloture_jours`, 0 par défaut, 24/11/2026) ; millésime affiché (`millesime`, « 2027/28 », 25/11/2026 : titre, bandeau, « Nouveautés », calendrier, agenda — changer d'année = changer cette cellule ; le mot du DGS n'en dépend pas). Le bouton « Voir le tuto » a été supprimé le même jour, à la demande de la MTAM : ne pas le rétablir. Seules les adresses https sont retenues ; une clé vide ou absente masque le bouton. Aucune adresse en dur dans `index.html` |
| `outils/extraire_catalogue.py` | Classeur → `offre.csv` (colonnes repérées par leur en-tête) |
| `outils/controle_csv.py` | Contrôle avant mise en ligne — **point d'entrée de toute mise à jour** |
| `outils/convertisseur.html` | Classeur → `offre.csv` + contrôle, page autonome hors ligne (SheetJS embarqué), pour travailler sans Python ni Claude. Transposition de `extraire_catalogue.py` et `controle_csv.py` : toute règle modifiée dans l'un se reporte dans l'autre. Équivalence vérifiée octet à octet le 17/11/2026 |
| `outils/construire_demo.py` | Démonstration autonome, ouvrable par double-clic — **jamais déposée ici** |
| `fonts/` | Montserrat, latin et latin-ext, graisses 300 à 900, licence SIL OFL (`fonts/OFL.txt`). Hébergée ici depuis le 18/11/2026 |
| `robots.txt`, `README.md`, `CLAUDE.md` | Indexation, mode d'emploi, ce fichier |

**Classeur (26/11/2026)** : colonne X « FSO » (Oui/Non, liste `L_OuiNon`) insérée après « Ouvert à l'inscription » ; le partage hérité d'Excel a été retiré pour cela (Excel interdit d'insérer une colonne dans un classeur partagé) : la MTAM le réactive si besoin. **Classeur (25/11/2026)** : le tableau Excel `T_Actions` a été converti en plage (filtre automatique conservé) pour permettre le partage du classeur ; ne pas en recréer. Le classeur se modifie cellule par cellule dans son XML, jamais réécrit par openpyxl (erreurs à l'ouverture sous Excel 2019).

Cycle : modifier le classeur → extraire → contrôler → déposer → vérifier la page avec `?src=intra34`.

## 3. `offre.csv` — le schéma

Point-virgule, UTF-8 avec BOM, quatorze colonnes dans cet ordre (`code_neeva` et `duree` ajoutées le 24/11/2026, `inscription_ouverte` le 25, `fso` le 26 ; leur absence dans un fichier antérieur n'est qu'un avertissement) :

```
id;titre;modalite;date;axe;thematiques;lien;type_lien;nouveau;presentation;code_neeva;duree;inscription_ouverte;fso
```

- `modalite` — douze libellés, ceux de la feuille Listes du classeur, sans table de correspondance : Formation · Formation e-learning · Parcours Hérault Managers · Atelier d'échange de pratiques · Guide / fiche boussole · Lundi RH · Lundi RH Replay · Outil'thèque · Ressources · #Managers · Webinaire · Autres. L'ancienne appellation « Atelier d'échange de pratiques » est encore lue par la page et signalée par le contrôle.
- `axe` — `1` · `2` · `3` · `1 et 2` · `1 et 3` · `2 et 3` · `Transverse`.
- `thematiques` — **une seule par action** (arbitrage du 11 novembre), parmi dix-huit libellés.
- `type_lien` — `direct` · `inscription` · `inscription Neeva` · `intra34` · `plateforme` · `externe` · `generique` · vide. Synonymes du classeur (table `TLIEN`) : « directe » → `direct`, « Inscription directe » → `inscription`, « Intra34 » → `intra34`, « Plateforme e-learning » → `plateforme`, « Plateforme externe » → `externe` (bouton « Consulter », 24/11/2026). **Une formation « Inscription Neeva » n'a pas de lien propre** (arbitrage MTAM du 24/11/2026 : l'agenda Intra34 renvoie au catalogue, qui ne renvoie plus aux pages événement) : un lien présent est signalé par le contrôle et n'est pas affiché. Depuis le 26/11/2026, l'encadré et le calendrier renvoient à Neeva par `neeva_ouvrir` (`parametres.csv`).
- `code_neeva` — colonne « Code Neeva » du classeur, première ligne renseignée de la fiche ; affiché dans l'encadré, vide → « communiqué prochainement ».
- `duree` — colonne « Durée » du classeur (texte libre, réservé aux durées en heures, 30 caractères au plus) ; à défaut, « Nombre de jours par session » mis en forme : 0,5 → « ½ journée », 1 → « 1 jour », 2 → « 2 jours ». Cette colonne numérique reste la référence des bilans en jours : ne pas y écrire d'heures. **Toute autre valeur passe telle quelle** : la page crée un type d'accès à son nom, bouton « Consulter ». Dans le classeur, « directe » (valeur de la liste déroulante depuis le 18/11/2026) est admis et écrit `direct` dans `offre.csv` (table `TLIEN` de `extraire_catalogue.py` et de `convertisseur.html`).
- `inscription_ouverte` — colonne « Ouvert à l'inscription » du classeur (W, après « Type de lien »), Oui/Non, première ligne renseignée de la fiche ; `oui` · `non` · vide, toute autre valeur avertie et écrite vide. Décision de la MTAM, bornée par les dates (voir § 6.6).
- `fso` — colonne « FSO » du classeur (X, 26/11/2026), formation statutaire obligatoire : `oui` ou vide, première ligne renseignée de la fiche ; toute autre valeur avertie et écrite vide. Choisie plutôt qu'une parenthèse dans le titre, les intitulés validés par la direction générale restant mot pour mot. Affichée par la pastille « Obligatoire (FSO) » (double filet noir, sans couleur), un filtre « Formations obligatoires (FSO) » (paramètre d'adresse `o=1`, masqué tant qu'aucune fiche n'est FSO) et la recherche (« obligatoire », « fso », « statutaire »).
- `nouveau` — `oui` si « Type projet » vaut « Nouveaux projets » ; affiché « *nouveau », sans toucher au titre.
- `presentation` — 300 caractères au plus. **Textes repris des sources de la MTAM : ne jamais en rédiger.**
- `date` — dates séparées par ` | `, `à venir`, ou vide (accès permanent, donc hors calendrier).

Colonnes supprimées, à ne pas rétablir : `effort`, `disponibilite` (8 novembre), `elearning` (11 novembre, devenue une modalité).

**Toute colonne hors schéma est une erreur bloquante** : c'est le garde-fou contre la sortie d'une colonne interne du classeur.

**Une valeur de liste renommée dans le classeur ne bloque jamais** (règle du 19/11/2026, pour que la MTAM puisse faire évoluer ses listes sans casser la mise à jour). Modalité inconnue → rubrique « Autres actions » ; axe illisible → « Transverse » ; type de lien inconnu → bouton « Consulter » à son nom ; « Type projet » commençant par « Nouveau » → nouveauté ; état d'avancement inconnu → traité comme « En cours ». Chaque cas produit un **avertissement** explicite. Restent bloquants : colonnes manquantes ou hors schéma, identifiant vide, mal formé ou en double, titre vide, lien non https, date illisible.

### Règles d'extraction

- Une ligne du classeur = une session. Les lignes de même identifiant forment une fiche ; leurs dates sont réunies.
- Ne sortent que les actions où « Publier au catalogue » vaut Oui.
- Date : les dates saisies, hors sessions « Suspendu » ou « Annulé » ; à défaut, vide si toutes les lignes sont « Déployé », sinon `à venir`.
- Les instances du parcours d'intégration ne sont pas publiées : ce sont des sessions, pas des entrées d'offre.

## 4. Intitulés et axes

**Les intitulés de la validation de la direction générale l'emportent**, en casse de phrase (arbitrage du 11 novembre, qui annule « les libellés d'Intra34 l'emportent » du 6). Un écart avec la convocation Intra34 est possible et assumé.

1. **AXE 1 — Renforcer un management humain et préventif**
2. **AXE 2 — Adapter les pratiques managériales aux transformations de la collectivité**
3. **AXE 3 — Accompagner les managers dans l'exercice de leurs responsabilités**

Mot pour mot.

## 5. Les dix-huit thématiques

Accompagner le changement et les transitions · Accompagner les moments clés de la vie d'une équipe · Adapter ses pratiques aux nouvelles organisations du travail · Affirmer sa posture de manager · Animer des réunions et des collectifs de travail · Communiquer et donner du feedback · Développer les compétences et accompagner les parcours · Développer un management humain et responsable · Être manager, acteur RH · Exercer ses responsabilités et sécuriser ses pratiques · Mobiliser et faire vivre les collectifs · Organiser son temps, déléguer et responsabiliser · Piloter l'activité et les projets · Piloter les compétences avec les outils RH · Prévenir et gérer les tensions et les conflits · Prévenir les violences, discriminations et harcèlements · Recruter et intégrer · Ressources et accompagnements permanents

**Onze de ces libellés sont câblés dans `index.html`** (constante `SITS`) et dans `outils/controle_csv.py` (`SITUATIONS`) : cinq boutons « situation » les appellent. Renommer une thématique se répercute dans les deux fichiers, dans le même commit.

## 6. Comment la page est construite

**Quatre vues**, en onglets, placés au-dessus de la recherche et des situations (26/11/2026, demande de la MTAM : la recherche ne porte que sur « Les ressources », et elle est masquée dans les autres vues), dans cet ordre fixé par la direction le 26/11/2026 : « Présentation par le DGS » (`?v=pres`), « Les 3 axes de Manag'Hérault » (`?v=axes`), « Les ressources » (vue par défaut, sans `v`), « Le calendrier » (`?v=cal`). La présentation (18/11/2026) reprend le mot d'accueil du DGS (millésime porté à 2027 à la demande de la MTAM ; texte antérieur aux intitulés officiels, dont les trois axes sont donc cités sous leur intitulé officiel, avec un lien vers leur carte, qui ouvre la vue « Les 3 axes ») ; la vue « Les 3 axes », séparée le 26/11/2026, présente pour chaque axe la finalité et objectifs des diapositives 8 à 10 de la présentation validée par la DGS, et un bouton vers les ressources de l'axe, dont le nombre est calculé. Ne pas réécrire ces textes.

**Vue « Les ressources »**

1. **Sept entrées par situation** : cinq par thématiques (« J'anime mon équipe », qui remplace « Je reprends une équipe » le 26/11/2026, couvre « Animer des réunions et des collectifs de travail », « Mobiliser et faire vivre les collectifs » et « Communiquer et donner du feedback » ; « Je mène mes entretiens » couvre « Être manager, acteur RH » et, depuis le 26/11/2026, « Piloter les compétences avec les outils RH »), « Je me forme » par les trois modalités de formation, « Les nouveautés 2027/28 » par la colonne `nouveau`.
2. **Recherche** : tous les mots saisis doivent figurer dans la fiche (titre, présentation, thématique, modalité, axe), sans tenir compte des accents ni d'un pluriel ; les mots trouvés sont surlignés ; les titres qui correspondent passent devant.
3. **Filtres cumulables** : nouveautés, formations obligatoires (FSO), modalité, thématique, axe, accès. Une modalité ou un type d'accès sans fiche n'est pas affiché.
4. **Classement** : par modalité (défaut), thématique, axe, date, alphabet — avec un intertitre par groupe.
5. **Les fiches** : pastille de modalité, « *nouveau », titre, présentation (quatre lignes, « Lire la suite » si elle est coupée), thématique cliquable, date (et durée), axe, lien copiable, bouton d'accès.
6. **Encadré « S'inscrire »** (24/11/2026), pour les types `inscription Neeva` et `inscription` : « Où » (« Neeva », lien vers `neeva_ouvrir` depuis le 26/11/2026 ; ou « Intra34 » avec le bouton « S'inscrire »), code Neeva, dates à venir, durée. Pastille d'état à côté de la modalité : « Inscription ouverte » (une session commence après aujourd'hui + `neeva_cloture_jours`), « Inscriptions closes », « Prochaines dates à venir ». « Ouvert à l'inscription » (colonne W du classeur, 25/11/2026) : « Oui » → règle des dates ; une session passée l'emporte sur un « Oui » oublié (**Inscriptions closes**) · « Non » → **Inscriptions prochainement** si une session est à venir · vide → règle des dates, sauf une formation Neeva sans code, jamais « ouverte » (**Inscriptions prochainement**). **Pas de couleur pour l'état** : plein noir, contour, pointillé, et toujours le libellé. Une fiche par module : chaque module d'un parcours a son identifiant ; les sessions d'un même identifiant restent réunies.

**Vue « Le calendrier »** : sessions à venir par mois, avec présentation et invitation d'agenda (`.ics`) ; puis « Programmation en cours », par modalité ; puis les sessions passées, **repliées** (`CAL_PASSE = false`).

**Partis pris à ne pas défaire**

- L'axe est une étiquette, pas un niveau de navigation.
- Une ressource, une fiche unique.
- **La couleur signifie la modalité**, jamais une valeur ni un axe ; jamais la couleur seule (RGAA 3.1). Douze modalités pour six complémentaires de charte : la couleur désigne la famille. Le prune plein est réservé à « *nouveau ».
- L'exclusion des ressources permanentes du calendrier découle de la cellule `date` vide ; ne jamais la déclarer par une liste de modalités.
- Les statistiques du pied de page sont calculées ; ne jamais les écrire en dur.
- Les notes de travail n'ont pas leur place dans le pied de page.
- Tout est dans l'adresse : `q`, `m`, `t`, `a`, `k`, `n`, `o`, `tri`, `v` (`pres`, `axes`, `cal`), `#r-id`, `#axe-1` à `#axe-3`. **C'est pourquoi les identifiants ne se renomment jamais.** Les thématiques se séparent par `|` (certaines contiennent une virgule). Les adresses d'avant le 11 novembre (`a=A1`, `a=TR`, thématiques à virgules, codes `guide`, `lundirh`, `outil`, `ressource`, `atelier`, `formation`) restent lues ; `m=formation` ne couvre plus l'e-learning ni le parcours.

## 7. La charte graphique

Design system « CD34 Formation ». Prune `#C0116F` (blanc dessus) · vert d'eau `#00CDAA` (**noir** dessus) · noir `#231F20` · prune 10 % `#F9E7F1`. Complémentaires : cyan `#00A5FF` · rose `#FF5FB4` · vert `#37D232` · orange `#FF691E` · jaune `#FFF500` · rouge `#E60514`.

| Modalité | Pastille |
|---|---|
| Formation | cyan |
| Formation e-learning | blanc, bandeau cyan |
| Parcours Hérault Managers | cyan, bandeau noir |
| Atelier d'échange de pratiques | rose |
| Guide / fiche boussole | vert |
| Lundi RH | orange |
| Outil'thèque | jaune |
| Ressources | rouge, texte blanc |
| Webinaire | vert d'eau |
| #Managers | prune 10 %, texte prune |
| Autres | blanc |

**Logo du Département** : version officielle monochrome prune de la charte (fichier fourni par la MTAM le 25/11/2026), sans liseré ajouté, 152 px de large (taille minimale de la charte : 40 mm). Angles droits, sans ombre ni dégradé · Montserrat, servie depuis `fonts/` — **ne jamais rétablir Google Fonts**, qui transmet à Google l'adresse IP de chaque manager · texte ferré à gauche · titres en casse de phrase · signature « Solidarité au quotidien, écologie en actions » et « herault.fr » · thème clair unique. Les six couleurs managériales sont un référentiel distinct et n'apparaissent que dans le bandeau. **Ne pas confondre avec `DGA_Code_couleurs.pdf`** (prune `#B40F64`, hors charte).

## 8. Le filtrage d'accès — et comment tester

Admis : `?src=intra34`, referrer `*.herault.fr`, ou entrée valide antérieure **dans la même session** (`sessionStorage`, depuis le 24/11/2026, à la demande de la MTAM : la mémorisation permanente ouvrait le site par simple adresse sur tout poste déjà admis ; l'ancienne valeur `localStorage` est effacée au chargement). `src=intra34` est conservé dans la barre d'adresse, pour que les favoris fonctionnent. **Tout test s'effectue avec `?src=intra34`** ; retester le refus demande une fenêtre privée. **Ce dispositif ne protège rien** : aucune donnée non diffusable dans le CSV.

La clé de mémorisation s'appelle toujours `mh-boussole-acces` : la renommer refuserait les favoris des managers déjà admis.

## 9. Pièges techniques

1. **Fuseau horaire.** `jourSuivant` calcule en `Date.UTC` ; les dates se comparent en texte `AAAA-MM-JJ`. Ne pas « simplifier ».
2. **BOM et point-virgule** : lire et écrire en les conservant.
3. **Ancres de la démonstration** : `outils/construire_demo.py` repère `var ok = autorise();` et `fetch("offre.csv" … .catch(…);`, et embarque les polices appelées par `url(fonts/….woff2)`. Si la page change à ces endroits, corriger le script — jamais la page pour faire passer la démonstration.
4. **`intra34.herault.fr` interdit l'accès automatisé.** Les liens du catalogue n'ont jamais été testés autrement qu'en vraisemblance. Ne pas contourner ; ne pas présenter ce contrôle comme une validation.
5. **Délai de publication** : une à deux minutes après un commit.
6. **Dates écrites en texte dans le classeur** : l'extraction les lit jour/mois/année. Une vraie date Excel ne pose aucune question.

Corrigé le 11 novembre : l'erreur de script sur la page de refus ; les adresses filtrées sur une thématique contenant une virgule, qui ne renvoyaient rien.

## 10. Décisions prises — ne pas les rouvrir

- Les identifiants ne se renomment jamais. `manager-par-l-intelligence-emotionnelle` désigne la formation intra CNFPT ; l'e-learning porte `developpement-intelligence-emotionnelle-elearning`.
- Numérotation des Lundis RH retirée des intitulés. Les Lundis RH sont des actions comme les formations.
- « Escale Manager » et « Gestion du temps » (CNFPT) : retirées.
- « L'entretien professionnel » existe en formation **et** en Lundi RH : ne pas fusionner.
- Pas de Word ni de PDF dans les productions.
- Hébergement GitHub Pages assumé comme public.

## 11. Ce qui reste ouvert

| Sujet | Action attendue |
|---|---|
| Présentations courtes | 28 fiches sur 101 en portent une ; les autres sont à rédiger par la MTAM, dans le classeur |
| Liens | 42 fiches sans lien |
| « Prévention des risques psycho-sociaux » | modalité « Autres », donc rubrique visible à une seule fiche : à requalifier dans le classeur |
| Une fiche d'atelier porte encore l'ancienne modalité | à corriger dans le classeur |
| Feuille d'export par formules dans le classeur | à construire, pour extraire sans script depuis un poste du Département |
| Programmation 2027/28 | une seule session datée à ce jour |
| Test depuis un poste du Département | jamais fait |
| Hébergement sur l'intranet | la bonne cible à terme |

## 12. Manière de travailler

Un contradicteur, pas un exécutant : commencer par l'objection la plus solide, donner un niveau de confiance, signaler ce qui n'a pas été vérifié. « Collaborateurs », jamais « employés ». **Tester la page rendue et dire ce qui n'a pas pu l'être** : c'est la seule contrepartie au fait que le code livré n'est pas relu. **Vérifier la source avant d'en tirer une conclusion.**
