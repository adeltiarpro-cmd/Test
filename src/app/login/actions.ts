"use server";

import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";

export type LoginState = { error: string } | null;
export type SignupState = { error?: string; success?: boolean } | null;
export type ResetState = { error?: string; success?: boolean } | null;

export async function loginAction(
  _prev: LoginState,
  formData: FormData
): Promise<LoginState> {
  const email = (formData.get("email") as string | null)?.trim() ?? "";
  const password = (formData.get("password") as string | null) ?? "";

  if (!email || !password) {
    return { error: "Email et mot de passe requis." };
  }

  const supabase = await createClient();
  const { error } = await supabase.auth.signInWithPassword({ email, password });

  if (error) {
    return { error: error.message };
  }

  redirect("/session");
}

export async function signupAction(
  _prev: SignupState,
  formData: FormData
): Promise<SignupState> {
  const email = (formData.get("email") as string | null)?.trim() ?? "";
  const password = (formData.get("password") as string | null) ?? "";
  const confirm = (formData.get("confirm") as string | null) ?? "";

  if (!email || !password) return { error: "Email et mot de passe requis." };
  if (password.length < 8) return { error: "Le mot de passe doit contenir au moins 8 caractères." };
  if (password !== confirm) return { error: "Les mots de passe ne correspondent pas." };

  const supabase = await createClient();
  const { error } = await supabase.auth.signUp({ email, password });

  if (error) {
    const msg = error.message ?? "";
    if (msg.toLowerCase().includes("invited") || msg.toLowerCase().includes("access denied")) {
      return { error: "Inscription refusée — votre email ne figure pas sur la liste d'invitation. Contactez l'administrateur." };
    }
    if (msg.toLowerCase().includes("already registered") || msg.toLowerCase().includes("user already")) {
      return { error: "Un compte existe déjà avec cet email. Connectez-vous à la place." };
    }
    return { error: msg || "Erreur lors de l'inscription." };
  }

  return { success: true };
}

export async function resetAction(
  _prev: ResetState,
  formData: FormData
): Promise<ResetState> {
  const email = (formData.get("email") as string | null)?.trim() ?? "";
  if (!email) return { error: "Email requis." };

  const supabase = await createClient();
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "";

  const { error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: siteUrl ? `${siteUrl}/login` : undefined,
  });

  if (error) return { error: error.message };
  return { success: true };
}
