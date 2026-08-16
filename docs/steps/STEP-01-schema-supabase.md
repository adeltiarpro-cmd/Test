# STEP-01 — Schéma Supabase, RLS, seed

## Contexte à lire
Rien d'autre que ce fichier — c'est la première session, le repo est vide.
Tout ce dont tu as besoin du master spec est recopié ci-dessous.

## Objectif
Poser tout le schéma Postgres, la RLS, et le seed initial de taxonomie.

## Tâches
1. Init repo Next.js + lien projet Supabase, `supabase/migrations/` en place.
2. Écrire les migrations SQL (numérotées, une table ou un groupe cohérent par
   fichier) pour :
   - `tracks`, `modules` (avec `parent_id`, `level` — hiérarchie chapitre/sous-chapitre),
     `module_targets` (`target_mastery numeric default 0.8`, `min_exercises int default 15`)
   - `lessons`, `concepts`, `concept_edges` (`kind` prerequisite/related, `check (source_id <> target_id)`)
   - `sources` (`kind`, `title`, `storage_path`, `meta jsonb`)
   - `exercise_type` enum (10 valeurs : `mcq, numeric, formula_cloze, excel_model,
     statement_interactive, graph_fill, case_structuring, market_sizing, case_math, short_answer`)
   - `exercises` (`payload jsonb`, `solution jsonb`, `external_key unique`,
     index GIN sur `payload` et `tags`, index sur `(module_id, type, difficulty)`)
   - `exercise_concepts`, `profiles`, `attempts`, `review_states` (FSRS-ready :
     `stability`, `difficulty_fsrs`, `reps`, `lapses`), `concept_mastery`
   - `knowledge_graphs`, `graph_nodes` (`key`, `layer`, `parent_key`), `graph_edges`
   - `model_templates` (`sheet jsonb`)
   - `invitations` (`email`, `used_at`) + trigger sur `auth.users` qui refuse
     la création de compte si l'email n'y figure pas
3. RLS :
   - Contenu (`tracks` → `sources` inclus) : lecture pour tout utilisateur
     authentifié, écriture réservée à `service_role` uniquement.
   - `attempts`, `review_states`, `concept_mastery`, `profiles` : `user_id = auth.uid()`
     en lecture ET écriture, sans exception.
4. Seed :
   - 5 tracks : `markets`, `corpfin`, `consulting`, `gmat`, `math`
   - Modules racine par sous-domaine cité dans le brief produit — pour `math`,
     3 modules explicites : `stochastic-calculus`, `linear-algebra`, `nonlinear-analysis`
   - Un `module_targets` par défaut pour chaque module créé.

## Hors périmètre
Pas de composant front. Pas de `packages/schemas` (STEP-02). Pas de données
d'exercices réelles (STEP-03 + ingestion).

## Definition of done
- `supabase db reset` passe sans erreur.
- Test manuel RLS avec 2 comptes : le compte B ne peut ni lire ni écrire les
  `attempts`/`review_states` du compte A.
- Seed visible en base (`select * from tracks` retourne 5 lignes, `modules`
  contient bien les 3 sous-modules math).

## À écrire dans PROGRESS.md
```
## <date> — STEP-01 — Schéma Supabase, RLS, seed
STATUT: FAIT
FAIT: schéma complet posé (18 tables), RLS testée avec 2 comptes, seed 5 tracks + modules math
DÉCISIONS: <si tu as dévié du schéma ci-dessus, note quoi et pourquoi>
FICHIERS CLÉS: supabase/migrations/*.sql
```
