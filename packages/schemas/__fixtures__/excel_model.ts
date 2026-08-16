export const valid = {
  type: "excel_model",
  payload: {
    template_id: "dcf-3-statement",
    editable_cells: ["C5", "C6", "C7", "C10", "C11"],
    given_cells: { B5: 1200, B6: 0.3, B7: 0.08 },
    check_mode: "both",
  },
  solution: {
    cells: {
      C5: {
        formula: "=B5*(1+C4)",
        value: 1272,
        tolerance: 1,
        explain_mdx: "Revenus projetés : base × (1 + g)",
      },
      C10: {
        formula: "=C5-C6-C7",
        value: 814.8,
        tolerance: 0.5,
        explain_mdx: "EBIT = Revenus − COGS − OpEx",
      },
    },
  },
};

// Invalid : check_mode = 'hybrid' n'est pas dans l'enum
export const invalid = {
  type: "excel_model",
  payload: {
    template_id: "dcf-3-statement",
    editable_cells: ["C5"],
    check_mode: "hybrid",
  },
  solution: {
    cells: { C5: { value: 1272 } },
  },
};
