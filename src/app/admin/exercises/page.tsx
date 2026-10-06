import Link from "next/link";
import { notFound } from "next/navigation";
import type { Route } from "next";
import { getAdminUser } from "@/lib/admin/guard";
import { createAdminClient } from "@/lib/supabase/admin";
import { Callout } from "@/components/ui/callout";
import { DeleteButton } from "./delete-button";

export const metadata = { title: "Mes exercices — Admin" };

type Row = {
  id: string;
  type: string;
  difficulty: number;
  payload: { prompt_mdx?: string } | null;
  created_at: string;
  modules: { title: string } | null;
};

export default async function AdminExercisesPage() {
  if (!(await getAdminUser())) notFound();

  const admin = createAdminClient();
  const { data } = await admin
    .from("exercises")
    .select("id, type, difficulty, payload, created_at, modules(title)")
    .like("external_key", "manual-%")
    .order("created_at", { ascending: false })
    .limit(200);
  const rows = (data ?? []) as unknown as Row[];

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-4xl flex flex-col gap-6">
        <header className="flex items-center justify-between gap-4 flex-wrap">
          <div>
            <h1 className="text-xl font-semibold text-foreground">Mes exercices</h1>
            <p className="text-sm text-muted-foreground mt-0.5">
              {rows.length} saisie{rows.length > 1 ? "s" : ""} manuelle{rows.length > 1 ? "s" : ""}.
            </p>
          </div>
          <Link
            href={"/admin/exercises/new" as Route}
            className="inline-flex items-center rounded-md bg-primary text-primary-foreground text-sm font-semibold px-4 py-2 min-h-[44px] hover:opacity-90"
          >
            Nouvel exercice
          </Link>
        </header>

        {rows.length === 0 ? (
          <Callout variant="info" title="Aucune saisie manuelle pour l'instant">
            <p>Les exercices créés avec le formulaire apparaîtront ici.</p>
          </Callout>
        ) : (
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="w-full text-sm">
              <thead className="bg-muted text-left text-xs text-muted-foreground">
                <tr>
                  <th scope="col" className="px-3 py-2 font-medium">Énoncé</th>
                  <th scope="col" className="px-3 py-2 font-medium">Type</th>
                  <th scope="col" className="px-3 py-2 font-medium">Module</th>
                  <th scope="col" className="px-3 py-2 font-medium">Diff.</th>
                  <th scope="col" className="px-3 py-2 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.id} className="border-t border-border align-top">
                    <td className="px-3 py-2 text-foreground max-w-[320px]">
                      <span className="line-clamp-2">{row.payload?.prompt_mdx ?? "(sans énoncé)"}</span>
                    </td>
                    <td className="px-3 py-2 text-muted-foreground whitespace-nowrap">{row.type}</td>
                    <td className="px-3 py-2 text-muted-foreground">{row.modules?.title ?? ""}</td>
                    <td className="px-3 py-2 tabular-nums text-muted-foreground">{row.difficulty}</td>
                    <td className="px-3 py-2">
                      <span className="inline-flex items-center gap-2 flex-wrap">
                        <Link
                          href={`/admin/exercises/${row.id}` as Route}
                          className="inline-flex items-center rounded-md border border-border px-2.5 py-1.5 text-xs font-semibold min-h-[36px] text-foreground hover:bg-muted"
                        >
                          Modifier
                        </Link>
                        <DeleteButton id={row.id} />
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}
