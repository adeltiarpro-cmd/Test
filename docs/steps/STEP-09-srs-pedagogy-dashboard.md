# STEP-09 — SRS, dispositifs pédagogiques, dashboard, vue Math

## Contexte à lire
Migrations `review_states`/`concept_mastery`/`module_targets`/`concept_edges`
(STEP-01), le runner générique (STEP-05, pour brancher la notation de confiance).

## Objectif
Implémente FSRS (ou SM-2) et les 8 dispositifs pédagogiques suivants —
recopiés ici pour ne pas avoir à relire la section 7 du master spec :

1. **Hiérarchie à 3 niveaux** : la barre de progression vit au niveau
   sous-chapitre (`modules.level = 1`), pas au niveau chapitre.
2. **Marge de progression explicite** : toujours afficher *actuel vs
   `target_mastery`* (ex. "72% — objectif 85%"), jamais un % brut. En dessous
   de `min_exercises` tentatives, afficher "pas assez de données".
3. **Portes souples** : ne jamais bloquer l'accès au sous-chapitre suivant
   sous le seuil, juste le signaler visuellement.
4. **Intercalage (interleaving)** : le constructeur de session ne pioche
   jamais tous les items dus dans un seul sous-chapitre — il mélange les
   modules dus.
5. **Notation de confiance** (1=au hasard, 2=incertain, 3=sûr) à chaque
   réponse, en plus de juste/faux — un "juste mais peu confiant" doit revenir
   plus vite dans le SRS qu'un "juste et sûr".
6. **Détection de leech** : `review_states.lapses` > 3 sur un même exercice →
   arrêter de le représenter tel quel, proposer le prérequis math lié
   (`concept_edges`) ou une reformulation.
7. **Rappel hebdomadaire** : fonction planifiée (Supabase Cron ou Vercel Cron)
   qui calcule chaque lundi les items dus + les 3 concepts les plus faibles,
   affichés en tête de dashboard. In-app suffit, pas besoin d'email.
8. **Format qui suit la maîtrise** : `mcq` pour un concept frais, formats à
   rappel libre (`numeric`, `formula_cloze`, `graph_fill` en `recall`) une
   fois `concept_mastery` au-dessus du seuil — sauf GMAT, qui reste en `mcq`
   puisque c'est le format réel de l'examen.

## Tâches
- SRS complet, branché sur la notation de confiance du point 5.
- Dashboard : items dus, 3 concepts faibles, série d'activité, progression
  par filière avec la marge explicite du point 2.
- Vue Math : graphe de prérequis (`concept_edges`), concepts bloquants
  surlignés selon les échecs réels de l'utilisateur.
- Session builder avec interleaving (point 4) et mode examen chronométré
  (GMAT).

## Definition of done
Dashboard affiche items dus + 3 concepts faibles. Une session piochée mélange
plusieurs modules dus, vérifiable. Confiance demandée à chaque soumission. Un
exercice à 4 lapses déclenche la proposition du prérequis math lié.

## À écrire dans PROGRESS.md
```
## <date> — STEP-09 — SRS + pédagogie + dashboard
STATUT: FAIT
FAIT: FSRS + 8 dispositifs pédagogiques + dashboard + vue Math + session builder avec interleaving
FICHIERS CLÉS: lib/srs/, app/dashboard/, app/math/
```
