"use server";

import { createClient } from "@/lib/supabase/server";

export type ModelTemplateSheet = {
  cols: string[];
  data: (string | number | null)[][];
};

export type ModelTemplate = {
  id: string;
  title: string;
  description: string | null;
  sheet: ModelTemplateSheet;
};

export async function fetchModelTemplate(templateId: string): Promise<ModelTemplate | null> {
  const supabase = await createClient();
  const { data } = await supabase
    .from("model_templates")
    .select("id, title, description, sheet")
    .eq("id", templateId)
    .single();
  return data as ModelTemplate | null;
}
