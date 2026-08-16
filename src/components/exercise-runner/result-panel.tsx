"use client";

import { CheckCircle2, XCircle } from "lucide-react";
import { MathText } from "./mdx";
import { Badge } from "@/components/ui/badge";
import { Callout } from "@/components/ui/callout";
import type { AttemptResult } from "@/lib/session-actions";

interface ResultPanelProps {
  result: AttemptResult;
  exerciseType: string;
}

export function ResultPanel({ result, exerciseType }: ResultPanelProps) {
  return (
    <div className="flex flex-col gap-3 border-t border-border pt-4 mt-4">
      {/* Verdict */}
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

      {/* Main explanation */}
      {result.explanation && (
        <Callout variant={result.isCorrect ? "success" : "info"} title="Explication">
          <MathText>{result.explanation}</MathText>
        </Callout>
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
    </div>
  );
}
