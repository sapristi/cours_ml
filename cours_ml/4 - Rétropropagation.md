
# 1. Notations
![[Pasted image 20260930145724.png]]
Vecteur d'entrée: $X = \begin{pmatrix} x_1 & x_2 & \dots & x_n   \end{pmatrix}$

Matrice des poids de la 1ᵉ colonne de neurones: 
![[Pasted image 20260930152903.png|281]]


<!-- $W^1 = \begin{pmatrix} w_{1,1} & w_{1,2} & \dots & w_{1,n} \\  w_{2,1} & w_{2,2} & \dots & w_{2,n} \\ & &\dots \\ w_{n,1} & w_{n,2} & \dots & w_{n,n} \\ \end{pmatrix}$ -->


On appelle $Z_1 = X W_1$, et $Y_1 = A(Z_1)$ où $A$ est la fonction d'activation. Pour chaque neurone $i$ de la 1ᵉ colonne, on a 
$$  z_i^1 =  \sum_{j=1}^1 x_j w_{j,i}  $$

Pour la deuxième rangée, on remplace $X$ par $Y_1$, ce qui donne:
$$Z^2 = Y^1 W^2$$
$$Y_2 = A(Z_2) = A(Y_1 W_2)$$

Et ainsi de suite...

# 2. Rétro-propagation

Le mécanisme de rétro-propagation fonctionne de la manière suivante: 
Pour chaque couche de neurone, on va modifier les poids en considérant la contribution des poids dans la dérivée de la fonction d'erreur.

## 2.1 Principe

## 2.2 Calcul des coefficients

On utilisera la fonction de coût: $C(Y) = \frac{1}{2}(Y - T)^2$, et donc $C'(Y) = Y - T$

### 2.2.1 Calcul pour une couche de neurones
On a
$$
\begin{eqnarray}
Y &=& A(XW) \\
E &=& C(Y) = C(A(XW))
\end{eqnarray}
$$
et donc
$$\begin{eqnarray}
\frac{dE}{dW} &=& C'(Y)\cdot A'(XW) \cdot X\\
\frac{dE}{dW} &=& (Y - T)\cdot A'(XW) \cdot X\\
\end{eqnarray}$$
### 2.2.2 Calcul pour deux couches de neurones

On a  
$$
\begin{eqnarray}
Y_1 &=& A(X  W_1) \\
Y_2 &=& A(Y_1 W_2) \\
E &=& C(Y_2)
\end{eqnarray}
$$
Pour la dérivée en $W_2$, on est dans la même situation qu'au dessus:
$$\begin{eqnarray}
\frac{dE}{dW_2} &=& (Y_2 - T) \cdot A'(Y_1 W_2) \cdot Y_1 \\
\end{eqnarray}$$

Pour la dérivée en $W_1$, il faut pousser un peu plus loin:

$$\begin{eqnarray}
\frac{dE}{dW_1} &=& \frac{dC(Y_2)}{dW_1} = C'(Y_2)\cdot \frac{dY_2}{dW_1}\\
\end{eqnarray}$$

Or

$$\begin{eqnarray}
\frac{dY_2}{dW_1} &=& \frac{dA(Y_1W_2)}{dW_1} = A'(Y_1W_2) \cdot \frac{dY_1W_2}{dW_1} \\
\frac{dY_2}{dW_1}  &=& A'(Y_1W_2) \cdot W_2 \cdot \frac{dY_1}{dW_1} \\
\end{eqnarray}$$

Et 

$$\begin{eqnarray}
\frac{dY_1}{dW_1} &=& \frac{dA(X  W_1)}{dW_1}\\
\frac{dY_1}{dW_1}  &=& A'(XW_1) \cdot X \\
\end{eqnarray}$$
d'où


$$\begin{eqnarray}
\frac{dE}{dW_1} &=& C'(Y_2)\cdot \frac{dY_2}{dW_1}\\
\frac{dE}{dW_1} &=& (Y_2 - T)\cdot A'(Y_1W_2)\cdot W_2 \cdot \frac{dY_1}{dW_1}\\
\frac{dE}{dW_1} &=& (Y_2 - T)\cdot A'(Y_1W_2)\cdot W_2 \cdot A'(XW_1) \cdot X\\
\end{eqnarray}$$

## 2.3 Généralisation à `n` couches


On note $Z_n = Y_{n-1}W_n$ ( avec $Y_0 = X$)

$$\begin{eqnarray}
\frac{dE}{dW_n} &=& (Y_n - T)\cdot A'(Z_n) \cdot Y_{n-1}\\
\frac{dE}{dW_{n-1}} &=& (Y_n - T)\cdot A'(Z_n) \cdot W_{n} \cdot A'(Z_{n-1}) \cdot Y_{n-2}\\
\frac{dE}{dW_{n-2}} &=& (Y_n - T)\cdot A'(Z_n) \cdot W_{n} \cdot A'(Z_{n-1}) \cdot W_{n-1} \cdot A'(Z_{n-2}) \cdot Y_{n-3}\\

\frac{dE}{dW_{n-i}} &=& 
(Y_n - T)\cdot A'(Z_n) \cdot W_{n}  \dots 
A'(Z_{n-i+1}) \cdot W_{n-i+1}
A'(Z_{n-i}) \cdot Y_{n-i-1}\\
\end{eqnarray}$$

