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
- $b$ règle le décalage par rapport à l'origine. Distance de la frontière à l'origine : $|b| / ||w||$.

> [!info] Correspondance variables ↔ pente ↔ translation (2D)
> $w_1 x_1 + w_2 x_2 + b = 0$, si $w_2 \neq 0$ :
> $$x_2 = -\frac{w_1}{w_2} x_1 - \frac{b}{w_2}$$
> - **Pente** $= -w_1 / w_2$ : ne dépend que du **rapport** $w_1/w_2$, donc de l'orientation de $w$.
> - **Ordonnée à l'origine** $= -b / w_2$ : translation verticale, réglée par $b$ à $w$ fixé.
> - Si $w_2 = 0$ : droite verticale $x_1 = -b / w_1$ (pente infinie).
> - Apprendre = faire bouger les deux : une correction sur $(1,0)$ ne touche que $w_1$ (redresse), sur $(0,1)$ que $w_2$ (aplatit), sur $(0,0)$ que $b$ (translate sans pivoter).

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
- Sur OU logique ($\eta=1$, 15 époques) : Hebb garde 1 erreur et $||w||$ croît sans borne, voir figure comparative ci-dessous.

## 2.2 Règle de Rosenblatt

- Même formule, mais **uniquement en cas d'erreur** :
  - Si $y_i \cdot (w^T x_i + b) \le 0$ (mal classé), alors :
  $$w \leftarrow w + \eta \cdot y_i \cdot x_i$$
  $$b \leftarrow b + \eta \cdot y_i$$
  - Sinon : on ne touche à rien.
- C'est une **correction d'erreur** : on pousse la frontière vers le bon côté. Exemple avant / après sur un seul point raté :

![[assets/03-rosenblatt-correction.png]]

> [!info] Théorème du perceptron (admis)
> Si les données sont **linéairement séparables**, Rosenblatt trouve un séparateur en un nombre fini d'étapes. Sinon, il oscille indéfiniment.
- Comparaison directe Hebb vs Rosenblatt sur OU : Rosenblatt tombe à 0 erreur et se stabilise, Hebb dérive :

![[assets/03-hebb-vs-rosenblatt.png]]

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

## 3.4 Exemple complet Rosenblatt (OU, $\eta=1$)

Données : $(0,0)\to-1$, $(0,1)\to+1$, $(1,0)\to+1$, $(1,1)\to+1$.
Poids initial : $w=(0,0)$, $b=0$ ($h=0$ partout, donc 4 erreurs au sens $y\cdot h\le 0$).

![[assets/03-rosenblatt-pasapas.png]]

Époque 1, calcul de chaque incrément ($h = w^T x + b$, erreur si $y\cdot h \le 0$) :

| $x$ | $y$ | $h$ avant | erreur ? | mise à jour | $w,b$ après |
|---|---|---|---|---|---|
| $(0,0)$ | $-1$ | $0.0$ | oui | $w+(-1)(0,0)$, $b-1$ | $(0,0), -1$ |
| $(0,1)$ | $+1$ | $-1.0$ | oui | $w+(0,1)$, $b+1$ | $(0,1), 0$ |
| $(1,0)$ | $+1$ | $0.0$ | oui ($h=0$) | $w+(1,0)$, $b+1$ | $(1,1), 1$ |
| $(1,1)$ | $+1$ | $3.0$ | non | rien | $(1,1), 1$ |

> [!example] Intra-époque 1 : voir la pente bouger
> D'après la correspondance $x_2 = -(w_1/w_2)x_1 - b/w_2$ :
> - après $(0,0)$ : $w=(0,0)$, $b=-1$ → pas de droite, translation seule ;
> - après $(0,1)$ : $w=(0,1)$, $b=0$ → $x_2=0$, pente $0$ ;
> - après $(1,0)$ : $w=(1,1)$, $b=1$ → $x_2=-x_1-1$, pente $-1$.
> Chaque exemple ne touche qu'une coordonnée de $w$ : $(0,1)$ aplatit, $(1,0)$ redresse, $(0,0)$ translate.

![[assets/03-intra-epoque1.png]]

> [!note] Cas $(0,0)$
> $x=(0,0)$ ne change jamais $w$ ($y\cdot x = 0$). Seul $b$ bouge : $b \leftarrow b-1$. C'est normal : pour isoler l'origine, il faut translater la droite, pas la pivoter.

Suite :
- Fin époque 2 : $(0,0)$ seul raté ($h=1$), $b:1\to0$, soit $w=(1,1), b=0$.
- Époques 3-4 : corrections alternées sur $(0,1)$ puis $(1,0)$, $w$ grandit à $(2,2)$.
- Fin époque 5 : $w=(2,2), b=-1$, $h = 2x_1+2x_2-1$. $0$ erreur. Stop.
- Impact : chaque correction pousse la frontière vers le point raté, sans toucher aux points justes.

## 3.5 Exemple complet Hebb (même OU, $\eta=1$)

Même init $w=(0,0), b=0$, mais mise à jour **systématique** $w\leftarrow w+yx$, $b\leftarrow b+y$.

![[assets/03-hebb-pasapas.png]]

Époque 1 :

| $x$ | $y$ | $h$ avant | juste ? | maj Hebb | $w,b$ après |
|---|---|---|---|---|---|
| $(0,0)$ | $-1$ | $0.0$ | non | $b-1$ | $(0,0), -1$ |
| $(0,1)$ | $+1$ | $-1.0$ | non | $w+(0,1)$, $b+1$ | $(0,1), 0$ |
| $(1,0)$ | $+1$ | $0.0$ | limite | $w+(1,0)$, $b+1$ | $(1,1), 1$ |
| $(1,1)$ | $+1$ | $3.0$ | oui | **quand même** $w+(1,1)$, $b+1$ | $(2,2), 2$ |

> [!danger] Différence clé
> $(1,1)$ était juste ($h=3$), Rosenblatt n'y touche pas, Hebb l'ajoute quand même. Résultat fin époque 1 : $w=(2,2), b=2$, frontière $x_1+x_2+1=0$ hors-champ, tout classé $+1$, $(0,0)$ toujours raté.

Époque 2 : même scénario, $w=(4,4), b=4$. $||w||$ double à chaque époque, erreur bloquée à 1. Hebb dérive sans converger.

Voir synthèse erreurs / norme : ![[assets/03-hebb-vs-rosenblatt.png]]

> [!example] À tester en Python / Octave
> Coder la boucle Rosenblatt en 10 lignes, tracer points + droite $w^T x + b = 0$ à chaque époque sur OU puis sur XOR. Constater : convergence vs oscillation.

---

## À retenir pour la suite

1. Perceptron = affine + seuil = **hyperplan** séparateur.
2. Hebb renforce toujours, Rosenblatt **corrige les erreurs**.
3. Si séparable : convergence garantie. Sinon : échec garanti.
4. $\eta$ règle la taille des pas, $\alpha$ (élan) les lisse.

Prochaine partie : [[04 - Données non linéairement séparables]] (pourquoi et comment sortir du linéaire).
