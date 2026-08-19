"use client";

import { useState, useMemo } from "react";
import { cn } from "@/lib/cn";
import { Button } from "@/components/ui/button";

type Line = {
  key: string;
  label: string;
  level: number;
  given?: boolean;
  editable: boolean;
  formula_hint?: string;
  value?: number;
};

type LinkedCheck = {
  rule: "balance" | "cf_ties_to_cash" | "ni_flows_to_re";
};

export type LineResult = {
  correct: boolean;
  explain_mdx: string;
};

interface Props {
  statement: "is" | "bs" | "cf";
  lines: Line[];
  linkedChecks?: LinkedCheck[];
  onSubmit: (values: Record<string, string>) => void;
  disabled?: boolean;
  lineResults?: Record<string, LineResult>;
}

function parseNum(s: string): number {
  return parseFloat(s.replace(",", ".")) || 0;
}

export function StatementInteractive({
  lines,
  linkedChecks,
  onSubmit,
  disabled,
  lineResults,
}: Props) {
  const [values, setValues] = useState<Record<string, string>>(() => {
    const init: Record<string, string> = {};
    for (const line of lines) {
      if (line.editable) init[line.key] = "";
    }
    return init;
  });

  const allFilled = lines
    .filter((l) => l.editable)
    .every((l) => values[l.key]?.trim() !== "");

  // Live consistency check (ni_flows_to_re): walk lines top-to-bottom,
  // track running subtotal; editable subtotals are compared to expected.
  const discrepancies = useMemo<string[]>(() => {
    const hasNiCheck = linkedChecks?.some((c) => c.rule === "ni_flows_to_re");
    if (!hasNiCheck || lineResults) return [];

    const result: string[] = [];
    let runningTotal: number | null = null;

    for (const line of lines) {
      const val = line.given
        ? (line.value ?? 0)
        : parseNum(values[line.key] ?? "0");

      if (line.level === 0) {
        if (runningTotal !== null && line.editable && values[line.key]?.trim()) {
          const delta = Math.abs(val - runningTotal);
          if (delta > 1) {
            result.push(
              `${line.label} : attendu ${runningTotal.toFixed(0)}, saisi ${val.toFixed(0)}`
            );
          }
        }
        runningTotal = val;
      } else {
        runningTotal = (runningTotal ?? 0) + val;
      }
    }
    return result;
  }, [lines, linkedChecks, values, lineResults]);

  const hasLinkedCheck = (linkedChecks?.length ?? 0) > 0;

  return (
    <div className="flex flex-col gap-4">
      <table className="w-full text-sm border-collapse">
        <tbody>
          {lines.map((line) => {
            const lr = lineResults?.[line.key];
            return (
              <tr
                key={line.key}
                className={cn(
                  "border-b border-border/40 last:border-0",
                  line.level === 0 ? "" : "text-muted-foreground"
                )}
              >
                {/* Label column */}
                <td
                  className={cn(
                    "py-1.5 text-foreground",
                    line.level === 0 ? "font-semibold" : "font-normal"
                  )}
                  style={{ paddingLeft: `${line.level * 24 + 8}px` }}
                >
                  {line.label}
                  {line.formula_hint && !lineResults && (
                    <span className="ml-2 text-xs font-normal text-muted-foreground italic">
                      {line.formula_hint}
                    </span>
                  )}
                </td>

                {/* Value column */}
                <td className="py-1.5 text-right w-36">
                  {line.editable ? (
                    <div className="flex flex-col items-end gap-0.5">
                      <input
                        type="number"
                        step="any"
                        value={values[line.key] ?? ""}
                        onChange={(e) =>
                          setValues((prev) => ({
                            ...prev,
                            [line.key]: e.target.value,
                          }))
                        }
                        disabled={!!disabled || !!lineResults}
                        aria-label={line.label}
                        className={cn(
                          "w-28 text-right px-2 py-1 text-sm font-mono rounded border bg-white",
                          "focus:outline-none focus:ring-1 focus:ring-primary",
                          "disabled:bg-muted/60 disabled:cursor-not-allowed",
                          lr
                            ? lr.correct
                              ? "border-green-500 bg-green-50"
                              : "border-red-400 bg-red-50"
                            : "border-border"
                        )}
                      />
                      {lr?.explain_mdx && (
                        <p
                          className={cn(
                            "text-xs max-w-[200px] text-right",
                            lr.correct ? "text-green-700" : "text-red-700"
                          )}
                        >
                          {lr.explain_mdx}
                        </p>
                      )}
                    </div>
                  ) : (
                    <span className="tabular-nums text-foreground">
                      {line.value !== undefined
                        ? line.value.toLocaleString("fr-FR")
                        : ""}
                    </span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Live linked-check indicator (shown only before submission) */}
      {hasLinkedCheck && !lineResults && (
        <div
          className={cn(
            "text-xs rounded px-3 py-2 border font-medium",
            discrepancies.length === 0
              ? "bg-green-50 border-green-300 text-green-700"
              : "bg-red-50 border-red-300 text-red-700"
          )}
        >
          {discrepancies.length === 0
            ? "Compte de résultat cohérent ✓"
            : `Incohérence : ${discrepancies.join(" · ")}`}
        </div>
      )}

      {!lineResults && (
        <Button
          onClick={() => onSubmit(values)}
          disabled={!allFilled || !!disabled}
          variant="secondary"
          size="sm"
          className="self-start"
        >
          Vérifier
        </Button>
      )}
    </div>
  );
}
