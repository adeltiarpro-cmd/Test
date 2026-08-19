# Journal de progression

Une entrée par session, ajoutée en fin de session, jamais réécrite. Format
fixe pour rester grep-able. Les entrées d'ingestion (livres/PDF traités) vont
dans `docs/ingest/COVERAGE.md`, pas ici — ce journal ne suit que le build.

Format d'entrée :

```
## AAAA-MM-JJ — STEP-XX — <titre court>
STATUT: FAIT | EN COURS
FAIT: <ce qui a été livré, en une ou deux lignes, factuel>
RESTE: <si EN COURS, point de reprise précis>
DÉCISIONS: <tout choix qui dévie du step file ou du master spec, et pourquoi>
FICHIERS CLÉS: <chemins créés/modifiés, pour que la session suivante sache où regarder>
```

---

## 2026-08-14 — STEP-01 — Schéma Supabase, RLS, seed
STATUT: FAIT
FAIT: scaffold Next.js 15 + App Router posé (src/, supabase/config.toml, package.json, Supabase client SSR) ; 10 migrations SQL créées — 18 tables + enum exercise_type (10 valeurs) + 2 triggers (check_invitation BEFORE, handle_new_user AFTER) + RLS complète + seed 5 tracks + 15 modules racine (dont 3 math explicites) + module_targets par défaut.
DÉCISIONS:
  - tags exercises : text[] plutôt que jsonb — type natif tableau, GIN fonctionne mieux ; Zod le validera au STEP-02.
  - difficulty exercises : smallint CHECK(1..5) — non précisé dans le spec, choix d'implémentation.
  - state smallint ajouté à review_states pour l'algo FSRS (new/learning/review/relearning) — nécessaire au STEP-09.
  - Trigger handle_new_user (AFTER INSERT auth.users → profiles) ajouté — non explicité dans le spec mais indispensable au flux auth.
  - supabase db reset + test RLS à valider manuellement après connexion au projet Supabase cloud (Docker absent en local).
FICHIERS CLÉS: supabase/migrations/20240001-20240010*.sql, src/lib/supabase/client.ts, src/lib/supabase/server.ts, src/middleware.ts
## 2026-08-14 — STEP-01 — Schéma Supabase, RLS, seed
STATUT: FAIT
FAIT: schéma complet posé, RLS testée avec 2 comptes réels (isolation confirmée sur profiles
via set local role authenticated + request.jwt.claims), seed 5 tracks + 17 modules
(dont 3 modules math : stochastic-calculus, linear-algebra, nonlinear-analysis)
DÉCISIONS: pas de colonne d'ordre sur tracks (id/slug/title/created_at seulement) — trier par
slug/title si besoin. Sur modules, la colonne de tri s'appelle "order" et non "position" —
toujours l'entourer de guillemets doubles dans les requêtes SQL futures.
FICHIERS CLÉS: supabase/migrations/20240001-20240010, projet cloud lié (ref: eeosjzhewztxhjnhwaxw)

## 2026-08-14 — STEP-02 — Schémas Zod
STATUT: FAIT
FAIT: 10 schémas Zod (payload + solution) + union discriminée ExerciseSchema + 10 fixtures valides + 10 fixtures invalides — 22/22 tests verts (vitest 2.1.9, 10 positifs + 10 négatifs + 2 discriminateur)
DÉCISIONS:
  - ExcelCellSolution : formula/value/tolerance/explain_mdx tous optionnels — pas de .refine() pour forcer "au moins un", laissé souple pour le runner.
  - Autoprefixer ajouté en devDependency (peer manquante de Tailwind, bloquait le démarrage de vitest via PostCSS).
  - vitest.config.ts : css:false pour éviter le traitement CSS en tests unitaires.
  - Alias TypeScript @prep/schemas → packages/schemas/exercises.ts ajouté dans tsconfig.json et vitest.config.ts.
FICHIERS CLÉS: packages/schemas/exercises.ts, packages/schemas/__fixtures__/*.ts, packages/schemas/__tests__/exercises.test.ts

## 2026-08-19 — STEP-06 — Explorateur Umbrex + graph_fill
STATUT: FAIT
FAIT: Explorateur de graphes (tree CSS récursif, couleur par layer) avec bascule lecture/à-trous instantanée. Recall par défaut (input inline dans l'arbre), dragdrop en option (click-to-select + click-to-place). graph_fill branché dans ExerciseRunner + scoreGraphFill() dans session-actions (matching case-insensitive sur accepted_labels). Session RSC pré-fetche le graphe pour les graph_fill (client reçoit _graphData). Pages /consulting (liste) + /consulting/[graphId] (explorateur). Migration 20240011 : graphe test Consulting Problem-Solving 12 nœuds + exercice graph_fill de seed (external_key seed-graph-fill-consulting-ps-001).
DÉCISIONS:
  - Pas de D3/force-directed — rendu en CSS via parent_key (arbre). Suffisant pour les graphes hiérarchiques Umbrex.
  - dragdrop implémenté comme click-select + click-place (accessible, sans librairie DnD).
  - Graph data pré-fetché côté RSC session (pas de fetch client-side dans le runner) → pas de useEffect asynchrone dans ExerciseRunner.
  - buttonVariants sur Link (pas asChild — Button ne l'implémente pas).
  - typedRoutes: .next/types générés par premier passage dans next dev avant tsc --noEmit.
FICHIERS CLÉS: supabase/migrations/20240011000000_seed_graph_test.sql, src/lib/graph-actions.ts, src/components/graph-explorer/{index,graph-tree,dragdrop-panel}.tsx, src/components/exercise-runner/runners/graph-fill.tsx, src/app/consulting/{page,[graphId]/page}.tsx

## 2026-08-16 — STEP-05 — Runner d'exercices (socle)
STATUT: FAIT
FAIT: ExerciseRunner + 4 runners (mcq, numeric, formula_cloze, short_answer) + page /session fonctionnelle. Scoring server-side (solution jamais transmis au client). Writes vers attempts + review_states (scheduling simplifié : +stability jours si correct, +10 min si raté) + concept_mastery (WMA α=0.3). MathText renderer KaTeX custom (pas de react-markdown). /session → 307 redirect si non authentifié, 200 après auth.
DÉCISIONS:
  - Validation server-side via server action (solution reste sur serveur). formula_cloze : mathjs `evaluate` avec comparaison Monte Carlo 3 points (gère commutativité EBIT*(1-t) ↔ (1-t)*EBIT + fallback string). short_answer : scoring par mots-clés pondérés (key_points) opérationnel dès le départ.
  - KaTeX via dangerouslySetInnerHTML avec échappement HTML des segments plain text — évite ESM compat issues de react-markdown.
  - Shuffle MCQ via useMemo (stable par render, aléatoire au montage).
  - review_states.stability incrémenté de 1 par bonne réponse, plafonné à 30 ; due_at = now + stability*24h.
  - concept_mastery : STEP-09 raffinera l'interleaving, ici simple WMA sur mastery_score.
FICHIERS CLÉS: src/lib/session-actions.ts, src/components/exercise-runner/{index,mdx,result-panel}.tsx, src/components/exercise-runner/runners/{mcq,numeric,formula-cloze,short-answer}.tsx, src/app/session/{page,session-client}.tsx, src/app/login/{page,actions}.tsx
NOTE: /login est une page minimale STEP-05 (email+password → /session). STEP-10 la remplacera par la version complète (signup, invitations, reset password).

## 2026-08-16 — STEP-04 — Design system + primitives UI
STATUT: FAIT
FAIT: design-system/prep-platform/MASTER.md généré (Minimalism & Swiss Style, indigo #4F46E5, orange #EA580C, Fira Sans/Fira Code, density 8). 3 page-overrides persistées (model-workshop, graph-explorer, exam-session). 6 primitives UI créées avec CVA + tailwind-merge : Button (5 variants, 4 tailles, aria-label icon-only), Input (label, hint, error, startIcon, aria-invalid), Card (6 sous-composants), Table (tabular-nums, overflow-auto), Badge (6 variants), Callout (info/success/warning/error). Page /style-guide opérationnelle (HTTP 200, 0 erreur TS sur les fichiers créés). Fonts chargées via next/font/google (swap). Tokens CSS injectés via globals.css + tailwind.config.ts.
DÉCISIONS:
  - Typographie surchargée : MASTER suggère Baloo 2/Comic Neue (trop enfantin pour finance). Remplacé par Fira Sans (corps) + Fira Code (monospace/chiffres). Meilleure lisibilité tabulaire.
  - on-accent = #000000 (noir) sur orange #EA580C — contraste 5.92:1, conforme 4.5:1 WCAG AA. MASTER indiquait white, corrigé.
  - cn() sans clsx (clsx non installé) : filter type-guard + twMerge suffisant pour les cas CVA.
  - Taille min 44×44px respectée via min-h-[44px] min-w-[44px] sur Button et Input.
FICHIERS CLÉS: tailwind.config.ts, src/app/globals.css, src/app/layout.tsx, src/lib/cn.ts, src/components/ui/{button,input,card,table,badge,callout}.tsx, src/app/style-guide/page.tsx, design-system/prep-platform/MASTER.md

## 2026-08-14 — STEP-03 — Pipeline d'ingestion
STATUT: FAIT
FAIT: validate/load/report/xls-extract fonctionnels. Testé sur lot factice
batch-001-fake.json (8 items : 3 mcq, 2 numeric, 1 formula_cloze, 1 case_math,
1 short_answer ; difficulté 1×2, 2×4, 3×2). Idempotence vérifiée (1er import :
avant=0 après=8 ; réimport : avant=8 après=8, 0 nouveau/8 inchangés).
report.ts génère docs/ingest/COVERAGE.md automatiquement.
DÉCISIONS: tsconfig.json de /ingest nécessitait un rootDir explicite pour
référencer packages/schemas/exercises.ts hors du dossier — corrigé.
FICHIERS CLÉS: ingest/scripts/{validate,load,report,xls-extract}.ts,
ingest/README.md, ingest/canonical/batch-001-fake.json, docs/ingest/COVERAGE.md

## 2026-08-19 — STEP-08 — Cas structurés
STATUT: FAIT
FAIT: case_math (chrono strict, auto-submit à expiration), case_structuring (matching mots-clés/rubrique avec must_have, bouton feedback IA via Haiku à la demande), market_sizing (fourchette acceptable_range, bouton feedback IA à la demande). API route POST /api/case-feedback (Anthropic SDK, auth Supabase, Haiku 4.5). 3 exercices seed migration 20240013 (profitabilité, structuration consulting, cafés France). case_structuring et market_sizing persistent comme les grid types (rubricResults + LLM button visibles après submit). case_math non-persistent (ResultPanel standard).
DÉCISIONS: runners case_structuring + market_sizing persistents (ajoutés à PERSISTENT_TYPES dans ExerciseRunner) — affichent rubric/résultat inline dans le runner ET ResultPanel (réponse modèle). LLM Haiku 4.5 car coût maîtrisé ; appel uniquement sur clic explicite. scoreCaseStructuring : is_correct = score ≥ 0.7 ET tous les must_have couverts. scoreMarketSizing : inRange = final_value dans acceptable_range.
FICHIERS CLÉS: src/components/exercise-runner/runners/{case-math,case-structuring,market-sizing}.tsx, src/app/api/case-feedback/route.ts, src/lib/session-actions.ts, supabase/migrations/20240013000000_seed_case_exercises.sql

## 2026-08-17 — STEP-07 — Atelier de modèles + comptes interactifs
STATUT: FAIT
FAIT: HyperFormula intégré (client + serveur), excel_model (3 check_mode, feedback
cellule par cellule confirmé vert/orange/rouge avec message explicite "valeur
juste — formule non conforme"), statement_interactive avec linked_checks
dynamiques (ni_flows_to_re actif, contrôle en direct confirmé avant validation).
Testé de bout en bout sur /session, attempts confirmés en base pour les 2 types.
DÉCISIONS: comparaison de formule suit le pattern Monte Carlo du STEP-05, via
HyperFormula au lieu de mathjs. linked_checks 'balance' et 'cf_ties_to_cash'
détectés dynamiquement mais sans logique de calcul — à coder côté composant
(pas côté ingestion) le jour où un template bilan/cash-flow est ajouté.
FICHIERS CLÉS: src/components/model-workshop/, src/components/statement-interactive/,
src/lib/model-actions.ts, supabase/migrations/20240012_*.sql

## 2026-08-19 — STEP-06 — Explorateur Umbrex + graph_fill (corrections post-session)
STATUT: FAIT
FAIT: explorateur lecture + mode à trous (recall par défaut, dragdrop en option),
graph_fill branché sur ExerciseRunner et scoreGraphFill(), testé de bout en bout
sur /consulting (attempts + review_states confirmés en base)
DÉCISIONS: migration 20240011 avait un littéral tableau malformé sur la colonne
tags (chaîne JSON au lieu de array Postgres) — corrigé en array['...','...'].
buttonVariants() exporté depuis button.tsx ("use client") était appelé directement
depuis le RSC /consulting/page.tsx — corrigé en extrayant buttonVariants dans
src/components/ui/button-variants.ts (sans directive client) ; button.tsx l'importe
et le ré-exporte pour ne rien casser côté composants clients.
Prochaine migration disponible : 20240012 (20240011 déjà pris par ce seed de test).
FICHIERS CLÉS: src/components/ui/button-variants.ts (nouveau),
src/components/ui/button.tsx (import depuis button-variants),
src/app/consulting/page.tsx, src/app/consulting/[graphId]/page.tsx,
supabase/migrations/20240011000000_seed_graph_test.sql