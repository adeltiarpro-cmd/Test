-- Seed : 1 modèle IS simplifié + 2 exercices (excel_model + statement_interactive)
-- Idempotent : ON CONFLICT DO NOTHING.

DO $$
DECLARE
  v_module_id   uuid;
  v_template_id uuid := 'bbbbbbbb-0000-0000-0000-000000000001';
BEGIN
  SELECT id INTO v_module_id
  FROM modules
  WHERE track_id = '10000000-0000-0000-0000-000000000002'
    AND slug = 'financial-modeling'
  LIMIT 1;

  IF v_module_id IS NULL THEN
    RAISE NOTICE 'Module financial-modeling introuvable — seed ignoré.';
    RETURN;
  END IF;

  -- ── Modèle IS 7 lignes (Revenue → Net Income) ────────────────────────────
  INSERT INTO model_templates (id, module_id, title, description, sheet)
  VALUES (
    v_template_id,
    v_module_id,
    'IS Simplifié — Modèle de base',
    'Compte de résultat 7 lignes, FY2023A et FY2024E. Les charges sont en valeur négative.',
    jsonb_build_object(
      'cols', jsonb_build_array('', 'FY2023A', 'FY2024E'),
      'data', jsonb_build_array(
        jsonb_build_array('Revenue',        1000,           1200          ),
        jsonb_build_array('COGS',           -400,           -480          ),
        jsonb_build_array('Gross Profit',   '=B1+B2',       '=C1+C2'     ),
        jsonb_build_array('Operating Exp.', -150,           -180          ),
        jsonb_build_array('EBIT',           '=B3+B4',       '=C3+C4'     ),
        jsonb_build_array('Tax (28%)',      '=B5*(-0.28)',  '=C5*(-0.28)'),
        jsonb_build_array('Net Income',     '=B5+B6',       '=C5+C6'     )
      )
    )
  )
  ON CONFLICT (id) DO NOTHING;

  -- ── Exercice 1 : excel_model — compléter les 3 sous-totaux ───────────────
  INSERT INTO exercises (module_id, type, difficulty, payload, solution, tags, external_key)
  VALUES (
    v_module_id,
    'excel_model',
    3,
    jsonb_build_object(
      'template_id',    v_template_id::text,
      'editable_cells', jsonb_build_array('B3','C3','B5','C5','B7','C7'),
      'check_mode',     'both'
    ),
    jsonb_build_object(
      'cells', jsonb_build_object(
        'B3', jsonb_build_object(
          'formula', '=B1+B2', 'value', 600, 'tolerance', 1,
          'explain_mdx', 'Gross Profit = Revenue + COGS (COGS est négatif).'
        ),
        'C3', jsonb_build_object(
          'formula', '=C1+C2', 'value', 720, 'tolerance', 1,
          'explain_mdx', 'Gross Profit FY2024E = 1 200 + (−480) = 720.'
        ),
        'B5', jsonb_build_object(
          'formula', '=B3+B4', 'value', 450, 'tolerance', 1,
          'explain_mdx', 'EBIT = Gross Profit + Charges opérat. (charges négatives).'
        ),
        'C5', jsonb_build_object(
          'formula', '=C3+C4', 'value', 540, 'tolerance', 1,
          'explain_mdx', 'EBIT FY2024E = 720 + (−180) = 540.'
        ),
        'B7', jsonb_build_object(
          'formula', '=B5+B6', 'value', 324, 'tolerance', 2,
          'explain_mdx', 'Net Income = EBIT + Tax. Tax = EBIT × (−28%) = −126 → NI = 324.'
        ),
        'C7', jsonb_build_object(
          'formula', '=C5+C6', 'value', 388.8, 'tolerance', 2,
          'explain_mdx', 'Net Income FY2024E = 540 × (1 − 0,28) = 388,8.'
        )
      )
    ),
    array['corpfin','financial-modeling','excel-model'],
    'seed-excel-model-is-subtotals-001'
  )
  ON CONFLICT (external_key) DO NOTHING;

  -- ── Exercice 2 : statement_interactive — IS avec contrôle de cohérence ───
  INSERT INTO exercises (module_id, type, difficulty, payload, solution, tags, external_key)
  VALUES (
    v_module_id,
    'statement_interactive',
    2,
    jsonb_build_object(
      'statement', 'is',
      'lines', jsonb_build_array(
        jsonb_build_object('key','revenue',      'label','Chiffre d''Affaires','level',0,'given',true, 'editable',false,'value',1000),
        jsonb_build_object('key','cogs',         'label','Coût des ventes',    'level',1,'given',true, 'editable',false,'value',-400),
        jsonb_build_object('key','gross_profit', 'label','Marge Brute',        'level',0,'given',false,'editable',true, 'formula_hint','= CA + Coût des ventes'),
        jsonb_build_object('key','opex',         'label','Charges opérat.',    'level',1,'given',true, 'editable',false,'value',-150),
        jsonb_build_object('key','ebit',         'label','EBIT',               'level',0,'given',false,'editable',true, 'formula_hint','= Marge Brute + Charges opérat.'),
        jsonb_build_object('key','tax',          'label','Impôt (28%)',        'level',1,'given',true, 'editable',false,'value',-126),
        jsonb_build_object('key','net_income',   'label','Résultat Net',       'level',0,'given',false,'editable',true, 'formula_hint','= EBIT + Impôt')
      ),
      'linked_checks', jsonb_build_array(jsonb_build_object('rule','ni_flows_to_re'))
    ),
    jsonb_build_object(
      'lines', jsonb_build_object(
        'revenue',      jsonb_build_object('value',1000, 'tolerance',0,'derivation_mdx','Donnée.'),
        'cogs',         jsonb_build_object('value',-400, 'tolerance',0,'derivation_mdx','Donnée.'),
        'gross_profit', jsonb_build_object('value',600,  'tolerance',1,'derivation_mdx','1 000 + (−400) = 600.'),
        'opex',         jsonb_build_object('value',-150, 'tolerance',0,'derivation_mdx','Donnée.'),
        'ebit',         jsonb_build_object('value',450,  'tolerance',1,'derivation_mdx','600 + (−150) = 450.'),
        'tax',          jsonb_build_object('value',-126, 'tolerance',0,'derivation_mdx','Donnée.'),
        'net_income',   jsonb_build_object('value',324,  'tolerance',2,'derivation_mdx','450 + (−126) = 324.')
      )
    ),
    array['corpfin','financial-modeling','statement'],
    'seed-statement-is-basic-001'
  )
  ON CONFLICT (external_key) DO NOTHING;

END;
$$;
