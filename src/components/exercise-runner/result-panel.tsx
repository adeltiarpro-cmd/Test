"use client";

import { CheckCircle2, XCircle } from "lucide-react";
import { MathText } from "./mdx";
import { Badge } from "@/components/ui/badge";
import { Callout } from "@/components/ui/callout";
import type { AttemptResult } from "@/lib/session-actions";

interface ResultPanelProps {
  result: AttemptResult;
  exerciseType: string;
  /** Called when user clicks "Ma réponse était juste" on a partial-scored exercise. */
  onOverride?: () => void;
}

export function ResultPanel({ result, exerciseType, onOverride }: ResultPanelProps) {
  const isSelfEval = result.scoringMode === "self_eval";
  const isPartial = result.scoringMode === "partial";

  return (
    <div className="flex flex-col gap-3 border-t border-border pt-4 mt-4">
      {/* Verdict — skipped for self_eval (user already saw the corrigé + chose their rating) */}
      {!isSelfEval && (
        <div className="flex items-center gap-2">
          {result.isCorrect ? (
            <CheckCircle2 className="h-5 w-5 text-green-600 shrink-0" />
          ) : (
            <XCircle className="h-5 w-5 text-destructive shrink-0" />
          )}
          <span className={`font-semibold ${result.isCorrect ? "text-green-700" : "text-destructive"}`}>
            {result.isCorrect ? "Correct" : "Incorrect"}
          </span>
          {result.score > 0 && result.score < 1 && (
            <Badge variant="muted" className="tabular-nums ml-auto">
              {Math.round(result.score * 100)} %
            </Badge>
          )}
        </div>
      )}

      {/* Self-eval: compact confirmation */}
      {isSelfEval && (
        <div className="flex items-center gap-2">
          {result.isCorrect ? (
            <CheckCircle2 className="h-5 w-5 text-green-600 shrink-0" />
          ) : (
            <XCircle className="h-5 w-5 text-amber-500 shrink-0" />
          )}
          <span className={`text-sm font-medium ${result.isCorrect ? "text-green-700" : "text-amber-700"}`}>
            {result.isCorrect ? "Enregistré — programmé pour révision" : "Noté pour retravailler"}
          </span>
        </div>
      )}

      {/* Main explanation — not repeated for self_eval (already shown during peek) */}
      {!isSelfEval && result.explanation && (
        <Callout variant={result.isCorrect ? "success" : "info"} title="Explication">
          <MathText>{result.explanation}</MathText>
        </Callout>
      )}

      {/* Partial scoring: covered / missed key-points */}
      {isPartial && result.pointResults && result.pointResults.length > 0 && (
        <div className="flex flex-col gap-1.5">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
            Points couverts
          </p>
          {result.pointResults.map((pt, i) => (
            <div key={i} className="flex items-start gap-2 text-sm">
              {pt.covered ? (
                <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 shrink-0" />
              ) : (
                <XCircle className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
              )}
              <span className={pt.covered ? "text-foreground" : "text-muted-foreground"}>
                {pt.text}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Partial: override button */}
      {isPartial && !result.isCorrect && onOverride && (
        <button
          type="button"
          onClick={onOverride}
          className="self-start text-xs text-muted-foreground hover:text-foreground underline underline-offset-2 transition-colors"
        >
          Ma réponse était juste
        </button>
      )}

      {/* MCQ: per-distractor explanations */}
      {result.distractorExplains && Object.keys(result.distractorExplains).length > 0 && (
        <div className="flex flex-col gap-1.5">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
            Analyse des distracteurs
          </p>
          {Object.entries(result.distractorExplains).map(([key, explain]) => (
            <div key={key} className="flex gap-2 text-sm">
              <Badge variant="outline" className="shrink-0">{key}</Badge>
              <MathText className="text-muted-foreground leading-snug">{explain}</MathText>
            </div>
          ))}
        </div>
      )}

      {/* Formula cloze: per-blank feedback */}
      {result.blankFeedback && Object.keys(result.blankFeedback).length > 0 && (
        <div className="flex flex-col gap-1.5">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
            Résultats par champ
          </p>
          {Object.entries(result.blankFeedback).map(([key, fb]) => (
            <div key={key} className="flex items-start gap-2 text-sm">
              {fb.correct ? (
                <CheckCircle2 className="h-4 w-4 text-green-600 mt-0.5 shrink-0" />
              ) : (
                <XCircle className="h-4 w-4 text-destructive mt-0.5 shrink-0" />
              )}
              <div>
                <span className="font-medium">{key}</span>
                {!fb.correct && (
                  <span className="text-muted-foreground"> — réponse attendue : </span>
                )}
                {!fb.correct && (
                  <MathText className="inline">{fb.canonical}</MathText>
                )}
                {exerciseType === "formula_cloze" && fb.explain && (
                  <MathText className="text-muted-foreground mt-0.5">{fb.explain}</MathText>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Leech warning */}
      {result.isLeech && (
        <Callout variant="warning" title="Point bloquant — 4+ erreurs sur cet exercice">
          <p>Recommandation : revoir les prérequis avant de continuer.</p>
          {result.prerequisiteConcepts && result.prerequisiteConcepts.length > 0 && (
            <ul className="mt-1 list-disc list-inside">
              {result.prerequisiteConcepts.map((c) => (
                <li key={c.id} className="text-sm">{c.title}</li>
              ))}
            </ul>
          )}
        </Callout>
      )}
    </div>
  );
}
