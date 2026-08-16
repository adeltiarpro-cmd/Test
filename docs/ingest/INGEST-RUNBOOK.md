# INGEST-RUNBOOK — à coller en tête de CHAQUE session d'ingestion d'un livre/PDF

Session de **chat normal** (pas forcément Claude Code) — tu vas uploader un
PDF ou un extrait, et j'en sors un lot JSON canonique. Une session = un livre
ou un chapitre, jamais plus, pour rester dans un budget de contexte raisonnable
et garder la qualité du parsing élevée.

## Contrat de sortie (rappel, cf. `/ingest/README.md` du repo pour le détail)

Un fichier JSON par lot :
```json
{
  "source": { "kind": "book|umbrex|biws|own", "title": "...", "external_key": "slug-stable" },
  "track": "markets|corpfin|consulting|gmat|math",
  "module": "slug-du-sous-chapitre",
  "items": [
    {
      "external_key": "slug-source-chXX-qYY",
      "type": "mcq|numeric|formula_cloze|excel_model|statement_interactive|graph_fill|case_structuring|market_sizing|case_math|short_answer",
      "difficulty": 1-5,
      "source_ref": "p.XXX, Q.Y",
      "concepts": ["slug-concept-1", "slug-concept-2"],
      "prompt_mdx": "...",
      "payload": { /* dépend du type, cf. formes ci-dessous */ },
      "solution": { /* idem */ }
    }
  ]
}
```

## Règles

1. **`external_key` stable et unique** : `<slug-source>-<chapitre>-<numéro>`.
   Ne jamais réutiliser un `external_key` pour deux items différents — le
   loader fait un upsert dessus, une collision écraserait un item existant.
2. **Choisis le `type` le plus adapté au contenu**, pas le plus simple à
   écrire. Un exercice de calcul de duration est `numeric`, pas `mcq` avec
   4 choix inventés.
3. **`concepts`** : réutilise les slugs déjà connus si possible (calcul
   stochastique, algèbre linéaire, analyse non linéaire pour les rattachements
   math). Un slug nouveau est acceptable — il sera créé automatiquement côté
   loader avec un flag `needs_review`.
4. **Ne reproduis jamais le texte du livre verbatim au-delà de ce qui est
   nécessaire pour poser l'exercice.** Reformule les énoncés dans tes propres
   mots, garde `source_ref` pour la traçabilité plutôt que de citer la page.
5. **Découpe par chapitre**, pas par livre entier — demande-moi de continuer
   sur le chapitre suivant dans une nouvelle session plutôt que d'essayer de
   tout faire d'un coup.
6. Si un exercice ne rentre proprement dans aucun des 10 types, dis-le
   explicitement plutôt que de forcer un mauvais type.

## Formes `payload`/`solution` par type

(identiques à `STEP-02-zod-schemas.md` — redemande-les-moi si tu ne les as pas
sous la main, je les régénère depuis `packages/schemas/exercises.ts`.)

## Fin de session

Je te donne un bloc JSON complet et valide. Tu le colles dans
`/ingest/canonical/<lot>.json` dans ton repo, puis tu lances
`validate.ts` et `load.ts`. Aucune écriture directe en base depuis cette
session de chat — tout passe par le pipeline pour garder la validation Zod.
