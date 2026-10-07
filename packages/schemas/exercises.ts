/**
 * Source de vérité unique des shapes payload/solution pour les 10 types d'exercices.
 * Utilisé par : pipeline d'ingestion (STEP-03), runner (STEP-05), correcteur.
 * Ne pas dupliquer ces shapes ailleurs dans le repo.
 */
import { z } from "zod";

// ── numeric ──────────────────────────────────────────────────────────────────

export const NumericPayloadSchema = z.object({
  variables: z.record(z.number()).optional(),
  unit: z.string(),
  precision: z.number().int().min(0),
  tolerance: z.object({
    type: z.enum(["abs", "rel"]),
    value: z.number().positive(),
  }),
  sub_answers: z
    .array(
      z.object({
        key: z.string(),
        label: z.string(),
        unit: z.string(),
        precision: z.number().int().min(0),
      })
    )
    .optional(),
});

export const NumericSolutionSchema = z.object({
  value: z.number(),
  sub_values: z.record(z.number()).optional(),
  steps_mdx: z.string(),
  formula_katex: z.string(),
});

const NumericExercise = z.object({
  type: z.literal("numeric"),
  payload: NumericPayloadSchema,
  solution: NumericSolutionSchema,
});

// ── formula_cloze ─────────────────────────────────────────────────────────────

export const FormulaClozePayloadSchema = z.object({
  template_mdx: z.string(),
  blanks: z.array(
    z.object({
      key: z.string(),
      kind: z.enum(["token", "expression", "number"]),
      hint: z.string().optional(),
      options: z.array(z.string()).optional(),
    })
  ),
});

export const FormulaClozeBlankSolutionSchema = z.object({
  accepted: z.array(z.string()),
  canonical: z.string(),
  explain_mdx: z.string(),
});

export const FormulaClozeAnswerSchema = z.object({
  blanks: z.record(FormulaClozeBlankSolutionSchema),
});

const FormulaClozeExercise = z.object({
  type: z.literal("formula_cloze"),
  payload: FormulaClozePayloadSchema,
  solution: FormulaClozeAnswerSchema,
});

// ── excel_model ───────────────────────────────────────────────────────────────

export const ExcelModelPayloadSchema = z.object({
  template_id: z.string(),
  editable_cells: z.array(z.string()),
  given_cells: z.record(z.union([z.string(), z.number()])).optional(),
  check_mode: z.enum(["formula", "value", "both"]),
});

export const ExcelCellSolutionSchema = z.object({
  formula: z.string().optional(),
  value: z.union([z.string(), z.number()]).optional(),
  tolerance: z.number().optional(),
  explain_mdx: z.string().optional(),
});

export const ExcelModelAnswerSchema = z.object({
  cells: z.record(ExcelCellSolutionSchema),
});

const ExcelModelExercise = z.object({
  type: z.literal("excel_model"),
  payload: ExcelModelPayloadSchema,
  solution: ExcelModelAnswerSchema,
});

// ── statement_interactive ─────────────────────────────────────────────────────

export const StatementLineSchema = z.object({
  key: z.string(),
  label: z.string(),
  level: z.number().int().min(0),
  given: z.boolean().optional(),
  editable: z.boolean(),
  formula_hint: z.string().optional(),
  value: z.number().optional(), // shown to user for given=true lines
});

export const StatementInteractivePayloadSchema = z.object({
  statement: z.enum(["is", "bs", "cf"]),
  lines: z.array(StatementLineSchema),
  linked_checks: z
    .array(
      z.object({
        rule: z.enum(["balance", "cf_ties_to_cash", "ni_flows_to_re"]),
      })
    )
    .optional(),
});

export const StatementLineSolutionSchema = z.object({
  value: z.number(),
  tolerance: z.number(),
  derivation_mdx: z.string(),
});

export const StatementInteractiveAnswerSchema = z.object({
  lines: z.record(StatementLineSolutionSchema),
});

const StatementInteractiveExercise = z.object({
  type: z.literal("statement_interactive"),
  payload: StatementInteractivePayloadSchema,
  solution: StatementInteractiveAnswerSchema,
});

// ── graph_fill ────────────────────────────────────────────────────────────────

export const GraphFillPayloadSchema = z.object({
  graph_id: z.string(),
  hidden_node_keys: z.array(z.string()),
  mode: z.enum(["recall", "dragdrop"]),
  distractors: z.array(z.string()).optional(),
});

export const GraphNodeSolutionSchema = z.object({
  accepted_labels: z.array(z.string()),
  explain_mdx: z.string(),
});

export const GraphFillAnswerSchema = z.object({
  nodes: z.record(GraphNodeSolutionSchema),
});

const GraphFillExercise = z.object({
  type: z.literal("graph_fill"),
  payload: GraphFillPayloadSchema,
  solution: GraphFillAnswerSchema,
});

// ── case_structuring ──────────────────────────────────────────────────────────

export const RubricBranchSchema = z.object({
  branch_key: z.string(),
  label: z.string(),
  keywords: z.array(z.string()),
  weight: z.number().min(0).max(1),
  must_have: z.boolean(),
});

export const CaseStructuringPayloadSchema = z.object({
  case_brief_mdx: z.string(),
  expected_branches: z.number().int().positive(),
  time_limit_seconds: z.number().int().positive().optional(),
});

export const CaseStructuringAnswerSchema = z.object({
  rubric: z.array(RubricBranchSchema),
  model_answer_mdx: z.string(),
});

const CaseStructuringExercise = z.object({
  type: z.literal("case_structuring"),
  payload: CaseStructuringPayloadSchema,
  solution: CaseStructuringAnswerSchema,
});

// ── market_sizing ─────────────────────────────────────────────────────────────

export const MarketSizingTreeNodeSchema = z.object({
  key: z.string(),
  label: z.string(),
  value: z.number(),
  unit: z.string(),
});

export const MarketSizingPayloadSchema = z.object({
  question: z.string(),
  allowed_assumptions: z.array(z.string()).optional(),
  unit: z.string(),
});

export const MarketSizingAnswerSchema = z.object({
  tree: z.array(MarketSizingTreeNodeSchema),
  final_value: z.number(),
  acceptable_range: z.tuple([z.number(), z.number()]),
  reasoning_mdx: z.string(),
});

const MarketSizingExercise = z.object({
  type: z.literal("market_sizing"),
  payload: MarketSizingPayloadSchema,
  solution: MarketSizingAnswerSchema,
});

// ── case_math ─────────────────────────────────────────────────────────────────

export const CaseMathPayloadSchema = z.object({
  prompt: z.string(),
  time_limit_seconds: z.number().int().positive(),
  tolerance: z.number().min(0),
});

export const CaseMathAnswerSchema = z.object({
  value: z.number(),
  steps_mdx: z.string(),
});

const CaseMathExercise = z.object({
  type: z.literal("case_math"),
  payload: CaseMathPayloadSchema,
  solution: CaseMathAnswerSchema,
});

// ── mcq ───────────────────────────────────────────────────────────────────────

export const McqOptionSchema = z.object({
  key: z.string(),
  text_mdx: z.string(),
});

export const McqPayloadSchema = z.object({
  options: z.array(McqOptionSchema).min(2),
  multiple: z.boolean(),
  shuffle: z.boolean(),
});

export const McqAnswerSchema = z.object({
  correct_keys: z.array(z.string()).min(1),
  explain_mdx: z.string(),
  distractor_explains: z.record(z.string()),
});

const McqExercise = z.object({
  type: z.literal("mcq"),
  payload: McqPayloadSchema,
  solution: McqAnswerSchema,
});

// ── short_answer ──────────────────────────────────────────────────────────────

export const KeyPointSchema = z.object({
  text: z.string(),
  weight: z.number().min(0).max(1),
});

export const ShortAnswerPayloadSchema = z.object({
  max_words: z.number().int().positive(),
  scoring_mode: z.enum(["auto", "self_eval", "partial"]).optional(),
});

export const ShortAnswerAnswerSchema = z.object({
  key_points: z.array(KeyPointSchema).min(1),
  model_answer_mdx: z.string(),
});

const ShortAnswerExercise = z.object({
  type: z.literal("short_answer"),
  payload: ShortAnswerPayloadSchema,
  solution: ShortAnswerAnswerSchema,
});

// ── numeric_steps ─────────────────────────────────────────────────────────────

export const NumericStepsStepSchema = z.object({
  label: z.string(),
  unit: z.string(),
  tolerance: z.number().min(0),
  hint_mdx: z.string().optional(),
  solution_mdx: z.string(),
  trap_mdx: z.string().optional(),
});

export const NumericStepsPayloadSchema = z.object({
  steps: z.array(NumericStepsStepSchema).min(2).max(6),
});

export const NumericStepsStepSolutionSchema = z.object({
  answer: z.number(),
});

export const NumericStepsSolutionSchema = z.object({
  steps: z.array(NumericStepsStepSolutionSchema),
});

const NumericStepsExercise = z.object({
  type: z.literal("numeric_steps"),
  payload: NumericStepsPayloadSchema,
  solution: NumericStepsSolutionSchema,
});

// ── Union discriminée ─────────────────────────────────────────────────────────

export const ExerciseSchema = z.discriminatedUnion("type", [
  NumericExercise,
  NumericStepsExercise,
  FormulaClozeExercise,
  ExcelModelExercise,
  StatementInteractiveExercise,
  GraphFillExercise,
  CaseStructuringExercise,
  MarketSizingExercise,
  CaseMathExercise,
  McqExercise,
  ShortAnswerExercise,
]);

export type Exercise = z.infer<typeof ExerciseSchema>;
export type NumericExercise = z.infer<typeof NumericExercise>;
export type FormulaClozeExercise = z.infer<typeof FormulaClozeExercise>;
export type ExcelModelExercise = z.infer<typeof ExcelModelExercise>;
export type StatementInteractiveExercise = z.infer<typeof StatementInteractiveExercise>;
export type GraphFillExercise = z.infer<typeof GraphFillExercise>;
export type CaseStructuringExercise = z.infer<typeof CaseStructuringExercise>;
export type MarketSizingExercise = z.infer<typeof MarketSizingExercise>;
export type CaseMathExercise = z.infer<typeof CaseMathExercise>;
export type McqExercise = z.infer<typeof McqExercise>;
export type ShortAnswerExercise = z.infer<typeof ShortAnswerExercise>;
export type NumericStepsExercise = z.infer<typeof NumericStepsExercise>;
