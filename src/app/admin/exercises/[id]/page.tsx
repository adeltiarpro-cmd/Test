import { notFound } from "next/navigation";
import { getAdminUser } from "@/lib/admin/guard";
import { createAdminClient } from "@/lib/supabase/admin";
import { ExerciseForm } from "../exercise-form";
import type { ExerciseType } from "@/lib/admin/skeleton";
import { fetchModuleOptions } from "../modules";

export const metadata = { title: "Modifier un exercice — Admin" };

type Row = {
  id: string;
  type: ExerciseType;
  module_id: string;
  difficulty: number;
  payload: Record<string, unknown>;
  solution: Record<string, unknown>;
  tags: string[];
  external_key: string | null;
  exercise_concepts: { concepts: { slug: string } | null }[] | null;
};

export default async function EditExercisePage({ params }: { params: Promise<{ id: string }> }) {
  if (!(await getAdminUser())) notFound();
  const { id } = await params;

  // La solution n'est pas lisible avec le client utilisateur : lecture service_role, côté serveur
  const admin = createAdminClient();
  const { data } = await admin
    .from("exercises")
    .select(
      "id, type, module_id, difficulty, payload, solution, tags, external_key, exercise_concepts(concepts(slug))"
    )
    .eq("id", id)
    .maybeSingle();
  const row = data as unknown as Row | null;
  if (!row || !row.external_key?.startsWith("manual-")) notFound();

  const { prompt_mdx: prompt, ...payload } = row.payload;
  const ref = row.tags.find((t) => t.startsWith("ref:"));
  const modules = await fetchModuleOptions();

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-4xl flex flex-col gap-6">
        <header>
          <h1 className="text-xl font-semibold text-foreground">Modifier l&apos;exercice</h1>
          <p className="text-sm text-muted-foreground mt-0.5 font-mono">{row.external_key}</p>
        </header>
        <ExerciseForm
          modules={modules}
          initial={{
            id: row.id,
            type: row.type,
            moduleId: row.module_id,
            difficulty: row.difficulty,
            promptMdx: typeof prompt === "string" ? prompt : "",
            payload: JSON.stringify(payload, null, 2),
            solution: JSON.stringify(row.solution, null, 2),
            sourceRef: ref ? ref.slice(4) : "",
            conceptSlug: row.exercise_concepts?.[0]?.concepts?.slug ?? "",
          }}
        />
      </div>
    </main>
  );
}
