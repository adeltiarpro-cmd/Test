-- Enum des 10 types d'exercices
CREATE TYPE exercise_type AS ENUM (
  'mcq',
  'numeric',
  'formula_cloze',
  'excel_model',
  'statement_interactive',
  'graph_fill',
  'case_structuring',
  'market_sizing',
  'case_math',
  'short_answer'
);

-- Exercices
CREATE TABLE exercises (
  id           uuid          PRIMARY KEY DEFAULT gen_random_uuid(),
  module_id    uuid          NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
  source_id    uuid          REFERENCES sources(id) ON DELETE SET NULL,
  type         exercise_type NOT NULL,
  difficulty   smallint      NOT NULL DEFAULT 3 CHECK (difficulty BETWEEN 1 AND 5),
  payload      jsonb         NOT NULL DEFAULT '{}',
  solution     jsonb         NOT NULL DEFAULT '{}',
  tags         text[]        NOT NULL DEFAULT '{}',
  external_key text          UNIQUE,
  created_at   timestamptz   DEFAULT now()
);

-- Index composite pour les requêtes de session (filtrage par module + type + difficulté)
CREATE INDEX idx_exercises_module_type_diff ON exercises (module_id, type, difficulty);
-- GIN pour filtrage sur le contenu du payload
CREATE INDEX idx_exercises_payload ON exercises USING GIN (payload);
-- GIN pour filtrage par tags
CREATE INDEX idx_exercises_tags ON exercises USING GIN (tags);

-- Table de jointure exercice ↔ concept
CREATE TABLE exercise_concepts (
  exercise_id uuid NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
  concept_id  uuid NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  PRIMARY KEY (exercise_id, concept_id)
);

CREATE INDEX idx_exercise_concepts_concept ON exercise_concepts (concept_id);
