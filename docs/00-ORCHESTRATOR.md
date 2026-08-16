# Prompt général — à coller en tête de CHAQUE nouvelle session de build

Tu travailles sur une plateforme de formation perso (finance de marché, finance
corpo, consulting, GMAT, math) — Next.js + Supabase + Vercel. Le spec complet
est dans `docs/00-MASTER-SPEC.md`, mais **tu ne le relis pas en entier à chaque
session** : c'est justement ce que ce système évite.

## Règle de fonctionnement, dans cet ordre, avant toute autre action

1. Lis `docs/PROGRESS.md` en entier — c'est un journal court, pas du code.
   Il te dit ce qui existe déjà et comment.
2. Lis `docs/CONTEXT-MAP.md`, repère la première ligne non cochée.
3. Ouvre **uniquement** `docs/steps/STEP-XX-*.md` correspondant. C'est ton
   unique périmètre pour cette session — pas le master spec en entier, pas le
   reste du repo au-delà de ce que le step file te dit explicitement de lire.
4. Si le step file te demande de lire d'autres fichiers du repo (migrations
   existantes, schémas déjà écrits...), lis-les. Rien d'autre. Ne relis pas un
   fichier déjà stable "pour être sûr" — si `PROGRESS.md` dit qu'il est fait
   et validé, fais-lui confiance.
5. Fais le travail décrit dans "Tâches". Respecte "Hors périmètre" à la
   lettre — ce n'est pas une suggestion, c'est ce qui évite à la session
   suivante de devoir tout relire pour comprendre ce qui a débordé.
6. Avant de terminer, ajoute une entrée à `docs/PROGRESS.md` au format donné
   en bas du step file. Tu n'édites jamais une entrée précédente.
7. Coche la ligne correspondante dans `docs/CONTEXT-MAP.md`.

## Si tu n'as pas fini dans cette session

Le budget de contexte peut se remplir avant la fin d'un step, surtout aux
steps 6-9. Ne force pas, n'improvise pas la suite en bâclant. Écris dans
`PROGRESS.md` un statut `EN COURS` avec un point de reprise précis, par ex. :

> STEP-01 — EN COURS. Fait : tables tracks/modules/lessons/concepts.
> Reste : concept_edges, RLS, seed. Reprendre par la RLS.

La session suivante lira ça et reprendra exactement là, sans tout refaire.

## Règles fixes

- Jamais un step "par avance" parce que ça semble logique — l'ordre encode
  des dépendances réelles (ex. : le runner d'exos au step 5 a besoin des
  schémas Zod du step 2).
- L'ingestion de contenu (parsing de PDF/XLS en exos) n'est **pas** un step
  numéroté — c'est un travail récurrent qui utilise `docs/ingest/INGEST-RUNBOOK.md`,
  une session par livre/source, en parallèle des steps de build dès que
  STEP-03 est terminé. Voir `CONTEXT-MAP.md`.
- Ne jamais coller le contenu d'un PDF entier dans un prompt de build —
  ça n'a rien à faire dans une session de code, ça appartient à une session
  d'ingestion dédiée.
