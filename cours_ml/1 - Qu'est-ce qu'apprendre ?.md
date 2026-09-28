---
titre: 02 - Qu'est-ce qu'apprendre ?
cours: "[[Entrypoint]]"
partie: 1
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Pas de prérequis ML. Python et Octave utilisés plus tard.
  Partie 2 : poser le vocabulaire et l'intuition avant les modèles.
---

> [!abstract] Objectif de cette partie
> Distinguer les formes d'apprentissage, comprendre la différence entre **mémoriser** et **généraliser**, et distinguer **classification** vs **régression**.

---
# 1. Introduction - Apprentissage automatique

## 1.1 L'apprentissage automatique: qu'est ce que c'est ?


> [!info] Idée centrale
> Apprendre = exploiter des données (passées), pour construire un modèle réutilisable (sur de futures données)


![[Pasted image 20260928144728.png]]


- On dispose d'un *modèle* (algorithme ou réseau de neurone)
- On dispose de *données d'entrainement*
- On va *entraîner* le modèle sur les données d'entraînement
- On obtient un *modèle "entraîné"*, qui va être capable d'exprimer une sortie sur des données d'entrée "nouvelles".

![[Pasted image 20260928173641.png|301]]

## 1.2 Applications


- reconnaissance de caractères / d'images
- reconnaissance de spam
- détection de fraude
- traduction
- prédiction (de vente, de croissance, etc)
- météo

## 1.3 Quel type de données ?

**En entrée:**
- texte
- valeurs numériques

**En sortie:**
- valeurs numériques / valeur quantitative→ **régression**
- catégories / valeur qualitative→ **classification**
- texte

> [!info] Dans tous les cas, on peut ramener les différents types de données à des valeurs numériques.

> [!question] Classifier les exemples précédents entre régression et classification.

# 2. Deux formes d'apprentissage automatique
## 2.1 Apprentissage supervisé

![[Pasted image 20260928183350.png]]


On entraîne le modèle sur des données dont on sait déjà quelle est la sortie attendue.

## 2.2 Apprentissage non supervisé

![[Pasted image 20260928183440.png]]

On entraîne le modèle sur des données pour lesquelles on ne sait pas quelle est la sortie attendue; on espère que l'entraînement va permettre de "découvrir" une structure dans les données d'entrée.

> [!note]
> - Globalement moins performant que l'apprentissage supervisé
> - Ne nécessite pas de données labellisées (qui coûtent cher)

# 3. Apprentissage supervisé : par cœur vs généraliser

## 3.1 Apprendre par cœur

- Exemple : table de correspondance mémorisée.
  - Erreur nulle sur les exemples vus.
  - Incapable de répondre sur un exemple jamais vu.
- En ML : un modèle trop flexible peut faire du « par cœur ».
  - Ex : polynôme de degré 50 qui passe par 51 points.

> [!example] Exemple
> Un étudiant apprend un contrôle en mémorisant les corrigés sans comprendre.


## 3.2 Qu'est-ce que généraliser ?

- **Généraliser** = être bon sur des données **nouvelles**, issues du même phénomène.
- Formalisation minimale :
  - Données d'apprentissage : $D_{train} = \{(x_i, y_i)\}_{i=1}^{n}$.
  - Erreur empirique : performance sur $D_{train}$.
  - Erreur vraie (risque) : performance moyenne sur de futures données.
  - Objectif : erreur vraie faible, pas seulement erreur empirique faible.

> [!info] Point clé
> On ne mesure la généralisation que sur des données **non vues** pendant l'entraînement.


TODO:
- divers exemples d'interpolation, à partir d'un même ensemble de points:
	- linéaire, approximative.
	- diverses solutions exactes, mais d'allure différente.
![[Pasted image 20260928145826.png|398]]

## 3.3 Quelles validations théoriques et pratiques ?

Essentiel à ce stade (détaillé en parties 4 et 7) :

1. **Séparation train / test**
   - On réserve une partie des données pour tester.
   - C'est la mesure empirique de la généralisation.

2. **Idée théorique à admettre**
   - Si le modèle est simple par rapport au nombre d'exemples, erreur train $\approx$ erreur vraie.
   - Si le modèle est trop complexe, écart possible très grand.
   - D'où le dilemme : modèle trop simple = sous-apprentissage, trop complexe = surapprentissage.

3. **Conséquence pratique**
   - Plus de données + modèle de complexité contrôlée = meilleure généralisation.
   - Ne jamais choisir un modèle uniquement sur l'erreur train.

> [!note] Vocabulaire à fixer
> - **Hypothèse / modèle** : la fonction $f$ choisie dans une famille.
> - **Erreur empirique / train** : sur données vues.
> - **Erreur test / généralisation** : sur données nouvelles.



---

# 4. Réseaux de neurone

## À retenir pour la suite

1. Le cours = surtout **supervisé**.
2. Apprendre $\neq$ mémoriser. Objectif = **généraliser**.
3. Train $\neq$ test. On juge sur du non-vu.
4. Deux types d'apprentissage: Classification ($y$ discret) vs régression ($y$ continu).

