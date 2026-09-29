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
