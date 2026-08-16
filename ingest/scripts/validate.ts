#!/usr/bin/env tsx
/**
 * validate.ts — valide chaque item de canonical/*.json contre ExerciseSchema.
 * Les items invalides sont écrits dans canonical/_rejected/ avec le message Zod.
 * Jamais de correction automatique silencieuse.
 *
 * Usage : tsx scripts/validate.ts [--file batch-001-fake.json]
 */
import { readdir, readFile, writeFile, mkdir } from "fs/promises";
import { existsSync } from "fs";
import { join, basename, dirname } from "path";
import { fileURLToPath } from "url";
import { ExerciseSchema } from "../../packages/schemas/exercises.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CANONICAL_DIR = join(__dirname, "../canonical");
const REJECTED_DIR  = join(CANONICAL_DIR, "_rejected");

type BatchItem = {
  external_key: string;
  type: string;
  difficulty: number;
  source_ref?: string;
  concepts?: string[];
  prompt_mdx: string;
  payload: unknown;
  solution: unknown;
};

type Batch = {
  source: string;
  track: string;
  module: string;
  items: BatchItem[];
};

async function main() {
  await mkdir(REJECTED_DIR, { recursive: true });

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

  let totalValid = 0;
  let totalInvalid = 0;

  for (const file of files) {
    const filePath = join(CANONICAL_DIR, file);
    const batch = JSON.parse(await readFile(filePath, "utf-8")) as Batch;

    console.log(`\n📄 ${file}  (${batch.track}/${batch.module})`);

    const rejected: Array<{ external_key: string; errors: unknown }> = [];

    for (const item of batch.items) {
      const toValidate = {
        type: item.type,
        payload: item.payload,
        solution: item.solution,
      };
      const result = ExerciseSchema.safeParse(toValidate);

      if (result.success) {
        console.log(`  ✓  ${item.external_key}`);
        totalValid++;
      } else {
        const formatted = result.error.format();
        console.error(`  ✗  ${item.external_key}`);
        console.error(`     ${JSON.stringify(formatted, null, 2).slice(0, 300)}`);
        rejected.push({ external_key: item.external_key, errors: formatted });
        totalInvalid++;
      }
    }

    if (rejected.length > 0) {
      const ts = new Date().toISOString().replace(/[:.]/g, "-");
      const rejPath = join(
        REJECTED_DIR,
        `${basename(file, ".json")}-${ts}.json`
      );
      await writeFile(
        rejPath,
        JSON.stringify({ source_file: filePath, track: batch.track, module: batch.module, rejected }, null, 2)
      );
      console.error(`\n  ⚠️  ${rejected.length} item(s) rejeté(s) → ${rejPath}`);
    }
  }

  console.log(
    `\n═══════════════════════════════\n` +
    `  ✓ Valides  : ${totalValid}\n` +
    `  ✗ Rejetés  : ${totalInvalid}\n` +
    `═══════════════════════════════`
  );

  if (totalInvalid > 0) process.exit(1);
}

main().catch((err) => { console.error(err); process.exit(1); });
