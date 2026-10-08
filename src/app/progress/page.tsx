import { redirect } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/server";
import { GoalForm } from "@/components/progress/goal-form";

export const metadata = { title: "Progression — Prep Platform" };

const SUPPORTED_TYPES = [
  "mcq", "numeric", "formula_cloze", "short_answer", "graph_fill",
  "excel_model", "statement_interactive", "case_math", "case_structuring",
  "market_sizing", "numeric_steps",
] as const;

// ── Types ────────────────────────────────────────────────────

type ModuleTargetData = { target_mastery: number; min_exercises: number };

type ModuleRow = {
  id: string;
  slug: string;
  title: string;
  parent_id: string | null;
  level: number;
  track_id: string;
  tracks: { slug: string; title: string } | null;
  module_targets: ModuleTargetData | ModuleTargetData[] | null;
};

type SubchapterStats = {
  id: string;
  slug: string;
  title: string;
  trackSlug: string;
  total: number;
  seen: number;
  dueCount: number;
  unseenCount: number;
  failedRecentCount: number;
  masteryPct: number | null;
  targetPct: number;
};

type ChapterGroup = {
  id: string;
  title: string;
  isLeaf: boolean;
  slug: string;
  trackSlug: string;
  subs: SubchapterStats[];
  leafStats?: SubchapterStats;
};

type TrackGroup = { slug: string; title: string; chapters: ChapterGroup[] };

// ── Helpers ──────────────────────────────────────────────────

function targetOf(t: ModuleTargetData | ModuleTargetData[] | null): ModuleTargetData {
  if (!t) return { target_mastery: 0.8, min_exercises: 15 };
  return Array.isArray(t) ? (t[0] ?? { target_mastery: 0.8, min_exercises: 15 }) : t;
}

type NextAction =
  | { kind: "mastered" }
  | { kind: "revise"; count: number }
  | { kind: "start"; count: number }
  | { kind: "redo"; count: number }
  | { kind: "uptodate" }
  | { kind: "empty" };

function nextActionOf(s: SubchapterStats): NextAction {
  if (s.total === 0) return { kind: "empty" };
  if (s.masteryPct !== null && s.masteryPct >= s.targetPct) return { kind: "mastered" };
  if (s.dueCount > 0) return { kind: "revise", count: s.dueCount };
  if (s.unseenCount > 0) return { kind: "start", count: s.unseenCount };
  if (s.failedRecentCount > 0) return { kind: "redo", count: s.failedRecentCount };
  return { kind: "uptodate" };
}

// ── Page ─────────────────────────────────────────────────────

export default async function ProgressPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const now = new Date();
  const sevenDaysAgo = new Date(now.getTime() - 7 * 86_400_000).toISOString();

  // Parallel data fetching
  const [
    modulesRes,
    exRes,
    statesRes,
    masteryRes,
    attemptsRes,
    profileRes,
  ] = await Promise.all([
    supabase
      .from("modules")
      .select("id, slug, title, parent_id, level, track_id, tracks(slug, title), module_targets(target_mastery, min_exercises)"),
    supabase
      .from("exercises")
      .select("id, module_id")
      .in("type", SUPPORTED_TYPES),
    supabase
      .from("review_states")
      .select("exercise_id, due_at, created_at")
      .eq("user_id", user.id),
    supabase
      .from("concept_mastery")
      .select("mastery_score, concepts(id, title, module_id)")
      .eq("user_id", user.id),
    supabase
      .from("attempts")
      .select("exercise_id, is_correct, created_at")
      .eq("user_id", user.id)
      .gte("created_at", sevenDaysAgo),
    supabase
      .from("profiles")
      .select("target_date, daily_goal")
      .eq("id", user.id)
      .maybeSingle(),
  ]);

  const modules = (modulesRes.data ?? []) as unknown as ModuleRow[];
  const exData = exRes.data ?? [];
  const statesData = statesRes.data ?? [];
  const masteryData = (masteryRes.data ?? []) as unknown as {
    mastery_score: number;
    concepts: { id: string; title: string; module_id: string } | null;
  }[];
  const attemptsData = attemptsRes.data ?? [];
  const profile = profileRes.data as { target_date: string | null; daily_goal: number | null } | null;

  // ── Build index structures ────────────────────────────────

  // exercises by module_id
  const exByModule = new Map<string, Set<string>>();
  for (const ex of exData) {
    const mid = ex.module_id as string;
    if (!mid) continue;
    if (!exByModule.has(mid)) exByModule.set(mid, new Set());
    exByModule.get(mid)!.add(ex.id as string);
  }

  // exercise_id → module_id (for cross-referencing review_states)
  const exIdToModuleId = new Map<string, string>();
  for (const ex of exData) {
    if (ex.module_id) exIdToModuleId.set(ex.id as string, ex.module_id as string);
  }

  // seen set and due set
  const nowIso = now.toISOString();
  const seenSet = new Set(statesData.map((s) => s.exercise_id as string));
  const dueSet = new Set(
    statesData
      .filter((s) => (s.due_at as string) <= nowIso)
      .map((s) => s.exercise_id as string)
  );

  // failed exercises this week
  const failedRecentSet = new Set(
    attemptsData
      .filter((a) => !a.is_correct)
      .map((a) => a.exercise_id as string)
  );

  // mastery aggregated by module_id
  const masteryAgg = new Map<string, { sum: number; count: number }>();
  for (const entry of masteryData) {
    const mid = entry.concepts?.module_id;
    if (!mid) continue;
    const cur = masteryAgg.get(mid) ?? { sum: 0, count: 0 };
    cur.sum += entry.mastery_score;
    cur.count++;
    masteryAgg.set(mid, cur);
  }

  // ── Compute stats for a leaf module (own + children rolled up) ──

  function statsFor(moduleId: string, trackSlug: string): SubchapterStats {
    const m = modules.find((x) => x.id === moduleId)!;
    const children = modules.filter((c) => c.parent_id === moduleId);
    const ownIds = [...(exByModule.get(moduleId) ?? [])];
    const childIds = children.flatMap((c) => [...(exByModule.get(c.id) ?? [])]);
    const allIds = [...ownIds, ...childIds];

    const total = allIds.length;
    const seen = allIds.filter((id) => seenSet.has(id)).length;
    const dueCount = allIds.filter((id) => dueSet.has(id)).length;
    const unseenCount = allIds.filter((id) => !seenSet.has(id)).length;
    const failedRecentCount = allIds.filter((id) => failedRecentSet.has(id)).length;

    // mastery: combine own + children's concepts
    const mids = children.length > 0 ? [moduleId, ...children.map((c) => c.id)] : [moduleId];
    let mSum = 0, mCount = 0;
    for (const mid of mids) {
      const a = masteryAgg.get(mid);
      if (a) { mSum += a.sum; mCount += a.count; }
    }
    const masteryPct = mCount > 0 ? Math.round((mSum / mCount) * 100) : null;

    const tgt = targetOf(m.module_targets);

    return {
      id: moduleId,
      slug: m.slug,
      title: m.title,
      trackSlug,
      total,
      seen,
      dueCount,
      unseenCount,
      failedRecentCount,
      masteryPct,
      targetPct: Math.round(tgt.target_mastery * 100),
    };
  }

  // ── Build track hierarchy ─────────────────────────────────

  const trackMap = new Map<string, TrackGroup>();
  for (const m of modules.filter((m) => m.level === 0 && m.tracks)) {
    const t = m.tracks!;
    if (!trackMap.has(t.slug)) {
      trackMap.set(t.slug, { slug: t.slug, title: t.title, chapters: [] });
    }
    const subs = modules.filter((c) => c.parent_id === m.id);

    if (subs.length > 0) {
      const subStats = subs
        .map((s) => statsFor(s.id, t.slug))
        .filter((s) => s.total > 0);
      if (subStats.length > 0) {
        trackMap.get(t.slug)!.chapters.push({
          id: m.id, slug: m.slug, title: m.title, trackSlug: t.slug,
          isLeaf: false, subs: subStats,
        });
      }
    } else {
      const ls = statsFor(m.id, t.slug);
      if (ls.total > 0) {
        trackMap.get(t.slug)!.chapters.push({
          id: m.id, slug: m.slug, title: m.title, trackSlug: t.slug,
          isLeaf: true, subs: [], leafStats: ls,
        });
      }
    }
  }

  const tracks = [...trackMap.values()]
    .filter((t) => t.chapters.length > 0)
    .sort((a, b) => a.title.localeCompare(b.title));

  // ── Goal stats ────────────────────────────────────────────

  const targetDateStr = profile?.target_date ?? null;
  const dailyGoalSaved = profile?.daily_goal ?? null;

  let daysLeft: number | null = null;
  let suggested: number | null = null;
  if (targetDateStr) {
    const target = new Date(targetDateStr);
    target.setHours(23, 59, 59);
    daysLeft = Math.max(1, Math.ceil((target.getTime() - now.getTime()) / 86_400_000));
    const totalEx = [...exByModule.values()].reduce((s, set) => s + set.size, 0);
    const remaining = totalEx - seenSet.size;
    suggested = Math.max(1, Math.ceil(Math.max(0, remaining) / daysLeft));
  }

  // ── Weekly stats ─────────────────────────────────────────

  const totalAttempts = attemptsData.length;
  const correctAttempts = attemptsData.filter((a) => a.is_correct).length;
  const correctPct = totalAttempts > 0 ? Math.round((correctAttempts / totalAttempts) * 100) : null;

  // Sections advanced this week (new review_states)
  const newStateModuleIds = new Set(
    statesData
      .filter((s) => (s.created_at as string) >= sevenDaysAgo)
      .map((s) => exIdToModuleId.get(s.exercise_id as string))
      .filter((mid): mid is string => !!mid)
  );
  const advancedModules = modules
    .filter((m) => newStateModuleIds.has(m.id))
    .map((m) => m.title)
    .slice(0, 5);

  // Weak concepts (mastery < 50%)
  const weakConcepts = masteryData
    .filter((e) => e.mastery_score < 0.5 && e.concepts?.title)
    .sort((a, b) => a.mastery_score - b.mastery_score)
    .slice(0, 5)
    .map((e) => ({ title: e.concepts!.title, pct: Math.round(e.mastery_score * 100) }));

  // ── Render ────────────────────────────────────────────────

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-3xl flex flex-col gap-8">

        {/* Header */}
        <header>
          <h1 className="text-xl font-semibold text-foreground">Par où continuer</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Parcours ordonné par filière, état et prochaine action recommandée.
          </p>
        </header>

        {/* Objectives */}
        <section className="rounded-lg border border-border bg-card p-4 flex flex-col gap-3">
          <h2 className="text-sm font-semibold text-foreground">Objectifs</h2>
          <GoalForm targetDate={targetDateStr} dailyGoal={dailyGoalSaved} />
          {targetDateStr && daysLeft !== null && (
            <p className="text-xs text-muted-foreground">
              <span className="font-medium text-foreground tabular-nums">{daysLeft}</span> jour{daysLeft > 1 ? "s" : ""} avant l&apos;entretien
              {suggested !== null && (
                <>
                  {" "}·{" "}
                  <span className="font-medium text-foreground tabular-nums">{suggested}</span> questions/jour conseillées
                  {dailyGoalSaved && suggested !== dailyGoalSaved && (
                    <span className="ml-1 opacity-70">(objectif fixé : {dailyGoalSaved})</span>
                  )}
                </>
              )}
            </p>
          )}
        </section>

        {/* Track hierarchy */}
        {tracks.length === 0 ? (
          <p className="text-sm text-muted-foreground text-center py-8">
            Aucun exercice disponible. Importez du contenu via le pipeline d&apos;ingestion.
          </p>
        ) : (
          tracks.map((track) => (
            <section key={track.slug} className="flex flex-col gap-4">
              <h2 className="text-base font-semibold text-foreground">{track.title}</h2>
              {track.chapters.map((chapter) => (
                <div key={chapter.id} className="flex flex-col gap-1.5">
                  {!chapter.isLeaf && (
                    <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground px-1">
                      {chapter.title}
                    </h3>
                  )}
                  {chapter.isLeaf && chapter.leafStats
                    ? <ProgressRow sub={chapter.leafStats} />
                    : chapter.subs.map((sub) => <ProgressRow key={sub.id} sub={sub} />)
                  }
                </div>
              ))}
            </section>
          ))
        )}

        {/* Weekly view */}
        {totalAttempts > 0 && (
          <section className="rounded-lg border border-border bg-card p-4 flex flex-col gap-3">
            <h2 className="text-sm font-semibold text-foreground">Cette semaine</h2>
            <p className="text-sm text-foreground">
              <span className="font-medium tabular-nums">{totalAttempts}</span> question{totalAttempts > 1 ? "s" : ""}
              {correctPct !== null && (
                <> · <span className="font-medium tabular-nums">{correctPct}%</span> correctes</>
              )}
            </p>
            {advancedModules.length > 0 && (
              <div>
                <p className="text-xs text-muted-foreground mb-1">Sections avancées</p>
                <p className="text-sm text-foreground">{advancedModules.join(", ")}</p>
              </div>
            )}
            {weakConcepts.length > 0 && (
              <div>
                <p className="text-xs text-muted-foreground mb-1">Points faibles</p>
                <div className="flex flex-wrap gap-1.5">
                  {weakConcepts.map((c) => (
                    <span
                      key={c.title}
                      className="inline-flex items-center gap-1 rounded-full border border-destructive/30 px-2 py-0.5 text-xs text-destructive"
                    >
                      {c.title}
                      <span className="tabular-nums opacity-70">{c.pct}%</span>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

      </div>
    </main>
  );
}

// ── ProgressRow ───────────────────────────────────────────────

function ProgressRow({ sub }: { sub: SubchapterStats }) {
  const action = nextActionOf(sub);
  const seenPct = sub.total > 0 ? Math.round((sub.seen / sub.total) * 100) : 0;

  const actionConfig: Record<NextAction["kind"], { label: string; cls: string }> = {
    mastered:  { label: "Maîtrisé ✓",        cls: "text-green-700 border-green-500/40 bg-green-50" },
    revise:    { label: `Réviser · ${(action as { kind: "revise"; count: number }).count} dus`, cls: "text-amber-700 border-amber-400/50 bg-amber-50" },
    start:     { label: `Attaquer · ${(action as { kind: "start"; count: number }).count} à voir`, cls: "text-primary border-primary/30 bg-primary/5" },
    redo:      { label: `Refaire · ${(action as { kind: "redo"; count: number }).count} ratés`, cls: "text-destructive border-destructive/30 bg-destructive/5" },
    uptodate:  { label: "À jour",             cls: "text-muted-foreground border-border" },
    empty:     { label: "Vide",               cls: "text-muted-foreground border-border" },
  };

  const cfg = actionConfig[action.kind];
  const sessionHref = {
    pathname: "/session" as const,
    query: { track: sub.trackSlug, module: sub.slug },
  };

  return (
    <div className="flex items-center gap-3 rounded-lg border border-border bg-card px-4 py-3">
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-foreground truncate">{sub.title}</p>
        <div className="flex items-center gap-2 mt-1 flex-wrap">
          <span className="text-xs tabular-nums text-muted-foreground">
            {sub.total} question{sub.total > 1 ? "s" : ""}
          </span>
          {sub.seen > 0 && (
            <span className="text-xs tabular-nums text-muted-foreground">{seenPct}% vu</span>
          )}
          {sub.masteryPct !== null && (
            <span
              className={`text-xs tabular-nums font-medium ${
                sub.masteryPct >= sub.targetPct ? "text-green-700" :
                sub.masteryPct >= 50 ? "text-amber-700" : "text-destructive"
              }`}
            >
              {sub.masteryPct}% maîtrise
            </span>
          )}
        </div>
      </div>

      {/* Seen progress bar */}
      {sub.total > 0 && (
        <div className="w-14 h-1.5 rounded-full bg-muted overflow-hidden shrink-0">
          <div className="h-full bg-primary transition-all" style={{ width: `${seenPct}%` }} />
        </div>
      )}

      {/* Next action */}
      {action.kind !== "empty" && (
        <Link
          href={sessionHref}
          className={`shrink-0 text-xs font-semibold rounded-full border px-2.5 py-1 whitespace-nowrap transition-opacity hover:opacity-80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${cfg.cls}`}
        >
          {cfg.label}
        </Link>
      )}
    </div>
  );
}
