
Contenu pédagogique en français: MACHINE LEARNING. 
Obsidian vault, pas un projet code.

## Conventions Obsidian

**À appliquer uniquement quand un fichier markdown est édité, pas un notebook .ipynb**

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`. (optionnel)

## Standards de notation (notebooks)

On distingue soigneusement la **cible** (ce qu'il faut prédire) de la **sortie** (ce que le modèle prédit). Conventions alignées sur le cours :

| Concept | Minuscule (scalaire/vecteur) | Majuscule (matrice) |
|---|---|---|
| Entrée | `x` | `X` (un échantillon par ligne, forme (N, d)) |
| **Cible (target)** | `t` | `T` (cibles one-hot, notation mathématique) |
| **Sortie / prédiction** | `y` | `Y` (activations d'une couche, sortie du réseau) |
| Pré-activation | `z` | `Z` |
| Poids / biais | `w`, `b` | `W`, `b` |
| Activation | `a` | `A` |
| Coût / erreur rétropropagée | `E`, `δ` | — |
| Taux d'apprentissage | `r` (perceptron), `η` (multi-couche) | `lr` en code |

Règle clé : la **cible** se note toujours `t` (jamais `y`) ; `y` est réservé à la **sortie** du modèle.

# Organisation du repo
- `cours_ml/` : cours au format markdown (interprété par Obsidian). Fichiers `*.md` à la racine, figures dans `cours_ml/assets/`, scripts de génération de figures dans `cours_ml/scripts/`.
- `td/` : notebooks des travaux dirigés, nommés `NN_<theme>.ipynb` (à plat). Ce sont les **corrigés** (solutions incluses).
- `scripts/` : scripts utilitaires du repo (ex. `prepare_notebooks.py`).
- `.dist/` : sortie du build JupyterLite (généré, ignoré par git, ne pas éditer à la main).
- `.github/workflows/` : CI (déploiement JupyterLite).
- `pyproject.toml` + `uv.lock` : dépendances gérées avec `uv`.

## Environnement Python
Toujours lancer Python via `uv run` (jamais `python` directement) :

```bash
uv run python <script>.py
```

## Préparation des notebooks pour la diffusion

Les notebooks du repo sont les **corrigés** (solutions incluses). Au build jupyterlite, `scripts/prepare_notebooks.py` les prépare pour la diffusion.

### Aperçu local (fichier → fichier)

```bash
uv run python scripts/prepare_notebooks.py <corrige>.ipynb <apercu>.ipynb
```

Sert à prévisualiser ce que verra l'étudiant. Écrire l'aperçu hors du repo (ex. `/tmp/`) : ne jamais écraser le corrigé, ne pas versionner l'aperçu.

### CI / in-place (dossier)

```bash
uv run python scripts/prepare_notebooks.py --in-place .dist/files/
```

Parcourt `**/*.ipynb` (hors `.ipynb_checkpoints`), applique le filtre sur place et insère le bouton « Clear notebook ». Idempotent (ne duplique pas le bouton).
