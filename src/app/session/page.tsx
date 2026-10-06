import { redirect } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/server";
import { fetchGraphData } from "@/lib/graph-actions";
import { fetchModelTemplate } from "@/lib/model-actions";
import { SessionClient } from "./session-client";
import type { SessionExercise } from "@/components/exercise-runner";

export const metadata = { title: "Session — Prep Platform" };

type ExerciseWithModule = SessionExercise & { module_id: string };

type ModuleRow = {
  id: string;
  slug: string;
  title: string;
  parent_id: string | null;
  tracks: { slug: string; title: string } | null;
};

// count = exercices du module lui-même + ceux de ses sous-chapitres
type ModuleChoice = ModuleRow & { count: number; childIds: string[] };

const SESSION_SIZE = 10;
const MAX_DUE = 7;

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

function shuffle<T>(items: T[]): T[] {
  const a = [...items];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
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

const EXERCISE_COLUMNS = "id, type, difficulty, payload, tags, module_id";

export default async function SessionPage({
  searchParams,
}: {
  searchParams: Promise<{ track?: string; module?: string }>;
}) {
  const { track: trackSlug, module: moduleSlug } = await searchParams;
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  // 0. Spécialités disponibles (modules contenant au moins un exercice)
  const { data: moduleData } = await supabase
    .from("modules")
    .select("id, slug, title, parent_id, tracks(slug, title)");
  const moduleRows = (moduleData ?? []) as unknown as ModuleRow[];

  const own = await Promise.all(
    moduleRows.map(async (m) => {
      const { count } = await supabase
        .from("exercises")
        .select("*", { count: "exact", head: true })
        .eq("module_id", m.id)
        .in("type", SUPPORTED_TYPES);
      return { ...m, own: count ?? 0 };
    })
  );
  const counted: ModuleChoice[] = own.map(({ own: ownCount, ...m }) => {
    const children = own.filter((c) => c.parent_id === m.id);
    return {
      ...m,
      count: ownCount + children.reduce((sum, c) => sum + c.own, 0),
      childIds: children.map((c) => c.id),
    };
  });
  const choices = counted
    .filter((m) => m.count > 0 && m.tracks)
    .sort(
      (a, b) =>
        a.tracks!.title.localeCompare(b.tracks!.title) || a.title.localeCompare(b.title)
    );

  const selected =
    trackSlug && moduleSlug
      ? choices.find((m) => m.slug === moduleSlug && m.tracks!.slug === trackSlug) ?? null
      : null;

  let exercises: SessionExercise[] = [];
  let dueCount = 0;
  let newCount = 0;

  if (selected) {
    // ── Tirage dans une spécialité : un sous-chapitre, ou un chapitre entier ──
    const moduleIds = [selected.id, ...selected.childIds];
    const { data: stateData } = await supabase
      .from("review_states")
      .select("exercise_id, due_at, exercises!inner(module_id)")
      .eq("user_id", user.id)
      .in("exercises.module_id", moduleIds);
    const states = (stateData ?? []) as unknown as { exercise_id: string; due_at: string }[];

    const nowIso = new Date().toISOString();
    const seen = new Set(states.map((s) => s.exercise_id));
    const dueIds = states
      .filter((s) => s.due_at <= nowIso)
      .map((s) => s.exercise_id)
      .slice(0, MAX_DUE);

    const { data: idData } = await supabase
      .from("exercises")
      .select("id")
      .in("module_id", moduleIds)
      .in("type", SUPPORTED_TYPES);
    const allIds = (idData ?? []).map((r) => r.id as string);

    // Priorité : révisions dues, puis questions jamais vues, puis déjà vues
    const unseen = shuffle(allIds.filter((id) => !seen.has(id)));
    const picked = [...dueIds, ...unseen].slice(0, SESSION_SIZE);
    if (picked.length < SESSION_SIZE) {
      const already = new Set(picked);
      const rest = shuffle(allIds.filter((id) => !already.has(id)));
      picked.push(...rest.slice(0, SESSION_SIZE - picked.length));
    }

    dueCount = dueIds.length;
    newCount = picked.filter((id) => !seen.has(id)).length;

    if (picked.length > 0) {
      const { data } = await supabase
        .from("exercises")
        .select(EXERCISE_COLUMNS)
        .in("id", picked);
      const byId = new Map((data ?? []).map((e) => [e.id as string, e]));
      exercises = picked
        .map((id) => byId.get(id))
        .filter((e): e is NonNullable<typeof e> => e !== undefined) as ExerciseWithModule[];
      // Chapitre entier : on alterne les sous-chapitres (interleaving, dispositif 4)
      if (moduleIds.length > 1) exercises = interleave(exercises as ExerciseWithModule[]);
    }
  } else {
    // ── Session mélangée (comportement d'origine) ─────────────────────────
    const { data: dueStates } = await supabase
      .from("review_states")
      .select("exercise_id")
      .eq("user_id", user.id)
      .lte("due_at", new Date().toISOString())
      .limit(MAX_DUE);

    const dueIds = (dueStates ?? []).map((s) => s.exercise_id as string);
    dueCount = dueIds.length;

    if (dueIds.length > 0) {
      const { data } = await supabase
        .from("exercises")
        .select(EXERCISE_COLUMNS)
        .in("id", dueIds)
        .in("type", SUPPORTED_TYPES);
      exercises = (data ?? []) as ExerciseWithModule[];
    }

    if (exercises.length < SESSION_SIZE) {
      // Complète avec des questions jamais vues, tirées dans plusieurs spécialités
      const leaves = shuffle(choices.filter((m) => m.childIds.length === 0)).slice(0, 5);
      const existing = new Set(exercises.map((e) => e.id));
      const need = SESSION_SIZE - exercises.length;
      const perModule = Math.max(1, Math.ceil(need / Math.max(1, leaves.length)));
      const pickedIds: string[] = [];

      for (const leaf of leaves) {
        const { data: st } = await supabase
          .from("review_states")
          .select("exercise_id, exercises!inner(module_id)")
          .eq("user_id", user.id)
          .eq("exercises.module_id", leaf.id);
        const seenIds = new Set(
          ((st ?? []) as unknown as { exercise_id: string }[]).map((r) => r.exercise_id)
        );
        const { data: idRows } = await supabase
          .from("exercises")
          .select("id")
          .eq("module_id", leaf.id)
          .in("type", SUPPORTED_TYPES);
        const all = (idRows ?? []).map((r) => r.id as string).filter((id) => !existing.has(id));
        const unseen = shuffle(all.filter((id) => !seenIds.has(id)));
        const pool = unseen.length > 0 ? unseen : shuffle(all);
        pickedIds.push(...pool.slice(0, perModule));
      }

      const fill = pickedIds.slice(0, need);
      if (fill.length > 0) {
        const { data } = await supabase.from("exercises").select(EXERCISE_COLUMNS).in("id", fill);
        exercises = [...exercises, ...((data ?? []) as ExerciseWithModule[])];
      }
    }

    exercises = interleave(exercises as ExerciseWithModule[]);
  }

  // Pre-fetch server-side data for graph_fill and excel_model
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

  // Sélecteur : filière → chapitre → sous-chapitres
  type Group = { key: string; heading: string; trackSlug: string; modules: ModuleChoice[] };
  const groups: Group[] = [];
  const loose = new Map<string, Group>();
  for (const m of choices) {
    if (m.parent_id) continue; // les sous-chapitres sont rangés sous leur chapitre
    const t = m.tracks!;
    const subs = choices.filter((c) => c.parent_id === m.id);
    if (subs.length > 0) {
      groups.push({
        key: m.id,
        heading: `${t.title} · ${m.title}`,
        trackSlug: t.slug,
        modules: [{ ...m, title: "Tout le chapitre" }, ...subs],
      });
    } else {
      if (!loose.has(t.slug)) {
        const g: Group = { key: t.slug, heading: t.title, trackSlug: t.slug, modules: [] };
        loose.set(t.slug, g);
        groups.push(g);
      }
      loose.get(t.slug)!.modules.push(m);
    }
  }
  groups.sort((a, b) => a.heading.localeCompare(b.heading));

  const parentTitle = selected?.parent_id
    ? moduleRows.find((m) => m.id === selected.parent_id)?.title ?? null
    : null;

  const chip =
    "inline-flex items-center rounded-full border px-3 py-1.5 text-sm min-h-[36px] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring";
  const chipOn = "bg-primary text-primary-foreground border-primary font-semibold";
  const chipOff = "bg-background text-foreground border-border hover:bg-muted";

  const subtitle = selected
    ? `${selected.tracks!.title} · ${parentTitle ? `${parentTitle} · ` : ""}${selected.title} : ${newCount} nouvelle${newCount > 1 ? "s" : ""}, ${dueCount} en révision, sur ${selected.count} questions.`
    : dueCount > 0
      ? `${dueCount} exercice${dueCount > 1 ? "s" : ""} en révision due.`
      : "Sélection depuis la bibliothèque.";

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-2xl flex flex-col gap-6">
        <header>
          <h1 className="text-xl font-semibold text-foreground">Session d&apos;entraînement</h1>
          <p className="text-sm text-muted-foreground mt-0.5">{subtitle}</p>
        </header>

        <nav aria-label="Choisir une spécialité" className="flex flex-col gap-3">
          <div>
            <Link href="/session" className={`${chip} ${selected ? chipOff : chipOn}`}>
              Toutes les spécialités
            </Link>
          </div>
          {groups.map((group) => (
            <div key={group.key} className="flex flex-col gap-1.5">
              <p className="text-xs font-medium text-muted-foreground">{group.heading}</p>
              <div className="flex flex-wrap gap-2">
                {group.modules.map((m) => (
                  <Link
                    key={m.id}
                    href={{ pathname: "/session", query: { track: group.trackSlug, module: m.slug } }}
                    aria-current={selected?.id === m.id ? "page" : undefined}
                    className={`${chip} ${selected?.id === m.id ? chipOn : chipOff}`}
                  >
                    {m.title}
                    <span className="ml-1.5 tabular-nums opacity-70">{m.count}</span>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </nav>

        <SessionClient key={selected?.id ?? "all"} exercises={enriched} />
      </div>
    </main>
  );
}
