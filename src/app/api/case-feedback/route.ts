import { NextRequest, NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@/lib/supabase/server";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

export async function POST(req: NextRequest) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

  const { exercise_id, user_text, exercise_type } = (await req.json()) as {
    exercise_id: string;
    user_text: string;
    exercise_type: "case_structuring" | "market_sizing";
  };

  const { data: ex } = await supabase
    .from("exercises")
    .select("solution, payload")
    .eq("id", exercise_id)
    .single();

  if (!ex) return NextResponse.json({ error: "Exercise not found" }, { status: 404 });

  const sol = ex.solution as Record<string, unknown>;
  const pay = ex.payload as Record<string, unknown>;

  let systemPrompt: string;
  let userPrompt: string;

  if (exercise_type === "case_structuring") {
    const rubric = sol.rubric as Array<{ label: string; keywords: string[]; weight: number; must_have: boolean }>;
    const modelAnswer = (sol.model_answer_mdx as string) ?? "";

    systemPrompt =
      "Tu es un expert en case interview (McKinsey, BCG, Bain). " +
      "Donne un feedback qualitatif concis (3–4 phrases) sur la structuration : " +
      "MECE, priorisation, exhaustivité, hypothèses implicites. " +
      "Cite des forces ET des lacunes spécifiques.";

    userPrompt =
      `Axes attendus : ${rubric.map((b) => b.label).join(" / ")}\n` +
      `Réponse modèle : ${modelAnswer}\n\n` +
      `Réponse de l'apprenant :\n${user_text}`;
  } else {
    const reasoningMdx = (sol.reasoning_mdx as string) ?? "";
    const range = sol.acceptable_range as [number, number];
    const unit = (pay.unit as string) ?? "";

    systemPrompt =
      "Tu es un expert en case interview (McKinsey, BCG, Bain). " +
      "Donne un feedback qualitatif concis (3–4 phrases) sur le market sizing : " +
      "logique de décomposition, hypothèses, ordre de grandeur, cohérence. " +
      "Cite des forces ET des lacunes spécifiques.";

    userPrompt =
      `Fourchette cible : ${range[0]}–${range[1]} ${unit}\n` +
      `Approche de référence : ${reasoningMdx}\n\n` +
      `Raisonnement de l'apprenant :\n${user_text}`;
  }

  try {
    const message = await anthropic.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 400,
      system: systemPrompt,
      messages: [{ role: "user", content: userPrompt }],
    });

    const feedback = (message.content[0] as { type: "text"; text: string }).text;
    return NextResponse.json({ feedback });
  } catch (err) {
    console.error("Anthropic API error:", err);
    return NextResponse.json({ error: "LLM unavailable" }, { status: 503 });
  }
}
