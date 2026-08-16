"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { MathText } from "../mdx";

type Blank = {
  key: string;
  kind: "token" | "expression" | "number";
  hint?: string;
  options?: string[];
};

interface FormulaClozeRunnerProps {
  payload: {
    template_mdx: string;
    blanks: Blank[];
  };
  onSubmit: (blanks: Record<string, string>) => void;
  disabled?: boolean;
}

// Replace {{key}} in template with labelled placeholder for display.
function buildDisplayTemplate(template: string, blanks: Blank[]): string {
  return blanks.reduce((t, b) => {
    const label = b.hint ?? b.key;
    return t.replace(new RegExp(`\\{\\{${b.key}\\}\\}`, "g"), `**[${label}]**`);
  }, template);
}

export function FormulaClozeRunner({ payload, onSubmit, disabled }: FormulaClozeRunnerProps) {
  const [answers, setAnswers] = useState<Record<string, string>>(() =>
    Object.fromEntries(payload.blanks.map((b) => [b.key, ""]))
  );

  const allFilled = payload.blanks.every((b) => (answers[b.key] ?? "").trim() !== "");
  const displayTemplate = buildDisplayTemplate(payload.template_mdx, payload.blanks);

  return (
    <div className="flex flex-col gap-4">
      {/* Rendered template showing where blanks are */}
      <div className="rounded-md border border-border bg-muted px-3 py-2 text-sm">
        <p className="text-xs text-muted-foreground mb-1 font-medium uppercase tracking-wide">
          Modèle
        </p>
        <MathText>{displayTemplate}</MathText>
      </div>

      {/* Input per blank */}
      <div className="flex flex-col gap-3">
        {payload.blanks.map((blank) => {
          if (blank.options && blank.options.length > 0) {
            return (
              <div key={blank.key} className="flex flex-col gap-1">
                <label className="text-sm font-medium text-foreground">
                  {blank.hint ?? blank.key}
                </label>
                <div className="flex flex-wrap gap-2">
                  {blank.options.map((opt) => (
                    <button
                      key={opt}
                      type="button"
                      disabled={disabled}
                      onClick={() => !disabled && setAnswers((a) => ({ ...a, [blank.key]: opt }))}
                      className={`rounded border px-3 py-1.5 text-sm font-mono transition-colors cursor-pointer min-h-[44px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${
                        answers[blank.key] === opt
                          ? "border-primary bg-primary/10 text-primary font-semibold"
                          : "border-border bg-card text-foreground hover:bg-muted"
                      } ${disabled ? "opacity-60 cursor-not-allowed" : ""}`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>
            );
          }

          return (
            <Input
              key={blank.key}
              label={blank.hint ?? blank.key}
              value={answers[blank.key] ?? ""}
              onChange={(e) =>
                setAnswers((a) => ({ ...a, [blank.key]: e.target.value }))
              }
              disabled={disabled}
              className="font-mono"
              placeholder={blank.kind === "number" ? "0.00" : blank.kind === "token" ? "EBIT" : "expression…"}
            />
          );
        })}
      </div>

      <Button
        variant="primary"
        size="md"
        disabled={!allFilled || disabled}
        onClick={() => onSubmit(answers)}
      >
        Valider
      </Button>
    </div>
  );
}
