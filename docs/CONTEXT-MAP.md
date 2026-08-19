# Carte de contexte — quel document à quel moment

Coche la case au fur et à mesure. Une ligne = une session de travail. Ne saute
pas de case tant que la précédente n'est pas cochée, sauf indication contraire.

| # | Step | Type de session | Fichiers à lire/donner | À NE PAS lire | Sortie | Fait |
|---|------|------------------|--------------------------|----------------|--------|------|
| 1 | `STEP-01-schema-supabase.md` | Claude Code | Le step file seul (auto-suffisant) | `00-MASTER-SPEC.md` en entier | Migrations SQL + RLS + seed | ☑ |
| 2 | `STEP-02-zod-schemas.md` | Claude Code | Le step file + `supabase/migrations/*.sql` | Le reste du repo | `packages/schemas/exercises.ts` + fixtures | ☑ |
| 3 | `STEP-03-ingestion-pipeline.md` | Claude Code | Le step file + `packages/schemas/exercises.ts` + migrations | — | `/ingest` fonctionnel + `ingest/README.md` | ☑ |
| 4 | `STEP-04-design-system.md` | Claude Code | Le step file + skill `ui-ux-pro-max` | Tout le reste (indépendant) | `design-system/prep-platform/MASTER.md` + primitives UI | ☑ |
| 5 | `STEP-05-exercise-runner-core.md` | Claude Code | Le step file + `exercises.ts` + primitives UI | Détail du pipeline d'ingestion | Runner `mcq`/`numeric`/`short_answer`/`formula_cloze` + page `/session` | ☑ |
| — | **`INGEST-RUNBOOK.md`** | **Chat normal** (upload PDF) | Le runbook + le PDF/chapitre du jour | Le reste du repo — pas nécessaire | 1 fichier JSON canonique par lot, à coller dans `/ingest/canonical/` puis charger avec `load.ts` | récurrent, dès que STEP-03 est fait |
| 6 | `STEP-06-graph-explorer.md` | Claude Code | Le step file + migrations `knowledge_graphs/*` + `exercises.ts` | — | Explorateur Umbrex + `graph_fill` | ☑ |
| 7 | `STEP-07-excel-model-statements.md` | Claude Code | Le step file + migrations `model_templates` + `exercises.ts` | — | Atelier de modèles (HyperFormula) + comptes de résultat interactifs | ☑ |
| 8 | `STEP-08-case-formats.md` | Claude Code | Le step file + `exercises.ts` | — | `case_structuring`/`market_sizing`/`case_math` + bouton feedback LLM | ☐ |
| 9 | `STEP-09-srs-pedagogy-dashboard.md` | Claude Code | Le step file + migrations `review_states/concept_mastery/module_targets` | — | SRS + 8 dispositifs pédagogiques + dashboard + vue Math | ☐ |
| 10 | `STEP-10-hardening-deploy.md` | Claude Code | Le step file, revue transverse | — | Audit RLS, invitations, checklist skill, déploiement Vercel | ☐ |
| 11 | `STEP-11-admin-form.md` | Claude Code | Le step file + `exercises.ts` + ExerciseRunner (STEP-05) | — | Formulaire admin de saisie manuelle + colonne `is_admin` | ☐ |

## Trois principes qui font tenir ce système

**Le master spec (`00-MASTER-SPEC.md`) n'est lu en entier qu'une seule fois, au
STEP-01.** Après ça, chaque step file contient déjà la tranche du spec dont il
a besoin, recopiée. Le relire en entier à chaque session serait justement le
problème que ce découpage résout.

**`PROGRESS.md` est la mémoire, pas le code.** Une session ne doit jamais avoir
à relire tout `src/` pour comprendre ce qui a été décidé — `PROGRESS.md` le
dit en quelques lignes par step.

**L'ingestion de contenu est hors numérotation.** Ce n'est pas un step de
build, c'est un flux continu : dès que `/ingest` existe (fin STEP-03), tu peux
lancer autant de sessions `INGEST-RUNBOOK.md` que tu as de livres/PDF, en
parallèle des steps 4 à 10. Une session = un livre ou un chapitre, jamais plus
— c'est ce qui garde chaque session d'ingestion dans un budget de contexte
raisonnable.
