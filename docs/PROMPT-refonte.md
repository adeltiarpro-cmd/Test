# Prompt de refonte (2026-10-06)

Tu reprends la plateforme de formation (Next.js 15, Supabase). Lis d'abord, dans cet ordre :
docs/PROGRESS.md, docs/CONTEXT-MAP.md, puis docs/00-ORCHESTRATOR.md. Ne relis pas le master spec en entier.

Sept chantiers. Commence par me présenter un plan court par chantier (fichiers touchés,
migrations, risques) et attends mon accord avant de coder. Ordre conseillé : 2, 3, 1, 4, 5, 6, 7.

## Référence visuelle obligatoire

design-system/references/entrainement-intra-fina20205.html est l'artefact d'entraînement
fait pour mon cours de gestion financière. C'est le niveau de qualité et l'esprit que je veux.
Ouvre-le et étudie-le avant toute proposition. Ce qu'il faut en retenir :
- Fond papier, cartes blanches à bord fin, une seule couleur d'accent, titres en serif
  (Source Serif 4), texte en IBM Plex Sans, calculs en IBM Plex Mono. Thème clair et sombre.
- Barre de filtres collante : une puce par section avec pastille de couleur et compteur,
  interrupteurs (« masquer les réussis »), progression « n / total réussis ».
- Chaque exercice est une carte : code (VAN-3), section en couleur, origine de l'exercice,
  difficulté en points, barème, titre, source, énoncé avec données en gras, puis les
  questions a) b) c) avec leurs points.
- Un indice dépliable (bleu), puis une solution détaillée dépliable (vert) : calcul ligne par
  ligne aligné en police mono, résultats en gras, conclusion en une phrase, encadré « Piège ».
- Auto-évaluation : case « Réussi sans regarder la solution ».
Reprends l'esprit, pas le code. Vois aussi design-system/prep-platform et la page /style-guide.

## Chantier 1 : remplacer le lot Hull (options et dérivés)

Fichier : ingest/canonical/batch-001-markets-derivatives-hull-all.clean.json (762 items).
Constats mesurés :
- 762/762 en short_answer avec un seul key_point « Voir la solution reproduite fidèlement
  ci-dessous. ». Le correcteur exige tous ces mots : tout est noté faux.
- 698 énoncés avec retours à la ligne du PDF, 118 avec césures (U+00AD), 249 avec un
  signe $ interprété comme formule KaTeX. Formules aplaties (exposants et indices perdus).
- Environ 244 questions de calcul typées en réponse libre. 146 renvois à une table, figure
  ou équation absente. Tout dans un seul module, 36 concepts = chapitres du manuel.
- Les énoncés sont la banque d'exercices complète d'un manuel et les corrigés une copie de
  son manuel de solutions.

À faire :
1. Ne pas réparer ce lot : le remplacer par des exercices originaux qui couvrent les mêmes
   36 thèmes (payoffs, stratégies, parités, arbres binomiaux, Black-Scholes, grecques,
   futures, swaps, taux, crédit, volatilité, VaR, etc.). Énoncés, données et corrigés
   construits de zéro, chaque résultat recalculé deux fois par deux méthodes.
2. Types adaptés : numeric pour un résultat chiffré unique, exercice à étapes (chantier 3)
   pour les calculs longs, mcq pour les propriétés, réponse ouverte pour le raisonnement.
3. Formules en KaTeX, montants en « USD ».
4. Sous-chapitres (modules.level = 1) sous markets/derivatives : regrouper les 36 thèmes en
   8 à 10 sections, sur le modèle de supabase/migrations/20240015000000_corpfin_subchapters.sql.
   Prochaine migration libre : 20240018.
5. Me proposer un plan de couverture (thème, nombre d'items, types) avant de générer.
   Une fois le nouveau lot chargé, me donner la requête SQL pour retirer l'ancien
   (je l'exécute moi-même).

## Chantier 2 : questions sans bonne ni mauvaise réponse

Aujourd'hui tout est rendu en « correct / incorrect ». C'est faux pour :
- les 127 questions de fit personnelles (batch-400 à 423), contournées par un mot-clé « e » ;
- les questions ouvertes de raisonnement, où la correction par mots-clés est trop binaire.

À faire :
1. Ajouter un mode d'auto-évaluation (champ additif dans le schéma short_answer ou nouveau
   type, à toi de proposer). Pas de verdict : on affiche le corrigé et la méthode, puis je me
   note (à revoir / moyen / maîtrisé). Cette note alimente la répétition espacée.
2. Ces questions sont exclues des moyennes de réussite et comptées à part (« pratiquées »).
3. Réponses ouvertes corrigées automatiquement : afficher points couverts et manquants avec
   un score partiel, et me laisser corriger le verdict (« ma réponse était juste »).
4. Régénérer les lots de fit dans ce mode et retirer le contournement.

## Chantier 3 : exercices numériques à étapes

Je veux plus d'exercices guidés par étapes quand c'est du calcul, comme les questions
a) b) c) de l'artefact de référence.
1. Nouveau format : un énoncé commun, puis 2 à 6 étapes, chacune avec sa propre saisie
   numérique, sa tolérance, son indice et son corrigé. Une étape fausse n'empêche pas de
   continuer : on affiche la bonne valeur et la suite se corrige à partir d'elle.
2. Score par étape (crédit partiel) et repérage de l'étape où je me trompe le plus.
3. Corrigé final ligne par ligne en police mono, avec encadré « Piège ».
4. Convertir en priorité les numeric existants dont le corrigé a plusieurs étapes
   (LBO, DCF, WACC, accrétion/dilution dans les lots batch-1xx à 3xx) sans changer les
   énoncés ni les résultats, puis utiliser ce format pour les nouveaux lots.

## Chantier 4 : questions organisées par section

1. En session, chaque question affiche son fil d'Ariane : filière, chapitre, sous-chapitre, source.
2. Page de parcours des sections avec, par sous-chapitre : nombre de questions, part déjà
   vue, maîtrise, bouton pour lancer une session. Puces filtrantes avec compteurs.
3. Session sur un chapitre entier : intertitre à chaque changement de sous-chapitre.
4. Même hiérarchie pour les filières qui n'ont pas encore de sous-chapitres.

## Chantier 5 : cartes d'industries pour le consulting

Il existe déjà un explorateur de graphes avec mode à trous (STEP-06, /consulting, guides
Umbrex). Je veux une vraie façon d'apprendre une industrie. Proposition à affiner :
1. Une fiche par industrie avec quatre vues du même graphe :
   - chaîne de valeur (étapes, qui capte la marge à chaque étape) ;
   - arbre de profit (revenus et coûts décomposés, ordres de grandeur) ;
   - acteurs et forces (concurrents, clients, fournisseurs, régulation) ;
   - indicateurs clés et tendances.
2. Quatre niveaux d'apprentissage sur chaque vue : lire, compléter les nœuds masqués,
   reconstruire la vue de mémoire à partir d'une page blanche, puis mini-cas (« la marge
   baisse de 3 points, où regardes-tu ? ») qui oblige à parcourir le graphe.
3. Maîtrise par industrie et par vue, intégrée à la répétition espacée.
4. Commencer par 3 industries pour valider le format avant de généraliser.

## Chantier 6 : guide de progression

1. Une page « Par où continuer » : pour chaque filière, un parcours ordonné des
   sous-chapitres (prérequis d'abord), mon état sur chacun, et la prochaine action
   recommandée (réviser les dus, attaquer telle section, refaire les questions ratées).
2. Objectifs : date d'entretien ou d'examen optionnelle, et rythme quotidien conseillé
   pour couvrir le stock d'ici là.
3. Vue hebdomadaire : questions faites, sections avancées, points faibles récurrents.
4. S'appuyer sur module_targets, concept_mastery et review_states existants.

## Chantier 7 : refonte de l'interface

Je n'aime pas l'interface actuelle. Applique l'esprit de la référence visuelle à l'écran
de session, à l'écran de correction, au dashboard et au sélecteur de sections. Propose
2 directions avec maquette de l'écran de session et de l'écran de correction, puis attends
mon choix.

## Règles

- Migrations additives uniquement, rejouables.
- Ne jamais envoyer la solution au client avant la réponse (mapper toClientExercise).
- Interface en français, sans tiret cadratin.
- `npm run build` doit passer avant chaque commit. Pas de `git push` sans me le demander.
- À la fin de chaque chantier : entrée dans docs/PROGRESS.md (FAIT, RESTE, DÉCISIONS, FICHIERS CLÉS).
