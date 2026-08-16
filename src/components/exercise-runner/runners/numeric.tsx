"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface NumericRunnerProps {
  payload: {
    unit?: string;
    precision: number;
    sub_answers?: { key: string; label: string; unit: string; precision: number }[];
  };
  onSubmit: (value: number) => void;
  disabled?: boolean;
}

export function NumericRunner({ payload, onSubmit, disabled }: NumericRunnerProps) {
  const [raw, setRaw] = useState("");
  const [error, setError] = useState<string | undefined>();

  function handleSubmit() {
    const parsed = parseFloat(raw.replace(",", "."));
    if (isNaN(parsed)) {
      setError("Veuillez entrer un nombre valide.");
      return;
    }
    setError(undefined);
    onSubmit(parsed);
  }

  return (
    <div className="flex flex-col gap-3">
      <Input
        label={`Réponse${payload.unit ? ` (${payload.unit})` : ""}`}
        type="text"
        inputMode="decimal"
        placeholder={`ex. ${payload.precision > 0 ? "3.14" : "42"}`}
        value={raw}
        onChange={(e) => setRaw(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && !disabled && handleSubmit()}
        error={error}
        disabled={disabled}
        className="font-mono tabular-nums"
      />
      {payload.precision > 0 && (
        <p className="text-xs text-muted-foreground">
          Précision demandée : {payload.precision} décimale{payload.precision > 1 ? "s" : ""}.
        </p>
      )}
      <Button
        variant="primary"
        size="md"
        disabled={raw.trim() === "" || disabled}
        onClick={handleSubmit}
      >
        Valider
      </Button>
    </div>
  );
}
