# STEP-07 — Atelier de modèles Excel + comptes de résultat interactifs

## Contexte à lire
Migration `model_templates` (STEP-01), schémas `excel_model` et
`statement_interactive` (STEP-02), le runner générique (STEP-05).

## Objectif
Le morceau techniquement le plus lourd du projet, volontairement placé après
que le socle simple (STEP-05) ait déjà rendu la plateforme utilisable.

## Tâches
1. Intègre **HyperFormula** (moteur de formules compatible Excel) + une grille
   éditable (react-datasheet-grid ou équivalent).
2. `excel_model` : charge `model_templates.sheet` dans HyperFormula, rend les
   `given_cells` en lecture seule et les `editable_cells` en saisie libre
   (formule ou valeur), recalcule en direct. Correction :
   - `check_mode: 'value'` → tolérance numérique sur le résultat calculé
   - `check_mode: 'formula'` → comparaison de l'**AST normalisé** de la
     formule (références relatives/absolues indifférentes sauf si l'exo porte
     précisément dessus)
   - `both` → les deux, avec un feedback distinct "bonne valeur, mauvaise
     construction"
   - Feedback **cellule par cellule** (vert / orange "valeur juste, formule
     non-conforme" / rouge) — jamais un simple faux global.
3. `statement_interactive` : rend les `lines` (compte de résultat / bilan /
   cash-flow) avec les niveaux d'indentation, calcule les `linked_checks` en
   temps réel (`balance`, `cf_ties_to_cash`, `ni_flows_to_re`) et les affiche
   comme indicateurs d'intégrité **avant même la validation** — c'est ce qui
   distingue un vrai exercice d'analyse financière d'un QCM déguisé.

## Hors périmètre
Pas d'extraction XLS ici (déjà fait côté pipeline au STEP-03) — ce step
consomme des `model_templates` déjà en base. Si aucun modèle BIWS réel n'a
encore été ingéré, crée 1-2 templates factices pour valider les composants.

## Definition of done
Un utilisateur remplit des cellules, voit le recalcul live, obtient un
feedback cellule par cellule. Un compte de résultat interactif signale
visuellement une balance qui ne tombe pas juste.

## À écrire dans PROGRESS.md
```
## <date> — STEP-07 — Atelier de modèles + comptes interactifs
STATUT: FAIT
FAIT: HyperFormula intégré, excel_model (3 check_mode) + statement_interactive avec linked_checks live
FICHIERS CLÉS: components/model-workshop/, components/statement-interactive/
```
