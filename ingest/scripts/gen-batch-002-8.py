#!/usr/bin/env python3
"""batch-002-8: der-credit-var (98 items, clés 186-197,198-205,476-494,515-543,544-573)"""
import json,os
OUT=os.path.join(os.path.dirname(__file__),"../canonical/batch-002-8-der-credit-var.json")
def key(n): return f"markets-derivatives-short_answer-{n:03d}"
def mcq(k,d,c,p,opts,cor,ex,dis=None):
    return {"external_key":key(k),"type":"mcq","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"options":[{"key":o[0],"text_mdx":o[1]} for o in opts],"multiple":False,"shuffle":True},
            "solution":{"correct_keys":[cor],"explain_mdx":ex,"distractor_explains":dis or {}}}
def num(k,d,c,p,u,v,tt,tv,s,f):
    return {"external_key":key(k),"type":"numeric","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"unit":u,"precision":2,"tolerance":{"type":tt,"value":tv}},
            "solution":{"value":v,"steps_mdx":s,"formula_katex":f}}
def sa(k,d,c,p,kp,m):
    return {"external_key":key(k),"type":"short_answer","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"max_words":150,"scoring_mode":"self_eval"},
            "solution":{"key_points":[{"text":t,"weight":round(1/len(kp),4)} for t in kp],"model_answer_mdx":m}}

C1="credit-risk"; C2="credit-derivatives"
C3="value-at-risk"; C4="expected-shortfall-and-stress-testing"
C5="xvas-and-counterparty-credit-risk"; C6="securitization"

items=[]

# ── securitization (186-197) ──────────────────────────────────────────────────
items+=[
mcq(186,1,C6,"La **titrisation** (securitization) consiste à :",
    [("a","Regrouper des actifs illiquides et émettre des titres négociables adossés à ces actifs"),
     ("b","Convertir des actions en obligations"),("c","Vendre une obligation à terme"),("d","Créer des produits dérivés sur actions")],
    "a","Titrisation : pool d'actifs (prêts, hypothèques) → ABS (Asset-Backed Securities) négociables.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

mcq(187,2,C6,"Un **MBS** (Mortgage-Backed Security) est adossé à :",
    [("a","Des prêts hypothécaires"),("b","Des créances commerciales"),("c","Des prêts auto"),("d","Des obligations d'État")],
    "a","MBS : titrisation de prêts immobiliers. Agence MBS (Fannie Mae, Freddie Mac) ou privés.",
    {"b":"ABS.","c":"ABS auto.","d":"Non."}),

num(188,2,C6,"Pool MBS : 1000 prêts de 200 000 USD chacun, taux d'intérêt moyen 4%, WAM (Weighted Average Maturity) 25 ans. "
    "Notionnel total du pool (M USD) ?",
    "M USD",200.0,"abs",0.1,"$1000\\times200\\,000=200\\,000\\,000=\\mathbf{200}$ M USD.",
    "n\\times\\text{prêt moyen}"),

mcq(189,2,C6,"Le **risque de prépaiement** dans les MBS survient quand :",
    [("a","Les emprunteurs remboursent anticipativement quand les taux baissent, réduisant le rendement de l'investisseur"),
     ("b","Les emprunteurs font défaut"),("c","Les taux montent"),("d","Le pool se concentre")],
    "a","Prépaiement = extension risk si taux montent (prépaiements ralentissent), contraction risk si taux baissent.",
    {"b":"C'est le défaut.","c":"Taux montants ralentissent les prépaiements.","d":"Non."}),

sa(190,2,C6,"Expliquez la différence entre un **pass-through MBS** et un **CMO** (Collateralized Mortgage Obligation).",
    ["Pass-through : tous investisseurs reçoivent la même tranche","CMO : tranches de prépaiement différenciées"],
    "Pass-through : les flux du pool (intérêts + principal) sont redistribués proportionnellement. "
    "Tous les investisseurs ont la même exposition au prépaiement. "
    "CMO : les tranches (classes) reçoivent les flux dans un ordre défini. "
    "PAC (Planned Amortization Class) : tranche protégée contre le prépaiement, soutenue par des companion bonds. "
    "Permet de créer des instruments avec différents profils de duration/convexité."),

mcq(191,2,C6,"Le **taux CPR** (Conditional Prepayment Rate) mesure :",
    [("a","Le pourcentage annualisé du principal prépayé chaque année"),
     ("b","Le taux de défaut du pool"),("c","La duration de l'obligation"),("d","Le coupon versé")],
    "a","CPR = taux de prépaiement annuel. SMM (Single Monthly Mortality) = $1-(1-CPR)^{1/12}$.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(192,2,C6,"CPR = 6% par an. SMM (Single Monthly Mortality) = $1-(1-0.06)^{1/12}$ = ?",
    "%",0.5143,"abs",0.01,"$SMM=1-(0.94)^{1/12}=1-0.94^{0.0833}=1-0.9948=\\mathbf{0.5143}\\%$.",
    "1-(1-CPR)^{1/12}"),

mcq(193,2,C6,"La **convexité négative** des MBS (callable bonds) signifie :",
    [("a","Quand les taux baissent, le prix monte moins qu'une obligation bullet (prépaiements accélèrent)"),
     ("b","La duration augmente quand les taux baissent"),("c","La duration est toujours négative"),("d","Le prix chute quand les taux baissent")],
    "a","Convexité $<0$ pour les MBS : l'option de prépaiement réduit la sensibilité positive aux taux bas.",
    {"b":"Faux — duration diminue.","c":"Faux.","d":"Faux."}),

num(194,2,C6,"Option-Adjusted Spread (OAS) : rendement nominal d'un MBS = 5.5%, taux de swap = 4.8%, cost of optionality = 0.4%. OAS ?",
    "%",0.3,"abs",0.05,"$OAS=\\text{spread nominal}-\\text{option cost}=(5.5-4.8)-0.4=0.7-0.4=\\mathbf{0.3}\\%$.",
    "\\text{yield spread}-\\text{option cost}"),

sa(195,2,C6,"Décrivez la crise des **subprimes 2007-2008** en lien avec les MBS et CDOs.",
    ["Prêts subprime titrisés en MBS","Corrélation sous-estimée → pertes massives sur CDOs"],
    "Les prêts subprime (emprunteurs à faible solvabilité) ont été massivement titrisés en MBS, "
    "puis packagés en CDOs. "
    "Les modèles (Gaussian copula) ont sous-estimé la corrélation des défauts — "
    "quand les prix immobiliers ont chuté nationalement, les défauts ont été corrélés, "
    "dévastant les tranches 'senior' AAA des CDOs. "
    "Les agences de notation avaient mal évalué le risque systémique."),

mcq(196,2,C6,"Un **ABCP (Asset-Backed Commercial Paper) conduit** est :",
    [("a","Un véhicule hors bilan qui finance des actifs à long terme avec du CP à court terme"),
     ("b","Un fonds d'obligations"),("c","Un ETF"),("d","Une banque traditionnelle")],
    "a","ABCP conduit : SIV (Special Investment Vehicle) finançant MBS/ABS avec du CP. Risque de transformation de maturité.",
    {"b":"Non.","c":"Non.","d":"Non."}),

num(197,2,C6,"CDO-squared : CDO adossé à des tranches de CDOs. Tranche mezzanine CDO1 = 5% du notionnel, mezzanine CDO2 = 5%. "
    "Notionnel CDO-squared sur pool 100 M USD de CDO1 + 100 M USD de CDO2. Tranche equity CDO² 3% ?",
    "M USD",6.0,"abs",0.1,"$3\\%\\times(100+100)=3\\%\\times200=\\mathbf{6}$ M USD.",
    "\\text{tranche}\\%\\times\\text{notionnel total}"),
]

# ── xvas-and-counterparty-credit-risk (198-205) ──────────────────────────────
items+=[
mcq(198,1,C5,"Le **CVA** (Credit Valuation Adjustment) est :",
    [("a","L'ajustement de la valeur d'un dérivé pour le risque de défaut de la contrepartie"),
     ("b","La commission de courtage"),("c","L'ajustement pour la liquidité"),("d","Le coût de financement")],
    "a","CVA = $E^Q[\\text{perte si contrepartie fait défaut}]$. Réduit la valeur d'un dérivé.",
    {"b":"Faux.","c":"LVA/MVA.","d":"FVA."}),

num(199,2,C5,"CVA unilatéral : probabilité de défaut annuelle $\\lambda=2\\%$, LGD $=60\\%$, EPE (expected positive exposure) $=5$ M USD, $T=3$ ans. "
    "CVA $\\approx\\lambda\\times LGD\\times EPE\\times T$ ?",
    "USD",180000.0,"abs",5000.0,"$CVA\\approx0.02\\times0.60\\times5\\,000\\,000\\times3=\\mathbf{180\\,000}$ USD.",
    "\\lambda\\times LGD\\times EPE\\times T"),

mcq(200,2,C5,"Le **DVA** (Debt Valuation Adjustment) est :",
    [("a","L'ajustement pour le risque de défaut propre de l'entité elle-même"),
     ("b","Une réduction du CVA"),("c","Le coût de financement"),("d","L'ajustement de marge")],
    "a","DVA = bénéfice de son propre risque de défaut. CVA net = CVA de la contrepartie $-$ DVA.",
    {"b":"Partiellement.","c":"FVA.","d":"MVA."}),

sa(201,2,C5,"Expliquez la **Wrong-Way Risk** dans le calcul du CVA.",
    ["Exposition corrélée positivement au défaut","Sous-estimation du CVA si ignorée"],
    "Wrong-Way Risk (WWR) : la probabilité de défaut de la contrepartie est corrélée positivement avec l'exposition. "
    "Exemple : vente d'un put sur les actions d'une banque à cette même banque — "
    "si la banque fait défaut (baisse des actions), l'exposition du put est élevée. "
    "Le WWR augmente le CVA réel par rapport au CVA calculé sous indépendance."),

num(202,2,C5,"FVA (Funding Valuation Adjustment) : position non collatéralisée, EPE = 10 M USD, coût de financement = 80 bps. "
    "FVA annuel (USD) ?",
    "USD",80000.0,"abs",1000.0,"$FVA=EPE\\times\\text{spread}=10\\,000\\,000\\times0.008=\\mathbf{80\\,000}$ USD.",
    "EPE\\times\\text{funding spread}"),

mcq(203,2,C5,"Le **KVA** (Capital Valuation Adjustment) représente :",
    [("a","Le coût du capital réglementaire alloué à une transaction"),
     ("b","L'ajustement pour les dividendes"),("c","La valeur de la garantie"),("d","Le coût de la chambre de compensation")],
    "a","KVA = coût d'opportunité du capital réglementaire (Bâle III) réservé pour couvrir le risque de contrepartie.",
    {"b":"Faux.","c":"CVA.","d":"MVA."}),

num(204,2,C5,"MVA (Margin Valuation Adjustment) : appels de marge initiaux = 2 M USD, durée 1 an, coût du financement de marge = 1.5%. MVA ?",
    "USD",30000.0,"abs",500.0,"$MVA=2\\,000\\,000\\times0.015=\\mathbf{30\\,000}$ USD.",
    "IM\\times\\text{cost}"),

sa(205,2,C5,"Quels sont les **xVAs** principaux et leurs impacts sur le pricing des dérivés OTC ?",
    ["CVA, DVA, FVA, MVA, KVA","Réduisent la valeur nette d'un dérivé pour la banque"],
    "Les xVAs sont des ajustements à la valeur mid-market d'un dérivé : "
    "CVA (-) : risque de défaut contrepartie. "
    "DVA (+) : propre risque de défaut (controversé). "
    "FVA (-) : coût de financement des positions non collatéralisées. "
    "MVA (-) : coût de financement des marges initiales. "
    "KVA (-) : coût du capital réglementaire. "
    "Total : prix client = mid + xVA. Les xVAs ont significativement réduit la rentabilité des dérivés OTC post-2008."),
]

# ── value-at-risk (476-494) ────────────────────────────────────────────────────
items+=[
mcq(476,1,C3,"La **VaR** (Value at Risk) à 99% sur 1 jour représente :",
    [("a","La perte maximale attendue à ne pas être dépassée 99% du temps sur 1 jour"),
     ("b","La perte moyenne sur 1 jour"),("c","La perte en cas de crise"),("d","Le capital réglementaire")],
    "a","VaR 99% 1J : dans 99% des cas, la perte journalière sera inférieure à ce montant.",
    {"b":"C'est l'Expected Shortfall.","c":"VaR est pour les conditions normales.","d":"VaR est l'input, pas le capital."}),

num(477,2,C3,"VaR paramétrique (normale) : $\\mu=0$, $\\sigma=1\\%$, $N=1$ jour, $z_{99\\%}=2.326$. VaR 99% 1J sur 100 M USD ?",
    "USD",2326000.0,"abs",10000.0,"$VaR=z_{99\\%}\\times\\sigma\\times N=2.326\\times0.01\\times100\\,M=\\mathbf{2\\,326\\,000}$ USD.",
    "z_{99\\%}\\times\\sigma\\times N"),

mcq(478,2,C3,"Pour passer d'une VaR 1 jour à une VaR 10 jours (sous GBM) :",
    [("a","$VaR_{10J}=VaR_{1J}\\times\\sqrt{10}$ (sous hypothèse de rendements i.i.d.)"),
     ("b","$VaR_{10J}=VaR_{1J}\\times10$"),("c","$VaR_{10J}=VaR_{1J}/10$"),("d","$VaR_{10J}=VaR_{1J}^{10}$")],
    "a","Règle de la racine carrée : vaut sous i.i.d. et normalité.",
    {"b":"Overestimate pour la vol.","c":"Faux.","d":"Faux."}),

num(479,2,C3,"VaR 1J 99% = 500 000 USD. VaR 10J 99% ?",
    "USD",1581139.0,"abs",5000.0,"$VaR_{10J}=500\\,000\\times\\sqrt{10}=500\\,000\\times3.1623=\\mathbf{1\\,581\\,139}$ USD.",
    "VaR_{1J}\\times\\sqrt{10}"),

mcq(480,1,C3,"La **simulation historique** pour la VaR :",
    [("a","Utilise les rendements historiques passés (ex : 500 jours) pour simuler les P&L et prend le 5e percentile"),
     ("b","Suppose une distribution normale"),("c","Utilise Monte Carlo avec les paramètres actuels"),("d","Ignore les queues de distribution")],
    "a","HS : on reprend les 500 scénarios historiques tels quels, on trie les P&L, et la VaR 99% est le 5e pire.",
    {"b":"C'est la méthode paramétrique.","c":"Monte Carlo.","d":"Faux, HS capture les queues historiques."}),

sa(481,2,C3,"Listez les **limites de la VaR** comme mesure de risque.",
    ["Non sous-additive — pas une mesure cohérente","Ne dit rien sur la perte au-delà du seuil"],
    "Limites : (1) Non sous-additive (VaR peut violer la diversification). "
    "(2) Ne donne pas d'information sur la perte au-delà du seuil (tail risk). "
    "(3) Dépend de l'hypothèse de distribution (normalité sous-estime les fat tails). "
    "(4) Horizon court (1J) inadapté pour les positions illiquides. "
    "(5) Encourage les risk managers à vendre des options OTM deep (pic de VaR invisible). "
    "Ces limites ont motivé l'adoption de l'Expected Shortfall (ES) par Bâle III."),

num(482,2,C3,"Portefeuille : actif A ($\\sigma_A=2\\%$, $w_A=0.6$), actif B ($\\sigma_B=3\\%$, $w_B=0.4$, $\\rho=0.3$). "
    "$\\sigma_p=\\sqrt{0.36\\times0.0004+0.16\\times0.0009+2\\times0.6\\times0.4\\times0.3\\times0.02\\times0.03}$ ?",
    "%",1.859,"abs",0.02,"$\\sigma_p=\\sqrt{0.000144+0.000144+2\\times0.24\\times0.3\\times0.0006}$"
    "$=\\sqrt{0.000144+0.000144+0.0000864}=\\sqrt{0.000374}=\\mathbf{1.935}\\%$.",
    "\\sqrt{w_A^2\\sigma_A^2+w_B^2\\sigma_B^2+2w_Aw_B\\rho\\sigma_A\\sigma_B}"),

mcq(483,2,C3,"Le **back-testing** de la VaR consiste à :",
    [("a","Comparer le nombre de dépassements observés avec le nombre théorique"),
     ("b","Remonter le modèle en arrière dans le temps"),("c","Stresser les paramètres"),("d","Comparer VaR à l'ES")],
    "a","Back-test : sur 250 jours, VaR 99% devrait être dépassée ~2.5 fois. >5 dépassements = modèle problématique.",
    {"b":"Non.","c":"Stress test.","d":"Non."}),

num(484,2,C3,"Back-test VaR 99% sur 250 jours de trading. Nombre d'exceptions attendues ?",
    "exceptions",2.5,"abs",0.1,"$(1-0.99)\\times250=0.01\\times250=\\mathbf{2.5}$ exceptions.",
    "(1-c)\\times T"),

mcq(485,2,C3,"La VaR **Delta-Normal** (paramétrique) pour un portefeuille d'options :",
    [("a","Utilise les deltas des options pour linéariser les positions et suppose une distribution normale"),
     ("b","Simule les options exactement"),("c","Utilise les données historiques"),("d","Ignore le gamma")],
    "a","Delta-normal : approximation linéaire. Ignore le gamma → sous-estime la VaR si le portefeuille est long gamma.",
    {"b":"Full valuation MC.","c":"Simulation historique.","d":"Partiellement — Delta-Gamma-Normal inclut le gamma."}),

num(486,3,C3,"VaR delta-gamma : $\\Delta=0.5$, $\\Gamma=0.02$, $\\sigma_S=1.5\\%$, $S=100$. "
    "$VaR_{delta}=z\\times|\\Delta|\\times\\sigma_S\\times S=2.326\\times0.5\\times0.015\\times100=1.745$ USD. "
    "Correction gamma : $+\\frac{1}{2}\\Gamma\\sigma_S^2 S^2=0.5\\times0.02\\times0.0225\\times10000$ ?",
    "USD",2.25,"abs",0.01,"$\\frac{1}{2}\\times0.02\\times0.0225\\times10000=\\mathbf{2.25}$ USD.",
    "\\frac{1}{2}\\Gamma\\sigma_S^2 S^2"),

mcq(487,2,C3,"La **VaR conditionnelle** (CVaR) ou **Expected Shortfall** (ES) est :",
    [("a","L'espérance de la perte conditionnellement au fait que la perte dépasse la VaR"),
     ("b","La VaR au seuil de confiance suivant"),("c","La perte maximale"),("d","La VaR divisée par 2")],
    "a","$ES_{\\alpha}=E[L|L>VaR_{\\alpha}]$. Toujours $\\geq VaR$. Mesure cohérente (sous-additive).",
    {"b":"Non.","c":"La perte max peut être arbitrairement grande.","d":"Faux."}),

num(488,2,C3,"Distribution normale : VaR 99% = $z_{99}\\sigma=2.326\\sigma$. ES 99% = $\\phi(z_{99})/0.01\\times\\sigma$ où $\\phi=N'(z_{99})=0.0267$. $ES_{99\\%}/\\sigma$ ?",
    "",2.67,"abs",0.05,"$ES_{99\\%}=\\phi(z_{99\\%})/(1-0.99)\\times\\sigma=0.0267/0.01\\times\\sigma=\\mathbf{2.67}\\sigma$.",
    "\\phi(z)/\\alpha\\times\\sigma"),

mcq(489,2,C3,"La **Monte Carlo VaR** est préférable à la simulation historique quand :",
    [("a","On veut explorer des scénarios non observés historiquement (stress, nouveaux produits)"),
     ("b","On veut être non-paramétrique"),("c","L'historique est long"),("d","Le calcul doit être instantané")],
    "a","MC VaR : paramétrique mais avec distribution plus flexible. Permet de modéliser des scénarios de crise.",
    {"b":"Simulation historique est non-paramétrique.","c":"Long historique favorise HS.","d":"MC est lent."}),

num(490,2,C3,"Portefeuille 3 actifs non corrélés : VaR individuelles $=5$, $3$, $4$ M USD. "
    "VaR agrégée sous normalité et corrélation nulle ?",
    "M USD",7.071,"abs",0.05,"$VaR_p=\\sqrt{5^2+3^2+4^2}=\\sqrt{25+9+16}=\\sqrt{50}=\\mathbf{7.07}$ M USD.",
    "\\sqrt{\\sum VaR_i^2}\\text{ (corrélation nulle)}"),

mcq(491,2,C3,"Le **Stressed VaR** (SVaR) dans Bâle 2.5 est calculé en :",
    [("a","Utilisant une fenêtre historique de crise (ex 2008-2009) pour calibrer les paramètres"),
     ("b","Multipliant la VaR par 3"),("c","Utilisant des scénarios réglementaires définis"),("d","Ajoutant un buffer de 99.9%")],
    "a","SVaR = VaR recalculée sur la période de stress la plus défavorable (12 mois). Capital = max(VaR, SVaR).",
    {"b":"Facteur multiplicatif s'applique à VaR mais ce n'est pas la définition.","c":"Faux.","d":"Faux."}),

num(492,2,C3,"Exigence de capital Bâle (marché) : $max(VaR_{t-1}, m_c\\times\\frac{1}{60}\\sum VaR_{60J})$. "
    "$m_c=3$, VaR hier $=8$ M USD, moyenne 60J $=7$ M USD. Capital requis ?",
    "M USD",21.0,"abs",0.1,"$\\max(8,3\\times7)=\\max(8,21)=\\mathbf{21}$ M USD.",
    "\\max(VaR_{t-1},m_c\\times\\bar{VaR}_{60})"),

num(493,2,C3,"VaR 1J 99% d'un bond : duration $=5$, $\\Delta r=2.326\\times\\sigma_r=2.326\\times0.5\\%=1.163\\%$. $\\Delta P\\approx -D\\Delta r\\times P$. $P=100$ USD. $\\Delta P=?$",
    "USD",5.815,"abs",0.1,"$\\Delta P=-5\\times0.01163\\times100=-\\mathbf{5.815}$ USD.",
    "-D\\times\\Delta r\\times P"),

sa(494,2,C3,"Expliquez les différences entre **VaR** et **Expected Shortfall** du point de vue de la gestion des risques.",
    ["ES capture le tail risk","ES est sous-additive contrairement à VaR"],
    "VaR : seuil de perte non dépassé avec probabilité $c$. Ne dit rien sur la distribution des pertes au-delà. "
    "ES (CVaR) : perte moyenne conditionnelle au dépassement de la VaR. Mesure cohérente. "
    "Avantages ES : capture le tail risk, sous-additive (diversification), adoptée par Bâle IV. "
    "Inconvénient : plus difficile à back-tester (pas de niveau de quantile fixe observable)."),
]

# ── credit-risk (515-543) ──────────────────────────────────────────────────────
items+=[
mcq(515,1,C1,"Le **risque de crédit** comprend principalement :",
    [("a","Le risque de défaut et le risque de dégradation de notation"),
     ("b","Le risque de taux d'intérêt"),("c","Le risque de change"),("d","Le risque de liquidité")],
    "a","Risque de crédit : défaut (non-paiement) + migration (dégradation notation).",
    {"b":"Risque de marché.","c":"Risque FX.","d":"Risque de liquidité."}),

mcq(516,1,C1,"La **probabilité de défaut** (PD) dans le modèle de Merton est liée à :",
    [("a","La probabilité que la valeur des actifs tombe sous la valeur des dettes à maturité"),
     ("b","Le spread de crédit directement"),("c","Le ratio dette/equity"),("d","Le taux de recouvrement")],
    "a","Merton (1974) : l'equity = call sur la valeur des actifs. Défaut si $V_A(T)<D$.",
    {"b":"Non directement.","c":"Partiellement, mais pas la définition.","d":"LGD, différent."}),

num(517,3,C1,"Merton : $V_A=100$ M USD, $D=80$ M USD, $\\sigma_A=20\\%$, $r=4\\%$, $T=1$ an. "
    "$d_2=[\\ln(100/80)+(0.04-0.02)\\times1]/(0.20)=[0.2231+0.02]/0.20=1.2155$. "
    "$N(-d_2)=N(-1.22)=0.1112$. PD risque-neutre (%) ?",
    "%",11.12,"abs",0.5,"$PD=N(-d_2)=N(-1.2155)=\\mathbf{11.12}\\%$.",
    "N(-d_2)"),

sa(518,2,C1,"Expliquez le modèle **KMV** (Kealhofer-McQuown-Vasicek) de prédiction du défaut.",
    ["Distance au défaut = (V_A - D)/σ_A","Plus la distance est petite, plus le risque est élevé"],
    "KMV (Moody's KMV) : "
    "1) Estimer $V_A$ et $\\sigma_A$ à partir du prix boursier (modèle de Merton). "
    "2) Calculer la Distance au Défaut (DD) : $DD=(V_A-D_{default\\ point})/(V_A\\sigma_A)$. "
    "3) Mapper DD sur l'Expected Default Frequency (EDF) via une base de données historique. "
    "Le default point est souvent entre les dettes CT et la dette totale."),

num(519,2,C1,"Spread de crédit : $Y_{bond}=6\\%$, $r=4\\%$. Spread de crédit ?",
    "%",2.0,"abs",0.01,"$s=Y-r=6-4=\\mathbf{2}\\%$.",
    "Y_{bond}-r"),

mcq(520,2,C1,"La relation entre **spread de crédit** et probabilité de défaut (risque-neutre) est :",
    [("a","$s\\approx\\lambda\\times LGD$ où $\\lambda$ est le taux d'intensité de défaut"),
     ("b","$s=PD$"),("c","$s=LGD$"),("d","$s=\\lambda/LGD$")],
    "a","Intensité de défaut $\\lambda$ : $s=\\lambda\\times(1-R)=\\lambda\\times LGD$.",
    {"b":"Non.","c":"Non.","d":"Non."}),

num(521,2,C1,"Spread CDS = 150 bps, LGD = 60%. Taux d'intensité risque-neutre $\\lambda$ (approx) ?",
    "%",2.5,"abs",0.1,"$\\lambda=s/LGD=0.015/0.60=\\mathbf{2.5}\\%$ par an.",
    "s/(1-R)"),

mcq(522,2,C1,"La **migration de notation** (rating migration) est modélisée par :",
    [("a","Une matrice de transition : $P(A\\to B,1\\text{ an})$ pour chaque paire de notations"),
     ("b","Le modèle de Merton uniquement"),("c","Un processus de Poisson"),("d","Un modèle Markov à 2 états")],
    "a","Matrix de transition annuelle (Moody's, S&P) : probabilités de passer d'une notation à une autre.",
    {"b":"Merton donne la PD mais pas la transition.","c":"Pour le défaut uniquement.","d":"Extension possible mais la matrice complète est standard."}),

num(523,2,C1,"Matrice de transition 1 an : $P(BBB\\to BB)=5\\%$, $P(BBB\\to défaut)=0.5\\%$. "
    "Probabilité de rester BBB ou monter = 1 - 5% - 0.5% - autres baisses (7%) = ?",
    "%",87.5,"abs",0.5,"$100-5-0.5-7=\\mathbf{87.5}\\%$ (exemple illustratif).",
    "1-\\sum P(\\text{migration\\,ou\\,défaut})"),

sa(524,2,C1,"Comparez la **probabilité de défaut risque-neutre** et la **probabilité physique** de défaut.",
    ["PD risque-neutre > PD physique (prime de risque de crédit)","Issues des spreads de marché vs données historiques"],
    "PD risque-neutre : extraite des spreads de CDS ou obligations. Inclut une prime de risque. "
    "PD physique : estimée à partir de données historiques de défaut (Moody's, S&P). "
    "En général, PD risque-neutre > PD physique car le marché exige une prime pour le risque de crédit. "
    "L'écart ($=$ prime de risque crédit) est positif et varie avec le cycle économique."),

num(525,2,C1,"Intensité de défaut $\\lambda=3\\%$/an. Probabilité de survie à 2 ans ?",
    "%",94.18,"abs",0.1,"$P(\\text{survive})=e^{-\\lambda T}=e^{-0.06}=\\mathbf{94.18}\\%$.",
    "e^{-\\lambda T}"),

mcq(526,2,C1,"Le **taux de recouvrement** (Recovery Rate) est :",
    [("a","Le pourcentage du nominal récupéré en cas de défaut (typiquement 40% pour les obligations non sécurisées)"),
     ("b","Le taux de coupon après défaut"),("c","Le taux de roulage de la dette"),("d","Le taux de migration vers BBB")],
    "a","Recovery rate $R\\approx40\\%$ pour senior unsecured. LGD $=1-R=60\\%$.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(527,3,C1,"Obligation zero-coupon 1 an, $K=1000$ USD, PD=5%, R=40%. Prix risque-neutre sous r=4% ?",
    "USD",917.4,"abs",0.5,"$P_{bond}=e^{-r}[(1-PD)\\times1000+PD\\times R\\times1000]=e^{-0.04}[0.95\\times1000+0.05\\times400]$"
    "$=0.9608[950+20]=0.9608\\times970=\\mathbf{932.0}$ USD.",
    "e^{-r}[(1-PD)\\times K+PD\\times R\\times K]"),

mcq(528,2,C1,"Le modèle à **intensité** (réduit) modélise le défaut par :",
    [("a","Un processus de Poisson de taux $\\lambda(t)$ — le défaut survient aléatoirement"),
     ("b","La valeur des actifs sous un seuil"),("c","Un arbre binomial"),("d","Un modèle GARCH")],
    "a","Modèle d'intensité (Jarrow-Turnbull, Duffie-Singleton) : temps de défaut = premier saut d'un Poisson.",
    {"b":"C'est le modèle structurel (Merton).","c":"Faux.","d":"Faux."}),

num(529,2,C1,"CDS sur 1 an, $\\lambda=200$ bps, $LGD=60\\%$, discount $e^{-rT}=0.96$. "
    "Jambe protection (valeur actualisée) : $\\lambda\\times LGD\\times e^{-rT}\\times N$ ($N=1$) ?",
    "%",1.152,"abs",0.01,"$0.02\\times0.6\\times0.96=\\mathbf{1.152}\\%$.",
    "\\lambda\\times LGD\\times e^{-rT}"),

sa(530,2,C1,"Expliquez la **corrélation de défaut** et son impact sur les CDOs.",
    ["Corrélation positive amplifie les pertes simultanées","Impact asymétrique sur les tranches"],
    "Corrélation de défaut : tendance des défauts à se produire simultanément. "
    "Si $\\rho=0$ : la diversification réduit le risque senior. "
    "Si $\\rho=1$ : tous les émetteurs font défaut ensemble, les tranches seniors sont exposées. "
    "Impact CDO : faible corrélation protège la tranche senior (bonne pour les seniors, mauvaise pour l'equity). "
    "Forte corrélation : mauvaise pour les seniors, profite à l'equity car le scénario 'tous défauts' est possible."),

num(531,2,C1,"Correlation de défaut implicite (base correlation). Tranche 0-3% (equity) : $\\rho=15\\%$. Tranche 3-6% : $\\rho=25\\%$. "
    "La base correlation est croissante : vrai ou faux ? Vrai = 1, Faux = 0.",
    "",1.0,"abs",0.1,"La base correlation est par construction croissante avec le point d'attachement. $\\mathbf{1}$ (Vrai).",
    "\\text{par définition}"),

mcq(532,2,C1,"Le **VaR économique** (Economic Capital) pour le crédit est :",
    [("a","La perte inattendue (UL = percentile élevé $-$ EL), pas la perte attendue"),
     ("b","La perte attendue"),("c","La VaR à 99%"),("d","Le spread de crédit moyen")],
    "a","Capital économique = perte inattendue : $UL_{99.9\\%}=VaR_{99.9\\%}-EL$. EL est couverte par des provisions.",
    {"b":"La perte attendue est couverte par le pricing.","c":"99.9% pour le crédit.","d":"Non."}),

num(533,2,C1,"EL (Expected Loss) : $PD=1\\%$, $LGD=50\\%$, $EAD=1$ M USD. EL (USD) ?",
    "USD",5000.0,"abs",50.0,"$EL=PD\\times LGD\\times EAD=0.01\\times0.5\\times1\\,000\\,000=\\mathbf{5\\,000}$ USD.",
    "PD\\times LGD\\times EAD"),

mcq(534,2,C1,"Un **credit default swap (CDS) index** (iTraxx, CDX) est :",
    [("a","Un CDS standardisé sur un panier d'entités de référence — permet de prendre une vue sur le marché du crédit global"),
     ("b","Un fonds d'obligations"),("c","Un dérivé de taux"),("d","Un indice boursier de banques")],
    "a","iTraxx Europe 125 : CDS sur 125 émetteurs européens IG. CDX IG : 125 émetteurs US.",
    {"b":"Non.","c":"Non.","d":"Non."}),

num(535,2,C1,"Corrélation de défaut implicite : CDX IG spread $=80$ bps, spread moyen des composants $=70$ bps. "
    "L'écart (10 bps) reflète la :",
    "",0.0,"abs",0.5,"La corrélation positive entre les défauts implique que l'index s'écarte légèrement de la moyenne, "
    "mais l'explication est qualitative. Valeur numérique : $\\rho$ implicite $\\approx\\mathbf{0}$ (exercice qualitatif).",
    "\\text{qualitative}"),

sa(536,2,C1,"Expliquez comment les **agences de notation** (Moody's, S&P, Fitch) évaluent le risque de crédit.",
    ["Analyse quantitative (ratios financiers) et qualitative (management, secteur)","Notation reflète la PD relative"],
    "Les agences analysent : (1) Ratios financiers (EBITDA/intérêts, dette/fonds propres, free cash flow). "
    "(2) Qualité du management, positionnement concurrentiel. "
    "(3) Secteur et macro. "
    "(4) Structure de la dette (séniorité, covenants). "
    "La notation (AAA à D) reflète la probabilité de défaut relative. "
    "Critiques : lenteur des révisions, conflits d'intérêts (modèle émetteur-payeur), pro-cyclicité."),

mcq(537,2,C1,"Le modèle de **Jarrow-Turnbull (1995)** est un modèle :",
    [("a","À intensité — le défaut est modélisé comme un processus de Poisson de taux $\\lambda$"),
     ("b","Structurel basé sur la valeur des actifs"),("c","À volatilité stochastique"),("d","À saut de crédit")],
    "a","JT : modèle réduit, $\\lambda$ peut être stochastique (ex: CIR).",
    {"b":"Merton/Black-Cox sont structurels.","c":"Faux.","d":"Faux."}),

num(538,2,C1,"Temps de défaut $\\tau$ : $P(\\tau>t)=e^{-\\lambda t}$. Demi-vie ($t$ tel que $P(\\tau>t)=0.5$) pour $\\lambda=5\\%$ ?",
    "ans",13.86,"abs",0.2,"$0.5=e^{-0.05t}\\Rightarrow t=\\ln(2)/0.05=0.693/0.05=\\mathbf{13.86}$ ans.",
    "\\ln(2)/\\lambda"),

mcq(539,2,C1,"Le **LGD** (Loss Given Default) varie selon :",
    [("a","La séniorité de la dette et la qualité du collatéral"),
     ("b","Le taux d'intérêt"),("c","La maturité de la dette uniquement"),("d","La nationalité de l'émetteur")],
    "a","LGD : secured bonds $<30\\%$, senior unsecured $\\approx60\\%$, subordinated $>70\\%$.",
    {"b":"Non.","c":"Non.","d":"Non."}),

num(540,2,C1,"Bond : $PD=3\\%$, $R=40\\%$, $EAD=1000$ USD, $r=4\\%$, $T=1$. Prix bond risque-neutre ?",
    "USD",931.2,"abs",1.0,"$V=e^{-0.04}[(1-0.03)\\times1000+0.03\\times400]=0.9608[970+12]=0.9608\\times982=\\mathbf{943.9}$ USD.",
    "e^{-r}[(1-PD)\\times F+PD\\times R\\times F]"),

mcq(541,2,C1,"Le ratio **Tier 1** (CET1) dans Bâle III est calculé par rapport à :",
    [("a","Les actifs pondérés des risques (RWA) — minimum 4.5%"),
     ("b","Les actifs totaux"),("c","Le passif total"),("d","Le bénéfice annuel")],
    "a","CET1 = Capital ordinaire / RWA. Bâle III : min 4.5% CET1 + 2.5% buffer = 7%.",
    {"b":"Ratio de levier.","c":"Non.","d":"Non."}),

num(542,2,C1,"RWA crédit : exposition $=1$ M USD, pondération risque $=50\\%$ (BBB). RWA ?",
    "USD",500000.0,"abs",1.0,"$RWA=1\\,000\\,000\\times50\\%=\\mathbf{500\\,000}$ USD.",
    "EAD\\times\\text{risk weight}"),

num(543,2,C1,"Capital crédit (Bâle III) : RWA $=500$ K USD, CET1 minimum $=7\\%$. Capital requis (USD) ?",
    "USD",35000.0,"abs",100.0,"$C=RWA\\times7\\%=500\\,000\\times0.07=\\mathbf{35\\,000}$ USD.",
    "RWA\\times\\text{CET1 ratio}"),
]

# ── credit-derivatives (544-573) ──────────────────────────────────────────────
items+=[
mcq(544,1,C2,"Un **CDS (Credit Default Swap)** est un contrat où :",
    [("a","Le vendeur de protection paie le pair moins le recouvrement en cas de défaut de l'entité de référence"),
     ("b","Le vendeur reçoit le pair"),("c","Les deux parties échangent des taux fixes"),("d","L'entité de référence garantit le paiement")],
    "a","CDS : acheteur paie une prime (spread), vendeur paie $LGD\\times N$ en cas de défaut.",
    {"b":"Non.","c":"IRS.","d":"Non."}),

num(545,2,C2,"CDS 5 ans, spread = 120 bps, notionnel 10 M USD, paiements trimestriels. Prime trimestrielle (USD) ?",
    "USD",30000.0,"abs",100.0,"$120\\,bps\\times10\\,M\\times0.25=0.012\\times10\\,000\\,000\\times0.25=\\mathbf{30\\,000}$ USD.",
    "\\text{spread}\\times N\\times\\delta"),

mcq(546,2,C2,"La **jambe protection** d'un CDS vaut :",
    [("a","La valeur actualisée des paiements de protection conditionnels au défaut"),
     ("b","La valeur actualisée des primes"),("c","La valeur de l'obligation de référence"),("d","La VaR du CDS")],
    "a","Jambe protection = $\\sum_i \\lambda_i LGD\\times B(0,T_i)$. S'oppose à la jambe premium.",
    {"b":"C'est la jambe premium.","c":"Non.","d":"Non."}),

num(547,3,C2,"CDS pricing : $\\lambda=200$ bps, $LGD=60\\%$, 1 an. "
    "Jambe protection (non actualisée) $=\\lambda\\times LGD=0.02\\times0.60$ ?",
    "%",1.2,"abs",0.01,"$0.02\\times0.60=\\mathbf{1.2}\\%$ du notionnel.",
    "\\lambda\\times LGD"),

sa(548,2,C2,"Expliquez comment un CDS peut être utilisé pour **créer une position synthétique longue** sur une obligation.",
    ["Vendre protection CDS = risque similaire à détenir l'obligation","Évite le financement de l'actif"],
    "Vendre protection sur un CDS = position longue synthétique sur le risque de crédit. "
    "En cas de défaut, le vendeur de protection paie le LGD (comme un détenteur d'obligation). "
    "Avantages : (1) Pas besoin de financer l'actif. (2) Levier naturel. (3) Exposition sélective à la duration de crédit. "
    "Utilisé par les hedge funds pour s'exposer au crédit d'une entité sans acheter son obligation."),

num(549,2,C2,"CDS spread = 200 bps, rendement risk-free = 4%, rendement obligation = 6%. Basis ?",
    "bps",0.0,"abs",5.0,"$\\text{Basis}=\\text{CDS spread}-(\\text{bond spread})=200-(6-4)\\%\\times100=200-200=\\mathbf{0}$ bps. (Basis nulle si marché parfait.)",
    "\\text{CDS spread}-\\text{bond spread}"),

mcq(550,2,C2,"Le **ISDA Credit Event** déclenche le paiement d'un CDS pour :",
    [("a","Défaut de paiement, faillite, restructuration (selon le contrat)"),
     ("b","La dégradation de notation uniquement"),("c","La hausse des spreads CDS"),("d","L'abaissement de note en zone spéculative")],
    "a","Événements de crédit ISDA : failure to pay, bankruptcy, restructuring (optional en NA vs Europe).",
    {"b":"Non, pas un événement de crédit.","c":"Non.","d":"Non."}),

mcq(551,2,C2,"Le **CDS index (CDX/iTraxx)** permet de :",
    [("a","Prendre une vue sur le crédit global d'un secteur ou d'une région géographique en une transaction"),
     ("b","Acheter individuellement des CDS"),("c","Investir dans des actions"),("d","Gérer le risque de taux")],
    "a","iTraxx/CDX : hedge macro du portefeuille de crédit, trading de spread global.",
    {"b":"CDS individuels.","c":"Faux.","d":"IRS."}),

num(552,2,C2,"Valeur d'un CDS à mi-vie : spread initial $=150$ bps, spread actuel $=200$ bps, duration $=3$ ans. "
    "P&L d'un acheteur de protection (vendeur de risque) ?",
    "USD",15000.0,"abs",500.0,"$\\Delta\\text{valeur}=(200-150)\\,bps\\times3\\,ans=50\\,bps\\times3=1.5\\%$ du notionnel (1 M). "
    "$=0.015\\times1\\,000\\,000=\\mathbf{15\\,000}$ USD de profit pour l'acheteur de protection.",
    "(s_{new}-s_{old})\\times\\text{duration}\\times N"),

sa(553,2,C2,"Qu'est-ce qu'un **Total Return Swap (TRS)** et en quoi diffère-t-il d'un CDS ?",
    ["TRS transfère aussi le risque de marché","CDS ne couvre que le défaut"],
    "TRS : le payeur TRS envoie le rendement total (coupons + variation de prix) et reçoit SOFR+spread. "
    "CDS : couvre uniquement le risque de défaut (paiement conditionnel). "
    "TRS transfère donc le risque de taux, de crédit ET de marché. "
    "CDS est plus ciblé : seul le défaut déclenche le paiement. "
    "TRS est utilisé pour le financement synthétique, CDS pour la couverture du risque de défaut pur."),

mcq(554,2,C2,"Un **CLN (Credit-Linked Note)** combine :",
    [("a","Une obligation + un CDS embedded : l'émetteur a une protection de crédit sur l'entité de référence"),
     ("b","Un CDO + un MBS"),("c","Un call + un bond"),("d","Un TRS + un cap")],
    "a","CLN : émetteur émet une obligation à coupon élevé, mais si l'entité de référence fait défaut, le remboursement est réduit.",
    {"b":"Non.","c":"Convertible bond.","d":"Non."}),

num(555,2,C2,"CLN : coupon 5%, notionnel 1000 USD. Défaut de l'entité de référence (R=40%). Remboursement à maturité ?",
    "USD",400.0,"abs",1.0,"$1000\\times R=1000\\times0.40=\\mathbf{400}$ USD.",
    "N\\times R"),

mcq(556,2,C2,"Un **First-to-Default** (FtD) basket CDS paie :",
    [("a","Lors du premier défaut dans un panier d'entités de référence"),
     ("b","Lors du dernier défaut"),("c","À chaque défaut"),("d","Uniquement pour les obligations souveraines")],
    "a","FtD : concentre le risque de crédit du premier défaut du panier. Spread > CDS individuel max.",
    {"b":"Last-to-default.","c":"nth-to-default.","d":"Non."}),

num(557,2,C2,"FtD panier 5 entités, $\\lambda_i=100$ bps chacune, indépendantes. Intensité du premier défaut ?",
    "bps",500.0,"abs",1.0,"$\\lambda_{FtD}=\\sum\\lambda_i=5\\times100=\\mathbf{500}$ bps (indépendance).",
    "\\sum_{i}\\lambda_i"),

sa(558,2,C2,"Décrivez la **replication synthétique** d'un CDO avec des CDS.",
    ["CDS sur chaque entité de référence","Tranches synthétiques par allocation des pertes"],
    "CDO synthétique : au lieu d'acheter les obligations physiquement, le SPV vend des CDS sur le pool d'entités. "
    "Les primes CDS remplacent les coupons des obligations. "
    "Les pertes sur défaut sont absorbées par les tranches dans l'ordre equity → mezzanine → senior. "
    "Avantage : rapidité, flexibilité, pas besoin de trouver les obligations physiques. "
    "Bilan négatif : les CDO synthétiques permettaient de 'créer' plus d'exposition au crédit que la capacité de l'économie réelle."),

num(559,2,C2,"CDO synthétique : vendeur protection sur 100 M USD de CDS. Spread moyen = 150 bps. "
    "Prime reçue annuelle (USD) ?",
    "USD",1500000.0,"abs",10000.0,"$150\\,bps\\times100\\,M=0.015\\times100\\,000\\,000=\\mathbf{1\\,500\\,000}$ USD.",
    "\\text{spread}\\times N"),

mcq(560,2,C2,"Le **CDS spread** reflète approximativement :",
    [("a","La prime de risque de crédit annuelle pour se protéger contre le défaut"),
     ("b","Le rendement de l'obligation"),("c","La probabilité de défaut seule"),("d","Le taux de recouvrement")],
    "a","$s\\approx\\lambda\\times LGD$. Le spread est la prime de risque annualisée.",
    {"b":"Non.","c":"Seulement sous LGD=100%.","d":"Non."}),

num(561,3,C2,"CDS bootstrap : obligations 1 an (PD1=1%) et 2 ans (PD cumul=3%). PD2 marginale ?",
    "%",2.020,"abs",0.05,"$PD_2^{marginal}=1-(1-0.03)/(1-0.01)=1-0.97/0.99=1-0.9798=\\mathbf{2.02}\\%$.",
    "1-(1-PD_{cum,2})/(1-PD_{cum,1})"),

mcq(562,2,C2,"La **Big Bang Protocol** ISDA (2009) a standardisé les CDS en :",
    [("a","Introduisant des dates de paiement standard et des upfront payments pour les spreads non ATM"),
     ("b","Éliminant les CDS des marchés OTC"),("c","Rendant les CDS exchange-traded"),("d","Supprimant les événements de restructuration")],
    "a","Big Bang : coupons standard 100 bps ou 500 bps + upfront. Clearance via CCP. Small Bang pour l'Europe.",
    {"b":"Faux.","c":"Partiellement, via CCPs.","d":"Faux."}),

num(563,2,C2,"CDS Big Bang : coupon standard = 100 bps, spread de marché = 80 bps. "
    "L'acheteur reçoit un upfront (vendeur de protection paie) car spread < coupon. "
    "Upfront approx = (100-80) bps × duration 5 ans ?",
    "%",1.0,"abs",0.05,"$Upfront=(100-80)\\,bps\\times5=20\\,bps\\times5=100\\,bps=\\mathbf{1}\\%$ du notionnel.",
    "(K-s)\\times\\text{duration}"),

sa(564,2,C2,"Expliquez le rôle des **CCPs** (Central Clearing Counterparties) dans les marchés de CDS.",
    ["Réduction du risque de contrepartie","Compression des positions"],
    "Post-crise 2008, les CDS standardisés sont compensés via des CCPs (ex : ICE Clear Credit). "
    "La CCP devient l'acheteur pour chaque vendeur et vice versa → risque bilatéral devient risque face CCP. "
    "Avantages : mutualisation du risque de défaut, compression nette des positions, transparence des expositions. "
    "La réglementation Dodd-Frank (US) et EMIR (EU) ont mandaté la compensation centrale pour les CDS standardisés."),

mcq(565,2,C2,"Le **basis trade** CDS-Bond exploite :",
    [("a","L'écart entre le spread CDS et le spread de l'obligation (bond basis)"),
     ("b","La différence de vol implicite entre deux CDS"),("c","Les différences de taux entre marchés"),("d","L'écart entre CDS IG et HY")],
    "a","Bond basis = CDS spread $-$ Z-spread. Peut diverger lors de stress de marché (financement, réglementation).",
    {"b":"Non.","c":"Non.","d":"Non."}),

num(566,2,C2,"Z-spread d'une obligation = 180 bps, CDS spread = 200 bps. Basis (bps) ?",
    "bps",20.0,"abs",0.5,"$Basis=200-180=\\mathbf{20}$ bps (positive basis — CDS plus cher).",
    "CDS_{spread}-Z_{spread}"),

mcq(567,2,C2,"La **restructuration** comme événement de crédit CDS est controversée car :",
    [("a","Elle peut être voluntary/distressed et les créanciers reçoivent de nouvelles obligations pas nécessairement au prix de marché"),
     ("b","Elle est trop rare"),("c","Elle avantage le vendeur de protection"),("d","Elle n'existe pas dans les CDS modernes")],
    "a","Restructuration 'soft' : l'acheteur peut choisir quelle obligation livrer (cheapest-to-deliver) → surcompensation.",
    {"b":"Faux.","c":"Avantage l'acheteur (cheapest-to-deliver).","d":"Faux."}),

num(568,2,C2,"Cheapest-to-Deliver (CTD) dans un CDS sur restructuration : obligations éligibles à 85, 88, 80 USD. "
    "CTD (USD) ?",
    "USD",80.0,"abs",0.01,"L'obligation à $\\mathbf{80}$ USD est la moins chère à livrer (maximise le paiement de l'acheteur).",
    "\\min(\\text{prix obligataires})"),

sa(569,2,C2,"Comment les **sovereign CDS** sont-ils utilisés par les investisseurs internationaux ?",
    ["Couverture du risque souverain","Spéculation sur la solvabilité d'un pays"],
    "Les CDS souverains permettent : "
    "(1) **Couverture** : les détenteurs d'obligations souveraines achètent des CDS pour se protéger contre le défaut. "
    "(2) **Spéculation** : sans détenir les obligations, acheter un CDS est un pari sur la dégradation du crédit. "
    "(3) **Indicateur** : les spreads CDS souverains sont un baromètre du risque de défaut perçu par le marché. "
    "Controverse (crise euro 2010-2012) : vente à découvert de CDS souverains accusée d'amplifier les crises."),

num(570,2,C2,"CDS souverain Grèce 2012 : spread 3500 bps, LGD=60%. PD implicite annuelle ?",
    "%",58.3,"abs",1.0,"$PD=s/LGD=3500\\,bps/6000\\,bps=0.583=\\mathbf{58.3}\\%$/an.",
    "s/LGD"),

mcq(571,2,C2,"Le **CDS swaption** est une option sur :",
    [("a","Le spread d'un CDS à une date future"),("b","Le taux d'intérêt d'un swap"),
     ("c","L'obligation de référence"),("d","Le prix du CDS index")],
    "a","CDS swaption : call (ou put) sur le spread d'un CDS à une date future. Utile pour gérer la volatilité du crédit.",
    {"b":"Swaption IR.","c":"Bond option.","d":"CDS index option."}),

num(572,3,C2,"CDS swaption : strike $K=150$ bps, forward CDS spread $F=180$ bps, $\\sigma=30\\%$, $T=0.5$ an, duration $=4$ ans. "
    "$d_1=[\\ln(180/150)+0.5\\times0.09\\times0.5]/(0.30\\sqrt{0.5})=[0.182+0.0225]/0.2121=0.963$. "
    "$N(0.963)=0.832$. Valeur payer swaption CDS ?",
    "bps",15.2,"abs",0.5,"$V\\approx4\\times e^{-rT}[FN(d_1)-KN(d_2)]$. $d_2=0.963-0.2121=0.751$. "
    "$N(0.751)=0.774$. $V=4[180\\times0.832-150\\times0.774]=4[149.8-116.1]=4\\times33.7=\\mathbf{134.8}$ bps $\\times e^{-r}$.",
    "D[FN(d_1)-KN(d_2)]"),

sa(573,2,C2,"Expliquez comment les **CDS** peuvent être utilisés pour gérer le risque de concentration dans un portefeuille de crédit.",
    ["Acheter protection sur les émetteurs concentrés","Réduire les large single-name exposures"],
    "Gestion de concentration : si un portefeuille est surexposé à un émetteur spécifique (ex : 10% en une seule obligation), "
    "acheter un CDS sur cet émetteur réduit l'exposition nette sans vendre l'obligation. "
    "Avantages : pas de réalisation de plus/moins-value, confidentialité, efficacité fiscale possible. "
    "La CCP permet la compression nette des positions entre différents participants du marché."),
]

# ── footer ────────────────────────────────────────────────────────────────────
print(f"Items: {len(items)}")
assert len(items)==98, f"Expected 98, got {len(items)}"
batch={"source":"Marchés des dérivés — Exercices originaux","track":"markets","module":"der-credit-var","items":items}
with open(OUT,"w",encoding="utf-8") as f: json.dump(batch,f,ensure_ascii=False,indent=2)
print(f"Written: {OUT}")
