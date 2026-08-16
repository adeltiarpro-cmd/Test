export const valid = {
  type: "market_sizing",
  payload: {
    question:
      "Estimez le marché annuel des coffee shops indépendants en France (en nombre de tasses vendues).",
    allowed_assumptions: [
      "Population France : 68 millions",
      "Adultes (18+) : 80 %",
      "Consommateurs de café : 70 % des adultes",
    ],
    unit: "tasses/an",
  },
  solution: {
    tree: [
      { key: "population",     label: "Population France",              value: 68_000_000, unit: "personnes" },
      { key: "adults",         label: "Adultes 18+",                   value: 54_400_000, unit: "personnes" },
      { key: "coffee_drinkers",label: "Buveurs de café",               value: 38_080_000, unit: "personnes" },
      { key: "indie_share",    label: "Part coffee shops indépendants", value: 0.3,        unit: "%" },
      { key: "cups_per_year",  label: "Tasses/an/personne",            value: 120,        unit: "tasses" },
      { key: "total",          label: "Total tasses/an",               value: 1_370_880_000, unit: "tasses" },
    ],
    final_value: 1_370_880_000,
    acceptable_range: [800_000_000, 2_000_000_000],
    reasoning_mdx:
      "68M × 80% adultes × 70% buveurs × 30% indep × 120 tasses/an ≈ **1,37 Mrd tasses/an**",
  },
};

// Invalid : acceptable_range n'est pas un tuple de 2 (un seul élément)
export const invalid = {
  type: "market_sizing",
  payload: {
    question: "Marché des coffee shops en France ?",
    unit: "tasses/an",
  },
  solution: {
    tree: [],
    final_value: 1_000_000,
    acceptable_range: [500_000],
    reasoning_mdx: "...",
  },
};
