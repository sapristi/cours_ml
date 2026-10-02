
Contenu pédagogique en français: MACHINE LEARNING. 
Obsidian vault, pas un projet code.

## Conventions Obsidian

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`.

# Organisation du repo
- fichiers markdown pour le cours, interprétés par obsidian
- dossier `scripts/` pour stocker des scripts utilitaires

## Export des notebooks étudiants

`scripts/filter_notebook.py` génère le notebook **étudiant** à partir d'un notebook **corrigé**.

Convention dans le corrigé : le code solution est délimité par `# BEGIN` / `# END`. À l'export, chaque bloc `# BEGIN … # END` est remplacé par `# TODO` + `pass`, les outputs sont vidés (`execution_count → None`).

### Local (fichier → fichier)

```bash
uv run python scripts/filter_notebook.py <corrige>.ipynb <etudiant>.ipynb
```

Exemple : `uv run python scripts/filter_notebook.py mlp.ipynb mlp_etudiant.ipynb` (corrigé jamais écrasé, destination régénérée).

### CI / in-place (dossier)

```bash
uv run python scripts/filter_notebook.py --in-place dist/files/
```

Parcourt `**/*.ipynb` (hors `.ipynb_checkpoints`), applique le filtre sur place et insère le bouton « Clear notebook ». Idempotent (ne duplique pas le bouton).