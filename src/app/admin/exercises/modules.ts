import { createClient } from "@/lib/supabase/server";
import type { ModuleOption } from "./exercise-form";

type Row = {
  id: string;
  title: string;
  parent_id: string | null;
  tracks: { title: string } | null;
};

/** Modules proposés au formulaire, libellés « Filière · Chapitre · Sous-chapitre ». */
export async function fetchModuleOptions(): Promise<ModuleOption[]> {
  const supabase = await createClient();
  const { data } = await supabase.from("modules").select("id, title, parent_id, tracks(title)");
  const rows = (data ?? []) as unknown as Row[];
  const titles = new Map(rows.map((r) => [r.id, r.title]));
  return rows
    .map((r) => ({
      id: r.id,
      label: [r.tracks?.title, r.parent_id ? titles.get(r.parent_id) : null, r.title]
        .filter(Boolean)
        .join(" · "),
    }))
    .sort((a, b) => a.label.localeCompare(b.label));
}
