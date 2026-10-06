-- ============================================================
-- STEP-11 : drapeau administrateur pour la saisie manuelle d'exercices
-- Migration additive. Pour te passer admin, une seule fois, dans le SQL Editor :
--   UPDATE profiles SET is_admin = true WHERE email = '<ton email>';
-- ============================================================

ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS is_admin boolean NOT NULL DEFAULT false;

-- La policy RLS existante laisse chaque utilisateur modifier sa propre ligne
-- de profiles. Sans garde-fou, il pourrait donc se donner is_admin lui-même.
-- Ce trigger réserve la modification de la colonne aux rôles serveur.
CREATE OR REPLACE FUNCTION protect_is_admin()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.is_admin IS DISTINCT FROM OLD.is_admin
     AND current_user NOT IN ('postgres', 'service_role', 'supabase_admin') THEN
    RAISE EXCEPTION 'is_admin ne peut être modifié que côté serveur';
  END IF;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_protect_is_admin ON profiles;
CREATE TRIGGER trg_protect_is_admin
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION protect_is_admin();
