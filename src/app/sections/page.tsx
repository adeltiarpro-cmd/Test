import { redirect } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/server";

export const metadata = { title: "Sections — Prep Platform" };

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
  "numeric_steps",
] as const;

type ModuleRow = {
  id: string;
  slug: string;
  title: string;
  parent_id: string | null;
  level: number;
  track_id: string;
  tracks: { slug: string; title: string } | null;
};

type SectionStats = { total: number; seen: number; mastery: number | null };

type SectionEntry = {
  id: string;
  slug: string;
  title: string;
  trackSlug: string;
  stats: SectionStats;
};

type HrefObj = { pathname: "/session"; query: { track: string; module: string } };

type ChapterGroup = {
  id: string;
  title: string;
  isLeaf: boolean;
  stats: SectionStats;
  slug: string;
  trackSlug: string;
  subchapters: SectionEntry[];
};

type TrackGroup = {
  slug: string;
  title: string;
  chapters: ChapterGroup[];
};

export default async function SectionsPage({
  searchParams,
}: {
  searchParams: Promise<{ track?: string }>;
}) {
  const { track: trackFilter } = await searchParams;
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  // 1. All modules
  const { data: moduleData } = await supabase
    .from("modules")
    .select("id, slug, title, parent_id, level, track_id, tracks(slug, title)");
  const modules = (moduleData ?? []) as unknown as ModuleRow[];

  // 2. Exercise ids + module mapping (one query)
  const { data: exData } = await supabase
    .from("exercises")
    .select("id, module_id")
    .in("type", SUPPORTED_TYPES);

  const exByModule = new Map<string, Set<string>>();
  for (const ex of exData ?? []) {
    const mid = ex.module_id as string;
    if (!mid) continue;
    if (!exByModule.has(mid)) exByModule.set(mid, new Set());
    exByModule.get(mid)!.add(ex.id as string);
  }

  // 3. Seen exercises for this user
  const { data: seenData } = await supabase
    .from("review_states")
    .select("exercise_id")
    .eq("user_id", user.id);
  const seenSet = new Set((seenData ?? []).map((s) => s.exercise_id as string));

  // 4. Concept mastery for this user, grouped by module
  const { data: masteryData } = await supabase
    .from("concept_mastery")
    .select("mastery_score, concepts(module_id)")
    .eq("user_id", user.id);

  const masteryAgg = new Map<string, { sum: number; count: number }>();
  for (const entry of (masteryData ?? []) as unknown as {
    mastery_score: number;
    concepts: { module_id: string } | null;
  }[]) {
    const mid = entry.concepts?.module_id;
    if (!mid) continue;
    const cur = masteryAgg.get(mid) ?? { sum: 0, count: 0 };
    cur.sum += entry.mastery_score;
    cur.count++;
    masteryAgg.set(mid, cur);
  }

  function statsOf(moduleId: string): SectionStats {
    const children = modules.filter((m) => m.parent_id === moduleId);
    const ownIds = [...(exByModule.get(moduleId) ?? [])];
    const childIds = children.flatMap((c) => [...(exByModule.get(c.id) ?? [])]);
    const allIds = [...ownIds, ...childIds];
    const seen = allIds.filter((id) => seenSet.has(id)).length;

    // mastery: average of own module + children
    const mids = children.length > 0 ? [moduleId, ...children.map((c) => c.id)] : [moduleId];
    let mSum = 0, mCount = 0;
    for (const mid of mids) {
      const a = masteryAgg.get(mid);
      if (a) { mSum += a.sum; mCount += a.count; }
    }

    return {
      total: allIds.length,
      seen,
      mastery: mCount > 0 ? mSum / mCount : null,
    };
  }

  // Build track → chapter → subchapters structure
  const trackMap = new Map<string, TrackGroup>();
  for (const m of modules.filter((m) => m.level === 0 && m.tracks)) {
    const t = m.tracks!;
    if (!trackMap.has(t.slug)) {
      trackMap.set(t.slug, { slug: t.slug, title: t.title, chapters: [] });
    }
    const subs = modules.filter((c) => c.parent_id === m.id);
    const chStats = statsOf(m.id);

    if (subs.length > 0) {
      const subEntries: SectionEntry[] = subs
        .map((s) => ({ id: s.id, slug: s.slug, title: s.title, trackSlug: t.slug, stats: statsOf(s.id) }))
        .filter((s) => s.stats.total > 0);
      if (subEntries.length > 0 || chStats.total > 0) {
        trackMap.get(t.slug)!.chapters.push({
          id: m.id, slug: m.slug, title: m.title, trackSlug: t.slug,
          isLeaf: false, stats: chStats, subchapters: subEntries,
        });
      }
    } else if (chStats.total > 0) {
      trackMap.get(t.slug)!.chapters.push({
        id: m.id, slug: m.slug, title: m.title, trackSlug: t.slug,
        isLeaf: true, stats: chStats, subchapters: [],
      });
    }
  }

  const tracks = [...trackMap.values()]
    .filter((t) => t.chapters.length > 0)
    .sort((a, b) => a.title.localeCompare(b.title));

  const displayedTracks = trackFilter
    ? tracks.filter((t) => t.slug === trackFilter)
    : tracks;

  const chip =
    "inline-flex items-center rounded-full border px-3 py-1.5 text-sm min-h-[36px] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring";
  const chipOn = "bg-primary text-primary-foreground border-primary font-semibold";
  const chipOff = "bg-background text-foreground border-border hover:bg-muted";

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-3xl flex flex-col gap-6">
        <header>
          <h1 className="text-xl font-semibold text-foreground">Sections</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Contenu disponible par filière et sous-chapitre.
          </p>
        </header>

        {/* Filter chips */}
        <nav aria-label="Filtrer par filière" className="flex flex-wrap gap-2">
          <Link href="/sections" className={`${chip} ${!trackFilter ? chipOn : chipOff}`}>
            Toutes
          </Link>
          {tracks.map((t) => (
            <Link
              key={t.slug}
              href={{ pathname: "/sections", query: { track: t.slug } }}
              className={`${chip} ${trackFilter === t.slug ? chipOn : chipOff}`}
            >
              {t.title}
            </Link>
          ))}
        </nav>

        {/* Sections */}
        {displayedTracks.length === 0 ? (
          <p className="text-sm text-muted-foreground py-8 text-center">
            Aucun contenu disponible. Importez des exercices via le pipeline d&apos;ingestion.
          </p>
        ) : (
          <div className="flex flex-col gap-8">
            {displayedTracks.map((track) => (
              <section key={track.slug}>
                <h2 className="text-base font-semibold text-foreground mb-3">{track.title}</h2>
                <div className="flex flex-col gap-4">
                  {track.chapters.map((chapter) => (
                    <div key={chapter.id}>
                      {!chapter.isLeaf && (
                        <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2 px-1">
                          {chapter.title}
                        </h3>
                      )}
                      <div className="flex flex-col gap-1.5">
                        {chapter.isLeaf ? (
                          <SectionRow
                            title={chapter.title}
                            stats={chapter.stats}
                            href={{ pathname: "/session", query: { track: track.slug, module: chapter.slug } }}
                          />
                        ) : (
                          chapter.subchapters.map((sub) => (
                            <SectionRow
                              key={sub.id}
                              title={sub.title}
                              stats={sub.stats}
                              href={{ pathname: "/session", query: { track: track.slug, module: sub.slug } }}
                            />
                          ))
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

function SectionRow({
  title,
  stats,
  href,
}: {
  title: string;
  stats: SectionStats;
  href: HrefObj;
}) {
  const seenPct = stats.total > 0 ? Math.round((stats.seen / stats.total) * 100) : 0;
  const masteryPct =
    stats.mastery !== null ? Math.round(stats.mastery * 100) : null;

  return (
    <div className="flex items-center gap-3 rounded-lg border border-border bg-card px-4 py-3">
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-foreground">{title}</p>
        <div className="flex items-center gap-3 mt-1 flex-wrap">
          <span className="text-xs tabular-nums text-muted-foreground">
            {stats.total} question{stats.total > 1 ? "s" : ""}
          </span>
          {stats.seen > 0 && (
            <span className="text-xs tabular-nums text-muted-foreground">
              {seenPct}% vu
            </span>
          )}
          {masteryPct !== null && (
            <span
              className={`text-xs tabular-nums font-medium ${
                masteryPct >= 80
                  ? "text-green-700"
                  : masteryPct >= 50
                  ? "text-amber-700"
                  : "text-destructive"
              }`}
            >
              {masteryPct}% maîtrise
            </span>
          )}
        </div>
      </div>

      {/* Seen progress bar */}
      {stats.total > 0 && (
        <div
          className="w-16 h-1.5 rounded-full bg-muted overflow-hidden shrink-0"
          title={`${seenPct}% vu`}
        >
          <div
            className="h-full bg-primary transition-all"
            style={{ width: `${seenPct}%` }}
          />
        </div>
      )}

      <Link
        href={href}
        className="shrink-0 text-xs font-semibold text-primary hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded px-2 py-1 whitespace-nowrap"
      >
        Lancer →
      </Link>
    </div>
  );
}
