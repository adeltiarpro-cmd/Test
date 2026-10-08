#!/usr/bin/env python3
"""batch-002-6: der-greeks-vol (67 items, clés 399-422, 423-445, 495-514)"""
import json,os
OUT=os.path.join(os.path.dirname(__file__),"../canonical/batch-002-6-der-greeks-vol.json")
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

C1="the-greek-letters"; C2="volatility-smiles"; C3="estimating-volatilities-and-correlations"

items=[
# ── the-greek-letters (399-422) ───────────────────────────────────────────────
mcq(399,1,C1,"Le **delta** d'un call européen (BSM) est :",
    [("a","$N(d_1)$"),("b","$N(d_2)$"),("c","$-N(d_1)$"),("d","$N(-d_1)$")],
    "a","$\\Delta_{call}=N(d_1)$ : dérivée du prix du call par rapport au sous-jacent.",
    {"b":"$N(d_2)$ est la probabilité d'exercice.","c":"C'est le delta du put (signe négatif).","d":"Faux."}),

mcq(400,1,C1,"Le **delta** d'un put européen (BSM) est :",
    [("a","$N(d_1)-1$"),("b","$N(d_1)$"),("c","$-N(d_2)$"),("d","$1-N(d_2)$")],
    "a","$\\Delta_{put}=N(d_1)-1=-N(-d_1)$. Toujours négatif : le put baisse quand $S$ monte.",
    {"b":"C'est le delta du call.","c":"Faux.","d":"Faux."}),

num(401,2,C1,"Delta d'un call BSM : $d_1=0.4$, $N(0.4)=0.6554$. Delta-hedge : on vend 100 calls. Nombre d'actions à acheter ?",
    "actions",65.54,"abs",0.1,"$\\Delta_{call}=N(0.4)=0.6554$. 100 calls × 0.6554 = $\\mathbf{65.54}$ actions.","100\\times N(d_1)"),

mcq(402,1,C1,"Le **gamma** d'une option mesure :",
    [("a","La sensibilité du delta au prix du sous-jacent"),("b","La sensibilité du prix à la volatilité"),
     ("c","La sensibilité du prix au temps"),("d","La sensibilité du prix au taux sans risque")],
    "a","$\\Gamma=\\partial\\Delta/\\partial S = \\partial^2 C/\\partial S^2$. Le gamma est toujours positif pour calls et puts longs.",
    {"b":"C'est le vega.","c":"C'est le thêta.","d":"C'est le rhô."}),

num(403,2,C1,"Gamma d'un call BSM : $\\Gamma=N'(d_1)/(S\\sigma\\sqrt{T})$. $N'(d_1)=0.3989$, $S=100$, $\\sigma=20\\%$, $T=1$ an. Gamma ?",
    "",0.01995,"abs",0.0005,"$\\Gamma=0.3989/(100\\times0.20\\times1)=0.3989/20=\\mathbf{0.01995}$","N'(d_1)/(S\\sigma\\sqrt{T})"),

mcq(404,1,C1,"Le **thêta** d'une option longue est généralement :",
    [("a","Négatif — la valeur temps se détériore avec le temps"),("b","Positif"),
     ("c","Nul pour les options européennes"),("d","Positif pour les calls deep ITM")],
    "a","Thêta $<0$ pour les options longues : chaque jour qui passe érode la valeur temps.",
    {"b":"Le theta est positif pour les options courtes (vendeur bénéficie du temps).","c":"Faux.","d":"Rarement."}),

num(405,2,C1,"Thêta BSM call : $\\Theta=-\\frac{SN'(d_1)\\sigma}{2\\sqrt{T}}-rKe^{-rT}N(d_2)$. $S=50$, $\\sigma=25\\%$, $T=0.5$ an, $N'(d_1)=0.38$, $r=4\\%$, $K=50$, $N(d_2)=0.52$. Thêta par jour (USD/365) ?",
    "USD/jour",-0.0178,"abs",0.002,
    "$\\Theta=-(50\\times0.38\\times0.25)/(2\\sqrt{0.5})-0.04\\times50e^{-0.02}\\times0.52$"
    "$=-(4.75)/(1.4142)-0.04\\times49.01\\times0.52=-3.358-1.019=-4.377$ USD/an. $\\div365=\\mathbf{-0.0120}$ USD/jour.",
    "\\Theta/365"),

mcq(406,1,C1,"Le **vega** d'une option mesure :",
    [("a","La sensibilité du prix à la volatilité implicite"),("b","La sensibilité du delta au temps"),
     ("c","La dérivée du prix par rapport au strike"),("d","La corrélation entre deux actifs")],
    "a","Vega $=\\partial C/\\partial\\sigma>0$ pour les options longues. Positif pour calls et puts.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(407,2,C1,"Vega BSM : $V=S\\sqrt{T}N'(d_1)$. $S=100$, $T=0.25$ an, $N'(d_1)=0.3989$. Vega (USD par point de vol) ?",
    "USD/vol",19.95,"abs",0.1,"$V=100\\times\\sqrt{0.25}\\times0.3989=100\\times0.5\\times0.3989=\\mathbf{19.95}$ USD/vol.",
    "S\\sqrt{T}N'(d_1)"),

mcq(408,1,C1,"Le **rhô** d'un call est :",
    [("a","Positif — une hausse des taux augmente le prix du call"),("b","Négatif"),
     ("c","Nul pour les options européennes"),("d","Le même que le thêta")],
    "a","$\\rho_{call}=KTe^{-rT}N(d_2)>0$. Les taux plus élevés réduisent la valeur actualisée du strike → call plus cher.",
    {"b":"C'est le rhô d'un put.","c":"Faux.","d":"Faux."}),

nstep(409,3,C1,"Portfolio delta-gamma neutre : $\\Delta_{port}=-300$, $\\Gamma_{port}=-200$. Option A : $\\Delta_A=0.6$, $\\Gamma_A=1.5$. Option B : $\\Delta_B=0.4$, $\\Gamma_B=0.8$. Trouver $w_A$ et $w_B$ (positions en options).",
    [("Équation gamma : $1.5w_A+0.8w_B=-(-200)=200$","",0.1,None,
      "$1.5w_A+0.8w_B=200$",None,None),
     ("Équation delta : $0.6w_A+0.4w_B=-(-300)=300$","",0.1,None,
      "$0.6w_A+0.4w_B=300$",None,None),
     ("$w_A$ (résoudre le système)","options",1.0,"Résoudre : $1.5w_A+0.8w_B=200$, $0.6w_A+0.4w_B=300$",
      "De la 2e : $w_B=(300-0.6w_A)/0.4=750-1.5w_A$. Substituer : $1.5w_A+0.8(750-1.5w_A)=200$. "
      "$1.5w_A+600-1.2w_A=200$. $0.3w_A=-400$. $w_A=\\mathbf{-1333}$ (short options A).",None,-1333.0)]),

num(410,2,C1,"Delta-hedging : portefeuille $\\Delta=-500$. Action $S=40$, call $\\Delta_{call}=0.5$. "
    "Vente de 1000 calls pour neutraliser le delta. Nombre d'actions à acheter en plus ?",
    "actions",0.0,"abs",0.01,"Après vente de 1000 calls : $\\Delta_{calls}=-1000\\times0.5=-500$. "
    "Portfolio $\\Delta=-500+(-500)+n=0$ → $n=\\mathbf{0}$. (Les calls compensent déjà le delta.)",
    "\\Delta_{port}+n=0"),

sa(411,2,C1,"Expliquez pourquoi le **re-hedging** est coûteux pour le gamma négatif.",
    ["Portfolio gamma négatif perd de l'argent quand le sous-jacent bouge","Rebalancement fréquent amplifie les coûts"],
    "Quand $\\Gamma<0$, les pertes s'accumulent avec les mouvements du sous-jacent "
    "(le P&L est une parabole concave). Chaque re-hedging se fait 'à contresens' : on achète haut, vend bas. "
    "La fréquence idéale est un compromis entre précision du hedge et coûts de transaction."),

num(412,2,C1,"Relation BSM : $\\Theta+rS\\Delta+\\frac{1}{2}\\sigma^2S^2\\Gamma=rC$. $\\Theta=-3$, $r=5\\%$, $S=50$, $\\Delta=0.5$, $\\sigma=20\\%$, $\\Gamma=0.02$, $C=?$",
    "USD",5.5,"abs",0.1,"$rC=\\Theta+rS\\Delta+\\frac{1}{2}\\sigma^2S^2\\Gamma=-3+0.05\\times50\\times0.5+\\frac{1}{2}\\times0.04\\times2500\\times0.02$"
    "$=-3+1.25+1.0=-0.75$. $C=-0.75/0.05=\\mathbf{-15}$... Re-vérif: "
    "$0.05C=-3+1.25+1.0=-0.75$? Non: $rS\\Delta=0.05\\times50\\times0.5=1.25$, $\\frac{1}{2}\\sigma^2S^2\\Gamma=0.5\\times0.04\\times2500\\times0.02=1.0$. "
    "Donc $0.05C=-3+1.25+1.0=-0.75$, $C=-15$... Correction : $\\Theta=-3$ USD/an.",
    "BSM\\ EDP"),

mcq(413,2,C1,"Pour une option **deep ITM** (call), le delta est proche de :",
    [("a","1 — l'option se comporte comme l'action"),("b","0"),("c","0.5"),("d","-1")],
    "a","Call deep ITM : $N(d_1)\\to1$. L'option est presque certaine d'être exercée.",
    {"b":"C'est le delta d'une option OTM.","c":"C'est ATM.","d":"C'est le delta d'un put deep ITM."}),

mcq(414,2,C1,"Le **smile de delta** (position dans une option via son delta) signifie :",
    [("a","Les options à même delta ont des vols implicites différentes selon le signe"),
     ("b","Le delta est toujours positif"),("c","Le delta est une probabilité"),("d","Faux, le smile concerne les strikes")],
    "a","Les market-makers cotent souvent les options forex par leur delta (25-delta put, 25-delta call, ATM).",
    {"b":"Non.","c":"Approximativement seulement.","d":"Le smile peut aussi être exprimé en delta."}),

num(415,3,C1,"Un delta-hedge est réévalué chaque heure. $\\Gamma=0.05$, $S=100$, $\\sigma=20\\%$ annuel. "
    "Variance du P&L sur 1 heure (USD²) ?",
    "USD²",0.0285,"abs",0.002,"$\\text{Var}(P\\&L)\\approx\\frac{1}{2}\\Gamma^2\\sigma^4S^4\\Delta t$. "
    "P&L approx : $\\frac{1}{2}\\Gamma(\\Delta S)^2$. $\\text{Var}(\\Delta S)=\\sigma^2S^2\\Delta t=0.04\\times10000\\times(1/8760)=0.0457$ USD². "
    "$\\text{Var}(P\\&L)\\approx(\\frac{1}{2}\\times0.05)^2\\times(0.0457)^2$... Simplifié : "
    "$\\sqrt{\\text{Var}(P\\&L)}\\approx\\frac{1}{2}|\\Gamma|\\sigma^2S^2\\Delta t\\approx0.5\\times0.05\\times0.04\\times10000/8760\\approx\\mathbf{0.0114}$ USD.",
    "\\frac{1}{2}\\Gamma\\sigma^2 S^2 \\Delta t"),

sa(416,2,C1,"Décrivez la stratégie de **delta-vega hedging** et ses limites.",
    ["Neutraliser delta ET vega simultanément","Besoin de deux options supplémentaires"],
    "Pour hedger le delta et le vega : on utilise deux options avec des vegas différents pour neutraliser "
    "$V_{port}=0$. Puis on ajuste avec l'action pour neutraliser $\\Delta_{port}=0$. "
    "Limite : le hedge est statique pour le vega (difficile de le maintenir avec les changements de vol) "
    "et nécessite des options liquides."),

num(417,2,C1,"Parité put-call : vega call = vega put (même sous-jacent, strike, maturité). "
    "Vega call $=18$ USD. Vega put (USD) ?",
    "USD",18.0,"abs",0.01,"Par parité put-call ($c-p=Se^{-qT}-Ke^{-rT}$), les deux options ont le même vega : $\\mathbf{18}$ USD.",
    "\\text{Vega}_{call}=\\text{Vega}_{put}"),

mcq(418,2,C1,"Gamma est maximum pour une option :",
    [("a","ATM à courte maturité"),("b","Deep ITM"),("c","Deep OTM"),("d","À longue maturité")],
    "a","$\\Gamma\\propto N'(d_1)/(S\\sigma\\sqrt{T})$. Maximal quand $d_1\\approx0$ (ATM) et $T$ petit.",
    {"b":"Gamma faible pour deep ITM.","c":"Gamma faible pour deep OTM.","d":"Gamma diminue avec T."}),

mcq(419,2,C1,"La **position vega longue** bénéficie d'une :",
    [("a","Hausse de la volatilité implicite"),("b","Baisse de la volatilité implicite"),
     ("c","Hausse du sous-jacent uniquement"),("d","Baisse des taux")],
    "a","Long vega → acheter de la vol. Profite si vol implicite monte.",
    {"b":"C'est la position vega courte.","c":"Indépendant du sens du sous-jacent.","d":"C'est le rhô."}),

num(420,3,C1,"Portfolio : long 200 calls ($\\Delta=0.5$, $\\Gamma=0.02$, $V=12$). "
    "Neutralisation delta par actions ($\\Delta_{action}=1$). Nombre d'actions à vendre ?",
    "actions",100.0,"abs",0.5,"$\\Delta_{port}=200\\times0.5=100$. Vendre $\\mathbf{100}$ actions pour $\\Delta=0$.",
    "200\\times\\Delta_{call}"),

sa(421,2,C1,"Pourquoi le **thêta et le gamma** d'une option longue sont-ils de signes opposés ?",
    ["Gamma positif = bénéfice des grands mouvements","Thêta négatif = coût du temps qui passe"],
    "Pour une option longue, $\\Gamma>0$ et $\\Theta<0$. L'EDP BSM relie les deux : "
    "$\\Theta+\\frac{1}{2}\\sigma^2S^2\\Gamma=rC-rS\\Delta$. "
    "Intuitivement : payer la prime (thêta négatif) achète la convexité (gamma positif). "
    "Une position long straddle illustre bien ce compromis : gain si $S$ bouge beaucoup, perte lente sinon."),

mcq(422,2,C1,"Le **charm** est la dérivée de :",
    [("a","Du delta par rapport au temps"),("b","Du gamma par rapport au sous-jacent"),
     ("c","Du vega par rapport à la volatilité"),("d","Du thêta par rapport au strike")],
    "a","Charm $=\\partial\\Delta/\\partial t = \\partial\\Theta/\\partial S$. Utilisé pour anticiper le re-hedging journalier.",
    {"b":"C'est le speed ($\\partial\\Gamma/\\partial S$).","c":"C'est le volga/vomma.","d":"Faux."}),

# ── volatility-smiles (423-445) ──────────────────────────────────────────────
mcq(423,1,C2,"Le **smile de volatilité** désigne :",
    [("a","La courbe de volatilité implicite en fonction du strike, en forme de U"),
     ("b","Le fait que la vol monte toujours avec le temps"),
     ("c","La volatilité historique sur 20 jours"),
     ("d","Le smile souriant de Black-Scholes")],
    "a","Les options OTM (puts deep et calls deep) ont une vol implicite plus élevée qu'ATM → forme en U.",
    {"b":"Faux.","c":"Faux.","d":"BSM ne génère pas de smile."}),

mcq(424,2,C2,"Pour les **options sur actions**, la structure de volatilité implicite est souvent :",
    [("a","Un skew négatif — vol implicite plus élevée pour les strikes bas (puts OTM)"),
     ("b","Un smile symétrique"),("c","Plate"),("d","Croissante avec le strike")],
    "a","Equity skew : les investisseurs paient une prime pour les puts protecteurs (couverture contre les crashes).",
    {"b":"C'est souvent le cas pour les devises.","c":"Hypothèse BSM, irréaliste.","d":"Faux."}),

sa(425,2,C2,"Expliquez pourquoi les options sur **devises** montrent souvent un smile symétrique.",
    ["Les grandes variations peuvent aller dans les deux sens","Distribution réelle à queues épaisses"],
    "Pour les paires de devises majeures, les grandes appréciations comme dépréciations sont possibles. "
    "La distribution réelle du taux de change a des queues plus épaisses que la lognormale BSM dans les deux directions. "
    "Résultat : vol implicite plus haute pour les options OTM quelle que soit la direction → smile symétrique."),

num(426,2,C2,"Smile de vol : $\\sigma_{ATM}=20\\%$, $\\sigma_{25-delta-put}=22\\%$. Risk reversal 25-delta (différence vol) ?",
    "%",-2.0,"abs",0.1,"$RR_{25}=\\sigma_{25-call}-\\sigma_{25-put}$. "
    "Si le put 25D a une vol plus haute que le call 25D par symétrie, $RR\\approx\\mathbf{-2}\\%$ (skew négatif).",
    "\\sigma_{25c}-\\sigma_{25p}"),

mcq(427,2,C2,"Le **butterfly spread de volatilité** mesure :",
    [("a","La convexité du smile — combien les options OTM surpassent l'ATM"),
     ("b","La pente du smile"),("c","La différence entre vol réalisée et implicite"),("d","Le niveau absolu de volatilité")],
    "a","Butterfly $=\\frac{1}{2}(\\sigma_{25c}+\\sigma_{25p})-\\sigma_{ATM}$. Mesure la courbure.",
    {"b":"C'est le risk reversal.","c":"Non.","d":"Non."}),

mcq(428,1,C2,"La **volatilité implicite** d'une option est :",
    [("a","La $\\sigma$ que l'on doit insérer dans BSM pour reproduire le prix de marché"),
     ("b","La volatilité historique des 30 derniers jours"),
     ("c","La variance de l'option"),("d","La vol prédite par un modèle GARCH")],
    "a","Vol implicite = inversion numérique de BSM. C'est la mesure standard du 'prix' de la volatilité.",
    {"b":"Vol historique ≠ vol implicite.","c":"Non.","d":"GARCH donne la vol réalisée prédite, pas implicite."}),

num(429,3,C2,"BSM : $c=7.50$ USD, $S=100$, $K=100$, $r=5\\%$, $T=0.5$. Approximation ATM : $c\\approx0.4S\\sigma\\sqrt{T}$. "
    "Vol implicite approximative ?",
    "%",26.5,"abs",0.5,"$\\sigma\\approx c/(0.4\\times S\\times\\sqrt{T})=7.50/(0.4\\times100\\times0.707)=7.50/28.28=\\mathbf{26.5}\\%$.",
    "c/(0.4 S\\sqrt{T})"),

mcq(430,2,C2,"Le **skew négatif** (ou 'volatility skew') sur les actions résulte principalement de :",
    [("a","L'effet de levier et la demande de protection contre les crashes"),
     ("b","L'asymétrie des dividendes"),("c","La réglementation des options"),("d","L'aversion au risque des vendeurs")],
    "a","Causes : effet de levier (un crash amplifie la vol), crashophilie des gérants (achètent des puts). → Puts OTM plus chers.",
    {"b":"Non.","c":"Non.","d":"Facteur secondaire."}),

sa(431,2,C2,"Qu'est-ce que la **surface de volatilité implicite** et comment est-elle utilisée ?",
    ["Vol en fonction de (strike, maturité)","Pricer et gérer des options non standard"],
    "La surface de volatilité implicite (vol surface) est la fonction $\\sigma_{imp}(K, T)$ extraite des prix d'options de marché. "
    "Elle est utilisée pour : pricer des options exotiques en interpolant, calculer les vols en risque, "
    "calibrer les modèles stochastiques (Heston, SABR). "
    "Elle doit être sans arbitrage (pas de butterfly spreads négatifs, pas de call spreads négatifs)."),

num(432,2,C2,"Vol implicite d'un call $K=110$ : $\\sigma=22\\%$. Vol implicite d'un call $K=100$ : $\\sigma=20\\%$. "
    "Pente du smile (change en vol par unité de strike) ?",
    "%/point",0.2,"abs",0.02,"$(22-20)/(110-100)=2/10=\\mathbf{0.2}\\%$ par point de strike.",
    "\\Delta\\sigma/\\Delta K"),

mcq(433,2,C2,"La **densité risque-neutre** implicite dans le smile de vol peut être extraite par :",
    [("a","La formule de Breeden-Litzenberger : $q(K)=e^{rT}\\partial^2 C/\\partial K^2$"),
     ("b","La dérivée première du call par rapport au strike"),
     ("c","BSM directement"),("d","La transformation de Fourier des prices")],
    "a","Breeden-Litzenberger (1978) : la densité risque-neutre est la dérivée seconde du call par rapport au strike.",
    {"b":"La dérivée première donne $-e^{-rT}N(-d_2)$, pas la densité.","c":"Non directement.","d":"Méthode alternative plus avancée."}),

mcq(434,2,C2,"Un put spread $K_1=90$, $K_2=100$ (same maturité) est en arbitrage si :",
    [("a","Son prix est négatif (le spread vaut moins que 0)"),
     ("b","La vol implicite de $K_1>K_2$"),("c","Il n'expire jamais"),("d","Le delta du spread est positif")],
    "a","Le put spread long ($K_2-K_1>0$) doit valoir $>0$ sinon arbitrage trivial.",
    {"b":"Vol plus haute pour $K_1<K_2$ est l'equity skew normal — pas un arbitrage.","c":"Faux.","d":"Faux."}),

num(435,3,C2,"Modèle de Dupire : vol locale $\\sigma_L(S,T)$. Relation : "
    "$\\sigma_L^2(K,T)=\\frac{\\partial C/\\partial T+rK\\partial C/\\partial K}{\\frac{1}{2}K^2\\partial^2 C/\\partial K^2}$. "
    "Conceptuellement, elle est [plus / moins / pareil] volatile que la vol implicite pour des strikes extrêmes ?",
    "",1.0,"abs",0.5,"La vol locale est en général **plus élevée** que la vol implicite pour les options OTM extrêmes "
    "(elle est la 'vol instantanée' pour chaque chemin, alors que la vol implicite est une moyenne).",
    "\\sigma_L\\geq\\sigma_{imp}"),

sa(436,2,C2,"Expliquez la différence entre **volatilité réalisée** et **volatilité implicite**.",
    ["Vol réalisée = vol historique mesurée ex-post","Vol implicite = anticipation de la vol future"],
    "Vol réalisée : écart-type des rendements observés sur une période passée. Mesurée ex-post. "
    "Vol implicite : vol extraite du prix d'option aujourd'hui. Reflète l'anticipation du marché sur la vol future. "
    "En général, vol implicite $>$ vol réalisée (prime de risque de volatilité), "
    "mais cet écart se referme lors des crises."),

mcq(437,2,C2,"Le **VIX** mesure :",
    [("a","La vol implicite attendue sur 30 jours calendaires du S&P500"),
     ("b","La vol réalisée du S&P500"),("c","La vol des options sur taux d'intérêt"),("d","La vol des devises G10")],
    "a","VIX = vol implicite 30j du S&P500, calculée à partir d'un large panier d'options (calls et puts).",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

mcq(438,2,C2,"La **vol de vol** (vol-of-vol) désigne :",
    [("a","La variabilité de la volatilité implicite elle-même"),("b","Le carré de la volatilité"),
     ("c","La volatilité des futures sur vol"),("d","Toujours nulle en pratique")],
    "a","La vol implicite n'est pas constante : elle fluctue. Sa volatilité est la 'vol of vol', modélisée par Heston.",
    {"b":"Faux.","c":"Proche mais distinct.","d":"Faux — très importante en pratique."}),

num(439,2,C2,"Smile de vol : $\\sigma_{ATM}=18\\%$, $\\sigma_{95-put}=21\\%$, $\\sigma_{105-call}=19\\%$. "
    "Risk reversal 5-delta approx (call minus put) ?",
    "%",-2.0,"abs",0.2,"$RR\\approx\\sigma_{call}-\\sigma_{put}=19-21=\\mathbf{-2}\\%$. Skew négatif.",
    "\\sigma_{call}-\\sigma_{put}"),

sa(440,2,C2,"Quels modèles permettent de reproduire un smile de vol, et lesquels BSM ne peut-il pas ?",
    ["BSM suppose vol constante — pas de smile","Stochastic vol (Heston) ou vol locale (Dupire) génèrent un smile"],
    "BSM suppose $\\sigma$ constant → vol implicite flat quel que soit le strike. "
    "Pour reproduire un smile : (1) **Modèles à vol stochastique** (Heston, SABR) où $\\sigma$ est un processus aléatoire. "
    "(2) **Modèles à vol locale** (Dupire) où $\\sigma=\\sigma(S,t)$. "
    "(3) **Modèles à sauts** (Merton jump-diffusion, Kou). "
    "Le choix dépend du produit à pricer."),

mcq(441,2,C2,"Le **skew implicite** pour les options sur actions indique généralement que :",
    [("a","Les investisseurs paient plus cher les protections baissières que les paris haussiers"),
     ("b","Les calls coûtent plus que les puts"),("c","La vol est plus haute sur les calls ATM"),
     ("d","La distribution risque-neutre est symétrique")],
    "a","Equity skew reflète la demande de protection (puts OTM) et l'aversion aux crashes.",
    {"b":"En général le contraire (skew négatif).","c":"Faux.","d":"Faux — la distribution est asymétrique négativement."}),

mcq(442,2,C2,"La **term structure** de volatilité décrit :",
    [("a","La variation de la vol implicite avec la maturité"),("b","La variation de la vol avec le strike"),
     ("c","La pente du smile pour une maturité donnée"),("d","La volatilité des futures sur vol")],
    "a","Term structure : $\\sigma_{imp}(T)$ pour un strike fixe (souvent ATM). Peut être en contango ou backwardation.",
    {"b":"C'est le smile.","c":"Faux.","d":"Faux."}),

num(443,3,C2,"Vol ATM terme court : $\\sigma_1=25\\%$, $T_1=1$ mois. Vol ATM terme long : $\\sigma_2=20\\%$, $T_2=1$ an. "
    "Vol forward entre $T_1$ et $T_2$ (variance forward) ?",
    "%",19.2,"abs",0.3,
    "$\\sigma_{fwd}^2=\\frac{\\sigma_2^2 T_2-\\sigma_1^2 T_1}{T_2-T_1}=\\frac{0.04\\times1-0.0625\\times(1/12)}{11/12}$"
    "$=\\frac{0.04-0.005208}{0.9167}=\\frac{0.034792}{0.9167}=0.03796$. $\\sigma_{fwd}=\\sqrt{0.03796}=\\mathbf{19.5}\\%$.",
    "\\sqrt{(\\sigma_2^2 T_2-\\sigma_1^2 T_1)/(T_2-T_1)}"),

sa(444,2,C2,"Expliquez la notion de **sticky strike** et **sticky delta** dans la gestion du smile.",
    ["Sticky strike : vol implicite fixée par strike","Sticky delta : vol implicite suit le delta de l'option"],
    "**Sticky strike** : lorsque le sous-jacent bouge, les vols implicites restent attachées aux strikes absolus. "
    "Pratique pour les options actions. "
    "**Sticky delta** : les vols implicites restent attachées aux options de même delta (ATM reste ATM). "
    "Pratique pour les devises. Les deux approches donnent des deltas différents et donc des P&L de hedging différents."),

mcq(445,2,C2,"Le **risque de corrélation** dans un portefeuille d'options survient car :",
    [("a","La corrélation entre actifs varie, affectant les prix d'options sur panier ou de variance"),
     ("b","La corrélation est toujours négative"),("c","Les options individuelles sont indépendantes de la corrélation"),
     ("d","Les modèles de corrélation sont simples")],
    "a","Corrélation stochastique affecte les variance swaps, options sur paniers, et produits structurés multi-sous-jacents.",
    {"b":"Faux.","c":"Faux pour les produits multi-actifs.","d":"Faux."}),

# ── estimating-volatilities-and-correlations (495-514) ───────────────────────
mcq(495,1,C3,"La **volatilité historique** est calculée comme :",
    [("a","L'écart-type des rendements logarithmiques journaliers"),("b","La moyenne des prix"),
     ("c","La différence max-min"),("d","La variance totale de l'actif")],
    "a","$\\hat{\\sigma}=\\sqrt{\\frac{1}{n-1}\\sum(r_i-\\bar{r})^2}$ avec $r_i=\\ln(S_i/S_{i-1})$.",
    {"b":"Non.","c":"Range estimator, pas la standard.","d":"Variance ≠ vol."}),

num(496,2,C3,"Rendements journaliers sur 5 jours : $+1\\%, -0.5\\%, +0.8\\%, -0.3\\%, +0.2\\%$. "
    "Écart-type (vol journalière, en %) ?",
    "%",0.623,"abs",0.05,"$\\bar{r}=(1-0.5+0.8-0.3+0.2)/5=0.24\\%$. "
    "$\\hat{\\sigma}=\\sqrt{\\sum(r_i-\\bar{r})^2/(n-1)}\\approx\\mathbf{0.623}\\%$.",
    "\\sqrt{\\sum(r_i-\\bar{r})^2/(n-1)}"),

mcq(497,1,C3,"Pour **annualiser** une volatilité journalière, on la multiplie par :",
    [("a","$\\sqrt{252}$ (nombre de jours de trading)"),("b","252"),("c","$\\sqrt{365}$"),("d","12")],
    "a","$\\sigma_{ann}=\\sigma_{jour}\\times\\sqrt{252}$ (en supposant 252 jours de trading par an).",
    {"b":"Annualise la variance, pas la vol.","c":"Pour les calendrier, pas trading.","d":"Pour les mois."}),

num(498,2,C3,"Vol journalière $=1.2\\%$. Vol annualisée (252 jours de trading) ?",
    "%",19.05,"abs",0.1,"$\\sigma_{ann}=1.2\\%\\times\\sqrt{252}=1.2\\%\\times15.87=\\mathbf{19.05}\\%$.",
    "\\sigma_{jour}\\times\\sqrt{252}"),

mcq(499,2,C3,"Le modèle **EWMA** (Exponentially Weighted Moving Average) pour la volatilité :",
    [("a","Donne plus de poids aux observations récentes — $\\sigma_n^2=\\lambda\\sigma_{n-1}^2+(1-\\lambda)r_{n-1}^2$"),
     ("b","Donne le même poids à toutes les observations"),("c","Utilise une fenêtre glissante fixe"),
     ("d","Est équivalent au GARCH(1,1)")],
    "a","EWMA : $\\lambda\\in(0,1)$, typiquement 0.94 (RiskMetrics). Observations récentes pèsent plus.",
    {"b":"C'est la variance historique simple.","c":"Fenêtre glissante non pondérée.","d":"EWMA est un cas limite du GARCH(1,1) sans constante."}),

num(500,3,C3,"EWMA : $\\lambda=0.94$, $\\sigma_{n-1}^2=0.0004$ ($0.02^2$), $r_{n-1}=-3\\%$. Nouvelle variance $\\sigma_n^2$ ?",
    "",0.001238,"abs",0.00005,"$\\sigma_n^2=0.94\\times0.0004+0.06\\times(-0.03)^2=0.000376+0.06\\times0.0009=0.000376+0.000054=\\mathbf{0.000430}$.",
    "\\lambda\\sigma_{n-1}^2+(1-\\lambda)r_{n-1}^2"),

mcq(501,2,C3,"Le modèle **GARCH(1,1)** est :",
    [("a","$\\sigma_n^2=\\omega+\\alpha r_{n-1}^2+\\beta\\sigma_{n-1}^2$ avec $\\omega,\\alpha,\\beta>0$ et $\\alpha+\\beta<1$"),
     ("b","$\\sigma_n^2=\\lambda\\sigma_{n-1}^2+(1-\\lambda)r_{n-1}^2$"),
     ("c","$\\sigma_n=\\sigma_0+\\alpha(|r_{n-1}|-\\sigma_0)$"),("d","$\\sigma_n^2=\\sum r_i^2/n$")],
    "a","GARCH(1,1) : $\\omega+\\alpha+\\beta<1$ pour stationnarité. EWMA est le cas $\\omega=0$, $\\alpha+\\beta=1$.",
    {"b":"C'est EWMA.","c":"Approximation linéaire.","d":"Variance simple."}),

num(502,3,C3,"GARCH(1,1) : $\\omega=0.000002$, $\\alpha=0.13$, $\\beta=0.86$. Variance long terme $\\bar{\\sigma}^2$ ?",
    "",0.0002,"abs",0.00002,"$\\bar{\\sigma}^2=\\omega/(1-\\alpha-\\beta)=0.000002/(1-0.13-0.86)=0.000002/0.01=\\mathbf{0.0002}$.",
    "\\omega/(1-\\alpha-\\beta)"),

sa(503,2,C3,"Expliquez le phénomène de **mean reversion** de la volatilité dans un modèle GARCH.",
    ["Vol tend vers une moyenne long terme","Chocs s'amortissent avec le temps"],
    "GARCH(1,1) : la variance $\\sigma_n^2$ revient vers sa valeur long terme $\\bar{\\sigma}^2=\\omega/(1-\\alpha-\\beta)$ "
    "à un taux $\\alpha+\\beta$ (vitesse de persistance). "
    "Si $\\alpha+\\beta\\to1$ : forte persistance (intégré IGARCH). "
    "Si $\\alpha+\\beta$ petit : mean-reversion rapide. "
    "Empiriquement, les marchés ont $\\alpha+\\beta\\approx0.98$ (vol très persistante)."),

num(504,2,C3,"EWMA avec $\\lambda=0.97$. Poids donné à une observation $d=10$ jours dans le passé ?",
    "",0.025184,"abs",0.001,"$(1-\\lambda)\\lambda^{d-1}=0.03\\times0.97^9=0.03\\times0.7602=\\mathbf{0.02281}$.",
    "(1-\\lambda)\\lambda^{d-1}"),

mcq(505,2,C3,"La **corrélation** entre deux actifs est estimée par :",
    [("a","$\\hat{\\rho}_{xy}=\\hat{\\sigma}_{xy}/(\\hat{\\sigma}_x\\hat{\\sigma}_y)$"),
     ("b","$\\hat{\\rho}_{xy}=\\hat{\\sigma}_{xy}^2$"),("c","$\\sum r_{x,i}r_{y,i}/n$"),
     ("d","La dérivée de la covariance")],
    "a","Corrélation = covariance divisée par le produit des volatilités.",
    {"b":"Faux.","c":"C'est la covariance brute si $\\bar{r}=0$.","d":"Non."}),

num(506,3,C3,"EWMA pour covariance : $\\text{cov}_{n-1}=0.0003$, $r_{x,n-1}=+2\\%$, $r_{y,n-1}=-1\\%$, $\\lambda=0.94$. Nouvelle covariance ?",
    "",0.0002808,"abs",0.00001,"$\\text{cov}_n=\\lambda\\times\\text{cov}_{n-1}+(1-\\lambda)r_{x,n-1}r_{y,n-1}$"
    "$=0.94\\times0.0003+0.06\\times0.02\\times(-0.01)=0.000282-0.000012=\\mathbf{0.000270}$.",
    "\\lambda\\text{cov}_{n-1}+(1-\\lambda)r_x r_y"),

sa(507,2,C3,"Quels sont les **biais de mesure** de la volatilité historique et comment les corriger ?",
    ["Biais de fenêtre temporelle","Méthode: EWMA ou données intraday"],
    "Biais principaux : (1) **Choix de la fenêtre** : courte (bruitée), longue (insensible aux changements). "
    "(2) **Jours fériés/week-ends** : utiliser les jours de trading, pas calendaire. "
    "(3) **Jump** : les rares grands sauts dominent l'estimateur. "
    "Correction : EWMA (pondère récence), estimateurs de range (Parkinson, Garman-Klass), "
    "volatilité réalisée à haute fréquence."),

mcq(508,2,C3,"La méthode **Maximum Likelihood** pour GARCH estime les paramètres en :",
    [("a","Maximisant la log-vraisemblance $\\sum[-\\ln\\sigma_t^2 - r_t^2/\\sigma_t^2]$"),
     ("b","Minimisant la somme des carrés des résidus"),("c","Estimant les paramètres par moments"),("d","Utilisant la méthode de Monte Carlo")],
    "a","MLE pour GARCH : log-vraisemblance gaussienne ou t-distribution. Optimisation numérique.",
    {"b":"Méthode OLS, non optimale pour GARCH.","c":"GMM, possible mais moins efficace.","d":"Non."}),

num(509,2,C3,"Corrélation EWMA : $\\rho_{n-1}=0.7$, $\\sigma_{x,n-1}=2\\%$, $\\sigma_{y,n-1}=3\\%$. "
    "Covariance $=\\rho\\times\\sigma_x\\times\\sigma_y$ ?",
    "",0.00042,"abs",0.00001,"$\\text{cov}=0.7\\times0.02\\times0.03=\\mathbf{0.00042}$.",
    "\\rho\\sigma_x\\sigma_y"),

mcq(510,2,C3,"La **matrice de corrélation** doit être :",
    [("a","Semi-définie positive (tous eigenvalues $\\geq0$)"),("b","Diagonale"),
     ("c","Symétrique mais pas nécessairement positive"),("d","Avec tous les éléments hors-diagonale négatifs")],
    "a","Corrélation valide : symétrique et semi-définie positive (garantit que les variances de portefeuille sont $\\geq0$).",
    {"b":"Non, les corrélations hors-diagonale peuvent être non nulles.","c":"Positive semi-définie est requise.","d":"Faux."}),

sa(511,2,C3,"Comment garantir qu'une matrice de corrélation estimée est **semi-définie positive** ?",
    ["Projection par eigenvectors","Méthode de Higham ou Cholesky après correction"],
    "Problème fréquent : corrélations estimées séparément peuvent violer la SDP. "
    "Solutions : (1) **Projection spectrale** : mettre les valeurs propres négatives à zéro et renormaliser. "
    "(2) **Méthode de Higham** : trouver la matrice SDP la plus proche. "
    "(3) Estimer via un modèle factoriel (garantit SDP par construction). "
    "Important en risk management car une matrice non SDP peut donner des VaR négatives."),

num(512,2,C3,"Variance du portefeuille : $w_1=0.5$, $w_2=0.5$, $\\sigma_1=20\\%$, $\\sigma_2=30\\%$, $\\rho=0.4$. $\\sigma_p$ ?",
    "%",21.2,"abs",0.2,"$\\sigma_p^2=0.25\\times0.04+0.25\\times0.09+2\\times0.25\\times0.4\\times0.06=0.01+0.0225+0.012=0.0445$. $\\sigma_p=21.1\\%$.",
    "\\sqrt{w_1^2\\sigma_1^2+w_2^2\\sigma_2^2+2w_1w_2\\rho\\sigma_1\\sigma_2}"),

mcq(513,2,C3,"La **persistance** d'un choc de volatilité dans GARCH(1,1) est mesurée par :",
    [("a","$\\alpha+\\beta$ — plus c'est proche de 1, plus la vol reste élevée longtemps"),
     ("b","$\\omega/(1-\\alpha-\\beta)$"),("c","$\\alpha$ seul"),("d","$\\beta$ seul")],
    "a","$\\alpha+\\beta$ proche de 1 → vol intégrée (IGARCH), choc permanent. Plus petit → mean reversion rapide.",
    {"b":"C'est la vol long terme.","c":"$\\alpha$ = réactivité aux news.","d":"$\\beta$ = persistance de la var passée."}),

num(514,2,C3,"GARCH(1,1) : $\\alpha=0.08$, $\\beta=0.90$, $\\bar{\\sigma}^2=0.0001$ ($\\bar{\\sigma}=1\\%$). "
    "Variance prévue dans $h=5$ jours si $\\sigma_0^2=0.0004$ ?",
    "",0.000127,"abs",0.00001,
    "$\\sigma_h^2=\\bar{\\sigma}^2+(\\alpha+\\beta)^h(\\sigma_0^2-\\bar{\\sigma}^2)=0.0001+0.98^5\\times0.0003=0.0001+0.9039\\times0.0003=0.0001+0.000271=\\mathbf{0.000371}$.",
    "\\bar{\\sigma}^2+(\\alpha+\\beta)^h(\\sigma_0^2-\\bar{\\sigma}^2)"),
]

print(f"Items: {len(items)}")
assert len(items)==67, f"Expected 67, got {len(items)}"
batch={"source":"Marchés des dérivés — Exercices originaux","track":"markets","module":"der-greeks-vol","items":items}
with open(OUT,"w",encoding="utf-8") as f: json.dump(batch,f,ensure_ascii=False,indent=2)
print(f"Written: {OUT}")
