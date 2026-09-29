# TD02 Mono-couche multi-sorties — Design (2026-09-29)

## 1. Contexte
- Suite de `cours_ml/2 - Perceptron.md` (TD01 : 1 neurone, AND OK, XOR KO).
- Prépare `cours_ml/3- Données non linéairement séparables.md` (§1 limite linéaire, §4 surapprentissage) et futur MLP (partie 5).
- Public : 4e année post-bac, 18h au total. Durée TP : 50 min cœur + 15 min bonus.
- Conventions repo : Obsidian vault, frontmatter YAML strict, liens `[[...]]`, callouts `[!faq]`, `[!example]`, `[!danger]`, `[!note]`.

## 2. Architecture imposée
Mono-couche multi-sorties, sans cachée :
- `x in R^d` → `h = W·x + b`, `W : (K x d)`, `b : (K)`, `K = nb classes`.
- Décision : `y = argmax_k h_k` (pas K Heaviside indépendants).
- Apprentissage : Rosenblatt multi-classes vectorisé, `r = 0.1` :
  - si `pred != target` : `W[target] += r·x`, `b[target] += r`, `W[pred] -= r·x`, `b[pred] -= r`.
  - sinon : rien.
- Justification : généralisation directe du TD01 Exo 4-6, même preuve d'oscillation si non-séparable.

## 3. Cœur A — 3 blobs 2D + piège (recommandé)
**Données :** 2D, 25 pts/classe, centres (-2,-2), (2,-2), (0,2), bruit gaussien σ=0.6. Séparables par construction.
- Exo 1 (20 min) : compléter `CoucheMonoCouche` numpy (`predict`, `learn_one`, `train(epochs=50)`).
- Exo 2 (15 min) : train → 100% train. Tracer points + 3 droites `w_k·x+b_k=0` + fond argmax. Question : pourquoi régions convexes ?
- Exo 3 (15 min) : ajout 15 pts classe 0 en (0,0) → chevauchement. Re-train → ~75-85%, oscillation. Question : lien avec TD01 Entrée 4 (XOR) ? Pourquoi aucun W ne marche ?

## 4. Bonus C — Lettres A/B/C 5x5
- 25 entrées (+1/-1) → 3 sorties. Même classe réutilisée, zéro nouveau code d'apprentissage.
- Templates fournis + générateur bruit (flip 1-2 px pour train, 4-5 px pour test robustesse).
- Exo 4 (15 min) : train 30 lettres → ~100%, visualiser les 3 lignes de W en 5x5 (templates appris), test robustesse, question surapprentissage (lien partie 3 §4).
- Choix validé le 2026-09-29 : remplace l'option Iris (clics browser : blobs + iris, puis arbitrage terminal vers A+C).

## 5. Livrables
- `td_02_mono_couche/TD02-mono-couche.md` : énoncé Obsidian (frontmatter, `[[2 - Perceptron]]`, `[[3- Données non linéairement séparables]]`, callouts).
- `td_02_mono_couche/mono_couche.ipynb` : squelette TODO + génération données + plots fournis.
- Stack : numpy + matplotlib uniquement.

## 6. Hors-scope
- Pas de softmax / gradient différentiable (c'est du MLP partie 5).
- Pas de hidden layer, pas de kernel, pas de sklearn obligatoire.
- Pas d'Iris (écarté au profit de C, plus fun et 100% numpy).

## 7. Critères de succès
- Étudiant code Rosenblatt multi-classes en <20 lignes.
- 100% sur blobs séparables, échec expliqué sur piège central.
- Bonus : W visualisé en lettres, robustesse testée.
