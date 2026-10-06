import { createClient as createSupabaseClient } from "@supabase/supabase-js";

/**
 * Client service_role : contourne la RLS. À n'utiliser que dans du code serveur
 * (server actions, route handlers), jamais dans un composant client.
 */
export function createAdminClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    throw new Error("NEXT_PUBLIC_SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY sont requis côté serveur");
  }
  return createSupabaseClient(url, key, { auth: { persistSession: false } });
}
