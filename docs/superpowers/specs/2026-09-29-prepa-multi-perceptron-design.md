# Prépa multi-perceptron (boucle puis vectorisation) — Design (2026-09-29)

## 1. Contexte et objectif
- Pont TD01 (`Perceptron` numpy, 1 neurone, Heaviside) → TD02 (`CoucheMonoCouche`, `W:(KxD)`, `argmax`).
- Blocage visé : vectorisation numpy `h = W@x+b`, pas l'`argmax`.
- Choix validé : approche B (boucle puis vectorisation), sans limite de temps courte, aider à comprendre.
- Livrable : notebook séparé uniquement, markdown dans le notebook, pas de `.md` d'énoncé à part.

## 2. Contenu du notebook
Fichier : `td_02_mono_couche/prepa_multi_perceptron.ipynb`.
- Cell markdown objectif : « 3 neurones = 3 perceptrons TD01, puis même chose en matrice ».
- Cell code fournie : `Perceptron` numpy TD01 + `gen_blobs()`, init `W=0`.
- Exo 1 boucle (`#TODO`) : `predict_liste(x, perceptrons) -> np.array([0/1,0/1,0/1])` via boucle `p.output(x)`. Test sur 3 points imposés.
- Exo 2 vectorisé (`#TODO`) : ranger 3 `w` en `W:(3xD)`, `b:(3)`, coder `h = W@x+b`, `predict_vect = (h>=0).astype(int)`, `assert` égalité boucle == matrice sur `X_train`.
- Cell constat : exhibe `[1,1,0]` et `[0,0,0]` sur points du piège → question ouverte « quelle classe choisir ? » → renvoi TD02 `argmax`.
- Tags `#EXPORT / #SKIP / #TODO` compatibles `scripts/filter_notebook.py`. Stack numpy + matplotlib uniquement.

## 3. Validation et hors-scope
- Succès : étudiant code boucle puis `W@x+b` en <20 lignes, assert égalité passe, exhibe ambiguïté, comprend besoin `argmax`.
- Test : version corrigée exécute 100 %, version étudiante générée par `filter_notebook.py`.
- Hors-scope : pas de règle `learn` multi-classes, pas d'`argmax`, pas de `plot_frontieres`, pas de lettres 5x5 (tout ça reste TD02).
