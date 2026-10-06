import { notFound } from "next/navigation";
import { getAdminUser } from "@/lib/admin/guard";
import { ExerciseForm } from "../exercise-form";
import { fetchModuleOptions } from "../modules";

export const metadata = { title: "Nouvel exercice — Admin" };

export default async function NewExercisePage() {
  // Le middleware renvoie déjà un 403 aux non-admins ; second contrôle côté serveur
  if (!(await getAdminUser())) notFound();
  const modules = await fetchModuleOptions();

  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-4xl flex flex-col gap-6">
        <header>
          <h1 className="text-xl font-semibold text-foreground">Nouvel exercice</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Saisie manuelle, rattachée à la source « Mes propres exercices ».
          </p>
        </header>
        <ExerciseForm modules={modules} />
      </div>
    </main>
  );
}
