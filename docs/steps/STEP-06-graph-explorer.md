# STEP-06 — Explorateur Umbrex + `graph_fill`

## Contexte à lire
Migrations `knowledge_graphs`/`graph_nodes`/`graph_edges` (STEP-01),
`packages/schemas/exercises.ts` (schéma `graph_fill`), le runner générique
(STEP-05, pour y brancher un nouveau type dans le `switch`).

## Objectif
Vue lecture des guides d'industrie Umbrex (arbre/canvas) + leur version "à
trous" branchée sur `ExerciseRunner`.

## Tâches
1. Explorateur en lecture : rendu du graphe (`layer` = profondeur, `parent_key`
   pour la hiérarchie), navigation par industrie.
2. Bascule "mode à trous" en un clic : masque `hidden_node_keys`, deux modes —
   `recall` (l'utilisateur tape le label, matching insensible à la casse +
   synonymes déclarés dans `accepted_labels`) en **défaut**, `dragdrop` (avec
   `distractors`) en option. Le mode recall est le défaut délibérément — c'est
   lui qui produit l'effort de récupération utile, pas la reconnaissance.
3. Branche `graph_fill` dans `ExerciseRunner`, écrit dans `attempts` comme les
   autres types.

## Hors périmètre
Pas de génération automatique de graphes depuis un PDF ici — remplir
`knowledge_graphs`/`graph_nodes`/`graph_edges` est un travail d'ingestion
(`INGEST-RUNBOOK.md`), en amont. Si aucun graphe réel n'a encore été ingéré,
crée-en un factice de test (une industrie, 8-10 nœuds) pour valider le composant.

## Definition of done
Navigation fluide dans un graphe existant, bascule lecture/à-trous
instantanée, soumission d'un `graph_fill` correctement notée et loguée.

## À écrire dans PROGRESS.md
```
## <date> — STEP-06 — Explorateur Umbrex + graph_fill
STATUT: FAIT
FAIT: explorateur lecture + mode à trous (recall par défaut, dragdrop en option)
FICHIERS CLÉS: components/graph-explorer/, app/consulting/[industry]/
```
