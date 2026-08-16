/**
 * Page de connexion minimale — STEP-05 uniquement.
 * Permet de tester /session avec un compte Supabase existant.
 * STEP-10 remplacera cette page par la version complète (signup,
 * invitations, reset password, validation côté client, etc.).
 */
"use client";

import { useActionState } from "react";
import { loginAction } from "./actions";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Callout } from "@/components/ui/callout";

export default function LoginPage() {
  const [state, action, isPending] = useActionState(loginAction, null);

  return (
    <main className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="w-full max-w-sm flex flex-col gap-6">
        <header className="text-center">
          <h1 className="text-xl font-semibold text-foreground">Connexion</h1>
          <p className="text-sm text-muted-foreground mt-1">Prep Platform</p>
        </header>

        <form action={action} className="flex flex-col gap-4">
          <Input
            label="Email"
            name="email"
            type="email"
            autoComplete="email"
            placeholder="vous@exemple.fr"
            required
            disabled={isPending}
          />
          <Input
            label="Mot de passe"
            name="password"
            type="password"
            autoComplete="current-password"
            placeholder="••••••••"
            required
            disabled={isPending}
          />

          {state?.error && (
            <Callout variant="error">{state.error}</Callout>
          )}

          <Button
            type="submit"
            variant="primary"
            size="md"
            className="w-full"
            disabled={isPending}
          >
            {isPending ? "Connexion…" : "Se connecter"}
          </Button>
        </form>
      </div>
    </main>
  );
}
