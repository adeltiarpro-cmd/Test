export const valid = {
  type: "numeric",
  payload: {
    variables: { r: 0.05, n: 10, fv: 1000 },
    unit: "EUR",
    precision: 2,
    tolerance: { type: "rel", value: 0.01 },
    sub_answers: [
      { key: "pv", label: "Valeur actuelle", unit: "EUR", precision: 2 },
    ],
  },
  solution: {
    value: 613.91,
    sub_values: { pv: 613.91 },
    steps_mdx:
      "## Résolution\n\nPV = FV / (1 + r)^n = 1000 / (1.05)^10 ≈ **613.91 EUR**",
    formula_katex: "PV = \\frac{FV}{(1+r)^n}",
  },
};

// Invalid : tolerance.type n'est pas dans l'enum 'abs' | 'rel'
export const invalid = {
  type: "numeric",
  payload: {
    unit: "EUR",
    precision: 2,
    tolerance: { type: "absolute", value: 0.5 },
  },
  solution: {
    value: 613.91,
    steps_mdx: "...",
    formula_katex: "PV = FV / (1+r)^n",
  },
};
