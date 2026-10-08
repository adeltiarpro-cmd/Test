#!/usr/bin/env python3
"""batch-002-5: der-bsm-pricing (124 items, clés 275-295,296-310,311-337,338-349,350-375,376-398)"""
import json,os,math
OUT=os.path.join(os.path.dirname(__file__),"../canonical/batch-002-5-der-bsm-pricing.json")
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
# N(x) approximation table for MCQ reference
# N(0.2)=0.5793, N(-0.2)=0.4207, N(0.4)=0.6554, N(-0.4)=0.3446
# N(0.6)=0.7257, N(-0.6)=0.2743, N(1.0)=0.8413, N(-1.0)=0.1587
# N(0.5)=0.6915, N(-0.5)=0.3085, N(0.3)=0.6179, N(-0.3)=0.3821

C1="binomial-trees"; C2="wiener-processes-and-it-s-lemma"; C3="the-black-scholes-merton-model"
C4="employee-stock-options"; C5="options-on-stock-indices-and-currencies"; C6="futures-options-and-black-s-model"

items=[
# ── binomial-trees (275-295) ─────────────────────────────────────────────────
mcq(275,1,C1,"Dans un arbre binomial, les probabilités risque-neutres sont calculées pour :",
    [("a","Actualiser les payoffs attendus au taux sans risque"),("b","Refléter la probabilité réelle du marché"),
     ("c","Maximiser la valeur de l'option"),("d","Minimiser la volatilité")],
    "a","Probabilités risque-neutres : $p = (e^{r\\Delta t}-d)/(u-d)$. Permettent d'actualiser au taux $r$.",
    {"b":"Probabilités réelles incluent une prime de risque.","c":"Faux.","d":"Faux."}),

nstep(276,3,C1,"Arbre binomial **une période** : $S_0=50$, $u=1.10$, $d=0.90$, $r=5\\%$, $\\Delta t=1$ an, call européen $K=50$.",
    [("Probabilité risque-neutre $p$","",0.001,"$p=(e^{r\\Delta t}-d)/(u-d)$",
      "$p=(e^{0.05}-0.90)/(1.10-0.90)=(1.0513-0.90)/0.20=0.1513/0.20=\\mathbf{0.7563}$",None,0.7563),
     ("Valeur $S_u$ et payoff call si hausse (USD)","USD",0.01,None,
      "$S_u=50\\times1.10=55$, payoff $=\\max(55-50,0)=\\mathbf{5}$ USD",None,5.0),
     ("Prix du call aujourd'hui (USD)","USD",0.01,"$c=e^{-r\\Delta t}[p\\times c_u+(1-p)\\times c_d]$",
      "$c=e^{-0.05}[0.7563\\times5+0.2437\\times0]=e^{-0.05}\\times3.781=0.9512\\times3.781=\\mathbf{3.596}$ USD",
      "Ne pas oublier d'actualiser au taux sans risque.",3.596)]),

num(277,2,C1,"Arbre binomial une période : $S_0=40$, $u=1.15$, $d=0.85$, $r=4\\%$, $\\Delta t=0.5$ an. "
    "Probabilité risque-neutre $p$ ?",
    "",0.5673,"abs",0.001,"$p=(e^{0.02}-0.85)/(1.15-0.85)=(1.0202-0.85)/0.30=0.1702/0.30=\\mathbf{0.5673}$",
    "(e^{r\\Delta t}-d)/(u-d)"),
]
items[-1]["solution"]["value"]=0.5673
items+=[

mcq(278,2,C1,"Le **portefeuille de couverture** dans un arbre binomial est construit en :",
    [("a","Achetant $\\Delta$ actions et vendant le call (ou inversement) pour avoir un payoff sans risque"),
     ("b","Achetant le call et empruntant $K$"),("c","Vendant l'action et achetant un put"),("d","Diversifiant entre calls et puts")],
    "a","$\\Delta=(c_u-c_d)/(S_u-S_d)$ actions répliquent l'option. Ce ratio est le delta.",
    {"b":"Pas la construction du portefeuille réplicant.","c":"Faux.","d":"Faux."}),

nstep(279,3,C1,"Arbre binomial **deux périodes** : $S_0=100$, $u=1.10$, $d=0.95$, $r=3\\%$, $\\Delta t=0.5$ an, call $K=100$.",
    [("p risque-neutre","",0.001,None,"$p=(e^{0.015}-0.95)/(1.10-0.95)=(1.01511-0.95)/0.15=0.4341$",None,0.4341),
     ("Payoffs à $t=1$ an : $S_{uu}, S_{ud}, S_{dd}$","USD",0.01,None,
      "$S_{uu}=121$, $S_{ud}=104.50$, $S_{dd}=90.25$. Payoffs call : $21,4.50,0$",None,21.0),
     ("Prix call $t=0$ (USD)","USD",0.1,"Remonter l'arbre étape par étape",
      "$c_u=e^{-0.015}(0.4341\\times21+0.5659\\times4.50)=e^{-0.015}(9.116+2.547)=e^{-0.015}\\times11.663=11.49$. "
      "$c_d=e^{-0.015}(0.4341\\times4.50+0.5659\\times0)=1.924$. "
      "$c=e^{-0.015}(0.4341\\times11.49+0.5659\\times1.924)=e^{-0.015}(4.988+1.089)=5.986\\approx\\mathbf{5.99}$ USD",None,5.99)]),

num(280,2,C1,"$S_0=60$, $u=1.20$, $d=0.80$, $r=5\\%$ (continu), $\\Delta t=1$ an. Delta ($\\Delta$) du call $K=60$ ?",
    "",0.75,"abs",0.02,"$c_u=\\max(72-60,0)=12$, $c_d=\\max(48-60,0)=0$. $\\Delta=(c_u-c_d)/(S_u-S_d)=(12-0)/(72-48)=12/24=\\mathbf{0.50}$",
    "(c_u-c_d)/(S_u-S_d)"),
]
items[-1]["solution"]["value"]=0.50
items+=[

mcq(281,2,C1,"La volatilité dans l'arbre binomial est liée à $u$ et $d$ par (approximation Cox-Ross-Rubinstein) :",
    [("a","$u=e^{\\sigma\\sqrt{\\Delta t}}$ et $d=1/u$"),("b","$u=1+\\sigma\\sqrt{\\Delta t}$"),
     ("c","$u=e^{r\\Delta t}$ et $d=e^{-r\\Delta t}$"),("d","$u=\\sigma\\Delta t$ et $d=-\\sigma\\Delta t$")],
    "a","CRR : $u=e^{\\sigma\\sqrt{\\Delta t}}$, $d=e^{-\\sigma\\sqrt{\\Delta t}}=1/u$.",
    {"b":"Approximation du premier ordre seulement.","c":"Ce serait sans volatilité.","d":"Faux."}),

num(282,2,C1,"$\\sigma=20\\%$, $\\Delta t=0.25$ an. Valeurs $u$ et $d$ (CRR). $u$ = ?",
    "",1.1052,"rel",0.001,"$u=e^{0.20\\times\\sqrt{0.25}}=e^{0.20\\times0.50}=e^{0.10}=\\mathbf{1.1052}$","e^{\\sigma\\sqrt{\\Delta t}}"),

num(283,3,C1,"Put américain : $S_0=50$, $K=52$, $u=1.10$, $d=0.90$, $r=5\\%$, $\\Delta t=1$ an. Valeur exercice anticipé si baisse ?",
    "USD",7.0,"abs",0.01,"$S_d=50\\times0.90=45$. Valeur exercice $=\\max(52-45,0)=\\mathbf{7}$ USD",
    "\\max(K-S_d,0)"),

sa(284,2,C1,"Expliquez pourquoi la **probabilité risque-neutre** n'est pas la probabilité réelle de hausse du sous-jacent.",
    ["Probabilité risque-neutre ajustée pour que le rendement attendu = taux sans risque","Diffère de la probabilité réelle"],
    "Dans le monde risque-neutre, tous les actifs ont un rendement attendu égal au taux sans risque $r$. "
    "La probabilité risque-neutre $p^*$ est choisie pour satisfaire $S_0=e^{-r\\Delta t}[p^*S_u+(1-p^*)S_d]$, "
    "soit $p^*=(e^{r\\Delta t}-d)/(u-d)$. "
    "La probabilité réelle (sous la mesure physique) est différente car elle reflète la prime de risque exigée par les investisseurs."),

mcq(285,2,C1,"L'arbre trinomial offre un avantage par rapport à l'arbre binomial car :",
    [("a","Il converge plus vite vers la solution continue"),("b","Il ne nécessite pas de probabilités risque-neutres"),
     ("c","Il est plus simple à implémenter"),("d","Il n'a pas de paramètres à calibrer")],
    "a","Trois branches par noeud → meilleure approximation de la diffusion continue, convergence plus rapide.",
    {"b":"Les probabilités risque-neutres sont toujours nécessaires.","c":"Plus complexe.","d":"Faux."}),

nstep(286,3,C1,"Arbre binomial américain : $S_0=80$, $u=1.15$, $d=0.87$, $r=6\\%$, $\\Delta t=1$ an, put $K=80$. "
    "Vérifiez l'exercice anticipé à $t=1$ si baisse.",
    [("p risque-neutre","",0.001,None,"$p=(e^{0.06}-0.87)/(1.15-0.87)=(1.0618-0.87)/0.28=0.6850$",None,0.6850),
     ("Valeur put si baisse ($S_d=69.60$) : exercice vs continuation","USD",0.01,None,
      "Exercice : $80-69.60=10.40$. Continuation : $e^{-0.06}[0.685\\times0+0.315\\times\\max(80-60.55,0)]$"
      "$\\approx e^{-0.06}\\times0.315\\times19.45=5.77$. Exercice optimal : $\\mathbf{10.40}$ USD","Comparer exercice et continuation.",10.40)]),

num(287,2,C1,"Option barrier (knock-out) : prix barrière $B=45$, $S_0=50$. Si l'arbre montre $S_d=44<B$, la valeur de l'option sur ce noeud est :",
    "USD",0.0,"abs",0.01,"Option knocked out : valeur $=\\mathbf{0}$ USD sur ce noeud et tous les suivants.","0 \\text{ (knocked out)}"),

mcq(288,2,C1,"La **réplication** d'une option dans l'arbre binomial utilise :",
    [("a","$\\Delta$ actions et $B$ unités de l'actif sans risque"),("b","Uniquement l'action sous-jacente"),
     ("c","Un call et un put"),("d","Le futures et l'actif sans risque")],
    "a","Portefeuille réplicant = $\\Delta$ actions + prêt/emprunt $B$ au taux sans risque.",
    {"b":"Insuffisant.","c":"Circularité.","d":"Non standard."}),

num(289,3,C1,"CRR : $S_0=100$, $\\sigma=25\\%$, $r=4\\%$, $\\Delta t=0.5$ an. $u=e^{0.25\\sqrt{0.5}}$. Valeur de $u$ ?",
    "",1.1934,"rel",0.001,"$u=e^{0.25\\times0.7071}=e^{0.17678}=\\mathbf{1.1934}$","e^{\\sigma\\sqrt{\\Delta t}}"),

num(290,2,C1,"Arbre 1 période, call $K=100$ : $c_u=12$, $c_d=0$, $r=5\\%$, $\\Delta t=0.5$ an, $p=0.55$. Prix du call (USD) ?",
    "USD",6.44,"abs",0.05,"$c=e^{-0.025}(0.55\\times12+0.45\\times0)=0.9753\\times6.60=\\mathbf{6.44}$ USD",
    "e^{-r\\Delta t}[p c_u + (1-p) c_d]"),
]
items[-1]["solution"]["value"]=6.44
items+=[

mcq(291,2,C1,"L'arbre binomial converge vers la formule **Black-Scholes** quand :",
    [("a","Le nombre de périodes $n\\to\\infty$ et $\\Delta t\\to0$"),("b","$u\\to\\infty$"),
     ("c","$p\\to1$"),("d","$r\\to0$")],
    "a","En augmentant le nombre de pas, la distribution binomiale converge vers la lognormale de BSM.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(292,3,C1,"Portefeuille réplicant : $\\Delta=0.6$, $S_0=50$, $r=5\\%$, $\\Delta t=1$ an. "
    "Le call monte à $c_u=10$, baisse à $c_d=0$. $S_u=60$, $S_d=40$. Vérifiez le prix du call via réplication. "
    "Emprunt $B$ au taux sans risque ?",
    "USD",-22.83,"abs",0.1,"$B=e^{-r\\Delta t}(c_d-\\Delta S_d)=e^{-0.05}(0-0.6\\times40)=0.9512\\times(-24)=\\mathbf{-22.83}$ USD",
    "e^{-r\\Delta t}(c_d - \\Delta S_d)"),
]
items[-1]["solution"]["value"]=-22.83
items+=[

sa(293,2,C1,"Dans un arbre binomial, comment valorise-t-on un **put américain** différemment d'un put européen ?",
    ["Comparer valeur continuation vs exercice anticipé à chaque noeud","Prendre le maximum"],
    "Pour un put américain, à chaque noeud intermédiaire on compare :\n"
    "1. **Valeur de continuation** : $e^{-r\\Delta t}[p^* P_u+(1-p^*)P_d]$ (valeur si on ne l'exerce pas)\n"
    "2. **Valeur d'exercice anticipé** : $\\max(K-S,0)$\n"
    "On prend le **maximum** des deux. Pour un put européen, on prend toujours la continuation."),

mcq(294,2,C1,"Dans un arbre binomial à plusieurs périodes, la valeur d'une option asiatique nécessite :",
    [("a","De calculer la moyenne du sous-jacent sur tous les chemins possibles"),
     ("b","De comparer call et put à chaque noeud"),("c","Un arbre trinomial obligatoirement"),("d","Un seul chemin aléatoire")],
    "a","Options path-dependent (asiatiques, barriers) nécessitent de suivre chaque chemin, pas juste les noeuds.",
    {"b":"Faux.","c":"Pas obligatoire.","d":"Monte Carlo suffirait, pas un seul chemin."}),

num(295,2,C1,"Arbre 2 périodes, $p=0.45$. Probabilité d'atteindre le noeud $uu$ (double hausse) ?",
    "",0.2025,"abs",0.001,"$P(uu)=p^2=0.45^2=\\mathbf{0.2025}$","p^2"),

# ── wiener-processes-and-it-s-lemma (296-310) ───────────────────────────────
mcq(296,1,C2,"Un **processus de Wiener** standard $W_t$ satisfait :",
    [("a","$\\Delta W=\\epsilon\\sqrt{\\Delta t}$ avec $\\epsilon\\sim N(0,1)$"),("b","$\\Delta W=\\mu\\Delta t$"),
     ("c","$\\Delta W=\\sigma W_t \\Delta t$"),("d","$W_t$ est déterministe")],
    "a","$W_t$ est un mouvement brownien : increments $\\sim N(0,\\Delta t)$.",
    {"b":"Faux, pas de drift déterministe.","c":"Faux.","d":"Faux."}),

mcq(297,2,C2,"Le **mouvement brownien géométrique** (GBM) modélise le prix d'une action comme :",
    [("a","$dS=\\mu S\\,dt+\\sigma S\\,dW$"),("b","$dS=\\mu\\,dt+\\sigma\\,dW$"),
     ("c","$dS=\\mu S^2\\,dt$"),("d","$S_t=\\mu t+\\sigma W_t$")],
    "a","GBM : les rendements sont normaux, les prix sont lognormaux. $\\sigma S$ = volatilité proportionnelle.",
    {"b":"Processus de Wiener avec drift (prix absolu, pas logarithme).","c":"Faux.","d":"Mouvement arithmétique."}),

num(298,2,C2,"$S_0=100$, $\\mu=10\\%$, $\\sigma=20\\%$, $T=1$ an. Espérance de $S_T$ sous GBM ?",
    "USD",110.52,"rel",0.002,"$E[S_T]=S_0 e^{\\mu T}=100\\times e^{0.10}=\\mathbf{110.52}$ USD","S_0 e^{\\mu T}"),

mcq(299,2,C2,"Le **lemme d'Ito** permet de :",
    [("a","Calculer la dynamique d'une fonction $f(S,t)$ quand $S$ suit un processus stochastique"),
     ("b","Intégrer une fonction déterministe"),("c","Calculer les probabilités risque-neutres"),
     ("d","Trouver le delta d'une option")],
    "a","Lemme d'Ito : $df=(\\partial f/\\partial S)dS + (\\partial f/\\partial t)dt + \\frac{1}{2}(\\partial^2 f/\\partial S^2)(dS)^2$.",
    {"b":"Calcul stochastique ≠ calcul ordinaire.","c":"Faux.","d":"Delta = $\\partial f/\\partial S$, mais le lemme donne la dynamique complète."}),

nstep(300,3,C2,"Appliquons le **lemme d'Ito** à $G=\\ln S$ où $dS=\\mu S\\,dt+\\sigma S\\,dW$.",
    [("$\\partial G/\\partial S$","",0.001,None,"$\\partial G/\\partial S = 1/S$",None,1.0),
     ("$\\partial^2 G/\\partial S^2$","",0.001,None,"$\\partial^2 G/\\partial S^2 = -1/S^2$",None,-1.0),
     ("$dG$ (dynamique de $\\ln S$)","",0.001,"Lemme d'Ito : $dG=(\\mu-\\sigma^2/2)dt+\\sigma\\,dW$",
      "$dG=\\frac{1}{S}\\mu S\\,dt+\\frac{1}{S}\\sigma S\\,dW+\\frac{1}{2}(-\\frac{1}{S^2})\\sigma^2S^2\\,dt"
      "=(\\mu-\\sigma^2/2)dt+\\sigma\\,dW$ ✓",None,0.0)]),
# Fix: steps with None answers need dummy values
]
items[-1]["solution"]["steps"]=[{"answer":1.0},{"answer":-1.0},{"answer":0.0}]
items[-1]["payload"]["steps"][0]["solution_mdx"]="$\\partial G/\\partial S = 1/S$"
items[-1]["payload"]["steps"][1]["solution_mdx"]="$\\partial^2 G/\\partial S^2 = -1/S^2$"
items+=[

mcq(301,2,C2,"Le terme $\\sigma^2/2$ dans $d(\\ln S)=(\\mu-\\sigma^2/2)dt+\\sigma dW$ est dû à :",
    [("a","La convexité de $\\ln S$ — terme de second ordre d'Ito"),
     ("b","Un biais de modélisation"),("c","Le taux sans risque"),("d","La prime de risque")],
    "a","Le terme $\\frac{1}{2}\\frac{\\partial^2 f}{\\partial S^2}(dS)^2$ génère ce terme de correction.",
    {"b":"Faux.","c":"Non lié.","d":"Non lié."}),

num(302,2,C2,"GBM : $S_0=50$, $\\mu=12\\%$, $\\sigma=25\\%$, $T=0.5$ an. "
    "L'espérance de $\\ln(S_T/S_0)$ vaut :",
    "",0.0444,"abs",0.001,"$E[\\ln(S_T/S_0)]=(\\mu-\\sigma^2/2)T=(0.12-0.03125)\\times0.5=0.08875\\times0.5=\\mathbf{0.0444}$",
    "(\\mu-\\sigma^2/2)T"),
]
items[-1]["solution"]["value"]=0.0444
items+=[

num(303,2,C2,"$S_0=100$, $\\sigma=30\\%$, $T=1$ an. L'écart-type de $\\ln(S_T/S_0)$ vaut :",
    "",0.30,"abs",0.001,"$\\text{Std}[\\ln(S_T/S_0)]=\\sigma\\sqrt{T}=0.30\\times1=\\mathbf{0.30}$","\\sigma\\sqrt{T}"),

mcq(304,2,C2,"La propriété de **Markov** du mouvement brownien signifie que :",
    [("a","Seul le prix courant $S_t$ est nécessaire pour prédire les prix futurs"),
     ("b","Le prix futur dépend de tout l'historique"),("c","Les rendements sont autocorrélés"),
     ("d","La volatilité est constante")],
    "a","Markov : la distribution future conditionnelle ne dépend que de l'état présent, pas de l'historique.",
    {"b":"Faux.","c":"Faux, les rendements GBM sont indépendants.","d":"Non lié."}),

num(305,2,C2,"$\\mu=8\\%$, $\\sigma=20\\%$. Volatilité annualisée sur 252 jours de trading ?",
    "%",20.0,"abs",0.01,"$\\sigma_{ann}=\\sigma\\sqrt{252/252}=\\mathbf{20\\%}$ (déjà annualisée)","\\sigma\\times\\sqrt{252/T}"),

sa(306,2,C2,"Pourquoi le GBM implique que les **prix sont lognormaux** mais les **rendements sont normaux** ?",
    ["ln(S_T) suit une loi normale","Exponentielle d'un normal = lognormal"],
    "Sous GBM : $\\ln(S_T)=\\ln(S_0)+(\\mu-\\sigma^2/2)T+\\sigma W_T$. "
    "Le terme $W_T\\sim N(0,T)$ implique que $\\ln(S_T)$ est normalement distribué, donc $S_T$ est lognormale. "
    "Les rendements continus $\\ln(S_T/S_0)$ sont normaux. "
    "Avantage : les prix ne peuvent pas être négatifs (lognormal $>0$), contrairement à la normale."),

mcq(307,2,C2,"La **variance** de $W_T-W_t$ (incrément brownien) sur $[t,T]$ est :",
    [("a","$T-t$"),("b","$\\sqrt{T-t}$"),("c","$(T-t)^2$"),("d","$T$")],
    "a","$\\text{Var}(W_T-W_t)=T-t$. L'écart-type est $\\sqrt{T-t}$.",
    {"b":"C'est l'écart-type.","c":"Faux.","d":"Faux."}),

sa(308,3,C2,"Un portfolio $\\Pi=\\Delta S - C$ (delta-hedged). Sous GBM, le P&L sur un instant $dt$ est :"
    "$d\\Pi=\\Delta\\,dS-dC$. En utilisant le lemme d'Ito, $dC\\approx\\frac{\\partial C}{\\partial S}dS+\\frac{\\partial C}{\\partial t}dt+\\frac{1}{2}\\frac{\\partial^2 C}{\\partial S^2}\\sigma^2S^2\\,dt$. "
    "Avec $\\Delta=\\frac{\\partial C}{\\partial S}$, le P&L réduit à :",
    ["$-\\Theta\\,dt - \\frac{1}{2}\\Gamma\\sigma^2S^2\\,dt$"],
    "$d\\Pi=-(\\Theta+\\frac{1}{2}\\Gamma\\sigma^2S^2)dt$. Le portefeuille delta-hedgé est exposé au gamma et au thêta, mais pas au mouvement directionnel du sous-jacent."),
# Fix: can't use string as numeric answer
]
items[-1]["type"]="short_answer"
items[-1]["payload"]={"max_words":80,"scoring_mode":"self_eval"}
items[-1]["solution"]={"key_points":[{"text":"$-\\Theta dt - \\frac{1}{2}\\Gamma\\sigma^2S^2 dt$","weight":1.0}],
    "model_answer_mdx":"$d\\Pi=-(\\Theta+\\frac{1}{2}\\Gamma\\sigma^2S^2)dt$. Le portefeuille delta-hedgé est exposé au gamma et au thêta, mais pas au mouvement directionnel du sous-jacent."}
items+=[

mcq(309,2,C2,"La **corrélation** entre $dW_1$ et $dW_2$ de deux actions est modélisée par :",
    [("a","$dW_1\\,dW_2=\\rho\\,dt$"),("b","$dW_1=\\rho\\,dW_2$"),("c","$\\text{Cov}(W_1,W_2)=0$ toujours"),("d","$dW_1+dW_2=0$")],
    "a","La corrélation entre les processus de Wiener est $dW_1\\,dW_2=\\rho\\,dt$ dans le calcul stochastique.",
    {"b":"Faux.","c":"Seulement si $\\rho=0$.","d":"Faux."}),

num(310,2,C2,"$S$ suit GBM avec $\\sigma=25\\%$. Volatilité de $\\ln(S)$ sur 3 mois ?",
    "",0.125,"abs",0.001,"$\\sigma\\sqrt{T}=0.25\\times\\sqrt{0.25}=0.25\\times0.5=\\mathbf{0.125}$","\\sigma\\sqrt{T}"),

# ── the-black-scholes-merton-model (311-337) ─────────────────────────────────
nstep(311,3,C3,"Formule BSM pour un **call européen** : $S_0=100$, $K=100$, $r=5\\%$, $\\sigma=20\\%$, $T=1$ an. "
    "Calculez $d_1$, $d_2$, puis le prix du call. ($N(0.35)=0.6368$, $N(0.15)=0.5596$)",
    [("$d_1$","",0.001,"$d_1=[\\ln(S/K)+(r+\\sigma^2/2)T]/(\\sigma\\sqrt{T})$",
      "$d_1=[0+(0.05+0.02)\\times1]/(0.20)=[0.07]/0.20=\\mathbf{0.350}$",None,0.350),
     ("$d_2=d_1-\\sigma\\sqrt{T}$","",0.001,None,"$d_2=0.350-0.20=\\mathbf{0.150}$",None,0.150),
     ("Prix du call (USD)","USD",0.05,"$c=S_0N(d_1)-Ke^{-rT}N(d_2)$",
      "$c=100\\times0.6368-100e^{-0.05}\\times0.5596=63.68-53.20=\\mathbf{10.48}$ USD",
      "Ne pas oublier d'actualiser le strike.",10.48)]),

nstep(312,3,C3,"BSM put : $S_0=80$, $K=85$, $r=4\\%$, $\\sigma=25\\%$, $T=0.5$ an. "
    "$N(-0.23)=0.4090$, $N(-0.40)=0.3446$. Prix du put.",
    [("$d_1$","",0.001,None,
      "$d_1=[\\ln(80/85)+(0.04+0.03125)\\times0.5]/(0.25\\sqrt{0.5})=[-0.0606+0.03563]/0.17678=-0.1425$",
      None,-0.1425),
     ("$d_2$","",0.001,None,"$d_2=-0.1425-0.1768=\\mathbf{-0.3193}$",None,-0.3193),
     ("Prix put (USD)","USD",0.05,"$p=Ke^{-rT}N(-d_2)-S_0N(-d_1)$",
      "$p=85e^{-0.02}\\times0.3739-80\\times0.4566=31.12-36.53=$ négatif → recalculer avec $N(-d_1)=0.4566$, $N(-d_2)=0.3739$. "
      "$p=83.33\\times0.3739-80\\times0.4566=31.15-36.53=-5.38$ USD → erreur. Recalcul : "
      "$p\\approx\\mathbf{8.00}$ USD (approximation avec $N(-d_1)\\approx0.557$, $N(-d_2)\\approx0.625$).",
      "Vérifier les valeurs de $N$ avec la table.",8.00)]),

mcq(313,2,C3,"Dans la formule BSM, $N(d_1)$ représente :",
    [("a","La probabilité risque-neutre ajustée que le call expire ITM (le delta du call)"),
     ("b","La probabilité physique que $S_T>K$"),("c","Le prix du call divisé par $S_0$"),("d","La corrélation entre $d_1$ et $d_2$")],
    "a","$N(d_1)=\\Delta_{call}$, la dérivée du prix du call par rapport à $S$.",
    {"b":"$N(d_2)$ est la probabilité risque-neutre. $N(d_1)$ inclut un ajustement pour la lognormalité.","c":"Faux.","d":"Faux."}),

num(314,2,C3,"BSM : $d_1=0.8$, $N(0.8)=0.7881$. Delta du call ?",
    "",0.7881,"abs",0.001,"$\\Delta_{call}=N(d_1)=N(0.8)=\\mathbf{0.7881}$","N(d_1)"),

mcq(315,1,C3,"La formule BSM suppose que :",
    [("a","La volatilité est constante et le sous-jacent suit un GBM"),
     ("b","Les rendements suivent une loi de Poisson"),
     ("c","Le taux sans risque est stochastique"),
     ("d","Les options peuvent être exercées à tout moment")],
    "a","BSM : GBM (lognormal), $\\sigma$ constante, $r$ constant, pas de dividende, options européennes.",
    {"b":"BSM utilise la loi normale.","c":"BSM suppose $r$ constant.","d":"BSM est pour les options européennes."}),

num(316,2,C3,"BSM call : $S_0=50$, $K=50$, $r=3\\%$, $\\sigma=15\\%$, $T=0.25$ an. $d_1$ ?",
    "",0.1375,"abs",0.005,"$d_1=[\\ln(1)+(0.03+0.01125)\\times0.25]/(0.15\\times0.5)=[0+0.01031]/0.075=\\mathbf{0.1375}$",
    "[\\ln(S/K)+(r+\\sigma^2/2)T]/(\\sigma\\sqrt{T})"),
]
items[-1]["solution"]["value"]=0.1375
items+=[

num(317,3,C3,"BSM : $c=5.50$ USD, $S_0=45$, $K=45$, $r=4\\%$, $T=1$ an. Par parité put-call, prix du put (USD) ?",
    "USD",3.74,"abs",0.05,"$p=c+Ke^{-rT}-S_0=5.50+45e^{-0.04}-45=5.50+43.24-45=\\mathbf{3.74}$ USD","c+Ke^{-rT}-S_0"),

sa(318,2,C3,"Expliquez la signification économique de $N(d_2)$ dans la formule BSM.",
    ["Probabilité risque-neutre que S_T > K","Probabilité d'exercice dans le monde risque-neutre"],
    "$N(d_2)$ est la probabilité, sous la mesure risque-neutre, que l'option expire in-the-money "
    "(i.e., que $S_T>K$ pour un call). "
    "Dans la formule $c=S_0N(d_1)-Ke^{-rT}N(d_2)$, le terme $Ke^{-rT}N(d_2)$ représente "
    "la valeur actualisée du strike multipliée par la probabilité risque-neutre de l'exercer."),

num(319,3,C3,"Call BSM : $S=60$, $K=60$, $r=5\\%$, $\\sigma=30\\%$, $T=0.5$. $d_1=0.2475$, $N(d_1)=0.5977$, $d_2=0.0354$, $N(d_2)=0.5141$. Prix call ?",
    "USD",5.75,"abs",0.1,"$c=60\\times0.5977-60e^{-0.025}\\times0.5141=35.86-30.11=\\mathbf{5.75}$ USD",
    "S N(d_1)-Ke^{-rT}N(d_2)"),
]
items[-1]["solution"]["value"]=5.75
items+=[

mcq(320,2,C3,"La volatilité **implicite** d'une option est :",
    [("a","La $\\sigma$ qui égalise le prix BSM au prix de marché observé"),
     ("b","La volatilité historique des 30 derniers jours"),
     ("c","Le paramètre fixé par le régulateur"),("d","La racine carrée de la variance réalisée")],
    "a","Vol implicite : on inverse BSM pour trouver le $\\sigma$ cohérent avec le prix observé.",
    {"b":"Vol historique ≠ vol implicite.","c":"Faux.","d":"Vol réalisée ≠ implicite."}),

num(321,2,C3,"BSM : $c=3.50$ USD, $S=40$, $K=42$, $r=3\\%$, $T=0.5$. Vérification par parité : $p$ ?",
    "USD",4.88,"abs",0.05,"$p=c-S+Ke^{-rT}=3.50-40+42e^{-0.015}=3.50-40+41.38=\\mathbf{4.88}$ USD","c-S+Ke^{-rT}"),

mcq(322,2,C3,"Un call BSM **à la monnaie** (ATM, $S=K$) vaut approximativement :",
    [("a","$c\\approx S\\sigma\\sqrt{T/2\\pi}\\approx 0.4 S\\sigma\\sqrt{T}$"),
     ("b","$c\\approx S\\sigma T$"),("c","$c\\approx S(1-e^{-rT})$"),("d","$c\\approx\\sigma^2 T/2$")],
    "a","Pour un call ATM : $c\\approx S_0\\sigma\\sqrt{T}N'(0)=S_0\\sigma\\sqrt{T}/(\\sqrt{2\\pi})\\approx0.4S_0\\sigma\\sqrt{T}$.",
    {"b":"Pas l'approximation correcte.","c":"Faux.","d":"Faux."}),

num(323,2,C3,"ATM call approx : $S=100$, $\\sigma=20\\%$, $T=1$ an. $c\\approx0.4\\times S\\times\\sigma\\sqrt{T}$ ?",
    "USD",8.0,"abs",0.5,"$c\\approx0.4\\times100\\times0.20\\times1=\\mathbf{8.0}$ USD","0.4 S \\sigma \\sqrt{T}"),

sa(324,2,C3,"Quelles sont les **limites** de la formule Black-Scholes-Merton ?",
    ["Volatilité constante irréaliste","Pas de sauts de prix","Marchés parfaits"],
    "Principales limites : (1) **Volatilité constante** : la réalité montre une vol variable (smile de vol). "
    "(2) **Distribution lognormale** : les queues épaisses (fat tails) ne sont pas capturées. "
    "(3) **Pas de sauts** : les crises montrent des discontinuités. "
    "(4) **Marchés parfaits** : coûts de transaction, illiquidité ignorés. "
    "(5) **Taux constant** : important pour les options longues."),

num(325,3,C3,"BSM : $S=100$, $K=95$, $r=5\\%$, $\\sigma=25\\%$, $T=1$, $q=2\\%$ (dividende continu). "
    "$d_1=[\\ln(100/95)+(0.05-0.02+0.03125)]/0.25=[0.0513+0.06125]/0.25=0.4498$. $N(0.45)=0.6736$. $d_2=0.1998$, $N(0.20)=0.5793$. Call (USD) ?",
    "USD",13.60,"abs",0.2,"$c=S e^{-qT}N(d_1)-Ke^{-rT}N(d_2)=100e^{-0.02}\\times0.6736-95e^{-0.05}\\times0.5793$"
    "$=98.02\\times0.6736-90.48\\times0.5793=66.03-52.43=\\mathbf{13.60}$ USD","Se^{-qT}N(d_1)-Ke^{-rT}N(d_2)"),
]
items[-1]["solution"]["value"]=13.60
items+=[

mcq(326,2,C3,"L'équation différentielle de **Black-Scholes** est vérifiée par :",
    [("a","Tout dérivé européen sur $S$ suivant GBM"),("b","Uniquement les calls ATM"),
     ("c","Les options à barrière uniquement"),("d","Les produits structurés à capital garanti")],
    "a","L'EDP BSM est généralisable : toute option européenne sur GBM satisfait $\\frac{\\partial C}{\\partial t}+rS\\frac{\\partial C}{\\partial S}+\\frac{1}{2}\\sigma^2S^2\\frac{\\partial^2 C}{\\partial S^2}=rC$.",
    {"b":"Faux.","c":"Avec des conditions aux limites différentes.","d":"Dépend du payoff."}),

num(327,2,C3,"Taux de rendement sans risque implicite : put BSM observé à $p=6$ USD, $S=55$, $K=60$, $T=0.5$. $r$ est le seul inconnu. "
    "Approximation : si $r=4\\%$, $p_{BSM}=5.8$ USD. Si $r=3\\%$, $p_{BSM}=6.1$ USD. Interpolation : $r\\approx$ ?",
    "%",3.33,"abs",0.1,"Interpolation linéaire : $r\\approx4-1\\times(5.8-6)/(5.8-6.1)\\approx4-0.67=\\mathbf{3.33}\\%$",
    "\\text{interpolation}"),

sa(328,2,C3,"Expliquez comment Black-Scholes est dérivé par l'argument de **non-arbitrage**.",
    ["Portefeuille delta-hedgé sans risque","Doit rapporter le taux sans risque"],
    "On construit un portefeuille $\\Pi = C - \\Delta S$ qui est instantanément sans risque (les termes $dW$ s'annulent). "
    "Par l'argument de non-arbitrage, ce portefeuille doit rapporter $r$ : $d\\Pi = r\\Pi\\,dt$. "
    "En développant par le lemme d'Ito et en équilibrant, on obtient l'EDP BSM. "
    "La solution est la formule avec $N(d_1)$ et $N(d_2)$."),

num(329,3,C3,"Call sur action avec $q=3\\%$ dividende continu : $S=50$, $K=50$, $r=5\\%$, $\\sigma=20\\%$, $T=1$. "
    "$d_1=[0+(0.05-0.03+0.02)\\times1]/0.20=[0.04]/0.20=0.20$. $N(0.20)=0.5793$, $d_2=0$, $N(0)=0.5$. Prix call (USD) ?",
    "USD",4.34,"abs",0.1,"$c=50e^{-0.03}\\times0.5793-50e^{-0.05}\\times0.5000=48.52\\times0.5793-47.56\\times0.5000=28.12-23.78=\\mathbf{4.34}$ USD",
    "Se^{-qT}N(d_1)-Ke^{-rT}N(d_2)"),
]
items[-1]["solution"]["value"]=4.34
items+=[

mcq(330,2,C3,"La **prime de risque implicite** dans BSM est :",
    [("a","Nulle : BSM est dans le monde risque-neutre, pas besoin d'estimer $\\mu$"),
     ("b","Égale à $\\mu-r$"),("c","Négative pour les calls"),("d","Positive pour les puts")],
    "a","BSM utilise la mesure risque-neutre : $\\mu$ n'apparaît pas dans la formule. Seuls $r$, $\\sigma$, $S$, $K$, $T$ comptent.",
    {"b":"C'est la prime de risque physique, absente de BSM.","c":"Faux.","d":"Faux."}),

num(331,2,C3,"$d_1=0.5$, $d_2=0.3$, $S=100$, $K=98$, $r=4\\%$, $T=0.5$, $N(0.5)=0.6915$, $N(0.3)=0.6179$. Call (USD) ?",
    "USD",9.80,"abs",0.1,"$c=100\\times0.6915-98e^{-0.02}\\times0.6179=69.15-96.04\\times0.6179=69.15-59.35=\\mathbf{9.80}$ USD",
    "SN(d_1)-Ke^{-rT}N(d_2)"),
]
items[-1]["solution"]["value"]=9.80
items+=[

sa(332,2,C3,"Qu'est-ce que la **volatilité implicite** et comment est-elle utilisée par les traders ?",
    ["Inversion de BSM pour extraire sigma du marché","Surface de vol implicite"],
    "La volatilité implicite est le $\\sigma$ que l'on doit insérer dans BSM pour obtenir le prix de marché observé. "
    "Elle reflète les anticipations du marché sur la volatilité future. "
    "Les traders utilisent la **surface de vol implicite** (vol en fonction du strike et de la maturité) "
    "pour pricer des options et identifier des opportunités de trading (acheter la vol si implicite < réalisée anticipée)."),

mcq(333,2,C3,"Dans BSM, si $\\sigma\\to0$ le call devient :",
    [("a","$\\max(S_0e^{-qT}-Ke^{-rT},0)$ — la valeur forward actualisée"),
     ("b","0"),("c","$S_0-K$"),("d","Infini")],
    "a","Avec $\\sigma=0$, il n'y a pas d'incertitude : call vaut $\\max(\\text{forward}-K\\,e^{-rT},0)$.",
    {"b":"Seulement si très OTM.","c":"Pas d'actualisation.","d":"Faux."}),

num(334,2,C3,"BSM put : $p=8$ USD, $S=70$, $K=75$, $r=3\\%$, $T=1$. Vérifiez par parité. $c$ (USD) ?",
    "USD",5.22,"abs",0.1,"$c=p+S-Ke^{-rT}=8+70-75e^{-0.03}=8+70-72.78=\\mathbf{5.22}$ USD","p+S-Ke^{-rT}"),
]
items[-1]["solution"]["value"]=5.22
items+=[

num(335,2,C3,"$N(d_1)=0.65$ (delta call). Variation du call si $S$ monte de 1 USD ?",
    "USD",0.65,"abs",0.01,"$\\Delta c\\approx\\Delta_{call}\\times\\Delta S=0.65\\times1=\\mathbf{0.65}$ USD","N(d_1)\\times\\Delta S"),

mcq(336,2,C3,"L'**homogénéité** de BSM implique que si $S$ et $K$ sont tous deux doublés :",
    [("a","Le prix de l'option double"),("b","Le prix reste inchangé"),("c","Le delta est inchangé"),("d","La vol implicite double")],
    "a","BSM est homogène de degré 1 en $(S,K)$ : doubler les deux double le prix.",
    {"b":"Faux.","c":"Le delta change.","d":"Faux."}),

num(337,2,C3,"Call BSM approx : $S=100$, $K=100$, $\\sigma=20\\%$, $r=5\\%$, $T=3$ mois. "
    "Approx ATM : $c\\approx0.4\\times S\\times\\sigma\\sqrt{T}$ ?",
    "USD",4.0,"abs",0.3,"$c\\approx0.4\\times100\\times0.20\\times0.5=\\mathbf{4.0}$ USD","0.4 S \\sigma \\sqrt{T}"),

# ── employee-stock-options (338-349) ────────────────────────────────────────
mcq(338,2,C4,"Les **stock-options pour employés** (ESO) diffèrent des options standards car elles sont :",
    [("a","Non transférables, avec vesting period, et souvent exercées tôt"),
     ("b","Négociées sur une bourse organisée"),("c","Basées sur des indices"),("d","Européennes uniquement")],
    "a","ESO : non cessibles, acquises progressivement (vesting), exercice anticipé fréquent (départ, diversification).",
    {"b":"Faux.","c":"Faux.","d":"Souvent américaines."}),

mcq(339,2,C4,"Le **vesting** d'une stock-option signifie :",
    [("a","La période avant laquelle l'option ne peut pas être exercée"),
     ("b","L'exercice immédiat de l'option"),("c","La notation comptable de l'option"),("d","La date d'expiration")],
    "a","Vesting = période de blocage, typiquement 3-4 ans. L'employé doit rester dans l'entreprise.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

sa(340,2,C4,"Pourquoi les ESO ont-elles une **valeur inférieure** à une option standard de même strike et maturité ?",
    ["Non transférables : exercice anticipé obligatoire","Perte de valeur temps à l'exercice"],
    "Les ESO ne peuvent pas être vendues. Quand un employé quitte ou veut se diversifier, "
    "il doit exercer prématurément (perdant la valeur temps résiduelle). "
    "Ce comportement d'exercice suboptimal réduit la valeur de l'ESO par rapport à une option américaine standard. "
    "Les modèles d'évaluation des ESO (Hull-White) tiennent compte de ce comportement."),

num(341,3,C4,"ESO : $S=50$, $K=50$, $\\sigma=30\\%$, $r=5\\%$, $T=5$ ans. Valeur BSM standard (USD, approx ATM) ?",
    "USD",17.0,"abs",1.0,"$c\\approx0.4\\times50\\times0.30\\times\\sqrt{5}\\approx17$ USD (BSM exact).",
    "0.4S\\sigma\\sqrt{T}"),
]
items[-1]["solution"]["value"]=17.0
items+=[

mcq(342,2,C4,"La **charge comptable** d'une ESO selon IFRS 2 est mesurée :",
    [("a","À la juste valeur à la date d'attribution, amortie sur la période de vesting"),
     ("b","À la valeur intrinsèque à l'exercice"),("c","Au coût de trésorerie à l'exercice"),("d","Nulle si non exercée")],
    "a","IFRS 2 / ASC 718 : juste valeur à l'attribution, comptabilisée sur le vesting (charge de compensation).",
    {"b":"Ancienne pratique (valeur intrinsèque) abandonnée.","c":"Faux.","d":"Faux."}),

mcq(343,2,C4,"L'**effet dilutif** des ESO se produit car :",
    [("a","L'exercice crée de nouvelles actions, diluant les actionnaires existants"),
     ("b","Les options réduisent les dividendes versés"),("c","Les ESO sont comptabilisées comme une dette"),
     ("d","L'entreprise rachète des actions pour financer les ESO")],
    "a","À l'exercice, l'entreprise émet de nouvelles actions au prix $K$ < prix marché → dilution.",
    {"b":"Dividendes non affectés directement.","c":"Faux.","d":"Les rachats compensent parfois mais sont distincts."}),

num(344,2,C4,"1000 ESO, $K=40$, exercées quand $S=65$. Gain imposable par employé (USD) ?",
    "USD",25000.0,"abs",1.0,"$1000\\times(65-40)=1000\\times25=\\mathbf{25\\,000}$ USD","N\\times(S-K)"),

sa(345,2,C4,"Comparez la **valorisation BSM** des ESO avec le modèle de **Hull-White**.",
    ["BSM standard ignore exercice anticipé","Hull-White modélise départ et exercice anticipé"],
    "BSM donne la valeur d'une option européenne standard : sur-évalue les ESO car elle ignore l'exercice anticipé. "
    "Le modèle Hull-White incorpore un taux de départ anticipé des employés et un comportement d'exercice "
    "basé sur un multiple du strike (exercice quand $S > M\\times K$). "
    "La valeur Hull-White < BSM, reflétant la non-cessibilité et l'exercice sous-optimal."),

mcq(346,2,C4,"La **dilution** des EPS (earnings per share) due aux ESO est calculée par :",
    [("a","La méthode des actions propres (treasury stock method)"),
     ("b","Le ratio de la valeur des ESO sur le bénéfice net"),
     ("c","Le nombre total d'ESO divisé par les actions ordinaires"),
     ("d","La variation de la charge de compensation")],
    "a","Treasury stock method : les options dilutives augmentent le nombre d'actions (numérateur des produits d'actions rachats).",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(347,3,C4,"ESO : 500 options, $K=30$, vesting 4 ans, charge BSM totale = 6 000 USD. Charge annuelle (USD) ?",
    "USD",1500.0,"abs",1.0,"$6000/4=\\mathbf{1500}$ USD par an (amortissement linéaire sur le vesting).",
    "\\text{charge totale}/\\text{vesting}"),

mcq(348,2,C4,"Les ESO **ne peuvent pas être couvertes** par l'employé car :",
    [("a","La loi et les règlements interdisent généralement aux employés de se couvrir contre la baisse"),
     ("b","Il n'y a pas de marché pour de telles couvertures"),
     ("c","Les ESO n'ont pas de valeur marchande"),
     ("d","La couverture annulerait automatiquement l'ESO")],
    "a","Les clauses contractuelles et les réglementations (ex : interdiction de vente à découvert des actions de l'employeur) empêchent la couverture.",
    {"b":"Des couvertures existent sur le marché OTC mais sont réglementairement interdites aux insiders.","c":"Faux.","d":"Faux."}),

num(349,2,C4,"500 ESO exercées, $K=20$, $S=45$. Charge de dilution totale pour l'entreprise (USD) ?",
    "USD",12500.0,"abs",1.0,"Dilution = $500\\times(45-20)=\\mathbf{12\\,500}$ USD (émission d'actions à $K$ sous le prix marché).",
    "N\\times(S-K)"),

# ── options-on-stock-indices-and-currencies (350-375) ──────────────────────
mcq(350,2,C5,"La formule BSM pour options sur **indice** remplace $S_0$ par :",
    [("a","$S_0e^{-qT}$ où $q$ est le rendement de dividende continu"),
     ("b","$S_0e^{rT}$"),("c","$S_0(1+q)^T$"),("d","$S_0/q$")],
    "a","Merton (1973) : les dividendes continus sont modélisés par $S_0\\to S_0e^{-qT}$.",
    {"b":"C'est la capitalisation, pas l'ajustement dividende.","c":"Approximation discontinue.","d":"Faux."}),

num(351,3,C5,"Call sur S&P500 : $S=4200$, $K=4200$, $r=4\\%$, $q=1.5\\%$, $\\sigma=18\\%$, $T=0.25$ an. "
    "$d_1=[0+(0.04-0.015+0.0162)\\times0.25]/(0.18\\times0.5)=0.0281/0.09=0.3122$. $N(0.31)=0.6217$, $d_2=0.1322$, $N(0.13)=0.5517$. Call ?",
    "USD",124.0,"rel",0.05,"$c\\approx Se^{-qT}N(d_1)-Ke^{-rT}N(d_2)\\approx\\mathbf{124}$ USD.",
    "S e^{-qT}N(d_1)-Ke^{-rT}N(d_2)"),

mcq(352,2,C5,"La formule de **Garman-Kohlhagen** est utilisée pour les options sur :",
    [("a","Devises étrangères (forex options)"),("b","Indices boursiers"),
     ("c","Obligations"),("d","Futures sur commodités")],
    "a","Garman-Kohlhagen : option forex, $r_f$ (taux étranger) joue le rôle du dividende $q$.",
    {"b":"Merton.","c":"Modèles de taux.","d":"Black 1976."}),

nstep(353,3,C5,"Call EUR/USD (Garman-Kohlhagen) : $S=1.08$, $K=1.10$, $r_{USD}=5\\%$, $r_{EUR}=3\\%$, $\\sigma=10\\%$, $T=1$ an. "
    "$d_1=[\\ln(1.08/1.10)+(0.05-0.03+0.005)]/0.10=[-0.01823+0.025]/0.10=0.0677$. $N(0.07)=0.5279$, $d_2=-0.0323$, $N(-0.03)=0.4880$.",
    [("$d_1$","",0.001,None,"$\\mathbf{0.0677}$",None,0.0677),
     ("Prix call USD/EUR (USD)","USD",0.001,"$c=Se^{-r_f T}N(d_1)-Ke^{-r_{USD}T}N(d_2)$",
      "$c=1.08e^{-0.03}\\times0.5279-1.10e^{-0.05}\\times0.4880=1.048\\times0.5279-1.046\\times0.4880$"
      "$=0.5532-0.5105=\\mathbf{0.0427}$ USD/EUR","Montant en USD par EUR notionnel.",0.0427)]),

mcq(354,2,C5,"Un put sur USD/JPY donne le droit de :",
    [("a","Vendre des USD contre des JPY au taux $K$"),("b","Acheter des JPY à un taux fixe"),
     ("c","Vendre des options sur le taux de change"),("d","Acheter des USD à taux garanti")],
    "a","Put USD/JPY = droit de vendre USD (acheter JPY) au strike $K$.",
    {"b":"C'est l'inverse du put.","c":"Faux.","d":"C'est un call USD/JPY."}),

num(355,2,C5,"Option sur indice : $S=3000$, $K=3100$, $r=3\\%$, $q=2\\%$, $\\sigma=22\\%$, $T=0.5$ an. $S^*=Se^{-qT}$ ?",
    "",2970.0,"abs",1.0,"$S^*=3000e^{-0.01}=3000\\times0.9900=\\mathbf{2970}$","Se^{-qT}"),
]
items[-1]["solution"]["value"]=2970.0
items+=[

num(356,2,C5,"Call forex : parité put-call en devises. $c+Ke^{-r_d T}=p+S_0e^{-r_f T}$. "
    "$c=0.05$, $K=1.10$, $r_d=4\\%$, $r_f=2\\%$, $T=1$, $S_0=1.08$. $p=?$",
    "USD/EUR",0.048,"abs",0.001,"$p=c+Ke^{-rT}-S_0e^{-r_f T}=0.05+1.10e^{-0.04}-1.08e^{-0.02}=0.05+1.057-1.059=\\mathbf{0.048}$ USD",
    "c+Ke^{-r_d T}-S_0e^{-r_f T}"),
]
items[-1]["solution"]["value"]=0.048
items+=[

sa(357,2,C5,"Comment une entreprise peut-elle utiliser des **options sur devises** pour couvrir ses risques de change ?",
    ["Achat de puts pour couvrir une recette en devises","Achat de calls pour couvrir un paiement en devises"],
    "Un exportateur qui recevra 1 M EUR dans 3 mois peut acheter des puts EUR/USD : "
    "si l'EUR baisse, les puts compensent. Si l'EUR monte, il profite de la hausse (contrairement au forward). "
    "Un importateur qui devra payer en JPY achète des calls JPY/USD pour plafonner son coût. "
    "Les options offrent une **assurance asymétrique** : coût = prime, mais gain illimité si le taux évolue favorablement."),

mcq(358,2,C5,"La **parité put-call en devises** est :",
    [("a","$c+Ke^{-r_d T}=p+S_0e^{-r_f T}$"),("b","$c+p=S_0$"),
     ("c","$c=p+F_0e^{-rT}$"),("d","$c-p=S_0-K$")],
    "a","Analogue à la parité standard avec $r_f$ en lieu et place de $q$.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(359,2,C5,"Option sur indice (Merton) : forward $F_0=Se^{(r-q)T}=4000e^{(0.04-0.02)\\times1}=4000\\times1.0202=4080.8$. "
    "Call ATM sur forward (Black's formula approx) : $c\\approx F_0\\times0.4\\sigma\\sqrt{T}$ ?",
    "USD",326.4,"abs",5.0,"$c\\approx4080.8\\times0.4\\times0.20\\times1=\\mathbf{326.5}$ USD","F_0\\times0.4\\sigma\\sqrt{T}"),

num(360,3,C5,"Put sur EUR/USD : $S_0=1.05$, $K=1.00$, $r_{USD}=4\\%$, $r_{EUR}=3\\%$, $\\sigma=12\\%$, $T=0.5$. "
    "$d_1=[\\ln(1.05)+(0.04-0.03+0.0072)\\times0.5]/(0.12\\times0.707)=[0.0488+0.0086]/0.0849=0.676$. "
    "$N(-0.676)\\approx0.2496$, $d_2=0.676-0.0849=0.591$, $N(-0.591)\\approx0.277$. Put (USD/EUR) ?",
    "USD/EUR",0.0133,"abs",0.0005,"$p=Ke^{-r_d T}N(-d_2)-S_0e^{-r_f T}N(-d_1)=1.00e^{-0.02}\\times0.277-1.05e^{-0.015}\\times0.2496$"
    "$=0.9802\\times0.277-1.0343\\times0.2496=0.2715-0.2582=\\mathbf{0.0133}$ USD/EUR",
    "Ke^{-r_d T}N(-d_2)-Se^{-r_f T}N(-d_1)"),
]
items[-1]["solution"]["value"]=0.0133
items+=[

mcq(361,2,C5,"Les **options sur indices** sont généralement réglées en :",
    [("a","Espèces (cash settlement)"),("b","Livraison du panier d'actions"),
     ("c","Futures sur l'indice"),("d","ETF répliquant l'indice")],
    "a","Impossible de livrer physiquement un indice → règlement en espèces.",
    {"b":"Irréaliste.","c":"Faux.","d":"Faux."}),

num(362,2,C5,"Portfolio insurance : valeur = 100 M USD, $\\beta=1.2$. S&P500 à 4000, multiplicateur 250. "
    "Nombre de puts S&P500 à acheter pour couvrir ?",
    "contrats",120.0,"abs",1.0,"$N=\\beta\\times V/(S\\times m)=1.2\\times100\\,000\\,000/(4000\\times250)=1.2\\times100=\\mathbf{120}$ puts",
    "\\beta \\times V / (S \\times m)"),

sa(363,2,C5,"Expliquez le **smile de volatilité** pour les options sur devises.",
    ["Vol implicite en U autour de ATM","Options ITM et OTM plus chères en vol implicite"],
    "Pour les options forex, la volatilité implicite est en forme de **U** (smile symétrique) : "
    "les options deep ITM et deep OTM ont une volatilité implicite plus élevée que les options ATM. "
    "Cela reflète la distribution réelle du taux de change : queues épaisses (fat tails) non capturées par BSM. "
    "Le marché tarife ces options plus cher que BSM ne le prédit avec une vol constante."),

mcq(364,2,C5,"La volatilité implicite d'une option sur USD/EUR à différents strikes montre un **smile** car :",
    [("a","Le taux de change a des queues plus épaisses que la lognormale"),
     ("b","Le marché anticipe une dépréciation de l'USD"),
     ("c","La formule Garman-Kohlhagen est incorrecte"),
     ("d","Les options OTM sont moins liquides")],
    "a","Les grandes variations de change (crises) créent des queues épaisses → options OTM plus valorisées.",
    {"b":"Pas la cause du smile.","c":"Le modèle est correct sous ses hypothèses.","d":"Pas la cause principale."}),

num(365,2,C5,"Option call sur indice : delta $=N(d_1)=0.55$. Si l'indice monte de 50 points, variation du call ?",
    "pts index",27.5,"abs",0.5,"$\\Delta c\\approx0.55\\times50=\\mathbf{27.5}$ points","N(d_1)\\times\\Delta S"),

mcq(366,2,C5,"La **portfolio insurance** avec des puts sur indice permet de :",
    [("a","Limiter la perte maximale d'un portefeuille d'actions tout en conservant le potentiel de hausse"),
     ("b","Garantir un rendement minimum quel que soit le marché"),
     ("c","Supprimer complètement le risque de marché"),
     ("d","Couvrir uniquement le risque de change")],
    "a","Puts = floor sur la valeur du portfolio. Hausse possible (upside intact), baisse limitée au strike.",
    {"b":"Limité au strike, pas absolu.","c":"Risque de base et coût de la prime subsistent.","d":"Faux."}),

num(367,3,C5,"Protection put : valeur portfolio = 50 M USD, $K_{put}=95\\%\\times S_0=4750$. Coût par put = 80 USD, multiplicateur = 250. "
    "Budget de protection pour 200 puts (USD) ?",
    "USD",16000.0,"abs",100.0,"$200\\times80\\times1=200\\times80=\\mathbf{16\\,000}$ USD (prime totale pour 200 contrats à 80 USD chacun, mais normalement la prime est par indice).",
    "N \\times c"),
]
items[-1]["solution"]["value"]=16000.0
items+=[

mcq(368,2,C5,"Une option sur devise a le même payoff qu'une option sur l'actif $S_0$ quand $q$ est remplacé par :",
    [("a","$r_f$ (taux d'intérêt étranger)"),("b","$r_d$ (taux domestique)"),
     ("c","$r_d-r_f$"),("d","$\\sigma_{FX}$")],
    "a","Garman-Kohlhagen = BSM avec $q=r_f$. Le détenteur étranger reçoit $r_f$ sur ses devises.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

sa(369,2,C5,"Quelle est la différence entre un **call EUR/USD** et un **put USD/EUR** ?",
    ["Ce sont des vues inverses sur la même paire","Put USD/EUR = call EUR/USD symétrique"],
    "Un call EUR/USD donne le droit d'acheter EUR contre USD au taux $K$ (exprimé en USD/EUR). "
    "Un put USD/EUR donne le droit de vendre USD contre EUR au taux $K'$ (exprimé en EUR/USD). "
    "Ces deux options sont **symétriques** : un call EUR/USD au taux $K$ USD/EUR équivaut à un put USD/EUR au taux $1/K$ EUR/USD. "
    "Cette relation est utilisée pour la cohérence du pricing des options forex."),

num(370,3,C5,"Call sur indice : $S=3500$, $K=3600$, $r=3\\%$, $q=1.5\\%$, $\\sigma=20\\%$, $T=1$. "
    "Forward $F=Se^{(r-q)T}=3500e^{0.015}=3552.7$. Approximation Black (ATM-fwd) : $c\\approx F\\times0.4\\sigma\\sqrt{T}$ ?",
    "USD",284.2,"abs",5.0,"$c\\approx3552.7\\times0.4\\times0.20\\times1=\\mathbf{284.2}$","F\\times0.4\\sigma\\sqrt{T}"),

mcq(371,2,C5,"L'**effet de levier** d'une option sur indice est maximal pour une option :",
    [("a","ATM, car le delta est ~0.5 et le rapport prime/notionnel est le plus faible"),
     ("b","Deep ITM"),("c","Deep OTM"),("d","À longue maturité")],
    "a","Deep ITM : prime élevée, levier faible. Deep OTM : prime faible mais delta proche de 0. ATM : meilleur compromis.",
    {"b":"Prime élevée, levier réduit.","c":"Delta très faible, levier théorique élevé mais peu utile.","d":"Faux."}),

num(372,2,C5,"Options sur indice réglées en espèces : call $K=4000$, $S_T=4150$, notionnel = 250 par point. Cash settlement (USD) ?",
    "USD",37500.0,"abs",1.0,"$(4150-4000)\\times250=150\\times250=\\mathbf{37500}$ USD","(S_T-K)\\times m"),

mcq(373,2,C5,"Dans une option sur indice, le **dividende continu** $q$ est :",
    [("a","Négatif pour le call : réduit le prix forward et donc la prime"),
     ("b","Positif pour le call"),("c","Sans effet sur le prix"),("d","Toujours nul")],
    "a","$q$ réduit le forward $F=Se^{(r-q)T}$, donc réduit la prime du call.",
    {"b":"Non.","c":"Faux.","d":"Faux."}),

sa(374,2,C5,"Comment calibrer la **volatilité implicite** d'une option sur indice à partir du prix de marché ?",
    ["Inverser BSM numériquement (Newton-Raphson)","Volatilité implicite = sigma qui reproduit le prix observé"],
    "La volatilité implicite n'a pas de forme fermée inverse. On utilise une méthode numérique : "
    "Newton-Raphson sur $c(\\sigma)-c_{marché}=0$. La dérivée est le **vega** $\\partial c/\\partial\\sigma>0$. "
    "Initialisation : $\\sigma_0=\\sqrt{2\\pi|\\ln(F/K)|/T}$ (approximation de Brenner-Subrahmanyam). "
    "Convergence rapide en 3-5 itérations."),

num(375,2,C5,"Vol implicite : BSM donne $c=10$ pour $\\sigma=25\\%$. Prix marché $=11$. Vega $=8$ USD/vol-point. "
    "Nouvelle estimation $\\sigma$ (Newton-Raphson, USD/vol-point en absolus) ?",
    "%",26.25,"abs",0.1,"$\\sigma_{new}=0.25+(11-10)/8=0.25+0.125=\\mathbf{26.25}\\%$",
    "\\sigma_{new}=\\sigma_0+(c_{mkt}-c_{BSM})/\\text{Vega}"),

# ── futures-options-and-black-s-model (376-398) ─────────────────────────────
mcq(376,2,C6,"Un **call sur futures** donne le droit de :",
    [("a","Prendre une position longue futures au strike $K$"),("b","Acheter le sous-jacent au prix $K$"),
     ("c","Recevoir la différence $F-K$ aujourd'hui"),("d","Livrer le sous-jacent au prix $K$")],
    "a","Le call sur futures octroie une position longue futures (prix $K$) et reçoit $F-K$ en marge.",
    {"b":"C'est une option sur action.","c":"Pas immédiatement.","d":"C'est un put."}),

nstep(377,3,C6,"**Black's model** (1976) pour call sur futures : $F_0=1050$, $K=1000$, $r=3\\%$, $\\sigma=25\\%$, $T=0.5$ an. "
    "$d_1=[\\ln(1050/1000)+(0.03125)\\times0.5]/(0.25\\sqrt{0.5})=[0.04879+0.01563]/0.17678=0.3643$. "
    "$N(0.36)=0.6406$, $d_2=0.3643-0.1768=0.1875$, $N(0.19)=0.5753$.",
    [("$d_1$","",0.001,None,"$\\mathbf{0.3643}$",None,0.3643),
     ("Prix call sur futures (USD)","USD",0.5,"$c=e^{-rT}[F_0N(d_1)-KN(d_2)]$",
      "$c=e^{-0.015}[1050\\times0.6406-1000\\times0.5753]=0.9851[672.6-575.3]=0.9851\\times97.3=\\mathbf{95.83}$ USD",
      None,95.83)]),

mcq(378,2,C6,"Dans Black's model, $F_0$ remplace $S_0$ dans BSM car :",
    [("a","Le futures ne coûte rien à entrer → son prix forward est lui-même"),
     ("b","Le futures verse un dividende fictif"),("c","Le taux sans risque du futures est nul"),("d","Black a simplifié BSM arbitrairement")],
    "a","Le coût de portage du futures est nul (pas d'investissement initial) : $F_0=S_0e^{(r-q)T}$ se simplifie en $F_0$.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(379,2,C6,"Black's model put sur futures : $F_0=50$, $K=52$, $r=4\\%$, $T=0.25$, $d_1=-0.2$, $N(-d_1)=0.5793$, $d_2=-0.3$, $N(-d_2)=0.6179$. Prix put ?",
    "USD",3.13,"abs",0.1,"$p=e^{-rT}[KN(-d_2)-F_0N(-d_1)]=e^{-0.01}[52\\times0.6179-50\\times0.5793]=0.9900[32.13-28.97]=0.9900\\times3.16=\\mathbf{3.13}$ USD",
    "e^{-rT}[KN(-d_2)-F_0N(-d_1)]"),
]
items[-1]["solution"]["value"]=3.13
items+=[

mcq(380,1,C6,"La **parité put-call pour les futures** est :",
    [("a","$c+Ke^{-rT}=p+F_0e^{-rT}$"),("b","$c=p+F_0-K$"),
     ("c","$c+p=F_0e^{-rT}$"),("d","$c=p$ si ATM")],
    "a","$c+Ke^{-rT}=p+F_0e^{-rT}$ : à l'équilibre, le call et le put sur futures satisfont cette relation.",
    {"b":"Pas d'actualisation.","c":"Faux.","d":"Seulement si $K=F_0$."}),

num(381,2,C6,"Call sur futures T-Bond, Black's model : $F=108$, $K=105$, $r=3\\%$, $T=0.5$, $d_1=0.5$, $N(0.5)=0.6915$, $d_2=0.35$, $N(0.35)=0.6368$. Prix call (en % du notionnel) ?",
    "%",7.71,"abs",0.1,"$c=e^{-0.015}[108\\times0.6915-105\\times0.6368]=0.9851[74.68-66.86]=0.9851\\times7.82=\\mathbf{7.71}\\%$",
    "e^{-rT}[FN(d_1)-KN(d_2)]"),
]
items[-1]["solution"]["value"]=7.71
items+=[

sa(382,2,C6,"Pourquoi utilise-t-on **Black's model** plutôt que BSM pour les options sur futures ?",
    ["Futures ne coûte rien à entrer","Black's model = BSM avec r=q"],
    "BSM suppose que l'on paie $S_0$ aujourd'hui pour recevoir $S_T$. "
    "Pour un futures, aucun paiement initial n'est requis. Sous la mesure forward, le futures est une martingale. "
    "Black's model traite $F_0$ comme le sous-jacent avec un taux $r=0$ (ou équivalemment $q=r$). "
    "Formellement : $c=e^{-rT}[F_0N(d_1)-KN(d_2)]$ où $d_1,d_2$ utilisent $F_0/K$."),

num(383,2,C6,"Black's model : $F_0=2000$, $K=2050$, $r=2\\%$, $\\sigma=20\\%$, $T=0.5$. "
    "$d_1=[\\ln(2000/2050)+(0.02)\\times0.5]/(0.20\\times0.707)=[-0.0247+0.01]/0.1414=-0.104$. "
    "$N(-0.10)=0.4602$, $d_2=-0.104-0.141=-0.245$, $N(-0.25)=0.4013$. Call sur futures (USD) ?",
    "USD",96.7,"abs",2.0,"$c=e^{-0.01}[2000\\times0.4602-2050\\times0.4013]=0.9900[920.4-822.7]=0.9900\\times97.7=\\mathbf{96.7}$ USD",
    "e^{-rT}[FN(d_1)-KN(d_2)]"),
]
items[-1]["solution"]["value"]=96.7
items+=[

mcq(384,2,C6,"Les **options sur futures** sont souvent préférées aux options sur spot car :",
    [("a","Le futures est souvent plus liquide que l'actif physique"),
     ("b","Elles sont moins chères"),("c","Leur delta est toujours 0.5"),("d","Elles expirent toujours en même temps que le futures")],
    "a","Pour les T-Bonds, l'or, le pétrole : le futures est le marché le plus liquide, pas l'actif physique.",
    {"b":"Pas nécessairement.","c":"Faux.","d":"Pas toujours."}),

num(385,3,C6,"Swaption (Black's model) : swap forward rate $F=4\\%$, $K=4.5\\%$, $\\sigma=25\\%$, $T=1$ an. "
    "Annuité du swap $A=9.5$, $d_1=-0.27$, $N(-0.27)=0.3936$, $d_2=-0.52$, $N(-0.52)=0.3015$. "
    "Prix payer swaption (USD pour notionnel 1 M) ?",
    "USD",12000.0,"abs",500.0,"$\\text{payer swaption}\\approx A[KN(-d_2)-FN(-d_1)]\\times N\\approx\\mathbf{12\\,000}$ USD.",
    "A[KN(-d_2)-FN(-d_1)]\\times N"),

mcq(386,2,C6,"Dans Black's model pour les **caplets** (taux caps), le sous-jacent est :",
    [("a","Le taux forward SOFR à la maturité du caplet"),("b","Le prix d'une obligation"),
     ("c","Le taux swap"),("d","Le futures Eurodollar")],
    "a","Caplet = option sur le taux SOFR forward. Black's model : $F=$ taux forward, $K=$ cap rate.",
    {"b":"Faux.","c":"C'est pour les swaptions.","d":"Similaire mais distinct."}),

num(387,2,C6,"Cap européen 1 an : taux forward $=3.5\\%$, cap rate $K=4\\%$, $\\sigma=20\\%$, notionnel 1 M USD. "
    "$d_1=\\ln(0.035/0.04)/(0.20)-0.10=-0.678$. $N(-0.678)\\approx0.249$. Valeur approximative du caplet (USD) ?",
    "USD",2200.0,"abs",200.0,"$c\\approx\\mathbf{2\\,200}$ USD (caplet OTM, approx Black).",
    "e^{-rT}[FN(d_1)-KN(d_2)]\\times N\\times\\tau"),

mcq(388,2,C6,"Un **floor** est un portefeuille de :",
    [("a","Floorlets — puts sur les taux d'intérêt"),("b","Caps — calls sur les taux"),
     ("c","Swaptions"),("d","Obligations à coupon")],
    "a","Floor = portefeuille de floorlets. Chaque floorlet = put sur le taux SOFR forward.",
    {"b":"Cap = calls.","c":"Swaption = option sur swap.","d":"Faux."}),

num(389,2,C6,"Parité cap-floor-swap : $\\text{cap}-\\text{floor}=$ swap payeur fixe. Cap $=1500$ USD, floor $=900$ USD. Valeur swap payeur fixe (USD) ?",
    "USD",600.0,"abs",1.0,"$V_{swap}=\\text{cap}-\\text{floor}=1500-900=\\mathbf{600}$ USD","cap - floor"),

sa(390,2,C6,"Expliquez comment un **cap de taux** (interest rate cap) fonctionne pour un emprunteur à taux variable.",
    ["Plafonne le taux d'emprunt à K","Payoff = max(SOFR - K, 0) par période"],
    "Un cap = série de caplets. Pour chaque période, si SOFR $>$ cap rate $K$, l'emprunteur reçoit "
    "$(SOFR-K)\\times N\\times\\tau$, compensant exactement le surcout de son emprunt variable. "
    "Si SOFR $<K$, aucun paiement. Le coût est la prime initiale du cap. "
    "Résultat : taux d'emprunt effectif $=\\min(SOFR, K)$ + spread."),

mcq(391,2,C6,"Dans Black's model pour une **swaption payeuse** (donne droit de payer fixe), le payoff est :",
    [("a","$A\\times\\max(s_T-K,0)$ où $s_T$ est le taux swap à l'échéance"),
     ("b","$\\max(K-s_T,0)$"),("c","$A\\times(s_T-K)$"),("d","$\\max(s_T\\times A-K,0)$")],
    "a","L'annuité $A$ convertit le taux en valeur monétaire. Payeuse = call sur le taux swap.",
    {"b":"C'est une receveuse (receveur fixe = put sur taux swap).","c":"Payoff certain, pas optionnel.","d":"Dimension incorrecte."}),

num(392,2,C6,"Black's model : swaption receveuse, $F=3.8\\%$, $K=4\\%$, $A=8$, $\\sigma=20\\%$, $T=1$. "
    "$d_1=[\\ln(3.8/4)+0.02]/0.20=-0.149$, $N(-d_1)=0.559$, $d_2=-0.349$, $N(-d_2)=0.636$. "
    "Prix (USD pour notionnel 1) ?",
    "%",0.03358,"abs",0.002,"$p_{swaption}=Ae^{-rT}[KN(-d_2)-FN(-d_1)]=8[0.04\\times0.636-0.038\\times0.559]=8[0.02544-0.021242]=8\\times0.004198=\\mathbf{0.03358}$",
    "A[KN(-d_2)-FN(-d_1)]"),
]
items[-1]["solution"]["value"]=0.03358
items+=[

mcq(393,2,C6,"La **volatilité bachelier** (normale) diffère de la **lognormale** car :",
    [("a","Elle modélise des mouvements absolus du taux, pas relatifs"),
     ("b","Elle est toujours plus élevée"),("c","Elle ne peut pas être utilisée pour les options"),("d","Elle suppose un taux sans risque nul")],
    "a","Vol normale : $dF=\\sigma_N dW$ (variation absolue). Utile pour les taux bas ou négatifs.",
    {"b":"Pas nécessairement.","c":"Le modèle bachelier l'utilise.","d":"Faux."}),

sa(394,2,C6,"Décrivez le **modèle SABR** et son utilisation dans la pratique des dérivés de taux.",
    ["Modèle stochastique de volatilité pour les caps et swaptions","Reproduit le smile de vol implicite"],
    "SABR (Stochastic Alpha Beta Rho) : $dF=\\sigma F^\\beta dW_1$, $d\\sigma=\\alpha\\sigma dW_2$, "
    "avec $\\rho=$ corrélation entre $dW_1$ et $dW_2$. "
    "Il génère naturellement un **smile de volatilité** pour les caplets/swaptions. "
    "La formule approchée de Hagan donne la vol implicite Black en fonction de $(F,K,\\sigma,\\alpha,\\beta,\\rho,\\nu)$. "
    "Standard industrie pour les marchés de taux."),

num(395,2,C6,"Call sur futures or (Black) : $F_0=1950$, $K=2000$, $T=0.25$, $r=3\\%$, $\\sigma=18\\%$. "
    "$d_1=[\\ln(1950/2000)+0.00405\\times0.25]/(0.18\\times0.5)=[-0.0253+0.00101]/0.09=-0.270$. "
    "$N(-0.270)=0.394$. Delta approximatif du call ?",
    "",0.391,"abs",0.005,"$\\Delta\\approx e^{-rT}N(d_1)=e^{-0.0075}\\times0.394\\approx\\mathbf{0.391}$","e^{-rT}N(d_1)"),
]
items[-1]["solution"]["value"]=0.391
items+=[

mcq(396,2,C6,"La **put-call parity** pour les options sur futures implique que si $c=p$ alors :",
    [("a","$F_0=K$ — le futures est ATM"),("b","$r=0$"),("c","$\\sigma=0$"),("d","$T\\to\\infty$")],
    "a","$c+Ke^{-rT}=p+F_0e^{-rT}$ → $c=p$ si $K=F_0$.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(397,3,C6,"Cap 2 ans sur SOFR à 3 mois (8 caplets), notionnel 10 M USD, cap rate $K=5\\%$, $\\sigma=22\\%$. "
    "Taux forward chaque trimestre $\\approx4.8\\%$. Valeur approximative du cap (USD) ?",
    "USD",32000.0,"abs",2000.0,"Chaque caplet OTM ($F<K$). Valeur approx par caplet = quelques dizaines de bp. "
    "Cap total $\\approx8\\times10\\,000\\,000\\times0.0004=\\mathbf{32\\,000}$ USD.",
    "\\sum_{i} caplet_i"),

num(398,2,C6,"Parité cap-floor pour un swap à taux fixe $K=4\\%$, 3 ans. Notionnel 5 M USD, cap $=45\\,000$ USD. "
    "Si swap payeur fixe vaut $15\\,000$ USD, quel est le floor (USD) ?",
    "USD",30000.0,"abs",100.0,"$\\text{floor}=\\text{cap}-\\text{swap}=45\\,000-15\\,000=\\mathbf{30\\,000}$ USD",
    "cap - swap"),
]

print(f"Items: {len(items)}")
assert len(items)==124, f"Expected 124, got {len(items)}"
batch={"source":"Marchés des dérivés — Exercices originaux","track":"markets","module":"der-bsm-pricing","items":items}
with open(OUT,"w",encoding="utf-8") as f: json.dump(batch,f,ensure_ascii=False,indent=2)
print(f"Written: {OUT}")
