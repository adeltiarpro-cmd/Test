import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { fetchGraphData } from "@/lib/graph-actions";
import { fetchModelTemplate } from "@/lib/model-actions";
import { SessionClient } from "./session-client";
import type { SessionExercise } from "@/components/exercise-runner";

export const metadata = { title: "Session — Prep Platform" };

type ExerciseWithModule = SessionExercise & { module_id: string };

function interleave(exercises: ExerciseWithModule[]): ExerciseWithModule[] {
  const groups = new Map<string, ExerciseWithModule[]>();
  for (const ex of exercises) {
    const key = ex.module_id ?? "unknown";
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key)!.push(ex);
  }
  const result: ExerciseWithModule[] = [];
  const buckets = [...groups.values()];
  while (result.length < exercises.length) {
    let added = false;
    for (const bucket of buckets) {
      const ex = bucket.shift();
      if (ex) { result.push(ex); added = true; }
    }
    if (!added) break;
  }
  return result;
}

const SUPPORTED_TYPES = [
  "mcq",
  "numeric",
  "formula_cloze",
  "short_answer",
  "graph_fill",
  "excel_model",
  "statement_interactive",
  "case_math",
  "case_structuring",
  "market_sizing",
] as const;

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
    .limit(7);

  const dueIds = (dueStates ?? []).map((s) => s.exercise_id as string);

  let exercises: SessionExercise[] = [];

  if (dueIds.length > 0) {
    const { data } = await supabase
      .from("exercises")
      .select("id, type, difficulty, payload, tags, module_id")
      .in("id", dueIds)
      .in("type", SUPPORTED_TYPES);
    exercises = (data ?? []) as ExerciseWithModule[];
  }

  // 2. Always fill remaining slots with newest exercises (includes unseen types)
  if (exercises.length < 10) {
    const { data } = await supabase
      .from("exercises")
      .select("id, type, difficulty, payload, tags, module_id")
      .in("type", SUPPORTED_TYPES)
      .order("created_at", { ascending: false })
      .limit(10);

    const existing = new Set(exercises.map((e) => e.id));
    const newOnes = (data ?? []).filter((e) => !existing.has(e.id)) as ExerciseWithModule[];
    exercises = [...exercises, ...newOnes].slice(0, 10);
  }

  exercises = interleave(exercises as ExerciseWithModule[]);

  // 3. Pre-fetch server-side data for graph_fill and excel_model
  const enriched = await Promise.all(
    exercises.map(async (ex) => {
      const pay = ex.payload as Record<string, unknown>;
      if (ex.type === "graph_fill") {
        const graphId = pay.graph_id as string | undefined;
        if (!graphId) return ex;
        const graphData = await fetchGraphData(graphId);
        return { ...ex, payload: { ...pay, _graphData: graphData } } as SessionExercise;
      }
      if (ex.type === "excel_model") {
        const templateId = pay.template_id as string | undefined;
        if (!templateId) return ex;
        const templateData = await fetchModelTemplate(templateId);
        return { ...ex, payload: { ...pay, _templateData: templateData } } as SessionExercise;
      }
      return ex;
    })
  );

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

        <SessionClient exercises={enriched} />
      </div>
    </main>
  );
}
