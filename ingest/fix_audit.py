#!/usr/bin/env python3
"""
ingest/fix_audit.py
CAT 1 – valeurs intermédiaires BSM fausses dans l'énoncé   (4 exercices)
CAT 2 – arrondis non documentés                             (1 exercice)
CAT 3 – exercices dépendants                                (2 exercices)
CAT 4 – exercices triviaux (réponse lisible sans calcul)    (13 exercices)
Total : 20 corrections.
Usage : python3 ingest/fix_audit.py
"""

import json
from pathlib import Path

BATCH_DIR = Path(__file__).parent / "canonical"

FIXES = {

    # ══════════════════════════════════════════════════════════════
    # CAT 1 — Valeurs intermédiaires BSM fausses dans l'énoncé
    # ══════════════════════════════════════════════════════════════

    # key-319 : d1=0,2475 énoncé mais calcul donne 0,2239 (σ=30%, T=0,5, ATM)
    "markets-derivatives-short_answer-319": {
        "prompt_mdx": (
            r"Call BSM : $S=60$, $K=60$, $r=5\%$, $\sigma=30\%$, $T=0{,}5$. "
            r"$d_1=0{,}2239$, $N(d_1)=0{,}5886$, $d_2=0{,}0118$, $N(d_2)=0{,}5047$. "
            r"Prix call (USD) ?"
        ),
        "value": 5.79,
        "steps_mdx": (
            r"$c=60\times0{,}5886-60\,e^{-0{,}025}\times0{,}5047"
            r"=35{,}316-60\times0{,}9753\times0{,}5047"
            r"=35{,}316-29{,}53=\mathbf{5{,}79}$ USD."
        ),
    },

    # key-351 : numérateur d1 affiché 0,0281 au lieu de 0,0103
    # (0,04−0,015+0,0162)×0,25 = 0,0412×0,25 = 0,0103, pas 0,0281
    # d1 correct = 0,1144 ; c correct = 163 USD
    "markets-derivatives-short_answer-351": {
        "prompt_mdx": (
            r"Call sur S\&P500 : $S=4200$, $K=4200$, $r=4\%$, $q=1{,}5\%$, "
            r"$\sigma=18\%$, $T=0{,}25$ an. "
            r"$(r-q+\sigma^2/2)\times T=(0{,}04-0{,}015+0{,}0162)\times0{,}25=0{,}0103$. "
            r"$d_1=0{,}0103/0{,}09=0{,}1144$, $N(d_1)=0{,}5455$, "
            r"$d_2=0{,}0244$, $N(d_2)=0{,}5097$. Call (USD) ?"
        ),
        "value": 163.0,
        "steps_mdx": (
            r"$c=Se^{-qT}N(d_1)-Ke^{-rT}N(d_2)"
            r"=4200\times0{,}9963\times0{,}5455-4200\times0{,}9900\times0{,}5097"
            r"=4\,184\times0{,}5455-4\,158\times0{,}5097"
            r"=2\,282-2\,119=\mathbf{163}$ USD."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 2.0}},
    },

    # key-405 : N'(d1)=0,38 et N(d2)=0,52 énoncé ; valeurs correctes 0,391 / 0,510
    # (S=50,K=50,r=4%,σ=25%,T=0,5 → d1=0,2015, N'=0,391, d2=0,0247, N=0,510)
    "markets-derivatives-short_answer-405": {
        "prompt_mdx": (
            r"Un call européen : $S=50$, $K=50$, $r=4\%$, $\sigma=25\%$, $T=0{,}5$ an, "
            r"$N'(d_1)=0{,}391$, $N(d_2)=0{,}510$. Calculez $\Theta/365$ (USD/jour)."
        ),
        "value": -0.0122,
        "steps_mdx": (
            r"$\Theta=-\dfrac{S N'(d_1)\sigma}{2\sqrt{T}}-rKe^{-rT}N(d_2)$. "
            r"Terme 1 : $-\dfrac{50\times0{,}391\times0{,}25}{2\sqrt{0{,}5}}"
            r"=-\dfrac{4{,}888}{1{,}4142}=-3{,}457$ USD/an. "
            r"Terme 2 : $-0{,}04\times50\times e^{-0{,}02}\times0{,}510"
            r"=-1{,}001$ USD/an. "
            r"$\Theta=-3{,}457-1{,}001=-4{,}458$ USD/an. "
            r"$\Theta/365=-4{,}458/365=\mathbf{-0{,}0122}$ USD/jour."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 0.002}},
    },

    # key-632 : d1 = (0+0,03)/0,1414 = 0,212 faux ; numérateur = 0,035 → d1=0,2475
    # steps utilisaient la mauvaise valeur (6,81) ; stored 6,89 était correct
    "markets-derivatives-short_answer-632": {
        "prompt_mdx": (
            r"Sous la mesure $Q$, $dS=rS\,dt+\sigma S\,dW^Q$. "
            r"Call $K=100$, $S_0=100$, $r=5\%$, $\sigma=20\%$, $T=0{,}5$. "
            r"$d_1=\dfrac{0+0{,}035}{0{,}1414}=0{,}2475$, "
            r"$N(0{,}2475)=0{,}5977$. Call BSM (USD) ?"
        ),
        "value": 6.89,
        "steps_mdx": (
            r"$d_2=0{,}2475-0{,}1414=0{,}1061$, $N(0{,}1061)=0{,}5423$. "
            r"$c=100\times0{,}5977-100\,e^{-0{,}025}\times0{,}5423"
            r"=59{,}77-97{,}53\times0{,}5423=59{,}77-52{,}88=\mathbf{6{,}89}$ USD."
        ),
    },

    # ══════════════════════════════════════════════════════════════
    # CAT 2 — Arrondis non documentés
    # ══════════════════════════════════════════════════════════════

    # key-148 : 235,69 contrats → stocké 235 (plancher), steps disaient ≈236
    # Règle manquante ; on documente l'arrondi supérieur et on stocke 236
    "markets-derivatives-short_answer-148": {
        "prompt_mdx": (
            r"Un gestionnaire détient 20 M USD d'obligations de duration $D_P=7$ ans. "
            r"T-Bond futures : prix $=108$, duration livrée $D_F=5{,}5$ ans. "
            r"Nombre de contrats à vendre pour immuniser totalement "
            r"(arrondi au contrat entier supérieur) ?"
        ),
        "value": 236.0,
        "steps_mdx": (
            r"$N=\dfrac{D_P\times V_P}{D_F\times Q_F}"
            r"=\dfrac{7\times20\,000\,000}{5{,}5\times108\,000}"
            r"=\dfrac{140\,000\,000}{594\,000}=235{,}69"
            r"\to\mathbf{236}$ contrats (arrondi supérieur)."
        ),
        "payload_patch": {"tolerance": {"type": "abs", "value": 1.0}},
    },

    # ══════════════════════════════════════════════════════════════
    # CAT 3 — Exercices dépendants
    # ══════════════════════════════════════════════════════════════

    # key-647 : "même données que call" → reformulé autonome
    "markets-derivatives-short_answer-647": {
        "prompt_mdx": (
            r"Swaption : $S_0=3{,}8\%$, $K=4\%$. "
            r"Parité swaption : receveuse $=$ payeuse $-$ swap payeur. "
            r"Payeuse $=0{,}0099$ USD (notionnel unitaire), "
            r"swap payeur $=-0{,}0090$ USD. "
            r"Receveuse (USD) ?"
        ),
    },

    # key-726 : "CDO (suite)" → structure CDO rajoutée dans l'énoncé
    "markets-derivatives-short_answer-726": {
        "prompt_mdx": (
            r"CDO : pool 100 M USD. "
            r"Tranche equity 0–10 M, mezzanine 10–30 M, senior 30–100 M. "
            r"Perte cumulée du pool $=15$ M USD. "
            r"Perte subie par la tranche mezzanine (USD) ?"
        ),
    },

    # ══════════════════════════════════════════════════════════════
    # CAT 4 — Exercices triviaux (7 clairs + 6 borderline)
    # ══════════════════════════════════════════════════════════════

    # key-180 : "Vérifiez que k donne V_swap=0" → calculez k* à la monnaie
    "markets-derivatives-short_answer-180": {
        "prompt_mdx": (
            r"Swap de taux plain vanilla, notionnel 50 M USD, 3 ans, paiements annuels. "
            r"Taux spots continus : $r_1=3\%$, $r_2=3{,}5\%$, $r_3=4\%$. "
            r"Calculez le taux fixe à la monnaie $k^*$ (\%)."
        ),
        "value": 4.054,
        "steps_mdx": (
            r"Facteurs : $B_1=e^{-0{,}03}=0{,}9704$, "
            r"$B_2=e^{-0{,}07}=0{,}9324$, $B_3=e^{-0{,}12}=0{,}8869$. "
            r"$k^*=\dfrac{1-B_3}{B_1+B_2+B_3}"
            r"=\dfrac{0{,}1131}{2{,}7897}=\mathbf{4{,}054}\%$."
        ),
        "formula_patch": r"\frac{1-e^{-r_3 T_3}}{e^{-r_1 T_1}+e^{-r_2 T_2}+e^{-r_3 T_3}}",
        "payload_patch": {
            "unit": "%",
            "precision": 3,
            "tolerance": {"type": "abs", "value": 0.05},
        },
    },

    # key-335 : N(d1)=0,65 donné → paramètres BSM complets, student calcule delta
    "markets-derivatives-short_answer-335": {
        "prompt_mdx": (
            r"Call BSM : $S=60$, $K=55$, $r=5\%$, $\sigma=25\%$, $T=1$ an. "
            r"Approximation linéaire (delta) : variation du prix du call "
            r"si $\Delta S=+1$ USD (USD) ?"
        ),
        "value": 0.75,
        "steps_mdx": (
            r"$d_1=\dfrac{\ln(60/55)+(0{,}05+0{,}03125)\times1}{0{,}25}"
            r"=\dfrac{0{,}0870+0{,}0813}{0{,}25}=\dfrac{0{,}1683}{0{,}25}=0{,}673$. "
            r"$N(0{,}673)=0{,}750=\Delta_{call}$. "
            r"$\Delta c\approx0{,}750\times1=\mathbf{0{,}750}$ USD."
        ),
        "formula_patch": r"N(d_1)\times\Delta S",
        "payload_patch": {"tolerance": {"type": "abs", "value": 0.01}},
    },

    # key-337 : formule c≈0,4Sσ√T donnée dans l'énoncé → retirée, student la connaît
    "markets-derivatives-short_answer-337": {
        "prompt_mdx": (
            r"Call BSM ATM : $S=K=100$, $\sigma=20\%$, $r=5\%$, $T=0{,}25$ an. "
            r"Approximation analytique de Brenner-Subrahmanyam (USD) ?"
        ),
        "steps_mdx": (
            r"$c\approx\dfrac{S\sigma\sqrt{T}}{\sqrt{2\pi}}"
            r"\approx0{,}4\times S\sigma\sqrt{T}"
            r"=0{,}4\times100\times0{,}20\times0{,}5=\mathbf{4{,}0}$ USD."
        ),
    },

    # key-531 : données montraient croissance, réponse lisible → données décroissantes,
    # student doit connaître la propriété théorique (answer 0 = Non)
    "markets-derivatives-short_answer-531": {
        "prompt_mdx": (
            r"Base correlation CDO (valeurs implicites Bloomberg). "
            r"Tranche equity (0–3\%) : $\rho=25\%$. "
            r"Tranche mezzanine (3–6\%) : $\rho=18\%$. "
            r"La base correlation est-elle croissante ici ? (1 = oui, 0 = non)"
        ),
        "value": 0.0,
        "steps_mdx": (
            r"La base correlation doit être croissante avec le point d'attachement "
            r"(propriété théorique). Ici $25\%\to18\%$ : décroissante "
            r"$\Rightarrow$ propriété violée $\Rightarrow\mathbf{0}$ (Non)."
        ),
    },

    # key-568 : CTD = min lisible directement → paiement de protection = 100 - CTD
    "markets-derivatives-short_answer-568": {
        "prompt_mdx": (
            r"CDS sur restructuration : obligations éligibles "
            r"85 USD, 88 USD, 80 USD (pour 100 nominal). "
            r"Paiement de protection reçu par l'acheteur (USD / 100 nominal) ?"
        ),
        "value": 20.0,
        "steps_mdx": (
            r"CTD = obligation la moins chère $= 80$ USD. "
            r"Paiement $= 100 - 80 = \mathbf{20}$ USD / 100 nominal."
        ),
        "payload_patch": {"unit": "USD", "tolerance": {"type": "abs", "value": 0.5}},
    },

    # key-585 : p_u+p_m+p_d=1 trivial → E[S1] avec S0=100
    "markets-derivatives-short_answer-585": {
        "prompt_mdx": (
            r"Arbre trinomial (Hull-White) : $S_0=100$ USD, "
            r"$u=1{,}10$, $m=1{,}00$, $d=0{,}91$, "
            r"$p_u=0{,}25$, $p_m=0{,}50$, $p_d=0{,}25$. "
            r"Calculer $E[S_1]$ (USD)."
        ),
        "value": 100.25,
        "steps_mdx": (
            r"$E[S_1]=p_u\cdot S_u+p_m\cdot S_m+p_d\cdot S_d"
            r"=0{,}25\times110+0{,}50\times100+0{,}25\times91"
            r"=27{,}5+50{,}0+22{,}75=\mathbf{100{,}25}$ USD."
        ),
        "formula_patch": r"p_u u S_0 + p_m m S_0 + p_d d S_0",
        "payload_patch": {
            "unit": "USD",
            "precision": 2,
            "tolerance": {"type": "abs", "value": 0.5},
        },
    },

    # key-656 : calcul complet dans l'énoncé → formule seule, student calcule
    "markets-derivatives-short_answer-656": {
        "prompt_mdx": (
            r"Hull-White : $B_{HW}(t,T)=\dfrac{1-e^{-a(T-t)}}{a}$. "
            r"$a=0{,}1$, $T-t=2$ ans. Calculer $B_{HW}$."
        ),
        "steps_mdx": (
            r"$B_{HW}=\dfrac{1-e^{-0{,}2}}{0{,}1}"
            r"=\dfrac{1-0{,}8187}{0{,}1}=\dfrac{0{,}1813}{0{,}1}=\mathbf{1{,}813}$."
        ),
    },

    # ── Borderlines ──────────────────────────────────────────────

    # key-262 : c3=1 = réponse → nouvelles primes pour que c3 ≠ coût net
    "markets-derivatives-short_answer-262": {
        "prompt_mdx": (
            r"Butterfly spread : achat call $K_1=45$ ($c_1=7$), "
            r"vente 2 calls $K_2=50$ ($c_2=3{,}5$ chacun), "
            r"achat call $K_3=55$ ($c_3=1{,}5$). Coût net (USD) ?"
        ),
        "value": 1.5,
        "steps_mdx": (
            r"$7-2\times3{,}5+1{,}5=7-7+1{,}5=\mathbf{1{,}5}$ USD."
        ),
    },

    # key-455 : max(8,5)=8 trop évident → valeurs proches, max non immédiat
    "markets-derivatives-short_answer-455": {
        "prompt_mdx": (
            r"Chooser option : $c=6{,}3$ USD, $p=6{,}8$ USD à la date de choix $T_1$. "
            r"Valeur du chooser (USD) ?"
        ),
        "value": 6.8,
        "steps_mdx": (
            r"Chooser $=\max(c,p)=\max(6{,}3;\,6{,}8)=\mathbf{6{,}8}$ USD."
        ),
    },

    # key-469 : max = premier élément lisible → max n'est plus le premier
    "markets-derivatives-short_answer-469": {
        "prompt_mdx": (
            r"Rainbow option sur 2 actifs : payoff $=\max(A_T,\,B_T,\,K)$. "
            r"$A_T=95$, $B_T=112$, $K=108$. Payoff (USD) ?"
        ),
        "value": 112.0,
        "steps_mdx": (
            r"$\max(95,\,112,\,108)=\mathbf{112}$ USD."
        ),
    },

    # key-563 : (100-80)×5=100 bps trop rond → nouvelles valeurs + durée
    "markets-derivatives-short_answer-563": {
        "prompt_mdx": (
            r"CDS Big Bang : coupon standard $=100$ bps, "
            r"spread de marché $=73$ bps, duration risquée $=4{,}8$ ans. "
            r"Upfront reçu par l'acheteur de protection (\% du notionnel) ?"
        ),
        "value": 1.296,
        "steps_mdx": (
            r"$\text{Upfront}=(100-73)\,\text{bps}\times4{,}8\,\text{ans}"
            r"=27\times4{,}8=129{,}6\,\text{bps}\cdot\text{an}"
            r"=\mathbf{1{,}296}\%$ du notionnel."
        ),
        "payload_patch": {
            "unit": "%",
            "precision": 3,
            "tolerance": {"type": "abs", "value": 0.05},
        },
    },

    # key-566 : soustraction directe → ajoute distractor (Z-spread), student choisit ASwap
    "markets-derivatives-short_answer-566": {
        "prompt_mdx": (
            r"Z-spread d'une obligation $=176$ bps, "
            r"asset-swap spread $=168$ bps, "
            r"CDS spread $=195$ bps. "
            r"Basis (bps) ?"
        ),
        "value": 27.0,
        "steps_mdx": (
            r"$\text{Basis}=\text{CDS spread}-\text{asset-swap spread}"
            r"=195-168=\mathbf{27}$ bps (basis positive)."
        ),
    },

    # key-667 : 2ab=0,03 trivial → calculer la marge 2ab−σ² (b=6% au lieu de 5%)
    "markets-derivatives-short_answer-667": {
        "prompt_mdx": (
            r"CIR : $a=0{,}3$, $b=6\%$, $\sigma=8\%$. "
            r"Calculer la marge de la condition de Feller $2ab-\sigma^2$."
        ),
        "value": 0.0296,
        "steps_mdx": (
            r"$2ab=2\times0{,}3\times0{,}06=0{,}036$. "
            r"$\sigma^2=0{,}08^2=0{,}0064$. "
            r"$2ab-\sigma^2=0{,}036-0{,}0064=\mathbf{0{,}0296}>0$ "
            r"(condition de Feller vérifiée)."
        ),
        "payload_patch": {
            "unit": "",
            "precision": 4,
            "tolerance": {"type": "abs", "value": 0.002},
        },
    },
}


def apply_fixes() -> dict:
    report = {"fixed": [], "errors": []}

    for batch_file in sorted(BATCH_DIR.glob("batch-002-*.json")):
        data = json.loads(batch_file.read_text())
        changed = False

        for ex in data["items"]:
            key = ex["external_key"]
            if key not in FIXES:
                continue

            fix = FIXES[key]
            old_val = ex["solution"].get("value")

            if "prompt_mdx" in fix:
                ex["prompt_mdx"] = fix["prompt_mdx"]
            if "value" in fix:
                ex["solution"]["value"] = fix["value"]
            if "steps_mdx" in fix:
                ex["solution"]["steps_mdx"] = fix["steps_mdx"]
            if "formula_patch" in fix:
                ex["solution"]["formula_katex"] = fix["formula_patch"]
            if "payload_patch" in fix:
                ex["payload"].update(fix["payload_patch"])

            new_val = ex["solution"].get("value")
            report["fixed"].append({
                "key": key,
                "old_value": old_val,
                "new_value": new_val,
                "changed_prompt": "prompt_mdx" in fix,
            })
            changed = True

        if changed:
            batch_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n"
            )

    return report


def print_report(report: dict):
    fixed = report["fixed"]
    print("=" * 70)
    print(f"CORRECTIONS APPLIQUÉES : {len(fixed)}")
    print("=" * 70)
    cats = {
        "CAT 1 — Valeurs intermédiaires BSM": ["319", "351", "405", "632"],
        "CAT 2 — Arrondis":                   ["148"],
        "CAT 3 — Dépendances":                ["647", "726"],
        "CAT 4 — Triviaux":                   ["180","335","337","531","568","585","656",
                                                "262","455","469","563","566","667"],
    }
    for cat, suffixes in cats.items():
        print(f"\n  {cat}")
        for f in fixed:
            if any(f["key"].endswith(f"-{s}") for s in suffixes):
                prompt_tag = " [prompt]" if f["changed_prompt"] else ""
                val_tag = (
                    f" {f['old_value']} → {f['new_value']}"
                    if f["old_value"] != f["new_value"] else " (valeur inchangée)"
                )
                print(f"    {f['key']}{val_tag}{prompt_tag}")

    print(f"\nTOTAL : {len(fixed)} exercices corrigés")


if __name__ == "__main__":
    report = apply_fixes()
    print_report(report)
