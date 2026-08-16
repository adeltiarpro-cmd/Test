-- Profils utilisateurs (miroir de auth.users, créé par trigger)
CREATE TABLE profiles (
  id           uuid        PRIMARY KEY REFERENCES auth.users (id) ON DELETE CASCADE,
  email        text        NOT NULL,
  display_name text,
  created_at   timestamptz DEFAULT now()
);

-- Tentatives de réponse
CREATE TABLE attempts (
  id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       uuid        NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  exercise_id   uuid        NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
  answer        jsonb       NOT NULL DEFAULT '{}',
  is_correct    boolean,
  time_spent_ms int,
  created_at    timestamptz DEFAULT now()
);

CREATE INDEX idx_attempts_user     ON attempts (user_id);
CREATE INDEX idx_attempts_exercise ON attempts (exercise_id);
CREATE INDEX idx_attempts_created  ON attempts (user_id, created_at DESC);

-- États de révision (FSRS-ready)
-- state: 0=new 1=learning 2=review 3=relearning
CREATE TABLE review_states (
  id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         uuid        NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  exercise_id     uuid        NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
  due_at          timestamptz NOT NULL DEFAULT now(),
  stability       numeric     NOT NULL DEFAULT 0,
  difficulty_fsrs numeric     NOT NULL DEFAULT 0.3 CHECK (difficulty_fsrs BETWEEN 0 AND 1),
  reps            int         NOT NULL DEFAULT 0,
  lapses          int         NOT NULL DEFAULT 0,
  state           smallint    NOT NULL DEFAULT 0 CHECK (state BETWEEN 0 AND 3),
  last_review_at  timestamptz,
  created_at      timestamptz DEFAULT now(),
  UNIQUE (user_id, exercise_id)
);

CREATE INDEX idx_review_states_user_due ON review_states (user_id, due_at);

-- Maîtrise par concept (agrégée, mise à jour par le runner)
CREATE TABLE concept_mastery (
  id             uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id        uuid        NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  concept_id     uuid        NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
  mastery_score  numeric     NOT NULL DEFAULT 0 CHECK (mastery_score BETWEEN 0 AND 1),
  last_updated   timestamptz DEFAULT now(),
  created_at     timestamptz DEFAULT now(),
  UNIQUE (user_id, concept_id)
);

CREATE INDEX idx_concept_mastery_user ON concept_mastery (user_id);

-- Trigger : création automatique du profil lors de l'inscription
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
