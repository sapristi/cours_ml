---
titre: "02 - Qu'est-ce qu'apprendre ?"
cours: "[[Entrypoint]]"
partie: 2
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Pas de prérequis ML. Python et Octave utilisés plus tard.
  Partie 2 : poser le vocabulaire et l'intuition avant les modèles.
---

> [!abstract] Objectif de cette partie
> Distinguer les formes d'apprentissage, comprendre la différence entre **mémoriser** et **généraliser**, et distinguer **classification** vs **régression**.

# 1. Les différentes formes d'apprentissage

> [!info] Idée centrale
> Apprendre = améliorer une performance sur des données **futures**, à partir de données **passées**.

## 1.1 Apprentissage supervisé

- On dispose de couples $(x, y)$ : entrée $x$, sortie désirée $y$ fournie par un « superviseur ».
- But : trouver $f$ telle que $f(x) \approx y$ sur de **nouveaux** $x$.
- Exemples :
  - $x$ = image, $y$ = « chat / chien ».
  - $x$ = surface + pièces, $y$ = prix appartement.

## 1.2 Apprentissage non supervisé

- On dispose seulement de $x$, sans étiquette $y$.
- But : découvrir une structure.
- Exemples :
  - Clustering : regrouper des clients par comportement.
  - Réduction de dimension, détection d'anomalies.

## 1.3 Apprentissage semi-supervisé

- Peu de $(x, y)$ étiquetés + beaucoup de $x$ non étiquetés.
- Cas typique : étiqueter coûte cher (avis médical, annotation image).
- Intuition : les $x$ non étiquetés renseignent sur la distribution $P(x)$.

> [!note] À retenir
> Supervisé : on apprend une correspondance $x \to y$.
> Non supervisé : on apprend une structure sur $x$.
> Semi-supervisé : un mix des deux.
> Le cours se concentre sur le **supervisé**.

# 2. Apprentissage supervisé : par cœur vs généraliser

## 2.1 Apprendre par cœur

- Exemple : table de correspondance mémorisée.
  - Erreur nulle sur les exemples vus.
  - Incapable de répondre sur un exemple jamais vu.
- En ML : un modèle trop flexible peut faire du « par cœur ».
  - Ex : polynôme de degré 50 qui passe par 51 points.

> [!example] Expérience de pensée
> Un étudiant apprend un contrôle en mémorisant les corrigés sans comprendre.
> 20/20 sur les anciens sujets, 5/20 sur un sujet inédit.
> C'est du **surapprentissage**, voir partie 7.

## 2.2 Qu'est-ce que généraliser ?

- **Généraliser** = être bon sur des données **nouvelles**, issues du même phénomène.
- Formalisation minimale (intuition, pas de preuve ici) :
  - Données d'apprentissage : $D_{train} = \{(x_i, y_i)\}_{i=1}^{n}$.
  - Erreur empirique : performance sur $D_{train}$.
  - Erreur vraie (risque) : performance moyenne sur de futures données.
  - Objectif : erreur vraie faible, pas seulement erreur empirique faible.

> [!info] Point clé
> L'erreur d'apprentissage (train) est **optimiste**.
> On ne mesure la généralisation que sur des données **non vues** pendant l'entraînement.

## 2.3 Quelles validations théoriques et pratiques ?

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

# 3. Classification vs Régression

## 3.1 Classification

- $y$ est **discret** : une classe parmi $K$.
- Binaire ($K=2$) : spam / non-spam, malade / sain.
- Multi-classe : chiffre 0-9, race de chien.
- Évaluation naturelle : **taux d'erreur** ou **accuracy**.

## 3.2 Régression

- $y$ est **continu** : une valeur numérique.
- Exemples : prix, température, taille.
- Évaluation naturelle : écart moyen, ex. erreur quadratique moyenne.

> [!example] Même $x$, deux tâches
> - $x$ = photo de pièce → classification : « cuisine / salon / chambre ».
> - $x$ = caractéristiques logement → régression : « prix en € ».

> [!danger] Ne pas confondre
> Prédire une probabilité (nombre entre 0 et 1) pour une classification reste une **classification**, même si la sortie est continue. Ce qui compte, c'est la nature de $y$ réel.

---

## À retenir pour la suite

1. Le cours = surtout **supervisé**.
2. Apprendre $\neq$ mémoriser. Objectif = **généraliser**.
3. Train $\neq$ test. On juge sur du non-vu.
4. Classification ($y$ discret) vs régression ($y$ continu).

Prochaine partie : [[03 - Classification et séparations linéaires]] (perceptron, Hebb, Rosenblatt).
