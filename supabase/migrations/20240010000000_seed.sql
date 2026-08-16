-- ============================================================
-- Seed — taxonomie initiale
-- 5 tracks + modules racine + module_targets par défaut
-- ============================================================

-- UUIDs fixes pour les tracks (stable entre resets)
INSERT INTO tracks (id, slug, title) VALUES
  ('10000000-0000-0000-0000-000000000001', 'markets',    'Finance de Marché'),
  ('10000000-0000-0000-0000-000000000002', 'corpfin',    'Finance d''Entreprise'),
  ('10000000-0000-0000-0000-000000000003', 'consulting', 'Consulting'),
  ('10000000-0000-0000-0000-000000000004', 'gmat',       'GMAT'),
  ('10000000-0000-0000-0000-000000000005', 'math',       'Mathématiques');

-- ── Finance de Marché ────────────────────────────────────────
INSERT INTO modules (track_id, level, slug, title, "order") VALUES
  ('10000000-0000-0000-0000-000000000001', 0, 'derivatives',  'Produits Dérivés',          1),
  ('10000000-0000-0000-0000-000000000001', 0, 'fixed-income',  'Taux et Obligations',       2),
  ('10000000-0000-0000-0000-000000000001', 0, 'equities',      'Actions et Valorisation',   3),
  ('10000000-0000-0000-0000-000000000001', 0, 'macro-rates',   'Macro et Taux',             4);

-- ── Finance d'Entreprise ─────────────────────────────────────
INSERT INTO modules (track_id, level, slug, title, "order") VALUES
  ('10000000-0000-0000-0000-000000000002', 0, 'valuation',          'Valorisation',              1),
  ('10000000-0000-0000-0000-000000000002', 0, 'mergers-acquisitions','Fusions-Acquisitions',      2),
  ('10000000-0000-0000-0000-000000000002', 0, 'capital-structure',   'Structure du Capital',      3),
  ('10000000-0000-0000-0000-000000000002', 0, 'financial-modeling',  'Modélisation Financière',   4);

-- ── Consulting ───────────────────────────────────────────────
INSERT INTO modules (track_id, level, slug, title, "order") VALUES
  ('10000000-0000-0000-0000-000000000003', 0, 'frameworks',      'Cadres d''Analyse',        1),
  ('10000000-0000-0000-0000-000000000003', 0, 'market-sizing',   'Estimation de Marché',     2),
  ('10000000-0000-0000-0000-000000000003', 0, 'case-structuring','Structuration de Cas',      3);

-- ── GMAT ─────────────────────────────────────────────────────
INSERT INTO modules (track_id, level, slug, title, "order") VALUES
  ('10000000-0000-0000-0000-000000000004', 0, 'quantitative',  'Quantitatif',     1),
  ('10000000-0000-0000-0000-000000000004', 0, 'verbal',        'Verbal',          2),
  ('10000000-0000-0000-0000-000000000004', 0, 'data-insights', 'Data Insights',   3);

-- ── Mathématiques (3 modules explicites du spec) ─────────────
INSERT INTO modules (track_id, level, slug, title, "order") VALUES
  ('10000000-0000-0000-0000-000000000005', 0, 'stochastic-calculus',  'Calcul Stochastique',    1),
  ('10000000-0000-0000-0000-000000000005', 0, 'linear-algebra',        'Algèbre Linéaire',       2),
  ('10000000-0000-0000-0000-000000000005', 0, 'nonlinear-analysis',    'Analyse Non-Linéaire',   3);

-- module_targets : une ligne par module, valeurs par défaut (0.8 / 15)
INSERT INTO module_targets (module_id)
SELECT id FROM modules;
