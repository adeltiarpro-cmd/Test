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

## 2026-10-08 — CHANTIER-4 — Questions organisées par section
STATUT: FAIT
FAIT: (1) Fil d'Ariane dans le runner : chaque exercice affiche "Filière › Chapitre › Sous-chapitre" en haut de sa carte. breadcrumbOf() construit à partir du moduleMap déjà chargé dans session/page.tsx, puis enrichit chaque exercice avant de le passer au client. (2) Page /sections : liste tous les sous-chapitres (ou chapitres feuilles) avec compteur de questions, barre % vu, score de maîtrise si disponible, bouton "Lancer →". Puces filtrantes par filière (navigation serveur via URL params). (3) Intertitre de section dans session-client.tsx : un séparateur "— Sous-chapitre —" apparaît entre deux exercices quand le sous-chapitre change (utile en mode "Tout le chapitre"). (4) Lien "Sections" ajouté dans la nav. `npm run build` : vert (14 routes).
RESTE:
  1. Les filières consulting/gmat/math n'ont pas de sous-chapitres (level=1) — elles apparaissent dans /sections comme chapitres feuilles dès qu'elles ont des exercices. Créer des sous-chapitres (migration 20240020) quand elles auront du contenu.
  2. La maîtrise dans /sections n'est visible que si des concepts ont été chargés en base (charger-lots.command non encore lancé sur les batch-002-*).
DÉCISIONS:
  - Pas de migration 20240020 : les filières sans sous-chapitres sont déjà gérées en fallback (module level=0 affiché comme feuille). Migration reportée au moment où du contenu est ajouté.
  - typedRoutes oblige à passer les hrefs sous forme d'objet `{ pathname, query }` dans SectionRow et les puces filtrantes.
FICHIERS CLÉS: src/components/exercise-runner/index.tsx (type Breadcrumb + affichage), src/app/session/page.tsx (breadcrumbOf + enrichedFinal), src/app/session/session-client.tsx (intertitre), src/app/sections/page.tsx (nouveau), src/components/layout/nav.tsx

---

## 2026-10-08 — CHANTIER-3 — Audit qualité : valeurs intermédiaires, arrondis, dépendances, triviaux
STATUT: FAIT
FAIT: Script `ingest/fix_audit.py` écrit et exécuté — 20 exercices corrigés dans les fichiers batch-002-*. CAT 1 (4) : valeurs intermédiaires BSM fausses dans l'énoncé corrigées (key-319 d1 0,2475→0,2239, key-351 numérateur 0,0281→0,0103/d1=0,1144/c=163, key-405 N'(d1) 0,38→0,391 et N(d2) 0,52→0,510/θ/365=-0,0122, key-632 d1=(0+0,03)/…→(0+0,035)/…=0,2475). CAT 2 (1) : key-148 236 contrats (non 235) + règle d'arrondi supérieur documentée. CAT 3 (2) : key-647 "même données que call" supprimé, key-726 structure CDO ajoutée à l'énoncé. CAT 4 (13) : 7 exercices clairs reformulés (answer littéralement lisible → calcul réel imposé) + 6 borderline (valeurs changées pour éviter la lecture directe). `npm run build` : vert.
RESTE:
  1. `npx supabase db push` pour appliquer la migration 20240019.
  2. `charger-lots.command` sur les 9 fichiers batch-002-* (762 exercices UPSERT).
  3. Test navigateur : /session filière markets → dérivés.
DÉCISIONS:
  - key-531 : answer changé de 1 (Vrai) à 0 (Non) en donnant des ρ décroissants — force l'étudiant à connaître la propriété théorique plutôt que de lire la tendance des données.
  - key-180 : exercice "vérifier V=0" remplacé par "calculer k*" (4,054%) — le k=3,5% d'origine ne donnait pas V=0 pour ces taux spots.
  - key-549 (basis=0) conservé tel quel : la base nulle est un point pédagogique valide.
FICHIERS CLÉS: ingest/fix_audit.py (nouveau), ingest/canonical/batch-002-{1..9}-der-*.json (20 items modifiés)

---

## 2026-10-07 — CHANTIER-2 — Vérification et correction des exercices numériques (dérivés)
STATUT: FAIT
FAIT: Script `ingest/verify_numeric.py` écrit et exécuté. 31 exercices corrigés sur les 335 numeric/numeric_steps des 9 fichiers batch-002-*. Corrections : 29 valeurs `solution.value` erronées (recalculées à partir des formules et des paramètres de l'énoncé), 2 exercices redesignés (key-412 : Γ 0,02→0,04 donne C=5,0 USD ; key-415 : variance→espérance gain gamma=0,0397 USD), 1 exercice numeric_steps avec réponses `null` corrigées et étape manquante ajoutée (key-409 : wA=-1333, wB=2750). Corrigés réécris ligne par ligne avec calcul explicite. 8 faux positifs détectés par la vérification automatique confirmés corrects (formules short position, profit net, strike actualisé, EAD en M USD). `npm run build` : vert.
RESTE:
  1. `npx supabase db push` pour appliquer la migration 20240019 (9 sous-chapitres dérivés).
  2. `charger-lots.command` sur les 9 fichiers batch-002-* pour ingérer les 762 exercices en base (UPSERT par external_key).
  3. Test navigateur : /session avec filière markets → dérivés.
DÉCISIONS:
  - Vérification par comparaison `\mathbf{X}` (dernière valeur en gras dans steps_mdx) vs solution.value, seuil max(tol*1,5, |val|*0,003).
  - Corrections hardcodées dans FIXES/NSTEP_FIXES après vérification mathématique indépendante — pas de correction automatique aveugle.
  - Script rejouable (idempotent) : un second run applique les mêmes valeurs sans effet de bord.
FICHIERS CLÉS: ingest/verify_numeric.py (nouveau), ingest/canonical/batch-002-{1..9}-der-*.json (31 items modifiés)

---

## 2026-10-07 — CHANTIER-1 — Remplacement des 762 exercices Hull (dérivés)
STATUT: FAIT
FAIT: 762 exercices originaux générés pour les 9 sous-chapitres de `markets/derivatives`, remplaçant les anciens exercices Hull (type `short_answer` avec faux `key_points`). UPSERT par `external_key` (`markets-derivatives-short_answer-001` à `-762`) : les clés existantes sont mises à jour en base sans recréation. Types utilisés : numeric (calculs BSM, Greeks, VaR, CDS), numeric_steps (arbres binomiaux, EWMA, LMM), mcq (définitions, propriétés), short_answer/self_eval (analyse, comparaisons). Formules KaTeX, montants en USD. 9 fichiers JSON produits dans `ingest/canonical/` : batch-002-1 (112) + batch-002-2 (50) + batch-002-3 (42) + batch-002-4 (69) + batch-002-5 (124) + batch-002-6 (67) + batch-002-7 (177) + batch-002-8 (98) + batch-002-9 (23) = 762 items. Migration additive `20240019` crée les 9 modules dérivés et leurs `module_targets`. `npm run build` : vert.
RESTE:
  1. `npx supabase db push` pour appliquer la migration 20240019 (9 sous-chapitres dérivés).
  2. `charger-lots.command` (ou `npx ts-node ingest/scripts/load.ts`) sur les 9 fichiers batch-002-* pour ingérer les 762 exercices en base (UPSERT par external_key).
  3. Test navigateur : /session avec filière markets → dérivés, vérifier que les 4 types s'affichent correctement.
DÉCISIONS:
  - Scripts générateurs écrits en blocs `items+=[...]` séparés (pas de `items[-1]` dans un littéral de liste) — évite le SyntaxError Python appris sur les batches 4 et 5.
  - Batches 4 et 5 (générés en session précédente avec `items[-1]` à l'intérieur du littéral) corrigés via `fix_batch5.py` et une transformation similaire pour le batch 4 ; les JSON résultants sont valides.
  - Batch 7 (der-exotic-models) comportait une ligne `python3 -c` parasite issue d'un heredoc mal délimité — filtrée en post-processing.
  - `scoring_mode: "self_eval"` sur tous les `short_answer` : pas de scoring automatique, corrigé passé uniquement après que l'étudiant a soumis sa réponse.
FICHIERS CLÉS: supabase/migrations/20240019000000_derivatives_subchapters.sql (nouveau), ingest/canonical/batch-002-{1..9}-der-*.json (762 items), ingest/scripts/gen-batch-002-{1..9}.py, ingest/scripts/fix_batch5.py

---

## 2026-10-06 — CHANTIER-3 — Exercice à étapes (numeric_steps)
STATUT: FAIT
FAIT: Nouveau type d'exercice numeric_steps entièrement câblé. Migration additive ALTER TYPE exercise_type ADD VALUE 'numeric_steps'. Schéma Zod complet (NumericStepsPayloadSchema, NumericStepsSolutionSchema) ajouté au discriminated union. Correction côté serveur dans scoreNumericSteps : tolérance absolue par étape, score = correct/total, isCorrect si >= 70%. stepResults (isCorrect, correctValue, solutionMdx, trapMdx) retournés dans AttemptResult. Runner NumericStepsRunner : progression séquentielle par étape avec barre de progression, indices collapsibles (bleu), soumission unique de toutes les étapes, affichage post-correction (bordure verte/rouge, valeur attendue, solution mono, boîte piège ambre). Ajout à PERSISTENT_TYPES (runner reste monté après correction pour afficher les solutions). session/page.tsx et exercise-runner/index.tsx mis à jour. tsc --noEmit : 0 nouvelles erreurs.
DÉCISIONS:
  - Soumission en une seule fois (pas de validation étape par étape côté serveur) — règle "solution jamais envoyée avant réponse" respectée ; l'UX séquentielle est purement côté client.
  - isCorrect >= 0.7 (70%) — cohérent avec partial scoring du C2.
  - numeric_steps ajouté à PERSISTENT_TYPES : le runner doit rester monté après correction pour afficher les solutions et pièges par étape.
  - NumericStepsPayloadSchema ne contient pas prompt_mdx : il est injecté par load.ts au moment de l'ingestion (payloadWithPrompt).
FICHIERS CLÉS: supabase/migrations/20240018000000_numeric_steps_type.sql (nouveau), packages/schemas/exercises.ts (+NumericSteps*), src/lib/session-actions.ts (+scoreNumericSteps, +StepResult, +stepResults dans AttemptResult), src/components/exercise-runner/runners/numeric-steps.tsx (nouveau), src/components/exercise-runner/index.tsx (+NumericStepsRunner), src/app/session/page.tsx (+numeric_steps dans SUPPORTED_TYPES)

---

## 2026-10-06 — CHANTIER-2 — Auto-évaluation (sans verdict)
STATUT: FAIT
FAIT: scoring_mode ajouté à ShortAnswerPayloadSchema (auto | self_eval | partial). self_eval : flux en 2 étapes — "Voir la correction" → révèle corrigé via peekSelfEvalAnswer (aucun attempt stocké à ce stade) → 3 boutons "À revoir / Moyen / Maîtrisé" → submitAttempt avec selfEvalRating. partial : scoreShortAnswer retourne pointResults (couvert/manqué par key_point) + bouton "Ma réponse était juste" → overrideToCorrect (reschedule SRS + WMA mastery). Statistiques dashboard non affectées (concept_mastery et review_states s'alimentent dans les deux modes). Sélecteur de confiance masqué pour self_eval (remplacé par les boutons de notation).
DÉCISIONS:
  - peekSelfEvalAnswer retourne model_answer_mdx uniquement après authentification ; appelé côté client après que l'utilisateur a rédigé sa réponse (jamais pré-chargé dans le payload → solution jamais envoyée avant la réponse).
  - overrideToCorrect utilise confidence=2 par défaut pour le reschedule SRS.
  - is_correct dans attempts reste boolean (true/false) même pour self_eval — null uniquement si l'utilisateur ferme la page avant de noter.
  - Fit batches (400-423) à régénérer en scoring_mode: 'self_eval' via sessions INGEST-RUNBOOK (hors scope code).
FICHIERS CLÉS: packages/schemas/exercises.ts, src/lib/session-actions.ts (+peekSelfEvalAnswer, +overrideToCorrect), src/components/exercise-runner/runners/short-answer.tsx, src/components/exercise-runner/index.tsx, src/components/exercise-runner/result-panel.tsx

---

## 2026-08-27 — STEP-10 — Durcissement et déploiement
STATUT: FAIT (partiel — tâches manuelles restantes documentées ci-dessous)
FAIT: Page /login complète — onglets Connexion/Créer un compte, gestion invitation error (trigger check_invitation → message clair côté UI), reset password (email envoyé via resetPasswordForEmail). .env.example documenté (4 variables : NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, ANTHROPIC_API_KEY + NEXT_PUBLIC_SITE_URL). Audit RLS : migration 20240009 couvre toutes les tables user-scoped (attempts/review_states/concept_mastery/profiles) avec user_id = auth.uid() + WITH CHECK. invitations : aucune policy user, service_role only, trigger SECURITY DEFINER — correct. Accessibilité : focus-ring visible sur Button (focus-visible:ring-2) et Input (focus:ring-2), min-h-[44px] sur les deux, aria-invalid + aria-describedby sur Input, labels htmlFor corrects.
RESTE (manuel) :
  1. npx supabase db push (migration 20240014 confidence column si pas encore appliquée)
  2. Smoke tests 10 types d'exos sur /session
  3. Déploiement Vercel : ajouter les 5 variables .env.example dans les env vars Vercel
  4. Configurer Supabase Dashboard > Authentication > URL Configuration > Site URL = URL Vercel
  5. Tester avec 2 comptes réels (toi + un ami invité)
DÉCISIONS:
  - Reset password : pas de page /auth/callback implémentée (hors scope) — Supabase envoie le lien vers NEXT_PUBLIC_SITE_URL/login, flow complet uniquement après configuration Site URL dans Supabase dashboard.
  - Signup error mapping : check sur msg.includes("invited") ET "access denied" — couvre les deux formulations possibles selon la version Supabase.
  - Pas de redirect automatique post-signup (email de confirmation d'abord) — Callout "Vérifiez votre email" affiché.
FICHIERS CLÉS: src/app/login/page.tsx (remplace version minimale STEP-05), src/app/login/actions.ts (+ signupAction + resetAction), .env.example (nouveau)

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

## 2026-08-21 — STEP-09 — SRS + pédagogie + dashboard
STATUT: FAIT
FAIT: SM-2 avec notation de confiance (1/2/3) remplace le placeholder STEP-05. Migration 20240014 ajoute `confidence` sur `attempts`. SRS : intervalles fractionnaires, `difficulty_fsrs` ajusté par confiance, cap 60 jours, état new/learning/review/relearning. Détection de leech (lapses > 4) + proposition des prérequis (`concept_edges`). Sélecteur de confiance "Au hasard / Incertain / Sûr" dans ExerciseRunner avant chaque soumission. Interleaving par `module_id` dans session/page.tsx (cap due à 7, fallback < 10). Dashboard `/dashboard` : due count, 3 concepts faibles, activité 7 jours, progression par filière avec barre target. Vue Math `/math` : concepts groupés par module, code couleur maîtrise (vert ≥80 %, ambre 50-80 %, rouge <50 %), badge "Leech", prérequis texte. Nav sticky (Dashboard / Entraînement / Consulting / Maths) dans layout global. Rappel lundi en-tête : bannière conditionnelle in-app (no cron externe nécessaire, calcul fresh à chaque load RSC).
DÉCISIONS:
  - `as unknown as T` pour les casts Supabase deep-join (concepts→modules→tracks) : les types générés Supabase auto ne sont pas présents, TypeScript ne peut pas inférer la direction FK. Aucun impact runtime.
  - Leech seuil = lapses > 3 (donc 4+ erreurs) aligné sur le spec ("> 3").
  - Dashboard track progression : agrégation concept_mastery → modules → tracks en JS après un seul deep-join Supabase. Si aucun concept ingéré, fallback Callout info.
  - `/math` montre tous les tracks math mais reste vide tant qu'aucun concept n'est ingéré (INGEST-RUNBOOK) — comportement attendu.
  - Nav masquée sur /login et /style-guide (check pathname client-side dans nav.tsx).
FICHIERS CLÉS: supabase/migrations/20240014000000_srs_confidence.sql, src/lib/srs.ts, src/lib/session-actions.ts, src/app/session/page.tsx, src/components/exercise-runner/index.tsx, src/components/exercise-runner/result-panel.tsx, src/app/dashboard/page.tsx, src/app/math/page.tsx, src/components/layout/nav.tsx, src/app/layout.tsx

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
## 2026-10-05 — STEP-09 — Sous-chapitres corpfin + tirage par spécialité
STATUT: EN COURS
FAIT: Dispositif 1 (hiérarchie à 3 niveaux) appliqué à la filière corpfin : 16 sous-chapitres (`modules.level = 1`) créés sous les 4 chapitres, avec `module_targets` par défaut. La migration rattache les 475 exercices et 99 concepts corpfin déjà chargés à leur sous-chapitre, d'après le concept de chaque exercice. Lots canoniques régénérés, un fichier par source et par sous-chapitre (batch-100 à batch-317, 498 items). Dashboard : barres de progression au niveau sous-chapitre, regroupées par chapitre, chaque titre ouvrant la session filtrée. Page /session : sélecteur filière → chapitre → sous-chapitres avec compteurs, et tirage de 10 questions dans la spécialité choisie (révisions dues, puis questions jamais vues au hasard, puis déjà vues).
RESTE:
  1. `npx supabase db push` pour appliquer la migration 20240015 (testée sur une base Postgres locale reproduisant l'état actuel, pas sur la base cloud).
  2. Test navigateur de /session et /dashboard : seul le contrôle TypeScript a été passé.
  3. Supprimer `ingest/_remplaces-par-sous-chapitres/` (anciens lots par chapitre, batch-010 à batch-037) et `ingest/_reformulees-non-chargees/`.
  4. Dispositif 2 incomplet : le dashboard affiche la moyenne dès le premier concept noté, sans attendre `min_exercises` tentatives.
  5. Sous-chapitres à créer pour les autres filières (markets, consulting, gmat, math) quand elles auront du contenu.
DÉCISIONS:
  - Tirage par spécialité : écart assumé au dispositif 4 (interleaving), ajouté comme un mode en plus. Le mode « Toutes les spécialités » garde la session mélangée d'origine, et le tirage sur un chapitre entier alterne ses sous-chapitres.
  - Le mode mélangé complète toujours avec les 10 exercices les plus récents de la base (fix STEP-08) : il ne parcourt donc pas tout le stock. Non modifié ici.
  - Slugs des sous-chapitres préfixés par chapitre (`fm-`, `val-`, `ma-`, `cs-`) à cause de la contrainte UNIQUE (track_id, slug).
  - Rattachement fait en SQL dans la migration plutôt que par rechargement des lots : un rechargement aurait recréé les concepts sous le sous-chapitre en laissant les anciens liens, donc deux concepts par exercice.
  - Un concept reste rattaché au sous-chapitre de son chapitre d'origine, même quand son nom évoque un autre chapitre (ex. `dcf` issu des questions de restructuring → `cs-restructuring`).
  - Contenu des lots d'entretiens : questions reprises des trois guides (Q&A annales, 400 Questions, Bible des entretiens), réponses rédigées à neuf et contrôlées numériquement contre les guides. Questions de fit non ingérées, faute de module.
FICHIERS CLÉS: supabase/migrations/20240015000000_corpfin_subchapters.sql, src/app/session/page.tsx, src/app/dashboard/page.tsx, ingest/canonical/batch-1xx à batch-3xx, charger-lots.command

## 2026-10-06 — STEP-09 — Compléments (dispositif 2, tirage mélangé, fit)
STATUT: EN COURS (reste le test navigateur)
FAIT: Dispositif 2 : le dashboard n'affiche la moyenne d'un sous-chapitre qu'à partir de `min_exercises` tentatives, sinon « pas assez de données (n/min) ». Mode « Toutes les spécialités » : après les révisions dues, la session se complète avec des questions jamais vues tirées dans jusqu'à 5 sous-chapitres au hasard, donc sur tout le stock. Nouveau chapitre corpfin `interview-fit` avec 6 sous-chapitres (migration 20240017) et 149 questions de fit (batch-400 à 405 : 400 Questions, 120 items ; batch-420 à 423 : Bible parties I et II, 29 items). Erreurs TypeScript préexistantes corrigées (cookies typés dans server.ts et middleware.ts, dossier ingest exclu du tsconfig racine) : `tsc --noEmit` passe sans erreur.
RESTE:
  1. `npx supabase db push` (migrations 20240015, 20240016, 20240017), puis `charger-lots.command` pour les lots de fit.
  2. Test navigateur de /session et /dashboard : seul le contrôle TypeScript a été passé.
  3. Dispositif 8 (le format suit la maîtrise) et mode examen GMAT : aucune trace dans le code, non faits.
  4. Supprimer `ingest/_remplaces-par-sous-chapitres/` et `ingest/_reformulees-non-chargees/`.
  5. Sous-chapitres des autres filières quand elles auront du contenu.
DÉCISIONS:
  - Questions de fit personnelles (127 sur 149) : pas de bonne réponse unique, donc correction volontairement indulgente (un seul point clé, mot-clé « e », toute réponse rédigée passe). Le corrigé donne la méthode et le dit en toutes lettres. Conséquence : la maîtrise affichée sur ces sous-chapitres mesure la pratique, pas la qualité. Les 22 questions de connaissance (métier, process, valorisation d'un deal) gardent de vrais mots-clés.
  - Les deux entrées de la Bible qui sont des thèmes et non des questions (« L'anglais ! », « L'actualité ») sont reprises avec une précision entre parenthèses.
  - Le signe dollar des énoncés est écrit « USD » (le rendu KaTeX interprète le signe).
FICHIERS CLÉS: supabase/migrations/20240017000000_corpfin_fit_chapter.sql, ingest/canonical/batch-4xx, src/app/dashboard/page.tsx, src/app/session/page.tsx

## 2026-10-06 — STEP-11 — Formulaire d'ajout manuel (admin)
STATUT: EN COURS (code écrit, non testé dans le navigateur)
FAIT: Colonne `profiles.is_admin` et trigger qui interdit à un utilisateur de se promouvoir (migration 20240016). Middleware : 403 sur /admin pour un non-admin. Pages /admin/exercises (liste des exercices manuels, édition, suppression), /admin/exercises/new et /admin/exercises/[id]. Formulaire : type, module, difficulté, énoncé, payload et solution en JSON avec squelette pré-rempli et validation Zod en direct, aperçu via ExerciseRunner (prop `preview`, aucune tentative enregistrée). Enregistrement par action serveur qui revérifie l'admin et le schéma, sous la source « Mes propres exercices » (kind `own`), clé `manual-<uuid>`.
RESTE:
  1. `npx supabase db push`, puis dans le SQL Editor : `UPDATE profiles SET is_admin = true WHERE id = (SELECT id FROM auth.users WHERE email = '...');`
  2. `SUPABASE_SERVICE_ROLE_KEY` dans `.env.local` (et sur Vercel).
  3. Test navigateur : création, aperçu, édition, suppression, 403 avec un compte non admin.
DÉCISIONS:
  - Payload et solution saisis en JSON à partir d'un squelette dérivé des schémas Zod, plutôt qu'un champ de formulaire par propriété : un seul formulaire couvre les 10 types et suit les schémas sans maintenance.
  - Pas d'aperçu pour `graph_fill` et `excel_model` (dépendent d'un graphe ou d'un template en base).
  - La note de source est rangée dans les tags (`ref:<texte>`), le concept est facultatif.
  - 403 renvoyé par le middleware, et vérification refaite dans chaque action serveur.
FICHIERS CLÉS: supabase/migrations/20240016000000_admin_flag.sql, src/middleware.ts, src/lib/admin/, src/lib/supabase/admin.ts, src/app/admin/exercises/, src/components/exercise-runner/index.tsx
