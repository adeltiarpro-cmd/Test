import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { SessionClient } from "./session-client";
import type { SessionExercise } from "@/components/exercise-runner";

export const metadata = { title: "Session — Prep Platform" };

const SUPPORTED_TYPES = ["mcq", "numeric", "formula_cloze", "short_answer"] as const;

export default async function SessionPage() {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  // 1. Try exercises due for review
  const { data: dueStates } = await supabase
    .from("review_states")
    .select("exercise_id")
    .eq("user_id", user.id)
    .lte("due_at", new Date().toISOString())
    .limit(10);

  const dueIds = (dueStates ?? []).map((s) => s.exercise_id as string);

  let exercises: SessionExercise[] = [];

  if (dueIds.length > 0) {
    const { data } = await supabase
      .from("exercises")
      .select("id, type, difficulty, payload, tags")
      .in("id", dueIds)
      .in("type", SUPPORTED_TYPES);
    exercises = (data ?? []) as SessionExercise[];
  }

  // 2. Fallback: newest exercises of supported types (includes new ones)
  if (exercises.length < 5) {
    const { data } = await supabase
      .from("exercises")
      .select("id, type, difficulty, payload, tags")
      .in("type", SUPPORTED_TYPES)
      .order("created_at", { ascending: false })
      .limit(10);

    const existing = new Set(exercises.map((e) => e.id));
    const newOnes = (data ?? []).filter((e) => !existing.has(e.id)) as SessionExercise[];
    exercises = [...exercises, ...newOnes].slice(0, 10);
  }

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-2xl flex flex-col gap-6">
        <header>
          <h1 className="text-xl font-semibold text-foreground">Session d&apos;entraînement</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            {dueIds.length > 0
              ? `${dueIds.length} exercice${dueIds.length > 1 ? "s" : ""} en révision due.`
              : "Sélection depuis la bibliothèque."}
          </p>
        </header>

        <SessionClient exercises={exercises} />
      </div>
    </main>
  );
}
