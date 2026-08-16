"use server";

import { evaluate } from "mathjs";
import { createClient } from "@/lib/supabase/server";

export type ExerciseAnswer =
  | { type: "mcq"; selected_keys: string[] }
  | { type: "numeric"; value: number }
  | { type: "formula_cloze"; blanks: Record<string, string> }
  | { type: "short_answer"; text: string };

export type AttemptResult = {
  isCorrect: boolean;
  score: number;
  explanation: string;
  distractorExplains?: Record<string, string>;
  blankFeedback?: Record<string, { correct: boolean; canonical: string; explain: string }>;
};

// ── Formula equivalence (AST-based, server-side only) ────────────────────────

// Known mathjs built-ins that should not be treated as free variables.
const MATH_BUILTINS = new Set([
  "pi", "e", "i", "Infinity", "NaN", "true", "false", "null",
  "sin", "cos", "tan", "asin", "acos", "atan", "atan2",
  "exp", "log", "log2", "log10", "ln", "sqrt", "cbrt", "abs",
  "ceil", "floor", "round", "sign", "min", "max", "pow", "mod",
]);

/** Extract free variable names from a formula string using regex. */
function extractVars(expr: string): string[] {
  const tokens = expr.match(/[a-zA-Z_][a-zA-Z0-9_]*/g) ?? [];
  return [...new Set(tokens.filter((t) => !MATH_BUILTINS.has(t)))];
}

/**
 * Returns true if two formula expressions are algebraically equivalent.
 * Strategy:
 *   1. Quick string check (strip whitespace, lowercase).
 *   2. Monte Carlo numeric evaluation with 3 random variable assignments —
 *      handles commutativity, associativity, and distributivity without
 *      needing a full symbolic algebra engine.
 */
function formulasEquivalent(a: string, b: string): boolean {
  const strip = (s: string) => s.replace(/\s+/g, "").toLowerCase();
  if (strip(a) === strip(b)) return true;

  const vars = [...new Set([...extractVars(a), ...extractVars(b)])];

  for (let trial = 0; trial < 3; trial++) {
    const scope: Record<string, number> = {};
    // Avoid 0 and 1 to catch bugs like x*1 ≡ x; use values in (1, 9).
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

// ── Scorers ───────────────────────────────────────────────────────────────────

function scoreMcq(
  selectedKeys: string[],
  sol: { correct_keys: string[]; explain_mdx: string; distractor_explains: Record<string, string> }
): AttemptResult {
  const correct = [...sol.correct_keys].sort().join(",");
  const given = [...selectedKeys].sort().join(",");
  const isCorrect = given === correct;
  return { isCorrect, score: isCorrect ? 1 : 0, explanation: sol.explain_mdx, distractorExplains: sol.distractor_explains };
}

function scoreNumeric(
  value: number,
  sol: { value: number; steps_mdx: string },
  tolerance: { type: "abs" | "rel"; value: number }
): AttemptResult {
  const diff = Math.abs(value - sol.value);
  const threshold = tolerance.type === "abs"
    ? tolerance.value
    : Math.abs(sol.value) * tolerance.value;
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

  for (const kp of sol.key_points) {
    total += kp.weight;
    const keywords = kp.text.toLowerCase().split(/[\s,;]+/).filter(Boolean);
    if (keywords.every((kw) => lower.includes(kw))) matched += kp.weight;
  }

  const score = total > 0 ? Math.round((matched / total) * 100) / 100 : 0;
  return { isCorrect: score >= 0.7, score, explanation: sol.model_answer_mdx };
}

// ── Main action ───────────────────────────────────────────────────────────────

export async function submitAttempt(
  exerciseId: string,
  answer: ExerciseAnswer,
  timeSpentMs: number
): Promise<AttemptResult> {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();
  if (!user) throw new Error("Not authenticated");

  // Fetch exercise + solution + concepts in one query
  const { data: ex, error } = await supabase
    .from("exercises")
    .select("type, payload, solution, exercise_concepts(concept_id)")
    .eq("id", exerciseId)
    .single();
  if (error || !ex) throw new Error("Exercise not found");

  const pay = ex.payload as Record<string, unknown>;
  const sol = ex.solution as Record<string, unknown>;
  const conceptIds = (ex.exercise_concepts as { concept_id: string }[] | null)
    ?.map((ec) => ec.concept_id) ?? [];

  // Score
  let result: AttemptResult;
  switch (answer.type) {
    case "mcq":
      result = scoreMcq(answer.selected_keys, sol as Parameters<typeof scoreMcq>[1]);
      break;
    case "numeric":
      result = scoreNumeric(
        answer.value,
        sol as Parameters<typeof scoreNumeric>[1],
        pay.tolerance as { type: "abs" | "rel"; value: number }
      );
      break;
    case "formula_cloze":
      result = scoreFormulaCloze(answer.blanks, {
        blanks: sol.blanks as Record<string, { accepted: string[]; canonical: string; explain_mdx: string }>,
      });
      break;
    case "short_answer":
      result = scoreShortAnswer(answer.text, sol as Parameters<typeof scoreShortAnswer>[1]);
      break;
  }

  // Record attempt — strip discriminant `type` before storing as jsonb
  const { type: _, ...answerPayload } = answer;
  await supabase.from("attempts").insert({
    user_id: user.id,
    exercise_id: exerciseId,
    answer: answerPayload as Record<string, unknown>,
    is_correct: result.isCorrect,
    time_spent_ms: timeSpentMs,
  });

  // Upsert review_states with simple SM-2-like scheduling
  const { data: rs } = await supabase
    .from("review_states")
    .select("reps, lapses, stability")
    .eq("user_id", user.id)
    .eq("exercise_id", exerciseId)
    .maybeSingle();

  const reps = (Number(rs?.reps) || 0) + 1;
  const lapses = result.isCorrect ? (Number(rs?.lapses) || 0) : (Number(rs?.lapses) || 0) + 1;
  const stability = result.isCorrect ? Math.min((Number(rs?.stability) || 0) + 1, 30) : 0.5;
  const dueAt = result.isCorrect
    ? new Date(Date.now() + stability * 86_400_000).toISOString()
    : new Date(Date.now() + 600_000).toISOString(); // 10 min

  await supabase.from("review_states").upsert(
    { user_id: user.id, exercise_id: exerciseId, due_at: dueAt, stability, reps, lapses, state: result.isCorrect ? 2 : 3, last_review_at: new Date().toISOString() },
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

    const newScore = Math.round((0.7 * Number(cm?.mastery_score || 0) + 0.3 * result.score) * 10_000) / 10_000;

    await supabase.from("concept_mastery").upsert(
      { user_id: user.id, concept_id: conceptId, mastery_score: newScore, last_updated: new Date().toISOString() },
      { onConflict: "user_id,concept_id" }
    );
  }

  return result;
}
