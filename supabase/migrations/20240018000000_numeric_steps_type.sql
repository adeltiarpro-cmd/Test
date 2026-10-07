-- ============================================================
-- Chantier 3 : nouveau type d'exercice "exercice à étapes"
-- ALTER TYPE est irréversible en Postgres, mais additif (n'affecte pas les lignes existantes).
-- ============================================================

ALTER TYPE exercise_type ADD VALUE IF NOT EXISTS 'numeric_steps';
