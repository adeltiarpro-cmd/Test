# STEP-11 — Formulaire admin pour saisie manuelle d'exercices

## Contexte à lire
`packages/schemas/exercises.ts` (STEP-02, réutilisé tel quel — pas de duplication
de validation), le composant `ExerciseRunner` (STEP-05, pour l'aperçu), les
migrations existantes (pour connaître les tables cibles). Ne touche à aucune
migration existante — si une colonne manque, ajoute une **nouvelle** migration,
n'édite jamais les 10 fichiers déjà appliqués.

## Objectif
Une deuxième porte d'entrée vers `exercises`, complémentaire à `/ingest` :
saisie directe dans l'app, pour tes propres questions (cas d'entretien vécus,
notes de cours reformulées, contenu généré en session de chat) — sans jamais
passer par un fichier JSON à la main. Les deux portes convergent sur le même
schéma (`ExerciseSchema`), donc la même garantie de structure, juste deux
points d'entrée différents : lot de fichier (`/ingest`) vs un item à la fois
(ce formulaire).

## Tâches

1. **Migration additive** (nouveau fichier, ex. `20240011_admin_flag.sql`) :
   ajoute `is_admin boolean not null default false` sur `profiles`. Passe ton
   propre compte à `true` manuellement via le SQL Editor une fois la migration
   appliquée — ce n'est pas dans le seed, c'est une action à faire toi-même,
   une fois.

2. **Route protégée** `/admin/exercises/new` : côté serveur, vérifie
   `profiles.is_admin = true` pour le compte courant avant de rendre quoi que
   ce soit — un utilisateur authentifié non-admin doit recevoir un 403, pas
   juste un lien caché côté UI.

3. **Formulaire dynamique** : un sélecteur de `type` (les 10 valeurs de
   `exercise_type`), qui affiche ensuite le sous-formulaire correspondant à
   la forme `payload`/`solution` de ce type précis (réutilise les schémas Zod
   du STEP-02 pour générer les champs et valider à la volée, ne réécris pas
   les 10 formes à la main dans le formulaire).

4. **Génération automatique de `external_key`** : les entrées manuelles n'ont
   pas de référence de page comme les livres — génère
   `manual-<uuid>` côté serveur à la soumission. Crée (ou réutilise s'il
   existe déjà) une ligne `sources` de `kind: 'own'`, titre "Mes propres
   exercices", et rattache chaque entrée manuelle à cette source via
   `source_id`. Un champ texte libre optionnel `source_ref` reste disponible
   pour une note perso (ex. "Entretien Goldman, mars 2026").

5. **Aperçu avant publication** : bouton "Aperçu" qui rend le formulaire
   soumis à travers le vrai `ExerciseRunner` (mode lecture, pas de
   soumission possible) — tu dois voir exactement ce que verra un utilisateur
   avant de valider.

6. **Écriture directe** : à la validation, valide côté serveur avec
   `ExerciseSchema.parse()` (jamais confiance au seul client), puis insert
   direct dans `exercises` via `service_role` (server action / route API,
   jamais la clé service_role exposée côté client).

7. **Liste + édition simple** : une page `/admin/exercises` listant les
   entrées de la source `own`, avec édition et suppression. Pas de
   recherche/filtre avancé à ce stade — un tableau simple suffit pour du
   contenu perso à faible volume.

## Hors périmètre
Pas d'import en masse depuis ce formulaire (ça reste le rôle de `/ingest`).
Pas de CMS complet (pas de recherche, pas de tags avancés, pas d'historique
de versions). Pas de ré-audit RLS complet des autres tables — seul le nouveau
chemin d'écriture (`is_admin`) a besoin d'être vérifié ici.

## Definition of done
- Un compte non-admin qui tente d'accéder à `/admin/exercises/new` reçoit un
  refus (403), vérifié avec le deuxième compte de test créé au STEP-01.
- Une saisie manuelle des 10 types passe par le formulaire, l'aperçu rend
  correctement via `ExerciseRunner`, et l'item validé apparaît en base avec
  un `external_key` unique et un `source_id` pointant vers la source `own`.
- La liste `/admin/exercises` reflète bien les entrées ajoutées, édition et
  suppression fonctionnelles.

## À écrire dans PROGRESS.md
```
## <date> — STEP-11 — Formulaire admin (saisie manuelle)
STATUT: FAIT
FAIT: colonne is_admin sur profiles, route /admin/exercises/new protégée,
formulaire dynamique par type (10/10) avec aperçu via ExerciseRunner,
écriture directe validée server-side, liste + édition sur /admin/exercises
DÉCISIONS: <toute décision de scope, ex. si tu as ajouté des champs perso>
FICHIERS CLÉS: supabase/migrations/20240011_admin_flag.sql,
app/admin/exercises/, lib/admin/
```
