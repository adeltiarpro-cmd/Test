-- ============================================================
-- Seed — exercices cas : case_math, case_structuring, market_sizing
-- Idempotent : ON CONFLICT (external_key) DO NOTHING
-- ============================================================

DO $$
DECLARE
  v_case_math_module    uuid;
  v_structuring_module  uuid;
  v_market_module       uuid;
BEGIN

  -- Resolve module IDs from slugs (consulting track)
  SELECT m.id INTO v_case_math_module
    FROM modules m JOIN tracks t ON t.id = m.track_id
   WHERE t.slug = 'consulting' AND m.slug = 'frameworks';

  SELECT m.id INTO v_structuring_module
    FROM modules m JOIN tracks t ON t.id = m.track_id
   WHERE t.slug = 'consulting' AND m.slug = 'case-structuring';

  SELECT m.id INTO v_market_module
    FROM modules m JOIN tracks t ON t.id = m.track_id
   WHERE t.slug = 'consulting' AND m.slug = 'market-sizing';

  -- ── case_math : calcul mental de rentabilité ─────────────────
  INSERT INTO exercises (
    module_id, type, difficulty, tags,
    payload, solution, external_key
  ) VALUES (
    v_case_math_module,
    'case_math', 3,
    array['consulting', 'profitability', 'mental-math'],
    jsonb_build_object(
      'prompt_mdx', 'Un magasin vend **1 200 articles par mois** à **15 € pièce**. Les coûts fixes sont de **8 000 €/mois** et le coût variable est de **6 € par article**. Quel est le **profit mensuel** (en €) ?',
      'time_limit_seconds', 90,
      'tolerance', 50
    ),
    jsonb_build_object(
      'value', 2800,
      'steps_mdx', 'CA = 1 200 × 15 = **18 000 €**. Coûts variables = 1 200 × 6 = **7 200 €**. Profit = 18 000 − 7 200 − 8 000 = **2 800 €**.'
    ),
    'seed-case-math-profitability-001'
  )
  ON CONFLICT (external_key) DO NOTHING;

  -- ── case_structuring : cas de profitabilité en baisse ────────
  INSERT INTO exercises (
    module_id, type, difficulty, tags,
    payload, solution, external_key
  ) VALUES (
    v_structuring_module,
    'case_structuring', 3,
    array['consulting', 'profitability', 'structuring'],
    jsonb_build_object(
      'prompt_mdx', 'Les **profits d''une chaîne de distribution** ont baissé de 30 % en 2 ans malgré une hausse du chiffre d''affaires. Structurez votre diagnostic en **3 axes principaux**.',
      'expected_branches', 3,
      'time_limit_seconds', 300
    ),
    jsonb_build_object(
      'rubric', jsonb_build_array(
        jsonb_build_object(
          'branch_key', 'revenues',
          'label', 'Analyse des revenus (mix produit, prix, volume)',
          'keywords', jsonb_build_array('revenu', 'prix', 'volume', 'mix'),
          'weight', 0.3,
          'must_have', false
        ),
        jsonb_build_object(
          'branch_key', 'costs',
          'label', 'Structure des coûts (fixes, variables, achats)',
          'keywords', jsonb_build_array('coût', 'marge', 'achat', 'charge'),
          'weight', 0.4,
          'must_have', true
        ),
        jsonb_build_object(
          'branch_key', 'operations',
          'label', 'Efficacité opérationnelle (supply chain, personnel)',
          'keywords', jsonb_build_array('opérat', 'supply', 'personnel', 'productiv'),
          'weight', 0.3,
          'must_have', false
        )
      ),
      'model_answer_mdx', '**1. Revenus :** analyser si la hausse du CA cache une dégradation du mix (produits moins rentables) ou une pression tarifaire.\n\n**2. Coûts :** identifier quels postes ont augmenté plus vite que le CA — achats, logistique, main-d''œuvre.\n\n**3. Efficacité opérationnelle :** pertes, obsolescence stock, productivité personnel, contrats fournisseurs renégociés.'
    ),
    'seed-case-structuring-profitability-001'
  )
  ON CONFLICT (external_key) DO NOTHING;

  -- ── market_sizing : marché des cafés en France ───────────────
  INSERT INTO exercises (
    module_id, type, difficulty, tags,
    payload, solution, external_key
  ) VALUES (
    v_market_module,
    'market_sizing', 3,
    array['consulting', 'market-sizing', 'france'],
    jsonb_build_object(
      'prompt_mdx', 'Estimez la **taille du marché des cafés (boissons chaudes) en France**, en milliards d''euros par an.',
      'unit', 'Mds €',
      'allowed_assumptions', jsonb_build_array(
        'Population française : 68 millions d''habitants',
        'Adultes (18+) : 80 % de la population',
        'Prix moyen d''un café : 2 €'
      )
    ),
    jsonb_build_object(
      'final_value', 6,
      'acceptable_range', jsonb_build_array(3, 12),
      'reasoning_mdx', '68 M × 80 % = **54 M adultes**. Hypothèse : 1 café/jour en moyenne (certains 0, certains 3). 54 M × 365 × 2 € ≈ **39 Mds €** en valeur brute — mais environ 15 % seulement en café hors domicile (restaurant, bar, distributeur). Estimation : **~6 Mds €**. Fourchette raisonnable : 3–12 Mds € selon les hypothèses de fréquence.',
      'tree', jsonb_build_array(
        jsonb_build_object('key', 'adults', 'label', 'Adultes', 'value', 54000000, 'unit', 'personnes'),
        jsonb_build_object('key', 'cups_per_day', 'label', 'Cafés/jour hors domicile', 'value', 0.3, 'unit', 'tasses/pers/jour'),
        jsonb_build_object('key', 'price', 'label', 'Prix moyen', 'value', 2, 'unit', '€'),
        jsonb_build_object('key', 'total', 'label', 'Total annuel', 'value', 11826000000, 'unit', '€')
      )
    ),
    'seed-market-sizing-cafes-france-001'
  )
  ON CONFLICT (external_key) DO NOTHING;

END $$;
