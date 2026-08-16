-- Templates de modèles Excel interactifs (HyperFormula)
-- sheet : structure JSON des cellules (colonnes, formules, validations)
CREATE TABLE model_templates (
  id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  module_id   uuid        REFERENCES modules(id) ON DELETE SET NULL,
  title       text        NOT NULL,
  description text,
  sheet       jsonb       NOT NULL DEFAULT '{}',
  created_at  timestamptz DEFAULT now()
);

CREATE INDEX idx_model_templates_module ON model_templates (module_id);
