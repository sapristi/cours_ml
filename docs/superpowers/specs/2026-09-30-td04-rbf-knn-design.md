# TD04 k-NN vs réseau RBF — Design (2026-09-30)

## 1. Contexte et objectif

- Suite logique de la partie 6 du cours « Réseau de neurones à fonction de Base Radiales » (voir `[[Entrypoint]]`), point **6.a « Relations avec les k plus proches voisins »**.
- Public : 4e année post-bac, 18h au total. Durée TP cible : ~1 séance.
- Objectif : implémenter en numpy **k-NN** (classification par vote majoritaire) et un **réseau RBF** (noyaux gaussiens + couche de sortie linéaire réutilisant la classe `MLP` de `mlp.ipynb`), puis comparer leurs frontières de décision et le rôle des hyperparamètres `k` et `σ` (sélection *dure* vs pondération *douce*).

## 2. Décisions validées avec l'utilisateur

| Sujet | Décision |
|---|---|
| Périmètre | **Notebook unique type TD03** (source de vérité avec solutions) + design + plan d'implémentation |
| Réutilisation | **Classe `MLP` copiée verbatim** de `mlp.ipynb` ; le RBF = `Phi(x)` fixe + `MLP([n_centres, 1], output_activation="sigmoid")` |
| Tâche | **Classification seulement** (un seul exercice, données non linéaires) |
| Centres RBF | **Centres = points d'entraînement** ; largeur `σ` = hyperparamètre |
| Jeu de données | **Cercles concentriques bruités** (centre −1, couronne +1) + split train/test |
| Comparaison | **Grille compacte** `k ∈ {1, 3, 10}` et `σ ∈ {0.1, 0.5, 1.0}` : frontières en sous-grille + précision train/test |
| Marqueurs | `# BEGIN` / `# END` (filtre `scripts/filter_notebook.py` → `# TODO` + `pass`) |
| Emplacement | `td_04_rbf/knn_rbf.ipynb` |
| Convention | Ligne `Z = X @ W.T + b` (comme `mlp.ipynb`), numpy + matplotlib seuls, pas de scikit-learn |

## 3. Modèle mathématique

**k-NN (classification)** : pour une requête `q`, prédiction = étiquette majoritaire des `k` voisins les plus proches au sens de la distance euclidienne `‖q − x_i‖`.

**Réseau RBF** : fonctions de base radiales (gaussiennes) centrées sur les points d'entraînement :

$$φ_j(x) = \exp\!\left(-\frac{\|x - c_j\|^2}{2σ^2}\right), \qquad c_j = x_j^{(\text{train})}$$

La couche de sortie est un neurone linéaire + sigmoïde sur les activations `Phi(x) = (φ_1(x), …, φ_m(x))` :

$$s(x) = σ\!\left(w \cdot φ(x) + b\right), \qquad \hat y = [s(x) > 0.5]$$

`MLP([m, 1], output_activation="sigmoid")` réalise exactement `s(x)` et s'entraîne par descente de gradient (coût MSE du cours), d'où la réutilisation.

**Lien conceptuel k-NN ↔ RBF** : avec `w_j = y_j` et une normalisation, `s(x)` devient une moyenne pondérée des étiquettes où *tous* les voisins comptent avec un poids gaussien décroissant en distance → « k-NN adouci » où la sélection dure des `k` voisins est remplacée par une pondération continue sur l'ensemble.

## 4. Structure du notebook

1. **Intro / lien conceptuel** (markdown) : k-NN paresseux (vote dur) vs RBF eager (pondération douce), annonce du parallèle.
2. **Imports** : `numpy`, `matplotlib`.
3. **Classe `MLP` réutilisée** : `sigmoid`/`sigmoid_prime`/`ACTIVATIONS` + classe `MLP` copiées telles quelles de `mlp.ipynb` (cellule fournie, pas un exercice).
4. **Jeu non linéaire** : `gen_circles()` + `plot_points()` + split train/test.
5. **Partie A — k-NN** :
   - `knn_predict(X, y, Xq, k)` : distances euclidiennes, `k` plus proches, vote majoritaire (**exercice** : compléter distance + vote).
   - frontière pour `k=1,3,10` + précision train/test.
6. **Partie B — RBF** :
   - `rbf_kernel` + `Phi(X, centres, σ)` (**exercice** : compléter le noyau et la matrice).
   - entraînement `MLP([m,1])` sur `(Phi(X_train), y_train)` via `fit_batch`, prédiction au seuil 0.5.
   - frontière pour `σ=0.1,0.5,1.0` + précision train/test.
7. **Partie C — Comparaison** : sous-grille 2×3 de frontières (ligne du haut = k-NN pour `k=1,3,10` ; ligne du bas = RBF pour `σ=0.1,0.5,1.0`), tableau de précision train/test, discussion lissage / sous/sur-apprentissage, coût paresseux vs eager.

## 5. Données & exercices

- `gen_circles(n=400, noise=0.15, seed=0)` : classe 0 = disque centre `r ≈ 0.5`, classe 1 = anneau `r ≈ 1.0`, bruit gaussien angulaire/radial, labels `{0,1}`. Split aléatoire 70/30.
- **Exercice 1** (k-NN) : compléter `knn_predict` — calcul des distances et vote majoritaire.
- **Exercice 2** (RBF) : compléter `rbf_kernel` et `Phi`.
- **Exercice 3** (RBF) : construire `Phi_train`/`Phi_test`, instancier et entraîner `MLP`, prédire au seuil.
- **Exercice 4** (comparaison) : interpréter l'effet de `k` et `σ` sur le lissage.

## 6. Outils de visualisation

- `plot_points(X, y)` : nuage des classes (matplotlib).
- `plot_decision(model_or_predict, X, y, grid)` : contourf de la frontière + points.
- Sous-grille finale 2×3 : ligne du haut k-NN (`k=1,3,10`), ligne du bas RBF (`σ=0.1,0.5,1.0`), plus un tableau de précision train/test.

## 7. Livrables

- `td_04_rbf/knn_rbf.ipynb` (notebook unique, source de vérité avec solutions, zones `# BEGIN`/`# END`).
- Aucune modification de `scripts/filter_notebook.py` ni `jupyter_lite_config.json` (hors scope, gérés par l'utilisateur).

## 8. Hors scope

- Pas de régression (classification seule, décision utilisateur).
- Pas de l'algorithme de Lloyd / k-means pour les centres (partie 6.b du cours).
- Pas de scikit-learn, pas de validation croisée, pas de noyau non gaussien.
- Pas d'énoncé Obsidian `.md` séparé.

## 9. Critères de succès

- Le notebook corrigé s'exécute de bout en bout (numpy + matplotlib seuls).
- k-NN : frontières pour `k=1,3,10` affichées, précision train/test calculée.
- RBF : `Phi` correcte (diagonale ≈ 1), `MLP([m,1])` entraîné, frontières pour 3 valeurs de `σ`, précision train/test.
- La sous-grille de comparaison rend visible le parallèle k ↔ σ (petit → dentelé/sur-apprend, grand → lissé/sous-apprend).
- Les zones `# BEGIN`/`# END` couvrent uniquement `knn_predict`, `rbf_kernel`/`Phi` et l'assemblage du RBF.
