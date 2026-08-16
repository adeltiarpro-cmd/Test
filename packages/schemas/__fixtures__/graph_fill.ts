export const valid = {
  type: "graph_fill",
  payload: {
    graph_id: "corp-valuation-umbrex",
    hidden_node_keys: ["wacc", "terminal_value", "ev"],
    mode: "recall",
    distractors: ["EBITDA multiple", "P/E ratio", "Price/Book"],
  },
  solution: {
    nodes: {
      wacc: {
        accepted_labels: ["WACC", "Coût moyen pondéré du capital"],
        explain_mdx: "WACC = ke×E/V + kd×(1−T)×D/V",
      },
      terminal_value: {
        accepted_labels: ["Valeur terminale", "Terminal Value", "TV"],
        explain_mdx: "TV = FCF_n+1 / (WACC − g)",
      },
      ev: {
        accepted_labels: ["Valeur d'entreprise", "Enterprise Value", "EV"],
        explain_mdx: "EV = Σ FCF actualisés + TV actualisée",
      },
    },
  },
};

// Invalid : mode = 'fill' n'est pas dans l'enum 'recall'|'dragdrop'
export const invalid = {
  type: "graph_fill",
  payload: {
    graph_id: "some-graph",
    hidden_node_keys: ["wacc"],
    mode: "fill",
  },
  solution: {
    nodes: {
      wacc: { accepted_labels: ["WACC"], explain_mdx: "..." },
    },
  },
};
