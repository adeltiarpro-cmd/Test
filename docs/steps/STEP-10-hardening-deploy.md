# STEP-10 — Durcissement et déploiement

## Contexte à lire
Revue transverse — pas de fichier spécifique à lire en amont, ce step audite
ce qui existe déjà.

## Objectif
Fermer la boucle avant usage réel avec les amis.

## Tâches
1. Audit RLS complet : tente un accès cross-user en test sur chaque table
   scoping user (`attempts`, `review_states`, `concept_mastery`, `profiles`) —
   doit échouer systématiquement.
2. Flow d'invitation bout en bout : email non listé dans `invitations` →
   création de compte refusée, avec message clair.
3. Variables d'environnement Vercel documentées dans `.env.example`.
4. Checklist du skill : lis `references/pro-rules.md` de `ui-ux-pro-max` et
   déroule la Pre-Delivery Checklist.
5. Smoke tests des 10 types d'exos sur `/session` (un passage minimal par
   type, pas une suite exhaustive).
6. Vérification accessibilité sur les pages critiques (`/session`,
   `model-workshop`) : contraste, navigation clavier complète, focus rings
   visibles.

## Hors périmètre
Pas de nouvelle feature — uniquement audit et correction de ce qui existe.

## Definition of done
Checklist cochée. Déploiement Vercel accessible, testé avec au moins 2
comptes invités réels (toi + un ami).

## À écrire dans PROGRESS.md
```
## <date> — STEP-10 — Durcissement et déploiement
STATUT: FAIT
FAIT: audit RLS passé, invitations testées, checklist skill déroulée, déployé sur Vercel avec 2 comptes tests
```
