-- Graphes de connaissances (un par track, style Umbrex)
CREATE TABLE knowledge_graphs (
  id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  track_id    uuid        NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  title       text        NOT NULL,
  description text,
  created_at  timestamptz DEFAULT now()
);

-- Noeuds du graphe
CREATE TABLE graph_nodes (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  graph_id   uuid        NOT NULL REFERENCES knowledge_graphs(id) ON DELETE CASCADE,
  key        text        NOT NULL,    -- identifiant stable (ex. "dcf", "wacc")
  label      text        NOT NULL,
  layer      text,                   -- couche logique (ex. "foundation", "advanced")
  parent_key text,                   -- noeud parent dans l'arbre (nullable)
  meta       jsonb       NOT NULL DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  UNIQUE (graph_id, key)
);

CREATE INDEX idx_graph_nodes_graph ON graph_nodes (graph_id);

-- Arêtes du graphe
CREATE TABLE graph_edges (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  graph_id   uuid        NOT NULL REFERENCES knowledge_graphs(id) ON DELETE CASCADE,
  source_key text        NOT NULL,
  target_key text        NOT NULL,
  weight     numeric     NOT NULL DEFAULT 1.0,
  created_at timestamptz DEFAULT now(),
  UNIQUE (graph_id, source_key, target_key)
);

CREATE INDEX idx_graph_edges_graph ON graph_edges (graph_id);
