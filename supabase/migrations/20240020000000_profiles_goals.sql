-- ============================================================
-- CHANTIER-6 : objectifs personnels (date d'entretien, rythme)
-- Additive et rejouable.
-- ============================================================

ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS target_date date,
  ADD COLUMN IF NOT EXISTS daily_goal  int CHECK (daily_goal > 0);

-- Politique UPDATE sur profiles (idempotente)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE tablename = 'profiles'
      AND policyname = 'users update own profile'
  ) THEN
    EXECUTE $p$
      CREATE POLICY "users update own profile"
        ON profiles
        FOR UPDATE
        TO authenticated
        USING     (id = auth.uid())
        WITH CHECK (id = auth.uid())
    $p$;
  END IF;
END $$;
