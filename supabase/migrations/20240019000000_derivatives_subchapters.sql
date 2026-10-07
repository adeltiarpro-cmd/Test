-- ============================================================
-- CHANTIER-1 : sous-chapitres de la filière markets/derivatives
-- 9 sections couvrant les 36 thèmes du lot Hull (762 items).
-- Additive et rejouable (ON CONFLICT DO NOTHING).
-- ============================================================

-- 1. Sous-chapitres
INSERT INTO modules (track_id, parent_id, level, slug, title, "order")
SELECT der.track_id, der.id, 1, v.slug, v.title, v.ord
FROM (VALUES
  ('der-futures-forwards',  'Futures et forwards',                      1),
  ('der-interest-rates',    'Taux d''intérêt et futures de taux',       2),
  ('der-swaps',             'Swaps et ajustements',                     3),
  ('der-options-mechanics', 'Mécaniques et stratégies options',         4),
  ('der-bsm-pricing',       'Arbres binomiaux et Black-Scholes-Merton', 5),
  ('der-greeks-vol',        'Grecques et volatilité',                   6),
  ('der-exotic-models',     'Options exotiques et modèles avancés',     7),
  ('der-credit-var',        'Risque de crédit et VaR',                  8),
  ('der-commodities',       'Matières premières et options réelles',    9)
) AS v(slug, title, ord)
JOIN modules der ON der.slug = 'derivatives' AND der.level = 0
JOIN tracks t    ON t.id = der.track_id AND t.slug = 'markets'
ON CONFLICT (track_id, slug) DO NOTHING;

-- 2. Objectifs de maîtrise par défaut
INSERT INTO module_targets (module_id)
SELECT m.id FROM modules m
JOIN tracks t ON t.id = m.track_id AND t.slug = 'markets'
WHERE m.level = 1
  AND m.slug IN (
    'der-futures-forwards', 'der-interest-rates', 'der-swaps',
    'der-options-mechanics', 'der-bsm-pricing', 'der-greeks-vol',
    'der-exotic-models', 'der-credit-var', 'der-commodities'
  )
ON CONFLICT (module_id) DO NOTHING;
