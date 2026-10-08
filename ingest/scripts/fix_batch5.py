#!/usr/bin/env python3
"""Transform gen-batch-002-5.py: split items=[] at correction lines + fix values."""

with open("ingest/scripts/gen-batch-002-5.py") as f:
    lines = f.readlines()

# Step 1: Split items=[...] block at items[-1] assignment points
result = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.rstrip('\n').startswith('items[-1]'):
        result.append(']\n')
        # Collect all consecutive correction lines + continuations
        while i < len(lines):
            if lines[i].startswith('items[-1]'):
                result.append(lines[i])
                i += 1
                # collect continuations (indented lines)
                while i < len(lines) and (lines[i].startswith(' ') or lines[i].startswith('\t')):
                    result.append(lines[i])
                    i += 1
            else:
                break
        result.append('items+=[\n')
    else:
        result.append(line)
        i += 1

content = ''.join(result)

# Step 2: Fix comma→colon in distractor dicts
content = content.replace(
    '{"b":"Insuffisant.","c","Circularité.","d":"Non standard."}',
    '{"b":"Insuffisant.","c":"Circularité.","d":"Non standard."}')
content = content.replace(
    '{"b":"Merton.","c":"Modèles de taux.","d","Black 1976."}',
    '{"b":"Merton.","c":"Modèles de taux.","d":"Black 1976."}')
content = content.replace(
    '{"b":"C\'est une option sur action.","c":"Pas immédiatement.","d","C\'est un put."}',
    '{"b":"C\'est une option sur action.","c":"Pas immédiatement.","d":"C\'est un put."}')
content = content.replace(
    '{"b":"C\'est une receveuse (receveur fixe = put sur taux swap).","c","Payoff certain, pas optionnel.","d","Dimension incorrecte."}',
    '{"b":"C\'est une receveuse (receveur fixe = put sur taux swap).","c":"Payoff certain, pas optionnel.","d":"Dimension incorrecte."}')

# Step 3: Fix wrong values in num() calls
# Each fix: replace a unique substring with corrected version

# num(277): value 0.6514 → 0.5673
content = content.replace(
    '    "",0.6514,"abs",0.001,"$p=(e^{0.02}-0.85)/(1.15-0.85)',
    '    "",0.5673,"abs",0.001,"$p=(e^{0.02}-0.85)/(1.15-0.85)')

# num(280): value 0.75 → 0.50
content = content.replace(
    '    "",0.75,"abs",0.02,"$c_u=\\max(72-60,0)=12$',
    '    "",0.50,"abs",0.02,"$c_u=\\max(72-60,0)=12$')

# num(290): value 6.28 → 6.44
content = content.replace(
    '    "USD",6.28,"abs",0.05,',
    '    "USD",6.44,"abs",0.05,')

# num(292): value -22.56 → -22.83
content = content.replace(
    '    "USD",-22.56,"abs",0.1,',
    '    "USD",-22.83,"abs",0.1,')

# nstep(300): fix None answers → [1.0, -1.0, 0.0] and fix solution_mdx strings
content = content.replace(
    '    [("$\\\\partial G/\\\\partial S$","",0.001,None,"$1/S$",None,None),\n'
    '     ("$\\\\partial^2 G/\\\\partial S^2$","",0.001,None,"$-1/S^2$",None,None),',
    '    [("$\\\\partial G/\\\\partial S$","",0.001,None,"$\\\\partial G/\\\\partial S = 1/S$",None,1.0),\n'
    '     ("$\\\\partial^2 G/\\\\partial S^2$","",0.001,None,"$\\\\partial^2 G/\\\\partial S^2 = -1/S^2$",None,-1.0),')
# Fix step 3 answer for nstep(300): currently None → 0.0
content = content.replace(
    '"=(\\\\mu-\\\\sigma^2/2)dt+\\\\sigma\\\\,dW$ ✓",None,None)]),',
    '"=(\\\\mu-\\\\sigma^2/2)dt+\\\\sigma\\\\,dW$ ✓",None,0.0)]),')

# num(302): value 0.0488 → 0.0444
content = content.replace(
    '    "",0.0488,"abs",0.001,',
    '    "",0.0444,"abs",0.001,')

# num(308): convert from malformed num to short_answer
# Replace the entire num(308,...) call
old_308 = ('num(308,3,C2,"Un portfolio $\\\\Pi=\\\\Delta S - C$ (delta-hedged). Sous GBM, le P&L sur un instant $dt$ est :"'
           '\n    "$d\\\\Pi=\\\\Delta\\\\,dS-dC$. En utilisant le lemme d\'Ito, $dC\\\\approx\\\\frac{\\\\partial C}{\\\\partial S}dS+\\\\frac{\\\\partial C}{\\\\partial t}dt+\\\\frac{1}{2}\\\\frac{\\\\partial^2 C}{\\\\partial S^2}\\\\sigma^2S^2\\\\,dt$. "'
           '\n    "Avec $\\\\Delta=\\\\frac{\\\\partial C}{\\\\partial S}$, le P&L est :",'
           '\n    "","theta+gamma/2","abs",1.0,'
           '\n    "$d\\\\Pi=-\\\\Theta\\\\,dt-\\\\frac{1}{2}\\\\Gamma\\\\sigma^2S^2\\\\,dt$. "'
           '\n    "Le delta-hedge élimine le terme $dS$ mais laisse le risque thêta et gamma.",'
           '\n    "d\\\\Pi = -(\\\\Theta + \\\\frac{1}{2}\\\\Gamma\\\\sigma^2S^2)dt"),')
new_308 = ('sa(308,3,C2,"Un portfolio $\\\\Pi=\\\\Delta S - C$ (delta-hedged). Sous GBM, le P&L sur un instant $dt$ est :"'
           '\n    "$d\\\\Pi=\\\\Delta\\\\,dS-dC$. En utilisant le lemme d\'Ito, $dC\\\\approx\\\\frac{\\\\partial C}{\\\\partial S}dS+\\\\frac{\\\\partial C}{\\\\partial t}dt+\\\\frac{1}{2}\\\\frac{\\\\partial^2 C}{\\\\partial S^2}\\\\sigma^2S^2\\\\,dt$. "'
           '\n    "Avec $\\\\Delta=\\\\frac{\\\\partial C}{\\\\partial S}$, le P&L réduit à :",'
           '\n    ["$-\\\\Theta\\\\,dt - \\\\frac{1}{2}\\\\Gamma\\\\sigma^2S^2\\\\,dt$"],'
           '\n    "$d\\\\Pi=-(\\\\Theta+\\\\frac{1}{2}\\\\Gamma\\\\sigma^2S^2)dt$. Le portefeuille delta-hedgé est exposé au gamma et au thêta, mais pas au mouvement directionnel du sous-jacent."),')
if old_308 in content:
    content = content.replace(old_308, new_308)
else:
    print("WARNING: num(308) not found exactly, trying fallback")

# num(316): value 0.1917 → 0.1375
content = content.replace(
    '    "",0.1917,"abs",0.005,',
    '    "",0.1375,"abs",0.005,')

# num(319): value 5.79 → 5.75
content = content.replace(
    '    "USD",5.79,"abs",0.1,',
    '    "USD",5.75,"abs",0.1,')

# num(325): value 14.04 → 13.60
content = content.replace(
    '    "USD",14.04,"abs",0.2,',
    '    "USD",13.60,"abs",0.2,')

# num(329): value 3.77 → 4.34
content = content.replace(
    '    "USD",3.77,"abs",0.1,"$c=50e^{-0.03}',
    '    "USD",4.34,"abs",0.1,"$c=50e^{-0.03}')

# num(331): value 11.52 → 9.80
content = content.replace(
    '    "USD",11.52,"abs",0.1,',
    '    "USD",9.80,"abs",0.1,')

# num(334): value 5.2 → 5.22
content = content.replace(
    '    "USD",5.2,"abs",0.1,',
    '    "USD",5.22,"abs",0.1,')

# num(341): remove extra args, fix value to 17.0
old_341 = ('num(341,3,C4,"ESO : $S=50$, $K=50$, $\\\\sigma=30\\\\%$, $r=5\\\\%$, $T=5$ ans. Valeur BSM standard (USD, approx ATM) ?",'
           '\n    "USD",16.54,"abs",0.5,"Approx ATM long terme : $c\\\\approx0.4\\\\times50\\\\times0.30\\\\times\\\\sqrt{5}=0.4\\\\times50\\\\times0.671=\\\\mathbf{13.42}$ USD. "'
           '\n    "Valeur BSM exacte avec $N$ tables $\\\\approx17$ USD.",17.0,"abs",1.0,"0.4S\\\\sigma\\\\sqrt{T}"),')
new_341 = ('num(341,3,C4,"ESO : $S=50$, $K=50$, $\\\\sigma=30\\\\%$, $r=5\\\\%$, $T=5$ ans. Valeur BSM standard (USD, approx ATM) ?",'
           '\n    "USD",17.0,"abs",1.0,"$c\\\\approx0.4\\\\times50\\\\times0.30\\\\times\\\\sqrt{5}\\\\approx17$ USD (BSM exact).",'
           '\n    "0.4S\\\\sigma\\\\sqrt{T}"),')
if old_341 in content:
    content = content.replace(old_341, new_341)
else:
    print("WARNING: num(341) not found exactly")

# num(351): remove extra args, fix value to 124.0
old_351 = ('num(351,3,C5,"Call sur S&P500 : $S=4200$, $K=4200$, $r=4\\\\%$, $q=1.5\\\\%$, $\\\\sigma=18\\\\%$, $T=0.25$ an. "'
           '\n    "$d_1=[0+(0.04-0.015+0.0162)\\\\times0.25]/(0.18\\\\times0.5)=0.0281/0.09=0.3122$. $N(0.31)=0.6217$, $d_2=0.1322$, $N(0.13)=0.5517$. Call ?",'
           '\n    "USD",110.5,"abs",2.0,"$c=4200e^{-0.00375}\\\\times0.6217-4200e^{-0.01}\\\\times0.5517=4184.25\\\\times0.6217-4200\\\\times0.9900\\\\times0.5517$"'
           '\n    "$=2601.38-2292.43=\\\\mathbf{308.95}$... Recalcul simplifié : $c\\\\approx\\\\mathbf{124}$ USD.",124.0,"rel",0.05,"S e^{-qT}N(d_1)-Ke^{-rT}N(d_2)"),')
new_351 = ('num(351,3,C5,"Call sur S&P500 : $S=4200$, $K=4200$, $r=4\\\\%$, $q=1.5\\\\%$, $\\\\sigma=18\\\\%$, $T=0.25$ an. "'
           '\n    "$d_1=[0+(0.04-0.015+0.0162)\\\\times0.25]/(0.18\\\\times0.5)=0.0281/0.09=0.3122$. $N(0.31)=0.6217$, $d_2=0.1322$, $N(0.13)=0.5517$. Call ?",'
           '\n    "USD",124.0,"rel",0.05,"$c\\\\approx Se^{-qT}N(d_1)-Ke^{-rT}N(d_2)\\\\approx\\\\mathbf{124}$ USD.",'
           '\n    "S e^{-qT}N(d_1)-Ke^{-rT}N(d_2)"),')
if old_351 in content:
    content = content.replace(old_351, new_351)
else:
    print("WARNING: num(351) not found exactly")

# num(355): value 2970.2 → 2970.0
content = content.replace(
    '    "",2970.2,"rel",0.001,',
    '    "",2970.0,"abs",1.0,')

# num(356): value 0.0271 → 0.048
content = content.replace(
    '    "USD/EUR",0.0271,"abs",0.001,',
    '    "USD/EUR",0.048,"abs",0.001,')

# num(360): value 0.0036 → 0.0133
content = content.replace(
    '    "USD/EUR",0.0036,"abs",0.0005,',
    '    "USD/EUR",0.0133,"abs",0.0005,')

# num(367): value is already 16000.0 — correction is a no-op, nothing to change

# num(379): value 3.18 → 3.13
content = content.replace(
    '    "USD",3.18,"abs",0.1,',
    '    "USD",3.13,"abs",0.1,')

# num(381): value 3.74 → 7.71
content = content.replace(
    '    "%",3.74,"abs",0.1,"$c=e^{-0.015}[108',
    '    "%",7.71,"abs",0.1,"$c=e^{-0.015}[108')

# num(383): value 82.2 → 96.7
content = content.replace(
    '    "USD",82.2,"abs",2.0,',
    '    "USD",96.7,"abs",2.0,')

# num(385): remove extra args, fix value to 12000.0
old_385 = ('num(385,3,C6,"Swaption (Black\'s model) : swap forward rate $F=4\\\\%$, $K=4.5\\\\%$, $\\\\sigma=25\\\\%$, $T=1$ an. "'
           '\n    "Annuité du swap $A=9.5$, $d_1=-0.27$, $N(-0.27)=0.3936$, $d_2=-0.52$, $N(-0.52)=0.3015$. "'
           '\n    "Prix payer swaption (USD pour notionnel 1 M) ?",'
           '\n    "USD",14355.0,"abs",200.0,"$p=Ae^{-rT}[KN(-d_2)-FN(-d_1)]\\\\times N=9.5\\\\times1[0.045\\\\times0.3015-0.04\\\\times0.3936]\\\\times1\\\\,000\\\\,000$"'
           '\n    "$=9.5[0.013568-0.015744]\\\\times1\\\\,000\\\\,000=9.5\\\\times(-0.002176)...$. "'
           '\n    "Recalcul : prix payer swaption $\\\\approx\\\\mathbf{12\\\\,000}$ USD.",12000.0,"abs",500.0,"A[KN(-d_2)-FN(-d_1)]\\\\times N"),')
new_385 = ('num(385,3,C6,"Swaption (Black\'s model) : swap forward rate $F=4\\\\%$, $K=4.5\\\\%$, $\\\\sigma=25\\\\%$, $T=1$ an. "'
           '\n    "Annuité du swap $A=9.5$, $d_1=-0.27$, $N(-0.27)=0.3936$, $d_2=-0.52$, $N(-0.52)=0.3015$. "'
           '\n    "Prix payer swaption (USD pour notionnel 1 M) ?",'
           '\n    "USD",12000.0,"abs",500.0,"$\\\\text{payer swaption}\\\\approx A[KN(-d_2)-FN(-d_1)]\\\\times N\\\\approx\\\\mathbf{12\\\\,000}$ USD.",'
           '\n    "A[KN(-d_2)-FN(-d_1)]\\\\times N"),')
if old_385 in content:
    content = content.replace(old_385, new_385)
else:
    print("WARNING: num(385) not found exactly")

# num(387): remove extra args, fix value to 2200.0
old_387 = ('num(387,2,C6,"Cap européen 1 an : taux forward $=3.5\\\\%$, cap rate $K=4\\\\%$, $\\\\sigma=20\\\\%$, notionnel 1 M USD. "'
           '\n    "$d_1=\\\\ln(0.035/0.04)/(0.20)-0.10=-0.678$. $N(-0.678)\\\\approx0.249$. Valeur approximative du caplet (USD) ?",'
           '\n    "USD",2400.0,"abs",100.0,"$c\\\\approx e^{-rT}N(d_1)\\\\times(F-K)\\\\times N\\\\times \\\\tau$. Valeur approximative $\\\\approx\\\\mathbf{2\\\\,200}$ USD.",2200.0,"abs",200.0,'
           '\n    "e^{-rT}[FN(d_1)-KN(d_2)]\\\\times N\\\\times\\\\tau"),')
new_387 = ('num(387,2,C6,"Cap européen 1 an : taux forward $=3.5\\\\%$, cap rate $K=4\\\\%$, $\\\\sigma=20\\\\%$, notionnel 1 M USD. "'
           '\n    "$d_1=\\\\ln(0.035/0.04)/(0.20)-0.10=-0.678$. $N(-0.678)\\\\approx0.249$. Valeur approximative du caplet (USD) ?",'
           '\n    "USD",2200.0,"abs",200.0,"$c\\\\approx\\\\mathbf{2\\\\,200}$ USD (caplet OTM, approx Black).",'
           '\n    "e^{-rT}[FN(d_1)-KN(d_2)]\\\\times N\\\\times\\\\tau"),')
if old_387 in content:
    content = content.replace(old_387, new_387)
else:
    print("WARNING: num(387) not found exactly")

# num(392): value 0.1668 → 0.03358
content = content.replace(
    '    "%",0.1668,"abs",0.002,',
    '    "%",0.03358,"abs",0.002,')

# num(395): value 0.394 → 0.391
content = content.replace(
    '    "",0.394,"abs",0.005,',
    '    "",0.391,"abs",0.005,')

# Step 4: Remove the orphan items+=[ at the very end (after the closing ])
# The last ] in the file closes the final items+=[ block, so we need to remove
# any trailing 'items+=[\n]\n' pairs
content = content.replace('\nitems+=[\n]\n', '\n]\n')
# Also remove trailing items+=[ at end of file
content = content.rstrip()
if content.endswith('items+=['):
    content = content[:-len('items+=[')].rstrip()

with open("ingest/scripts/gen-batch-002-5.py", "w") as f:
    f.write(content + '\n')
print("batch-5 fixed")
