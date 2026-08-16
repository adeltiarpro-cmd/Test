export const valid = {
  type: "statement_interactive",
  payload: {
    statement: "is",
    lines: [
      { key: "revenue",  label: "Chiffre d'affaires", level: 0, given: true,  editable: false },
      { key: "cogs",     label: "Coût des ventes",    level: 1, given: true,  editable: false },
      { key: "gross",    label: "Marge brute",         level: 0, given: false, editable: true, formula_hint: "Revenue − COGS" },
      { key: "ebit",     label: "EBIT",                level: 0, given: false, editable: true },
      { key: "net",      label: "Résultat net",        level: 0, given: false, editable: true },
    ],
    linked_checks: [{ rule: "ni_flows_to_re" }],
  },
  solution: {
    lines: {
      gross: { value: 420,  tolerance: 1, derivation_mdx: "1200 − 780 = 420" },
      ebit:  { value: 300,  tolerance: 1, derivation_mdx: "420 − 120 = 300" },
      net:   { value: 210,  tolerance: 1, derivation_mdx: "300 × (1 − 0.30) = 210" },
    },
  },
};

// Invalid : statement = 'income' n'est pas dans l'enum 'is'|'bs'|'cf'
export const invalid = {
  type: "statement_interactive",
  payload: {
    statement: "income",
    lines: [
      { key: "revenue", label: "Revenue", level: 0, editable: false },
    ],
  },
  solution: {
    lines: {
      revenue: { value: 1200, tolerance: 0, derivation_mdx: "donné" },
    },
  },
};
