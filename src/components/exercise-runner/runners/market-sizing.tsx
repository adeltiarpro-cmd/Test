"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

interface MarketSizingRunnerProps {
  payload: { unit: string; allowed_assumptions?: string[] };
  onSubmit: (finalValue: number, reasoning: string) => void;
  disabled?: boolean;
  exerciseId: string;
  submitted?: boolean;
}

export function MarketSizingRunner({
  payload,
  onSubmit,
  disabled,
  exerciseId,
  submitted,
}: MarketSizingRunnerProps) {
  const [valueInput, setValueInput] = useState("");
  const [reasoning, setReasoning] = useState("");
  const [llmFeedback, setLlmFeedback] = useState<string | null>(null);
  const [loadingLlm, setLoadingLlm] = useState(false);

  async function getLlmFeedback() {
    setLoadingLlm(true);
    try {
      const res = await fetch("/api/case-feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          exercise_id: exerciseId,
          user_text: reasoning.trim() || `Estimation finale : ${valueInput} ${payload.unit}`,
          exercise_type: "market_sizing",
        }),
      });
      const data = await res.json() as { feedback?: string };
      setLlmFeedback(data.feedback ?? "Feedback non disponible.");
    } catch {
      setLlmFeedback("Erreur lors de la génération du feedback.");
    } finally {
      setLoadingLlm(false);
    }
  }

  const parsed = parseFloat(valueInput.replace(/\s/g, "").replace(",", "."));
  const canSubmit = !isNaN(parsed) && valueInput.trim() !== "";

  return (
    <div className="flex flex-col gap-3">
      {payload.allowed_assumptions && payload.allowed_assumptions.length > 0 && (
        <div className="rounded-md bg-muted/30 border border-border px-3 py-2">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
            Hypothèses autorisées
          </p>
          <ul className="text-sm text-foreground list-disc pl-4 space-y-0.5">
            {payload.allowed_assumptions.map((a, i) => <li key={i}>{a}</li>)}
          </ul>
        </div>
      )}

      <div className="flex gap-2 items-center">
        <input
          type="text"
          inputMode="decimal"
          value={valueInput}
          onChange={(e) => setValueInput(e.target.value)}
          disabled={!!disabled}
          placeholder="Votre estimation…"
          className="flex-1 rounded-md border border-border bg-card px-3 py-2 text-base text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <span className="text-sm text-muted-foreground shrink-0">{payload.unit}</span>
      </div>

      <textarea
        value={reasoning}
        onChange={(e) => setReasoning(e.target.value)}
        disabled={!!disabled}
        rows={4}
        className="w-full rounded-md border border-border bg-card px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground resize-none focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        placeholder="Détaillez votre raisonnement : segmentation, hypothèses, calculs… (optionnel, pour le feedback IA)"
      />

      {!submitted && (
        <Button
          variant="primary"
          size="md"
          disabled={!canSubmit || !!disabled}
          onClick={() => onSubmit(parsed, reasoning.trim())}
        >
          Valider
        </Button>
      )}

      {submitted && (
        <div className="flex flex-col gap-2">
          {!llmFeedback && (
            <Button
              variant="outline"
              size="sm"
              disabled={loadingLlm}
              onClick={getLlmFeedback}
              className="self-start"
            >
              {loadingLlm ? "Génération en cours…" : "Feedback qualitatif (IA)"}
            </Button>
          )}
          {llmFeedback && (
            <div className="rounded-md border border-border bg-muted/30 p-3 text-sm text-foreground whitespace-pre-wrap">
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">Feedback IA</p>
              {llmFeedback}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
