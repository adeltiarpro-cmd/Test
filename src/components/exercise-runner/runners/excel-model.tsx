"use client";

import { ModelWorkshop, type CellResult } from "@/components/model-workshop";
import type { ModelTemplate } from "@/lib/model-actions";

interface ExcelModelRunnerProps {
  payload: {
    template_id: string;
    editable_cells: string[];
    given_cells?: Record<string, string | number>;
    check_mode: "value" | "formula" | "both";
    _templateData?: ModelTemplate;
  };
  onSubmit: (cells: Record<string, string>) => void;
  disabled?: boolean;
  cellResults?: Record<string, CellResult>;
}

export function ExcelModelRunner({
  payload,
  onSubmit,
  disabled,
  cellResults,
}: ExcelModelRunnerProps) {
  const { _templateData, editable_cells, given_cells, check_mode } = payload;

  if (!_templateData) {
    return (
      <p className="text-sm text-muted-foreground italic">
        Données du modèle non disponibles — relancez la session.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      <p className="text-sm font-semibold text-foreground">{_templateData.title}</p>
      {_templateData.description && (
        <p className="text-xs text-muted-foreground">{_templateData.description}</p>
      )}
      <ModelWorkshop
        sheet={_templateData.sheet}
        editableCells={editable_cells}
        givenCells={given_cells}
        checkMode={check_mode}
        onSubmit={onSubmit}
        disabled={disabled}
        cellResults={cellResults}
      />
    </div>
  );
}
