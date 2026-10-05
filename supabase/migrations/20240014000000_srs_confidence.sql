-- Add confidence rating to attempts (1=guess, 2=uncertain, 3=sure)
ALTER TABLE attempts
  ADD COLUMN IF NOT EXISTS confidence smallint
  CHECK (confidence BETWEEN 1 AND 3);
