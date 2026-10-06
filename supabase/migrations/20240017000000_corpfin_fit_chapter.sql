-- ============================================================
-- Chapitre "Entretiens : fit et motivation" de la filière corpfin
-- et ses 6 sous-chapitres (modules.level = 1).
-- Migration additive et rejouable.
-- ============================================================

-- 1. Chapitre
INSERT INTO modules (track_id, level, slug, title, "order")
SELECT t.id, 0, 'interview-fit', 'Entretiens : fit et motivation', 5
FROM tracks t WHERE t.slug = 'corpfin'
ON CONFLICT (track_id, slug) DO NOTHING;

-- 2. Sous-chapitres
INSERT INTO modules (track_id, parent_id, level, slug, title, "order")
SELECT chap.track_id, chap.id, 1, v.slug, v.title, v.ord
FROM (VALUES
  ('fit-parcours',     'Parcours et CV',                   1),
  ('fit-motivation',   'Motivation et engagement',         2),
  ('fit-personnalite', 'Personnalité et travail en équipe', 3),
  ('fit-metier',       'Connaissance du métier',           4),
  ('fit-business',     'Sens des affaires et actualité',   5),
  ('fit-deals',        'Parler de ses deals',              6)
) AS v(slug, title, ord)
JOIN modules chap ON chap.slug = 'interview-fit' AND chap.level = 0
JOIN tracks t ON t.id = chap.track_id AND t.slug = 'corpfin'
ON CONFLICT (track_id, slug) DO NOTHING;

-- 3. Objectifs de maîtrise par défaut
INSERT INTO module_targets (module_id)
SELECT m.id FROM modules m
JOIN tracks t ON t.id = m.track_id AND t.slug = 'corpfin'
WHERE m.slug = 'interview-fit' OR m.slug LIKE 'fit-%'
ON CONFLICT (module_id) DO NOTHING;
