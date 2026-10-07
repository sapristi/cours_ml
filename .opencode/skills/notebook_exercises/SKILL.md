---
name: notebook_exercises
description: Use when creating or editing a Jupyter notebook containing exercices (typically TD "Travaux dirigés"n otebook), or preparing notebooks for distribution with scripts/prepare_notebooks.py.
---

# TD Jupyter

## Vue d'ensemble

Un TD est un notebook Jupyter, source unique : le **corrigé** (solutions incluses), versionné dans le repo (`td/NN_<theme>.ipynb`). Au build jupyterlite, `scripts/prepare_notebooks.py` produit la version **diffusée** (sans solutions) directement dans `.dist/files/` : elle n'a pas vocation à être versionnée ailleurs.

## Interfacer avec `prepare_notebooks.py`

Le script remplace chaque bloc `# BEGIN` … `# END` par `# TODO` + `pass`, vide les outputs et remet `execution_count` à `None`. Les commentaires écrits juste après `# BEGIN` deviennent le corps du TODO (voir « Corps du TODO »).

### Aperçu local (fichier → fichier)

```bash
uv run python scripts/prepare_notebooks.py <corrige>.ipynb <apercu>.ipynb
```

Sert à prévisualiser ce que verra l'étudiant. Écrire l'aperçu hors du repo (ex. `/tmp/`) : ne jamais écraser le corrigé, ne pas versionner l'aperçu.

## Écrire un exercice

Chaque exercice est énoncé dans une **cellule markdown**, sous la forme d'un blockquote numéroté :

```markdown
> **Exercice 7** — Complétez `forward` (renvoie X, Z1, Y1, Z2, Y2).
```

- Numérotation **séquentielle** sur tout le notebook (Exercice 1, 2, 3…), lettres pour les sous-étapes (`Exercice 7a`, `7b`, …).
- L'énoncé nomme précisément ce qu'il faut compléter (fonction/méthode), puis la tâche.

## Cellule de vérification

**Chaque exercice doit être suivi d'une cellule de code qui teste que le code est correct.** Elle vérifie par `assert` et imprime un message `… OK` en cas de succès.

```python
def check_forward(model, X, tol=1e-9):
    ...
    assert np.allclose(Z1, Z1r, atol=tol), "Z1 incorrect"
    print("forward check — OK")

m = PerceptronCache(2, 3, 1, seed=1)
X = np.random.default_rng(0).normal(size=(4, 2))
check_forward(m, X)
```

- La cellule de vérification **ne doit pas** être dans un bloc `# BEGIN`/`# END` : elle reste visible dans la version diffusée pour l'auto-évaluation.
- Elle teste ce que l'étudiant vient de coder : comparaison à une implémentation naïve, gradient numérique, `assert` sur une valeur attendue, etc.

## Règles BEGIN/END

- `# BEGIN` et `# END` sur leur **propre ligne**, dans des cellules de code uniquement.
- Tout le code solution est entre les deux ; la ligne `# BEGIN` devient `# TODO` + `pass` à la préparation.
- Le code « pédagogique » non solution (imports, fonctions de visualisation, fonctions de test) reste **hors** des blocs.

### Corps du TODO

Les commentaires écrits **immédiatement après** `# BEGIN` (avant la première ligne de code solution) deviennent le corps du `# TODO` dans la version diffusée :

- `# <code>` → dé-commenté, devient du **code** (ex. `# raise NotImplementedError` → `raise NotImplementedError`).
- `## <texte>` → garde un seul `#`, reste un **indice** (commentaire).

```python
def forward(self, X):
    # BEGIN
    # raise NotImplementedError
    ## Indice : Z1 = Y0 @ W1.T + b1
    Y0 = X
    ...
    # END
```

donne, une fois préparé :

```python
def forward(self, X):
    # TODO
    raise NotImplementedError
    # Indice : Z1 = Y0 @ W1.T + b1
```

- Sans commentaire après `# BEGIN`, le script émet `# TODO` + `pass` comme avant.
- Si seul des indices (`##`) sont présents, un `pass` est ajouté pour éviter un corps vide.
- ⚠️ Tout commentaire en **première ligne** d'une solution sera dé-commenté : pour un commentaire ordinaire, écris-le avant `# BEGIN` ou utilise `##`.

## Erreurs courantes

- Marqueur `# BEGIN`/`# END` dans une cellule markdown → ignoré (le filtre ne traite que le code).
- Versionner un aperçu / une version diffusée dans le repo → seul le corrigé est versionné.
- Modifier le corrigé après la préparation → relancer le script.
- Cellule de vérification enfermée dans `# BEGIN`/`# END` → masquée à l'étudiant, il ne peut plus s'auto-tester.
