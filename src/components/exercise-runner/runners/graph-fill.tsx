"use client";

import { GraphExplorer } from "@/components/graph-explorer";
import type { GraphData } from "@/lib/graph-actions";

interface GraphFillRunnerProps {
  payload: {
    hidden_node_keys: string[];
    mode: "recall" | "dragdrop";
    distractors?: string[];
    // Pre-fetched by the session RSC
    _graphData: GraphData;
  };
  onSubmit: (nodes: Record<string, string>) => void;
  disabled?: boolean;
}

export function GraphFillRunner({ payload, onSubmit, disabled }: GraphFillRunnerProps) {
  if (!payload._graphData) {
    return (
      <p className="text-sm text-muted-foreground">
        Graphe introuvable (graph_id manquant ou non chargé).
      </p>
    );
  }

  return (
    <GraphExplorer
      graph={payload._graphData}
      exerciseHiddenKeys={payload.hidden_node_keys}
      exerciseMode={payload.mode}
      exerciseDistractors={payload.distractors ?? []}
      onSubmit={onSubmit}
      submitDisabled={disabled}
    />
  );
}
