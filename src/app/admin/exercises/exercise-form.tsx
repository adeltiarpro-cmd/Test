"use client";

import { useMemo, useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import type { Route } from "next";
import { ExerciseSchema } from "@prep/schemas";
import { ExerciseRunner } from "@/components/exercise-runner";
import type { SessionExercise } from "@/components/exercise-runner";
import { Callout } from "@/components/ui/callout";
import { EXERCISE_TYPES, exerciseSkeleton, type ExerciseType } from "@/lib/admin/skeleton";
import { saveExercise } from "@/lib/admin/actions";

const TYPE_LABELS: Record<ExerciseType, string> = {
  mcq: "QCM",
  numeric: "Numérique",
  short_answer: "Réponse courte",
  formula_cloze: "Formule à trous",
  case_math: "Math de cas",
  case_structuring: "Structuration de cas",
  market_sizing: "Market sizing",
  statement_interactive: "État financier interactif",
  graph_fill: "Graphe à trous",
  excel_model: "Modèle Excel",
};

// Ces deux types ont besoin de données chargées côté serveur pour s'afficher
const NO_PREVIEW = new Set<ExerciseType>(["graph_fill", "excel_model"]);

export type ModuleOption = { id: string; label: string };

export type ExerciseFormInitial = {
  id: string;
  type: ExerciseType;
  moduleId: string;
  difficulty: number;
  promptMdx: string;
  payload: string;
  solution: string;
  sourceRef: string;
  conceptSlug: string;
};

const field =
  "w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-foreground min-h-[44px] focus:outline-none focus:ring-2 focus:ring-ring";
const label = "text-sm font-medium text-foreground";
const button =
  "inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-semibold min-h-[44px] transition-opacity focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50 disabled:cursor-not-allowed";

function parseJson(text: string): { value: unknown; error: string | null } {
  try {
    return { value: JSON.parse(text), error: null };
  } catch (e) {
    return { value: null, error: e instanceof Error ? e.message : "JSON invalide" };
  }
}

export function ExerciseForm({
  modules,
  initial,
}: {
  modules: ModuleOption[];
  initial?: ExerciseFormInitial;
}) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();

  const firstType: ExerciseType = initial?.type ?? "short_answer";
  const firstSkeleton = useMemo(() => exerciseSkeleton(firstType), [firstType]);

  const [type, setType] = useState<ExerciseType>(firstType);
  const [moduleId, setModuleId] = useState(initial?.moduleId ?? modules[0]?.id ?? "");
  const [difficulty, setDifficulty] = useState(initial?.difficulty ?? 3);
  const [promptMdx, setPromptMdx] = useState(initial?.promptMdx ?? "");
  const [payloadText, setPayloadText] = useState(initial?.payload ?? firstSkeleton.payload);
  const [solutionText, setSolutionText] = useState(initial?.solution ?? firstSkeleton.solution);
  const [sourceRef, setSourceRef] = useState(initial?.sourceRef ?? "");
  const [conceptSlug, setConceptSlug] = useState(initial?.conceptSlug ?? "");
  const [showPreview, setShowPreview] = useState(false);
  const [serverError, setServerError] = useState<string | null>(null);

  const skeleton = useMemo(() => exerciseSkeleton(type), [type]);

  function changeType(next: ExerciseType) {
    setType(next);
    setShowPreview(false);
    // Le changement de type repart du squelette Zod de ce type
    const s = exerciseSkeleton(next);
    setPayloadText(s.payload);
    setSolutionText(s.solution);
  }

  // Validation en direct avec le même schéma que le serveur
  const payload = parseJson(payloadText);
  const solution = parseJson(solutionText);
  const issues: string[] = [];
  if (!promptMdx.trim()) issues.push("L'énoncé est vide.");
  if (!moduleId) issues.push("Aucun module sélectionné.");
  if (payload.error) issues.push(`payload : ${payload.error}`);
  if (solution.error) issues.push(`solution : ${solution.error}`);
  if (!payload.error && !solution.error) {
    const parsed = ExerciseSchema.safeParse({
      type,
      payload: payload.value,
      solution: solution.value,
    });
    if (!parsed.success) {
      for (const issue of parsed.error.issues) {
        issues.push(`${issue.path.join(".") || "(racine)"} : ${issue.message}`);
      }
    }
  }
  const valid = issues.length === 0;

  const previewExercise: SessionExercise | null =
    valid && !NO_PREVIEW.has(type)
      ? {
          id: "apercu",
          type,
          difficulty,
          payload: { prompt_mdx: promptMdx, ...(payload.value as Record<string, unknown>) },
          tags: sourceRef.trim() ? [`ref:${sourceRef.trim()}`] : [],
        }
      : null;

  function submit() {
    if (!valid) return;
    setServerError(null);
    startTransition(async () => {
      const res = await saveExercise({
        id: initial?.id,
        type,
        moduleId,
        difficulty,
        promptMdx,
        payload: payload.value,
        solution: solution.value,
        sourceRef,
        conceptSlug,
      });
      if (res.ok) {
        router.push("/admin/exercises" as Route);
        router.refresh();
      } else {
        setServerError(res.error);
      }
    });
  }

  return (
    <div className="flex flex-col gap-5">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="flex flex-col gap-1">
          <label htmlFor="ex-type" className={label}>Type</label>
          <select
            id="ex-type"
            className={field}
            value={type}
            disabled={!!initial}
            onChange={(e) => changeType(e.target.value as ExerciseType)}
          >
            {EXERCISE_TYPES.map((t) => (
              <option key={t} value={t}>{TYPE_LABELS[t]}</option>
            ))}
          </select>
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="ex-module" className={label}>Module</label>
          <select
            id="ex-module"
            className={field}
            value={moduleId}
            onChange={(e) => setModuleId(e.target.value)}
          >
            {modules.map((m) => (
              <option key={m.id} value={m.id}>{m.label}</option>
            ))}
          </select>
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="ex-difficulty" className={label}>Difficulté (1 à 5)</label>
          <select
            id="ex-difficulty"
            className={field}
            value={difficulty}
            onChange={(e) => setDifficulty(Number(e.target.value))}
          >
            {[1, 2, 3, 4, 5].map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="ex-prompt" className={label}>Énoncé</label>
        <textarea
          id="ex-prompt"
          className={`${field} min-h-[96px]`}
          value={promptMdx}
          onChange={(e) => setPromptMdx(e.target.value)}
          aria-describedby="ex-prompt-hint"
        />
        <p id="ex-prompt-hint" className="text-xs text-muted-foreground">
          Les formules s&apos;écrivent entre deux signes dollar. Évite ce signe pour les montants.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex flex-col gap-1">
          <label htmlFor="ex-payload" className={label}>Payload (JSON)</label>
          <textarea
            id="ex-payload"
            spellCheck={false}
            className={`${field} font-mono min-h-[260px]`}
            value={payloadText}
            onChange={(e) => setPayloadText(e.target.value)}
            aria-invalid={!!payload.error}
          />
          {skeleton.payloadOptional.length > 0 && (
            <p className="text-xs text-muted-foreground">
              Champs optionnels : {skeleton.payloadOptional.join(", ")}
            </p>
          )}
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="ex-solution" className={label}>Solution (JSON)</label>
          <textarea
            id="ex-solution"
            spellCheck={false}
            className={`${field} font-mono min-h-[260px]`}
            value={solutionText}
            onChange={(e) => setSolutionText(e.target.value)}
            aria-invalid={!!solution.error}
          />
          {skeleton.solutionOptional.length > 0 && (
            <p className="text-xs text-muted-foreground">
              Champs optionnels : {skeleton.solutionOptional.join(", ")}
            </p>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex flex-col gap-1">
          <label htmlFor="ex-concept" className={label}>Concept (optionnel)</label>
          <input
            id="ex-concept"
            className={field}
            value={conceptSlug}
            onChange={(e) => setConceptSlug(e.target.value)}
            placeholder="ex. wacc"
          />
          <p className="text-xs text-muted-foreground">
            Sert au suivi de maîtrise. Créé dans le module s&apos;il n&apos;existe pas.
          </p>
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="ex-ref" className={label}>Note de source (optionnel)</label>
          <input
            id="ex-ref"
            className={field}
            value={sourceRef}
            onChange={(e) => setSourceRef(e.target.value)}
            placeholder="ex. Entretien, mars 2026"
          />
        </div>
      </div>

      {issues.length > 0 && (
        <Callout variant="warning" title="À corriger avant de publier">
          <ul className="list-disc pl-5">
            {issues.map((issue, i) => (
              <li key={i}>{issue}</li>
            ))}
          </ul>
        </Callout>
      )}
      {serverError && (
        <Callout variant="error" title="Enregistrement refusé">
          <p>{serverError}</p>
        </Callout>
      )}

      <div className="flex flex-wrap gap-3">
        <button
          type="button"
          className={`${button} border border-border bg-background text-foreground hover:bg-muted`}
          disabled={!valid}
          onClick={() => setShowPreview((v) => !v)}
        >
          {showPreview ? "Masquer l'aperçu" : "Aperçu"}
        </button>
        <button
          type="button"
          className={`${button} bg-primary text-primary-foreground hover:opacity-90`}
          disabled={!valid || pending}
          onClick={submit}
        >
          {pending ? "Enregistrement…" : initial ? "Enregistrer les modifications" : "Publier l'exercice"}
        </button>
      </div>

      {showPreview && valid && (
        <section aria-label="Aperçu de l'exercice" className="flex flex-col gap-2">
          <p className="text-xs text-muted-foreground">
            Aperçu tel que le verra un utilisateur. Rien n&apos;est envoyé ni enregistré.
          </p>
          {previewExercise ? (
            <ExerciseRunner
              key={`${type}-${payloadText.length}-${promptMdx.length}`}
              exercise={previewExercise}
              onNext={() => {}}
              preview
            />
          ) : (
            <Callout variant="info" title="Pas d'aperçu pour ce type">
              <p>
                Ce type s&apos;appuie sur un graphe ou un modèle chargé côté serveur. Il sera
                visible dans une session après publication.
              </p>
            </Callout>
          )}
        </section>
      )}
    </div>
  );
}
