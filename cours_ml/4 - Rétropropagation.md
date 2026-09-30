
# 1. Notations
![[Pasted image 20260930182302.png]]

Vecteur d'entrée: $X = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{pmatrix}$

Matrice des poids de la 1ᵉ colonne de neurones: 
![[Pasted image 20260930185304.png|261]]



<!-- $W^1 = \begin{pmatrix} w_{1,1} & w_{1,2} & \dots & w_{1,n} \\  w_{2,1} & w_{2,2} & \dots & w_{2,n} \\ & &\dots \\ w_{n,1} & w_{n,2} & \dots & w_{n,n} \\ \end{pmatrix}$ -->



On appelle $Z_1 = W_1 X$, et $Y_1 = A(Z_1)$ où $A$ est la fonction d'activation. Pour chaque neurone $i$ de la 1ᵉ colonne, on a 
$$  z_i^1 =  \sum_{j=1}^n w_{i,j}\, x_j  $$

Pour la deuxième rangée, on remplace $X$ par $Y_1$, ce qui donne:
$$Z_2 = W_2 Y_1$$
$$Y_2 = A(Z_2) = A(W_2 Y_1)$$

Et ainsi de suite...

# 2. Rétro-propagation

## 2.1 Principe

Le mécanisme de rétro-propagation fonctionne de la manière suivante: 
Pour chaque couche de neurone, on va modifier les poids en considérant la contribution des poids dans la dérivée de la fonction d'erreur.

Notons $E$ l'erreur de sortie du réseau. On peut exprimer cette erreur de sortie comme une fonction des poids du réseau:
$$E = f(W_1,W_2, ..., W_n)$$
La mise à jour des poids fonctionne de la manière suivante:
$$\Delta W_i = - \eta \cdot \frac{\partial E}{\partial W_i}$$
Ainsi, il va falloir calculer les dérivées partielles de la fonction d'erreur suivant chacun des poids du réseau.

## 2.2 Calcul des coefficients

On utilisera la fonction de coût: $C(Y) = \frac{1}{2}(Y - T)^2$, et donc $C'(Y) = Y - T$. On note $\odot$ le produit terme à terme (Hadamard) entre deux vecteurs.

### 2.2.1 Calcul pour une couche de neurones
On a
$$
\begin{eqnarray}
Y &=& A(WX) \\
E &=& C(Y) = C(A(WX))
\end{eqnarray}
$$
et donc
$$\begin{eqnarray}
\frac{dE}{dW} &=& C'(Y) \odot A'(WX) \cdot X^T\\
\frac{dE}{dW} &=& (Y - T) \odot A'(WX) \cdot X^T\\
\end{eqnarray}$$
### 2.2.2 Calcul pour deux couches de neurones

On a  
$$
\begin{eqnarray}
Y_1 &=& A(W_1 X) \\
Y_2 &=& A(W_2 Y_1) \\
E &=& C(Y_2)
\end{eqnarray}
$$
Pour la dérivée en $W_2$, on est dans la même situation qu'au dessus:
$$\begin{eqnarray}
\frac{dE}{dW_2} &=& (Y_2 - T) \odot A'(W_2 Y_1) \cdot Y_1^T \\
\end{eqnarray}$$

Pour la dérivée en $W_1$, il faut pousser un peu plus loin:

$$\begin{eqnarray}
\frac{dE}{dW_1} &=& \frac{dC(Y_2)}{dW_1} = C'(Y_2)\cdot \frac{dY_2}{dW_1}\\
\end{eqnarray}$$

Or

$$\begin{eqnarray}
\frac{dY_2}{dW_1} &=& \frac{dA(W_2Y_1)}{dW_1} = A'(W_2Y_1) \cdot \frac{dW_2Y_1}{dW_1} \\
\frac{dY_2}{dW_1}  &=& A'(W_2Y_1) \cdot W_2 \cdot \frac{dY_1}{dW_1} \\
\end{eqnarray}$$

Et 

$$\begin{eqnarray}
\frac{dY_1}{dW_1} &=& \frac{dA(W_1 X)}{dW_1}\\
\frac{dY_1}{dW_1}  &=& A'(W_1 X) \cdot X^T \\
\end{eqnarray}$$
d'où


$$\begin{eqnarray}
\frac{dE}{dW_1} &=& C'(Y_2)\cdot \frac{dY_2}{dW_1}\\
\frac{dE}{dW_1} &=& (Y_2 - T) \odot A'(W_2Y_1)\cdot W_2 \cdot \frac{dY_1}{dW_1}\\
\frac{dE}{dW_1} &=& (Y_2 - T) \odot A'(W_2Y_1)\cdot W_2 \cdot A'(W_1 X) \cdot X^T\\
\end{eqnarray}$$

## 2.3 Généralisation à `n` couches


On note $Z_n = W_n Y_{n-1}$ ( avec $Y_0 = X$)

$$\begin{eqnarray}
\frac{dE}{dW_n} &=& (Y_n - T) \odot A'(Z_n) \cdot Y_{n-1}^T\\
\frac{dE}{dW_{n-1}} &=& (Y_n - T) \odot A'(Z_n) \cdot W_{n} \cdot A'(Z_{n-1}) \cdot Y_{n-2}^T\\
\frac{dE}{dW_{n-2}} &=& (Y_n - T) \odot A'(Z_n) \cdot W_{n} \cdot A'(Z_{n-1}) \cdot W_{n-1} \cdot A'(Z_{n-2}) \cdot Y_{n-3}^T\\

\frac{dE}{dW_{n-i}} &=& 
(Y_n - T) \odot A'(Z_n) \cdot W_{n}  \dots 
A'(Z_{n-i+1}) \cdot W_{n-i+1}
A'(Z_{n-i}) \cdot Y_{n-i-1}^T\\
\end{eqnarray}$$


# 3. Élan

## 3.1 Motivation

La règle de mise à jour du §2.1 ne prend en compte que le gradient **courant** : chaque poids est déplacé proportionnellement à $\frac{\partial E}{\partial W_i}$
Dans les « vallées » étroites de la surface d'erreur, le gradient oscille d'un bord à l'autre : la descente avance en **zigzag** et converge lentement. Augmenter le pas d'apprentissage ne fait qu'amplifier les oscillations, jusqu'à diverger.

## 3.2 Principe

L'**élan** (momentum) consiste à accumuler une **vitesse** $v$ et à déplacer les poids selon cette vitesse plutôt que selon le gradient brut. Le gradient ne modifie plus directement $W$, il modifie la vitesse :

$$v \leftarrow \mu\, v + \eta\,\frac{\partial E}{\partial W}, \qquad W \leftarrow W - v$$

- $\eta$ : pas d'apprentissage (le même qu'au §2.1) ;
- $\mu \in [0,1)$ : coefficient d'élan, typiquement $0.9$ ;
- $v$ : vitesse, même forme que $W$, initialisée à $0$.

> [!note] Cas particulier
> $\mu = 0$ redonne exactement la descente de gradient classique : $v = \eta\,\frac{\partial E}{\partial W}$, donc $W \leftarrow W - \eta\,\frac{\partial E}{\partial W}$.

## 3.3 Pourquoi ça accélère

La vitesse est une moyenne pondérée des gradients passés :

$$v^{(t)} = \eta \sum_{k=0}^{t-1} \mu^{k}\, \frac{\partial E}{\partial W}^{(t-k)}$$

- Les composantes du gradient qui gardent le même signe **s'accumulent** : on accélère le long de la vallée.
- Les composantes qui oscillent d'un bord à l'autre **se compensent** : le zigzag est amorti.

Image : une bille qui roule. La gravité (le gradient) l'accélère, l'inertie ($\mu$) l'empêche de changer brusquement de direction.

## 3.4 En pratique

On garde en mémoire une vitesse par paramètre (en plus des poids) et, à chaque étape, on remplace la mise à jour directe par :

$$v \leftarrow \mu\, v + \eta\,\frac{\partial E}{\partial W}, \qquad W \leftarrow W - v$$

> [!info] Ce que ça ne change pas
> L'élan ne modifie **ni** le calcul du gradient (§2) **ni** sa forme : il change seulement la façon de l'utiliser pour mettre à jour les poids. C'est un hyperparamètre de plus ($\mu$) à régler.

# 4. Convention ligne

Tout le cours utilise la convention **colonne** : $X$ est un vecteur colonne et la matrice des poids est à gauche, $Z = W X$. C'est la convention la plus simple pour les dérivations du §2.

Le notebook `mlp.ipynb`, lui, range les échantillons en **lignes** (numpy : un batch $X$ est de forme $(N, d)$). On y écrit donc $Z = X W^T$, la matrice des poids à droite. Les calculs sont identiques, seules les transposées changent de côté.

## 4.1 Passe avant

- $X$ : batch de forme $(N, d)$ (une ligne = un échantillon).
- $W_l$ : matrice $(n_{out}, n_{in})$ ; $b_l$ : biais $(n_{out},)$.
- $Y_0 = X$, puis pour chaque couche $l$ :
  $$Z_l = Y_{l-1} W_l^T + b_l, \qquad Y_l = A(Z_l)$$

  (la couche de sortie utilise $A_o$).

## 4.2 Passe arrière

$\delta_l$ est la **sensibilité** de la couche $l$ : la dérivée du coût par rapport aux pré-activations $Z_l$. Pour un échantillon, c'est un **vecteur ligne** $(1, n_{out})$, dont la composante $k$ vaut $\delta_{l,k} = \frac{\partial E}{\partial z_{l,k}}$ (de combien bouge $E$ quand on perturbe la pré-activation du neurone $k$). On note $\delta_l^{(i)}$ le delta de l'échantillon $i$.

$$\begin{eqnarray}
\delta_L &=& (Y - T) \odot A_o'(Z_L) \\
\\
\delta_l &=& (\delta_{l+1} \, W_{l+1}) \odot A'(Z_l)
\end{eqnarray}$$
Les delta à appliquer pour la backpropagation sont alors les suivants:
$$\frac{\partial E}{\partial W_l} = \frac{1}{N}\,\delta_l^T Y_{l-1}, \qquad \frac{\partial E}{\partial b_l} = \frac{1}{N}\sum_{i=1}^{N} \delta_l^{(i)}$$

La somme porte sur les échantillons $i$ uniquement (pas sur les composantes) : le résultat garde la forme d'un vecteur ligne $(1, n_{out})$, identique à $b_l$. 

## 4.3 Différence avec la colonne

| | Colonne (§2) | Ligne (§4) |
|---|---|---|
| entrée | $X$ colonne $(n, 1)$ | $X$ ligne $(1, n)$ |
| passe avant | $Z = W X$ | $Z = X W^T$ |
| récursion | $\delta_l = (W_{l+1}^T \delta_{l+1}) \odot A'(Z_l)$ | $\delta_l = (\delta_{l+1} W_{l+1}) \odot A'(Z_l)$ |
| gradient | $\frac{\partial E}{\partial W_l} = \delta_l Y_{l-1}^T$ | $\frac{\partial E}{\partial W_l} = \delta_l^T Y_{l-1}$ |

La transposée « passe » du facteur de droite ($X^T$) au facteur de gauche ($\delta^T$), et dans la récursion de $W_{l+1}^T$ (colonne) à $W_{l+1}$ (ligne).
