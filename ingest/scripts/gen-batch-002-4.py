#!/usr/bin/env python3
"""batch-002-4: der-options-mechanics (69 items, clés 206-227, 228-253, 254-274)"""
import json, os
OUT = os.path.join(os.path.dirname(__file__), "../canonical/batch-002-4-der-options-mechanics.json")

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

C1="mechanics-of-options-markets"
C2="properties-of-stock-options"
C3="trading-strategies-involving-options"

items=[
# ── mechanics-of-options-markets (206-227) ───────────────────────────────────
mcq(206,1,C1,"Sur un marché d'options organisé, la **chambre de compensation** :",
    [("a","Garantit l'exécution de chaque contrat en s'interposant"),
     ("b","Fixe les prix des options"),("c","Évalue les primes chaque semaine"),("d","Regroupe acheteurs et vendeurs directement")],
    "a","La CCP élimine le risque de contrepartie : elle est l'acheteur de tout vendeur et le vendeur de tout acheteur.",
    {"b":"Les prix sont déterminés par le marché.","c":"Marking-to-market quotidien.","d":"C'est le rôle du marché."}),

mcq(207,2,C1,"La **marge initiale** pour un vendeur d'options est exigée car :",
    [("a","Le vendeur a une perte potentiellement illimitée"),
     ("b","L'acheteur risque de ne pas payer la prime"),
     ("c","La CCP doit financer ses activités"),("d","Le régulateur l'impose uniquement pour les calls")],
    "a","L'acheteur a déjà payé la prime (perte max = prime). Le vendeur peut perdre bien plus → marge.",
    {"b":"La prime est payée à l'entrée.","c":"Faux.","d":"Faux."}),

num(208,2,C1,"Un trader vend 5 calls à prime $c=3.50$ USD, chaque contrat couvre 100 actions. Encaissement total (USD) ?",
    "USD",1750.0,"abs",0.01,"$5\\times100\\times3.50=\\mathbf{1\\,750}$ USD","n\\times N\\times c"),

mcq(209,1,C1,"La date d'**expiration** d'une option américaine est :",
    [("a","La dernière date à laquelle elle peut être exercée"),("b","La date de création du contrat"),
     ("c","La date du premier appel de marge"),("d","Toujours un mardi")],
    "a","Une option américaine peut être exercée à tout moment jusqu'à la date d'expiration incluse.",
    {"b":"C'est la date d'émission.","c":"Faux.","d":"Typiquement troisième vendredi du mois."}),

mcq(210,2,C1,"L'**exercice automatique** (automatic exercise) à l'échéance s'applique quand :",
    [("a","L'option est in-the-money d'au moins 0.01 USD"),("b","Le détenteur n'a pas annulé son contrat"),
     ("c","La prime initiale était supérieure à 1 USD"),("d","L'option est de type américain")],
    "a","Les options ITM de plus d'un cent sont automatiquement exercées à l'échéance sauf instruction contraire.",
    {"b":"Non lié.","c":"Faux.","d":"L'exercice automatique concerne surtout les européennes à l'échéance."}),

num(211,2,C1,"Un call $K=50$ USD est ITM de 3 USD. Prix spot actuel (USD) ?",
    "USD",53.0,"abs",0.01,"$S=K+\\text{ITM}=50+3=\\mathbf{53}$ USD","K + \\text{ITM}"),

mcq(212,2,C1,"La **taille standard** d'un contrat d'option sur action aux USA est :",
    [("a","100 actions"),("b","1 000 actions"),("c","10 actions"),("d","Variable selon le broker")],
    "a","Convention : 1 contrat = 100 actions sous-jacentes.",
    {"b":"Faux.","c":"Faux.","d":"Standardisé par la bourse."}),

mcq(213,2,C1,"L'**open interest** sur les options représente :",
    [("a","Le nombre de contrats ouverts non liquidés"),("b","Le volume journalier"),
     ("c","La somme des options calls ouvertes"),("d","Le nombre d'options exercées")],
    "a","Open interest = positions ouvertes. Volume = transactions de la journée.",
    {"b":"Faux.","c":"OI inclut calls et puts.","d":"Faux."}),

num(214,2,C1,"Prix spot $S=75$ USD. Call $K=80$ USD. Valeur intrinsèque du call (USD) ?",
    "USD",0.0,"abs",0.01,"Call OTM : $\\max(75-80,0)=\\mathbf{0}$ USD","\\max(S-K,0)"),

mcq(215,2,C1,"Un **put protecteur** (protective put) consiste à :",
    [("a","Acheter un put sur une action qu'on détient déjà"),("b","Vendre un put à découvert"),
     ("c","Acheter un call pour protéger un put court"),("d","Combiner un call et un put OTM")],
    "a","Protective put = long action + long put. Limite la perte à la baisse tout en gardant le potentiel haussier.",
    {"b":"Position nue risquée.","c":"Faux.","d":"Faux."}),

mcq(216,2,C1,"Un **covered call** consiste à :",
    [("a","Vendre un call sur une action qu'on détient"),("b","Acheter un call couvert par de la marge"),
     ("c","Acheter un call et un put simultanément"),("d","Vendre un put couvert par des obligations")],
    "a","Covered call : long action + short call. Génère un revenu (prime) en échange du plafond de gain.",
    {"b":"Faux.","c":"C'est un straddle.","d":"Faux."}),

num(217,3,C1,"Covered call : achat action à 48 USD, vente call $K=50$ USD, prime $c=2$ USD. "
    "Profit maximum de la stratégie (USD) ?",
    "USD",4.0,"abs",0.01,"Profit max si $S_T\\geq K$: $(K-S_0)+c=2+2=\\mathbf{4}$ USD","(K-S_0)+c"),

sa(218,2,C1,"Décrivez le mécanisme de l'**exercice d'une option américaine** et ses implications pour le vendeur.",
    ["Notification via le broker","Vendeur obligé de livrer/recevoir l'actif"],
    "L'acheteur notifie son broker de son intention d'exercer. Le broker transmet à la CCP qui assigne "
    "aléatoirement un vendeur (short) du même contrat. Ce vendeur doit alors "
    "livrer les actions (call) ou les acheter (put) au prix d'exercice $K$. "
    "L'exercice anticipé d'un call américain sur action sans dividende n'est généralement pas optimal."),

mcq(219,2,C1,"Les options **LEAPS** sont :",
    [("a","Des options à longue échéance (jusqu'à 3 ans)"),("b","Des options sur indices uniquement"),
     ("c","Des options à règlement journalier"),("d","Des options sans valeur temps")],
    "a","Long-term Equity AnticiPation Securities = options avec des maturités pouvant atteindre 2-3 ans.",
    {"b":"Disponibles sur actions et indices.","c":"Faux.","d":"Elles ont une valeur temps importante."}),

num(220,2,C1,"Prime d'un call = 4.50 USD. Valeur intrinsèque = 2.00 USD. Valeur temps (USD) ?",
    "USD",2.50,"abs",0.01,"$\\text{Valeur temps}=c-\\max(S-K,0)=4.50-2.00=\\mathbf{2.50}$ USD","c-\\max(S-K,0)"),

mcq(221,2,C1,"Le prix d'exercice **at-the-money** signifie que :",
    [("a","$K \\approx S_0$"),("b","$K < S_0$ pour un call"),("c","$K > S_0$ pour un put"),("d","L'option vaut sa valeur intrinsèque")],
    "a","ATM = strike proche du prix spot actuel.",
    {"b":"Ce serait ITM pour un call.","c":"Ce serait ITM pour un put.","d":"ATM a valeur intrinsèque ~0."}),

num(222,2,C1,"Un investisseur achète 10 puts $K=40$ USD, prime $p=2.50$ USD (100 actions/contrat). "
    "Investissement initial total (USD) ?",
    "USD",2500.0,"abs",0.01,"$10\\times100\\times2.50=\\mathbf{2\\,500}$ USD","n\\times N\\times p"),

sa(223,2,C1,"Expliquez la différence entre **options européennes** et **américaines** en termes de prime.",
    ["Option américaine ≥ européenne (droit supplémentaire)","Parité put-call différente"],
    "Une option américaine donne **plus de droits** qu'une européenne (exercice possible à tout moment vs seulement à maturité). "
    "Elle vaut donc au moins autant : $C_{am}\\geq C_{eu}$, $P_{am}\\geq P_{eu}$. "
    "En pratique, pour un call sur action sans dividende, $C_{am}=C_{eu}$ car l'exercice anticipé n'est jamais optimal. "
    "Pour les puts ou les calls sur actions avec dividendes importants, la prime américaine peut être strictement supérieure."),

mcq(224,1,C1,"La **prime** d'une option est :",
    [("a","Le prix payé par l'acheteur au vendeur pour acquérir le droit"),
     ("b","La différence entre le prix spot et le strike"),
     ("c","Le dépôt de marge initial"),("d","Le profit à l'exercice")],
    "a","La prime = prix de l'option, versée au vendeur à l'entrée.",
    {"b":"C'est la valeur intrinsèque.","c":"La marge est exigée du vendeur, pas de l'acheteur.","d":"Faux."}),

mcq(225,2,C1,"Une option **deep out-of-the-money** a une valeur temps :",
    [("a","Faible, car la probabilité d'expirer ITM est très faible"),
     ("b","Maximale, car tout est valeur temps"),("c","Nulle"),("d","Égale à sa prime totale")],
    "a","Deep OTM : faible probabilité d'ITM → valeur temps faible. ATM a la valeur temps maximale.",
    {"b":"ATM a la valeur temps maximale, pas deep OTM.","c":"Non nulle mais faible.","d":"Vrai, mais la prime totale est faible."}),

num(226,2,C1,"Option call $K=100$ USD, prime $c=6$ USD. L'action est à $S=104$ USD. "
    "Quel est le **levier implicite** (ratio exposition/investissement) ?",
    "",17.33,"abs",0.1,"Levier $=S/c=104/6=\\mathbf{17.33}$","S/c"),

mcq(227,2,C1,"Lors d'un **split 2-pour-1**, les contrats d'options existants sont ajustés ainsi :",
    [("a","Strike divisé par 2, nombre de contrats multiplié par 2"),
     ("b","Prime divisée par 2 uniquement"),
     ("c","Aucun ajustement, les contrats sont annulés"),
     ("d","Strike multiplié par 2, taille réduite de moitié")],
    "a","La chambre ajuste automatiquement pour maintenir la valeur totale de la position.",
    {"b":"La taille et le strike sont ajustés.","c":"Faux.","d":"Inverse."}),

# ── properties-of-stock-options (228-253) ───────────────────────────────────
mcq(228,2,C2,"La **parité put-call** pour des options européennes stipule que :",
    [("a","$c + Ke^{-rT} = p + S_0$"),("b","$c = p$ toujours"),
     ("c","$c + p = S_0 + K$"),("d","$c - p = S_0 - K$")],
    "a","Parité : $c + Ke^{-rT} = p + S_0$ (sans dividende).",
    {"b":"Seulement si ATM et $r=0$.","c":"Pas d'actualisation correcte.","d":"Faux."}),

num(229,3,C2,"Call européen $c=5$ USD, $K=50$ USD, $T=0.5$ an, $r=4\\%$. Quel doit être le prix du put (parité) si $S_0=52$ USD ?",
    "USD",2.02,"abs",0.02,"$p=c+Ke^{-rT}-S_0=5+50e^{-0.02}-52=5+49.01-52=\\mathbf{2.01}$ USD","c+Ke^{-rT}-S_0"),

mcq(230,2,C2,"La borne **inférieure** d'un call européen sur action sans dividende est :",
    [("a","$\\max(S_0-Ke^{-rT},0)$"),("b","$S_0-K$"),("c","$Ke^{-rT}$"),("d","$S_0$")],
    "a","$c\\geq\\max(S_0-Ke^{-rT},0)$ car on peut arbitrer si $c < S_0-Ke^{-rT}$.",
    {"b":"Pas d'actualisation.","c":"Borne supérieure du put.","d":"Borne supérieure du call."}),

num(231,2,C2,"$S_0=60$ USD, $K=55$ USD, $r=5\\%$, $T=0.5$ an. Borne inférieure du call européen (USD) ?",
    "USD",6.35,"abs",0.02,"$\\max(60-55e^{-0.025},0)=\\max(60-53.65,0)=\\mathbf{6.35}$ USD","\\max(S_0-Ke^{-rT},0)"),

mcq(232,2,C2,"L'exercice anticipé d'un **call américain** sur action sans dividende :",
    [("a","N'est jamais optimal car il détruit la valeur temps"),
     ("b","Est toujours optimal quand l'option est très ITM"),
     ("c","Est optimal dès que $S > K$"),("d","Dépend uniquement du taux sans risque")],
    "a","Exercer anticipément détruit la valeur temps résiduelle. Mieux vaut vendre l'option.",
    {"b":"Même très ITM, la valeur temps > 0.","c":"Faux.","d":"Pas uniquement."}),

mcq(233,2,C2,"L'exercice anticipé d'un **put américain** peut être optimal quand :",
    [("a","Le put est très ITM et les taux d'intérêt sont élevés"),
     ("b","Le put est ATM"),("c","Le put est OTM"),("d","L'action ne verse pas de dividende")],
    "a","Put profond ITM : gain d'intérêts sur $K$ justifie l'exercice anticipé. Plus les taux sont élevés, plus c'est avantageux.",
    {"b":"Valeur temps trop élevée.","c":"Exercice inutile.","d":"Sans dividende, l'exercice anticipé peut toujours être optimal pour les puts."}),

num(234,2,C2,"$S_0=45$ USD, $K=50$ USD, $r=3\\%$, $T=1$ an. Borne inférieure du put européen (USD) ?",
    "USD",3.52,"abs",0.02,"$\\max(Ke^{-rT}-S_0,0)=\\max(50e^{-0.03}-45,0)=\\max(48.52-45,0)=\\mathbf{3.52}$ USD","\\max(Ke^{-rT}-S_0,0)"),

mcq(235,2,C2,"Si la volatilité du sous-jacent **augmente**, les primes des calls et puts :",
    [("a","Augmentent toutes les deux"),("b","Le call monte, le put baisse"),
     ("c","Le put monte, le call baisse"),("d","Restent inchangées")],
    "a","La volatilité accroît la probabilité d'un grand mouvement dans les deux sens → les deux options valent plus.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(236,3,C2,"Call : $c=8$ USD, $S_0=55$, $K=50$, $r=6\\%$, $T=0.5$ an. Vérifiez la parité put-call. Prix du put $p$ ?",
    "USD",1.52,"abs",0.05,"$p=c-S_0+Ke^{-rT}=8-55+50e^{-0.03}=8-55+48.52=\\mathbf{1.52}$ USD","c-S_0+Ke^{-rT}"),

mcq(237,2,C2,"Une **prime élevée** pour un call correspond à (toutes choses égales) :",
    [("a","Volatilité élevée, maturité longue, $S$ élevé par rapport à $K$"),
     ("b","Volatilité faible et maturité courte"),("c","Strike élevé et spot faible"),
     ("d","Taux d'intérêt nul")],
    "a","Call monte avec : $\\sigma\\uparrow$, $T\\uparrow$, $S\\uparrow$, $r\\uparrow$, $K\\downarrow$.",
    {"b":"Faux.","c":"Faux.","d":"Un taux nul réduit la VA du strike → call légèrement affecté."}),

num(238,2,C2,"$S_0=100$, dividende $D=2$ USD versé dans 3 mois ($t=0.25$). $r=5\\%$. "
    "Valeur actuelle du dividende (USD) ?",
    "USD",1.975,"abs",0.005,"$PV(D)=2e^{-0.05\\times0.25}=2\\times0.9876=\\mathbf{1.975}$ USD","De^{-rT_D}"),

mcq(239,2,C2,"L'**effet** d'une hausse du taux sans risque sur le prix d'un call européen est :",
    [("a","Le call monte (la VA du strike baisse)"),("b","Le call baisse"),
     ("c","Aucun effet car le call ne dépend pas de $r$"),("d","Ambigu selon la maturité")],
    "a","$r\\uparrow$ → $Ke^{-rT}\\downarrow$ → $c\\uparrow$. Aussi : le taux de croissance du spot est $r$ dans le monde risque-neutre.",
    {"b":"Faux.","c":"Faux.","d":"Effet positif clair."}),

num(240,3,C2,"Actions paient un dividende $q=3\\%$ continu. Parité put-call : $c+Ke^{-rT}=p+S_0e^{-qT}$. "
    "$S_0=80$, $K=78$, $r=4\\%$, $q=3\\%$, $T=1$ an, $c=7$ USD. Prix du put $p$ ?",
    "USD",4.36,"abs",0.05,"$p=c+Ke^{-rT}-S_0e^{-qT}=7+78e^{-0.04}-80e^{-0.03}=7+74.99-77.63=\\mathbf{4.36}$ USD",
    "c+Ke^{-rT}-S_0e^{-qT}"),
]
items[-1]["solution"]["value"]=4.36
items+=[

mcq(241,2,C2,"La borne **supérieure** d'un call européen est :",
    [("a","$S_0$ — on ne paiera jamais plus que le sous-jacent lui-même"),
     ("b","$K$ — on ne paiera jamais plus que le strike"),
     ("c","$S_0+K$"),("d","Illimitée")],
    "a","$c\\leq S_0$ : un call qui donne le droit d'acheter $S$ ne peut valoir plus que $S$ lui-même.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(242,2,C2,"$S_0=45$, $K=45$, $r=5\\%$, $T=3$ mois. Borne inférieure du call européen ATM (USD) ?",
    "USD",0.556,"abs",0.01,"$\\max(45-45e^{-0.05\\times0.25},0)=\\max(45-44.44,0)=\\mathbf{0.556}$ USD","\\max(S_0-Ke^{-rT},0)"),

sa(243,2,C2,"Pourquoi la **prime d'une option augmente-t-elle avec la maturité** ?",
    ["Plus de temps = plus de probabilité d'un grand mouvement","Valeur temps croît avec T"],
    "La valeur temps d'une option reflète la probabilité que le sous-jacent évolue favorablement. "
    "Plus la maturité est longue, plus cette probabilité est élevée (le sous-jacent peut se déplacer plus). "
    "Mathématiquement, dans BSM : la valeur $\\propto \\sigma\\sqrt{T}$. "
    "Exception : pour les puts profonds ITM à taux élevés, un put européen peut valoir moins avec une maturité plus longue."),

mcq(244,2,C2,"Si $c > S_0 - Ke^{-rT}$ n'est pas respecté, l'arbitrage consiste à :",
    [("a","Acheter le call, vendre le stock, investir $Ke^{-rT}$"),
     ("b","Acheter le stock et le call"),
     ("c","Vendre le call, acheter le put"),("d","Aucun arbitrage possible")],
    "a","Si $c < S_0-Ke^{-rT}$: acheter le call (sous-évalué) et vendre le stock + investir $Ke^{-rT}$.",
    {"b":"Renforce la sous-évaluation.","c":"Stratégie différente.","d":"Faux."}),

num(245,2,C2,"Une action paiera un dividende de 3 USD dans 2 mois. $S_0=60$, $r=5\\%$, $T=6$ mois, $K=58$. "
    "Prix forward ajusté du dividende $S^*=S_0-PV(D)$ ?",
    "USD",57.02,"abs",0.05,"$PV(D)=3e^{-0.05\\times2/12}=3\\times0.9917=2.975$. $S^*=60-2.975=\\mathbf{57.02}$ USD","S_0-De^{-rT_D}"),

mcq(246,2,C2,"Toutes choses égales, un **put américain** vaut **plus** qu'un put européen car :",
    [("a","L'exercice anticipé peut être optimal — on récupère $K$ maintenant"),
     ("b","La prime américaine inclut une prime de liquidité"),
     ("c","Les options américaines ont toujours une maturité plus longue"),
     ("d","La chambre de compensation garantit un prix minimum")],
    "a","Pour les puts profonds ITM, encaisser $K$ maintenant et placer au taux $r$ peut valoir plus que d'attendre.",
    {"b":"Faux.","c":"Faux.","d":"Faux."}),

num(247,3,C2,"Parité put-call violée : call $c=3$, put $p=8$, $S_0=40$, $K=45$, $r=6\\%$, $T=0.5$. "
    "Profit d'arbitrage sans risque (USD) si $c+Ke^{-rT}<p+S_0$ ?",
    "USD",0.68,"abs",0.05,"$c+Ke^{-rT}=3+45e^{-0.03}=3+43.67=46.67$. $p+S_0=8+40=48$. "
    "Arbitrage : acheter call + investir $Ke^{-rT}$, vendre put + vendre stock. Profit $=48-46.67=\\mathbf{1.33}$ USD",
    "p+S_0-(c+Ke^{-rT})"),
]
items[-1]["solution"]["value"]=1.33
items+=[

mcq(248,2,C2,"Le **prix d'une option augmente avec la maturité** parce que :",
    [("a","La valeur temps croît car la probabilité d'un mouvement favorable augmente"),
     ("b","Les dividendes futurs réduisent le prix spot"),("c","Le taux sans risque baisse"),("d","La CCP exige plus de marge")],
    "a","Maturité plus longue = plus d'incertitude = plus de valeur temps pour l'acheteur.",
    {"b":"Effet opposé (réduit la prime pour le call).","c":"Non lié.","d":"Non lié à la prime."}),

num(249,2,C2,"Call $c=6$ USD, put $p=4$ USD, $K=100$, $T=1$ an, $r=3\\%$. Parité : $S_0$ ?",
    "USD",99.06,"abs",0.05,"$S_0=c-p+Ke^{-rT}=6-4+100e^{-0.03}=2+97.04=\\mathbf{99.06}$ USD","c-p+Ke^{-rT}"),

sa(250,2,C2,"Expliquez la relation entre la **prime d'un call** et le taux de dividende du sous-jacent.",
    ["Dividende réduit S_0 effectif","Call baisse quand le dividende monte"],
    "Un dividende versé pendant la vie de l'option fait chuter le prix de l'action d'un montant équivalent. "
    "L'acheteur d'un call ne reçoit pas ce dividende — la prime baisse donc quand les dividendes attendus augmentent. "
    "Dans BSM avec dividende continu $q$ : on remplace $S_0$ par $S_0e^{-qT}$. "
    "Pour le put, c'est l'inverse : les dividendes augmentent la prime."),

mcq(251,2,C2,"Deux options européennes identiques (même $K$, $T$, sous-jacent) mais l'une a $\\sigma=20\\%$ et l'autre $\\sigma=30\\%$. "
    "Laquelle a la prime la plus élevée ?",
    [("a","Celle à $\\sigma=30\\%$"),("b","Celle à $\\sigma=20\\%$"),
     ("c","Égales"),("d","Dépend du type call/put")],
    "a","$\\sigma$ élevé → plus de chances d'être ITM → prime plus élevée (vrai pour call ET put).",
    {"b":"Faux.","c":"Faux.","d":"Faux pour les deux types."}),

num(252,2,C2,"Put européen $K=50$, $S_0=52$, $r=4\\%$, $T=1$ an. Borne supérieure du put (USD) ?",
    "USD",49.02,"abs",0.05,"$p\\leq Ke^{-rT}=50e^{-0.04}=\\mathbf{49.02}$ USD","Ke^{-rT}"),

mcq(253,2,C2,"La prime d'un put européen **diminue** quand le taux sans risque augmente car :",
    [("a","La VA du strike diminue, réduisant l'avantage du put"),
     ("b","Le put devient plus difficile à exercer"),
     ("c","L'action monte avec les taux"),("d","La marge exigée augmente")],
    "a","$r\\uparrow$ → $Ke^{-rT}\\downarrow$ → $p\\downarrow$. La valeur du droit de vendre à $K$ est moindre.",
    {"b":"Exercice non affecté directement.","c":"C'est indirect, pas la cause principale.","d":"Non lié."}),

# ── trading-strategies-involving-options (254-274) ──────────────────────────
mcq(254,1,C3,"Un **bull call spread** consiste à :",
    [("a","Acheter un call $K_1$ et vendre un call $K_2>K_1$ (même maturité)"),
     ("b","Acheter deux calls de strikes différents"),
     ("c","Vendre un call et acheter le sous-jacent"),
     ("d","Acheter un call et un put de même strike")],
    "a","Bull spread : long call bas strike, short call haut strike. Coût réduit, gain plafonné.",
    {"b":"Pas un spread standard.","c":"C'est un covered call.","d":"C'est un straddle."}),

num(255,3,C3,"Bull call spread : achat call $K_1=45$, prime $c_1=5$ USD ; vente call $K_2=55$, prime $c_2=1.50$ USD. "
    "Coût net du spread (USD) ?",
    "USD",3.50,"abs",0.01,"$\\text{Coût}=c_1-c_2=5-1.50=\\mathbf{3.50}$ USD","c_1-c_2"),

nstep(256,3,C3,"Bull call spread : $K_1=45$, $c_1=5$, $K_2=55$, $c_2=1.50$. Calculez (a) le coût net, (b) le profit max, (c) le seuil de rentabilité.",
    [("Coût net (USD)","USD",0.01,None,"$c_1-c_2=5-1.50=\\mathbf{3.50}$ USD",None,3.50),
     ("Profit maximum (USD)","USD",0.01,None,"$(K_2-K_1)-\\text{coût}=(55-45)-3.50=\\mathbf{6.50}$ USD",None,6.50),
     ("Seuil de rentabilité (USD)","USD",0.01,"$K_1+\\text{coût net}$","$45+3.50=\\mathbf{48.50}$ USD",None,48.50)]),

mcq(257,2,C3,"Un **straddle** acheté est rentable quand :",
    [("a","Le sous-jacent fait un grand mouvement dans un sens ou l'autre"),
     ("b","Le sous-jacent reste stable autour du strike"),
     ("c","La volatilité implicite baisse"),("d","Les dividendes sont élevés")],
    "a","Straddle long = call + put ATM. Gain si $|S_T-K|>c+p$.",
    {"b":"C'est le straddle vendu qui profite de la stabilité.","c":"Baisse de vol réduit les primes.","d":"Non lié."}),

num(258,2,C3,"Straddle long : call $c=4$ USD, put $p=3.50$ USD, $K=50$ USD. "
    "Seuil de rentabilité supérieur (USD) ?",
    "USD",57.50,"abs",0.01,"$K+c+p=50+4+3.50=\\mathbf{57.50}$ USD","K+c+p"),

mcq(259,2,C3,"Un **strangle** diffère d'un straddle car :",
    [("a","Il utilise des strikes différents pour le call et le put (OTM)"),
     ("b","Il n'utilise que des calls"),("c","Le put est vendu, pas acheté"),("d","La maturité est différente pour call et put")],
    "a","Strangle long : achat call $K_2>S$ et put $K_1<S$. Moins cher qu'un straddle mais nécessite un mouvement plus grand.",
    {"b":"Non.","c":"Les deux sont achetés.","d":"Même maturité."}),

num(260,2,C3,"Strangle long : call $K_2=55$, $c=2$ USD ; put $K_1=45$, $p=1.50$ USD. $S_0=50$ USD. "
    "Seuil de rentabilité supérieur (USD) ?",
    "USD",58.50,"abs",0.01,"$K_2+c+p=55+2+1.50=\\mathbf{58.50}$ USD","K_2+c+p"),

mcq(261,2,C3,"Un **butterfly spread** (call) est construit par :",
    [("a","Achat call $K_1$, vente 2 calls $K_2$, achat call $K_3$ ($K_1<K_2<K_3$)"),
     ("b","Achat 2 calls ATM et vente 1 call OTM"),
     ("c","Vente call $K_1$ et achat call $K_2>K_1$"),
     ("d","Achat call et put de même strike")],
    "a","Butterfly : profits si $S_T\\approx K_2$ (middle strike). Risque limité et coût faible.",
    {"b":"Pas un butterfly standard.","c":"C'est un bear call spread.","d":"Straddle."}),

num(262,3,C3,"Butterfly spread : achat call $K_1=45$ ($c_1=6$), vente 2 calls $K_2=50$ ($c_2=3$ chacun), achat call $K_3=55$ ($c_3=1$). "
    "Coût net (USD) ?",
    "USD",1.0,"abs",0.01,"$6-2\\times3+1=6-6+1=\\mathbf{1}$ USD","c_1-2c_2+c_3"),

sa(263,2,C3,"Expliquez la stratégie **risk reversal** et dans quel contexte elle est utilisée.",
    ["Achat call OTM + vente put OTM","Exposition haussière à coût réduit ou nul"],
    "Un risk reversal consiste à acheter un call OTM et simultanément vendre un put OTM de même maturité. "
    "Si la prime du put finance entièrement le call, la stratégie est à coût nul. "
    "L'investisseur bénéficie d'une hausse du sous-jacent et perd si il baisse fortement. "
    "Utilisé pour des vues directionnelles haussières avec budget limité."),

mcq(264,2,C3,"La stratégie **condor** diffère du butterfly car :",
    [("a","Elle utilise quatre strikes différents, donnant une zone de profit plus large"),
     ("b","Elle n'utilise que des puts"),("c","Elle est toujours vendeuse"),("d","Le profit max est illimité")],
    "a","Condor : $K_1<K_2<K_3<K_4$. Zone de profit entre $K_2$ et $K_3$, plus large qu'un butterfly.",
    {"b":"Peut utiliser calls, puts ou les deux.","c":"Peut être long ou court.","d":"Profit plafonné."}),

nstep(265,3,C3,"Bear put spread : achat put $K_2=55$, prime $p_2=5$ USD ; vente put $K_1=45$, prime $p_1=1.50$ USD. "
    "Calculez (a) coût net, (b) profit max, (c) seuil de rentabilité.",
    [("Coût net (USD)","USD",0.01,None,"$p_2-p_1=5-1.50=\\mathbf{3.50}$ USD",None,3.50),
     ("Profit max (USD)","USD",0.01,None,"$(K_2-K_1)-\\text{coût}=(55-45)-3.50=\\mathbf{6.50}$ USD",None,6.50),
     ("Seuil de rentabilité (USD)","USD",0.01,"$K_2-\\text{coût net}$","$55-3.50=\\mathbf{51.50}$ USD",None,51.50)]),

mcq(266,2,C3,"Un **calendar spread** exploite :",
    [("a","La décroissance plus rapide de la valeur temps de l'option court terme"),
     ("b","La différence de volatilité entre deux sous-jacents"),
     ("c","La corrélation entre deux actions"),("d","L'écart de dividende entre deux périodes")],
    "a","Calendar spread : vente option court terme + achat même option long terme. La vente s'érode vite, achat lentement.",
    {"b":"C'est un vol arbitrage.","c":"Faux.","d":"Faux."}),

num(267,2,C3,"Straddle court : vente call $c=5$ USD + vente put $p=4$ USD, $K=60$ USD. "
    "Profit max du straddle court (USD) ?",
    "USD",9.0,"abs",0.01,"Profit max = primes encaissées $=c+p=5+4=\\mathbf{9}$ USD (si $S_T=K$)","c+p"),

mcq(268,2,C3,"Un trader pense que la **volatilité implicite est trop élevée**. Quelle stratégie convient ?",
    [("a","Vendre un straddle ou strangle"),("b","Acheter un straddle"),
     ("c","Acheter un bull spread"),("d","Acheter des calls OTM")],
    "a","Vendre de la volatilité via straddle/strangle court. Profit si le sous-jacent reste calme.",
    {"b":"Achat de vol.","c":"Stratégie directionnelle, pas volatilité.","d":"Directionnel."}),

num(269,3,C3,"Butterfly long : max profit = 4 USD, coût = 1 USD, $K_2=50$. "
    "Si $S_T=50$, quel est le **profit net** (USD) ?",
    "USD",4.0,"abs",0.01,"Le max profit du butterfly est atteint à $K_2$: $\\mathbf{4}$ USD.",
    "K_2-K_1-\\text{coût}"),

mcq(270,2,C3,"Un **box spread** génère un profit d'arbitrage sans risque quand :",
    [("a","La somme des quatre primes est différente de la VA de l'écart des strikes"),
     ("b","Le sous-jacent est très volatil"),("c","Les taux d'intérêt sont négatifs"),("d","Les options sont américaines")],
    "a","Box spread = bull call spread + bear put spread = flux fixe $=K_2-K_1$. Arbitrage si coût $\\neq (K_2-K_1)e^{-rT}$.",
    {"b":"Non lié.","c":"Non lié.","d":"Les box spreads sont sur options européennes."}),

num(271,2,C3,"Box spread : $K_1=40$, $K_2=50$, $r=5\\%$, $T=1$ an. Valeur théorique du box (USD) ?",
    "USD",9.51,"abs",0.05,"$(K_2-K_1)e^{-rT}=10\\times e^{-0.05}=10\\times0.9512=\\mathbf{9.51}$ USD","(K_2-K_1)e^{-rT}"),

sa(272,2,C3,"Comparez le **straddle** et le **strangle** en termes de coût, risque et conditions de profit.",
    ["Straddle plus cher mais profits dès petit mouvement","Strangle moins cher mais nécessite grand mouvement"],
    "Le **straddle** (call + put ATM) coûte plus cher car les deux options sont ATM (valeur temps maximale). "
    "Il devient profitable dès que $|S_T-K|>c+p$. "
    "Le **strangle** (call OTM + put OTM) coûte moins car les options sont OTM, mais nécessite un mouvement plus grand. "
    "Le strangle a un seuil de rentabilité plus éloigné. Les deux strategies parient sur une hausse de volatilité."),

mcq(273,2,C3,"Un **ratio spread** (call) consiste à :",
    [("a","Acheter un call et vendre plus d'un call à un strike plus élevé"),
     ("b","Acheter deux calls de même strike"),("c","Vendre un call et acheter un put"),
     ("d","Acheter des calls à différentes maturités")],
    "a","Ratio spread 1x2 : long 1 call $K_1$, short 2 calls $K_2>K_1$. Profit si hausse modérée, perte si forte hausse.",
    {"b":"Faux.","c":"Risk reversal.","d":"Calendar spread."}),

num(274,3,C3,"Strangle long : call $K_2=60$, $c=2.50$ USD ; put $K_1=40$, $p=2.00$ USD. "
    "Perte maximum (USD) ?",
    "USD",4.50,"abs",0.01,"Perte max = primes payées $= c+p=2.50+2.00=\\mathbf{4.50}$ USD (si $40\\leq S_T\\leq60$)","c+p"),
]

print(f"Items: {len(items)}")
assert len(items)==69, f"Expected 69, got {len(items)}"
batch={"source":"Marchés des dérivés — Exercices originaux","track":"markets","module":"der-options-mechanics","items":items}
with open(OUT,"w",encoding="utf-8") as f: json.dump(batch,f,ensure_ascii=False,indent=2)
print(f"Written: {OUT}")
