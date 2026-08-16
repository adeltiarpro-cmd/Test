"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { MathText } from "../mdx";
import { cn } from "@/lib/cn";

type McqOption = { key: string; text_mdx: string };

interface McqRunnerProps {
  payload: { options: McqOption[]; multiple: boolean; shuffle: boolean };
  onSubmit: (selectedKeys: string[]) => void;
  disabled?: boolean;
}

export function McqRunner({ payload, onSubmit, disabled }: McqRunnerProps) {
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const options = useMemo<McqOption[]>(() => {
    if (!payload.shuffle) return payload.options;
    return [...payload.options].sort(() => Math.random() - 0.5);
  }, [payload.options, payload.shuffle]);

  function toggle(key: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (payload.multiple) {
        if (next.has(key)) next.delete(key);
        else next.add(key);
      } else {
        next.clear();
        next.add(key);
      }
      return next;
    });
  }

  return (
    <div className="flex flex-col gap-3">
      <p className="text-xs text-muted-foreground">
        {payload.multiple ? "Sélectionnez toutes les réponses correctes." : "Sélectionnez une réponse."}
      </p>

      <div role="group" aria-label="Options de réponse" className="flex flex-col gap-2">
        {options.map((opt) => {
          const isSelected = selected.has(opt.key);
          return (
            <button
              key={opt.key}
              type="button"
              onClick={() => !disabled && toggle(opt.key)}
              disabled={disabled}
              aria-pressed={isSelected}
              className={cn(
                "flex items-start gap-3 rounded-md border px-3 py-2 text-left text-sm transition-colors duration-150 cursor-pointer min-h-[44px]",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                isSelected
                  ? "border-primary bg-primary/10 text-primary font-medium"
                  : "border-border bg-card text-foreground hover:bg-muted",
                disabled && "opacity-60 cursor-not-allowed"
              )}
            >
              <span
                className={cn(
                  "mt-px flex h-5 w-5 shrink-0 items-center justify-center rounded border text-xs font-bold",
                  payload.multiple ? "rounded-sm" : "rounded-full",
                  isSelected ? "border-primary bg-primary text-white" : "border-border"
                )}
                aria-hidden="true"
              >
                {isSelected && (payload.multiple ? "✓" : opt.key)}
                {!isSelected && !payload.multiple && opt.key}
              </span>
              <MathText className="flex-1 leading-snug">{opt.text_mdx}</MathText>
            </button>
          );
        })}
      </div>

      <Button
        variant="primary"
        size="md"
        disabled={selected.size === 0 || disabled}
        onClick={() => onSubmit([...selected])}
      >
        Valider
      </Button>
    </div>
  );
}
