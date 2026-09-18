---
titre: "03 - Classification et séparations linéaires"
cours: "[[Entrypoint]]"
partie: 3
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Suite de [[02 - Qu'est-ce qu'apprendre]].
  Partie 3 : premier modèle concret, le séparateur linéaire et son apprentissage.
---

> [!abstract] Objectif de cette partie
> Comprendre ce qu'est une **séparation linéaire**, ce que calcule un **perceptron**, et comment on l'entraîne avec les règles de **Hebb** et **Rosenblatt**. Introduire **pas d'apprentissage** et **élan**.

# 1. Retour sur le perceptron

## 1.1 Modèle

- Entrée $x \in \mathbb{R}^d$, poids $w \in \mathbb{R}^d$, biais $b \in \mathbb{R}$.
- Potentiel : $h = w^T x + b$.
- Sortie binaire : $f(x) = \text{sign}(h)$, soit $+1 / -1$ (ou $1 / 0$ selon convention).
- Inspiration biologique : neurone qui « tire » si la stimulation dépasse un seuil.

> [!info] Idée centrale
> Un perceptron = une **fonction affine** + un **seuil**. Toute l'intelligence est dans $w, b$.

## 1.2 Lecture géométrique

- L'équation $w^T x + b = 0$ définit une **frontière de décision** :
  - en 1D : un point,
  - en 2D : une droite,
  - en 3D : un plan,
  - en $d$D : un hyperplan.
- $w$ est le vecteur **normal** à la frontière. Il pointe vers le côté $+1$.
- $b$ règle le décalage par rapport à l'origine.

> [!example] En 2D
> $x = (x_1, x_2)$, $w = (1, -1)$, $b = 0$.
> Frontière : $x_1 - x_2 = 0$, soit la diagonale. Le point $(2, 0)$ donne $h = 2 > 0$ donc classe $+1$.

![[assets/03-geometrie-hyperplan.png]]

> [!note] À retenir
> Classer avec un modèle linéaire = couper l'espace en deux avec un hyperplan. Si les données ne s'y prêtent pas, on échouera toujours — voir [[04 - Données non linéairement séparables]].

# 2. Apprentissage sur un modèle linéaire

But : trouver $w, b$ qui classent bien les exemples $\{(x_i, y_i)\}_{i=1}^{n}$ avec $y_i \in \{+1, -1\}$.

## 2.1 Règle de Hebb

- Principe neurobiologique : « ce qui tire ensemble se lie ensemble ».
- Mise à jour sans notion d'erreur :
  $$w \leftarrow w + \eta \cdot y_i \cdot x_i$$
  avec $\eta > 0$ le pas d'apprentissage.
- On renforce la liaison dès que $x_i$ et $y_i$ sont actifs ensemble.
- Limite : on ne vérifie pas si la prédiction était fausse. Ne converge pas vers un séparateur même simple. Intérêt surtout historique / intuitif.

## 2.2 Règle de Rosenblatt

- Même formule, mais **uniquement en cas d'erreur** :
  - Si $y_i \cdot (w^T x_i + b) \le 0$ (mal classé), alors :
  $$w \leftarrow w + \eta \cdot y_i \cdot x_i$$
  $$b \leftarrow b + \eta \cdot y_i$$
  - Sinon : on ne touche à rien.
- C'est une **correction d'erreur** : on pousse la frontière vers le bon côté.

> [!info] Théorème du perceptron (admis)
> Si les données sont **linéairement séparables**, Rosenblatt trouve un séparateur en un nombre fini d'étapes. Sinon, il oscille indéfiniment.

Algorithme (essentiel) :

1. Initialiser $w = 0$, $b = 0$.
2. Répéter : parcourir les exemples, appliquer la correction sur chaque erreur.
3. Stop quand plus d'erreur ou nombre max d'itérations atteint.

## 2.3 Pas d'apprentissage $\eta$

- $\eta$ petit : apprentissage lent mais stable.
- $\eta$ grand : pas brusques, risque d'oscillations / de « sauter » par-dessus la solution.
- En pratique pour le perceptron pur : $\eta$ ne change que l'échelle de $w$, pas la frontière finale. Son rôle devient crucial pour le gradient (partie 5).
- Recette : commencer à $\eta = 0.1$ ou $1$, observer le nombre d'erreurs.

## 2.4 Élan (momentum)

- Intuition : une bille qui descend une pente prend de la vitesse et franchit les petites bosses.
- On ajoute une mémoire de la mise à jour précédente $\Delta w_{prev}$ :
  $$\Delta w = \eta \cdot y_i \cdot x_i + \alpha \cdot \Delta w_{prev}$$
  $$w \leftarrow w + \Delta w$$
  avec $\alpha \in [0, 1[$, typiquement $0.9$.
- Effet : lisse les oscillations, accélère dans les directions cohérentes.
- À ce stade : juste l'intuition. On le réutilisera pour la rétropropagation (partie 5).

> [!danger] Ne pas confondre
> Hebb = toujours renforcer. Rosenblatt = corriger **seulement si erreur**. Pas d'apprentissage $\eta$ = taille des pas. Élan $\alpha$ = mémoire des pas passés.

# 3. Exemples

## 3.1 OU logique (séparable)

- Points : $(0,0) \to -1$, $(0,1) \to +1$, $(1,0) \to +1$, $(1,1) \to +1$.
- Rosenblatt trouve par ex. $w = (1,1)$, $b = -0.5$.
- Frontière $x_1 + x_2 - 0.5 = 0$ : une droite qui isole $(0,0)$.

![[assets/03-exemple-OU.png]]

## 3.2 ET logique (séparable)

- $(0,0) \to -1$, $(0,1) \to -1$, $(1,0) \to -1$, $(1,1) \to +1$.
- Solution : $w = (1,1)$, $b = -1.5$.

![[assets/03-exemple-ET.png]]

## 3.3 XOR (non séparable, annonce partie 4)

- $(0,0) \to -1$, $(1,1) \to -1$, $(0,1) \to +1$, $(1,0) \to +1$.
- Aucune droite ne sépare les $+1$ des $-1$. Rosenblatt oscille.
- C'est la limite historique du perceptron qui a motivé les modèles multi-couches.

![[assets/03-exemple-XOR.png]]

> [!example] À tester en Python / Octave
> Coder la boucle Rosenblatt en 10 lignes, tracer points + droite $w^T x + b = 0$ à chaque époque sur OU puis sur XOR. Constater : convergence vs oscillation.

---

## À retenir pour la suite

1. Perceptron = affine + seuil = **hyperplan** séparateur.
2. Hebb renforce toujours, Rosenblatt **corrige les erreurs**.
3. Si séparable : convergence garantie. Sinon : échec garanti.
4. $\eta$ règle la taille des pas, $\alpha$ (élan) les lisse.

Prochaine partie : [[04 - Données non linéairement séparables]] (pourquoi et comment sortir du linéaire).
