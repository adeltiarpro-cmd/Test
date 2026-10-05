import { redirect } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/server";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Callout } from "@/components/ui/callout";

export const metadata = { title: "Dashboard — Prep Platform" };

type WeakConcept = {
  mastery_score: number;
  concepts: { id: string; title: string; modules: { title: string } | null } | null;
};

type MasteryEntry = {
  mastery_score: number;
  concepts: {
    module_id: string;
    modules: {
      id: string;
      title: string;
      level: number;
      module_targets: Array<{ target_mastery: number; min_exercises: number }> | null;
      tracks: { id: string; slug: string; title: string } | null;
    } | null;
  } | null;
};

export default async function DashboardPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const now = new Date();
  const isMonday = now.getDay() === 1;
  const sevenDaysAgo = new Date(now.getTime() - 7 * 86_400_000).toISOString();
  const DAY_LABELS = ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"];

  const [dueResult, weakResult, activityResult, masteriesResult] = await Promise.all([
    supabase
      .from("review_states")
      .select("*", { count: "exact", head: true })
      .eq("user_id", user.id)
      .lte("due_at", now.toISOString()),

    supabase
      .from("concept_mastery")
      .select("mastery_score, concepts(id, title, modules(title))")
      .eq("user_id", user.id)
      .order("mastery_score", { ascending: true })
      .limit(3),

    supabase
      .from("attempts")
      .select("created_at, is_correct")
      .eq("user_id", user.id)
      .gte("created_at", sevenDaysAgo),

    supabase
      .from("concept_mastery")
      .select(`
        mastery_score,
        concepts (
          module_id,
          modules (
            id, title, level,
            module_targets ( target_mastery, min_exercises ),
            tracks ( id, slug, title )
          )
        )
      `)
      .eq("user_id", user.id),
  ]);

  const dueCount = dueResult.count ?? 0;
  const weakConcepts = (weakResult.data ?? []) as unknown as WeakConcept[];

  // Activity: group by day (last 7, oldest first)
  const activity: { date: string; label: string; count: number }[] = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(now.getTime() - i * 86_400_000);
    activity.push({
      date: d.toISOString().slice(0, 10),
      label: DAY_LABELS[d.getDay()],
      count: 0,
    });
  }
  for (const row of activityResult.data ?? []) {
    const dateStr = (row.created_at as string).slice(0, 10);
    const slot = activity.find((a) => a.date === dateStr);
    if (slot) slot.count++;
  }
  const maxCount = Math.max(...activity.map((a) => a.count), 1);

  // Track progression
  const masteries = (masteriesResult.data ?? []) as unknown as MasteryEntry[];
  const trackMap = new Map<
    string,
    {
      title: string;
      slug: string;
      moduleMap: Map<string, { title: string; target: number; scores: number[] }>;
    }
  >();

  for (const m of masteries) {
    const mod = m.concepts?.modules;
    if (!mod?.tracks) continue;
    const track = mod.tracks;
    if (!trackMap.has(track.id)) {
      trackMap.set(track.id, { title: track.title, slug: track.slug, moduleMap: new Map() });
    }
    const te = trackMap.get(track.id)!;
    if (!te.moduleMap.has(mod.id)) {
      te.moduleMap.set(mod.id, {
        title: mod.title,
        target: mod.module_targets?.[0]?.target_mastery ?? 0.8,
        scores: [],
      });
    }
    te.moduleMap.get(mod.id)!.scores.push(Number(m.mastery_score));
  }

  const trackProgression = [...trackMap.values()].map((t) => ({
    title: t.title,
    slug: t.slug,
    modules: [...t.moduleMap.values()].map((m) => ({
      title: m.title,
      target: m.target,
      avg: m.scores.length > 0 ? m.scores.reduce((a, b) => a + b, 0) / m.scores.length : null,
    })),
  }));

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-3xl flex flex-col gap-6">
        <header>
          <h1 className="text-xl font-semibold text-foreground">Tableau de bord</h1>
        </header>

        {/* Monday weekly plan banner */}
        {isMonday && (
          <Callout variant="info" title="Plan de révision hebdomadaire">
            <p>
              {dueCount > 0
                ? `${dueCount} exercice${dueCount > 1 ? "s" : ""} en révision due.`
                : "Aucune révision due pour l'instant — bonne semaine !"}
              {weakConcepts.length > 0 &&
                ` Points faibles à retravailler : ${weakConcepts.map((c) => c.concepts?.title ?? "—").join(", ")}.`}
            </p>
          </Callout>
        )}

        {/* Due count + Weakest concepts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm text-muted-foreground font-medium">Révisions du jour</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-4xl font-bold tabular-nums">{dueCount}</p>
              <p className="text-xs text-muted-foreground mt-1">
                exercice{dueCount !== 1 ? "s" : ""} en attente
              </p>
              {dueCount > 0 && (
                <Link
                  href="/session"
                  className="mt-3 inline-flex items-center gap-1 rounded-md bg-primary text-primary-foreground text-sm font-semibold px-3 py-1.5 hover:opacity-90 transition-opacity"
                >
                  Commencer →
                </Link>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm text-muted-foreground font-medium">
                3 concepts les plus faibles
              </CardTitle>
            </CardHeader>
            <CardContent>
              {weakConcepts.length === 0 ? (
                <p className="text-sm text-muted-foreground">Aucune donnée encore — faites des sessions !</p>
              ) : (
                <ul className="flex flex-col gap-2.5">
                  {weakConcepts.map((wc, i) => (
                    <li key={i} className="flex items-center justify-between gap-2">
                      <div className="flex flex-col min-w-0">
                        <span className="text-sm font-medium truncate">
                          {wc.concepts?.title ?? "—"}
                        </span>
                        <span className="text-xs text-muted-foreground truncate">
                          {wc.concepts?.modules?.title ?? ""}
                        </span>
                      </div>
                      <Badge variant="muted" className="tabular-nums shrink-0">
                        {Math.round(wc.mastery_score * 100)} %
                      </Badge>
                    </li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Activity last 7 days */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm text-muted-foreground font-medium">
              Activité (7 derniers jours)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-end gap-1.5 h-16">
              {activity.map((d) => (
                <div key={d.date} className="flex flex-col items-center gap-1 flex-1">
                  <div
                    className="w-full rounded-sm bg-primary/80 min-h-[2px] transition-all"
                    style={{ height: `${Math.max(2, (d.count / maxCount) * 48)}px` }}
                    title={`${d.count} tentative${d.count !== 1 ? "s" : ""}`}
                  />
                  <span className="text-[10px] text-muted-foreground">{d.label}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Track progression */}
        {trackProgression.length > 0 ? (
          <Card>
            <CardHeader>
              <CardTitle className="text-sm text-muted-foreground font-medium">
                Progression par filière
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-5">
                {trackProgression.map((track) => (
                  <div key={track.slug}>
                    <p className="text-sm font-semibold text-foreground mb-2">{track.title}</p>
                    <div className="flex flex-col gap-3">
                      {track.modules.map((mod) => (
                        <div key={mod.title}>
                          <div className="flex justify-between items-baseline mb-1">
                            <span className="text-xs text-muted-foreground">{mod.title}</span>
                            {mod.avg !== null ? (
                              <span className="text-xs tabular-nums text-muted-foreground">
                                {Math.round(mod.avg * 100)} % — obj.{" "}
                                {Math.round(mod.target * 100)} %
                              </span>
                            ) : (
                              <span className="text-xs text-muted-foreground italic">
                                pas assez de données
                              </span>
                            )}
                          </div>
                          {mod.avg !== null && (
                            <div className="relative h-2 rounded-full bg-muted overflow-hidden">
                              <div
                                className={`absolute left-0 top-0 h-full rounded-full transition-all ${
                                  mod.avg >= mod.target ? "bg-green-500" : "bg-primary"
                                }`}
                                style={{ width: `${Math.min(100, mod.avg * 100)}%` }}
                              />
                              {/* Target marker */}
                              <div
                                className="absolute top-0 h-full w-px bg-foreground/30"
                                style={{ left: `${mod.target * 100}%` }}
                              />
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ) : (
          <Callout variant="info" title="Aucune donnée de maîtrise disponible">
            <p>
              Faites des sessions d&apos;entraînement — la progression par filière apparaîtra
              ici une fois les premiers concepts révisés.
            </p>
          </Callout>
        )}
      </div>
    </main>
  );
}
