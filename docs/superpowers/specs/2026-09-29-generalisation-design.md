# Design - Généralisation (par cœur vs généraliser, définition, validation intuitive)

Date: 2026-09-29
Statut: validé par l'utilisateur (approche A)
Fichier cible: `cours_ml/1 - Qu'est-ce qu'apprendre ?.md`, section 3 existante

## 1. Contexte et contraintes

- Public: 4e année post-bac, 18h au total, pas de prérequis ML.
- Contraintes validées: niveau intuitif seulement (pas de Hoeffding, VC, PAC), volume court (compléter section 3, 20-30 min), exemple support régression polynomiale.
- Conventions: Obsidian vault, liens wiki `[[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`, frontmatter YAML strict inchangé.
- Articulation: prépare partie 4 (courbe en U, complexité) et partie 7 (surapprentissage) sans les traiter. Évite doublon.

## 2. Emplacement et structure (validé)

Pas de nouveau fichier. Compléter Section 3 `Apprentissage supervisé : tentative de généralisation`:

- 3.1 Apprendre par cœur vs généraliser
- 3.2 Qu'est-ce que généraliser ? (définition intuitive train/test)
- 3.3 Comment valider ? (protocole intuitif hold-out)

## 3. Contenu (validé)

### 3.1 Par cœur vs généraliser
- Par cœur = erreur train 0 mais fragile au bruit. Illustration: polynôme degré 15 qui passe par tous les points bruités.
- Généraliser = capter la tendance. Illustration: degré 2-3, petite erreur train mais stable.
- Sous-apprentissage mention rapide: degré 1, erreur partout.

### 3.2 Qu'est-ce que généraliser ?
- Définition: erreur faible sur données non-vues, pas sur train.
- Vocabulaire: erreur train vs erreur test, split, données non-vues.
- Schéma split train/test.

### 3.3 Validation intuitive (pas de théorie formelle)
- Protocole hold-out: couper jeu en train/test, entraîner sur train, juger sur test verrouillé jusqu'à la fin.
- Règle: jamais juger sur train seul, 100% train ne prouve rien.
- Annonce: validation croisée et courbe en U détaillées en partie 7, complexité en partie 4.

Interprétation de `validations théoriques`: volontairement restreint à validation empirique par protocole. Pas de bornes.

## 4. Forme et pédagogie (validé)

- Callouts: `[!example]` pour polynômes, `[!info]` pour définition généraliser, `[!danger]` pour `train seul ment`.
- Visuels: 1 figure régression polynomiale (degrés 1/4/15 sur mêmes points bruités) + 1 schéma split train/test, style cohérent avec `assets/04-*` partie 4.
- Exercice: 1 question `pourquoi 100% train ne prouve rien ? Donner un contre-exemple par cœur`.
- Liens: vers `[[3- Données non linéairement séparables]]` et partie 7 Surapprentissage. Réutiliser image existante section 3 si possible.
- Anti-contresens: séparable train != bon, plus complexe != meilleur, test ne sert pas à régler le modèle.

## 5. Hors scope

- Pas de code Python, pas de script génération figure dans ce design (option C écartée).
- Pas de biais-variance formel, pas de validation croisée détaillée, pas de courbe en U complète.
- Pas de modification frontmatter, Entrypoint, autres parties.

## 6. Critères de succès

- Section 3 lisible en 20-30 min, 1-2 pages Obsidian rendues.
- Étudiant sait définir généraliser et expliquer protocole hold-out.
- Aucune formule au-delà de moyenne d'erreur.
- Rendu Obsidian sans lien cassé.
