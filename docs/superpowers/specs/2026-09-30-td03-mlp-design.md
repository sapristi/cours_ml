# TD03 Perceptron multi-couche (MLP + rétropropagation) — Design (2026-09-30)

## 1. Contexte et objectif

- Suite logique de `cours_ml/4 - Rétropropagation.md` (récemment basculé en convention **colonne** : $Z = W X$, $X$ vecteur colonne, dérivées avec transposées).
- Public : 4e année post-bac, 18h au total. Durée TP cible : ~2 séances (implémentation + XOR + fonctions 1D/2D).
- Objectif : implémenter un MLP numpy à partir des formules du cours, l'utiliser sur XOR (classification) puis sur des fonctions à 1 et 2 dimensions (régression), avec split train/test, early stopping, et visualisation des prédictions.

## 2. Décisions validées avec l'utilisateur

| Sujet | Décision |
|---|---|
| Convention vectorielle | **Colonne** `h = W@x + b`, backprop avec transposées (aligné cours 4 mis à jour + TD02) |
| Architecture | Classe **générique** `MLP(sizes=[d, h1, …, k])` ; XOR en 2 couches, fonctions en plus profond |
| Activation | **Paramétrable** : `sigmoid` (défaut) + `tanh`, dérivées fournies ; bonus comparaison |
| Apprentissage | **Deux méthodes séparées** `fit_batch` (GD batch) et `fit_online` (SGD), toutes deux avec early stopping |
| Visualisation | **matplotlib 2D** (courbe 1D, frontière XOR) + **plotly 3D** (surface 2D→1D) |
| Emplacement | `td_03_backpropagation/mlp.ipynb` |
| Format | **Notebook unique** (source de vérité avec solutions) ; `# SKIP` seul marqueur ; pas de `# EXPORT` ; pas d'énoncé `.md` séparé |
| Filtre/config | **Non modifiés** par l'auteur (l'utilisateur adapte `filter_notebook.py` pour exporter toutes les cellules et met à jour `jupyter_lite_config.json`) |

## 3. Modèle mathématique (convention colonne)

Pour un batch $X:(N,d)$ :

- Forward, $A_0 = X$ ; pour chaque couche $l$ ($W_l:(n_{out},n_{in})$, $b_l:(n_{out},)$) :
  $$Z_l = A_{l-1} W_l^T + b_l, \qquad A_l = g_l(Z_l)$$
- Coût (moyenne MSE) : $L = \tfrac12 \, \text{mean}((Y-T)^2)$, $Y = A_L$.
- Backprop :
  $$\delta_L = (Y - T) \odot g'_L(Z_L)$$
  $$\delta_l = (\delta_{l+1} \, W_{l+1}) \odot g'_l(Z_l)$$
  $$\frac{\partial E}{\partial W_l} = \frac{1}{N}\,\delta_l^T A_{l-1}, \qquad \frac{\partial E}{\partial b_l} = \frac{1}{N}\sum_i \delta_l$$

Pour un échantillon unique, $N=1$ (le même code batch marche en passant `X[i:i+1]`). Ceci rend `fit_online` trivial : boucle sur les échantillons en réutilisant la même passe avant/arrière.

Formules cohérentes avec le cours : $\frac{dE}{dW_n}=(Y_n-T)\,A'(Z_n)\,Y_{n-1}^T$ (somme sur le batch puis moyennée).

## 4. Structure de la classe `MLP`

```python
class MLP:
    def __init__(self, sizes, activation="sigmoid", output_activation="linear"): ...
        # self.Ws = [W_l], self.bs = [b_l]
        # activation   : appliquée aux couches cachées (sigmoid | tanh)
        # output_activation : appliquée à la sortie (linear | sigmoid | tanh)
    def forward(self, X): -> (liste des A_l, liste des Z_l)   # X:(N,d)
    def backward(self, X, y): -> liste de (dW_l, db_l)
    def predict(self, X): -> A_L
    def mse(self, X, y): -> float
    def _step(self, X, y, lr):   # un pas de GD (batch complet)
    def fit_batch(self, X, y, X_test=None, y_test=None, lr=..., epochs=..., patience=...): -> history
    def fit_online(self, X, y, X_test=None, y_test=None, lr=..., epochs=..., patience=...): -> history
```

- Poids initialisés petits aléatoires (`rng.normal(0, 0.5)` ou Xavier simplifié), biais à 0.
- `linear` = identité, dérivée `1`.
- XOR : `output_activation="sigmoid"` (squash vers 0/1). Fonctions 1D/2D : `output_activation="linear"` (défaut).
- `history` = `{"train": [...], "test": [...]}` (MSE par epoch) pour tracer la courbe d'apprentissage.
- Early stopping : garder une copie des meilleurs poids (min MSE test), restaurer en fin ; arrêt après `patience` epochs sans amélioration.

## 5. Données & exercices

1. **Activations** : coder `sigmoid`, `sigmoid_prime`, `tanh`, `tanh_prime`.
2. **`forward`** : passe avant générique.
3. **`backward`** : gradients par couche.
4. **`fit_batch` + `fit_online`** : boucle d'apprentissage + early stopping + historique.
5. **XOR** : $X=\{(0,0),(0,1),(1,0),(1,1)\}$, cibles 0/1, `sizes=[2,4,1]`, sigmoïde, seuil 0.5. Attendu 100 % sur les 4 points. Courbe de frontière 2D.
6. **Fonction 1D** : $f(x)=\sin(x)$ sur $[-\pi,\pi]$, $N\approx200$ points bruités, split 80/20 aléatoire. `sizes=[1,16,16,1]`, `activation="tanh"`, sortie linéaire. Tracer (a) erreurs train/test vs epoch (visualise l'early stopping), (b) prédiction vs vraie courbe (matplotlib 2D).
7. **Fonction 2D** : $f(x_1,x_2)=\sin(x_1)\cos(x_2)$ sur $[-3,3]^2$, split train/test. `sizes=[2,16,16,1]`, `activation="tanh"`, sortie linéaire. Surface prédite vs vraie (plotly `go.Surface`).
8. **Bonus** : comparer sigmoid/tanh et batch/online (vitesse, qualité, surapprentissage).

## 6. Outils de visualisation

- `plot_decision_2d(model, X, y)` : contour de la sortie sigmoïde + points (matplotlib), pour XOR.
- `plot_fit_1d(model, X, y, X_true, y_true)` : nuage + courbe prédite sur grille dense (matplotlib).
- `plot_history(history)` : erreurs train/test vs epoch (matplotlib).
- `plot_surface_3d(model, f, Xgrid)` : surfaces vraie et prédite côte à côte (plotly). Cellule `%pip install plotly` en tête (JupyterLite pyodide).

## 7. Livrables

- `td_03_backpropagation/mlp.ipynb` (unique notebook, source de vérité avec solutions, `# SKIP` pour les zones à compléter).
- Aucune modification de `scripts/filter_notebook.py` ni de `jupyter_lite_config.json` (hors scope, gérés par l'utilisateur).

## 8. Hors scope

- Pas de softmax/cross-entropy (coût MSE du cours uniquement).
- Pas de mini-batch (seulement batch complet et SGD en ligne).
- Pas de momentum, régularisation, dropout, ni scikit-learn.
- Pas d'énoncé Obsidian `.md` séparé.

## 9. Critères de succès

- Le notebook corrigé s'exécute de bout en bout (numpy seul + plotly installé à la volée).
- XOR : 100 % sur les 4 points, frontière affichée.
- Fonction 1D : courbe d'erreur train/test montrant l'arrêt, prédiction collant à $\sin(x)$.
- Fonction 2D : surface 3D prédite proche de la vraie.
- Les zones `# SKIP` laissent aux étudiants l'implémentation de `forward`, `backward`, `fit_*` (cœur du TP).
