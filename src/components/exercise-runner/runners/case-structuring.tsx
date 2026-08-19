"use client";

import { useState } from "react";
import { CheckCircle2, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { RubricBranchResult } from "@/lib/session-actions";

interface CaseStructuringRunnerProps {
  payload: { expected_branches: number };
  onSubmit: (text: string) => void;
  disabled?: boolean;
  rubricResults?: RubricBranchResult[];
  exerciseId: string;
}

export function CaseStructuringRunner({
  payload,
  onSubmit,
  disabled,
  rubricResults,
  exerciseId,
}: CaseStructuringRunnerProps) {
  const [text, setText] = useState("");
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
          user_text: text,
          exercise_type: "case_structuring",
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

  return (
    <div className="flex flex-col gap-3">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={!!disabled}
        rows={6}
        className="w-full rounded-md border border-border bg-card px-3 py-2 text-base text-foreground placeholder:text-muted-foreground resize-none focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        placeholder={`Structurez votre réponse en ${payload.expected_branches} axes principaux…`}
      />

      {!rubricResults && (
        <Button
          variant="primary"
          size="md"
          disabled={text.trim() === "" || !!disabled}
          onClick={() => onSubmit(text.trim())}
        >
          Valider
        </Button>
      )}

      {rubricResults && (
        <div className="flex flex-col gap-2">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Résultats par axe</p>
          {rubricResults.map((r) => (
            <div key={r.branch_key} className="flex items-center gap-2 text-sm">
              {r.covered ? (
                <CheckCircle2 className="h-4 w-4 text-green-600 shrink-0" />
              ) : (
                <XCircle className={`h-4 w-4 shrink-0 ${r.must_have ? "text-destructive" : "text-muted-foreground"}`} />
              )}
              <span className={r.must_have && !r.covered ? "font-medium text-destructive" : "text-foreground"}>
                {r.label}
              </span>
              <span className="ml-auto text-xs tabular-nums text-muted-foreground">
                {Math.round(r.weight * 100)} %{r.must_have ? " ★" : ""}
              </span>
            </div>
          ))}

          {!llmFeedback && (
            <Button
              variant="outline"
              size="sm"
              disabled={loadingLlm}
              onClick={getLlmFeedback}
              className="self-start mt-2"
            >
              {loadingLlm ? "Génération en cours…" : "Feedback qualitatif (IA)"}
            </Button>
          )}

          {llmFeedback && (
            <div className="rounded-md border border-border bg-muted/30 p-3 text-sm text-foreground whitespace-pre-wrap mt-1">
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">Feedback IA</p>
              {llmFeedback}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
