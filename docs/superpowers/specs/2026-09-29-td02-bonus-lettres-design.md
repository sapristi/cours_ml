# Design — TD02 bonus lettres didactique + visualisations explicites

Date: 2026-09-29
Statut: validé option A, implémenté.

## Contexte
- Bonus lettres passif : tout fourni, élève Run seulement, aucun TODO.
- `plot_frontieres` illisible : fond `argmax` + pointillés `h_k=0` superposés sans légende, confusion frontière vs zéro.
- `W` 5x5 en `imshow` sans tâche d'interprétation.

## Objectifs (validés)
1. Généralisation 25D : même modèle OK quand séparable, contraste piège central.
2. Interprétabilité W : chaque ligne = prototype A/B/C.
3. Activité élève : courbe robustesse `n_flip` 0..8.
4. Temps flexible (plus de limite 15 min).

## Décisions
- `plot_frontieres` : on **garde + explique** (choix utilisateur). Ajout légende `h_k=0 (indicatif, pas frontière)`, markdown Ex 2-3 : trouver un pointillé traversant une zone uniforme.
- Bonus en 3 actes :
  - Acte 0 : coder `enc` + `gen_lettres` (SKIP → TODO étudiant).
  - Ex4 : `show_lettre(x)` = image 5x5 + barres `h0,h1,h2`, prédire à la main via `argmax`.
  - Ex5 : templates vs W côte à côte (2x3), associer + justifier pixels discriminants B vs C, expliquer flou (moyenne + Rosenblatt).
  - Ex6 : boucle `n_flip` 0..8 à coder, plot accuracy. Attendu : 100% flip 0-2, ~70% flip 5, ~60% flip 8.
  - Ex7 synthèse : dimension vs séparabilité linéaire, prépare TD03.
- Filtre étudiant : 4 TODO (classe, enc/gen, visu W, courbe). Markdowns questions conservés.
- Énoncé Obsidian TD02 : §2 clarifié fond vs pointillés, §3 découpé Ex4-7.

## Fichiers
- `td_02_mono_couche/mono_couche_corrige.ipynb` (30 cellules, source vérité, exécuté 0 erreur).
- `td_02_mono_couche/mono_couche.ipynb` (régénéré via `filter_notebook.py`, 4 TODO).
- `td_02_mono_couche/TD02-mono-couche.md` (Ex1-7).

## Vérification
- `.venv/bin/python` smoke : train 100%, test flip5 73.3%, courbe 100→60%.
- `nbconvert --execute` corrige : 0 erreur.
- `filter_notebook.py` : TODO count 4.

## Non-scope
- Pas de frontières paires `h_i==h_j` tracées (fond suffit).
- Pas d'attaque adversariale ciblée (option C écartée).
