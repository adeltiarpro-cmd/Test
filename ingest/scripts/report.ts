#!/usr/bin/env tsx
/**
 * report.ts — couverture par module/type/difficulté.
 * Lit canonical/*.json et écrit docs/ingest/COVERAGE.md.
 * Ne lit PAS la base — travaille sur les fichiers locaux.
 *
 * Usage : tsx scripts/report.ts
 */
import { readdir, readFile, writeFile } from "fs/promises";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname  = dirname(fileURLToPath(import.meta.url));
const CANONICAL  = join(__dirname, "../canonical");
const COVERAGE_PATH = join(__dirname, "../../docs/ingest/COVERAGE.md");

type BatchItem = {
  external_key: string;
  type: string;
  difficulty: number;
};
type Batch = { source: string; track: string; module: string; items: BatchItem[] };

type ModuleKey = string; // "track/module"
type TypeKey   = string;

type Stats = {
  total: number;
  byType: Record<TypeKey, number>;
  byDifficulty: Record<number, number>;
};

const DIFFICULTIES = [1, 2, 3, 4, 5];
const TYPES = [
  "mcq", "numeric", "formula_cloze", "excel_model", "statement_interactive",
  "graph_fill", "case_structuring", "market_sizing", "case_math", "short_answer",
];

function pad(s: string | number, n: number) {
  return String(s).padEnd(n);
}

async function main() {
  const allFiles = await readdir(CANONICAL);
  const files = allFiles.filter((f) => f.endsWith(".json") && !f.startsWith("_"));

  const statsMap = new Map<ModuleKey, Stats>();
  let grandTotal = 0;

  for (const file of files) {
    const batch = JSON.parse(
      await readFile(join(CANONICAL, file), "utf-8")
    ) as Batch;

    const key: ModuleKey = `${batch.track}/${batch.module}`;
    if (!statsMap.has(key)) {
      statsMap.set(key, { total: 0, byType: {}, byDifficulty: {} });
    }
    const stats = statsMap.get(key)!;

    for (const item of batch.items) {
      stats.total++;
      grandTotal++;
      stats.byType[item.type] = (stats.byType[item.type] ?? 0) + 1;
      stats.byDifficulty[item.difficulty] = (stats.byDifficulty[item.difficulty] ?? 0) + 1;
    }
  }

  // ── Console output ─────────────────────────────────────────
  console.log("\n📊 Couverture des exercices (depuis canonical/)\n");
  console.log(`Modules couverts : ${statsMap.size}   |   Total items : ${grandTotal}\n`);

  for (const [module, stats] of statsMap) {
    console.log(`  ${module}  (${stats.total} items)`);
    for (const t of TYPES) {
      if (stats.byType[t]) console.log(`    ${pad(t, 24)} ${stats.byType[t]}`);
    }
    for (const d of DIFFICULTIES) {
      if (stats.byDifficulty[d]) console.log(`    diff=${d}: ${stats.byDifficulty[d]}`);
    }
  }

  // ── Markdown pour COVERAGE.md ──────────────────────────────
  const lines: string[] = [
    "# Couverture des exercices ingérés",
    "",
    `*Mis à jour par \`report.ts\` — ${new Date().toISOString().slice(0, 10)}*`,
    "",
    `**Total :** ${grandTotal} exercices — **${statsMap.size}** module(s) couverts`,
    "",
  ];

  for (const [module, stats] of statsMap) {
    lines.push(`## ${module}  *(${stats.total} items)*`);
    lines.push("");

    // Tableau types
    lines.push("| Type | Count |");
    lines.push("|---|---|");
    for (const t of TYPES) {
      if (stats.byType[t]) lines.push(`| \`${t}\` | ${stats.byType[t]} |`);
    }
    lines.push("");

    // Tableau difficultés
    lines.push("| Difficulté | Count |");
    lines.push("|---|---|");
    for (const d of DIFFICULTIES) {
      if (stats.byDifficulty[d]) lines.push(`| ${d} | ${stats.byDifficulty[d]} |`);
    }
    lines.push("");
  }

  await writeFile(COVERAGE_PATH, lines.join("\n"));
  console.log(`\n✓ ${COVERAGE_PATH} mis à jour`);
}

main().catch((err) => { console.error(err); process.exit(1); });
