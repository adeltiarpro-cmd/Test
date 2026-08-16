# Pipeline d'ingestion — `/ingest`

Workspace Node **jamais déployé** (pas de PDF parsing dans Vercel).  
Toutes les commandes se lancent depuis ce répertoire.

## Pré-requis

```bash
cd ingest
npm install
# .env.local à la racine du repo avec NEXT_PUBLIC_SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY
```

---

## Format des lots canoniques

Un lot = **un fichier JSON** dans `canonical/`, correspondant à **un seul module**.

```jsonc
{
  "source":  "Nom du livre / PDF source",
  "track":   "markets",              // slug de la table tracks
  "module":  "derivatives",          // slug de la table modules
  "items": [
    {
      "external_key": "markets-deriv-mcq-001",   // clé stable et unique (slug libre)
      "type":         "mcq",                       // un des 10 types ExerciseSchema
      "difficulty":   2,                           // 1-5
      "source_ref":   "Hull p. 214",               // référence optionnelle dans la source
      "concepts":     ["delta", "gamma"],           // slugs de concepts déjà en base (optionnel)
      "prompt_mdx":   "Quelle est la définition du delta ?",  // question affichée à l'étudiant
      "payload":      { /* shape définie par ExerciseSchema selon type */ },
      "solution":     { /* shape définie par ExerciseSchema selon type */ }
    }
  ]
}
```

> **`prompt_mdx`** est fusionné dans `payload` lors du chargement en base  
> (colonne `exercises.payload` stocke `{ prompt_mdx, ...payload }`).

---

## Workflow d'ingestion

```
1. Session Chat (INGEST-RUNBOOK.md) → produit canonical/<batch>.json
2. npm run validate              → valide contra ExerciseSchema
3. npm run load                  → upsert Supabase (idempotent)
4. npm run report                → met à jour docs/ingest/COVERAGE.md
```

### 1. Valider

```bash
npm run validate
# ou fichier précis :
npm run validate -- --file batch-001-fake.json
```

- Items invalides → `canonical/_rejected/<filename>-<timestamp>.json` avec erreur Zod.
- Exit code 1 si au moins un rejet. **Jamais de correction silencieuse.**

### 2. Charger

```bash
npm run load
# ou fichier précis :
npm run load -- --file batch-001-fake.json
# mode lecture seule :
npm run load -- --dry-run
```

- **Idempotent** : `ON CONFLICT (external_key) DO UPDATE` garantit qu'un réimport
  du même lot ne crée aucun doublon. La sortie indique "N nouveau(x), M inchangé(s)".
- Les concepts référencés (`concepts[]`) doivent exister en base ; ceux introuvables
  sont skippés avec un warning.

### 3. Rapport de couverture

```bash
npm run report
```

Affiche une table en console + écrit `docs/ingest/COVERAGE.md`.

### 4. Extraire un classeur Excel (pour model_templates)

```bash
npm run xls -- <workbook.xlsx> [--sheet "P&L"] [--blanks mymodel.blanks.json]
```

- Sans `--blanks` : toutes les cellules sont marquées `locked: true`.
- `mymodel.blanks.json` : `{ "blanks": ["C5", "D10", "E15"] }`.
  **Le choix des cellules à masquer est toujours manuel** (décision pédagogique).
- Sortie JSON vers stdout — copier-coller dans un batch ou piper vers la DB.

---

## Convention de nommage des lots

```
batch-<NNN>-<track>-<module>-<source-abrégée>.json
```

Ex. : `batch-002-markets-derivatives-hull-ch9.json`

## Convention de nommage des external_key

```
<track>-<module-slug>-<type>-<NNN>
```

Ex. : `markets-deriv-mcq-042`

Stable entre réimports — ne jamais changer après la première importation.

---

## Types de payload/solution supportés

Voir `packages/schemas/exercises.ts` — **source de vérité unique**.  
Ne jamais dupliquer les shapes ici.

| Type | Payload clé | Solution clé |
|---|---|---|
| `mcq` | `options`, `multiple`, `shuffle` | `correct_keys`, `explain_mdx`, `distractor_explains` |
| `numeric` | `unit`, `precision`, `tolerance` | `value`, `steps_mdx`, `formula_katex` |
| `formula_cloze` | `template_mdx`, `blanks` | `blanks: Record<key, {accepted, canonical, explain_mdx}>` |
| `excel_model` | `template_id`, `editable_cells`, `check_mode` | `cells: Record<ref, {...}>` |
| `statement_interactive` | `statement`, `lines`, `linked_checks?` | `lines: Record<key, {value, tolerance, derivation_mdx}>` |
| `graph_fill` | `graph_id`, `hidden_node_keys`, `mode` | `nodes: Record<key, {accepted_labels, explain_mdx}>` |
| `case_structuring` | `case_brief_mdx`, `expected_branches` | `rubric`, `model_answer_mdx` |
| `market_sizing` | `question`, `unit` | `tree`, `final_value`, `acceptable_range` |
| `case_math` | `prompt`, `time_limit_seconds`, `tolerance` | `value`, `steps_mdx` |
| `short_answer` | `max_words` | `key_points`, `model_answer_mdx` |
