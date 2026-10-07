---
name: td-jupyter
description: Use when creating or editing a TD (travaux dirigés) Jupyter notebook for the machine learning course — writing exercices, solution code in # BEGIN/# END blocks, verification cells, or preparing notebooks for distribution with scripts/prepare_notebooks.py.
---

# TD Jupyter

## Vue d'ensemble

Un TD est un notebook Jupyter, source unique : le **corrigé** (solutions incluses), versionné dans le repo (`td_NN_<theme>/<theme>.ipynb`). Au build jupyterlite, `scripts/prepare_notebooks.py` produit la version **diffusée** (sans solutions) directement dans `dist/files/` : elle n'a pas vocation à être versionnée ailleurs.

## Interfacer avec `prepare_notebooks.py`

Le script remplace chaque bloc `# BEGIN` … `# END` par `# TODO` + `pass`, vide les outputs et remet `execution_count` à `None`.

### Aperçu local (fichier → fichier)

```bash
uv run python scripts/prepare_notebooks.py <corrige>.ipynb <apercu>.ipynb
```

Sert à prévisualiser ce que verra l'étudiant. Écrire l'aperçu hors du repo (ex. `/tmp/`) : ne jamais écraser le corrigé, ne pas versionner l'aperçu.

### CI / in-place (dossier)

```bash
uv run python scripts/prepare_notebooks.py --in-place dist/files/
```

Parcourt `**/*.ipynb` (hors `.ipynb_checkpoints`), filtre sur place et insère le bouton « Clear notebook ». Idempotent : détecte le bouton existant et ne re-traite pas.

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

## Erreurs courantes

- Marqueur `# BEGIN`/`# END` dans une cellule markdown → ignoré (le filtre ne traite que le code).
- Versionner un aperçu / une version diffusée dans le repo → seul le corrigé est versionné.
- Modifier le corrigé après la préparation → relancer le script.
- Cellule de vérification enfermée dans `# BEGIN`/`# END` → masquée à l'étudiant, il ne peut plus s'auto-tester.
