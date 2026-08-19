-- Graphe de test : Consulting — Principes de résolution de problème (Umbrex-style)
-- Idempotent : ON CONFLICT DO NOTHING sur les clés stables.

DO $$
DECLARE
  v_graph_id  uuid;
  v_module_id uuid;
BEGIN
  -- Module "Cadres d'Analyse" dans le track consulting
  SELECT id INTO v_module_id
  FROM modules
  WHERE track_id = '10000000-0000-0000-0000-000000000003'
    AND slug = 'frameworks'
  LIMIT 1;

  IF v_module_id IS NULL THEN
    RAISE NOTICE 'Module frameworks introuvable, seed ignoré.';
    RETURN;
  END IF;

  -- Graphe principal
  INSERT INTO knowledge_graphs (id, track_id, title, description)
  VALUES (
    'aaaaaaaa-0000-0000-0000-000000000001',
    '10000000-0000-0000-0000-000000000003',
    'Consulting — Problem-Solving',
    'Carte conceptuelle Umbrex des approches de résolution de problème en consulting'
  )
  ON CONFLICT DO NOTHING;

  v_graph_id := 'aaaaaaaa-0000-0000-0000-000000000001';

  -- Nœuds  (layer : foundation → core → advanced)
  INSERT INTO graph_nodes (graph_id, key, label, layer, parent_key, meta) VALUES
    (v_graph_id, 'root',         'Problem Solving',          'foundation', NULL,            '{}'),
    (v_graph_id, 'structure',    'Structuration',            'foundation', 'root',          '{}'),
    (v_graph_id, 'analysis',     'Analyse',                  'core',       'root',          '{}'),
    (v_graph_id, 'deliverables', 'Livrables',                'core',       'root',          '{}'),
    (v_graph_id, 'mece',         'MECE',                     'core',       'structure',     '{"definition":"Mutually Exclusive Collectively Exhaustive"}'),
    (v_graph_id, 'issue_tree',   'Issue Tree',               'core',       'structure',     '{}'),
    (v_graph_id, 'hypothesis',   'Hypothesis-driven',        'advanced',   'structure',     '{}'),
    (v_graph_id, '3c',           '3C (Company/Customers/Competitors)', 'core', 'analysis',  '{}'),
    (v_graph_id, 'swot',         'SWOT',                     'core',       'analysis',      '{}'),
    (v_graph_id, 'porter',       'Porter 5 Forces',          'advanced',   'analysis',      '{}'),
    (v_graph_id, 'pyramid',      'Principe Pyramidal',       'advanced',   'deliverables',  '{"author":"Barbara Minto"}'),
    (v_graph_id, 'exec_summary', 'Executive Summary',        'core',       'deliverables',  '{}')
  ON CONFLICT (graph_id, key) DO NOTHING;

  -- Arêtes (relations cross-branch)
  INSERT INTO graph_edges (graph_id, source_key, target_key, weight) VALUES
    (v_graph_id, 'mece',       'issue_tree',   1.0),
    (v_graph_id, 'issue_tree', 'hypothesis',   0.8),
    (v_graph_id, 'pyramid',    'exec_summary', 0.9),
    (v_graph_id, '3c',         'swot',         0.7)
  ON CONFLICT (graph_id, source_key, target_key) DO NOTHING;

  -- Exercice graph_fill associé (mode recall, 3 nœuds cachés)
  INSERT INTO exercises (module_id, type, difficulty, payload, solution, tags, external_key)
  VALUES (
    v_module_id,
    'graph_fill',
    3,
    jsonb_build_object(
      'prompt_mdx',        'Complétez la carte des approches de problem-solving en consulting en identifiant les nœuds manquants.',
      'graph_id',          'aaaaaaaa-0000-0000-0000-000000000001',
      'hidden_node_keys',  '["mece","porter","pyramid"]'::jsonb,
      'mode',              'recall',
      'distractors',       '["MECE","Porter 5 Forces","Principe Pyramidal","Blue Ocean","BCG Matrix","SWOT","Value Chain"]'::jsonb
    ),
    jsonb_build_object(
      'nodes', jsonb_build_object(
        'mece', jsonb_build_object(
          'accepted_labels', '["MECE","Mutually Exclusive Collectively Exhaustive","ME/CE"]'::jsonb,
          'explain_mdx',     'MECE (Mutually Exclusive, Collectively Exhaustive) garantit que les branches d''une issue tree couvrent tout le problème sans chevauchement.'
        ),
        'porter', jsonb_build_object(
          'accepted_labels', '["Porter 5 Forces","Porter","5 Forces","Five Forces","Porter''s Five Forces"]'::jsonb,
          'explain_mdx',     'Le modèle des 5 Forces de Porter analyse l''attractivité d''un secteur : concurrents, nouveaux entrants, substituts, pouvoir fournisseurs, pouvoir clients.'
        ),
        'pyramid', jsonb_build_object(
          'accepted_labels', '["Principe Pyramidal","Pyramide de Minto","Minto Pyramid","Pyramid Principle"]'::jsonb,
          'explain_mdx',     'Le Principe Pyramidal (Barbara Minto) structure les communications top-down : conclusion en premier, arguments en support, données en base.'
        )
      )
    ),
    array['consulting','frameworks','problem-solving'],
    'seed-graph-fill-consulting-ps-001'
  )
  ON CONFLICT (external_key) DO NOTHING;

END;
$$;
