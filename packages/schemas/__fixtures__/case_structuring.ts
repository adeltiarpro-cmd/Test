export const valid = {
  type: "case_structuring",
  payload: {
    case_brief_mdx:
      "## Cas : MediCorp\n\nMediCorp, fabricant de dispositifs médicaux, voit ses marges baisser de 5 pts en 3 ans. Le directeur vous demande de diagnostiquer la situation et de proposer un plan d'action.",
    expected_branches: 3,
    time_limit_seconds: 180,
  },
  solution: {
    rubric: [
      {
        branch_key: "profitability",
        label: "Analyse de la rentabilité",
        keywords: ["marges", "revenus", "coûts", "EBITDA"],
        weight: 0.4,
        must_have: true,
      },
      {
        branch_key: "market",
        label: "Analyse du marché",
        keywords: ["concurrence", "part de marché", "pricing"],
        weight: 0.35,
        must_have: false,
      },
      {
        branch_key: "operations",
        label: "Efficience opérationnelle",
        keywords: ["supply chain", "R&D", "lean"],
        weight: 0.25,
        must_have: false,
      },
    ],
    model_answer_mdx:
      "**Structure recommandée :**\n1. Profitability (why margins down?)\n2. Market (competition, pricing pressure?)\n3. Operations (cost drivers?)",
  },
};

// Invalid : expected_branches = -1, viole z.number().int().positive()
export const invalid = {
  type: "case_structuring",
  payload: {
    case_brief_mdx: "Cas test",
    expected_branches: -1,
  },
  solution: {
    rubric: [],
    model_answer_mdx: "...",
  },
};
