"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

interface ShortAnswerRunnerProps {
  payload: { max_words: number; scoring_mode?: string };
  onSubmit: (text: string) => void;
  /** For self_eval mode — called instead of onSubmit to reveal the answer first. */
  onPeek?: (text: string) => void;
  disabled?: boolean;
}

function countWords(s: string) {
  return s.trim().split(/\s+/).filter(Boolean).length;
}

export function ShortAnswerRunner({ payload, onSubmit, onPeek, disabled }: ShortAnswerRunnerProps) {
  const [text, setText] = useState("");
  const words = countWords(text);
  const overLimit = words > payload.max_words;
  const isSelfEval = payload.scoring_mode === "self_eval";

  function handleAction() {
    if (isSelfEval && onPeek) {
      onPeek(text.trim());
    } else {
      onSubmit(text.trim());
    }
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-col gap-1">
        <label htmlFor="short-answer-input" className="text-sm font-medium text-foreground">
          Votre réponse
        </label>
        <textarea
          id="short-answer-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={disabled}
          rows={4}
          className="w-full rounded-md border border-border bg-card px-3 py-2 text-base text-foreground placeholder:text-muted-foreground resize-none transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 focus:border-primary disabled:opacity-50 disabled:cursor-not-allowed"
          placeholder="Rédigez votre réponse ici…"
          aria-describedby="word-count"
        />
        <p
          id="word-count"
          className={`text-xs tabular-nums text-right ${overLimit ? "text-destructive" : "text-muted-foreground"}`}
        >
          {words} / {payload.max_words} mots
        </p>
      </div>

      <Button
        variant="primary"
        size="md"
        disabled={text.trim().length === 0 || overLimit || disabled}
        onClick={handleAction}
      >
        {isSelfEval ? "Voir la correction" : "Valider"}
      </Button>
    </div>
  );
}
