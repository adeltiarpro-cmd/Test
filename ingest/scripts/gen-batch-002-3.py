#!/usr/bin/env python3
"""Génère batch-002-3: der-swaps (42 items, clés 163-185 + 674-685 + 733-739)"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "../canonical/batch-002-3-der-swaps.json")

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

# ── swaps (163-185) ──────────────────────────────────────────────────────────

items += [
mcq(163,1,"swaps",
    "Un **swap de taux d'intérêt** (IRS) plain vanilla échange :",
    [("a","Des flux à taux fixe contre des flux à taux variable sur un notionnel commun"),
     ("b","Le notionnel entre les deux contreparties"),
     ("c","Des dividendes contre des intérêts"),
     ("d","Des flux en deux devises différentes")],
    "a","IRS plain vanilla : une partie paie fixe, l'autre paie variable (ex : SOFR). Seuls les flux nets sont échangés.",
    {"b":"Le notionnel ne change pas de mains dans un IRS.","c":"C'est un equity swap.",
     "d":"C'est un currency swap."}),

num(164,2,"swaps",
    "IRS : notionnel 10 M USD, taux fixe $k=4\\%$, SOFR courant $=5\\%$, paiement semestriel. "
    "Flux net payé par le **payeur fixe** à cette échéance (USD) ?",
    "USD",-50000.0,"abs",1.0,
    "Payeur fixe reçoit variable et paie fixe. Flux net $=(k-r_{var})\\times N\\times0.5=(0.04-0.05)\\times10\\,000\\,000\\times0.5=\\mathbf{-50\\,000}$ USD (perte).",
    "(k - r_{SOFR}) \\times N \\times \\tau"),

nstep(165,3,"swaps",
    "IRS 2 ans, notionnel 20 M USD, taux fixe $k=3.5\\%$, paiements annuels. "
    "Taux spot SOFR : $r_1=3\\%$, $r_2=3.8\\%$ (continus). "
    "Valorisez la **position fixe payeuse** en calculant : (a) la valeur de la jambe fixe, (b) la valeur de la jambe variable, (c) la valeur du swap.",
    [("Valeur jambe fixe (USD)","USD",100.0,
      "Actualiser les flux fixes $N\\times k$ aux taux spot",
      "$700\\,000\\,e^{-0.03}+20\\,700\\,000\\,e^{-0.076}=679\\,395+18\\,971\\,508=\\mathbf{19\\,650\\,903}$ USD",None,19650903.0),
     ("Valeur jambe variable (USD)","USD",100.0,
      "La jambe variable vaut le notionnel à la date de reset",
      "Juste après reset : valeur $=N=\\mathbf{20\\,000\\,000}$ USD (ou actualiser les flux variables prévus)",None,20000000.0),
     ("Valeur du swap payeur fixe (USD)","USD",100.0,None,
      "$V_{swap}=V_{variable}-V_{fixe}=20\\,000\\,000-19\\,650\\,903=\\mathbf{+349\\,097}$ USD","Le payeur fixe gagne quand les taux montent.",349097.0)]),

mcq(166,2,"swaps",
    "Le **taux de swap** (swap rate) à l'initiation est choisi de sorte que :",
    [("a","La valeur initiale du swap soit nulle"),
     ("b","Les paiements fixes soient toujours inférieurs aux paiements variables"),
     ("c","Le swap soit avantageux pour le payeur fixe"),
     ("d","Le notionnel soit minimisé")],
    "a","À l'initiation, $V_{swap}=0$ : le taux fixe $k$ est le taux de marché qui égalise jambe fixe et variable.",
    {"b":"Dépend des taux futurs.","c":"Valeur nulle = aucun avantage initial.","d":"Faux."}),

num(167,2,"swaps",
    "Taux SOFR 1 an $r_1=2.5\\%$, 2 ans $r_2=3.0\\%$, 3 ans $r_3=3.4\\%$ (continus). "
    "Quel est le **taux de swap 3 ans** $k$ (annuel, notionnel 1) ?",
    "%",3.35,"abs",0.05,
    "$k = \\frac{1-e^{-r_3 T_3}}{\\sum_{i=1}^3 e^{-r_i T_i}} = \\frac{1-e^{-0.034\\times3}}{e^{-0.025}+e^{-0.06}+e^{-0.102}}$"
    "$=\\frac{1-0.9028}{0.9753+0.9418+0.9031}=\\frac{0.0972}{2.8202}=\\mathbf{3.45}\\%$",
    "\\frac{1-e^{-r_n T_n}}{\\sum e^{-r_i T_i}}"),

sa(168,2,"swaps",
    "Expliquez comment un **swap** peut être vu comme un échange d'obligations.",
    ["Payeur fixe = long flottant + court fixe","Correspond à une obligation synthétique"],
    "Le payeur fixe dans un IRS peut être vu comme ayant :\n"
    "- **vendu** une obligation à taux fixe (obligation qu'il devrait payer des coupons fixes)\n"
    "- **acheté** une obligation à taux variable (qui lui verse SOFR)\n"
    "La valeur du swap = $B_{flottant} - B_{fixe}$ pour le payeur fixe. "
    "Cette décomposition facilite la valorisation : $B_{flottant}=N$ au reset, $B_{fixe}$ s'actualise aux taux spot."),

mcq(169,2,"swaps",
    "Dans un **currency swap**, le notionnel :",
    [("a","Est échangé au début et à la fin, en deux devises différentes"),
     ("b","N'est jamais échangé"),
     ("c","Est échangé uniquement à l'échéance"),
     ("d","Est déterminé par le taux de change à l'échéance")],
    "a","Currency swap : échange du principal en devises au début (et souvent à la fin), plus les intérêts.",
    {"b":"Contrairement à l'IRS où le notionnel n'est pas échangé.",
     "c":"En général, échangé aussi au début.","d":"Taux de change fixé au début."}),

num(170,3,"swaps",
    "Currency swap : société A paie $4\\%$ sur 10 M USD, reçoit $2\\%$ sur 8 M EUR. "
    "EUR/USD $=1.25$. Flux nets annuels en USD si l'EUR monte à $1.30$ ?",
    "USD",-240000.0,"abs",100.0,
    "Paie $: 10\\,000\\,000\\times0.04=400\\,000$ USD. Reçoit $: 8\\,000\\,000\\times0.02\\times1.30=208\\,000$ USD. "
    "Flux net $=208\\,000-400\\,000=\\mathbf{-192\\,000}$ USD.",
    "reçoit_{EUR}\\times FX - paie_{USD}"),

sa(171,2,"swaps",
    "Pourquoi les entreprises utilisent-elles des **swaps de devises** pour réduire leur coût d'emprunt ?",
    ["Avantage comparatif sur différents marchés","Arbitrage réglementaire et accès au marché"],
    "Chaque entreprise a un avantage comparatif sur un marché obligataire particulier. "
    "Par exemple, une firme américaine emprunte en USD à conditions avantageuses mais veut des EUR. "
    "Une firme européenne a l'avantage inverse. Elles empruntent chacune sur leur marché naturel "
    "puis **échangent** les flux via un swap. Les deux réduisent leur coût d'emprunt grâce à l'avantage comparatif."),

mcq(172,2,"swaps",
    "Un **equity swap** verse :",
    [("a","Le rendement total d'un indice contre un taux fixe ou variable"),
     ("b","Des dividendes contre des coupons"),
     ("c","La valeur d'une option sur action"),
     ("d","Des dividendes en actions contre des dividendes en espèces")],
    "a","Equity swap : une partie reçoit le rendement d'un indice (gains + dividendes), l'autre paie fixe ou LIBOR.",
    {"b":"Incomplet.","c":"Ce n'est pas un swap.","d":"Faux."}),

num(173,3,"swaps",
    "IRS 1 an, notionnel 5 M USD, taux fixe $k=4\\%$, paiements trimestriels. SOFR trimestriels : Q1=3.8%, Q2=4.1%, Q3=4.3%, Q4=4.5%. "
    "Gain **net** pour le receveur fixe sur l'année (USD) ?",
    "USD",8750.0,"abs",100.0,
    "Flux nets trimestriels $(r_{var}-k)\\times N\\times0.25$ : Q1=$(3.8-4)\\times5M\\times0.25=-2500$, Q2=+1250, Q3=+3750, Q4=+6250. "
    "Total $=-2500+1250+3750+6250=\\mathbf{8750}$ USD.",
    "\\sum (r_i - k) \\times N \\times \\tau"),

mcq(174,2,"swaps",
    "Le **risque de crédit** d'un swap est :",
    [("a","Le risque que la contrepartie ne respecte pas ses obligations"),
     ("b","Le risque de variation des taux d'intérêt"),
     ("c","Le risque de change"),
     ("d","Le risque de liquidité du marché")],
    "a","Le risque de crédit (contrepartie) est la préoccupation principale dans les swaps OTC non compensés.",
    {"b":"C'est le risque de marché.","c":"Faux pour un IRS en USD.","d":"Risque de liquidité ≠ crédit."}),

nstep(175,3,"swaps",
    "Société A : notation AAA, emprunte fixe à 4%, variable à SOFR+0.3%. "
    "Société B : notation BBB, emprunte fixe à 5.2%, variable à SOFR+0.8%. "
    "Montrez le **gain d'arbitrage** d'un swap où A emprunte fixe et B variable.",
    [("Avantage comparatif de A (pb fixe vs variable)","bp",0.5,
      "Différentiel fixe $-$ différentiel variable",
      "Fixe : $5.2-4=1.2\\%$. Variable : $0.8-0.3=0.5\\%$. Avantage A sur fixe : $1.2-0.5=\\mathbf{70}$ bp.",None,70.0),
     ("Gain total à partager (bp)","bp",0.5,None,
      "Gain total $=\\mathbf{70}$ bp (partagé entre A, B et le dealer).",None,70.0)]),

mcq(176,2,"swaps",
    "Un **amortizing swap** se distingue d'un vanilla IRS par :",
    [("a","Son notionnel qui diminue dans le temps"),
     ("b","Ses taux qui varient à chaque échéance"),
     ("c","Son règlement en capital"),
     ("d","Sa duration nulle")],
    "a","Amortizing swap : notionnel réduit selon un calendrier, utilisé pour couvrir des prêts immobiliers.",
    {"b":"Le taux fixe est constant.","c":"Comme un IRS standard.","d":"Faux."}),

num(177,3,"swaps",
    "IRS : payeur fixe $k=3\\%$, notionnel 10 M USD, 2 ans restants. Courbe plate à $r=4\\%$ (continu). "
    "La **valeur mark-to-market** du swap (payeur fixe) est :",
    "USD",190800.0,"abs",500.0,
    "$V=B_{flot}-B_{fixe}$. $B_{flot}=10\\,000\\,000$ (au prochain reset). "
    "$B_{fixe}=300\\,000\\,e^{-0.04}+10\\,300\\,000\\,e^{-0.08}=288\\,534+9\\,520\\,666=9\\,809\\,200$. "
    "$V=10\\,000\\,000-9\\,809\\,200=\\mathbf{+190\\,800}$ USD.",
    "B_{float} - B_{fix}"),

sa(178,2,"swaps",
    "Quels sont les **usages principaux** d'un swap de taux d'intérêt pour une entreprise ?",
    ["Convertir dette fixe en variable ou vice-versa","Spéculation sur la direction des taux"],
    "Un IRS permet à une entreprise de : (1) **convertir** un emprunt à taux fixe en taux variable "
    "(ou l'inverse) sans rembourser la dette, (2) **arbitrer** son avantage comparatif sur certains marchés, "
    "(3) **gérer** l'actif-passif (ALM) en alignant la sensibilité aux taux des actifs et passifs. "
    "Les banques utilisent massivement les IRS pour gérer leur risque de taux."),

mcq(179,2,"swaps",
    "Un **total return swap** (TRS) permet à l'acheteur de protection de :",
    [("a","Transférer le risque de crédit ET le risque de marché d'un actif"),
     ("b","Assurer uniquement le risque de défaut"),
     ("c","Recevoir les coupons d'une obligation sans la détenir"),
     ("d","Vendre l'obligation sous-jacente à terme")],
    "a","TRS : le vendeur de protection reçoit le rendement total (coupons + variation de prix), paie LIBOR±spread.",
    {"b":"C'est un CDS.","c":"Le vendeur de protection reçoit le rendement total.",
     "d":"Faux."}),

num(180,3,"swaps",
    "Swap de taux $k=3.5\\%$, notionnel 50 M USD, 3 ans, paiements annuels. "
    "Taux spot : $r_1=3\\%$, $r_2=3.5\\%$, $r_3=4\\%$ (continus). Vérifiez que $k$ donne $V_{swap}=0$.",
    "USD",0.0,"abs",100.0,
    "Jambe fixe : $\\sum 1\\,750\\,000\\,e^{-r_i}+50\\,000\\,000\\,e^{-0.12}$. "
    "Jambe variable = 50 M USD. Avec $k=3.5\\%$, on peut vérifier numériquement que $V=0$ au taux de marché initial.",
    "V_{swap}=B_{float}-B_{fixed}=0"),

mcq(181,2,"swaps",
    "Dans un IRS, le **risque de crédit net** est typiquement :",
    [("a","Inférieur au notionnel, car seuls les flux nets sont exposés"),
     ("b","Égal au notionnel"),
     ("c","Supérieur au notionnel à cause du levier"),
     ("d","Nul grâce à la chambre de compensation")],
    "a","Seul le flux net (différence fixe/variable) est à risque, pas le notionnel (qui n'est pas échangé).",
    {"b":"Faux.","c":"Faux.","d":"Vrai si compensé centralement, mais pas toujours."}),

num(182,3,"swaps",
    "Swap de devises : A paie $3\\%$ sur 8 M USD, reçoit $1.5\\%$ sur 7 M EUR. "
    "Taux forward EUR/USD dans 1 an $=1.12$. Valeur du flux variable EUR en USD ?",
    "USD",117600.0,"abs",100.0,
    "Flux EUR $= 7\\,000\\,000\\times0.015=105\\,000$ EUR. En USD $: 105\\,000\\times1.12=\\mathbf{117\\,600}$ USD.",
    "CF_{EUR} \\times FX_{forward}"),

sa(183,2,"swaps",
    "Comment un swap peut-il être utilisé pour **transformer un actif** (asset swap) ?",
    ["Convertit le rendement d'une obligation fixe en rendement variable","Utile pour les institutions à passifs variables"],
    "Dans un asset swap, un investisseur détient une obligation à coupon fixe $c$ et entre dans un IRS "
    "où il **paie fixe** $c$ et **reçoit** SOFR + spread. Le résultat synthétique est une obligation à taux variable. "
    "L'asset swap spread mesure la qualité de crédit de l'émetteur au-dessus de SOFR."),

mcq(184,2,"swaps",
    "Le **DV01** d'un IRS payeur fixe est :",
    [("a","Positif : si les taux montent, la valeur du swap augmente pour le payeur fixe"),
     ("b","Négatif : le payeur fixe perd quand les taux montent"),
     ("c","Nul car les flux se compensent"),
     ("d","Égal au DV01 du notionnel")],
    "a","Payeur fixe = position longue duration variable, courte duration fixe. Net : duration positive. Taux montent → valeur augmente.",
    {"b":"Inverse.","c":"Faux.","d":"Faux."}),

num(185,2,"swaps",
    "IRS de 5 ans, notionnel 100 M USD, taux fixe $k=5\\%$. DV01 = 4 200 USD/bp. "
    "Si les taux baissent de 30 bp, gain/perte pour le **receveur fixe** (USD) ?",
    "USD",-126000.0,"abs",500.0,
    "Receveur fixe a un DV01 **négatif** (positions inverses du payeur). "
    "Perte $= -4\\,200\\times30=\\mathbf{-126\\,000}$ USD.",
    "-DV01 \\times \\Delta bp"),
]

# ── convexity-timing-and-quanto-adjustments (674-685) ──────────────────────

items += [
mcq(674,3,"convexity-timing-and-quanto-adjustments",
    "L'**ajustement de convexité** pour passer du taux futures au taux forward est :",
    [("a","Positif : le taux futures est supérieur au taux forward"),
     ("b","Nul : les deux taux sont identiques"),
     ("c","Négatif : le futures est inférieur au forward"),
     ("d","Variable selon la durée du contrat uniquement")],
    "a","Le marking-to-market du futures crée un biais positif : taux futures $>$ taux forward de même maturité.",
    {"b":"Faux.","c":"Faux.","d":"L'ajustement dépend aussi de la volatilité."}),

num(675,3,"convexity-timing-and-quanto-adjustments",
    "Taux futures Eurodollar à 5 ans : $4.80\\%$. Volatilité $\\sigma=1.2\\%$ annuel. "
    "Ajustement de convexité approx $=\\frac{1}{2}\\sigma^2 t_1 t_2$ (Hull). "
    "Avec $t_1=5$ ans, $t_2=5.25$ ans, taux forward $\\approx$ ?",
    "%",4.611,"abs",0.01,
    "Ajustement $= \\frac{1}{2}(0.012)^2\\times5\\times5.25=\\frac{1}{2}\\times0.000144\\times26.25=0.00189=\\mathbf{0.189}\\%$. "
    "Forward $\\approx4.80-0.189=\\mathbf{4.611}\\%$.",
    "r_f \\approx r_{futures} - \\frac{1}{2}\\sigma^2 t_1 t_2"),

mcq(676,2,"convexity-timing-and-quanto-adjustments",
    "L'**ajustement de timing** est nécessaire quand :",
    [("a","Le paiement du flux se produit à un moment différent de la période d'observation"),
     ("b","Le taux n'est pas le LIBOR"),
     ("c","Le notionnel varie dans le temps"),
     ("d","L'ajustement de convexité est nul")],
    "a","Si un taux SOFR 6 mois est observé en $t$ mais payé en $t + 6$ mois, un ajustement de timing est requis.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(677,3,"convexity-timing-and-quanto-adjustments",
    "SOFR 6 mois dans 2 ans : forward $=3.5\\%$, $\\sigma=0.8\\%$, corrélation taux/FX $\\rho=0.3$, "
    "volatilité FX $\\sigma_{FX}=10\\%$, $t=2$ ans. "
    "Ajustement quanto approx $=-\\rho\\sigma\\sigma_{FX}t$ : valeur ?",
    "%",-0.048,"abs",0.002,
    "$= -0.3\\times0.008\\times0.10\\times2 = \\mathbf{-0.048}\\%$",
    "-\\rho \\sigma_r \\sigma_{FX} t"),

sa(678,2,"convexity-timing-and-quanto-adjustments",
    "Qu'est-ce qu'un **quanto** et pourquoi nécessite-t-il un ajustement de valorisation ?",
    ["Payoff dans une devise, sous-jacent dans une autre","Corrélation taux/FX crée un biais"],
    "Un quanto est un dérivé dont le payoff est calculé dans une devise mais réglé dans une autre à taux de change fixé. "
    "Par exemple, un investisseur européen reçoit le rendement du S&P500 en EUR à 1:1. "
    "La corrélation entre le sous-jacent et le taux de change crée un biais dans l'espérance du payoff : "
    "l'ajustement quanto est $\\exp(-\\rho\\sigma_S\\sigma_{FX}T)$."),

mcq(679,3,"convexity-timing-and-quanto-adjustments",
    "L'ajustement de convexité pour les SOFR futures à longue maturité est important car :",
    [("a","La volatilité des taux amplifiée sur de longues périodes crée un écart significatif"),
     ("b","Les contrats lointains ont moins de liquidité"),
     ("c","Le taux SOFR est naturellement plus convexe que le LIBOR"),
     ("d","Les marchés à terme sont inefficients sur les longues maturités")],
    "a","L'ajustement $\\propto \\sigma^2 t_1 t_2$ croît avec le temps, devenant significatif au-delà de 2 ans.",
    {"b":"Liquidité ≠ convexité.","c":"Faux.","d":"Faux."}),

num(680,3,"convexity-timing-and-quanto-adjustments",
    "Taux forward à 3 ans : $4.0\\%$. Ajustement de convexité calculé : $+15$ bp. "
    "Taux futures correspondant ?",
    "%",4.15,"abs",0.01,
    "Taux futures $=$ forward $+$ ajustement $= 4.0+0.15=\\mathbf{4.15}\\%$.",
    "r_{futures} = r_{forward} + CA"),

nstep(681,3,"convexity-timing-and-quanto-adjustments",
    "Un contrat futures Eurodollar à 4 ans cote 94.50. Volatilité $\\sigma=1.5\\%$, $t_1=4$, $t_2=4.25$ ans. "
    "Estimez : (a) l'ajustement de convexité, (b) le taux forward.",
    [("Ajustement de convexité (bp)","bp",0.5,
      "$CA=\\frac{1}{2}\\sigma^2 t_1 t_2$",
      "$CA=\\frac{1}{2}(0.015)^2\\times4\\times4.25=\\frac{1}{2}\\times0.000225\\times17=0.001913=\\mathbf{19.1}$ bp",None,19.1),
     ("Taux forward (%)","%" ,0.01,None,
      "Taux futures $=100-94.50=5.50\\%$. Forward $=5.50-0.191=\\mathbf{5.309}\\%$",None,5.309)]),

sa(682,2,"convexity-timing-and-quanto-adjustments",
    "Expliquez intuitivement pourquoi le **taux futures est supérieur au taux forward** de même maturité.",
    ["Marking-to-market avantage le court sur futures de taux","Corrélation gains/réinvestissement"],
    "Le détenteur d'une position **courte** sur un futures de taux (qui bénéficie d'une hausse des taux) "
    "reçoit des flux de marge précisément quand les taux sont élevés → ces flux sont réinvestis à un taux élevé. "
    "À l'inverse, le long paie des flux quand les taux sont élevés et reçoit quand ils sont bas. "
    "Pour compenser ce désavantage du long, le taux futures doit être plus élevé que le taux forward."),

mcq(683,2,"convexity-timing-and-quanto-adjustments",
    "Dans un **CMS swap** (Constant Maturity Swap), un ajustement est nécessaire car :",
    [("a","Le taux CMS est observé mais payé à une fréquence différente de sa maturité naturelle"),
     ("b","Le CMS est toujours plus élevé que le taux swap court"),
     ("c","Le notionnel est en devises étrangères"),
     ("d","Le CMS n'est pas un taux de marché standard")],
    "a","Le taux swap 10 ans observé à chaque trimestre et payé trimestriellement nécessite un ajustement de convexité et de timing.",
    {"b":"Pas toujours.","c":"Pas lié.","d":"Faux."}),

num(684,3,"convexity-timing-and-quanto-adjustments",
    "Swap CMS : taux 5 ans forward $=3.8\\%$, ajustement de convexité $=12$ bp, ajustement de timing $=-3$ bp. "
    "Taux CMS ajusté ?",
    "%",3.89,"abs",0.01,
    "$r_{CMS}=3.80+0.12-0.03=\\mathbf{3.89}\\%$",
    "r_{fwd} + CA + TA"),

sa(685,2,"convexity-timing-and-quanto-adjustments",
    "Pourquoi les ajustements de **quanto, timing et convexité** sont-ils souvent groupés dans les modèles de taux ?",
    ["Ils corrigent tous des biais liés à la non-linéarité ou au décalage temporel","Nécessaires pour pricing cohérent"],
    "Ces trois ajustements corrigent des **biais systématiques** introduits par (1) la convexité de la relation prix/taux, "
    "(2) le décalage entre la date d'observation et la date de paiement, "
    "(3) la corrélation entre le taux et le taux de change dans les produits multi-devises. "
    "Dans un modèle de taux cohérent (HJM, BGM), ces ajustements émergent naturellement du changement de mesure."),
]

# ── swaps-revisited (733-739) ────────────────────────────────────────────────

items += [
sa(733,2,"swaps-revisited",
    "Comment les **OIS** (Overnight Index Swaps) diffèrent-ils des IRS classiques, et pourquoi sont-ils devenus la référence d'actualisation post-2008 ?",
    ["OIS indexé sur taux overnight","Risque de crédit quasi-nul → taux sans risque de marché"],
    "Un OIS échange un taux fixe contre le taux overnight composé (SOFR, €STR...) sur la période. "
    "Contrairement au LIBOR (panel de banques, risque de crédit intégré), l'OIS reflète quasi exactement "
    "le taux sans risque à court terme. Post-2008, l'écart LIBOR-OIS s'est élargi, montrant que le LIBOR "
    "contenait une prime de crédit significative. Les desks de dérivés actualisent désormais à l'OIS."),

nstep(734,3,"swaps-revisited",
    "IRS avec **CSA** (Credit Support Annex) : notionnel 10 M USD, payeur fixe $k=3\\%$, 1 an restant. "
    "Taux OIS 1 an $=2.5\\%$ (continu). Valorisez le swap payeur fixe.",
    [("Flux fixe actualisé à l'OIS (USD)","USD",10.0,
      "Actualiser le flux fixe $N\\times k$ à l'OIS",
      "$300\\,000\\,e^{-0.025}=300\\,000\\times0.9753=\\mathbf{292\\,590}$ USD",None,292590.0),
     ("Flux variable actualisé (USD)","USD",10.0,None,
      "La jambe variable vaut $N=10\\,000\\,000$ USD au reset (actualisation OIS).",None,10000000.0),
     ("Valeur du swap payeur fixe (USD)","USD",10.0,None,
      "$V = 10\\,000\\,000 - (292\\,590+10\\,000\\,000\\,e^{-0.025})$"
      "$= 10\\,000\\,000 - (292\\,590+9\\,753\\,099) = 10\\,000\\,000-10\\,045\\,689 = \\mathbf{-45\\,689}$ USD",
      "Taux fixe > OIS : payeur fixe est en perte.",
      -45689.0)]),

mcq(735,2,"swaps-revisited",
    "Le **SOFR** (Secured Overnight Financing Rate) remplace le LIBOR USD car :",
    [("a","Il est basé sur des transactions réelles de repo, non sur des déclarations bancaires"),
     ("b","Il est plus élevé que le LIBOR"),
     ("c","Il intègre le risque de crédit bancaire"),
     ("d","Il n'est disponible que pour les maturités courtes")],
    "a","SOFR = taux de marché des repos overnight sur T-Bills. Objectif : éliminér la manipulation possible du LIBOR.",
    {"b":"En général plus bas (sans prime crédit).","c":"Sans risque de crédit.","d":"Des term rates SOFR existent."}),

num(736,2,"swaps-revisited",
    "Spread LIBOR-OIS = 25 bp. Valeur d'un IRS à taux LIBOR vs IRS à taux OIS, notionnel 100 M USD, 5 ans, paiements annuels ? "
    "Différence de valeur approx (USD) en supposant 25 bp de spread constant ?",
    "USD",1175000.0,"abs",10000.0,
    "VA d'un spread de 25 bp annuel sur 5 ans $\\approx 0.0025\\times100\\,000\\,000\\times\\sum_{t=1}^5 e^{-r_t t}$. "
    "Avec $r=2\\%$ : $\\sum = 4.71$. Valeur $\\approx 250\\,000\\times4.71=\\mathbf{1\\,177\\,500}$ USD.",
    "N \\times \\Delta r \\times \\sum e^{-r_t t}"),

sa(737,2,"swaps-revisited",
    "Qu'est-ce que le **swap spread** et qu'indique-t-il sur les conditions de marché ?",
    ["Écart entre taux swap et taux T-Bond de même maturité","Reflète le risque de crédit bancaire agrégé"],
    "Le swap spread = taux fixe d'un IRS − taux T-Bond de même maturité. "
    "Il reflète : (1) la **prime de crédit** du secteur bancaire (les contreparties swaps sont typiquement des banques), "
    "(2) la **demande de couverture** de duration par les assureurs et fonds de pension, "
    "(3) des effets de liquidité. Un swap spread négatif (observé post-2008 aux USA) indique que "
    "les T-Bonds sont perçus comme moins liquides que les swaps, phénomène paradoxal."),

mcq(738,2,"swaps-revisited",
    "Un **swaption** est :",
    [("a","Une option pour entrer dans un swap à des conditions prédéfinies"),
     ("b","Un swap où les taux sont des options"),
     ("c","Un swap avec option de remboursement anticipé"),
     ("d","Une obligation avec des clauses swap intégrées")],
    "a","Une payer swaption donne le droit (sans obligation) d'entrer dans un IRS en tant que payeur fixe.",
    {"b":"Faux.","c":"C'est un callable swap.","d":"Faux."}),

nstep(739,3,"swaps-revisited",
    "Swap 3 ans existant : payeur fixe $k=3\\%$, notionnel 20 M USD. Taux de marché actuels : "
    "$r_1=2.8\\%, r_2=3.2\\%, r_3=3.5\\%$ (continus). Calculez la **valeur du swap payeur fixe**.",
    [("Valeur jambe variable (USD)","USD",100.0,None,
      "Juste après reset : $B_{float}=\\mathbf{20\\,000\\,000}$ USD",None,20000000.0),
     ("Valeur jambe fixe (USD)","USD",100.0,
      "$B_{fix}=600\\,000\\,e^{-r_1}+600\\,000\\,e^{-2r_2}+20\\,600\\,000\\,e^{-3r_3}$",
      "$=600\\,000\\times0.9724+600\\,000\\times0.9394+20\\,600\\,000\\times0.9003$"
      "$=583\\,440+563\\,640+18\\,546\\,180=\\mathbf{19\\,693\\,260}$ USD",None,19693260.0),
     ("Valeur du swap payeur fixe (USD)","USD",100.0,None,
      "$V=B_{float}-B_{fix}=20\\,000\\,000-19\\,693\\,260=\\mathbf{+306\\,740}$ USD",
      "Payeur fixe gagne quand les taux de marché > taux du swap.",306740.0)]),
]

print(f"Items: {len(items)}")
assert len(items) == 42, f"Expected 42, got {len(items)}"

batch = {"source":"Marchés des dérivés — Exercices originaux","track":"markets","module":"der-swaps","items":items}
with open(OUT,"w",encoding="utf-8") as f: json.dump(batch,f,ensure_ascii=False,indent=2)
print(f"Written: {OUT}")
