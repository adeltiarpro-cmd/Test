"use client";

import { useState } from "react";
import { ExerciseRunner } from "@/components/exercise-runner";
import type { SessionExercise } from "@/components/exercise-runner";
import { CheckCircle2 } from "lucide-react";

interface SessionClientProps {
  exercises: SessionExercise[];
}

export function SessionClient({ exercises }: SessionClientProps) {
  const [index, setIndex] = useState(0);
  const [done, setDone] = useState(false);

  if (exercises.length === 0) {
    return (
      <div className="flex flex-col items-center gap-3 py-16 text-center">
        <p className="text-lg font-semibold text-foreground">
          Aucun exercice disponible pour le moment.
        </p>
        <p className="text-sm text-muted-foreground">
          Importez du contenu via le pipeline d&apos;ingestion.
        </p>
      </div>
    );
  }

  if (done) {
    return (
      <div className="flex flex-col items-center gap-4 py-16 text-center">
        <CheckCircle2 className="h-12 w-12 text-green-600" />
        <h2 className="text-xl font-semibold text-foreground">Session terminée !</h2>
        <p className="text-sm text-muted-foreground">
          {exercises.length} exercice{exercises.length > 1 ? "s" : ""} complété{exercises.length > 1 ? "s" : ""}.
        </p>
        <button
          type="button"
          onClick={() => { setIndex(0); setDone(false); }}
          className="inline-flex items-center justify-center gap-2 rounded-md bg-primary text-primary-foreground font-semibold px-4 py-2 min-h-[44px] transition-all duration-200 hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 cursor-pointer"
        >
          Recommencer
        </button>
      </div>
    );
  }

  const exercise = exercises[index];

  return (
    <div className="flex flex-col gap-4">
      {/* Progress */}
      <div className="flex items-center gap-3">
        <div
          className="h-2 flex-1 rounded-full bg-muted overflow-hidden"
          role="progressbar"
          aria-valuenow={index}
          aria-valuemin={0}
          aria-valuemax={exercises.length}
          aria-label="Progression de la session"
        >
          <div
            className="h-full bg-primary transition-all duration-300"
            style={{ width: `${(index / exercises.length) * 100}%` }}
          />
        </div>
        <span className="text-xs tabular-nums text-muted-foreground whitespace-nowrap">
          {index + 1} / {exercises.length}
        </span>
      </div>

      <ExerciseRunner
        key={exercise.id}
        exercise={exercise}
        onNext={() => {
          if (index + 1 >= exercises.length) setDone(true);
          else setIndex((i) => i + 1);
        }}
      />
    </div>
  );
}
