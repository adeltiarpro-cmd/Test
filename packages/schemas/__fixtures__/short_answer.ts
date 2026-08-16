export const valid = {
  type: "short_answer",
  payload: {
    max_words: 120,
  },
  solution: {
    key_points: [
      { text: "Le DCF actualise les free cash flows futurs au WACC", weight: 0.4 },
      { text: "La valeur terminale représente la valeur au-delà de l'horizon explicite", weight: 0.35 },
      { text: "L'EV est obtenu en additionnant FCF actualisés + TV actualisée ; on déduit la dette nette pour obtenir la valeur des fonds propres", weight: 0.25 },
    ],
    model_answer_mdx:
      "Un DCF valorise une entreprise en actualisant ses **free cash flows** futurs sur un horizon explicite (5−10 ans) au **WACC**, puis en ajoutant une **valeur terminale** (Gordon-Shapiro ou multiple de sortie). La somme donne l'**EV** ; on déduit la dette nette pour obtenir la valeur des fonds propres.",
  },
};

// Invalid : key_points = [] viole .min(1)
export const invalid = {
  type: "short_answer",
  payload: {
    max_words: 100,
  },
  solution: {
    key_points: [],
    model_answer_mdx: "...",
  },
};
