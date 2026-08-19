import { notFound, redirect } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/server";
import { fetchGraphData } from "@/lib/graph-actions";
import { GraphExplorer } from "@/components/graph-explorer";
import { buttonVariants } from "@/components/ui/button-variants";

interface Props {
  params: Promise<{ graphId: string }>;
}

export async function generateMetadata({ params }: Props) {
  const { graphId } = await params;
  const graph = await fetchGraphData(graphId);
  return { title: graph ? `${graph.title} — Consulting` : "Graphe introuvable" };
}

export default async function GraphPage({ params }: Props) {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { graphId } = await params;
  const graph = await fetchGraphData(graphId);
  if (!graph) notFound();

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-3xl flex flex-col gap-6">
        <nav>
          <Link href="/consulting" className={buttonVariants({ variant: "ghost", size: "sm" })}>
            ← Consulting
          </Link>
        </nav>

        {/* GraphExplorer is a client component — standalone (read + fill toggle) */}
        <GraphExplorer graph={graph} />
      </div>
    </main>
  );
}
