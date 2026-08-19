"use client";

import {
  StatementInteractive,
  type LineResult,
} from "@/components/statement-interactive";

interface StatementInteractiveRunnerProps {
  payload: {
    statement: "is" | "bs" | "cf";
    lines: Array<{
      key: string;
      label: string;
      level: number;
      given?: boolean;
      editable: boolean;
      formula_hint?: string;
      value?: number;
    }>;
    linked_checks?: Array<{
      rule: "balance" | "cf_ties_to_cash" | "ni_flows_to_re";
    }>;
  };
  onSubmit: (values: Record<string, string>) => void;
  disabled?: boolean;
  lineResults?: Record<string, LineResult>;
}

export function StatementInteractiveRunner({
  payload,
  onSubmit,
  disabled,
  lineResults,
}: StatementInteractiveRunnerProps) {
  return (
    <StatementInteractive
      statement={payload.statement}
      lines={payload.lines}
      linkedChecks={payload.linked_checks}
      onSubmit={onSubmit}
      disabled={disabled}
      lineResults={lineResults}
    />
  );
}
