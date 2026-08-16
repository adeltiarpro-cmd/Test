-- ============================================================
-- RLS — Row Level Security
-- ============================================================
-- Règle globale :
--   • Contenu (tracks → model_templates) : SELECT pour tout authentifié,
--     INSERT/UPDATE/DELETE réservé au service_role (qui bypasse le RLS).
--   • Données utilisateur (profiles, attempts, review_states, concept_mastery) :
--     toutes opérations limitées à user_id = auth.uid().
--   • invitations : aucun accès utilisateur direct (service_role uniquement).
-- ============================================================

-- ── Tables de contenu ────────────────────────────────────────

ALTER TABLE tracks              ENABLE ROW LEVEL SECURITY;
ALTER TABLE modules             ENABLE ROW LEVEL SECURITY;
ALTER TABLE module_targets      ENABLE ROW LEVEL SECURITY;
ALTER TABLE lessons             ENABLE ROW LEVEL SECURITY;
ALTER TABLE concepts            ENABLE ROW LEVEL SECURITY;
ALTER TABLE concept_edges       ENABLE ROW LEVEL SECURITY;
ALTER TABLE sources             ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercises           ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercise_concepts   ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_graphs    ENABLE ROW LEVEL SECURITY;
ALTER TABLE graph_nodes         ENABLE ROW LEVEL SECURITY;
ALTER TABLE graph_edges         ENABLE ROW LEVEL SECURITY;
ALTER TABLE model_templates     ENABLE ROW LEVEL SECURITY;

CREATE POLICY "authenticated read tracks"
  ON tracks FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read modules"
  ON modules FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read module_targets"
  ON module_targets FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read lessons"
  ON lessons FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read concepts"
  ON concepts FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read concept_edges"
  ON concept_edges FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read sources"
  ON sources FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read exercises"
  ON exercises FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read exercise_concepts"
  ON exercise_concepts FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read knowledge_graphs"
  ON knowledge_graphs FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read graph_nodes"
  ON graph_nodes FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read graph_edges"
  ON graph_edges FOR SELECT TO authenticated USING (true);

CREATE POLICY "authenticated read model_templates"
  ON model_templates FOR SELECT TO authenticated USING (true);

-- ── Tables utilisateur ────────────────────────────────────────

ALTER TABLE profiles        ENABLE ROW LEVEL SECURITY;
ALTER TABLE attempts        ENABLE ROW LEVEL SECURITY;
ALTER TABLE review_states   ENABLE ROW LEVEL SECURITY;
ALTER TABLE concept_mastery ENABLE ROW LEVEL SECURITY;

-- profiles
CREATE POLICY "users read own profile"
  ON profiles FOR SELECT TO authenticated USING (id = auth.uid());

CREATE POLICY "users update own profile"
  ON profiles FOR UPDATE TO authenticated USING (id = auth.uid());

-- attempts
CREATE POLICY "users read own attempts"
  ON attempts FOR SELECT TO authenticated USING (user_id = auth.uid());

CREATE POLICY "users insert own attempts"
  ON attempts FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid());

-- review_states
CREATE POLICY "users read own review_states"
  ON review_states FOR SELECT TO authenticated USING (user_id = auth.uid());

CREATE POLICY "users insert own review_states"
  ON review_states FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid());

CREATE POLICY "users update own review_states"
  ON review_states FOR UPDATE TO authenticated USING (user_id = auth.uid());

-- concept_mastery
CREATE POLICY "users read own concept_mastery"
  ON concept_mastery FOR SELECT TO authenticated USING (user_id = auth.uid());

CREATE POLICY "users insert own concept_mastery"
  ON concept_mastery FOR INSERT TO authenticated WITH CHECK (user_id = auth.uid());

CREATE POLICY "users update own concept_mastery"
  ON concept_mastery FOR UPDATE TO authenticated USING (user_id = auth.uid());

-- ── invitations : aucun accès utilisateur ────────────────────

ALTER TABLE invitations ENABLE ROW LEVEL SECURITY;
-- Pas de politique SELECT/INSERT/UPDATE/DELETE pour les utilisateurs authentifiés.
-- Le service_role bypasse le RLS et peut tout faire.
-- La fonction check_invitation() est SECURITY DEFINER et contourne le RLS.
