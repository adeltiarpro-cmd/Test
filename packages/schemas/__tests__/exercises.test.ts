import { describe, it, expect } from "vitest";
import { ExerciseSchema } from "../exercises";
import * as numeric            from "../__fixtures__/numeric";
import * as formulaCloze       from "../__fixtures__/formula_cloze";
import * as excelModel         from "../__fixtures__/excel_model";
import * as statementInteractive from "../__fixtures__/statement_interactive";
import * as graphFill          from "../__fixtures__/graph_fill";
import * as caseStructuring    from "../__fixtures__/case_structuring";
import * as marketSizing       from "../__fixtures__/market_sizing";
import * as caseMath           from "../__fixtures__/case_math";
import * as mcq                from "../__fixtures__/mcq";
import * as shortAnswer        from "../__fixtures__/short_answer";

const TYPES = [
  { name: "numeric",              fixtures: numeric },
  { name: "formula_cloze",        fixtures: formulaCloze },
  { name: "excel_model",          fixtures: excelModel },
  { name: "statement_interactive",fixtures: statementInteractive },
  { name: "graph_fill",           fixtures: graphFill },
  { name: "case_structuring",     fixtures: caseStructuring },
  { name: "market_sizing",        fixtures: marketSizing },
  { name: "case_math",            fixtures: caseMath },
  { name: "mcq",                  fixtures: mcq },
  { name: "short_answer",         fixtures: shortAnswer },
] as const;

describe("ExerciseSchema", () => {
  describe("valid fixtures — 10/10 doivent passer", () => {
    for (const { name, fixtures } of TYPES) {
      it(`accepte la fixture valide : ${name}`, () => {
        const result = ExerciseSchema.safeParse(fixtures.valid);
        if (!result.success) {
          // Message d'erreur explicite pour faciliter le debug
          console.error(JSON.stringify(result.error.format(), null, 2));
        }
        expect(result.success).toBe(true);
      });
    }
  });

  describe("invalid fixtures — 10/10 doivent être rejetées avec un message clair", () => {
    for (const { name, fixtures } of TYPES) {
      it(`rejette la fixture invalide : ${name}`, () => {
        const result = ExerciseSchema.safeParse(fixtures.invalid);
        expect(result.success).toBe(false);
        if (!result.success) {
          // Vérifie qu'il y a au moins une erreur de validation
          expect(result.error.issues.length).toBeGreaterThan(0);
        }
      });
    }
  });

  describe("discriminateur de type", () => {
    it("rejette un objet sans champ type", () => {
      const result = ExerciseSchema.safeParse({ payload: {}, solution: {} });
      expect(result.success).toBe(false);
    });

    it("rejette un type inconnu", () => {
      const result = ExerciseSchema.safeParse({
        type: "essay",
        payload: {},
        solution: {},
      });
      expect(result.success).toBe(false);
    });
  });
});
