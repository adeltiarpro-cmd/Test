"use server";

import { revalidatePath } from "next/cache";
import { ExerciseSchema } from "@prep/schemas";
import { createAdminClient } from "@/lib/supabase/admin";
import { getAdminUser } from "./guard";

const OWN_SOURCE_TITLE = "Mes propres exercices";

export type SaveExerciseInput = {
  id?: string;
  type: string;
  moduleId: string;
  difficulty: number;
  promptMdx: string;
  payload: unknown;
  solution: unknown;
  sourceRef?: string;
  conceptSlug?: string;
};

export type ActionResult = { ok: true; id: string } | { ok: false; error: string };

type Admin = ReturnType<typeof createAdminClient>;

async function ownSourceId(admin: Admin): Promise<string> {
  const { data: existing } = await admin
    .from("sources")
    .select("id")
    .eq("kind", "own")
    .eq("title", OWN_SOURCE_TITLE)
    .maybeSingle();
  if (existing) return existing.id as string;

  const { data: created, error } = await admin
    .from("sources")
    .insert({ kind: "own", title: OWN_SOURCE_TITLE })
    .select("id")
    .single();
  if (error || !created) throw new Error(`Source non créée : ${error?.message ?? "inconnue"}`);
  return created.id as string;
}

function slugify(text: string): string {
  return text
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export async function saveExercise(input: SaveExerciseInput): Promise<ActionResult> {
  // Jamais confiance au seul client : droit admin et schéma revérifiés ici
  const user = await getAdminUser();
  if (!user) return { ok: false, error: "Accès réservé à l'administrateur." };

  const parsed = ExerciseSchema.safeParse({
    type: input.type,
    payload: input.payload,
    solution: input.solution,
  });
  if (!parsed.success) {
    const details = parsed.error.issues
      .map((issue) => `${issue.path.join(".") || "(racine)"} : ${issue.message}`)
      .join(" | ");
    return { ok: false, error: `Exercice invalide. ${details}` };
  }

  const prompt = input.promptMdx.trim();
  if (!prompt) return { ok: false, error: "L'énoncé est vide." };
  if (!Number.isInteger(input.difficulty) || input.difficulty < 1 || input.difficulty > 5) {
    return { ok: false, error: "La difficulté doit être un entier de 1 à 5." };
  }

  try {
    const admin = createAdminClient();

    const { data: moduleRow } = await admin
      .from("modules")
      .select("id")
      .eq("id", input.moduleId)
      .maybeSingle();
    if (!moduleRow) return { ok: false, error: "Module introuvable." };

    const sourceId = await ownSourceId(admin);
    const ref = input.sourceRef?.trim();
    const row = {
      module_id: input.moduleId,
      source_id: sourceId,
      type: parsed.data.type,
      difficulty: input.difficulty,
      payload: { prompt_mdx: prompt, ...(parsed.data.payload as Record<string, unknown>) },
      solution: parsed.data.solution,
      tags: ref ? [`ref:${ref}`] : [],
    };

    let exerciseId: string;
    if (input.id) {
      // Édition : limitée aux exercices de la source « own »
      const { data, error } = await admin
        .from("exercises")
        .update(row)
        .eq("id", input.id)
        .eq("source_id", sourceId)
        .select("id")
        .maybeSingle();
      if (error) return { ok: false, error: error.message };
      if (!data) return { ok: false, error: "Exercice introuvable parmi tes saisies manuelles." };
      exerciseId = data.id as string;
    } else {
      const { data, error } = await admin
        .from("exercises")
        .insert({ ...row, external_key: `manual-${crypto.randomUUID()}` })
        .select("id")
        .single();
      if (error || !data) return { ok: false, error: error?.message ?? "Insertion impossible." };
      exerciseId = data.id as string;
    }

    // Concept optionnel : créé dans le module s'il n'existe pas, comme le fait le loader
    await admin.from("exercise_concepts").delete().eq("exercise_id", exerciseId);
    const slug = input.conceptSlug ? slugify(input.conceptSlug) : "";
    if (slug) {
      let { data: concept } = await admin
        .from("concepts")
        .select("id")
        .eq("module_id", input.moduleId)
        .eq("slug", slug)
        .maybeSingle();
      if (!concept) {
        const title = slug.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
        const created = await admin
          .from("concepts")
          .insert({ module_id: input.moduleId, slug, title })
          .select("id")
          .single();
        concept = created.data;
      }
      if (concept) {
        await admin
          .from("exercise_concepts")
          .insert({ exercise_id: exerciseId, concept_id: concept.id as string });
      }
    }

    revalidatePath("/admin/exercises");
    return { ok: true, id: exerciseId };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e.message : "Erreur inconnue." };
  }
}

export async function deleteExercise(id: string): Promise<ActionResult> {
  const user = await getAdminUser();
  if (!user) return { ok: false, error: "Accès réservé à l'administrateur." };

  try {
    const admin = createAdminClient();
    const sourceId = await ownSourceId(admin);
    const { error } = await admin
      .from("exercises")
      .delete()
      .eq("id", id)
      .eq("source_id", sourceId);
    if (error) return { ok: false, error: error.message };

    revalidatePath("/admin/exercises");
    return { ok: true, id };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e.message : "Erreur inconnue." };
  }
}
