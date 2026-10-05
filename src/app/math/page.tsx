import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { Callout } from "@/components/ui/callout";

export const metadata = { title: "Maths — Prep Platform" };

export default async function MathPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  // Math track
  const { data: mathTrack } = await supabase
    .from("tracks")
    .select("id, title")
    .eq("slug", "math")
    .single();

  if (!mathTrack) {
    return (
      <main className="min-h-screen bg-background px-4 py-8">
        <p className="text-sm text-muted-foreground">Track &quot;math&quot; introuvable.</p>
      </main>
    );
  }

  // Math modules ordered
  const { data: mathModules } = await supabase
    .from("modules")
    .select("id, title")
    .eq("track_id", mathTrack.id)
    .order("order", { ascending: true });

  const mathModuleIds = (mathModules ?? []).map((m) => m.id);

  // Concepts in those modules
  const { data: concepts } =
    mathModuleIds.length > 0
      ? await supabase
          .from("concepts")
          .select("id, title, module_id")
          .in("module_id", mathModuleIds)
          .order("title", { ascending: true })
      : { data: [] as { id: string; title: string; module_id: string }[] };

  const conceptIds = (concepts ?? []).map((c) => c.id);

  type EdgeRow = { source_id: string; target_id: string; kind: string };
  type MasteryRow = { concept_id: string; mastery_score: number };

  const emptyEdges: { data: EdgeRow[] } = { data: [] };
  const emptyMastery: { data: MasteryRow[] } = { data: [] };

  const [edgesResult, masteryResult, leechResult] = await Promise.all([
    conceptIds.length > 0
      ? supabase
          .from("concept_edges")
          .select("source_id, target_id, kind")
          .in("source_id", conceptIds)
          .in("target_id", conceptIds)
      : Promise.resolve(emptyEdges),

    conceptIds.length > 0
      ? supabase
          .from("concept_mastery")
          .select("concept_id, mastery_score")
          .eq("user_id", user.id)
          .in("concept_id", conceptIds)
      : Promise.resolve(emptyMastery),

    supabase
      .from("review_states")
      .select("exercise_id, lapses")
      .eq("user_id", user.id)
      .gt("lapses", 3),
  ]);

  // Leech concept IDs
  const leechExerciseIds = (leechResult.data ?? []).map((s) => s.exercise_id as string);
  const leechConceptSet = new Set<string>();
  if (leechExerciseIds.length > 0) {
    const { data: links } = await supabase
      .from("exercise_concepts")
      .select("concept_id")
      .in("exercise_id", leechExerciseIds);
    (links ?? []).forEach((l) => leechConceptSet.add(l.concept_id as string));
  }

  const masteryMap = new Map(
    (masteryResult.data ?? []).map((m) => [m.concept_id as string, Number(m.mastery_score)])
  );

  const conceptTitleMap = new Map((concepts ?? []).map((c) => [c.id, c.title]));

  // prerequisite source_ids per target concept
  const prereqMap = new Map<string, string[]>();
  for (const edge of edgesResult.data ?? []) {
    if (edge.kind === "prerequisite") {
      if (!prereqMap.has(edge.target_id)) prereqMap.set(edge.target_id, []);
      prereqMap.get(edge.target_id)!.push(edge.source_id);
    }
  }

  // Group concepts by module
  const byModule = new Map<string, typeof concepts>();
  for (const concept of concepts ?? []) {
    if (!byModule.has(concept.module_id)) byModule.set(concept.module_id, []);
    byModule.get(concept.module_id)!.push(concept);
  }

  const leechCount = (concepts ?? []).filter((c) => leechConceptSet.has(c.id)).length;

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-3xl flex flex-col gap-6">
        <header>
          <h1 className="text-xl font-semibold text-foreground">Vue Mathématiques</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Graphe de prérequis — concepts bloquants mis en évidence
          </p>
        </header>

        {leechCount > 0 && (
          <Callout variant="warning" title={`${leechCount} concept${leechCount > 1 ? "s" : ""} bloquant${leechCount > 1 ? "s" : ""}`}>
            <p>Ces concepts ont accumulé 4+ erreurs. Travaillez leurs prérequis en priorité.</p>
          </Callout>
        )}

        {(mathModules ?? []).map((mod) => {
          const modConcepts = byModule.get(mod.id) ?? [];
          return (
            <section key={mod.id} className="flex flex-col gap-3">
              <h2 className="text-base font-semibold text-foreground border-b border-border pb-1.5">
                {mod.title}
              </h2>
              {modConcepts.length === 0 ? (
                <p className="text-sm text-muted-foreground italic">
                  Aucun concept ingéré pour ce module — lancez une session INGEST-RUNBOOK.
                </p>
              ) : (
                <div className="flex flex-col gap-2">
                  {modConcepts.map((concept) => {
                    const mastery = masteryMap.get(concept.id) ?? null;
                    const isLeech = leechConceptSet.has(concept.id);
                    const prereqs = (prereqMap.get(concept.id) ?? [])
                      .map((id) => conceptTitleMap.get(id))
                      .filter(Boolean) as string[];

                    const borderColor =
                      isLeech
                        ? "border-destructive"
                        : mastery === null
                        ? "border-border"
                        : mastery >= 0.8
                        ? "border-green-500"
                        : mastery >= 0.5
                        ? "border-amber-400"
                        : "border-destructive/60";

                    const bgColor =
                      isLeech
                        ? "bg-destructive/5"
                        : mastery === null
                        ? "bg-card"
                        : mastery >= 0.8
                        ? "bg-green-50"
                        : mastery >= 0.5
                        ? "bg-amber-50"
                        : "bg-destructive/5";

                    const barColor =
                      mastery !== null && mastery >= 0.8
                        ? "bg-green-500"
                        : mastery !== null && mastery >= 0.5
                        ? "bg-amber-400"
                        : "bg-destructive/60";

                    return (
                      <div
                        key={concept.id}
                        className={`rounded-lg border p-3 flex flex-col gap-1.5 ${borderColor} ${bgColor} ${
                          isLeech ? "ring-1 ring-destructive" : ""
                        }`}
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-sm font-medium text-foreground">
                            {concept.title}
                          </span>
                          <div className="flex items-center gap-2 shrink-0">
                            {isLeech && (
                              <span className="text-[10px] font-bold bg-destructive text-white rounded px-1.5 py-0.5 uppercase tracking-wide">
                                Leech
                              </span>
                            )}
                            <span className="text-xs tabular-nums text-muted-foreground">
                              {mastery !== null ? `${Math.round(mastery * 100)} %` : "non révisé"}
                            </span>
                          </div>
                        </div>

                        {mastery !== null && (
                          <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                            <div
                              className={`h-full rounded-full transition-all ${barColor}`}
                              style={{ width: `${Math.min(100, mastery * 100)}%` }}
                            />
                          </div>
                        )}

                        {prereqs.length > 0 && (
                          <p className="text-xs text-muted-foreground">
                            Prérequis : {prereqs.join(", ")}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </section>
          );
        })}
      </div>
    </main>
  );
}
