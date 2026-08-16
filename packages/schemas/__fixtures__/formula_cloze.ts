export const valid = {
  type: "formula_cloze",
  payload: {
    template_mdx:
      "Le WACC se calcule comme __[wacc]__ = __[ke]__ × E/V + __[kd]__ × D/V × (1 − T)",
    blanks: [
      { key: "wacc", kind: "token" },
      { key: "ke", kind: "token", hint: "Coût des fonds propres" },
      { key: "kd", kind: "token", hint: "Coût de la dette avant impôt" },
    ],
  },
  solution: {
    blanks: {
      wacc: {
        accepted: ["WACC", "wacc"],
        canonical: "WACC",
        explain_mdx: "WACC = weighted average cost of capital.",
      },
      ke: {
        accepted: ["ke", "Ke", "r_e"],
        canonical: "ke",
        explain_mdx: "ke est le coût des fonds propres (CAPM).",
      },
      kd: {
        accepted: ["kd", "Kd", "r_d"],
        canonical: "kd",
        explain_mdx: "kd est le coût brut de la dette.",
      },
    },
  },
};

// Invalid : blank.kind = 'text' n'est pas dans l'enum 'token'|'expression'|'number'
export const invalid = {
  type: "formula_cloze",
  payload: {
    template_mdx: "PV = __[pv]__",
    blanks: [{ key: "pv", kind: "text" }],
  },
  solution: {
    blanks: {
      pv: { accepted: ["PV"], canonical: "PV", explain_mdx: "..." },
    },
  },
};
