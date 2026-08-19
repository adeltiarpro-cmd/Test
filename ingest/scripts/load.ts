#!/usr/bin/env tsx
/**
 * load.ts — importe les lots canonical/*.json dans Supabase (service_role).
 * Idempotent : ON CONFLICT (external_key) DO UPDATE.
 * Un réimport du même lot ne crée aucun doublon.
 *
 * Usage : tsx scripts/load.ts [--file batch-001-fake.json] [--dry-run]
 */
import { readdir, readFile } from "fs/promises";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import { createClient } from "@supabase/supabase-js";
import ws from "ws";
import { ExerciseSchema } from "../../packages/schemas/exercises.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Charge les variables d'environnement depuis la racine du repo
dotenv.config({ path: join(__dirname, "../../.env.local") });

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_KEY  = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SERVICE_KEY) {
  console.error("NEXT_PUBLIC_SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY requis dans .env.local");
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SERVICE_KEY, {
  auth: { persistSession: false },
  realtime: { transport: ws },
});

const CANONICAL_DIR = join(__dirname, "../canonical");
const DRY_RUN = process.argv.includes("--dry-run");

type BatchItem = {
  external_key: string;
  type: string;
  difficulty: number;
  source_ref?: string;
  concepts?: string[];
  prompt_mdx: string;
  payload: Record<string, unknown>;
  solution: Record<string, unknown>;
};

type Batch = {
  source: string;
  track: string;
  module: string;
  items: BatchItem[];
};

// ── Helpers ───────────────────────────────────────────────────────────────────

async function resolveModuleId(track: string, module: string): Promise<string | null> {
  const { data } = await supabase
    .from("modules")
    .select("id, tracks!inner(slug)")
    .eq("slug", module)
    .eq("tracks.slug", track)
    .single();
  return data?.id ?? null;
}

async function resolveOrCreateSourceId(title: string): Promise<string | null> {
  const { data: existing } = await supabase
    .from("sources")
    .select("id")
    .eq("title", title)
    .maybeSingle();

  if (existing) return existing.id;

  const { data: created, error } = await supabase
    .from("sources")
    .insert({ kind: "internal", title })
    .select("id")
    .single();

  if (error) { console.warn(`  ⚠️  source "${title}" non créée : ${error.message}`); return null; }
  return created.id;
}

async function resolveConceptIds(slugs: string[], moduleId: string): Promise<string[]> {
  if (slugs.length === 0) return [];

  const { data: existing } = await supabase
    .from("concepts")
    .select("id, slug")
    .eq("module_id", moduleId)
    .in("slug", slugs);

  const found = new Map((existing ?? []).map((r) => [r.slug as string, r.id as string]));
  const missing = slugs.filter((s) => !found.has(s));

  if (missing.length > 0) {
    if (DRY_RUN) {
      console.log(`  [dry] concepts à créer : ${missing.join(", ")}`);
    } else {
      const toInsert = missing.map((slug) => ({
        module_id: moduleId,
        slug,
        title: slug.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()),
      }));
      const { data: created, error } = await supabase
        .from("concepts")
        .insert(toInsert)
        .select("id, slug");
      if (error) {
        console.warn(`  ⚠️  concepts non créés : ${error.message}`);
      } else {
        for (const r of created ?? []) found.set(r.slug as string, r.id as string);
        console.log(`  ➕  concepts créés : ${missing.join(", ")}`);
      }
    }
  }

  return slugs.map((s) => found.get(s)).filter((id): id is string => id !== undefined);
}

async function upsertExercise(
  item: BatchItem,
  moduleId: string,
  sourceId: string | null
): Promise<string | null> {
  const validation = ExerciseSchema.safeParse({
    type: item.type,
    payload: item.payload,
    solution: item.solution,
  });

  if (!validation.success) {
    console.warn(`  ✗  ${item.external_key} — validation échouée, skipped`);
    return null;
  }

  // prompt_mdx est fusionné dans le payload stocké en DB
  const payloadWithPrompt = { prompt_mdx: item.prompt_mdx, ...item.payload };

  if (DRY_RUN) {
    console.log(`  [dry] upsert ${item.external_key} (${item.type}, diff=${item.difficulty})`);
    return "dry-run";
  }

  const { data, error } = await supabase
    .from("exercises")
    .upsert(
      {
        module_id:    moduleId,
        source_id:    sourceId,
        type:         item.type,
        difficulty:   item.difficulty,
        payload:      payloadWithPrompt,
        solution:     item.solution,
        tags:         [],
        external_key: item.external_key,
      },
      { onConflict: "external_key" }
    )
    .select("id")
    .single();

  if (error) {
    console.error(`  ✗  ${item.external_key} — ${error.message}`);
    return null;
  }
  return data.id;
}

async function upsertExerciseConcepts(exerciseId: string, conceptIds: string[]) {
  if (conceptIds.length === 0) return;
  const rows = conceptIds.map((concept_id) => ({ exercise_id: exerciseId, concept_id }));
  const { error } = await supabase
    .from("exercise_concepts")
    .upsert(rows, { onConflict: "exercise_id,concept_id" });
  if (error) console.warn(`  ⚠️  exercise_concepts : ${error.message}`);
}

// ── Vérification d'idempotence ────────────────────────────────────────────────

async function checkIdempotence(externalKeys: string[]): Promise<number> {
  const { count } = await supabase
    .from("exercises")
    .select("*", { count: "exact", head: true })
    .in("external_key", externalKeys);
  return count ?? 0;
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  if (DRY_RUN) console.log("🔍 Mode dry-run — aucune écriture en base\n");

  const targetFile = process.argv.includes("--file")
    ? process.argv[process.argv.indexOf("--file") + 1]
    : undefined;

  const allFiles = await readdir(CANONICAL_DIR);
  const files = allFiles.filter(
    (f) => f.endsWith(".json") && !f.startsWith("_") && (targetFile ? f === targetFile : true)
  );

  if (files.length === 0) {
    console.log("Aucun fichier JSON trouvé dans canonical/");
    return;
  }

  let totalInserted = 0;
  let totalSkipped  = 0;

  for (const file of files) {
    const filePath = join(CANONICAL_DIR, file);
    const batch = JSON.parse(await readFile(filePath, "utf-8")) as Batch;
    console.log(`\n📦 ${file}  →  ${batch.track}/${batch.module}`);

    const moduleId = await resolveModuleId(batch.track, batch.module);
    if (!moduleId) {
      console.error(`  ✗ Module "${batch.track}/${batch.module}" introuvable — batch ignoré`);
      continue;
    }

    const sourceId = await resolveOrCreateSourceId(batch.source);

    // Compte avant pour détecter les doublons
    const externalKeys = batch.items.map((i) => i.external_key);
    const countBefore = await checkIdempotence(externalKeys);

    for (const item of batch.items) {
      const conceptIds = await resolveConceptIds(item.concepts ?? [], moduleId);
      const exerciseId = await upsertExercise(item, moduleId, sourceId);

      if (exerciseId && exerciseId !== "dry-run") {
        await upsertExerciseConcepts(exerciseId, conceptIds);
        console.log(`  ✓  ${item.external_key} (${item.type})`);
        totalInserted++;
      } else if (!exerciseId) {
        totalSkipped++;
      }
    }

    if (!DRY_RUN) {
      const countAfter = await checkIdempotence(externalKeys);
      const newRows = countAfter - countBefore;
      console.log(
        `\n  Idempotence : avant=${countBefore} après=${countAfter} — ${newRows} nouveau(x), ${batch.items.length - newRows} inchangé(s)`
      );
    }
  }

  console.log(
    `\n═══════════════════════════════\n` +
    `  ✓ Importés : ${totalInserted}\n` +
    `  ✗ Ignorés  : ${totalSkipped}\n` +
    `═══════════════════════════════`
  );
}

main().catch((err) => { console.error(err); process.exit(1); });
