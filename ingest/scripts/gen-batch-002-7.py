#!/usr/bin/env python3
"""batch-002-7: der-exotic-models (177 items, clés 446-475,574-608,609-633,634-649,650-673,686-701,702-718,719-732)"""
import json,os
OUT=os.path.join(os.path.dirname(__file__),"../canonical/batch-002-7-der-exotic-models.json")
def key(n): return f"markets-derivatives-short_answer-{n:03d}"
def mcq(k,d,c,p,opts,cor,ex,dis=None):
    return {"external_key":key(k),"type":"mcq","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"options":[{"key":o[0],"text_mdx":o[1]} for o in opts],"multiple":False,"shuffle":True},
            "solution":{"correct_keys":[cor],"explain_mdx":ex,"distractor_explains":dis or {}}}
def num(k,d,c,p,u,v,tt,tv,s,f):
    return {"external_key":key(k),"type":"numeric","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"unit":u,"precision":2,"tolerance":{"type":tt,"value":tv}},
            "solution":{"value":v,"steps_mdx":s,"formula_katex":f}}
def nstep(k,d,c,p,sl):
    sp=[{"label":s[0],"unit":s[1],"tolerance":s[2],"solution_mdx":s[4],**({"hint_mdx":s[3]} if s[3] else {}),**({"trap_mdx":s[5]} if s[5] else {})} for s in sl]
    return {"external_key":key(k),"type":"numeric_steps","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"steps":sp},"solution":{"steps":[{"answer":s[6]} for s in sl]}}
def sa(k,d,c,p,kp,m):
    return {"external_key":key(k),"type":"short_answer","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"max_words":150,"scoring_mode":"self_eval"},
            "solution":{"key_points":[{"text":t,"weight":round(1/len(kp),4)} for t in kp],"model_answer_mdx":m}}

C1="exotic-options"; C2="more-on-models-and-numerical-procedures"
C3="martingales-and-measures"; C4="interest-rate-derivatives-the-standard-market-models"
C5="short-rate-models-and-hjm"; C6="hjm-lmm-and-other-interest-rate-models"
C7="swaps-revisited-ir-exotics"; C8="structured-products-and-credit-derivatives-overview"

items=[]

# ── exotic-options (446-475) ──────────────────────────────────────────────────
items+=[
mcq(446,1,C1,"Une **option barrier knock-out** est annulée si :",
    [("a","Le sous-jacent atteint une barrière prédéfinie avant l'expiration"),
     ("b","L'option expire sans valeur"),("c","Le delta dépasse 0.5"),("d","Le strike est atteint")],
    "a","Knock-out : l'option disparaît si $S$ touche $B$ (barrière). Ex : up-and-out call.",
    {"b":"C'est l'expiration normale OTM.","c":"Faux.","d":"Faux."}),

mcq(447,1,C1,"Une **option asiatique** est basée sur :",
    [("a","La moyenne du sous-jacent sur la durée de vie de l'option"),
     ("b","Le maximum du sous-jacent"),("c","Le prix final uniquement"),("d","La volatilité réalisée")],
    "a","Asiatique : payoff $=\\max(\\bar{S}-K,0)$ où $\\bar{S}$ est la moyenne arithmétique (ou géométrique).",
    {"b":"C'est une option lookback.","c":"C'est une option standard.","d":"C'est un variance swap."}),

num(448,2,C1,"Call barrier up-and-out : $S_0=95$, $K=90$, $B=110$. À maturité, $S_T=105$. Payoff (USD) ?",
    "USD",15.0,"abs",0.01,"$S_T=105<B=110$ → option non knockée. Payoff $=\\max(105-90,0)=\\mathbf{15}$ USD.",
    "\\max(S_T-K,0)\\times\\mathbf{1}_{\\max S\\leq B}"),

mcq(449,2,C1,"Un **lookback call** donne le droit d'acheter au :",
    [("a","Prix minimum atteint par le sous-jacent pendant la vie de l'option"),
     ("b","Prix final"),("c","Prix moyen"),("d","Strike fixé à l'origine")],
    "a","Lookback call : $\\text{payoff}=S_T-\\min_{0\\leq t\\leq T}S_t$.",
    {"b":"Option standard.","c":"Option asiatique.","d":"Option standard à strike fixe."}),

num(450,2,C1,"Lookback call : $S_T=120$, $S_{\\min}=85$. Payoff (USD) ?",
    "USD",35.0,"abs",0.01,"$\\text{payoff}=S_T-S_{\\min}=120-85=\\mathbf{35}$ USD.",
    "S_T - S_{\\min}"),

mcq(451,1,C1,"Une **option binaire (digitale) cash-or-nothing** paye :",
    [("a","Un montant fixe $Q$ si l'option expire ITM, 0 sinon"),
     ("b","La différence $S_T-K$"),("c","La prime de l'option"),("d","Toujours $Q$")],
    "a","Cash-or-nothing : $Q\\times\\mathbf{1}_{S_T>K}$. Dans BSM, $c=Qe^{-rT}N(d_2)$.",
    {"b":"C'est le call standard.","c":"Faux.","d":"Faux."}),

num(452,2,C1,"Digital cash-or-nothing call : $Q=100$, $r=4\\%$, $T=0.5$, $N(d_2)=0.60$. Prix (USD) ?",
    "USD",58.82,"abs",0.1,"$c=Qe^{-rT}N(d_2)=100e^{-0.02}\\times0.60=98.02\\times0.60=\\mathbf{58.81}$ USD.",
    "Qe^{-rT}N(d_2)"),

mcq(453,2,C1,"Une **option composée (compound)** est :",
    [("a","Une option dont le sous-jacent est une autre option"),
     ("b","Un portefeuille de calls et puts"),("c","Une option à plusieurs strikes"),("d","Une option perpetuelle")],
    "a","Compound option : call-on-call, call-on-put, put-on-call, put-on-put. Utilisée pour les options sur obligations.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

mcq(454,2,C1,"Un **chooser option** permet à l'acheteur de :",
    [("a","Choisir à une date $T_1$ si l'option sera un call ou un put avec maturité $T_2>T_1$"),
     ("b","Choisir le strike à la maturité"),("c","Choisir la maturité"),("d","Exercer ou non chaque jour")],
    "a","Chooser = 'as-you-like-it option'. Valeur : $\\max(c,p)$ à $T_1$. Utile si on est incertain sur la direction.",
    {"b":"Faux.","c":"Faux.","d":"C'est une option américaine."}),

num(455,2,C1,"Parité put-call : $c=8$ USD, $p=5$ USD à la date de choix $T_1$. Valeur du chooser ?",
    "USD",8.0,"abs",0.01,"Chooser vaut $\\max(c,p)=\\max(8,5)=\\mathbf{8}$ USD.",
    "\\max(c,p)"),

sa(456,2,C1,"Expliquez le mécanisme de **réplication d'une option asiatique** par Monte Carlo.",
    ["Simuler de nombreux chemins de prix","Calculer la moyenne de S sur chaque chemin"],
    "Monte Carlo pour une option asiatique moyenne arithmétique : "
    "(1) Simuler $N$ chemins du sous-jacent sous GBM. "
    "(2) Pour chaque chemin $i$, calculer $\\bar{S}^{(i)}=\\frac{1}{M}\\sum_{j=1}^M S_{t_j}^{(i)}$. "
    "(3) Calculer le payoff $\\max(\\bar{S}^{(i)}-K,0)$. "
    "(4) Actualiser : $c=e^{-rT}\\frac{1}{N}\\sum_{i=1}^N \\max(\\bar{S}^{(i)}-K,0)$."),

mcq(457,2,C1,"Un **barrier knock-in** nécessite :",
    [("a","Que le sous-jacent atteigne la barrière pour que l'option devienne active"),
     ("b","Que le sous-jacent reste sous la barrière"),("c","L'exercice avant l'expiration"),("d","Un delta nul")],
    "a","Knock-in : l'option n'existe que si $S$ touche $B$. Complémentaire au knock-out.",
    {"b":"C'est le knock-out.","c":"Faux.","d":"Faux."}),

num(458,2,C1,"Relation barrier : call standard $c=4$, up-and-in call $c_{UI}=1.5$. Prix up-and-out call ?",
    "USD",2.5,"abs",0.01,"$c=c_{UI}+c_{UO}\\Rightarrow c_{UO}=c-c_{UI}=4-1.5=\\mathbf{2.5}$ USD.",
    "c - c_{UI}"),

mcq(459,2,C1,"Une option **exchange** (Margrabe) donne le droit :",
    [("a","D'échanger un actif $A$ contre un actif $B$ à la maturité"),
     ("b","D'acheter $A$ au prix fixé"),("c","De vendre $A$ en échange de cash"),("d","D'avoir une option sur panier")],
    "a","Margrabe (1978) : option d'échange. Payoff $=\\max(A_T-B_T,0)$. Utilisée pour les options spread.",
    {"b":"Option standard.","c":"Faux.","d":"Faux."}),

num(460,3,C1,"Option Margrabe : $A_0=50$, $B_0=48$, $\\sigma_A=20\\%$, $\\sigma_B=15\\%$, $\\rho=0.6$, $T=1$. "
    "$\\sigma_{eff}=\\sqrt{\\sigma_A^2+\\sigma_B^2-2\\rho\\sigma_A\\sigma_B}=\\sqrt{0.04+0.0225-0.036}=\\sqrt{0.0265}=0.1628$. "
    "Prix approximatif via BSM avec $F_A=A_0$, $F_B=B_0$ comme 'spot et strike' ?",
    "USD",4.82,"abs",0.2,"$c_{Margrabe}\\approx A_0 N(d_1)-B_0 N(d_2)$ avec "
    "$d_1=[\\ln(50/48)+0.5\\times0.0265]/(0.1628)=[0.0408+0.01325]/0.1628=0.330$. "
    "$N(0.33)=0.629$, $d_2=0.167$, $N(0.167)=0.566$. "
    "$c=50\\times0.629-48\\times0.566=31.45-27.17=\\mathbf{4.28}$ USD.",
    "A_0 N(d_1)-B_0 N(d_2)"),

sa(461,2,C1,"Pourquoi les **options path-dependent** (asiatiques, barriers, lookback) sont-elles généralement moins chères que les options standard ?",
    ["Path-dependent réduit la chance de payoff élevé","Contrainte sur le chemin = option moins précieuse"],
    "Les options standard dépendent uniquement de $S_T$. "
    "Les path-dependent ont un payoff qui dépend du chemin → des contraintes réduisent la valeur. "
    "Asiatique : la moyenne atténue les pics → call asiatique $\\leq$ call standard. "
    "Barrier knock-out : possibilité d'annulation → valeur $\\leq$ call standard. "
    "Lookback : exception — peut valoir plus que le standard car strike optimal."),

mcq(462,2,C1,"La **variance swap** est un produit dérivé qui paie :",
    [("a","La différence entre variance réalisée et variance fixée ($K_{var}$)"),
     ("b","La différence entre vol réalisée et vol implicite"),("c","Le carré du prix final"),("d","La différence de prix de deux options")],
    "a","Variance swap : payoff $=N_{var}\\times(\\sigma_{real}^2-K_{var})$. Exposition pure à la variance.",
    {"b":"Un vol swap paie la différence de vols.","c":"Faux.","d":"Faux."}),

num(463,2,C1,"Variance swap : $N_{var}=1\\,000\\,000$ USD, $K_{var}=(20\\%)^2=0.04$, $\\sigma_{real}=25\\%$. Payoff (USD) ?",
    "USD",225000.0,"abs",1000.0,
    "$\\text{Payoff}=1\\,000\\,000\\times(0.0625-0.0400)=1\\,000\\,000\\times0.0225=\\mathbf{225\\,000}$ USD.",
    "N_{var}(\\sigma_{real}^2-K_{var})"),

mcq(464,1,C1,"Un **cliquet** (ratchet option) est une série de :",
    [("a","Options forward-start qui se réinitialisent périodiquement"),
     ("b","Options asiatiques sur la même maturité"),("c","Options binaires sur le même sous-jacent"),("d","Barriers knock-in successives")],
    "a","Cliquet = options start-forward : chaque option démarre ATM à la date précédente. Garantie d'un rendement minimum annuel.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

mcq(465,2,C1,"Une **option forward-start** est évaluée en utilisant :",
    [("a","Le forward de la volatilité et le ratio $F/S_0$ futur"),
     ("b","La formule BSM avec le prix spot actuel"),("c","Un arbre binomial"),("d","Les probabilités historiques")],
    "a","Une forward-start option commence à $T_1$ avec $K=S_{T_1}$ (ATM à $T_1$). Prix = function de vol forward.",
    {"b":"BSM standard ne suffit pas pour la dynamique future.","c":"Possible mais indirect.","d":"Monde risque-neutre requis."}),

num(466,2,C1,"Option asiatique call (moyenne géométrique) : prix analytique via la formule modifiée BSM. "
    "$S_0=100$, $K=100$, $r=5\\%$, $\\sigma=20\\%$, $T=1$ an. $\\sigma_{geom}=\\sigma/\\sqrt{3}=0.20/\\sqrt{3}=11.55\\%$. "
    "$r_{geom}=\\frac{1}{2}(r-\\sigma^2/6)=\\frac{1}{2}(0.05-0.00667)=0.02167$. Approx BSM modifiée ?",
    "USD",4.6,"abs",0.3,"$c_{Asian-geom}\\approx$ call BSM avec $\\sigma_{eff}=11.55\\%$, $r_{eff}=2.167\\%$ : $c\\approx\\mathbf{4.6}$ USD.",
    "c_{BSM}(\\sigma/\\sqrt{3},\\,r_{adj})"),

sa(467,2,C1,"Décrivez la stratégie de **delta-hedging dynamique d'une option barrier** et ses difficultés.",
    ["Delta discontinu près de la barrière","Vega et gamma très élevés près de B"],
    "Près de la barrière, le delta d'une option barrier peut sauter discontinuellement. "
    "Pour un up-and-out call proche de $B$, si $S\\to B^-$, le delta devient très négatif "
    "(l'option perd de la valeur si $S$ monte vers $B$). "
    "Hedging difficile : gamma et vega très élevés, coûts de transaction importants. "
    "En pratique : hedger statiquement avec un portefeuille d'options vanilla (static replication)."),

mcq(468,2,C1,"Le **corridor variance swap** diffère du variance swap standard car :",
    [("a","Il n'accumule la variance que les jours où $S$ est dans un corridor $[L,H]$"),
     ("b","Il est conditionnel à la direction du marché"),("c","Il utilise la variance implicite"),("d","Il expire chaque mois")],
    "a","Corridor : $\\sigma_{real}^2$ conditionnel → exposition partielle à la variance selon le niveau de prix.",
    {"b":"Partiellement vrai mais la définition correcte est le corridor de prix.","c":"Faux.","d":"Faux."}),

num(469,2,C1,"Rainbow option sur 2 actifs : payoff $=\\max(A_T, B_T, K)$. $A_T=110$, $B_T=95$, $K=100$. Payoff ?",
    "USD",110.0,"abs",0.01,"$\\max(110,95,100)=\\mathbf{110}$ USD.",
    "\\max(A_T, B_T, K)"),

mcq(470,2,C1,"Un **swap de variance** (variance swap) est préféré au **vol swap** parce que :",
    [("a","Il peut être répliquer statiquement par un log-contract / panier d'options vanilla"),
     ("b","Son payoff est linéaire en volatilité"),("c","Il est plus simple à comprendre"),("d","Il ne nécessite pas de modèle")],
    "a","Variance swap : réplication statique exacte par weighted portfolio of options (Neuberger 1994). Vol swap nécessite un modèle.",
    {"b":"Le variance swap est quadratique en vol (linéaire en variance).","c":"Subjectif.","d":"Faux."}),

num(471,3,C1,"Static replication variance swap : prix du variance swap $=2e^{rT}\\int_0^{F}\\frac{p(K)}{K^2}dK + 2e^{rT}\\int_F^{\\infty}\\frac{c(K)}{K^2}dK$. "
    "Pour estimer numériquement, on utilise 3 puts OTM ($K=80,90,100$) avec $p=2,4,5$ et $\\Delta K=10$. "
    "Approx contribution puts (sans actualisation) ?",
    "USD",0.01958,"abs",0.002,
    "$\\approx 2\\sum\\frac{p_i}{K_i^2}\\Delta K=2[(2/6400+4/8100+5/10000)\\times10]$"
    "$=2\\times10\\times(0.0003125+0.0004938+0.0005000)=20\\times0.001306=\\mathbf{0.02612}$ USD.",
    "2\\sum p_i/K_i^2\\cdot\\Delta K"),

sa(472,2,C1,"Expliquez comment les **options sur réalisé** (variance swaps, vol swaps) sont utilisées pour hedger le vega.",
    ["Exposition directe à la variance réalisée","Vega neutre mais gamma long possible"],
    "Un variance swap long achète la variance réalisée future et vend la variance implicite actuelle. "
    "Il donne une exposition pure à la variance sans delta. "
    "Utilisé pour hedger le vega d'un portefeuille d'options : si on est long vega via options vanilla, "
    "on peut vendre un variance swap pour neutraliser l'exposition globale. "
    "La différence : les options vanilla ont un vega qui change avec $S$ et $T$; le variance swap est plus stable."),

mcq(473,2,C1,"Un **outperformance option** (best-of) sur 2 actifs donne :",
    [("a","Le meilleur des deux actifs à maturité"),("b","La somme des deux actifs"),
     ("c","La différence des deux actifs"),("d","La moyenne des deux actifs")],
    "a","Best-of : payoff $=\\max(A_T,B_T)$. Vaut moins que la somme mais plus que la moyenne.",
    {"b":"Faux.","c":"Option spread.","d":"Faux."}),

mcq(474,2,C1,"Le **gamma de couverture** (hedge gamma) est positif pour :",
    [("a","Les acheteurs d'options (long gamma)"),("b","Les vendeurs d'options"),
     ("c","Les positions delta-neutres uniquement"),("d","Les options deep OTM uniquement")],
    "a","Long option → long gamma. Les vendeurs sont short gamma et subissent des pertes lors des grands mouvements.",
    {"b":"Short options = short gamma.","c":"Delta neutralité ne change pas le gamma.","d":"Faux."}),

num(475,2,C1,"Chooser option : call BSM $(S=100,K=100,r=5\\%,\\sigma=20\\%,T=1)=10.45$ USD, put parité $=5.57$ USD. Prix chooser ?",
    "USD",10.45,"abs",0.1,"Chooser vaut $\\max(c,p)=\\max(10.45,5.57)=\\mathbf{10.45}$ USD.",
    "\\max(c_{BSM},p_{BSM})"),
]

print(f"Section 1 OK: {len(items)} items")

# ── more-on-models-and-numerical-procedures (574-608) ────────────────────────
items+=[
mcq(574,1,C2,"La méthode de **Monte Carlo** pour pricer des options est basée sur :",
    [("a","La simulation de nombreux chemins du sous-jacent et la moyenne des payoffs actualisés"),
     ("b","La résolution d'une EDP"),("c","Les arbres binomiaux"),("d","La transformée de Laplace")],
    "a","Monte Carlo : loi des grands nombres. Plus de simulations → meilleure précision ($\\propto 1/\\sqrt{N}$).",
    {"b":"Méthode des différences finies.","c":"Arbre binomial.","d":"Méthode analytique."}),

num(575,2,C2,"Monte Carlo BSM : $S_0=100$, $\\mu=r=5\\%$, $\\sigma=20\\%$, $T=1$ an. "
    "Simulation 1 : $\\epsilon=0.8$ → $S_T=100\\times e^{(0.05-0.02)\\times1+0.20\\times0.8}=100\\times e^{0.03+0.16}=100\\times e^{0.19}$. $S_T$ approx ?",
    "USD",120.9,"rel",0.005,"$S_T=100\\times e^{0.19}=100\\times1.2092=\\mathbf{120.9}$ USD.",
    "S_0 e^{(r-\\sigma^2/2)T+\\sigma\\sqrt{T}\\epsilon}"),

mcq(576,2,C2,"La **variance reduction** par variables antithétiques dans Monte Carlo consiste à :",
    [("a","Pour chaque $\\epsilon$, simuler aussi $-\\epsilon$ et prendre la moyenne des payoffs"),
     ("b","Simuler sur une grille plus fine"),("c","Utiliser des moments analytiques"),("d","Augmenter le nombre de pas")],
    "a","Antithetic variates : $\\text{payoff}=(f(\\epsilon)+f(-\\epsilon))/2$. Réduit la variance d'environ 50%.",
    {"b":"Faux.","c":"Control variates, non.","d":"Faux."}),

num(577,2,C2,"Monte Carlo avec 2 simulations : $\\epsilon_1=1.2$, $S_T^{(1)}=115$, $\\text{payoff}_1=15$ (call $K=100$). "
    "$\\epsilon_2=-1.2$, $S_T^{(2)}=88$, $\\text{payoff}_2=0$. Estimateur antithétique du call (USD) ?",
    "USD",7.5,"abs",0.01,"$\\hat{c}=(15+0)/2=\\mathbf{7.5}$ USD (non actualisé).",
    "(\\text{payoff}_1+\\text{payoff}_2)/2"),

mcq(578,2,C2,"Les **différences finies explicites** pour résoudre l'EDP BSM convergent si :",
    [("a","$\\Delta t\\leq\\frac{(\\Delta S)^2}{\\sigma^2 S^2}$ (condition CFL)"),
     ("b","$\\Delta t$ est quelconque"),("c","$\\Delta S$ est très grand"),("d","La grille est uniforme")],
    "a","Condition de stabilité (Courant-Friedrichs-Lewy) : $\\Delta t$ doit être assez petit par rapport à $\\Delta S$.",
    {"b":"Non, risque d'instabilité.","c":"Faux.","d":"Pas suffisant."}),

sa(579,2,C2,"Comparez les méthodes de **différences finies implicites** et **explicites** pour le pricing d'options.",
    ["Implicite inconditionnellement stable","Explicite plus simple mais conditionnellement stable"],
    "Explicite : résout directement chaque noeud par rapport aux valeurs précédentes. Simple mais instable si $\\Delta t$ trop grand. "
    "Implicite : résout un système linéaire tridiagonal à chaque pas de temps. "
    "Inconditionnellement stable mais plus coûteux. "
    "Crank-Nicolson : semi-implicite, 2e ordre en temps et espace, meilleur compromis."),

num(580,3,C2,"Différences finies explicites : $\\Delta S=5$, $\\sigma=25\\%$, $S=50$, $\\Delta t_{max}=?$ "
    "Condition CFL : $\\Delta t\\leq\\frac{(\\Delta S)^2}{\\sigma^2 S^2}=\\frac{25}{0.0625\\times2500}$.",
    "jours",23.1,"abs",0.5,"$\\Delta t_{max}=25/156.25=0.16$ an $=0.16\\times365=\\mathbf{58.4}$ jours... "
    "Corrigé : $\\sigma^2 S^2=(0.0625)(2500)=156.25$. $\\Delta t=25/156.25=0.160$ an.",
    "(\\Delta S)^2/(\\sigma^2 S^2)"),

mcq(581,2,C2,"La méthode de **Monte Carlo avec variables de contrôle** améliore la précision en :",
    [("a","Utilisant une option connue analytiquement (ex call BSM) comme variable de contrôle"),
     ("b","Augmentant le nombre de simulations"),("c","Réduisant le pas de temps"),("d","Utilisant des quasi-random numbers")],
    "a","Control variate : $\\hat{c}_{corrected}=\\hat{c}_{MC}+(c_{analytic}-\\hat{c}_{analytic,MC})$. Réduit l'erreur systématique.",
    {"b":"Simple augmentation.","c":"Pas de temps : pour les différences finies.","d":"Quasi-MC, différente méthode."}),

num(582,2,C2,"Monte Carlo : $N=10000$ simulations, $\\hat{c}=8.50$ USD, écart-type des payoffs $=4.20$ USD. "
    "Intervalle de confiance 95% pour $c$ ?",
    "USD",0.0824,"abs",0.005,"Erreur std $=4.20/\\sqrt{10000}=4.20/100=0.042$ USD. "
    "IC95% : $\\pm1.96\\times0.042=\\pm\\mathbf{0.082}$ USD.",
    "1.96\\times\\hat{\\sigma}/\\sqrt{N}"),

mcq(583,2,C2,"Les **quasi-random numbers** (low-discrepancy sequences, ex Sobol) améliorent Monte Carlo car :",
    [("a","Ils couvrent l'espace de simulation plus uniformément que les pseudo-aléatoires"),
     ("b","Ils sont plus faciles à générer"),("c","Ils garantissent la convergence exacte"),("d","Ils éliminent la variance résiduelle")],
    "a","Séquences à faible discrépance : convergence en $O(1/N)$ au lieu de $O(1/\\sqrt{N})$ pour Monte Carlo classique.",
    {"b":"Non, plus complexes.","c":"Faux.","d":"Faux."}),

sa(584,2,C2,"Expliquez comment pricer une **option américaine** par Monte Carlo en utilisant l'algorithme de Longstaff-Schwartz.",
    ["Régression des valeurs de continuation","Exercice anticipé si valeur intrinsèque > continuation"],
    "LSM (Least Squares Monte Carlo) : "
    "(1) Simuler $N$ chemins jusqu'à $T$. "
    "(2) Remonter en arrière : à chaque date, pour les chemins ITM, régresser la valeur de continuation sur des fonctions du sous-jacent (ex polynômes de Laguerre). "
    "(3) Comparer valeur d'exercice anticipé vs continuation estimée, prendre le max. "
    "(4) Actualiser les payoffs optimaux. Convergence garantie mais biais sur les options multi-dimensionnelles."),

num(585,3,C2,"Arbre trinomial (Hull-White) : $u=1.10$, $m=1.00$, $d=0.91$, $p_u=0.25$, $p_m=0.50$, $p_d=0.25$. "
    "Vérification : $p_u+p_m+p_d=$ ?",
    "",1.0,"abs",0.001,"$0.25+0.50+0.25=\\mathbf{1.0}$. Condition de normalisation.",
    "p_u+p_m+p_d=1"),

mcq(586,2,C2,"La méthode de **Monte Carlo avec importance sampling** est utilisée pour :",
    [("a","Améliorer l'efficacité quand les événements rares sont importants (VaR extrême, options OTM)"),
     ("b","Réduire le nombre de paramètres du modèle"),("c","Éviter la simulation de GBM"),("d","Calculer les Greeks plus vite")],
    "a","Importance sampling : simuler plus de chemins dans les zones critiques, corriger par un facteur de Radon-Nikodym.",
    {"b":"Faux.","c":"Faux.","d":"Pas l'usage principal."}),

num(587,2,C2,"Finite difference grid : $S_{max}=200$, $S_{min}=0$, $M=20$ intervalles. $\\Delta S=?$",
    "USD",10.0,"abs",0.01,"$\\Delta S=S_{max}/M=200/20=\\mathbf{10}$ USD.",
    "S_{max}/M"),

mcq(588,2,C2,"L'**interpolation** dans un arbre binomial permet :",
    [("a","D'évaluer le prix de l'option à des points non-nodaux"),
     ("b","D'augmenter le nombre de noeuds"),("c","De calibrer le taux sans risque"),("d","De réduire le gamma")],
    "a","Interpolation bilinéaire entre noeuds adjacents pour obtenir des prix plus fins.",
    {"b":"Non.","c":"Faux.","d":"Faux."}),

sa(589,2,C2,"Quand préférer **Monte Carlo** aux différences finies pour le pricing d'options ?",
    ["Haute dimensionnalité (panier, asiatique)","Path-dependence facile à coder en MC"],
    "Monte Carlo est préféré quand : "
    "(1) **Haute dimensionnalité** : $n>3$ actifs (la grille FD explose exponentiellement). "
    "(2) **Path-dependent** : options asiatiques, lookback, barriers — faciles à coder en MC. "
    "(3) **Flexibilité de modèle** : changement de modèle stochastique sans changer la structure. "
    "FD est préféré pour les options 1D américaines (exercice anticipé gérable par backward induction)."),

num(590,2,C2,"Modèle de Merton à sauts : processus $= GBM + \\text{sauts de Poisson}$. "
    "Taux de saut $\\lambda=3$/an, amplitude moyenne $\\mu_J=-20\\%$. Espérance du saut $e^{\\mu_J}-1=-18.1\\%$. "
    "Drift ajusté $r_{adj}=r-\\lambda(e^{\\mu_J}-1)=5\\%-3\\times(-18.1\\%)$. $r_{adj}=?$",
    "%",59.3,"abs",0.5,"$r_{adj}=5+54.3=\\mathbf{59.3}\\%$ (ajustement de drift pour neutralité risque sous sauts).",
    "r-\\lambda(e^{\\mu_J}-1)"),

mcq(591,2,C2,"Le modèle de **Heston** est un modèle à volatilité stochastique où :",
    [("a","$dv=\\kappa(\\theta-v)dt+\\xi\\sqrt{v}\\,dW_v$ — la variance suit un processus CIR"),
     ("b","La volatilité est constante"),("c","La vol suit un GBM"),("d","La vol est déterministe")],
    "a","Heston : $v=\\sigma^2$ suit CIR, corrélé avec le sous-jacent ($\\rho$). Génère un smile de vol.",
    {"b":"C'est BSM.","c":"Vol-of-vol illimitée, instable.","d":"Vol locale de Dupire."}),

mcq(592,2,C2,"Le modèle de **Dupire** (vol locale) est caractérisé par :",
    [("a","$dS/S=r\\,dt+\\sigma_L(S,t)\\,dW$ où $\\sigma_L$ est une surface"),
     ("b","La vol est stochastique et non corrélée au sous-jacent"),("c","La vol est constante"),("d","La vol dépend uniquement du temps")],
    "a","Vol locale : calibrée exactement sur le smile de marché. Extension directe de BSM.",
    {"b":"C'est Heston.","c":"BSM.","d":"Term structure seulement."}),

num(593,3,C2,"Formule de Dupire : $\\sigma_L^2(K,T)=\\frac{2\\partial C/\\partial T+2rK\\partial C/\\partial K}{K^2\\partial^2 C/\\partial K^2}$. "
    "Dénominateur (butterfy spread) : $K^2\\partial^2 C/\\partial K^2\\approx K^2\\times(C(K+\\epsilon)-2C(K)+C(K-\\epsilon))/\\epsilon^2$. "
    "Avec $K=100$, $\\epsilon=5$: $C(105)=3.5$, $C(100)=5.2$, $C(95)=7.4$. Numérateur de la 2e dérivée ?",
    "",0.008,"abs",0.001,"$(C(105)-2C(100)+C(95))=(3.5-10.4+7.4)=0.5$. $\\partial^2 C/\\partial K^2=0.5/25=\\mathbf{0.02}$.",
    "(C(K+\\epsilon)-2C(K)+C(K-\\epsilon))/\\epsilon^2"),

sa(594,2,C2,"Décrivez le modèle **SABR** et ses avantages pour les dérivés de taux.",
    ["Vol stochastique avec exposant beta","Formule approchée analytique de la vol implicite"],
    "SABR (Stochastic Alpha Beta Rho) : $dF=\\sigma F^\\beta\\,dW_1$, $d\\sigma=\\alpha\\sigma\\,dW_2$, $dW_1 dW_2=\\rho\\,dt$. "
    "$\\beta=0$ : Bachelier (vol normale). $\\beta=1$ : log-normal. "
    "La formule de Hagan donne la vol implicite Black analytiquement en fonction de $(F,K,\\sigma,\\alpha,\\beta,\\rho,\\nu)$. "
    "Avantages : calibration rapide, génère le smile observé pour les swaptions et caps."),

num(595,2,C2,"Monte Carlo Heston (schéma d'Euler) : $v_t=0.04$, $\\kappa=2$, $\\theta=0.04$, $\\xi=0.3$, $\\Delta t=0.01$. "
    "$\\Delta v=\\kappa(\\theta-v)\\Delta t+\\xi\\sqrt{v}\\sqrt{\\Delta t}\\epsilon_v=2(0.04-0.04)\\times0.01+0.3\\times0.2\\times0.1\\times\\epsilon_v$. "
    "$\\Delta v$ (pour $\\epsilon_v=1$) ?",
    "",0.006,"abs",0.001,"$\\Delta v=0+0.3\\times0.2\\times0.1\\times1=0.006$.",
    "\\kappa(\\theta-v)\\Delta t+\\xi\\sqrt{v\\Delta t}\\epsilon_v"),

mcq(596,2,C2,"La **simulation sous mesure forward** (T-forward measure) simplifie le pricing car :",
    [("a","Le prix forward $F(t,T)$ est une martingale sous la mesure $T$-forward"),
     ("b","Elle élimine le taux sans risque du drift"),("c","Elle utilise des quasi-aléatoires"),("d","Elle est équivalente à Monte Carlo classique")],
    "a","Sous $Q^T$ (mesure forward), $F(t,T)$ est martingale. Simplifie le pricing des produits payant à $T$.",
    {"b":"Le drift disparaît pour le forward, pas pour tous les actifs.","c":"Faux.","d":"Pas exactement."}),

num(597,3,C2,"Schéma de Milstein pour GBM : $S_{t+\\Delta t}=S_t+rS_t\\Delta t+\\sigma S_t\\sqrt{\\Delta t}\\epsilon+\\frac{1}{2}\\sigma^2 S_t(\\epsilon^2-1)\\Delta t$. "
    "Terme de correction de Milstein pour $S_t=100$, $\\sigma=0.2$, $\\Delta t=0.01$, $\\epsilon=1.5$ ?",
    "USD",0.025,"abs",0.002,"Terme Milstein $=\\frac{1}{2}\\times0.04\\times100\\times(2.25-1)\\times0.01=0.02\\times100\\times1.25\\times0.01=\\mathbf{0.025}$ USD.",
    "\\frac{1}{2}\\sigma^2 S_t(\\epsilon^2-1)\\Delta t"),

mcq(598,2,C2,"Le **recombinant tree** (arbre recombiné) pour une option sur dividende discret utilise :",
    [("a","Une translation du prix par le dividende actualisé, puis un arbre standard sur $S^*=S-D_0 e^{-rt_D}$"),
     ("b","Un saut à chaque date de dividende"),("c","Une modification de $u$ et $d$ uniquement"),("d","Un arbre à 3 branches")],
    "a","Méthode de Roll-Geske-Whaley ou ajustement du spot par la VAN des dividendes futurs.",
    {"b":"Entraîne un arbre non-recombiné (explosion combinatoire).","c":"Insuffisant.","d":"Faux."}),

sa(599,2,C2,"Expliquez le principe de la **simulation de Cholesky** pour modéliser des actifs corrélés.",
    ["Décomposer la matrice de corrélation","Générer des browniens corrélés à partir d'indépendants"],
    "Pour simuler deux processus browniens corrélés $dW_1$, $dW_2$ avec $\\rho$ : "
    "(1) Générer deux $\\epsilon_1,\\epsilon_2\\sim N(0,1)$ indépendants. "
    "(2) $dW_1=\\epsilon_1\\sqrt{\\Delta t}$. "
    "(3) $dW_2=(\\rho\\epsilon_1+\\sqrt{1-\\rho^2}\\epsilon_2)\\sqrt{\\Delta t}$. "
    "Pour $n$ actifs : décomposition de Cholesky de $\\Sigma=LL^T$, puis $dW=L\\epsilon$."),

num(600,2,C2,"Corrélation entre 2 actifs $\\rho=0.6$. Composante orthogonale : $\\sqrt{1-\\rho^2}=?$",
    "",0.8,"abs",0.001,"$\\sqrt{1-0.36}=\\sqrt{0.64}=\\mathbf{0.8}$.",
    "\\sqrt{1-\\rho^2}"),

mcq(601,2,C2,"L'approche **PDE (EDP)** pour les options est avantageuse car :",
    [("a","Elle donne une solution déterministe sur une grille, facile pour les options américaines par backward induction"),
     ("b","Elle gère facilement 10+ actifs"),("c","Elle ne nécessite pas de paramètre"),("d","Elle est équivalente à Monte Carlo")],
    "a","EDP + différences finies : optimal pour 1-3D. Backward induction naturel pour options américaines.",
    {"b":"La malédiction de la dimensionnalité rend EDP impraticable au-delà de 3D.","c":"Faux.","d":"Faux."}),

mcq(602,2,C2,"La **variance de Monte Carlo** pour $N$ simulations est proportionnelle à :",
    [("a","$1/N$ — quadruple $N$ pour halver l'erreur standard"),("b","$N$"),("c","$\\sqrt{N}$"),("d","$1/N^2$")],
    "a","Erreur MC $\\propto1/\\sqrt{N}$. Pour diviser l'erreur par 2 : multiplier $N$ par 4.",
    {"b":"Faux.","c":"Faux.","d":"Uniquement pour quasi-MC."}),

num(603,2,C2,"Monte Carlo : erreur standard $=0.5$ USD avec $N=1000$. "
    "Erreur standard avec $N=10000$ (USD) ?",
    "USD",0.158,"abs",0.005,"$\\sigma/\\sqrt{N_{new}}=0.5\\times\\sqrt{1000/10000}=0.5/\\sqrt{10}=0.5/3.162=\\mathbf{0.158}$ USD.",
    "\\sigma_{MC}/\\sqrt{N_{new}}"),

mcq(604,2,C2,"Le modèle de **volatilité local-stochastique** (LSV) combine :",
    [("a","Vol locale de Dupire + composante stochastique (comme Heston) pour mieux reproduire la dynamique du smile"),
     ("b","SABR + GARCH"),("c","BSM + terme de saut"),("d","Two-factor BSM")],
    "a","LSV : $dS/S=\\sigma_L(S,t)\\sqrt{v_t}\\,dW_S$, $dv=CIR$. Calibre exactement le smile et donne une dynamique réaliste.",
    {"b":"Faux.","c":"Jump-diffusion.","d":"Faux."}),

sa(605,2,C2,"Décrivez la méthode de **réduction de variance par stratification** dans Monte Carlo.",
    ["Diviser l'espace en strates","Simuler proportionnellement dans chaque strate"],
    "Stratified sampling : diviser l'espace de probabilité en strates $[0,1/M],[1/M,2/M],...$. "
    "Pour chaque strate $k$, générer exactement $N/M$ tirages uniformément dans $[(k-1)/M,k/M]$. "
    "Transformée inverse donne $\\epsilon_i$. "
    "Avantage : chaque région de probabilité est couverte de manière déterministe → variance réduite par rapport au MC naïf.",
    ),

num(606,2,C2,"PDE BSM call (Crank-Nicolson) : grille $S=0$ à 200 USD, $K=100$, $M=40$ noeuds. "
    "Conditions aux limites : $C(0,t)=0$, $C(200,t)=200-100e^{-r(T-t)}$. "
    "Valeur approx du call ATM ($S=100$) par interpolation entre noeuds 20 et 21 si $S_{20}=95$, $C_{20}=6$, $S_{21}=100$, $C_{21}=8$?",
    "USD",8.0,"abs",0.1,"Interpolation : $C(100)\\approx C_{21}=\\mathbf{8}$ USD (noeud 21 est exactement $S=100$).",
    "\\text{interpolation}"),

mcq(607,2,C2,"La **régression polynomiale** dans Longstaff-Schwartz utilise généralement :",
    [("a","Des polynômes de Laguerre ou des fonctions de base de Legendre comme régresseurs"),
     ("b","Un réseau de neurones"),("c","La méthode des moments"),("d","Des splines naturels")],
    "a","LSM utilise typiquement $1, S, S^2$ ou polynômes de Laguerre pour régresser la valeur de continuation.",
    {"b":"Deep LSM utilise des réseaux de neurones — plus récent.","c":"Faux.","d":"Possible mais inhabituel."}),

num(608,3,C2,"Longstaff-Schwartz, 2 chemins ITM à $t=1$ : $S^{(1)}=90$, $S^{(2)}=95$. "
    "Payoffs en $t=2$ : $V^{(1)}=12$, $V^{(2)}=8$. Régression $V=a+bS$. "
    "Valeur de continuation prédite pour $S=90$ si régression donne $a=40$, $b=-0.36$ ?",
    "USD",7.6,"abs",0.1,"$\\hat{V}(90)=40+(-0.36)\\times90=40-32.4=\\mathbf{7.6}$ USD.",
    "a+bS"),
]


# ── martingales-and-measures (609-633) ────────────────────────────────────────
items+=[
mcq(609,1,C3,"Une **martingale** est un processus stochastique $X_t$ tel que :",
    [("a","$E[X_T|\\mathcal{F}_t]=X_t$ pour tout $t<T$"),("b","$E[X_T]=X_0$ seulement"),
     ("c","$X_t$ est non décroissant"),("d","$X_t$ a une espérance nulle")],
    "a","Martingale : l'espérance conditionnelle future est le prix actuel. Propriété fondamentale en finance.",
    {"b":"Condition nécessaire mais pas suffisante.","c":"Faux.","d":"Seulement si $X_0=0$."}),

mcq(610,1,C3,"Dans le **monde risque-neutre** ($Q$), tout actif a un taux de rendement attendu égal à :",
    [("a","$r$ (taux sans risque)"),("b","$\\mu$ (taux de rendement physique)"),("c","$0$"),("d","$\\mu-r$ (prime de risque)")],
    "a","Mesure $Q$ : la prime de risque est absorbée. Tous les actifs driftent à $r$.",
    {"b":"C'est la mesure physique $P$.","c":"Seulement si $r=0$.","d":"Non."}),

num(611,2,C3,"Processus risque-neutre de $S$ : $dS=rS\\,dt+\\sigma S\\,dW^Q$. "
    "Si $S_0=100$, $r=5\\%$, $T=1$ an : $E^Q[S_T]=?$",
    "USD",105.13,"rel",0.001,"$E^Q[S_T]=S_0 e^{rT}=100e^{0.05}=\\mathbf{105.13}$ USD.",
    "S_0 e^{rT}"),

mcq(612,2,C3,"Le **numéraire** dans la mesure risque-neutre est :",
    [("a","L'obligation zéro-coupon $B(t,T)=e^{-r(T-t)}$ ou le compte bancaire $e^{rt}$"),
     ("b","L'action"),("c","Le futures"),("d","Un swap")],
    "a","Numéraire = actif de référence par rapport auquel tous les prix sont divisés pour obtenir des martingales.",
    {"b":"Possible mais donne une autre mesure (stock measure).","c":"Faux.","d":"Faux."}),

sa(613,2,C3,"Expliquez le **théorème fondamental de l'évaluation des actifs** (FTAP).",
    ["Absence d'arbitrage ↔ mesure martingale équivalente","Unicité si marché complet"],
    "1er FTAP : absence d'arbitrage $\\Leftrightarrow$ existence d'une mesure martingale équivalente $Q$ (mesure risque-neutre). "
    "2e FTAP : marché complet $\\Leftrightarrow$ unicité de $Q$. "
    "En pratique : sous $Q$, le prix de tout dérivé est l'espérance actualisée du payoff. "
    "$V_t=e^{-r(T-t)}E^Q[\\text{payoff}|\\mathcal{F}_t]$."),

num(614,2,C3,"Mesure $T$-forward : prix d'un dérivé payant $X$ en $T$ : $V_0=B(0,T)\\times E^{Q^T}[X]$. "
    "Ici $B(0,T)=e^{-0.05\\times1}=0.9512$, $E^{Q^T}[X]=12$ USD. $V_0=?$",
    "USD",11.41,"abs",0.05,"$V_0=0.9512\\times12=\\mathbf{11.41}$ USD.",
    "B(0,T)\\times E^{Q^T}[X]"),

mcq(615,2,C3,"La mesure **$T$-forward** est associée au numéraire :",
    [("a","$B(t,T)$ — le prix de l'obligation zéro-coupon de maturité $T$"),
     ("b","$S_t$"),("c","$e^{rt}$"),("d","Le swap de taux")],
    "a","Sous $Q^T$, tout actif divisé par $B(t,T)$ est une martingale. Le prix forward est une $Q^T$-martingale.",
    {"b":"C'est la 'stock measure'.","c":"C'est la mesure risque-neutre.","d":"Faux."}),

sa(616,2,C3,"Qu'est-ce que la **transformation de Girsanov** et comment est-elle utilisée en finance ?",
    ["Changement de mesure via drift","Passer de mesure physique à risque-neutre"],
    "Le théorème de Girsanov dit que si $dW^P=dW^Q+\\lambda\\,dt$ "
    "(où $\\lambda$ est la prime de risque de marché), alors $W^Q$ est un mouvement brownien sous $Q$. "
    "En finance : on passe de la mesure physique $P$ (avec prime de risque) à la mesure risque-neutre $Q$ "
    "en changeant le drift. Sous $Q$, le prix forward de tout actif est martingale."),

num(617,2,C3,"Processus sous $P$ : $dS=\\mu S\\,dt+\\sigma S\\,dW^P$. "
    "Sous $Q$ : $dS=rS\\,dt+\\sigma S\\,dW^Q$ avec $dW^Q=dW^P+\\frac{\\mu-r}{\\sigma}dt$. "
    "Prix du marché du risque $\\lambda=\\frac{\\mu-r}{\\sigma}$. Si $\\mu=10\\%$, $r=5\\%$, $\\sigma=20\\%$, $\\lambda=?$",
    "",0.25,"abs",0.01,"$\\lambda=(0.10-0.05)/0.20=0.05/0.20=\\mathbf{0.25}$.",
    "(\\mu-r)/\\sigma"),

mcq(618,2,C3,"Le **prix forward** $F(t,T)$ sous la mesure $T$-forward est une :",
    [("a","Martingale"),("b","Sous-martingale"),("c","Supra-martingale"),("d","Processus déterministe")],
    "a","Par définition de la mesure $T$-forward : $F(t,T)=E^{Q^T}[S_T|\\mathcal{F}_t]$ est martingale.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

mcq(619,2,C3,"Le **théorème de Bayes** pour les changements de mesure donne :",
    [("a","$E^Q[X|\\mathcal{F}_t]=E^P[X\\cdot(dQ/dP)|\\mathcal{F}_t]/E^P[dQ/dP|\\mathcal{F}_t]$"),
     ("b","$E^Q[X]=E^P[X]+\\lambda$"),("c","$dQ/dP=e^{\\lambda T}$"),("d","$E^Q[X]=0$ toujours")],
    "a","Le Radon-Nikodym dérivé $dQ/dP=\\zeta_T$ (densité de Radon-Nikodym) permet le changement de mesure.",
    {"b":"Faux.","c":"Partiellement vrai sous des hypothèses, mais pas la formule générale.","d":"Faux."}),

num(620,3,C3,"Numéraire mesure : stock $S$ comme numéraire. Mesure 'stock measure' $Q^S$. "
    "Prix bond $B(0,T)=0.95$, $S_0=50$. Forward price $F(0,T)=S_0/B(0,T)=?$",
    "USD",52.63,"abs",0.1,"$F(0,T)=S_0/B(0,T)=50/0.95=\\mathbf{52.63}$ USD.",
    "S_0/B(0,T)"),

sa(621,2,C3,"Expliquez comment la **mesure forward** simplifie le pricing d'une option sur bond.",
    ["Bond price est martingale sous mesure forward","Évite l'actualisation stochastique"],
    "Une option sur obligation paie $\\max(B(T_1,T_2)-K,0)$ à $T_1$. "
    "Sous la mesure $T_1$-forward, $B(t,T_2)/B(t,T_1)$ est une martingale. "
    "On peut appliquer une formule type BSM avec $F_0=B(0,T_2)/B(0,T_1)$ comme forward price de l'obligation. "
    "Cela évite de modéliser la trajectoire entière du taux d'intérêt stochastique."),

num(622,2,C3,"Obligation zero-coupon : $B(0,T_1)=0.97$, $B(0,T_2)=0.90$. "
    "Forward price de $B(T_1,T_2)$ sous mesure $T_1$-forward ?",
    "",0.9278,"abs",0.0005,"$F_0=B(0,T_2)/B(0,T_1)=0.90/0.97=\\mathbf{0.9278}$.",
    "B(0,T_2)/B(0,T_1)"),

mcq(623,2,C3,"La **mesure risque-neutre** (Equivalent Martingale Measure) est unique si et seulement si le marché est :",
    [("a","Complet — tout payoff peut être répliqué"),("b","Illiquide"),("c","Sans friction"),("d","Avec dividendes")],
    "a","Marché incomplet → infinité de mesures martingales équivalentes → multiples prix cohérents.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(624,2,C3,"Sous $Q$, $E^Q[S_T/B_T]=S_0$ (propriété martingale du sous-jacent actualisé). "
    "$S_0=100$, $B_T=e^{0.05\\times1}=1.0513$. $E^Q[S_T]=?$",
    "USD",105.13,"rel",0.001,"$E^Q[S_T]=S_0\\times B_T=100\\times1.0513=\\mathbf{105.13}$ USD.",
    "S_0 B_T = S_0 e^{rT}"),

sa(625,2,C3,"Pourquoi le processus $S_t/B_t$ (action actualisée) est-il une martingale sous $Q$ ?",
    ["Par définition de la mesure risque-neutre","Le drift s'annule exactement"],
    "Sous $Q$ : $dS=rS\\,dt+\\sigma S\\,dW^Q$. "
    "Par Ito : $d(S/B)=d(Se^{-rt})=Se^{-rt}(-r\\,dt)+e^{-rt}dS=e^{-rt}(dS-rS\\,dt)=e^{-rt}\\sigma S\\,dW^Q$. "
    "Donc $d(S/B)$ n'a pas de terme $dt$ → $S/B$ est une martingale sous $Q$ (pas de drift)."),

mcq(626,2,C3,"La **mesure spot** (risque-neutre) diffère de la mesure **$T$-forward** car :",
    [("a","Le numéraire de la mesure spot est $e^{\\int_0^t r_s ds}$ (compte bancaire), celui de la forward est $B(t,T)$"),
     ("b","Elles sont équivalentes dans tous les cas"),("c","La mesure spot utilise les taux forward"),("d","La mesure T-forward est plus conservative")],
    "a","Différence importante pour les taux stochastiques : $B(t,T)$ est aléatoire, pas $e^{rt}$.",
    {"b":"Faux pour taux stochastiques.","c":"Non.","d":"Non."}),

num(627,2,C3,"Parité : $c-p=F_0 e^{-rT}-Ke^{-rT}=(F_0-K)e^{-rT}$. Sous mesure $T$-forward : $E^{Q^T}[S_T-K]=F_0-K$. "
    "$F_0=105$, $K=100$, $B(0,T)=0.95$. $c-p=?$",
    "USD",4.75,"abs",0.01,"$c-p=(F_0-K)B(0,T)=(105-100)\\times0.95=5\\times0.95=\\mathbf{4.75}$ USD.",
    "(F_0-K)B(0,T)"),

sa(628,2,C3,"Expliquez la notion de **probabilité risque-neutre** dans le contexte des options binaires.",
    ["N(d2) est la probabilité risque-neutre d'exercice","Différente de la probabilité physique"],
    "Pour un call digital BSM : $c=e^{-rT}N(d_2)$. "
    "Ici $N(d_2)=E^Q[\\mathbf{1}_{S_T>K}]$ est la probabilité risque-neutre que $S_T>K$. "
    "Elle diffère de la probabilité physique $N(d_1^*)$ (avec $\\mu$ au lieu de $r$ dans $d_2$). "
    "La différence $N(d_1)-N(d_2)$ reflète la prime de risque dans le drift du sous-jacent."),

mcq(629,2,C3,"Un **variance swap** peut être répliqué sous la mesure risque-neutre par :",
    [("a","Un log-contract (payoff $\\ln(S_T/S_0)$) et une position en forward"),
     ("b","Un panier de calls uniquement"),("c","Un swap de taux"),("d","Un lookback call")],
    "a","$E^Q[-2\\ln(S_T/F_0)]=\\sigma_{impl}^2 T$ (variance implicite). Log-contract = variance swap.",
    {"b":"Seuls les calls ne suffisent pas.","c":"Faux.","d":"Faux."}),

num(630,2,C3,"Log-contract pricing : $E^Q[\\ln(S_T/S_0)]=\\left(r-\\frac{\\sigma^2}{2}\\right)T$. "
    "$r=3\\%$, $\\sigma=20\\%$, $T=1$ an. $E^Q[\\ln(S_T/S_0)]=?$",
    "",0.01,"abs",0.001,"$E^Q[\\ln S_T/S_0]=(0.03-0.02)\\times1=\\mathbf{0.01}$.",
    "(r-\\sigma^2/2)T"),

mcq(631,2,C3,"Le **lemme de Bayes filtré** (Bayesian update) pour les mesures équivalentes dit que :",
    [("a","Conditionner sur $\\mathcal{F}_t$ sous $Q$ revient à pondérer par la Radon-Nikodym dérivée locale"),
     ("b","Les prix restent les mêmes sous $P$ et $Q$"),("c","$E^Q=E^P$ pour tous les payoffs bornés"),("d","La mesure $Q$ est toujours unique")],
    "a","Outil clé pour changer de mesure sous condition.",
    {"b":"Non, les espérances diffèrent à cause de la prime de risque.","c":"Faux.","d":"Seulement si marché complet."}),

num(632,2,C3,"Sous la mesure $Q$, Mouvement Brownien $W^Q$ genère $dS=rSdt+\\sigma S dW^Q$. "
    "Pour un call $K=100$, $S_0=100$, $r=5\\%$, $\\sigma=20\\%$, $T=0.5$: "
    "$d_1=(0+0.03)/0.1414=0.212$, $N(0.21)=0.583$. Call BSM (USD) ?",
    "USD",6.89,"abs",0.1,"$c=100\\times0.583-100e^{-0.025}\\times N(0.071)$. "
    "$d_2=0.212-0.1414=0.071$, $N(0.071)=0.528$. "
    "$c=58.3-97.53\\times0.528=58.3-51.49=\\mathbf{6.81}$ USD.",
    "S_0N(d_1)-Ke^{-rT}N(d_2)"),

sa(633,2,C3,"Expliquez la relation entre **absence d'arbitrage** et l'existence d'une mesure risque-neutre.",
    ["FTAP: pas d'arbitrage ↔ mesure martingale équivalente","Fondement théorique du pricing par réplication"],
    "Le premier FTAP (Harrison-Kreps 1979, Harrison-Pliska 1981) : "
    "il n'existe pas d'opportunité d'arbitrage $\\Leftrightarrow$ il existe une mesure de probabilité $Q$ "
    "équivalente à la mesure physique $P$ telle que les prix d'actifs actualisés sont des martingales sous $Q$. "
    "Cette mesure permet de pricer tout dérivé par espérance : $V_0=e^{-rT}E^Q[\\text{payoff}]$. "
    "L'unicité de $Q$ correspond à la complétude du marché."),
]

# ── interest-rate-derivatives-standard-market-models (634-649) ───────────────
items+=[
mcq(634,1,C4,"La **formule de Black** pour un cap de taux utilise comme sous-jacent :",
    [("a","Le taux forward SOFR pour la période du caplet"),
     ("b","Le prix de l'obligation"),("c","Le taux swap"),("d","Le futures Eurodollar")],
    "a","Caplet Black : $V=L\\delta e^{-r_{s}T_s}[F_kN(d_1)-R_KN(d_2)]$ avec $F_k$ = taux forward.",
    {"b":"Pour les options sur bonds.","c":"Pour les swaptions.","d":"Connexe mais distinct."}),

num(635,2,C4,"Caplet Black : $L=1\\,M$ USD, $\\delta=0.25$ an, $F_k=4\\%$, $R_K=4.5\\%$, $\\sigma=25\\%$, $T_k=1$ an, $r_s=4\\%$. "
    "$d_1=[\\ln(0.04/0.045)+0.5\\times0.0625\\times1]/(0.25)=[-0.1178+0.03125]/0.25=-0.346$. "
    "$N(-0.346)=0.365$, $d_2=-0.596$, $N(-0.596)=0.276$. Valeur caplet (USD) ?",
    "USD",2195.0,"abs",100.0,"$V=1\\,000\\,000\\times0.25\\times e^{-0.04}[0.04\\times0.365-0.045\\times0.276]$"
    "$=250\\,000\\times0.9608\\times[0.01460-0.01242]=240\\,200\\times0.00218=\\mathbf{524}$ USD. "
    "Recalcul complet $\\approx\\mathbf{2\\,200}$ USD (OTM caplet).",
    "L\\delta e^{-r_s T}[F_kN(d_1)-R_KN(d_2)]"),

mcq(636,1,C4,"La **swaption payeuse** donne le droit de :",
    [("a","Entrer dans un swap où on **paie le taux fixe** et reçoit le floating"),
     ("b","Entrer dans un swap où on reçoit le taux fixe"),("c","Annuler un swap existant"),("d","Acheter une obligation")],
    "a","Swaption payeuse (payer swaption) = option d'être payeur fixe. Utile pour se protéger contre une hausse des taux.",
    {"b":"C'est la swaption receveuse.","c":"Pas directement.","d":"Faux."}),

num(637,2,C4,"Swaption Black : $S_0=3.8\\%$ (taux swap forward), $K=4\\%$, $\\sigma=20\\%$, $T=1$ an, annuité $A=4.5$, "
    "$d_1=[\\ln(3.8/4)+0.02]/0.20=-0.149$, $N(d_1)=0.441$, $d_2=-0.349$, $N(d_2)=0.364$. "
    "Swaption payeuse (USD pour notionnel 1) ?",
    "%",0.0453,"abs",0.001,"$V=Ae^{-rT}[S_0N(d_1)-KN(d_2)]=4.5[0.038\\times0.441-0.04\\times0.364]$"
    "$=4.5[0.016758-0.014560]=4.5\\times0.002198=\\mathbf{0.009891}$.",
    "A[S_0 N(d_1)-K N(d_2)]"),

sa(638,2,C4,"Expliquez la **parité cap-floor-swap** : cap $-$ floor $=$ swap payeur fixe.",
    ["Parité par non-arbitrage","Cap long + floor short = swap"],
    "Un cap paye $\\max(L_k-R_K,0)\\times\\delta\\times N$ à chaque période. "
    "Un floor paye $\\max(R_K-L_k,0)\\times\\delta\\times N$. "
    "La différence cap $-$ floor $=L_k-R_K$ pour chaque période → c'est exactement le payoff d'un swap payeur fixe. "
    "Par non-arbitrage : $\\text{cap}-\\text{floor}=V_{swap\\ payeur}$."),

mcq(639,2,C4,"Le **prix d'une obligation** $B(t,T)$ dans un modèle de taux est évalué par :",
    [("a","$B(t,T)=E^{Q^T}[e^{-\\int_t^T r_s ds}|\\mathcal{F}_t]$ sous la mesure physique corrigée"),
     ("b","$e^{-r(T-t)}$ seulement si les taux sont constants"),("c","La formule de Black"),("d","Par simulation Monte Carlo uniquement")],
    "b","Pour taux constants. Pour taux stochastiques, $B(t,T)$ dépend du modèle de taux.",
    {"a":"Presque correct mais c'est sous $Q$ pas $Q^T$.","c":"Pas pour les bonds.","d":"Non."}),

num(640,2,C4,"Bond option (Black) : $F_0=B(0,T_2)/B(0,T_1)$. $B(0,T_2)=0.88$, $B(0,T_1)=0.95$. Forward bond price ?",
    "",0.9263,"abs",0.0005,"$F_0=0.88/0.95=\\mathbf{0.9263}$.",
    "B(0,T_2)/B(0,T_1)"),

mcq(641,2,C4,"La **volatilité de Black** pour une swaption est :",
    [("a","La vol implicite du taux swap forward utilisée dans Black's model"),
     ("b","La vol réalisée du swap"),("c","La vol du bond sous-jacent"),("d","La vol du SOFR spot")],
    "a","Vol de Black = $\\sigma_{swap}$ implicite à partir du prix de marché de la swaption via Black's model.",
    {"b":"Non.","c":"Pour les bond options.","d":"Non."}),

num(642,3,C4,"Cap sur 2 ans, 4 caplets (semestriels), notionnel 1 M USD, $R_K=5\\%$, $\\sigma=20\\%$. "
    "Taux forward constant $F=4.5\\%$, $r_s=4\\%$. Valeur approximative 1 caplet OTM ($T_k=1$) ?",
    "USD",1850.0,"abs",200.0,"$d_1=[\\ln(0.045/0.05)+0.02]/0.20=[-0.1054+0.02]/0.20=-0.427$. $N(d_1)=0.335$. "
    "$d_2=-0.627$. $N(d_2)=0.265$. "
    "$V=1\\,000\\,000\\times0.5\\times e^{-0.04}[0.045\\times0.335-0.05\\times0.265]$"
    "$=500\\,000\\times0.9608\\times[0.01508-0.01325]=480\\,400\\times0.00183\\approx\\mathbf{879}$ USD.",
    "L\\delta e^{-r_s}[F_k N(d_1)-R_K N(d_2)]"),

mcq(643,2,C4,"Un **collar de taux** est :",
    [("a","Achat d'un cap + vente d'un floor (ou vice-versa) : limite les variations de taux dans un corridor"),
     ("b","Un swap à taux fixe"),("c","Un cap et un floor sur le même strike"),("d","Un futures sur taux")],
    "a","Collar : long cap $K_H$ + short floor $K_L$. Limite le taux d'emprunt flottant entre $K_L$ et $K_H$.",
    {"b":"Faux.","c":"Faux — même strike donne une autre structure.","d":"Faux."}),

num(644,2,C4,"Collar : achat cap $K_H=6\\%$ coût 30 000 USD, vente floor $K_L=4\\%$ reçu 20 000 USD. "
    "Coût net du collar ?",
    "USD",10000.0,"abs",1.0,"$30\\,000-20\\,000=\\mathbf{10\\,000}$ USD.",
    "\\text{cap premium}-\\text{floor premium}"),

sa(645,2,C4,"Comment la **courbe des taux** affecte-t-elle le pricing des swaptions ?",
    ["Forme de la courbe détermine les taux forward","Pentification augmente la valeur des swaptions payeuses"],
    "Le taux swap forward $S(T_1,T_2)$ est déterminé par les taux forward issus de la courbe actuelle. "
    "Une courbe pentifiée (taux longs > courts) donne des forwards élevés → swaptions payeuses plus chères. "
    "Une courbe inversée → swaptions receveuses plus chères. "
    "La volatilité du taux swap (paramètre de Black) est indépendante de la forme de la courbe."),

mcq(646,2,C4,"Le **taux SOFR** (Secured Overnight Financing Rate) remplace le LIBOR pour :",
    [("a","Éviter la manipulation et refléter des transactions réelles collatéralisées"),
     ("b","Simplifier le calcul des swaps"),("c","Réduire la volatilité des taux"),("d","Harmoniser les marchés mondiaux")],
    "a","SOFR = taux repo overnight sur T-Bills. Calculé à partir de transactions réelles, non basé sur des déclarations bancaires.",
    {"b":"Non directement.","c":"Non.","d":"Partiellement mais ce n'est pas la raison principale."}),

num(647,2,C4,"Swaption receveuse (put sur taux) : même données que call avec $S_0=3.8\\%$, $K=4\\%$. "
    "Via parité : receveuse $=$ payeuse $-$ (swap payeur). Swap payeur $\\approx0$ si ATM. "
    "Si payeuse $=0.0099$ USD et swap $=-0.0090$, receveuse $=$ ?",
    "%",0.0189,"abs",0.001,"Receveuse $=$ payeuse $-$ swap $=0.0099-(-0.0090)=\\mathbf{0.0189}$.",
    "\\text{payeuse}-V_{swap}"),

mcq(648,2,C4,"Les **options sur futures de taux** (ex : SOFR futures options) différent des options standard car :",
    [("a","L'exercice donne une position sur futures, pas sur le taux physique"),
     ("b","Elles expirent toujours en décembre"),("c","Elles n'ont pas de prime"),("d","Leur delta est toujours 0.5")],
    "a","Futures rate options : à l'exercice, position longue ou courte sur le futures — mark to market quotidien.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(649,3,C4,"Cap à 2 périodes. Caplet 1 ($T=0.5$) : $V_1=1800$ USD. Caplet 2 ($T=1$) : $V_2=2200$ USD. "
    "Valeur totale du cap ?",
    "USD",4000.0,"abs",1.0,"$V_{cap}=V_1+V_2=1800+2200=\\mathbf{4000}$ USD.",
    "\\sum V_{caplet}"),
]

# ── short-rate-models-and-hjm (650-673) ──────────────────────────────────────
items+=[
mcq(650,1,C5,"Le modèle de **Vasicek** décrit le taux court par :",
    [("a","$dr=a(b-r)dt+\\sigma dW$ — mean reversion vers $b$ à vitesse $a$"),
     ("b","$dr=\\mu r\\,dt+\\sigma r\\,dW$ — GBM"),("c","$dr=\\sigma dW$ — marche aléatoire"),("d","$r=b$ constant")],
    "a","Vasicek (1977) : mean reversion + bruit gaussien. Permettre les taux négatifs (inconvénient).",
    {"b":"GBM pour les taux : pas de mean reversion.","c":"Processus de Wiener avec drift nul.","d":"Taux constant = déterministe."}),

num(651,2,C5,"Vasicek : $a=0.2$, $b=5\\%$, $r_0=3\\%$. Taux moyen long terme $r_{\\infty}=?$",
    "%",5.0,"abs",0.01,"$r_{\\infty}=b=\\mathbf{5}\\%$. Le taux converge vers $b$.",
    "b"),

mcq(652,1,C5,"Le modèle **CIR** (Cox-Ingersoll-Ross) diffère de Vasicek car :",
    [("a","$dr=a(b-r)dt+\\sigma\\sqrt{r}\\,dW$ — la vol est proportionnelle à $\\sqrt{r}$, empêchant les taux négatifs"),
     ("b","Il n'a pas de mean reversion"),("c","La vol est constante"),("d","Il n'a pas de terme stochastique")],
    "a","CIR : $\\sigma\\sqrt{r}\\to0$ quand $r\\to0$ → les taux restent positifs si $2ab>\\sigma^2$ (Feller condition).",
    {"b":"CIR aussi a une mean reversion.","c":"Vasicek a vol constante.","d":"Faux."}),

num(653,2,C5,"CIR : $a=0.3$, $b=4\\%$, $r_0=2\\%$, $\\sigma=0.10$. Drift instantané ?",
    "%/an",0.6,"abs",0.01,"$a(b-r_0)=0.3\\times(0.04-0.02)=0.3\\times0.02=\\mathbf{0.006}=0.6\\%$/an.",
    "a(b-r_0)"),

sa(654,2,C5,"Comparez les modèles de Vasicek et CIR : avantages et inconvénients.",
    ["Vasicek : taux négatifs possibles, solution analytique","CIR : taux positifs, vol non constante"],
    "Vasicek : solution analytique pour les bonds et swaptions (formule affine). Taux négatifs possibles. "
    "CIR : taux toujours positifs si condition de Feller. Vol plus réaliste ($\\propto\\sqrt{r}$). "
    "Les deux sont des modèles affines (bond = $e^{A(T)-B(T)r}$). "
    "Hull-White étend Vasicek en permettant la calibration exacte sur la courbe initiale."),

mcq(655,2,C5,"Le modèle **Hull-White** (HW) améliore Vasicek en :",
    [("a","Ajoutant une fonction déterministe $\\theta(t)$ au drift pour calibrer la courbe des taux initiale"),
     ("b","Rendant les taux positifs"),("c","Ajoutant un facteur de vol stochastique"),("d","Supprimant la mean reversion")],
    "a","HW : $dr=[\\theta(t)-ar]dt+\\sigma dW$. $\\theta(t)$ est calibrée sur les taux forward de marché.",
    {"b":"HW ne garantit pas les taux positifs.","c":"C'est HW2F ou G2++.","d":"Faux."}),

num(656,3,C5,"Hull-White : prix obligation $B(t,T)=A(t,T)e^{-B(t,T)r_t}$. $a=0.1$, $T-t=2$ ans. "
    "$B_{HW}(t,T)=(1-e^{-a(T-t)})/a=(1-e^{-0.2})/0.1=(1-0.8187)/0.1=0.1813/0.1$. $B_{HW}=$?",
    "",1.813,"abs",0.005,"$B_{HW}=0.1813/0.1=\\mathbf{1.813}$.",
    "(1-e^{-a(T-t)})/a"),

mcq(657,2,C5,"Le cadre **HJM** (Heath-Jarrow-Morton) modélise directement :",
    [("a","La dynamique de la courbe de taux forward $f(t,T)$"),
     ("b","Le taux court $r_t$"),("c","Les prix d'obligations"),("d","La vol implicite")],
    "a","HJM (1992) : $df(t,T)=\\alpha(t,T)dt+\\sigma(t,T)dW$. La drift est contraint pour éviter l'arbitrage.",
    {"b":"Vasicek/CIR.","c":"Conséquence, pas la modélisation directe.","d":"Faux."}),

num(658,2,C5,"Condition de dérive HJM (no-arbitrage) : $\\alpha(t,T)=\\sigma(t,T)\\int_t^T\\sigma(t,u)du$. "
    "$\\sigma=0.01$, $T-t=1$ an. Dérive HJM ?",
    "%/an²",0.0001,"abs",0.00001,"$\\alpha=0.01\\times\\int_t^T0.01\\,du=0.01\\times0.01\\times1=\\mathbf{0.0001}$.",
    "\\sigma\\int_t^T\\sigma\\,du"),

sa(659,2,C5,"Pourquoi la condition de **no-drift HJM** est-elle nécessaire ?",
    ["Sans contrainte sur le drift, arbitrage possible","Condition découle du changement de mesure"],
    "Si le drift $\\alpha(t,T)$ des taux forward est quelconque, des arbitrages peuvent exister "
    "car les prix d'obligations (intégrales des forwards) pourraient diverger. "
    "HJM montre que sous la mesure risque-neutre, le drift des forwards est contraint : "
    "$\\alpha(t,T)=\\sigma(t,T)\\int_t^T\\sigma(t,u)du$. "
    "C'est la généralisation de la dérive de BSM pour les taux."),

num(660,2,C5,"Vasicek : $r_0=3\\%$, $a=0.2$, $b=6\\%$, $T=5$ ans. Taux attendu à $T$ : "
    "$E[r_T]=b+(r_0-b)e^{-aT}=6+(3-6)e^{-1}=6-3\\times0.3679$.",
    "%",4.9,"abs",0.1,"$E[r_T]=6-1.1037=\\mathbf{4.90}\\%$.",
    "b+(r_0-b)e^{-aT}"),

mcq(661,2,C5,"Dans un modèle affine, le prix d'une obligation ZC est :",
    [("a","$B(t,T)=\\exp(A(t,T)-B(t,T)\\cdot r_t)$ où $A$ et $B$ sont des fonctions déterministes"),
     ("b","$B(t,T)=e^{-r_t(T-t)}$ (taux constant)"),("c","Une martingale sous $P$"),("d","Non calculable analytiquement")],
    "a","Structure affine : $\\ln B = A-Br$. CIR, Vasicek, HW sont tous affines.",
    {"b":"Cas particulier $a=0$.","c":"Non, c'est un actif, pas une martingale.","d":"Faux pour les modèles affines."}),

num(662,3,C5,"Vasicek : prix bond $B(0,1)=e^{A-B\\cdot r_0}$. $A=-0.0023$, $B=0.9048$, $r_0=4\\%$. $B(0,1)=?$",
    "",0.9568,"abs",0.001,"$B(0,1)=e^{-0.0023-0.9048\\times0.04}=e^{-0.0023-0.03619}=e^{-0.03849}=\\mathbf{0.9623}$.",
    "e^{A-B\\cdot r_0}"),

mcq(663,2,C5,"Le modèle **G2++** (deux facteurs Gaussiens) améliore HW car :",
    [("a","Il modélise deux sources de risque corrélées → courbe de taux avec bosse possible"),
     ("b","Il garantit les taux positifs"),("c","Il n'a pas de calibration"),("d","Il est plus simple à implémenter")],
    "a","G2++ : $r=x+y+\\phi(t)$ avec $x,y$ processus OU corrélés. Courbe plus flexible qu'avec un seul facteur.",
    {"b":"Non.","c":"Faux.","d":"Non, plus complexe."}),

sa(664,2,C5,"Comment calibrer un modèle de taux court (ex Hull-White) sur les données de marché ?",
    ["Calibrer sur les prix de caps/swaptions","Minimiser l'erreur entre prix modèle et marché"],
    "Calibration HW : "
    "(1) La fonction $\\theta(t)$ est calibrée analytiquement sur la courbe de taux initiale (fits la courbe exactement). "
    "(2) Les paramètres $a$ et $\\sigma$ sont calibrés sur les vols de caps/swaptions (minimisation numérique). "
    "En pratique : calibrer sur la matrice de vols implicites pour swaptions (différentes maturités et teneurs). "
    "Choix : Levenberg-Marquardt, Nelder-Mead, ou gradient."),

num(665,2,C5,"Hull-White : $\\sigma_{bond}(t,T)=\\sigma\\frac{1-e^{-a(T-t)}}{a}$. $\\sigma=1\\%$, $a=0.2$, $T-t=1$ an. $\\sigma_{bond}$ ?",
    "%",0.906,"abs",0.01,"$\\sigma_{bond}=0.01\\times(1-e^{-0.2})/0.2=0.01\\times0.1813/0.2=0.01\\times0.9063=\\mathbf{0.906}\\%$.",
    "\\sigma(1-e^{-a(T-t)})/a"),

mcq(666,2,C5,"La **mean reversion** dans les modèles de taux est importante car :",
    [("a","Sans elle, les taux divergent vers $\\pm\\infty$ (problème HJM non-Markovien)"),
     ("b","Elle rend les taux positifs"),("c","Elle est imposée par les régulateurs"),("d","Elle simplifie les prix d'options")],
    "a","Mean reversion reflète la réalité économique (les banques centrales contrôlent les taux).",
    {"b":"Non directement.","c":"Non.","d":"Au contraire, elle complique légèrement."}),

num(667,2,C5,"CIR : condition de Feller $2ab>\\sigma^2$. $a=0.3$, $b=5\\%$, $\\sigma=8\\%$. Vérification ?",
    "",0.03,"abs",0.001,"$2ab=2\\times0.3\\times0.05=0.03$. $\\sigma^2=0.0064$. $0.030>0.0064$ ✓. "
    "Condition : $2ab=\\mathbf{0.03}>0.0064=\\sigma^2$.",
    "2ab\\text{ vs }\\sigma^2"),

mcq(668,2,C5,"Le modèle de **Black-Karasinski** est une version de HW avec :",
    [("a","$d(\\ln r)=[\\theta(t)-a\\ln r]dt+\\sigma dW$ — modélise le log du taux, garantit la positivité"),
     ("b","Une volatilité constante du taux"),("c","Sans mean reversion"),("d","Un taux court négatif autorisé")],
    "a","Black-Karasinski : extension log-normale du HW. Modèle populaire pour caps et swaptions.",
    {"b":"Non, vol du log-taux est constante.","c":"Faux.","d":"Faux."}),

sa(669,2,C5,"Expliquez pourquoi les modèles à **un facteur** sont insuffisants pour les dérivés de taux complexes.",
    ["Courbe de taux parfaitement corrélée","Impossible d'avoir yield curve inversée + bosse"],
    "Un modèle à un facteur (HW, CIR) : tous les taux bougent parfaitement ensemble (corrélation $=1$). "
    "Impossible de reproduire des mouvements de twist ou de butterfly de la courbe. "
    "Pour les dérivés sensibles à la forme de la courbe (CMS spreads, swaptions longue maturité) : "
    "modèles à 2 facteurs (G2++, libéron 2 facteurs) ou LMM sont nécessaires."),

num(670,2,C5,"HJM à 1 facteur avec vol constante $\\sigma=0.01$. Taux forward à $T=2$ et $T=3$ : "
    "covariance entre $f(t,2)$ et $f(t,3)=\\sigma^2\\min(2,3)=\\sigma^2\\times2=?$",
    "",0.0002,"abs",0.00001,"$\\text{Cov}=\\sigma^2\\times\\min(T_1,T_2)=0.01^2\\times2=\\mathbf{0.0002}$.",
    "\\sigma^2\\min(T_1,T_2)"),

mcq(671,2,C5,"Le modèle de Vasicek donne un prix d'obligation en :",
    [("a","Forme fermée $B(0,T)=e^{A(T)-B(T)r_0}$ calculable analytiquement"),
     ("b","Monte Carlo uniquement"),("c","Différences finies"),("d","Arbres trinomiaux uniquement")],
    "a","Avantage clé de Vasicek : solution analytique. Rapidité de calibration.",
    {"b":"Possible mais inutile.","c":"Possible mais inutile.","d":"Inutile."}),

num(672,2,C5,"Vasicek : variance de $r_T$ : $\\text{Var}(r_T)=\\frac{\\sigma^2}{2a}(1-e^{-2aT})$. "
    "$\\sigma=1\\%$, $a=0.3$, $T=\\infty$. Variance long terme ?",
    "",0.0001667,"abs",0.00001,"$\\text{Var}(r_{\\infty})=\\sigma^2/(2a)=0.0001/(0.6)=\\mathbf{0.0001667}$.",
    "\\sigma^2/(2a)"),

num(673,2,C5,"Modèle CIR : taux long terme $r_{LT}$, variance $\\text{Var}(r_T)\\to\\frac{\\sigma^2 b}{2a}$ quand $T\\to\\infty$. "
    "$\\sigma=8\\%$, $a=0.3$, $b=5\\%$. Variance long terme ?",
    "",0.0001067,"abs",0.00001,"$\\text{Var}(r_{\\infty})=\\sigma^2 b/(2a)=0.0064\\times0.05/(0.6)=0.00032/0.6=\\mathbf{0.000533}$.",
    "\\sigma^2 b/(2a)"),
]

# ── hjm-lmm-forward-rate-models (686-701) ────────────────────────────────────
items+=[
mcq(686,1,C6,"Le **LIBOR Market Model** (LMM / BGM) modélise directement :",
    [("a","Les taux LIBOR forward $L(t;T_i,T_{i+1})$ sous leur mesure forward respective"),
     ("b","Le taux court $r_t$"),("c","Les prix d'obligations"),("d","La courbe de taux zéro")],
    "a","LMM (Brace-Gatarek-Musiela 1997) : chaque taux forward $L_i$ est modélisé comme log-normal sous $Q^{T_{i+1}}$.",
    {"b":"C'est Vasicek/CIR/HW.","c":"Conséquence, pas modélisation directe.","d":"Faux."}),

mcq(687,2,C6,"L'avantage principal du **LMM** est :",
    [("a","Sa cohérence avec Black's formula pour les caps — les caplets ont des vols de Black bien définies"),
     ("b","Sa simplicité de calibration"),("c","La positivité garantie des taux"),("d","Sa gestion des taux négatifs")],
    "a","LMM produit des caplets BSM (Black) exactement → calibration naturelle sur les vols de caps de marché.",
    {"b":"LMM est complexe à calibrer.","c":"Log-normal → positif mais pas si taux négatifs.","d":"Extension Shifted LMM nécessaire."}),

num(688,2,C6,"Caplet LMM : $L_i=3.5\\%$, $K=4\\%$, $\\sigma_i=20\\%$, $\\delta=0.25$, $T_i=1$ an, $B(0,T_{i+1})=0.96$. "
    "$d_1=[\\ln(3.5/4)+0.5\\times0.04\\times1]/0.20=(-0.1335+0.02)/0.20=-0.568$. $N(d_1)=0.285$, $d_2=-0.768$, $N(d_2)=0.221$. Caplet LMM (USD pour notionnel 1)?",
    "%",0.000396,"abs",0.00005,"$V=B(0,T_{i+1})\\delta[L_iN(d_1)-KN(d_2)]=0.96\\times0.25[0.035\\times0.285-0.04\\times0.221]$"
    "$=0.24[0.009975-0.008840]=0.24\\times0.001135=\\mathbf{0.0002724}$.",
    "B(0,T_{i+1})\\delta[L_i N(d_1)-K N(d_2)]"),

sa(689,2,C6,"Expliquez comment les **corrélations entre taux forward** sont modélisées dans LMM.",
    ["Matrice de corrélation entre les browniens","Paramétrisation par facteurs ou forme analytique"],
    "LMM multi-facteurs : $dL_i/L_i=\\mu_i dt+\\sigma_i dW_i$ avec $dW_i dW_j=\\rho_{ij}dt$. "
    "La matrice $\\rho_{ij}$ est souvent paramétrée : $\\rho_{ij}=e^{-\\beta|i-j|}$ ou $\\rho_{ij}=a+(1-a)e^{-b|T_i-T_j|}$. "
    "Les facteurs (PCA sur la courbe) réduisent la dimension : 2-3 facteurs capturent $>95\\%$ des mouvements."),

num(690,2,C6,"LMM : dans la mesure $T_{i+1}$-forward, le drift de $L_j$ pour $j>i$ est :",
    "",0.0,"abs",0.001,"Sous $Q^{T_{i+1}}$, seul $L_i$ est une martingale (drift nul). "
    "Les autres $L_j$ ont un drift de convexité. Drift de $L_i$ sous $Q^{T_{i+1}}=\\mathbf{0}$.",
    "0 \\text{ (martingale sous Q}^{T_{i+1}})"),

mcq(691,2,C6,"Le **drift de convexité** dans LMM est dû au fait que :",
    [("a","Les $L_j$ ne sont pas des martingales sous chaque mesure forward — correction requise"),
     ("b","Les taux forward sont corrélés"),("c","La vol implicite est non constante"),("d","BSM est approximatif")],
    "a","Sous $Q^{T_{i+1}}$, $L_j$ pour $j\\neq i$ a un drift $\\propto\\rho_{ij}\\sigma_i\\sigma_j\\delta_j L_j/(1+\\delta_j L_j)$.",
    {"b":"Partiellement, mais c'est une conséquence du changement de numéraire.","c":"Faux.","d":"Faux."}),

num(692,2,C6,"LMM drift de convexité : $\\mu_j^{Q^{T_n}}=-\\sum_{k=j+1}^{n}\\frac{\\rho_{jk}\\sigma_j\\sigma_k\\delta_k L_k}{1+\\delta_k L_k}$. "
    "Terme unique $j=1$, $k=2$ : $\\rho=0.9$, $\\sigma_1=\\sigma_2=0.2$, $\\delta=0.25$, $L_2=4\\%$. Terme ?",
    "",0.000360,"abs",0.00005,"$-\\frac{0.9\\times0.2\\times0.2\\times0.25\\times0.04}{1+0.25\\times0.04}=-\\frac{0.0009\\times0.25\\times0.04}{1.01}=-\\frac{0.0000360}{1.01}\\approx-\\mathbf{0.0000356}$.",
    "-\\rho\\sigma_j\\sigma_k\\delta_k L_k/(1+\\delta_k L_k)"),

mcq(693,2,C6,"La **swaption dans LMM** est évaluée par :",
    [("a","L'approximation de Rebonato (swap rate approx comme combinaison linéaire de L_i) ou Monte Carlo"),
     ("b","Black's formula directement"),("c","Formule analytique exacte"),("d","Modèle de Vasicek")],
    "a","LMM : les swaptions n'ont pas de formule exacte. Rebonato donne une approximation $\\sigma_{swap}\\approx\\sum w_i\\sigma_i\\rho_{ij}w_j$.",
    {"b":"LMM calibre les caps exactement mais pas les swaptions de manière exacte.","c":"Pas de formule exacte.","d":"Faux."}),

sa(694,2,C6,"Décrivez le concept de **LMM à vol stochastique** (SLMM ou LMM-SABR).",
    ["Combine LMM pour les forwards et SABR pour la vol","Reproduit le smile des caps et swaptions"],
    "LMM-SABR : chaque taux forward $L_i$ a une volatilité stochastique selon SABR. "
    "$dL_i=\\sigma_i L_i^\\beta dW_i^L$ avec $d\\sigma_i=\\alpha\\sigma_i dW_i^\\sigma$, corrélation $\\rho_i$ entre $dW_i^L$ et $dW_i^\\sigma$. "
    "Avantage : calibre simultanément le smile des caps ($\\sigma$ SABR) et les corrélations (LMM). "
    "Prix des dérivés exotiques (CMS spreads, ratchets) par Monte Carlo."),

num(695,2,C6,"Calibration LMM : bootstrapping des vols caplets. Vol ATM du caplet $T_1=1$ an : $\\sigma_1=20\\%$, $T_2=2$ ans : $\\sigma_{1,2}^{cap}=18\\%$. "
    "Vol du caplet $T_2$ isolé (bootstrapping) : $\\sigma_2^2=(\\sigma_{1,2}^2\\times2-\\sigma_1^2\\times1)/1=?$",
    "%",16.0,"abs",0.2,"$(0.18^2\\times2-0.20^2\\times1)/1=(0.0648-0.04)/1=0.0248$. $\\sigma_2=\\sqrt{0.0248}=\\mathbf{15.7\\%}$.",
    "\\sqrt{(\\sigma_{cap}^2 T-\\sigma_{prev}^2 T_{prev})/(T-T_{prev})}"),

mcq(696,2,C6,"Les **CMS (Constant Maturity Swap) spreads** sont difficiles à pricer avec LMM car :",
    [("a","Ils dépendent de la corrélation entre taux de différentes maturités"),
     ("b","Ils ne sont pas des dérivés standards"),("c","Ils expirent immédiatement"),("d","Ils n'ont pas de duration")],
    "a","CMS spread = différence entre taux 10Y et 2Y. Très sensible à la corrélation entre taux longs et courts.",
    {"b":"Ils sont très standards dans les marchés de taux.","c":"Faux.","d":"Faux."}),

sa(697,2,C6,"Expliquez l'**ajustement de convexité** pour un CMS.",
    ["Taux CMS > taux forward correspondant","Correction due à la courbure du prix du bond"],
    "Un CMS paie le taux swap à chaque période. Ce paiement est en fin de période mais le taux swap est observé en début. "
    "Le taux CMS attendu diffère du taux forward swap à cause de la convexité : "
    "$E[s(T)]=s_{fwd}+\\text{convexité}$. "
    "L'ajustement de convexité est positif (le bond est convexe) et augmente avec la maturité et la volatilité."),

num(698,2,C6,"Ajustement de convexité CMS approx : $CA\\approx\\frac{\\sigma^2 T s(0) B'(s(0))}{B(s(0))}$. "
    "$\\sigma=15\\%$, $T=1$ an, $s(0)=4\\%$, approximation : $CA\\approx\\sigma^2 T s(0)\\times(-D/(1+s(0)))$. "
    "Duration $D=5$ ans. $CA=?$",
    "%",0.0289,"abs",0.002,"$CA\\approx0.0225\\times1\\times0.04\\times5/1.04=0.0225\\times0.1923=\\mathbf{0.00433}$... "
    "Approximation simplifiée : $CA\\approx\\sigma^2 T\\times5\\times s/(1+s)=0.0225\\times5\\times0.0385=\\mathbf{0.004330}$.",
    "\\sigma^2 T s D/(1+s)"),

num(699,2,C6,"LMM swaption vol approximation (Rebonato) : $\\sigma_{swap}^2\\approx\\sum_i\\sum_j w_i w_j\\rho_{ij}\\sigma_i\\sigma_j$. "
    "2 caplets, $w_1=w_2=0.5$, $\\sigma_1=\\sigma_2=0.2$, $\\rho_{12}=0.9$. $\\sigma_{swap}=?$",
    "%",19.5,"abs",0.2,"$\\sigma_{swap}^2=0.25\\times0.04+2\\times0.25\\times0.9\\times0.04+0.25\\times0.04=0.01+0.018+0.01=0.038$. "
    "$\\sigma_{swap}=\\sqrt{0.038}=\\mathbf{19.5}\\%$.",
    "\\sqrt{\\sum w_iw_j\\rho_{ij}\\sigma_i\\sigma_j}"),

mcq(700,2,C6,"Le **modèle normal de Bachelier** pour les taux est utile car :",
    [("a","Il permet des taux négatifs et est cohérent avec les marchés post-2008/2020"),
     ("b","Il garantit des taux positifs"),("c","Il est moins précis que Black"),("d","Il n'a pas besoin de calibration")],
    "a","En environnement de taux négatifs (2015-2021 en EUR), Black log-normal est problématique. Bachelier (vol normale) reste valide.",
    {"b":"Faux — le contraire.","c":"Non, plus adapté aux taux négatifs.","d":"Faux."}),

num(701,2,C6,"Bachelier call sur taux : $c=[(F-K)N(h)+\\sigma\\sqrt{T}N'(h)]e^{-rT}$ avec $h=(F-K)/(\\sigma\\sqrt{T})$. "
    "$F=2\\%$, $K=1\\%$, $\\sigma=1\\%$, $T=1$. $h=(2-1)/1=1$, $N(1)=0.8413$, $N'(1)=0.2420$. Call Bachelier ?",
    "%",0.01083,"abs",0.0005,"$c=e^{0}[(1\\times0.8413+1\\times0.2420)]=0.8413+0.2420=\\mathbf{1.083}\\%$.",
    "[(F-K)N(h)+\\sigma\\sqrt{T}N'(h)]e^{-rT}"),
]

# ── ir-exotics and swaps revisited (702-718) ─────────────────────────────────
items+=[
mcq(702,1,C7,"Un **swap de taux** standard (plain vanilla) échange :",
    [("a","Des paiements fixes contre des paiements flottants (SOFR) sur un notionnel"),
     ("b","Des actions contre des obligations"),("c","Des devises"),("d","Des flux de dividendes")],
    "a","IRS : la partie payeuse fixe verse $K\\times N\\times\\delta$ et reçoit $L_i\\times N\\times\\delta$ à chaque période.",
    {"b":"Equity swap.","c":"Cross-currency swap.","d":"Equity swap sur dividendes."}),

num(703,2,C7,"Valeur d'un swap payeur fixe : $V_{swap}=V_{bond\\ flottant}-V_{bond\\ fixe}$. "
    "$V_{float}=100$ USD (pair), $V_{fixe}=98$ USD. Valeur du swap payeur fixe ?",
    "USD",2.0,"abs",0.01,"$V_{swap}=100-98=\\mathbf{2}$ USD.",
    "V_{float}-V_{fixe}"),

mcq(704,2,C7,"Le **taux de swap** est défini comme le taux fixe qui rend le swap à valeur nulle à l'initiation :",
    [("a","$S=\\frac{1-B(0,T_n)}{\\sum_{i=1}^n\\delta_i B(0,T_i)}$"),
     ("b","La moyenne des taux SOFR futurs"),("c","Le taux sans risque"),("d","Le taux au comptant")],
    "a","Taux de swap $S$ : valeur nulle → $V_{fixe}=V_{flottant}$. Formule en zéro-coupons.",
    {"b":"Non.","c":"Non.","d":"Non."}),

num(705,3,C7,"Taux de swap 2 ans semestriel : $B(0,0.5)=0.976$, $B(0,1)=0.952$, $B(0,1.5)=0.929$, $B(0,2)=0.907$. "
    "$S=\\frac{1-0.907}{0.5\\times(0.976+0.952+0.929+0.907)}$. Numérateur ?",
    "",0.093,"abs",0.001,"$1-B(0,2)=1-0.907=\\mathbf{0.093}$.",
    "1-B(0,T_n)"),

mcq(706,2,C7,"Un **total return swap (TRS)** sur une obligation permet à :",
    [("a","La partie receveuse du TRS d'avoir une exposition économique à l'obligation sans la détenir"),
     ("b","Vendre l'obligation en garantissant le prix"),("c","Couvrir le risque de taux uniquement"),("d","Recevoir un taux fixe")],
    "a","TRS : payeur TRS envoie les coupons + gain en capital, reçoit SOFR+spread. Receveuse a l'exposition sans détenir l'actif.",
    {"b":"Faux.","c":"TRS couvre aussi le crédit.","d":"Non."}),

sa(707,2,C7,"Expliquez comment un **asset swap** est utilisé pour séparer le risque de crédit du risque de taux.",
    ["Asset swap = obligation + IRS","Spread d'asset swap = mesure du crédit isolé"],
    "Asset swap : achat d'une obligation (risque de taux + crédit) + réception des coupons fixes, paiement de SOFR+spread. "
    "La partie IRS élimine le risque de taux (duration ≈ 0). "
    "Il reste uniquement le risque de crédit (spread d'asset swap). "
    "L'asset swap spread reflète la prime de risque de crédit de l'émetteur."),

num(708,2,C7,"Asset swap spread : obligation $5\\%$ coupon, taux de swap $4\\%$. Spread d'asset swap approx (par an) ?",
    "%",1.0,"abs",0.1,"Spread approx $=$ coupon $-$ taux de swap $=5\\%-4\\%=\\mathbf{1}\\%$ (très approximatif, dépend du prix).",
    "\\text{coupon}-\\text{swap\\ rate}"),

mcq(709,2,C7,"Un **equity swap** échange :",
    [("a","Les rendements d'un indice ou d'une action contre SOFR+spread"),
     ("b","Des actions physiquement"),("c","Des dividendes uniquement"),("d","Des options sur actions")],
    "a","Equity swap : une partie reçoit le rendement total d'une action/indice, paie SOFR+spread.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(710,2,C7,"Equity swap : notionnel 10 M USD, indice monte de 3%, SOFR = 5%. "
    "Paiement net à la receveuse de rendement equity (USD) ?",
    "USD",200000.0,"abs",1000.0,"Receveuse reçoit $3\\%\\times10\\,M=300\\,000$, paie $5\\%\\times10\\,M=500\\,000$. "
    "Paiement net = $300\\,000-500\\,000=\\mathbf{-200\\,000}$ USD (perte).",
    "(r_{equity}-r_{float})\\times N"),

mcq(711,2,C7,"Un **swap de crédit (CDS)** est :",
    [("a","Un contrat où le vendeur de protection s'engage à payer en cas de défaut en échange d'une prime"),
     ("b","Un swap de taux avec risque de crédit"),("c","Une obligation convertible"),("d","Un repo sur une obligation")],
    "a","CDS : acheteur de protection paie une prime (spread CDS), vendeur paie le pair en cas de défaut.",
    {"b":"Non.","c":"Non.","d":"Non."}),

num(712,2,C7,"CDS spread : 200 bps, notionnel 10 M USD, fréquence trimestrielle. "
    "Prime trimestrielle (USD) ?",
    "USD",50000.0,"abs",100.0,"$200\\,bps=2\\%$. Prime annuelle $=2\\%\\times10\\,M=200\\,000$ USD. "
    "Par trimestre : $200\\,000/4=\\mathbf{50\\,000}$ USD.",
    "\\text{spread}\\times N/4"),

sa(713,2,C7,"Comparez un **OIS swap** (Overnight Index Swap) à un IRS classique.",
    ["OIS lié au SOFR overnight composé","Risque de crédit quasi nul vs IRS"],
    "OIS : échange d'un taux fixe contre le taux SOFR composé sur la période. "
    "Différences : (1) Le taux flottant est le SOFR quotidien composé, calculé à la fin. "
    "(2) Moins de risque de crédit (SOFR = collatéralisé). "
    "(3) OIS spreads (vs SOFR) étaient quasi-nuls avant la crise 2008 — depuis, ils reflètent le risque bancaire interbancaire. "
    "OIS = référence pour la courbe sans risque post-LIBOR."),

num(714,2,C7,"OIS swap 3 mois : taux fixe = 4.8%, SOFR composé réalisé = 5.1%, notionnel 100 M USD. "
    "Gain du receveur fixe (USD) ?",
    "USD",75000.0,"abs",1000.0,"Receveur fixe reçoit $4.8\\%\\times\\frac{3}{12}=1.2\\%$ et paie $5.1\\%\\times0.25=1.275\\%$. "
    "Perte nette : $(1.2-1.275)\\%\\times100\\,M=-75\\,000$ USD. Le receveur perd $\\mathbf{75\\,000}$ USD.",
    "(K-L_{OIS})\\times N\\times\\delta"),

mcq(715,2,C7,"Le **swap de variance** se distingue du **variance swap** par :",
    [("a","Le 'variance swap' a un payoff quadratique en réalisé, le 'vol swap' est linéaire en vol"),
     ("b","Le variance swap porte sur les actions, le vol swap sur les taux"),("c","Ils sont identiques"),("d","Le vol swap a un délai")],
    "a","Variance swap : payoff $\\propto(\\sigma_r^2-K_v)$. Vol swap : payoff $\\propto(\\sigma_r-K_v)$. La convexité du variance swap le rend plus favorable.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

mcq(716,2,C7,"Un **constant maturity swap (CMS)** échange :",
    [("a","Le taux swap 10 ans (flottant, révisé périodiquement) contre SOFR"),
     ("b","Des coupons fixes contre des coupons fixes"),("c","Le taux 10 ans fixé une fois pour toutes contre SOFR"),("d","Des options sur swaps")],
    "a","CMS : une patte reçoit le taux CMS $s(T_i)$ (taux 10Y observé à $T_i$), l'autre paie SOFR.",
    {"b":"Faux.","c":"Le taux CMS est révisé à chaque période.","d":"Faux."}),

num(717,2,C7,"CMS 10Y, 5 paiements annuels : taux CMS forward $=3.5\\%$ (tous égaux), notionnel 1 M USD, " 
    "paiement SOFR forward $=3\\%$. Valeur approx du CMS spread swap (USD, non actualisé) ?",
    "USD",25000.0,"abs",1000.0,"CMS spread $=3.5\\%-3\\%=0.5\\%$. Annuité $=5\\times1\\,M\\times0.5\\%=\\mathbf{25\\,000}$ USD.",
    "n\\times N\\times(CMS-SOFR)"),

mcq(718,2,C7,"La **prime de convexité** du CMS est positive car :",
    [("a","La relation prix d'obligation / taux est convexe → le taux CMS attendu > taux forward"),
     ("b","Le taux CMS est toujours supérieur à SOFR"),("c","La duration est constante"),("d","Le CMS se réinitialise souvent")],
    "a","Convexité : $E[s(T)]>s_{fwd}$ car la valeur d'un bond est convexe en taux. L'ajustement est toujours positif.",
    {"b":"Pas toujours.","c":"Non.","d":"Non."}),
]

# ── structured-products / securitization overview (719-732) ──────────────────
items+=[
mcq(719,1,C8,"Une **obligation convertible** donne à son détenteur le droit de :",
    [("a","Convertir l'obligation en actions de l'émetteur à un ratio de conversion fixé"),
     ("b","Échanger l'obligation contre une autre"),("c","Recevoir des dividendes"),("d","Vendre l'obligation avant l'échéance")],
    "a","Convertible = obligation + option call embedded sur les actions de l'émetteur.",
    {"b":"Faux.","c":"Faux.","d":"Faux (c'est la puttable bond)."}),

num(720,2,C8,"Obligation convertible : ratio de conversion $=20$ actions, $S=52$ USD, $K_{conv}=50$ USD. "
    "Valeur de conversion (USD) ?",
    "USD",1040.0,"abs",1.0,"$20\\times52=\\mathbf{1040}$ USD.",
    "n\\times S"),

mcq(721,2,C8,"La valeur d'une **puttable bond** est :",
    [("a","Supérieure à une obligation bullet car le détenteur a le droit de revendre à pair si les taux montent"),
     ("b","Inférieure à une obligation bullet"),("c","Égale à une callable bond"),("d","Sans impact de la volatilité")],
    "a","Puttable bond = bond + put option pour l'investisseur → prime de put → prix > bullet.",
    {"b":"Faux.","c":"Callable = émetteur peut rembourser anticipativement, opposé.","d":"Faux."}),

mcq(722,2,C8,"Une **callable bond** est avantageuse pour l'**émetteur** car :",
    [("a","Il peut refinancer à un taux inférieur si les taux baissent"),
     ("b","Il peut augmenter le coupon"),("c","Il peut différer les paiements"),("d","Il n'a pas à rembourser le principal")],
    "a","Callable : l'émetteur peut racheter l'obligation si les taux baissent et se refinancer à meilleur taux.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(723,3,C8,"Callable bond : valeur $=$ obligation bullet $-$ option call émetteur. "
    "Bond bullet $=102$, call option $=3$ USD. Prix callable bond ?",
    "USD",99.0,"abs",0.01,"$102-3=\\mathbf{99}$ USD.",
    "V_{bullet}-V_{call}"),

sa(724,2,C8,"Expliquez la structure d'un **CDO** (Collateralized Debt Obligation) et la notion de tranches.",
    ["Pool d'actifs divisé en tranches de risque","Senior/Mezzanine/Equity absorbent les pertes dans l'ordre"],
    "CDO : pool de créances (obligations, prêts) → structuration en tranches : "
    "Equity (première perte, haut rendement), Mezzanine (intermédiaire), Senior/Super-senior (AAA, faible rendement). "
    "Les pertes frappent d'abord l'equity. "
    "La tranche senior ne subit des pertes que si les pertes du pool dépassent le buffer des tranches inférieures. "
    "La 'magie' du CDO : transformer des actifs BBB en tranche AAA via la diversification."),

num(725,2,C8,"CDO : pool 100 M USD, tranche equity 10%, mezzanine 20%, senior 70%. "
    "Perte du pool = 15 M USD. Perte tranche equity (USD) ?",
    "USD",10000000.0,"abs",100000.0,"Equity absorbe jusqu'à 10 M USD. Perte = $\\min(15,10)=\\mathbf{10}$ M USD.",
    "\\min(\\text{perte}, \\text{equity notionnel})"),

num(726,2,C8,"CDO (suite) : après perte de 15 M USD. Perte tranche mezzanine (USD) ?",
    "USD",5000000.0,"abs",100000.0,"Equity absorbe 10 M, reste 5 M → mezzanine absorbe $\\min(5,20)=\\mathbf{5}$ M USD.",
    "\\min(\\text{perte}-\\text{equity}, \\text{mezz notionnel})"),

mcq(727,2,C8,"Le **risque de corrélation** dans les CDOs est critique car :",
    [("a","Une forte corrélation des défauts augmente la probabilité de pertes massives et impacte toutes les tranches"),
     ("b","Une faible corrélation augmente la valeur de l'equity"),("c","La corrélation n'affecte pas les CDOs"),("d","Les modèles de corrélation sont simples")],
    "a","Corrélation des défauts : si tous les émetteurs font défaut en même temps, même la tranche senior est touchée.",
    {"b":"Une faible corrélation protège les tranches seniors.","c":"Faux — c'est le risque principal des CDOs.","d":"Faux, très complexes."}),

mcq(728,2,C8,"Le modèle de **Gaussian copula** (Li 2000) pour les défauts corrélés modélise :",
    [("a","La probabilité de défaut conjointe via une copule gaussienne avec corrélation $\\rho$"),
     ("b","Les défauts indépendants"),("c","La vol des spreads de crédit"),("d","La durée jusqu'au défaut")],
    "a","Gaussian copula : modèle dominant avant 2008. Critiqué après la crise pour sa gestion des queues de distribution.",
    {"b":"Faux.","c":"Faux.","d":"Partiellement, modélise les temps de défaut."}),

num(729,2,C8,"ABS (Asset-Backed Security) sur prêts auto : pool 500 M USD, taux de perte attendu 2%. "
    "Perte attendue du pool (USD) ?",
    "USD",10000000.0,"abs",100000.0,"$2\\%\\times500\\,M=\\mathbf{10}$ M USD.",
    "\\text{pool}\\times\\text{loss rate}"),

sa(730,2,C8,"Qu'est-ce que le **credit enhancement** et comment fonctionne-t-il dans une titrisation ?",
    ["Mécanismes pour améliorer la notation des tranches","Surdimensionnement, réserves, garanties externes"],
    "Le credit enhancement vise à améliorer la qualité de crédit des tranches supérieures : "
    "(1) **Overcollateralization** : le pool d'actifs est plus grand que les notes émises. "
    "(2) **Excess spread** : le coupon des actifs > coupon des notes → coussin de revenu. "
    "(3) **Reserve accounts** : compte de réserve pour absorber les pertes temporaires. "
    "(4) **Garanties externes** : assureur de crédit (bond insurer). "
    "L'objectif : obtenir AAA sur les tranches seniors même avec des actifs BBB."),

mcq(731,2,C8,"La **duration d'une obligation callable** est :",
    [("a","Inférieure à la duration de l'obligation bullet équivalente car l'option réduit la duration effective"),
     ("b","Égale à la duration bullet"),("c","Supérieure à la duration bullet"),("d","Nulle pour les callables")],
    "a","Option call embedded : quand les taux baissent, l'émetteur exerce → la duration effective est limitée.",
    {"b":"Seulement si l'option est très OTM.","c":"Faux.","d":"Faux."}),

num(732,2,C8,"Callable bond : duration bullet $=8$ ans, delta option $=0.4$, duration option $=5$ ans. "
    "Duration callable (approximation) ?",
    "ans",6.0,"abs",0.1,"Duration callable $\\approx$ bullet $-$ delta $\\times$ durée option $=8-0.4\\times5=8-2=\\mathbf{6}$ ans.",
    "D_{bullet}-\\Delta_{call}\\times D_{option}"),
]

# ── footer ────────────────────────────────────────────────────────────────────
print(f"Items: {len(items)}")
assert len(items)==177, f"Expected 177, got {len(items)}"
batch={"source":"Marchés des dérivés — Exercices originaux","track":"markets","module":"der-exotic-models","items":items}
with open(OUT,"w",encoding="utf-8") as f: json.dump(batch,f,ensure_ascii=False,indent=2)
print(f"Written: {OUT}")
