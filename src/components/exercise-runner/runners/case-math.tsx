"use client";

import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";

interface CaseMathRunnerProps {
  payload: { time_limit_seconds: number };
  onSubmit: (value: number) => void;
  disabled?: boolean;
}

export function CaseMathRunner({ payload, onSubmit, disabled }: CaseMathRunnerProps) {
  const [input, setInput] = useState("");
  const [timeLeft, setTimeLeft] = useState(payload.time_limit_seconds);
  const [expired, setExpired] = useState(false);
  const inputRef = useRef("");
  const submittedRef = useRef(false);

  function handleChange(val: string) {
    setInput(val);
    inputRef.current = val;
  }

  useEffect(() => {
    if (disabled) return;
    const id = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(id);
          setExpired(true);
          if (!submittedRef.current) {
            submittedRef.current = true;
            const num = parseFloat(inputRef.current.replace(",", "."));
            onSubmit(isNaN(num) ? 0 : num);
          }
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [disabled, onSubmit]);

  function handleManualSubmit() {
    if (submittedRef.current || disabled || expired) return;
    submittedRef.current = true;
    const num = parseFloat(input.replace(",", "."));
    onSubmit(isNaN(num) ? 0 : num);
  }

  const minutes = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  const timeStr = `${minutes}:${String(secs).padStart(2, "0")}`;
  const urgent = timeLeft <= 10 && timeLeft > 0;

  return (
    <div className="flex flex-col gap-3">
      {!disabled && (
        <p className={`text-sm font-mono font-semibold tabular-nums ${urgent ? "text-destructive" : "text-muted-foreground"}`}>
          ⏱ {timeStr}
        </p>
      )}
      <div className="flex gap-2">
        <input
          type="text"
          inputMode="decimal"
          value={input}
          onChange={(e) => handleChange(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") handleManualSubmit(); }}
          disabled={!!disabled || expired}
          placeholder="Votre réponse…"
          className="flex-1 rounded-md border border-border bg-card px-3 py-2 text-base text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <Button
          variant="primary"
          size="md"
          disabled={input.trim() === "" || !!disabled || expired}
          onClick={handleManualSubmit}
        >
          Valider
        </Button>
      </div>
      {expired && (
        <p className="text-sm text-destructive font-medium">Temps écoulé — réponse soumise automatiquement.</p>
      )}
    </div>
  );
}
