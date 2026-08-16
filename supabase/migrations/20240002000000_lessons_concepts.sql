-- Leçons : séquences pédagogiques au sein d'un module
CREATE TABLE lessons (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  module_id  uuid        NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
  title      text        NOT NULL,
  "order"    int         NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX idx_lessons_module ON lessons(module_id);

-- Concepts : unités de connaissance atomiques
CREATE TABLE concepts (
  id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  module_id   uuid        NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
  slug        text        NOT NULL,
  title       text        NOT NULL,
  description text,
  created_at  timestamptz DEFAULT now(),
  UNIQUE (module_id, slug)
);

CREATE INDEX idx_concepts_module ON concepts(module_id);

-- Arêtes entre concepts : prérequis ou relation
CREATE TABLE concept_edges (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id  uuid        NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  target_id  uuid        NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  kind       text        NOT NULL CHECK (kind IN ('prerequisite', 'related')),
  created_at timestamptz DEFAULT now(),
  CHECK (source_id <> target_id),
  UNIQUE (source_id, target_id)
);
