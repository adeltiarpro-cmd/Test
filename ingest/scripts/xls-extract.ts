#!/usr/bin/env tsx
/**
 * xls-extract.ts — extrait la structure d'un classeur Excel en JSON
 * pour alimenter model_templates.sheet (jsonb).
 *
 * Usage :
 *   tsx scripts/xls-extract.ts <workbook.xlsx> [--sheet SheetName] [--blanks <blanks.json>]
 *
 * Sortie JSON vers stdout — pipe vers un fichier ou une commande Supabase.
 *
 * Format de sortie :
 *   {
 *     "sheets": {
 *       "Sheet1": {
 *         "cells": { "A1": { "value": ..., "formula": ..., "format": ..., "locked": ... } },
 *         "merge_cells": [...],
 *         "dimensions": { "rows": N, "cols": M }
 *       }
 *     },
 *     "editable_cells": ["C5", "D10"]   ← cellules non verrouillées selon blanks.json
 *   }
 *
 * blanks.json : { "blanks": ["C5", "D10", ...] }
 * Le choix des cellules à masquer est TOUJOURS manuel — jamais deviné par heuristique.
 */
import { readFile } from "fs/promises";
import { existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import * as XLSX from "xlsx";

const __dirname = dirname(fileURLToPath(import.meta.url));

type CellData = {
  value:   string | number | boolean | null;
  formula: string | null;
  format:  string | null;
  locked:  boolean;
};

type SheetData = {
  cells:      Record<string, CellData>;
  merge_cells: string[];
  dimensions: { rows: number; cols: number };
};

type ExtractResult = {
  sheets:         Record<string, SheetData>;
  editable_cells: string[];
};

function parseCellAddress(ref: string): { r: number; c: number } {
  return XLSX.utils.decode_cell(ref);
}

function extractSheet(ws: XLSX.WorkSheet, blankCells: Set<string>): SheetData {
  const cells: Record<string, CellData> = {};
  const range = XLSX.utils.decode_range(ws["!ref"] ?? "A1:A1");
  const merges = (ws["!merges"] ?? []).map(
    (m) => `${XLSX.utils.encode_cell(m.s)}:${XLSX.utils.encode_cell(m.e)}`
  );

  for (let r = range.s.r; r <= range.e.r; r++) {
    for (let c = range.s.c; c <= range.e.c; c++) {
      const ref  = XLSX.utils.encode_cell({ r, c });
      const cell = ws[ref] as XLSX.CellObject | undefined;
      if (!cell) continue;

      cells[ref] = {
        value:   cell.v !== undefined ? (cell.v as string | number | boolean) : null,
        formula: cell.f ? `=${cell.f}` : null,
        format:  cell.z ?? null,
        locked:  !blankCells.has(ref),
      };
    }
  }

  return {
    cells,
    merge_cells: merges,
    dimensions: {
      rows: range.e.r - range.s.r + 1,
      cols: range.e.c - range.s.c + 1,
    },
  };
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0].startsWith("--")) {
    console.error(
      "Usage: tsx scripts/xls-extract.ts <workbook.xlsx> [--sheet SheetName] [--blanks blanks.json]"
    );
    process.exit(1);
  }

  const workbookPath = args[0];
  if (!existsSync(workbookPath)) {
    console.error(`Fichier introuvable : ${workbookPath}`);
    process.exit(1);
  }

  const targetSheet = args.includes("--sheet")
    ? args[args.indexOf("--sheet") + 1]
    : undefined;

  const blanksFile = args.includes("--blanks")
    ? args[args.indexOf("--blanks") + 1]
    : undefined;

  // Charge la config des cellules éditables (décision manuelle, jamais heuristique)
  const blankCells = new Set<string>();
  if (blanksFile) {
    if (!existsSync(blanksFile)) {
      console.error(`Fichier blanks introuvable : ${blanksFile}`);
      process.exit(1);
    }
    const blanksData = JSON.parse(await readFile(blanksFile, "utf-8")) as {
      blanks: string[];
    };
    blanksData.blanks.forEach((ref) => blankCells.add(ref.toUpperCase()));
  }

  const workbook = XLSX.readFile(workbookPath, { cellStyles: true, cellFormula: true });

  const sheetsToProcess = targetSheet
    ? [targetSheet]
    : workbook.SheetNames;

  const result: ExtractResult = { sheets: {}, editable_cells: [...blankCells] };

  for (const name of sheetsToProcess) {
    const ws = workbook.Sheets[name];
    if (!ws) {
      console.error(`Onglet "${name}" introuvable dans le classeur`);
      continue;
    }
    result.sheets[name] = extractSheet(ws, blankCells);
  }

  // Sortie JSON vers stdout
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

main().catch((err) => { console.error(err); process.exit(1); });
