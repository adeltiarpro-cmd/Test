import { createClient } from "@/lib/supabase/server";

/** Renvoie l'utilisateur courant s'il est admin (profiles.is_admin = true), sinon null. */
export async function getAdminUser() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) return null;

  const { data } = await supabase
    .from("profiles")
    .select("is_admin")
    .eq("id", user.id)
    .maybeSingle();

  return data?.is_admin === true ? user : null;
}
