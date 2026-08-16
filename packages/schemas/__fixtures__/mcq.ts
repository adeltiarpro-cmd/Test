export const valid = {
  type: "mcq",
  payload: {
    options: [
      { key: "A", text_mdx: "La valeur terminale est **indépendante** du taux de croissance à long terme." },
      { key: "B", text_mdx: "Le WACC est utilisé pour actualiser les **free cash flows**." },
      { key: "C", text_mdx: "L'EV inclut la **dette nette** de l'entreprise." },
      { key: "D", text_mdx: "Le ratio P/E est un multiple **d'actif**." },
    ],
    multiple: false,
    shuffle: true,
  },
  solution: {
    correct_keys: ["B"],
    explain_mdx:
      "**B est correct** : le WACC est bien le taux d'actualisation des FCF dans un DCF.\n\n- A : faux — la TV est très sensible à g.\n- C : faux — l'EV exclut la trésorerie et inclut la dette brute.\n- D : faux — P/E est un multiple de résultat.",
    distractor_explains: {
      A: "La valeur terminale = FCF_{n+1} / (WACC − g). Un changement de 1 pt de g peut modifier TV de 20−30 %.",
      C: "EV = Capitalisation + Dette brute − Trésorerie. La dette nette est déduite pour passer à la valeur des fonds propres.",
      D: "P/E (Price-to-Earnings) rapporte le prix à un flux de résultat, pas à un actif. P/B serait un multiple d'actif.",
    },
  },
};

// Invalid : options = [] viole .min(2)
export const invalid = {
  type: "mcq",
  payload: {
    options: [],
    multiple: false,
    shuffle: false,
  },
  solution: {
    correct_keys: ["A"],
    explain_mdx: "...",
    distractor_explains: {},
  },
};
