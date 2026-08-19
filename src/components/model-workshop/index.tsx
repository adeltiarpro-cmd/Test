"use client";

import { useMemo, useState, useCallback } from "react";
import HyperFormula from "hyperformula";
import type { ModelTemplateSheet } from "@/lib/model-actions";
import { cn } from "@/lib/cn";
import { Button } from "@/components/ui/button";

type CheckMode = "value" | "formula" | "both";

export type CellResult = {
  valueCorrect: boolean;
  formulaCorrect: boolean | null;
  explain_mdx?: string;
};

interface Props {
  sheet: ModelTemplateSheet;
  editableCells: string[];
  givenCells?: Record<string, string | number>;
  checkMode: CheckMode;
  onSubmit: (cells: Record<string, string>) => void;
  disabled?: boolean;
  cellResults?: Record<string, CellResult>;
}

// "B3" → { row: 2, col: 1 } (0-indexed)
function parseRef(ref: string): { row: number; col: number } {
  const up = ref.toUpperCase().replace(/\$/g, "");
  const colStr = up.match(/^([A-Z]+)/)?.[1] ?? "A";
  const rowStr = up.match(/(\d+)$/)?.[1] ?? "1";
  let col = 0;
  for (const ch of colStr) col = col * 26 + (ch.charCodeAt(0) - 64);
  return { row: parseInt(rowStr) - 1, col: col - 1 };
}

function cellColLetter(colIdx: number): string {
  // colIdx is 0-based; returns "A", "B", "C"...
  return String.fromCharCode(65 + colIdx);
}

export function ModelWorkshop({
  sheet,
  editableCells,
  givenCells,
  checkMode,
  onSubmit,
  disabled,
  cellResults,
}: Props) {
  const editableSet = useMemo(() => new Set(editableCells), [editableCells]);

  const [formulas, setFormulas] = useState<Record<string, string>>(() => {
    const init: Record<string, string> = {};
    for (const ref of editableCells) init[ref] = "";
    return init;
  });

  // Build HyperFormula instance from template data.
  // Editable cells are cleared; givenCells overrides are applied.
  const hf = useMemo(() => {
    const data = sheet.data.map((row) =>
      row.map((cell) => (cell === null ? "" : cell))
    ) as (string | number)[][];

    for (const ref of editableCells) {
      const { row, col } = parseRef(ref);
      if (data[row]) data[row][col] = "";
    }
    if (givenCells) {
      for (const [ref, val] of Object.entries(givenCells)) {
        const { row, col } = parseRef(ref);
        if (data[row]) data[row][col] = val;
      }
    }
    return HyperFormula.buildFromArray(data, { licenseKey: "gpl-v3" });
  }, [sheet, editableCells, givenCells]);

  const updateHF = useCallback(
    (ref: string, raw: string) => {
      const { row, col } = parseRef(ref);
      const cellValue = raw.startsWith("=")
        ? raw
        : raw.trim() === ""
        ? null
        : isNaN(Number(raw))
        ? raw
        : Number(raw);
      try {
        hf.setCellContents({ sheet: 0, row, col }, cellValue);
      } catch {
        // ignore formula parse errors — HF marks cell as error, that's fine
      }
    },
    [hf]
  );

  const handleChange = useCallback(
    (ref: string, value: string) => {
      updateHF(ref, value);
      setFormulas((prev) => ({ ...prev, [ref]: value }));
    },
    [updateHF]
  );

  const getDisplayValue = useCallback(
    (rowIdx: number, colIdx: number): string => {
      try {
        const val = hf.getCellValue({ sheet: 0, row: rowIdx, col: colIdx });
        if (val === null || val === undefined || val === "") return "";
        if (typeof val === "object") return "#ERR"; // DetailedCellError
        if (typeof val === "number") {
          if (Number.isInteger(val)) return val.toLocaleString("fr-FR");
          return val.toFixed(1).replace(".", ",");
        }
        return String(val);
      } catch {
        return "";
      }
    },
    [hf]
  );

  const allFilled = editableCells.every((ref) => formulas[ref]?.trim());
  const numCols = sheet.cols.length;

  function cellBorderClass(ref: string): string {
    if (!cellResults) return "";
    const r = cellResults[ref];
    if (!r) return "";
    if (r.valueCorrect && r.formulaCorrect !== false) return "ring-2 ring-green-500 bg-green-50";
    if (r.valueCorrect && r.formulaCorrect === false) return "ring-2 ring-orange-400 bg-orange-50";
    return "ring-2 ring-red-400 bg-red-50";
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="overflow-x-auto rounded border border-border">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-muted border-b border-border">
              {sheet.cols.map((col, ci) => (
                <th
                  key={ci}
                  className={cn(
                    "px-3 py-2 font-semibold text-foreground",
                    ci === 0 ? "text-left min-w-[160px]" : "text-right min-w-[110px]"
                  )}
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sheet.data.map((_, rowIdx) => (
              <tr key={rowIdx} className="border-b border-border/40 last:border-0">
                {Array.from({ length: numCols }, (__, colIdx) => {
                  // Col 0: always row label (read-only text)
                  if (colIdx === 0) {
                    return (
                      <td key={0} className="px-3 py-1.5 font-medium text-foreground">
                        {String(sheet.data[rowIdx][0] ?? "")}
                      </td>
                    );
                  }

                  const ref = `${cellColLetter(colIdx)}${rowIdx + 1}`;
                  const isEditable = editableSet.has(ref);
                  const cr = cellResults?.[ref];

                  if (isEditable) {
                    return (
                      <td key={colIdx} className="px-1.5 py-1">
                        <div className={cn("rounded", cellBorderClass(ref))}>
                          <input
                            type="text"
                            value={formulas[ref] ?? ""}
                            onChange={(e) => handleChange(ref, e.target.value)}
                            disabled={!!disabled || !!cellResults}
                            placeholder="="
                            aria-label={`Cellule ${ref}`}
                            className={cn(
                              "w-full px-2 py-1 text-right text-sm font-mono rounded border border-border bg-white",
                              "focus:outline-none focus:ring-1 focus:ring-primary",
                              "disabled:bg-muted/60 disabled:cursor-not-allowed"
                            )}
                          />
                          {/* Show computed result when formula starts with = */}
                          {formulas[ref]?.startsWith("=") && !cellResults && (
                            <p className="text-xs text-muted-foreground text-right px-2 pb-0.5">
                              = {getDisplayValue(rowIdx, colIdx)}
                            </p>
                          )}
                        </div>
                        {cr && cr.valueCorrect && cr.formulaCorrect === false && (
                          <p className="text-xs mt-1 text-right text-orange-700 font-medium">
                            Valeur juste — formule non conforme
                          </p>
                        )}
                        {cr?.explain_mdx && (
                          <p
                            className={cn(
                              "text-xs mt-0.5 text-right",
                              cr.valueCorrect && cr.formulaCorrect !== false
                                ? "text-green-700"
                                : cr.valueCorrect
                                ? "text-orange-700"
                                : "text-red-700"
                            )}
                          >
                            {cr.explain_mdx}
                          </p>
                        )}
                      </td>
                    );
                  }

                  // Read-only cell
                  return (
                    <td
                      key={colIdx}
                      className="px-3 py-1.5 text-right tabular-nums text-foreground bg-muted/20"
                    >
                      {getDisplayValue(rowIdx, colIdx)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend when check_mode=both and results available */}
      {cellResults && checkMode === "both" && (
        <div className="flex flex-wrap gap-4 text-xs text-muted-foreground">
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-sm ring-2 ring-green-500 bg-green-50 inline-block" />
            Correct
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-sm ring-2 ring-orange-400 bg-orange-50 inline-block" />
            Valeur juste · formule non conforme
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-sm ring-2 ring-red-400 bg-red-50 inline-block" />
            Incorrect
          </span>
        </div>
      )}

      {!cellResults && (
        <Button
          onClick={() => onSubmit(formulas)}
          disabled={!allFilled || !!disabled}
          variant="secondary"
          size="sm"
          className="self-start"
        >
          Vérifier les formules
        </Button>
      )}
    </div>
  );
}
