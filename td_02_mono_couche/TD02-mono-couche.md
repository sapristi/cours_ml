---
titre: TD02 - Reseau mono-couche multi-sorties
cours: "[[Entrypoint]]"
partie: TD02
statut: draft
Contexte: |-
  4e annee post-bac, 50 min + 15 min bonus.
  Suite de [[2 - Perceptron]].
  Prepare [[3- Données non linéairement séparables]].
---

> [!abstract] Objectif
> Passer d'un neurone a une couche de 3 perceptrons : `argmax(W.x+b)`, Rosenblatt multi-classes, visualisation des 3 droites, echec controle, bonus lettres 5x5.

# 1. Couche mono-couche



> [!example] Modele
> `h = W.x + b`, `W:(KxD)`, `y = argmax h`. Si `pred != target` : `W[target]+=r.x`, `W[pred]-=r.x`, idem biais. `r=0.1`.

Algorithme : Rosenblatt multi-classes
On dispose de n exemples $(x^j, t^j)$ avec $x^j ∈ ℝ^d$ et $t^j ∈ {0, …, K−1}$ (ici K = 3 classes).
1. Choisir un pas d'apprentissage r (par exemple r = 0.1).
2. Initialiser tous les poids à 0 : W = 0 (matrice K×d), b = 0 (vecteur de taille K).
3. Pour chaque exemple x^j :
- Calculer les K scores : $h_k = W[k]·x^j + b[k]$ pour k = 0 … K−1.
- Prédire la classe gagnante : $p^j$ = $argmax_k  h_k$.
- Si $p^j == t^j$, ne rien faire.
- Sinon, corriger les deux neurones concernés :
- renforcer le bon : $W[t^j] += r·x^j, b[t^j] += r$;
- punir le mauvais gagnant : $W[p^j] −= r·x^j, b[p^j] −= r$.
1. Recommencer l'étape 3 pendant au plus epochs passages (par exemple 50), en s'arrêtant dès qu'un passage complet ne fait aucune erreur.
Si les données sont linéairement séparables, l'algorithme converge vers 100 % (comme le perceptron simple du TD01). Sinon — c'est le cas du piège central — il oscille indéfiniment et ne converge jamais : c'est le signal que le modèle mono-couche est trop pauvre.

### [!faq] Exercice 1 — Coder `CoucheMonoCouche`
Completer `predict`, `learn_one`, `train` dans `mono_couche.ipynb` (cellule classe). Verifier 100% sur `X_train`.

# 2. Blobs + piege

### [!faq] Exercice 2 — Succes separable
Entrainer, tracer `plot_frontieres`. Pourquoi regions convexes ?

> [!danger] Exercice 3 — Piege central
> Ajouter `X_dur`. Constater oscillation, <100%. Lien avec XOR du TD01 ? Pourquoi aucun `W` ne marche ?

# 3. Bonus lettres

### [!faq] Exercice 4 — A/B/C en 5x5
Reutiliser la meme classe en 25D. Visualiser `W` en 5x5. Tester flip 5 px. Lien surapprentissage [[3- Données non linéairement séparables]] §4 ?
