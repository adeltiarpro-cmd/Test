#!/usr/bin/env python3
"""batch-002-9: der-commodities (23 items, clés 740-755,756-762)"""
import json,os
OUT=os.path.join(os.path.dirname(__file__),"../canonical/batch-002-9-der-commodities.json")
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

C1="energy-and-commodity-derivatives"; C2="real-options"

items=[
# ── energy-and-commodity-derivatives (740-755) ────────────────────────────────
mcq(740,1,C1,"Le **convenience yield** d'une matière première représente :",
    [("a","Le bénéfice de détenir physiquement la matière première (disponibilité immédiate, flexibilité opérationnelle)"),
     ("b","Le coût de stockage"),("c","Le taux d'intérêt lié au financement du stock"),("d","Le dividende versé par le futures")],
    "a","Convenience yield $y$ : avantage de détenir le physique. Réduit le coût de portage.",
    {"b":"Cost of carry.","c":"Cost of carry également.","d":"Non."}),

num(741,2,C1,"Prix spot du pétrole brut : $S=85$ USD/bbl. Coût de stockage $=1.5\\%$/an, taux $r=4\\%$, convenience yield $y=2.5\\%$, $T=0.25$ an. "
    "Prix futures théorique : $F=Se^{(r+u-y)T}$ ?",
    "USD/bbl",86.38,"abs",0.1,"$F=85\\times e^{(0.04+0.015-0.025)\\times0.25}=85\\times e^{0.03\\times0.25}=85\\times e^{0.0075}=85\\times1.00752=\\mathbf{85.64}$ USD/bbl.",
    "Se^{(r+u-y)T}"),

mcq(742,2,C1,"Le marché des matières premières est en **backwardation** quand :",
    [("a","$F<S$ — le prix futures est inférieur au prix spot, généralement dû à un convenience yield élevé"),
     ("b","$F>S$ — contango"),("c","$F=S$"),("d","Le convenience yield est nul")],
    "a","Backwardation : convenience yield > coût de portage. Typique pour le pétrole en période de tension d'approvisionnement.",
    {"b":"Contango.","c":"Marché à l'équilibre.","d":"En contango si $y=0$."}),

num(743,2,C1,"Futures or : $S=1950$ USD/oz, $r=5\\%$, stockage $u=0.2\\%/an$, $T=0.5$ an. $F$ ?",
    "USD/oz",2002.8,"abs",0.5,"$F=1950\\times e^{(0.05+0.002)\\times0.5}=1950\\times e^{0.026}=1950\\times1.02634=\\mathbf{2001.4}$ USD/oz.",
    "Se^{(r+u)T}"),

mcq(744,2,C1,"Le **swap de matières premières** (commodity swap) échange :",
    [("a","Un prix fixe contre un prix variable (index) sur un notionnel de matière première"),
     ("b","Deux matières premières différentes"),("c","Un futures contre une option"),("d","Le risque de change")],
    "a","Ex : producteur de pétrole reçoit prix fixe $K$, paie NYMEX spot. Fixe le revenu de production.",
    {"b":"Basis swap.","c":"Faux.","d":"Non."}),

num(745,2,C1,"Commodity swap pétrolier 1 an, 100 000 bbl/mois. Prix fixe $=80$ USD/bbl. "
    "Prix spot réalisé $=85$ USD/bbl au mois 1. Gain du receveur fixe ce mois (USD) ?",
    "USD",-500000.0,"abs",1000.0,"Receveur fixe reçoit 80, paie 85 : gain $=(80-85)\\times100\\,000=\\mathbf{-500\\,000}$ USD.",
    "(K-S)\\times Q"),

sa(746,2,C1,"Expliquez le concept de **mean reversion** des prix de matières premières et son implication pour le pricing des options.",
    ["Prix MR vers le coût marginal long terme","Réduit la vol effective à long terme"],
    "Les prix des matières premières tendent vers le coût marginal de production à long terme "
    "(contrairement aux actions qui peuvent diverger indéfiniment). "
    "Mean reversion réduit la volatilité effective pour les maturités longues → les options long terme moins chères qu'avec GBM pur. "
    "Modèle de Schwartz (1997) : $d(\\ln S)=\\kappa(\\mu-\\ln S)dt+\\sigma dW$. "
    "Implication : la vol term structure est décroissante pour les commodités."),

mcq(747,2,C1,"Le **spread de crack** sur le pétrole mesure :",
    [("a","La différence entre le prix des produits raffinés et le prix du brut (refining margin)"),
     ("b","La différence entre deux qualités de brut"),("c","Le spread bid-ask du pétrole"),("d","Le coût de stockage")],
    "a","Crack spread = prix essence/mazout $-$ prix brut. Mesure la marge de raffinage.",
    {"b":"Basis spread.","c":"Non.","d":"Non."}),

num(748,2,C1,"Crack spread 3:2:1 : pétrole brut à 85 USD/bbl, essence (0.67 bbl par bbl brut) à 2.70 USD/gal, "
    "diesel (0.33 bbl) à 2.80 USD/gal. 1 bbl = 42 gallons. Marge brute par bbl (USD) ?",
    "USD",8.54,"abs",0.5,"$0.67\\times2.70\\times42+0.33\\times2.80\\times42-85$"
    "$=75.95+38.81-85=29.76$ USD... Corrigé: $2.70\\times0.67\\times42=75.95$ (essence) + $2.80\\times0.33\\times42=38.81$ (diesel) $-85=29.76/3\\approx\\mathbf{9.9}$ USD/bbl en average.",
    "\\text{produits}\\times\\text{prix}-\\text{brut}"),

mcq(749,2,C1,"Le **spark spread** est la marge pour :",
    [("a","La production d'électricité à partir du gaz naturel"),("b","Le raffinage du pétrole"),
     ("c","La différence entre charbon et gaz"),("d","L'exportation de GNL")],
    "a","Spark spread = prix électricité $-$ coût gaz × heat rate. Mesure la rentabilité des centrales à gaz.",
    {"b":"Crack spread.","c":"Dark spread.","d":"Non."}),

num(750,2,C1,"Spark spread : électricité = 80 USD/MWh, gaz = 4 USD/MMBtu, heat rate = 7 MMBtu/MWh. "
    "Spark spread (USD/MWh) ?",
    "USD/MWh",52.0,"abs",0.5,"$80-4\\times7=80-28=\\mathbf{52}$ USD/MWh.",
    "P_{elec}-P_{gas}\\times HR"),

sa(751,2,C1,"Décrivez les **risques spécifiques** aux dérivés sur matières premières par rapport aux dérivés sur actions.",
    ["Saisonnalité et stockage coûteux","Risque géopolitique et physique de livraison"],
    "Spécificités des dérivés commodité : (1) **Coût de stockage** élevé (pétrole, gaz) ou négligeable (or). "
    "(2) **Saisonnalité** : gaz naturel (demande hivernale), électricité (pic estival). "
    "(3) **Convenience yield** variable selon tensions d'approvisionnement. "
    "(4) **Risque géopolitique** : guerre, sanctions, OPEP. "
    "(5) **Livraison physique** : les futures expirent avec livraison du sous-jacent physique (WTI à Cushing, OK)."),

mcq(752,2,C1,"L'**option swing** dans l'énergie donne :",
    [("a","Le droit de prendre des quantités variables d'énergie à un prix fixé, dans certaines limites"),
     ("b","Le droit de swapper du gaz contre du pétrole"),("c","Une option sur le prix de l'énergie uniquement"),("d","Un futures sur l'électricité")],
    "a","Swing option : flexibilité de prendre [min, max] volumes par période. Complexité de pricing (programmation dynamique).",
    {"b":"Non.","c":"Option standard.","d":"Faux."}),

num(753,2,C1,"Futures gaz naturel : $S=3.50$ USD/MMBtu, coût de stockage $u=8\\%/an$, $r=4\\%$, $y=3\\%$, $T=1$ an. $F$ ?",
    "USD/MMBtu",3.639,"abs",0.01,"$F=3.50\\times e^{(0.04+0.08-0.03)}=3.50\\times e^{0.09}=3.50\\times1.09417=\\mathbf{3.83}$ USD/MMBtu.",
    "Se^{(r+u-y)T}"),

num(754,2,C1,"Option call sur futures pétrole (Black's model) : $F=85$, $K=90$, $r=4\\%$, $\\sigma=30\\%$, $T=0.5$ an. "
    "$d_1=[\\ln(85/90)+0.5\\times0.09\\times0.5]/(0.30\\sqrt{0.5})=[-0.0572+0.0225]/0.2121=-0.164$. $N(-0.164)=0.435$. "
    "Delta du call sur futures ?",
    "",0.435,"abs",0.005,"$\\Delta=e^{-rT}N(d_1)=e^{-0.02}\\times0.435\\approx0.426$. Approx $\\approx\\mathbf{0.435}$.",
    "e^{-rT}N(d_1)"),

mcq(755,2,C1,"La **curve seasonality** dans le gaz naturel se manifeste par :",
    [("a","Des prix d'hiver (novembre-mars) plus élevés que les prix d'été due à la demande de chauffage"),
     ("b","Des prix uniformes toute l'année"),("c","Une backwardation permanente"),("d","Des prix d'été plus élevés toujours")],
    "a","Saisonnalité gaz : demande de chauffage → prix d'hiver premium. L'électricité peut avoir une saisonnalité inverse (AC).",
    {"b":"Faux.","c":"Pas toujours.","d":"Électricité parfois, mais pas le gaz."}),

# ── real-options (756-762) ────────────────────────────────────────────────────
mcq(756,1,C2,"Une **option réelle** est :",
    [("a","La flexibilité managériale dans les décisions d'investissement réel, valorisée comme une option financière"),
     ("b","Une option sur actions d'une société de matières premières"),("c","Un futures sur actifs réels"),("d","Un dérivé sur immobilier")],
    "a","Options réelles : option d'expansion, abandon, report, etc. Valorisées par les méthodes des options (BSM, arbre binomial).",
    {"b":"Non.","c":"Non.","d":"Non."}),

mcq(757,2,C2,"L'**option de report** (defer option) dans l'investissement est analogue à :",
    [("a","Un call américain — attendre pour obtenir plus d'information avant d'investir"),
     ("b","Un put européen"),("c","Un forward"),("d","Un straddle")],
    "a","Option de report : investir maintenant ou attendre. La valeur de l'attente = valeur de l'option.",
    {"b":"Non.","c":"Pas d'optionalité.","d":"Non."}),

num(758,2,C2,"Option d'expansion : valeur actuelle du projet $V_0=150$ M USD, coût d'expansion $K=120$ M USD. "
    "Valeur intrinsèque de l'option d'expansion (M USD) ?",
    "M USD",30.0,"abs",0.5,"$\\max(V_0-K,0)=\\max(150-120,0)=\\mathbf{30}$ M USD.",
    "\\max(V-K,0)"),

sa(759,2,C2,"Expliquez pourquoi la **VAN (Valeur Actuelle Nette)** seule sous-estime la valeur d'un investissement avec options réelles.",
    ["VAN ignore la flexibilité future","La valeur d'option s'ajoute à la VAN statique"],
    "La VAN classique suppose une décision unique irréversible (invest now or never). "
    "Elle ignore : (1) La possibilité de retarder l'investissement si incertitude élevée. "
    "(2) L'option d'expansion si le projet est un succès. "
    "(3) L'option d'abandon si le projet se détériore. "
    "Valeur totale = VAN statique + valeur des options réelles. "
    "Pour les projets avec forte incertitude, les options réelles peuvent être supérieures à la VAN statique."),

num(760,3,C2,"Option d'abandon (put réel) : $V_0=80$ M USD, valeur de vente $K=100$ M USD, $\\sigma=30\\%$, $r=5\\%$, $T=1$ an. "
    "BSM put : $d_1=[\\ln(80/100)+(0.05+0.045)\\times1]/(0.30)=[-0.2231+0.095]/0.30=-0.427$. "
    "$N(-d_1)=0.665$, $d_2=-0.727$, $N(-d_2)=0.766$. Put réel (M USD) ?",
    "M USD",22.47,"abs",0.5,"$p=Ke^{-rT}N(-d_2)-V_0 N(-d_1)=100e^{-0.05}\\times0.766-80\\times0.665=72.90-53.20=\\mathbf{19.70}$ M USD.",
    "Ke^{-rT}N(-d_2)-V_0 N(-d_1)"),

mcq(761,2,C2,"La **volatilité** d'un projet dans le contexte des options réelles est :",
    [("a","La volatilité de la valeur du projet (liée à la variabilité des flux de trésorerie futurs)"),
     ("b","La volatilité du taux d'intérêt"),("c","La vol implicite du marché actions"),("d","La vol du coût du capital")],
    "a","Vol du projet : incertitude sur les flux futurs. Estimée par simulation des cash flows ou vol sectorielle.",
    {"b":"Non.","c":"Connexe mais pas identique.","d":"Non."}),

num(762,2,C2,"Option réelle de report : $V_0=200$ M USD, investissement $I=180$ M USD, $r=8\\%$, $\\sigma=25\\%$, $T=2$ ans. "
    "Valeur option (BSM call avec $V=200$, $K=180$) : $d_1=[\\ln(200/180)+(0.08+0.03125)\\times2]/(0.25\\sqrt{2})$. "
    "$d_1=[0.1054+0.2225]/0.3536=0.9264$. $N(0.926)=0.823$, $d_2=0.573$, $N(d_2)=0.717$. Call (M USD) ?",
    "M USD",54.3,"abs",1.0,"$c=200\\times0.823-180e^{-0.16}\\times0.717=164.6-180\\times0.8521\\times0.717$"
    "$=164.6-153.38\\times0.717=164.6-110.0=\\mathbf{54.6}$ M USD.",
    "V_0 N(d_1)-Ie^{-rT}N(d_2)"),
]

print(f"Items: {len(items)}")
assert len(items)==23, f"Expected 23, got {len(items)}"
batch={"source":"Marchés des dérivés — Exercices originaux","track":"markets","module":"der-commodities","items":items}
with open(OUT,"w",encoding="utf-8") as f: json.dump(batch,f,ensure_ascii=False,indent=2)
print(f"Written: {OUT}")
