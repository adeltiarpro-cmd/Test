"use client";

import { useState, useActionState } from "react";
import { loginAction, signupAction, resetAction } from "./actions";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Callout } from "@/components/ui/callout";

type View = "login" | "signup" | "reset";

export default function LoginPage() {
  const [view, setView] = useState<View>("login");

  const [loginState, loginDispatch, loginPending] = useActionState(loginAction, null);
  const [signupState, signupDispatch, signupPending] = useActionState(signupAction, null);
  const [resetState, resetDispatch, resetPending] = useActionState(resetAction, null);

  return (
    <main className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="w-full max-w-sm flex flex-col gap-6">
        <header className="text-center">
          <h1 className="text-xl font-semibold text-foreground">Prep Platform</h1>
          <p className="text-sm text-muted-foreground mt-1">Finance · Consulting · GMAT · Maths</p>
        </header>

        {/* Tab switcher — visible on login/signup only */}
        {view !== "reset" && (
          <div className="flex rounded-lg border border-border overflow-hidden">
            <button
              type="button"
              onClick={() => setView("login")}
              className={`flex-1 py-2 text-sm font-medium transition-colors ${
                view === "login"
                  ? "bg-primary text-primary-foreground"
                  : "bg-card text-muted-foreground hover:bg-muted"
              }`}
            >
              Connexion
            </button>
            <button
              type="button"
              onClick={() => setView("signup")}
              className={`flex-1 py-2 text-sm font-medium transition-colors ${
                view === "signup"
                  ? "bg-primary text-primary-foreground"
                  : "bg-card text-muted-foreground hover:bg-muted"
              }`}
            >
              Créer un compte
            </button>
          </div>
        )}

        {/* ── LOGIN ── */}
        {view === "login" && (
          <form action={loginDispatch} className="flex flex-col gap-4">
            <Input
              label="Email"
              name="email"
              type="email"
              autoComplete="email"
              placeholder="vous@exemple.fr"
              required
              disabled={loginPending}
            />
            <Input
              label="Mot de passe"
              name="password"
              type="password"
              autoComplete="current-password"
              placeholder="••••••••"
              required
              disabled={loginPending}
            />

            {loginState?.error && (
              <Callout variant="error">{loginState.error}</Callout>
            )}

            <Button
              type="submit"
              variant="primary"
              size="md"
              className="w-full"
              disabled={loginPending}
            >
              {loginPending ? "Connexion…" : "Se connecter"}
            </Button>

            <button
              type="button"
              onClick={() => setView("reset")}
              className="text-xs text-muted-foreground hover:text-foreground text-center underline-offset-2 hover:underline transition-colors"
            >
              Mot de passe oublié ?
            </button>
          </form>
        )}

        {/* ── SIGNUP ── */}
        {view === "signup" && (
          <>
            {signupState?.success ? (
              <Callout variant="info" title="Vérifiez votre email">
                <p>
                  Un email de confirmation a été envoyé. Cliquez sur le lien
                  pour activer votre compte.
                </p>
              </Callout>
            ) : (
              <form action={signupDispatch} className="flex flex-col gap-4">
                <Input
                  label="Email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder="vous@exemple.fr"
                  required
                  disabled={signupPending}
                />
                <Input
                  label="Mot de passe"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  placeholder="8 caractères minimum"
                  required
                  disabled={signupPending}
                />
                <Input
                  label="Confirmer le mot de passe"
                  name="confirm"
                  type="password"
                  autoComplete="new-password"
                  placeholder="••••••••"
                  required
                  disabled={signupPending}
                />

                {signupState?.error && (
                  <Callout variant="error">{signupState.error}</Callout>
                )}

                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                  className="w-full"
                  disabled={signupPending}
                >
                  {signupPending ? "Création…" : "Créer mon compte"}
                </Button>
              </form>
            )}
          </>
        )}

        {/* ── RESET PASSWORD ── */}
        {view === "reset" && (
          <>
            <div className="text-center">
              <h2 className="text-base font-semibold text-foreground">Réinitialiser le mot de passe</h2>
              <p className="text-sm text-muted-foreground mt-1">
                Entrez votre email — vous recevrez un lien de réinitialisation.
              </p>
            </div>

            {resetState?.success ? (
              <Callout variant="info" title="Email envoyé">
                <p>
                  Si cet email est associé à un compte, un lien de
                  réinitialisation a été envoyé.
                </p>
              </Callout>
            ) : (
              <form action={resetDispatch} className="flex flex-col gap-4">
                <Input
                  label="Email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder="vous@exemple.fr"
                  required
                  disabled={resetPending}
                />

                {resetState?.error && (
                  <Callout variant="error">{resetState.error}</Callout>
                )}

                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                  className="w-full"
                  disabled={resetPending}
                >
                  {resetPending ? "Envoi…" : "Envoyer le lien"}
                </Button>
              </form>
            )}

            <button
              type="button"
              onClick={() => setView("login")}
              className="text-xs text-muted-foreground hover:text-foreground text-center underline-offset-2 hover:underline transition-colors"
            >
              ← Retour à la connexion
            </button>
          </>
        )}
      </div>
    </main>
  );
}
