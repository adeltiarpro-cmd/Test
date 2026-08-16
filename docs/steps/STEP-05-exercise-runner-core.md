# STEP-05 — Runner d'exercices : le socle (mcq, numeric, short_answer, formula_cloze)

## Contexte à lire
`packages/schemas/exercises.ts` (STEP-02), primitives UI + `design-system/prep-platform/MASTER.md`
(STEP-04). Pas besoin de relire le détail du pipeline d'ingestion (STEP-03) —
la forme du payload est déjà connue via les schémas Zod.

## Objectif
Ce socle couvre à lui seul GMAT, finance de marché, **et le volet "réponses
simples" de finance corpo et consulting** — c'est délibérément la priorité :
il rend la plateforme utilisable sur 4 des 5 filières dès que le contenu
arrive, avant d'investir dans les types d'exos les plus coûteux à construire.

## Tâches
1. Composant générique `<ExerciseRunner exercise={...} onSubmit={...}>` qui
   dispatch sur `exercise.type`.
2. Implémente 4 types :
   - `mcq` : options, shuffle si demandé, correction stricte sur `correct_keys`,
     affiche `distractor_explains` après soumission.
   - `numeric` : input numérique, correction avec tolérance abs/rel, barème
     partiel si `sub_answers` sont notés indépendamment.
   - `formula_cloze` : champs à trous dans le `template_mdx`, normalisation de
     l'expression (mathjs ou équivalent) avant comparaison à `canonical` —
     une comparaison de chaînes brutes est inutilisable (`EBIT*(1-t)` doit
     matcher `(1-t)*EBIT`).
   - `short_answer` : matching par mots-clés pondérés (`key_points`), pas de
     LLM à ce stade (option ajoutée en STEP-08).
3. Page `/session` : pioche des exercices dus (ou tous si aucune donnée SRS
   encore), affiche le runner, écrit dans `attempts`, met à jour
   `review_states` (grade dérivé du score) et `concept_mastery` (moyenne
   mobile pondérée) — logique simple ici, l'interleaving raffiné arrive en
   STEP-09.

## Hors périmètre
Pas de LLM. Pas d'interleaving intelligent (tri simple des dus suffit). Pas
de shuffle avancé au-delà du basique.

## Definition of done
Un utilisateur de test peut faire les 4 types d'exos sur `/session`, voir
juste/faux + explication, et vérifier en base que `attempts`, `review_states`
et `concept_mastery` se mettent bien à jour.

## À écrire dans PROGRESS.md
```
## <date> — STEP-05 — Runner d'exercices (socle)
STATUT: FAIT
FAIT: ExerciseRunner + mcq/numeric/formula_cloze/short_answer + page /session fonctionnelle
FICHIERS CLÉS: components/exercise-runner/, app/session/
```

## Après ce step
Le pipeline (STEP-03) + ce runner (STEP-05) sont en place : tu peux commencer
les sessions `docs/ingest/INGEST-RUNBOOK.md` en parallèle des steps suivants.
