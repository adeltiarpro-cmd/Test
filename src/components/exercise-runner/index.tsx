"use client";

import { useState, useRef } from "react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/cn";
import { MathText } from "./mdx";
import { ResultPanel } from "./result-panel";
import { McqRunner } from "./runners/mcq";
import { NumericRunner } from "./runners/numeric";
import { FormulaClozeRunner } from "./runners/formula-cloze";
import { ShortAnswerRunner } from "./runners/short-answer";
import { GraphFillRunner } from "./runners/graph-fill";
import { ExcelModelRunner } from "./runners/excel-model";
import { StatementInteractiveRunner } from "./runners/statement-interactive";
import { CaseMathRunner } from "./runners/case-math";
import { CaseStructuringRunner } from "./runners/case-structuring";
import { MarketSizingRunner } from "./runners/market-sizing";
import { submitAttempt } from "@/lib/session-actions";
import type { AttemptResult } from "@/lib/session-actions";

export type SessionExercise = {
  id: string;
  type:
    | "mcq"
    | "numeric"
    | "formula_cloze"
    | "short_answer"
    | "graph_fill"
    | "excel_model"
    | "statement_interactive"
    | "case_math"
    | "case_structuring"
    | "market_sizing";
  difficulty: number;
  payload: Record<string, unknown>;
  tags: string[];
  module_id?: string;
};

interface ExerciseRunnerProps {
  exercise: SessionExercise;
  onNext: () => void;
}

const DIFFICULTY_LABELS: Record<number, string> = {
  1: "Très facile",
  2: "Facile",
  3: "Moyen",
  4: "Difficile",
  5: "Expert",
};
const CONFIDENCE_LABELS: Record<1 | 2 | 3, string> = {
  1: "Au hasard",
  2: "Incertain",
  3: "Sûr",
};

const TYPE_LABELS: Record<string, string> = {
  mcq: "QCM",
  numeric: "Numérique",
  formula_cloze: "Formule à trous",
  short_answer: "Réponse courte",
  graph_fill: "Graphe à trous",
  excel_model: "Modèle Excel",
  statement_interactive: "État financier interactif",
  case_math: "Math de Cas",
  case_structuring: "Structuration de Cas",
  market_sizing: "Market Sizing",
};

// Grid-based runners stay mounted so colored cells remain visible.
const GRID_TYPES = new Set(["excel_model", "statement_interactive"]);
// Case runners stay mounted so rubric results and LLM button remain visible.
const CASE_TYPES = new Set(["case_structuring", "market_sizing"]);
const PERSISTENT_TYPES = new Set([...GRID_TYPES, ...CASE_TYPES]);

export function ExerciseRunner({ exercise, onNext }: ExerciseRunnerProps) {
  const [result, setResult] = useState<AttemptResult | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const startRef = useRef(Date.now());
  const resultRef = useRef<HTMLDivElement>(null);
  const [confidence, setConfidence] = useState<1 | 2 | 3>(2);

  const pay = exercise.payload as Record<string, unknown>;
  const promptMdx = (pay.prompt_mdx as string | undefined) ?? "";
  const isPersistent = PERSISTENT_TYPES.has(exercise.type);
  const isGrid = GRID_TYPES.has(exercise.type);

  async function handleSubmit(answer: Record<string, unknown>) {
    if (isSubmitting || result) return;
    setIsSubmitting(true);
    try {
      const res = await submitAttempt(
        exercise.id,
        { type: exercise.type, ...answer } as Parameters<typeof submitAttempt>[1],
        Date.now() - startRef.current,
        confidence
      );
      setResult(res);
      setTimeout(
        () => resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }),
        50
      );
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <article className="flex flex-col gap-4 rounded-lg border border-border bg-card p-4 shadow-md">
      {/* Header */}
      <header className="flex items-center gap-2 flex-wrap">
        <Badge variant="outline">{TYPE_LABELS[exercise.type] ?? exercise.type}</Badge>
        <Badge
          variant={
            exercise.difficulty >= 4
              ? "accent"
              : exercise.difficulty === 3
              ? "default"
              : "muted"
          }
        >
          {DIFFICULTY_LABELS[exercise.difficulty] ?? `Niveau ${exercise.difficulty}`}
        </Badge>
        {exercise.tags.slice(0, 3).map((tag) => (
          <Badge key={tag} variant="muted">
            {tag}
          </Badge>
        ))}
      </header>

      {/* Prompt */}
      {promptMdx && (
        <div className="text-base text-foreground leading-relaxed">
          <MathText>{promptMdx}</MathText>
        </div>
      )}

      {/* Confidence selector — set before submitting */}
      {!result && (
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-muted-foreground shrink-0">Confiance :</span>
          {([1, 2, 3] as const).map((c) => (
            <button
              key={c}
              type="button"
              onClick={() => setConfidence(c)}
              className={cn(
                "px-2 py-0.5 rounded text-xs font-medium border transition-colors",
                confidence === c
                  ? "bg-primary text-primary-foreground border-primary"
                  : "text-muted-foreground border-border hover:border-foreground hover:text-foreground"
              )}
            >
              {CONFIDENCE_LABELS[c]}
            </button>
          ))}
        </div>
      )}

      {/* Runner — persistent types stay visible after submission */}
      {(!result || isPersistent) && (
        <div aria-live="polite">
          {exercise.type === "mcq" && (
            <McqRunner
              payload={pay as Parameters<typeof McqRunner>[0]["payload"]}
              onSubmit={(selectedKeys) => handleSubmit({ selected_keys: selectedKeys })}
              disabled={isSubmitting}
            />
          )}
          {exercise.type === "numeric" && (
            <NumericRunner
              payload={pay as Parameters<typeof NumericRunner>[0]["payload"]}
              onSubmit={(value) => handleSubmit({ value })}
              disabled={isSubmitting}
            />
          )}
          {exercise.type === "formula_cloze" && (
            <FormulaClozeRunner
              payload={pay as Parameters<typeof FormulaClozeRunner>[0]["payload"]}
              onSubmit={(blanks) => handleSubmit({ blanks })}
              disabled={isSubmitting}
            />
          )}
          {exercise.type === "short_answer" && (
            <ShortAnswerRunner
              payload={pay as Parameters<typeof ShortAnswerRunner>[0]["payload"]}
              onSubmit={(text) => handleSubmit({ text })}
              disabled={isSubmitting}
            />
          )}
          {exercise.type === "graph_fill" && (
            <GraphFillRunner
              payload={pay as Parameters<typeof GraphFillRunner>[0]["payload"]}
              onSubmit={(nodes) => handleSubmit({ nodes })}
              disabled={isSubmitting}
            />
          )}
          {exercise.type === "excel_model" && (
            <ExcelModelRunner
              payload={pay as Parameters<typeof ExcelModelRunner>[0]["payload"]}
              onSubmit={(cells) => handleSubmit({ cells })}
              disabled={isSubmitting}
              cellResults={result?.cellResults}
            />
          )}
          {exercise.type === "statement_interactive" && (
            <StatementInteractiveRunner
              payload={pay as Parameters<typeof StatementInteractiveRunner>[0]["payload"]}
              onSubmit={(values) => handleSubmit({ values })}
              disabled={isSubmitting}
              lineResults={result?.lineResults}
            />
          )}
          {exercise.type === "case_math" && (
            <CaseMathRunner
              payload={pay as Parameters<typeof CaseMathRunner>[0]["payload"]}
              onSubmit={(value) => handleSubmit({ value })}
              disabled={isSubmitting || !!result}
            />
          )}
          {exercise.type === "case_structuring" && (
            <CaseStructuringRunner
              payload={pay as Parameters<typeof CaseStructuringRunner>[0]["payload"]}
              onSubmit={(text) => handleSubmit({ text })}
              disabled={isSubmitting || !!result}
              rubricResults={result?.rubricResults}
              exerciseId={exercise.id}
            />
          )}
          {exercise.type === "market_sizing" && (
            <MarketSizingRunner
              payload={pay as Parameters<typeof MarketSizingRunner>[0]["payload"]}
              onSubmit={(finalValue, reasoning) => handleSubmit({ final_value: finalValue, reasoning })}
              disabled={isSubmitting || !!result}
              exerciseId={exercise.id}
              submitted={!!result}
            />
          )}
          {isSubmitting && (
            <p className="text-sm text-muted-foreground animate-pulse mt-2">
              Correction en cours…
            </p>
          )}
        </div>
      )}

      {/* Result */}
      {result && (
        <div ref={resultRef} aria-live="assertive">
          {/* Grid types: compact score line instead of full ResultPanel */}
          {isGrid ? (
            <p
              className={cn(
                "text-sm font-semibold mt-2",
                result.isCorrect ? "text-green-700" : "text-foreground"
              )}
            >
              {result.isCorrect
                ? "✓ Tout correct"
                : `Score : ${Math.round(result.score * 100)} %`}
            </p>
          ) : (
            <ResultPanel result={result} exerciseType={exercise.type} />
          )}
          <button
            type="button"
            onClick={onNext}
            className="mt-4 inline-flex items-center justify-center gap-2 rounded-md bg-accent text-accent-foreground font-semibold px-4 py-2 min-h-[44px] transition-all duration-200 hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 cursor-pointer"
          >
            Exercice suivant →
          </button>
        </div>
      )}
    </article>
  );
}
