"use client";

import { useState } from "react";
import { Eye, PencilLine, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Callout } from "@/components/ui/callout";
import { GraphTree } from "./graph-tree";
import { DragDropPanel } from "./dragdrop-panel";
import type { GraphData } from "@/lib/graph-actions";

interface GraphExplorerProps {
  graph: GraphData;
  /** If provided, these keys are hidden in fill mode (from an exercise payload). */
  exerciseHiddenKeys?: string[];
  exerciseMode?: "recall" | "dragdrop";
  exerciseDistractors?: string[];
  /** Called when the user submits answers (exercise integration). */
  onSubmit?: (answers: Record<string, string>) => void;
  submitDisabled?: boolean;
}

export function GraphExplorer({
  graph,
  exerciseHiddenKeys,
  exerciseMode,
  exerciseDistractors = [],
  onSubmit,
  submitDisabled,
}: GraphExplorerProps) {
  const [fillMode, setFillMode] = useState(!!exerciseHiddenKeys);
  const [mode, setMode] = useState<"recall" | "dragdrop">(exerciseMode ?? "recall");
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);

  // Hidden keys: from exercise or auto-select "advanced" nodes for standalone explorer
  const hiddenKeys = exerciseHiddenKeys
    ?? graph.nodes.filter((n) => n.layer === "advanced").map((n) => n.key);

  const allFilled = hiddenKeys.every((k) => (answers[k] ?? "").trim() !== "");

  function handleAnswerChange(key: string, value: string) {
    setAnswers((prev) => ({ ...prev, [key]: value }));
  }

  function handleSubmit() {
    if (!onSubmit) return;
    onSubmit(answers);
    setSubmitted(true);
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <h2 className="text-base font-semibold text-foreground">{graph.title}</h2>
          {graph.description && (
            <p className="text-sm text-muted-foreground mt-0.5">{graph.description}</p>
          )}
          <div className="flex gap-2 mt-1.5">
            <Badge variant="muted">{graph.nodes.length} nœuds</Badge>
            <Badge variant="muted">{graph.edges.length} arêtes</Badge>
          </div>
        </div>

        {/* Mode toggles — only shown in standalone explorer (no exercise) */}
        {!exerciseHiddenKeys && (
          <div className="flex items-center gap-2 flex-wrap">
            <button
              type="button"
              onClick={() => { setFillMode(false); setAnswers({}); setSubmitted(false); }}
              className={`inline-flex items-center gap-1.5 rounded-md border px-3 py-1.5 text-sm font-medium transition-colors cursor-pointer min-h-[36px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${!fillMode ? "border-primary bg-primary/10 text-primary" : "border-border bg-card text-muted-foreground hover:bg-muted"}`}
              aria-pressed={!fillMode}
            >
              <Eye className="h-3.5 w-3.5" aria-hidden="true" />
              Lecture
            </button>
            <button
              type="button"
              onClick={() => { setFillMode(true); setAnswers({}); setSubmitted(false); }}
              className={`inline-flex items-center gap-1.5 rounded-md border px-3 py-1.5 text-sm font-medium transition-colors cursor-pointer min-h-[36px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${fillMode ? "border-accent bg-accent/10 text-foreground" : "border-border bg-card text-muted-foreground hover:bg-muted"}`}
              aria-pressed={fillMode}
            >
              <PencilLine className="h-3.5 w-3.5" aria-hidden="true" />
              Mode à trous
            </button>
          </div>
        )}
      </div>

      {/* Sub-mode toggle (recall / dragdrop) — only in fill mode */}
      {fillMode && !exerciseHiddenKeys && (
        <div className="flex items-center gap-2 text-xs">
          <span className="text-muted-foreground font-medium">Mode :</span>
          {(["recall", "dragdrop"] as const).map((m) => (
            <button
              key={m}
              type="button"
              onClick={() => { setMode(m); setAnswers({}); }}
              aria-pressed={mode === m}
              className={`rounded border px-2.5 py-1 transition-colors cursor-pointer min-h-[32px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1 ${mode === m ? "border-primary bg-primary/10 text-primary font-semibold" : "border-border text-muted-foreground hover:bg-muted"}`}
            >
              {m === "recall" ? "Rappel (défaut)" : "Glisser-déposer"}
            </button>
          ))}
        </div>
      )}

      {/* Graph tree (always shown) */}
      <div className="rounded-lg border border-border bg-card p-4">
        <GraphTree
          nodes={graph.nodes}
          hiddenKeys={fillMode ? new Set(hiddenKeys) : new Set()}
          fillMode={fillMode && mode === "recall"}
          answers={answers}
          onAnswerChange={handleAnswerChange}
        />
      </div>

      {/* Dragdrop panel (below tree, fill + dragdrop mode) */}
      {fillMode && mode === "dragdrop" && !submitted && (
        <div className="rounded-lg border border-border bg-card p-4">
          <DragDropPanel
            hiddenKeys={hiddenKeys}
            distractors={exerciseDistractors.length > 0 ? exerciseDistractors : [
              ...graph.nodes.filter((n) => hiddenKeys.includes(n.key)).map((n) => n.label),
              // Add some extra distractors derived from non-hidden node labels
              ...graph.nodes.filter((n) => !hiddenKeys.includes(n.key)).slice(0, 3).map((n) => n.label),
            ]}
            answers={answers}
            onAnswerChange={handleAnswerChange}
          />
        </div>
      )}

      {/* Recall hint */}
      {fillMode && mode === "recall" && !submitted && (
        <Callout variant="info">
          Tapez le label exact (insensible à la casse et aux variantes connues).
        </Callout>
      )}

      {/* Submit button */}
      {fillMode && onSubmit && !submitted && (
        <Button
          variant="primary"
          disabled={!allFilled || submitDisabled}
          onClick={handleSubmit}
        >
          Valider
        </Button>
      )}

      {/* Standalone success */}
      {fillMode && !onSubmit && allFilled && !submitted && (
        <Button variant="primary" onClick={() => setSubmitted(true)}>
          Vérifier mes réponses
        </Button>
      )}
      {submitted && !onSubmit && (
        <Callout variant="success" title="Réponses enregistrées">
          <div className="flex flex-col gap-1 mt-1">
            {hiddenKeys.map((key) => {
              const node = graph.nodes.find((n) => n.key === key);
              const userAnswer = (answers[key] ?? "").trim().toLowerCase();
              const correct = userAnswer === (node?.label ?? "").toLowerCase();
              return (
                <div key={key} className="flex items-center gap-2 text-sm">
                  {correct ? (
                    <CheckCircle2 className="h-4 w-4 text-green-600 shrink-0" />
                  ) : (
                    <span className="text-destructive font-bold shrink-0">✗</span>
                  )}
                  <span className="font-medium">{key}</span>
                  <span className="text-muted-foreground">→ {node?.label}</span>
                  {!correct && (
                    <span className="text-destructive text-xs">(vous : {answers[key]})</span>
                  )}
                </div>
              );
            })}
          </div>
        </Callout>
      )}
    </div>
  );
}
