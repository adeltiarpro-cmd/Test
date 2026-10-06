"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { deleteExercise } from "@/lib/admin/actions";

export function DeleteButton({ id }: { id: string }) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  const [confirming, setConfirming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const base =
    "inline-flex items-center rounded-md px-2.5 py-1.5 text-xs font-semibold min-h-[36px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50";

  if (!confirming) {
    return (
      <button
        type="button"
        className={`${base} border border-border text-foreground hover:bg-muted`}
        onClick={() => setConfirming(true)}
      >
        Supprimer
      </button>
    );
  }

  return (
    <span className="inline-flex items-center gap-2">
      <button
        type="button"
        className={`${base} bg-destructive text-destructive-foreground hover:opacity-90`}
        disabled={pending}
        onClick={() =>
          startTransition(async () => {
            const res = await deleteExercise(id);
            if (res.ok) router.refresh();
            else setError(res.error);
          })
        }
      >
        {pending ? "Suppression…" : "Confirmer"}
      </button>
      <button
        type="button"
        className={`${base} border border-border text-foreground hover:bg-muted`}
        onClick={() => setConfirming(false)}
      >
        Annuler
      </button>
      {error && <span className="text-xs text-destructive">{error}</span>}
    </span>
  );
}
