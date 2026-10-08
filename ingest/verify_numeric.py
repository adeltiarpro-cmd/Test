#!/usr/bin/env python3
"""
ingest/verify_numeric.py
Recalcule chaque réponse numeric/numeric_steps à partir des données de l'énoncé,
compare à solution.value avec la tolérance de l'exercice, et corrige les écarts.

Usage : python3 ingest/verify_numeric.py
"""

import json
import re
import math
import copy
from pathlib import Path
from typing import Optional

# ─── Helpers ─────────────────────────────────────────────────────────────────

def N(x: float) -> float:
    """CDF de la loi normale standard."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def Nprime(x: float) -> float:
    """PDF de la loi normale standard."""
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

def within_tol(a: float, b: float, tol_val: float, tol_type: str) -> bool:
    if tol_type == "rel":
        return abs(a - b) / (abs(b) + 1e-10) <= tol_val
    return abs(a - b) <= tol_val

def extract_bold(mdx: str) -> Optional[float]:
    """Extrait la dernière valeur \\mathbf{X} dans steps_mdx."""
    hits = re.findall(r'\\mathbf\{([-+]?[^}]+)\}', mdx)
    for h in reversed(hits):
        h = h.replace('{,}', '.').replace(',', '.').replace('\\,', '').replace('\\%', '').replace('%', '')
        h = re.sub(r'\\[a-zA-Z]+', '', h).strip()
        try:
            return float(h)
        except ValueError:
            continue
    return None

def extract_params(prompt: str) -> dict:
    """
    Extrait les paramètres $var = value$ depuis le prompt LaTeX.
    Gère la virgule décimale française {,}, les pourcentages, les indices.
    """
    params = {}
    text = prompt.replace('{,}', '.')
    VAR = r'[\\A-Za-z][A-Za-z0-9_{\\]*'
    NUM = r'[-+]?(?:\d+\.?\d*|\.\d+)'

    def norm_var(v: str) -> str:
        v = re.sub(r'\\', '', v.strip())
        v = re.sub(r'_\{?(\w+)\}?', r'\1', v)
        v = re.sub(r'\{|\}', '', v)
        return v

    patterns = [
        (rf'\$\s*({VAR})\s*=\s*({NUM})\s*\\%\s*\$', True),
        (rf'\$\s*({VAR})\s*=\s*({NUM})\s*%\s*\$', True),
        (rf'\$\s*({VAR})\s*=\s*({NUM})\s*\$', False),
    ]
    for pat, is_pct in patterns:
        for m in re.finditer(pat, text):
            var = norm_var(m.group(1))
            val = float(m.group(2))
            if is_pct:
                val /= 100.0
            if var not in params:
                params[var] = val
    return params

def try_calculate(ex: dict) -> Optional[float]:
    """
    Tente de recalculer solution.value depuis les données de l'énoncé.
    Retourne None si le calcul n'est pas gérable automatiquement.
    """
    p = extract_params(ex['prompt_mdx'])
    f = ex['solution'].get('formula_katex', '')

    def g(*names, default=None):
        for n in names:
            if n in p:
                return p[n]
        return default

    try:
        # ── Payoffs futures/forwards ──
        if re.search(r'\(F_0\s*-\s*S_T\)\s*\\times\s*N', f):
            return (g('F0', 'F') - g('ST')) * g('N')
        if re.search(r'\(S_T\s*-\s*F_0\)\s*\\times\s*N', f):
            return (g('ST') - g('F0', 'F')) * g('N')
        if re.search(r'\(F_T\s*-\s*F_0\)\s*\\times\s*N', f):
            return (g('FT', 'F1') - g('F0', 'F')) * g('N')
        if re.search(r'\(F_0\s*-\s*F_1\)\s*\\times\s*N', f):
            return (g('F0', 'F') - g('F1')) * g('N')
        if re.search(r'\(F_1\s*-\s*F_0\)\s*\\times\s*N', f):
            return (g('F1') - g('F0', 'F')) * g('N')

        # ── Pricing futures/forwards ──
        if 'S_0 e^{(r+u)T}' in f or 'Se^{(r+u)T}' in f:
            S, r, u, T = g('S0', 'S'), g('r'), g('u'), g('T')
            if None not in (S, r, u, T):
                return S * math.exp((r + u) * T)
        if 'S_0 e^{rT}' in f or re.match(r'S_?0?\s*e\^\{?rT\}?$', f):
            S, r, T = g('S0', 'S'), g('r'), g('T')
            if None not in (S, r, T):
                return S * math.exp(r * T)
        if 'S_0 e^{(r-q)T}' in f or '(r-q)T' in f:
            S, r, q, T = g('S0', 'S'), g('r'), g('q'), g('T')
            if None not in (S, r, q, T):
                return S * math.exp((r - q) * T)
        if 'S_0 e^{(r-r_f)T}' in f or '(r-r_f)T' in f:
            S, r, rf, T = g('S0', 'S'), g('r'), g('rf', 'r_f'), g('T')
            if None not in (S, r, rf, T):
                return S * math.exp((r - rf) * T)
        if 'Se^{(r+u-y)T}' in f or 'S_0 e^{(r+u-y)T}' in f:
            S, r, u, y, T = g('S0', 'S'), g('r'), g('u'), g('y'), g('T')
            if None not in (S, r, u, y, T):
                return S * math.exp((r + u - y) * T)

        # ── Zero coupon bond ──
        if '1000 e^{-rT}' in f:
            r, T = g('r'), g('T')
            if None not in (r, T):
                return 1000 * math.exp(-r * T)

        # ── Conversions de taux ──
        if '(1+r_m/m)^m - 1' in f:
            rm = g('rm', 'r_m')
            m_m = re.search(r'm\s*=\s*(\d+)', ex['prompt_mdx'])
            m = int(m_m.group(1)) if m_m else g('m')
            if rm is not None and m is not None:
                return ((1 + rm / m) ** m - 1) * 100
        if '\\ln(1+(r_m/m)^m)' in f:
            rm = g('rm', 'r_m')
            m_m = re.search(r'm\s*=\s*(\d+)', ex['prompt_mdx'])
            m = int(m_m.group(1)) if m_m else g('m')
            if rm is not None and m is not None:
                EAR = (1 + rm / m) ** m - 1
                return math.log(1 + EAR) * 100

        # ── Spot rate depuis prix bond ──
        if '-\\frac{\\ln(P/F)}{T}' in f or '-{\\ln(P/F)}{T}' in f:
            P = g('P')
            if P is None:
                pm = re.search(r'(?:prix\s*spot|P)\s*[=:]\s*([\d.]+)', ex['prompt_mdx'], re.IGNORECASE)
                if pm:
                    P = float(pm.group(1))
            T = g('T', default=0.5)
            F_par = g('F', default=100.0)
            if P is not None and T:
                return -math.log(P / F_par) / T * 100

        # ── Option payoffs ──
        if re.search(r'\\max\(S_?[T0]?\s*-\s*K', f) and 'mathbf{1}' not in f:
            S, K = g('ST', 'S0', 'S'), g('K')
            if None not in (S, K):
                return max(S - K, 0)
        if re.search(r'\\max\(K\s*-\s*S', f) and 'mathbf{1}' not in f:
            S, K = g('ST', 'S0', 'S'), g('K')
            if None not in (S, K):
                return max(K - S, 0)

        # ── Probabilité risque-neutre (binomial CRR) ──
        if '(e^{r\\Delta t}-d)/(u-d)' in f:
            r, u, d = g('r'), g('u'), g('d')
            dt_m = re.search(r'\\Delta\s*t\s*=\s*([\d.]+)', ex['prompt_mdx'])
            dt = float(dt_m.group(1)) if dt_m else g('Deltat')
            if None not in (r, u, d, dt):
                return (math.exp(r * dt) - d) / (u - d)

        # ── CRR u = e^(sigma*sqrt(dt)) ──
        if 'e^{\\sigma\\sqrt{\\Delta t}}' in f:
            sigma = g('sigma')
            dt_m = re.search(r'\\Delta\s*t\s*=\s*([\d.]+)', ex['prompt_mdx'])
            dt = float(dt_m.group(1)) if dt_m else None
            if None not in (sigma, dt):
                return math.exp(sigma * math.sqrt(dt))

        # ── Vasicek bond: e^{A-B*r0} ──
        if 'e^{A-B\\cdot r_0}' in f or re.match(r'e\^\{A-B', f):
            A, B = g('A'), g('B')
            r0 = g('r0', 'r')
            if None not in (A, B, r0):
                return math.exp(A - B * r0)

        # ── Gamma = N'(d1)/(S sigma sqrt(T)) ──
        if "N'(d_1)/(S\\sigma\\sqrt{T})" in f:
            npm = re.search(r"N'\(d_1\)\s*=\s*([\d.]+)", ex['prompt_mdx'])
            Np = float(npm.group(1)) if npm else None
            S, sigma, T = g('S'), g('sigma'), g('T')
            if None not in (Np, S, sigma, T):
                return Np / (S * sigma * math.sqrt(T))

        # ── Theta / 365 ──
        if '\\Theta/365' in f:
            S, sigma, T, r, K = g('S'), g('sigma'), g('T'), g('r'), g('K')
            npm = re.search(r"N'\(d_1\)\s*=\s*([\d.]+)", ex['prompt_mdx'])
            nd2m = re.search(r"N\(d_2\)\s*=\s*([\d.]+)", ex['prompt_mdx'])
            Np = float(npm.group(1)) if npm else None
            Nd2 = float(nd2m.group(1)) if nd2m else None
            if None not in (S, sigma, T, r, K, Np, Nd2):
                theta = -(S * Np * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * Nd2
                return theta / 365

        # ── Digital cash-or-nothing: Q*e^{-rT}*N(d2) ──
        if 'Qe^{-rT}N(d_2)' in f:
            Q, r, T = g('Q'), g('r'), g('T')
            nd2m = re.search(r'N\(d_2\)\s*=\s*([\d.]+)', ex['prompt_mdx'])
            Nd2 = float(nd2m.group(1)) if nd2m else None
            if None not in (Q, r, T, Nd2):
                return Q * math.exp(-r * T) * Nd2

        # ── SMM depuis CPR ──
        if '1-(1-CPR)^{1/12}' in f:
            CPR = g('CPR')
            if CPR is not None:
                return (1 - (1 - CPR) ** (1 / 12)) * 100

        # ── EWMA variance ──
        if '\\lambda\\sigma_{n-1}^2+(1-\\lambda)r_{n-1}^2' in f:
            lam = g('lam', 'lambda', 'Lambda')
            s2m = re.search(r'sigma_\{n-1\}\^2\s*=\s*([\d.]+)', ex['prompt_mdx'])
            r2m = re.search(r'r_\{n-1\}\s*=\s*([-\d.]+%?)', ex['prompt_mdx'])
            if lam is not None and s2m and r2m:
                sig2 = float(s2m.group(1))
                rv = r2m.group(1).replace('%', '')
                r_val = float(rv) / 100 if '%' in r2m.group(1) else float(rv)
                return lam * sig2 + (1 - lam) * r_val ** 2

        # ── EWMA poids (1-lambda)*lambda^(d-1) ──
        if '(1-\\lambda)\\lambda^{d-1}' in f:
            lam = g('lam', 'lambda', 'Lambda')
            dm = re.search(r'd\s*=\s*(\d+)', ex['prompt_mdx'])
            d = int(dm.group(1)) if dm else None
            if None not in (lam, d):
                return (1 - lam) * lam ** (d - 1)

        # ── Survie: e^{-lambda*T} ──
        if 'e^{-\\lambda T}' in f:
            lam = g('lam', 'lambda')
            T = g('T')
            if None not in (lam, T):
                return math.exp(-lam * T)

        # ── Perte attendue: PD*LGD*EAD ──
        if 'PD\\times LGD\\times EAD' in f:
            PD, LGD, EAD = g('PD'), g('LGD'), g('EAD')
            if None not in (PD, LGD, EAD):
                return PD * LGD * EAD

        # ── Commodity futures Se^{(r+u-y)T} ──
        if 'Se^{(r+u-y)T}' in f and 'S_0' not in f:
            S, r, u, y, T = g('S'), g('r'), g('u'), g('y'), g('T')
            if None not in (S, r, u, y, T):
                return S * math.exp((r + u - y) * T)

        # ── Vol bootstrapping LMM ──
        if '(\\sigma_{cap}^2 T-\\sigma_{prev}^2 T_{prev})' in f:
            sc_m = re.search(r'sigma_\{1,2\}\^?\{?cap\}?\s*=\s*([\d.]+%?)', ex['prompt_mdx'])
            sp_m = re.search(r'sigma_1\s*=\s*([\d.]+%?)', ex['prompt_mdx'])
            if sc_m and sp_m:
                sc = float(sc_m.group(1).replace('%', '')) / 100
                sp = float(sp_m.group(1).replace('%', '')) / 100
                Tp, T7 = 2.0, 1.0
                v2 = (sc ** 2 * Tp - sp ** 2 * T7) / (Tp - T7)
                return math.sqrt(v2) * 100

    except (TypeError, ValueError, ZeroDivisionError):
        pass

    return None


# ─── Corrections manuelles (hardcodées après vérification mathématique) ──────

# Chaque entrée: (external_key, new_value, new_steps_mdx, new_prompt_mdx|None)
FIXES = {
    # ── Batch 2 — Interest rates ──
    "markets-derivatives-short_answer-093": {
        "value": 2.836,
        "steps_mdx": (
            r"Flux actualisés (taux continu $r=5\%$, annuel) : "
            r"$PV_1=6e^{-0.05}=6\times0{,}9512=5{,}707$, "
            r"$PV_2=6e^{-0.10}=6\times0{,}9048=5{,}429$, "
            r"$PV_3=106e^{-0.15}=106\times0{,}8607=91{,}235$. "
            r"Prix $P=5{,}707+5{,}429+91{,}235=\mathbf{102{,}371}$. "
            r"$D_{Mac}=\dfrac{1\times5{,}707+2\times5{,}429+3\times91{,}235}{102{,}371}"
            r"=\dfrac{5{,}707+10{,}858+273{,}705}{102{,}371}=\dfrac{290{,}270}{102{,}371}=\mathbf{2{,}836}$ ans."
        ),
    },
    "markets-derivatives-short_answer-100": {
        "value": 11.83,
        "steps_mdx": (
            r"Taux nominal $r_m=12\%$, capitalisation trimestrielle ($m=4$). "
            r"Taux effectif annuel : $r_{eff}=(1+0{,}12/4)^4-1=(1{,}03)^4-1=1{,}12551-1=12{,}551\%$. "
            r"Taux continu équivalent : $r_c=\ln(1+r_{eff})=\ln(1{,}12551)=\mathbf{11{,}83}\%$."
        ),
    },
    "markets-derivatives-short_answer-106": {
        "value": 3.02,
        "steps_mdx": (
            r"Obligation zéro-coupon : $P=98{,}50$ USD, $F=100$ USD, $T=0{,}5$ an. "
            r"$r=-\dfrac{\ln(P/F)}{T}=-\dfrac{\ln(98{,}50/100)}{0{,}5}"
            r"=-\dfrac{\ln(0{,}985)}{0{,}5}=-\dfrac{-0{,}01511}{0{,}5}=\mathbf{3{,}02}\%$."
        ),
    },
    "markets-derivatives-short_answer-112": {
        "value": 4.36,
        "steps_mdx": (
            r"Obligation 5 ans, coupon annuel 50 USD, nominal 1 000 USD, $y=4{,}5\%$. "
            r"$PV_1=50/1{,}045=47{,}847$, $PV_2=50/1{,}045^2=45{,}785$, "
            r"$PV_3=50/1{,}045^3=43{,}820$, $PV_4=50/1{,}045^4=41{,}929$, "
            r"$PV_5=1050/1{,}045^5=842{,}569$. "
            r"$P=1\,021{,}950$. "
            r"$D_{Mac}=\dfrac{1\times47{,}847+2\times45{,}785+3\times43{,}820+4\times41{,}929+5\times842{,}569}{1\,021{,}950}"
            r"=\dfrac{4\,651{,}4}{1\,021{,}950}=4{,}551$ ans. "
            r"$D^*=D_{Mac}/(1+y)=4{,}551/1{,}045=\mathbf{4{,}36}$ ans."
        ),
    },
    # ── Batch 1 — Futures/Forwards ──
    "markets-derivatives-short_answer-118": {
        "value": 27.91,
        "steps_mdx": (
            r"$F_0=S_0 e^{(r+u)T}=25\times e^{(0{,}08+0{,}03)\times1}"
            r"=25\times e^{0{,}11}=25\times1{,}11628=\mathbf{27{,}91}$ USD."
        ),
    },
    # ── Batch 3 — Swaps ──
    "markets-derivatives-short_answer-167": {
        "value": 3.44,
        "steps_mdx": (
            r"Taux SOFR continus : $r_1=2{,}5\%$, $r_2=3{,}0\%$, $r_3=3{,}4\%$. "
            r"Facteurs d'actualisation : $e^{-0{,}025}=0{,}9753$, $e^{-0{,}060}=0{,}9418$, $e^{-0{,}102}=0{,}9030$. "
            r"$k=\dfrac{1-e^{-r_3 T_3}}{e^{-r_1}+e^{-r_2\times2}+e^{-r_3\times3}}"
            r"=\dfrac{1-0{,}9030}{0{,}9753+0{,}9418+0{,}9030}=\dfrac{0{,}0970}{2{,}8201}=\mathbf{3{,}44}\%$."
        ),
    },
    # ── Batch 6 — Greeks ──
    "markets-derivatives-short_answer-405": {
        "value": -0.0120,
        "steps_mdx": (
            r"$\Theta=-\dfrac{S N'(d_1)\sigma}{2\sqrt{T}}-rKe^{-rT}N(d_2)$. "
            r"Terme 1 : $-\dfrac{50\times0{,}38\times0{,}25}{2\sqrt{0{,}5}}"
            r"=-\dfrac{4{,}75}{1{,}4142}=-3{,}358$ USD/an. "
            r"Terme 2 : $-0{,}04\times50\times e^{-0{,}02}\times0{,}52"
            r"=-0{,}04\times50\times0{,}9802\times0{,}52=-1{,}019$ USD/an. "
            r"$\Theta=-3{,}358-1{,}019=-4{,}377$ USD/an. "
            r"$\Theta/365=-4{,}377/365=\mathbf{-0{,}0120}$ USD/jour."
        ),
    },
    "markets-derivatives-short_answer-412": {
        "prompt_mdx": (
            r"Relation BSM : $\Theta+rS\Delta+\frac{1}{2}\sigma^2S^2\Gamma=rC$. "
            r"$\Theta=-3$, $r=5\%$, $S=50$, $\Delta=0{,}5$, $\sigma=20\%$, $\Gamma=0{,}04$. $C=?$"
        ),
        "value": 5.0,
        "steps_mdx": (
            r"EDP BSM : $rC=\Theta+rS\Delta+\tfrac{1}{2}\sigma^2 S^2\Gamma$. "
            r"$rS\Delta=0{,}05\times50\times0{,}5=1{,}25$. "
            r"$\tfrac{1}{2}\sigma^2 S^2\Gamma=\tfrac{1}{2}\times0{,}04\times2\,500\times0{,}04=2{,}00$. "
            r"$0{,}05C=-3+1{,}25+2{,}00=\mathbf{0{,}25}$. "
            r"$C=0{,}25/0{,}05=\mathbf{5{,}0}$ USD."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 0.1}},
    },
    "markets-derivatives-short_answer-415": {
        "prompt_mdx": (
            r"Portefeuille delta-hedgé, rééquilibré quotidiennement ($\Delta t=1/252$ an). "
            r"$\Gamma=0{,}05$, $S=100$ USD, $\sigma=20\%$ annuel. "
            r"Espérance du gain journalier lié au gamma (USD) ?"
        ),
        "value": 0.0397,
        "steps_mdx": (
            r"$E[\text{gain gamma}]=\tfrac{1}{2}\Gamma\sigma^2 S^2\Delta t"
            r"=\tfrac{1}{2}\times0{,}05\times0{,}04\times10\,000\times\dfrac{1}{252}"
            r"=\dfrac{10}{252}=\mathbf{0{,}0397}$ USD/jour."
        ),
        "formula_patch": r"\frac{1}{2}\Gamma\sigma^2 S^2 \Delta t",
        "payload_patch": {
            "unit": "USD",
            "precision": 4,
            "tolerance": {"type": "abs", "value": 0.005},
        },
    },
    # ── Batch 7 — Exotiques / Modèles ──
    "markets-derivatives-short_answer-460": {
        "value": 4.28,
        "steps_mdx": (
            r"Margrabe : $\sigma_{eff}=\sqrt{\sigma_A^2+\sigma_B^2-2\rho\sigma_A\sigma_B}"
            r"=\sqrt{0{,}04+0{,}0225-0{,}036}=\sqrt{0{,}0265}=0{,}1628$. "
            r"$d_1=\dfrac{\ln(50/48)+\tfrac{1}{2}\times0{,}0265}{0{,}1628}"
            r"=\dfrac{0{,}0408+0{,}01325}{0{,}1628}=0{,}330$. "
            r"$N(0{,}330)=0{,}629$. $d_2=0{,}330-0{,}163=0{,}167$. $N(0{,}167)=0{,}566$. "
            r"$c=50\times0{,}629-48\times0{,}566=31{,}45-27{,}17=\mathbf{4{,}28}$ USD."
        ),
    },
    "markets-derivatives-short_answer-471": {
        "value": 0.02613,
        "steps_mdx": (
            r"Contribution puts (sans actualisation) : "
            r"$2\sum_{i}\dfrac{p_i}{K_i^2}\Delta K"
            r"=2\times10\times\left(\dfrac{2}{80^2}+\dfrac{4}{90^2}+\dfrac{5}{100^2}\right)$. "
            r"$=2\times10\times(0{,}000313+0{,}000494+0{,}000500)"
            r"=20\times0{,}001306=\mathbf{0{,}02613}$ USD."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 0.001}},
    },
    "markets-derivatives-short_answer-572": {
        "value": 134.8,
        "steps_mdx": (
            r"CDS swaption payeuse Black : $V=D\cdot[F\cdot N(d_1)-K\cdot N(d_2)]$. "
            r"$d_1=0{,}963$ → $N(0{,}963)=0{,}832$. $d_2=0{,}751$ → $N(0{,}751)=0{,}774$. "
            r"$V=4\times[180\times0{,}832-150\times0{,}774]"
            r"=4\times[149{,}8-116{,}1]=4\times33{,}7=\mathbf{134{,}8}$ bps."
        ),
    },
    "markets-derivatives-short_answer-635": {
        "value": 524.0,
        "steps_mdx": (
            r"Caplet Black : $V=L\delta e^{-r_s T}[F_k N(d_1)-R_K N(d_2)]$. "
            r"$d_1=[\ln(0{,}04/0{,}045)+0{,}5\times0{,}0625]/0{,}25"
            r"=[-0{,}1178+0{,}0313]/0{,}25=-0{,}346$. "
            r"$N(-0{,}346)=0{,}365$. $d_2=-0{,}596$. $N(-0{,}596)=0{,}276$. "
            r"$V=1\,000\,000\times0{,}25\times e^{-0{,}04}"
            r"\times[0{,}04\times0{,}365-0{,}045\times0{,}276]"
            r"=240\,200\times0{,}00218=\mathbf{524}$ USD."
        ),
    },
    "markets-derivatives-short_answer-637": {
        "value": 0.009935,
        "steps_mdx": (
            r"Swaption payeuse Black : $V=A[S_0 N(d_1)-K N(d_2)]$. "
            r"$d_1=-0{,}149$ → $N(-0{,}149)=0{,}441$. "
            r"$d_2=-0{,}349$ → $N(-0{,}349)=0{,}364$. "
            r"$V=4{,}5\times[0{,}038\times0{,}441-0{,}04\times0{,}364]"
            r"=4{,}5\times[0{,}01676-0{,}01456]"
            r"=4{,}5\times0{,}00220=\mathbf{0{,}009935}$ (pour notionnel 1)."
        ),
        "payload_patch": {
            "unit": "",
            "tolerance": {"type": "abs", "value": 0.0005},
        },
    },
    "markets-derivatives-short_answer-642": {
        "value": 879.0,
        "steps_mdx": (
            r"Caplet OTM Black : $L=1\,\text{M}$, $\delta=0{,}5$, $F_k=4{,}5\%$, $R_K=5\%$, $\sigma=20\%$. "
            r"$d_1=[\ln(0{,}045/0{,}05)+0{,}02]/0{,}20=[-0{,}1054+0{,}02]/0{,}20=-0{,}427$. "
            r"$N(-0{,}427)=0{,}335$. $d_2=-0{,}627$. $N(-0{,}627)=0{,}265$. "
            r"$V=1\,000\,000\times0{,}5\times e^{-0{,}04}"
            r"\times[0{,}045\times0{,}335-0{,}05\times0{,}265]"
            r"=480\,400\times0{,}00183=\mathbf{879}$ USD."
        ),
    },
    "markets-derivatives-short_answer-662": {
        "value": 0.9623,
        "steps_mdx": (
            r"$B(0,1)=e^{A-B\cdot r_0}=e^{-0{,}0023-0{,}9048\times0{,}04}"
            r"=e^{-0{,}0023-0{,}03619}=e^{-0{,}03849}=\mathbf{0{,}9623}$."
        ),
    },
    "markets-derivatives-short_answer-695": {
        "value": 15.75,
        "steps_mdx": (
            r"Bootstrapping LMM : $\sigma_2^2"
            r"=\dfrac{\sigma_{1,2}^2\times T_2-\sigma_1^2\times T_1}{T_2-T_1}"
            r"=\dfrac{0{,}18^2\times2-0{,}20^2\times1}{1}=\dfrac{0{,}0648-0{,}040}{1}=0{,}0248$. "
            r"$\sigma_2=\sqrt{0{,}0248}=\mathbf{15{,}75}\%$."
        ),
    },
    "markets-derivatives-short_answer-698": {
        "value": 0.00433,
        "steps_mdx": (
            r"Ajustement convexité CMS approx. ($\sigma=15\%$, $T=1$, $s=4\%$, $D=5$ ans) : "
            r"$CA\approx\sigma^2 T\cdot s\cdot\dfrac{D}{1+s}"
            r"=0{,}0225\times1\times0{,}04\times\dfrac{5}{1{,}04}"
            r"=0{,}0225\times0{,}1923=\mathbf{0{,}00433}$ (en décimal)."
        ),
        "payload_patch": {
            "unit": "",
            "tolerance": {"type": "abs", "value": 0.0005},
        },
    },
    "markets-derivatives-short_answer-701": {
        "value": 1.083,
        "steps_mdx": (
            r"Bachelier call sur taux : "
            r"$h=(F-K)/(\sigma\sqrt{T})=(2\%-1\%)/(1\%\times1)=1$. "
            r"$c=[(F-K)N(h)+\sigma\sqrt{T}N'(h)]e^{-rT}"
            r"=[(1\%)(0{,}8413)+(1\%)(0{,}2420)]\times1"
            r"=1\%\times(0{,}8413+0{,}2420)=\mathbf{1{,}083}\%$."
        ),
    },
    # ── Batch 5 — BSM/Binomial ──
    "markets-derivatives-short_answer-500": {
        "value": 0.000430,
        "steps_mdx": (
            r"EWMA : $\sigma_n^2=\lambda\sigma_{n-1}^2+(1-\lambda)r_{n-1}^2$. "
            r"$=0{,}94\times0{,}0004+0{,}06\times(-0{,}03)^2"
            r"=0{,}000376+0{,}06\times0{,}0009=0{,}000376+0{,}000054=\mathbf{0{,}000430}$."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 1e-5}},
    },
    "markets-derivatives-short_answer-504": {
        "value": 0.02281,
        "steps_mdx": (
            r"Poids EWMA de l'observation à $d=10$ jours : "
            r"$(1-\lambda)\lambda^{d-1}=0{,}03\times0{,}97^9=0{,}03\times0{,}7602=\mathbf{0{,}02281}$."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 0.0005}},
    },
    "markets-derivatives-short_answer-580": {
        "value": 58.4,
        "steps_mdx": (
            r"Condition CFL pour différences finies explicites : "
            r"$\Delta t\leq\dfrac{(\Delta S)^2}{\sigma^2 S^2}"
            r"=\dfrac{5^2}{0{,}25^2\times50^2}=\dfrac{25}{156{,}25}=0{,}160$ an "
            r"$=0{,}160\times365=\mathbf{58{,}4}$ jours."
        ),
    },
    "markets-derivatives-short_answer-593": {
        "value": 0.02,
        "steps_mdx": (
            r"Butterfly spread discret ($K=100$, $\varepsilon=5$) : "
            r"$(C(105)-2C(100)+C(95))=(3{,}5-2\times5{,}2+7{,}4)=(3{,}5-10{,}4+7{,}4)=0{,}5$. "
            r"$\partial^2 C/\partial K^2=0{,}5/\varepsilon^2=0{,}5/25=\mathbf{0{,}02}$."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 0.001}},
    },
    # ── Batch 6 — Greeks / Vol ──
    "markets-derivatives-short_answer-482": {
        "value": 1.935,
        "steps_mdx": (
            r"$\sigma_p=\sqrt{w_A^2\sigma_A^2+w_B^2\sigma_B^2+2w_Aw_B\rho\sigma_A\sigma_B}$. "
            r"$w_A^2\sigma_A^2=0{,}36\times0{,}0004=0{,}000144$. "
            r"$w_B^2\sigma_B^2=0{,}16\times0{,}0009=0{,}000144$. "
            r"$2w_Aw_B\rho\sigma_A\sigma_B=2\times0{,}6\times0{,}4\times0{,}3\times0{,}02\times0{,}03=0{,}0000864$. "
            r"$\sigma_p=\sqrt{0{,}000144+0{,}000144+0{,}0000864}=\sqrt{0{,}0003744}=\mathbf{1{,}935}\%$."
        ),
    },
    # ── Batch 8 — Credit / VaR ──
    "markets-derivatives-short_answer-527": {
        "value": 932.0,
        "steps_mdx": (
            r"Bond zéro-coupon risqué : $V=e^{-r}[(1-PD)\times K+PD\times R\times K]$. "
            r"$=e^{-0{,}04}[0{,}95\times1\,000+0{,}05\times0{,}40\times1\,000]"
            r"=0{,}9608\times[950+20]=0{,}9608\times970=\mathbf{932{,}0}$ USD."
        ),
    },
    "markets-derivatives-short_answer-540": {
        "value": 943.9,
        "steps_mdx": (
            r"Bond risqué : $V=e^{-r}[(1-PD)\times K+PD\times R\times K]$. "
            r"$=e^{-0{,}04}[0{,}97\times1\,000+0{,}03\times0{,}40\times1\,000]"
            r"=0{,}9608\times[970+12]=0{,}9608\times982=\mathbf{943{,}9}$ USD."
        ),
    },
    # ── Batch 9 — Commodities / Real Options ──
    "markets-derivatives-short_answer-741": {
        "value": 85.64,
        "steps_mdx": (
            r"$F=Se^{(r+u-y)T}=85\times e^{(0{,}04+0{,}015-0{,}025)\times0{,}25}"
            r"=85\times e^{0{,}03\times0{,}25}=85\times e^{0{,}0075}=85\times1{,}00752=\mathbf{85{,}64}$ USD/bbl."
        ),
    },
    "markets-derivatives-short_answer-748": {
        "value": 29.79,
        "steps_mdx": (
            r"Crack spread 3:2:1 par bbl de brut (rendements : $2/3$ essence, $1/3$ diesel) : "
            r"Essence : $0{,}67\times2{,}70\times42=0{,}67\times113{,}40=75{,}98$ USD/bbl. "
            r"Diesel : $0{,}33\times2{,}80\times42=0{,}33\times117{,}60=38{,}81$ USD/bbl. "
            r"$\text{Marge}=75{,}98+38{,}81-85=\mathbf{29{,}79}$ USD/bbl."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 0.5}},
    },
    "markets-derivatives-short_answer-753": {
        "value": 3.830,
        "steps_mdx": (
            r"$F=S\,e^{(r+u-y)T}=3{,}50\times e^{(0{,}04+0{,}08-0{,}03)\times1}"
            r"=3{,}50\times e^{0{,}09}=3{,}50\times1{,}09417=\mathbf{3{,}830}$ USD/MMBtu."
        ),
    },
    "markets-derivatives-short_answer-760": {
        "value": 19.70,
        "steps_mdx": (
            r"Put réel (option d'abandon) BSM : $d_1=[\ln(80/100)+(0{,}05+0{,}045)\times1]/0{,}30"
            r"=[-0{,}2231+0{,}095]/0{,}30=-0{,}427$. $N(-d_1)=N(0{,}427)=0{,}665$. "
            r"$d_2=-0{,}427-0{,}30=-0{,}727$. $N(-d_2)=N(0{,}727)=0{,}766$. "
            r"$p=100\,e^{-0{,}05}\times0{,}766-80\times0{,}665"
            r"=95{,}12\times0{,}766-53{,}20=72{,}86-53{,}20=\mathbf{19{,}70}$ M USD."
        ),
    },
}

# ─── Correction des numeric_steps avec réponses None ─────────────────────────

NSTEP_FIXES = {
    "markets-derivatives-short_answer-409": {
        "steps_answers_patch": [200.0, 300.0, -1333.0],
        "steps_labels_patch": [
            r"Équation gamma : $1{,}5w_A+0{,}8w_B=200$ (RHS)",
            r"Équation delta : $0{,}6w_A+0{,}4w_B=300$ (RHS)",
            r"$w_A$ (résoudre le système 2×2)",
        ],
        "add_step": {
            "label": r"$w_B$ (substitution dans l'équation delta)",
            "unit": "options",
            "tolerance": 5.0,
            "solution_mdx": r"$w_B=\dfrac{300-0{,}6\times(-1\,333)}{0{,}4}=\dfrac{300+800}{0{,}4}=\dfrac{1\,100}{0{,}4}=\mathbf{2\,750}$",
            "answer": 2750.0,
        },
    },
}


# ─── Application des corrections ─────────────────────────────────────────────

BATCH_DIR = Path(__file__).parent / "canonical"


def apply_fixes() -> dict:
    """Applique toutes les corrections et retourne un rapport."""
    report = {"fixed": [], "auto_verified": [], "unchanged": [], "errors": []}

    for batch_file in sorted(BATCH_DIR.glob("batch-002-*.json")):
        data = json.loads(batch_file.read_text())
        changed = False

        for i, ex in enumerate(data["items"]):
            key = ex["external_key"]
            ex_type = ex["type"]

            # ── Corrections numériques manuelles ──
            if key in FIXES and ex_type == "numeric":
                fix = FIXES[key]
                old_val = ex["solution"]["value"]
                old_steps = ex["solution"].get("steps_mdx", "")

                if "value" in fix:
                    ex["solution"]["value"] = fix["value"]
                if "steps_mdx" in fix:
                    ex["solution"]["steps_mdx"] = fix["steps_mdx"]
                if "formula_patch" in fix:
                    ex["solution"]["formula_katex"] = fix["formula_patch"]
                if "prompt_mdx" in fix:
                    ex["prompt_mdx"] = fix["prompt_mdx"]
                if "payload_patch" in fix:
                    ex["payload"].update(fix["payload_patch"])

                new_val = ex["solution"]["value"]
                report["fixed"].append({
                    "key": key,
                    "old_value": old_val,
                    "new_value": new_val,
                    "delta": f"{abs(new_val - old_val):.6g}",
                    "redesigned": "prompt_mdx" in fix,
                })
                changed = True

            # ── Corrections numeric_steps ──
            elif key in NSTEP_FIXES and ex_type == "numeric_steps":
                fix = NSTEP_FIXES[key]
                steps = ex["payload"]["steps"]
                sol_steps = ex["solution"]["steps"]

                if "steps_answers_patch" in fix:
                    for j, ans in enumerate(fix["steps_answers_patch"]):
                        if j < len(sol_steps):
                            sol_steps[j]["answer"] = ans
                if "steps_labels_patch" in fix:
                    for j, lbl in enumerate(fix["steps_labels_patch"]):
                        if j < len(steps):
                            steps[j]["label"] = lbl
                if "add_step" in fix:
                    add = fix["add_step"]
                    steps.append({
                        "label": add["label"],
                        "unit": add["unit"],
                        "tolerance": {"type": "abs", "value": add["tolerance"]},
                        "solution_mdx": add["solution_mdx"],
                    })
                    sol_steps.append({"answer": add["answer"]})

                report["fixed"].append({
                    "key": key,
                    "old_value": "None steps",
                    "new_value": "steps corrigées",
                    "delta": "N/A",
                    "redesigned": False,
                })
                changed = True

            # ── Vérification automatique ──
            elif ex_type == "numeric":
                calc = try_calculate(ex)
                if calc is not None:
                    tol = ex["payload"].get("tolerance", {})
                    tol_val = tol.get("value", 0.05)
                    tol_type = tol.get("type", "abs")
                    ok = within_tol(calc, ex["solution"]["value"], tol_val, tol_type)
                    report["auto_verified"].append({
                        "key": key,
                        "formula": ex["solution"].get("formula_katex", "")[:50],
                        "calculated": round(calc, 6),
                        "stored": ex["solution"]["value"],
                        "ok": ok,
                    })
                else:
                    report["unchanged"].append(key)

        if changed:
            batch_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n"
            )

    return report


def print_report(report: dict):
    fixed = report["fixed"]
    verified = report["auto_verified"]
    mismatches = [v for v in verified if not v["ok"]]

    print("=" * 70)
    print(f"CORRECTIONS APPLIQUÉES : {len(fixed)}")
    print("=" * 70)
    for f in fixed:
        tag = " [redesigné]" if f.get("redesigned") else ""
        print(f"  {f['key']}: {f['old_value']} → {f['new_value']}"
              f" (écart={f['delta']}){tag}")

    print()
    print("=" * 70)
    print(f"VÉRIFICATION AUTO : {len(verified)} exercices calculables")
    print(f"  OK      : {len(verified) - len(mismatches)}")
    print(f"  Écarts  : {len(mismatches)}")
    print("=" * 70)
    if mismatches:
        print("Écarts détectés par la vérification automatique :")
        for m in sorted(mismatches, key=lambda x: x["key"]):
            print(f"  {m['key']}: calculé={m['calculated']}, "
                  f"stocké={m['stored']} (formule: {m['formula']}...)")

    print()
    non_calc = len(report["unchanged"])
    print(f"Exercices sans calcul automatique : {non_calc}")
    print()
    print(f"TOTAL EXERCICES CORRIGÉS : {len(fixed)}")


if __name__ == "__main__":
    report = apply_fixes()
    print_report(report)
