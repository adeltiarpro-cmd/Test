-- ============================================================
-- STEP-09, dispositif 1 : hiérarchie à 3 niveaux pour la filière corpfin
-- Crée les sous-chapitres (modules.level = 1) et y rattache les exercices
-- et concepts déjà chargés, d'après le concept de chaque exercice.
-- Migration additive et rejouable : aucune table existante n'est modifiée.
-- ============================================================

-- 1. Sous-chapitres
INSERT INTO modules (track_id, parent_id, level, slug, title, "order")
SELECT chap.track_id, chap.id, 1, v.slug, v.title, v.ord
FROM (VALUES
  ('financial-modeling', 'fm-three-statements', 'Les trois états financiers', 1),
  ('financial-modeling', 'fm-statement-impacts', 'Impacts sur les états', 2),
  ('financial-modeling', 'fm-working-capital', 'BFR et trésorerie', 3),
  ('financial-modeling', 'fm-projections', 'Projections et business plan', 4),
  ('valuation', 'val-enterprise-value', 'Enterprise Value et Equity Value', 1),
  ('valuation', 'val-methods', 'Méthodes de valorisation', 2),
  ('valuation', 'val-multiples', 'Multiples et comparables', 3),
  ('valuation', 'val-dcf', 'DCF et valeur terminale', 4),
  ('valuation', 'val-wacc', 'WACC et coût du capital', 5),
  ('mergers-acquisitions', 'ma-strategy', 'Logique stratégique et synergies', 1),
  ('mergers-acquisitions', 'ma-accretion', 'Relution, dilution et financement', 2),
  ('mergers-acquisitions', 'ma-accounting', 'Comptabilité d''acquisition', 3),
  ('mergers-acquisitions', 'ma-process', 'Processus et structuration', 4),
  ('capital-structure', 'cs-lbo', 'LBO : modèle et rendement', 1),
  ('capital-structure', 'cs-debt', 'Dette et covenants', 2),
  ('capital-structure', 'cs-restructuring', 'Restructuring', 3)
) AS v(parent_slug, slug, title, ord)
JOIN modules chap ON chap.slug = v.parent_slug AND chap.level = 0
JOIN tracks t ON t.id = chap.track_id AND t.slug = 'corpfin'
ON CONFLICT (track_id, slug) DO NOTHING;

-- 2. Objectifs de maîtrise par défaut (0.8 / 15) pour les nouveaux sous-chapitres
INSERT INTO module_targets (module_id)
SELECT m.id FROM modules m
JOIN tracks t ON t.id = m.track_id AND t.slug = 'corpfin'
WHERE m.level = 1
ON CONFLICT (module_id) DO NOTHING;

-- 3. Table de correspondance (chapitre, concept) -> sous-chapitre
CREATE TABLE _subchapter_map (parent_slug text, concept_slug text, sub_slug text);
INSERT INTO _subchapter_map VALUES
  ('financial-modeling', 'three-statements', 'fm-three-statements'),
  ('financial-modeling', 'ebitda', 'fm-three-statements'),
  ('financial-modeling', 'retained-earnings', 'fm-three-statements'),
  ('financial-modeling', 'equity', 'fm-three-statements'),
  ('financial-modeling', 'net-debt', 'fm-three-statements'),
  ('financial-modeling', 'dividends', 'fm-three-statements'),
  ('financial-modeling', 'stock-options', 'fm-three-statements'),
  ('financial-modeling', 'debt-types', 'fm-three-statements'),
  ('financial-modeling', 'da-impact', 'fm-statement-impacts'),
  ('financial-modeling', 'debt-capex', 'fm-statement-impacts'),
  ('financial-modeling', 'write-down', 'fm-statement-impacts'),
  ('financial-modeling', 'inventory', 'fm-statement-impacts'),
  ('financial-modeling', 'tax', 'fm-statement-impacts'),
  ('financial-modeling', 'deferred-tax', 'fm-statement-impacts'),
  ('financial-modeling', 'leases', 'fm-statement-impacts'),
  ('financial-modeling', 'goodwill', 'fm-statement-impacts'),
  ('financial-modeling', 'working-capital', 'fm-working-capital'),
  ('financial-modeling', 'revenue-recognition', 'fm-working-capital'),
  ('financial-modeling', 'bankruptcy', 'fm-working-capital'),
  ('financial-modeling', 'capex-vs-opex', 'fm-working-capital'),
  ('financial-modeling', 'exceptional-items', 'fm-working-capital'),
  ('financial-modeling', 'revenue-model', 'fm-projections'),
  ('financial-modeling', 'expense-model', 'fm-projections'),
  ('financial-modeling', 'business-plan', 'fm-projections'),
  ('financial-modeling', 'sensitivity', 'fm-projections'),
  ('financial-modeling', 'npv', 'fm-projections'),
  ('valuation', 'enterprise-value', 'val-enterprise-value'),
  ('valuation', 'equity-value', 'val-enterprise-value'),
  ('valuation', 'ev-bridge', 'val-enterprise-value'),
  ('valuation', 'dilution', 'val-enterprise-value'),
  ('valuation', 'valuation-methods', 'val-methods'),
  ('valuation', 'private-company', 'val-methods'),
  ('valuation', 'bank-valuation', 'val-methods'),
  ('valuation', 'ipo', 'val-methods'),
  ('valuation', 'liquidation-value', 'val-methods'),
  ('valuation', 'lbo-valuation', 'val-methods'),
  ('valuation', 'negative-earnings', 'val-methods'),
  ('valuation', 'financial-policy', 'val-methods'),
  ('valuation', 'accretion-dilution', 'val-methods'),
  ('valuation', 'multiples', 'val-multiples'),
  ('valuation', 'comparables', 'val-multiples'),
  ('valuation', 'control-premium', 'val-multiples'),
  ('valuation', 'ltm', 'val-multiples'),
  ('valuation', 'dcf', 'val-dcf'),
  ('valuation', 'terminal-value', 'val-dcf'),
  ('valuation', 'fcff', 'val-dcf'),
  ('valuation', 'fcfe', 'val-dcf'),
  ('valuation', 'ddm', 'val-dcf'),
  ('valuation', 'discount-rate', 'val-dcf'),
  ('valuation', 'wacc', 'val-wacc'),
  ('valuation', 'capm', 'val-wacc'),
  ('valuation', 'beta', 'val-wacc'),
  ('valuation', 'cost-of-debt', 'val-wacc'),
  ('mergers-acquisitions', 'ma-rationale', 'ma-strategy'),
  ('mergers-acquisitions', 'synergies', 'ma-strategy'),
  ('mergers-acquisitions', 'control-premium', 'ma-strategy'),
  ('mergers-acquisitions', 'spin-off', 'ma-strategy'),
  ('mergers-acquisitions', 'enterprise-value', 'ma-strategy'),
  ('mergers-acquisitions', 'accretion-dilution', 'ma-accretion'),
  ('mergers-acquisitions', 'deal-financing', 'ma-accretion'),
  ('mergers-acquisitions', 'exchange-ratio', 'ma-accretion'),
  ('mergers-acquisitions', 'convertibles', 'ma-accretion'),
  ('mergers-acquisitions', 'dilution', 'ma-accretion'),
  ('mergers-acquisitions', 'purchase-accounting', 'ma-accounting'),
  ('mergers-acquisitions', 'goodwill', 'ma-accounting'),
  ('mergers-acquisitions', 'deferred-tax', 'ma-accounting'),
  ('mergers-acquisitions', 'consolidation', 'ma-accounting'),
  ('mergers-acquisitions', 'ma-process', 'ma-process'),
  ('mergers-acquisitions', 'ma-documents', 'ma-process'),
  ('mergers-acquisitions', 'deal-structure', 'ma-process'),
  ('mergers-acquisitions', 'earn-out', 'ma-process'),
  ('capital-structure', 'lbo', 'cs-lbo'),
  ('capital-structure', 'lbo-returns', 'cs-lbo'),
  ('capital-structure', 'irr', 'cs-lbo'),
  ('capital-structure', 'lbo-candidate', 'cs-lbo'),
  ('capital-structure', 'lbo-valuation', 'cs-lbo'),
  ('capital-structure', 'lbo-model', 'cs-lbo'),
  ('capital-structure', 'lbo-types', 'cs-lbo'),
  ('capital-structure', 'lbo-exit', 'cs-lbo'),
  ('capital-structure', 'value-creation-levers', 'cs-lbo'),
  ('capital-structure', 'investment-thesis', 'cs-lbo'),
  ('capital-structure', 'purchase-accounting', 'cs-lbo'),
  ('capital-structure', 'goodwill', 'cs-lbo'),
  ('capital-structure', 'deal-structure', 'cs-lbo'),
  ('capital-structure', 'lbo-debt', 'cs-debt'),
  ('capital-structure', 'dividend-recap', 'cs-debt'),
  ('capital-structure', 'revolver', 'cs-debt'),
  ('capital-structure', 'covenants', 'cs-debt'),
  ('capital-structure', 'tax-shield', 'cs-debt'),
  ('capital-structure', 'cost-of-debt', 'cs-debt'),
  ('capital-structure', 'restructuring', 'cs-restructuring'),
  ('capital-structure', 'bankruptcy', 'cs-restructuring'),
  ('capital-structure', 'ma-process', 'cs-restructuring'),
  ('capital-structure', 'dcf', 'cs-restructuring'),
  ('capital-structure', 'liquidation-value', 'cs-restructuring'),
  ('capital-structure', 'equity', 'cs-restructuring'),
  ('capital-structure', 'valuation-methods', 'cs-restructuring'),
  ('capital-structure', 'working-capital', 'cs-restructuring'),
  ('capital-structure', 'exceptional-items', 'cs-restructuring');

-- 4. Rattache les exercices au sous-chapitre de leur concept
UPDATE exercises e
SET module_id = sub.id
FROM exercise_concepts ec
JOIN concepts c       ON c.id = ec.concept_id
JOIN modules chap     ON chap.id = c.module_id AND chap.level = 0
JOIN tracks t         ON t.id = chap.track_id AND t.slug = 'corpfin'
JOIN _subchapter_map mp ON mp.parent_slug = chap.slug AND mp.concept_slug = c.slug
JOIN modules sub      ON sub.track_id = chap.track_id AND sub.slug = mp.sub_slug
WHERE ec.exercise_id = e.id
  AND e.module_id = chap.id;

-- 5. Rattache les concepts eux-mêmes, pour que la maîtrise suive le sous-chapitre
UPDATE concepts c
SET module_id = sub.id
FROM modules chap
JOIN tracks t           ON t.id = chap.track_id AND t.slug = 'corpfin'
JOIN _subchapter_map mp ON mp.parent_slug = chap.slug
JOIN modules sub        ON sub.track_id = chap.track_id AND sub.slug = mp.sub_slug
WHERE c.module_id = chap.id
  AND chap.level = 0
  AND c.slug = mp.concept_slug;

DROP TABLE _subchapter_map;
