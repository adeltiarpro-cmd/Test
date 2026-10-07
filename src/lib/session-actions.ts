"use server";

import { evaluate } from "mathjs";
import HyperFormula from "hyperformula";
import { createClient } from "@/lib/supabase/server";
import type { CellResult } from "@/components/model-workshop";
import type { LineResult } from "@/components/statement-interactive";
import { schedule } from "./srs";

export type ExerciseAnswer =
  | { type: "mcq"; selected_keys: string[] }
  | { type: "numeric"; value: number }
  | { type: "numeric_steps"; steps: number[] }
  | { type: "formula_cloze"; blanks: Record<string, string> }
  | { type: "short_answer"; text: string }
  | { type: "graph_fill"; nodes: Record<string, string> }
  | { type: "excel_model"; cells: Record<string, string> }
  | { type: "statement_interactive"; values: Record<string, string> }
  | { type: "case_math"; value: number }
  | { type: "case_structuring"; text: string }
  | { type: "market_sizing"; final_value: number; reasoning?: string };

export type RubricBranchResult = {
  branch_key: string;
  label: string;
  covered: boolean;
  weight: number;
  must_have: boolean;
};

export type PointResult = { text: string; covered: boolean; weight: number };
export type StepResult = {
  isCorrect: boolean;
  correctValue: number;
  solutionMdx: string;
  trapMdx?: string;
};

export type AttemptResult = {
  isCorrect: boolean;
  score: number;
  explanation: string;
  scoringMode?: "auto" | "self_eval" | "partial";
  pointResults?: PointResult[];
  stepResults?: StepResult[];
  distractorExplains?: Record<string, string>;
  blankFeedback?: Record<string, { correct: boolean; canonical: string; explain: string }>;
  cellResults?: Record<string, CellResult>;
  lineResults?: Record<string, LineResult>;
  rubricResults?: RubricBranchResult[];
  isLeech?: boolean;
  prerequisiteConcepts?: { id: string; title: string }[];
};

// ── Formula equivalence (mathjs — for formula_cloze) ─────────────────────────

const MATH_BUILTINS = new Set([
  "pi", "e", "i", "Infinity", "NaN", "true", "false", "null",
  "sin", "cos", "tan", "asin", "acos", "atan", "atan2",
  "exp", "log", "log2", "log10", "ln", "sqrt", "cbrt", "abs",
  "ceil", "floor", "round", "sign", "min", "max", "pow", "mod",
]);

function extractVars(expr: string): string[] {
  const tokens = expr.match(/[a-zA-Z_][a-zA-Z0-9_]*/g) ?? [];
  return [...new Set(tokens.filter((t) => !MATH_BUILTINS.has(t)))];
}

function formulasEquivalent(a: string, b: string): boolean {
  const strip = (s: string) => s.replace(/\s+/g, "").toLowerCase();
  if (strip(a) === strip(b)) return true;
  const vars = [...new Set([...extractVars(a), ...extractVars(b)])];
  for (let trial = 0; trial < 3; trial++) {
    const scope: Record<string, number> = {};
    vars.forEach((v) => { scope[v] = Math.random() * 7 + 1.5; });
    try {
      const rA = Number(evaluate(a, scope));
      const rB = Number(evaluate(b, scope));
      if (!isFinite(rA) || !isFinite(rB)) return false;
      const tol = 1e-9 * Math.max(1, Math.abs(rA));
      if (Math.abs(rA - rB) > tol) return false;
    } catch {
      return false;
    }
  }
  return true;
}

// ── Excel formula equivalence (HyperFormula Monte Carlo) ─────────────────────

// Parse A1 ref to 0-indexed { row, col }
function parseRef(ref: string): { row: number; col: number } {
  const up = ref.toUpperCase().replace(/\$/g, "");
  const colStr = up.match(/^([A-Z]+)/)?.[1] ?? "A";
  const rowStr = up.match(/(\d+)$/)?.[1] ?? "1";
  let col = 0;
  for (const ch of colStr) col = col * 26 + (ch.charCodeAt(0) - 64);
  return { row: parseInt(rowStr) - 1, col: col - 1 };
}

type HFInstance = ReturnType<typeof HyperFormula.buildFromArray>;

/**
 * Returns {row, col, originalValue} for every cell in the template that holds
 * a plain number (not a formula, not an editable cell). These are the
 * "free variables" we perturb to test algebraic equivalence of two formulas.
 */
function findPrimitiveInputs(
  templateData: (string | number | null)[][],
  editableSet: Set<string>
): { row: number; col: number; originalValue: number }[] {
  const result: { row: number; col: number; originalValue: number }[] = [];
  templateData.forEach((row, ri) => {
    row.forEach((cell, ci) => {
      const ref = `${String.fromCharCode(65 + ci)}${ri + 1}`;
      if (!editableSet.has(ref) && typeof cell === "number") {
        result.push({ row: ri, col: ci, originalValue: cell });
      }
    });
  });
  return result;
}

/**
 * Test whether userFormula and expectedFormula are algebraically equivalent by
 * perturbing primitive input cells (3 Monte Carlo trials) and comparing the
 * values HyperFormula computes for each formula at the target cell.
 *
 * Strategy mirrors the mathjs Monte Carlo used for formula_cloze:
 *   - vary the concrete numeric inputs (e.g., Revenue, COGS)
 *   - apply user formula → read value
 *   - apply expected formula → read value
 *   - if the two values agree in all 3 trials → formulas are equivalent
 *
 * Example: =B2+B1 vs =B1+B2 — both produce the same result for any B1, B2.
 * Example: =B1*B2 vs =B1+B2 — differ for most {B1, B2} combinations.
 */
function excelFormulasEquivalent(
  hf: HFInstance,
  ref: string,
  userFormula: string,
  expectedFormula: string,
  primitiveInputs: { row: number; col: number; originalValue: number }[]
): boolean {
  const { row, col } = parseRef(ref);
  let ok = true;

  for (let trial = 0; trial < 3; trial++) {
    // Perturb primitive inputs by a random factor in (0.7, 1.3).
    // Multiplying a negative number (e.g. COGS = -400) keeps its sign.
    for (const ic of primitiveInputs) {
      const factor = 0.7 + Math.random() * 0.6;
      try {
        hf.setCellContents({ sheet: 0, row: ic.row, col: ic.col }, ic.originalValue * factor);
      } catch {}
    }

    try {
      // Evaluate user formula at target cell
      hf.setCellContents({ sheet: 0, row, col }, userFormula);
      const userVal = hf.getCellValue({ sheet: 0, row, col });

      // Evaluate expected formula at same cell
      hf.setCellContents({ sheet: 0, row, col }, expectedFormula);
      const expVal = hf.getCellValue({ sheet: 0, row, col });

      // Restore user formula for subsequent iterations (keeps cascading cells correct)
      hf.setCellContents({ sheet: 0, row, col }, userFormula);

      if (typeof userVal !== "number" || typeof expVal !== "number") { ok = false; break; }
      if (!isFinite(userVal) || !isFinite(expVal)) { ok = false; break; }
      const tol = 1e-9 * Math.max(1, Math.abs(expVal));
      if (Math.abs(userVal - expVal) > tol) { ok = false; break; }
    } catch {
      ok = false;
      break;
    }
  }

  // Restore original input values
  for (const ic of primitiveInputs) {
    try { hf.setCellContents({ sheet: 0, row: ic.row, col: ic.col }, ic.originalValue); } catch {}
  }

  return ok;
}

// ── Scorers ───────────────────────────────────────────────────────────────────

function scoreMcq(
  selectedKeys: string[],
  sol: { correct_keys: string[]; explain_mdx: string; distractor_explains: Record<string, string> }
): AttemptResult {
  const correct = [...sol.correct_keys].sort().join(",");
  const given = [...selectedKeys].sort().join(",");
  const isCorrect = given === correct;
  return {
    isCorrect,
    score: isCorrect ? 1 : 0,
    explanation: sol.explain_mdx,
    distractorExplains: sol.distractor_explains,
  };
}

function scoreNumeric(
  value: number,
  sol: { value: number; steps_mdx: string },
  tolerance: { type: "abs" | "rel"; value: number }
): AttemptResult {
  const diff = Math.abs(value - sol.value);
  const threshold =
    tolerance.type === "abs" ? tolerance.value : Math.abs(sol.value) * tolerance.value;
  const isCorrect = diff <= threshold;
  return { isCorrect, score: isCorrect ? 1 : 0, explanation: sol.steps_mdx };
}

function scoreFormulaCloze(
  blanks: Record<string, string>,
  sol: { blanks: Record<string, { accepted: string[]; canonical: string; explain_mdx: string }> }
): AttemptResult {
  const feedback: Record<string, { correct: boolean; canonical: string; explain: string }> = {};
  let hit = 0;
  const total = Object.keys(sol.blanks).length;
  for (const [key, blankSol] of Object.entries(sol.blanks)) {
    const userInput = (blanks[key] ?? "").trim();
    const candidates = [...blankSol.accepted, blankSol.canonical];
    const ok = candidates.some((c) => formulasEquivalent(userInput, c));
    feedback[key] = { correct: ok, canonical: blankSol.canonical, explain: blankSol.explain_mdx };
    if (ok) hit++;
  }
  const score = total > 0 ? hit / total : 0;
  return {
    isCorrect: score === 1,
    score,
    explanation: Object.values(feedback).map((f) => f.explain).join("\n\n"),
    blankFeedback: feedback,
  };
}

function scoreShortAnswer(
  text: string,
  sol: { key_points: { text: string; weight: number }[]; model_answer_mdx: string }
): AttemptResult {
  const lower = text.toLowerCase();
  let total = 0;
  let matched = 0;
  const pointResults: PointResult[] = [];
  for (const kp of sol.key_points) {
    total += kp.weight;
    const keywords = kp.text.toLowerCase().split(/[\s,;]+/).filter(Boolean);
    const covered = keywords.every((kw) => lower.includes(kw));
    if (covered) matched += kp.weight;
    pointResults.push({ text: kp.text, covered, weight: kp.weight });
  }
  const score = total > 0 ? Math.round((matched / total) * 100) / 100 : 0;
  return { isCorrect: score >= 0.7, score, explanation: sol.model_answer_mdx, pointResults };
}

function scoreGraphFill(
  nodes: Record<string, string>,
  sol: { nodes: Record<string, { accepted_labels: string[]; explain_mdx: string }> }
): AttemptResult {
  let hit = 0;
  const total = Object.keys(sol.nodes).length;
  const explanations: string[] = [];
  for (const [key, nodeSol] of Object.entries(sol.nodes)) {
    const userLabel = (nodes[key] ?? "").trim().toLowerCase();
    const ok = nodeSol.accepted_labels.some((a) => a.toLowerCase() === userLabel);
    if (ok) hit++;
    else explanations.push(nodeSol.explain_mdx);
  }
  const score = total > 0 ? hit / total : 0;
  return {
    isCorrect: score === 1,
    score,
    explanation:
      explanations.length > 0
        ? explanations.join("\n\n")
        : "Tous les nœuds sont corrects.",
  };
}

async function scoreExcelModel(
  userCells: Record<string, string>,
  sol: { cells: Record<string, { formula?: string; value?: number | string; tolerance?: number; explain_mdx?: string }> },
  pay: { template_id: string; editable_cells: string[]; given_cells?: Record<string, string | number>; check_mode: "value" | "formula" | "both" }
): Promise<AttemptResult> {
  // Fetch template to reconstruct HyperFormula sheet for value scoring
  const supabase = await createClient();
  const { data: tmpl } = await supabase
    .from("model_templates")
    .select("sheet")
    .eq("id", pay.template_id)
    .single();

  const sheet = tmpl?.sheet as { cols: string[]; data: (string | number | null)[][] } | null;

  const editableSet = new Set(pay.editable_cells);
  let hf: HFInstance | null = null;
  let primitiveInputs: ReturnType<typeof findPrimitiveInputs> = [];

  if (sheet) {
    const data = sheet.data.map((row) =>
      row.map((cell) => (cell === null ? "" : cell))
    ) as (string | number)[][];

    primitiveInputs = findPrimitiveInputs(sheet.data, editableSet);

    // Clear editable cells (start empty)
    for (const ref of pay.editable_cells) {
      const { row, col } = parseRef(ref);
      if (data[row]) data[row][col] = "";
    }
    if (pay.given_cells) {
      for (const [ref, val] of Object.entries(pay.given_cells)) {
        const { row, col } = parseRef(ref);
        if (data[row]) data[row][col] = val;
      }
    }
    hf = HyperFormula.buildFromArray(data, { licenseKey: "gpl-v3" });
  }

  const cellResults: Record<string, CellResult> = {};
  let hit = 0;
  const total = Object.keys(sol.cells).length;

  for (const [ref, solCell] of Object.entries(sol.cells)) {
    const userFormula = (userCells[ref] ?? "").trim();
    const tolerance = solCell.tolerance ?? 1;
    const checkMode = pay.check_mode;

    let valueCorrect = false;
    let formulaCorrect: boolean | null = null;

    if (hf) {
      // Apply user formula and read computed value
      const { row, col } = parseRef(ref);
      const cellValue = userFormula.startsWith("=")
        ? userFormula
        : userFormula === ""
        ? null
        : isNaN(Number(userFormula))
        ? userFormula
        : Number(userFormula);
      try {
        hf.setCellContents({ sheet: 0, row, col }, cellValue);
      } catch {}

      const computed = hf.getCellValue({ sheet: 0, row, col });
      const computedNum =
        typeof computed === "number" ? computed : parseFloat(String(computed ?? ""));
      const expectedNum =
        typeof solCell.value === "number"
          ? solCell.value
          : parseFloat(String(solCell.value ?? ""));

      valueCorrect =
        !isNaN(computedNum) && !isNaN(expectedNum) && Math.abs(computedNum - expectedNum) <= tolerance;
    } else {
      // No template — fall back to raw value comparison
      const userNum = parseFloat(userFormula);
      const expectedNum =
        typeof solCell.value === "number"
          ? solCell.value
          : parseFloat(String(solCell.value ?? ""));
      valueCorrect =
        !isNaN(userNum) && !isNaN(expectedNum) && Math.abs(userNum - expectedNum) <= tolerance;
    }

    // Formula equivalence — HyperFormula Monte Carlo (same strategy as mathjs for formula_cloze).
    // Quick string check first (fast path); Monte Carlo only when strings differ.
    if ((checkMode === "formula" || checkMode === "both") && solCell.formula && hf) {
      const normalUser = userFormula.trim().toUpperCase().replace(/\s+/g, "").replace(/\$/g, "");
      const normalExpected = solCell.formula.trim().toUpperCase().replace(/\s+/g, "").replace(/\$/g, "");
      if (normalUser === normalExpected) {
        formulaCorrect = true;
      } else {
        formulaCorrect = excelFormulasEquivalent(hf, ref, userFormula, solCell.formula, primitiveInputs);
      }
    } else if ((checkMode === "formula" || checkMode === "both") && solCell.formula && !hf) {
      // No HF instance — fall back to string check only
      const normalUser = userFormula.trim().toUpperCase().replace(/\s+/g, "").replace(/\$/g, "");
      const normalExpected = solCell.formula.trim().toUpperCase().replace(/\s+/g, "").replace(/\$/g, "");
      formulaCorrect = normalUser === normalExpected;
    }

    const cellCorrect =
      checkMode === "value"
        ? valueCorrect
        : checkMode === "formula"
        ? (formulaCorrect ?? false)
        : valueCorrect && formulaCorrect !== false;

    if (cellCorrect) hit++;
    cellResults[ref] = {
      valueCorrect,
      formulaCorrect,
      explain_mdx: solCell.explain_mdx ?? "",
    };
  }

  if (hf) hf.destroy();

  const score = total > 0 ? hit / total : 0;
  return {
    isCorrect: score === 1,
    score,
    explanation:
      score === 1
        ? "Toutes les cellules sont correctes."
        : `${hit} / ${total} cellules correctes.`,
    cellResults,
  };
}

function scoreStatementInteractive(
  userValues: Record<string, string>,
  sol: { lines: Record<string, { value: number; tolerance: number; derivation_mdx: string }> }
): AttemptResult {
  const lineResults: Record<string, LineResult> = {};
  let hit = 0;
  let total = 0;

  for (const [key, lineSol] of Object.entries(sol.lines)) {
    if (!(key in userValues)) continue; // given or not submitted → skip
    total++;
    const userNum = parseFloat(
      (userValues[key] ?? "").replace(",", ".")
    );
    const correct =
      !isNaN(userNum) && Math.abs(userNum - lineSol.value) <= lineSol.tolerance;
    if (correct) hit++;
    lineResults[key] = { correct, explain_mdx: lineSol.derivation_mdx };
  }

  const score = total > 0 ? hit / total : 0;
  return {
    isCorrect: score === 1,
    score,
    explanation:
      score === 1
        ? "Toutes les lignes sont correctes."
        : `${hit} / ${total} lignes correctes.`,
    lineResults,
  };
}

function scoreCaseMath(
  value: number,
  sol: { value: number; steps_mdx: string },
  tolerance: number
): AttemptResult {
  const isCorrect = Math.abs(value - sol.value) <= tolerance;
  return { isCorrect, score: isCorrect ? 1 : 0, explanation: sol.steps_mdx };
}

function scoreCaseStructuring(
  text: string,
  sol: {
    rubric: Array<{ branch_key: string; label: string; keywords: string[]; weight: number; must_have: boolean }>;
    model_answer_mdx: string;
  }
): AttemptResult {
  const lower = text.toLowerCase();
  const rubricResults: RubricBranchResult[] = [];
  let totalWeight = 0;
  let coveredWeight = 0;
  let allMustHaveCovered = true;

  for (const branch of sol.rubric) {
    const covered = branch.keywords.every((kw) => lower.includes(kw.toLowerCase()));
    rubricResults.push({
      branch_key: branch.branch_key,
      label: branch.label,
      covered,
      weight: branch.weight,
      must_have: branch.must_have,
    });
    totalWeight += branch.weight;
    if (covered) coveredWeight += branch.weight;
    if (branch.must_have && !covered) allMustHaveCovered = false;
  }

  const score = totalWeight > 0 ? Math.round((coveredWeight / totalWeight) * 100) / 100 : 0;
  const isCorrect = score >= 0.7 && allMustHaveCovered;

  return {
    isCorrect,
    score,
    explanation: sol.model_answer_mdx,
    rubricResults,
  };
}

function scoreMarketSizing(
  finalValue: number,
  sol: { final_value: number; acceptable_range: [number, number]; reasoning_mdx: string }
): AttemptResult {
  const [lo, hi] = sol.acceptable_range;
  const inRange = finalValue >= lo && finalValue <= hi;
  return {
    isCorrect: inRange,
    score: inRange ? 1 : 0,
    explanation: sol.reasoning_mdx,
  };
}

function scoreNumericSteps(
  userSteps: number[],
  pay: {
    steps: Array<{
      label: string;
      unit: string;
      tolerance: number;
      hint_mdx?: string;
      solution_mdx: string;
      trap_mdx?: string;
    }>;
  },
  sol: { steps: Array<{ answer: number }> }
): AttemptResult {
  let correct = 0;
  const stepResults: StepResult[] = [];

  for (let i = 0; i < sol.steps.length; i++) {
    const expected = sol.steps[i].answer;
    const given = userSteps[i] ?? NaN;
    const tol = pay.steps[i]?.tolerance ?? 0;
    const isCorrect = isFinite(given) && Math.abs(given - expected) <= Math.max(tol, Math.abs(expected) * 1e-9);
    if (isCorrect) correct++;
    stepResults.push({
      isCorrect,
      correctValue: expected,
      solutionMdx: pay.steps[i]?.solution_mdx ?? "",
      trapMdx: pay.steps[i]?.trap_mdx,
    });
  }

  const total = sol.steps.length;
  const score = total > 0 ? Math.round((correct / total) * 100) / 100 : 0;
  const allSolutions = pay.steps.map((s) => s.solution_mdx).join("\n\n");
  return { isCorrect: score >= 0.7, score, explanation: allSolutions, stepResults };
}

// ── Main action ───────────────────────────────────────────────────────────────

export async function submitAttempt(
  exerciseId: string,
  answer: ExerciseAnswer,
  timeSpentMs: number,
  confidence: 1 | 2 | 3 = 2,
  selfEvalRating?: 1 | 2 | 3
): Promise<AttemptResult> {
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) throw new Error("Not authenticated");

  const { data: ex, error } = await supabase
    .from("exercises")
    .select("type, payload, solution, exercise_concepts(concept_id)")
    .eq("id", exerciseId)
    .single();
  if (error || !ex) throw new Error("Exercise not found");

  const pay = ex.payload as Record<string, unknown>;
  const sol = ex.solution as Record<string, unknown>;
  const conceptIds =
    (ex.exercise_concepts as { concept_id: string }[] | null)?.map((ec) => ec.concept_id) ?? [];

  let result: AttemptResult;
  switch (answer.type) {
    case "mcq":
      result = scoreMcq(
        answer.selected_keys,
        sol as Parameters<typeof scoreMcq>[1]
      );
      break;
    case "numeric":
      result = scoreNumeric(
        answer.value,
        sol as Parameters<typeof scoreNumeric>[1],
        pay.tolerance as { type: "abs" | "rel"; value: number }
      );
      break;
    case "numeric_steps":
      result = scoreNumericSteps(
        answer.steps,
        pay as Parameters<typeof scoreNumericSteps>[1],
        sol as Parameters<typeof scoreNumericSteps>[2]
      );
      break;
    case "formula_cloze":
      result = scoreFormulaCloze(answer.blanks, {
        blanks: sol.blanks as Record<
          string,
          { accepted: string[]; canonical: string; explain_mdx: string }
        >,
      });
      break;
    case "short_answer": {
      const scoringMode = (pay.scoring_mode as string | undefined) ?? "auto";
      if (scoringMode === "self_eval" && selfEvalRating !== undefined) {
        result = {
          isCorrect: selfEvalRating >= 2,
          score: selfEvalRating >= 2 ? 1 : 0,
          explanation: (sol.model_answer_mdx as string) ?? "",
          scoringMode: "self_eval",
        };
      } else {
        result = scoreShortAnswer(answer.text, sol as Parameters<typeof scoreShortAnswer>[1]);
        result.scoringMode = scoringMode as "auto" | "partial";
      }
      break;
    }
    case "graph_fill":
      result = scoreGraphFill(answer.nodes, {
        nodes: sol.nodes as Record<
          string,
          { accepted_labels: string[]; explain_mdx: string }
        >,
      });
      break;
    case "excel_model":
      result = await scoreExcelModel(answer.cells, { cells: sol.cells as Parameters<typeof scoreExcelModel>[1]["cells"] }, {
        template_id: pay.template_id as string,
        editable_cells: pay.editable_cells as string[],
        given_cells: pay.given_cells as Record<string, string | number> | undefined,
        check_mode: pay.check_mode as "value" | "formula" | "both",
      });
      break;
    case "statement_interactive":
      result = scoreStatementInteractive(answer.values, {
        lines: sol.lines as Record<
          string,
          { value: number; tolerance: number; derivation_mdx: string }
        >,
      });
      break;
    case "case_math":
      result = scoreCaseMath(
        answer.value,
        sol as Parameters<typeof scoreCaseMath>[1],
        pay.tolerance as number
      );
      break;
    case "case_structuring":
      result = scoreCaseStructuring(answer.text, {
        rubric: sol.rubric as Parameters<typeof scoreCaseStructuring>[1]["rubric"],
        model_answer_mdx: sol.model_answer_mdx as string,
      });
      break;
    case "market_sizing":
      result = scoreMarketSizing(answer.final_value, {
        final_value: sol.final_value as number,
        acceptable_range: sol.acceptable_range as [number, number],
        reasoning_mdx: sol.reasoning_mdx as string,
      });
      break;
  }

  // Record attempt
  const { type: _, ...answerPayload } = answer;
  await supabase.from("attempts").insert({
    user_id: user.id,
    exercise_id: exerciseId,
    answer: answerPayload as Record<string, unknown>,
    is_correct: result.isCorrect,
    time_spent_ms: timeSpentMs,
    confidence,
  });

  // Upsert review_states — SM-2 with confidence rating
  const { data: rs } = await supabase
    .from("review_states")
    .select("reps, lapses, stability, difficulty_fsrs, state")
    .eq("user_id", user.id)
    .eq("exercise_id", exerciseId)
    .maybeSingle();

  const srs = schedule(
    {
      reps: Number(rs?.reps) || 0,
      lapses: Number(rs?.lapses) || 0,
      stability: Number(rs?.stability) || 0,
      difficulty_fsrs: Number(rs?.difficulty_fsrs) || 0.3,
      state: Number(rs?.state) || 0,
    },
    result.isCorrect,
    confidence
  );

  await supabase.from("review_states").upsert(
    {
      user_id: user.id,
      exercise_id: exerciseId,
      due_at: srs.dueAt.toISOString(),
      stability: srs.stability,
      difficulty_fsrs: srs.difficulty_fsrs,
      reps: srs.reps,
      lapses: srs.lapses,
      state: srs.state,
      last_review_at: new Date().toISOString(),
    },
    { onConflict: "user_id,exercise_id" }
  );

  // Weighted-moving-average concept mastery
  for (const conceptId of conceptIds) {
    const { data: cm } = await supabase
      .from("concept_mastery")
      .select("mastery_score")
      .eq("user_id", user.id)
      .eq("concept_id", conceptId)
      .maybeSingle();

    const newScore =
      Math.round((0.7 * Number(cm?.mastery_score || 0) + 0.3 * result.score) * 10_000) / 10_000;

    await supabase.from("concept_mastery").upsert(
      {
        user_id: user.id,
        concept_id: conceptId,
        mastery_score: newScore,
        last_updated: new Date().toISOString(),
      },
      { onConflict: "user_id,concept_id" }
    );
  }

  // Leech detection: 4+ lapses → show prerequisite suggestion
  if (srs.lapses > 3) {
    result.isLeech = true;
    if (conceptIds.length > 0) {
      const { data: edges } = await supabase
        .from("concept_edges")
        .select("source_id")
        .in("target_id", conceptIds)
        .eq("kind", "prerequisite");
      const prereqIds = (edges ?? []).map((e) => e.source_id as string);
      if (prereqIds.length > 0) {
        const { data: prereqConcepts } = await supabase
          .from("concepts")
          .select("id, title")
          .in("id", prereqIds);
        result.prerequisiteConcepts = (prereqConcepts ?? []) as { id: string; title: string }[];
      }
    }
  }

  return result;
}

// ── Self-eval helpers ─────────────────────────────────────────────────────────

/** Returns the model answer for a self_eval short_answer — called after user has written their answer. */
export async function peekSelfEvalAnswer(
  exerciseId: string
): Promise<{ model_answer_mdx: string }> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) throw new Error("Not authenticated");

  const { data: ex } = await supabase
    .from("exercises")
    .select("solution")
    .eq("id", exerciseId)
    .single();

  const sol = ex?.solution as Record<string, unknown> | null;
  return { model_answer_mdx: (sol?.model_answer_mdx as string) ?? "" };
}

/** Override the last attempt to correct — for partial scoring "ma réponse était juste". */
export async function overrideToCorrect(exerciseId: string): Promise<void> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) throw new Error("Not authenticated");

  const { data: ex } = await supabase
    .from("exercises")
    .select("exercise_concepts(concept_id)")
    .eq("id", exerciseId)
    .single();
  const conceptIds =
    (ex?.exercise_concepts as { concept_id: string }[] | null)?.map((ec) => ec.concept_id) ?? [];

  const { data: rs } = await supabase
    .from("review_states")
    .select("reps, lapses, stability, difficulty_fsrs, state")
    .eq("user_id", user.id)
    .eq("exercise_id", exerciseId)
    .maybeSingle();

  const srs = schedule(
    {
      reps: Number(rs?.reps) || 0,
      lapses: Number(rs?.lapses) || 0,
      stability: Number(rs?.stability) || 0,
      difficulty_fsrs: Number(rs?.difficulty_fsrs) || 0.3,
      state: Number(rs?.state) || 0,
    },
    true,
    2
  );

  await supabase.from("review_states").upsert(
    {
      user_id: user.id,
      exercise_id: exerciseId,
      due_at: srs.dueAt.toISOString(),
      stability: srs.stability,
      difficulty_fsrs: srs.difficulty_fsrs,
      reps: srs.reps,
      lapses: srs.lapses,
      state: srs.state,
      last_review_at: new Date().toISOString(),
    },
    { onConflict: "user_id,exercise_id" }
  );

  for (const conceptId of conceptIds) {
    const { data: cm } = await supabase
      .from("concept_mastery")
      .select("mastery_score")
      .eq("user_id", user.id)
      .eq("concept_id", conceptId)
      .maybeSingle();
    const newScore =
      Math.round((0.7 * Number(cm?.mastery_score || 0) + 0.3 * 1) * 10_000) / 10_000;
    await supabase.from("concept_mastery").upsert(
      {
        user_id: user.id,
        concept_id: conceptId,
        mastery_score: newScore,
        last_updated: new Date().toISOString(),
      },
      { onConflict: "user_id,concept_id" }
    );
  }
}
