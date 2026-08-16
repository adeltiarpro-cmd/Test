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