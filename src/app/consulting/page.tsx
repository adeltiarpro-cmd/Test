import { redirect } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/server";
import { listConsultingGraphs } from "@/lib/graph-actions";
import { Card, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button-variants";

export const metadata = { title: "Consulting — Graphes de connaissances" };

export default async function ConsultingPage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const graphs = await listConsultingGraphs();

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-3xl flex flex-col gap-6">
        <header>
          <h1 className="text-xl font-semibold text-foreground">Consulting — Cartes de connaissances</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Explorez les guides d&apos;industrie Umbrex. Basculez en mode à trous pour vous tester.
          </p>
        </header>

        {graphs.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            Aucun graphe disponible. Exécutez{" "}
            <code className="font-mono text-xs bg-muted px-1 rounded">supabase db reset</code>{" "}
            pour charger les données de test.
          </p>
        ) : (
          <div className="grid sm:grid-cols-2 gap-3">
            {graphs.map((g) => (
              <Card key={g.id}>
                <CardHeader>
                  <CardTitle>{g.title}</CardTitle>
                  {g.description && (
                    <CardDescription>{g.description}</CardDescription>
                  )}
                </CardHeader>
                <CardFooter className="justify-between">
                  <Badge variant="muted">{g.node_count} nœuds</Badge>
                  <Link
                    href={`/consulting/${g.id}`}
                    className={buttonVariants({ variant: "outline", size: "sm" })}
                  >
                    Explorer →
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
