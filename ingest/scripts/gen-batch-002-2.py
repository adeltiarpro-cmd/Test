#!/usr/bin/env python3
"""Génère batch-002-2: der-interest-rates (50 items, clés 087-112 + 139-162)"""
import json, os, math

OUT = os.path.join(os.path.dirname(__file__), "../canonical/batch-002-2-der-interest-rates.json")

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
    ss=[{"answer":s[6]} for s in sl]
    return {"external_key":key(k),"type":"numeric_steps","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"steps":sp},"solution":{"steps":ss}}
def sa(k,d,c,p,kp,m):
    return {"external_key":key(k),"type":"short_answer","difficulty":d,"source_ref":"Exercice original","concepts":[c],
            "prompt_mdx":p,"payload":{"max_words":150,"scoring_mode":"self_eval"},
            "solution":{"key_points":[{"text":pt,"weight":round(1/len(kp),4)} for pt in kp],"model_answer_mdx":m}}

items = []

# ── interest-rates (087-112) ────────────────────────────────────────────────

items += [
mcq(87,1,"interest-rates","Le **taux au comptant** (spot rate) $r(t,T)$ est :",
    [("a","Le taux d'intérêt pour un emprunt commençant aujourd'hui et se terminant en $T$"),
     ("b","Le taux d'intérêt anticipé pour une période future"),
     ("c","Le taux d'un prêt bancaire à court terme"),
     ("d","Le taux directeur de la banque centrale")],
    "a","Le taux spot est le taux en vigueur aujourd'hui pour une maturité $T$.",
    {"b":"C'est le taux forward.","c":"Approximation insuffisante.","d":"Faux."}),

num(88,2,"interest-rates",
    "Obligations zéro-coupon : valeur nominale 1 000 USD, maturité 3 ans, taux spot continu $r = 5\\%$. Prix ?",
    "USD",860.71,"rel",0.002,
    "$P = 1000 e^{-0.05\\times3} = 1000\\times0.86071 = \\mathbf{860.71}$ USD","1000 e^{-rT}"),

mcq(89,2,"interest-rates","La **courbe des taux** (yield curve) normale est :",
    [("a","Croissante : les taux longs sont supérieurs aux taux courts"),
     ("b","Plate : tous les taux sont identiques"),
     ("c","Inversée : les taux courts dépassent les longs"),
     ("d","En forme de bosse au milieu")],
    "a","Courbe normale = prime de terme positive : les investisseurs exigent un rendement supplémentaire pour les maturités longues.",
    {"b":"Courbe plate.","c":"Courbe inversée, souvent précurseur de récession.","d":"Courbe en bosse."}),

num(90,2,"interest-rates",
    "Taux nominal annuel $= 12\\%$ avec capitalisation **mensuelle**. Quel est le taux effectif annuel ?",
    "%",12.68,"abs",0.05,
    "$(1 + 0.12/12)^{12} - 1 = (1.01)^{12} - 1 = 1.12683 - 1 = \\mathbf{12.68}\\%$","(1+r_m/m)^m - 1"),

nstep(91,3,"interest-rates","Taux nominal $r_m = 8\\%$ capitalisé semestriellement. Convertissez en (a) taux effectif annuel, (b) taux continu équivalent.",
    [("Taux effectif annuel (%)","%" ,0.01,"$(1+r_m/2)^2-1$","$(1+0.04)^2-1=1.0816-1=\\mathbf{8.16}\\%$",None,8.16),
     ("Taux continu équivalent (%)","%" ,0.01,"$r_c=\\ln(1+r_{eff})$","$r_c=\\ln(1.0816)=\\mathbf{7.84}\\%$","Ne pas oublier de prendre le log naturel du taux effectif, pas du taux nominal.",7.84)]),

mcq(92,2,"interest-rates","La **durée de Macaulay** mesure :",
    [("a","La sensibilité du prix d'une obligation à une variation de taux"),
     ("b","La maturité résiduelle de l'obligation"),
     ("c","Le temps moyen pondéré jusqu'aux flux de trésorerie"),
     ("d","La convexité de l'obligation")],
    "c","Durée de Macaulay = $\\sum t_i \\frac{PV(CF_i)}{P}$, moyenne pondérée des dates des flux.",
    {"a":"C'est la durée modifiée.","b":"Pas exactement.","d":"La convexité est différente."}),

num(93,3,"interest-rates",
    "Obligation : coupon annuel 6 USD sur 100 USD, maturité 3 ans, YTM $= 5\\%$. Calculez la **durée de Macaulay** (années).",
    "ans",2.832,"abs",0.01,
    "Flux : $CF_1=6,CF_2=6,CF_3=106$. $P = 6e^{-0.05}+6e^{-0.1}+106e^{-0.15}=5.706+5.427+91.136=102.27$. "
    "$D=\\frac{1\\times5.706+2\\times5.427+3\\times91.136}{102.27}=\\frac{5.706+10.854+273.408}{102.27}=\\frac{289.97}{102.27}=\\mathbf{2.836}$ ans","\\frac{\\sum t_i PV(CF_i)}{P}"),

num(94,2,"interest-rates",
    "Durée modifiée $D^* = 4.2$ ans, YTM augmente de 50 bp $= 0.005$. Variation **approximative** du prix (%)?",
    "%",-2.1,"abs",0.05,
    "$\\Delta P / P \\approx -D^* \\Delta y = -4.2 \\times 0.005 = -\\mathbf{2.1}\\%$","-D^* \\Delta y"),

sa(95,2,"interest-rates","Expliquez la différence entre **duration modifiée** et **duration de Macaulay**.",
    ["Duration modifiée = Macaulay/(1+y)","Mesure directe de la sensibilité au taux"],
    "La durée de Macaulay mesure la **durée moyenne** des flux en années. "
    "La durée modifiée $D^* = D/(1+y/m)$ (ou $D$ pour les taux continus) mesure directement la **sensibilité** : "
    "$\\Delta P/P \\approx -D^* \\Delta y$. Pour les taux continus, $D^* = D$ exactement."),

mcq(96,2,"interest-rates","La **convexité** d'une obligation fait que :",
    [("a","Le prix monte plus que prédit par la durée si les taux baissent"),
     ("b","Le prix baisse plus que prédit par la durée si les taux montent"),
     ("c","La duration surestime toujours la perte"),
     ("d","Les obligations convexes sont plus risquées")],
    "a","La relation prix/taux est convexe : la durée sous-estime la hausse de prix (et surestrime la baisse).",
    {"b":"La durée surestime la perte (convexité est favorable).","c":"Faux.","d":"Faux, la convexité est un avantage."}),

num(97,3,"interest-rates",
    "Taux spot 1 an $r_1=3\\%$, taux spot 2 ans $r_2=4\\%$ (continus). **Taux forward** 1 an dans 1 an ?",
    "%",5.0,"abs",0.05,
    "$r_f = \\frac{r_2 T_2 - r_1 T_1}{T_2-T_1} = \\frac{0.04\\times2-0.03\\times1}{1} = \\frac{0.05}{1} = \\mathbf{5.0}\\%$",
    "\\frac{r_2 T_2 - r_1 T_1}{T_2-T_1}"),

nstep(98,3,"interest-rates",
    "Taux spot : $r_1=2\\%$, $r_2=2.5\\%$, $r_3=3\\%$, $r_4=3.3\\%$ (continus). Calculez les taux forward annuels : $f(1,2)$, $f(2,3)$, $f(3,4)$.",
    [("f(1,2) (%)","%" ,0.01,"$f(t_1,t_2)=r_2 t_2-r_1 t_1$","$2.5\\%\\times2-2\\%\\times1=5\\%-2\\%=\\mathbf{3.0}\\%$",None,3.0),
     ("f(2,3) (%)","%" ,0.01,None,"$3\\%\\times3-2.5\\%\\times2=9\\%-5\\%=\\mathbf{4.0}\\%$",None,4.0),
     ("f(3,4) (%)","%" ,0.01,None,"$3.3\\%\\times4-3\\%\\times3=13.2\\%-9\\%=\\mathbf{4.2}\\%$",None,4.2)]),

mcq(99,2,"interest-rates","Une obligation **à coupon** a toujours une durée :",
    [("a","Inférieure à sa maturité"),("b","Égale à sa maturité"),
     ("c","Supérieure à sa maturité"),("d","Nulle")],
    "a","Les coupons intermédiaires raccourcissent la durée : $D < T$ pour tout coupon $> 0$.",
    {"b":"Seulement pour un zéro-coupon.","c":"Impossible.","d":"Impossible."}),

num(100,2,"interest-rates",
    "Taux nominal $12\\%$ capitalisé **trimestriellement**. Taux continu équivalent ?",
    "%",11.71,"abs",0.05,
    "Taux effectif annuel $= (1+0.03)^4-1=1.12551-1=12.551\\%$. "
    "$r_c=\\ln(1.12551)=\\mathbf{11.83}\\%$","\\ln(1+(r_m/m)^m)"),

sa(101,2,"interest-rates","Qu'est-ce que la **structure par terme** des taux d'intérêt, et quelles théories l'expliquent ?",
    ["Relation taux/maturité","Théories : anticipations, préférence pour la liquidité, segmentation"],
    "La structure par terme décrit la relation entre les taux spot et leur maturité. "
    "Trois théories principales : (1) **Anticipations pures** : la courbe reflète uniquement les taux courts futurs anticipés. "
    "(2) **Préférence pour la liquidité** : une prime est requise pour les maturités longues. "
    "(3) **Segmentation des marchés** : l'offre/demande à chaque maturité détermine les taux indépendamment."),

num(102,2,"interest-rates",
    "Obligation d'État : nominal 1 000 USD, coupon annuel 8%, maturité 5 ans, YTM $= 6\\%$ (annuel). Prix ?",
    "USD",1084.25,"rel",0.002,
    "$P=\\sum_{t=1}^5 \\frac{80}{1.06^t}+\\frac{1000}{1.06^5}$"
    "$=80\\times4.2124+1000\\times0.7473=336.99+747.26=\\mathbf{1084.25}$ USD","\\sum CF_t/(1+y)^t"),

mcq(103,2,"interest-rates","Le **YTM** (rendement à l'échéance) d'une obligation est :",
    [("a","Le taux d'actualisation qui égalise le prix aux flux de trésorerie futurs"),
     ("b","Le taux coupon divisé par le prix"),
     ("c","Le taux moyen des coupons"),
     ("d","Le taux auquel l'obligation sera réinvestie")],
    "a","$P = \\sum CF_t/(1+y)^t$ — $y$ est le YTM.",
    {"b":"C'est le current yield.","c":"Faux.","d":"Hypothèse nécessaire mais pas la définition."}),

num(104,3,"interest-rates",
    "Portfolio immunisé : valeur actuelle des engagements = 1 M USD dans 5 ans. Duration cible = 5 ans. "
    "Obligations A ($D_A=3$ ans, poids $w_A$) et B ($D_B=8$ ans, poids $w_B=1-w_A$). Quel est $w_A$ ?",
    "",0.6,"abs",0.01,
    "$w_A D_A + (1-w_A) D_B = 5$ → $3w_A + 8-8w_A = 5$ → $-5w_A=-3$ → $w_A=\\mathbf{0.6}$","\\frac{D_B-D_T}{D_B-D_A}"),

sa(105,2,"interest-rates","Expliquez le risque de **réinvestissement** pour le détenteur d'une obligation à coupon.",
    ["Les coupons sont réinvestis à un taux incertain","YTM suppose réinvestissement au même taux"],
    "Le YTM suppose que tous les coupons sont réinvestis au taux $y$. En pratique, si les taux baissent, "
    "les coupons sont réinvestis à un taux inférieur, ce qui réduit le rendement effectif. "
    "Le risque de réinvestissement est proportionnel à la durée et au montant des coupons. "
    "Les obligations zéro-coupon éliminent ce risque."),

num(106,2,"interest-rates",
    "Prix spot 6 mois $= 98.50$ USD (obligation 100 USD). Taux spot 6 mois continu ?",
    "%",3.05,"abs",0.05,
    "$r = -\\frac{\\ln(98.50/100)}{0.5} = -\\frac{\\ln(0.985)}{0.5} = -\\frac{-0.01511}{0.5} = \\mathbf{3.02}\\%$","-\\frac{\\ln(P/F)}{T}"),

mcq(107,2,"interest-rates","Une **obligation à coupon** peut être vue comme :",
    [("a","Un portefeuille d'obligations zéro-coupon"),
     ("b","Un seul flux terminal"),
     ("c","Un call sur le taux d'intérêt"),
     ("d","Un swap de taux fixe contre variable")],
    "a","Chaque coupon est un zéro-coupon de maturité correspondante. On décompose et valorise par les taux spot.",
    {"b":"C'est un zéro-coupon.","c":"Faux.","d":"Un swap a une structure différente."}),

num(108,3,"interest-rates",
    "Obligation : nominal 1 000 USD, coupon semestriel 3%, 4 ans. Taux spot semestriels (continus) : "
    "$r_{0.5}=2\\%, r_1=2.2\\%, r_{1.5}=2.4\\%, r_2=2.6\\%, r_{2.5}=2.8\\%, r_3=3\\%, r_{3.5}=3.1\\%, r_4=3.2\\%$. Prix ?",
    "USD",993.15,"rel",0.005,
    "Actualiser chaque flux $30$ ou $1030$ USD avec les taux spot correspondants. "
    "$P = 30(e^{-0.01}+e^{-0.022}+...)+1030e^{-0.032\\times4}$. Calcul numérique $\\approx \\mathbf{993}$ USD.","\\sum CF_i e^{-r_i T_i}"),

num(109,2,"interest-rates",
    "Duration modifiée $D^*=6.5$ ans, prix $= 950$ USD. Si taux augmente de 25 bp, variation de prix (USD) ?",
    "USD",-15.44,"abs",0.1,
    "$\\Delta P = -D^* \\times P \\times \\Delta y = -6.5 \\times 950 \\times 0.0025 = \\mathbf{-15.44}$ USD","-D^* \\times P \\times \\Delta y"),

nstep(110,3,"interest-rates",
    "Obligation de nominal 1 000 USD, coupon annuel $c=6\\%$, maturité $T=3$ ans, $r=5\\%$ (continu). "
    "Calculez : (a) le prix, (b) la durée de Macaulay, (c) la duration modifiée.",
    [("Prix (USD)","USD",0.1,"$P=\\sum CF_i e^{-rT_i}$",
      "$60e^{-0.05}+60e^{-0.1}+1060e^{-0.15}=57.07+57.14+906.77=\\mathbf{1020.98}$ USD",None,1020.98),
     ("Duration de Macaulay (ans)","ans",0.01,None,
      "$D=\\frac{1\\times57.07+2\\times57.14+3\\times906.77}{1020.98}=\\frac{57.07+114.28+2720.31}{1020.98}=\\frac{2891.66}{1020.98}=\\mathbf{2.832}$ ans","Utiliser les VA des flux, pas les flux bruts.",2.832),
     ("Duration modifiée (ans)","ans",0.005,None,
      "Taux continus : $D^*=D=\\mathbf{2.832}$ ans (pas de division par $1+y$ pour taux continus)",
      "Pour taux continus $D^*=D$. Pour taux discrets $D^*=D/(1+y)$.",2.832)]),

mcq(111,2,"interest-rates","Le phénomène de **pull to par** signifie que :",
    [("a","Le prix d'une obligation converge vers son nominal à l'approche de l'échéance"),
     ("b","Le taux coupon augmente avec le temps"),
     ("c","La duration diminue quand les taux augmentent"),
     ("d","L'obligation est rappelée par l'émetteur")],
    "a","À l'échéance, l'obligation vaut son nominal quels que soient les taux du marché.",
    {"b":"Coupon fixe.","c":"La duration diminue avec le temps, mais ce n'est pas pull to par.","d":"C'est un callable bond."}),

num(112,2,"interest-rates",
    "Courbe des taux plates à $r=4\\%$. Obligation 5 ans, coupon annuel $5\\%$, nominal $1000$ USD. "
    "Les taux montent immédiatement à $4.5\\%$. Nouvelle duration modifiée ?",
    "ans",4.28,"abs",0.05,
    "Nouveau prix : recalculer les flux à $4.5\\%$. $D^* \\approx 4.28$ ans (légèrement réduite car prix baisse).",
    "D^* \\approx D/(1+y)"),
]

# ── interest-rate-futures (139-162) ─────────────────────────────────────────

items += [
mcq(139,2,"interest-rate-futures","Un **Eurodollar futures** couvre :",
    [("a","Un dépôt USD de 1 million USD à 3 mois, taux LIBOR/SOFR"),
     ("b","Un achat d'euros contre dollars"),
     ("c","Un emprunt en EUR à taux fixe"),
     ("d","Un swap de devise EUR/USD")],
    "a","Eurodollar futures = contrat sur le taux interbancaire USD à 3 mois (LIBOR puis SOFR).",
    {"b":"C'est un futures de change.","c":"Faux.","d":"Faux."}),

num(140,2,"interest-rate-futures",
    "Futures Eurodollar à 94.20 (prix = 100 − taux). Quel est le taux **LIBOR implicite** ?",
    "%",5.80,"abs",0.01,
    "Taux implicite $= 100 - 94.20 = \\mathbf{5.80}\\%$","100 - F"),

nstep(141,3,"interest-rate-futures",
    "Un emprunteur prévoit d'emprunter 10 M USD dans 3 mois pour 3 mois. Il vend 10 contrats Eurodollar "
    "(1 M USD chacun) à 94.50 ($r=5.5\\%$). À l'emprunt, le taux SOFR est 6.0%, futures à 94.00.",
    [("Gain sur futures (USD)","USD",1.0,"Variation de 50 bp, DV01 = 25 USD/bp/contrat",
      "50 bp $\\times$ 25 USD $\\times$ 10 contrats $= \\mathbf{12\\,500}$ USD",None,12500.0),
     ("Surcoût d'emprunt vs anticipé (USD)","USD",1.0,None,
      "0.5% $\\times$ 10 M $\\times$ 0.25 $= \\mathbf{12\\,500}$ USD","Vérifier que le gain compense exactement.",12500.0),
     ("Taux effectif de l'emprunt (%)","%" ,0.01,None,
      "Surcoût compensé : taux effectif $\\approx \\mathbf{5.50}\\%$",None,5.50)]),

mcq(142,2,"interest-rate-futures","La **convexity adjustment** entre le taux futures et le taux forward est due à :",
    [("a","Le marking-to-market quotidien des futures crée un biais vs les forwards"),
     ("b","Le futures est toujours plus cher que le forward"),
     ("c","Les obligations à coupon ont une convexité positive"),
     ("d","Le taux LIBOR est différent du taux OIS")],
    "a","Le marking-to-market des futures crée une corrélation entre les flux et les taux : taux futures $>$ taux forward.",
    {"b":"Pas toujours.","c":"Non lié directement.","d":"Écart basis, pas convexity adjustment."}),

num(143,2,"interest-rate-futures",
    "Futures T-Bond (nominal 100 000 USD). Prix futures $= 105{-}16$ (en 32es). Valeur faciale du contrat (USD) ?",
    "USD",105500.0,"abs",1.0,
    "$105 + 16/32 = 105.50\\%$. Valeur $= 100\\,000 \\times 1.0550 = \\mathbf{105\\,500}$ USD.",
    "F \\times N"),

mcq(144,2,"interest-rate-futures","Le **facteur de conversion** d'un T-Bond futures sert à :",
    [("a","Rendre comparables des obligations de coupons différents lors de la livraison"),
     ("b","Calculer les intérêts courus"),
     ("c","Déterminer le prix du futures en 32es"),
     ("d","Ajuster pour la durée du contrat")],
    "a","Le vendeur peut livrer n'importe quelle T-Bond éligible ; le facteur ajuste le prix reçu selon le coupon.",
    {"b":"Les intérêts courus sont séparés.","c":"Faux.","d":"Faux."}),

nstep(145,3,"interest-rate-futures",
    "T-Bond futures, prix futures $Q_F=110$, obligation livrable : nominal $100\\,000$, coupon $6\\%$, "
    "facteur de conversion $CF=1.0452$, intérêts courus $AI=2.50\\%$. Prix facturé (invoice price) ?",
    [("Prix ajusté (USD)","USD",1.0,"$Q_F \\times CF$",
      "$110 \\times 1.0452 = 114.97\\%$ du nominal $= \\mathbf{114\\,972}$ USD",None,114972.0),
     ("Invoice price (USD)","USD",1.0,"$+$ intérêts courus",
      "$114\\,972 + 0.025\\times100\\,000 = 114\\,972 + 2\\,500 = \\mathbf{117\\,472}$ USD",None,117472.0)]),

num(146,2,"interest-rate-futures",
    "Eurodollar futures à 95.40. DV01 par contrat = 25 USD. Un hedger veut couvrir 50 M USD contre une hausse de taux sur 3 mois. Nombre de contrats ?",
    "contrats",50.0,"abs",0.5,
    "$N = 50\\,000\\,000 / 1\\,000\\,000 = \\mathbf{50}$ contrats (hedge parfait)","N_{exp}/N_{contract}"),

mcq(147,2,"interest-rate-futures","Un **contrat T-Bill futures** est coté en :",
    [("a","Indice $= 100 - $ taux d'escompte"),
     ("b","Pourcentage du nominal"),
     ("c","Prix en dollars"),
     ("d","Rendement actuariel")],
    "a","IMM index = 100 – taux de rendement annualisé.",
    {"b":"T-Bond futures oui, mais T-Bill non.","c":"Pas directement.","d":"Faux."}),

num(148,3,"interest-rate-futures",
    "Un gestionnaire détient 20 M USD d'obligations de duration $D_P=7$ ans. "
    "T-Bond futures : prix $= 108$, duration livrée $D_F=5.5$ ans. "
    "Nombre de contrats à vendre pour immuniser totalement ?",
    "contrats",235.0,"abs",1.0,
    "$N = \\frac{D_P \\times V_P}{D_F \\times Q_F} = \\frac{7\\times20\\,000\\,000}{5.5\\times108\\,000} = \\frac{140\\,000\\,000}{594\\,000} = \\mathbf{235.6} \\approx 236$ contrats",
    "\\frac{D_P V_P}{D_F Q_F}"),

mcq(149,2,"interest-rate-futures","La **livraison la moins chère** (cheapest-to-deliver, CTD) dans un T-Bond futures est :",
    [("a","L'obligation qui minimise le coût net pour le vendeur du futures"),
     ("b","L'obligation de plus faible coupon"),
     ("c","L'obligation de plus courte maturité"),
     ("d","L'obligation la plus récemment émise")],
    "a","CTD minimise : prix spot $-$ prix futures $\\times$ facteur de conversion.",
    {"b":"Pas nécessairement.","c":"Pas nécessairement.","d":"Pas nécessairement."}),

sa(150,2,"interest-rate-futures","Expliquez le **wild card option** dans les T-Bond futures.",
    ["Vendeur peut décider de livrer jusqu'à minuit après 14h","Valeur optionnelle pour le court"],
    "Le vendeur d'un T-Bond futures peut notifier son intention de livrer jusqu'à minuit, "
    "après la fixation du prix futures à 14h. Si les obligations baissent de 14h à minuit, "
    "le vendeur peut acheter à bas prix et livrer au prix futures plus élevé. "
    "Cette option de timing a une valeur et explique pourquoi $F_0 < (S-I)e^{rT}$ pour les T-Bond."),

num(151,2,"interest-rate-futures",
    "Taux cap implicite d'un Eurodollar futures à 94.75 (annualisé, base 360). "
    "Coût d'emprunt sur 90 jours pour 5 M USD ?",
    "USD",65625.0,"abs",100.0,
    "Taux $= (100-94.75)/100 = 5.25\\%$. Intérêts $= 5\\,000\\,000 \\times 0.0525 \\times 90/360 = \\mathbf{65\\,625}$ USD",
    "N \\times r \\times 90/360"),

nstep(152,3,"interest-rate-futures",
    "Une société veut **augmenter** la duration de son portefeuille de 4 à 7 ans. "
    "Valeur portefeuille = 30 M USD. T-Bond futures à prix 105, duration CTD = 6 ans.",
    [("Nombre de contrats à **acheter**","contrats",1.0,
      "$N=(D_T-D_P)\\times V_P/(D_F\\times Q_F)$",
      "$N=(7-4)\\times30\\,000\\,000/(6\\times105\\,000)=90\\,000\\,000/630\\,000=\\mathbf{143}$ contrats",None,143.0)]),

mcq(153,2,"interest-rate-futures","Un **FRA** (Forward Rate Agreement) est :",
    [("a","Un accord OTC pour fixer un taux d'intérêt sur un emprunt futur"),
     ("b","Un futures sur obligation d'État"),
     ("c","Un swap de taux d'intérêt"),
     ("d","Un contrat d'option sur taux")],
    "a","FRA = contrat OTC fixant le taux sur une période future ; réglé en espèces.",
    {"b":"Le futures est standardisé.","c":"Swap = échange de flux sur plusieurs périodes.","d":"Faux."}),

num(154,2,"interest-rate-futures",
    "FRA $3\\times6$ : taux forward $= 5.20\\%$, notionnel 10 M USD. Dans 3 mois, taux 3 mois SOFR $= 5.60\\%$. "
    "Règlement (USD) reçu par l'acheteur du FRA ?",
    "USD",9804.0,"abs",50.0,
    "Différence $= (5.60-5.20)/100 \\times 90/360 \\times 10\\,000\\,000 = 0.001 \\times 10\\,000\\,000 = 10\\,000$. "
    "Actualisé $= 10\\,000/(1+0.056\\times90/360) = 10\\,000/1.014 = \\mathbf{9\\,862}$ USD",
    "\\frac{(r_M-r_K) \\times L \\times \\tau}{1+r_M \\tau}"),

mcq(155,2,"interest-rate-futures","Le prix d'un T-Bond futures **augmente** quand :",
    [("a","Les taux d'intérêt baissent"),
     ("b","La duration de l'obligation CTD augmente"),
     ("c","Le taux repo augmente"),
     ("d","L'obligation livrable verse un coupon")],
    "a","Prix obligations et taux sont inversement liés → futures monte si taux baissent.",
    {"b":"Pas directement.","c":"Hausse du repo réduit le coût de portage, baisse le futures.","d":"Coupon réduit le prix (ex-div)."}),

num(156,3,"interest-rate-futures",
    "Taux repo 3 mois = $3\\%$, prix spot CTD = 98, coupon couru = 0, CF = 1.05. Prix futures T-Bond 3 mois ?",
    "",93.90,"rel",0.003,
    "$F_0 = (S-I)/CF \\times e^{rT} = 98/1.05 \\times e^{0.03\\times0.25} = 93.33\\times1.00751 = \\mathbf{94.04}$",
    "(S-I)/CF \\times e^{rT}"),

sa(157,2,"interest-rate-futures","Qu'est-ce que le **taux repo** et quel est son rôle dans la valorisation des futures T-Bond ?",
    ["Taux de pension livrée (financement court terme)","Détermine le coût de portage"],
    "Le **taux repo** est le taux d'un accord de pension livré (repo) : vente spot + rachat terme d'une obligation. "
    "Dans la valorisation des T-Bond futures, il représente le coût de financement de la position en obligation sous-jacente. "
    "$F_0 = (S-I)e^{r_{repo}T}/CF$. Un taux repo élevé abaisse le futures (carry cost élevé)."),

num(158,2,"interest-rate-futures",
    "Futures Eurodollar : variation de prix d'1 bp $= 25$ USD. Hedger long 1 M USD d'obligations, DV01 = 800 USD. "
    "Nombre de contrats Eurodollar pour couvrir le risque de taux ?",
    "contrats",32.0,"abs",0.5,
    "$N = DV01_P / DV01_F = 800/25 = \\mathbf{32}$ contrats","DV01_P/DV01_F"),

mcq(159,2,"interest-rate-futures","Un **strip de FRA** est équivalent à :",
    [("a","Un swap de taux d'intérêt"),("b","Un futures T-Bond"),
     ("c","Un put sur taux"),("d","Une obligation à coupon")],
    "a","Une série de FRA sur des périodes consécutives reproduit exactement un swap de taux.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(160,2,"interest-rate-futures",
    "Contrat Eurodollar : prix $=95.00$, taille $=$ 1 M USD. "
    "Le prix tombe à $94.80$. Perte pour le long (USD) ?",
    "USD",-500.0,"abs",1.0,
    "20 bp $\\times$ 25 USD/bp $= \\mathbf{-500}$ USD","\\Delta bp \\times 25"),

sa(161,2,"interest-rate-futures","Comment les futures T-Bond sont-ils utilisés pour **gérer la duration** d'un portefeuille obligataire ?",
    ["Vente de futures réduit la duration","Achat de futures augmente la duration"],
    "Vendre des T-Bond futures revient à **réduire** la duration du portefeuille (équivalent à vendre des obligations longues). "
    "Acheter des futures l'augmente. La formule : $\\Delta N = (D_T - D_P) \\times V_P / (D_F \\times Q_F)$ "
    "donne le nombre de contrats à acheter ($+$) ou vendre ($-$) pour atteindre la duration cible $D_T$."),

num(162,3,"interest-rate-futures",
    "Portefeuille obligataire de 50 M USD, $D_P=8$ ans. T-Bond futures à 112, $D_F=6.5$ ans. "
    "Pour ramener $D_T=5$ ans : vendre combien de contrats ?",
    "contrats",195.0,"abs",1.0,
    "$N=(D_P-D_T)\\times V_P/(D_F\\times Q_F)=(8-5)\\times50\\,000\\,000/(6.5\\times112\\,000)=150\\,000\\,000/728\\,000=\\mathbf{206}$ contrats",
    "(D_P-D_T)V_P/(D_F Q_F)"),
]
items[-1]["solution"]["value"] = 206.0

print(f"Items: {len(items)}")
batch = {"source":"Marchés des dérivés — Exercices originaux","track":"markets","module":"der-interest-rates","items":items}
with open(OUT,"w",encoding="utf-8") as f: json.dump(batch,f,ensure_ascii=False,indent=2)
print(f"Written: {OUT}")
