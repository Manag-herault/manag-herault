# Boussole Manag'Hérault — déposer et mettre à jour

## Les deux fichiers

| Fichier | Rôle | Qui y touche |
|---|---|---|
| `index.html` | La page : mise en page, filtres, moteur de recherche. Ne bouge plus. | personne, sauf refonte |
| `offre.csv` | Le catalogue : une ligne par ressource. | la MTAM, dans Excel |

Les deux doivent être **déposés côte à côte**, dans le même dossier, et servis par un serveur web (intranet, GitHub Pages, Codeberg Pages…). Ouverte directement depuis le disque, la page affiche un message d'erreur : un navigateur refuse de lire un fichier voisin en `file://`.

Un troisième fichier, `robots.txt`, doit être déposé **à la racine du site**.

## Accès — ce que le filtrage fait, et ce qu'il ne fait pas

L'adresse de publication est `https://manag-herault.github.io/manag-herault/`.

**Le lien à poser sur Intra34 est celui-ci, paramètre compris :**

```
https://manag-herault.github.io/manag-herault/?src=intra34
```

Le paramètre `?src=intra34` n'est pas décoratif : il garantit l'ouverture même si l'intranet n'envoie pas d'en-tête `Referer`. Sans lui, une partie des managers verrait la page de refus.

La page admet un visiteur selon trois conditions, dans cet ordre :

1. l'adresse porte `?src=intra34` ;
2. le visiteur arrive d'un site en `*.herault.fr` (Intra34, Otium) ;
3. le visiteur est déjà entré validement depuis ce navigateur — un favori reste donc fonctionnel.

Tout autre visiteur reçoit une page de refus renvoyant vers Intra34. En parallèle, `robots.txt` et les balises `noindex` écartent les moteurs de recherche et les robots d'entraînement conformes.

### Ce dispositif ne protège rien

À dire clairement à la MTAM, car la confusion est facile :

- GitHub Pages sert des fichiers **publics**. Le filtrage s'exécute dans le navigateur du visiteur, donc **après** l'envoi du contenu.
- `offre.csv` reste téléchargeable directement par qui connaît l'adresse, filtrage ou non.
- `robots.txt` et `noindex` sont des **demandes** : les moteurs sérieux les respectent, les aspirateurs malveillants les ignorent.

**Conséquence : ne placer dans `offre.csv` aucune donnée qui ne pourrait pas être rendue publique** — ni nom de collaborateur, ni situation individuelle, ni information interne sensible. Un catalogue d'offre de formation ne pose pas de difficulté ; une liste nominative en poserait une.

Si un besoin réel de confidentialité apparaît, il faut changer d'hébergement : dépôt des deux fichiers directement sur l'intranet, derrière l'authentification du Département.

## Mettre à jour le catalogue

1. Ouvrir `offre.csv` dans Excel (il s'ouvre correctement en français : séparateur `;`, encodage UTF-8 avec BOM).
2. Corriger, ajouter ou supprimer des lignes.
3. **Enregistrer sous → CSV UTF-8 (délimité par points-virgules)**.
4. Redéposer le fichier au même endroit. La page se met à jour au prochain chargement.

Aucune ligne de code n'est à toucher. Une valeur inconnue dans `modalite`, `effort`, `axe` ou `type_lien` ne casse pas la page : elle bascule sur une valeur par défaut.

## Les colonnes

| Colonne | Contenu | Valeurs attendues |
|---|---|---|
| `id` | identifiant unique, sert aux liens directs vers une fiche | texte sans espace |
| `titre` | intitulé affiché | texte libre — **obligatoire** |
| `modalite` | pastille de couleur | `formation` · `atelier` · `guide` · `lundirh` · `outil` · `ressource` |
| `effort` | filtre « Effort demandé » | `lire` · `animer` · `participer` · `former` · `accompagne` |
| `disponibilite` | mention sous la fiche | `immediat` · `session` |
| `axe` | étiquette d'axe | `A1` · `A2` · `A3` · `A1+A2` · `A1+A3` · `TR` |
| `thematiques` | une ou plusieurs, séparées par ` \| ` | texte libre — l'ordre d'apparition dans le fichier fixe l'ordre du filtre |
| `elearning` | badge « e-learning » | `oui` ou vide |
| `lien` | adresse de la ressource | URL complète, ou vide |
| `type_lien` | libellé du bouton | `direct` · `inscription` · `plateforme` · `generique` — vide si pas de lien |

## Les axes

- **A1** — Renforcer un management humain et préventif
- **A2** — Adapter les pratiques managériales aux transformations de la collectivité
- **A3** — Accompagner les managers dans l'exercice de leurs responsabilités
- **TR** — Ressource transverse

## Ajouter une thématique

Écrivez simplement son libellé dans la colonne `thematiques` d'une ligne. Elle apparaît dans le filtre, à la place où la première ligne qui la porte se trouve dans le fichier. Pour la placer plus haut dans la liste, remontez cette ligne dans le CSV.

## Les six raccourcis « Je… »

Ils sont définis dans `index.html` et pointent vers des **libellés de thématiques**. Si vous renommez une thématique dans le CSV, prévenez : le raccourci correspondant doit être mis à jour dans la page.
