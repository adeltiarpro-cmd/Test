#!/bin/bash
# Charge les lots d'entretiens finance (batch-100 à batch-423, fit compris) dans Supabase, puis met à jour le rapport de couverture.
cd "$(dirname "$0")/ingest" || exit 1
for f in canonical/batch-[1234]??-*.json; do
  npm run load -- --file "$(basename "$f")" || echo "ECHEC : $f"
done
npm run report
echo
echo "Terminé. Tu peux fermer cette fenêtre."
