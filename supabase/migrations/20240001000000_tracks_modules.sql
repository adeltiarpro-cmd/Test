-- Tracks : domaines de formation (markets, corpfin, consulting, gmat, math)
CREATE TABLE tracks (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  slug       text        UNIQUE NOT NULL,
  title      text        NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Modules : chapitres/sous-chapitres d'un track (arbre via parent_id)
CREATE TABLE modules (
  id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  track_id    uuid        NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  parent_id   uuid        REFERENCES modules(id) ON DELETE SET NULL,
  level       int         NOT NULL DEFAULT 0,
  slug        text        NOT NULL,
  title       text        NOT NULL,
  description text,
  "order"     int         NOT NULL DEFAULT 0,
  created_at  timestamptz DEFAULT now(),
  UNIQUE (track_id, slug)
);

CREATE INDEX idx_modules_track    ON modules(track_id);
CREATE INDEX idx_modules_parent   ON modules(parent_id);

-- Objectifs de maîtrise par module
CREATE TABLE module_targets (
  id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  module_id       uuid        NOT NULL UNIQUE REFERENCES modules(id) ON DELETE CASCADE,
  target_mastery  numeric     NOT NULL DEFAULT 0.8 CHECK (target_mastery BETWEEN 0 AND 1),
  min_exercises   int         NOT NULL DEFAULT 15,
  created_at      timestamptz DEFAULT now()
);
