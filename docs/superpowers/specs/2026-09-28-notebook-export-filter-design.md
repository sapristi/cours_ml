# Design : filtre EXPORT / SKIP pour notebooks étudiants

Date : 2026-09-28
Statut : approuvé par utilisateur (« go »)
Contexte : repo `machine_learning` (vault Obsidian, JupyterLite), inspiré de `../cours_algo/other/post_treatment.py`.

## 1. Objectif

Ne publier aux étudiants qu'un sous-ensemble des cellules du corrigé :
- n'exporter que les cellules code contenant `# EXPORT` (substring, comme `BEGIN` dans cours_algo) ;
- si une ligne contient `#SKIP`, tronquer la cellule à cet endroit (ligne `SKIP` + tout en dessous supprimés, remplacés par `# TODO`) ;
- vider outputs / execution_count et insérer le bouton « Clear notebook » (reprise de cours_algo).

## 2. Non-objectifs

- Pas de preprocessor nbconvert ni addon JupyterLite.
- Pas de suite pytest (pas de harness dans ce vault).
- Pas de modification du format markdown existant.

## 3. Architecture

Un seul fichier `scripts/filter_notebook.py`, stdlib uniquement (`json`, `pathlib`, `argparse`).

Fonctions :
- `load_notebook(path) -> dict`
- `source_text(cell) -> str` : gère `source` en liste ou string.
- `filter_cells(nb) -> nb` : garde markdown/raw toujours ; supprime les cellules code sans `EXPORT` dans le source.
- `truncate_skip(lines: list[str]) -> list[str]` : coupe à la 1re ligne contenant `SKIP`, ajoute `# TODO\n` (ou `# TODO` + reste de la ligne ? choix : ligne fixe `# TODO`).
- `clear_outputs(cell)` : `outputs = []`, `execution_count = None`.
- `insert_clear_button(nb, rel_path)` : reprise exacte de cours_algo, avec garde anti-doublon (si 1re cellule contient déjà `button_for_indexeddb`, ne pas réinsérer).
- `treat_notebook_data(data, rel_path|None)` : enchaîne filtre + truncate + clear (+ bouton seulement en mode CI / in-place).
- CLI double-mode :
  - `python scripts/filter_notebook.py corrige.ipynb perceptron.ipynb` (génération locale, bouton non inséré — le build CI l'ajoutera) ;
  - `python scripts/filter_notebook.py --in-place dist/files/` (parcourt `**/*.ipynb`, hors `.ipynb_checkpoints`, applique filtre + clear + bouton, écrit sur place).

## 4. Sémantique précise

- `EXPORT` : test substring `"EXPORT" in source_text`, insensible à la position (`# EXPORT`, `#EXPORT`, `code # EXPORT` matchent). Ne s'applique qu'aux cellules `cell_type == "code"`.
- Cellule code sans `EXPORT` : supprimée du tableau `cells` (pas remplacée par une cellule vide).
- `SKIP` : test substring `"SKIP" in line`, ligne par ligne, premier match. Lignes au-dessus gardées telles quelles. Ligne du match et suivantes jetées. Ajout d'une ligne `# TODO` (avec `\n` final cohérent avec le style de la cellule).
- Normalisation source : travaille en liste de lignes (splitlines keepends si string), réécrit en liste de lignes (format majoritaire des notebooks actuels).
- Cellule vidée par troncature (aucune ligne au-dessus) : gardée avec `["# TODO\n"]` pour rester exécutable.
- `execution_count → None`, `outputs → []` dans tous les cas traités.

## 5. Data flow

- Local (source de vérité = `td_01_perceptron/corrige.ipynb`, jamais écrasé) :
  `uv run python scripts/filter_notebook.py td_01_perceptron/corrige.ipynb td_01_perceptron/perceptron.ipynb`
- CI (` .github/workflows/deploy.yml`) après `jupyter lite build` :
  `uv run python scripts/filter_notebook.py --in-place dist/files/` (ou `dist/` selon contenu réel, à valider au plan).
- `jupyter_lite_config.json` inchangé (`contents` pointe toujours sur le notebook étudiant).

## 6. Erreurs / edge cases

- Fichier source manquant / JSON invalide / pas de clé `cells` : message stderr + exit non-zéro (local) ; en mode `--in-place`, notebook illisible = erreur bloquante (pas de skip silencieux).
- `.ipynb_checkpoints` ignorés.
- Idempotence : re-run local écrase dest proprement ; re-run CI ne duplique pas le bouton Clear.
- Encodage : `read_text(encoding="utf-8")`, `json.dumps(..., ensure_ascii=False, indent=1)`.

## 7. Test / vérification

- Notebook jouet couvrant : code+EXPORT gardé, code sans EXPORT supprimé, markdown gardé, SKIP en milieu/fin/début, source string vs liste.
- `python -m py_compile scripts/filter_notebook.py`.
- Diff JSON avant/après sur `corrige.ipynb` copié en tmp.
- `jupyter lite build` local si rapide, sinon CI PR.

## 8. Alternatives rejetées

- B (nbconvert preprocessor) : overkill, nouvelle dépendance.
- C (2 scripts) : duplication logique SKIP/TODO.

## Self-review

- Pas de TBD/TODO ouvert (le `# TODO` généré est un artefact voulu, pas un placeholder du spec).
- Cohérence interne : filtre code-only + markdown gardé + suppression (pas vidage) validés avec l'utilisateur le 2026-09-28.
- Scope : un script + une étape CI, assez focalisé pour un seul plan d'implémentation.
- Ambiguïtés levées : substring match, `# TODO` fixe, bouton seulement en CI/in-place, source string vs liste gérée.
