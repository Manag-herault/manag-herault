# Manag'Hérault 2027/28 — déposer et mettre à jour le catalogue

Le catalogue en ligne de l'offre d'accompagnement des managers du Département de l'Hérault (MTAM, DGA Ressources humaines). Jusqu'au 11 novembre 2026, cet objet s'appelait « la boussole ».

## Les fichiers

| Fichier | Rôle | Qui y touche |
|---|---|---|
| `index.html` | La page : recherche, filtres, classement, calendrier, filtrage d'accès. Ne contient aucune donnée. | personne, sauf évolution décidée |
| `offre.csv` | Le catalogue : une ligne par fiche. **Extrait du classeur de pilotage de la MTAM, jamais modifié à la main.** | produit par extraction |
| `parametres.csv` | Adresses des boutons du bandeau NEEVA (« Ouvrir NEEVA », « Voir le tuto »). Se modifie directement sur GitHub (icône crayon), sans toucher à la page. Une adresse vide masque le bouton. | quand une adresse change |
| `robots.txt` | Interdiction d'indexation, à la racine du site | non |
| `outils/` | Extraction du CSV, contrôle avant mise en ligne, démonstration hors ligne, convertisseur sans installation | à chaque changement de schéma |

`index.html` et `offre.csv` doivent être **déposés côte à côte** et servis par un serveur web. Ouverte directement depuis le disque, la page ne peut pas lire le CSV.

## Accès — ce que le filtrage fait, et ce qu'il ne fait pas

L'adresse de publication est `https://manag-herault.github.io/manag-herault/`.

**Le lien à poser sur Intra34 est celui-ci, paramètre compris :**

```
https://manag-herault.github.io/manag-herault/?src=intra34
```

La page admet un visiteur selon trois conditions, dans cet ordre :

1. l'adresse porte `?src=intra34` ;
2. le visiteur arrive d'un site en `*.herault.fr` ;
3. le visiteur est déjà entré validement depuis ce navigateur — un favori reste donc fonctionnel.

Tout autre visiteur reçoit une page de refus. Les boutons « Copier le lien de cette sélection » et « Copier le lien vers cette fiche » ajoutent d'eux-mêmes le paramètre : un lien transmis par une référente s'ouvre donc chez son destinataire.

### Ce dispositif ne protège rien

- GitHub Pages sert des fichiers **publics**. Le filtrage s'exécute dans le navigateur, donc **après** l'envoi du contenu.
- `offre.csv` reste téléchargeable par qui connaît l'adresse.
- `robots.txt` et `noindex` sont des **demandes**, que les aspirateurs malveillants ignorent.

**Conséquence : seules dix colonnes publiables sortent du classeur.** Ni intervenant, ni référent, ni remarque, ni salle, ni effectif. Le contrôle refuse toute colonne supplémentaire.

## Mettre à jour le catalogue

1. Modifier le **classeur de pilotage** (feuille Actions, une ligne par session).
2. Extraire. **Sans Python ni Claude** : ouvrir `outils/convertisseur.html` par double-clic, y déposer le classeur ; la page contrôle, puis fournit `offre.csv` et le message de dépôt. **Avec Python** : `python3 outils/extraire_catalogue.py classeur.xlsx offre.csv`
3. Contrôler : `python3 outils/controle_csv.py offre.csv ancien-offre.csv` — aucune erreur bloquante ne doit rester ; une erreur se corrige dans le classeur, puis on extrait à nouveau.
4. Déposer `offre.csv` au même endroit. La page se met à jour au prochain chargement.

Une valeur inconnue ne casse pas la page : une modalité inconnue est rangée sous « Autres actions », un axe illisible sous « Transverse ».

## Les dix colonnes de `offre.csv`

Séparateur point-virgule, encodage UTF-8 avec BOM.

| Colonne | Contenu | Valeurs attendues |
|---|---|---|
| `id` | identifiant stable de la fiche ; sert aux liens directs. **Ne se renomme jamais.** | minuscules, chiffres, tirets |
| `titre` | intitulé affiché (validation de la direction générale, casse de phrase) | texte — obligatoire |
| `modalite` | rubrique et pastille de couleur | les douze libellés ci-dessous |
| `date` | dates des sessions — alimente le calendrier | dates séparées par ` \| `, `à venir`, ou vide |
| `axe` | étiquette d'axe | `1` · `2` · `3` · `1 et 2` · `1 et 3` · `2 et 3` · `Transverse` |
| `thematiques` | thématique de l'action (une seule) | l'un des dix-huit libellés |
| `lien` | adresse de la ressource | URL en https, ou vide |
| `type_lien` | libellé du bouton | `direct` · `inscription` · `inscription Neeva` · `plateforme` · `generique` — vide si pas de lien |
| `nouveau` | mention « *nouveau » | `oui` ou vide |
| `presentation` | présentation courte affichée sur la fiche | 300 caractères au plus, ou vide |

### Les douze modalités

Formation · Formation e-learning · Parcours Hérault Managers · Atelier d'échange de pratiques · Guide / fiche boussole · Lundi RH · Lundi RH Replay · Outil'thèque · Ressources · #Managers · Webinaire · Autres.

Même liste, même orthographe que la feuille Listes du classeur. Une modalité sans fiche n'apparaît pas dans la page. La charte du Département ne compte que six couleurs complémentaires : la couleur désigne la famille, le pictogramme et le libellé désignent la modalité.

### La colonne `date`

| Valeur | Effet |
|---|---|
| une ou plusieurs dates | une entrée par session au calendrier ; la date s'affiche sur la fiche |
| `à venir` | la fiche apparaît sous « Programmation en cours », sans date |
| *vide* | ressource accessible en permanence : absente du calendrier |

L'extraction applique trois règles : les dates saisies sortent telles quelles (hors sessions « Suspendu » ou « Annulé ») ; sans date, une action dont toutes les lignes sont « Déployé » est en accès permanent ; toute autre est « à venir ». Deux écritures de date sont lues, `2027-03-09` et `09/03/2027`. Les jours consécutifs d'une même fiche sont regroupés en une session — « 9 et 10 mars 2027 ».

## Les axes

1. Renforcer un management humain et préventif
2. Adapter les pratiques managériales aux transformations de la collectivité
3. Accompagner les managers dans l'exercice de leurs responsabilités

## Les sept raccourcis de l'en-tête

Cinq pointent vers des **libellés de thématiques**, inscrits dans `index.html` : renommer une thématique dans le classeur impose de mettre la page à jour dans le même dépôt. « Je me forme » pointe vers les trois modalités de formation ; « Les nouveautés 2027/28 » vers la colonne `nouveau`.

## Adresses pré-filtrées

Les filtres, le classement et la vue sont inscrits dans l'adresse : `?m=guide`, `?a=1`, `?t=…`, `?n=1`, `?tri=axe`, `?v=cal`, `#r-identifiant`. Les adresses diffusées avant le 11 novembre 2026 (`a=A1`, `m=formation`…) restent lues.
