# STEP-08 — Cas structurés : structuring, market sizing, case math

## Contexte à lire
`packages/schemas/exercises.ts` (schémas `case_structuring`, `market_sizing`,
`case_math`), le runner générique (STEP-05).

## Objectif
Les 3 derniers types d'exos, plus le bouton optionnel de feedback qualitatif
via LLM — **à la demande, jamais systématique**, pour maîtriser le coût.

## Tâches
1. `case_math` : chrono strict, pas de calculatrice, tolérance sur `value`,
   focus vitesse.
2. `case_structuring` : correction en deux temps —
   - matching mots-clés/rubrique contre `rubric` (déterministe, instantané,
     gratuit) : coche chaque `branch_key` couverte, pondère par `weight`,
     signale les `must_have` manqués
   - bouton "feedback détaillé" **explicite** → appel API Anthropic optionnel
     pour un retour qualitatif sur la structure (MECE, priorisation,
     hypothèses), comparé à `model_answer_mdx`
3. `market_sizing` : ce qui est noté est l'**ordre de grandeur** et la
   cohérence de l'arbre, pas le chiffre exact — vérifie `final_value` contre
   `acceptable_range`, pas une égalité stricte. Même bouton de feedback
   qualitatif optionnel que `case_structuring`.

## Hors périmètre
Le rubric-matching n'a pas besoin d'être parfait dès ce step — une correction
par mots-clés simple suffit, elle s'affinera avec plus de contenu réel ingéré.

## Definition of done
Les 3 types fonctionnent avec correction déterministe par défaut. Le bouton
feedback LLM appelle l'API uniquement sur clic et affiche un retour qualitatif
distinct de la correction automatique.

## À écrire dans PROGRESS.md
```
## <date> — STEP-08 — Cas structurés
STATUT: FAIT
FAIT: case_math/case_structuring/market_sizing + bouton feedback LLM à la demande
FICHIERS CLÉS: components/case-runner/, app/api/case-feedback/
```
