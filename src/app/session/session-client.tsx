"use client";

import { useState } from "react";
import Link from "next/link";
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
      <>
        <SessionTopbar breadcrumb={null} current={0} total={0} />
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <p className="text-lg font-semibold text-foreground">
            Aucun exercice disponible pour le moment.
          </p>
          <p className="text-sm text-muted-foreground">
            Importez du contenu via le pipeline d&apos;ingestion.
          </p>
        </div>
      </>
    );
  }

  const exercise = exercises[index];

  if (done) {
    return (
      <>
        <SessionTopbar breadcrumb={null} current={exercises.length} total={exercises.length} />
        <div className="flex flex-col items-center gap-5 py-20 text-center">
          <CheckCircle2 className="h-12 w-12 text-green-400" />
          <h2 className="text-xl font-semibold text-foreground">Session terminée !</h2>
          <p className="text-sm text-muted-foreground">
            {exercises.length} exercice{exercises.length > 1 ? "s" : ""} complété{exercises.length > 1 ? "s" : ""}.
          </p>
          <button
            type="button"
            onClick={() => { setIndex(0); setDone(false); }}
            className="inline-flex items-center justify-center rounded-lg bg-primary text-primary-foreground font-semibold px-5 py-2.5 min-h-[44px] hover:opacity-90 transition-opacity focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            Recommencer
          </button>
        </div>
      </>
    );
  }

  function handleNext() {
    if (index + 1 >= exercises.length) setDone(true);
    else setIndex((i) => i + 1);
  }

  function handlePrev() {
    setIndex((i) => Math.max(0, i - 1));
  }

  return (
    <>
      <SessionTopbar
        breadcrumb={exercise.breadcrumb ?? null}
        current={index + 1}
        total={exercises.length}
      />
      <div className="max-w-3xl mx-auto px-5 py-10 pb-20">
        <ExerciseRunner
          key={exercise.id}
          exercise={exercise}
          onNext={handleNext}
          onPrev={index > 0 ? handlePrev : undefined}
        />
      </div>
    </>
  );
}

/* ── Topbar sticky ── */

interface TopbarProps {
  breadcrumb: SessionExercise["breadcrumb"] | null;
  current: number;
  total: number;
}

function SessionTopbar({ breadcrumb, current, total }: TopbarProps) {
  const pct = total > 0 ? Math.round(((current - 1) / total) * 100) : 0;

  const crumbs: string[] = [];
  if (breadcrumb?.track) crumbs.push(breadcrumb.track);
  if (breadcrumb?.chapter) crumbs.push(breadcrumb.chapter);
  if (breadcrumb?.subchapter) crumbs.push(breadcrumb.subchapter);

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/80">
      <div className="max-w-3xl mx-auto px-5 h-12 flex items-center gap-3">
        {/* Logo */}
        <span className="text-sm font-bold text-foreground shrink-0">Prep</span>

        {/* Breadcrumb */}
        {crumbs.length > 0 && (
          <>
            <span className="text-border text-lg font-light shrink-0">/</span>
            <nav className="flex items-center gap-1.5 text-xs text-muted-foreground min-w-0 overflow-hidden">
              {crumbs.map((c, i) => (
                <span key={i} className="flex items-center gap-1.5 min-w-0">
                  {i > 0 && <span className="opacity-40 shrink-0">›</span>}
                  <span
                    className={
                      i === crumbs.length - 1
                        ? "font-semibold text-foreground truncate"
                        : "truncate"
                    }
                  >
                    {c}
                  </span>
                </span>
              ))}
            </nav>
          </>
        )}

        {/* Spacer */}
        <div className="flex-1" />

        {/* Progress pill */}
        {total > 0 && (
          <div className="flex items-center gap-2 bg-muted border border-border rounded-full px-3 py-1 shrink-0">
            <div className="w-16 h-1 rounded-full bg-border overflow-hidden">
              <div
                className="h-full bg-primary rounded-full transition-all duration-300"
                style={{ width: `${pct}%` }}
              />
            </div>
            <span className="text-xs font-mono font-semibold text-foreground tabular-nums">
              {current} / {total}
            </span>
          </div>
        )}

        {/* Exit */}
        <Link
          href="/dashboard"
          className="text-xs text-muted-foreground border border-border rounded-md px-2.5 py-1 hover:text-foreground hover:border-muted-foreground transition-colors shrink-0"
        >
          Quitter
        </Link>
      </div>
    </header>
  );
}
