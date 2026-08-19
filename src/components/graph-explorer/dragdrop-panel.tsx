"use client";

import { useState } from "react";
import { cn } from "@/lib/cn";
import { Badge } from "@/components/ui/badge";

interface DragDropPanelProps {
  hiddenKeys: string[];
  distractors: string[];
  answers: Record<string, string>;
  onAnswerChange: (key: string, value: string) => void;
}

export function DragDropPanel({ hiddenKeys, distractors, answers, onAnswerChange }: DragDropPanelProps) {
  const [selected, setSelected] = useState<string | null>(null);

  const placed = new Set(Object.values(answers).filter(Boolean));
  const available = distractors.filter((d) => !placed.has(d));

  function handleChipClick(label: string) {
    setSelected((prev) => (prev === label ? null : label));
  }

  function handleSlotClick(key: string) {
    if (!selected) return;
    onAnswerChange(key, selected);
    setSelected(null);
  }

  function handleSlotClear(key: string) {
    onAnswerChange(key, "");
    setSelected(null);
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Available chips */}
      <div>
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
          Labels disponibles — cliquez pour sélectionner
        </p>
        <div className="flex flex-wrap gap-2" role="group" aria-label="Labels disponibles">
          {available.map((label) => (
            <button
              key={label}
              type="button"
              onClick={() => handleChipClick(label)}
              aria-pressed={selected === label}
              className={cn(
                "rounded-full border px-3 py-1 text-sm font-medium transition-colors cursor-pointer min-h-[36px]",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                selected === label
                  ? "border-accent bg-accent text-accent-foreground"
                  : "border-border bg-card text-foreground hover:bg-muted"
              )}
            >
              {label}
            </button>
          ))}
          {available.length === 0 && (
            <p className="text-xs text-muted-foreground italic">Tous les labels ont été placés.</p>
          )}
        </div>
      </div>

      {/* Drop slots */}
      <div>
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
          Nœuds à compléter — cliquez pour placer
        </p>
        <div className="flex flex-col gap-2">
          {hiddenKeys.map((key) => {
            const placed = answers[key];
            return (
              <div key={key} className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground w-24 font-mono shrink-0">{key}</span>
                {placed ? (
                  <div className="flex items-center gap-1">
                    <Badge variant="default">{placed}</Badge>
                    <button
                      type="button"
                      onClick={() => handleSlotClear(key)}
                      aria-label={`Retirer ${placed} du nœud ${key}`}
                      className="text-xs text-muted-foreground hover:text-destructive transition-colors cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    >
                      ×
                    </button>
                  </div>
                ) : (
                  <button
                    type="button"
                    onClick={() => handleSlotClick(key)}
                    disabled={!selected}
                    aria-label={`Emplacement pour ${key}${selected ? ` — placer "${selected}"` : " — sélectionnez d'abord un label"}`}
                    className={cn(
                      "rounded border border-dashed px-4 py-1 text-sm text-muted-foreground min-h-[36px] min-w-[120px] transition-colors",
                      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                      selected ? "border-accent hover:bg-accent/10 cursor-pointer" : "border-border cursor-not-allowed opacity-50"
                    )}
                  >
                    {selected ? `→ placer "${selected}"` : "vide"}
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
