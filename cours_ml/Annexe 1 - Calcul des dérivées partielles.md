# 1. Contexte

Nous voulons calculer les dérivées partielles de la fonction d'erreur, afin de pouvoir effectuer une descente de gradient.

Afin de simplifier les calculs, supposons que
- l'entrée $x$ est de dimension $1$
- chaque couche $l$ a un unique neurone, de poids $w_l$
- la fonction d'activation (partagée par toutes les couches) est notée $a$, et $a'$ sa dérivée.
- on ne considère pas le biais

Ainsi, tout se passe en dimension 1, et l'on évite les considérations matricielles.

## 1.1 Rappels et notations

### 1.1.1 Sortie de chaque couche
Pour chaque couche $l$ du réseau, on a
$$\begin{eqnarray}
z_{l} &=& y_{l-1} \cdot w_l\\
y_{l} &=& a(z_{l})\\
\end{eqnarray}$$
(avec $y_0 = x$).

### 1.1.2 Fonction d'erreur

Soient
- $x$ un échantillon d'entrée
- $t$ la valeur attendue
- $y$ la valeur de sortie

On définit la fonction d'erreur $E$ comme:
$$E= \frac{1}{2}(y-t)^2$$
Nous voulons calculer les dérivées partielles de $E$ par rapport aux poids, pour chacun des poids $w_l$: $$\frac{\delta E}{\delta w_l}$$
On définit la fonction $c(y) = \frac{1}{2}(y-t)^2$; on a $c'(y) = (y-t)$
# 2. Calcul des dérivées partielles

## 2.1 Calcul pour un réseau à une couche
On a
$$
\begin{eqnarray}
y &=& a(wx) \\
E &=& c(y) = c(a(wx))
\end{eqnarray}
$$
et donc
$$\begin{eqnarray}
\frac{\delta E}{\delta w} &=& \frac{\delta \ c(y)}{\delta w}
= \frac{\delta \ c(y)}{\delta y} \cdot \frac{\delta y}{\delta w}\\
\frac{\delta E}{\delta w} &=& c'(y) \cdot \frac{\delta \ a(wx)}{\delta w} \\
\frac{\delta E}{\delta w} &=& (y - t) \cdot a'(wx) \cdot x
\end{eqnarray}$$
## 2.2 Calcul pour un réseau à deux couches

On a  
$$
\begin{eqnarray}
y_1 &=& a(w_1 x) \\
y_2 &=& a(w_2 y_1) \\
E &=& c(y_2)
\end{eqnarray}
$$
### 2.2.1 Dérivée en $w_2$

Pour la dérivée en $w_2$, on est dans la même situation qu'au dessus, en remplaçant $x$ par $y_1$:
$$\begin{eqnarray}
\frac{\delta E}{\delta w_2} &=& (y_2 - t) \cdot a'(w_2 y_1) \cdot y_1 \\
\end{eqnarray}$$
### 2.2.2 Dérivée en $w_1$
Pour la dérivée en $w_1$, il faut pousser un peu plus loin:

$$\begin{eqnarray}
\frac{\delta E}{\delta w_1} &=& \frac{\delta\ c(y_2)}{\delta\ w_1} = c'(y_2)\cdot \frac{\delta y_2}{\delta w_1}\\
\frac{\delta E}{\delta w_1} &=& (y_2 - t) \cdot \frac{\delta y_2}{\delta w_1} \\
\end{eqnarray}$$

Or
$$\begin{eqnarray}
\frac{\delta y_2}{\delta w_1} &=& \frac{\delta \ a(w_2y_1)}{\delta w_1} = a'(w_2y_1) \cdot \frac{\delta \ w_2y_1}{\delta w_1} \\
\frac{\delta y_2}{\delta w_1}  &=& a'(w_2y_1) \cdot w_2 \cdot \frac{\delta y_1}{\delta w_1} \\
\end{eqnarray}$$

Et 

$$\begin{eqnarray}
\frac{\delta y_1}{\delta w_1} &=& \frac{\delta \ a(w_1 x)}{\delta w_1}\\
\frac{\delta y_1}{\delta w_1}  &=& a'(w_1 x) \cdot x \\
\end{eqnarray}$$
d'où


$$\begin{eqnarray}
\frac{\delta E}{\delta w_1} &=& (y_2 - t)\cdot \frac{\delta y_2}{\delta w_1}\\
\frac{\delta E}{\delta w_1} &=& (y_2 - t) \cdot a'(w_2y_1)\cdot w_2 \cdot \frac{\delta y_1}{\delta w_1}\\
\frac{\delta E}{\delta w_1} &=& (y_2 - t) \cdot a'(w_2y_1)\cdot w_2 \cdot a'(w_1 x) \cdot x\\
\end{eqnarray}$$
### 2.2.3 Conclusion
Nous avons donc:
$$\begin{eqnarray}
\frac{\delta E}{\delta w_2} &=& (y_2 - t) \cdot a'(w_2 y_1) \cdot y_1 \\
\frac{\delta E}{\delta w_1} &=& (y_2 - t) \cdot a'(w_2y_1)\cdot w_2 \cdot a'(w_1 x) \cdot x\\
\end{eqnarray}$$
Nous pouvons remarquer un terme commun $(y_2 - t) \cdot a'(w_2 y_1)$ entre ceux deux expressions. 

# 3. Formule générale pour un réseau à $L$ couches

En continuant les calculs dans le cas d'un réseau à $L$ couches, on obtiendrait

$$\begin{eqnarray}
\frac{\delta E}{\delta w_L} &=& (y_L - t) \cdot a'(z_L) \cdot y_{L-1}\\
\frac{\delta E}{\delta w_{L-1}} &=& (y_L - t) \cdot a'(z_L) \cdot w_{L} \cdot a'(z_{L-1}) \cdot y_{L-2}\\
\frac{\delta E}{\delta w_{L-2}} &=& (y_L - t) \cdot a'(z_n) \cdot w_{L} \cdot a'(z_{L-1}) \cdot w_{L-1} \cdot a'(z_{L-2}) \cdot y_{L-3}\\
\\
\dots\\
\\
\frac{\delta E}{\delta w_{L-i}} &=& 
(y_L - t) \cdot a'(z_L) \cdot w_{L}  \dots 
a'(z_{L-i+1}) \cdot w_{L-i+1}
a'(z_{L-i}) \cdot y_{L-i-1}\\
\end{eqnarray}$$

Ainsi, en posant
$$\begin{eqnarray}
\delta_L &=& (y_L - t)\cdot a'(z_L)\\
\delta_{l-1} &=& \delta_l \cdot w_l \cdot  a'(z_{l-1}) 
\end{eqnarray}$$
on peut calculer chacune des dérivées partielles avec 
$$\frac{\delta E}{\delta w_l} = \delta_l \cdot y_{l-1}$$