# STEP-02 — Schémas Zod des 10 types d'exercices

## Contexte à lire
`supabase/migrations/*.sql` — en particulier la forme de la table `exercises`
(`payload jsonb`, `solution jsonb`). Rien d'autre.

## Objectif
`packages/schemas/exercises.ts` : un schéma Zod par type d'exercice, une union
discriminée, et des fixtures de validation. C'est la source de vérité unique
utilisée ensuite par le validateur d'ingestion, les composants de rendu et le
moteur de correction — ne la duplique jamais ailleurs.

## Tâches
Écrire un schéma Zod pour chacun des 10 types, avec exactement ces champs
`payload`/`solution` (résumé — adapte la syntaxe Zod, la structure ne bouge pas) :

- **numeric** : `payload{variables?, unit, precision, tolerance{type:'abs'|'rel', value}, sub_answers?}` / `solution{value, sub_values?, steps_mdx, formula_katex}`
- **formula_cloze** : `payload{template_mdx, blanks[{key, kind:'token'|'expression'|'number', hint?, options?}]}` / `solution{blanks: Record<key,{accepted[], canonical, explain_mdx}>}`
- **excel_model** : `payload{template_id, editable_cells[], given_cells?, check_mode:'formula'|'value'|'both'}` / `solution{cells: Record<ref,{formula?, value?, tolerance?, explain_mdx?}>}`
- **statement_interactive** : `payload{statement:'is'|'bs'|'cf', lines[{key,label,level,given?,editable,formula_hint?}], linked_checks?[{rule:'balance'|'cf_ties_to_cash'|'ni_flows_to_re'}]}` / `solution{lines: Record<key,{value,tolerance,derivation_mdx}>}`
- **graph_fill** : `payload{graph_id, hidden_node_keys[], mode:'recall'|'dragdrop', distractors?[]}` / `solution{nodes: Record<key,{accepted_labels[], explain_mdx}>}`
- **case_structuring** : `payload{case_brief_mdx, expected_branches, time_limit_seconds?}` / `solution{rubric[{branch_key,label,keywords[],weight,must_have}], model_answer_mdx}`
- **market_sizing** : `payload{question, allowed_assumptions?[], unit}` / `solution{tree[{key,label,value,unit}], final_value, acceptable_range:[min,max], reasoning_mdx}`
- **case_math** : `payload{prompt, time_limit_seconds, tolerance}` / `solution{value, steps_mdx}`
- **mcq** : `payload{options[{key,text_mdx}], multiple, shuffle}` / `solution{correct_keys[], explain_mdx, distractor_explains}`
- **short_answer** : `payload{max_words}` / `solution{key_points[{text,weight}], model_answer_mdx}`

Exporte `ExerciseSchema = z.discriminatedUnion('type', [...])`.
Écris un exemple valide par type dans `__fixtures__/`.
Écris un test qui valide chaque fixture positive et rejette une fixture
volontairement invalide par type (10 cas positifs + 10 négatifs minimum).

## Hors périmètre
Pas de pipeline d'ingestion complet (STEP-03). Pas d'UI (STEP-05+).

## Definition of done
Suite de tests verte, 10/10 fixtures valides acceptées, 10/10 fixtures
invalides rejetées avec un message d'erreur clair.

## À écrire dans PROGRESS.md
```
## <date> — STEP-02 — Schémas Zod
STATUT: FAIT
FAIT: 10 schémas + union discriminée + 20 fixtures (10 valides/10 invalides), tests verts
DÉCISIONS: <écarts éventuels par rapport aux shapes ci-dessus>
FICHIERS CLÉS: packages/schemas/exercises.ts, packages/schemas/__fixtures__/
```
