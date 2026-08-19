"use server";

import { createClient } from "@/lib/supabase/server";

export type GraphNode = {
  id: string;
  key: string;
  label: string;
  layer: string | null;
  parent_key: string | null;
  meta: Record<string, unknown>;
};

export type GraphEdge = {
  id: string;
  source_key: string;
  target_key: string;
  weight: number;
};

export type GraphData = {
  id: string;
  title: string;
  description: string | null;
  nodes: GraphNode[];
  edges: GraphEdge[];
};

export type GraphSummary = {
  id: string;
  title: string;
  description: string | null;
  node_count: number;
};

export async function fetchGraphData(graphId: string): Promise<GraphData | null> {
  const supabase = await createClient();

  const { data: graph } = await supabase
    .from("knowledge_graphs")
    .select("id, title, description")
    .eq("id", graphId)
    .single();

  if (!graph) return null;

  const { data: nodes } = await supabase
    .from("graph_nodes")
    .select("id, key, label, layer, parent_key, meta")
    .eq("graph_id", graphId)
    .order("layer", { ascending: true });

  const { data: edges } = await supabase
    .from("graph_edges")
    .select("id, source_key, target_key, weight")
    .eq("graph_id", graphId);

  return {
    id: graph.id,
    title: graph.title,
    description: graph.description,
    nodes: (nodes ?? []) as GraphNode[],
    edges: (edges ?? []) as GraphEdge[],
  };
}

export async function listConsultingGraphs(): Promise<GraphSummary[]> {
  const supabase = await createClient();

  const { data } = await supabase
    .from("knowledge_graphs")
    .select("id, title, description, graph_nodes(id)")
    .eq("track_id", "10000000-0000-0000-0000-000000000003")
    .order("title");

  return (data ?? []).map((g) => ({
    id: g.id,
    title: g.title,
    description: g.description,
    node_count: Array.isArray(g.graph_nodes) ? g.graph_nodes.length : 0,
  }));
}
