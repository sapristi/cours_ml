
Contenu pédagogique en français: MACHINE LEARNING. 
Obsidian vault, pas un projet code.

## Conventions Obsidian

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`.

# Organisation du repo
- fichiers markdown pour le cours, interprétés par obsidian
- dossier `scripts/` pour stocker des scripts utilitaires

## Préparation des notebooks pour la diffusion

Les notebooks du repo sont les **corrigés** (solutions incluses). Au build jupyterlite, `scripts/prepare_notebooks.py` les prépare pour la diffusion : chaque bloc `# BEGIN … # END` est remplacé par `# TODO` + `pass`, les outputs sont vidés (`execution_count → None`).

### Aperçu local (fichier → fichier)

```bash
uv run python scripts/prepare_notebooks.py <corrige>.ipynb <apercu>.ipynb
```

Sert à prévisualiser ce que verra l'étudiant. Écrire l'aperçu hors du repo (ex. `/tmp/`) : ne jamais écraser le corrigé, ne pas versionner l'aperçu.

### CI / in-place (dossier)

```bash
uv run python scripts/prepare_notebooks.py --in-place dist/files/
```

Parcourt `**/*.ipynb` (hors `.ipynb_checkpoints`), applique le filtre sur place et insère le bouton « Clear notebook ». Idempotent (ne duplique pas le bouton).