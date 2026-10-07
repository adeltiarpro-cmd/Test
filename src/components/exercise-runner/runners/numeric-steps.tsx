"use client";

import { useState } from "react";
import { CheckCircle2, XCircle, ChevronDown, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { MathText } from "../mdx";
import { cn } from "@/lib/cn";
import type { StepResult } from "@/lib/session-actions";

type Step = {
  label: string;
  unit: string;
  tolerance: number;
  hint_mdx?: string;
  solution_mdx: string;
  trap_mdx?: string;
};

interface NumericStepsRunnerProps {
  payload: { steps: Step[] };
  onSubmit: (steps: number[]) => void;
  disabled?: boolean;
  stepResults?: StepResult[];
}

export function NumericStepsRunner({
  payload,
  onSubmit,
  disabled,
  stepResults,
}: NumericStepsRunnerProps) {
  const steps = payload.steps ?? [];
  const [inputs, setInputs] = useState<string[]>(() => steps.map(() => ""));
  const [currentStep, setCurrentStep] = useState(0);
  const [hintOpen, setHintOpen] = useState<boolean[]>(() => steps.map(() => false));
  const [solutionOpen, setSolutionOpen] = useState(false);

  const allDone = stepResults !== undefined;

  function setInput(i: number, val: string) {
    setInputs((prev) => {
      const next = [...prev];
      next[i] = val;
      return next;
    });
  }

  function toggleHint(i: number) {
    setHintOpen((prev) => {
      const next = [...prev];
      next[i] = !next[i];
      return next;
    });
  }

  function advanceStep() {
    if (currentStep < steps.length - 1) {
      setCurrentStep((s) => s + 1);
    }
  }

  function handleSubmit() {
    const values = inputs.map((v) => parseFloat(v.replace(",", ".")));
    onSubmit(values);
  }

  const isLastStep = currentStep === steps.length - 1;
  const currentValue = inputs[currentStep];
  const currentValid = currentValue !== "" && isFinite(parseFloat(currentValue.replace(",", ".")));

  return (
    <div className="flex flex-col gap-4">
      {/* Progress indicator */}
      <div className="flex items-center gap-1.5">
        {steps.map((s, i) => (
          <div
            key={i}
            title={s.label}
            className={cn(
              "h-1.5 flex-1 rounded-full transition-colors",
              allDone
                ? stepResults[i]?.isCorrect
                  ? "bg-green-500"
                  : "bg-destructive"
                : i < currentStep
                ? "bg-primary/60"
                : i === currentStep
                ? "bg-primary"
                : "bg-muted"
            )}
          />
        ))}
      </div>

      {/* Steps — show completed ones above current */}
      <div className="flex flex-col gap-3">
        {steps.map((step, i) => {
          const sr = stepResults?.[i];
          const isVisible = allDone || i <= currentStep;
          const isActive = !allDone && i === currentStep;
          const isCompleted = !allDone && i < currentStep;

          if (!isVisible) return null;

          return (
            <div
              key={i}
              className={cn(
                "rounded-lg border p-3 flex flex-col gap-2 transition-colors",
                allDone
                  ? sr?.isCorrect
                    ? "border-green-300 bg-green-50"
                    : "border-destructive/30 bg-destructive/5"
                  : isActive
                  ? "border-primary/50 bg-card"
                  : "border-border bg-muted/40"
              )}
            >
              {/* Step header */}
              <div className="flex items-center gap-2">
                {allDone && sr ? (
                  sr.isCorrect ? (
                    <CheckCircle2 className="h-4 w-4 text-green-600 shrink-0" />
                  ) : (
                    <XCircle className="h-4 w-4 text-destructive shrink-0" />
                  )
                ) : isCompleted ? (
                  <CheckCircle2 className="h-4 w-4 text-primary/50 shrink-0" />
                ) : (
                  <span className="h-4 w-4 rounded-full border-2 border-primary shrink-0 flex items-center justify-center text-[9px] font-bold text-primary">
                    {i + 1}
                  </span>
                )}
                <span className="text-sm font-semibold text-foreground">{step.label}</span>
              </div>

              {/* Input — active step only (or show frozen value if completed/done) */}
              {isActive && !disabled && (
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    step="any"
                    value={inputs[i]}
                    onChange={(e) => setInput(i, e.target.value)}
                    placeholder="0"
                    className="w-40 rounded-md border border-border bg-card px-3 py-1.5 text-base tabular-nums text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                    autoFocus
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && currentValid) {
                        isLastStep ? handleSubmit() : advanceStep();
                      }
                    }}
                  />
                  <span className="text-sm text-muted-foreground">{step.unit}</span>
                </div>
              )}

              {/* Frozen value for completed steps (before results) */}
              {isCompleted && (
                <p className="text-sm tabular-nums text-muted-foreground">
                  Votre réponse : <span className="font-medium text-foreground">{inputs[i]} {step.unit}</span>
                </p>
              )}

              {/* After scoring: show user answer + correct value if wrong */}
              {allDone && sr && (
                <div className="flex flex-col gap-1">
                  <p className="text-sm tabular-nums">
                    <span className="text-muted-foreground">Votre réponse : </span>
                    <span className={cn("font-medium", sr.isCorrect ? "text-green-700" : "text-destructive")}>
                      {inputs[i] || "—"} {step.unit}
                    </span>
                  </p>
                  {!sr.isCorrect && (
                    <p className="text-sm tabular-nums">
                      <span className="text-muted-foreground">Attendu : </span>
                      <span className="font-medium text-foreground">
                        {sr.correctValue} {step.unit}
                      </span>
                    </p>
                  )}
                </div>
              )}

              {/* Hint (active step only, before scoring) */}
              {isActive && step.hint_mdx && (
                <div>
                  <button
                    type="button"
                    onClick={() => toggleHint(i)}
                    className="flex items-center gap-1 text-xs font-medium text-blue-600 hover:text-blue-700 transition-colors"
                  >
                    {hintOpen[i] ? (
                      <ChevronDown className="h-3.5 w-3.5" />
                    ) : (
                      <ChevronRight className="h-3.5 w-3.5" />
                    )}
                    Indice
                  </button>
                  {hintOpen[i] && (
                    <div className="mt-1.5 rounded-md bg-blue-50 border border-blue-200 px-3 py-2 text-sm text-blue-900">
                      <MathText>{step.hint_mdx}</MathText>
                    </div>
                  )}
                </div>
              )}

              {/* After scoring: solution + trap */}
              {allDone && (
                <div className="flex flex-col gap-2 mt-1">
                  <pre className="rounded-md bg-muted border border-border px-3 py-2 text-xs font-mono leading-relaxed overflow-x-auto whitespace-pre-wrap">
                    <MathText>{step.solution_mdx}</MathText>
                  </pre>
                  {step.trap_mdx && (
                    <div className="rounded-md bg-amber-50 border border-amber-200 px-3 py-2">
                      <p className="text-[10px] font-bold uppercase tracking-wider text-amber-700 mb-1">
                        Piege
                      </p>
                      <div className="text-sm text-amber-900">
                        <MathText>{step.trap_mdx}</MathText>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Navigation / submit */}
      {!allDone && !disabled && (
        <div className="flex items-center gap-3">
          {!isLastStep ? (
            <Button
              variant="secondary"
              size="md"
              disabled={!currentValid}
              onClick={advanceStep}
            >
              Étape suivante →
            </Button>
          ) : (
            <Button
              variant="primary"
              size="md"
              disabled={!currentValid || disabled}
              onClick={handleSubmit}
            >
              Valider tout ({steps.length} étapes)
            </Button>
          )}
          <span className="text-xs text-muted-foreground tabular-nums">
            Étape {currentStep + 1} / {steps.length}
          </span>
        </div>
      )}

      {/* Global solution toggle (after scoring) */}
      {allDone && (
        <button
          type="button"
          onClick={() => setSolutionOpen((o) => !o)}
          className="flex items-center gap-1.5 text-xs font-medium text-green-700 hover:text-green-800 transition-colors self-start"
        >
          {solutionOpen ? (
            <ChevronDown className="h-3.5 w-3.5" />
          ) : (
            <ChevronRight className="h-3.5 w-3.5" />
          )}
          Solution complète
        </button>
      )}
    </div>
  );
}
