"use client";

import { useState, useRef } from "react";
import { Callout } from "@/components/ui/callout";
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
import { NumericStepsRunner } from "./runners/numeric-steps";
import {
  submitAttempt,
  peekSelfEvalAnswer,
  overrideToCorrect,
} from "@/lib/session-actions";
import type { AttemptResult } from "@/lib/session-actions";

export type Breadcrumb = {
  track: string;
  chapter?: string;
  subchapter?: string;
};

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
    | "market_sizing"
    | "numeric_steps";
  difficulty: number;
  payload: Record<string, unknown>;
  tags: string[];
  module_id?: string;
  breadcrumb?: Breadcrumb;
};

interface ExerciseRunnerProps {
  exercise: SessionExercise;
  onNext: () => void;
  onPrev?: () => void;
  /** Aperçu admin : l'exercice s'affiche, mais rien n'est envoyé ni enregistré. */
  preview?: boolean;
}

const CONFIDENCE_LABELS: Record<1 | 2 | 3, string> = {
  1: "Au hasard",
  2: "Incertain",
  3: "Sûr",
};

const SELF_EVAL_LABELS: Record<1 | 2 | 3, string> = {
  1: "À revoir",
  2: "Moyen",
  3: "Maîtrisé",
};

const TYPE_LABELS: Record<string, string> = {
  mcq:                    "QCM",
  numeric:                "Numérique",
  formula_cloze:          "Formule à trous",
  short_answer:           "Réponse courte",
  graph_fill:             "Graphe à trous",
  excel_model:            "Modèle Excel",
  statement_interactive:  "État financier",
  case_math:              "Math de Cas",
  case_structuring:       "Structuration",
  market_sizing:          "Market Sizing",
  numeric_steps:          "Exercice à étapes",
};

const TYPE_ABBREV: Record<string, string> = {
  numeric:               "NUM",
  mcq:                   "MCQ",
  short_answer:          "SA",
  formula_cloze:         "FC",
  graph_fill:            "GF",
  excel_model:           "EM",
  statement_interactive: "SI",
  case_math:             "CM",
  case_structuring:      "CS",
  market_sizing:         "MS",
  numeric_steps:         "NS",
};

// Grid-based runners stay mounted so colored cells remain visible.
const GRID_TYPES = new Set(["excel_model", "statement_interactive"]);
// Case runners stay mounted so rubric results and LLM button remain visible.
const CASE_TYPES = new Set(["case_structuring", "market_sizing"]);
// numeric_steps stays mounted so per-step results and solutions remain visible.
const PERSISTENT_TYPES = new Set([...GRID_TYPES, ...CASE_TYPES, "numeric_steps"]);

function deriveShortCode(id: string, type: string): string {
  const segs = id.split("-");
  const num = segs.at(-1) ?? "?";
  const abbrev = TYPE_ABBREV[type] ?? type.slice(0, 3).toUpperCase();
  return `${abbrev}-${num}`;
}

export function ExerciseRunner({ exercise, onNext, onPrev, preview = false }: ExerciseRunnerProps) {
  const [result, setResult] = useState<AttemptResult | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const startRef = useRef(Date.now());
  const resultRef = useRef<HTMLDivElement>(null);
  const [confidence, setConfidence] = useState<1 | 2 | 3>(2);

  // Self-eval two-step state
  const [selfEvalPhase, setSelfEvalPhase] = useState<"input" | "revealed">("input");
  const [selfEvalText, setSelfEvalText] = useState("");
  const [revealedModelAnswer, setRevealedModelAnswer] = useState<string | null>(null);

  const pay = exercise.payload as Record<string, unknown>;
  const promptMdx = (pay.prompt_mdx as string | undefined) ?? "";
  const scoringMode =
    exercise.type === "short_answer"
      ? ((pay.scoring_mode as string | undefined) ?? "auto")
      : "auto";
  const isSelfEval = scoringMode === "self_eval";
  const isPersistent = PERSISTENT_TYPES.has(exercise.type) || isSelfEval;
  const isGrid = GRID_TYPES.has(exercise.type);

  async function handleSubmit(answer: Record<string, unknown>) {
    if (preview || isSubmitting || result) return;
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
        () => resultRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" }),
        50
      );
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handlePeek(text: string) {
    if (preview || isSubmitting) return;
    setIsSubmitting(true);
    setSelfEvalText(text);
    try {
      const { model_answer_mdx } = await peekSelfEvalAnswer(exercise.id);
      setRevealedModelAnswer(model_answer_mdx);
      setSelfEvalPhase("revealed");
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleSelfEvalSubmit(rating: 1 | 2 | 3) {
    if (preview || isSubmitting || result) return;
    setIsSubmitting(true);
    try {
      const res = await submitAttempt(
        exercise.id,
        { type: "short_answer", text: selfEvalText },
        Date.now() - startRef.current,
        rating,
        rating
      );
      setResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleOverride() {
    if (preview) return;
    try {
      await overrideToCorrect(exercise.id);
      setResult((prev) =>
        prev ? { ...prev, isCorrect: true, score: 1, scoringMode: "partial" } : prev
      );
    } catch (e) {
      console.error(e);
    }
  }

  const shortCode = deriveShortCode(exercise.id, exercise.type);

  return (
    <article className="flex flex-col gap-6 rounded-xl border border-border bg-card p-8 shadow-[0_4px_32px_rgba(0,0,0,.4)]">
      {/* ── Meta row ── */}
      <div className="flex items-center gap-3 flex-wrap">
        <span className="inline-flex items-center rounded-md border border-primary/25 bg-primary/10 px-2.5 py-1 text-xs font-semibold uppercase tracking-wide text-primary">
          {TYPE_LABELS[exercise.type] ?? exercise.type}
        </span>
        {/* Difficulty dots (5) */}
        <span className="flex items-center gap-1" title={`Difficulté ${exercise.difficulty}/5`}>
          {Array.from({ length: 5 }, (_, i) => (
            <span
              key={i}
              className={cn(
                "w-1.5 h-1.5 rounded-full border",
                i < exercise.difficulty
                  ? "bg-muted-foreground border-muted-foreground"
                  : "border-muted-foreground/30"
              )}
            />
          ))}
        </span>
        <span className="ml-auto font-mono text-xs text-muted-foreground">{shortCode}</span>
      </div>

      {/* ── Subchapter label (serif) ── */}
      {exercise.breadcrumb?.subchapter && (
        <p className="font-serif text-lg font-semibold leading-snug text-foreground -mt-2">
          {exercise.breadcrumb.subchapter}
        </p>
      )}

      {/* ── Divider ── */}
      <div className="h-px bg-border" />

      {/* ── Prompt ── */}
      {promptMdx && (
        <div className="text-base text-foreground leading-relaxed max-w-prose">
          <MathText>{promptMdx}</MathText>
        </div>
      )}

      {/* ── Confidence selector (hidden for self_eval) ── */}
      {!result && !isSelfEval && (
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-muted-foreground shrink-0">Confiance :</span>
          {([1, 2, 3] as const).map((c) => (
            <button
              key={c}
              type="button"
              onClick={() => setConfidence(c)}
              className={cn(
                "px-2.5 py-1 rounded-md text-xs font-medium border transition-colors",
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

      {/* ── Runner — persistent types stay visible after submission ── */}
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
              onPeek={isSelfEval ? handlePeek : undefined}
              disabled={isSubmitting || (isSelfEval && selfEvalPhase === "revealed")}
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
          {exercise.type === "numeric_steps" && (
            <NumericStepsRunner
              payload={pay as Parameters<typeof NumericStepsRunner>[0]["payload"]}
              onSubmit={(steps) => handleSubmit({ steps })}
              disabled={isSubmitting || !!result}
              stepResults={result?.stepResults}
            />
          )}
          {isSubmitting && (
            <p className="text-sm text-muted-foreground animate-pulse mt-2">
              Correction en cours…
            </p>
          )}
        </div>
      )}

      {/* ── Self-eval: revealed model answer + rating buttons ── */}
      {isSelfEval && selfEvalPhase === "revealed" && revealedModelAnswer && !result && (
        <div className="flex flex-col gap-3 border-t border-border pt-4">
          <Callout variant="info" title="Corrigé">
            <MathText>{revealedModelAnswer}</MathText>
          </Callout>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-muted-foreground shrink-0">Votre auto-évaluation :</span>
            {([1, 2, 3] as const).map((r) => (
              <button
                key={r}
                type="button"
                disabled={isSubmitting}
                onClick={() => handleSelfEvalSubmit(r)}
                className={cn(
                  "px-3 py-1.5 rounded-md text-sm font-medium border transition-colors min-h-[36px]",
                  r === 1
                    ? "border-destructive/50 text-destructive hover:bg-destructive/10"
                    : r === 2
                    ? "border-amber-500/50 text-amber-400 hover:bg-amber-950/60"
                    : "border-green-500/50 text-green-400 hover:bg-green-950/60",
                  isSubmitting && "opacity-50 cursor-not-allowed"
                )}
              >
                {SELF_EVAL_LABELS[r]}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── Result ── */}
      {result && (
        <div ref={resultRef} aria-live="assertive">
          {isGrid ? (
            <p
              className={cn(
                "text-sm font-semibold mt-2",
                result.isCorrect ? "text-green-400" : "text-foreground"
              )}
            >
              {result.isCorrect
                ? "Tout correct"
                : `Score : ${Math.round(result.score * 100)} %`}
            </p>
          ) : (
            <ResultPanel
              result={result}
              exerciseType={exercise.type}
              onOverride={
                result.scoringMode === "partial" && !result.isCorrect
                  ? handleOverride
                  : undefined
              }
            />
          )}
        </div>
      )}

      {/* ── Navigation (visible après soumission) ── */}
      {result && (
        <div className="flex items-center justify-between gap-3 pt-2 border-t border-border">
          {onPrev ? (
            <button
              type="button"
              onClick={onPrev}
              className="inline-flex items-center justify-center rounded-lg border border-border text-muted-foreground text-sm font-medium px-4 py-2.5 min-h-[42px] hover:text-foreground hover:border-muted-foreground transition-colors"
            >
              ← Précédent
            </button>
          ) : (
            <div />
          )}
          <button
            type="button"
            onClick={onNext}
            className="inline-flex items-center justify-center rounded-lg bg-primary text-primary-foreground font-semibold text-sm px-5 py-2.5 min-h-[42px] hover:opacity-90 transition-opacity focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            Exercice suivant →
          </button>
        </div>
      )}
    </article>
  );
}
