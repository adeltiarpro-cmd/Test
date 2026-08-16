# STEP-03 — Pipeline d'ingestion (`/ingest`)

## Contexte à lire
`packages/schemas/exercises.ts` (STEP-02) + `supabase/migrations/*.sql`
(STEP-01, pour connaître les tables cibles et la contrainte `external_key unique`).

## Objectif
Construire l'outil, pas le contenu. `/ingest` est un workspace Node **séparé,
jamais déployé** (contrainte d'architecture : pas de parsing PDF/XLS dans une
fonction Vercel — timeouts et mémoire ingérables sur un livre de 600 pages).

## Tâches
1. `/ingest/scripts/validate.ts` : lit `/ingest/canonical/*.json`, valide
   chaque item contre `ExerciseSchema`, écrit les rejets dans
   `/ingest/canonical/_rejected/` avec le message d'erreur — **jamais de
   correction automatique silencieuse**.
2. `/ingest/scripts/load.ts` : upsert vers Supabase via `service_role`,
   `on conflict (external_key) do update` — c'est ce qui rend un réimport
   idempotent, condition nécessaire vu le volume (plusieurs milliers d'items,
   réimportés après correction).
3. `/ingest/scripts/xls-extract.ts` (SheetJS) : lit un classeur, produit le
   `sheet jsonb` de `model_templates` (cellules : valeur/formule/format/
   verrouillage) + repère les cellules candidates au masquage via un fichier
   de config `<modèle>.blanks.json` — le choix des cellules à masquer reste
   **manuel**, jamais deviné par heuristique (c'est la décision pédagogique
   la plus importante du modèle).
4. `/ingest/scripts/report.ts` : couverture par module/type/difficulté,
   affichée en console et écrite dans `docs/ingest/COVERAGE.md`.
5. `/ingest/README.md` : documente le contrat JSON exact (un fichier = un lot,
   `{source, track, module, items[{external_key, type, difficulty,
   source_ref, concepts[], prompt_mdx, payload, solution}]}`), pour que
   `INGEST-RUNBOOK.md` (sessions de chat séparées) puisse s'y référer sans
   avoir à relire ce step file.

## Hors périmètre
Pas d'ingestion réelle de contenu (pas de vrai PDF traité ici) — juste un lot
factice de 8-10 items couvrant plusieurs types, pour tester le pipeline.

## Definition of done
- Le lot factice s'importe sans erreur.
- Un réimport identique du même lot ne crée **aucun** doublon (test explicite).
- `report.ts` affiche une table de couverture cohérente avec le lot factice.

## À écrire dans PROGRESS.md
```
## <date> — STEP-03 — Pipeline d'ingestion
STATUT: FAIT
FAIT: validate/load/xls-extract/report fonctionnels, testé sur lot factice, idempotence vérifiée
FICHIERS CLÉS: ingest/scripts/*.ts, ingest/README.md
```
