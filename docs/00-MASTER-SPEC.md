# PROMPT DE BUILD — Plateforme de formation personnelle (Finance / Consulting / GMAT / Math)

> À coller dans Claude Code (ou équivalent agentique) à la racine d'un repo vide.
> Le skill `ui-ux-pro-max` (SKILLUX.md) doit être installé et est **obligatoire** pour toute décision visuelle.

---

## 0. Hypothèses retenues (corrige-les avant de lancer si besoin)

- **Sources** : PDF (livres, guides Umbrex, banques d'exos) + XLS/XLSX (modèles BIWS réadaptés).
- **Volume cible** : plusieurs milliers d'exercices → le schéma doit encaisser 10k+ items sans refonte.
- **Utilisateurs** : 5 à 15 personnes max (moi + amis), sur invitation. Pas de public.
- **Priorité** : volume et qualité de la banque d'exos > features annexes. Pas de deadline dure.
- **Parsing** : les PDF sont analysés hors-ligne (par un LLM en session dédiée) et rendus sous forme de **JSON canonique**, jamais de SQL écrit à la main. Un script de validation + un loader idempotent font le reste.

---

## 1. Objectif

Construire une plateforme d'apprentissage privée, à 5 filières, alternant **modules de cours** et **exercices intensifs**, avec suivi de progression et répétition espacée.

| Filière | Sous-domaines | Spécificité technique dominante |
|---|---|---|
| **Finance de marché** | Fixed income, Options/Futures/Derivatives, Risk, Commodities, Equities | Exos **calculatoires** : réponse numérique avec tolérance, unités, étapes intermédiaires |
| **Finance corpo** | LBO, Valuation, Oil & Gas, M&A advanced, Biotech, Growth Equity & VC | Démarre par du **volume de réponses simples** (`mcq`, `short_answer`, `formula_cloze`) ; **mini-simulateurs Excel** et **comptes de résultat interactifs** arrivent en second temps une fois le socle construit |
| **Consulting** | Guides d'industrie Umbrex, cas pratiques, structuring, case math, market sizing | Démarre lui aussi par du **volume de réponses simples** (`mcq`, `short_answer`, `graph_fill` en mode rappel sur les guides Umbrex) ; `case_structuring`/`market_sizing`, plus lourds à corriger, arrivent ensuite |
| **GMAT** | Quant (PS, DS), Verbal (RC, CR), Data Insights | Banque d'items classiques, chrono, adaptatif |
| **Math** | **Calcul stochastique**, **algèbre linéaire**, **analyse non linéaire** | Pas un cours de math générale : uniquement ce qui sert les 4 autres filières — Itô/Black-Scholes pour les dérivés, matrices de covariance/valeurs propres pour le risk et le portefeuille, optimisation sous contrainte pour le LBO/valuation |

**Math n'est pas une filière isolée** : c'est une couche de prérequis explicite, avec ses 3 sous-domaines ci-dessus comme modules à part entière. Chaque concept de finance/consulting/GMAT peut pointer vers un ou plusieurs concepts math via `concept_edges`. Quand un utilisateur échoue répétitivement sur un concept, le système propose le prérequis math en amont plutôt que de simplement remontrer le même exercice.

**Priorité de construction** (cf. section 9) : Finance corpo et Consulting démarrent tous les deux par leur volet « réponses simples » — c'est ce qui donne le plus de matière révisable le plus vite, avant d'investir dans les simulateurs Excel et les graphes interactifs qui prennent plus de temps à construire correctement.

---

## 2. Stack imposée

- **Next.js 15 (App Router) + TypeScript strict** — déployé sur **Vercel**.
- **Supabase** : Postgres 15+, Auth (email + allowlist d'invitations), Storage (PDF/XLS sources), RLS activée partout.
- **Tailwind + shadcn/ui** pour la couche composants.
- **HyperFormula** (moteur de formules compatible Excel, open source) pour les simulateurs de modèles + **une grille type Glide Data Grid ou react-datasheet-grid** pour le rendu.
- **SheetJS (xlsx)** côté pipeline d'ingestion uniquement, pas au runtime.
- **KaTeX** pour le rendu des formules ; **MDX** pour les contenus de cours.

### Contrainte d'architecture non négociable

**Aucun parsing de PDF/XLS ne tourne dans une fonction Vercel.** Les timeouts serverless (10–60s) et les limites mémoire rendent ça ingérable sur un livre de 600 pages. Le pipeline d'ingestion est un **workspace Node local séparé** (`/ingest`) qui lit les fichiers, valide le JSON canonique et écrit dans Supabase via la clé service. L'app Next.js ne fait que **lire** du contenu déjà normalisé.

---

## 3. Modèle de données

Principe : **une seule table `exercises`** avec un discriminant `type` et un `payload jsonb` validé par contrainte CHECK + schéma Zod partagé. C'est ce qui permet d'ajouter un 11ᵉ type d'exercice sans migration lourde, tout en gardant des index GIN performants sur des milliers de lignes.

### Tables de contenu

```sql
-- Taxonomie
create table tracks (            -- 5 filières
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,     -- 'markets' | 'corpfin' | 'consulting' | 'gmat' | 'math'
  title text not null,
  position int not null
);

create table modules (           -- chapitre OU sous-chapitre, hiérarchie via parent_id
  id uuid primary key default gen_random_uuid(),
  track_id uuid not null references tracks(id) on delete cascade,
  parent_id uuid references modules(id) on delete cascade,  -- null = chapitre racine
  slug text not null, title text not null, position int not null,
  level smallint not null default 0,   -- 0 = chapitre ('Fixed Income'), 1 = sous-chapitre ('Duration & Convexity')
  unique (track_id, slug)
);

-- Objectif de maîtrise par sous-chapitre : affiche une vraie marge de progression
-- ("72% — objectif 85%") plutôt qu'un simple binaire fait / pas fait
create table module_targets (
  module_id uuid primary key references modules(id) on delete cascade,
  target_mastery numeric not null default 0.8,
  min_exercises int not null default 15   -- volume minimal avant de calculer un taux fiable
);

create table lessons (           -- contenu de cours (MDX)
  id uuid primary key default gen_random_uuid(),
  module_id uuid not null references modules(id) on delete cascade,
  slug text not null, title text not null, position int not null,
  body_mdx text not null,
  est_minutes int,
  unique (module_id, slug)
);

-- Graphe de concepts (transverse, porte la couche Math)
create table concepts (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  title text not null,
  track_id uuid references tracks(id),
  summary text
);

create table concept_edges (     -- prérequis : source est requis pour target
  source_id uuid not null references concepts(id) on delete cascade,
  target_id uuid not null references concepts(id) on delete cascade,
  kind text not null default 'prerequisite',  -- 'prerequisite' | 'related'
  primary key (source_id, target_id, kind),
  check (source_id <> target_id)
);

-- Provenance : indispensable avec des milliers d'exos issus de dizaines de bouquins
create table sources (
  id uuid primary key default gen_random_uuid(),
  kind text not null,            -- 'book' | 'umbrex' | 'biws' | 'own'
  title text not null,
  storage_path text,             -- Supabase Storage
  meta jsonb default '{}'
);
```

### Table centrale des exercices

```sql
create type exercise_type as enum (
  'mcq',                  -- QCM (GMAT, quiz de cours)
  'numeric',              -- réponse chiffrée + tolérance (finance de marché)
  'formula_cloze',        -- texte/formule à trou
  'excel_model',          -- mini-simulateur : remplir les bonnes cellules
  'statement_interactive',-- compte de résultat / bilan interactif
  'graph_fill',           -- graphe de connaissance à trous (Umbrex)
  'case_structuring',     -- issue tree / framework
  'market_sizing',        -- arbre d'estimation
  'case_math',            -- calcul chronométré
  'short_answer'          -- réponse courte (finance corpo conceptuelle)
);

create table exercises (
  id uuid primary key default gen_random_uuid(),
  module_id uuid not null references modules(id) on delete cascade,
  source_id uuid references sources(id),
  source_ref text,                       -- "p.147, ex. 4.3"
  type exercise_type not null,
  difficulty smallint not null check (difficulty between 1 and 5),
  est_seconds int,
  prompt_mdx text not null,
  payload jsonb not null,                -- schéma dépendant de `type`
  solution jsonb not null,               -- corrigé + étapes
  tags text[] default '{}',
  external_key text unique,              -- clé d'idempotence pour l'ingestion
  created_at timestamptz default now()
);

create index on exercises using gin (payload jsonb_path_ops);
create index on exercises using gin (tags);
create index on exercises (module_id, type, difficulty);

create table exercise_concepts (
  exercise_id uuid references exercises(id) on delete cascade,
  concept_id uuid references concepts(id) on delete cascade,
  primary key (exercise_id, concept_id)
);
```

### Tables de progression (par utilisateur, RLS stricte)

```sql
create table profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text, created_at timestamptz default now()
);

create table attempts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references profiles(id) on delete cascade,
  exercise_id uuid not null references exercises(id) on delete cascade,
  response jsonb not null,
  is_correct boolean,
  score numeric,                 -- 0..1 pour les exos à barème partiel
  seconds_spent int,
  feedback jsonb,                -- retour détaillé cellule par cellule / nœud par nœud
  created_at timestamptz default now()
);
create index on attempts (user_id, exercise_id, created_at desc);

-- Répétition espacée au niveau exercice ET concept
create table review_states (
  user_id uuid not null references profiles(id) on delete cascade,
  exercise_id uuid not null references exercises(id) on delete cascade,
  due_at timestamptz not null,
  stability numeric, difficulty_fsrs numeric,
  reps int default 0, lapses int default 0,
  last_grade smallint,
  primary key (user_id, exercise_id)
);
create index on review_states (user_id, due_at);

create table concept_mastery (
  user_id uuid not null references profiles(id) on delete cascade,
  concept_id uuid not null references concepts(id) on delete cascade,
  mastery numeric not null default 0,   -- 0..1, moyenne mobile pondérée
  updated_at timestamptz default now(),
  primary key (user_id, concept_id)
);
```

### Tables spécifiques

```sql
-- Graphes Umbrex (consulting) : stockés une fois, servis en mode lecture ou "à trous"
create table knowledge_graphs (
  id uuid primary key default gen_random_uuid(),
  module_id uuid references modules(id) on delete cascade,
  industry text not null,               -- 'Oil & Gas', 'Insurance', ...
  slug text unique not null,
  title text not null,
  source_id uuid references sources(id)
);

create table graph_nodes (
  id uuid primary key default gen_random_uuid(),
  graph_id uuid not null references knowledge_graphs(id) on delete cascade,
  key text not null,                    -- stable, référencé par les exos graph_fill
  label text not null,
  layer smallint not null,              -- profondeur dans l'arbre
  body_mdx text,
  parent_key text,
  unique (graph_id, key)
);

create table graph_edges (
  graph_id uuid not null references knowledge_graphs(id) on delete cascade,
  from_key text not null, to_key text not null,
  label text,
  primary key (graph_id, from_key, to_key)
);

-- Modèles Excel (finance corpo) : template + corrigé, extraits du XLS à l'ingestion
create table model_templates (
  id uuid primary key default gen_random_uuid(),
  module_id uuid references modules(id) on delete cascade,
  slug text unique not null,
  title text not null,
  sheet jsonb not null,       -- { cols, rows, cells: { "B7": {v, f, style, locked, label} } }
  source_id uuid references sources(id)
);
```

### RLS

- `tracks`, `modules`, `lessons`, `concepts`, `exercises`, `knowledge_graphs`, `graph_*`, `model_templates`, `sources` → **lecture pour tout utilisateur authentifié**, écriture réservée au rôle `service_role` (donc au pipeline d'ingestion).
- `attempts`, `review_states`, `concept_mastery`, `profiles` → **`user_id = auth.uid()`** en lecture et écriture. Aucune exception : les amis ne voient pas les scores des autres, sauf via une vue agrégée explicite si tu ajoutes un leaderboard plus tard.
- Accès à l'app conditionné à une table `invitations (email, used_at)` vérifiée par un trigger sur `auth.users`.

---

## 4. Les 10 types d'exercices — schémas `payload` / `solution`

Écris un fichier `packages/schemas/exercises.ts` avec un **schéma Zod par type**, exporté et utilisé (a) par le validateur d'ingestion, (b) par les composants de rendu, (c) par le moteur de correction. Une seule source de vérité.

### 4.1 `numeric` — cœur de la finance de marché
```ts
payload: {
  variables?: Record<string, number>,      // permet la génération de variantes
  unit: string,                            // '%', '$', 'bps', 'years'
  precision: number,                       // décimales attendues
  tolerance: { type: 'abs'|'rel', value: number },
  sub_answers?: Array<{ key, label, unit, tolerance }>  // étapes intermédiaires notées
}
solution: { value: number, sub_values?: Record<string, number>, steps_mdx: string, formula_katex: string }
```
Correction **déterministe**. Barème partiel si l'étape intermédiaire est juste mais le résultat final faux — essentiel en fixed income où une erreur de convention de jours ne doit pas annuler toute la démarche.

### 4.2 `formula_cloze` — textes à trou avec formules (finance corpo)
```ts
payload: {
  template_mdx: string,        // "FCF = EBIT × (1 − {{t}}) + {{da}} − {{capex}} − {{Δnwc}}"
  blanks: Array<{ key, kind: 'token'|'expression'|'number', hint?, options?: string[] }>
}
solution: { blanks: Record<string, { accepted: string[], canonical: string, explain_mdx: string }> }
```
Pour `kind: 'expression'`, **normaliser avant comparaison** (parse via HyperFormula ou mathjs, comparaison d'AST) : `EBIT*(1-t)` et `(1-t)*EBIT` doivent tous deux passer. Une comparaison de chaînes serait inutilisable en pratique.

### 4.3 `excel_model` — mini-simulateurs BIWS
```ts
payload: {
  template_id: uuid,                       // → model_templates
  editable_cells: string[],                // ["C12","C13","D12"]
  given_cells?: string[],                  // pré-remplies, en lecture seule
  check_mode: 'formula'|'value'|'both'
}
solution: {
  cells: Record<string, { formula?: string, value?: number, tolerance?: number, explain_mdx?: string }>
}
```
Le simulateur charge la feuille dans HyperFormula, laisse l'utilisateur saisir formules ou valeurs dans les cellules éditables, recalcule en direct, puis corrige :
- `check_mode: 'value'` → compare la valeur calculée avec tolérance,
- `check_mode: 'formula'` → compare l'**AST normalisé** de la formule (références relatives/absolues indifférentes sauf si l'exo porte précisément là-dessus),
- `both` → les deux, avec feedback distinct « bonne valeur, mauvaise construction ».

Le feedback est **cellule par cellule** (vert / orange « valeur juste, formule non-conforme » / rouge), jamais un simple faux global.

### 4.4 `statement_interactive` — comptes de résultat interactifs
```ts
payload: {
  statement: 'is'|'bs'|'cf',
  lines: Array<{ key, label, level, given?: number, editable: boolean, formula_hint? }>,
  linked_checks?: Array<{ rule: 'balance'|'cf_ties_to_cash'|'ni_flows_to_re' }>
}
solution: { lines: Record<string, { value: number, tolerance: number, derivation_mdx: string }> }
```
Les `linked_checks` sont ce qui distingue un vrai exercice d'analyse financière d'un QCM déguisé : le bilan doit **équilibrer**, le net income doit **remonter** aux capitaux propres, la variation de cash doit **coller**. Affiche ces contrôles en temps réel comme des indicateurs d'intégrité, avant même la validation.

### 4.5 `graph_fill` — graphes Umbrex à trous
```ts
payload: {
  graph_id: uuid,
  hidden_node_keys: string[],
  mode: 'recall'|'dragdrop',
  distractors?: string[]        // en mode dragdrop
}
solution: { nodes: Record<string, { accepted_labels: string[], explain_mdx: string }> }
```
Deux modes : rappel libre (l'utilisateur tape le label, matching insensible à la casse + synonymes déclarés) ou glisser-déposer avec distracteurs. Le mode `recall` doit être le défaut — c'est lui qui produit l'effort de récupération utile.

### 4.6 `case_structuring` / `market_sizing`
```ts
// case_structuring
payload: { case_brief_mdx, expected_branches: number, time_limit_seconds? }
solution: { rubric: Array<{ branch_key, label, keywords: string[], weight, must_have: boolean }>,
            model_answer_mdx: string }

// market_sizing
payload: { question, allowed_assumptions?: string[], unit }
solution: { tree: Array<{ key, label, value, unit }>, final_value, acceptable_range: [min,max],
            reasoning_mdx }
```
Correction en deux temps : **matching par mots-clés/rubrique d'abord** (déterministe, instantané, gratuit), puis **appel LLM optionnel** pour un feedback qualitatif sur la structure (MECE, priorisation, hypothèses). Le bouton « feedback détaillé » est explicite — pas d'appel API à chaque soumission.

Pour `market_sizing`, ce qui est noté c'est l'**ordre de grandeur** et la **cohérence de l'arbre**, pas le chiffre exact.

### 4.7 `case_math`, `mcq`, `short_answer`
- `case_math` : `{ prompt, time_limit_seconds, tolerance }` — chrono strict, pas de calculatrice, focus vitesse.
- `mcq` : `{ options: [{key, text_mdx}], multiple: boolean, shuffle: boolean }` / `solution: { correct_keys, explain_mdx, distractor_explains }`. Les explications de distracteurs sont **obligatoires** pour le GMAT.
- `short_answer` : `{ max_words }` / `solution: { key_points: [{text, weight}], model_answer_mdx }` — scoring par points-clés, LLM en option.

---

## 5. Pipeline d'ingestion (`/ingest`)

Workspace Node séparé, exécuté en local, **jamais déployé**.

```
/ingest
  /raw            # PDF/XLS d'origine (gitignored)
  /canonical      # JSON canonique produit par l'analyse LLM, versionné en git
  /scripts
    validate.ts   # Zod sur tout /canonical, refuse tout item invalide
    load.ts       # upsert idempotent vers Supabase via service_role
    xls-extract.ts# SheetJS : XLS → model_templates.sheet + solution.cells
    report.ts     # couverture : #exos par module/type/difficulté
```

### Contrat d'ingestion

Un fichier JSON par lot, structure fixe :
```json
{
  "source": { "kind": "book", "title": "...", "external_key": "hull-11e" },
  "track": "markets",
  "module": "options-futures-derivatives",
  "items": [
    { "external_key": "hull-11e-c13-q07", "type": "numeric", "difficulty": 3,
      "source_ref": "p.312, Q13.7", "concepts": ["black-scholes", "log-normal"],
      "prompt_mdx": "...", "payload": { ... }, "solution": { ... } }
  ]
}
```

Règles :
- **`external_key` obligatoire et stable** → le loader fait un `upsert on conflict`, donc réimporter un lot corrigé ne crée jamais de doublon. À l'échelle de plusieurs milliers d'exos issus de dizaines de sources, c'est la seule protection viable contre la dérive.
- Tout item qui échoue au schéma Zod est écrit dans `/canonical/_rejected/` avec le message d'erreur — jamais silencieusement ignoré, jamais « réparé » automatiquement.
- Les concepts sont référencés par slug ; un slug inconnu est créé automatiquement avec un flag `needs_review` plutôt que de faire échouer le lot.
- `report.ts` sort un tableau de couverture après chaque import : c'est l'outil qui dit où la banque est trop mince.

### Extraction XLS → `model_templates`
`xls-extract.ts` lit le classeur BIWS réadapté, et pour chaque feuille cible produit : la grille de cellules (valeur, formule, format, verrouillage), la liste des cellules candidates à masquer, et le corrigé. Les cellules masquées sont choisies manuellement via un fichier de config `‹model›.blanks.json` — pas d'heuristique automatique, le choix pédagogique de ce qu'on fait construire à l'utilisateur est trop important pour être deviné.

---

## 6. Application — surfaces à construire

1. **Dashboard** — révisions dues aujourd'hui (SRS), progression par filière, points faibles détectés (concepts à faible `mastery`), série d'activité.
2. **Lecteur de cours** — MDX + KaTeX, exos inline en fin de section, marquage « compris / à revoir » par concept.
3. **Runner d'exercices** — un composant par `exercise_type`, chrono, soumission, feedback immédiat, bouton « expliquer autrement ».
4. **Mode session** — série d'exos filtrée (module / type / difficulté / dus / échoués), format examen chronométré pour le GMAT.
5. **Explorateur de graphes** (consulting) — vue lecture du graphe Umbrex, bascule en mode « à trous » d'un clic.
6. **Atelier de modèles** (finance corpo) — la grille type Excel, plein écran, avec panneau de contrôles d'intégrité.
7. **Vue Math** — graphe de prérequis, avec les concepts bloquants surlignés en fonction des échecs réels de l'utilisateur.
8. **Admin léger** — parcourir/éditer un exo, signaler une erreur de corrigé, relancer un import.

### Répétition espacée
Implémente **FSRS** (ou SM-2 si tu préfères la simplicité) sur `review_states`, avec grade à 4 niveaux dérivé automatiquement du score et du temps passé pour les exos à correction déterministe. Propagation : chaque tentative met à jour `concept_mastery` des concepts liés (moyenne mobile pondérée par la difficulté).

---

## 7. Dispositifs pédagogiques ajoutés

Au-delà de ce que tu as demandé, ces éléments changent concrètement la vitesse d'apprentissage et coûtent peu à implémenter puisqu'ils s'appuient sur des tables déjà prévues (`review_states`, `concept_mastery`, `module_targets`).

1. **Hiérarchie à 3 niveaux, pas 2** : domaine (`track`) → chapitre → sous-chapitre (`modules.parent_id`/`level`). C'est le sous-chapitre, pas le chapitre, qui porte la barre de progression — « Duration & Convexity » doit pouvoir être vert pendant que « Fixed Income » dans son ensemble est encore à 60%.

2. **Marge de progression explicite, pas un pourcentage brut.** L'UI affiche toujours *maîtrise actuelle vs `target_mastery`* (ex. « 72% — objectif 85% »), jamais juste « 72% ». En dessous de `min_exercises` tentatives, afficher « pas assez de données » plutôt qu'un taux trompeur sur 3 exos.

3. **Portes souples entre sous-chapitres.** Ne pas bloquer l'accès au sous-chapitre suivant sous le seuil — juste le signaler visuellement. Un vrai blocage frustre plus qu'il n'aide en auto-formation ; un signal visuel suffit à orienter.

4. **Intercalage (interleaving) dans les sessions de révision.** Le constructeur de session ne pioche jamais tous les items dus dans un seul sous-chapitre : il mélange les modules dus. C'est ce qui produit une meilleure rétention à long terme qu'une pratique bloquée — particulièrement pertinent vu le volume de matière à couvrir.

5. **Notation de confiance à chaque réponse** (1 = au hasard, 2 = incertain, 3 = sûr), en plus de juste/faux. Un « juste mais peu confiant » et un « faux mais très confiant » se traitent différemment dans le SRS — le second doit revenir plus vite. Particulièrement utile pour calibrer le GMAT, où la confiance mal calibrée coûte cher en conditions d'examen.

6. **Détection de leech.** `review_states.lapses` (déjà dans le schéma) sert de compteur : au-delà de 3 échecs sur le même exercice, arrêter de le représenter tel quel — proposer plutôt le prérequis math lié (`concept_edges`) ou une reformulation, sinon on entraîne l'échec plus que la maîtrise.

7. **Rappel hebdomadaire simple.** Une fonction planifiée (Supabase Cron ou Vercel Cron) calcule chaque lundi les items dus + les 3 concepts les plus faibles, affichés en tête de dashboard. Pas besoin d'email au départ — l'in-app suffit tant que c'est solo/amis.

8. **Format d'exercice qui suit la maîtrise, pas l'inverse.** Pour un concept encore frais, privilégier `mcq` (reconnaissance, moins coûteux cognitivement). Une fois `concept_mastery` au-dessus d'un seuil, prioriser les formats à rappel libre (`numeric`, `formula_cloze`, `graph_fill` en mode `recall`) qui produisent un meilleur ancrage — sauf pour le GMAT, où le format reste `mcq` puisque c'est le format réel de l'examen.

---

## 8. Direction UI/UX — usage obligatoire du skill `ui-ux-pro-max`

Suis le workflow de SKILLUX.md dans l'ordre. Stack détectée : **`nextjs`** (confirmée par `package.json`) — ne pas supposer, vérifier.

**Étape 2 — design system + persistance :**
```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" \
  "education learning platform finance quantitative content-dense focused study" \
  --design-system --persist -p "Prep Platform" --output-dir "<racine-du-repo>" \
  --variance 3 --motion 3 --density 8
```
Justification des dials : `variance 3` (l'interface doit s'effacer devant le contenu — pas de mise en page bavarde pendant une session de calcul), `motion 3` (micro-interactions seulement ; toute animation décorative pendant un exo chronométré est un coût cognitif net), `density 8` (tableaux financiers, grilles de cellules, graphes — il faut de la matière à l'écran).

Vérifie d'abord si `design-system/prep-platform/MASTER.md` existe : si oui, **lis-le et ne régénère pas** sans `--force`.

**Overrides de page** à générer avec `--page` pour les surfaces qui divergent du master :
- `--page "model-workshop"` (grille dense, chrome minimal)
- `--page "graph-explorer"` (canvas, navigation spatiale)
- `--page "exam-session"` (mode focus, distractions supprimées)

**Étape 3 — recherches ciblées, au minimum :**
```bash
--domain ux "forms inline-validation error-clarity focus-management"
--domain ux "keyboard navigation accessibility contrast"
--domain chart "financial time-series dashboard"
--domain typography "technical data numeric tabular"
--domain icons "navigation outline"
--domain gsap "subtle micro-interaction feedback"
--stack nextjs "suspense streaming bundle rerender"
```

**Contraintes issues du tableau de priorité (1→10) :**
- Priorité 1–2 : contraste 4.5:1 minimum, cibles tactiles 44×44px, focus rings **jamais supprimés**, tout icon-only bouton porte un `aria-label`. Navigation clavier complète dans la grille de modèle et le runner d'exos — quelqu'un qui enchaîne 200 QCM ne doit jamais toucher la souris.
- Priorité 4 : **icônes SVG uniquement, aucun emoji**.
- Priorité 6 : tokens de couleur sémantiques, jamais de hex brut dans les composants. Police à **chiffres tabulaires** partout où il y a des nombres alignés (états financiers, grilles, résultats) — sans ça, les colonnes dansent.
- Priorité 7 : 150–300ms, `prefers-reduced-motion` respecté, aucune animation qui retarde l'affichage d'un feedback de correction.
- Priorité 8 : labels visibles (jamais placeholder-only), erreurs **à côté du champ**.

**Avant livraison :** lis `references/pro-rules.md` et déroule la Pre-Delivery Checklist ; en cas de doute sur une catégorie, `references/quick-reference.md` à la section correspondante.

Si une recherche renvoie 0 résultat : reformuler une fois, puis **dire explicitement que la recommandation vient des défauts intégrés** et non d'un match en base. Ne jamais présenter un résultat vide comme une donnée.

---

## 9. Ordre de construction

1. Schéma Supabase + RLS + seed de la taxonomie (5 tracks, hiérarchie chapitre/sous-chapitre, `module_targets`, concepts de base — dont les 3 modules Math : calcul stochastique, algèbre linéaire, analyse non linéaire).
2. `packages/schemas` — les 10 schémas Zod. **Avant tout composant** : ils contraignent tout le reste.
3. Pipeline `/ingest` : validate + load + report, testé sur un lot de 20 exos réels.
4. Design system via le skill, puis primitives UI.
5. Runner d'exercices : `mcq`, `numeric`, `short_answer`, `formula_cloze` — ce socle couvre déjà GMAT, finance de marché, **et le volet « réponses simples » de finance corpo et consulting**.
6. Ingestion massive sur ce socle : GMAT + finance de marché + finance corpo (réponses simples) + consulting (Umbrex en rappel/`short_answer`) → plusieurs milliers d'items exploitables rapidement, sur les 4 filières prioritaires.
7. `graph_fill` + explorateur Umbrex (lecture puis mode à trous).
8. `excel_model` + `statement_interactive` (HyperFormula) — le morceau techniquement le plus lourd, volontairement en dernier côté finance corpo.
9. `case_structuring` / `market_sizing` / `case_math` + feedback LLM optionnel.
10. SRS + dispositifs pédagogiques (interleaving, confiance, leech, rappel hebdo) + dashboard + vue Math.

Cet ordre est délibéré : il rend la plateforme **utilisable pour réviser sur les 5 filières dès l'étape 6**, en volume, avant d'investir dans les types d'exos les plus coûteux à construire (simulateurs Excel, graphes, cas structurés).

---

## 10. Livrables attendus

- Migrations SQL numérotées dans `supabase/migrations/`, avec RLS incluse dans la même migration que la table.
- `packages/schemas/exercises.ts` documenté, avec un exemple valide par type dans `__fixtures__/`.
- `/ingest` fonctionnel + README expliquant comment produire un lot canonique à partir d'un PDF.
- App Next.js déployable sur Vercel, avec `.env.example` complet.
- Un `SEEDING.md` : le format exact à me donner quand je te fournis un PDF, pour que la sortie soit chargeable sans retouche.

Commence par me proposer le schéma complet et les 10 schémas Zod, et attends ma validation avant d'écrire l'app.

---

## 11. Coûts & dépendances externes

Non — la contrainte « `/ingest` tourne en local, jamais déployé » n'implique **aucun coût nouveau en soi**. Détail par poste :

- **Le script `/ingest` lui-même** : gratuit, toujours. C'est du Node local, il n'est jamais hébergé, donc aucune facturation Vercel/Supabase ne lui est associée.
- **La production du JSON canonique à partir d'un PDF** : si tu me donnes le PDF en session de chat (comme on fait là) et que je te sors le JSON à coller dans `/ingest/canonical`, le coût est celui de ton usage Claude habituel — rien de spécifique à cette architecture. Un livre entier se fera en plusieurs lots vu les limites de contexte ; c'est du temps, pas un coût caché.
- **Automatisation à grande échelle (optionnelle)** : si un jour tu veux un script qui appelle directement l'API Anthropic sur des centaines de pages sans passer par le chat, ça devient une clé API facturée au token. Ce n'est pas requis par le design — juste une option si le volume manuel devient trop lourd.
- **Supabase** : le tier gratuit (500 Mo DB, 1 Go Storage, auth jusqu'à 50k users) suffit largement à cette échelle — des milliers de lignes JSON pèsent quelques Ko chacune. Le seul risque réel : stocker les PDF/XLS **bruts** dans Supabase Storage plutôt que juste leur texte extrait. Recommandation : ne garde le fichier source que le temps de l'extraction, versionne le JSON canonique en git, et ne remonte dans Storage que ce qui doit rester consultable (ex. le XLS original d'un modèle BIWS).
- **Vercel** : le tier Hobby (gratuit) suffit pour un usage perso/amis, tant que ce n'est pas un usage commercial.
- **Le seul poste vraiment variable en usage courant** : le feedback qualitatif optionnel sur `case_structuring`/`market_sizing`/`short_answer` (bouton explicite, section 4.6–4.7), s'il appelle l'API Anthropic à la demande. Tout le reste — `numeric`, `formula_cloze`, `excel_model`, `graph_fill`, `mcq` — se corrige en code pur, sans appel externe, donc gratuit à l'usage.

En résumé : à 5–15 utilisateurs et quelques milliers d'exercices, tu tiens dans les tiers gratuits. Le seul coût possible est optionnel et à ta discrétion, pas imposé par l'architecture.
