import type { z } from "zod";
import { ExerciseSchema } from "@prep/schemas";

export const EXERCISE_TYPES = [
  "mcq",
  "numeric",
  "short_answer",
  "formula_cloze",
  "case_math",
  "case_structuring",
  "market_sizing",
  "statement_interactive",
  "graph_fill",
  "excel_model",
] as const;

export type ExerciseType = (typeof EXERCISE_TYPES)[number];

type Def = { typeName: string } & Record<string, unknown>;

const defOf = (schema: z.ZodTypeAny) => schema._def as unknown as Def;

/**
 * Construit une valeur d'exemple à partir d'un schéma Zod : les champs
 * obligatoires sont présents, les champs optionnels sont omis. Sert de point
 * de départ au formulaire, sans réécrire à la main les 10 formes.
 */
export function skeletonOf(schema: z.ZodTypeAny): unknown {
  const def = defOf(schema);
  switch (def.typeName) {
    case "ZodString":
      return "";
    case "ZodNumber":
      return 1;
    case "ZodBoolean":
      return false;
    case "ZodLiteral":
      return def.value;
    case "ZodEnum":
      return (def.values as string[])[0];
    case "ZodArray":
      return [skeletonOf(def.type as z.ZodTypeAny)];
    case "ZodTuple":
      return (def.items as z.ZodTypeAny[]).map(skeletonOf);
    case "ZodRecord":
      return { cle: skeletonOf(def.valueType as z.ZodTypeAny) };
    case "ZodObject": {
      const shape = (schema as z.ZodObject<z.ZodRawShape>).shape;
      const out: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(shape)) {
        if (defOf(value as z.ZodTypeAny).typeName === "ZodOptional") continue;
        out[key] = skeletonOf(value as z.ZodTypeAny);
      }
      return out;
    }
    case "ZodOptional":
    case "ZodNullable":
    case "ZodDefault":
      return skeletonOf(def.innerType as z.ZodTypeAny);
    case "ZodUnion":
      return skeletonOf((def.options as z.ZodTypeAny[])[0]);
    case "ZodEffects":
      return skeletonOf(def.schema as z.ZodTypeAny);
    default:
      return null;
  }
}

/** Noms des champs optionnels de premier niveau, affichés en aide sous le champ. */
function optionalKeys(schema: z.ZodTypeAny): string[] {
  if (defOf(schema).typeName !== "ZodObject") return [];
  const shape = (schema as z.ZodObject<z.ZodRawShape>).shape;
  return Object.entries(shape)
    .filter(([, value]) => defOf(value as z.ZodTypeAny).typeName === "ZodOptional")
    .map(([key]) => key);
}

export function exerciseSkeleton(type: ExerciseType) {
  const option = ExerciseSchema.optionsMap.get(type) as
    | z.ZodObject<{ payload: z.ZodTypeAny; solution: z.ZodTypeAny }>
    | undefined;
  if (!option) throw new Error(`Type d'exercice inconnu : ${type}`);
  const { payload, solution } = option.shape;
  return {
    payload: JSON.stringify(skeletonOf(payload), null, 2),
    solution: JSON.stringify(skeletonOf(solution), null, 2),
    payloadOptional: optionalKeys(payload),
    solutionOptional: optionalKeys(solution),
  };
}
