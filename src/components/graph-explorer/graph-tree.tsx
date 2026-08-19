"use client";

import { cn } from "@/lib/cn";
import type { GraphNode } from "@/lib/graph-actions";

const LAYER_COLORS: Record<string, string> = {
  foundation: "border-primary bg-primary/10 text-primary",
  core: "border-secondary bg-secondary/10 text-foreground",
  advanced: "border-accent bg-accent/10 text-foreground",
};

const LAYER_DOTS: Record<string, string> = {
  foundation: "bg-primary",
  core: "bg-secondary",
  advanced: "bg-accent",
};

interface TreeNodeProps {
  node: GraphNode;
  allNodes: GraphNode[];
  hiddenKeys: Set<string>;
  fillMode: boolean;
  answers: Record<string, string>;
  onAnswerChange: (key: string, value: string) => void;
  depth?: number;
}

function TreeNode({ node, allNodes, hiddenKeys, fillMode, answers, onAnswerChange, depth = 0 }: TreeNodeProps) {
  const children = allNodes.filter((n) => n.parent_key === node.key);
  const isHidden = hiddenKeys.has(node.key);
  const colorClass = LAYER_COLORS[node.layer ?? "core"] ?? LAYER_COLORS.core;
  const dotClass = LAYER_DOTS[node.layer ?? "core"] ?? LAYER_DOTS.core;

  return (
    <div className="flex flex-col gap-0.5">
      {/* Node */}
      <div className="flex items-center gap-2">
        {depth > 0 && (
          <div className="flex items-center gap-0" aria-hidden="true">
            <div className="w-4 border-b border-border" />
          </div>
        )}
        <div
          className={cn(
            "flex items-center gap-1.5 rounded border px-2 py-1 text-sm font-medium transition-colors duration-150",
            fillMode && isHidden
              ? "border-dashed border-muted-foreground bg-muted min-w-[120px]"
              : colorClass
          )}
        >
          <span className={cn("h-1.5 w-1.5 rounded-full shrink-0", fillMode && isHidden ? "bg-muted-foreground" : dotClass)} aria-hidden="true" />
          {fillMode && isHidden ? (
            <input
              type="text"
              value={answers[node.key] ?? ""}
              onChange={(e) => onAnswerChange(node.key, e.target.value)}
              placeholder={`${node.key}…`}
              aria-label={`Nœud caché : ${node.key}`}
              className="w-full bg-transparent outline-none text-sm placeholder:text-muted-foreground focus:ring-0 min-w-[80px]"
            />
          ) : (
            <span>{node.label}</span>
          )}
        </div>
      </div>

      {/* Children */}
      {children.length > 0 && (
        <div
          className={cn("flex flex-col gap-0.5", depth > 0 ? "ml-6 border-l border-border pl-2 mt-0.5" : "ml-3 border-l border-border pl-2 mt-0.5")}
        >
          {children.map((child) => (
            <TreeNode
              key={child.key}
              node={child}
              allNodes={allNodes}
              hiddenKeys={hiddenKeys}
              fillMode={fillMode}
              answers={answers}
              onAnswerChange={onAnswerChange}
              depth={depth + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}

interface GraphTreeProps {
  nodes: GraphNode[];
  hiddenKeys: Set<string>;
  fillMode: boolean;
  answers: Record<string, string>;
  onAnswerChange: (key: string, value: string) => void;
}

export function GraphTree({ nodes, hiddenKeys, fillMode, answers, onAnswerChange }: GraphTreeProps) {
  const roots = nodes.filter((n) => n.parent_key === null);

  if (nodes.length === 0) {
    return <p className="text-sm text-muted-foreground">Aucun nœud dans ce graphe.</p>;
  }

  return (
    <div className="flex flex-col gap-2" role="tree" aria-label="Graphe de connaissances">
      {/* Legend */}
      <div className="flex flex-wrap gap-2 text-xs text-muted-foreground mb-1">
        {Object.entries(LAYER_COLORS).map(([layer, cls]) => (
          <span key={layer} className={cn("flex items-center gap-1 px-1.5 py-0.5 rounded border text-xs", cls)}>
            <span className={cn("h-1.5 w-1.5 rounded-full", LAYER_DOTS[layer])} aria-hidden="true" />
            {layer}
          </span>
        ))}
        {fillMode && (
          <span className="flex items-center gap-1 px-1.5 py-0.5 rounded border border-dashed border-muted-foreground text-muted-foreground">
            <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground" aria-hidden="true" />
            à remplir
          </span>
        )}
      </div>

      {roots.map((root) => (
        <TreeNode
          key={root.key}
          node={root}
          allNodes={nodes}
          hiddenKeys={hiddenKeys}
          fillMode={fillMode}
          answers={answers}
          onAnswerChange={onAnswerChange}
        />
      ))}
    </div>
  );
}
