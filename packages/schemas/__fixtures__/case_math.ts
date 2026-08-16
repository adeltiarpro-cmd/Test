export const valid = {
  type: "case_math",
  payload: {
    prompt:
      "Une usine produit 2 400 unités/jour sur 250 jours ouvrés. Le prix de vente est 45 €/unité, le coût variable 28 €/unité et les charges fixes annuelles sont 1,2 M€. Calculez le résultat opérationnel annuel.",
    time_limit_seconds: 120,
    tolerance: 500,
  },
  solution: {
    value: 8_820_000,
    steps_mdx:
      "## Résolution\n\n- Volume = 2 400 × 250 = **600 000 unités/an**\n- Marge sur coût variable = 600 000 × (45 − 28) = **10,2 M€**\n- Résultat opérationnel = 10,2 M€ − 1,2 M€ = **9,0 M€**",
  },
};

// Invalid : tolerance = -0.1, viole z.number().min(0)
export const invalid = {
  type: "case_math",
  payload: {
    prompt: "Calculez X.",
    time_limit_seconds: 60,
    tolerance: -0.1,
  },
  solution: {
    value: 42,
    steps_mdx: "...",
  },
};
