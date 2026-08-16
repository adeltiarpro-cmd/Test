# STEP-04 — Design system (skill obligatoire) + primitives UI

## Contexte à lire
Le skill `ui-ux-pro-max` lui-même. Rien d'autre dans le repo — ce step est
indépendant des précédents.

## Objectif
Générer et persister le design system via le skill, puis construire les
primitives UI de base. Stack détectée : `nextjs` — vérifie via `package.json`,
ne suppose jamais.

## Tâches
1. Vérifie si `design-system/prep-platform/MASTER.md` existe déjà. Si oui,
   **lis-le et ne régénère pas** sans `--force`.
2. Sinon, génère :
```
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" \
  "education learning platform finance quantitative content-dense focused study" \
  --design-system --persist -p "Prep Platform" --output-dir "<racine-du-repo>" \
  --variance 3 --motion 3 --density 8
```
   Dials : `variance 3` (l'interface s'efface devant le contenu pendant une
   session de calcul), `motion 3` (micro-interactions seulement), `density 8`
   (tableaux financiers, grilles, graphes — il faut de la matière à l'écran).
3. Overrides de page : `--page "model-workshop"`, `--page "graph-explorer"`,
   `--page "exam-session"`.
4. Recherches ciblées minimum :
```
--domain ux "forms inline-validation error-clarity focus-management"
--domain ux "keyboard navigation accessibility contrast"
--domain chart "financial time-series dashboard"
--domain typography "technical data numeric tabular"
--domain icons "navigation outline"
--stack nextjs "suspense streaming bundle rerender"
```
5. Construis les primitives : Button, Input, Card, Table, Badge, Callout —
   contraste 4.5:1, cibles tactiles 44×44px, focus rings jamais supprimés,
   `aria-label` sur tout icon-only, **icônes SVG uniquement, aucun emoji**,
   police à chiffres tabulaires partout où des nombres s'alignent (états
   financiers, grilles, résultats).

## Hors périmètre
Pas de pages complètes, juste les primitives + le design system persisté.

## Definition of done
`design-system/prep-platform/MASTER.md` existe et est lisible. Les primitives
sont rendues dans une page `/style-guide` de vérification, navigable au clavier.

## À écrire dans PROGRESS.md
```
## <date> — STEP-04 — Design system
STATUT: FAIT
FAIT: design system persisté + 3 overrides de page + primitives (Button/Input/Card/Table/Badge/Callout)
FICHIERS CLÉS: design-system/prep-platform/, components/ui/
```
