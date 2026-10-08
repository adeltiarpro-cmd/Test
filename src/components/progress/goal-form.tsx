"use client";

import { useTransition, useState } from "react";
import { saveGoal } from "@/lib/progress-actions";

interface GoalFormProps {
  targetDate: string | null;
  dailyGoal: number | null;
}

export function GoalForm({ targetDate, dailyGoal }: GoalFormProps) {
  const [isPending, startTransition] = useTransition();
  const [saved, setSaved] = useState(false);

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    startTransition(async () => {
      await saveGoal(formData);
      setSaved(true);
      setTimeout(() => setSaved(false), 2500);
    });
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap items-end gap-3">
      <div className="flex flex-col gap-1">
        <label htmlFor="target_date" className="text-xs text-muted-foreground">
          Date d&apos;entretien (optionnelle)
        </label>
        <input
          id="target_date"
          name="target_date"
          type="date"
          defaultValue={targetDate ?? ""}
          className="h-9 rounded-md border border-border bg-background px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        />
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="daily_goal" className="text-xs text-muted-foreground">
          Objectif (questions/jour)
        </label>
        <input
          id="daily_goal"
          name="daily_goal"
          type="number"
          min={1}
          max={500}
          defaultValue={dailyGoal ?? ""}
          placeholder="ex. 20"
          className="h-9 w-28 rounded-md border border-border bg-background px-3 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        />
      </div>
      <button
        type="submit"
        disabled={isPending}
        className="h-9 rounded-md bg-primary text-primary-foreground text-sm font-semibold px-4 hover:opacity-90 disabled:opacity-50 transition-opacity focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        {isPending ? "Enregistrement…" : saved ? "Enregistré ✓" : "Enregistrer"}
      </button>
    </form>
  );
}
