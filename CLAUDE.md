# Boussole Manag'Hérault — instructions de travail

Ce fichier est lu automatiquement par Claude Code au début de chaque session, en
terminal comme dans la version web. Il fait autorité sur ce dépôt. Le lire en
entier avant toute modification.

**État au 9 novembre 2026 : le dépôt et l'artefact claude.ai « Boussole
Manag'Hérault » sont synchronisés, version 18.** Ce n'était pas le cas avant ce
jour ; si un écart réapparaît, l'artefact fait foi et la remise à niveau du dépôt
passe avant tout autre travail.

---

## 1. L'objet

La MTAM — Mission Transversale d'Accompagnement des Managers, DGA Ressources
humaines, Conseil départemental de l'Hérault — porte **Manag'Hérault**, l'offre
d'accompagnement des 503 encadrants de la collectivité. Cette offre était
présentée dans un Genially linéaire que les managers n'ouvraient pas.

La **Boussole Manag'Hérault** la remplace : une page web unique, cherchable et
filtrable, qui part du besoin du manager plutôt que du catalogue. Elle est liée
depuis l'intranet du Département et servie par GitHub Pages à l'adresse
`https://manag-herault.github.io/manag-herault/`.

**Interlocuteur : Benjamin Pavageau**, chef de projet Accompagnement managérial et
coach interne à la MTAM. **Il ne lit pas le code et ne travaille pas en ligne de
commande.** Il maintient le dépôt par l'interface web de GitHub, souvent depuis un
poste de travail sans accès à ses fichiers personnels. Toute explication, tout
compte rendu, toute question lui sont adressés en français professionnel, sans
jargon technique non traduit.

---

## 2. Les fichiers

| Fichier | Rôle | Qui le modifie |
|---|---|---|
| `offre.csv` | Le catalogue. Neuf colonnes, une ligne par ressource. **Source unique de vérité du contenu.** | la MTAM, dans Excel |
| `index.html` | La page : deux vues, recherche, filtres, calendrier, filtrage d'accès. **Ne contient aucune donnée.** | exceptionnel, à justifier |
| `robots.txt` | Interdiction d'indexation, à la racine | non |
| `README.md` | Colonnes, procédure de mise à jour, section « Accès » | à la demande |
| `CLAUDE.md` | Ce fichier | à chaque décision structurante |

**Le fichier de documentation s'appelle `README.md`, et plus `LISEZ-MOI.md`.**
Arbitrage du 9 novembre : c'est ce que GitHub affiche sur la page d'accueil du
dépôt. Un commentaire en tête d'`index.html` y renvoie — le garder cohérent en cas
de nouveau renommage.

**Ce dépôt porte le nom de son propriétaire**, ce qui en fait aux yeux de GitHub un
dépôt de profil : **son `README.md` est affiché publiquement sur la page de profil
du compte `manag-herault`**. N'y écrire rien qui ne puisse être lu par n'importe qui.

**Un fichier n'entre jamais dans le dépôt** : `demo-boussole-managherault.html`,
démonstration autonome ouvrable par double-clic. Depuis que la page en service
porte le calendrier 2026, elle n'a plus d'objet.

### Ce qui n'est pas dans le dépôt et qu'une session web ne voit pas

- Le skill `maj-boussole-managherault` : procédure de mise à jour, **script de
  contrôle du CSV** et `construire_demo.py`.
- Les documents de projet claude.ai : `claude/journal-catalogue.md`,
  `claude/controle-liens-intra34.md`, `claude/thematisation-corrigee-mtam.md`,
  `claude/PASSATION-boussole-managherault.md`, `claude/PASSATION-claude-code.md`.

Une session Claude Code travaille sur le dépôt seul. **Si un travail a besoin du
script de contrôle, il faut d'abord le verser au dépôt**, dans un dossier `outils/`
exclu de GitHub Pages — ou traiter le sujet depuis claude.ai. Ne pas le réécrire de
mémoire : il embarque des règles qui ont déjà rattrapé des défauts en production.

---

## 3. `offre.csv` — le schéma

Séparateur **point-virgule**, encodage **UTF-8 avec BOM** (Excel français le
réécrit ainsi ; ne pas le retirer). Neuf colonnes, dans cet ordre :

```
id;titre;modalite;date;axe;thematiques;elearning;lien;type_lien
```

Les colonnes `effort` et `disponibilite` ont été **supprimées le 8 novembre** —
l'une était déductible de la modalité pour 96 fiches sur 100, l'autre doublait
`date`. **Ne pas les rétablir**, ni la famille de filtres « Effort demandé ».

**Vocabulaires fermés** — toute autre valeur est une erreur bloquante :

- `modalite` : `formation` · `atelier` · `guide` · `lundirh` · `outil` · `ressource`
- `axe` : `A1` · `A2` · `A3` · `A1+A2` · `A1+A3` · `TR` (transverse)
- `elearning` : `oui` ou vide
- `type_lien` : `direct` · `inscription` · `generique` · `plateforme` · vide
- `thematiques` : un ou plusieurs des dix-huit libellés de la section 5,
  **séparés par ` | `** (barre verticale entourée d'espaces), orthographiés mot
  pour mot

### La colonne `date` pilote le calendrier

Trois cas, et trois seulement :

| Valeur | Effet |
|---|---|
| une ou plusieurs dates séparées par ` \| ` | une entrée par session au calendrier ; la date s'affiche sur la fiche |
| `à venir` | la fiche apparaît sous « Programmation en cours », sans date |
| vide | ressource accessible en permanence : **absente** du calendrier |

Deux écritures acceptées, `AAAA-MM-JJ` et `JJ/MM/AAAA`, parce qu'Excel français
réécrit spontanément la première en la seconde. Toute autre forme est une erreur
bloquante : un calendrier doit pouvoir trier.

Les jours consécutifs d'une même fiche sont regroupés en une session unique —
« 9 et 10 mars 2026 », « 1er et 2 juin 2026 ». Deux sessions réellement distinctes
sur deux jours qui se suivent seraient fusionnées à tort ; cas non rencontré, à
signaler s'il se présente.

**L'exclusion des ressources permanentes ne se déclare nulle part** : elle découle
de la cellule vide. Ne jamais réintroduire dans la page une liste de modalités à
écarter.

### État du catalogue au 9 novembre 2026

**100 ressources · 59 liens renseignés · 41 à renseigner.**
Par modalité : formation 34 · guide 26 · lundirh 13 · ressource 12 · outil 10 · atelier 5.
Calendrier : **19 fiches datées (21 sessions) · 25 en « à venir » · 56 en accès permanent.**
18 thématiques · 6 entrées par situation · 3 axes.

---

## 4. Les trois axes — version officielle

1. **AXE 1 — Renforcer un management humain et préventif**
2. **AXE 2 — Adapter les pratiques managériales aux transformations de la collectivité**
3. **AXE 3 — Accompagner les managers dans l'exercice de leurs responsabilités**

Arrêtés le 6 novembre 2026. Toute reprise ailleurs s'y conforme **mot pour mot**.
L'intitulé « Accompagner les prises de poste », que donnait le sommaire du Genially,
est abandonné.

---

## 5. Les dix-huit thématiques

Développer un management humain et responsable · Communiquer et donner du feedback ·
Animer des réunions et des collectifs de travail · Prévenir et gérer les tensions et
les conflits · Prévenir les violences, discriminations et harcèlements · Organiser son
temps, déléguer et responsabiliser · Accompagner les moments clés de la vie d'une
équipe · Accompagner le changement et les transitions · Mobiliser et faire vivre les
collectifs · Piloter l'activité et les projets · Adapter ses pratiques aux nouvelles
organisations du travail · Développer les compétences et accompagner les parcours ·
Affirmer sa posture de manager · Être manager, acteur RH · Recruter et intégrer ·
Piloter les compétences avec les outils RH · Exercer ses responsabilités et sécuriser
ses pratiques · Ressources et accompagnements permanents

**Attention : cinq de ces libellés sont câblés dans `index.html`.** Les boutons
« entrées par situation » appellent des thématiques par leur libellé exact.
**Renommer une thématique dans le CSV casse le raccourci correspondant**, sans
message d'erreur. Toute renomination se répercute dans `index.html` dans le même
commit.

---

## 6. Les sources de dates — point ouvert

Deux fichiers Excel de la MTAM donnent des dates, et **ils se contredisent**.

| Fichier | Statut | Écarts constatés |
|---|---|---|
| **ManagHerault2026.xlsx**, feuille « 2026 » | **fait foi depuis le 9 novembre** | — |
| **Événement Intra34 2026.xlsx** | faisait foi jusqu'au 9 novembre | intelligence collaborative M1 au 9 avril contre le 16 septembre ; M3 au 8 octobre contre le 4 février 2027 ; mobilisation et cohésion d'équipe au 5 juin contre le 4 décembre ; atelier conflits au 10 décembre contre le 7 |
| **Genially** (export PDF) | historique | dates fausses, jusqu'à six mois d'écart. Ne jamais les reprendre |

**Le point n'est pas tranché sur le fond.** Intra34 édite les convocations que les
managers reçoivent ; si les deux fichiers restent désaccordés, la boussole et la
convocation afficheront deux dates différentes. À faire arbitrer par la MTAM.

Le tableau de dates de `claude/PASSATION-boussole-managherault.md`, section 9, est
**périmé**.

### Règles de versement d'un calendrier

- Les actions **suspendues ou annulées** ne sont **pas datées**, même quand la
  source leur donne une date : annoncer une session qui n'aura pas lieu fait perdre
  son temps au manager. Elles restent en `à venir`.
- Les **instances du parcours d'intégration** — Primo promos, Découverte groupes,
  Journées Acteur RH, ateliers Déontologie / Marchés / Systèmes d'information — ne
  sont pas exposées : ce sont des sessions, pas des entrées d'offre. Elles relèvent
  des fiches *Parcours Hérault'Manager* et *Parcours des nouveaux arrivants*.
- Les **e-learning portés « Déployé »** avec une date « sans objet » sont en accès
  permanent : cellule vide, donc hors calendrier.

---

## 7. Comment la page est construite

**Deux vues**, basculées par un onglet : « Les ressources » et « Le calendrier ».
La seconde s'ouvre directement par `?v=cal`, paramètre combinable aux autres.

**Vue « Les ressources »**, trois niveaux de lecture :

1. **Six entrées par situation** — « Je reprends une équipe », « J'ai un conflit dans
   mon équipe », « Je recrute et j'intègre », « Je conduis un changement », « Je mène
   mes entretiens », « Je me forme ». Les cinq premières pilotent des filtres
   thématiques, définis dans `index.html` par libellé (voir section 5). La sixième
   pointe vers la modalité `formation`, par la clé `mod` de `SITS`.
2. **Une recherche plein texte** et quatre familles de filtres cumulables :
   modalité, accès, thématique, axe. Les compteurs se recalculent à chaque filtre.
3. **Les fiches** : pastille de modalité, mention de date, axe, bouton d'accès.

**Vue « Le calendrier »** : sessions à venir groupées par mois, puis l'encart
« Programmation en cours », puis les sessions passées.

**Deux réglages à connaître, posés le 9 novembre :**

- Le bandeau porte **Manag'Hérault 2026/2027**.
- `CAL_PASSE` vaut **`true`** : les sessions passées sont **dépliées d'emblée**.
  C'était justifié tant que l'essentiel de l'année était derrière nous.
  **À repasser à `false` quand la programmation 2027 sera versée** : un calendrier
  en service n'a pas vocation à s'ouvrir sur l'année écoulée.

**Partis pris à ne pas défaire :**

- **L'axe est une étiquette, pas un niveau de navigation.** Une ressource de l'axe 3
  peut répondre à un besoin classé en axe 1.
- **Une ressource, une fiche unique**, rattachable à plusieurs thématiques.
- **La couleur signifie toujours la modalité** sous l'en-tête. Jamais une valeur,
  jamais un axe. Et jamais la couleur seule : pastille + libellé (RGAA 3.1).
- Les filtres et la vue sont encodés dans l'URL : une référente peut envoyer un lien
  pré-filtré. **C'est pourquoi les identifiants de fiche ne se renomment pas** (voir
  section 11).

---

## 8. La charte graphique

Design system **« CD34 Formation »**, tiré de la charte de communication graphique
du Département.

| Rôle | Valeur | Contraste vérifié |
|---|---|---|
| Prune, dominante | `#C0116F` | blanc dessus 5,9:1 |
| Vert d'eau, secondaire | `#00CDAA` | **noir** dessus 8,0:1 — le blanc n'y tient pas (2,0:1) |
| Noir | `#231F20` | sur blanc 16,3:1 |
| Prune 10 % | `#F9E7F1` | fonds d'encart, texte prune 5,0:1 |

Modalités, en couleurs complémentaires de la charte : formation cyan `#00A5FF` ·
atelier rose `#FF5FB4` · guide vert `#37D232` · Lundi RH orange `#FF691E` ·
Outil'thèque jaune `#FFF500` (texte noir) · ressource rouge `#E60514` (texte blanc).

**Règles structurantes** : texte blanc uniquement sur prune · angles droits, sans
ombre ni dégradé · **Montserrat**, en remplacement de Codec Pro et Azo Sans, non
licenciées · texte ferré à gauche · titres en casse de phrase · bloc signature
« Solidarité au quotidien, écologie en actions » et « herault.fr » en pied de page ·
**thème clair unique**.

Les **six couleurs managériales** — Responsabilité `#1AB497` · Bienveillance
`#0070C0` · Confiance `#B71739` · Efficience `#ED7D31` · Respect `#687A79` ·
Agilité `#8C3475` — sont un référentiel Manag'Hérault, **distinct de la charte
CD34**. Elles n'apparaissent que dans le bandeau, où les six pétales ouvrent le
référentiel sur Intra34.

**Ne pas confondre avec `DGA_Code_couleurs.pdf`**, qui donne un prune `#B40F64`
n'appartenant pas à la charte. Deux mois de travail ont déjà été menés sur ce
mauvais prune.

---

## 9. Le filtrage d'accès — et comment tester

La page n'admet un visiteur que s'il arrive avec `?src=intra34`, depuis un domaine
`*.herault.fr`, ou s'il est déjà entré validement depuis ce navigateur. Tout autre
visiteur reçoit une page de refus aux couleurs de la charte.

Le lien posé sur Intra34 porte obligatoirement son paramètre :

```
https://manag-herault.github.io/manag-herault/?src=intra34
```

**Tout test, local ou en ligne, s'effectue avec ce paramètre.** Sans lui, on ne voit
que la page de refus et l'on conclut à tort à une panne. Inversement, **une fois le
navigateur admis, il s'en souvient** : retester le refus demande une fenêtre de
navigation privée.

**Ce dispositif ne protège rien.** GitHub Pages sert des fichiers publics ; le
filtrage s'exécute dans le navigateur du visiteur, donc après l'envoi du contenu, et
`offre.csv` reste téléchargeable par qui connaît l'adresse. Conséquence à redire à
chaque fois : **aucune donnée non diffusable dans le CSV** — ni nom de collaborateur,
ni situation individuelle.

---

## 10. Pièges techniques déjà rencontrés

1. **Fuseau horaire.** Tout calcul de date dans `index.html` passe par `Date.UTC`.
   Construire une `Date` depuis une chaîne `AAAA-MM-JJ` puis appeler `toISOString()`
   décale d'un jour hors UTC et casse le regroupement des jours consécutifs. **Ne pas
   « simplifier » ce code.**
2. **BOM et point-virgule.** Le CSV vient d'Excel français. Lire en tenant compte du
   BOM, écrire en le conservant.
3. **Libellés de thématiques câblés** dans `index.html` : voir section 5.
4. **Défaut connu, non corrigé** : sur la page de refus — celle qu'on obtient sans
   `?src=intra34` — le script lève `Cannot set properties of null (setting
   'innerHTML')`, parce qu'il cherche à garnir des éléments que cette page ne
   contient pas. Présent à l'identique depuis au moins la version 16 ; sans effet
   pour un manager arrivant par Intra34. À traiter un jour, pas en urgence.
5. **`intra34.herault.fr` interdit l'accès automatisé** par son `robots.txt`. Les
   59 liens du catalogue **n'ont jamais pu être testés** autrement qu'en vraisemblance
   — forme de l'URL, unicité de l'identifiant, cohérence du *slug* avec l'intitulé.
   Ne pas contourner la règle. Ne pas présenter ce contrôle comme une validation.
6. **Délai de publication.** GitHub Pages reconstruit le site après chaque commit :
   compter une à deux minutes, et recharger avec un paramètre quelconque pour
   contourner le cache. Une page encore ancienne n'est pas un échec de dépôt ;
   vérifier l'onglet *Actions* avant de conclure.

---

## 11. Décisions prises — ne pas les rouvrir

- **Les identifiants de fiche (`id`) ne se renomment jamais.** Ce sont des clés
  stables, et les liens pré-filtrés déjà diffusés reposent dessus. Conséquence
  assumée : `lundi-rh-5-entretien-professionnel` porte le titre « Lundi RH 3 », et
  `prevention-des-risques-professionnels` le titre « Lundi RH 2 ». Décalage interne
  au fichier, invisible pour le manager.
- **Numérotation des Lundis RH** : celle de `ManagHerault2026.xlsx` l'emporte —
  1 renfort temporaire · 2 prévention des risques professionnels · 3 entretien
  professionnel · 4 RPS · les frais de déplacement sans numéro (action suspendue).
- Pour le reste, **les libellés d'Intra34 l'emportent** : c'est ce que le manager lit
  sur sa convocation.
- **« Escale Manager »** n'est pas reconduite : retirée du catalogue.
- La modalité « Co-développement » du Genially s'appelle **« Atelier de résolution de
  situations »**.
- **« L'entretien professionnel » existe sous deux formes**, toutes deux conservées :
  la formation du parcours Hérault'Manager (axe 3) **et** le Lundi RH. Ne pas
  fusionner, ne pas reclasser.
- La fiche Agilité a été **scindée** en quatre ; « Mobiliser l'intelligence collective »
  **éclatée en trois modules**.
- Les **notes de travail du pied de page** ont été retirées : elles s'adressaient à
  l'équipe projet, pas au manager. **Ne pas les rétablir.**
- **Pas de Word ni de PDF** dans les productions. **Gamma abandonné.**
- **Hébergement GitHub Pages assumé comme public**, avec filtrage de convenance côté
  navigateur.

---

## 12. Ce qui reste ouvert

| Sujet | Action attendue |
|---|---|
| **Quelle source fait foi pour les dates** | Arbitrage MTAM entre `ManagHerault2026.xlsx` et « Événement Intra34 2026 ». Voir section 6. |
| **Test depuis un poste du Département** | Jamais fait : ouverture par le lien Intra34, rechargement, favori. |
| **Lien posé sur Intra34** | Vérifier qu'il porte bien `?src=intra34`. |
| **Compte GitHub `manag-herault`** | S'il s'agit d'une organisation, y ajouter une référente de la MTAM comme propriétaire. Ajouter aussi le compte relié à Claude en écriture dispenserait de passer par le navigateur. |
| **Scripts au dépôt** | Verser le contrôle du CSV dans un dossier `outils/` pour qu'une session Claude Code puisse l'exécuter. |
| **Hébergement sur l'intranet** | La bonne cible à terme : l'authentification du Département remplacerait le filtrage bricolé. Bloqué côté DSI. |
| **Programmation 2027** | Dès réception des vraies dates, renseigner `date` et repasser `CAL_PASSE` à `false`. |
| **41 liens à renseigner** | Travail de fond, à répartir entre les référentes. Filtrer sur « Accès → Lien à renseigner ». |
| **Vérification humaine des 59 liens** | Deux méritent un clic : l'atelier conflits (JEvent 29445393, renommé sur Intra34) et le module 2 d'intelligence collaborative (28280486, *slug* qui semble tronqué). |
| **Métadonnées manquantes** | Aucune fiche ne porte de durée, de public cible ni de contact référent. C'est ce qui sépare encore un catalogue d'un outil. |

---

## 13. Manière de travailler

Benjamin attend un **contradicteur, pas un exécutant** : commencer par l'objection la
plus solide, ne jamais valider par complaisance, **donner un niveau de confiance à
chaque réponse**, et signaler ce qui n'a pas pu être vérifié plutôt que de le
présenter comme acquis.

Français professionnel, partageable en clientèle ou en Master/MBA. **Collaborateurs**,
jamais *employés*.

Il ne lit pas le code : il ne peut donc pas auditer ce qui lui est livré. **Tester ce
qui est produit, et dire ce qui n'a pas pu l'être, n'est pas une politesse
méthodologique — c'est la seule contrepartie à cette asymétrie.** Les tests sur page
rendue ont déjà rattrapé plusieurs défauts qui seraient passés en production.

**Vérifier la source avant d'en tirer une conclusion.** Trois erreurs commises sur ce
chantier : avoir affirmé qu'`intra34.herault.fr` ne résolvait pas publiquement, alors
que c'était l'environnement d'exécution qui n'avait pas de DNS ; avoir travaillé deux
mois sur un prune relevé sur le mauvais document ; avoir proposé un second fichier CSV
pour les dates, alors que le CSV employait déjà la barre verticale pour les valeurs
multiples.
